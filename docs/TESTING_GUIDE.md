# Testing Guide: Multi-Agent System

## ✅ System Status: Ready for Testing

All imports are working and the multi-agent system is ready to test!

## Prerequisites

### 1. Environment Variables

Make sure you have these set in your `.env` file:

```bash
# Required for Content Creator Agent
OPENAI_API_KEY=your_openai_key_here

# Required for Image Generator Agent
STABILITY_API_KEY=your_stability_key_here

# Required for Instagram Poster Agent
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id_here

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/instagramapp
```

**📖 Need help getting Instagram credentials?** See `docs/INSTAGRAM_SETUP_GUIDE.md` for detailed instructions.

### 2. Database Setup

**📖 Full guide**: See `docs/DATABASE_SETUP_GUIDE.md` for detailed instructions.

**Quick setup**:
```bash
# Run the database setup script
source venv/bin/activate
python scripts/setup_database.py
```

This script will:
- ✅ Check database connection
- ✅ Create tables if missing
- ✅ Test CRUD operations
- ✅ Test relationships
- ✅ Verify everything works

**Manual check**:
```bash
# Check if database is accessible
psql -U your_username -d instagram_agents -c "SELECT 1;"
```

**Note**: Database name is `instagram_agents` (not `instagramapp`)

## Testing Steps

### Step 1: Start the Backend Server

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp
source venv/bin/activate
uvicorn backend.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 2: Start the Frontend (Optional)

```bash
cd frontend
npm run dev
# or
npm start
```

### Step 3: Create a Test User

**Option A: Via Frontend**
1. Open http://localhost:3000 (or your frontend URL)
2. Fill in the form with a User ID (e.g., "test_user")
3. Click "Create User" button

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/api/users/create \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "instagram_user_id": "test_user",
    "access_token": "test_token"
  }'
```

### Step 4: Test Individual Agents

#### Test Content Creator Agent

```python
from agents.content_creator_agent import run_content_creator

result = run_content_creator(topic="LLM", format="post")
print(result)
# Expected: {"caption": "...", "hashtags": "...", "status": "completed"}
```

#### Test Image Generator Agent

```python
from agents.image_generator_agent import run_image_generator

result = run_image_generator(
    prompt="A professional image about AI",
    aspect_ratio="1:1"
)
print(result)
# Expected: {"image_url": "...", "status": "completed"}
```

#### Test Instagram Poster Agent

```python
from agents.instagram_poster_agent import run_instagram_poster

result = run_instagram_poster(
    image_url="https://example.com/image.png",
    caption="Test caption",
    instagram_account_id="your_instagram_account_id"
)
print(result)
# Expected: {"post_id": "...", "permalink": "...", "status": "completed"}
```

### Step 5: Test Full Workflow (Coordinator Agent)

#### Via API

```bash
curl -X POST http://localhost:8000/api/content/generate-and-post \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LLM",
    "format": "post",
    "user_id": "test_user",
    "posting_time": "19:00"
  }'
```

#### Via Python

```python
from agents.coordinator_agent import run_coordinator

result = run_coordinator(
    topic="LLM",
    format="post",
    user_id="test_user",
    instagram_account_id="your_instagram_account_id"
)
print(result)
```

#### Via Frontend

1. Open http://localhost:3000
2. Select "Generate & Post (LangGraph Agent)" radio button
3. Fill in:
   - Topic: "LLM"
   - Format: "post" (optional)
   - User ID: "test_user"
4. Click "Generate & Post"
5. Wait for the workflow to complete

## Expected Workflow

When you test the full workflow, you should see:

1. **Content Creator Agent** runs first
   - Generates caption and hashtags
   - Status: "content_created"

2. **Image Generator Agent** runs second
   - Generates image from topic
   - Status: "image_generated"

3. **Instagram Poster Agent** runs third
   - Posts to Instagram
   - Status: "posted"

4. **Database** saves results
   - ContentRequest record created
   - Post record created

5. **Response** returned with:
   - post_id
   - image_url
   - content_preview
   - status: "success"

## Troubleshooting

### Error: "User does not exist"
- **Solution**: Create a user first using Step 3

### Error: "Instagram Account ID not configured"
- **Solution**: Set `INSTAGRAM_ACCOUNT_ID` in your `.env` file

### Error: "OpenAI API key is required"
- **Solution**: Set `OPENAI_API_KEY` in your `.env` file

### Error: "Stability AI API key is required"
- **Solution**: Set `STABILITY_API_KEY` in your `.env` file

### Error: Import errors
- **Solution**: Make sure you're in the virtual environment:
  ```bash
  source venv/bin/activate
  ```

### Error: Database connection failed
- **Solution**: Check PostgreSQL is running and DATABASE_URL is correct

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] Frontend loads (if using)
- [ ] Can create a test user
- [ ] Content Creator Agent works independently
- [ ] Image Generator Agent works independently
- [ ] Instagram Poster Agent works independently
- [ ] Coordinator Agent orchestrates all agents
- [ ] Full workflow completes successfully
- [ ] Data is saved to database
- [ ] Response is returned correctly

## Next Steps After Testing

Once testing is successful:

1. **Add Error Recovery**: Implement retry logic for failed agents
2. **Add Progress Tracking**: Use WebSockets for real-time updates
3. **Add Image Hosting**: Implement ngrok/public tunnel for image URLs
4. **Add Validation**: More input validation and sanitization
5. **Add Logging**: Better logging for debugging

## Support

If you encounter issues:
1. Check the error message carefully
2. Verify all environment variables are set
3. Check the logs in the terminal
4. Review the agent code for any issues

