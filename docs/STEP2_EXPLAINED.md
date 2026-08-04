# Step 2: Database Setup - Explained

## What We're Building

**Goal**: Set up PostgreSQL database and create our 3 essential tables using SQLAlchemy ORM.

---

## Concepts to Understand

### 1. What is PostgreSQL?

**PostgreSQL** is a relational database management system (RDBMS).

**Think of it like:**
- A filing cabinet that stores data permanently
- Data survives even if your server restarts
- Organized into "tables" (like spreadsheets)

**Why PostgreSQL?**
- Free and open-source
- Reliable and widely used
- Supports complex queries
- Great for production applications

---

### 2. What is SQLAlchemy ORM?

**ORM** = Object-Relational Mapping

**What it does:**
- Lets you write Python code instead of SQL
- Converts Python classes to database tables
- Converts Python objects to database rows

**Example:**

**Without ORM (Raw SQL):**
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL
);

INSERT INTO users (id, username) VALUES ('123', 'john_doe');
```

**With ORM (SQLAlchemy):**
```python
class User(Base):
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)

user = User(id='123', username='john_doe')
session.add(user)
session.commit()
```

**Why use ORM?**
- ✅ Write Python, not SQL (easier for Python developers)
- ✅ Type safety (Python checks your code)
- ✅ Database-agnostic (can switch databases easily)
- ✅ Less error-prone (no SQL syntax errors)

---

### 3. Our 3 Essential Tables

#### Table 1: `users`
**Purpose**: Store Instagram influencer accounts

**Fields:**
- `id` - Unique identifier
- `instagram_user_id` - Instagram account ID
- `username` - Instagram username
- `access_token` - Instagram API token (for authentication)
- `created_at` - When account was added

**Why needed?** To identify who's making requests and authenticate with Instagram API.

---

#### Table 2: `content_requests`
**Purpose**: Track every content generation request

**Fields:**
- `id` - Unique identifier
- `user_id` - Which user made the request (links to `users`)
- `topic` - What topic to create content about
- `format` - "post", "story", or "reel"
- `posting_time` - When to post (optional)
- `status` - "pending", "processing", "completed", "failed"
- `created_at` - When request was made
- `completed_at` - When request finished

**Why needed?** To track all requests and their status.

---

#### Table 3: `posts`
**Purpose**: Store successfully posted Instagram content

**Fields:**
- `id` - Unique identifier
- `request_id` - Which request this post came from (links to `content_requests`)
- `instagram_post_id` - Instagram's post ID
- `format` - "post", "story", or "reel"
- `image_url` - URL of posted image
- `caption` - Posted caption text
- `hashtags` - Array of hashtags
- `posted_at` - When it was posted to Instagram

**Why needed?** To track what was posted and link back to original request.

---

## Database Relationships

```
users (1) ──→ (many) content_requests
                      │
                      └──→ (1) posts
```

**Explanation:**
- One user can make many requests
- One request can result in one post (if successful)

---

## What We'll Create

1. **Database Connection** (`database/connection.py`)
   - Connects to PostgreSQL
   - Creates connection pool (efficient!)
   - Handles errors gracefully

2. **Database Models** (`database/models.py`)
   - Python classes representing tables
   - SQLAlchemy ORM models
   - Defines relationships between tables

3. **Database Schema** (`database/schema.sql`)
   - SQL script to create tables
   - Can run directly if needed

4. **Test Script** (`tests/test_step2_database.py`)
   - Tests database connection
   - Tests table creation
   - Tests inserting/reading data

---

## Key Concepts

### Connection Pooling
**What**: Reuse database connections instead of creating new ones each time

**Why**: Much faster! Creating connections is expensive.

**Example:**
```python
# Without pooling (slow)
for i in range(100):
    conn = create_connection()  # Slow!
    query(conn)
    close(connection)

# With pooling (fast)
pool = create_pool()  # Create once
for i in range(100):
    conn = pool.get_connection()  # Fast!
    query(conn)
    pool.return_connection(conn)  # Reuse
```

### Foreign Keys
**What**: Links between tables

**Example:**
- `content_requests.user_id` → `users.id`
- Ensures data integrity (can't create request for non-existent user)

### Timestamps
**What**: `created_at`, `posted_at` fields

**Why**: Track when things happened (useful for analytics, debugging)

---

## Next Steps

1. Check if PostgreSQL is installed
2. Create database
3. Set up SQLAlchemy connection
4. Create models (Python classes)
5. Create tables in database
6. Test everything works

---

Ready to build? Let's start!

