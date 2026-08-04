# Simple Flow Plan: Content + Image → Instagram Post

## Goal
Build a simple, working flow that:
1. Takes a topic from user
2. Generates content (text/caption)
3. Generates an image
4. Posts to Instagram
5. Saves to database

**No complex decisions yet** - just make it work end-to-end!

---

## Flow Steps

```
User Input (Topic)
    ↓
1. Generate Content (Text/Caption)
    ↓
2. Generate Image
    ↓
3. Post to Instagram
    ↓
4. Save to Database
    ↓
Success Response
```

---

## What We'll Build

### Step 1: Content Generation Tool
- **What**: Generates Instagram caption/text from topic
- **How**: Use LLM (OpenAI/Gemini) to create engaging caption
- **Output**: Text content, hashtags

### Step 2: Image Generation Tool
- **What**: Generates image from topic/content
- **How**: Use image generation API (Stability AI/Hugging Face)
- **Output**: Image URL

### Step 3: Instagram Posting Tool
- **What**: Posts content + image to Instagram
- **How**: Use Instagram Graph API
- **Output**: Instagram post ID

### Step 4: Connect Everything
- **What**: API endpoint that orchestrates all 3 tools
- **How**: FastAPI route that calls tools in sequence
- **Output**: Success response with post details

---

## Tools We Need

1. **Content Generator Tool** (`tools/content_generator.py`)
   - Input: topic
   - Output: caption, hashtags

2. **Image Generator Tool** (`tools/image_generator.py`)
   - Input: topic/content
   - Output: image URL

3. **Instagram Poster Tool** (`tools/instagram_poster.py`)
   - Input: caption, image URL, user access token
   - Output: Instagram post ID

---

## API Endpoint

**POST `/api/content/generate-and-post`**

**Request:**
```json
{
  "topic": "LLM",
  "user_id": "aimllearning"
}
```

**Response:**
```json
{
  "status": "success",
  "post_id": "ig_123456",
  "caption": "Generated caption...",
  "image_url": "https://...",
  "instagram_post_id": "123456789"
}
```

---

## Build Order

1. **Content Generator Tool** - Generate text from topic
2. **Image Generator Tool** - Generate image from topic
3. **Instagram Poster Tool** - Post to Instagram
4. **Orchestration Endpoint** - Connect all tools
5. **Frontend Integration** - Update UI to use new endpoint

---

## Why This Order?

- **Start Simple**: One tool at a time
- **Test Each Step**: Verify each tool works before moving on
- **Build Up**: Add complexity gradually
- **Working End-to-End**: Get full flow working first, then optimize

---

Let's start building! 🚀

