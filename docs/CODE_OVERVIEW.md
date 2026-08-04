# Code Overview: Instagram Content Generator

## Project Structure

```
instagramapp/
├── agents/                    # Multi-Agent System
├── backend/                   # FastAPI Backend
├── database/                  # Database Models & Connection
├── docs/                      # Documentation
├── frontend/                  # React Frontend
├── scripts/                   # Helper Scripts
├── tests/                     # Test Files
├── tools/                     # MCP Tools
└── requirements.txt           # Python Dependencies
```

## Core Components

### 1. Multi-Agent System (`agents/`)

**Purpose**: Specialized agents that work together to create and post Instagram content

#### Files:
- **`agents/coordinator_agent.py`** - Main orchestrator
  - Coordinates all agents
  - Manages workflow: Content → Image → Post
  - Logs progress for each step
  
- **`agents/content_creator_agent.py`** - Content generation
  - Generates Instagram captions and hashtags
  - Uses OpenAI GPT
  
- **`agents/image_generator_agent.py`** - Image generation
  - Generates images from prompts
  - Uses Stability AI
  
- **`agents/instagram_poster_agent.py`** - Instagram posting
  - Posts content to Instagram
  - Uses Instagram Graph API

**Key Features**:
- Each agent is specialized for one task
- Coordinator orchestrates the workflow
- Progress logging at each step
- Error handling per agent

### 2. MCP Server (`mcp_server/`) + Tool Logic (`tools/`)

**Purpose**: A real MCP server exposing the tools agents call, wrapping the underlying tool logic

#### Files:
- **`mcp_server/instagram_tools_server.py`** - FastMCP server (stdio transport)
  - `generate_content` - Wraps ContentGenerator
  - `generate_image` - Wraps ImageGenerator
  - `post_to_instagram` - Wraps InstagramPoster

- **`tools/content_generator.py`** - Content generation logic
  - Uses OpenAI API
  - Generates captions and hashtags
  
- **`tools/image_generator.py`** - Image generation logic
  - Uses Stability AI API
  - Generates images from prompts
  
- **`tools/instagram_poster.py`** - Instagram posting logic
  - Uses Instagram Graph API
  - Handles media upload and publishing

**Key Features**:
- MCP (Model Context Protocol) pattern
- Standardized interfaces
- Reusable across agents
- Error handling

### 3. Backend API (`backend/`)

**Purpose**: FastAPI REST API server

#### Files:
- **`backend/main.py`** - Main FastAPI application
  - Creates FastAPI app
  - Sets up CORS
  - Includes routers
  - Configures logging
  
- **`backend/routes/content.py`** - Content generation routes
  - `/api/content/generate-and-post` - Full workflow endpoint
  - Handles user lookup
  - Calls coordinator agent
  - Saves to database
  - Returns progress log

- **`backend/models/schemas.py`** - Pydantic models
  - Request validation
  - Response models
  - Progress log models

**Key Features**:
- RESTful API
- Request/response validation
- Database integration
- Progress tracking
- Error handling

### 4. Database (`database/`)

**Purpose**: PostgreSQL database with SQLAlchemy ORM

#### Files:
- **`database/connection.py`** - Database connection
  - SQLAlchemy engine setup
  - Session management
  - Connection testing
  
- **`database/models.py`** - Database models
  - `User` - Instagram accounts
  - `ContentRequest` - Content generation requests
  - `Post` - Posted Instagram content

**Key Features**:
- PostgreSQL database
- SQLAlchemy ORM
- 3 essential tables
- Relationships between models

### 5. Frontend (`frontend/`)

**Purpose**: React web interface

#### Files:
- **`frontend/src/App.jsx`** - Main React component
- **`frontend/src/components/ContentForm.jsx`** - Content form
  - Form inputs (topic, format, user_id)
  - Progress display
  - Results display
  - Error handling
  
- **`frontend/src/components/ContentForm.css`** - Styling
  - Form styles
  - Progress display styles
  - Responsive design
  
