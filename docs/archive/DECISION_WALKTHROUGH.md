# Decision Walkthrough: Coordinator Agent Step-by-Step

## How Coordinator Agent Makes Decisions

This document walks through how the Coordinator Agent makes decisions for different topics.

---

## Example 1: Topic = "LLM" (AI Education)

### Step-by-Step Decision Process

```
STEP 1: User Request
┌─────────────────────────────────────┐
│ POST /api/content/generate          │
│ {                                    │
│   "topic": "LLM",                   │
│   "user_id": "influencer_123"       │
│ }                                    │
└─────────────────────────────────────┘
         │
         ▼
STEP 2: Coordinator Agent Receives Request
┌─────────────────────────────────────┐
│ Coordinator Agent                   │
│ - Topic: "LLM"                      │
│ - User ID: "influencer_123"         │
└─────────────────────────────────────┘
         │
         ▼
DECISION 1: Check Trending Topics
┌─────────────────────────────────────────────────────────────┐
│ Using: TrendingTopicsTool                                 │
│                                                             │
│ Action: Check Google Trends for "LLM"                      │
│                                                             │
│ Conditions Checked:                                         │
│ ├─→ Search term: "LLM"                                      │
│ ├─→ Time period: Last 7 days                                │
│ └─→ Interest score calculation                              │
│                                                             │
│ Result:                                                     │
│ ├─→ Interest score: 75 (out of 100)                        │
│ ├─→ Is trending: YES (score > 50)                          │
│ ├─→ Trend score: 0.75                                       │
│ └─→ Recommendation: "capitalize_now"                       │
│                                                             │
│ DECISION LOGIC:                                             │
│ IF interest_score > 50:                                    │
│     is_trending = True                                      │
│     trend_score = interest_score / 100                      │
│ ELSE:                                                       │
│     is_trending = False                                     │
│     trend_score = interest_score / 100                      │
│                                                             │
│ Outcome:                                                    │
│ ✅ Topic is trending (score: 0.75)                         │
│ ⚠️  Not highly trending (score < 0.8)                      │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 2: Analyze Engagement
┌─────────────────────────────────────────────────────────────┐
│ Using: EngagementAnalyzerTool                              │
│                                                             │
│ Action: Query Instagram Basic Display API                  │
│ - Get last 30 posts for user "influencer_123"              │
│ - Analyze engagement by content type                       │
│ - Analyze engagement by format (post/story/reel)           │
│ - Find best posting times                                  │
│                                                             │
│ Conditions Checked:                                         │
│ ├─→ Past posts with "educational" content type             │
│ ├─→ Past posts with "entertaining" content type            │
│ ├─→ Past posts with "inspirational" content type          │
│ ├─→ Engagement rates for each content type                 │
│ ├─→ Engagement rates for each format                       │
│ └─→ Time-based engagement patterns                         │
│                                                             │
│ Analysis Results:                                           │
│ ├─→ Educational posts:                                     │
│ │   ├─→ Count: 15 posts                                    │
│ │   ├─→ Avg engagement: 4.8%                              │
│ │   └─→ Best time: 18:00                                   │
│ │                                                           │
│ ├─→ Entertaining posts:                                     │
│ │   ├─→ Count: 8 posts                                     │
│ │   ├─→ Avg engagement: 3.2%                                │
│ │   └─→ Best time: 12:00                                   │
│ │                                                           │
│ ├─→ Inspirational posts:                                    │
│ │   ├─→ Count: 7 posts                                     │
│ │   ├─→ Avg engagement: 3.5%                                │
│ │   └─→ Best time: 19:00                                   │
│ │                                                           │
│ └─→ Format Performance:                                     │
│     ├─→ Posts: 4.5% engagement, 5000 avg reach             │
│     ├─→ Stories: 8% engagement, 3000 avg reach             │
│     └─→ Reels: 12% engagement, 10000 avg reach              │
│                                                             │
│ DECISION LOGIC:                                             │
│ best_content_type = max(engagement_by_type)                │
│ best_format = max(engagement_by_format)                     │
│ best_posting_time = time_with_highest_engagement            │
│                                                             │
│ Outcome:                                                    │
│ ✅ Best content type: "educational" (4.8% engagement)      │
│ ✅ Best format: "reel" (12% engagement)                    │
│ ✅ Best posting time: "18:00" (for educational)            │
│ ✅ Avg engagement rate: 4.5%                                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 3: Format Decision
┌─────────────────────────────────────────────────────────────┐
│ Using: FormatDecisionTool                                  │
│                                                             │
│ Inputs:                                                     │
│ ├─→ Trending data: {is_trending: True, score: 0.75}       │
│ ├─→ Engagement data: {best_content_type: "educational"}    │
│ └─→ Topic: "LLM"                                           │
│                                                             │
│ DECISION LOGIC - Step by Step:                              │
│                                                             │
│ STEP 3.1: Check if highly trending                         │
│ ├─→ Condition: trending_data["is_trending"] == True        │
│ │   AND trending_data["trend_score"] > 0.8                  │
│ ├─→ Check: True AND 0.75 > 0.8?                            │
│ └─→ Result: FALSE (0.75 is not > 0.8)                      │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.2: Check content type                               │
│ ├─→ Condition: content_type == "trending"                  │
│ ├─→ Check: "educational" == "trending"?                     │
│ └─→ Result: FALSE                                          │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.3: Check if entertaining                            │
│ ├─→ Condition: content_type == "entertaining"               │
│ ├─→ Check: "educational" == "entertaining"?                 │
│ └─→ Result: FALSE                                          │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.4: Check if educational                             │
│ ├─→ Condition: content_type == "educational"               │
│ ├─→ Check: "educational" == "educational"?                  │
│ └─→ Result: TRUE ✅                                         │
│     └─→ BUT: Topic is trending (0.75)                      │
│         └─→ Need to balance: Educational vs Trending       │
│                                                             │
│ STEP 3.5: Final Decision Logic                             │
│ ├─→ IF trending AND educational:                           │
│ │   ├─→ Check format performance:                           │
│ │   │   ├─→ Reel: 12% engagement (highest)                  │
│ │   │   ├─→ Story: 8% engagement                            │
│ │   │   └─→ Post: 4.5% engagement                            │
│ │   │                                                       │
│ │   └─→ Decision: REEL                                     │
│ │       Reason: Trending topic + highest engagement        │
│ │                                                           │
│ └─→ ELSE IF just educational:                              │
│     └─→ Decision: POST (carousel works best)               │
│                                                             │
│ Outcome:                                                    │
│ ✅ Recommended format: "reel"                               │
│ ✅ Reason: "Topic is trending and reels have highest       │
│    engagement (12%)"                                        │
│ ✅ Predicted engagement: 12%                               │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 4: Pass to Content Creator Agent
┌─────────────────────────────────────────────────────────────┐
│ Coordinator calls Content Creator Agent                     │
│                                                             │
│ Parameters passed:                                          │
│ ├─→ topic: "LLM"                                            │
│ ├─→ content_type: "educational" (from engagement analysis) │
│ ├─→ format: "reel" (from format decision)                  │
│ ├─→ trending_data: {is_trending: True, score: 0.75}        │
│ └─→ context: {                                              │
│       "budget": "medium",                                   │
│       "quality": "high",                                    │
│       "verify_quality": True                                │
│     }                                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Example 2: Topic = "Ragi Dosa Recipe" (Food Content)

### Step-by-Step Decision Process

```
STEP 1: User Request
┌─────────────────────────────────────┐
│ POST /api/content/generate          │
│ {                                    │
│   "topic": "Ragi Dosa Recipe",      │
│   "user_id": "influencer_123"       │
│ }                                    │
└─────────────────────────────────────┘
         │
         ▼
