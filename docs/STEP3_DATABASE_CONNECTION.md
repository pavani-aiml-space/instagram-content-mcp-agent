# Step 3.4: Connect Database to FastAPI - Explained

## What We're Building

**Goal**: Connect our PostgreSQL database to FastAPI routes so we can save and read data.

**Think of it like:**
- Connecting a phone to a charger
- Connecting a TV to cable
- Connecting your API to your database

---

## Why We Need This

### Problem Without Database Connection

```python
@app.post("/api/content/generate")
def generate_content(request: ContentGenerateRequest):
    # Where do we save the request?
    # How do we track what was generated?
    # We need database access!
```

**Issues:**
- ❌ Can't save requests
- ❌ Can't track content
- ❌ Can't persist data

### Solution: Database Dependency Injection

```python
from database.connection import get_db

@app.post("/api/content/generate")
def generate_content(request: ContentGenerateRequest, db: Session = Depends(get_db)):
    # Now we have database access!
    # db is a SQLAlchemy session
    # We can save data, read data, etc.
```

**Benefits:**
- ✅ Automatic database connection
- ✅ Automatic cleanup (closes connection after use)
- ✅ Safe (one connection per request)
- ✅ Easy to use

---

## What is Dependency Injection?

**Dependency Injection** = FastAPI automatically provides what your function needs

**Example:**
```python
def my_function(db: Session = Depends(get_db)):
    # FastAPI automatically:
    # 1. Calls get_db()
    # 2. Gets database session
    # 3. Passes it to function
    # 4. Closes connection after function finishes
```

**Why it's useful:**
- No manual connection management
- Automatic cleanup
- One connection per request (safe)

---

## How It Works

### Step 1: The Dependency Function

```python
# database/connection.py
def get_db():
    db = SessionLocal()  # Create session
    try:
        yield db  # Give it to function
    finally:
        db.close()  # Always close after use
```

**What this does:**
- Creates database session
- Yields it (gives it to function)
- Closes it after function finishes (cleanup)

### Step 2: Use in Route

```python
from fastapi import Depends
from database.connection import get_db
from sqlalchemy.orm import Session

@app.post("/api/content/generate")
def generate_content(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)  # FastAPI provides this!
):
    # db is now a database session
    # We can use it to save/read data
```

**What FastAPI does:**
1. Sees `db: Session = Depends(get_db)`
2. Calls `get_db()` function
3. Gets database session
4. Passes it to your function
5. Closes connection after function finishes

---

## What We'll Build

1. **Update main.py**: Import database dependency
2. **Add health check route**: Test database connection
3. **Add content request route**: Save requests to database
4. **Test**: Verify everything works

---

## Step-by-Step: Building It

### Step 1: Import Dependencies

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
```

**What this does:**
- `Depends` = FastAPI's dependency injection
- `Session` = SQLAlchemy database session type
- `get_db` = Our dependency function

### Step 2: Add Health Check Route

```python
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint - tests database connection
    """
    try:
        # Try to query database
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
```

**What this does:**
- Tests database connection
- Returns status
- Useful for monitoring

### Step 3: Add Route That Saves Data

```python
from database.models import ContentRequest

@app.post("/api/content/request")
def create_content_request(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Save a content generation request to database
    """
    # Create database record
    db_request = ContentRequest(
        topic=request.topic,
        format=request.format,
        user_id=request.user_id,
        status="pending"
    )
    
    # Save to database
    db.add(db_request)
    db.commit()  # Actually save it
    db.refresh(db_request)  # Get the ID that was generated
    
    return {
        "status": "success",
        "request_id": db_request.id,
        "message": "Request saved to database"
    }
```

**What this does:**
- Creates database record from request
- Saves it to database
- Returns the saved record ID

---

## Key Concepts

### Dependency Injection Pattern

```python
def my_route(db: Session = Depends(get_db)):
    # db is automatically provided by FastAPI
    # No need to manually create/close connection
```

**Benefits:**
- ✅ Automatic connection management
- ✅ One connection per request
- ✅ Automatic cleanup

### Database Session

**What it is:**
- Connection to database
- Used to execute queries
- Must be closed after use

**How we use it:**
```python
db.add(object)      # Add new record
db.commit()         # Save changes
db.refresh(object)  # Get updated data (like ID)
db.query(Model)     # Query database
```

---

## What Happens When Request Comes In

```
1. User sends POST /api/content/request
   {
     "topic": "LLM",
     "user_id": "123"
   }
         ↓
2. FastAPI receives request
         ↓
3. FastAPI validates with Pydantic
   ✅ Valid!
         ↓
4. FastAPI sees: db: Session = Depends(get_db)
         ↓
5. FastAPI calls get_db()
   - Creates database session
   - Yields it
         ↓
6. FastAPI passes session to function
   generate_content(request, db)
         ↓
7. Function uses db to save data
   db.add(...)
   db.commit()
         ↓
8. Function returns response
         ↓
9. FastAPI closes database connection
   (automatic cleanup!)
```

---

## Benefits

✅ **Automatic Connection Management**: No manual open/close
✅ **Safe**: One connection per request
✅ **Clean**: Automatic cleanup
✅ **Easy**: Just add `Depends(get_db)` parameter

---

## Ready to Build?

We'll:
1. Update `main.py` with database imports
2. Add health check route
3. Add route that saves to database
4. Test everything works

Let's build it step by step!

