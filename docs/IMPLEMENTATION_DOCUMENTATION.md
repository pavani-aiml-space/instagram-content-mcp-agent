# Instagram App Implementation Documentation

## Overview

This document describes the complete implementation of the Instagram automated posting system, including the multi-agent architecture, content generation, image generation, and end-to-end flow.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [What We've Built](#what-weve-built)
3. [Agent Architecture](#agent-architecture)
4. [Content Generation](#content-generation)
5. [Image Generation](#image-generation)
6. [End-to-End Flow](#end-to-end-flow)
7. [Key Features](#key-features)
8. [Configuration](#configuration)

---

## Architecture Overview

The system uses a **multi-agent architecture** built with LangGraph, where specialized agents handle different aspects of content creation:

```
┌─────────────────────────────────────────────────────────────┐
│                    Coordinator Agent                         │
│              (Orchestrates the entire flow)                  │
└───────────────┬─────────────────────────────────────────────┘
                │
                ├─────────────────┬─────────────────┬──────────────┐
                │                 │                 │              │
                ▼                 ▼                 ▼              ▼
    ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Content Creator  │ │ Image         │ │ Instagram    │ │ Database     │
    │ Agent            │ │ Generator     │ │ Poster       │ │ Storage      │
    │                  │ │ Agent         │ │ Agent        │ │              │
    └──────────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

## What We've Built

### 1. **Multi-Agent System**
   - **Coordinator Agent**: Orchestrates the entire workflow
   - **Content Creator Agent**: Generates Instagram captions and hashtags
   - **Image Generator Agent**: Creates images from prompts
   - **Instagram Poster Agent**: Posts content to Instagram

### 2. **Content Generation**
   - **Recipe Detection**: Automatically detects recipe topics and formats content accordingly
   - **Engineering Topics**: Formats technical/educational content with bullet points and step-by-step explanations
   - **Smart Formatting**: Removes unwanted headings and markdown, keeps essential structure

### 3. **Image Generation**
   - **Stability AI Integration**: Primary image generation provider
   - **OpenAI Fallback**: Optional fallback to OpenAI DALL-E
   - **No Text Overlay**: Clean images without text overlay (text only in Instagram caption)
   - **Anti-Infographic**: Explicitly avoids infographic/diagram styles

### 4. **Instagram Integration**
   - **Graph API**: Posts images and captions to Instagram
   - **Database Storage**: Saves all posts to database for tracking

---

## Agent Architecture

### Coordinator Agent (`agents/coordinator_agent.py`)

The main orchestrator that coordinates all agents in sequence.

**Responsibilities:**
- Receives topic and optional topic details
- Calls Content Creator Agent
- Calls Image Generator Agent
- Calls Instagram Poster Agent
- Manages state and error handling
- Logs progress at each step

**State Management:**
```python
class CoordinatorState(TypedDict):
    topic: str
    topic_details: str
    caption: str
    bullets: list
    hashtags: str
    image_url: str
    instagram_post_id: str
    status: str
    error: str
    progress_log: list
```

### Content Creator Agent (`agents/content_creator_agent.py`)

Generates Instagram-optimized captions and hashtags.

**Features:**
- **Recipe Detection**: Automatically detects recipe topics
- **Dual Format Support**:
  - **Recipes**: Intro → Hashtags → Ingredients → Recipe steps
  - **Engineering**: Intro → Bullet Points → Step-by-Step → Hashtags
- **Clean Output**: Removes markdown formatting, keeps only essential headings

**Output Structure:**

**For Recipes:**
```
[1-2 catchy intro lines]
[Hashtags]
Ingredients:
- [ingredient list]
Recipe:
1. [Step 1]
2. [Step 2]
...
```

**For Engineering Topics:**
```
[Introduction paragraph]
• [Bullet point 1] - [Explanation]
• [Bullet point 2] - [Explanation]
...
1. [Step 1 with detailed explanation]
2. [Step 2 with detailed explanation]
...
[Hashtags]
```

### Image Generator Agent (`agents/image_generator_agent.py`)

Generates images from captions, topics, and content.

**Features:**
- Builds prompts from caption, topic, and topic_details
- Prioritizes caption as main description
- Uses Stability AI by default (OpenAI as fallback)
- Generates clean images without text overlay
- Explicitly avoids infographic styles

**Prompt Building:**
```python
def _build_image_prompt(state):
    # Priority: Use caption if available
    if caption:
        prompt = caption
        if topic_details and topic_details not in caption:
            prompt = f"{prompt}, {topic_details}"
    elif base_topic:
        prompt = base_topic
        if topic_details:
            prompt = f"{prompt}, {topic_details}"
    return prompt
```

### Instagram Poster Agent (`agents/instagram_poster_agent.py`)

Posts generated content to Instagram using Graph API.

**Features:**
- Uploads image to Instagram
- Posts with generated caption
- Returns Instagram post ID
- Handles API errors gracefully

---

## Content Generation

### Recipe Detection

The system automatically detects recipe topics using keyword matching:

```python
recipe_keywords = [
    'recipe', 'cooking', 'dish', 'food', 'cuisine', 'ingredient',
    'bake', 'baking', 'cook', 'meal', 'pie', 'cake', 'soup', etc.
]
```

### Content Formatting

**Recipe Format:**
- ✅ 1-2 catchy intro lines (no "Intro:" heading)
- ✅ Hashtags (no "Hashtags:" heading)
- ✅ **Ingredients:** heading (kept)
- ✅ Ingredients list
- ✅ **Recipe:** heading (kept)
- ✅ Numbered recipe steps
- ✅ No markdown formatting (`**`, `##`)

**Engineering Format:**
- ✅ Introduction paragraph
- ✅ Bullet points with explanations
- ✅ Detailed step-by-step explanation
- ✅ Hashtags
- ✅ No section headings
- ✅ No markdown formatting

---

## Image Generation

### Provider Configuration

**Default:** Stability AI
- Set via `IMAGE_PROVIDER=stability` (default)
- Or `IMAGE_PROVIDER=openai` for OpenAI

### Image Generation Process

1. **Prompt Building**: Combines caption, topic, and topic_details
2. **Style Guidance**: Adds instructions to avoid infographics
3. **Negative Prompts** (Stability AI): Explicitly excludes infographic styles
4. **Generation**: Creates clean, photographic images
5. **Storage**: Saves to `assets/` directory with public URL

### Anti-Infographic Measures

**Prompt Enhancement:**
```python
style_guidance = ", professional photography, realistic image, high quality, Instagram-worthy, not an infographic or diagram"
```

**Negative Prompts (Stability AI):**
```
"infographic, diagram, flowchart, chart, recipe card, instruction manual, 
step-by-step guide layout, text-heavy, boxes with arrows, numbered steps layout"
```

---

## End-to-End Flow

### Step-by-Step Flow: From Button Click to Instagram Post

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          STEP 1: USER INTERACTION                                    │
│                                                                                       │
│  User fills out form in React frontend (ContentForm.jsx):                           │
│  • Topic: "Pumpkin Pie"                                                              │
│  • Topic Details: (optional)                                                         │
│  • Format: "post"                                                                    │
│  • User ID: "user_123"                                                              │
│                                                                                       │
│  User clicks "Generate & Post" button                                                │
│  └─► Triggers handleSubmit() event handler                                          │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 2: FRONTEND API CALL                                         │
│                                                                                       │
│  ContentForm.jsx → handleSubmit()                                                    │
│  │                                                                                   │
│  ├─► setLoading(true)                                                               │
│  ├─► setProgress([{ step: "0", agent: "System", status: "starting" }])             │
│  │                                                                                   │
│  └─► Calls: generateAndPost(data) from api.js                                       │
│      │                                                                               │
│      └─► HTTP POST Request:                                                         │
│          URL: http://localhost:8000/api/content/generate-and-post                  │
│          Method: POST                                                                │
│          Headers: { "Content-Type": "application/json" }                             │
│          Body: {                                                                    │
│            "topic": "Pumpkin Pie",                                                  │
│            "topic_details": "",                                                     │
│            "format": "post",                                                        │
│            "user_id": "user_123"                                                    │
│          }                                                                           │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Request (via fetch API)
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 3: BACKEND API RECEIVES REQUEST                              │
│                                                                                       │
│  FastAPI Server (main.py) - Port 8000                                                │
│  │                                                                                   │
│  ├─► CORS Middleware validates origin (localhost:3000, localhost:5173)              │
│  │                                                                                   │
│  └─► Route Handler: POST /api/content/generate-and-post                             │
│      Location: backend/routes/content.py                                            │
│      Function: generate_and_post()                                                   │
│      │                                                                               │
│      ├─► Step 3.1: Pydantic Validation                                              │
│      │   • Validates request body against ContentGenerateRequest schema             │
│      │   • Ensures required fields (topic, user_id) are present                     │
│      │                                                                               │
│      ├─► Step 3.2: Database User Lookup                                            │
│      │   • Queries User table: db.query(User).filter(...)                           │
│      │   • Looks for user by user_id or instagram_user_id                           │
│      │   • If not found → HTTP 400 error                                            │
│      │                                                                               │
│      ├─► Step 3.3: Get Instagram Account ID                                         │
│      │   • Retrieves INSTAGRAM_ACCOUNT_ID from environment variables               │
│      │   • If not set → HTTP 400 error                                              │
│      │                                                                               │
│      └─► Step 3.4: Call Coordinator Agent                                           │
│          │                                                                           │
│          └─► run_coordinator(                                                       │
│                topic=request.topic,                                                 │
│                format=request.format,                                              │
│                user_id=str(user.id),                                               │
│                instagram_account_id=instagram_account_id,                           │
│                topic_details=request.topic_details                                  │
│              )                                                                       │
│              Location: agents/coordinator_agent.py                                  │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Function call: run_coordinator()
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 4: COORDINATOR AGENT STARTS                                 │
│                                                                                       │
│  Coordinator Agent (agents/coordinator_agent.py)                                    │
│  Framework: LangGraph StateGraph                                                     │
│  │                                                                                   │
│  ├─► Creates initial state:                                                          │
│  │   {                                                                               │
│  │     topic: "Pumpkin Pie",                                                        │
│  │     topic_details: "",                                                           │
│  │     format: "post",                                                              │
│  │     user_id: "user_123",                                                         │
│  │     instagram_account_id: "123456789",                                           │
│  │     caption: "",                                                                 │
│  │     bullets: [],                                                                 │
│  │     hashtags: "",                                                                │
│  │     image_url: "",                                                               │
│  │     post_id: "",  # Will contain Instagram post ID                             │
│  │     permalink: "",                                                               │
│  │     status: "starting",                                                          │
│  │     error: "",                                                                   │
│  │     current_step: "",                                                            │
│  │     progress_log: []                                                             │
│  │   }                                                                               │
│  │                                                                                   │
│  └─► Invokes workflow: workflow.invoke(initial_state)                               │
│      │                                                                               │
│      └─► Workflow executes nodes in sequence:                                        │
│          │                                                                           │
│          ├─► Node 1: call_content_creator_node()                                     │
│          │   │                                                                       │
│          │   └─► Calls: run_content_creator()                                       │
│          │       Location: agents/content_creator_agent.py                          │
│          │                                                                           │
│          ├─► Node 2: call_image_generator_node()                                     │
│          │   │                                                                       │
│          │   └─► Calls: run_image_generator()                                       │
│          │       Location: agents/image_generator_agent.py                          │
│          │                                                                           │
│          └─► Node 3: call_instagram_poster_node()                                    │
│              │                                                                       │
│              └─► Calls: run_instagram_poster()                                       │
│                  Location: agents/instagram_poster_agent.py                          │
│                                                                                       │
│      Note: Workflow uses sequential edges:                                          │
│      • content_creator → image_generator → instagram_poster → END                    │
│      • Each node passes state to the next                                           │
│      • Errors in any node stop the workflow                                         │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Workflow execution
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│              STEP 5: CONTENT CREATOR AGENT (Node 1)                                   │
│                                                                                       │
│  Content Creator Agent (agents/content_creator_agent.py)                             │
│  │                                                                                   │
│  ├─► Creates workflow: create_content_creator_workflow()                            │
│  │                                                                                   │
│  ├─► Invokes: generate_content_node(state)                                         │
│  │   │                                                                               │
│  │   └─► Calls tool: generate_content_tool.invoke({                                 │
│  │         topic: state["topic"],                                                   │
│  │         format: state["format"],                                                 │
│  │         topic_details: state["topic_details"]                                    │
│  │       })                                                                          │
│  │       Location: mcp_server/instagram_tools_server.py (MCP tool)                   │
│  │                                                                                   │
│  └─► Tool calls: ContentGenerator.generate()                                        │
│      Location: tools/content_generator.py                                           │
│      │                                                                               │
│      ├─► Detects topic type: _is_recipe_topic()                                     │
│      │   • Checks for keywords: recipe, cooking, dish, food, bake, etc.             │
│      │   • Result: is_recipe = True                                                 │
│      │                                                                               │
│      ├─► Builds prompt for recipe format                                            │
│      │   • Intro (1-2 lines)                                                        │
│      │   • Hashtags                                                                 │
│      │   • Ingredients: heading                                                      │
│      │   • Recipe: heading                                                           │
│      │                                                                               │
│      ├─► Calls OpenAI API:                                                          │
│      │   POST https://api.openai.com/v1/chat/completions                           │
│      │   Model: gpt-4o-mini                                                          │
│      │   Messages: [system, user prompts]                                            │
│      │   │                                                                           │
│      │   └─► Returns: { choices: [{ message: { content: "..." } }] }              │
│      │                                                                               │
│      ├─► Parses response: _parse_recipe_content()                                   │
│      │   • Removes markdown (**, ##)                                                │
│      │   • Removes unwanted headings (Intro:, Hashtags:)                            │
│      │   • Keeps Ingredients: and Recipe: headings                                  │
│      │   • Extracts hashtags                                                        │
│      │                                                                               │
│      └─► Returns: {                                                                 │
│            caption: "Get ready to indulge...\n#pumpkinpie...\nIngredients:\n...",   │
│            bullets: [],                                                              │
│            hashtags: "#pumpkinpie #fallbaking..."                                   │
│          }                                                                           │
│                                                                                       │
│  State Updated:                                                                      │
│  { caption: "...", bullets: [], hashtags: "..." }                                   │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ State passed to next node
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│              STEP 6: IMAGE GENERATOR AGENT (Node 2)                                  │
│                                                                                       │
│  Image Generator Agent (agents/image_generator_agent.py)                            │
│  │                                                                                   │
│  ├─► Creates workflow: create_image_generator_workflow()                            │
│  │                                                                                   │
│  ├─► Invokes: generate_image_node(state)                                            │
│  │   │                                                                               │
│  │   ├─► Builds prompt: _build_image_prompt(state)                                 │
│  │   │   • Uses caption as primary (from Step 5)                                    │
│  │   │   • Adds topic_details if not in caption                                    │
│  │   │   • Result: "Get ready to indulge in the ultimate fall classic!..."         │
│  │   │                                                                               │
│  │   └─► Calls tool: generate_image_tool.invoke({                                  │
│  │         prompt: image_prompt,                                                    │
│  │         aspect_ratio: "1:1",                                                     │
│  │         caption: state["caption"],                                               │
│  │         bullets: state["bullets"],                                               │
│  │         topic_details: state["topic_details"]                                    │
│  │       })                                                                          │
│  │       Location: mcp_server/instagram_tools_server.py (MCP tool)                   │
│  │                                                                                   │
│  └─► Tool calls: ImageGenerator.generate()                                         │
│      Location: tools/image_generator.py                                            │
│      │                                                                               │
│      ├─► Enhances prompt with style guidance:                                      │
│      │   "..., professional photography, realistic image,                           │
│      │    high quality, Instagram-worthy, not an infographic or diagram"            │
│      │                                                                               │
│      ├─► Calls Stability AI API:                                                    │
│      │   POST https://api.stability.ai/v1/generation/.../text-to-image             │
│      │   Headers: { Authorization: "Bearer STABILITY_API_KEY" }                    │
│      │   Body: {                                                                   │
│      │     text_prompts: [                                                          │
│      │       { text: enhanced_prompt, weight: 1.0 },                               │
│      │       { text: negative_prompt, weight: -1.0 }                               │
│      │     ],                                                                       │
│      │     cfg_scale: 8,                                                           │
│      │     width: 1024,                                                            │
│      │     height: 1024,                                                           │
│      │     samples: 1                                                              │
│      │   }                                                                          │
│      │   │                                                                           │
│      │   └─► Returns: { artifacts: [{ base64: "..." }] }                          │
│      │                                                                               │
│      ├─► Decodes base64 image data                                                  │
│      │                                                                               │
│      ├─► Saves to assets/ directory:                                                │
│      │   • Filename: aiimg-{timestamp}-{seed}.png                                  │
│      │   • Path: assets/aiimg-20250116123456-12345.png                             │
│      │   • Saved locally on server                                                  │
│      │                                                                               │
│      ├─► Generates public URL:                                                      │
│      │   • Base: PUBLIC_IMAGE_SERVER_URL from .env                                  │
│      │   • Example: https://5458e8598a69.ngrok-free.app                            │
│      │   • Full URL: https://5458e8598a69.ngrok-free.app/assets/aiimg-...png      │
│      │   • Note: Image server must be running on port 8002 with ngrok tunnel       │
│      │                                                                               │
│      └─► Returns: {                                                                 │
│            image_url: "https://.../assets/aiimg-...png",                           │
│            image_base64: "...",                                                      │
│            seed: 12345                                                               │
│          }                                                                           │
│                                                                                       │
│  State Updated:                                                                      │
│  { image_url: "https://.../assets/aiimg-...png" }                                   │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ State passed to next node
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│              STEP 7: INSTAGRAM POSTER AGENT (Node 3)                                  │
│                                                                                       │
│  Instagram Poster Agent (agents/instagram_poster_agent.py)                          │
│  │                                                                                   │
│  ├─► Creates workflow: create_instagram_poster_workflow()                           │
│  │                                                                                   │
│  ├─► Invokes: post_to_instagram_node(state)                                         │
│  │   │                                                                               │
│  │   └─► Calls tool: post_to_instagram_tool.invoke({                                │
│  │         image_url: state["image_url"],                                           │
│  │         caption: state["caption"],                                               │
│  │         instagram_account_id: state["instagram_account_id"]                      │
│  │       })                                                                          │
│  │       Location: mcp_server/instagram_tools_server.py (MCP tool)                   │
│  │                                                                                   │
│  └─► Tool calls: InstagramPoster.post_image()                                       │
│      Location: tools/instagram_poster.py                                           │
│      │                                                                               │
│      ├─► Validates image URL is publicly accessible:                               │
│      │   • HEAD request to image_url                                                │
│      │   • Checks status code 200                                                  │
│      │                                                                               │
│      ├─► Step 7.1: Create Media Container                                           │
│      │   POST https://graph.facebook.com/v18.0/{account_id}/media                   │
│      │   Params: {                                                                  │
│      │     image_url: "https://.../assets/aiimg-...png",                           │
│      │     caption: "Get ready to indulge...\nIngredients:\n...",                  │
│      │     access_token: INSTAGRAM_ACCESS_TOKEN                                      │
│      │   }                                                                          │
│      │   │                                                                           │
│      │   └─► Returns: { id: "creation_id_123456" }                                 │
│      │                                                                               │
│      ├─► Wait 2 seconds (for container to be ready)                                 │
│      │                                                                               │
│      ├─► Step 7.2: Publish Media                                                    │
│      │   POST https://graph.facebook.com/v18.0/{account_id}/media_publish          │
│      │   Params: {                                                                  │
│      │     creation_id: "creation_id_123456",                                       │
│      │     access_token: INSTAGRAM_ACCESS_TOKEN                                      │
│      │   }                                                                          │
│      │   │                                                                           │
│      │   └─► Returns: {                                                             │
│      │         id: "instagram_post_id_123456789"                                   │
│      │       }                                                                       │
│      │                                                                               │
│      └─► Returns: {                                                                 │
│            post_id: "instagram_post_id_123456789",                                  │
│            permalink: "https://www.instagram.com/p/123456789/",                     │
│            status: "success"                                                        │
│          }                                                                           │
│                                                                                       │
│  State Updated:                                                                      │
│  { post_id: "instagram_post_id_123456789", permalink: "...", status: "posted" }    │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Final state returned
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 8: COORDINATOR RETURNS RESULT                                │
│                                                                                       │
│  Coordinator Agent completes workflow                                                │
│  │                                                                                   │
│  └─► Returns final state dictionary:                                               │
│      {                                                                               │
│        caption: "Get ready to indulge...",                                         │
│        bullets: [],                                                                 │
│        hashtags: "#pumpkinpie #fallbaking...",                                      │
│        image_url: "https://.../assets/aiimg-...png",                               │
│        post_id: "instagram_post_id_123456789",  # Instagram post ID                │
│        permalink: "https://www.instagram.com/p/123456789/",                        │
│        status: "posted",  # Final status from coordinator                          │
│        error: "",                                                                   │
│        current_step: "instagram_posting",                                          │
│        progress_log: [                                                              │
│          { step: "1", agent: "Content Creator", status: "completed", ... },        │
│          { step: "2", agent: "Image Generator", status: "completed", ... },         │
│          { step: "3", agent: "Instagram Poster", status: "completed", ... }         │
│        ]                                                                             │
│      }                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Return to route handler
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 9: BACKEND SAVES TO DATABASE                                  │
│                                                                                       │
│  Route Handler (backend/routes/content.py) - continued                               │
│  │                                                                                   │
│  ├─► Step 9.1: Save ContentRequest                                                  │
│  │   db_request = ContentRequest(                                                  │
│  │     topic="Pumpkin Pie",                                                        │
│  │     format="post",                                                              │
│  │     user_id=user.id,                                                            │
│  │     status="completed"                                                          │
│  │   )                                                                              │
│  │   db.add(db_request)                                                            │
│  │   db.commit()                                                                    │
│  │                                                                                   │
│  ├─► Step 9.2: Save Post Record                                                    │
│  │   db_post = Post(                                                               │
│  │     request_id=db_request.id,                                                    │
│  │     instagram_post_id=result["post_id"],  # From coordinator result           │
│  │     format="post",                                                              │
│  │     image_url=result["image_url"],                                             │
│  │     caption=result["caption"],                                                  │
│  │     hashtags=[tag.strip("#") for tag in result["hashtags"].split()            │
│  │               if tag.startswith("#")]                                          │
│  │   )                                                                              │
│  │   db.add(db_post)                                                               │
│  │   db.commit()                                                                    │
│  │                                                                                   │
│  └─► Step 9.3: Build Response                                                      │
│      return ContentGenerateResponse(                                                │
│        status="success",                                                            │
│        post_id=result["post_id"],  # Instagram post ID from coordinator            │
│        format="post",                                                               │
│        posted_at="now",                                                            │
│        content_preview=result["caption"][:100] + "...",                            │
│        image_url=result["image_url"],                                              │
│        message=f"Successfully posted to Instagram! Post ID: {result['post_id']}", │
│        progress_log=result.get("progress_log", [])                                │
│      )                                                                              │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Response (JSON)
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    STEP 10: FRONTEND RECEIVES RESPONSE                               │
│                                                                                       │
│  api.js → handleResponse()                                                           │
│  │                                                                                   │
│  ├─► Parses JSON response                                                           │
│  │                                                                                   │
│  └─► Returns to ContentForm.jsx                                                     │
│      │                                                                               │
│      └─► handleSubmit() continues:                                                  │
│          │                                                                           │
│          ├─► setLoading(false)                                                      │
│          ├─► setProgress(response.progress_log)                                     │
│          ├─► setResult(response)                                                   │
│          │                                                                           │
│          └─► UI Updates:                                                            │
│              • Displays success message                                             │
│              • Shows progress log with all steps                                     │
│              • Displays image preview (from image_url)                               │
│              • Shows Instagram post link (from permalink)                           │
│              • Displays full response JSON                                          │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ✅ POST SUCCESSFULLY CREATED ON INSTAGRAM
```

### Complete System Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    FRONTEND LAYER                                    │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  React Application (Vite + React)                                            │   │
│  │  Location: frontend/src/                                                     │   │
│  │                                                                               │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐  │   │
│  │  │  ContentForm.jsx Component                                             │  │   │
│  │  │  ──────────────────────────────────────────────────────────────────── │  │   │
│  │  │  • User fills form: topic, topic_details, format, user_id            │  │   │
│  │  │  • User clicks "Generate & Post" button                               │  │   │
│  │  │  • Shows progress updates in real-time                                │  │   │
│  │  │  • Displays success/error results                                     │  │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘  │   │
│  │                          │                                                   │   │
│  │                          │ handleSubmit()                                    │   │
│  │                          ▼                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐  │   │
│  │  │  api.js Service Layer                                                  │  │   │
│  │  │  ──────────────────────────────────────────────────────────────────── │  │   │
│  │  │  • generateAndPost(data) function                                      │  │   │
│  │  │  • Makes HTTP POST request to backend                                  │  │   │
│  │  │  • Handles response/error parsing                                      │  │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘  │   │
│  │                          │                                                   │   │
│  │                          │ HTTP POST                                        │   │
│  │                          │ /api/content/generate-and-post                   │   │
│  └──────────────────────────┼───────────────────────────────────────────────────┘   │
│                             │                                                       │
│                             │ JSON Payload:                                        │
│                             │ { topic, topic_details, format, user_id }          │
└─────────────────────────────┼───────────────────────────────────────────────────────┘
                              │
                              │ HTTP Request (CORS enabled)
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    BACKEND LAYER                                     │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  FastAPI Server (main.py)                                                   │   │
│  │  Location: backend/main.py                                                  │   │
│  │  Port: 8000                                                                 │   │
│  │                                                                               │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐  │   │
│  │  │  CORS Middleware                                                        │  │   │
│  │  │  • Allows requests from localhost:3000, localhost:5173                 │  │   │
│  │  └───────────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                               │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐  │   │
│  │  │  Route: POST /api/content/generate-and-post                           │  │   │
│  │  │  Location: backend/routes/content.py                                  │  │   │
│  │  │  ──────────────────────────────────────────────────────────────────── │  │   │
│  │  │  1. Receives request with Pydantic validation                         │  │   │
│  │  │  2. Looks up user in database (User model)                            │  │   │
│  │  │  3. Validates Instagram account ID                                    │  │   │
│  │  │  4. Calls run_coordinator() to start multi-agent workflow            │  │   │
│  │  │  5. Saves results to database                                         │  │   │
│  │  │  6. Returns response with post details                                │  │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘  │   │
│  │                          │                                                   │   │
│  │                          │ run_coordinator()                                 │   │
│  │                          ▼                                                   │   │
│  └──────────────────────────┼───────────────────────────────────────────────────┘   │
│                             │                                                       │
└─────────────────────────────┼───────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              MULTI-AGENT ORCHESTRATION                              │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  Coordinator Agent (coordinator_agent.py)                                   │   │
│  │  Location: agents/coordinator_agent.py                                      │   │
│  │  Framework: LangGraph StateGraph                                            │   │
│  │  ────────────────────────────────────────────────────────────────────────── │   │
│  │                                                                               │   │
│  │  Initial State:                                                              │   │
│  │  { topic, topic_details, format, user_id, instagram_account_id, ... }       │   │
│  │                                                                               │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Step 1: Content Creator Agent                                         │ │   │
│  │  │  ──────────────────────────────────────────────────────────────────── │ │   │
│  │  │  Agent: agents/content_creator_agent.py                               │ │   │
│  │  │  Tool: mcp_server.instagram_tools_server.generate_content (MCP tool)  │ │   │
│  │  │  Implementation: tools/content_generator.py                            │ │   │
│  │  │                                                                         │ │   │
│  │  │  Process:                                                              │ │   │
│  │  │  1. Detect topic type (recipe vs engineering)                          │ │   │
│  │  │     • Recipe keywords: recipe, cooking, dish, food, bake, etc.        │ │   │
│  │  │  2. Generate content based on type:                                    │ │   │
│  │  │     • Recipe: Intro → Hashtags → Ingredients → Recipe                  │ │   │
│  │  │     • Engineering: Intro → Bullets → Step-by-Step → Hashtags          │ │   │
│  │  │  3. Call OpenAI GPT-4o-mini API                                        │ │   │
│  │  │  4. Parse response, remove markdown, clean headings                     │ │   │
│  │  │  5. Extract: caption, bullets, hashtags                                │ │   │
│  │  │                                                                         │ │   │
│  │  │  State Update:                                                          │ │   │
│  │  │  { caption: "...", bullets: [...], hashtags: "..." }                  │ │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘ │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Step 2: Image Generator Agent                                         │ │   │
│  │  │  ──────────────────────────────────────────────────────────────────── │ │   │
│  │  │  Agent: agents/image_generator_agent.py                               │ │   │
│  │  │  Tool: mcp_server.instagram_tools_server.generate_image (MCP tool)    │ │   │
│  │  │  Implementation: tools/image_generator.py                             │ │   │
│  │  │                                                                         │ │   │
│  │  │  Process:                                                              │ │   │
│  │  │  1. Build prompt from caption + topic + topic_details                  │ │   │
│  │  │     • Prioritizes caption as main description                          │ │   │
│  │  │  2. Add style guidance:                                                │ │   │
│  │  │     "professional photography, realistic image,                       │ │   │
│  │  │      not an infographic or diagram"                                    │ │   │
│  │  │  3. Generate image via Stability AI API (default)                     │ │   │
│  │  │     • Provider: Stability AI (or OpenAI as fallback)                  │ │   │
│  │  │     • Negative prompts: infographic, diagram, flowchart, etc.         │ │   │
│  │  │  4. Receive base64 image data                                          │ │   │
│  │  │  5. Save to assets/ directory with timestamp                          │ │   │
│  │  │  6. Generate public URL (via PUBLIC_IMAGE_SERVER_URL)                 │ │   │
│  │  │                                                                         │ │   │
│  │  │  State Update:                                                          │ │   │
│  │  │  { image_url: "https://.../assets/aiimg-...png" }                     │ │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘ │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Step 3: Instagram Poster Agent                                       │ │   │
│  │  │  ──────────────────────────────────────────────────────────────────── │ │   │
│  │  │  Agent: agents/instagram_poster_agent.py                              │ │   │
│  │  │  Tool: mcp_server.instagram_tools_server.post_to_instagram (MCP tool) │ │   │
│  │  │  Implementation: tools/instagram_poster.py                            │ │   │
│  │  │                                                                         │ │   │
│  │  │  Process:                                                              │ │   │
│  │  │  1. Validate image URL is publicly accessible                          │ │   │
│  │  │  2. Create media container via Instagram Graph API:                   │ │   │
│  │  │     POST /{account_id}/media                                            │ │   │
│  │  │     • image_url: public image URL                                      │ │   │
│  │  │     • caption: generated caption text                                  │ │   │
│  │  │  3. Wait 2 seconds for container to be ready                          │ │   │
│  │  │  4. Publish media container:                                           │ │   │
│  │  │     POST /{account_id}/media_publish                                   │ │   │
│  │  │     • creation_id: from step 2                                         │ │   │
│  │  │  5. Receive Instagram post ID                                         │ │   │
│  │  │                                                                         │ │   │
│  │  │  State Update:                                                          │ │   │
│  │  │  { post_id: "123456789", permalink: "...", status: "posted" }        │ │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘ │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Final State                                                          │ │   │
│  │  │  { topic, caption, bullets, hashtags, image_url,                     │ │   │
│  │  │    post_id, permalink, status: "posted", progress_log }              │ │   │
│  │  └───────────────────────┬───────────────────────────────────────────────┘ │   │
│  │                          │                                                   │   │
│  │                          │ Return result to route handler                  │   │
│  └──────────────────────────┼───────────────────────────────────────────────────┘   │
│                             │                                                       │
└─────────────────────────────┼───────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  DATABASE LAYER                                      │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  Database Operations (backend/routes/content.py)                            │   │
│  │  Database: SQLite/PostgreSQL (via SQLAlchemy ORM)                            │   │
│  │  Location: database/models.py                                                │   │
│  │  ────────────────────────────────────────────────────────────────────────── │   │
│  │                                                                               │   │
│  │  1. Save ContentRequest record:                                              │   │
│  │     • topic, format, posting_time, user_id, status="completed"              │   │
│  │                                                                               │   │
│  │  2. Save Post record:                                                        │   │
│  │     • request_id (FK to ContentRequest)                                     │   │
│  │     • instagram_post_id                                                      │   │
│  │     • format, image_url, caption, hashtags                                  │   │
│  │                                                                               │   │
│  │  3. Commit transaction                                                       │   │
│  └───────────────────────┬───────────────────────────────────────────────────────┘   │
│                          │                                                           │
│                          │ Return response                                           │
│                          ▼                                                           │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Response
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  RESPONSE TO FRONTEND                                 │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  JSON Response                                                              │   │
│  │  {                                                                           │   │
│  │    "status": "success",                                                      │   │
│  │    "post_id": "instagram_post_id_123456789",  # Instagram post ID           │   │
│  │    "format": "post",                                                         │   │
│  │    "posted_at": "now",                                                      │   │
│  │    "content_preview": "Get ready to indulge...",                            │   │
│  │    "image_url": "https://ngrok-url.com/assets/aiimg-...png",               │   │
│  │    "message": "Successfully posted to Instagram! Post ID: ...",            │   │
│  │    "progress_log": [                                                         │   │
│  │      {                                                                       │   │
│  │        "step": "1",                                                          │   │
│  │        "agent": "Content Creator",                                          │   │
│  │        "status": "completed",                                                │   │
│  │        "message": "Generating content for topic: Pumpkin Pie"                │   │
│  │      },                                                                      │   │
│  │      {                                                                       │   │
│  │        "step": "2",                                                          │   │
│  │        "agent": "Image Generator",                                           │   │
│  │        "status": "completed",                                                │   │
│  │        "message": "Generated image: https://..."                             │   │
│  │      },                                                                      │   │
│  │      {                                                                       │   │
│  │        "step": "3",                                                          │   │
│  │        "agent": "Instagram Poster",                                          │   │
│  │        "status": "completed",                                                │   │
│  │        "message": "Posted to Instagram! Post ID: ..."                       │   │
│  │      }                                                                       │   │
│  │    ]                                                                         │   │
│  │  }                                                                           │   │
│  └───────────────────────┬───────────────────────────────────────────────────────┘   │
│                          │                                                           │
│                          │ Update UI                                                  │
│                          ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  Frontend Updates                                                           │   │
│  │  • Display success message                                                  │   │
│  │  • Show progress log                                                        │   │
│  │  • Display image preview                                                    │   │
│  │  • Show Instagram post link                                                 │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ External API Calls
                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL SERVICES                                        │
│                                                                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │  OpenAI API          │  │  Stability AI API     │  │  Instagram Graph API │   │
│  │  ────────────────────│  │  ────────────────────│  │  ────────────────────│   │
│  │  • Content Generation│  │  • Image Generation   │  │  • Media Container   │   │
│  │  • GPT-4o-mini       │  │  • Stable Diffusion   │  │  • Media Publish    │   │
│  │  • Returns: caption  │  │  • Returns: base64   │  │  • Returns: post_id  │   │
│  │    + hashtags       │  │    image data         │  │    + permalink       │   │
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Component Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          COMPONENT INTERACTIONS                               │
└──────────────────────────────────────────────────────────────────────────────┘

Frontend (React)
    │
    │ HTTP POST /api/content/generate-and-post
    │ { topic, topic_details, format, user_id }
    │
    ▼
Backend FastAPI Route Handler
    │
    │ 1. Validate request (Pydantic)
    │ 2. Query database for User
    │ 3. Get Instagram account ID
    │
    ▼
Coordinator Agent (LangGraph)
    │
    ├─► Content Creator Agent
    │   │
    │   ├─► Content Generator Tool
    │   │   │
    │   │   ├─► OpenAI API (GPT-4o-mini)
    │   │   │   └─► Returns: caption, bullets, hashtags
    │   │   │
    │   │   └─► Parse & Clean Content
    │   │       └─► Remove markdown, headings
    │   │
    │   └─► Update State: { caption, bullets, hashtags }
    │
    ├─► Image Generator Agent
    │   │
    │   ├─► Image Generator Tool
    │   │   │
    │   │   ├─► Build Prompt (caption + topic + details)
    │   │   │
    │   │   ├─► Stability AI API
    │   │   │   ├─► Generate image
    │   │   │   └─► Returns: base64 image
    │   │   │
    │   │   ├─► Save to assets/ directory
    │   │   │   └─► Generate public URL (via PUBLIC_IMAGE_SERVER_URL)
    │   │   │   └─► Image server on port 8002 (exposed via ngrok)
    │   │   │
    │   │   └─► Return: image_url
    │   │
    │   └─► Update State: { image_url }
    │
    └─► Instagram Poster Agent
        │
        ├─► Instagram Poster Tool
        │   │
        │   ├─► Validate image URL accessibility
        │   │
        │   ├─► Instagram Graph API
        │   │   ├─► POST /{account_id}/media
        │   │   │   └─► Create media container
        │   │   │       └─► Returns: creation_id
        │   │   │
        │   │   ├─► Wait 2 seconds
        │   │   │
        │   │   └─► POST /{account_id}/media_publish
        │   │       └─► Publish media
        │   │           └─► Returns: post_id, permalink
    │   │
    │   └─► Return: post_id (Instagram post ID)
    │
    └─► Update State: { post_id, permalink, status: "posted" }

    │
    ▼
Backend Route Handler (continued)
    │
    ├─► Save ContentRequest to database
    ├─► Save Post to database
    └─► Return response to frontend
        │
        ▼
Frontend (React)
    │
    ├─► Display success message
    ├─► Show progress log
    ├─► Display image preview
    └─► Show Instagram post link
```

### Detailed Flow with State

```
Initial State:
{
    topic: "Pumpkin Pie",
    topic_details: "",
    format: "post",
    user_id: "user_123",
    instagram_account_id: "123456789",
    caption: "",
    bullets: [],
    hashtags: "",
    image_url: "",
    post_id: "",
    permalink: "",
    status: "starting",
    error: "",
    current_step: "",
    progress_log: []
}

    │
    ▼
[Content Creator Agent]
    │
    ├─> Detect: is_recipe = True
    ├─> Generate recipe-format caption
    ├─> Parse and clean output
    │
    ▼
State Updated:
{
    caption: "Get ready to indulge...\n#pumpkinpie...\nIngredients:\n- ...\nRecipe:\n1. ...",
    bullets: [],
    hashtags: "#pumpkinpie #fallbaking..."
}

    │
    ▼
[Image Generator Agent]
    │
    ├─> Build prompt from caption
    ├─> Add style guidance
    ├─> Generate image (Stability AI)
    ├─> Save to assets/
    │
    ▼
State Updated:
{
    image_url: "https://.../assets/aiimg-...png",
    status: "image_generated"
}

    │
    ▼
[Instagram Poster Agent]
    │
    ├─> Validate image URL accessibility
    ├─> Create media container (POST /{account_id}/media)
    ├─> Wait 2 seconds
    ├─> Publish media (POST /{account_id}/media_publish)
    │
    ▼
State Updated:
{
    post_id: "123456789",  # Instagram post ID
    permalink: "https://www.instagram.com/p/123456789/",
    status: "posted"
}

    │
    ▼
[Database Storage]
    │
    ├─> Save ContentRequest record
    ├─> Save Post record (with instagram_post_id from result["post_id"])
    │
    ▼
Final Response:
{
    status: "success",
    post_id: "123456789",  # Instagram post ID (not database ID)
    format: "post",
    posted_at: "now",
    content_preview: "Get ready to indulge...",
    image_url: "https://.../assets/aiimg-...png",
    message: "Successfully posted to Instagram! Post ID: 123456789",
    progress_log: [...]
}
```

---

## Infrastructure Requirements

### Image Server Setup

The system requires a publicly accessible image server for Instagram posting:

1. **Image Server**: Runs on port 8002, serves files from `assets/` directory
   - Start with: `python scripts/start_image_server.py`
   - Or use: `./scripts/start_image_server_and_ngrok.sh`

2. **Ngrok Tunnel**: Exposes local image server to the internet
   - Required for Instagram API to access images
   - Free tier requires browser verification (Instagram API can bypass this)
   - Set `PUBLIC_IMAGE_SERVER_URL` in `.env` to the ngrok URL

3. **Image URLs**: Generated images are saved locally and served via:
   - Local: `http://localhost:8002/assets/aiimg-...png`
   - Public: `https://ngrok-url.com/assets/aiimg-...png`

---

## Key Features

### 1. **Smart Content Formatting**
   - Automatically detects recipe vs. engineering topics
   - Formats content appropriately for each type
   - Removes unwanted headings and markdown
   - Keeps essential structure (Ingredients, Recipe headings)

### 2. **Clean Image Generation**
   - No text overlay on images
   - Photographic style (not infographic)
   - Professional, Instagram-worthy output
   - Explicit anti-infographic measures

### 3. **Multi-Provider Support**
   - Stability AI (default)
   - OpenAI DALL-E (fallback)
   - Configurable via environment variable

### 4. **Error Handling**
   - Graceful error handling at each step
   - Detailed error messages
   - Progress logging
   - State preservation

### 5. **Database Integration**
   - Stores all posts
   - Tracks metadata
   - Enables post history

---

## Configuration

### Environment Variables

```bash
# OpenAI (for content generation)
OPENAI_API_KEY=your_openai_key

# Stability AI (for image generation)
STABILITY_API_KEY=your_stability_key

# Image Provider (optional, default: stability)
IMAGE_PROVIDER=stability  # or "openai"

# Instagram
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
INSTAGRAM_ACCOUNT_ID=your_account_id

# Image Server (for public image URLs)
# Image server runs on port 8002, exposed via ngrok
PUBLIC_IMAGE_SERVER_URL=https://your-ngrok-url.com
# To start: ./scripts/start_image_server_and_ngrok.sh
```

### File Structure

```
instagramapp/
├── agents/
│   ├── coordinator_agent.py      # Main orchestrator
│   ├── content_creator_agent.py  # Content generation
│   ├── image_generator_agent.py  # Image generation
│   └── instagram_poster_agent.py # Instagram posting
├── tools/
│   ├── content_generator.py      # Content generation logic
│   ├── image_generator.py        # Image generation logic
│   └── schemas.py                 # ContentSchema for structured LLM output
mcp_server/
│   └── instagram_tools_server.py  # Real MCP server (stdio) - generate_content, generate_image, post_to_instagram
├── backend/
│   ├── main.py                   # FastAPI server
│   └── routes/
│       └── content.py            # API routes
├── database/
│   ├── connection.py             # DB connection
│   └── models.py                 # DB models
└── assets/                       # Generated images
```

---

## API Usage

### Endpoint: `POST /api/content/generate-and-post`

**Request:**
```json
{
    "topic": "Pumpkin Pie",
    "topic_details": "A classic fall dessert recipe"
}
```

**Response:**
```json
{
    "status": "success",
    "post_id": "123",
    "instagram_post_id": "123456789",
    "image_url": "https://.../assets/aiimg-...png",
    "caption": "Get ready to indulge...\n#pumpkinpie...\nIngredients:\n- ...\nRecipe:\n1. ...",
    "hashtags": "#pumpkinpie #fallbaking..."
}
```

---

## Recent Changes Summary

### Removed Features
- ❌ Text overlay on images
- ❌ ByteByteGo infographic style
- ❌ Unused text-based image generation functions
- ❌ Unused font loading functions

### Added Features
- ✅ Recipe detection and formatting
- ✅ Engineering topic formatting
- ✅ Clean image generation (no overlay)
- ✅ Anti-infographic measures
- ✅ Stability AI as default provider

### Improved Features
- ✅ Better prompt building (prioritizes caption)
- ✅ Cleaner content output (removes unwanted headings)
- ✅ Better error handling
- ✅ Progress logging

---

## Future Enhancements

1. **Content Scheduling**: Schedule posts for specific times
2. **Multiple Accounts**: Support multiple Instagram accounts
3. **Content Templates**: Pre-defined content templates
4. **Analytics**: Track post performance
5. **A/B Testing**: Test different content formats
6. **Image Variations**: Generate multiple image options
7. **Content Approval**: Manual approval workflow

---

## Troubleshooting

### Images Still Look Like Infographics
- Check that `IMAGE_PROVIDER=stability` is set
- Verify negative prompts are being applied
- Check prompt doesn't contain infographic keywords

### Content Formatting Issues
- Verify recipe detection is working (check keywords)
- Check that markdown is being removed
- Verify heading removal logic

### Image Generation Fails
- Check API keys are set
- Verify `PUBLIC_IMAGE_SERVER_URL` is accessible
- Check Stability AI API quota

---

## Conclusion

This implementation provides a complete, automated Instagram posting system with:
- Smart content generation (recipe vs. engineering)
- Clean image generation (no infographics)
- Multi-agent architecture
- Full Instagram integration
- Database tracking

The system is production-ready and can be extended with additional features as needed.

