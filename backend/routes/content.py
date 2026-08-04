"""
Content Generation Routes
Orchestrates the full flow: content → image → Instagram post
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.schemas import ContentGenerateRequest, ContentGenerateResponse
from database.connection import get_db
from database.models import User, ContentRequest, Post
from agents.coordinator_agent import run_coordinator
import os

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/api/content", tags=["content"])


@router.post("/generate-and-post", response_model=ContentGenerateResponse)
async def generate_and_post(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Complete flow: Generate content → Generate image → Post to Instagram
    
    This endpoint:
    1. Generates content (caption + hashtags) from topic
    2. Generates an image
    3. Posts to Instagram
    4. Saves to database
    """
    try:
        logger.info(f"📥 Received content generation request - Topic: {request.topic}, Format: {request.format}, User: {request.user_id}")
        
        # Look up user
        logger.info(f"🔍 Looking up user: {request.user_id}")
        user = db.query(User).filter(
            (User.id == request.user_id) | (User.instagram_user_id == request.user_id)
        ).first()
        
        if not user:
            logger.warning(f"❌ User not found: {request.user_id}")
            raise HTTPException(
                status_code=400,
                detail=f"User '{request.user_id}' does not exist. Please create the user first."
            )
        
        logger.info(f"✅ User found: {user.username} (ID: {user.id})")
        
        # Get Instagram account ID from user (for now, we'll need to add this to User model)
        # For MVP, we'll use a default or from env
        instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        if not instagram_account_id:
            logger.error("❌ Instagram Account ID not configured")
            raise HTTPException(
                status_code=400,
                detail="Instagram Account ID not configured. Set INSTAGRAM_ACCOUNT_ID environment variable."
            )
        
        logger.info(f"🚀 Starting multi-agent workflow...")

        # Run Coordinator Agent (orchestrates all specialized agents, over a real MCP session)
        result = await run_coordinator(
            topic=request.topic,
            format=request.format or "post",
            user_id=str(user.id),
            instagram_account_id=instagram_account_id,
            topic_details=request.topic_details,
            dry_run=request.dry_run or False,
        )
        
        logger.info(f"✅ Multi-agent workflow completed - Status: {result.get('status')}")
        
        # Check for errors
        if result.get("status") == "error":
            logger.error(f"❌ Workflow failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error occurred")
            )
        
        # Save to database
        logger.info("💾 Saving to database...")
        db_request = ContentRequest(
            topic=request.topic,
            format=request.format or "post",
            posting_time=request.posting_time,
            user_id=user.id,
            status="completed"
        )
        
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        logger.info(f"✅ Content request saved (ID: {db_request.id})")
        
        # Save post record
        db_post = Post(
            request_id=db_request.id,
            instagram_post_id=result["post_id"],
            format=request.format or "post",
            image_url=result["image_url"],
            caption=result["caption"],
            hashtags=[tag.strip("#") for tag in result["hashtags"].split() if tag.startswith("#")]
        )
        
        db.add(db_post)
        db.commit()
        logger.info(f"✅ Post record saved (ID: {db_post.id})")
        
        logger.info(f"🎉 Request completed successfully - Post ID: {result['post_id']}")
        
        return ContentGenerateResponse(
            status="success",
            post_id=result["post_id"],
            format=request.format or "post",
            posted_at="now",  # TODO: Get actual timestamp
            content_preview=result["caption"][:100] + "..." if len(result["caption"]) > 100 else result["caption"],
            image_url=result["image_url"],
            message=f"Successfully posted to Instagram! Post ID: {result['post_id']}",
            progress_log=result.get("progress_log", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in content generation flow: {str(e)}"
        )

