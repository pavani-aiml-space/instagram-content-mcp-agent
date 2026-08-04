# Tool Walkthrough: Step-by-Step Code Explanation

## 🎓 Learning Approach

We'll walk through each tool line by line, explaining:
- **What** each part does
- **Why** it's structured that way
- **How** it fits into the bigger picture

---

## Tool 1: Content Generator

**File**: `tools/langchain-tools/content-generator.js`

### Part 1: Setup and Imports

```javascript
const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });
```

**What this does:**
- `axios`: HTTP client for API calls
- `path`: File path utilities
- `dotenv`: Loads environment variables from `.env` file

**Why:**
- We need to call OpenAI API (axios)
- We need to find the `.env` file (path)
- We need the API key (dotenv)

**Learning point**: Always load environment variables at the top!

---

### Part 2: The Core Function

```javascript
async function generateAIEducationContent(topic) {
  if (!topic || !topic.trim()) {
    throw new Error('Topic is required');
  }
```

**What this does:**
- Defines the main function
- Validates input (topic must exist and not be empty)

**Why validate first?**
- **Fail fast**: Catch errors early
- **Clear errors**: Better error messages
- **Prevent API calls**: Don't waste API credits on bad input

**Learning point**: Always validate inputs before processing!

---

### Part 3: Building the Prompt

```javascript
const prompt = `You are an AI education content creator. For the topic "${topic}", generate educational content for an Instagram reel/post about AI, Machine Learning, or Generative AI concepts.

REPLY ONLY in this exact format (no markdown, no extra text, no explanations):

Key Concepts:
1. ...
2. ...
3. ...

Real-World Examples:
- ...
- ...

Applications:
1. ...
2. ...
3. ...

Caption: ...

Visual Prompt: ...`;
```

**What this does:**
- Creates a detailed prompt for GPT-4
- Specifies the exact format we want

**Why this format?**
- **Structured output**: Easy to parse
- **Consistent**: Same format every time
- **Complete**: Gets all the data we need

**Learning point**: Clear prompts = better results!

---

### Part 4: Making the API Call

```javascript
const response = await axios.post(
  'https://api.openai.com/v1/chat/completions',
  {
    model: 'gpt-4-turbo-2024-04-09',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7
  },
  {
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    }
  }
);
```

**Breaking it down:**

1. **URL**: OpenAI's chat completions endpoint
2. **Model**: `gpt-4-turbo-2024-04-09` - The AI model to use
3. **Messages**: Array of conversation messages
   - `role: 'user'` - This is from the user
   - `content: prompt` - The actual prompt text
4. **Temperature**: `0.7` - Controls randomness
   - Lower (0.1) = More consistent, less creative
   - Higher (0.9) = More creative, less consistent
   - 0.7 = Balanced
5. **Headers**: Authentication and content type
   - `Authorization`: API key (from `.env`)
   - `Content-Type`: Tells API we're sending JSON

**Learning point**: Understanding API parameters helps you control output!

---

### Part 5: Parsing the Response

```javascript
const content = response.data.choices[0].message.content;

// Parse the response
const keyConceptsMatch = content.match(/Key Concepts\s*:?\s*([\s\S]*?)(?:\n+Real-World Examples:|\n+Real-World Examples\s*:?|$)/i);
```

**What this does:**
1. Extracts the text from OpenAI's response
2. Uses regex to find each section

**Regex Explanation:**
- `/Key Concepts\s*:?\s*` - Matches "Key Concepts" with optional colon and spaces
- `([\s\S]*?)` - Captures everything (including newlines) until...
- `(?:\n+Real-World Examples:|$)` - ...until "Real-World Examples" or end of string
- `i` - Case insensitive

**Why regex?**
- LLMs sometimes format differently
- Handles variations in spacing/formatting
- More robust than string splitting

**Learning point**: Regex is powerful for parsing text!

---

### Part 6: Cleaning the Data

```javascript
// Remove leading Markdown formatting
keyConcepts = keyConcepts.replace(/^[:*#>\s-]+/, '').replace(/^(\*\*)+/, '').trim();
```

**What this does:**
- Removes leading colons, asterisks, hashes, etc.
- Removes markdown bold markers (`**`)
- Trims whitespace

**Why clean?**
- LLMs sometimes add formatting we don't want
- Ensures clean output
- Makes data consistent

**Learning point**: Always clean parsed data!

---

### Part 7: Validation

```javascript
if (!keyConcepts || !caption || !visualPrompt) {
  throw new Error(`Failed to parse content. Missing required fields. Raw: ${content.substring(0, 200)}`);
}
```

