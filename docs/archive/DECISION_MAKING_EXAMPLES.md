# Decision Making Examples - Quick Reference

## 🎯 Quick Examples

### Example 1: Simple Retry Logic

**Before (No Decision Making):**
```javascript
// Fails immediately if error occurs
const imageUrl = await generateAndHostImage(prompt);
```

**After (With Decision Making):**
```javascript
// Retries up to 3 times with exponential backoff
async function generateImageWithRetry(prompt, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await generateAndHostImage(prompt);
    } catch (error) {
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        continue; // Decision: Retry
      }
      throw error; // Decision: Give up
    }
  }
}
```

---

### Example 2: Quality Check Decision

**Before (No Quality Check):**
```javascript
// Uses content even if it's poor quality
const content = await generateInstagramContent(prompt);
// Proceed with potentially poor content
```

**After (With Quality Check):**
```javascript
// Decision: Is content good enough?
function isContentQualityGood(content) {
  if (content.caption.length < 50) return false; // Decision: Too short
  if (!content.keyConcepts) return false; // Decision: Missing concepts
  return true; // Decision: Good enough
}

// Use decision
const content = await generateInstagramContent(prompt);
if (!isContentQualityGood(content)) {
  // Decision: Regenerate or use fallback
  content = await generateInstagramContent(prompt + " (detailed)");
}
```

---

### Example 3: Conditional Branching

**Before (No Branching):**
```javascript
// Always creates post, never reel
const imageUrl = await generateAndHostImage(prompt);
await postToInstagram(caption, imageUrl);
```

**After (With Branching):**
```javascript
// Decision: Post or Reel?
function shouldCreateReel(day) {
  if (day <= 7) return false; // Decision: First week = posts
  if (day % 7 === 0) return true; // Decision: Weekly = reel
  return false; // Decision: Default = post
}

// Use decision
if (shouldCreateReel(day)) {
  // Branch 1: Create reel
  const reel = await generateReel(content);
  await postReelToInstagram(reel);
} else {
  // Branch 2: Create post
  const image = await generateAndHostImage(prompt);
  await postToInstagram(caption, image);
}
```

---

### Example 4: Error Recovery Decision

**Before (No Recovery):**
```javascript
// Crashes on any error
try {
  await postToInstagram(caption, imageUrl);
} catch (error) {
  throw error; // Decision: Give up
}
```

**After (With Recovery):**
```javascript
// Decision: What type of error?
try {
  await postToInstagram(caption, imageUrl);
} catch (error) {
  if (error.message.includes('token')) {
    // Decision: Token expired - save for later
    await savePostForLater(caption, imageUrl);
  } else if (error.message.includes('rate limit')) {
    // Decision: Rate limited - retry later
    await scheduleRetry(caption, imageUrl, 3600000);
  } else {
    // Decision: Unknown error - throw
    throw error;
  }
}
```

---

### Example 5: Fallback Strategy Decision

**Before (No Fallback):**
```javascript
// Fails if primary method fails
const imageUrl = await generateAndHostImage(prompt);
// If this fails, whole workflow fails
```

**After (With Fallback):**
```javascript
// Decision: Try primary, use fallback if fails
let imageUrl;
try {
  imageUrl = await generateAndHostImage(prompt);
} catch (error) {
  // Decision: Use fallback
  console.log('Using fallback image');
  imageUrl = 'https://example.com/fallback.jpg';
}
```

---

## 📊 Decision Flow Diagrams

### Decision 1: Retry Logic Flow

```
Generate Image
    ↓
Success? ──YES──→ Use Image
    ↓
   NO
    ↓
Attempt < Max? ──YES──→ Wait → Retry
    ↓
   NO
    ↓
Use Fallback
```

### Decision 2: Quality Check Flow

```
Generate Content
    ↓
Quality Good? ──YES──→ Use Content
    ↓
   NO
    ↓
Attempts < Max? ──YES──→ Enhance Prompt → Retry
    ↓
   NO
    ↓
Use Fallback Content
```

### Decision 3: Error Recovery Flow

```
Post to Instagram
    ↓
Success? ──YES──→ Done ✅
    ↓
   NO
    ↓
Token Error? ──YES──→ Save for Later
    ↓
   NO
    ↓
Rate Limit? ──YES──→ Schedule Retry
    ↓
   NO
    ↓
Throw Error
```

---

## 🔄 Complete Decision Flow Example

```
START
  ↓
Generate Content
  ↓
Quality Good? ──NO──→ Retry (up to 3x)
  ↓ YES
Generate Image
  ↓
Success? ──NO──→ Retry (up to 3x)
  ↓ YES
Compose Caption
  ↓
Post to Instagram
  ↓
Success? ──YES──→ DONE ✅
  ↓ NO
Token Error? ──YES──→ Save for Later
  ↓ NO
Rate Limit? ──YES──→ Schedule Retry
  ↓ NO
Image Error? ──YES──→ Use Fallback Image → Retry Post
  ↓ NO
Throw Error
```

---

## 💡 Key Decision Patterns

### Pattern 1: Retry with Backoff
```javascript
for (let attempt = 1; attempt <= maxRetries; attempt++) {
  try {
    return await operation();
  } catch (error) {
    if (attempt < maxRetries) {
      await wait(Math.pow(2, attempt) * 1000); // Exponential backoff
      continue; // Decision: Retry
    }
    throw error; // Decision: Give up
  }
}
```

### Pattern 2: Quality Gate
```javascript
let result;
let attempts = 0;
while (attempts < maxAttempts) {
  result = await generate();
  if (isQualityGood(result)) {
    break; // Decision: Good enough
  }
  attempts++;
  // Decision: Retry
}
if (!isQualityGood(result)) {
  result = getFallback(); // Decision: Use fallback
}
```

### Pattern 3: Error Type Handling
```javascript
try {
  await operation();
} catch (error) {
  if (isRetryableError(error)) {
    await retry(); // Decision: Retry
  } else if (isFallbackError(error)) {
    await useFallback(); // Decision: Fallback
  } else {
    throw error; // Decision: Give up
  }
}
```

### Pattern 4: Conditional Branching
```javascript
if (condition1) {
  // Branch 1
  await path1();
} else if (condition2) {
  // Branch 2
  await path2();
} else {
  // Default branch
  await defaultPath();
}
```

---

## 🎓 Learning Path

1. **Start Simple**: Add retry logic to one operation
2. **Add Quality Checks**: Validate before proceeding
3. **Implement Fallbacks**: Use alternatives if primary fails
4. **Error Recovery**: Handle different error types
5. **Conditional Branching**: Choose different paths

---

## 📝 Quick Checklist

- [ ] Retry logic for API calls
- [ ] Quality checks for generated content
- [ ] Fallback strategies for failures
- [ ] Error type detection and handling
- [ ] Conditional branching for different paths
- [ ] Exponential backoff for retries
- [ ] Logging for decision points

---

**See Also:**
- `docs/DECISION_MAKING_GUIDE.md` - Complete guide
- `src/agent-enhanced.js` - Enhanced agent implementation
- `src/agent.js` - Current agent (for comparison)


