# Step 1: Python Environment Setup - Explained

## What We Just Did

### 1. Created Virtual Environment
```bash
python3 -m venv venv
```

**What is a virtual environment?**
- Isolated Python environment for this project
- Has its own Python interpreter and packages
- Prevents conflicts with other projects

**Why use it?**
- Project A might need `fastapi==0.100.0`
- Project B might need `fastapi==0.104.0`
- Virtual environments keep them separate!

**How to activate:**
```bash
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate     # On Windows
```

**How to deactivate:**
```bash
deactivate
```

---

### 2. Created requirements.txt

**What is requirements.txt?**
- List of all Python packages this project needs
- Version numbers ensure consistency
- Anyone can install exact same versions

**Package Groups Explained:**

#### FastAPI Backend
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server (runs FastAPI)
- `python-dotenv` - Loads `.env` file (environment variables)

#### Database
- `sqlalchemy` - ORM (Object-Relational Mapping) - write Python, not SQL
- `psycopg2-binary` - PostgreSQL driver (connects to database)
- `alembic` - Database migrations (change database structure over time)

#### LangGraph & LangChain
- `langchain` - Framework for building LLM applications
- `langgraph` - State-based workflows (for agents)
- `langchain-openai` - OpenAI integration for LangChain
- `langchain-google-genai` - Google Gemini integration for LangChain

#### LLM Providers
- `openai` - Direct OpenAI API client
- `google-generativeai` - Google Gemini API client

#### Image Processing
- `Pillow` - Image manipulation (resize, optimize)
- `requests` - HTTP library (call APIs)

#### Utilities
- `pydantic` - Data validation (for FastAPI request/response)
- `pydantic-settings` - Settings management

---

### 3. Installing Dependencies

**Command:**
```bash
pip install -r requirements.txt
```

**What happens:**
- Reads `requirements.txt`
- Downloads each package
- Installs them in `venv/` folder
- Creates dependency tree (some packages depend on others)

**Why `-r`?**
- `-r` means "read from file"
- Without it, you'd have to type each package name manually

---

## Key Concepts Learned

### Virtual Environment
- **Isolation**: Each project has its own Python packages
- **Reproducibility**: Same packages, same versions
- **Safety**: Won't break other projects

### requirements.txt
- **Dependency Management**: Track what packages you need
- **Version Pinning**: `fastapi==0.104.1` ensures exact version
- **Sharing**: Others can install same environment

### pip
- **Package Manager**: Installs Python packages
- **PyPI**: Python Package Index (where packages come from)
- **Dependencies**: Automatically installs required packages

---

## Next Steps

After installing, we'll:
1. Verify installation worked
2. Test importing key packages
3. Create basic project structure
4. Ready for Step 2: Database Setup!

---

## Common Issues & Solutions

**Issue**: `python3: command not found`
- **Solution**: Install Python 3.11+ from python.org or use `brew install python3`

**Issue**: `pip: command not found`
- **Solution**: Python 3.4+ includes pip. Try `python3 -m pip`

**Issue**: Permission errors
- **Solution**: Use virtual environment (we just created one!)

**Issue**: Package installation fails
- **Solution**: Check internet connection, try `pip install --upgrade pip` first

