#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Citation Source Tests

This module tests whether the server is returning actual citations from
Supabase or fallback mock citations. It helps verify that the external
content retrieval system is working properly.

Tests:
    - Detection of mock vs. real citations
    - Citation structure and content
    - URL patterns in citations
    - Deduplication of citations with identical URLs
"""

import unittest
import requests
import json
import re

class TestCitationSources(unittest.TestCase):
    """Test suite for citation source verification."""
    
    BASE_URL = "http://localhost:3000/api/chat/"
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - ensure server is running."""
        try:
            response = requests.get("http://localhost:3000/")
            if response.status_code == 200:
                print("Server is running.")
            else:
                print(f"Unexpected status code: {response.status_code}")
        except requests.RequestException:
            print("WARNING: Server appears to be offline. Tests may fail.")
    
    def test_citation_sources(self):
        """Test if citations are real or mock."""
        test_request = {
            "message": "What are large language models?",
            "conversationHistory": [],
            "proficiencyLevel": "Intermediate",
            "conversationSummary": ""
        }
        
        response = requests.post(self.BASE_URL, json=test_request)
        
        # Check status code
        self.assertEqual(response.status_code, 200, 
                         f"Expected status 200, got {response.status_code}: {response.text}")
        
        # Parse response
        data = response.json()
        
        # Verify citations exist
        self.assertIn("sources", data, "Response is missing 'sources' field")
        self.assertIsInstance(data["sources"], list, "Sources is not a list")
        self.assertGreater(len(data["sources"]), 0, "No sources/citations returned")
        
        # Check if citations are likely mock or real
        is_mock = self.are_citations_mock(data["sources"])
        
        # Print for information (don't fail the test either way)
        if is_mock:
            print("\nℹ️ Server appears to be returning MOCK citations")
        else:
            print("\nℹ️ Server appears to be returning REAL citations from Supabase")
        
        # Validate citation structure regardless of source
        self.validate_citation_structure(data["sources"])
    
    def test_citation_deduplication(self):
        """Test that citations with duplicate URLs are deduplicated."""
        # Use a query likely to return results from the same document/URL
        test_request = {
            "message": "Explain MCP and connections in detail",
            "conversationHistory": [],
            "proficiencyLevel": "Expert",  # Expert to get more results
            "conversationSummary": ""
        }
        
        response = requests.post(self.BASE_URL, json=test_request)
        
        # Check status code
        self.assertEqual(response.status_code, 200, 
                         f"Expected status 200, got {response.status_code}: {response.text}")
        
        # Parse response
        data = response.json()
        
        # Verify citations exist
        self.assertIn("sources", data, "Response is missing 'sources' field")
        self.assertIsInstance(data["sources"], list, "Sources is not a list")
        
        # Check for duplicate URLs
        urls = [source["url"] for source in data["sources"]]
        unique_urls = set(urls)
        
        # Verify no duplicate URLs
        self.assertEqual(len(urls), len(unique_urls), 
                         f"Found duplicate URLs in citations: {urls}")
        
        # Verify sequential IDs (1, 2, 3...)
        ids = [source["id"] for source in data["sources"]]
        expected_ids = list(range(1, len(ids) + 1))
        self.assertEqual(ids, expected_ids, 
                         f"Citation IDs are not sequential: {ids}")
        
        print(f"\nℹ️ Found {len(urls)} unique citations with no duplicates")
    
    def are_citations_mock(self, sources):
        """
        Determine if citations are likely mock data.
        
        This uses several heuristics:
        1. Check for hardcoded URLs in chat.py's fallback data
        2. Check for exactly 2 sources (the fallback count)
        3. Check for specific titles from the fallback data
        """
        # Known fallback/mock patterns
        mock_patterns = [
            r"module[12]/.*\.html",  # Fallback URLs like module1/llms.html
            r"AI Foundations",       # Fallback title 
            r"AI Technical Concepts" # Fallback title
        ]
        
        # Check number of sources
        if len(sources) == 2:  # Fallback returns exactly 2 sources
            mock_score = 1
        else:
            mock_score = 0
        
        # Check content patterns
        for source in sources:
            for pattern in mock_patterns:
                if re.search(pattern, source.get("title", "")) or re.search(pattern, source.get("url", "")):
                    mock_score += 1
        
        # If we have multiple indicators, likely mock data
        return mock_score >= 2
    
    def validate_citation_structure(self, sources):
        """Validate that citation structure is correct regardless of source."""
        for i, source in enumerate(sources):
            # Check required fields
            self.assertIn("id", source, f"Source {i} missing 'id'")
            self.assertIn("title", source, f"Source {i} missing 'title'")
            self.assertIn("url", source, f"Source {i} missing 'url'")
            self.assertIn("section_title", source, f"Source {i} missing 'section_title'")
            self.assertIn("relevance_score", source, f"Source {i} missing 'relevance_score'")
            
            # Check types
            self.assertIsInstance(source["id"], int, f"Source {i} 'id' is not an integer")
            self.assertIsInstance(source["title"], str, f"Source {i} 'title' is not a string")
            self.assertIsInstance(source["url"], str, f"Source {i} 'url' is not a string")
            self.assertIsInstance(source["relevance_score"], (int, float), 
                                 f"Source {i} 'relevance_score' is not a number")
            
            # Check value ranges
            self.assertGreaterEqual(source["relevance_score"], 0, 
                                   f"Source {i} has negative relevance score")
            self.assertLessEqual(source["relevance_score"], 1, 
                                f"Source {i} has relevance score > 1")

if __name__ == '__main__':
    unittest.main() 