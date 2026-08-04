#!/usr/bin/env python3
"""
Database Setup Script
Helps you set up and test the database
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import (
    test_connection,
    create_tables,
    engine,
    DATABASE_URL
)
from database import models
from sqlalchemy import inspect, text


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def check_database_url():
    """Check and display database URL"""
    print_header("Database Configuration")
    print(f"Database URL: {DATABASE_URL}")
    print()
    
    # Check if .env file exists
    env_file = project_root / ".env"
    if env_file.exists():
        print("✅ Found .env file")
        with open(env_file) as f:
            if "DATABASE_URL" in f.read():
                print("✅ DATABASE_URL found in .env")
            else:
                print("⚠️  DATABASE_URL not found in .env (using default)")
    else:
        print("⚠️  .env file not found (using default DATABASE_URL)")
    
    print()
    response = input("Is this correct? (y/n): ").strip().lower()
    if response != 'y':
        print("\nTo change it, add to your .env file:")
        print("DATABASE_URL=postgresql://username:password@localhost:5432/instagram_agents")
        return False
    return True


def test_connection_step():
    """Test database connection"""
    print_header("Step 1: Testing Database Connection")
    
    if test_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("\n❌ Database connection failed!")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check DATABASE_URL in .env file")
        print("3. Verify database exists: psql -c 'CREATE DATABASE instagram_agents;'")
        return False


def check_tables_step():
    """Check if tables exist"""
    print_header("Step 2: Checking Tables")
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected_tables = ["users", "content_requests", "posts"]
    
    missing_tables = []
    for table in expected_tables:
        if table in tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' missing")
            missing_tables.append(table)
    
    if missing_tables:
        print(f"\n⚠️  Missing tables: {', '.join(missing_tables)}")
        response = input("Create missing tables? (y/n): ").strip().lower()
        if response == 'y':
            print("\nCreating tables...")
            create_tables()
            print("✅ Tables created!")
            return True
        else:
            return False
    
    return True


def test_crud_operations():
    """Test CRUD operations"""
    print_header("Step 3: Testing Database Operations")
    
    from database.connection import SessionLocal
    
    try:
        db = SessionLocal()
        
        # Test CREATE
        print("Testing CREATE...")
        test_user = models.User(
            instagram_user_id="setup_test_user",
            username="setup_test",
            access_token="test_token"
        )
        db.add(test_user)
        db.commit()
        print(f"✅ Created test user: {test_user.username} (ID: {test_user.id})")
        
        # Test READ
        print("\nTesting READ...")
        user = db.query(models.User).filter(
            models.User.instagram_user_id == "setup_test_user"
        ).first()
        if user:
            print(f"✅ Found user: {user.username}")
        else:
            print("❌ User not found")
            return False
        
        # Test UPDATE
        print("\nTesting UPDATE...")
        user.username = "setup_test_updated"
        db.commit()
        print(f"✅ Updated user: {user.username}")
        
        # Test DELETE
        print("\nTesting DELETE...")
        db.delete(user)
        db.commit()
        print("✅ Deleted test user")
        
        # Test counts
        print("\nTesting counts...")
        user_count = db.query(models.User).count()
        request_count = db.query(models.ContentRequest).count()
        post_count = db.query(models.Post).count()
        
        print(f"✅ Users in database: {user_count}")
        print(f"✅ Content requests in database: {request_count}")
        print(f"✅ Posts in database: {post_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error during CRUD testing: {e}")
        db.rollback()
        db.close()
        return False


def test_relationships():
    """Test table relationships"""
    print_header("Step 4: Testing Relationships")
    
    from database.connection import SessionLocal
    
    try:
        db = SessionLocal()
        
        # Create user
        user = models.User(
            instagram_user_id="relationship_test",
            username="relationship_test",
            access_token="test_token"
        )
        db.add(user)
        db.commit()
        
        # Create content request linked to user
        request = models.ContentRequest(
            user_id=user.id,
            topic="Test Topic",
            format="post",
            status="pending"
        )
        db.add(request)
        db.commit()
        
        # Test relationship: user -> content_requests
        print("Testing User -> ContentRequests relationship...")
        if user.content_requests:
            print(f"✅ User has {len(user.content_requests)} content request(s)")
        else:
            print("❌ Relationship not working")
            return False
        
        # Create post linked to request
        post = models.Post(
            request_id=request.id,
            instagram_post_id="ig_test_123",
            format="post",
            image_url="https://example.com/image.jpg",
            caption="Test caption",
            hashtags=["#test"]
        )
        db.add(post)
        db.commit()
        
        # Test relationship: request -> post
        print("\nTesting ContentRequest -> Post relationship...")
        if request.post:
            print(f"✅ Request has post: {request.post.instagram_post_id}")
        else:
            print("❌ Relationship not working")
            return False
        
        # Clean up
        db.delete(post)
        db.delete(request)
        db.delete(user)
        db.commit()
        print("\n✅ Cleaned up test data")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error during relationship testing: {e}")
        db.rollback()
        db.close()
        return False


def main():
    """Main setup function"""
    print_header("Database Setup and Testing")
    print("This script will help you set up and test your database.")
    print()
    
    # Step 0: Check configuration
    if not check_database_url():
        print("\n⚠️  Please configure DATABASE_URL and run again.")
        return
    
    # Step 1: Test connection
    if not test_connection_step():
        print("\n❌ Setup failed at connection step.")
        print("Please fix the connection issue and try again.")
        return
    
    # Step 2: Check/create tables
    if not check_tables_step():
        print("\n❌ Setup failed at table creation step.")
        return
    
    # Step 3: Test CRUD operations
    if not test_crud_operations():
        print("\n❌ Setup failed at CRUD testing step.")
        return
    
    # Step 4: Test relationships
    if not test_relationships():
        print("\n❌ Setup failed at relationship testing step.")
        return
    
    # Success!
    print_header("✅ Database Setup Complete!")
    print("\nYour database is ready to use!")
    print("\nNext steps:")
    print("1. Start the FastAPI server: uvicorn backend.main:app --reload")
    print("2. Test API endpoints")
    print("3. Create users via API")
    print("\nFor more information, see docs/DATABASE_SETUP_GUIDE.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

