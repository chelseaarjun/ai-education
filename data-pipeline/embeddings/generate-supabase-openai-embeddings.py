#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate OpenAI Embeddings for Supabase Storage

This script:
1. Reads the structured content extracted by extract-structured-content.py
2. Generates embeddings for each content chunk using OpenAI's embeddings API
3. Stores the content and embeddings in Supabase with pgvector

Requires:
- openai
- supabase-py
- tenacity (for retries)
"""

import os
import sys
import json
import time
import uuid
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

import openai
from dotenv import load_dotenv
from supabase import create_client, Client
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables from .env file
load_dotenv()

# Configuration
ROOT_DIR = Path(__file__).resolve().parents[2] # ai-education root directory
DATA_DIR = ROOT_DIR / "data-pipeline" / "data"
INPUT_FILE = DATA_DIR / "structured-content.json"
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', "text-embedding-3-small")  # Updated default to newer model
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 20))  # OpenAI recommends batches of 20
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 8191))  # OpenAI token limit for embeddings

# Set a higher token limit for text-embedding-3-large model if used
if EMBEDDING_MODEL == "text-embedding-3-large":
    MAX_TOKENS = 8191  # Maximum for text-embedding-3-large
elif EMBEDDING_MODEL == "text-embedding-3-small":
    MAX_TOKENS = 8191  # Maximum for text-embedding-3-small
elif EMBEDDING_MODEL == "text-embedding-ada-002":
    MAX_TOKENS = 8191  # Maximum for text-embedding-ada-002

print(f"Using maximum token limit of {MAX_TOKENS} for model {EMBEDDING_MODEL}")

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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
        elif "text-embedding-3" in model_name:
            self.embedding_dim = 1536  # text-embedding-3-small/large both use 1536
        else:
            # Default to 1536 dimensions
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
            # Course content table with vector support (updated for 1536 dimensions)
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
                embedding VECTOR(1536)
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
            
            # Function for similarity search (updated for 1536 dimensions)
            """
            CREATE OR REPLACE FUNCTION match_course_content(
                query_embedding VECTOR(1536),
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
    """
    Use entire sections as chunks, only splitting if they exceed max_tokens.
    This preserves the semantic coherence of sections.
    """
    # Simple approximation: ~4 chars per token for English text
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    
    # If text is short enough, return as is
    if len(text) <= max_chars:
        return [text]
    
    # For longer sections, we need to split but we'll try to do it intelligently
    # Look for natural breakpoints like headers, bullet points, or paragraph breaks
    
    # First try splitting by headers (indicated by numbers followed by period and space)
    header_pattern = r'(\d+\.\s+[A-Z][^\.]+\.)'
    header_splits = re.split(header_pattern, text)
    
    if len(header_splits) > 1:
        # We found headers to split on
        chunks = []
        current_chunk = ""
        current_length = 0
        
        for i in range(len(header_splits)):
            segment = header_splits[i]
            segment_length = len(segment)
            
            # If adding this segment would exceed max_chars, start a new chunk
            if current_length + segment_length > max_chars and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = segment
                current_length = segment_length
            else:
                current_chunk += segment
                current_length += segment_length
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    # If no headers found, try paragraph breaks
    paragraphs = text.split('\n\n')
    if len(paragraphs) > 1:
        chunks = []
        current_chunk = ""
        current_length = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            paragraph_length = len(paragraph)
            
            # If adding this paragraph exceeds max_chars, start a new chunk
            if current_length + paragraph_length > max_chars and current_chunk:
                chunks.append(current_chunk)
                current_chunk = paragraph
                current_length = paragraph_length
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                current_length += paragraph_length
                
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
    
    # If no natural breaks found, fall back to sentence-based chunking
    # but with larger chunks and more overlap
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Use a 20% overlap between chunks
    overlap_chars = int(max_chars * 0.2)
    overlap_sentences = []
    
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
            # Add the current chunk with any overlap sentences from previous chunk
            chunks.append(' '.join(current_chunk))
            
            # Start new chunk with overlap from previous chunk (for context continuity)
            overlap_length = 0
            for s in reversed(current_chunk):
                if overlap_length + len(s) <= overlap_chars:
                    overlap_sentences.insert(0, s)
                    overlap_length += len(s)
                else:
                    break
            
            # New chunk starts with overlap sentences plus current sentence
            current_chunk = overlap_sentences + [sentence]
            current_length = sum(len(s) for s in current_chunk)
            overlap_sentences = []
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
            
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

def process_structured_content(input_file: Path, embedding_generator: OpenAIEmbeddingGenerator, supabase: SupabaseClient, setup_db: bool = False, clear_data: bool = False):
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
    content_links = []
    all_texts = []
    id_to_index_map = {}
    
    print("Using section-level chunking strategy for improved context retention")
    
    # First pass: collect all sections for embedding generation
    for page in pages:
        page_id = page.get("id", str(uuid.uuid4()))
        sections = page.get("sections", [])
        
        print(f"Processing page: {page.get('title', 'Untitled')} with {len(sections)} sections")
        
        for section in sections:
            section_content = section.get("content", "")
            section_id = section.get("id", str(uuid.uuid4()))
            
            if not section_content:
                print(f"  Skipping empty section: {section.get('title', 'Untitled')}")
                continue
            
            print(f"  Processing section: {section.get('title', 'Untitled')} ({len(section_content)} chars)")
            
            # Try to keep each section as a single chunk if possible
            # Only split if it exceeds the token limit
            chunks = chunk_text(section_content)
            print(f"    Split into {len(chunks)} chunks")
            
            # Create a parent item for the first chunk to maintain the section relationship
            parent_chunk_id = str(uuid.uuid4())
            
            for i, chunk in enumerate(chunks):
                # Generate a unique ID for this chunk
                chunk_id = parent_chunk_id if i == 0 else str(uuid.uuid4())
                
                # Store the text and its index
                all_texts.append(chunk)
                id_to_index_map[chunk_id] = len(all_texts) - 1
                
                # Prepare content item (without embedding for now)
                content_items.append({
                    "id": chunk_id,
                    "title": section.get("title", "") + (f" (part {i+1})" if len(chunks) > 1 and i > 0 else ""),
                    "content": chunk,
                    "url": section.get("url", ""),
                    "content_type": section.get("type", ""),
                    "part_id": page.get("part_id", ""),
                    "module_id": page.get("module_id", ""),
                    # Only set parent_id for continuation chunks, not the first chunk
                    "parent_id": parent_chunk_id if i > 0 else None,  
                    "importance": section.get("importance", 0.7) * (1.0 if i == 0 else 0.9)  # Slightly lower importance for continuation chunks
                })
                
                # Process links if available - only attach to the primary chunk
                if i == 0:  # Only add links to the first chunk of a section
                    links = section.get("links", [])
                    for link in links:
                        link_id = str(uuid.uuid4())
                        content_links.append({
                            "id": link_id,
                            "content_id": chunk_id,
                            "link_text": link.get("text", ""),
                            "url": link.get("url", ""),
                            "is_internal": link.get("is_internal", False),
                            "is_reference": link.get("is_reference", False)
                        })
    
    print(f"Collected {len(all_texts)} text chunks for embedding")
    print(f"  Average chunk size: {sum(len(text) for text in all_texts) / len(all_texts):.1f} chars")
    
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
    
    # Store content in batches (Supabase has insertion limits)
    batch_size = 50  # Smaller batch size for Supabase
    for i in range(0, len(content_items), batch_size):
        batch = content_items[i:i+batch_size]
        supabase.store_content_batch(batch)
    
    # Store links in batches
    for i in range(0, len(content_links), batch_size):
        batch = content_links[i:i+batch_size]
        supabase.store_links_batch(batch)
    
    print(f"Processing complete. Stored {len(content_items)} content items and {len(content_links)} links.")

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="Generate OpenAI embeddings and store in Supabase")
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
        supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
        
        # Process content
        process_structured_content(
            input_file=input_file,
            embedding_generator=embedding_generator,
            supabase=supabase,
            setup_db=args.setup_db,
            clear_data=args.clear_data
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    main() 