# Installation Guide: Fixing npm Permissions

## 🔧 The Problem

Your `node_modules` directory is owned by `root` instead of your user, which prevents npm from installing new packages.

## ✅ Solution Options

### Option 1: Fix Permissions (Recommended)

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp

# Fix ownership of node_modules
sudo chown -R $(whoami) node_modules

# Now install LangChain packages
npm install langchain @langchain/core @langchain/openai @langchain/community @langchain/langgraph
```

### Option 2: Clean Reinstall (If Option 1 doesn't work)

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp

# Backup your .env file first!
cp .env .env.backup

# Remove node_modules and package-lock
rm -rf node_modules package-lock.json

# Reinstall all dependencies
npm install

# Install LangChain packages
npm install langchain @langchain/core @langchain/openai @langchain/community @langchain/langgraph
```

### Option 3: Use npx (Temporary, for testing)

If you just want to test without installing globally:

```bash
# This won't work for our use case, but good to know
npx langchain --version
```

## ✅ Verify Installation

After installing, verify:

```bash
# Check if packages are installed
npm list langchain @langchain/core @langchain/openai @langchain/community @langchain/langgraph

# Or check package.json
cat package.json | grep langchain
```

## 🎯 What Gets Installed

1. **langchain**: Core framework
2. **@langchain/core**: Core utilities and types
3. **@langchain/openai**: OpenAI integration
4. **@langchain/community**: Community tools and integrations
5. **@langchain/langgraph**: State graph library

## 📝 After Installation

Once installed, we'll:
1. Update the tool to use `StructuredTool`
2. Add Zod for schema validation
3. Create more tools
4. Build the LangGraph workflow

---

**Note**: The current tool code works without dependencies (it's a simple wrapper). Once dependencies are installed, we'll enhance it with proper LangChain classes.







