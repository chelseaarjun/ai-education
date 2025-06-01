#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search Functionality Tests

This module tests the search functionality using OpenAI embeddings with Supabase.
It validates embedding generation, similarity search, and result formatting.

Tests:
    - OpenAI embedding generation
    - Supabase vector search
    - Search result formatting and relevance
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

def test_search_functionality():
    """Test search functionality with OpenAI embeddings."""
    print("=== Testing Search Functionality ===")
    
    # Check environment variables
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Missing Supabase configuration. Please check environment variables.")
        return False
    
    # Initialize Supabase client
    print(f"Connecting to Supabase: {SUPABASE_URL}")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return False
    
    # Test queries
    test_queries = [
        "What is a context window in LLMs?",
        "How do agents use tools?",
        "What is tokenization?",
    ]
    
    success = True
    
    # Run searches for each query
    for i, query in enumerate(test_queries):
        print(f"\n\n{'-' * 80}")
        print(f"Test Query {i+1}: '{query}'")
        print(f"{'-' * 80}")
        
        try:
            # Generate embedding
            embedding = generate_embedding(query)
            print(f"✅ Generated embedding with {len(embedding)} dimensions")
            
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
                print(f"❌ Error: {response.error}")
                success = False
                continue
                
            results = response.data
            
            # Print results
            if results:
                print(f"✅ Found {len(results)} results:")
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
                
                # Verify result quality
                if len(results) > 0 and results[0].get('similarity', 0) > 0.6:
                    print(f"✅ Found high-quality match with similarity: {results[0].get('similarity', 0):.4f}")
                else:
                    print("⚠️ No high-quality matches found")
            else:
                print("⚠️ No results found.")
                success = False
        
        except Exception as e:
            print(f"❌ Error: {e}")
            success = False
    
    if success:
        print("\n✅ All search tests completed successfully")
    else:
        print("\n⚠️ Some search tests failed")
    
    return success

if __name__ == "__main__":
    test_search_functionality() 