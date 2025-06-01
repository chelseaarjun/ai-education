#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Migration Script

This script tests the migration from sentence-transformers/Supabase to OpenAI/PostgreSQL.
It validates:
1. OpenAI API connectivity and embedding generation
2. PostgreSQL connectivity and vector search
3. End-to-end search functionality
"""

import os
import sys
import time
import openai
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-ada-002")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize database connection pool
db_pool = None

def get_db_pool():
    """Get or create database connection pool."""
    global db_pool
    if db_pool is None:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is not set")
        db_pool = ConnectionPool(DATABASE_URL, min_size=1, max_size=5)
    return db_pool

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def generate_embedding(text):
    """Generate embedding using OpenAI API with retries."""
    try:
        response = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        raise

def test_openai_connection():
    """Test OpenAI API connectivity and embedding generation."""
    print("\n=== Testing OpenAI API Connection ===")
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY is not set")
        return False
    
    try:
        start_time = time.time()
        test_text = "Testing OpenAI embeddings for AI Education chatbot"
        embedding = generate_embedding(test_text)
        elapsed = time.time() - start_time
        
        print(f"✅ Successfully generated embedding in {elapsed:.2f} seconds")
        print(f"   Model: {EMBEDDING_MODEL}")
        print(f"   Embedding dimensions: {len(embedding)}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API test failed: {str(e)}")
        return False

def test_postgres_connection():
    """Test PostgreSQL connection and basic functionality."""
    print("\n=== Testing PostgreSQL Connection ===")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL is not set")
        return False
    
    try:
        # Get connection pool
        pool = get_db_pool()
        
        # Test connection
        with pool.connection() as conn:
            # Check PostgreSQL version
            result = conn.execute("SELECT version();").fetchone()
            print(f"✅ Connected to PostgreSQL: {result[0]}")
            
            # Check if pgvector extension is installed
            has_vector = conn.execute(
                "SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector';"
            ).fetchone()[0]
            
            if has_vector:
                print("✅ pgvector extension is installed")
            else:
                print("❌ pgvector extension is NOT installed")
                return False
            
            # Check if tables exist
            tables = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('course_content', 'content_links');
            """).fetchall()
            
            table_names = [row[0] for row in tables]
            if 'course_content' in table_names:
                print("✅ course_content table exists")
            else:
                print("❌ course_content table does NOT exist")
                return False
                
            if 'content_links' in table_names:
                print("✅ content_links table exists")
            else:
                print("❌ content_links table does NOT exist")
            
            # Check if there's any content
            count = conn.execute("SELECT COUNT(*) FROM course_content;").fetchone()[0]
            print(f"   Total content items: {count}")
            
            return True
    except Exception as e:
        print(f"❌ PostgreSQL test failed: {str(e)}")
        return False

def test_vector_search():
    """Test vector search functionality."""
    print("\n=== Testing Vector Search ===")
    
    try:
        # Generate a test embedding
        query = "What are large language models?"
        print(f"Query: '{query}'")
        
        start_time = time.time()
        embedding = generate_embedding(query)
        print(f"✅ Generated embedding in {time.time() - start_time:.2f} seconds")
        
        # Search in PostgreSQL
        pool = get_db_pool()
        
        with pool.connection() as conn:
            start_time = time.time()
            results = conn.execute(
                "SELECT * FROM match_course_content($1, $2, $3)",
                (embedding, 0.5, 3)  # threshold, limit
            ).fetchall()
            
            search_time = time.time() - start_time
            print(f"✅ Completed search in {search_time:.2f} seconds")
            print(f"   Found {len(results)} results")
            
            # Print results
            if results:
                print("\nTop results:")
                for i, row in enumerate(results):
                    print(f"\n{i+1}. {row[1]}")  # Title
                    print(f"   URL: {row[3]}")  # URL
                    print(f"   Similarity: {row[5]:.4f}")  # Similarity
                    # Print a snippet of content
                    content = row[2]
                    if len(content) > 100:
                        content = content[:97] + "..."
                    print(f"   Content: {content}")
            
            return len(results) > 0
    except Exception as e:
        print(f"❌ Vector search test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n=== Migration Test Suite ===")
    print("Testing OpenAI and PostgreSQL integration")
    
    tests = [
        ("OpenAI API", test_openai_connection),
        ("PostgreSQL Connection", test_postgres_connection),
        ("Vector Search", test_vector_search)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' failed with error: {str(e)}")
            results.append((name, False))
    
    # Print summary
    print("\n=== Test Summary ===")
    all_passed = True
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Migration appears successful.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 