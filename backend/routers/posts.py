from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Tạo bài confession mới (cần đăng nhập)"""
    new_post = models.Post(
        author_id=current_user.id,
        content=post_data.content
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Lấy danh sách posts (có phân trang, mới nhất trước)"""
    posts = (
        db.query(models.Post)
        .options(joinedload(models.Post.author))
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 post (kèm thông tin author)"""
    post = (
        db.query(models.Post)
        .options(joinedload(models.Post.author))
        .filter(models.Post.id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài post")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Xóa bài post (chỉ tác giả mới được xóa)"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài post")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa bài post này")

    db.delete(post)
    db.commit()
