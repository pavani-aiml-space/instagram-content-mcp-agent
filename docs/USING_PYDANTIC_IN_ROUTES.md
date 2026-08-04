# Using Pydantic Models in Routes - Explained

## How to Use Pydantic Models in FastAPI Routes

### Basic Pattern

```python
from backend.models.schemas import ContentGenerateRequest

@app.post("/api/content/generate")
def generate_content(request: ContentGenerateRequest):
    # FastAPI automatically validates request body
    # If invalid → Returns error (function never runs)
    # If valid → Passes validated object to function
    
    # Use validated data
    topic = request.topic  # Guaranteed to be a string
    format = request.format  # Either string or None
```

---

## Step-by-Step: What Happens

### 1. User Sends Request

```json
POST /api/content/generate
{
    "topic": "LLM",
    "format": "reel",
    "user_id": "123"
}
```

### 2. FastAPI Receives Request

FastAPI sees:
- Route: `@app.post("/api/content/generate")`
- Parameter: `request: ContentGenerateRequest`
- **Action**: Validate request body against `ContentGenerateRequest` model

### 3. Pydantic Validates

Pydantic checks:
- ✅ `topic` is string? YES
- ✅ `format` is string or None? YES
- ✅ `user_id` is string? YES
- ✅ All required fields present? YES

### 4. If Valid

```python
# FastAPI creates ContentGenerateRequest object
request = ContentGenerateRequest(
    topic="LLM",
    format="reel",
    user_id="123"
)

# Passes to function
generate_content(request)
```

### 5. If Invalid

```python
# FastAPI returns error immediately
# Function never runs!
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

---

## Example Route

```python
@app.post("/api/content/generate-example")
def generate_content_example(request: ContentGenerateRequest):
    """
    Example endpoint showing Pydantic validation
    """
    # Pydantic already validated!
    # request.topic is guaranteed to be a string
    # request.format is either string or None
    
    return ContentGenerateResponse(
        status="success",
        format=request.format or "reel",  # Use format or default
        posted_at="2024-01-15 19:00:00",
        message=f"Would generate content about '{request.topic}'"
    )
```

---

## Key Points

1. **Type Hint in Function**: `request: ContentGenerateRequest`
   - Tells FastAPI to validate against this model

2. **Automatic Validation**: FastAPI does it for you
   - No manual checking needed

3. **Type Safety**: After validation, types are guaranteed
   - `request.topic` is always a string
   - `request.format` is always string or None

4. **Error Handling**: Invalid requests return errors automatically
   - Clear error messages
   - Function never runs with invalid data

---

## Testing the Route

### Valid Request
```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LLM",
    "format": "reel",
    "user_id": "123"
  }'
```

**Response**: `{"status": "success", ...}`

### Invalid Request (Missing Topic)
```bash
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "format": "reel",
    "user_id": "123"
  }'
```

**Response**: Error - "topic field required"

---

This is how Pydantic keeps our API safe and validated!

