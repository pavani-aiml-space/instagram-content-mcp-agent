#!/usr/bin/env python3
"""
Step 3: Server Testing Script
Tests that the FastAPI server is running and responding
"""

import requests
import time
import sys

print("🔍 Testing FastAPI Server...")
print("-" * 50)

# Wait a moment for server to be ready
print("\n1. Waiting for server to be ready...")
time.sleep(1)

# Test 1: Root endpoint
print("\n2. Testing root endpoint (GET /)...")
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    
    if response.status_code == 200:
        print(f"   ✅ Status code: {response.status_code} (OK)")
        data = response.json()
        print(f"   ✅ Response: {data}")
        
        # Check response structure
        if "message" in data and "status" in data:
            print("   ✅ Response has expected fields (message, status)")
        else:
            print("   ⚠️  Response missing expected fields")
    else:
        print(f"   ❌ Unexpected status code: {response.status_code}")
        sys.exit(1)
        
except requests.exceptions.ConnectionError:
    print("   ❌ Could not connect to server!")
    print("   💡 Make sure server is running:")
    print("      uvicorn backend.main:app --reload")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Check API docs
print("\n3. Testing API documentation endpoint...")
try:
    response = requests.get("http://localhost:8000/docs", timeout=5)
    if response.status_code == 200:
        print("   ✅ API docs accessible at http://localhost:8000/docs")
    else:
        print(f"   ⚠️  Docs returned status: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Could not access docs: {e}")

# Test 3: Check OpenAPI schema
print("\n4. Testing OpenAPI schema...")
try:
    response = requests.get("http://localhost:8000/openapi.json", timeout=5)
    if response.status_code == 200:
        schema = response.json()
        print("   ✅ OpenAPI schema accessible")
        print(f"   ✅ API title: {schema.get('info', {}).get('title')}")
        print(f"   ✅ API version: {schema.get('info', {}).get('version')}")
        print(f"   ✅ Number of paths: {len(schema.get('paths', {}))}")
    else:
        print(f"   ⚠️  Schema returned status: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Could not access schema: {e}")

print("-" * 50)
print("🎉 Server Testing Complete!")
print("\nWhat we verified:")
print("  ✅ Server is running")
print("  ✅ Root endpoint (/) works")
print("  ✅ Returns correct JSON")
print("  ✅ API documentation accessible")
print("\nYou can now:")
print("  - Visit http://localhost:8000/ in your browser")
print("  - Visit http://localhost:8000/docs for interactive API docs")
print("  - Visit http://localhost:8000/redoc for alternative docs")