STEP 2: Coordinator Agent Receives Request
┌─────────────────────────────────────┐
│ Coordinator Agent                   │
│ - Topic: "Ragi Dosa Recipe"         │
│ - User ID: "influencer_123"         │
└─────────────────────────────────────┘
         │
         ▼
DECISION 1: Check Trending Topics
┌─────────────────────────────────────────────────────────────┐
│ Using: TrendingTopicsTool                                 │
│                                                             │
│ Action: Check Google Trends for "Ragi Dosa Recipe"        │
│                                                             │
│ Conditions Checked:                                         │
│ ├─→ Search term: "Ragi Dosa Recipe"                        │
│ ├─→ Alternative: "Ragi Dosa" (broader term)                 │
│ ├─→ Time period: Last 7 days                                │
│ └─→ Interest score calculation                              │
│                                                             │
│ Result:                                                     │
│ ├─→ Interest score: 25 (out of 100)                        │
│ ├─→ Is trending: NO (score < 50)                           │
│ ├─→ Trend score: 0.25                                       │
│ └─→ Recommendation: "normal_post"                           │
│                                                             │
│ DECISION LOGIC:                                             │
│ IF interest_score > 50:                                    │
│     is_trending = True                                      │
│ ELSE:                                                       │
│     is_trending = False                                     │
│                                                             │
│ Outcome:                                                    │
│ ❌ Topic is NOT trending (score: 0.25)                     │
│ ✅ Normal flow (not high priority)                          │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 2: Analyze Engagement
┌─────────────────────────────────────────────────────────────┐
│ Using: EngagementAnalyzerTool                              │
│                                                             │
│ Action: Query Instagram Basic Display API                  │
│ - Get last 30 posts for user "influencer_123"              │
│                                                             │
│ Analysis Results:                                           │
│ ├─→ Educational posts:                                     │
│ │   ├─→ Count: 15 posts                                    │
│ │   ├─→ Avg engagement: 4.8%                              │
│ │   └─→ Best time: 18:00                                   │
│ │                                                           │
│ ├─→ Entertaining posts:                                    │
│ │   ├─→ Count: 8 posts                                     │
│ │   ├─→ Avg engagement: 3.2%                              │
│ │   └─→ Best time: 12:00                                   │
│ │                                                           │
│ ├─→ Food/Recipe posts: (NEW - detected from topic)         │
│ │   ├─→ Count: 5 posts                                     │
│ │   ├─→ Avg engagement: 6.5% (HIGHEST!)                    │
│ │   └─→ Best time: 19:00                                   │
│ │                                                           │
│ └─→ Format Performance:                                     │
│     ├─→ Posts: 4.5% engagement, 5000 avg reach             │
│     ├─→ Stories: 8% engagement, 3000 avg reach             │
│     └─→ Reels: 12% engagement, 10000 avg reach              │
│                                                             │
│ DECISION LOGIC:                                             │
│ ├─→ Topic contains "recipe" → Food content type            │
│ ├─→ Check if food content type exists in past posts        │
│ ├─→ IF food posts exist:                                    │
│ │   └─→ Use food content type performance                   │
│ └─→ ELSE:                                                   │
│     └─→ Use best overall content type                       │
│                                                             │
│ Outcome:                                                    │
│ ✅ Best content type: "food" (6.5% engagement)             │
│ ✅ Best format: "reel" (12% engagement)                     │
│ ✅ Best posting time: "19:00" (for food content)           │
│ ✅ Avg engagement rate: 6.5% (higher than educational!)    │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 3: Format Decision
┌─────────────────────────────────────────────────────────────┐
│ Using: FormatDecisionTool                                  │
│                                                             │
│ Inputs:                                                     │
│ ├─→ Trending data: {is_trending: False, score: 0.25}       │
│ ├─→ Engagement data: {best_content_type: "food"}          │
│ └─→ Topic: "Ragi Dosa Recipe"                              │
│                                                             │
│ DECISION LOGIC - Step by Step:                              │
│                                                             │
│ STEP 3.1: Check if highly trending                         │
│ ├─→ Condition: trending_data["is_trending"] == True        │
│ │   AND trending_data["trend_score"] > 0.8                  │
│ ├─→ Check: False AND 0.25 > 0.8?                          │
│ └─→ Result: FALSE                                          │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.2: Check content type                               │
│ ├─→ Condition: content_type == "trending"                  │
│ ├─→ Check: "food" == "trending"?                           │
│ └─→ Result: FALSE                                          │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.3: Check if entertaining                            │
│ ├─→ Condition: content_type == "entertaining"               │
│ ├─→ Check: "food" == "entertaining"?                        │
│ └─→ Result: FALSE                                          │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.4: Check if educational                             │
│ ├─→ Condition: content_type == "educational"               │
│ ├─→ Check: "food" == "educational"?                         │
│ └─→ Result: FALSE                                          │
│     └─→ Continue to next check                              │
│                                                             │
│ STEP 3.5: Check if food/recipe content                     │
│ ├─→ Condition: content_type == "food"                        │
│ │   OR topic contains "recipe"                              │
│ ├─→ Check: "food" == "food"?                                │
│ └─→ Result: TRUE ✅                                         │
│     └─→ Food content detected                               │
│                                                             │
│ STEP 3.6: Food Content Format Decision                     │
│ ├─→ Food content typically works well as:                  │
│ │   ├─→ Reels: High engagement (12%)                       │
│ │   │   └─→ Good for: Step-by-step cooking                 │
│ │   ├─→ Stories: Medium engagement (8%)                    │
│ │   │   └─→ Good for: Quick tips                           │
│ │   └─→ Posts: Lower engagement (4.5%)                     │
│ │       └─→ Good for: Detailed recipes                     │
│ │                                                           │
│ ├─→ Check format performance:                               │
│ │   ├─→ Reel: 12% engagement (highest)                      │
│ │   ├─→ Story: 8% engagement                                │
│ │   └─→ Post: 4.5% engagement                                │
│ │                                                           │
│ └─→ Decision: REEL                                         │
│     Reason: Food content + highest engagement format       │
│     (Reels work great for recipe content)                   │
│                                                             │
│ Outcome:                                                    │
│ ✅ Recommended format: "reel"                               │
│ ✅ Reason: "Food content performs best as reels (12%        │
│    engagement) - great for step-by-step cooking"            │
│ ✅ Predicted engagement: 12%                                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 4: Pass to Content Creator Agent
┌─────────────────────────────────────────────────────────────┐
│ Coordinator calls Content Creator Agent                     │
│                                                             │
│ Parameters passed:                                          │
│ ├─→ topic: "Ragi Dosa Recipe"                              │
│ ├─→ content_type: "food" (detected from topic)              │
│ ├─→ format: "reel" (from format decision)                   │
│ ├─→ trending_data: {is_trending: False, score: 0.25}        │
│ └─→ context: {                                              │
│       "budget": "medium",                                   │
│       "quality": "medium",                                  │
│       "verify_quality": False                               │
│     }                                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Logic Summary

