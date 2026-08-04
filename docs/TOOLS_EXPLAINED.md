# Tools Explained - Simple Flow

## Three Tools We're Using

### 1. Content Generator (OpenAI)
- **Service**: OpenAI GPT-4
- **Purpose**: Generate Instagram captions and hashtags
- **Input**: Topic (e.g., "LLM")
- **Output**: Caption text + hashtags

### 2. Image Generator (Stability AI)
- **Service**: Stability AI Stable Diffusion
- **Purpose**: Generate images from text prompts
- **Input**: Text prompt (e.g., "AI robot teaching")
- **Output**: Image URL

### 3. Instagram Poster (Graph API)
- **Service**: Instagram Graph API
- **Purpose**: Post content to Instagram
- **Input**: Image URL + Caption
- **Output**: Instagram post ID

---

## Flow

```
Topic
  ↓
[Content Generator] → Caption + Hashtags
  ↓
[Image Generator] → Image URL
  ↓
[Instagram Poster] → Post to Instagram
  ↓
Success!
```

---

## Environment Variables Needed

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Stability AI
STABILITY_API_KEY=sk-...

# Instagram
INSTAGRAM_ACCESS_TOKEN=...
```

---

## Next: Connect All Three!

We'll create an endpoint that:
1. Takes topic from user
2. Generates content (OpenAI)
3. Generates image (Stability AI)
4. Posts to Instagram (Graph API)
5. Returns success

