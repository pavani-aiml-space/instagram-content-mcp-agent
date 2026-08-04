"""
FastAPI Application - Main Entry Point

This is the heart of our backend server.
It creates the FastAPI app and sets up routes.
"""

# Import FastAPI - this is the framework we're using
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

# Import Pydantic models for request/response validation
from backend.models.schemas import (
    ContentGenerateRequest,
    ContentGenerateResponse,
    CreateUserRequest
)

# Import database connection and models
from database.connection import get_db
from database.models import ContentRequest, User

# Import routes
from backend.routes.content import router as content_router

# Create FastAPI app instance
# Think of this as creating a new restaurant
# app = the restaurant itself

app = FastAPI(
    title="Instagram Content Generator API",  # Name of our API
    description="Multi-agent system for generating Instagram content",  # What it does
    version="1.0.0"  # Version number
)

# Add CORS middleware to allow frontend to call API
# Regex covers Vite/React falling over to 5174+ when 5173 is already in use
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a route (endpoint)
# This is like a door in our restaurant
# When someone visits this URL, this function runs
@app.get("/")
def read_root():
    """
    Root endpoint - the homepage of our API
    
    GET / means: "When someone visits the root URL"
    Returns: A simple message
    """
    return {
        "message": "Welcome to Instagram Content Generator API!",
        "status": "running"
    }
@app.get("/test")
def myfirst_page():
    """
    Test endpoint - a simple route to practice
    
    GET /test means: "When someone visits /test URL"
    Returns: A simple test message
    """
    return {
        "message": "Hello, test"
    }


@app.post("/api/users/create")
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db)
):
    """
    Create a test user (for testing purposes)
    
    This endpoint creates a user in the database so you can test content requests.
    """
    from fastapi import HTTPException
    from sqlalchemy.exc import IntegrityError
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.instagram_user_id == request.instagram_user_id).first()
        if existing_user:
            return {
                "status": "success",
                "message": f"User '{request.username}' already exists",
                "user_id": existing_user.id,
                "username": existing_user.username
            }
        
        # Create new user
        new_user = User(
            instagram_user_id=request.instagram_user_id,
            username=request.username,
            access_token=request.access_token
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "status": "success",
            "message": f"User '{request.username}' created successfully",
            "user_id": new_user.id,
            "username": new_user.username
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating user: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint - tests database connection
    
    This endpoint checks if:
    - API is running
    - Database is connected
    
    Returns: Status of API and database
    """
    try:
        # Try to query database
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "API and database are working!"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@app.post("/api/content/request")
def create_content_request(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Save a content generation request to database
    
    This endpoint:
    1. Validates request (Pydantic)
    2. Looks up user by instagram_user_id or user_id
    3. Saves to database (SQLAlchemy)
    4. Returns saved request ID
    
    The db parameter is automatically provided by FastAPI
    using dependency injection (Depends(get_db))
    """
    from fastapi import HTTPException
    from sqlalchemy.exc import IntegrityError
    
    try:
        # Look up user - request.user_id can be either User.id (UUID) or instagram_user_id
        user = db.query(User).filter(
            (User.id == request.user_id) | (User.instagram_user_id == request.user_id)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"User '{request.user_id}' does not exist. Please create the user first using the 'Create User' button."
            )
        
        # Create database record from validated request
        db_request = ContentRequest(
            topic=request.topic,
            format=request.format or "reel",  # Default to "reel" if not provided
            posting_time=request.posting_time,
            user_id=user.id,  # Use the actual User.id (UUID)
            status="pending"  # Initial status
        )
        
        # Save to database
        db.add(db_request)  # Add to session
        db.commit()  # Actually save to database
        db.refresh(db_request)  # Refresh to get the auto-generated ID
        
        return {
            "status": "success",
            "request_id": db_request.id,
            "message": f"Content request saved for topic '{request.topic}'",
            "user_id": user.id,
            "username": user.username,
            "created_at": db_request.created_at.isoformat() if db_request.created_at else None
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        raise HTTPException(
            status_code=400,
            detail=f"Database error: {error_msg}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error saving request: {str(e)}"
        )

# Include content router (adds /api/content/* routes)
app.include_router(content_router)

# This is the entry point when we run the server
# We'll use uvicorn to run this (in the next step)
if __name__ == "__main__":
    import uvicorn
    # Run the server on localhost, port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

