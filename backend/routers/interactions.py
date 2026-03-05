from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models
import schemas

router = APIRouter(tags=["Interactions"])


# ========================
# Post Interactions
# ========================
@router.post("/api/posts/{post_id}/like", response_model=schemas.InteractionResponse, status_code=status.HTTP_201_CREATED)
def like_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Like bài post (cần đăng nhập)"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài post")

    # Kiểm tra đã like chưa
    existing = db.query(models.Interaction).filter(
        models.Interaction.user_id == current_user.id,
        models.Interaction.post_id == post_id,
        models.Interaction.interaction_type == "like"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bạn đã like bài post này rồi")

    interaction = models.Interaction(
        user_id=current_user.id,
        post_id=post_id,
        interaction_type="like"
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/api/posts/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Unlike bài post (cần đăng nhập)"""
    interaction = db.query(models.Interaction).filter(
        models.Interaction.user_id == current_user.id,
        models.Interaction.post_id == post_id,
        models.Interaction.interaction_type == "like"
    ).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Bạn chưa like bài post này")

    db.delete(interaction)
    db.commit()


# ========================
# Comment Interactions
# ========================
@router.post("/api/comments/{comment_id}/like", response_model=schemas.CommentInteractionResponse, status_code=status.HTTP_201_CREATED)
def like_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Like comment (cần đăng nhập)"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Không tìm thấy comment")

    existing = db.query(models.CommentInteraction).filter(
        models.CommentInteraction.user_id == current_user.id,
        models.CommentInteraction.comment_id == comment_id,
        models.CommentInteraction.interaction_type == "like"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bạn đã like comment này rồi")

    interaction = models.CommentInteraction(
        user_id=current_user.id,
        comment_id=comment_id,
        interaction_type="like"
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/api/comments/{comment_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Unlike comment (cần đăng nhập)"""
    interaction = db.query(models.CommentInteraction).filter(
        models.CommentInteraction.user_id == current_user.id,
        models.CommentInteraction.comment_id == comment_id,
        models.CommentInteraction.interaction_type == "like"
    ).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Bạn chưa like comment này")

    db.delete(interaction)
    db.commit()
