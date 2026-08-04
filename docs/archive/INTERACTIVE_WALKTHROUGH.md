# Interactive Tool Walkthrough

## 🎯 Let's Walk Through Each Tool Together

---

## Tool 1: Content Generator 🔤

### What It Does
Generates educational AI content using OpenAI GPT-4.

### Step-by-Step Execution

**Step 1: You call it**
```javascript
const { generateAIEducationContent } = require('./tools/langchain-tools/content-generator');
const result = await generateAIEducationContent("Neural Networks");
```

**Step 2: Inside the function**
```javascript
// 1. Validates input
if (!topic || !topic.trim()) {
  throw new Error('Topic is required');
}
// ✅ "Neural Networks" passes validation
```

**Step 3: Builds prompt**
```javascript
const prompt = `You are an AI education content creator. 
For the topic "Neural Networks", generate educational content...`;
// This becomes the message sent to GPT-4
```

**Step 4: Makes API call**
```javascript
const response = await axios.post('https://api.openai.com/v1/chat/completions', {
  model: 'gpt-4-turbo-2024-04-09',
  messages: [{ role: 'user', content: prompt }],
  temperature: 0.7
});
// Sends request, waits for response
```

**Step 5: Gets response**
```javascript
const content = response.data.choices[0].message.content;
// Raw text from GPT-4, like:
// "Key Concepts:\n1. Neural networks are...\n\nReal-World Examples:\n- ..."
```

**Step 6: Parses response**
```javascript
const keyConceptsMatch = content.match(/Key Concepts\s*:?\s*([\s\S]*?)(?:\n+Real-World Examples:|$)/i);
// Extracts: "1. Neural networks are...\n2. They consist of..."
```

**Step 7: Cleans data**
```javascript
keyConcepts = keyConcepts.replace(/^[:*#>\s-]+/, '').trim();
// Removes any leading formatting
```

**Step 8: Returns structured data**
```javascript
return {
  keyConcepts: "1. Neural networks...",
  examples: "- Image recognition...",
  applications: "1. Computer vision...",
  caption: "🧠 Neural Networks explained! #AI #MachineLearning",
  imagePrompt: "A futuristic workspace with neural network diagrams..."
};
```

### Real Example Output
```javascript
{
  keyConcepts: "1. Neural networks are computing systems inspired by biological neural networks\n2. They consist of interconnected nodes (neurons) organized in layers\n3. They learn patterns from data through training",
  examples: "- Image recognition in photos\n- Voice assistants like Siri\n- Recommendation systems",
  applications: "1. Computer vision and image processing\n2. Natural language processing\n3. Predictive analytics",
  caption: "🧠 Neural Networks: The building blocks of modern AI! Learn how these interconnected systems power everything from image recognition to language translation. #AI #NeuralNetworks #MachineLearning",
  imagePrompt: "A futuristic workspace with holographic displays showing neural network architecture diagrams, interconnected nodes glowing with data flow, code snippets floating in the air, and a clear view of a starry sky through large windows"
}
```

---

## Tool 2: Image Generator 🖼️

### What It Does
Generates images using Stability AI and hosts them via local server.

### Step-by-Step Execution

**Step 1: You call it**
```javascript
const { generateAndHostImage } = require('./tools/langchain-tools/image-generator');
const imageUrl = await generateAndHostImage("A futuristic workspace with neural network diagrams...");
```

**Step 2: Inside generateImage()**
```javascript
// 1. Validates API key
const apiKey = process.env.STABILITY_API_KEY;
if (!apiKey) throw new Error('STABILITY_API_KEY is missing');

// 2. Validates prompt
if (!prompt || !prompt.trim()) {
  throw new Error('Image prompt is required');
}
```

**Step 3: Creates FormData**
```javascript
const form = new FormData();
form.append('prompt', prompt);           // "A futuristic workspace..."
form.append('output_format', 'jpeg');    // Instagram needs JPEG
// FormData is needed for multipart/form-data API
```

**Step 4: Sets headers**
```javascript
const headers = {
  ...form.getHeaders(),                    // Content-Type, boundary
  'Authorization': `Bearer ${apiKey}`,     // API key
  'Accept': 'image/*'                      // We want image back
};
```

**Step 5: Makes API call**
```javascript
const response = await axios.post(
  'https://api.stability.ai/v2beta/stable-image/generate/core',
  form,
  { headers, responseType: 'arraybuffer' }
);
// responseType: 'arraybuffer' = binary data (image bytes)
```

**Step 6: Saves image**
```javascript
const filename = `stability-${Date.now()}.jpeg`;
// Example: "stability-1762638614114.jpeg"
const outPath = path.join(assetsDir, filename);
// Example: "/path/to/assets/stability-1762638614114.jpeg"
fs.writeFileSync(outPath, response.data);
// Writes binary image data to file
```

**Step 7: In generateAndHostImage()**
```javascript
// 1. Generate image (gets local path)
const localPath = await generateImage(prompt);
// Returns: "/path/to/assets/stability-1762638614114.jpeg"

// 2. Ensure JPEG (already is, but check)
let jpegPath = localPath;
// No conversion needed in this case

// 3. Create public URL
const filenameBase = path.basename(jpegPath);
// "stability-1762638614114.jpeg"
const publicImageServerUrl = process.env.PUBLIC_IMAGE_SERVER_URL || 'http://localhost:3001';
const imageUrl = `${publicImageServerUrl}/assets/${filenameBase}`;
// "https://tunnel-url.loca.lt/assets/stability-1762638614114.jpeg"
```

**Step 8: Returns URL**
```javascript
return imageUrl;
// "https://ripe-lions-poke.loca.lt/assets/stability-1762638614114.jpeg"
```

