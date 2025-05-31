#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test OpenAI Embeddings with Supabase Search

This script tests the semantic search functionality using OpenAI embeddings
and the Supabase pgvector extension.
"""

import os
import sys
from typing import List, Dict, Any

import openai
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', "text-embedding-3-small")

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SemanticSearch:
    def __init__(self):
        """Initialize the semantic search client."""
        # Set up OpenAI
        if not OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in .env file.")
        openai.api_key = OPENAI_API_KEY
        
        # Set up Supabase
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Missing Supabase URL or key. Set SUPABASE_URL and SUPABASE_KEY in .env file.")
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print(f"Using OpenAI model: {EMBEDDING_MODEL}")
        print(f"Connected to Supabase: {SUPABASE_URL}")
        
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for a single text string using OpenAI API."""
        response = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    
    def search(self, query: str, threshold: float = 0.5, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for content similar to the query."""
        # Generate embeddings for the query
        query_embedding = self.generate_embedding(query)
        
        # Call the match_course_content function in Supabase
        response = self.supabase.rpc(
            "match_course_content",
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": limit
            }
        ).execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"Error in search: {response.error}")
            return []
        
        return response.data

def main():
    """Main function to test semantic search."""
    try:
        searcher = SemanticSearch()
        
        # List of test queries
        test_queries = [
            "What is a context window in LLMs?",
            "How do agents use tools?",
            "What is tokenization?",
            "How do I build an AI application?",
            "Explain embedding dimensions",
            "What is CRISP Prompts?",
            "What is agentic AI?",
            "What is an LLM Workflow?",
            "What is an Agentic LLM Workflow?",
            "What is an LLM Workflow?",
        ]
        
        # Run searches for each query
        for i, query in enumerate(test_queries):
            print(f"\n\n{'-' * 80}")
            print(f"Test Query {i+1}: '{query}'")
            print(f"{'-' * 80}")
            
            results = searcher.search(query, threshold=0.5, limit=3)
            
            if results:
                print(f"Found {len(results)} results:")
                for j, result in enumerate(results):
                    similarity = result.get('similarity', 0)
                    title = result.get('title', 'Untitled')
                    url = result.get('url', '')
                    
                    print(f"\n{j+1}. {title} ({similarity:.4f})")
                    print(f"   URL: {url}")
                    
                    # Show a snippet of the content
                    content = result.get('content', '')
                    if content:
                        snippet = content[:200] + "..." if len(content) > 200 else content
                        print(f"   Snippet: {snippet}")
            else:
                print("No results found.")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 