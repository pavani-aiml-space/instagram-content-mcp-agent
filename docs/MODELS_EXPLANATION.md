# Models Explanation: What We Store

## Two Types of Models

We have **two different model directories** for different purposes:

1. **`backend/models/schemas.py`** - Pydantic models (API validation)
2. **`database/models.py`** - SQLAlchemy ORM models (database tables)

---

## 1. Backend Models (`backend/models/schemas.py`)

**Purpose**: Request/Response validation for FastAPI endpoints

**What we store**:
- API request schemas (what the frontend sends)
- API response schemas (what we send back)
- Data validation rules

### Request Models

```python
# Content Generation Request
class ContentGenerateRequest(BaseModel):
    topic: str                    # Required: "LLM", "Ragi Dosa Recipe"
    format: Optional[str] = None  # Optional: "post", "story", "reel"
    posting_time: Optional[str] = None  # Optional: "19:00", "now", "best"
    user_id: str                 # Required: Instagram user ID
```

### Response Models

```python
# Success Response
class ContentGenerateResponse(BaseModel):
    status: str                  # "success" or "error"
    post_id: Optional[str]       # Instagram post ID
    format: str                  # "post", "story", or "reel"
    posted_at: str               # "19:00" or timestamp
    content_preview: str         # First 100 chars of content
    image_url: str               # Generated image URL
    message: Optional[str]      # Success/error message

# Format Decision Request (for human-in-the-loop)
class FormatDecisionResponse(BaseModel):
    status: str                  # "needs_format_decision"
    options: dict                # Format options with descriptions
    recommendation: str          # Recommended format
    reason: str                 # Why this recommendation
```

**Why Pydantic?**
- Automatic validation (type checking, required fields)
- FastAPI auto-generates API documentation
- Prevents invalid data from reaching agents

---

## 2. Database Models (`database/models.py`)

**Purpose**: SQLAlchemy ORM models for PostgreSQL database

**What we store**: Persistent data that needs to survive server restarts

### Database Tables (MVP - Must Haves Only)

#### 1. **User Model** (`users` table)
```python
class User(Base):
    id: str                      # Primary key
    instagram_user_id: str       # Instagram account ID
    username: str                # Instagram username
    access_token: str            # Instagram API token
    created_at: datetime         # Account creation time
```

**Stores**: Instagram influencer accounts

**Why essential?** Need to identify who's making requests and authenticate with Instagram API.

---

#### 2. **Content Request Model** (`content_requests` table)
```python
class ContentRequest(Base):
    id: str                      # Primary key
    user_id: str                 # Foreign key → users
    topic: str                   # "LLM", "Ragi Dosa Recipe"
    format: str                  # "post", "story", "reel"
    posting_time: Optional[str]  # "19:00" or null
    status: str                  # "pending", "processing", "completed", "failed"
    created_at: datetime         # Request timestamp
    completed_at: Optional[datetime]  # Completion time
```

**Stores**: Each content generation request from users

**Why essential?** Need to track every request and its status.

---

#### 3. **Post Model** (`posts` table)
```python
class Post(Base):
    id: str                      # Primary key
    request_id: str              # Foreign key → content_requests
    instagram_post_id: str       # Instagram's post ID
    format: str                  # "post", "story", "reel"
    image_url: str               # Posted image URL
    caption: str                 # Posted caption
    hashtags: List[str]          # Array of hashtags
    posted_at: datetime          # When posted to Instagram
```

**Stores**: Successfully posted Instagram content

**Why essential?** Need to track what was posted and link back to the original request.

---

## Removed Tables (Not Essential for MVP)

### ❌ GeneratedContent Table
**Why removed?** Content can be stored directly in `ContentRequest` or `Post` tables.
- Generated text → Store in `Post.caption`
- Generated image URL → Store in `Post.image_url`
- Tool used → Can add to `ContentRequest` if needed later

### ❌ AgentState Table
**Why removed?** Workflow resumption is a nice-to-have, not essential for MVP.
- Can add later if needed for production
- For MVP, if workflow fails, user can retry

---

## Simplified Data Flow

```
1. User makes request
   ↓
   ContentRequest created (status: "pending")
   
2. Agents generate content
   ↓
   ContentRequest updated (status: "processing")
   
3. Content posted to Instagram
   ↓
   Post created
   ↓
   ContentRequest updated (status: "completed")
```

---

## Data Flow: Models in Action (Simplified)

```
1. Frontend sends request
   ↓
   backend/models/schemas.py (Pydantic)
   ↓ Validates: topic, format, posting_time
   
2. Request validated → Coordinator Agent
   ↓
   database/models.py (SQLAlchemy)
   ↓ Creates: ContentRequest record (status: "pending")
   
3. Agents generate content (in memory)
   ↓
   Content Creator → generates text
   Image Generator → generates image
   
4. Instagram Tool posts content
   ↓
   database/models.py
   ↓ Creates: Post record (with caption, image_url, hashtags)
   ↓ Updates: ContentRequest.status = "completed"
   
5. Response sent to frontend
   ↓
   backend/models/schemas.py (Pydantic)
   ↓ Formats: ContentGenerateResponse
```

---

## Summary

### Backend Models (`backend/models/schemas.py`)
- ✅ **Request validation** (what frontend sends)
- ✅ **Response formatting** (what we send back)
- ✅ **Type safety** (Pydantic validation)
- ❌ **NOT stored in database** (temporary, per-request)

### Database Models (`database/models.py`)
- ✅ **Persistent storage** (survives server restarts)
- ✅ **User accounts** (Instagram influencers)
- ✅ **Request history** (all content generation requests)
- ✅ **Posted content** (Instagram posts with caption, image, hashtags)

---

## Key Differences

| Aspect | Backend Models | Database Models |
|--------|---------------|-----------------|
| **Purpose** | API validation | Data persistence |
| **Library** | Pydantic | SQLAlchemy |
| **Lifetime** | Per-request | Permanent |
| **Storage** | Memory (temporary) | PostgreSQL (permanent) |
| **Used by** | FastAPI routes | Agents, tools |

---

This structure ensures:
- ✅ API requests are validated before processing
- ✅ Essential data is persisted (users, requests, posts)
- ✅ Simple and minimal for MVP
- ✅ Can add more tables later if needed (GeneratedContent, AgentState)

