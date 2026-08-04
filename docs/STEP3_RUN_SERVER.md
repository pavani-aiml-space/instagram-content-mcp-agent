# Step 3: Running and Testing the Server

## How to Run the FastAPI Server

### Method 1: Using Python (Simple)
```bash
# Activate virtual environment
source venv/bin/activate

# Run the server
python backend/main.py
```

**What happens:**
- Python executes `backend/main.py`
- The `if __name__ == "__main__"` block runs
- Uvicorn starts the server
- Server listens on `http://localhost:8000`

---

### Method 2: Using Uvicorn Directly (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Run with uvicorn
uvicorn backend.main:app --reload
```

**What `--reload` does:**
- Automatically restarts server when code changes
- Great for development!
- **Don't use in production**

**Breakdown:**
- `uvicorn` = The server
- `backend.main:app` = "Use the `app` from `backend/main.py`"
- `--reload` = Auto-reload on changes

---

## What You'll See

When the server starts, you'll see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**What this means:**
- ✅ Server is running
- ✅ Listening on port 8000
- ✅ Ready to receive requests

---

## How to Test the Server

### Test 1: Visit in Browser (Easiest)

1. **Open browser**
2. **Go to**: `http://localhost:8000/`
3. **You should see**: JSON response
   ```json
   {
     "message": "Welcome to Instagram Content Generator API!",
     "status": "running"
   }
   ```

**What's happening:**
- Browser makes GET request to `/`
- FastAPI receives it
- Runs `read_root()` function
- Returns JSON
- Browser displays it

---

### Test 2: Auto-Generated API Documentation

FastAPI automatically creates interactive API docs!

1. **Go to**: `http://localhost:8000/docs`
2. **You'll see**: Swagger UI (interactive API documentation)
3. **Try it**: Click "Try it out" → "Execute"
4. **See response**: The JSON response

**Why this is amazing:**
- ✅ No need to write documentation manually
- ✅ Can test API directly from browser
- ✅ Shows all available endpoints
- ✅ Shows request/response formats

---

### Test 3: Alternative Docs (ReDoc)

1. **Go to**: `http://localhost:8000/redoc`
2. **You'll see**: Beautiful alternative documentation

---

### Test 4: Using curl (Command Line)

```bash
# Test root endpoint
curl http://localhost:8000/

# Expected output:
# {"message":"Welcome to Instagram Content Generator API!","status":"running"}
```

**What curl does:**
- Makes HTTP requests from command line
- `curl` = Client URL (tool for making requests)

---

### Test 5: Using Python requests

```python
import requests

# Make GET request
response = requests.get("http://localhost:8000/")

# Print response
print(response.status_code)  # Should be 200
print(response.json())       # Should be our JSON
```

---

## Understanding HTTP Status Codes

When you make a request, you get a status code:

- **200 OK**: Success! Request worked
- **404 Not Found**: URL doesn't exist
- **500 Internal Server Error**: Server error (bug in code)

**Our endpoint should return**: `200 OK`

---

## Common Issues & Solutions

### Issue: "Address already in use"
**Problem**: Port 8000 is already taken
**Solution**: 
```bash
# Use a different port
uvicorn backend.main:app --reload --port 8001
```

### Issue: "Module not found"
**Problem**: Virtual environment not activated
**Solution**: 
```bash
source venv/bin/activate
```

### Issue: "Connection refused"
**Problem**: Server not running
**Solution**: Start the server first!

---

## What to Look For

✅ Server starts without errors
✅ Can visit `http://localhost:8000/` in browser
✅ See JSON response
✅ Can visit `http://localhost:8000/docs`
✅ See interactive API documentation

---

## Next Steps After Testing

Once server is running and tested:
1. ✅ We know FastAPI works
2. ✅ We can make HTTP requests
3. ✅ Ready to add more routes
4. ✅ Ready to add request/response models

---

Ready to run it? Let's do it step by step!

