# MCP Agent Architecture

## Overview

This project uses **LangGraph agents** with **MCP (Model Context Protocol) tools** to create a multi-agent system for Instagram content generation.

## Architecture Components

### 1. MCP Tools (`tools/langchain_tools.py`)

**MCP Pattern**: Tools are standardized, reusable components that agents can use.

Each tool:
- Is decorated with `@tool` from LangChain
- Has clear input/output contracts
- Handles errors gracefully
- Returns structured dictionaries

**Available Tools**:

1. **`generate_content_tool`**
   - Input: `topic` (str), `format` (str)
   - Output: `{caption, hashtags, status}`
   - Uses: `ContentGenerator` class

2. **`generate_image_tool`**
   - Input: `prompt` (str), `aspect_ratio` (str)
   - Output: `{image_url, status}`
   - Uses: `ImageGenerator` class

3. **`post_to_instagram_tool`**
   - Input: `image_url` (str), `caption` (str), `instagram_account_id` (str)
   - Output: `{post_id, permalink, status}`
   - Uses: `InstagramPoster` class

### 2. LangGraph Agent (`agents/content_creator_agent.py`)

**Two Approaches**:

#### A. ReAct Agent (`create_langgraph_agent()`)
- Uses LangGraph's `create_react_agent`
- Agent can reason about which tools to use
- More flexible, agent decides the flow

#### B. State-Based Workflow (`create_langgraph_workflow()`)
- Uses `StateGraph` with predefined nodes
- Each node calls an MCP tool
- Fixed flow: `generate_content` → `generate_image` → `post_to_instagram`
- More predictable, easier to debug

**Current Implementation**: Uses **State-Based Workflow** for reliability.

### 3. Agent State

```python
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]  # Chat messages (for ReAct agent)
    topic: str                      # Content topic
    format: str                     # Content format
    user_id: str                    # User ID
    instagram_account_id: str       # Instagram Account ID
    caption: str                    # Generated caption
    hashtags: str                   # Generated hashtags
    image_url: str                   # Generated image URL
    post_id: str                    # Instagram post ID
    status: str                     # Current status
    error: str                      # Error message if any
```

### 4. Workflow Flow

```
1. generate_content_node
   └─> Calls generate_content_tool
   └─> Updates state: caption, hashtags

2. generate_image_node
   └─> Calls generate_image_tool
   └─> Updates state: image_url

3. post_to_instagram_node
   └─> Calls post_to_instagram_tool
   └─> Updates state: post_id
```

## Flow Diagram

```
User Request
    │
    ▼
FastAPI Route (/api/content/generate-and-post)
    │
    ▼
Create Initial State
    │
    ▼
LangGraph Workflow
    │
    ├─► Node 1: generate_content
    │       │
    │       └─► MCP Tool: generate_content_tool
    │               │
    │               └─► ContentGenerator.generate()
    │
    ├─► Node 2: generate_image
    │       │
    │       └─► MCP Tool: generate_image_tool
    │               │
    │               └─► ImageGenerator.generate()
    │
    └─► Node 3: post_to_instagram
            │
            └─► MCP Tool: post_to_instagram_tool
                    │
                    └─► InstagramPoster.post_image()
    │
    ▼
Final State
    │
    ▼
Save to Database
    │
    ▼
Return Response
```

## Key Benefits of MCP Pattern

1. **Standardized Tools**: All tools follow the same pattern
2. **Reusability**: Tools can be used by different agents
3. **Testability**: Tools can be tested independently
4. **Maintainability**: Changes to tools don't affect agent logic
5. **Composability**: Easy to add new tools or agents

## Usage Example

```python
from agents.content_creator_agent import create_langgraph_workflow

# Create workflow
workflow = create_langgraph_workflow()

# Initial state
state = {
    "messages": [],
    "topic": "LLM",
    "format": "post",
    "user_id": "user-123",
    "instagram_account_id": "ig-account-123",
    "caption": "",
    "hashtags": "",
    "image_url": "",
    "post_id": "",
    "status": "starting",
    "error": ""
}

# Run workflow
final_state = workflow.invoke(state)

# Access results
print(f"Caption: {final_state['caption']}")
print(f"Image URL: {final_state['image_url']}")
print(f"Post ID: {final_state['post_id']}")
```

## Adding New Tools

1. Create the tool class (e.g., `tools/my_tool.py`)
2. Wrap it as an MCP tool in `tools/langchain_tools.py`:
   ```python
   @tool
   def my_new_tool(param: str) -> dict:
       """Tool description"""
       try:
           tool_instance = MyTool()
           result = tool_instance.do_something(param)
           return {"result": result, "status": "success"}
       except Exception as e:
           return {"status": "error", "error": str(e)}
   ```
3. Add tool to agent's tool list
4. Use in workflow nodes or let ReAct agent decide when to use it