### Decision 1: Trending Check
```
IF interest_score > 50:
    is_trending = True
    trend_score = interest_score / 100
ELSE:
    is_trending = False
    trend_score = interest_score / 100

Examples:
- "LLM": score = 75 → is_trending = True, trend_score = 0.75
- "Ragi Dosa Recipe": score = 25 → is_trending = False, trend_score = 0.25
```

### Decision 2: Engagement Analysis
```
1. Query Instagram API for past posts
2. Group posts by content type
3. Calculate engagement rate for each type
4. Find best posting time for each type
5. Analyze format performance

Logic:
best_content_type = type_with_highest_engagement
best_format = format_with_highest_engagement
best_posting_time = time_with_highest_engagement

Special handling:
- IF topic contains "recipe" → Detect as "food" content type
- IF food content type exists in past posts → Use its performance
- ELSE → Use best overall content type
```

### Decision 3: Format Decision
```
STEP 1: Check if highly trending (score > 0.8)
    IF True → REEL (viral content)

STEP 2: Check content type
    IF "trending" → REEL
    IF "entertaining" → Check story performance
        IF story > 7% → STORY
        ELSE → REEL
    IF "educational" → POST (carousel works best)
    IF "food" → REEL (step-by-step works great)

STEP 3: Default
    Use format with highest engagement
    (Usually REEL: 12% > Story: 8% > Post: 4.5%)
```

