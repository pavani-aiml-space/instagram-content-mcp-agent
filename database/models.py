"""
Database Models (SQLAlchemy ORM)
Defines our 3 essential tables: User, ContentRequest, Post
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from database.connection import Base


class User(Base):
    """
    User Model - Stores Instagram influencer accounts
    
    Why needed: Identify who's making requests and authenticate with Instagram API
    """
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    instagram_user_id = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    access_token = Column(String, nullable=False)  # Instagram API token
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship: One user can have many content requests
    content_requests = relationship("ContentRequest", back_populates="user")


class ContentRequest(Base):
    """
    Content Request Model - Tracks every content generation request
    
    Why needed: Track all requests and their status
    """
    __tablename__ = "content_requests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)  # "LLM", "Ragi Dosa Recipe"
    format = Column(String, nullable=False)  # "post", "story", "reel"
    posting_time = Column(String, nullable=True)  # "19:00" or null
    status = Column(String, nullable=False, default="pending")  # "pending", "processing", "completed", "failed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="content_requests")
    post = relationship("Post", back_populates="content_request", uselist=False)


class Post(Base):
    """
    Post Model - Stores successfully posted Instagram content
    
    Why needed: Track what was posted and link back to original request
    """
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String, ForeignKey("content_requests.id"), nullable=False, unique=True)
    instagram_post_id = Column(String, nullable=False)  # Instagram's post ID
    format = Column(String, nullable=False)  # "post", "story", "reel"
    image_url = Column(String, nullable=False)  # Posted image URL
    caption = Column(String, nullable=False)  # Posted caption text
    hashtags = Column(ARRAY(String), nullable=False)  # Array of hashtags
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    content_request = relationship("ContentRequest", back_populates="post")

