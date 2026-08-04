# Implementation Plan: LangChain/LangGraph Integration & Instagram Reel Generation

## 📋 Overview

This plan outlines the implementation of:
1. **LangChain/LangGraph Integration**: Replace custom orchestration with industry-standard agent framework
2. **Instagram Reel Generation**: Add video creation and posting capabilities
3. **Educational Content System**: Generate daily educational content about LLM/Generative AI, Agents, and Agentic Workflows
4. **Progressive Curriculum**: Beginner to Advanced learning path

---

## 🎯 Goals

### Primary Goals
- ✅ Integrate LangChain for tool management and LangGraph for workflow orchestration
- ✅ Generate Instagram Reels (videos) instead of just static images
- ✅ Create educational content about AI/ML concepts
- ✅ Implement progressive curriculum system (beginner → advanced)

### Secondary Goals
- ✅ Maintain backward compatibility with existing post functionality
- ✅ Support both posts and reels
- ✅ Add content scheduling and curriculum tracking
- ✅ Improve error handling and retry logic with LangGraph

---

## 📐 Architecture Changes

### Current Architecture
```
Custom Agent (src/agent.js) → Direct API Calls → Tools (tools/)
```

### Proposed Architecture
```
LangGraph StateGraph → LangChain Tools → External APIs
```

---

## 🏗️ Phase 1: LangChain/LangGraph Integration

### 1.1 Dependencies Installation

**New Dependencies:**
```json
{
  "langchain": "^0.3.0",
  "@langchain/core": "^0.3.0",
  "@langchain/openai": "^0.3.0",
  "@langchain/community": "^0.3.0",
  "langgraph": "^0.2.0"
}
```

**Files to Modify:**
- `package.json` - Add dependencies
- `.env` - No changes needed (uses existing OPENAI_API_KEY)

### 1.2 Create LangChain Tools

**New Directory Structure:**
```
tools/
├── langchain-tools/          # NEW: LangChain tool wrappers
│   ├── index.js              # Tool exports
│   ├── content-generator.js  # LangChain wrapper for ChatGPT
│   ├── image-generator.js    # LangChain wrapper for image generation
│   ├── reel-generator.js     # NEW: Video/reel generation tool
│   └── instagram-poster.js  # LangChain wrapper for Instagram API
├── chatgpt/                  # Existing (keep for backward compat)
├── image-generator/          # Existing (keep for backward compat)
└── instagram/                # Existing (keep for backward compat)
```

**Implementation Steps:**
1. Convert existing tools to LangChain `Tool` format
2. Create tool descriptions for agent understanding
3. Add error handling and retry logic
4. Maintain backward compatibility

### 1.3 Create LangGraph State Graph

**New File: `src/langgraph-agent.js`**

**State Schema:**
```javascript
{
  prompt: string,           // User input or daily prompt
  level: string,            // "beginner" | "intermediate" | "advanced"
  day: number,              // Day in curriculum (1-365)
  content: {                // Generated content
    topic: string,
    explanation: string,
    examples: string[],
    codeSnippets: string[],
    visualPrompt: string
  },
  media: {
    type: "image" | "reel",
    url: string,
    thumbnail: string
  },
  caption: string,
  hashtags: string[],
  errors: string[],
  status: "pending" | "content_generated" | "media_created" | "posted" | "error"
}
```

**Graph Nodes:**
1. **determineLevel** - Determine curriculum level based on day
2. **generateTopic** - Generate daily topic based on level
3. **generateContent** - Create educational content
4. **generateMedia** - Create image or reel
5. **composeCaption** - Create Instagram caption with hashtags
6. **postToInstagram** - Post content
7. **handleError** - Error recovery node

**Graph Edges:**
- Linear flow with conditional branching for errors
- Retry logic for failed steps

### 1.4 Migration Strategy

**Approach:**
- Keep existing `src/agent.js` for backward compatibility
- Create new `src/langgraph-agent.js` for new workflows
- Gradually migrate endpoints to use LangGraph
- Feature flag to switch between implementations

---

## 🎬 Phase 2: Instagram Reel Generation

### 2.1 Video Generation Options

**Option A: Text-to-Video API (Recommended)**
- **Stability AI Video API** (when available)
- **Runway ML API** - Text-to-video generation
- **Pika Labs API** - Video generation
- **HeyGen API** - AI video creation

**Option B: Image-to-Video**
- Generate multiple images
- Animate using tools like:
  - **LeiaPix** - 2D to 3D animation
  - **Stable Video Diffusion** - Image to video
  - **AnimateDiff** - Animation framework

**Option C: Programmatic Video Creation**
- Use **FFmpeg** + **Canvas/Node-canvas**
- Create slideshow videos with text overlays
- Add animations and transitions
- Synthesize audio with **ElevenLabs** or **OpenAI TTS**

### 2.2 Recommended Approach: Hybrid

