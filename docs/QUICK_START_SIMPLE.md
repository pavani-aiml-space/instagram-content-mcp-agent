# Quick Start: Simple Multi-Agent System (1-3 Decisions)

## For Beginners: Keep It Simple!

**Only 3 decision points in the entire flow:**
1. **Topic** - What to create about
2. **Format** - Post/Story/Reel (optional - can auto-decide)
3. **Posting Time** - When to post (optional - can auto-decide)

Everything else is **automatic**!

---

## Simplest Flow (1 Decision Only)

```
User Input:
┌─────────────────────────────────────┐
│ Topic: "LLM"                         │
└─────────────────────────────────────┘
         │
         ▼
System Automatically:
┌─────────────────────────────────────┐
│ ✅ Checks if trending                │
│ ✅ Decides format (Reel - trending)  │
│ ✅ Generates content                 │
│ ✅ Generates image                   │
│ ✅ Generates hashtags                │
│ ✅ Decides posting time (19:00)      │
│ ✅ Posts to Instagram                │
└─────────────────────────────────────┘
         │
         ▼
Success!
```

**That's it!** Just provide the topic, system does the rest.

---

## With Format Choice (2 Decisions)

```
User Input:
┌─────────────────────────────────────┐
│ Topic: "LLM"                         │
│ Format: "post" (user chooses)        │
└─────────────────────────────────────┘
         │
         ▼
System Automatically:
┌─────────────────────────────────────┐
│ ✅ Uses user's format choice         │
│ ✅ Generates content                 │
│ ✅ Generates image                   │
│ ✅ Generates hashtags                │
│ ✅ Decides posting time (18:00)      │
│ ✅ Posts to Instagram                │
└─────────────────────────────────────┘
```

**User controls format, system handles everything else.**

---

## Full Control (3 Decisions)

```
User Input:
┌─────────────────────────────────────┐
│ Topic: "LLM"                         │
│ Format: "reel" (user chooses)        │
│ Posting Time: "20:00" (user chooses)  │
└─────────────────────────────────────┘
         │
         ▼
System Automatically:
┌─────────────────────────────────────┐
│ ✅ Uses user's choices               │
│ ✅ Generates content                 │
│ ✅ Generates image                   │
│ ✅ Generates hashtags                │
│ ✅ Posts at user's specified time    │
└─────────────────────────────────────┘
```

**User controls everything, system executes.**

---

## Simple API Examples

### Example 1: Minimal (1 Decision)

```bash
POST /api/content/generate
{
    "topic": "LLM"
}

# System decides:
# - Format: "reel" (topic is trending)
# - Posting time: "19:00" (best for reels)
```

### Example 2: With Format (2 Decisions)

```bash
POST /api/content/generate
{
    "topic": "LLM",
    "format": "post"
}

# System decides:
# - Posting time: "18:00" (best for posts)
```

### Example 3: Full Control (3 Decisions)

```bash
POST /api/content/generate
{
    "topic": "LLM",
    "format": "reel",
    "posting_time": "20:00"
}

# System uses all user choices
```

---

## Simple Frontend (React)

```jsx
function SimpleGenerator() {
    const [topic, setTopic] = useState("");
    const [format, setFormat] = useState(null);  // Optional
    const [postingTime, setPostingTime] = useState("best");  // Optional
    
    return (
        <form>
            {/* Decision 1: Topic (Required) */}
            <input 
                placeholder="What topic? (e.g., LLM, Ragi Dosa Recipe)"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
            />
            
            {/* Decision 2: Format (Optional) */}
            <div>
                <label>Format (optional - we'll decide if you don't)</label>
                <select onChange={(e) => setFormat(e.target.value)}>
                    <option value="">Let System Decide</option>
                    <option value="post">📸 Post</option>
                    <option value="story">📱 Story</option>
                    <option value="reel">🎬 Reel</option>
                </select>
            </div>
            
            {/* Decision 3: Posting Time (Optional) */}
            <div>
                <label>When to post? (optional)</label>
                <select value={postingTime} onChange={(e) => setPostingTime(e.target.value)}>
                    <option value="best">🎯 Best Time (Recommended)</option>
                    <option value="now">⏰ Post Now</option>
                    <option value="schedule">📅 Schedule</option>
                </select>
            </div>
            
            <button>Generate & Post</button>
        </form>
    );
}
```

---

## Decision Logic (Simplified)

```python
# Coordinator Agent - Simplified
class CoordinatorAgent:
    def generate_post(self, topic, format=None, posting_time=None):
        """
        Simple 3-decision flow
        """
        # Decision 1: Topic (from user - no processing)
        
        # Decision 2: Format (user choice OR auto)
        if not format:
            format = self._auto_decide_format(topic)
        
        # Decision 3: Posting time (user choice OR auto)
        if not posting_time or posting_time == "best":
            posting_time = self._auto_decide_time(format)
        
        # Everything else automatic
        content = self.content_agent.generate(topic)
        image = self.image_agent.generate(topic, format)
        hashtags = self.hashtag_tool.generate(topic)
        
        # Post
        return self.instagram_tool.post(content, image, format, posting_time)
    
    def _auto_decide_format(self, topic):
        """Simple auto-format decision"""
        trending = self.trending_checker.execute(topic)
        
        if trending["is_trending"]:
            return "reel"
        
        if "recipe" in topic.lower():
            return "reel"
        
        return "post"  # Default
    
    def _auto_decide_time(self, format):
        """Simple auto-time decision"""
        return {
            "reel": "19:00",
            "story": "12:00",
            "post": "18:00"
        }.get(format, "19:00")
```

---

## What's Automatic vs Manual

### Automatic (No User Input Needed):
- ✅ Check if topic is trending
- ✅ Generate content (using best LLM tool)
- ✅ Generate image (using best image tool)
- ✅ Generate hashtags
- ✅ Optimize content for format
- ✅ Choose posting time (if not specified)
- ✅ Post to Instagram

### Manual (User Can Choose):
- 📝 Topic (required)
- 📱 Format (optional - can auto-decide)
- ⏰ Posting time (optional - can auto-decide)

---

## Learning Path

### Level 1: Beginner (1 Decision)
```
Just provide topic → System does everything
```

### Level 2: Intermediate (2 Decisions)
```
Provide topic + format → System handles timing
```

### Level 3: Advanced (3 Decisions)
```
Provide topic + format + time → Full control
```

**Start simple, add control as you learn!**

---

## Summary

**For Beginners:**
- ✅ Only 1 decision needed: Topic
- ✅ System handles format, timing, everything else
- ✅ Simple and fast

**For More Control:**
- ✅ Add format choice (2 decisions)
- ✅ Add posting time (3 decisions)
- ✅ Still simple, just more control

**Key Principle:**
- Start with minimal decisions
- Add control only when needed
- System makes good defaults automatically

This keeps it simple for beginners while allowing growth as you learn!

