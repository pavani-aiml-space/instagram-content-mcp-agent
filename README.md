# Instagram Content Generator

A multi-agent app that generates and posts Instagram content from a topic: an LLM writes the caption, an image model generates the visual, and the post goes live via the Instagram Graph API. Built with **FastAPI**, **LangChain**, and a real **MCP (Model Context Protocol) server**.

---

## Architecture

```
React Frontend (frontend/)
    ↓
FastAPI Backend (backend/): POST /api/content/generate-and-post
    ↓
Coordinator Agent (agents/coordinator_agent.py): LangChain LCEL chain
    ↓ opens one MCP session (agents/mcp_client.py)
mcp_server/instagram_tools_server.py: a real MCP server (stdio transport)
    ├─ generate_content   → tools/content_generator.py (ChatOpenAI, structured output)
    ├─ generate_image     → tools/image_generator.py (Stability AI / OpenAI Images)
    └─ post_to_instagram  → tools/instagram_poster.py (Instagram Graph API)
```

The three agents (`agents/content_creator_agent.py`, `agents/image_generator_agent.py`, `agents/instagram_poster_agent.py`) each call one MCP tool over a real client/server boundary, not an in-process function call. The Coordinator Agent chains them with LangChain Expression Language (LCEL, the `|` operator) rather than a graph framework, the flow is strictly linear (content → image → post), and each step gets `.with_retry()` for free, retrying once on a transient API failure before recording it.

Requests and generated posts are persisted via SQLAlchemy (`database/`) to Postgres.

📖 See [docs/CODE_OVERVIEW.md](docs/CODE_OVERVIEW.md) and [docs/MULTI_AGENT_ARCHITECTURE.md](docs/MULTI_AGENT_ARCHITECTURE.md) for more detail.

---

## Setup

1. **Create a virtualenv and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**: create a `.env` file in the project root with:
   - `OPENAI_API_KEY`: content generation
   - `STABILITY_API_KEY`: image generation (default provider)
   - `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_ACCOUNT_ID`: Instagram Graph API (see [docs/INSTAGRAM_SETUP_GUIDE.md](docs/INSTAGRAM_SETUP_GUIDE.md))
   - `DATABASE_URL`: Postgres connection string
   - `PUBLIC_IMAGE_SERVER_URL`: public URL for generated images (Instagram requires a public HTTPS image URL; see [docs/NGROK_SETUP.md](docs/NGROK_SETUP.md))

3. **Set up the database:**
   ```bash
   python scripts/setup_database.py
   ```

4. **(Optional) Install frontend dependencies:**
   ```bash
   cd frontend && npm install
   ```

---

## Running

1. **Start the image server + public tunnel** (needed so Instagram can fetch generated images):
   ```bash
   scripts/start_image_server_and_ngrok.sh
   ```

2. **Start the backend:**
   ```bash
   uvicorn backend.main:app --reload
   ```
   API docs at http://localhost:8000/docs

3. **Start the frontend:**
   ```bash
   cd frontend && npm run dev
   ```
   http://localhost:5173

The backend spawns `mcp_server/instagram_tools_server.py` as a subprocess automatically per request, no separate step needed to run it.

---

## Testing

- **Inspect the MCP server's tools directly:**
  ```bash
  mcp dev mcp_server/instagram_tools_server.py
  ```
- **Dry run** (validates and logs the pipeline without publishing to Instagram): pass `"dry_run": true` in a request to `POST /api/content/generate-and-post`, or set `DRY_RUN=true` in `.env` as a deployment-wide safety net.
- See [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md).

---

## Project structure

```
agents/       Multi-agent orchestration (LangGraph coordinator + 3 tool-calling agents)
mcp_server/   The real MCP server exposing generate_content / generate_image / post_to_instagram
tools/        Tool implementations wrapped by the MCP server
backend/      FastAPI app, routes, Pydantic request/response models
database/     SQLAlchemy models and connection
frontend/     React + Vite client
scripts/      Setup and dev-environment helpers (DB setup, Instagram credentials, image server/tunnel)
docs/         Architecture and setup docs
```

---

## Resources

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
