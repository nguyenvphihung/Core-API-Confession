from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(tags=["Comments"])


@router.post("/api/posts/{post_id}/comments", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, comment_data: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Thêm comment vào post (hoặc reply nếu có parent_id)"""
    # Kiểm tra post tồn tại
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài post")

    # Nếu là reply, kiểm tra parent comment tồn tại và cùng post
    if comment_data.parent_id:
        parent = db.query(models.Comment).filter(models.Comment.id == comment_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Không tìm thấy comment cha")
        if parent.post_id != post_id:
            raise HTTPException(status_code=400, detail="Comment cha không thuộc bài post này")

    new_comment = models.Comment(
        user_id=current_user.id,
        post_id=post_id,
        parent_id=comment_data.parent_id,
        content=comment_data.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/api/posts/{post_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách comments của post (chỉ comment gốc, kèm replies nested)"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài post")

    comments = (
        db.query(models.Comment)
        .options(joinedload(models.Comment.user))
        .filter(models.Comment.post_id == post_id, models.Comment.parent_id == None)
        .order_by(models.Comment.created_at.asc())
        .all()
    )
    return comments


@router.delete("/api/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Xóa comment (chỉ người viết mới được xóa)"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Không tìm thấy comment")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa comment này")

    db.delete(comment)
    db.commit()
