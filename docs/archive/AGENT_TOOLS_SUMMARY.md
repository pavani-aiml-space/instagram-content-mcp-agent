# Agent Tools Summary

## Quick Reference: Tools Used by Each Agent

### Coordinator Agent (4 Tools)
```
1. TrendingTopicsTool
   └─→ Checks if topic is trending (Google Trends API)

2. EngagementAnalyzerTool
   └─→ Analyzes past post performance (Instagram API)

3. FormatDecisionTool
   └─→ Decides Post/Story/Reel format

4. InstagramTool
   └─→ Posts content to Instagram (Graph API)
```

---

### Content Creator Agent (9 Tools)
```
1. TrendingTopicsTool (shared)
   └─→ Used for LLM tool selection decision

2. EngagementAnalyzerTool (shared)
   └─→ Used for content type selection

3. FormatDecisionTool (shared)
   └─→ Used for format recommendation

4. LocalLLMTool
   └─→ Free, local LLM (Ollama/LM Studio)

5. GeminiFlashTool
   └─→ Free tier, fast (15 req/min)

6. GeminiProTool
   └─→ Paid, cost-effective (~$0.001/req)

7. OpenAIGPTTool
   └─→ Paid, best quality (~$0.03/req)

8. HuggingFaceTool
   └─→ Free tier (1000 req/month)

9. HashtagGeneratorTool
   └─→ Generates relevant hashtags
```

---

### Image Generator Agent (4 Tools)
```
1. ImageStyleAnalyzerTool
   └─→ Analyzes best image style (Instagram API)

2. StableDiffusionLocalTool
   └─→ Free, local image generation

3. HuggingFaceImageTool
   └─→ Free tier image generation

4. ImageOptimizerTool
   └─→ Optimizes images for Instagram (PIL/Pillow)
```

---

## Tool Selection Flow

### Content Creator Agent Tool Selection:
```
Trending Check
    ↓
Is highly trending? (score > 0.8)
    ├─→ YES → OpenAI GPT-4 or Gemini Pro
    └─→ NO → Continue
        ↓
Quality = "premium"?
    ├─→ YES → OpenAI GPT-4 or Gemini Pro
    └─→ NO → Continue
        ↓
Speed = "fast"?
    ├─→ YES → Gemini Flash
    └─→ NO → Continue
        ↓
Budget = "low"?
    ├─→ YES → Local LLM → Gemini Flash → Hugging Face
    └─→ NO → Continue
        ↓
Default: Local LLM → Gemini Flash → Hugging Face
```

### Image Generator Agent Tool Selection:
```
Style Analysis
    ↓
Using: ImageStyleAnalyzerTool
    ↓
Decide Style (Realistic/Artistic/Trending)
    ↓
Tool Selection:
    ├─→ Stable Diffusion Local available?
    │   └─→ YES → Use it (free, fast)
    └─→ NO → Hugging Face (free tier)
        ↓
Generate Image
    ↓
Optimize using: ImageOptimizerTool
```

---

## Tool Sharing Between Agents

**Shared Tools:**
- `TrendingTopicsTool` → Used by Coordinator and Content Creator
- `EngagementAnalyzerTool` → Used by Coordinator and Content Creator
- `FormatDecisionTool` → Used by Coordinator and Content Creator

**Agent-Specific Tools:**
- **Coordinator**: InstagramTool (only coordinator posts)
- **Content Creator**: All LLM tools + HashtagGeneratorTool
- **Image Generator**: All image tools + ImageStyleAnalyzerTool

---

## Complete Tool Inventory

| Tool Name | Used By | Purpose | Cost |
|-----------|---------|---------|------|
| TrendingTopicsTool | Coordinator, Content Creator | Check trending | Free |
| EngagementAnalyzerTool | Coordinator, Content Creator | Analyze performance | Free |
| FormatDecisionTool | Coordinator, Content Creator | Decide format | Free |
| InstagramTool | Coordinator | Post to Instagram | Free API |
| LocalLLMTool | Content Creator | Generate content | Free |
| GeminiFlashTool | Content Creator | Generate content | Free tier |
| GeminiProTool | Content Creator | Generate content | ~$0.001 |
| OpenAIGPTTool | Content Creator | Generate content | ~$0.03 |
| HuggingFaceTool | Content Creator | Generate content | Free tier |
| HashtagGeneratorTool | Content Creator | Generate hashtags | Free |
| ImageStyleAnalyzerTool | Image Generator | Analyze style | Free |
| StableDiffusionLocalTool | Image Generator | Generate images | Free |
| HuggingFaceImageTool | Image Generator | Generate images | Free tier |
| ImageOptimizerTool | Image Generator | Optimize images | Free |

---

## Tool Decision Matrix

### When to Use Each LLM Tool:

| Condition | Tool Selected | Reason |
|-----------|---------------|--------|
| High trending (score > 0.8) | OpenAI GPT-4 or Gemini Pro | Best quality for viral content |
| Premium quality requested | OpenAI GPT-4 or Gemini Pro | Highest quality |
| Fast generation needed | Gemini Flash | Fast, free tier |
| Low budget | Local LLM → Gemini Flash → Hugging Face | Free options |
| Default | Local LLM → Gemini Flash → Hugging Face | Free, reliable |

### When to Use Each Image Tool:

| Condition | Tool Selected | Reason |
|-----------|---------------|--------|
| Local available | Stable Diffusion Local | Free, fast, no API limits |
| Local unavailable | Hugging Face | Free tier fallback |

---

This summary shows all tools used by each agent in the multi-agent system!

