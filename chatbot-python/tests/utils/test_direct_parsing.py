#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct Response Parsing Tests

This module tests the direct parsing of Claude responses
without making actual API calls. It simulates the response
parsing logic to verify that nested JSON is handled correctly.

Tests:
    - Direct parsing of nested JSON from Claude
    - Adding sources to the response
    - Validating with Pydantic models
"""

import json
from api.chat import Answer, Source, ChatResponse

def test_direct_parsing():
    """Test direct parsing of Claude responses with nested JSON."""
    print("=== Direct Response Parsing Test ===")
    
    # Simulate Claude response with nested JSON
    claude_response = {
        "answer": "{\"text\": \"This is a test response from Claude with nested JSON.\"}",
        "followUpQuestions": ["Question 1?", "Question 2?", "Question 3?"],
        "conversationSummary": "Test conversation about AI education"
    }
    
    print(f"Original response: {claude_response}")
    
    # Step 1: Parse nested JSON in answer field
    if isinstance(claude_response.get("answer"), str):
        try:
            # Try to parse as JSON
            answer_json = json.loads(claude_response["answer"])
            if isinstance(answer_json, dict):
                claude_response["answer"] = answer_json
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON, create an answer object
            claude_response["answer"] = {"text": claude_response["answer"]}
    
    print(f"\nAfter parsing nested JSON: {claude_response}")
    
    # Step 2: Add mock sources
    claude_response["sources"] = [
        {
            "id": 1,
            "title": "Test Source",
            "url": "http://example.com/test",
            "section_title": "Test Section",
            "relevance_score": 0.95
        }
    ]
    
    # Step 3: Validate with Pydantic
    chat_response = ChatResponse(**claude_response)
    
    # Step 4: Convert back to dictionary
    response_dict = chat_response.model_dump()
    print(f"\nFinal response structure:")
    print(json.dumps(response_dict, indent=2))
    
    # Verify
    assert isinstance(response_dict["answer"], dict), "answer should be an object"
    assert "text" in response_dict["answer"], "answer should have a text field"
    assert isinstance(response_dict["followUpQuestions"], list), "followUpQuestions should be a list"
    
    print("\n✅ Validation successful!")
    return True

if __name__ == "__main__":
    test_direct_parsing() 