#!/usr/bin/env python3
"""
Quick Database Test
Quick script to verify database is working
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import test_connection, create_tables, engine
from database import models
from sqlalchemy import inspect

def main():
    print("🔍 Quick Database Test\n")
    
    # Test 1: Connection
    print("1. Testing connection...", end=" ")
    if test_connection():
        print("✅")
    else:
        print("❌")
        print("   Error: Cannot connect to database")
        print("   Check: DATABASE_URL, PostgreSQL running, database exists")
        return False
    
    # Test 2: Tables
    print("2. Checking tables...", end=" ")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected = ["users", "content_requests", "posts"]
    
    missing = [t for t in expected if t not in tables]
    if missing:
        print("❌")
        print(f"   Missing: {', '.join(missing)}")
        print("   Creating tables...", end=" ")
        create_tables()
        print("✅")
    else:
        print("✅")
    
    # Test 3: Count records
    print("3. Checking data...", end=" ")
    from database.connection import SessionLocal
    db = SessionLocal()
    try:
        user_count = db.query(models.User).count()
        request_count = db.query(models.ContentRequest).count()
        post_count = db.query(models.Post).count()
        print("✅")
        print(f"   Users: {user_count}, Requests: {request_count}, Posts: {post_count}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()
    
    print("\n✅ Database is ready!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