---

## Complete Decision Flow Table

| Topic | Trending? | Score | Content Type | Format | Reason |
|-------|-----------|-------|--------------|--------|--------|
| "LLM" | Yes | 0.75 | Educational | Reel | Trending + Educational, Reels have 12% engagement |
| "Ragi Dosa Recipe" | No | 0.25 | Food | Reel | Food content, Reels work best for recipes (12%) |
| "Neural Networks" | Yes | 0.85 | Educational | Reel | Highly trending (0.85), Reel for viral (12%) |
| "Python Basics" | No | 0.30 | Educational | Post | Not trending, Educational → Post (carousel) |
| "AI Art" | Yes | 0.90 | Entertaining | Reel | Highly trending, Entertaining → Reel (12%) |

---

## Key Conditions Explained

### Condition 1: Highly Trending (score > 0.8)
- **When**: Topic is very popular right now
- **Action**: Always use REEL format
- **Reason**: Reels have highest engagement (12%) and are best for viral content

### Condition 2: Trending but not highly (0.5 < score ≤ 0.8)
- **When**: Topic is somewhat popular
- **Action**: Consider trending in format decision, but also check content type
- **Reason**: Balance between trending opportunity and content type performance

### Condition 3: Not Trending (score ≤ 0.5)
- **When**: Topic is not currently popular
- **Action**: Rely on content type and format performance
- **Reason**: Focus on what works best for this type of content

