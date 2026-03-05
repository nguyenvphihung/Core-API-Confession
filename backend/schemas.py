from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ========================
# User Schemas
# ========================
class UserCreate(BaseModel):
    student_id: str
    password: str
    display_name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    student_id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ========================
# Auth Schemas
# ========================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    student_id: str
    password: str


# ========================
# Post Schemas
# ========================
class PostCreate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: int
    author_id: int
    content: str
    created_at: datetime
    author: Optional[UserResponse] = None

    class Config:
        from_attributes = True


# ========================
# Comment Schemas
# ========================
class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None

class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    parent_id: Optional[int] = None
    content: str
    created_at: datetime
    user: Optional[UserResponse] = None
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


# ========================
# Interaction Schemas
# ========================
class InteractionCreate(BaseModel):
    interaction_type: str = "like"

class InteractionResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    interaction_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ========================
# Comment Interaction Schemas
# ========================
class CommentInteractionCreate(BaseModel):
    interaction_type: str = "like"

class CommentInteractionResponse(BaseModel):
    id: int
    user_id: int
    comment_id: int
    interaction_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ========================
# Post Media Schemas
# ========================
class PostMediaResponse(BaseModel):
    id: int
    post_id: int
    file_url: str
    file_name: str
    file_size: int
    media_type: str
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True
