#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Integration Tests for Chat API

This module contains integration tests for the chat API endpoint,
testing the full request-response cycle including server communication,
response structure validation, and checking for JSON nesting issues.

These tests require the server to be running.
Server can be started with: python server.py

Tests:
    - Basic API response validation
    - JSON structure and data type verification
    - Handling of nested JSON in responses
    - Different proficiency levels
"""

import unittest
import requests
import json
import time
import os

class TestChatAPI(unittest.TestCase):
    """Integration test suite for the Chat API."""
    
    BASE_URL = "http://localhost:3000/api/chat/"
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - ensure server is running."""
        # Check if server is available
        max_retries = 1
        for i in range(max_retries):
            try:
                response = requests.get("http://localhost:3000/")
                if response.status_code == 200:
                    print("Server is running.")
                    break
                else:
                    print(f"Unexpected status code: {response.status_code}")
            except requests.RequestException:
                if i < max_retries - 1:
                    print("Server not available, waiting...")
                    time.sleep(2)
                else:
                    print("WARNING: Server appears to be offline. Tests may fail.")
    
    def test_basic_response(self):
        """Test basic API response with default parameters."""
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
        
        # Verify structure
        self.assertIn("answer", data, "Response is missing 'answer' field")
        self.assertIn("text", data["answer"], "Response is missing 'answer.text' field")
        self.assertIn("followUpQuestions", data, "Response is missing 'followUpQuestions' field")
        self.assertIsInstance(data["followUpQuestions"], list, 
                             "'followUpQuestions' is not a list")
        self.assertIn("sources", data, "Response is missing 'sources' field")
        self.assertIsInstance(data["sources"], list, "'sources' is not a list")
        
        # Check for JSON nesting issue
        self.assertIsInstance(data["answer"], dict, 
                             "'answer' is a string instead of an object - nesting issue detected")
    
    def test_different_proficiency_levels(self):
        """Test API responses with different proficiency levels."""
        proficiency_levels = ["Beginner", "Intermediate", "Expert"]
        
        for level in proficiency_levels:
            with self.subTest(proficiency_level=level):
                test_request = {
                    "message": "What is prompt engineering?",
                    "conversationHistory": [],
                    "proficiencyLevel": level,
                    "conversationSummary": ""
                }
                
                response = requests.post(self.BASE_URL, json=test_request)
                
                # Check status code
                self.assertEqual(response.status_code, 200)
                
                # Parse response
                data = response.json()
                
                # Verify structure
                self.assertIn("answer", data)
                self.assertIn("text", data["answer"])
                self.assertIn("followUpQuestions", data)
    
    def test_conversation_history(self):
        """Test API response with conversation history."""
        test_request = {
            "message": "Can you elaborate on that?",
            "conversationHistory": [
                {
                    "role": "user",
                    "content": "What are large language models?"
                },
                {
                    "role": "assistant", 
                    "content": "Large Language Models (LLMs) are sophisticated AI systems trained on vast amounts of text data."
                }
            ],
            "proficiencyLevel": "Intermediate",
            "conversationSummary": "Discussing what large language models are."
        }
        
        response = requests.post(self.BASE_URL, json=test_request)
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Parse response
        data = response.json()
        
        # Verify structure
        self.assertIn("answer", data)
        self.assertIn("text", data["answer"])
        self.assertIn("conversationSummary", data)
        self.assertIsInstance(data["conversationSummary"], str)

if __name__ == '__main__':
    unittest.main() 