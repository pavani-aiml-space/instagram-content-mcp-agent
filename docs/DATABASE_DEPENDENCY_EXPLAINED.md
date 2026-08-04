# Database Dependency Injection - How It Works

## The Magic: `Depends(get_db)`

**Short answer**: FastAPI automatically provides a database session to your route function.

---

## What You Write

```python
@app.post("/api/content/request")
def create_content_request(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)  # ← This is the magic!
):
    # db is automatically a database session
    db.add(...)
    db.commit()
```

---

## What Happens Behind the Scenes

### Step 1: Request Comes In

```
POST /api/content/request
{
    "topic": "LLM",
    "user_id": "123"
}
```

### Step 2: FastAPI Sees the Dependency

```python
def create_content_request(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)  # ← FastAPI sees this!
):
```

**FastAPI thinks:**
- "Oh! This function needs a database session"
- "I'll call `get_db()` to get one"
- "Then pass it to the function"

### Step 3: FastAPI Calls `get_db()`

```python
# database/connection.py
def get_db():
    db = SessionLocal()  # Create session
    try:
        yield db  # Give it to FastAPI
    finally:
        db.close()  # Close after function finishes
```

**What happens:**
1. Creates database session
2. Yields it (gives it to FastAPI)
3. FastAPI passes it to your function
4. After function finishes, closes connection

### Step 4: Function Runs

```python
def create_content_request(request, db):
    # db is now a real database session!
    db.add(...)  # Use it
    db.commit()  # Save changes
```

### Step 5: Cleanup

After function finishes:
- FastAPI automatically closes database connection
- No memory leaks!
- Connection returned to pool

---

## Visual Flow

```
┌─────────────────────────────────────────┐
│  Request: POST /api/content/request     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  FastAPI sees: db: Session = Depends(...)│
│  "I need to provide a database session!" │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  FastAPI calls: get_db()                │
│  - Creates SessionLocal()               │
│  - Yields database session              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  FastAPI passes session to function:     │
│  create_content_request(request, db)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Function uses db:                      │
│  db.add(...)                            │
│  db.commit()                            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Function returns response              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  FastAPI automatically:                 │
│  - Closes database connection           │
│  - Returns response to user             │
└─────────────────────────────────────────┘
```

---

## Why Use Dependency Injection?

### Without Dependency Injection (Manual)

```python
@app.post("/api/content/request")
def create_content_request(request: ContentGenerateRequest):
    # Manual connection management - error-prone!
    db = SessionLocal()
    try:
        db.add(...)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()  # Easy to forget!
```

**Problems:**
- ❌ Have to remember to close connection
- ❌ Error handling is manual
- ❌ Easy to forget cleanup
- ❌ Repetitive code

### With Dependency Injection (Automatic)

```python
@app.post("/api/content/request")
def create_content_request(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db)
):
    # FastAPI handles everything!
    db.add(...)
    db.commit()
    # Connection automatically closed after function
```

**Benefits:**
- ✅ Automatic cleanup
- ✅ Automatic error handling
- ✅ Less code
- ✅ Can't forget to close

---

## Key Points

1. **`Depends(get_db)`** = "FastAPI, provide me a database session"
2. **Automatic**: FastAPI handles connection creation/cleanup
3. **Safe**: One connection per request
4. **Clean**: No manual connection management needed

---

## Summary

**How it works:**
1. You add `db: Session = Depends(get_db)` parameter
2. FastAPI automatically calls `get_db()`
3. FastAPI provides database session to your function
4. After function finishes, FastAPI closes connection

**The magic**: Just add the parameter, FastAPI does the rest! 🎉

