#!/usr/bin/env python3
"""
Step 1: Python Environment Setup - Verification Script
Tests that all packages are installed correctly
"""

print("🔍 Testing Python Environment Setup...")
print("-" * 50)

# Test imports
try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI: {e}")

try:
    import sqlalchemy
    print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
except ImportError as e:
    print(f"❌ SQLAlchemy: {e}")

try:
    import langchain
    print(f"✅ LangChain {langchain.__version__}")
except ImportError as e:
    print(f"❌ LangChain: {e}")

try:
    import langgraph
    print("✅ LangGraph (imported successfully)")
except ImportError as e:
    print(f"❌ LangGraph: {e}")

try:
    import openai
    print(f"✅ OpenAI {openai.__version__}")
except ImportError as e:
    print(f"❌ OpenAI: {e}")

try:
    import google.generativeai
    print("✅ Google Generative AI")
except ImportError as e:
    print(f"❌ Google Generative AI: {e}")

try:
    from PIL import Image
    print(f"✅ Pillow (PIL)")
except ImportError as e:
    print(f"❌ Pillow: {e}")

try:
    import pydantic
    print(f"✅ Pydantic {pydantic.__version__}")
except ImportError as e:
    print(f"❌ Pydantic: {e}")

print("-" * 50)
print("🎉 Step 1 Complete: Python Environment Setup!")
print("\nNext: Step 2 - Database Setup (PostgreSQL + SQLAlchemy)")

