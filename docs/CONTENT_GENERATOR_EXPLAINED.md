# Content Generator Tool - Explained

## What It Does

Generates Instagram-ready content (caption + hashtags) from a topic using OpenAI GPT.

---

## How It Works

### Input
- **Topic**: e.g., "LLM", "AI Agents"
- **Format**: "post", "story", or "reel"

### Output
```python
{
    "caption": "Generated caption text...",
    "hashtags": "#ai #machinelearning #tech",
    "full_text": "Complete generated text"
}
```

---

## Key Features

1. **Format-Specific**: Different prompts for post/story/reel
2. **Hashtag Extraction**: Automatically extracts hashtags from generated text
3. **Fallback Hashtags**: Generates default hashtags if none found
4. **Error Handling**: Clear error messages

---

## Usage

```python
from tools.content_generator import ContentGenerator

generator = ContentGenerator()
result = generator.generate("LLM", "post")

print(result["caption"])
print(result["hashtags"])
```

---

## Next Step

Once this works, we'll build the Image Generator Tool!

