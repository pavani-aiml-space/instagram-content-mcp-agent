# New User Decision Handling: Human-in-the-Loop (Simplified)

## Problem: New Instagram Influencer

**Challenge**: New influencers don't have engagement data to make informed decisions.

**Solution (Simplified for Beginners)**: 
1. **Only 1-3 decisions needed** - Keep it simple!
2. Allow user to manually specify format (optional)
3. Use intelligent defaults when no data available
4. Everything else is automatic

## Quick Start: Minimal Decisions

**For absolute beginners:**
- ✅ Just provide topic → System handles everything else

**For more control:**
- ✅ Topic + Format → 2 decisions
- ✅ Topic + Format + Posting Time → 3 decisions

**That's it!** No complex decision trees.

---

## Decision Flow for New Users

### Scenario: New User, No Engagement Data

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
STEP 2: Check User Status
┌─────────────────────────────────────────────────────────────┐
│ EngagementAnalyzerTool                                     │
│                                                             │
│ Action: Query Instagram API for past posts                 │
│                                                             │
│ Result:                                                     │
│ ├─→ Post count: 0                                          │
│ ├─→ Engagement data: NOT AVAILABLE                         │
│ └─→ User status: NEW_USER                                  │
│                                                             │
│ Flag: needs_engagement_data = True                         │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
STEP 3: Format Decision Options
┌─────────────────────────────────────────────────────────────┐
│ FormatDecisionTool                                         │
│                                                             │
│ Inputs:                                                     │
│ ├─→ User has engagement data: FALSE                        │
│ ├─→ User specified format: null (or "reel"/"post"/"story") │
│ ├─→ Trending data: Available                               │
│ └─→ Topic: "LLM"                                           │
│                                                             │
│ DECISION LOGIC:                                             │
│                                                             │
│ OPTION 1: User Specified Format                            │
│ ├─→ IF user_preference["format"] is set:                   │
│ │   └─→ Use user preference                                │
│ │       Example: user wants "post" → Use POST              │
│ │                                                           │
│ OPTION 2: Intelligent Default                              │
│ ├─→ IF topic is trending (score > 0.5):                    │
│ │   └─→ Default: REEL (best for trending)                  │
│ │                                                           │
│ ├─→ ELSE IF content type detected:                         │
│ │   ├─→ Educational → POST (carousel for details)          │
│ │   ├─→ Food/Recipe → REEL (step-by-step)                  │
│ │   └─→ Entertaining → STORY (quick, engaging)             │
│ │                                                           │
│ └─→ ELSE:                                                   │
│     └─→ Request human input                                │
│                                                             │
│ OPTION 3: Human-in-the-Loop                                │
│ ├─→ IF needs_human_input == True:                          │
│ │   └─→ Return decision request                             │
│ │       {                                                   │
│ │         "format": null,                                  │
│ │         "needs_human_input": true,                       │
│ │         "options": ["post", "story", "reel"],            │
│ │         "recommendation": "reel",                        │
│ │         "reason": "Topic is trending, reels work best"  │
│ │       }                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Options

### Option 1: User Specifies Format in Request

```python
# API Request
POST /api/content/generate
{
    "topic": "LLM",
    "user_id": "new_influencer_456",
    "format": "reel"  // User manually specifies
}

# Coordinator Agent Logic
def decide_format(self, trending_data, engagement_data, user_preference):
    # Priority 1: User preference (human decision)
    if user_preference.get("format"):
        return {
            "format": user_preference["format"],
            "reason": f"User specified: {user_preference['format']}",
            "needs_human_input": False
        }
    
    # Priority 2: Use engagement data if available
    if engagement_data.get("has_data"):
        return self._decide_from_engagement(trending_data, engagement_data)
    
    # Priority 3: Intelligent default for new users
    return self._decide_for_new_user(trending_data, engagement_data)
```

### Option 2: Human-in-the-Loop (Interactive)

```python
# API Request (First Call)
POST /api/content/generate
{
    "topic": "LLM",
    "user_id": "new_influencer_456"
}

# Response (Decision Request)
{
    "status": "needs_format_decision",
    "message": "No engagement data available. Please choose format:",
    "options": {
        "post": {
            "description": "Best for detailed educational content",
            "engagement_estimate": "4-6%"
        },
        "story": {
            "description": "Best for quick tips and behind-the-scenes",
            "engagement_estimate": "6-10%"
        },
        "reel": {
            "description": "Best for trending topics and step-by-step",
            "engagement_estimate": "10-15%",
            "recommended": true,
            "reason": "Topic is trending, reels have highest engagement"
        }
    },
    "recommendation": "reel"
}

# User Response (Second Call)
POST /api/content/generate
{
    "topic": "LLM",
    "user_id": "new_influencer_456",
    "format": "reel"  // User chooses
}
```

