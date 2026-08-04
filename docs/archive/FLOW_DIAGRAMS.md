# Visual Flow Diagrams - Agentic Flow, MCP, and LangGraph

## 📊 Quick Reference Diagrams

---

## 1. Current Architecture (MCP Pattern)

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  Web UI / API / Cron Scheduler                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATION LAYER (MCP Agent)                │
│                    src/agent.js                             │
│  • Coordinates tools                                        │
│  • Manages workflow                                        │
│  • Handles errors                                          │
└───────────┬───────────────┬───────────────┬─────────────────┘
            │               │               │
            ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  TOOL LAYER      │ │  TOOL LAYER      │ │  TOOL LAYER      │
│  (MCP Servers)   │ │  (MCP Servers)   │ │  (MCP Servers)   │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ tools/chatgpt/   │ │ tools/image-    │ │ tools/           │
│                  │ │   generator/    │ │   instagram/     │
│ • OpenAI API     │ │ • Stability AI   │ │ • Graph API      │
│ • Content Gen    │ │ • Image Gen     │ │ • Media Post     │
│ • Parsing        │ │ • Hosting       │ │ • Publishing     │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                     │
         ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                        │
│  OpenAI API  │  Stability AI  │  Instagram Graph API       │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- ✅ **MCP Pattern**: Tools are independent modules
- ✅ **Agent Orchestration**: `src/agent.js` coordinates tools
- ✅ **Separation of Concerns**: Tools don't know about each other

---

## 2. Agentic Flow - Current Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC WORKFLOW                          │
│              (src/agent.js - runDailyInstagramPostAgent)     │
└─────────────────────────────────────────────────────────────┘

