# End-to-End Flow Diagram: Multi-Agent System

## Complete Visual Flow (Viewable Directly)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER REQUEST                                       │
│                    "Generate Instagram Content"                              │
│                         Topic: "Neural Networks"                             │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                                      │
│                    POST /api/content/generate                                │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COORDINATOR AGENT                                      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ DECISION 1: Check Trending Topics                                   │  │
│  │    Is "Neural Networks" trending?                                    │  │
│  │    ├─→ YES (score: 0.85) → High Priority                            │  │
│  │    └─→ NO → Normal Flow                                             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                 │                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ DECISION 2: Analyze Engagement                                      │  │
│  │    What content type performs best?                                  │  │
│  │    ├─→ Best: "educational"                                           │  │
│  │    ├─→ Best time: "18:00"                                            │  │
│  │    └─→ Avg engagement: 4.5%                                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                 │                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ DECISION 3: Format Decision (Post/Story/Reel)                        │  │
│  │    Factors:                                                           │  │
│  │    ├─→ Trending? YES → REEL (best for viral)                         │  │
│  │    ├─→ Content type? "educational" → Could be Post                    │  │
│  │    └─→ Performance? Reel: 12%, Story: 8%, Post: 4.5%                 │  │
│  │                                                                        │  │
│  │    DECISION: REEL (trending topic, highest engagement)               │  │
│  │    Predicted engagement: 12%                                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│   CONTENT CREATOR AGENT                    │  │   IMAGE GENERATOR AGENT        │
│                                            │  │                                │
│  TOOLS AVAILABLE:                          │  │  TOOLS AVAILABLE:              │
│  ┌──────────────────────────────────────┐ │  │  ┌───────────────────────────┐ │
│  │ 1. TrendingTopicsTool (shared)      │ │  │  │ 1. ImageStyleAnalyzerTool │ │
│  │ 2. EngagementAnalyzerTool (shared)  │ │  │  │ 2. StableDiffusionLocalTool│ │
│  │ 3. FormatDecisionTool (shared)     │ │  │  │ 3. HuggingFaceImageTool    │ │
│  │ 4. LocalLLMTool                    │ │  │  │ 4. ImageOptimizerTool     │ │
│  │ 5. GeminiFlashTool                 │ │  │  └───────────────────────────┘ │
│  │ 6. GeminiProTool                   │ │  │                                │
│  │ 7. OpenAIGPTTool                   │ │  │                                │
│  │ 8. HuggingFaceTool                 │ │  │                                │
│  │ 9. HashtagGeneratorTool             │ │  │                                │
│  └──────────────────────────────────────┘ │  │                                │
│                                            │  │                                │
│  DECISION 4: LLM Tool Selection           │  │  DECISION 5: Image Style        │
│  ┌──────────────────────────────────────┐ │  │  ┌───────────────────────────┐ │
│  │ Factors:                              │ │  │  │ Using: ImageStyleAnalyzer │ │
│  │ ├─→ Trending? YES                     │ │  │  │                          │ │
│  │ ├─→ Quality? Premium                  │ │  │  │ Factors:                  │ │
│  │ └─→ Budget? Medium                    │ │  │  │ ├─→ Content type           │ │
│  │                                       │ │  │  │ ├─→ Performance data       │ │
│  │ Options:                              │ │  │  │ └─→ Format (Reel)          │ │
│  │ ├─→ OpenAI GPT-4 ✓                   │ │  │  │                          │ │
│  │ ├─→ Gemini Pro                        │ │  │  │ Decision: Trending Style   │ │
│  │ ├─→ Gemini Flash                      │ │  │  │                          │ │
│  │ ├─→ Local LLM                         │ │  │  │                          │ │
│  │ └─→ Hugging Face                      │ │  │  │                          │ │
│  │                                       │ │  │  │                          │ │
│  │ DECISION: OpenAI GPT-4                │ │  │  │                          │ │
│  │ (High trending = best quality)       │ │  │  │                          │ │
│  └───────────┬──────────────────────────┘ │  │  └───────────┬───────────────┘ │
│              │                              │  │              │                 │
│  ┌───────────▼──────────────────────────┐ │  │  ┌───────────▼───────────────┐ │
│  │ Generate Content                     │ │  │  │ DECISION 6: Image Tool   │ │
│  │                                      │ │  │  │                          │ │
│  │ Using: OpenAIGPTTool                 │ │  │  │ Options:                 │ │
│  │ Topic: "Neural Networks"             │ │  │  │ ├─→ StableDiffusionTool ✓ │ │
│  │ Type: "trending"                      │ │  │  │ └─→ HuggingFaceImageTool │ │
│  │                                      │ │  │  │                          │ │
│  │ Result:                              │ │  │  │ Decision: StableDiffusion │ │
│  │ - Key concepts                        │ │  │  │ (Local, free, fast)       │ │
│  │ - Examples                            │ │  │  │                          │ │
│  │ - Caption                             │ │  │  │                          │ │
│  └───────────┬──────────────────────────┘ │  │  └───────────┬───────────────┘ │
│              │                              │  │              │                 │
│  ┌───────────▼──────────────────────────┐ │  │  ┌───────────▼───────────────┐ │
│  │ Quality Check (if enabled)           │ │  │  │ Generate Image            │ │
│  │                                      │ │  │  │                          │ │
│  │ Score: 0.92 (PASS) ✓                 │ │  │  │ Using: StableDiffusionTool│ │
│  │                                      │ │  │  │ Style: Trending           │ │
│  │                                      │ │  │  │ Format: Reel (1080x1080)  │ │
│  │                                      │ │  │  │                          │ │
│  │                                      │ │  │  │ Result:                  │ │
│  │                                      │ │  │  │ - Image URL               │ │
│  │                                      │ │  │  │                          │ │
│  └───────────┬──────────────────────────┘ │  │  └───────────┬───────────────┘ │
│              │                              │  │              │                 │
│              │                              │  │  ┌───────────▼───────────────┐ │
│              │                              │  │  │ Optimize Image            │ │
│              │                              │  │  │                          │ │
│              │                              │  │  │ Using: ImageOptimizerTool│ │
│              │                              │  │  │ Format: Reel              │ │
│              │                              │  │  │ Size: 1080x1080           │ │
│              │                              │  │  │                          │ │
│              │                              │  │  │ Result: Optimized URL     │ │
│              │                              │  │  └───────────┬───────────────┘ │
└──────────────┼───────────────┘  └──────────────┼─────────────────┘
               │                                    │
               └──────────────┬────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COORDINATOR ASSEMBLES                                    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Combine Results                                                      │  │
