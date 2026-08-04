# Testing API from Frontend

## New Route: `/test-form`

We've added a simple HTML form page that lets you test the API endpoint directly from your browser!

---

## How to Use

### Step 1: Start the Server

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp
source venv/bin/activate
uvicorn backend.main:app --reload
```

### Step 2: Open in Browser

Visit: **http://localhost:8000/test-form**

You'll see a beautiful form with:
- ✅ Topic field (required)
- ✅ Format dropdown (optional: post, story, reel)
- ✅ Posting Time field (optional)
- ✅ User ID field (required)
- ✅ Submit button

### Step 3: Fill Out the Form

**Example:**
- **Topic**: `LLM`
- **Format**: `reel` (or leave empty)
- **Posting Time**: `19:00` (or leave empty)
- **User ID**: `test_user_123`

### Step 4: Submit

Click "Test API Endpoint" and see the result!

---

## What You'll See

### ✅ Success Response

If the request is valid:
- Green success box appears
- Shows status code: `200 OK`
- Displays the JSON response

**Example Response:**
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

### ❌ Validation Error

If the request is invalid (missing required fields, wrong types):
- Red error box appears
- Shows status code: `422 Unprocessable Entity`
- Displays validation error details

**Example Error:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "topic"],
      "msg": "Field required"
    }
  ]
}
```

---

## Testing Scenarios

### Test 1: Valid Request (All Fields)
- Fill all fields
- Submit
- ✅ Should return success

### Test 2: Valid Request (Minimal Fields)
- Fill only Topic and User ID
- Leave Format and Posting Time empty
- Submit
- ✅ Should return success (uses defaults)

### Test 3: Invalid Request (Missing Topic)
- Fill User ID only
- Leave Topic empty
- Submit
- ❌ Should return validation error

### Test 4: Invalid Request (Missing User ID)
- Fill Topic only
- Leave User ID empty
- Submit
- ❌ Should return validation error

---

## Features

✅ **Beautiful UI**: Modern, responsive design
✅ **Real-time Validation**: See errors immediately
✅ **Formatted JSON**: Pretty-printed responses
✅ **Status Codes**: Clear success/error indicators
✅ **Loading States**: Button shows "Testing..." while processing

---

## How It Works

1. **Form Submission**: JavaScript intercepts form submit
2. **API Call**: Makes POST request to `/api/content/generate-example`
3. **Response Handling**: Displays result in formatted box
4. **Error Handling**: Shows network errors if server is down

---

## Code Location

- **Route**: `backend/main.py` - `@app.get("/test-form")`
- **HTML/CSS/JS**: Embedded in the route (inline for simplicity)

---

## Next Steps

Once you're comfortable testing with the form:
1. Test the `/api/content/request` route (saves to database)
2. Build a React frontend (Step 9)
3. Continue with Step 4: Building MCP Tools

---

**Enjoy testing!** 🎉

