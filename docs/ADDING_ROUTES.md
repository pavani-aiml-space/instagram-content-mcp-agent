# How to Add Routes in FastAPI

## Basic Route Syntax

```python
@app.get("/route-path")
def function_name():
    return {"message": "response"}
```

---

## What You Need to Know

### 1. The Decorator
```python
@app.get("/test")
```
**Breakdown:**
- `@app.get` = Handle GET requests
- `"/test"` = The URL path (must be a string in quotes!)
- **Important**: The path must be in quotes: `"/test"` not `test`

### 2. The Function
```python
def myfirst_page():
```
**Breakdown:**
- `def` = Define a function
- `myfirst_page` = Function name (you choose this)
- `()` = No parameters needed (for now)
- **Note**: Function name doesn't affect the URL, only the decorator does

### 3. The Return
```python
return {"message": "Hello, test"}
```
**Breakdown:**
- `return` = Send this back
- `{...}` = Dictionary (becomes JSON)
- FastAPI automatically converts to JSON

---

## Common Mistakes

### ❌ Wrong: Missing Quotes
```python
@app.get(test)  # ERROR! 'test' is not defined
```

### ✅ Correct: With Quotes
```python
@app.get("/test")  # Correct! "/test" is a string
```

### ❌ Wrong: Missing Slash
```python
@app.get("test")  # Works, but not standard
```

### ✅ Correct: With Leading Slash
```python
@app.get("/test")  # Standard format
```

---

## Examples

### Example 1: Simple Route
```python
@app.get("/test")
def test_endpoint():
    return {"message": "This is a test"}
```
**URL**: `http://localhost:8000/test`
**Response**: `{"message": "This is a test"}`

### Example 2: Multiple Routes
```python
@app.get("/")
def home():
    return {"message": "Home"}

@app.get("/test")
def test():
    return {"message": "Test"}

@app.get("/about")
def about():
    return {"message": "About"}
```
**URLs**:
- `http://localhost:8000/` → Home
- `http://localhost:8000/test` → Test
- `http://localhost:8000/about` → About

### Example 3: Route with Path Parameter
```python
@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```
**URL**: `http://localhost:8000/user/123`
**Response**: `{"user_id": 123}`

---

## Testing Your Route

### Method 1: Browser
1. Start server: `uvicorn backend.main:app --reload`
2. Visit: `http://localhost:8000/test`
3. See: `{"message": "Hello, test"}`

### Method 2: curl
```bash
curl http://localhost:8000/test
```

### Method 3: API Docs
1. Visit: `http://localhost:8000/docs`
2. See your new `/test` endpoint
3. Click "Try it out" → "Execute"

---

## Your Fixed Code

```python
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
```

**What this does:**
- When someone visits `http://localhost:8000/test`
- FastAPI runs `myfirst_page()` function
- Returns `{"message": "Hello, test"}`

---

## Key Points

1. **Route path must be a string**: `"/test"` not `test`
2. **Use leading slash**: `"/test"` not `"test"`
3. **Function name doesn't matter**: `myfirst_page()` could be `anything()`
4. **Return a dictionary**: FastAPI converts it to JSON automatically

---

Now your route is fixed! Test it by visiting `http://localhost:8000/test` in your browser!

