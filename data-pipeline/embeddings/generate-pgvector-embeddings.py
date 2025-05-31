#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate Embeddings for PostgreSQL with pgvector

This script:
1. Reads the structured content extracted by extract-structured-content.py
2. Generates embeddings for each content chunk using OpenAI's embeddings API
3. Stores the content and embeddings in PostgreSQL with pgvector

Requires:
- openai
- psycopg
- tenacity (for retries)
"""

import os
import sys
import json
import time
import uuid
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

import openai
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
ROOT_DIR = Path(__file__).resolve().parents[2] # ai-education root directory
DATA_DIR = ROOT_DIR / "data-pipeline" / "data"
INPUT_FILE = DATA_DIR / "structured-content.json"
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', "text-embedding-ada-002")  # OpenAI model (1536 dimensions)
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 20))  # OpenAI recommends batches of 20
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 8191))  # OpenAI token limit for embeddings

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# PostgreSQL configuration
DATABASE_URL = os.getenv("DATABASE_URL")

class OpenAIEmbeddingGenerator:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """Initialize the OpenAI embedding generator."""
        if not OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env file.")
            
        openai.api_key = OPENAI_API_KEY
        self.model = model_name
        print(f"Using OpenAI embedding model: {model_name}")
        
        # For OpenAI models, set dimension based on model
        if model_name == "text-embedding-ada-002":
            self.embedding_dim = 1536
        else:
            # Default to Ada dimensions, may need adjustment for other models
            self.embedding_dim = 1536
            
        print(f"Embedding dimension: {self.embedding_dim}")
        
    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def generate_embeddings(self, texts: List[str], batch_size: int = BATCH_SIZE) -> List[List[float]]:
        """Generate embeddings for a list of texts in batches with retries."""
        if not texts:
            return []
            
        all_embeddings = []
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            print(f"Generating embeddings for batch {i//batch_size + 1}/{total_batches}")
            
            try:
                response = openai.embeddings.create(
                    model=self.model,
                    input=batch_texts
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
                
                # Sleep briefly to avoid rate limits
                if i + batch_size < len(texts):
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error generating embeddings: {str(e)}")
                raise
                
        return all_embeddings

class PostgresVectorClient:
    def __init__(self, db_url: str):
        """Initialize connection to PostgreSQL."""
        if not db_url:
            raise ValueError("Missing PostgreSQL URL. Set DATABASE_URL in .env file.")
            
        print(f"Connecting to PostgreSQL database")
        self.pool = ConnectionPool(db_url, min_size=1, max_size=5)
        self.test_connection()
        
    def test_connection(self):
        """Test database connection and print version."""
        with self.pool.connection() as conn:
            result = conn.execute("SELECT version();").fetchone()
            print(f"Connected to PostgreSQL: {result[0]}")
        
    def setup_tables(self):
        """Create tables and extensions if they don't exist."""
        print("Setting up database schema...")
        
        queries = [
            # Enable vector extension
            "CREATE EXTENSION IF NOT EXISTS vector;",
            
            # Course content table with vector support
            """
            CREATE TABLE IF NOT EXISTS course_content (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                url TEXT,
                content_type TEXT,
                part_id TEXT,
                module_id TEXT,
                parent_id UUID,
                importance REAL DEFAULT 0.7,
                embedding vector(1536)
            );
            """,
            
            # Links table
            """
            CREATE TABLE IF NOT EXISTS content_links (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
                link_text TEXT,
                url TEXT NOT NULL,
                is_internal BOOLEAN DEFAULT FALSE,
                is_reference BOOLEAN DEFAULT FALSE
            );
            """,
            
            # Function for similarity search
            """
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
            """,
            
            # Create vector search index
            """
            CREATE INDEX IF NOT EXISTS course_content_embedding_idx 
            ON course_content 
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
            """
        ]
        
        with self.pool.connection() as conn:
            for query in queries:
                conn.execute(query)
            conn.commit()
            
        print("Database schema setup complete")
        
    def clear_existing_data(self):
        """Clear existing data from tables."""
        print("Clearing existing data...")
        
        with self.pool.connection() as conn:
            conn.execute("DELETE FROM content_links;")
            conn.execute("DELETE FROM course_content;")
            conn.commit()
            
        print("Existing data cleared")
        
    def store_content_batch(self, content_items: List[Dict[str, Any]]):
        """Store a batch of content items with embeddings."""
        if not content_items:
            return
            
        print(f"Storing batch of {len(content_items)} content items...")
        
        # Prepare values for insertion
        values = []
        for item in content_items:
            # Create values tuple for each item
            values.append((
                str(item.get('id', uuid.uuid4())),
                item.get('title', ''),
                item.get('content', ''),
                item.get('url', ''),
                item.get('type', ''),
                item.get('part_id', None),
                item.get('module_id', None),
                item.get('parent_id', None),
                float(item.get('importance', 0.7)),
                item.get('embedding', [])
            ))
        
        # Insert into database
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                # Use execute_values for efficient batch insertion
                psycopg.extras.execute_values(
                    cur,
                    """
                    INSERT INTO course_content 
                    (id, title, content, url, content_type, part_id, module_id, parent_id, importance, embedding)
                    VALUES %s
                    RETURNING id
                    """,
                    values
                )
                conn.commit()
        
    def store_links_batch(self, links: List[Dict[str, Any]]):
        """Store a batch of links."""
        if not links:
            return
            
        print(f"Storing batch of {len(links)} links...")
        
        # Prepare values for insertion
        values = []
        for link in links:
            # Create values tuple for each link
            values.append((
                str(link.get('id', uuid.uuid4())),
                link.get('content_id', None),
                link.get('text', ''),
                link.get('url', ''),
                link.get('is_internal', False),
                link.get('is_reference', False)
            ))
        
        # Insert into database
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                # Use execute_values for efficient batch insertion
                psycopg.extras.execute_values(
                    cur,
                    """
                    INSERT INTO content_links 
                    (id, content_id, link_text, url, is_internal, is_reference)
                    VALUES %s
                    """,
                    values
                )
                conn.commit()

