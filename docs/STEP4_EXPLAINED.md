# Step 4: First MCP Tool (Trending Tool) - Explained

## What We're Building

**Goal**: Create a simple tool that checks if a topic is trending using Google Trends API.

**Think of it like:**
- A weather app that checks if it's raining
- A stock checker that tells you if a stock is up
- A tool that agents can use to make decisions

---

## Why We Need This

### Problem: Agents Need Information

```python
# Coordinator Agent needs to decide:
# "Is 'LLM' trending? Should I create content about it?"

# Without tools:
# Agent has no way to check trending status
# Can't make informed decisions
```

**Issues:**
- ❌ Agents can't access external data
- ❌ Can't check if topics are trending
- ❌ Can't make data-driven decisions

### Solution: MCP Tools

```python
# With tools:
trending_tool = TrendingTool()
result = trending_tool.check("LLM")
# Returns: {"is_trending": True, "score": 85}

# Agent can use this to decide:
if result["is_trending"]:
    # Create content about this topic!
```

**Benefits:**
- ✅ Agents can access external data
- ✅ Reusable across multiple agents
- ✅ Testable independently
- ✅ Clear separation of concerns

---

## What is MCP (Model-Context-Protocol)?

**MCP** = A pattern where AI agents use tools to get information and perform actions

**Key Idea**: 
- **Agent** = AI that makes decisions
- **Tool** = Function that does something specific
- **MCP** = Pattern for agents to discover and use tools

**Why MCP?**
- **Separation of Concerns**: Agent logic separate from tool logic
- **Reusability**: One tool can be used by multiple agents
- **Testability**: Test tools independently
- **Discoverability**: Agents can discover available tools

---

## What is a Tool?

**Tool** = A function with:
1. **Name**: What it's called
2. **Description**: What it does (agents read this!)
3. **Input**: What data it needs
4. **Output**: What data it returns

**Example:**
```python
def check_trending(topic: str) -> dict:
    """
    Check if a topic is currently trending on Google Trends.
    
    Args:
        topic: The topic to check (e.g., "LLM", "AI")
    
    Returns:
        {
            "is_trending": bool,
            "score": int (0-100),
            "trend_direction": "up" | "down" | "stable"
        }
    """
    # Implementation here
```

**Why this structure?**
- Agents can read the description
- Agents know what inputs are needed
- Agents know what to expect as output

---

## What We'll Build

### File Structure

```
tools/
└── trending_tool.py  # Our first MCP tool
```

### Tool Structure

```python
class TrendingTool:
    """
    Tool to check if a topic is trending on Google Trends.
    
    This tool will be used by the Coordinator Agent to decide
    if a topic is worth creating content about.
    """
    
    def check(self, topic: str) -> dict:
        """
        Check trending status for a topic.
        
        Returns structured data that agents can use.
        """
        # Implementation
```

---

## Step-by-Step: Building the Tool

### Step 1: Create Tools Directory

```
tools/
└── trending_tool.py
```

### Step 2: Choose API

**Options:**
1. **Google Trends API** (Free, but limited)
2. **Pytrends** (Python library for Google Trends - Free!)
3. **Mock/Simulated** (For learning, no API needed)

**For Step 4**: We'll use **Pytrends** (free, easy to use)

### Step 3: Install Dependencies

```bash
pip install pytrends
```

### Step 4: Build the Tool

```python
from pytrends.request import TrendReq

class TrendingTool:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
    
    def check(self, topic: str) -> dict:
        """
        Check if topic is trending.
        
        Returns:
            {
                "is_trending": bool,
                "score": int (0-100),
                "trend_direction": str
            }
        """
        # Build payload
        self.pytrends.build_payload([topic], timeframe='today 3-m')
        
        # Get interest over time
        data = self.pytrends.interest_over_time()
        
        # Calculate if trending
        if not data.empty:
            recent_score = data[topic].tail(7).mean()
            is_trending = recent_score > 50
            
            return {
                "is_trending": bool(is_trending),
                "score": int(recent_score),
                "trend_direction": "up" if recent_score > 70 else "stable"
            }
        
        return {
            "is_trending": False,
            "score": 0,
            "trend_direction": "unknown"
        }
```

### Step 5: Test the Tool

```python
tool = TrendingTool()
result = tool.check("LLM")
print(result)
# {"is_trending": True, "score": 85, "trend_direction": "up"}
```

---

## How Agents Will Use This Tool

### Later (Step 5-6): Agent Integration

```python
# Coordinator Agent will use it like this:
trending_tool = TrendingTool()
result = trending_tool.check("LLM")

if result["is_trending"]:
    # Create content about this topic!
    create_content("LLM")
else:
    # Maybe skip or use different topic
    pass
```

**For now**: We'll just build and test the tool directly.

---

## Key Concepts

### 1. Tool Structure

**Standard Pattern:**
```python
class ToolName:
    def __init__(self):
        # Setup (API clients, etc.)
        pass
    
    def method_name(self, input: str) -> dict:
        """
        Description that agents can read.
        
        Args:
            input: What the tool needs
        
        Returns:
            Structured data
        """
        # Implementation
        return {"result": "data"}
```

### 2. Tool Description

**Why important?**
- Agents read descriptions to understand what tools do
- Clear descriptions = better tool selection
- Later, LangChain/LangGraph will use these descriptions

### 3. Structured Output

**Why structured?**
- Agents need consistent data format
- Easy to parse and use
- Predictable responses

---

## What Happens Next

### Step 4 (Now):
- Build trending tool
- Test it directly
- Understand MCP pattern

### Step 5 (Next):
- Build Content Creator Agent
- Agent will use tools (including this one)
- LangGraph integration

### Step 6 (Later):
- Coordinator Agent uses trending tool
- Makes decisions based on trending data
- Full multi-agent workflow

---

## Benefits of MCP Pattern

✅ **Reusability**: One tool, many agents
✅ **Testability**: Test tools independently
✅ **Separation**: Tool logic separate from agent logic
✅ **Discoverability**: Agents can find available tools
✅ **Maintainability**: Update tools without changing agents

---

## Ready to Build?

We'll:
1. Create `tools/` directory
2. Install `pytrends` library
3. Build `TrendingTool` class
4. Test it with real topics
5. Understand how it fits into the bigger picture

**This is where the AI/agent magic begins!** 🎉

Let's build our first MCP tool!

