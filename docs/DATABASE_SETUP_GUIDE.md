# Database Setup and Testing Guide

## Overview

This project uses **PostgreSQL** as the database with **SQLAlchemy ORM** for database operations.

## Database Schema

We have 3 essential tables:

1. **`users`** - Instagram influencer accounts
2. **`content_requests`** - Content generation requests
3. **`posts`** - Successfully posted Instagram content

## Step 1: Install PostgreSQL

### macOS (using Homebrew)

```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Verify installation
psql --version
```

### Linux (Ubuntu/Debian)

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

### Windows

1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Remember the password you set for the `postgres` user
4. PostgreSQL will start automatically as a service

## Step 2: Create Database

### macOS/Linux

```bash
# Connect to PostgreSQL (default user is your system username on macOS)
psql postgres

# Or if you need to use 'postgres' user:
psql -U postgres
```

Then in the PostgreSQL prompt:

```sql
-- Create database
CREATE DATABASE instagram_agents;

-- Verify it was created
\l

-- Exit
\q
```

### Windows

1. Open **pgAdmin** (installed with PostgreSQL)
2. Right-click on **Databases** → **Create** → **Database**
3. Name: `instagram_agents`
4. Click **Save**

Or use command line:

```bash
# Open Command Prompt as Administrator
psql -U postgres

# Create database
CREATE DATABASE instagram_agents;
\q
```

## Step 3: Configure Database URL

### Option 1: Environment Variable (Recommended)

Add to your `.env` file:

```bash
# macOS (uses your system username)
DATABASE_URL=postgresql://your_username@localhost:5432/instagram_agents

# Linux/Windows (uses postgres user)
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/instagram_agents

# With password (if you set one)
DATABASE_URL=postgresql://username:password@localhost:5432/instagram_agents
```

### Option 2: Default (macOS)

If you don't set `DATABASE_URL`, it defaults to:
```
postgresql://{your_username}@localhost:5432/instagram_agents
```

## Step 4: Test Database Connection

### Quick Test

```bash
# Activate virtual environment
source venv/bin/activate

# Test connection
python -c "from database.connection import test_connection; test_connection()"
```

Expected output:
```
✅ Database connection successful!
```

### Using the Test Script

```bash
# Run the database test script
python tests/test_step2_database.py
```

This will:
- ✅ Test database connection
- ✅ Check if tables exist
- ✅ Create tables if missing
- ✅ Test inserting data
- ✅ Test reading data
- ✅ Clean up test data

## Step 5: Create Tables

### Automatic (Recommended)

Tables are created automatically when you run the test script or start the server.

### Manual

```python
from database.connection import create_tables
create_tables()
```

Or using Python:

```bash
python -c "from database.connection import create_tables; create_tables()"
```

## Step 6: Verify Tables

### Using psql

```bash
psql instagram_agents

# List all tables
\dt

# Describe a table
\d users
\d content_requests
\d posts

# Exit
\q
```

### Using Python

```python
from database.connection import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables:", tables)
# Expected: ['users', 'content_requests', 'posts']
```

## Common Issues and Solutions

### Issue 1: "role 'postgres' does not exist" (macOS)

**Problem**: macOS PostgreSQL uses your system username, not 'postgres'.

**Solution**: Use your system username in DATABASE_URL:
```bash
DATABASE_URL=postgresql://your_username@localhost:5432/instagram_agents
```

Or create a postgres user:
```bash
createuser -s postgres
```

### Issue 2: "password authentication failed"

**Problem**: PostgreSQL requires a password.

**Solution**: 
1. Set password in DATABASE_URL:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/instagram_agents
   ```

2. Or configure PostgreSQL to allow local connections without password (for development only):
   Edit `/etc/postgresql/14/main/pg_hba.conf`:
   ```
   local   all             all                                     trust
   host    all             all             127.0.0.1/32            trust
   ```
   Then restart PostgreSQL:
   ```bash
   sudo systemctl restart postgresql
   ```

### Issue 3: "database does not exist"

**Problem**: Database hasn't been created.

**Solution**: Create the database:
```bash
psql postgres -c "CREATE DATABASE instagram_agents;"
```

### Issue 4: "connection refused"

**Problem**: PostgreSQL service is not running.

**Solution**: Start PostgreSQL:
```bash
# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql

# Windows
# Check Services → PostgreSQL
```

### Issue 5: "port 5432 already in use"

**Problem**: Another PostgreSQL instance is running.

**Solution**: 
1. Find the process:
   ```bash
   lsof -i :5432
   ```
2. Kill it or use a different port in DATABASE_URL

## Testing Database Operations

### Test 1: Create a User

```python
from database.connection import SessionLocal
from database.models import User

db = SessionLocal()

# Create user
user = User(
    instagram_user_id="test_user_123",
    username="test_user",
    access_token="test_token"
)
db.add(user)
db.commit()
print(f"Created user: {user.id}")

db.close()
```

### Test 2: Create a Content Request

```python
from database.connection import SessionLocal
from database.models import User, ContentRequest

db = SessionLocal()

# Get user
user = db.query(User).filter(User.instagram_user_id == "test_user_123").first()

# Create request
request = ContentRequest(
    user_id=user.id,
    topic="LLM",
    format="post",
    status="pending"
)
db.add(request)
db.commit()
print(f"Created request: {request.id}")

db.close()
```

### Test 3: Query Data

```python
from database.connection import SessionLocal
from database.models import User, ContentRequest, Post

db = SessionLocal()

# Count records
user_count = db.query(User).count()
request_count = db.query(ContentRequest).count()
post_count = db.query(Post).count()

print(f"Users: {user_count}")
print(f"Requests: {request_count}")
print(f"Posts: {post_count}")

# Get all users
users = db.query(User).all()
for user in users:
    print(f"User: {user.username} ({user.instagram_user_id})")

db.close()
```

## Database Maintenance

### View All Data

```sql
-- Connect to database
psql instagram_agents

-- View users
SELECT * FROM users;

-- View content requests
SELECT * FROM content_requests;

-- View posts
SELECT * FROM posts;

-- View with relationships
SELECT 
    u.username,
    cr.topic,
    cr.status,
    p.instagram_post_id
FROM users u
LEFT JOIN content_requests cr ON u.id = cr.user_id
LEFT JOIN posts p ON cr.id = p.request_id;
```

### Clear Test Data

```python
from database.connection import SessionLocal
from database.models import User, ContentRequest, Post

db = SessionLocal()

# Delete all posts
db.query(Post).delete()

# Delete all content requests
db.query(ContentRequest).delete()

# Delete all users
db.query(User).delete()

db.commit()
db.close()
print("All data cleared")
```

### Backup Database

```bash
# Backup
pg_dump instagram_agents > backup.sql

# Restore
psql instagram_agents < backup.sql
```

## Integration with FastAPI

The database is automatically used by FastAPI through dependency injection:

```python
from fastapi import Depends
from database.connection import get_db
from sqlalchemy.orm import Session

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

## Next Steps

After database setup:
1. ✅ Test connection: `python tests/test_step2_database.py`
2. ✅ Start FastAPI server: `uvicorn backend.main:app --reload`
3. ✅ Test API endpoints that use database
4. ✅ Create test users via API

## Quick Reference

```bash
# Test connection
python -c "from database.connection import test_connection; test_connection()"

# Create tables
python -c "from database.connection import create_tables; create_tables()"

# Run full test
python tests/test_step2_database.py

# Connect to database
psql instagram_agents

# List tables
\dt

# Exit psql
\q
```