│  │ ├─→ Content: [Generated text]                                       │  │
│  │ ├─→ Image: [URL]                                                     │  │
│  │ └─→ Format: REEL                                                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ DECISION 7: Generate Hashtags                                        │  │
│  │ Using: HashtagGeneratorTool (from Content Creator Agent)            │  │
│  │ ├─→ #NeuralNetworks                                                  │  │
│  │ ├─→ #AIEducation                                                      │  │
│  │ ├─→ #TechTips                                                         │  │
│  │ ├─→ #Trending                                                         │  │
│  │ └─→ #AITrends                                                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ DECISION 8: Optimal Posting Time                                      │  │
│  │ Format: REEL                                                          │  │
│  │ ├─→ Reel: 19:00 (evening, highest engagement)                        │  │
│  │ ├─→ Story: 12:00 (midday)                                             │  │
│  │ └─→ Post: 18:00 (evening)                                             │  │
│  │                                                                        │  │
│  │ DECISION: 19:00 (Reel optimal time)                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INSTAGRAM TOOL                                       │
│                                                                             │
│  TOOL: InstagramTool (Used by Coordinator)                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ - Uses Instagram Graph API                                            │  │
│  │ - Handles authentication                                              │  │
│  │ - Supports Post/Story/Reel formats                                    │  │
│  │ - Validates image URLs                                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Post to Instagram                                                     │  │
│  │ ├─→ Format: REEL                                                      │  │
│  │ ├─→ Image URL: [Generated URL]                                         │  │
│  │ ├─→ Caption: [Generated caption with hashtags]                         │  │
│  │ ├─→ Posting Time: 19:00 (scheduled)                                   │  │
│  │ └─→ Status: POSTED                                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATABASE                                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Save to PostgreSQL                                                    │  │
│  │ ├─→ Content: [Generated content]                                      │  │
│  │ ├─→ Image URL: [URL]                                                  │  │
│  │ ├─→ Format: "reel"                                                     │  │
│  │ ├─→ Post ID: [Instagram post ID]                                      │  │
│  │ ├─→ Engagement Prediction: 12%                                         │  │
│  │ ├─→ Tool Used: "openai_gpt"                                            │  │
│  │ ├─→ Is Trending: true                                                  │  │
│  │ └─→ Posting Time: 19:00                                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SUCCESS!                                         │
│                  Content posted to Instagram                                │
│                      Format: REEL                                           │
│                  Predicted Engagement: 12%                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Decision Tree (Detailed)

