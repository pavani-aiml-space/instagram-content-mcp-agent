# Route Explanation: `/api/content/generate-example`

## What This Route Does

This route is an **example/demo endpoint** that shows how Pydantic validation works in FastAPI.

### Purpose
- Demonstrates automatic request validation
- Shows how to use Pydantic models in routes
- Returns a mock response (doesn't actually generate content)

### Route Details

**Endpoint**: `POST /api/content/generate-example`

**What it does:**
1. Receives a `ContentGenerateRequest` (validated automatically by Pydantic)
2. Returns a mock `ContentGenerateResponse` 
3. Shows the topic and format that would be used

**Important**: This is just an example - it doesn't actually:
- ❌ Generate content
- ❌ Create images
- ❌ Post to Instagram
- ❌ Save to database

It's purely for **learning/validation demonstration**.

---

## Request Format

```json
POST /api/content/generate-example
Content-Type: application/json

{
    "topic": "LLM",
    "format": "reel",
    "posting_time": "19:00",
    "user_id": "user_123"
}
```

**Required fields:**
- `topic` (string) - What content to create about
- `user_id` (string) - User making the request

**Optional fields:**
- `format` (string) - "post", "story", or "reel" (defaults to "reel" if not provided)
- `posting_time` (string) - When to post (defaults to None if not provided)

---

## Response Format

```json
{
    "status": "success",
    "format": "reel",
    "posted_at": "2024-01-15 19:00:00",
    "message": "Would generate content about 'LLM' for user user_123"
}
```

---

## How to Test

### Option 1: Using curl (Terminal)

```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LLM",
    "format": "reel",
    "user_id": "test_user_123"
  }'
```

### Option 2: Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/content/generate-example",
    json={
        "topic": "LLM",
        "format": "reel",
        "user_id": "test_user_123"
    }
)

print(response.json())
```

### Option 3: Using FastAPI TestClient

```python
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
response = client.post(
    "/api/content/generate-example",
    json={
        "topic": "LLM",
        "format": "reel",
        "user_id": "test_user_123"
    }
)
print(response.json())
```

---

## What Happens Behind the Scenes

```
1. Request comes in:
   POST /api/content/generate-example
   Body: {"topic": "LLM", "user_id": "123"}
         ↓
2. FastAPI validates with Pydantic:
   ✅ topic is string? YES
   ✅ user_id is string? YES
   ✅ format is optional? YES (not provided, will be None)
         ↓
3. Function receives validated request:
   request.topic = "LLM"
   request.user_id = "123"
   request.format = None
         ↓
4. Function returns mock response:
   {
     "status": "success",
     "format": "reel",  # Uses "reel" as default since format was None
     "posted_at": "2024-01-15 19:00:00",
     "message": "Would generate content about 'LLM' for user 123"
   }
```

---

## Testing Validation

### Valid Request ✅

```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{"topic": "LLM", "user_id": "123"}'
```

**Response**: 200 OK with success message

### Invalid Request ❌ (Missing Required Field)

```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{"format": "reel"}'
  # topic and user_id missing!
```

**Response**: 422 Unprocessable Entity with validation error

---

## Difference from `/api/content/request`

| Route | Purpose | What It Does |
|-------|---------|--------------|
| `/api/content/generate-example` | **Demo/Example** | Shows validation, returns mock response |
| `/api/content/request` | **Real Functionality** | Saves request to database |

**Key Difference:**
- `generate-example` = Just for learning (no database)
- `request` = Actually saves to database (real functionality)

---

This route is perfect for testing Pydantic validation without affecting the database!

