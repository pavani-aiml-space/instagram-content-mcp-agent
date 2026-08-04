# Agent Decision Making: Multiple Tools

## Concept

**Agents can have multiple tools and decide which one to use** based on:
- Context (budget, quality, time)
- Requirements (style, format, constraints)
- Results (quality checks, retries)

---

## Example 1: Content Creator Agent

### Agent with Multiple Content Tools

```python
# agents/content_creator.py
from tools.content_tools import OpenAIContentTool, ClaudeContentTool, LocalLLMTool
from tools.quality_tools import QualityCheckTool

class ContentCreatorAgent:
    def __init__(self):
        # Agent has access to MULTIPLE tools
        self.openai_tool = OpenAIContentTool()      # Tool 1: OpenAI GPT-4
        self.claude_tool = ClaudeContentTool()      # Tool 2: Claude (Anthropic)
        self.local_tool = LocalLLMTool()            # Tool 3: Local LLM (free)
        self.quality_checker = QualityCheckTool()  # Tool 4: Quality validation
    
    def generate(self, topic: str, context: dict) -> dict:
        """
        Agent DECIDES which tool to use based on context
        """
        # Decision 1: Choose content generation tool
        budget = context.get("budget", "medium")
        quality_required = context.get("quality", "medium")
        
        if budget == "low":
            # Decision: Use free local tool
            print("🤖 Agent decision: Using local tool (free)")
            content = self.local_tool.execute(topic)
        
        elif quality_required == "premium":
            # Decision: Use Claude (best quality)
            print("🤖 Agent decision: Using Claude tool (premium quality)")
            content = self.claude_tool.execute(topic)
        
        else:
            # Decision: Use OpenAI (default, good balance)
            print("🤖 Agent decision: Using OpenAI tool (default)")
            content = self.openai_tool.execute(topic)
        
        # Decision 2: Check quality if required
        if context.get("verify_quality", False):
            print("🤖 Agent decision: Checking quality...")
            quality_score = self.quality_checker.execute(content)
            
            # Decision 3: Retry if quality is low
            if quality_score < 0.7:
                print(f"🤖 Agent decision: Quality low ({quality_score}), retrying with OpenAI")
                content = self.openai_tool.execute(topic)  # Retry with better tool
        
        return content
```

### Flow Diagram

```
Content Creator Agent
    │
    ├─→ Has multiple tools:
    │   ├─→ openai_tool
    │   ├─→ claude_tool
    │   ├─→ local_tool
    │   └─→ quality_checker
    │
    ├─→ Analyzes context:
    │   ├─→ Budget: low/medium/high?
    │   ├─→ Quality: low/medium/premium?
    │   └─→ Verify quality: yes/no?
    │
    ├─→ DECIDES: Which tool to use
    │   ├─→ Budget low → local_tool
    │   ├─→ Quality premium → claude_tool
    │   └─→ Default → openai_tool
    │
    ├─→ Executes chosen tool
    │
    ├─→ DECIDES: Need quality check?
    │   └─→ If yes → quality_checker
    │
    ├─→ DECIDES: Retry needed?
    │   └─→ If quality low → retry with openai_tool
    │
    └─→ Returns result
```

---

## Example 2: Image Generator Agent

### Agent with Multiple Image Tools

```python
# agents/image_generator.py
from tools.image_tools import StabilityAITool, DalleTool, MidjourneyTool
from tools.image_processing import UpscaleTool, EnhanceTool

class ImageGeneratorAgent:
    def __init__(self):
        # Multiple image generation tools
        self.stability_tool = StabilityAITool()     # Fast, affordable
        self.dalle_tool = DalleTool()              # Good quality
        self.midjourney_tool = MidjourneyTool()    # Best quality, expensive
        self.upscale_tool = UpscaleTool()          # Image enhancement
        self.enhance_tool = EnhanceTool()          # Quality improvement
    
    def generate(self, prompt: str, requirements: dict) -> dict:
        """
        Agent DECIDES which tool(s) to use
        """
        style = requirements.get("style", "default")
        budget = requirements.get("budget", "medium")
        quality = requirements.get("quality", "medium")
        min_resolution = requirements.get("min_resolution", 1024)
        
        # Decision 1: Choose generation tool
        if quality == "premium" and budget == "high":
            print("🤖 Agent decision: Using Midjourney (premium quality)")
            image = self.midjourney_tool.execute(prompt)
        
        elif style == "artistic" or style == "creative":
            print("🤖 Agent decision: Using DALL-E (artistic style)")
            image = self.dalle_tool.execute(prompt)
        
        else:
            print("🤖 Agent decision: Using Stability AI (default)")
            image = self.stability_tool.execute(prompt)
        
        # Decision 2: Check if upscaling needed
        if image.resolution < min_resolution:
            print(f"🤖 Agent decision: Upscaling image ({image.resolution} → {min_resolution})")
            image = self.upscale_tool.execute(image)
        
        # Decision 3: Enhance if quality is low
        if image.quality_score < 0.8:
            print("🤖 Agent decision: Enhancing image quality")
            image = self.enhance_tool.execute(image)
        
        return image
```

