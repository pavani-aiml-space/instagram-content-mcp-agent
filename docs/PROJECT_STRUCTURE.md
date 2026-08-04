# Project Structure & Tech Stack

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **Frontend**: React
- **AI Framework**:  LangGraph, MCP
- **LLM Options**: OpenAI GPT, Google Gemini (Flash/Pro), Local LLM (Ollama), Hugging Face
- **Image Generation**: Stable Diffusion (Local), Hugging Face
- **Image Hosting**: Free server (local server + ngrok/public tunnel)
- **APIs**: Instagram Graph API, Google Trends API

---

## Directory Structure

```
instagramapp/
├── .env                          # Environment variables
├── .gitignore
├── README.md                     # Project overview
├── requirements.txt              # Python dependencies
│
├── backend/                      # FastAPI Backend
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration & settings
│   ├── routes/                  # API routes
│   │   └── content.py           # Content generation endpoints
│   └── models/                  # Pydantic schemas
│       └── schemas.py           # Request/response models (API validation)
│
├── agents/                       # AI Agents (LangGraph)
│   ├── coordinator.py           # Main orchestrator agent
│   ├── content_creator.py       # Content generation agent
│   ├── image_generator.py       # Image generation agent
│   └── base.py                  # Base agent class
│
├── tools/                        # MCP Tools
│   ├── trending_tool.py         # Google Trends API
│   ├── engagement_tool.py      # Instagram analytics
│   ├── format_decision_tool.py  # Format decision logic
│   ├── content_tool.py          # LLM content generation
│   ├── image_tool.py            # Image generation
│   ├── instagram_tool.py        # Instagram posting
│   └── base.py                  # Base tool class
│
├── database/                     # PostgreSQL
│   ├── connection.py           # SQLAlchemy connection
│   ├── models.py                # SQLAlchemy ORM models (database tables)
│   ├── schema.sql               # Database schema
│   └── migrations/              # Alembic migrations
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── App.jsx              # Main component
│   │   ├── components/           # UI components
│   │   │   ├── ContentGenerator.jsx
│   │   │   └── FormatSelector.jsx
│   │   └── index.js
│   ├── public/
│   └── package.json
│
├── config/                       # Configuration files
│   └── default-prompt.txt
│
├── assets/                       # Generated images
│
└── docs/                         # Documentation
    ├── PROJECT_STRUCTURE.md     # This file
    ├── FLOW_DIAGRAM.md          # Complete flow diagram
    ├── QUICK_START_SIMPLE.md    # Quick start guide
    ├── SIMPLE_DECISIONS.md      # Decision logic
    ├── SIMPLE_FLOW.md           # Simplified flow
    └── archive/                 # Old documentation
```

---

## Component Responsibilities

### Backend (`backend/`)
- **Purpose**: HTTP API layer
- **Files**:
  - `main.py`: FastAPI app initialization, CORS, route registration
  - `routes/content.py`: API endpoints (`POST /api/content/generate`)
  - `models/schemas.py`: Pydantic models for validation

### Agents (`agents/`)
- **Purpose**: AI decision-making and orchestration
- **Files**:
  - `coordinator.py`: Main orchestrator, coordinates other agents
  - `content_creator.py`: Generates text content using LangGraph
  - `image_generator.py`: Generates images using LangGraph
  - `base.py`: Shared agent functionality

### Tools (`tools/`)
- **Purpose**: Reusable MCP tools for external APIs
- **Files**:
  - `trending_tool.py`: Google Trends API integration
  - `engagement_tool.py`: Instagram analytics
  - `format_decision_tool.py`: Format decision logic
  - `content_tool.py`: LLM content generation (OpenAI, Gemini, etc.)
  - `image_tool.py`: Image generation (Stable Diffusion, Hugging Face)
  - `instagram_tool.py`: Instagram Graph API posting
  - `base.py`: Base tool class

### Database (`database/`)
- **Purpose**: Data persistence
- **Files**:
  - `connection.py`: SQLAlchemy connection pool
  - `models.py`: ORM models (User, Content, Post, etc.)
  - `schema.sql`: Database schema
  - `migrations/`: Database migrations

### Frontend (`frontend/`)
- **Purpose**: User interface
- **Files**:
  - `src/App.jsx`: Main React component
  - `src/components/`: UI components for content generation

---

## Flow Summary

1. **User Input** → React Frontend
2. **API Request** → FastAPI Backend (`backend/routes/content.py`)
3. **Orchestration** → Coordinator Agent (`agents/coordinator.py`)
4. **Content Generation** → Content Creator Agent (`agents/content_creator.py`)
5. **Image Generation** → Image Generator Agent (`agents/image_generator.py`)
6. **Posting** → Instagram Tool (`tools/instagram_tool.py`)
7. **Storage** → PostgreSQL Database (`database/`)

---

## Key Decisions

- **1-3 Decisions Only**: Topic (required), Format (optional), Posting Time (optional)
- **Everything Else Automatic**: Trending check, content generation, image generation, hashtags, posting
- **Beginner-Friendly**: Start simple, add control as needed