**Implementation:**
1. **Content Structure**: Generate slides with text/images
2. **Video Assembly**: Use FFmpeg to create video from slides
3. **Audio**: Generate narration with TTS
4. **Final Assembly**: Combine video + audio

**New Dependencies:**
```json
{
  "fluent-ffmpeg": "^2.1.2",
  "canvas": "^2.11.2",
  "@elevenlabs/elevenlabs": "^0.8.0",
  "sharp": "^0.34.2"  // Already installed
}
```

### 2.3 New Tool: `reel-generator/`

**Directory Structure:**
```
reel-generator/
├── index.js              # Main export
├── video-creator.js      # Video generation logic
├── slide-generator.js    # Create slides from content
├── audio-generator.js    # TTS for narration
├── video-assembler.js    # FFmpeg operations
└── package.json
```

**Key Functions:**
```javascript
async function generateReel(content, options) {
  // 1. Generate slides from content
  // 2. Create video from slides
  // 3. Generate audio narration
  // 4. Combine video + audio
  // 5. Upload and return URL
}
```

### 2.4 Instagram Reel API Integration

**Update: `tools/instagram/index.js`**

**New Function:**
```javascript
async function postReelToInstagram(videoUrl, caption, accessToken) {
  // Instagram Reels API requires:
  // 1. Upload video (different endpoint than images)
  // 2. Create reel container
  // 3. Publish reel
}
```

**API Endpoints:**
- `POST /{user-id}/media` with `media_type=REELS`
- `POST /{user-id}/media_publish` with `creation_id`

**Requirements:**
- Video format: MP4, MOV
- Aspect ratio: 9:16 (vertical)
- Duration: 3-90 seconds
- Max file size: 100MB

---

## 📚 Phase 3: Educational Content System

### 3.1 Curriculum Structure

**New File: `curriculum/curriculum.json`**

**Structure:**
```json
{
  "beginner": {
    "duration_days": 30,
    "topics": [
      {
        "day": 1,
        "title": "What is a Large Language Model?",
        "concepts": ["LLM basics", "Transformer architecture"],
        "prerequisites": [],
        "learning_objectives": ["Understand LLMs", "Know use cases"]
      },
      // ... more topics
    ]
  },
  "intermediate": {
    "duration_days": 60,
    "topics": [...]
  },
  "advanced": {
    "duration_days": 90,
    "topics": [...]
  }
}
```

### 3.2 Content Generation Prompts

**New File: `curriculum/prompts.js`**

**Prompt Templates:**
```javascript
const BEGINNER_PROMPT = `
Generate educational content for Day {day} of a beginner LLM course.
Topic: {topic}
Format:
- Simple explanation (2-3 sentences)
- Real-world analogy
- One code example
- Visual description for reel
`;

const INTERMEDIATE_PROMPT = `
Generate intermediate content about {topic}.
Include:
- Technical explanation
- Architecture diagrams description
- Code examples
- Best practices
`;

const ADVANCED_PROMPT = `
Generate advanced content about {topic}.
Include:
- Deep technical dive
- Research papers references
- Implementation details
- Performance considerations
`;
```

### 3.3 Content Types

**For Each Day:**
1. **Topic Title** - Catchy, educational
2. **Explanation** - Clear, level-appropriate
3. **Code Examples** - Practical snippets
4. **Visual Elements** - Diagrams, animations
5. **Real-world Applications** - Use cases
6. **Next Steps** - What to learn next

### 3.4 Progress Tracking

**New File: `curriculum/tracker.js`**

**Features:**
- Track current day in curriculum
- Store completed topics
- Calculate progress percentage
- Suggest review topics
- Handle curriculum resets

---

## 🔄 Phase 4: Integration & Workflow

### 4.1 New Agent Workflow

**LangGraph Workflow:**
```
START
  ↓
[Determine Level] → Based on day number
  ↓
[Generate Topic] → From curriculum
  ↓
[Generate Content] → LangChain + OpenAI
  ↓
[Generate Media] → Image or Reel
  ↓
[Compose Caption] → With hashtags
  ↓
[Post to Instagram] → API call
  ↓
[Update Progress] → Save to tracker
  ↓
END
```

### 4.2 Content vs Reel Decision

**Logic:**
- **Days 1-7**: Static images (onboarding)
- **Days 8+**: Reels (more engaging)
- **Special days**: Both post + reel
- **User override**: Allow manual selection

### 4.3 New Endpoints

**API Endpoints:**
```javascript
// Get current curriculum progress
GET /curriculum/progress

// Generate today's content
POST /curriculum/generate-today

// Generate reel for specific day
POST /curriculum/generate-reel?day=5

// Get curriculum overview
GET /curriculum/overview

// Reset curriculum
POST /curriculum/reset
```

---

## 📦 Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Install LangChain/LangGraph dependencies
- [ ] Create LangChain tool wrappers
- [ ] Set up basic LangGraph state graph
- [ ] Test with existing post workflow
- [ ] Document new architecture