START
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Generate Content                                    │
│ ───────────────────────────────────────────────────────────│
│ Input:  User prompt ("Attention Mechanisms")               │
│ Action: Call generateInstagramContent()                    │
│ Tool:   tools/chatgpt/index.js                             │
│ API:    OpenAI GPT-4                                       │
│ Output: { caption, keyConcepts, examples, imagePrompt }    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Generate Image                                      │
│ ───────────────────────────────────────────────────────────│
│ Input:  imagePrompt from Step 1                            │
│ Action: Call generateAndHostImage()                        │
│ Tool:   tools/image-generator/index.js                     │
│ API:    Stability AI                                       │
│ Output: Public image URL                                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Compose Caption                                    │
│ ───────────────────────────────────────────────────────────│
│ Input:  Content from Step 1                               │
│ Action: Combine caption + keyConcepts + examples           │
│ Output: Full Instagram caption                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Post to Instagram                                   │
│ ───────────────────────────────────────────────────────────│
│ Input:  Caption + Image URL                                │
│ Action: Call postToInstagram()                             │
│ Tool:   tools/instagram/index.js                           │
│ API:    Instagram Graph API                                │
│ Output: Post ID and status                                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                          END
```

**Agentic Characteristics:**
- ✅ **Autonomous**: Runs without human intervention
- ✅ **Tool-Using**: Uses multiple tools to accomplish goal
- ⚠️ **Limited Adaptation**: Basic error handling (try/catch)
- ⚠️ **No Decision-Making**: Fixed sequence

---

## 3. Future Architecture (MCP + LangGraph)

```
┌─────────────────────────────────────────────────────────────┐
│              LANGGRAPH STATEGRAPH                           │
│              (src/langgraph-agent.js)                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    STATE                             │  │
│  │  {                                                   │  │
│  │    prompt: "Attention Mechanisms",                  │  │
│  │    content: {...},                                  │  │
│  │    imageUrl: "...",                                 │  │
│  │    caption: "...",                                  │  │
│  │    status: "pending" | "content_generated" | ...    │  │
│  │    errors: []                                       │  │
│  │  }                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    NODE 1: Generate Content                 │
│ ───────────────────────────────────────────────────────────│
│ Function: generateContentNode(state)                      │
│ Tool:     LangChain Tool (wraps generateAIEducationContent)│
│ Updates:  state.content, state.status                      │
│ Error:    Updates state.errors, state.status = "error"    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (if success)
┌─────────────────────────────────────────────────────────────┐
│                    NODE 2: Generate Image                   │
│ ───────────────────────────────────────────────────────────│
│ Function: generateImageNode(state)                         │
│ Tool:     LangChain Tool (wraps generateAndHostImage)      │
│ Updates:  state.imageUrl, state.status                      │
│ Error:    Updates state.errors, can RETRY                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (if success)
┌─────────────────────────────────────────────────────────────┐
│                    NODE 3: Compose Caption                  │
│ ───────────────────────────────────────────────────────────│
│ Function: composeCaptionNode(state)                        │
│ Updates:  state.caption, state.status                       │
│ Error:    Updates state.errors                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (if success)
┌─────────────────────────────────────────────────────────────┐
│                    NODE 4: Post to Instagram                 │
│ ───────────────────────────────────────────────────────────│
│ Function: postToInstagramNode(state)                       │
│ Tool:     LangChain Tool (wraps postImageToInstagram)      │
│ Updates:  state.postResult, state.status                    │
│ Error:    Updates state.errors, can RETRY                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                          END
```

**LangGraph Advantages:**
- ✅ **State Management**: State flows through all nodes
- ✅ **Error Recovery**: Can retry failed nodes
- ✅ **Conditional Branching**: Can skip nodes based on state
- ✅ **Visual Debugging**: Can visualize workflow

---

## 4. MCP Pattern - Tool Independence

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP PATTERN                              │
│              (Model Context Protocol)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    AGENT (Orchestrator)                     │
│              src/agent.js                                   │
│  • Knows about all tools                                    │
│  • Coordinates tool execution                               │
│  • Manages data flow                                        │
└───────────┬───────────────┬───────────────┬─────────────────┘
            │               │               │
            │               │               │
    ┌───────┴───────┐ ┌─────┴──────┐ ┌─────┴──────┐
    │               │ │            │ │            │
    ▼               ▼ ▼            ▼ ▼            ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Tool 1  │    │ Tool 2  │    │ Tool 3  │    │ Tool N  │
│         │    │         │    │         │    │         │
│ ChatGPT │    │ Image   │    │ Instagram│   │ Video   │
│         │    │ Gen     │    │         │    │ Gen     │
│         │    │         │    │         │    │         │
│ ❌ Doesn't│    │ ❌ Doesn't│    │ ❌ Doesn't│    │ ❌ Doesn't│
│   know   │    │   know  │    │   know  │    │   know  │
│   about  │    │   about│    │   about │    │   about │
│   other  │    │   other│    │   other │    │   other │
│   tools  │    │   tools│    │   tools │    │   tools │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

**MCP Principles:**
- ✅ **Independence**: Tools don't know about each other
- ✅ **Modularity**: Easy to add/remove tools
- ✅ **Standardized Interface**: Consistent APIs
- ✅ **Composability**: Tools can be combined

---

## 5. LangChain vs LangGraph Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    LANGCHAIN                                │
│              (Framework for LLM Apps)                       │
└─────────────────────────────────────────────────────────────┘

Tools:
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Tool 1  │  │ Tool 2  │  │ Tool 3  │
│ (Func)  │  │ (Func)  │  │ (Func)  │
└────┬────┘  └────┬────┘  └────┬────┘
     │           │           │
     └───────────┼───────────┘
                 │
                 ▼
         ┌───────────────┐
         │   Agent       │
         │  (Uses Tools) │
         └───────────────┘

Features:
• Tool wrapping
• Agent creation
• Chain composition
• Basic state


┌─────────────────────────────────────────────────────────────┐
│                    LANGGRAPH                                │
│         (State-Based Workflows on LangChain)                 │
└─────────────────────────────────────────────────────────────┘

Tools (from LangChain):
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Tool 1  │  │ Tool 2  │  │ Tool 3  │
│ (Func)  │  │ (Func)  │  │ (Func)  │
└────┬────┘  └────┬────┘  └────┬────┘
     │           │           │
     └───────────┼───────────┘
                 │
                 ▼
         ┌───────────────┐
         │  StateGraph   │
         │  (Workflow)   │
         └───────┬───────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Node 1  │→│ Node 2  │→│ Node 3  │
│         │ │         │ │         │
│ State   │ │ State   │ │ State   │
│ Flows   │ │ Flows   │ │ Flows   │
└─────────┘ └─────────┘ └─────────┘

Features:
• State management
• Visual workflows
• Error recovery
• Conditional branching
• Retry logic
```

