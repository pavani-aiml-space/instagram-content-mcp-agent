# Multi-Agent Architecture

## Overview

This system uses a **multi-agent architecture** where specialized agents work together under the coordination of a **Coordinator Agent**. Each agent is responsible for a specific task and uses MCP tools to accomplish its goals.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│              Coordinator Agent                           │
│  (Orchestrates the entire workflow)                     │
│                                                          │
│  - Receives: Topic, Format, User Info                   │
│  - Coordinates: All specialized agents                  │
│  - Manages: Workflow state and error handling          │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┼───────┐
       │       │       │
       ▼       ▼       ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Content  │ │  Image   │ │  Instagram   │
│ Creator  │ │ Generator│ │   Poster     │
│  Agent   │ │  Agent   │ │   Agent      │
│          │ │          │ │              │
│ Uses:    │ │ Uses:    │ │ Uses:        │
│ - Content│ │ - Image  │ │ - Instagram  │
│   Tool   │ │   Tool   │ │   Tool       │
└──────────┘ └──────────┘ └──────────────┘
```

## Agents

### 1. Content Creator Agent (`agents/content_creator_agent.py`)

**Role**: Specialized in generating Instagram content

**Responsibilities**:
- Generate engaging captions from topics
- Create relevant hashtags
- Optimize content for Instagram format (post/story/reel)

**Tools Used**:
- `generate_content_tool` (MCP tool)

**State**:
```python
{
    "topic": str,
    "format": str,
    "caption": str,
    "hashtags": str,
    "status": str,
    "error": str
}
```

**Usage**:
```python
from agents.content_creator_agent import run_content_creator

result = run_content_creator(topic="LLM", format="post")
# Returns: {caption, hashtags, status, error}
```

### 2. Image Generator Agent (`agents/image_generator_agent.py`)

**Role**: Specialized in generating images

**Responsibilities**:
- Generate images from prompts
- Optimize images for Instagram (aspect ratios)
- Create Instagram-worthy visuals

**Tools Used**:
- `generate_image_tool` (MCP tool)

**State**:
```python
{
    "prompt": str,
    "aspect_ratio": str,
    "image_url": str,
    "status": str,
    "error": str
}
```

**Usage**:
```python
from agents.image_generator_agent import run_image_generator

result = run_image_generator(
    prompt="A professional image about AI",
    aspect_ratio="1:1"
)
# Returns: {image_url, status, error}
```

### 3. Instagram Poster Agent (`agents/instagram_poster_agent.py`)

**Role**: Specialized in posting to Instagram

**Responsibilities**:
- Post images with captions to Instagram
- Handle Instagram Graph API interactions
- Manage posting workflow

**Tools Used**:
- `post_to_instagram_tool` (MCP tool)

**State**:
```python
{
    "image_url": str,
    "caption": str,
    "instagram_account_id": str,
    "post_id": str,
    "permalink": str,
    "status": str,
    "error": str
}
```

**Usage**:
```python
from agents.instagram_poster_agent import run_instagram_poster

result = run_instagram_poster(
    image_url="https://...",
    caption="Caption text...",
    instagram_account_id="123456"
)
# Returns: {post_id, permalink, status, error}
```

### 4. Coordinator Agent (`agents/coordinator_agent.py`)

**Role**: Orchestrates all specialized agents

**Responsibilities**:
- Coordinate the workflow between agents
- Manage state across agents
- Handle errors and retries
- Assemble final results

**Workflow**:
1. Call Content Creator Agent → Get caption + hashtags
2. Call Image Generator Agent → Get image URL
3. Call Instagram Poster Agent → Post to Instagram

**State**:
```python
{
    "topic": str,
    "format": str,
    "user_id": str,
    "instagram_account_id": str,
    "caption": str,          # From Content Creator
    "hashtags": str,         # From Content Creator
    "image_url": str,        # From Image Generator
    "post_id": str,          # From Instagram Poster
    "permalink": str,        # From Instagram Poster
    "status": str,
    "error": str,
    "current_step": str
}
```

**Usage**:
```python
from agents.coordinator_agent import run_coordinator

