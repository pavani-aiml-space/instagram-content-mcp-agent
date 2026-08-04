#!/usr/bin/env python3
"""
Step 3.1: Basic FastAPI App - Verification Script
Tests that FastAPI app can be created and basic route works
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 Testing Basic FastAPI App...")
print("-" * 50)

# Test 1: Import FastAPI app
print("\n1. Testing FastAPI app creation...")
try:
    from backend.main import app
    print(f"   ✅ FastAPI app created!")
    print(f"   ✅ App title: {app.title}")
    print(f"   ✅ App version: {app.version}")
except Exception as e:
    print(f"   ❌ Error creating app: {e}")
    sys.exit(1)

# Test 2: Check routes are registered
print("\n2. Testing routes...")
try:
    routes = [route.path for route in app.routes]
    print(f"   ✅ Found {len(routes)} route(s):")
    for route in routes:
        print(f"      - {route}")
    
    if "/" in routes:
        print("   ✅ Root route (/) is registered")
    else:
        print("   ❌ Root route (/) not found")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error checking routes: {e}")
    sys.exit(1)

# Test 3: Test the route function directly
print("\n3. Testing route function...")
try:
    from backend.main import read_root
    result = read_root()
    print(f"   ✅ Route function works!")
    print(f"   ✅ Returns: {result}")
    
    # Check it returns a dictionary
    if isinstance(result, dict):
        print("   ✅ Returns a dictionary (will become JSON)")
    else:
        print("   ⚠️  Returns something other than dict")
except Exception as e:
    print(f"   ❌ Error testing route: {e}")
    sys.exit(1)

print("-" * 50)
print("🎉 Step 3.1 Complete: Basic FastAPI App Created!")
print("\nWhat we accomplished:")
print("  ✅ FastAPI app created")
print("  ✅ Root route (/) defined")
print("  ✅ Route function works")
print("\nNext: We'll start the server and test it with HTTP requests!")
print("\nTo run the server:")
print("  python backend/main.py")
print("  OR")
print("  uvicorn backend.main:app --reload")

