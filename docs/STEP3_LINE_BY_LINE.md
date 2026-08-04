# Step 3: FastAPI Code - Line by Line Explanation

## File: `backend/main.py`

Let's break down every single line:

---

### Line 1-4: Comments
```python
"""
FastAPI Application - Main Entry Point

This is the heart of our backend server.
It creates the FastAPI app and sets up routes.
"""
```
**What**: Documentation string (docstring)
**Why**: Explains what this file does
**Note**: Python uses triple quotes `"""` for multi-line strings

---

### Line 7: Import Statement
```python
from fastapi import FastAPI
```
**What**: Imports the FastAPI class
**Why**: We need FastAPI to create our web server
**Think of it like**: Importing a tool from a toolbox

**Breakdown:**
- `from fastapi` = From the fastapi package
- `import FastAPI` = Import the FastAPI class
- `FastAPI` = The main class that creates our app

---

### Line 10-14: Create FastAPI App
```python
app = FastAPI(
    title="Instagram Content Generator API",
    description="Multi-agent system for generating Instagram content",
    version="1.0.0"
)
```
**What**: Creates our FastAPI application instance
**Why**: This is the "server" - it handles all requests

**Breakdown:**
- `app =` = Store it in a variable called "app"
- `FastAPI(...)` = Create a new FastAPI application
- `title=` = Name shown in API documentation
- `description=` = What our API does
- `version=` = Version number

**Think of it like:**
- Creating a new restaurant
- `app` = the restaurant itself
- The parameters = restaurant name, description, etc.

---

### Line 18-26: Define a Route
```python
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
```

**What**: Defines a route (endpoint) that responds to GET requests

**Breakdown:**

1. **`@app.get("/")`** - This is a **decorator**
   - `@` = Decorator syntax (Python feature)
   - `app.get` = "When someone makes a GET request"
   - `"/"` = The URL path (root/homepage)
   - **Together**: "When someone visits the root URL with GET, run this function"

2. **`def read_root():`** - Function definition
   - `def` = Define a function
   - `read_root` = Function name (we chose this)
   - `()` = No parameters needed
   - **This function runs when someone visits `/`**

3. **`return {...}`** - What to send back
   - `return` = Send this data back to the requester
   - `{...}` = Dictionary (JSON object)
   - FastAPI automatically converts Python dict to JSON

**What happens:**
```
User visits: http://localhost:8000/
         ↓
FastAPI sees: GET request to "/"
         ↓
FastAPI runs: read_root() function
         ↓
Function returns: {"message": "...", "status": "running"}
         ↓
FastAPI sends: JSON response to user
```

---

### Line 29-33: Run the Server
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**What**: Code that runs when we execute this file directly

**Breakdown:**

1. **`if __name__ == "__main__":`**
   - `__name__` = Special Python variable
   - When file is run directly, `__name__` = `"__main__"`
   - **Meaning**: "Only run this code if file is executed directly (not imported)"

2. **`import uvicorn`**
   - Uvicorn = ASGI server (runs FastAPI)
   - **Think of it like**: The engine that runs our restaurant

3. **`uvicorn.run(app, host="0.0.0.0", port=8000)`**
   - `app` = Our FastAPI application
   - `host="0.0.0.0"` = Listen on all network interfaces (accessible from anywhere)
   - `port=8000` = Port number (like a door number)
   - **Together**: "Start the server on port 8000"

---

## Key Concepts Explained

### Decorators (`@app.get`)
**What**: Special syntax that modifies functions
**Example**: `@app.get("/")` means "This function handles GET requests to /"
**Why**: Clean, readable way to define routes

### Dictionary (`{...}`)
**What**: Python data structure (key-value pairs)
**Example**: `{"message": "Hello", "status": "ok"}`
**Why**: Easy way to structure data, automatically becomes JSON

### JSON
**What**: JavaScript Object Notation - data format
**Why**: Standard way to send data over HTTP
**FastAPI**: Automatically converts Python dicts to JSON

---

## What Happens When We Run This?

1. **We run**: `python backend/main.py`
2. **Python executes**: The code
3. **FastAPI app created**: `app = FastAPI(...)`
4. **Route registered**: `@app.get("/")` tells FastAPI about our route
5. **Uvicorn starts**: Server starts listening on port 8000
6. **Server ready**: Can now receive requests!

---

## Testing It

Once running, we can:
- Visit `http://localhost:8000/` in browser
- See: `{"message": "Welcome...", "status": "running"}`
- Visit `http://localhost:8000/docs` for auto-generated API docs!

---

This is the foundation! Everything else builds on this.