result = run_coordinator(
    topic="LLM",
    format="post",
    user_id="user-123",
    instagram_account_id="ig-123"
)
# Returns: Complete result from all agents
```

## Workflow Flow

```
1. User Request
   │
   ▼
2. FastAPI Route (/api/content/generate-and-post)
   │
   ▼
3. Coordinator Agent
   │
   ├─► Step 1: Content Creator Agent
   │       │
   │       └─► Uses: generate_content_tool
   │       └─► Returns: {caption, hashtags}
   │
   ├─► Step 2: Image Generator Agent
   │       │
   │       └─► Uses: generate_image_tool
   │       └─► Returns: {image_url}
   │
   └─► Step 3: Instagram Poster Agent
           │
           └─► Uses: post_to_instagram_tool
           └─► Returns: {post_id, permalink}
   │
   ▼
4. Coordinator assembles results
   │
   ▼
5. Save to database
   │
   ▼
6. Return response to user
```

## Benefits of Multi-Agent Architecture

### 1. **Specialization**
- Each agent is expert in one domain
- Better quality decisions
- Easier to improve individual agents

### 2. **Modularity**
- Agents can be developed independently
- Easy to test each agent separately
- Can swap agents without affecting others

### 3. **Scalability**
- Can add new agents easily
- Can run agents in parallel (future enhancement)
- Can scale individual agents independently

### 4. **Maintainability**
- Clear separation of concerns
- Easier to debug issues
- Easier to add features

### 5. **Flexibility**
- Can use agents individually
- Can combine agents in different ways
- Can add new coordination strategies

## Agent Communication

### Current Approach: Sequential (via Coordinator)

```
Coordinator → Content Creator → Coordinator
Coordinator → Image Generator → Coordinator
Coordinator → Instagram Poster → Coordinator
```

### Future Enhancement: Parallel Execution

```
Coordinator
    ├─► Content Creator (parallel)
    └─► Image Generator (parallel)
    ↓ (both complete)
Coordinator → Instagram Poster
```

## Error Handling

Each agent handles errors independently:

1. **Agent Level**: Each agent catches and reports errors
2. **Coordinator Level**: Coordinator checks agent results and stops on error
3. **API Level**: FastAPI route handles coordinator errors

## Adding New Agents

To add a new agent:

1. Create agent file: `agents/my_new_agent.py`
2. Define agent state (TypedDict)
3. Create agent workflow
4. Create `run_my_new_agent()` function
5. Add to coordinator workflow
6. Export from `agents/__init__.py`

Example:
```python
# agents/my_new_agent.py
def run_my_new_agent(input: str) -> dict:
    workflow = create_my_new_agent_workflow()
    state = {"input": input, "output": "", "status": "starting"}
    final_state = workflow.invoke(state)
    return {"output": final_state["output"], "status": final_state["status"]}
```

Then add to coordinator:
```python
# agents/coordinator_agent.py
def call_my_new_agent_node(state: CoordinatorState) -> CoordinatorState:
    result = run_my_new_agent(state["some_input"])
    state["some_output"] = result["output"]
    return state
```

## Testing Individual Agents

You can test each agent independently:

```python
# Test Content Creator Agent
from agents.content_creator_agent import run_content_creator
result = run_content_creator("LLM", "post")
print(result)

# Test Image Generator Agent
from agents.image_generator_agent import run_image_generator
result = run_image_generator("AI robot", "1:1")
print(result)

# Test Instagram Poster Agent
from agents.instagram_poster_agent import run_instagram_poster
result = run_instagram_poster("https://...", "Caption", "ig-123")
print(result)
```

## MCP Tools Integration

All agents use MCP (Model Context Protocol) tools:

- **Standardized Interface**: All tools follow same pattern
- **Reusable**: Tools can be used by multiple agents
- **Testable**: Tools can be tested independently
- **Maintainable**: Changes to tools don't affect agent logic

Tools are defined in `mcp_server/instagram_tools_server.py`, a real MCP server (stdio transport). Agents connect to it via `agents/mcp_client.py` and load its tools as LangChain `BaseTool` objects through `langchain-mcp-adapters`.