**What this does:**
- Checks if required fields were extracted
- Throws error if missing
- Includes raw content for debugging

**Why validate?**
- Prevents downstream errors
- Helps with debugging
- Ensures data quality

**Learning point**: Validate after parsing!

---

### Part 8: Error Handling

```javascript
} catch (error) {
  if (error.response) {
    throw new Error(`OpenAI API error: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
  }
  throw error;
}
```

**What this does:**
- Catches any errors
- If it's an API error, extracts status and data
- Otherwise, re-throws the original error

**Why this pattern?**
- **API errors**: Have response data (status, error message)
- **Network errors**: Don't have response data
- **Better debugging**: See what went wrong

**Learning point**: Different errors need different handling!

---

### Part 9: Tool Creator

```javascript
function createContentGeneratorTool() {
  return {
    name: "generate_ai_education_content",
    description: `Generates educational content about AI/ML topics...`,
    async call(topic) {
      return await generateAIEducationContent(topic);
    }
  };
}
```

**What this does:**
- Creates a LangChain tool interface
- Wraps our function in a tool format

**Tool Structure:**
- **name**: Unique identifier
- **description**: What the LLM reads (very important!)
- **call**: The function to execute

**Why separate?**
- Function can be used standalone
- Tool can be used by agents
- Best of both worlds!

**Learning point**: Separate concerns - function vs tool!

---

## Tool 2: Image Generator

**File**: `tools/langchain-tools/image-generator.js`

### Part 1: Setup

```javascript
const assetsDir = path.join(__dirname, '../../assets');
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir, { recursive: true });
}
```

**What this does:**
- Defines where to save images
- Creates directory if it doesn't exist

**Why:**
- Need a place to save images
- `recursive: true` creates parent directories too
- Prevents errors if directory missing

**Learning point**: Always ensure directories exist!

---

### Part 2: Generate Image Function

```javascript
async function generateImage(prompt) {
  const apiKey = process.env.STABILITY_API_KEY;
  if (!apiKey) {
    throw new Error('STABILITY_API_KEY is missing. Check your .env file.');
  }
```

**What this does:**
- Gets API key from environment
- Validates it exists

**Why check first?**
- Better error message
- Fails before making API call
- Saves time

---

### Part 3: FormData for API

```javascript
const form = new FormData();
form.append('prompt', prompt);
form.append('output_format', 'jpeg');
```

**What this does:**
- Creates multipart form data
- Adds prompt and format

**Why FormData?**
- Stability AI API requires multipart/form-data
- Different from JSON (like OpenAI)
- Each API has its own format

**Learning point**: Different APIs, different formats!

---

### Part 4: Headers

```javascript
const headers = {
  ...form.getHeaders(),
  'Authorization': `Bearer ${apiKey}`,
  'Accept': 'image/*'
};
```

**What this does:**
- Gets headers from FormData (content-type, boundary)
- Adds authorization
- Sets accept header

**Why spread `form.getHeaders()`?**
- FormData needs special headers
- Includes boundary for multipart
- Required for the API to work

**Learning point**: FormData needs special headers!

---

### Part 5: Save Image

```javascript
const filename = `stability-${Date.now()}.jpeg`;
const outPath = path.join(assetsDir, filename);
fs.writeFileSync(outPath, response.data);
```

**What this does:**
- Creates unique filename (timestamp)
- Saves image to assets directory

**Why timestamp?**
- Prevents filename conflicts
- Easy to identify when created
- Unique every time

**Learning point**: Use timestamps for unique filenames!

---

### Part 6: Generate and Host

```javascript
async function generateAndHostImage(prompt) {
  // 1. Generate image
  const localPath = await generateImage(prompt);

  // 2. Ensure JPEG format
  let jpegPath = localPath;
  if (!localPath.endsWith('.jpeg') && !localPath.endsWith('.jpg')) {
    jpegPath = localPath.replace(/\.[^.]+$/, '.jpeg');
    await sharp(localPath).jpeg().toFile(jpegPath);
    try { fs.unlinkSync(localPath); } catch (e) {}
  }
```

**What this does:**
1. Generates image (gets local file path)
2. Converts to JPEG if needed (using Sharp library)
3. Cleans up original if converted

**Why convert?**
- Instagram requires JPEG
- Ensures compatibility
- Sharp is fast and reliable

**Learning point**: Always ensure output format matches requirements!

---

### Part 7: Create Public URL

```javascript
const PORT = process.env.IMAGE_SERVER_PORT || 3001;
const publicImageServerUrl = process.env.PUBLIC_IMAGE_SERVER_URL || `http://localhost:${PORT}`;
const imageUrl = `${publicImageServerUrl}/assets/${filenameBase}`;
```

**What this does:**
- Gets port from env (or defaults to 3001)
- Gets public URL from env (or uses localhost)
- Constructs full image URL

**Why this pattern?**
- **Development**: Uses localhost
- **Production**: Uses tunnel URL
- **Flexible**: Works in both environments

**Learning point**: Use environment variables for configuration!

---

## Tool 3: Instagram Poster

**File**: `tools/langchain-tools/instagram-poster.js`

### Part 1: Validation

```javascript
if (!accessToken || !IG_USER_ID) {
  throw new Error('Missing INSTAGRAM_ACCESS_TOKEN or IG_USER_ID');
}

if (!imageUrl.startsWith('https://')) {
  throw new Error(`Image URL must be HTTPS. Got: ${imageUrl}`);
}
```

**What this does:**
- Validates credentials exist
- Validates URL is HTTPS

**Why validate URL?**
- Instagram requires HTTPS
- Won't work with HTTP
- Better to fail early

**Learning point**: Validate API requirements!

---

### Part 2: Verify Image Accessibility

```javascript
await axios.head(imageUrl, { timeout: 10000, maxRedirects: 5 });
```

**What this does:**
- Makes HEAD request (no body, just headers)
- Checks if image is accessible
- Times out after 10 seconds
- Follows up to 5 redirects

**Why verify first?**
- Instagram will fail if image not accessible
- Better error message
- Saves API quota

**Learning point**: Verify external resources before using!

---

### Part 3: Two-Step Posting Process

```javascript
// Step 1: Create media container
const mediaRes = await axios.post(
  `https://graph.facebook.com/v19.0/${IG_USER_ID}/media`,
  {},
  {
    params: {
      image_url: imageUrl,
      caption: caption,
      access_token: accessToken
    }
  }
);

// Step 2: Publish the media
const publishRes = await axios.post(
  `https://graph.facebook.com/v19.0/${IG_USER_ID}/media_publish`,
  {},
  {
    params: {
      creation_id: creationId,
      access_token: accessToken
    }
  }
);
```

**What this does:**
1. **Step 1**: Creates a "media container" (prepares the post)
2. **Step 2**: Publishes it (actually posts)

**Why two steps?**
- Instagram API design
- Allows validation before posting
- Can cancel if something's wrong

**Learning point**: Some APIs have multi-step processes!

---

### Part 4: Tool with Object Input

```javascript
async call({ caption, imageUrl, accessToken = ACCESS_TOKEN }) {
  return await postImageToInstagram(caption, imageUrl, accessToken);
}
```

**What this does:**
- Tool accepts an object
- Uses destructuring
- Defaults accessToken if not provided

**Why object input?**
- Multiple parameters
- More readable
- Can add more params later

**Learning point**: Objects are better for multiple parameters!

---

## 🔄 How They Work Together

### The Flow

```
1. Content Generator
   Input: "Neural Networks"
   Output: { keyConcepts, examples, applications, caption, imagePrompt }
   
2. Image Generator
   Input: imagePrompt from step 1
   Output: "https://tunnel-url/assets/image.jpeg"
   
3. Instagram Poster
   Input: caption + imageUrl from steps 1 & 2
   Output: { success: true, postId: "123" }
```

### State Flow

```
State starts: { prompt: "Neural Networks" }
    ↓
After Content: { prompt, content: {...} }
    ↓
After Image: { prompt, content: {...}, imageUrl: "..." }
    ↓
After Post: { prompt, content: {...}, imageUrl: "...", postResult: {...} }
```

---

## 💡 Key Patterns You've Learned

### 1. Input Validation
- Always validate inputs first
- Fail fast with clear errors

### 2. Error Handling
- Try-catch around API calls
- Different handling for different error types
- Include context in error messages

### 3. Environment Variables
- Load at the top
- Use for configuration
- Provide defaults

### 4. Function + Tool Pattern
- Function: Can be used directly
- Tool: Can be used by agents
- Both: Share same logic

### 5. API Patterns
- Different APIs, different formats (JSON vs FormData)
- Some APIs need multi-step processes
- Always verify external resources

---

## 🎯 Next Steps

1. **Test each tool** individually
2. **Understand the flow** between tools
3. **See how LangGraph** connects them
4. **Add error recovery** in the workflow

---

**Questions to think about:**
- What happens if the image generation fails?
- How would you add retry logic?
- What if Instagram API is down?

These are things we'll address in the LangGraph workflow! 🚀







