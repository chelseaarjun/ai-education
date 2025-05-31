# Migration Plan: Memory-Efficient Embeddings with OpenAI and Postgres+pgvector

## Current System Issues
1. **Memory Constraint**: Running out of 512MB memory on Render with sentence-transformers
2. **URL Citation Problems**: Incorrect URL fragment references (#) in content extraction
3. **Technology Stack**: Need to migrate from Supabase to Render Postgres with pgvector

## Migration Strategy Overview

### Phase 1: Update Data Pipeline for OpenAI Embeddings
1. Replace sentence-transformers with OpenAI Embeddings API
2. Fix URL fragment reference issues in content extraction
3. Modify schema for compatibility with OpenAI's embedding dimensions

### Phase 2: Setup Render PostgreSQL with pgvector
1. Create Render PostgreSQL database
2. Configure pgvector extension
3. Design optimized schema for vector search

### Phase 3: Update Chatbot API
1. Remove sentence-transformers dependency
2. Implement OpenAI embedding generation
3. Connect to Render PostgreSQL 
4. Update search functions for new embedding format

## Detailed Implementation Plan

### 1. Data Pipeline Changes

#### 1.1 Update Content Extraction (`extract-structured-content.py`)
- Fix URL fragment references:
  - Only use actual IDs from the HTML, not generated ones
  - Check element.get('id') exists before using in URL fragments
  - Only generate reference URLs for sections with valid IDs

```python
# Current problematic code:
subsection_id = heading.get('id', re.sub(r'[^a-z0-9]+', '-', title.lower()))
# ...
"url": f"{url}#{subsection_id}"

# Replacement approach:
if heading.get('id'):
    subsection_id = heading.get('id')
    section_url = f"{url}#{subsection_id}"
else:
    subsection_id = f"section-{i}"
    section_url = url  # No fragment if no ID exists
```

#### 1.2 Create New OpenAI Embeddings Generator (`generate-pgvector-embeddings.py`)
- Replace sentence-transformers with OpenAI API
- Update embedding dimensions (1536 for text-embedding-ada-002)
- Implement rate limiting and batching for API calls
- Add error handling for API failures

```python
# Sample implementation snippet
import openai
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def generate_embeddings(texts, batch_size=20):
    """Generate embeddings using OpenAI API with retries."""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=batch
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        
    return all_embeddings
```

### 2. PostgreSQL + pgvector Setup

#### 2.1 Create Schema and Functions in Postgres
```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Course content table
CREATE TABLE course_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT,
    content_type TEXT,
    part_id TEXT,
    module_id TEXT,
    parent_id UUID,
    importance REAL DEFAULT 0.7,
    embedding vector(1536)  -- OpenAI dimensions
);

-- Create index for vector similarity search
CREATE INDEX ON course_content USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Function for similarity search
CREATE OR REPLACE FUNCTION match_course_content(
    query_embedding vector(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    content TEXT,
    url TEXT,
    content_type TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cc.id,
        cc.title,
        cc.content,
        cc.url,
        cc.content_type,
        1 - (cc.embedding <=> query_embedding) AS similarity
    FROM course_content cc
    WHERE 1 - (cc.embedding <=> query_embedding) > match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;
```

#### 2.2 Database Connection Management
- Create connection pool for efficient DB access
- Implement environment-based configuration

### 3. Chatbot API Updates

#### 3.1 Remove sentence-transformers Dependency
- Update requirements.txt to remove sentence-transformers
- Add OpenAI dependency

#### 3.2 Update Embedding Generation in API
```python
# Replace sentence-transformers with OpenAI
def generate_embedding(text):
    """Generate embedding using OpenAI API."""
    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        raise
```

#### 3.3 PostgreSQL Connection Management
```python
import psycopg
from psycopg_pool import ConnectionPool

# Initialize connection pool
DB_URL = os.environ.get("DATABASE_URL")
pool = ConnectionPool(DB_URL, min_size=1, max_size=10)

async def query_database(embedding, threshold=0.5, limit=5):
    """Query the database for similar content."""
    async with pool.connection() as conn:
        result = await conn.execute(
            "SELECT * FROM match_course_content($1, $2, $3)",
            (embedding, threshold, limit)
        )
        return await result.fetchall()
```

## Testing Strategy

### 1. Component Testing
- Test OpenAI embedding generation separately
- Verify PostgreSQL query performance
- Test URL fragment extraction accuracy

### 2. Integration Testing
- Compare search results between old and new systems
- Verify citation URLs are correct
- Test memory usage on Render

### 3. Performance Testing
- Measure response times under load
- Monitor memory usage
- Test recovery from API rate limits

## Deployment Plan

### 1. Development Environment Setup
- Create Render PostgreSQL database
- Configure local environment for testing
- Update environment variables

### 2. Staging Deployment
- Deploy updated data pipeline
- Generate new embeddings
- Verify search quality

### 3. Production Migration
- Schedule maintenance window
- Execute migration scripts
- Deploy updated chatbot API
- Monitor performance and errors

## Rollback Plan
- Maintain Supabase instance during migration
- Create DB snapshots before migration
- Prepare rollback scripts to revert code changes

## Resource Requirements
- OpenAI API usage costs (~$0.0004 per 1K tokens)
- Render PostgreSQL database (at least 1GB plan)
- Temporary increased memory during migration 