```
START: User Request
│
├─→ FastAPI Backend
│   │
│   └─→ Coordinator Agent
│       │
│       ├─→ DECISION 1: Trending Check
│       │   │
│       │   ├─→ Topic trending? (score > 0.8)
│       │   │   ├─→ YES → High Priority Path
│       │   │   └─→ NO → Normal Path
│       │   │
│       │   └─→ Result: Trending data
│       │
│       ├─→ DECISION 2: Engagement Analysis
│       │   │
│       │   ├─→ What content type performs best?
│       │   ├─→ What posting time is optimal?
│       │   └─→ What format performs best?
│       │
│       │   └─→ Result: Engagement data
│       │
│       └─→ DECISION 3: Format Decision
│           │
│           ├─→ Is topic highly trending? (score > 0.8)
│           │   └─→ YES → REEL
│           │
│           ├─→ Content type = "trending"?
│           │   └─→ YES → REEL
│           │
│           ├─→ Content type = "entertaining"?
│           │   ├─→ Story performance > 7%?
│           │   │   ├─→ YES → STORY
│           │   │   └─→ NO → REEL
│           │
│           ├─→ Content type = "educational"?
│           │   └─→ YES → POST
│           │
│           └─→ Default → Best performing format
│               ├─→ Reel: 12% engagement
│               ├─→ Story: 8% engagement
│               └─→ Post: 4.5% engagement
│
├─→ Content Creator Agent
│   │
│   └─→ DECISION 4: LLM Tool Selection
│       │
│       ├─→ Is topic highly trending? (score > 0.8)
│       │   ├─→ Prefer Gemini? → Gemini Pro
│       │   └─→ Default → OpenAI GPT-4
│       │
│       ├─→ Quality = "premium"?
│       │   ├─→ Prefer Gemini? → Gemini Pro
│       │   └─→ Default → OpenAI GPT-4
│       │
│       ├─→ Speed = "fast"?
│       │   └─→ YES → Gemini Flash (free, fast)
│       │
│       ├─→ Budget = "low"?
│       │   ├─→ Local LLM available? → Local LLM
│       │   ├─→ Gemini Flash available? → Gemini Flash
│       │   └─→ Fallback → Hugging Face
│       │
│       └─→ Default Strategy:
│           ├─→ Try Local LLM (free)
│           ├─→ Try Gemini Flash (free, fast)
│           ├─→ Try Hugging Face (free)
│           └─→ Fallback → Gemini Pro / OpenAI
│
└─→ Image Generator Agent
    │
    └─→ DECISION 5: Image Style Selection
        │
        ├─→ Content type = "trending"?
        │   └─→ YES → Trending Style
        │
        ├─→ Content type = "entertaining"?
        │   └─→ YES → Artistic Style
        │
        └─→ Default → Best performing style
            └─→ (Based on user's past performance)
        │
        └─→ DECISION 6: Image Tool Selection
            │
            ├─→ Stable Diffusion local available?
            │   └─→ YES → Stable Diffusion (free, local)
            │
            └─→ Fallback → Hugging Face (free tier)
```

---

## Decision Points Summary Table

