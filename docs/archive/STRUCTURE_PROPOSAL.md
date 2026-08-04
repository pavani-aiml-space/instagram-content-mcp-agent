# Proposed Directory Structure

## Clean, Minimal Structure

```
instagramapp/
├── .env                          # Environment variables
├── .gitignore
├── package.json
├── README.md                     # Simple project overview
│
├── backend/                      # Backend server
│   ├── server.js                 # Express server
│   └── routes.js                 # API routes
│
├── agents/                       # All agents here
│   ├── content-creator.js        # Step 4: First LangGraph agent
│   ├── image-generator.js        # Step 5: Second agent
│   ├── coordinator.js            # Step 5: Multi-agent coordinator
│   └── index.js                  # Export all agents
│
├── tools/                        # MCP Tools (Step 3)
│   ├── content-tool.js           # Content generation tool
│   ├── image-tool.js             # Image generation tool
│   ├── instagram-tool.js         # Instagram posting tool
│   └── index.js                  # Export all tools
│
├── database/                     # PostgreSQL
│   ├── connection.js             # DB connection
│   ├── schema.sql                # Database schema
│   └── migrations/               # (Future) DB migrations
│
├── frontend/                     # React app (Step 6)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── index.js
│   ├── package.json
│   └── public/
│
├── config/                       # Configuration files
│   └── default-prompt.txt
│
├── assets/                       # Generated images, etc.
│
└── docs/                         # Minimal docs
    ├── BUILD_PLAN.md              # Step-by-step plan
    └── STEP_X_COMPLETE.md        # One per completed step
```

## What Gets Removed/Archived

- All old agent files in `src/` → Move to `archive/` or delete
- Old test files → Archive
- Old documentation → Already in `archive/docs/`
- Old scripts → Archive if not needed
- `CustomerSupport/` → Archive or remove
- `chat-server.js`, `chat-ui.html` → Archive

## What We Keep

- `tools/` → Clean up, keep only what we need
- `database/` → Keep (we just created it)
- `assets/` → Keep (for generated images)
- `config/` → Keep
- `BUILD_PLAN.md` → Keep

## Questions for You

1. **Do you want to keep the old `tools/chatgpt/`, `tools/image-generator/`, `tools/instagram/`?**
   - Option A: Keep and refactor them into new `tools/` structure
   - Option B: Start fresh with new MCP tools

2. **Frontend location:**
   - Option A: `frontend/` folder (separate React app)
   - Option B: `public/` folder (simpler, but less organized)

3. **Backend location:**
   - Option A: `backend/` folder (clear separation)
   - Option B: `src/` folder (current)

## Recommendation

- **Backend**: Use `backend/` for clarity
- **Agents**: Use `agents/` folder (as you requested)
- **Tools**: Keep existing `tools/` but clean up structure
- **Frontend**: Use `frontend/` for React app
- **Archive**: Move old files to `archive/` (don't delete yet)

**Does this structure work for you? Any changes before we proceed?**

