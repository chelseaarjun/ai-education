# Testing Strategy for AI Education Chatbot

## Testing Philosophy: **Practical & Lightweight**

Given budget constraints and project scope, we focus on **high-impact, low-effort testing** that catches critical bugs without over-engineering.

## Testing Levels

### 1. Integration Testing (Priority: HIGH)
**What to test:**
- API endpoints respond correctly
- Claude integration works
- Rate limiting functions
- Cache operations
- Content search accuracy

**Cursor Prompt for Test Creation:**
```
Create integration tests for the chatbot API using Jest that cover:
- POST /api/chat with valid course questions
- Rate limiting (6th request should fail)
- Non-course questions get rejected
- Response includes follow-up questions
- Caching works for identical questions
- Error handling for Claude API failures

Include test data with sample course questions and expected responses.
```

### 2. Manual Testing (Priority: HIGH)
**Testing Checklist:**
- [ ] Chat widget loads on all pages
- [ ] Questions about LLMs get accurate responses
- [ ] Questions about prompt engineering work
- [ ] Non-course questions get rejection message
- [ ] Follow-up questions are relevant
- [ ] Mobile/desktop responsiveness
- [ ] Error states display properly

### 3. Load Testing (Priority: MEDIUM)
**Simple approach:**
- Test with 10-20 concurrent requests
- Verify rate limiting works under load
- Check response times stay under 2 seconds

**Cursor Prompt:**
```
Create a simple load testing script that:
- Sends 20 concurrent requests to /api/chat
- Measures response times
- Verifies rate limiting kicks in
- Reports success/failure rates
- Uses realistic course-related questions
```

### 4. Unit Testing (Priority: LOW)
**Minimal unit tests for:**
- Embedding search function
- Content filtering logic
- Response formatting

## Test Structure

```
tests/
├── integration/
│   ├── api.test.js           # API endpoint tests
│   └── chat-flow.test.js     # End-to-end chat tests
├── manual/
│   ├── checklist.md          # Manual testing checklist
│   └── test-questions.md     # Sample questions for testing
├── load/
│   └── simple-load.js        # Basic load testing
└── utils/
    ├── test-data.js          # Sample questions and responses
    └── mock-responses.js     # Mock Claude responses
```

## Test Data

### Sample Course Questions (for testing)
```javascript
const courseQuestions = [
  "What is a large language model?",
  "How does prompt engineering work?",
  "What are AI agents?",
  "Explain the Model Context Protocol",
  "What is temperature in LLMs?",
  "How do I write better prompts?",
  "What tools work with AWS Bedrock?"
];

const nonCourseQuestions = [
  "What's the weather today?",
  "How do I cook pasta?",
  "Tell me a joke",
  "What's the stock price of Apple?"
];
```

## Automated Testing with Cursor

### Test Creation Prompt
```
Create a comprehensive test suite for the AI education chatbot that includes:

1. **API Tests** - Test all endpoints with valid/invalid inputs
2. **Content Tests** - Verify course content detection works
3. **Rate Limiting Tests** - Ensure abuse protection works
4. **Error Handling Tests** - Test graceful failures
5. **Mock Tests** - Test without hitting real Claude API

Include:
- Test setup/teardown procedures
- Mock data for consistent testing
- Clear assertions and error messages
- Documentation for running tests locally and in CI
```

## Production Testing

### Monitoring Tests (Auto-generated alerts)
- API response time > 3 seconds
- Error rate > 5%
- Unusual usage patterns
- Budget approaching limits

### A/B Testing Opportunities
- Different follow-up question styles
- Response length variations
- Greeting message effectiveness

## Test Automation

### Vercel Deployment Testing
```json
// In vercel.json
{
  "github": {
    "checks": true
  },
  "buildCommand": "npm test"
}
```

### GitHub Actions (Optional)
Simple workflow to run tests on PR:
```yaml
name: Test Chatbot
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm test
```

## Testing Best Practices

1. **Start Simple**: Basic happy path tests first
2. **Real Data**: Test with actual course content
3. **Edge Cases**: Empty messages, very long messages
4. **Error States**: Network failures, API limits
5. **Performance**: Response times, memory usage
6. **Security**: Prompt injection attempts

## Success Criteria

### Tests Must Pass:
- ✅ Course questions get relevant responses
- ✅ Non-course questions are rejected
- ✅ Rate limiting prevents abuse
- ✅ Widget loads on all course pages
- ✅ Mobile/desktop compatibility
- ✅ Error handling works gracefully

### Performance Benchmarks:
- ⚡ Response time < 2 seconds (95th percentile)
- 🛡️ Rate limiting blocks 6th request/minute
- 💰 Daily costs stay under $0.35
- 📊 Uptime > 99% (excluding planned maintenance)

## Cursor Commands for Testing

### Generate Test Suite
```
"Create a complete test suite for the AI education chatbot following the testing strategy. Include integration tests, mock data, and a manual testing checklist."
```

### Add Test Coverage
```
"Add test coverage reporting and identify any untested critical paths in the chatbot codebase."
```

### Create Performance Tests
```
"Build performance tests that verify the chatbot responds within 2 seconds and handles 20 concurrent users."
```

## When to Skip Testing

**Don't over-test these:**
- Simple configuration files
- Static content
- One-time setup scripts
- Obvious DOM manipulations

**Focus testing energy on:**
- API logic and integrations
- User-facing functionality
- Cost/security critical paths
- Error handling