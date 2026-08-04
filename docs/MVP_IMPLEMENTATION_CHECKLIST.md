# MVP Implementation Checklist

This is a practical checklist for implementing the MVP of the agentic Instagram post generation workflow.

## Quick Start Guide

### Prerequisites
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed (for frontend)
- [ ] PostgreSQL installed (or SQLite for MVP)
- [ ] API keys:
  - [ ] OpenAI API key
  - [ ] Stability AI API key
  - [ ] Instagram Graph API access token
  - [ ] Instagram Business Account ID

---

## Phase 1: Foundation Setup

### 1.1 Project Structure
```
instagramapp/
├── agents/              # Agent implementations
├── backend/             # FastAPI backend
├── database/            # Database models and migrations
├── frontend/           # React frontend
├── tools/              # Utility tools
├── tests/              # Test files
├── docs/               # Documentation
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md          # Project overview
```

- [ ] Create project directory structure
- [ ] Initialize Git repository
- [ ] Create `.gitignore`
- [ ] Create `README.md` with setup instructions

### 1.2 Python Environment
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Create `requirements.txt` with dependencies
- [ ] Install dependencies: `pip install -r requirements.txt`

### 1.3 Environment Configuration
- [ ] Create `.env.example` template
- [ ] Create `.env` file (add to `.gitignore`)
- [ ] Add all required environment variables
- [ ] Document environment variables in README

### 1.4 Database Setup
- [ ] Install PostgreSQL (or use SQLite for MVP)
- [ ] Create database
- [ ] Set up SQLAlchemy connection
- [ ] Create database models:
  - [ ] User model
  - [ ] Post model
  - [ ] WorkflowLog model
- [ ] Set up Alembic for migrations
- [ ] Create initial migration
- [ ] Run migration

---

## Phase 2: Core Agents

### 2.1 Content Creator Agent

**File**: `agents/content_creator_agent.py`

- [ ] Create agent class/structure
- [ ] Implement topic analysis function
- [ ] Set up OpenAI API client
- [ ] Create prompt templates:
  - [ ] Caption generation prompt
  - [ ] Hashtag generation prompt
- [ ] Implement caption generation:
  - [ ] Call OpenAI API
  - [ ] Parse response
  - [ ] Format for Instagram
- [ ] Implement hashtag generation:
  - [ ] Extract relevant hashtags
  - [ ] Format hashtags
- [ ] Add content validation:
  - [ ] Check caption length (max 2200 chars)
  - [ ] Validate hashtag count (max 30)
- [ ] Add error handling
- [ ] Write unit tests

**Test Cases:**
- [ ] Test with recipe topic
- [ ] Test with informational topic
- [ ] Test with empty topic (should error)
- [ ] Test with very long topic details
- [ ] Test API failure handling

### 2.2 Image Generator Agent

**File**: `agents/image_generator_agent.py`

- [ ] Create agent class/structure
- [ ] Implement prompt building from content:
  - [ ] Extract key concepts from caption
  - [ ] Build image generation prompt
  - [ ] Add style guidance
- [ ] Set up Stability AI API client
- [ ] Implement image generation:
  - [ ] Call Stability AI API
  - [ ] Receive base64 image
  - [ ] Decode image
- [ ] Implement image validation:
  - [ ] Check image format
  - [ ] Check image dimensions (min 320x320)
  - [ ] Validate file size
- [ ] Set up image storage:
  - [ ] Create `assets/` directory
  - [ ] Save image with unique filename
  - [ ] Generate public URL
- [ ] Set up image server (simple HTTP server or ngrok)
- [ ] Add error handling
- [ ] Write unit tests

**Test Cases:**
- [ ] Test image generation with valid prompt
- [ ] Test with invalid prompt (should handle gracefully)
- [ ] Test image saving and URL generation
- [ ] Test API failure handling
- [ ] Test image validation

### 2.3 Instagram Poster Agent

**File**: `agents/instagram_poster_agent.py`

- [ ] Create agent class/structure
- [ ] Set up Instagram Graph API client
- [ ] Implement image URL validation:
  - [ ] Check URL is accessible
  - [ ] Verify image format
- [ ] Implement media container creation:
  - [ ] POST to `/media` endpoint
  - [ ] Handle response
  - [ ] Extract creation_id
- [ ] Implement media publishing:
  - [ ] Wait for container to be ready
  - [ ] POST to `/media_publish` endpoint
  - [ ] Extract post_id and permalink
- [ ] Add error handling:
  - [ ] Handle rate limits
  - [ ] Handle invalid image URLs
  - [ ] Handle API errors
- [ ] Write unit tests

**Test Cases:**
- [ ] Test successful post creation
- [ ] Test with invalid image URL
- [ ] Test with inaccessible image
- [ ] Test API rate limit handling
- [ ] Test API error handling

---

## Phase 3: Workflow Orchestration

### 3.1 Workflow Coordinator

**File**: `agents/coordinator_agent.py`

- [ ] Set up LangGraph workflow
- [ ] Define state schema (TypedDict)
- [ ] Create workflow nodes:
  - [ ] `content_creator_node`
  - [ ] `image_generator_node`
  - [ ] `instagram_poster_node`