- **`frontend/src/services/api.js`** - API client
  - HTTP requests to backend
  - Error handling
  - Response parsing

**Key Features**:
- React components
- Progress tracking UI
- Real-time updates
- Error display

### 6. Scripts (`scripts/`)

**Purpose**: Helper scripts for setup and testing

#### Files:
- **`scripts/get_instagram_credentials.py`** - Get Instagram credentials
- **`scripts/get_instagram_id.py`** - Get Instagram Account ID
- **`scripts/setup_database.py`** - Database setup helper
- **`scripts/test_database_quick.py`** - Quick database test

### 7. Documentation (`docs/`)

**Purpose**: Project documentation

#### Key Files:
- **`docs/MULTI_AGENT_ARCHITECTURE.md`** - Multi-agent system architecture
- **`docs/MCP_AGENT_ARCHITECTURE.md`** - MCP pattern explanation
- **`docs/INSTAGRAM_SETUP_GUIDE.md`** - Instagram setup instructions
- **`docs/DATABASE_SETUP_GUIDE.md`** - Database setup guide
- **`docs/TESTING_GUIDE.md`** - Testing instructions
- **`docs/IMPLEMENTATION_SUMMARY.md`** - Implementation overview

## Data Flow

```
User Input (Frontend)
    ↓
POST /api/content/generate-and-post
    ↓
FastAPI Route (backend/routes/content.py)
    ↓
Coordinator Agent (agents/coordinator_agent.py)
    └─► opens one MCP session (agents/mcp_client.py) against
        mcp_server/instagram_tools_server.py, a real MCP server (stdio)
    ├─► Content Creator Agent (agents/content_creator_agent.py)
    │       └─► generate_content MCP tool (mcp_server/instagram_tools_server.py)
    │               └─► ContentGenerator (tools/content_generator.py)
    │
    ├─► Image Generator Agent (agents/image_generator_agent.py)
    │       └─► generate_image MCP tool (mcp_server/instagram_tools_server.py)
    │               └─► ImageGenerator (tools/image_generator.py)
    │
    └─► Instagram Poster Agent (agents/instagram_poster_agent.py)
            └─► post_to_instagram MCP tool (mcp_server/instagram_tools_server.py)
                    └─► InstagramPoster (tools/instagram_poster.py)
    ↓
Save to Database (database/models.py)
    ↓
Return Response with Progress Log
    ↓
Display in Frontend (frontend/src/components/ContentForm.jsx)
```

## Key Technologies

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **LangGraph** - Agent workflow
- **LangChain** - Tool framework
- **OpenAI** - Content generation
- **Stability AI** - Image generation
- **Instagram Graph API** - Posting

### Frontend
- **React** - UI framework
- **JavaScript/JSX** - Frontend code
- **CSS** - Styling

## Environment Variables

Required in `.env`:
```bash
# OpenAI
OPENAI_API_KEY=your_key

# Stability AI
STABILITY_API_KEY=your_key

# Instagram
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_ACCOUNT_ID=your_account_id

# Database
DATABASE_URL=postgresql://user@localhost:5432/instagram_agents
```

## Main Entry Points

1. **Backend**: `backend/main.py` - Run with `uvicorn backend.main:app --reload`
2. **Frontend**: `frontend/src/App.jsx` - Run with `npm run dev`
3. **Coordinator**: `agents/coordinator_agent.py` - Called by API route
4. **Tools**: `mcp_server/instagram_tools_server.py` - Real MCP server, called by agents via `agents/mcp_client.py`

## File Count Summary

- **Python files**: ~15 files
- **React files**: ~5 files
- **Documentation**: ~10 markdown files
- **Scripts**: ~4 helper scripts
- **Tests**: ~2 test files

## Next Steps

1. Set up environment variables
2. Set up database
3. Start backend server
4. Start frontend
5. Test the workflow

For detailed setup, see:
- `docs/TESTING_GUIDE.md`
- `docs/INSTAGRAM_SETUP_GUIDE.md`
- `docs/DATABASE_SETUP_GUIDE.md`

