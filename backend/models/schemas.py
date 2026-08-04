"""
Pydantic Models for Request/Response Validation

These models define:
- What data we accept from frontend (Request models)
- What data we send back (Response models)

Pydantic automatically validates data matches these models.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================================================
# REQUEST MODELS (What frontend sends to us)
# ============================================================================

class ContentGenerateRequest(BaseModel):
    """
    Request model for content generation
    
    This is what the frontend sends when user wants to generate content.
    """
    topic: str = Field(
        ...,
        description="Main topic/headline (e.g., 'Embeddings', 'LLM', 'RAG')",
        example="Embeddings"
    )
    topic_details: Optional[str] = Field(
        None,
        description="Additional details, context, or specific points you want to cover about the topic",
        example="Explain how embeddings represent words as vectors in high-dimensional space, show similarity between related concepts, and enable semantic search."
    )
    format: Optional[str] = Field(
        None,
        description="Content format: 'post', 'story', or 'reel'. If not provided, system will decide.",
        example="reel"
    )
    posting_time: Optional[str] = Field(
        None,
        description="When to post: 'now', 'best', or specific time like '19:00'. If not provided, uses best time.",
        example="19:00"
    )
    user_id: str = Field(
        ...,
        description="Instagram user ID making the request",
        example="user_123"
    )
    dry_run: Optional[bool] = Field(
        False,
        description="If true, the Instagram Poster tool validates and logs the post without publishing it to the real account",
        example=False
    )

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Embeddings",
                "topic_details": "Explain how embeddings represent words as vectors, show similarity between concepts, and enable semantic search.",
                "format": "reel",
                "posting_time": "19:00",
                "user_id": "user_123",
                "dry_run": False
            }
        }


# ============================================================================
# RESPONSE MODELS (What we send back to frontend)
# ============================================================================

class ProgressLogEntry(BaseModel):
    """Single progress log entry"""
    step: str = Field(..., description="Step number (1, 2, 3)")
    agent: str = Field(..., description="Agent name")
    status: str = Field(..., description="Status: 'starting', 'completed', 'error'")
    message: str = Field(..., description="Progress message")


class ContentGenerateResponse(BaseModel):
    """
    Response model for successful content generation
    """
    status: str = Field(..., description="Status: 'success' or 'error'")
    post_id: Optional[str] = Field(None, description="Instagram post ID if posted successfully")
    format: str = Field(..., description="Format used: 'post', 'story', or 'reel'")
    posted_at: str = Field(..., description="When content was posted (timestamp or time)")
    content_preview: Optional[str] = Field(None, description="First 100 characters of generated content")
    image_url: Optional[str] = Field(None, description="URL of generated image")
    message: str = Field(..., description="Success or error message")
    progress_log: Optional[List[ProgressLogEntry]] = Field(None, description="Progress log for each step")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "post_id": "ig_123456",
                "format": "reel",
                "posted_at": "2024-01-15 19:00:00",
                "content_preview": "Learn about Large Language Models...",
                "image_url": "https://example.com/image.jpg",
                "message": "Content posted successfully!"
            }
        }


class CreateUserRequest(BaseModel):
    """Request model for creating a user"""
    username: str = Field(..., description="Username")
    instagram_user_id: str = Field(..., description="Instagram user ID")
    access_token: str = Field("test_token", description="Access token (optional, defaults to test_token)")