def chunk_text(text: str, max_tokens: int = MAX_TOKENS) -> List[str]:
    """Split text into chunks of approximately max_tokens.
    
    Note: This is a simplified approximation. For production use, 
    consider using tiktoken for accurate token counting.
    """
    # Simple approximation: ~4 chars per token for English text
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    
    # If text is short enough, return as is
    if len(text) <= max_chars:
        return [text]
        
    # Split into sentences and combine into chunks
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Add period back if it was removed during split
        if not sentence.endswith('.'):
            sentence += '.'
            
        sentence_length = len(sentence)
        
        # If adding this sentence exceeds max_chars, start a new chunk
        if current_length + sentence_length > max_chars and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
            
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

def process_structured_content(input_file: Path, embedding_generator: OpenAIEmbeddingGenerator, 
                              db_client: PostgresVectorClient, setup_db: bool = False, 
                              clear_data: bool = False):
    """Process structured content, generate embeddings, and store in PostgreSQL."""
    # Read input file
    print(f"Reading structured content from {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    pages = data.get("pages", [])
    print(f"Found {len(pages)} pages to process")
    
    # Setup database if needed
    if setup_db:
        db_client.setup_tables()
        
    # Clear existing data if requested
    if clear_data:
        db_client.clear_existing_data()
    
    # Process pages and sections
    content_items = []
    content_links = []
    all_texts = []
    id_to_index_map = {}
    
    # First pass: collect all texts for embedding generation
    for page in pages:
        page_id = page.get("id", str(uuid.uuid4()))
        sections = page.get("sections", [])
        
        for section in sections:
            section_content = section.get("content", "")
            if not section_content:
                continue
                
            # Chunk content if needed
            chunks = chunk_text(section_content)
            
            for i, chunk in enumerate(chunks):
                # Generate a unique ID for this chunk
                chunk_id = str(uuid.uuid4())
                
                # Store the text and its index
                all_texts.append(chunk)
                id_to_index_map[chunk_id] = len(all_texts) - 1
                
                # Prepare content item (without embedding for now)
                content_items.append({
                    "id": chunk_id,
                    "title": section.get("title", ""),
                    "content": chunk,
                    "url": section.get("url", ""),
                    "type": section.get("type", ""),
                    "part_id": page.get("part_id", ""),
                    "module_id": page.get("module_id", ""),
                    "parent_id": page_id if i > 0 else None,  # Link chunks to parent page
                    "importance": section.get("importance", 0.7)
                })
                
                # Process links if available
                links = section.get("links", [])
                for link in links:
                    link_id = str(uuid.uuid4())
                    content_links.append({
                        "id": link_id,
                        "content_id": chunk_id,
                        "text": link.get("text", ""),
                        "url": link.get("url", ""),
                        "is_internal": link.get("is_internal", False),
                        "is_reference": link.get("is_reference", False)
                    })
    
    print(f"Collected {len(all_texts)} text chunks for embedding")
    
    # Generate embeddings for all texts
    embeddings = embedding_generator.generate_embeddings(all_texts)
    print(f"Generated {len(embeddings)} embeddings")
    
    # Add embeddings to content items
    for item in content_items:
        item_id = item["id"]
        if item_id in id_to_index_map:
            index = id_to_index_map[item_id]
            if index < len(embeddings):
                item["embedding"] = embeddings[index]
    
    # Store content in batches
    batch_size = 100  # Adjust based on your database performance
    for i in range(0, len(content_items), batch_size):
        batch = content_items[i:i+batch_size]
        db_client.store_content_batch(batch)
    
    # Store links in batches
    for i in range(0, len(content_links), batch_size):
        batch = content_links[i:i+batch_size]
        db_client.store_links_batch(batch)
    
    print(f"Processing complete. Stored {len(content_items)} content items and {len(content_links)} links.")

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="Generate OpenAI embeddings and store in PostgreSQL with pgvector")
    parser.add_argument("--input", "-i", type=str, default=str(INPUT_FILE),
                        help=f"Input JSON file (default: {INPUT_FILE})")
    parser.add_argument("--setup-db", action="store_true",
                        help="Set up database schema")
    parser.add_argument("--clear-data", action="store_true",
                        help="Clear existing data before processing")
    args = parser.parse_args()
    
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    # Initialize embedding generator and database client
    try:
        embedding_generator = OpenAIEmbeddingGenerator()
        db_client = PostgresVectorClient(DATABASE_URL)
        
        # Process content
        process_structured_content(
            input_file=input_file,
            embedding_generator=embedding_generator,
            db_client=db_client,
            setup_db=args.setup_db,
            clear_data=args.clear_data
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    main() 