# Frontend Setup - React with Vite

## What We Built

A modern React frontend using Vite to test and interact with the FastAPI backend.

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ContentForm.jsx      # Main form component
│   │   └── ContentForm.css      # Form styles
│   ├── services/
│   │   └── api.js               # API service functions
│   ├── App.jsx                  # Main app component
│   ├── App.css                  # App styles
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── package.json                 # Dependencies
└── vite.config.js              # Vite configuration
```

---

## Features

✅ **ContentForm Component**
- Form to test API endpoints
- Two endpoint options:
  - Example endpoint (mock response)
  - Request endpoint (saves to database)
- Real-time validation feedback
- Success/error result display

✅ **API Service**
- Centralized API calls
- Error handling
- Easy to extend

✅ **Modern UI**
- Beautiful gradient background
- Responsive design
- Loading states
- Clear error messages

---

## How to Run

### Step 1: Start Backend Server

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp
source venv/bin/activate
uvicorn backend.main:app --reload
```

Backend runs on: `http://localhost:8000`

### Step 2: Start Frontend Dev Server

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp/frontend
npm run dev
```

Frontend runs on: `http://localhost:5173` (Vite default)

### Step 3: Open in Browser

Visit: `http://localhost:5173`

---

## API Endpoints Tested

### 1. Example Endpoint
- **Route**: `/api/content/generate-example`
- **Purpose**: Mock response (for learning/validation)
- **Does**: Returns example response, doesn't save to database

### 2. Request Endpoint
- **Route**: `/api/content/request`
- **Purpose**: Real functionality
- **Does**: Saves request to database, returns request ID

---

## How It Works

### 1. Form Submission

```javascript
// User fills form and clicks submit
// Form data is collected
const data = {
  topic: "LLM",
  format: "reel",
  user_id: "user_123"
};

// API call is made
const response = await testGenerateExample(data);
```

### 2. API Service

```javascript
// services/api.js
export async function testGenerateExample(data) {
  const response = await fetch('http://localhost:8000/api/content/generate-example', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return response.json();
}
```

### 3. Result Display

- **Success**: Green box with formatted JSON
- **Error**: Red box with error details

---

## CORS Configuration

Backend has CORS middleware configured to allow requests from:
- `http://localhost:3000` (Create React App default)
- `http://localhost:5173` (Vite default)

See `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Scenarios

### Test 1: Valid Request (All Fields)
1. Fill all fields
2. Select "Example Endpoint"
3. Click "Test API Endpoint"
4. ✅ Should see success response

### Test 2: Valid Request (Minimal Fields)
1. Fill only Topic and User ID
2. Leave Format and Posting Time empty
3. Click "Test API Endpoint"
4. ✅ Should see success (uses defaults)

### Test 3: Invalid Request
1. Leave Topic empty
2. Fill User ID
3. Click "Test API Endpoint"
4. ❌ Should see validation error

### Test 4: Database Endpoint
1. Fill all fields
2. Select "Request Endpoint"
3. Click "Test API Endpoint"
4. ✅ Should see request ID (saved to database)

---

## Next Steps

Now that we have a working frontend:

1. **Test the endpoints** - Use the form to test both endpoints
2. **Extend the UI** - Add more features as we build agents
3. **Build Step 4** - Create MCP tools (agents will use them)
4. **Integrate agents** - Connect agents to the frontend

---

## Troubleshooting

### CORS Errors
- Make sure backend CORS middleware is configured
- Check that frontend URL matches allowed origins

### Connection Errors
- Verify backend is running on port 8000
- Check `API_BASE_URL` in `services/api.js`

### Build Errors
- Run `npm install` in frontend directory
- Check Node.js version (should be 18+)

---

**Enjoy testing!** 🎉