**Key Difference:**
- **LangChain**: Tools + Agents (foundation)
- **LangGraph**: Workflows + State (built on LangChain)

---

## 6. Decision Tree: Do We Need LangGraph?

```
                    START
                      │
                      ▼
            ┌─────────────────────┐
            │ Current Workflow   │
            │ Simple?            │
            └─────────┬───────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼ YES                       ▼ NO
┌───────────────┐          ┌──────────────────┐
│ Keep Current  │          │ Need Error       │
│ Agent         │          │ Recovery?        │
│               │          └─────────┬──────────┘
│ ✅ Works      │                   │
│ ✅ Simple     │          ┌────────┴────────┐
│ ✅ Maintainable│         │                  │
└───────────────┘          ▼ YES              ▼ NO
                    ┌──────────────┐   ┌──────────────┐
                    │ Need State   │   │ Keep Current │
                    │ Management?  │   │ Agent        │
                    └──────┬───────┘   └──────────────┘
                           │
                  ┌─────────┴─────────┐
                  │                    │
                  ▼ YES                ▼ NO
          ┌───────────────┐    ┌───────────────┐
          │ Use LangGraph │    │ Keep Current  │
          │               │    │ Agent         │
          │ ✅ State      │    │               │
          │ ✅ Retry     │    │ ✅ Simple     │
          │ ✅ Visual    │    │ ✅ Works      │
          └───────────────┘    └───────────────┘
```

**Our Answer:**
- **Now**: Keep current agent (simple, works)
- **Future**: Add LangGraph (when adding reels, curriculum, error recovery)

---

## 7. Complete Flow: From User to Instagram Post

```
USER
 │
 │ "Create post about Attention Mechanisms"
 │
 ▼
┌─────────────────────────────────────────────────────────────┐
│              src/server.js (Express)                         │
│  • Receives request                                          │
│  • Routes to agent                                           │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              src/agent.js (MCP Agent)                        │
│  • Orchestrates workflow                                    │
│  • Coordinates tools                                         │
└───────────┬───────────────┬───────────────┬─────────────────┘
            │               │               │
            ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ tools/chatgpt/  │ │ tools/image-    │ │ tools/          │
│                  │ │   generator/    │ │   instagram/    │
│ OpenAI API       │ │ Stability AI    │ │ Graph API       │
│ ↓                │ │ ↓                │ │ ↓              │
│ Content Generated│ │ Image Generated  │ │ Post Published  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Result       │
                    │  Post ID      │
                    │  Status       │
                    └───────────────┘
                            │
                            ▼
                          USER
                    (Post on Instagram)
```

---

## Summary

1. **MCP Pattern**: Tools are independent, agent orchestrates
2. **Agentic Flow**: Autonomous workflow with tool coordination
3. **LangChain**: Framework for tools and agents
4. **LangGraph**: State-based workflows built on LangChain
5. **Current**: MCP + Custom Agent (works well)
6. **Future**: MCP + LangGraph (when complexity increases)

---

**See Also:**
- `docs/AGENTIC_FLOW_EXPLAINED.md` - Detailed explanations
- `docs/ARCHITECTURE.md` - Complete architecture
- `src/agent.js` - Current agent implementation
- `src/langgraph-agent.js` - Future LangGraph implementation


