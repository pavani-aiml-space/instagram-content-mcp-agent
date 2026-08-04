#!/usr/bin/env python3
"""
Step 2: Database Setup - Verification Script
Tests database connection, models, and table creation
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import test_connection, create_tables, SessionLocal, engine
from database import models
from sqlalchemy import inspect

print("🔍 Testing Database Setup...")
print("-" * 50)

# Test 1: Database Connection
print("\n1. Testing database connection...")
if test_connection():
    print("   ✅ Connection successful!")
else:
    print("   ❌ Connection failed!")
    sys.exit(1)

# Test 2: Check if tables exist
print("\n2. Checking if tables exist...")
inspector = inspect(engine)
tables = inspector.get_table_names()
expected_tables = ["users", "content_requests", "posts"]

all_tables_exist = True
for table in expected_tables:
    if table in tables:
        print(f"   ✅ Table '{table}' exists")
    else:
        print(f"   ❌ Table '{table}' missing")
        all_tables_exist = False

if not all_tables_exist:
    print("\n   Creating missing tables...")
    create_tables()

# Test 3: Test inserting data
print("\n3. Testing data insertion...")
try:
    db = SessionLocal()
    
    # Create a test user
    test_user = models.User(
        instagram_user_id="test_123",
        username="test_user",
        access_token="test_token"
    )
    db.add(test_user)
    db.commit()
    print(f"   ✅ Created test user: {test_user.username} (ID: {test_user.id})")
    
    # Create a test content request
    test_request = models.ContentRequest(
        user_id=test_user.id,
        topic="LLM",
        format="reel",
        status="pending"
    )
    db.add(test_request)
    db.commit()
    print(f"   ✅ Created test request: {test_request.topic} (ID: {test_request.id})")
    
    # Create a test post
    test_post = models.Post(
        request_id=test_request.id,
        instagram_post_id="ig_123",
        format="reel",
        image_url="https://example.com/image.jpg",
        caption="Test caption",
        hashtags=["#test", "#llm"]
    )
    db.add(test_post)
    db.commit()
    print(f"   ✅ Created test post: {test_post.instagram_post_id} (ID: {test_post.id})")
    
    # Test 4: Test reading data
    print("\n4. Testing data retrieval...")
    user_count = db.query(models.User).count()
    request_count = db.query(models.ContentRequest).count()
    post_count = db.query(models.Post).count()
    
    print(f"   ✅ Users in database: {user_count}")
    print(f"   ✅ Content requests in database: {request_count}")
    print(f"   ✅ Posts in database: {post_count}")
    
    # Clean up test data
    print("\n5. Cleaning up test data...")
    db.delete(test_post)
    db.delete(test_request)
    db.delete(test_user)
    db.commit()
    print("   ✅ Test data cleaned up")
    
    db.close()
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    db.rollback()
    db.close()
    sys.exit(1)

print("-" * 50)
print("🎉 Step 2 Complete: Database Setup!")
print("\nWhat we accomplished:")
print("  ✅ PostgreSQL database connected")
print("  ✅ 3 tables created (users, content_requests, posts)")
print("  ✅ SQLAlchemy ORM models working")
print("  ✅ Can insert and read data")
print("\nNext: Step 3 - FastAPI Backend (Basic API)")

