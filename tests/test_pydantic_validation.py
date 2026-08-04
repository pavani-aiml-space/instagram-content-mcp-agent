#!/usr/bin/env python3
"""
Test to demonstrate how Pydantic validation works automatically
This shows what happens when you use type hints in FastAPI
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 Demonstrating Automatic Pydantic Validation")
print("=" * 60)

# Import FastAPI and our models
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.models.schemas import ContentGenerateRequest

# Create a test app
app = FastAPI()

@app.post("/test-validation")
def test_route(request: ContentGenerateRequest):
    """
    Test route - notice the type hint: request: ContentGenerateRequest
    This tells FastAPI to automatically validate!
    """
    return {
        "message": "Validation passed!",
        "topic": request.topic,
        "format": request.format
    }

# Create test client
client = TestClient(app)

print("\n1. Testing VALID request (should work):")
print("-" * 60)
try:
    response = client.post(
        "/test-validation",
        json={
            "topic": "LLM",
            "format": "reel",
            "user_id": "123"
        }
    )
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✅ VALID request passed validation!")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n2. Testing INVALID request (missing required field):")
print("-" * 60)
try:
    response = client.post(
        "/test-validation",
        json={
            "format": "reel",
            "user_id": "123"
            # topic is missing!
        }
    )
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 422:
        print("   ✅ INVALID request was rejected (validation worked!)")
        print("   ✅ Function never ran - FastAPI returned error first!")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n3. Testing INVALID request (wrong type):")
print("-" * 60)
try:
    response = client.post(
        "/test-validation",
        json={
            "topic": 123,  # Should be string!
            "user_id": "123"
        }
    )
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 422:
        print("   ✅ Wrong type was rejected (validation worked!)")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("🎯 Key Takeaway:")
print("   Just by adding 'request: ContentGenerateRequest' as a type hint,")
print("   FastAPI automatically validates ALL requests!")
print("   No extra code needed - it's automatic! 🎉")

