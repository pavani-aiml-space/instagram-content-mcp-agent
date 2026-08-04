# Quick Start: Using the New LangChain Tools

## 🚀 Direct Usage (No Dependencies Needed)

The new tools can be used **directly** as regular functions, even without LangChain installed!

### Example 1: Generate Content

```javascript
const { generateAIEducationContent } = require('./tools/langchain-tools/content-generator');

async function example() {
  const content = await generateAIEducationContent("Neural Networks");
  console.log(content);
  // {
  //   keyConcepts: "...",
  //   examples: "...",
  //   applications: "...",
  //   caption: "...",
  //   imagePrompt: "..."
  // }
}
```

### Example 2: Generate Image

```javascript
const { generateAndHostImage } = require('./tools/langchain-tools/image-generator');

async function example() {
  const imageUrl = await generateAndHostImage("A futuristic AI workspace");
  console.log(imageUrl);
  // "https://your-tunnel.loca.lt/assets/stability-1234567890.jpeg"
}
```

### Example 3: Post to Instagram

```javascript
const { postImageToInstagram } = require('./tools/langchain-tools/instagram-poster');

async function example() {
  const result = await postImageToInstagram(
    "Learn about AI! #AI #MachineLearning",
    "https://your-tunnel.loca.lt/assets/image.jpeg",
    process.env.INSTAGRAM_ACCESS_TOKEN
  );
  console.log(result);
  // { success: true, postId: "123456", creationId: "789" }
}
```

### Example 4: Use LangGraph Workflow

```javascript
const { runLangGraphWorkflow } = require('./src/langgraph-agent');

async function example() {
  const result = await runLangGraphWorkflow("Transformers");
  console.log(result);
  // {
  //   prompt: "Transformers",
  //   content: { ... },
  //   imageUrl: "...",
  //   caption: "...",
  //   postResult: { ... },
  //   status: "posted"
  // }
}
```

---

## 🔧 Using as LangChain Tools (After Dependencies Installed)

Once LangChain is installed, tools can be used by agents:

```javascript
const { getAllTools } = require('./tools/langchain-tools');

// Get all tools for an agent
const tools = getAllTools();

// Agent can now use these tools automatically
```

---

## 📝 Test the Tools

Run the test file:

```bash
node tests/test-langchain-tools.js
```

This will:
1. Test content generation
2. Test image generation (commented out - requires tunnel)
3. Test tool interface
4. Show all available tools

---

## ✅ What's Different

### Old Way (Wrapper)
```javascript
// Wrapped existing function
const { generateInstagramContent } = require('./tools/chatgpt/index');
// Used old code through wrapper
```

### New Way (Direct)
```javascript
// Direct implementation
const { generateAIEducationContent } = require('./tools/langchain-tools/content-generator');
// Fresh, purpose-built code
```

---

## 🎯 Benefits

1. **No Dependencies**: Works without LangChain installed
2. **Direct**: No wrapper overhead
3. **Clean**: Purpose-built for this use case
4. **Flexible**: Can be used standalone OR as tools

---

**Ready to use right now!** 🎉







