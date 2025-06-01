#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit Tests for Pydantic Models

This module contains unit tests for the Pydantic models used in the chat API,
focusing on validating the JSON response structure and handling nested JSON.

Tests:
    - Parsing nested JSON strings in the answer field
    - Handling plain text strings in the answer field
    - Processing already structured answer objects
    - Handling doubly nested JSON (edge case)
    - Validation of required fields and data types
"""

import unittest
import json
from api.chat import Answer, Source, ChatResponse

class TestPydanticModels(unittest.TestCase):
    """Test suite for Pydantic models used in the chat API."""
    
    def test_nested_json_string(self):
        """Test handling of nested JSON strings in the answer field."""
        nested_json_response = {
            "answer": "{\"text\": \"This is a test answer with nested JSON.\"}",
            "followUpQuestions": ["Question 1?", "Question 2?"],
            "conversationSummary": "Test conversation",
            "sources": [{"id": 1, "title": "Test", "url": "test.html", 
                        "section_title": "Test Section", "relevance_score": 0.9}]
        }
        
        # Test parsing
        chat_response = ChatResponse(**nested_json_response)
        
        # Verify structure
        self.assertEqual(chat_response.answer.text, "This is a test answer with nested JSON.")
        self.assertIsInstance(chat_response.model_dump()['answer'], dict)
        self.assertIn('text', chat_response.model_dump()['answer'])
    
    def test_plain_string(self):
        """Test handling of plain text strings in the answer field."""
        string_response = {
            "answer": "This is a plain text answer",
            "followUpQuestions": ["Question 1?", "Question 2?"],
            "conversationSummary": "Test conversation",
            "sources": [{"id": 1, "title": "Test", "url": "test.html", 
                        "section_title": "Test Section", "relevance_score": 0.9}]
        }
        
        # Test parsing
        chat_response = ChatResponse(**string_response)
        
        # Verify structure
        self.assertEqual(chat_response.answer.text, "This is a plain text answer")
        self.assertIsInstance(chat_response.model_dump()['answer'], dict)
        self.assertIn('text', chat_response.model_dump()['answer'])
    
    def test_structured_answer(self):
        """Test handling of already structured answer objects."""
        structured_response = {
            "answer": {"text": "This is a pre-structured answer object"},
            "followUpQuestions": ["Question 1?", "Question 2?"],
            "conversationSummary": "Test conversation",
            "sources": [{"id": 1, "title": "Test", "url": "test.html", 
                        "section_title": "Test Section", "relevance_score": 0.9}]
        }
        
        # Test parsing
        chat_response = ChatResponse(**structured_response)
        
        # Verify structure
        self.assertEqual(chat_response.answer.text, "This is a pre-structured answer object")
        self.assertIsInstance(chat_response.model_dump()['answer'], dict)
        self.assertIn('text', chat_response.model_dump()['answer'])
    
    def test_doubly_nested_json(self):
        """Test handling of doubly nested JSON (edge case)."""
        doubly_nested_response = {
            "answer": "{\"text\": \"{\\\"content\\\": \\\"Doubly nested content\\\"}\"}",
            "followUpQuestions": ["Question 1?"],
            "conversationSummary": "Test conversation"
        }
        
        # Test parsing
        chat_response = ChatResponse(**doubly_nested_response)
        
        # The model should extract just the first level of nesting
        self.assertIsInstance(chat_response.model_dump()['answer'], dict)
        self.assertIn('text', chat_response.model_dump()['answer'])
        # Note: Depending on the implementation, this might contain the inner JSON string
        # or it might be further parsed - adjust the assertion as needed
    
    def test_validation_errors(self):
        """Test validation of required fields and data types."""
        # Missing required field
        with self.assertRaises(Exception):
            ChatResponse(followUpQuestions=["Question?"])
        
        # Invalid data type for followUpQuestions
        with self.assertRaises(Exception):
            ChatResponse(answer={"text": "Test"}, followUpQuestions="Not a list")
        
        # Invalid source structure
        with self.assertRaises(Exception):
            ChatResponse(
                answer={"text": "Test"}, 
                followUpQuestions=["Question?"],
                sources=[{"missing_required_fields": True}]
            )

if __name__ == '__main__':
    unittest.main() 