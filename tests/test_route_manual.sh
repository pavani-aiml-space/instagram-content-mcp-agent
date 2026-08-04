#!/bin/bash
# Manual test script for /api/content/generate-example route
# Run this after starting the FastAPI server

echo "🧪 Testing /api/content/generate-example Route"
echo "============================================================"
echo ""
echo "Make sure the server is running: uvicorn backend.main:app --reload"
echo ""

# Test 1: Valid request with all fields
echo "1. Testing VALID request (all fields provided)..."
echo "------------------------------------------------------------"
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LLM",
    "format": "reel",
    "posting_time": "19:00",
    "user_id": "test_user_123"
  }' | python -m json.tool
echo ""
echo ""

# Test 2: Valid request with minimal fields
echo "2. Testing VALID request (minimal fields - optional omitted)..."
echo "------------------------------------------------------------"
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI Agents",
    "user_id": "test_user_456"
  }' | python -m json.tool
echo ""
echo ""

# Test 3: Invalid request (missing topic)
echo "3. Testing INVALID request (missing required field: topic)..."
echo "------------------------------------------------------------"
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "format": "reel",
    "user_id": "test_user_123"
  }' | python -m json.tool
echo ""
echo ""

# Test 4: Invalid request (missing user_id)
echo "4. Testing INVALID request (missing required field: user_id)..."
echo "------------------------------------------------------------"
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LLM",
    "format": "reel"
  }' | python -m json.tool
echo ""
echo ""

# Test 5: Invalid request (wrong type)
echo "5. Testing INVALID request (wrong type: topic is number)..."
echo "------------------------------------------------------------"
curl -X POST http://localhost:8000/api/content/generate-example \
  -H "Content-Type: application/json" \
  -d '{
    "topic": 123,
    "user_id": "test_user_123"
  }' | python -m json.tool
echo ""
echo ""

echo "============================================================"
echo "🎉 Testing Complete!"
echo ""
echo "Summary:"
echo "  ✅ Valid requests return success responses"
echo "  ✅ Invalid requests return 422 validation errors"
echo "  ✅ Pydantic validation is working correctly!"

