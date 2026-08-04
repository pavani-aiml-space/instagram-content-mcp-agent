# Testing `/api/content/generate-example` Route

## What This Route Does

**Purpose**: Example/demo endpoint that demonstrates Pydantic validation

**What it does:**
1. ✅ Receives a request (validated automatically by Pydantic)
2. ✅ Returns a mock response showing what would happen
3. ❌ Does NOT actually generate content
4. ❌ Does NOT save to database
5. ❌ Does NOT post to Instagram

**It's purely for learning/validation demonstration!**

---

## How to Test

### Step 1: Start the Server

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp
source venv/bin/activate
uvicorn backend.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### Step 2: Test Valid Request

**Open a new terminal** and run:

```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LLM",
    "format": "reel",
    "user_id": "test_user_123"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "post_id": null,
  "format": "reel",
  "posted_at": "2024-01-15 19:00:00",
  "content_preview": null,
  "image_url": null,
  "message": "Would generate content about 'LLM' for user test_user_123"
}
```

**Status Code**: 200 OK ✅

---

### Step 3: Test Invalid Request (Missing Required Field)

```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "format": "reel",
    "user_id": "test_user_123"
  }'
  # topic is missing!
```

**Expected Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "topic"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Status Code**: 422 Unprocessable Entity ❌

**This shows validation is working!**

---

### Step 4: Test with Optional Fields Omitted

```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI Agents",
    "user_id": "test_user_456"
  }'
  # format and posting_time are optional - not provided
```

**Expected Response:**
```json
{
  "status": "success",
  "format": "reel",  // Defaults to "reel" since format was None
  "posted_at": "2024-01-15 19:00:00",
  "message": "Would generate content about 'AI Agents' for user test_user_456"
}
```

**Status Code**: 200 OK ✅

---

## Quick Test Script

You can also use the provided test script:

```bash
# Make sure server is running first!
./tests/test_route_manual.sh
```

---

## What You Should See

### ✅ Valid Request
- Status: 200 OK
- Response: Success message with topic and format

### ❌ Invalid Request
- Status: 422 Unprocessable Entity
- Response: Clear error message showing what's wrong

---

## Understanding the Response

The route returns a **mock response** - it doesn't actually:
- Generate content
- Create images
- Post to Instagram

It just shows:
- ✅ Validation worked (request was valid)
- ✅ What format would be used
- ✅ What topic would be processed

**This is perfect for learning how Pydantic validation works!**

---

## Next Steps

Once you understand this route, you can:
1. Test the `/api/content/request` route (actually saves to database)
2. Move to Step 4: Building MCP Tools
3. Build agents that use these routes

