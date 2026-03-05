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

    # Relationships
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="user")
    interactions = relationship("Interaction", back_populates="user")
    comment_interactions = relationship("CommentInteraction", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", order_by="Comment.created_at")
    media = relationship("PostMedia", back_populates="post")
    interactions = relationship("Interaction", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # NULL = comment gốc
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side="Comment.id", backref="replies")
    comment_interactions = relationship("CommentInteraction", back_populates="comment")


class PostMedia(Base):
    __tablename__ = "post_media"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    file_url = Column(String(500), nullable=False)        # Đường dẫn file trên server
    file_name = Column(String(255), nullable=False)       # Tên file gốc khi upload
    file_size = Column(Integer, nullable=False)            # Kích thước file (bytes)
    media_type = Column(String(20), nullable=False)       # 'image' hoặc 'audio'
    mime_type = Column(String(100), nullable=False)        # VD: 'image/jpeg', 'audio/mpeg'
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    post = relationship("Post", back_populates="media")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    interaction_type = Column(String(50), default="like")  # like, view...
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", "interaction_type", name="uq_user_post_interaction"),
    )

    # Relationships
    user = relationship("User", back_populates="interactions")
    post = relationship("Post", back_populates="interactions")


class CommentInteraction(Base):
    __tablename__ = "comment_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    interaction_type = Column(String(50), default="like")  # like, dislike...
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "comment_id", "interaction_type", name="uq_user_comment_interaction"),
    )

    # Relationships
    user = relationship("User", back_populates="comment_interactions")
    comment = relationship("Comment", back_populates="comment_interactions")