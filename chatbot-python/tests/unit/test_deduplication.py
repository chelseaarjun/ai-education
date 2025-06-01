#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Citation Deduplication Tests

This module tests the deduplicate_citations function to ensure it properly
removes duplicate citations and maintains proper ordering and ID assignment.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the API modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from api.chat import deduplicate_citations


class TestDeduplication(unittest.TestCase):
    """Test suite for the citation deduplication function."""

    def test_basic_deduplication(self):
        """Test basic deduplication of identical URLs."""
        # Input with duplicate URLs
        test_input = [
            {
                "id": 1,
                "content": "First content",
                "title": "Title 1",
                "url": "same/url.html",
                "relevance_score": 0.85,
                "section_title": "Section 1"
            },
            {
                "id": 2,
                "content": "Second content",
                "title": "Title 2",
                "url": "same/url.html",  # Duplicate URL
                "relevance_score": 0.75,
                "section_title": "Section 2"
            },
            {
                "id": 3,
                "content": "Third content",
                "title": "Title 3",
                "url": "different/url.html",
                "relevance_score": 0.65,
                "section_title": "Section 3"
            }
        ]
        
        # Run deduplication
        result = deduplicate_citations(test_input)
        
        # Should only have 2 results (duplicate removed)
        self.assertEqual(len(result), 2, "Deduplication failed to remove duplicate URL")
        
        # Check URLs are unique
        urls = [item["url"] for item in result]
        self.assertEqual(len(urls), len(set(urls)), "Output contains duplicate URLs")
        
        # Check sequential IDs
        ids = [item["id"] for item in result]
        self.assertEqual(ids, [1, 2], "IDs were not reassigned sequentially")

    def test_higher_relevance_kept(self):
        """Test that the higher relevance score is kept when duplicates exist."""
        # Input with duplicate URLs but different relevance scores
        test_input = [
            {
                "id": 1,
                "content": "Lower relevance",
                "title": "Title 1",
                "url": "same/url.html",
                "relevance_score": 0.75,
                "section_title": "Section 1"
            },
            {
                "id": 2,
                "content": "Higher relevance",
                "title": "Title 2",
                "url": "same/url.html",  # Duplicate URL
                "relevance_score": 0.85,  # Higher score
                "section_title": "Section 2"
            }
        ]
        
        # Run deduplication
        result = deduplicate_citations(test_input)
        
        # Should only have 1 result
        self.assertEqual(len(result), 1, "Deduplication failed to remove duplicate URL")
        
        # Should keep the higher relevance score
        self.assertEqual(result[0]["relevance_score"], 0.85, 
                         "Deduplication did not keep the item with higher relevance score")
        
        # Should have content from the higher relevance item
        self.assertEqual(result[0]["content"], "Higher relevance", 
                         "Deduplication did not keep the content from higher relevance item")

    def test_sorting_by_relevance(self):
        """Test that results are sorted by relevance after deduplication."""
        test_input = [
            {
                "id": 1,
                "content": "Medium relevance",
                "title": "Title 1",
                "url": "url1.html",
                "relevance_score": 0.75,
                "section_title": "Section 1"
            },
            {
                "id": 2,
                "content": "Lowest relevance",
                "title": "Title 2",
                "url": "url2.html",
                "relevance_score": 0.65,
                "section_title": "Section 2"
            },
            {
                "id": 3,
                "content": "Highest relevance",
                "title": "Title 3",
                "url": "url3.html",
                "relevance_score": 0.85,
                "section_title": "Section 3"
            }
        ]
        
        # Run deduplication
        result = deduplicate_citations(test_input)
        
        # Should still have 3 results (no duplicates)
        self.assertEqual(len(result), 3, "Deduplication incorrectly removed non-duplicate URLs")
        
        # Check sorting by relevance (highest first)
        self.assertEqual(result[0]["relevance_score"], 0.85, "First result should have highest relevance")
        self.assertEqual(result[1]["relevance_score"], 0.75, "Second result should have medium relevance")
        self.assertEqual(result[2]["relevance_score"], 0.65, "Third result should have lowest relevance")
        
        # Check IDs are reassigned in order of relevance
        self.assertEqual(result[0]["id"], 1, "First result should have ID 1")
        self.assertEqual(result[1]["id"], 2, "Second result should have ID 2")
        self.assertEqual(result[2]["id"], 3, "Third result should have ID 3")

    def test_empty_input(self):
        """Test with empty input."""
        result = deduplicate_citations([])
        self.assertEqual(result, [], "Empty input should return empty output")

    def test_anchor_fragments(self):
        """Test that URLs with different anchor fragments are treated as different."""
        test_input = [
            {
                "id": 1,
                "content": "First section",
                "title": "Title 1",
                "url": "page.html#section1",
                "relevance_score": 0.85,
                "section_title": "Section 1"
            },
            {
                "id": 2,
                "content": "Second section",
                "title": "Title 2",
                "url": "page.html#section2",  # Same page, different anchor
                "relevance_score": 0.75,
                "section_title": "Section 2"
            }
        ]
        
        # Run deduplication
        result = deduplicate_citations(test_input)
        
        # Should keep both results since they have different anchors
        self.assertEqual(len(result), 2, 
                         "Deduplication incorrectly removed URLs with different anchors")
        
        # Urls should include both fragments
        urls = sorted([item["url"] for item in result])
        self.assertEqual(urls, ["page.html#section1", "page.html#section2"], 
                         "URLs with different anchors should be treated as unique")


if __name__ == "__main__":
    unittest.main() 