### Option 3: Default with Override Option

```python
# Coordinator Agent Logic
def decide_format(self, trending_data, engagement_data, user_preference):
    # Check if new user
    if not engagement_data.get("has_data"):
        # Use intelligent default
        default_format = self._get_intelligent_default(trending_data)
        
        # If user wants to override, they can specify
        if user_preference.get("format"):
            return {
                "format": user_preference["format"],
                "reason": f"User override: {user_preference['format']}",
                "default_was": default_format
            }
        
        return {
            "format": default_format,
            "reason": f"New user - using default: {default_format}",
            "can_override": True,
            "needs_human_input": False
        }
    
    # Existing user logic...
```

---

## Updated Decision Logic for New Users

### FormatDecisionTool - New User Handling

```python
class FormatDecisionTool:
    def execute(self, user_id, topic, trending_data, content_type, 
                engagement_data, user_preference=None):
        """
        Decision logic with new user handling
        """
        # Priority 1: User specified format (human decision)
        if user_preference and user_preference.get("format"):
            return {
                "recommended_format": user_preference["format"],
                "reason": f"User specified format: {user_preference['format']}",
                "needs_human_input": False,
                "source": "user_preference"
            }
        
        # Priority 2: Check if user has engagement data
        if not engagement_data.get("has_data"):
            # NEW USER PATH
            return self._decide_for_new_user(
                topic, trending_data, content_type, user_preference
            )
        
        # Priority 3: Use engagement data (existing user)
        return self._decide_from_engagement(
            trending_data, engagement_data, content_type
        )
    
    def _decide_for_new_user(self, topic, trending_data, content_type, 
                             user_preference):
        """
        Decision logic for new users without engagement data
        """
        # Option 1: Request human input
        if user_preference and user_preference.get("request_human_input"):
            return {
                "recommended_format": None,
                "needs_human_input": True,
                "options": ["post", "story", "reel"],
                "recommendation": self._get_default_recommendation(
                    trending_data, content_type
                ),
                "reason": "New user - please choose format"
            }
        
        # Option 2: Use intelligent default
        default = self._get_intelligent_default(trending_data, content_type)
        
        return {
            "recommended_format": default,
            "reason": self._get_default_reason(default, trending_data, content_type),
            "needs_human_input": False,
            "source": "intelligent_default",
            "can_override": True,
            "note": "No engagement data available, using defaults. You can override by specifying format."
        }
    
    def _get_intelligent_default(self, trending_data, content_type):
        """
        Get intelligent default format for new users
        """
        # If highly trending, use Reel
        if trending_data.get("is_trending") and trending_data.get("trend_score", 0) > 0.8:
            return "reel"
        
        # If trending (but not highly), use Reel
        if trending_data.get("is_trending") and trending_data.get("trend_score", 0) > 0.5:
            return "reel"
        
        # Based on content type
        if content_type == "food" or "recipe" in content_type.lower():
            return "reel"  # Recipes work great as reels
        
        if content_type == "educational":
            return "post"  # Educational content works well as carousel posts
        
        if content_type == "entertaining":
            return "story"  # Entertaining content works well as stories
        
        # Default: Reel (highest industry average engagement)
        return "reel"
    
    def _get_default_reason(self, format, trending_data, content_type):
        """
        Get reason for default format recommendation
        """
        reasons = {
            "reel": f"Reel recommended - {'Topic is trending' if trending_data.get('is_trending') else 'Reels have highest average engagement (10-15%)'}",
            "story": "Story recommended - Quick, engaging format for entertaining content",
            "post": "Post recommended - Best for detailed educational content (carousel format)"
        }
        return reasons.get(format, "Reel recommended as default")
```

---

## API Endpoints for Human-in-the-Loop

### Endpoint 1: Generate Content (with format option)

