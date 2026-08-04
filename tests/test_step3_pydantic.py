#!/usr/bin/env python3
"""
Step 3.3: Pydantic Models - Verification Script
Tests that Pydantic models work correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 Testing Pydantic Models...")
print("-" * 50)

# Test 1: Import models
print("\n1. Testing model imports...")
try:
    from backend.models.schemas import (
        ContentGenerateRequest,
        ContentGenerateResponse,
    )
    print("   ✅ All models imported successfully!")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Create valid request
print("\n2. Testing valid request creation...")
try:
    request = ContentGenerateRequest(
        topic="LLM",
        format="reel",
        posting_time="19:00",
        user_id="user_123"
    )
    print(f"   ✅ Created request:")
    print(f"      - Topic: {request.topic}")
    print(f"      - Format: {request.format}")
    print(f"      - Posting time: {request.posting_time}")
    print(f"      - User ID: {request.user_id}")
except Exception as e:
    print(f"   ❌ Error creating request: {e}")
    sys.exit(1)

# Test 3: Test optional fields (format can be None)
print("\n3. Testing optional fields...")
try:
    request_minimal = ContentGenerateRequest(
        topic="LLM",
        user_id="user_123"
        # format and posting_time are optional - not provided
    )
    print(f"   ✅ Created minimal request (optional fields omitted):")
    print(f"      - Topic: {request_minimal.topic}")
    print(f"      - Format: {request_minimal.format} (None - optional)")
    print(f"      - Posting time: {request_minimal.posting_time} (None - optional)")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Test validation (should fail for missing required field)
print("\n4. Testing validation (should reject invalid data)...")
try:
    # This should fail - topic is required
    invalid_request = ContentGenerateRequest(
        format="reel",
        user_id="user_123"
        # topic is missing!
    )
    print("   ❌ Validation failed - should have rejected missing topic!")
    sys.exit(1)
except Exception as e:
    print(f"   ✅ Validation working! Rejected invalid request:")
    print(f"      Error: {str(e)[:100]}...")

# Test 5: Test response model
print("\n5. Testing response model...")
try:
    response = ContentGenerateResponse(
        status="success",
        post_id="ig_123456",
        format="reel",
        posted_at="2024-01-15 19:00:00",
        message="Content posted successfully!"
    )
    print(f"   ✅ Created response:")
    print(f"      - Status: {response.status}")
    print(f"      - Format: {response.format}")
    print(f"      - Post ID: {response.post_id}")
except Exception as e:
    print(f"   ❌ Error creating response: {e}")
    sys.exit(1)

# Test 6: Test JSON conversion
print("\n6. Testing JSON conversion...")
try:
    request = ContentGenerateRequest(topic="LLM", user_id="123")
    json_data = request.model_dump()  # Convert to dict (becomes JSON)
    print(f"   ✅ Model converts to JSON:")
    print(f"      {json_data}")
except Exception as e:
    print(f"   ❌ Error converting to JSON: {e}")
    sys.exit(1)

print("-" * 50)
print("🎉 Step 3.3 Complete: Pydantic Models Working!")
print("\nWhat we accomplished:")
print("  ✅ Request models created (ContentGenerateRequest)")
print("  ✅ Response models created (ContentGenerateResponse)")
print("  ✅ Validation working (rejects invalid data)")
print("  ✅ Optional fields working (can be omitted)")
print("  ✅ JSON conversion working")
print("\nNext: Add route that uses these models!")