### Phase 2: Reel Generation (Week 2)
- [ ] Research and choose video generation approach
- [ ] Implement slide generation
- [ ] Implement video assembly (FFmpeg)
- [ ] Add audio generation (TTS)
- [ ] Test video creation pipeline
- [ ] Update Instagram API for reels

### Phase 3: Curriculum System (Week 3)
- [ ] Design curriculum structure
- [ ] Create curriculum JSON file
- [ ] Implement topic generation prompts
- [ ] Build progress tracker
- [ ] Create curriculum management endpoints

### Phase 4: Integration (Week 4)
- [ ] Integrate all components
- [ ] Update LangGraph workflow
- [ ] Add content type selection logic
- [ ] Implement error handling
- [ ] Add monitoring and logging

### Phase 5: Testing & Refinement (Week 5)
- [ ] End-to-end testing
- [ ] Content quality review
- [ ] Performance optimization
- [ ] User feedback integration
- [ ] Documentation updates

---

## 🛠️ Technical Decisions

### Decision 1: LangChain vs Custom
**Decision**: Use LangChain/LangGraph
**Rationale**: 
- Industry standard
- Better error handling
- Tool management
- Future extensibility

### Decision 2: Video Generation Method
**Decision**: Hybrid (Slides + FFmpeg + TTS)
**Rationale**:
- More control over content
- Lower cost than API-based
- Better for educational content
- Reusable components

### Decision 3: Curriculum Format
**Decision**: JSON-based with prompts
**Rationale**:
- Easy to modify
- Version controllable
- Can be AI-generated
- Flexible structure

### Decision 4: Backward Compatibility
**Decision**: Keep existing `src/agent.js`
**Rationale**:
- No breaking changes
- Gradual migration
- Feature flags
- Easier rollback

---

## 📊 Success Metrics

### Technical Metrics
- ✅ Successful reel generation rate > 90%
- ✅ Average generation time < 5 minutes
- ✅ API error rate < 5%
- ✅ Curriculum completion tracking accuracy

### Content Metrics
- ✅ Daily content generation success
- ✅ Content quality (educational value)
- ✅ Engagement metrics (when posted)
- ✅ Curriculum progression accuracy

---

## 🚨 Risks & Mitigations

### Risk 1: Video Generation Complexity
**Mitigation**: Start with simple slideshow, iterate

### Risk 2: Instagram Reel API Limitations
**Mitigation**: Test thoroughly, have fallback to posts

### Risk 3: Content Quality
**Mitigation**: Review prompts, add quality checks

### Risk 4: Cost of Video Generation APIs
**Mitigation**: Use FFmpeg-based approach (free)

### Risk 5: Curriculum Completeness
**Mitigation**: Start with 30-day beginner curriculum, expand

---

## 📝 Files to Create/Modify

### New Files
```
tools/
  └── langchain-tools/          # NEW: LangChain tool wrappers
      ├── index.js
      ├── content-generator.js
      ├── image-generator.js
      ├── reel-generator.js
      └── instagram-poster.js

tools/
  └── reel-generator/           # NEW: Reel generation
      ├── index.js
      ├── video-creator.js
      ├── slide-generator.js
      ├── audio-generator.js
      └── video-assembler.js

src/
  └── langgraph-agent.js        # NEW: LangGraph agent

config/
  └── curriculum/               # NEW: Curriculum system
      ├── curriculum.json
      ├── prompts.js
      └── tracker.js
```

### Modified Files
```
package.json                    # Add dependencies
src/server.js                   # Add new endpoints
tools/instagram/index.js        # Add reel posting
docs/ARCHITECTURE.md            # Update documentation
README.md                      # Update features
```

---

## 🎓 Curriculum Sample Topics

### Beginner (Days 1-30)
1. What is a Large Language Model?
2. How do Transformers work?
3. Prompt Engineering Basics
4. Introduction to Agents
5. Simple Agent Workflows
6. LangChain Basics
7. Tool Calling in LLMs
... (30 topics)

### Intermediate (Days 31-90)
1. Advanced Prompt Engineering
2. Multi-Agent Systems
3. LangGraph State Management
4. Agent Memory Systems
5. Tool Chaining
6. Error Handling in Agents
... (60 topics)

### Advanced (Days 91-180)
1. Custom Agent Architectures
2. Agent Optimization
3. Production Agent Systems
4. Agent Evaluation
5. Research Frontiers
... (90 topics)

---

## ✅ Next Steps

1. **Review this plan** - Get approval on approach
2. **Set up development branch** - `feature/langgraph-reels`
3. **Phase 1 implementation** - Start with LangChain integration
4. **Iterative development** - Build and test each phase
5. **Documentation** - Update as we build

---

## 📚 Resources

- [LangChain Documentation](https://js.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Instagram Reels API](https://developers.facebook.com/docs/instagram-api/guides/content-publishing/#reels)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [ElevenLabs API](https://elevenlabs.io/docs/api-reference)

---

**Status**: 📋 Planning Complete - Ready for Implementation
**Last Updated**: 2024-11-08

