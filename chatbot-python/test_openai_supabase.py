#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test OpenAI Embeddings with Supabase Search

This script tests the search functionality using OpenAI embeddings in the chatbot.
"""

import os
from dotenv import load_dotenv
from api.search import generate_embedding
from supabase import create_client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def main():
    """Test search functionality with OpenAI embeddings."""
    print("Testing search with OpenAI embeddings...")
    
    # Initialize Supabase client
    print(f"Connecting to Supabase: {SUPABASE_URL}")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Test queries
    test_queries = [
        "What is a context window in LLMs?",
        "How do agents use tools?",
        "What is tokenization?",
        "How do I build an AI application?",
        "Explain embedding dimensions"
    ]
    
    # Run searches for each query
    for i, query in enumerate(test_queries):
        print(f"\n\n{'-' * 80}")
        print(f"Test Query {i+1}: '{query}'")
        print(f"{'-' * 80}")
        
        # Generate embedding
        embedding = generate_embedding(query)
        print(f"Generated embedding with {len(embedding)} dimensions")
        
        # Search in Supabase
        response = supabase.rpc(
            'match_course_content',
            {
                'query_embedding': embedding,
                'match_threshold': 0.5,
                'match_count': 3
            }
        ).execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"Error: {response.error}")
            continue
            
        results = response.data
        
        # Print results
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

if __name__ == "__main__":
    main() 