### Condition 4: Content Type Detection
- **"recipe" in topic** → Food content type
- **"tutorial" in topic** → Educational content type
- **"tips" in topic** → Entertaining content type
- **Default** → Use best performing content type from past posts

### Condition 5: Format Selection
- **Reel**: Best for trending, food (recipes), entertaining content
- **Story**: Best for entertaining, quick tips, behind-the-scenes
- **Post**: Best for educational, detailed information, carousel content

---

---

## Example 3: New User - No Engagement Data

### Scenario: New Instagram Influencer

```
STEP 1: User Request
┌─────────────────────────────────────┐
│ POST /api/content/generate          │
│ {                                    │
│   "topic": "LLM",                   │
│   "user_id": "new_influencer_456",  │
│   "format": null  // Optional       │
│ }                                    │
└─────────────────────────────────────┘
         │
         ▼
DECISION 2: Analyze Engagement (NEW USER)
┌─────────────────────────────────────────────────────────────┐
│ Using: EngagementAnalyzerTool                              │
│                                                             │
│ Action: Query Instagram API                               │
│                                                             │
│ Result:                                                     │
│ ├─→ Post count: 0                                          │
│ ├─→ Engagement data: NOT AVAILABLE                         │
│ └─→ User status: NEW_USER                                  │
│                                                             │
│ DECISION LOGIC:                                             │
│ IF post_count == 0:                                         │
│     has_data = False                                        │
│     FLAG: needs_engagement_data = True                      │
│                                                             │
│ Outcome:                                                    │
│ ⚠️  No engagement data available                           │
│ ✅ Detected content type: "educational" (from topic)       │
│ ⚠️  Format: PENDING (needs decision)                       │
│ 🔔 FLAG: Human-in-the-loop or use default                  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
DECISION 3: Format Decision (NEW USER)
┌─────────────────────────────────────────────────────────────┐
│ Using: FormatDecisionTool                                  │
│                                                             │
│ Inputs:                                                     │
│ ├─→ Trending data: {is_trending: True, score: 0.75}       │
│ ├─→ Engagement data: {has_data: False}                     │
│ ├─→ User preference: {format: null}                         │
│ └─→ Topic: "LLM"                                           │
│                                                             │
│ DECISION LOGIC - New User Path:                             │
│                                                             │
│ STEP 3.1: Check user preference                            │
│ ├─→ Condition: user_preference["format"] is not null       │
│ ├─→ Check: null?                                            │
│ └─→ Result: FALSE (no user preference)                     │
│     └─→ Continue to default logic                           │
│                                                             │
│ STEP 3.2: Check if trending                                │
│ ├─→ Condition: trending_data["is_trending"] == True        │
│ │   AND trending_data["trend_score"] > 0.5                  │
│ ├─→ Check: True AND 0.75 > 0.5?                            │
│ └─→ Result: TRUE ✅                                         │
│     └─→ Topic is trending → Use REEL                        │
│                                                             │
│ STEP 3.3: Final Decision                                   │
│ ├─→ IF trending (score > 0.5):                              │
│ │   └─→ Decision: REEL                                     │
│ │       Reason: "Topic is trending, reels work best"        │
│ │                                                           │
│ ├─→ ELSE IF content type detected:                         │
│ │   ├─→ Educational → POST (default)                         │
│ │   ├─→ Food/Recipe → REEL (step-by-step)                  │
│ │   └─→ Entertaining → STORY (quick)                        │
│ │                                                           │
│ └─→ ELSE:                                                   │
│     └─→ Request human input                                 │
│                                                             │
│ Outcome:                                                    │
│ ✅ Recommended format: "reel" (intelligent default)       │
│ ✅ Reason: "Topic is trending (score: 0.75), reels work    │
│    best for trending content"                               │
│ ⚠️  Note: "No engagement data available, using defaults.   │
│    You can override by specifying format in request."       │
│ ✅ Can override: True                                        │
└─────────────────────────────────────────────────────────────┘
```

