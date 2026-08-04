# Pydantic Validation - Practical Example

## How Validation Works: Step-by-Step Example

Let's see exactly what happens when you use Pydantic models in FastAPI routes.

---

## The Code

```python
from fastapi import FastAPI
from backend.models.schemas import ContentGenerateRequest

app = FastAPI()

@app.post("/api/content/generate")
def generate_content(request: ContentGenerateRequest):
    return {"message": f"Creating content about {request.topic}"}
```

**Key**: The type hint `request: ContentGenerateRequest` tells FastAPI to validate automatically!

---

## Example 1: Valid Request ✅

### What User Sends

```bash
POST /api/content/generate
Content-Type: application/json

{
    "topic": "LLM",
    "format": "reel",
    "user_id": "user_123"
}
```

### What Happens Behind the Scenes

```
1. FastAPI receives request
   ↓
2. FastAPI sees: request: ContentGenerateRequest
   ↓
3. FastAPI validates JSON against ContentGenerateRequest model:
   
   ✅ topic: "LLM" → Is string? YES → Valid
   ✅ format: "reel" → Is string or None? YES → Valid
   ✅ posting_time: Missing → Optional field → Valid (uses None)
   ✅ user_id: "user_123" → Is string? YES → Valid
   ↓
4. All valid! FastAPI creates:
   ContentGenerateRequest(
       topic="LLM",
       format="reel",
       posting_time=None,
       user_id="user_123"
   )
   ↓
5. Passes to function: generate_content(request)
   ↓
6. Function runs and returns:
   {"message": "Creating content about LLM"}
```

### Response

```json
{
    "message": "Creating content about LLM"
}
```

**Status Code**: 200 OK

---

## Example 2: Invalid Request - Missing Required Field ❌

### What User Sends

```bash
POST /api/content/generate
Content-Type: application/json

{
    "format": "reel",
    "user_id": "user_123"
    // topic is missing!
}
```

### What Happens Behind the Scenes

```
1. FastAPI receives request
   ↓
2. FastAPI sees: request: ContentGenerateRequest
   ↓
3. FastAPI validates JSON against ContentGenerateRequest model:
   
   ❌ topic: Missing → Required field! → INVALID
   ✅ format: "reel" → Valid (but validation stops here)
   ✅ user_id: "user_123" → Valid (but validation stops here)
   ↓
4. Validation FAILED!
   ↓
5. FastAPI returns error immediately
   ↓
6. Function NEVER runs!
```

### Response

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

**Status Code**: 422 Unprocessable Entity

**Key Point**: The function `generate_content()` never runs! FastAPI stops before it.

---

## Example 3: Invalid Request - Wrong Type ❌

### What User Sends

```bash
POST /api/content/generate
Content-Type: application/json

{
    "topic": 123,  // Should be string!
    "format": "reel",
    "user_id": "user_123"
}
```

### What Happens Behind the Scenes

```
1. FastAPI receives request
   ↓
2. FastAPI sees: request: ContentGenerateRequest
   ↓
3. FastAPI validates JSON against ContentGenerateRequest model:
   
   ❌ topic: 123 → Is string? NO (it's a number) → INVALID
   ↓
4. Validation FAILED!
   ↓
5. FastAPI returns error immediately
   ↓
6. Function NEVER runs!
```

### Response

```json
{
    "detail": [
        {
            "loc": ["body", "topic"],
            "msg": "Input should be a valid string",
            "type": "string_type"
        }
    ]
}
```

**Status Code**: 422 Unprocessable Entity

---

## Example 4: Valid Request - Optional Fields Omitted ✅

### What User Sends

```bash
POST /api/content/generate
Content-Type: application/json

{
    "topic": "LLM",
    "user_id": "user_123"
    // format and posting_time are optional - not provided
}
```

### What Happens Behind the Scenes

```
1. FastAPI receives request
   ↓
2. FastAPI sees: request: ContentGenerateRequest
   ↓
3. FastAPI validates JSON against ContentGenerateRequest model:
   
   ✅ topic: "LLM" → Is string? YES → Valid
   ✅ format: Missing → Optional field → Valid (uses None)
   ✅ posting_time: Missing → Optional field → Valid (uses None)
   ✅ user_id: "user_123" → Is string? YES → Valid
   ↓
4. All valid! FastAPI creates:
   ContentGenerateRequest(
       topic="LLM",
       format=None,  // Default value
       posting_time=None,  // Default value
       user_id="user_123"
   )
   ↓
5. Passes to function: generate_content(request)
   ↓
6. Function runs and returns:
   {"message": "Creating content about LLM"}
```

### Response

```json
{
    "message": "Creating content about LLM"
}
```

**Status Code**: 200 OK

**Key Point**: Optional fields can be omitted - Pydantic uses default values (None).

---

## Visual Comparison

### Without Pydantic (Manual Validation)

```python
@app.post("/api/content/generate")
def generate_content(request_data: dict):
    # Manual validation - error-prone!
    if "topic" not in request_data:
        return {"error": "topic is required"}, 400
    if not isinstance(request_data["topic"], str):
        return {"error": "topic must be string"}, 400
    if "user_id" not in request_data:
        return {"error": "user_id is required"}, 400
    if not isinstance(request_data["user_id"], str):
        return {"error": "user_id must be string"}, 400
    
    # Finally can use the data
    topic = request_data["topic"]
    # ... rest of code
```

**Problems:**
- ❌ Lots of repetitive code
- ❌ Easy to miss checks
- ❌ Inconsistent error messages
- ❌ No type safety

### With Pydantic (Automatic Validation)

```python
@app.post("/api/content/generate")
def generate_content(request: ContentGenerateRequest):
    # Pydantic already validated everything!
    # request.topic is guaranteed to be a string
    # request.user_id is guaranteed to be a string
    
    topic = request.topic  # Safe to use!
    # ... rest of code
```

**Benefits:**
- ✅ Automatic validation
- ✅ Consistent error messages
- ✅ Type safety
- ✅ Less code

---

## How FastAPI Knows to Validate

### The Type Hint is the Magic

```python
def generate_content(request: ContentGenerateRequest):
                            # ↑ This type hint!
```

**What FastAPI does:**
1. Reads the type hint: `ContentGenerateRequest`
2. Checks: "Is this a Pydantic BaseModel?" → YES
3. Automatically sets up validation for this route
4. Every request to this route is validated automatically

**No extra code needed!** Just the type hint.

---

## Summary

| Scenario | What Happens | Result |
|----------|--------------|--------|
| **Valid request** | All fields correct | ✅ Function runs, returns success |
| **Missing required field** | `topic` missing | ❌ Error returned, function never runs |
| **Wrong type** | `topic` is number instead of string | ❌ Error returned, function never runs |
| **Optional fields omitted** | `format` and `posting_time` missing | ✅ Valid (uses defaults), function runs |

**Key Takeaway**: Just by adding `request: ContentGenerateRequest` as a type hint, FastAPI automatically validates all requests. No extra code needed!