| # | Decision Point | Factors | Options | Decision Logic |
|---|---------------|---------|---------|----------------|
| 1 | **Trending Check** | Topic popularity | Trending / Not Trending | Score > 0.8 = Trending |
| 2 | **Engagement Analysis** | Past performance | Best content type, time, format | Query Instagram API |
| 3 | **Format Decision** | Trending, Content type, Performance | Post / Story / Reel | Trending → Reel, Educational → Post, Entertaining → Story |
| 4 | **LLM Tool** | Trending, Quality, Budget, Speed | OpenAI / Gemini Pro / Gemini Flash / Local / Hugging Face | Trending → OpenAI/Gemini Pro, Fast → Gemini Flash, Low budget → Free options |
| 5 | **Image Style** | Content type, Performance | Realistic / Artistic / Trending | Trending content → Trending style |
| 6 | **Image Tool** | Availability, Cost | Stable Diffusion / Hugging Face | Prefer local (free), fallback to cloud |
| 7 | **Hashtags** | Topic, Content type | Generated list | Based on topic and content type |
| 8 | **Posting Time** | Format | 18:00 / 12:00 / 19:00 | Reel: 19:00, Story: 12:00, Post: 18:00 |

---

## Flow Sequence (Numbered Steps)

```
STEP 1: User Request
    └─→ POST /api/content/generate
        └─→ Topic: "Neural Networks"

STEP 2: Coordinator Agent - Trending Check
    └─→ Tool: TrendingTopicsTool
        └─→ Result: YES (score: 0.85)

STEP 3: Coordinator Agent - Engagement Analysis
    └─→ Tool: EngagementAnalyzerTool
        └─→ Result: Best = "educational", Time = "18:00"

STEP 4: Coordinator Agent - Format Decision
    └─→ Tool: FormatDecisionTool
        └─→ Decision: REEL (trending topic, 12% engagement)

STEP 5: Content Creator Agent - LLM Tool Decision
    └─→ Decision: OpenAI GPT-4 (high trending = best quality)
        └─→ Generate content

STEP 6: Content Creator Agent - Quality Check
    └─→ Score: 0.92 (PASS)
        └─→ Content ready

STEP 7: Image Generator Agent - Style Decision
    └─→ Decision: Trending Style (content type = trending)

STEP 8: Image Generator Agent - Tool Decision
    └─→ Decision: Stable Diffusion Local (free, available)
        └─→ Generate image

STEP 9: Image Generator Agent - Optimization
    └─→ Format: Reel (1080x1080)
        └─→ Image ready

STEP 10: Coordinator - Assemble
    └─→ Combine content + image
    └─→ Generate hashtags
    └─→ Optimal time: 19:00 (Reel)

STEP 11: Instagram Tool
    └─→ Post as Reel
    └─→ Save to database

STEP 12: Success
    └─→ Return result to user
```

---

## Visual Tool Selection Flow

```
LLM Tool Selection:
┌─────────────────────────────────────────┐
│ Is topic highly trending? (score > 0.8)│
└───────────────┬─────────────────────────┘
                │
        ┌───────┴───────┐
        │               │
        YES             NO
        │               │
        ▼               ▼
┌───────────────┐  ┌──────────────────┐
│ OpenAI GPT-4  │  │ Quality premium? │
│ or            │  └────────┬─────────┘
│ Gemini Pro   │           │
└───────────────┘      ┌───┴───┐
                       YES     NO
                       │       │
                       ▼       ▼
                ┌─────────┐ ┌──────────────┐
                │Gemini   │ │ Speed fast?   │
                │Pro or   │ └──────┬────────┘
                │OpenAI   │        │
                └─────────┘    ┌───┴───┐
                               YES     NO
                               │       │
                               ▼       ▼
                        ┌──────────┐ ┌──────────────┐
                        │Gemini    │ │ Budget low?  │
                        │Flash     │ └──────┬───────┘
                        └──────────┘        │
                                        ┌───┴───┐
                                        YES     NO
                                        │       │
                                        ▼       ▼
                                ┌──────────┐ ┌──────────┐
                                │Local LLM │ │Gemini    │
                                │or        │ │Flash or  │
                                │Gemini    │ │Hugging   │
                                │Flash     │ │Face      │
                                └──────────┘ └──────────┘
```

---

## Format Decision Flow

```
Format Selection:
┌─────────────────────────────────────┐
│ Topic highly trending? (score > 0.8)│
└───────────────┬─────────────────────┘
                │
        ┌───────┴───────┐
        │               │
        YES             NO
        │               │
        ▼               ▼
┌───────────┐  ┌──────────────────────┐
│   REEL    │  │ Content type?        │
│ (12% eng) │  └──────────┬───────────┘
└───────────┘             │
                   ┌───────┴───────┐
                   │               │
              Trending        Educational
                   │               │
                   ▼               ▼
              ┌──────────┐    ┌──────────┐
              │   REEL   │    │   POST   │
              │ (12%)    │    │ (4.5%)   │
              └──────────┘    └──────────┘
                   │
              Entertaining
                   │
                   ▼
              ┌──────────┐
              │  STORY   │
              │  (8%)    │
              └──────────┘
```

