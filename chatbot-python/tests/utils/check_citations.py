#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Citation Check Utility

A simple utility script to check if the AI Education chatbot is
returning mock citations or real citations from Supabase.

This can be run directly as a script:
    python -m tests.utils.check_citations [port]

or imported and used programmatically.

Usage:
    python -m tests.utils.check_citations [port]

Arguments:
    port - Optional port number (default: 3000)
"""

import sys
import requests
import re
import json

def check_citations(port=3000):
    """Check if the server is returning mock or real citations."""
    base_url = f"http://localhost:{port}/api/chat/"
    
    print(f"Testing server at {base_url}...")
    
    # First check if server is running
    try:
        requests.get(f"http://localhost:{port}/")
    except requests.RequestException:
        print("❌ ERROR: Server not running or not accessible")
        return False
    
    # Make a request to the API
    test_request = {
        "message": "What are large language models?",
        "conversationHistory": [],
        "proficiencyLevel": "Intermediate",
        "conversationSummary": ""
    }
    
    try:
        response = requests.post(base_url, json=test_request, timeout=30)
    except requests.RequestException as e:
        print(f"❌ ERROR: Failed to get response from server: {e}")
        return False
    
    if response.status_code != 200:
        print(f"❌ ERROR: Server returned status code {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Parse response
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("❌ ERROR: Response is not valid JSON")
        print(f"Response: {response.text}")
        return False
    
    # Check for sources
    if "sources" not in data or not isinstance(data["sources"], list):
        print("❌ ERROR: Response does not contain sources")
        return False
    
    sources = data["sources"]
    if not sources:
        print("❌ ERROR: Response contains empty sources list")
        return False
    
    # Check if sources are mock or real
    mock_patterns = [
        r"module[12]/.*\.html",  # Fallback URLs like module1/llms.html
        r"AI Foundations",       # Fallback title 
        r"AI Technical Concepts" # Fallback title
    ]
    
    # Check number of sources (fallback gives exactly 2)
    mock_score = 1 if len(sources) == 2 else 0
    
    # Check content patterns
    for source in sources:
        for pattern in mock_patterns:
            if re.search(pattern, source.get("title", "")) or re.search(pattern, source.get("url", "")):
                mock_score += 1
    
    # Display results
    print("\nResults:")
    print(f"- Number of citations: {len(sources)}")
    
    for i, source in enumerate(sources):
        print(f"\nCitation {i+1}:")
        print(f"  Title: {source.get('title', 'N/A')}")
        print(f"  URL: {source.get('url', 'N/A')}")
        print(f"  Relevance: {source.get('relevance_score', 'N/A')}")
    
    print("\nAnalysis:")
    if mock_score >= 2:
        print("❗ MOCK CITATIONS DETECTED")
        print("The server appears to be returning fallback/mock citations.")
        print("Possible causes:")
        print("- Supabase connection error")
        print("- Missing or invalid API keys")
        print("- Empty vector database")
        return {"is_mock": True, "sources": sources, "mock_score": mock_score}
    else:
        print("✅ REAL CITATIONS DETECTED")
        print("The server appears to be returning real citations from Supabase.")
        return {"is_mock": False, "sources": sources, "mock_score": mock_score}

def main():
    """Run the citation check as a script."""
    # Get port from command line if provided
    port = 3000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    if not check_citations(port):
        sys.exit(1)

if __name__ == "__main__":
    main() 