```python
POST /api/content/generate
{
    "topic": "LLM",
    "user_id": "new_influencer_456",
    "format": "reel",  // Optional: user can specify
    "request_human_input": false  // Optional: request decision
}

Response:
{
    "status": "processing",
    "format": "reel",
    "format_source": "user_preference",  // or "intelligent_default" or "engagement_data"
    "reason": "User specified format: reel"
}
```

### Endpoint 2: Request Format Decision

```python
POST /api/content/request-format-decision
{
    "topic": "LLM",
    "user_id": "new_influencer_456"
}

Response:
{
    "status": "needs_format_decision",
    "options": {
        "post": {
            "description": "Best for detailed educational content",
            "engagement_estimate": "4-6%",
            "best_for": ["Educational", "Tutorials", "Carousel content"]
        },
        "story": {
            "description": "Best for quick tips and behind-the-scenes",
            "engagement_estimate": "6-10%",
            "best_for": ["Entertaining", "Quick tips", "Behind scenes"]
        },
        "reel": {
            "description": "Best for trending topics and step-by-step",
            "engagement_estimate": "10-15%",
            "best_for": ["Trending", "Recipes", "Step-by-step"],
            "recommended": true,
            "reason": "Topic is trending, reels have highest engagement"
        }
    },
    "recommendation": "reel",
    "trending_info": {
        "is_trending": true,
        "score": 0.75
    }
}
```

### Endpoint 3: Confirm Format Decision

```python
POST /api/content/generate
{
    "topic": "LLM",
    "user_id": "new_influencer_456",
    "format": "reel"  // User's choice
}
```

---

## Frontend Integration (React)

### Component: Format Selection

```jsx
function FormatSelector({ topic, trendingData, onFormatSelected }) {
    const [format, setFormat] = useState(null);
    const [recommendation, setRecommendation] = useState(null);
    
    useEffect(() => {
        // Request format recommendation
        fetch('/api/content/request-format-decision', {
            method: 'POST',
            body: JSON.stringify({ topic, user_id: currentUser.id })
        })
        .then(res => res.json())
        .then(data => {
            setRecommendation(data.recommendation);
            setFormat(data.recommendation); // Auto-select recommendation
        });
    }, [topic]);
    
    return (
        <div className="format-selector">
            <h3>Choose Format</h3>
            <p>No engagement data available. Please choose:</p>
            
            {recommendation && (
                <div className="recommendation">
                    💡 Recommended: {recommendation.toUpperCase()}
                    <br/>
                    {trendingData.is_trending && 
                        "Topic is trending, reels work best!"}
                </div>
            )}
            
            <div className="format-options">
                <button 
                    className={format === 'post' ? 'selected' : ''}
                    onClick={() => setFormat('post')}
                >
                    📸 POST
                    <small>Best for detailed content</small>
                </button>
                
                <button 
                    className={format === 'story' ? 'selected' : ''}
                    onClick={() => setFormat('story')}
                >
                    📱 STORY
                    <small>Best for quick tips</small>
                </button>
                
                <button 
                    className={format === 'reel' ? 'selected' : ''}
                    onClick={() => setFormat('reel')}
                >
                    🎬 REEL
                    <small>Best for trending & step-by-step</small>
                </button>
            </div>
            
            <button onClick={() => onFormatSelected(format)}>
                Continue with {format?.toUpperCase() || 'Selected Format'}
            </button>
        </div>
    );
}
```

---

## Decision Priority Order

```
1. User Specified Format (Highest Priority)
   └─→ If user provides format → Use it immediately

2. Engagement Data (If Available)
   └─→ If user has past posts → Use performance data

3. Intelligent Default (New Users)
   └─→ If no engagement data → Use smart defaults
       ├─→ Trending topic → Reel
       ├─→ Educational → Post
       ├─→ Food/Recipe → Reel
       └─→ Default → Reel

4. Human-in-the-Loop (Optional)
   └─→ If requested → Return options for user to choose
```

---

## Summary

**For New Users:**
- ✅ Can manually specify format in request
- ✅ Can request human-in-the-loop decision
- ✅ Gets intelligent defaults based on topic/trending
- ✅ Can override defaults anytime

**For Existing Users:**
- ✅ Uses engagement data (automatic)
- ✅ Can still override with manual format
- ✅ Gets personalized recommendations

**Human-in-the-Loop:**
- ✅ Optional - user can request decision help
- ✅ Shows recommendations with reasons
- ✅ User makes final decision

This ensures new influencers can use the system immediately while still getting intelligent recommendations!