---

---

## Complete Tool Inventory by Agent

### Coordinator Agent Tools:
1. **TrendingTopicsTool**
   - Purpose: Check if topic is trending
   - API: Google Trends (Free)
   - Returns: Trend score, is_trending flag

2. **EngagementAnalyzerTool**
   - Purpose: Analyze past post performance
   - API: Instagram Basic Display API (Free)
   - Returns: Best content type, posting time, format performance

3. **FormatDecisionTool**
   - Purpose: Decide Post/Story/Reel format
   - Logic: Based on trending, content type, performance
   - Returns: Recommended format, predicted engagement

4. **InstagramTool**
   - Purpose: Post content to Instagram
   - API: Instagram Graph API
   - Supports: Post, Story, Reel formats

---

### Content Creator Agent Tools:
1. **TrendingTopicsTool** (shared with Coordinator)
   - Purpose: Check trending status
   - Used for: LLM tool selection decision

2. **EngagementAnalyzerTool** (shared with Coordinator)
   - Purpose: Get performance data
   - Used for: Content type selection

3. **FormatDecisionTool** (shared with Coordinator)
   - Purpose: Format recommendation
   - Used for: Content generation context

4. **LocalLLMTool**
   - Purpose: Generate content using local LLM
   - Model: Ollama/LM Studio (Free)
   - Cost: $0.00

5. **GeminiFlashTool**
   - Purpose: Generate content using Gemini Flash
   - Model: Gemini 1.5 Flash
   - Cost: Free tier (15 req/min)

6. **GeminiProTool**
   - Purpose: Generate content using Gemini Pro
   - Model: Gemini 1.5 Pro
   - Cost: ~$0.001 per request

7. **OpenAIGPTTool**
   - Purpose: Generate content using OpenAI
   - Model: GPT-4
   - Cost: ~$0.03 per request

8. **HuggingFaceTool**
   - Purpose: Generate content using Hugging Face
   - Model: Various (Free tier)
   - Cost: Free tier (1000 req/month)

9. **HashtagGeneratorTool**
   - Purpose: Generate relevant hashtags
   - Logic: Based on topic and content type
   - Cost: Free (local logic)

---

### Image Generator Agent Tools:
1. **ImageStyleAnalyzerTool**
   - Purpose: Analyze which image style performs best
   - API: Instagram Basic Display API (Free)
   - Returns: Best style, color preferences, aspect ratio

2. **StableDiffusionLocalTool**
   - Purpose: Generate images locally
   - Model: Stable Diffusion (Local)
   - Cost: $0.00 (runs locally)

3. **HuggingFaceImageTool**
   - Purpose: Generate images using Hugging Face
   - Model: Stable Diffusion v1.5
   - Cost: Free tier

4. **ImageOptimizerTool**
   - Purpose: Optimize images for Instagram
   - Library: PIL/Pillow (Free)
   - Functions: Resize, compress, format conversion

---

## Tool Usage Flow

```
COORDINATOR AGENT:
├─→ TrendingTopicsTool → Check trending
├─→ EngagementAnalyzerTool → Get performance data
├─→ FormatDecisionTool → Decide format
└─→ InstagramTool → Post to Instagram

CONTENT CREATOR AGENT:
├─→ TrendingTopicsTool → Check trending (for LLM decision)
├─→ EngagementAnalyzerTool → Get best content type
├─→ FormatDecisionTool → Get format recommendation
├─→ LocalLLMTool / GeminiFlashTool / GeminiProTool / 
│   OpenAIGPTTool / HuggingFaceTool → Generate content
└─→ HashtagGeneratorTool → Generate hashtags

IMAGE GENERATOR AGENT:
├─→ ImageStyleAnalyzerTool → Get best style
├─→ StableDiffusionLocalTool / HuggingFaceImageTool → Generate image
└─→ ImageOptimizerTool → Optimize for format
```

---

This diagram is fully viewable directly in any text editor or markdown viewer - no external tools needed!
