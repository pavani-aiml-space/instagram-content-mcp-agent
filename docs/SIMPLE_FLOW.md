# Simplified Flow: 1-3 Decisions Only

## Beginner-Friendly Multi-Agent Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    USER INPUT (1-3 Decisions)                               │
│                                                                             │
│  DECISION 1: Topic (Required)                                              │
│  └─→ User types: "LLM" or "Ragi Dosa Recipe"                               │
│                                                                             │
│  DECISION 2: Format (Optional - Can Auto-Decide)                           │
│  └─→ User chooses: Post / Story / Reel                                      │
│      OR: Let system decide (automatic)                                      │
│                                                                             │
│  DECISION 3: Posting Time (Optional - Can Auto-Decide)                    │
│  └─→ User chooses: Now / Schedule / Best Time                                │
│      OR: Use best time (automatic)                                          │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              COORDINATOR AGENT (Automatic)                                 │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Automatic: Check Trending                                            │  │
│  │ Using: TrendingTopicsTool                                            │  │
│  │ Result: {is_trending: True, score: 0.75}                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Automatic: Decide Format (if user didn't specify)                   │  │
│  │ Using: FormatDecisionTool                                            │  │
│  │ Logic:                                                               │  │
│  │ ├─→ IF user specified format → Use it                              │  │
│  │ └─→ ELSE:                                                           │  │
│  │     ├─→ Trending? → Reel                                            │  │
│  │     ├─→ Recipe? → Reel                                               │  │
│  │     └─→ Default → Post                                              │  │
│  │ Result: "reel" (auto-decided)                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Automatic: Decide Posting Time (if user didn't specify)             │  │
│  │ Logic:                                                               │  │
│  │ ├─→ IF user specified time → Use it                                │  │
│  │ └─→ ELSE:                                                           │  │
│  │     ├─→ Reel → 19:00                                                │  │
│  │     ├─→ Story → 12:00                                                │  │
│  │     └─→ Post → 18:00                                                │  │
│  │ Result: "19:00" (auto-decided for Reel)                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
┌───────────────────────────────┐  ┌───────────────────────────────┐
│   CONTENT CREATOR AGENT        │  │   IMAGE GENERATOR AGENT        │
│   (Automatic)                  │  │   (Automatic)                  │
│                                │  │                                │
│  Automatic:                    │  │  Automatic:                    │
│  ├─→ Choose LLM tool            │  │  ├─→ Choose image style        │
│  ├─→ Generate content           │  │  ├─→ Choose image tool        │
│  └─→ Generate hashtags          │  │  ├─→ Generate image           │
│                                │  │  └─→ Optimize for format       │
└───────────────┬─────────────────┘  └───────────────┬─────────────────┘
                │                                    │
                └──────────────┬─────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              COORDINATOR ASSEMBLES (Automatic)                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Combine: Content + Image + Hashtags                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              INSTAGRAM TOOL (Automatic)                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Post to Instagram                                                    │  │
│  │ Format: reel (from decision 2)                                      │  │
│  │ Time: 19:00 (from decision 3)                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SUCCESS!                                                 │
│         Content posted automatically!                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Decision Points Summary

| # | Decision | Required? | Options | Default |
|---|----------|----------|---------|---------|
| 1 | **Topic** | ✅ Yes | User types | None |
| 2 | **Format** | ❌ No | Post / Story / Reel | Auto: Reel (if trending) |
| 3 | **Posting Time** | ❌ No | Now / Schedule / Best Time | Auto: Best time for format |

---

## Three Levels of Control

### Level 1: Minimal (1 Decision)
```json
{
    "topic": "LLM"
}
```
**System decides:** Format, Posting Time, Everything else

### Level 2: Moderate (2 Decisions)
```json
{
    "topic": "LLM",
    "format": "post"
}
```
**System decides:** Posting Time, Everything else

### Level 3: Full Control (3 Decisions)
```json
{
    "topic": "LLM",
    "format": "reel",
    "posting_time": "20:00"
}
```
**System decides:** Everything else (content, image, hashtags)

---

## Simple Decision Tree

```
START
 │
 ├─→ Decision 1: Topic (User Input)
 │   └─→ Required: Yes
 │
 ├─→ Decision 2: Format
 │   ├─→ User specified?
 │   │   └─→ YES → Use user choice
 │   └─→ NO → Auto-decide
 │       ├─→ Trending? → Reel
 │       ├─→ Recipe? → Reel
 │       └─→ Default → Post
 │
 ├─→ Decision 3: Posting Time
 │   ├─→ User specified?
 │   │   └─→ YES → Use user choice
 │   └─→ NO → Auto-decide
 │       ├─→ Reel → 19:00
 │       ├─→ Story → 12:00
 │       └─→ Post → 18:00
 │
 └─→ Everything Else: Automatic
     ├─→ Generate content
     ├─→ Generate image
     ├─→ Generate hashtags
     └─→ Post to Instagram
```

---

## What's Automatic

✅ **Automatic (No Decisions Needed):**
- Check if topic is trending
- Choose LLM tool (based on trending/quality)
- Generate content
- Choose image tool
- Generate image
- Generate hashtags
- Optimize content
- Post to Instagram

📝 **Manual (User Decisions - Only 1-3):**
- Topic (required)
- Format (optional)
- Posting time (optional)

---

## Beginner-Friendly Features

1. **Start Simple**: Just provide topic, system handles rest
2. **Learn Gradually**: Add format choice when ready
3. **Full Control**: Add posting time when needed
4. **Smart Defaults**: System makes good decisions automatically
5. **No Complexity**: No complex decision trees or multiple steps

---

This simplified flow makes it easy for beginners to get started while allowing more control as they learn!