### Real Example Flow
```
Input: "A futuristic workspace with neural network diagrams..."
  ↓
Stability AI generates image
  ↓
Saved to: assets/stability-1762638614114.jpeg
  ↓
URL created: https://tunnel-url.loca.lt/assets/stability-1762638614114.jpeg
  ↓
Output: "https://ripe-lions-poke.loca.lt/assets/stability-1762638614114.jpeg"
```

---

## Tool 3: Instagram Poster 📱

### What It Does
Posts images with captions to Instagram via Graph API.

### Step-by-Step Execution

**Step 1: You call it**
```javascript
const { postImageToInstagram } = require('./tools/langchain-tools/instagram-poster');
const result = await postImageToInstagram(
  "🧠 Neural Networks explained! #AI",
  "https://tunnel-url.loca.lt/assets/image.jpeg",
  process.env.INSTAGRAM_ACCESS_TOKEN
);
```

**Step 2: Validates credentials**
```javascript
if (!accessToken || !IG_USER_ID) {
  throw new Error('Missing INSTAGRAM_ACCESS_TOKEN or IG_USER_ID');
}
// ✅ Both exist, continue
```

**Step 3: Validates URL**
```javascript
if (!imageUrl.startsWith('https://')) {
  throw new Error('Image URL must be HTTPS');
}
// ✅ "https://..." passes
```

**Step 4: Verifies image is accessible**
```javascript
await axios.head(imageUrl, { timeout: 10000, maxRedirects: 5 });
// HEAD request = just headers, no body (faster)
// Checks if image actually exists and is accessible
// ✅ Image is accessible, continue
```

**Step 5: Create media container**
```javascript
const mediaRes = await axios.post(
  `https://graph.facebook.com/v19.0/${IG_USER_ID}/media`,
  {},
  {
    params: {
      image_url: "https://tunnel-url.loca.lt/assets/image.jpeg",
      caption: "🧠 Neural Networks explained! #AI",
      access_token: "EAAQ..."
    }
  }
);
// Instagram prepares the post (but doesn't publish yet)
// Returns: { id: "17841474622378736_123456789" }
```

**Step 6: Get creation ID**
```javascript
const creationId = mediaRes.data.id;
// "17841474622378736_123456789"
```

**Step 7: Publish the media**
```javascript
const publishRes = await axios.post(
  `https://graph.facebook.com/v19.0/${IG_USER_ID}/media_publish`,
  {},
  {
    params: {
      creation_id: "17841474622378736_123456789",
      access_token: "EAAQ..."
    }
  }
);
// Actually posts to Instagram
// Returns: { id: "12345678901234567" } (the post ID)
```

**Step 8: Returns result**
```javascript
return {
  success: true,
  postId: "12345678901234567",
  creationId: "17841474622378736_123456789"
};
```

### Real Example Flow
```
Input: {
  caption: "🧠 Neural Networks explained! #AI",
  imageUrl: "https://tunnel-url.loca.lt/assets/image.jpeg"
}
  ↓
Verify URL accessible ✅
  ↓
Create media container → creationId: "17841474622378736_123456789"
  ↓
Publish media → postId: "12345678901234567"
  ↓
Output: {
  success: true,
  postId: "12345678901234567",
  creationId: "17841474622378736_123456789"
}
```

---

## 🔗 How They Connect

### Complete Flow Example

```javascript
// Step 1: Generate content
const content = await generateAIEducationContent("Neural Networks");
// Returns: { keyConcepts, examples, applications, caption, imagePrompt }

// Step 2: Generate image using the visual prompt
const imageUrl = await generateAndHostImage(content.imagePrompt);
// Returns: "https://tunnel-url.loca.lt/assets/stability-1234567890.jpeg"

// Step 3: Compose full caption
let fullCaption = content.caption;
fullCaption += `\n\n🔑 Key Concepts:\n${content.keyConcepts}`;
fullCaption += `\n\n💡 Real-World Examples:\n${content.examples}`;
fullCaption += `\n\n🚀 Applications:\n${content.applications}`;

// Step 4: Post to Instagram
const result = await postImageToInstagram(
  fullCaption,
  imageUrl,
  process.env.INSTAGRAM_ACCESS_TOKEN
);
// Returns: { success: true, postId: "12345678901234567" }
```

---

## 🎓 Key Learning Points

### 1. Each Tool Has a Single Responsibility
- Content Generator: Creates text content
- Image Generator: Creates and hosts images
- Instagram Poster: Posts to Instagram

### 2. Tools Pass Data to Each Other
- Content Generator → Image Generator (via imagePrompt)
- Content Generator + Image Generator → Instagram Poster (via caption + imageUrl)

### 3. Error Handling at Each Step
- Each tool validates its inputs
- Each tool handles its own errors
- Errors don't propagate silently

### 4. State Flows Through
```
State: { prompt: "Neural Networks" }
  ↓
State: { prompt, content: {...} }
  ↓
State: { prompt, content: {...}, imageUrl: "..." }
  ↓
State: { prompt, content: {...}, imageUrl: "...", postResult: {...} }
```

---

## 🧪 Try It Yourself

Run the test:
```bash
node tests/test-langchain-tools.js
```

This will:
1. Test content generation
2. Show tool interface
3. Demonstrate the workflow

---

## 💡 Questions to Explore

1. **What happens if the image URL isn't accessible?**
   - Instagram Poster checks first and fails early

2. **What if GPT-4 returns malformed content?**
   - Content Generator validates and throws error

3. **What if Stability AI is down?**
   - Image Generator catches error and throws meaningful message

4. **How would you add retry logic?**
   - We'll see this in LangGraph workflow!

---

**Next**: Let's see how LangGraph connects these tools together! 🚀







