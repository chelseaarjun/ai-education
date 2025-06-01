import requests
import json

# Test data
test_request = {
    "message": "What are large language models?",
    "conversationHistory": [],
    "proficiencyLevel": "Intermediate",
    "conversationSummary": ""
}

# Send the request to our locally running API
response = requests.post("http://localhost:8000/", json=test_request)

# Print the status code
print(f"Status code: {response.status_code}")

# Parse and pretty-print the response
try:
    data = response.json()
    print("\nResponse data:")
    print(json.dumps(data, indent=2))
    
    # Verify the structure of the response
    assert "answer" in data and "text" in data["answer"], "Response is missing 'answer.text'"
    assert "followUpQuestions" in data and isinstance(data["followUpQuestions"], list), "Response is missing 'followUpQuestions' list"
    assert "sources" in data and isinstance(data["sources"], list), "Response is missing 'sources' list"
    
    print("\nResponse structure verification: PASSED")
    
    # Check if we have nested JSON objects (the issue we're trying to fix)
    if isinstance(data["answer"], str):
        print("\nWARNING: 'answer' is a string instead of an object - nesting issue may still exist")
    else:
        print("\nNo JSON nesting issue detected in 'answer' field")
        
except Exception as e:
    print(f"Error processing response: {e}")
    print(f"Raw response: {response.text}") 