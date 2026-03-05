from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author")
    interactions = relationship("Interaction", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("User", back_populates="posts")
    interactions = relationship("Interaction", back_populates="post")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    interaction_type = Column(String(50), default="like")
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", "interaction_type", name="uq_user_post_interaction"),
    )

    user = relationship("User", back_populates="interactions")
    post = relationship("Post", back_populates="interactions")