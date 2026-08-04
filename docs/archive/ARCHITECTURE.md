# Instagram MCP AI Content Creator - Complete Architecture Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [End-to-End Data Flow](#end-to-end-data-flow)
5. [API Endpoints](#api-endpoints)
6. [Environment Configuration](#environment-configuration)
7. [Deployment Architecture](#deployment-architecture)
8. [Error Handling & Logging](#error-handling--logging)
9. [Extensibility](#extensibility)

---

## System Overview

The Instagram MCP AI Content Creator is a **modular, AI-powered application** that automates the creation and posting of Instagram content. It follows the **Model-Context-Protocol (MCP)** architecture pattern, enabling clean separation of concerns and easy extensibility.

### Key Capabilities
- **AI Content Generation**: Uses OpenAI GPT-4 to generate captions, ingredients, recipes, and image prompts
- **AI Image Generation**: Uses Stability AI to create food images from text prompts
- **Image Hosting**: Serves images via local Express server with optional S3 or tunnel-based public access
- **Instagram Automation**: Posts generated content to Instagram via Graph API
- **Scheduled Posting**: Cron-based daily posting at 9 AM
- **Web Interface**: User-friendly UI for manual testing and content generation

### Technology Stack
- **Runtime**: Node.js
- **Framework**: Express.js
- **AI Services**: OpenAI API, Stability AI API
- **Social Media**: Instagram Graph API
- **Storage**: Local file system, optional AWS S3
- **Tunneling**: localtunnel/ngrok for public access (free alternative to S3)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Web Browser (localhost:3000)  │  API Clients  │  Cron Scheduler │
└────────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ENTRY POINT LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                    src/server.js                                 │
│  • Express HTTP Server (Port 3000)                              │
│  • Request Routing                                               │
│  • Static File Serving                                           │
│  • Cron Job Management                                           │
│  • Logging (console + file)                                      │
└────────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                      src/agent.js                                │
│  • Workflow Orchestration                                        │
│  • Tool Coordination                                             │
│  • Error Handling & Retry Logic                                 │
│  • Data Transformation                                          │
└───────┬───────────────┬───────────────┬─────────────────────────┘
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  TOOL LAYER   │ │  TOOL LAYER   │ │  TOOL LAYER   │
├───────────────┤ ├───────────────┤ ├───────────────┤
│tools/chatgpt/ │ │tools/image-   │ │tools/         │
│               │ │  generator/   │ │  instagram/   │
│ • OpenAI API  │ │ • Stability   │ │ • Graph API   │
│ • Content Gen │ │   AI API      │ │ • Media Post  │
│ • Parsing     │ │ • Image Gen   │ │ • Publishing  │
│               │ │ • Hosting     │ │               │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
        │                 │                   │
        ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                           │
├─────────────────────────────────────────────────────────────────┤
│  OpenAI API  │  Stability AI  │  Instagram Graph API  │  S3/Tunnel│
└──────────────┴────────────────┴──────────────────────┴──────────┘
```

---

## Component Details

### 1. Entry Point: `src/server.js`

**Purpose**: Main HTTP server and application entry point

**Responsibilities**:
- Initialize Express server on port 3000
- Serve static files from `public/` directory
- Handle HTTP requests and route to appropriate handlers
- Manage cron jobs for scheduled posting
- Log all operations to `server.log`
- Provide REST API endpoints for manual operations

**Key Features**:
- **File Logging**: All console output is duplicated to `server.log`
- **Cron Scheduling**: Daily posts at 9 AM via `node-cron`
- **Multiple Endpoints**: Support for web UI, API, and scheduled jobs

**Ports**:
- `3000`: Main server (HTTP API + Web UI)
- `3001`: Image server (serves generated images)
- `3002`: Instagram service (internal)

### 2. Orchestration: `src/agent.js`

**Purpose**: Central workflow coordinator following MCP pattern

**Responsibilities**:
- Read prompts from `daily_prompt.txt` or accept user input
- Coordinate execution of tool modules in sequence
- Transform data between tool boundaries
- Handle errors and provide meaningful feedback
- Aggregate results from all tools

**Workflow Steps**:
1. **Prompt Acquisition**: Read from file or accept parameter
2. **Content Generation**: Call `generateInstagramContent()`
3. **Image Generation**: Call `generateAndHostImage()`
4. **Instagram Posting**: Call `postToInstagram()`
5. **Result Return**: Return success/failure status

**Error Handling**:
- Each step wrapped in try-catch
- Errors logged with context
- Failures propagate with descriptive messages

### 3. Tool: `tools/chatgpt/index.js`

**Purpose**: AI-powered content generation using OpenAI GPT-4

**Responsibilities**:
- Generate Instagram post content from user prompts
- Create structured output: caption, ingredients, recipe, tips, image prompt
- Parse LLM response into structured format
- Handle API errors and rate limiting

**Input**:
- `userPrompt` (string): Food dish name or description

**Output**:
```javascript
{
  caption: "Instagram caption with hashtags",
  ingredients: "List of ingredients",
  recipe: "Step-by-step recipe",
  tips: "Cooking tips",
  imagePrompt: "Detailed prompt for image generation"
}
```

**API Details**:
- **Model**: `gpt-4-turbo-2024-04-09`
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Endpoint**: `https://api.openai.com/v1/chat/completions`

**Parsing Logic**:
- Extracts structured data from LLM text response
- Handles variations in formatting
- Provides fallbacks for missing sections

### 4. Tool: `tools/image-generator/index.js`

**Purpose**: Generate and host images for Instagram posts

**Responsibilities**:
- Generate images using Stability AI API
- Convert images to JPEG format (required by Instagram)
- Host images via local Express server or AWS S3
- Provide publicly accessible URLs for Instagram

**Components**:

#### 4a. Image Generation (`generateImage`)
- **API**: Stability AI v2beta
- **Format**: JPEG (required by Instagram)
- **Storage**: Local `assets/` directory
- **Naming**: `stability-{timestamp}.jpeg`

#### 4b. Image Hosting (`generateAndHostImage`)
- **Strategy 1 (S3)**: Upload to AWS S3 if credentials available
- **Strategy 2 (Local + Tunnel)**: Serve via Express + public tunnel (free)
- **URL Format**: 
  - S3: `https://{bucket}.s3.amazonaws.com/{key}`
  - Local: `{PUBLIC_IMAGE_SERVER_URL}/assets/{filename}`

**Image Server**:
- Express server on port 3001
- Serves static files from `assets/` directory
- Accessible at `/assets/{filename}`

**Public Access Options**:
1. **AWS S3** (paid): Direct cloud hosting
2. **localtunnel** (free): Public tunnel to local server
3. **ngrok** (free tier): Alternative tunnel service

### 5. Tool: `tools/instagram/index.js`

**Purpose**: Post content to Instagram via Graph API

**Responsibilities**:
- Validate image URL accessibility
- Create media container via Graph API
- Publish media to Instagram account
- Handle authentication errors
- Provide detailed error logging

**API Flow**:
1. **Media Creation**: `POST /{user-id}/media`
   - Parameters: `image_url`, `caption`, `access_token`
   - Returns: `creation_id`

2. **Media Publishing**: `POST /{user-id}/media_publish`
   - Parameters: `creation_id`, `access_token`
   - Returns: Post ID and status

**Validation**:
- Verifies image URL is HTTPS
- Checks image accessibility before posting
- Validates access token format

**Error Handling**:
- Detailed logging of API errors
- Token expiration detection
- Image accessibility verification

---

## End-to-End Data Flow

### Flow 1: Manual Post via Web UI

```
User Input (Browser)
    ↓
[POST /test-instagram-post?prompt="Ragi Dosa"]
    ↓
src/server.js → generateInstagramContent("Ragi Dosa")
    ↓
tools/chatgpt/index.js → OpenAI API
    ↓
Returns: {caption, ingredients, recipe, imagePrompt}
    ↓
src/server.js → generateAndHostImage(imagePrompt)
    ↓
tools/image-generator/index.js → Stability AI API
    ↓
Saves image to assets/stability-{timestamp}.jpeg
    ↓
Serves via Express (port 3001) or uploads to S3
    ↓
Returns: https://tunnel-url/assets/image.jpeg
    ↓
src/server.js → postToInstagram(caption, imageUrl)
    ↓
tools/instagram/index.js → Instagram Graph API
    ↓
1. POST /media (create container)
2. POST /media_publish (publish)
    ↓
Returns: {id: "post_id", ...}
    ↓
Response to Browser: Success + post details
```

### Flow 2: Scheduled Daily Post (Cron)

```
Cron Trigger (9 AM daily)
    ↓
src/server.js → runDailyInstagramPost()
    ↓
src/agent.js → runDailyInstagramPostAgent()
    ↓
Reads config/daily_prompt.txt
    ↓
[Same flow as Flow 1 from here]
    ↓
Logs result to server.log
```

### Flow 3: API Endpoint Post

```
API Client
    ↓
[POST /run-instagram-post]
Body: {prompt: "Dish name"}
    ↓
[Same flow as Flow 1]
    ↓
JSON Response: {caption, imageUrl, ...}
```

---

## API Endpoints

### Main Server (Port 3000)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/` | Web UI for testing | - |
| `GET` | `/test-instagram-post` | Test post generation | `?prompt={dish}` |
| `POST` | `/run-instagram-post` | Generate and post | `{prompt: "dish"}` |
| `POST` | `/generate-instagram-post` | Generate only (no post) | - |
| `POST` | `/set-daily-prompt` | Update daily prompt | `{prompt: "text"}` |
| `POST` | `/run-daily-cron-now` | Trigger cron manually | - |

### Image Server (Port 3001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/assets/{filename}` | Serve generated images |

### Instagram Service (Port 3002)

| Method | Endpoint | Description |
|--------|----------|-------------|
| Internal | N/A | Module only, no HTTP server |

---

## Environment Configuration

### Required Variables

```bash
# OpenAI API (Content Generation)
OPENAI_API_KEY=sk-proj-...

# Stability AI (Image Generation)
STABILITY_API_KEY=sk-...

# Instagram Graph API
INSTAGRAM_ACCESS_TOKEN=EAAQ...
IG_USER_ID=17841474622378736

# Image Hosting (Optional - choose one)
# Option 1: AWS S3
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=your-bucket
AWS_REGION=us-east-1

# Option 2: Public Tunnel (Free)
PUBLIC_IMAGE_SERVER_URL=https://your-tunnel.loca.lt
```

### Optional Variables

```bash
# Server Ports
PORT=3000              # Main server
IMAGE_SERVER_PORT=3001 # Image server
IG_SERVICE_PORT=3002   # Instagram service

# Logging
LOG_LEVEL=info         # Optional log level
```

### Environment Setup Steps

1. **Copy `.env.example` to `.env`** (if exists)
2. **Add API keys** from respective services
3. **Choose image hosting**:
   - **S3**: Add AWS credentials
   - **Tunnel**: Run `npx localtunnel --port 3001` and set `PUBLIC_IMAGE_SERVER_URL`
4. **Get Instagram token**:
   - Use Facebook Graph API Explorer
   - Required permissions: `instagram_basic`, `instagram_content_publish`
5. **Set daily prompt** (optional):
   - Edit `daily_prompt.txt` or use `/set-daily-prompt` endpoint

---

## Deployment Architecture

### Development Setup

```
┌─────────────────────────────────────────┐
│         Developer Machine                │
├─────────────────────────────────────────┤
│  • Node.js Application                   │
│  • Express Servers (3000, 3001, 3002)   │
│  • localtunnel (port 3001)               │
│  • Cron Jobs                             │
└─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│         External APIs                   │
├─────────────────────────────────────────┤
│  • OpenAI API                            │
│  • Stability AI API                       │
│  • Instagram Graph API                    │
└─────────────────────────────────────────┘
```

### Production Considerations

1. **Image Hosting**:
   - Use AWS S3 for reliability
   - Or deploy image server with public domain
   - Avoid tunnels in production

2. **Token Management**:
   - Implement token refresh for Instagram
   - Use secrets management (AWS Secrets Manager, etc.)
   - Rotate tokens regularly

3. **Error Monitoring**:
   - Add error tracking (Sentry, etc.)
   - Set up alerts for failures
   - Monitor API rate limits

4. **Scaling**:
   - Use process managers (PM2, systemd)
   - Consider containerization (Docker)
   - Load balancing for multiple instances

5. **Security**:
   - Never commit `.env` files
   - Use environment-specific configs
   - Implement rate limiting
   - Add authentication for API endpoints

---

## Error Handling & Logging

### Logging Strategy

**File Logging**:
- All logs written to `server.log`
- Format: `[LOG]` or `[ERROR]` prefix
- Includes timestamps and context

**Console Logging**:
- Real-time output for development
- Mirrored to file via custom logger

### Error Types & Handling

1. **API Errors**:
   - **OpenAI**: Rate limits, invalid keys → Logged, retried if possible
   - **Stability AI**: API errors → Logged, fallback options
   - **Instagram**: Token expiration → Detailed error, user notification

2. **Network Errors**:
   - Timeout handling (10s for image verification)
   - Retry logic (can be added)
   - Connection failures logged

3. **Validation Errors**:
   - Missing environment variables → Startup failure
   - Invalid image URLs → Pre-flight checks
   - Missing prompts → Default values or errors

### Error Response Format

```javascript
{
  error: "Error message",
  stack: "Stack trace (development)",
  status: 400,
  details: {
    api: "instagram",
    code: "OAuthException",
    message: "Token expired"
  }
}
```

---

## Extensibility

### Adding New Tools

1. **Create Tool Module**:
   ```javascript
   // new-tool/index.js
   async function newToolFunction(input) {
     // Tool logic
     return result;
   }
   module.exports = { newToolFunction };
   ```

2. **Register in Agent**:
   ```javascript
   // agent.js
   const { newToolFunction } = require('./new-tool');
   // Use in workflow
   ```

3. **Add to Server** (if needed):
   ```javascript
   // server.js
   const { newToolFunction } = require('./new-tool');
   app.post('/new-endpoint', async (req, res) => {
     const result = await newToolFunction(req.body.input);
     res.json(result);
   });
   ```

### Extending Workflows

**Add Pre-Posting Steps**:
- Image editing/optimization
- Content validation
- Hashtag optimization
- Analytics tracking

**Add Post-Posting Steps**:
- Cross-platform posting (Twitter, Facebook)
- Analytics collection
- Engagement tracking
- Notification systems

### Integration Examples

1. **Database Storage**:
   - Store generated content
   - Track posting history
   - Analytics database

2. **Notification System**:
   - Email/SMS on success/failure
   - Slack/Discord webhooks
   - Push notifications

3. **Content Management**:
   - Content approval workflow
   - A/B testing
   - Scheduling system

4. **Analytics**:
   - Post performance tracking
   - Engagement metrics
   - Content optimization

---

## File Structure

```
instagramapp/
├── src/                      # Main application source
│   ├── server.js            # Express server
│   ├── agent.js             # Agent orchestration
│   └── index.js             # Entry point
│
├── tools/                    # Tool modules (MCP servers)
│   ├── chatgpt/             # Content generation
│   │   ├── index.js
│   │   └── package.json
│   ├── image-generator/     # Image generation
│   │   ├── index.js
│   │   ├── s3-upload.js
│   │   └── package.json
│   └── instagram/           # Instagram posting
│       ├── index.js
│       └── package.json
│
├── scripts/                  # Utility scripts
│   ├── setup-tunnel.sh
│   ├── run-tunnel.sh
│   └── install-deps.sh
│
├── tests/                    # Test files
│   ├── test-instagram-post.js
│   ├── test-s3-upload.js
│   └── test-stability-image.js
│
├── config/                   # Configuration files
│   ├── daily_prompt.txt
│   └── post-reel.mcp.json
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── QUICK_START_PLAN.md
│
├── assets/                    # Generated assets
│   └── stability-*.jpeg
│
├── public/                    # Static web files
│   └── index.html
│
├── logs/                     # Log files
│   └── server.log
│
├── tmp/                      # Temporary files
│
├── node_modules/             # Dependencies
│
├── .env                      # Environment variables
├── package.json              # Package config
└── README.md                 # Main readme
```

---

## Summary

This architecture provides:

✅ **Modularity**: Clean separation of concerns via MCP pattern  
✅ **Extensibility**: Easy to add new tools and workflows  
✅ **Reliability**: Comprehensive error handling and logging  
✅ **Flexibility**: Multiple deployment and hosting options  
✅ **Developer Experience**: Clear structure, good documentation  
✅ **Production Ready**: Scalable, secure, maintainable  

The system successfully automates the entire Instagram content creation pipeline from prompt to published post, with robust error handling and multiple hosting options for different use cases.