- [ ] Implement state transitions
- [ ] Add progress logging:
  - [ ] Log each step start
  - [ ] Log each step completion
  - [ ] Log errors
- [ ] Implement error handling:
  - [ ] Catch exceptions in each node
  - [ ] Update state with error messages
  - [ ] Stop workflow on critical errors
- [ ] Add retry logic (optional for MVP)
- [ ] Write integration tests

**Test Cases:**
- [ ] Test complete successful workflow
- [ ] Test workflow with content creation failure
- [ ] Test workflow with image generation failure
- [ ] Test workflow with Instagram posting failure
- [ ] Test state transitions

### 3.2 API Integration

**File**: `backend/routes/posts.py`

- [ ] Create FastAPI route for post generation:
  - [ ] `POST /api/v1/posts/generate`
- [ ] Implement request validation (Pydantic models)
- [ ] Implement user lookup
- [ ] Call workflow coordinator
- [ ] Save results to database
- [ ] Format response
- [ ] Add error handling
- [ ] Write API tests

**File**: `backend/main.py`

- [ ] Set up FastAPI app
- [ ] Configure CORS
- [ ] Add routes
- [ ] Add middleware
- [ ] Add health check endpoint

**Test Cases:**
- [ ] Test API endpoint with valid request
- [ ] Test with invalid request (validation)
- [ ] Test with non-existent user
- [ ] Test error responses
- [ ] Test database persistence

---

## Phase 4: Frontend

### 4.1 React Setup

- [ ] Initialize React app (Vite)
- [ ] Install dependencies
- [ ] Set up project structure
- [ ] Configure build tools

### 4.2 UI Components

**File**: `frontend/src/components/PostGenerator.jsx`

- [ ] Create form component:
  - [ ] Topic input field
  - [ ] Topic details textarea (optional)
  - [ ] Submit button
- [ ] Add form validation
- [ ] Add loading states
- [ ] Add error display
- [ ] Add success display:
  - [ ] Show generated caption
  - [ ] Show generated image
  - [ ] Show Instagram post link
- [ ] Style components

### 4.3 API Integration

**File**: `frontend/src/services/api.js`

- [ ] Create API service
- [ ] Implement `generatePost()` function
- [ ] Add error handling
- [ ] Add request/response interceptors

### 4.4 Progress Tracking

- [ ] Implement progress display:
  - [ ] Show current step
  - [ ] Show progress log
  - [ ] Update in real-time (polling or WebSocket)

---

## Phase 5: Testing & Polish

### 5.1 Unit Tests
- [ ] Content Creator Agent tests
- [ ] Image Generator Agent tests
- [ ] Instagram Poster Agent tests
- [ ] Workflow Coordinator tests
- [ ] API route tests

### 5.2 Integration Tests
- [ ] End-to-end workflow test
- [ ] API integration test
- [ ] Database integration test

### 5.3 Manual Testing
- [ ] Test complete flow with real APIs
- [ ] Test error scenarios
- [ ] Test with different topics
- [ ] Verify Instagram posts are created correctly

### 5.4 Documentation
- [ ] Update README with setup instructions
- [ ] Document API endpoints
- [ ] Document environment variables
- [ ] Create user guide
- [ ] Document known issues/limitations

---

## MVP Completion Criteria

Before considering MVP complete, verify:

- [ ] User can input a topic and generate a post
- [ ] Content is generated and formatted correctly
- [ ] Image is generated and matches content
- [ ] Post is successfully published to Instagram
- [ ] All errors are handled gracefully
- [ ] Progress is logged and visible
- [ ] Database records are created
- [ ] Basic tests are passing
- [ ] Documentation is complete

---

## Quick Reference: File Structure

```
instagramapp/
├── agents/
│   ├── __init__.py
│   ├── coordinator_agent.py      # Workflow orchestrator
│   ├── content_creator_agent.py   # Content generation
│   ├── image_generator_agent.py   # Image generation
│   └── instagram_poster_agent.py  # Instagram posting
│
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── routes/
│   │   └── posts.py               # API routes
│   └── models/
│       └── schemas.py             # Pydantic models
│
├── database/
│   ├── __init__.py
│   ├── connection.py              # DB connection
│   └── models.py                  # SQLAlchemy models
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   └── PostGenerator.jsx
│   │   └── services/
│   │       └── api.js
│   └── package.json
│
├── tools/
│   └── (utility functions)
│
├── tests/
│   ├── test_agents/
│   ├── test_api/
│   └── test_integration/
│
├── .env
├── requirements.txt
└── README.md
```

---

## Common Issues & Solutions

### Issue: Image URL not accessible
**Solution**: Ensure image server is running and publicly accessible (use ngrok)

### Issue: Instagram API rate limits
**Solution**: Implement rate limiting and retry logic with exponential backoff

### Issue: Content too long
**Solution**: Add validation to truncate or split content

### Issue: Image generation fails
**Solution**: Add fallback to alternative image provider

---

## Next Steps After MVP

1. Add content scheduling
2. Add content approval workflow
3. Add multiple account support
4. Add analytics and insights
5. Add content templates
6. Add A/B testing capabilities

---

**Last Updated**: 2024-01-15