### Option: User Specifies Format

```
STEP 1: User Request (with format)
┌─────────────────────────────────────┐
│ POST /api/content/generate          │
│ {                                    │
│   "topic": "LLM",                   │
│   "user_id": "new_influencer_456",  │
│   "format": "post"  // User specifies│
│ }                                    │
└─────────────────────────────────────┘
         │
         ▼
DECISION 3: Format Decision (User Specified)
┌─────────────────────────────────────────────────────────────┐
│ Using: FormatDecisionTool                                  │
│                                                             │
│ Inputs:                                                     │
│ ├─→ User preference: {format: "post"}                     │
│                                                             │
│ DECISION LOGIC:                                             │
│ ├─→ Check: user_preference["format"] is not null?          │
│ └─→ Result: TRUE ✅                                         │
│     └─→ Use user preference (HUMAN DECISION)                │
│                                                             │
│ Outcome:                                                    │
│ ✅ Format: "post" (user specified)                        │
│ ✅ Reason: "User specified format: post"                   │
│ ✅ Source: "user_preference"                                │
│ ✅ Needs human input: False                                 │
└─────────────────────────────────────────────────────────────┘
```

### Option: Human-in-the-Loop Request

```
STEP 1: User Request (request decision)
┌─────────────────────────────────────┐
│ POST /api/content/generate          │
│ {                                    │
│   "topic": "LLM",                   │
│   "user_id": "new_influencer_456",   │
│   "request_human_input": true        │
│ }                                    │
└─────────────────────────────────────┘
         │
         ▼
RESPONSE: Format Decision Request
┌─────────────────────────────────────────────────────────────┐
│ {                                                            │
│   "status": "needs_format_decision",                        │
│   "message": "No engagement data. Please choose format:",   │
│   "options": {                                               │
│     "post": {                                                │
│       "description": "Best for detailed educational",       │
│       "engagement_estimate": "4-6%"                        │
│     },                                                       │
│     "story": {                                               │
│       "description": "Best for quick tips",                 │
│       "engagement_estimate": "6-10%"                        │
│     },                                                       │
│     "reel": {                                                │
│       "description": "Best for trending topics",            │
│       "engagement_estimate": "10-15%",                      │
│       "recommended": true,                                  │
│       "reason": "Topic is trending, reels work best"        │
│     }                                                       │
│   },                                                         │
│   "recommendation": "reel"                                  │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
STEP 2: User Chooses Format
┌─────────────────────────────────────┐
│ POST /api/content/generate          │
│ {                                    │
│   "topic": "LLM",                   │
│   "user_id": "new_influencer_456",   │
│   "format": "reel"  // User chooses │
│ }                                    │
└─────────────────────────────────────┘
```

---

## Decision Priority for New Users

```
Priority Order:
1. User Specified Format (Highest)
   └─→ If user provides format → Use it immediately

2. Intelligent Default
   └─→ If no user preference → Use smart defaults
       ├─→ Trending topic → Reel
       ├─→ Educational → Post
       ├─→ Food/Recipe → Reel
       └─→ Default → Reel

3. Human-in-the-Loop (Optional)
   └─→ If requested → Return options for user to choose
```

---

This walkthrough shows exactly how the Coordinator Agent makes decisions step-by-step, including handling new users without engagement data!

