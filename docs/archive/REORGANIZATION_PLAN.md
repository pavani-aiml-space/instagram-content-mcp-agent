# Directory Reorganization Plan

## 🎯 Goals
- Clear separation of concerns
- Easy to navigate
- Scalable for future additions
- Follow Node.js best practices

## 📁 Proposed Structure

```
instagramapp/
├── src/                      # Main application source
│   ├── server.js            # Express server (moved from root)
│   ├── agent.js             # Agent orchestration (moved from root)
│   └── index.js             # Entry point (moved from root)
│
├── tools/                    # Tool modules (MCP servers)
│   ├── chatgpt/             # Content generation
│   ├── image-generator/     # Image generation
│   └── instagram/           # Instagram posting
│
├── scripts/                  # Utility scripts
│   ├── setup-tunnel.sh      # Tunnel setup
│   ├── run-tunnel.sh        # Run tunnel
│   └── install-deps.sh      # Dependency installation
│
├── tests/                    # Test files
│   ├── test-instagram-post.js
│   ├── test-s3-upload.js
│   └── test-stability-image.js
│
├── config/                   # Configuration files
│   ├── daily_prompt.txt     # Daily prompt
│   └── post-reel.mcp.json   # MCP config
│
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── QUICK_START_PLAN.md
│
├── assets/                    # Generated assets (keep as is)
├── public/                    # Static web files (keep as is)
├── logs/                     # Log files
│   └── server.log
│
├── tmp/                      # Temporary files (keep as is)
├── node_modules/             # Dependencies (keep as is)
│
├── .env                      # Environment variables (root)
├── .gitignore               # Git ignore (root)
├── package.json             # Package config (root)
└── README.md                # Main readme (root)
```

## 🔄 File Movements

### Source Files
- `server.js` → `src/server.js`
- `agent.js` → `src/agent.js`
- `index.js` → `src/index.js`

### Tools (already in subdirectories, keep structure)
- `chatgpt/` → `tools/chatgpt/`
- `image-generator/` → `tools/image-generator/`
- `instagram/` → `tools/instagram/`

### Scripts
- `setup-free-tunnel.sh` → `scripts/setup-tunnel.sh`
- `start-tunnel.sh` → `scripts/run-tunnel.sh`
- `run-tunnel.sh` → `scripts/run-tunnel.sh` (merge if duplicate)
- `install-deps.sh` → `scripts/install-deps.sh`
- `run-image-post` → `scripts/run-image-post`

### Tests
- `test-instagram-post.js` → `tests/test-instagram-post.js`
- `test-s3-upload.js` → `tests/test-s3-upload.js`
- `test-stability-image.js` → `tests/test-stability-image.js`

### Config
- `daily_prompt.txt` → `config/daily_prompt.txt`
- `post-reel.mcp.json` → `config/post-reel.mcp.json`

### Docs
- `ARCHITECTURE.md` → `docs/ARCHITECTURE.md`
- `IMPLEMENTATION_PLAN.md` → `docs/IMPLEMENTATION_PLAN.md`
- `QUICK_START_PLAN.md` → `docs/QUICK_START_PLAN.md`

### Logs
- `server.log` → `logs/server.log`

### Cleanup (delete or archive)
- `server.js.bak` → Delete (backup file)
- `chatgpt/index.js.bak` → Delete (backup file)
- `chat-server.js` → Review (might be unused)
- `chat-ui.html` → Review (might be unused)
- `image.jpg` → Move to assets/ or delete
- `instagramworkingcursor.code-workspace` → Move to .vscode/ or delete

## 📝 Code Updates Needed

After reorganization, update import paths:

### In `src/server.js`:
```javascript
// Old
const { runDailyInstagramPostAgent } = require('./agent');
const { generateInstagramContent } = require('./chatgpt/index');
const { generateAndHostImage } = require('./image-generator/index');
const { postToInstagram } = require('./instagram/index');

// New
const { runDailyInstagramPostAgent } = require('./agent');
const { generateInstagramContent } = require('../tools/chatgpt/index');
const { generateAndHostImage } = require('../tools/image-generator/index');
const { postToInstagram } = require('../tools/instagram/index');
```

### In `src/agent.js`:
```javascript
// Old
const { generateInstagramContent } = require('./chatgpt/index');
const { generateImage, generateAndHostImage } = require('./image-generator/index');
const { postToInstagram } = require('./instagram/index');

// New
const { generateInstagramContent } = require('../tools/chatgpt/index');
const { generateImage, generateAndHostImage } = require('../tools/image-generator/index');
const { postToInstagram } = require('../tools/instagram/index');
```

### In `tools/image-generator/index.js`:
```javascript
// Update .env path if needed
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });
```

### In `tools/instagram/index.js`:
```javascript
// Update .env path if needed
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });
```

### In `package.json`:
```json
{
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js"
  }
}
```

## ✅ Implementation Steps

1. Create new directory structure
2. Move files to new locations
3. Update import paths in code
4. Update package.json
5. Test that everything still works
6. Clean up old files
7. Update documentation paths

## 🚨 Important Notes

- Keep `.env` in root (standard practice)
- Keep `node_modules/` in root
- Keep `package.json` in root
- Test after each major move
- Update all relative paths

