#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate Embeddings for Supabase Storage

This script:
1. Reads the structured content extracted by extract-structured-content.py
2. Generates embeddings for each content chunk using sentence-transformers
3. Stores the content and embeddings in Supabase with pgvector

Requires:
- sentence-transformers
- supabase-py
- numpy
"""

import os
import sys
import json
import time
import uuid
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
from dotenv import load_dotenv
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

# Configuration
ROOT_DIR = Path(__file__).resolve().parents[2] # ai-education root directory
DATA_DIR = ROOT_DIR / "data-pipeline" / "data"
INPUT_FILE = DATA_DIR / "structured-content.json"
MODEL_NAME = os.getenv('MODEL_NAME', "sentence-transformers/all-MiniLM-L6-v2")  # 384 dimensions
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 32))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 512))  # Approximate max tokens per chunk

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class EmbeddingGenerator:
    def __init__(self, model_name: str = MODEL_NAME):
        """Initialize the embedding generator with specified model."""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded with dimension: {self.embedding_dim}")
        
    def generate_embeddings(self, texts: List[str], batch_size: int = BATCH_SIZE) -> np.ndarray:
        """Generate embeddings for a list of texts in batches."""
        if not texts:
            return np.array([])
            
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            print(f"Generating embeddings for batch {i//batch_size + 1}/{len(texts)//batch_size + 1}")
            batch_embeddings = self.model.encode(batch_texts)
            all_embeddings.append(batch_embeddings)
            
        return np.vstack(all_embeddings)

class SupabaseClient:
    def __init__(self, url: str, key: str):
        """Initialize connection to Supabase."""
        if not url or not key:
            raise ValueError("Missing Supabase URL or key. Set SUPABASE_URL and SUPABASE_KEY in .env file.")
            
        print(f"Connecting to Supabase: {url}")
        self.client: Client = create_client(url, key)
        
    def setup_tables(self):
        """Create tables and extensions if they don't exist."""
        print("Setting up database schema...")
        
        # Create vector extension
        self.client.postgrest.rpc(
            "create_pg_extension", 
            {"name": "vector"}
        ).execute()
        
        # Create tables using SQL (easier than multiple API calls)
        queries = [
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
                embedding VECTOR(384)
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
                query_embedding VECTOR(384),
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
            """
        ]
        
        for query in queries:
            self.client.postgrest.rpc(
                "run_sql", 
                {"query": query}
            ).execute()
            
        print("Database schema setup complete")
        
    def clear_existing_data(self):
        """Clear existing data from tables."""
        print("Clearing existing data...")
        self.client.table("content_links").delete().filter("id", "neq", "00000000-0000-0000-0000-000000000000").execute()
        self.client.table("course_content").delete().filter("id", "neq", "00000000-0000-0000-0000-000000000000").execute()
        print("Existing data cleared")
        
    def store_content_batch(self, content_items: List[Dict[str, Any]]):
        """Store a batch of content items with embeddings."""
        if not content_items:
            return
            
        print(f"Storing batch of {len(content_items)} content items...")
        response = self.client.table("course_content").insert(content_items).execute()
        if hasattr(response, 'error') and response.error:
            print(f"Error storing content: {response.error}")
        return response
        
    def store_links_batch(self, links: List[Dict[str, Any]]):
        """Store a batch of links."""
        if not links:
            return
            
        print(f"Storing batch of {len(links)} links...")
        response = self.client.table("content_links").insert(links).execute()
        if hasattr(response, 'error') and response.error:
            print(f"Error storing links: {response.error}")
        return response

def chunk_text(text: str, max_tokens: int = MAX_TOKENS) -> List[str]:
    """Split text into chunks of approximately max_tokens."""
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

def process_structured_content(input_file: Path, embedding_generator: EmbeddingGenerator, supabase: SupabaseClient, setup_db: bool = False, clear_data: bool = False):
    """Process structured content, generate embeddings, and store in Supabase."""
    # Read input file
    print(f"Reading structured content from {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    pages = data.get("pages", [])
    print(f"Found {len(pages)} pages to process")
    
    # Setup database if needed
    if setup_db:
        supabase.setup_tables()
        
    # Clear existing data if requested
    if clear_data:
        supabase.clear_existing_data()
    
    # Process pages and sections
    content_items = []
    all_links = []
    
    # Maps original section IDs to new UUIDs
    id_map = {}
    section_id_to_content_id = {}
    
    for page in pages:
        page_id = str(uuid.uuid4())
        page_type = page.get("type", "page")
        page_title = page.get("title", "Untitled")
        page_url = page.get("url", "")
        part_id = page.get("part_id")
        module_id = page.get("module_id")
        
        # Process each section
        for section in page.get("sections", []):
            section_id = str(uuid.uuid4())
            section_title = section.get("title", "Untitled Section")
            section_content = section.get("content", "")
            section_type = section.get("type", "section")
            section_url = section.get("url", page_url)
            importance = section.get("importance", 0.7)
            
            # Store mapping from original ID to new UUID
            original_id = section.get("id")
            if original_id:
                id_map[original_id] = section_id
                
            # Chunk the content if needed
            content_chunks = chunk_text(section_content)
            
            # Process links for this section
            links = section.get("links", [])
            for link in links:
                link_id = str(uuid.uuid4())
                all_links.append({
                    "id": link_id,
                    "content_id": section_id,
                    "link_text": link.get("text", ""),
                    "url": link.get("url", ""),
                    "is_internal": link.get("is_internal", False),
                    "is_reference": link.get("is_reference", False)
                })
                
            # Generate embeddings for each chunk
            embeddings = embedding_generator.generate_embeddings(content_chunks)
            
            # Store each chunk as a separate item
            for i, (chunk, embedding) in enumerate(zip(content_chunks, embeddings)):
                chunk_id = section_id if i == 0 else str(uuid.uuid4())
                chunk_title = f"{section_title} (Part {i+1})" if i > 0 else section_title
                
                content_items.append({
                    "id": chunk_id,
                    "title": chunk_title,
                    "content": chunk,
                    "url": section_url,
                    "content_type": section_type,
                    "parent_id": page_id,
                    "part_id": part_id,
                    "module_id": module_id,
                    "importance": importance,
                    "embedding": embedding.tolist()
                })
                
            # Store in batches of 50 to avoid rate limits
            if len(content_items) >= 50:
                supabase.store_content_batch(content_items)
                content_items = []
    
    # Store any remaining content items
    if content_items:
        supabase.store_content_batch(content_items)
        
    # Wait a moment to ensure all content is stored before adding links
    time.sleep(2)
        
    # Store links in batches
    for i in range(0, len(all_links), 100):
        batch = all_links[i:i+100]
        supabase.store_links_batch(batch)
        
    print("Processing complete!")

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings from structured content and store in Supabase")
    parser.add_argument('--input', type=str, default=str(INPUT_FILE), help='Path to structured content JSON file')
    parser.add_argument('--model', type=str, default=MODEL_NAME, help='Sentence transformer model to use')
    parser.add_argument('--setup-db', action='store_true', help='Setup database schema')
    parser.add_argument('--clear-data', action='store_true', help='Clear existing data before import')
    args = parser.parse_args()
    
    # Validate Supabase credentials
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        sys.exit(1)
    
    try:
        # Initialize embedding generator
        embedding_generator = EmbeddingGenerator(model_name=args.model)
        
        # Initialize Supabase client
        supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
        
        # Process content
        process_structured_content(
            Path(args.input), 
            embedding_generator, 
            supabase,
            setup_db=args.setup_db,
            clear_data=args.clear_data
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 