---

## Example 3: Coordinator Agent with Multiple Strategies

### Coordinator Decides Between Different Workflows

```python
# agents/coordinator.py
from agents.content_creator import ContentCreatorAgent
from agents.image_generator import ImageGeneratorAgent
from tools.instagram_tool import InstagramTool
from tools.scheduler_tool import SchedulerTool

class CoordinatorAgent:
    def __init__(self):
        self.content_agent = ContentCreatorAgent()
        self.image_agent = ImageGeneratorAgent()
        self.instagram_tool = InstagramTool()
        self.scheduler_tool = SchedulerTool()
    
    def generate_post(self, topic: str, options: dict) -> dict:
        """
        Coordinator DECIDES the workflow based on options
        """
        # Decision 1: Parallel or sequential?
        if options.get("parallel", False):
            # Decision: Generate content and image in parallel
            print("🤖 Coordinator decision: Parallel generation")
            content, image = self._parallel_generation(topic, options)
        else:
            # Decision: Sequential (content first, then image)
            print("🤖 Coordinator decision: Sequential generation")
            content = self.content_agent.generate(topic, options)
            image = self.image_agent.generate(content["visual_prompt"], options)
        
        # Decision 2: Post immediately or schedule?
        if options.get("schedule"):
            print("🤖 Coordinator decision: Scheduling post")
            self.scheduler_tool.execute(image["url"], content["caption"], options["schedule_time"])
            return {"status": "scheduled", "scheduled_at": options["schedule_time"]}
        else:
            print("🤖 Coordinator decision: Posting immediately")
            result = self.instagram_tool.execute(image["url"], content["caption"])
            return {"status": "posted", "post_id": result["id"]}
    
    def _parallel_generation(self, topic, options):
        # Use async/threading for parallel execution
        import asyncio
        async def run_parallel():
            content_task = self.content_agent.generate(topic, options)
            # Image needs content first, so we wait a bit
            await asyncio.sleep(0.1)
            image_task = self.image_agent.generate(topic, options)  # Uses topic directly
            return await asyncio.gather(content_task, image_task)
        return asyncio.run(run_parallel())
```

---

## Decision Making Patterns

### Pattern 1: Cost-Based Decision

```python
def choose_tool_by_cost(budget):
    if budget == "low":
        return free_tool
    elif budget == "medium":
        return affordable_tool
    else:
        return premium_tool
```

### Pattern 2: Quality-Based Decision

```python
def choose_tool_by_quality(quality_required):
    if quality_required == "high":
        return best_quality_tool
    elif quality_required == "medium":
        return good_quality_tool
    else:
        return basic_tool
```

### Pattern 3: Fallback Decision

```python
def execute_with_fallback(primary_tool, backup_tool):
    try:
        return primary_tool.execute(...)
    except ToolError:
        print("Primary tool failed, using backup")
        return backup_tool.execute(...)
```

### Pattern 4: Conditional Chaining

```python
def execute_with_conditional_chain(base_tool, conditional_tool, condition):
    result = base_tool.execute(...)
    
    if condition(result):
        result = conditional_tool.execute(result)
    
    return result
```

### Pattern 5: Multi-Tool Composition

```python
def execute_multi_tool_workflow(tools, workflow):
    result = None
    for tool_name in workflow:
        tool = tools[tool_name]
        result = tool.execute(result or initial_input)
    return result
```

---

## Benefits

✅ **Intelligence**: Agents make smart decisions
✅ **Flexibility**: Adapt to different situations
✅ **Resilience**: Fallback if tool fails
✅ **Optimization**: Choose best tool for the job
✅ **Composition**: Chain tools together
✅ **Cost Control**: Choose tools based on budget
✅ **Quality Control**: Choose tools based on quality needs

---

## Summary

**Key Points:**

1. **Agents can have multiple tools** - Not limited to one
2. **Agents make decisions** - Based on context, requirements, results
3. **Agents can chain tools** - Use multiple tools in sequence
4. **Agents can fallback** - Try different tools if one fails
5. **Agents optimize** - Choose best tool for cost, quality, speed

**This makes agents intelligent and adaptable!**

