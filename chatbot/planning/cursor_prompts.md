# Cursor Prompts for AI Education Chatbot

## Setup & Configuration Prompts

### 1. Project Setup
```
Create a Vercel configuration for an AI education chatbot with the following requirements:
- Node.js 18 runtime for API functions in chatbot/api/
- Environment variables for ANTHROPIC_API_KEY and KV store
- Static file serving for frontend assets
- CORS configuration for chat widget

Include package.json with dependencies: @anthropic-ai/sdk, @vercel/kv, and sentence-transformers for Python scripts.
```

### 2. Content Extraction & Embedding Generation
```
Create a Python script that:
- Extracts text content from HTML files in pages/ directory
- Removes HTML tags and navigation elements
- Uses course-optimized chunking strategy:
  * Extract content by sections (h2, h3 headers) to maintain topic boundaries
  * Split long sections (>500 chars) by sentences for granular search
  * Keep short sections whole to preserve context
  * Include metadata (module, section, content type) for each chunk
- Generates embeddings using sentence-transformers model 'all-MiniLM-L6-v2'
- Implements cosine similarity search function
- Outputs structured course-content.json and embeddings.json files
- Handles errors gracefully and provides progress feedback
- Includes function to test semantic search quality with sample questions
```

## API Development Prompts

### 3. Main Chat API with Semantic Search
```
Create a Vercel serverless function at chatbot/api/chat.js that:
- Accepts POST requests with {message, sessionId, conversationHistory}
- Implements rate limiting (5 requests/minute per IP using Vercel KV)
- Performs semantic content search using pre-computed embeddings:
  * Load embeddings.json and course-content.json
  * Convert user query to embedding using same model
  * Use cosine similarity to find top 3 most relevant content chunks
  * Filter results to ensure course-relevance (score threshold > 0.3)
- Integrates with Claude Haiku API for response generation:
  * Include relevant content chunks in prompt context
  * Use system prompt to stay on course topics only
  * Generate response with educational tone
- Only answers course-related questions (LLMs, prompt engineering, agents, MCP)
- Returns response with 3 contextual follow-up question suggestions
- Caches responses for identical questions using Vercel KV
- Includes comprehensive error handling and logging
- Protects against prompt injection attacks
```

### 4. Health Check API
```
Create a simple health check endpoint at chatbot/api/health.js that:
- Returns API status, cache status, and basic metrics
- Checks Claude API connectivity
- Returns response times and error rates
- Used for monitoring and debugging
```

## Frontend Development Prompts

### 5. Chat Widget
```
Create a vanilla JavaScript chat widget that:
- Integrates with existing chatbot placeholder in the course website
- Maintains conversation history within session
- Shows typing indicators during API calls
- Displays follow-up question buttons
- Handles errors gracefully with retry options
- Matches the existing site design (clean, educational)
- Works on mobile and desktop
- Includes accessibility features (keyboard navigation, screen reader support)
```

### 6. Widget Styling
```
Create CSS for the chat widget with:
- Modern, clean design matching the AI education site
- Smooth animations for open/close
- Responsive layout for mobile/desktop
- Proper z-index layering
- Loading states and error states
- Color scheme: primary blue (#2563eb), secondary gray (#6b7280)
- Typography matching the main site
```

## Testing Prompts

### 7. API Integration Tests with Semantic Search
```
Create comprehensive integration tests for the chatbot API that:
- Test successful chat responses for course-related questions
- Verify semantic search accuracy with test questions about:
  * LLM concepts (temperature, tokens, context windows)
  * Prompt engineering techniques (few-shot, chain-of-thought)
  * Agent fundamentals (memory, tools, orchestration)
  * Model Context Protocol (MCP architecture, SDKs)
- Test content chunking and embedding quality:
  * Verify course content is chunked appropriately by sections
  * Test that related concepts are found with semantic search
  * Validate cosine similarity scoring and thresholds
- Verify rate limiting works correctly
- Test non-course questions get appropriate rejection responses
- Verify caching functionality for identical questions
- Test error handling for API failures
- Check response format includes contextual follow-up questions
- Run with Jest framework in chatbot/tests/integration/
- Include setup/teardown for test data and mock embeddings
```

### 8. Frontend Testing
```
Create manual testing checklist and basic automated tests for:
- Chat widget opens/closes correctly
- Messages send and display properly
- Follow-up questions work
- Error states display correctly
- Mobile responsiveness
- Cross-browser compatibility (Chrome, Firefox, Safari)
- Accessibility testing with keyboard navigation
```

## Analytics & Monitoring Prompts

### 9. PostHog Integration
```
Integrate PostHog analytics to track:
- Chat widget opens/closes
- Questions asked (categorized by topic)
- Response satisfaction ratings
- Session duration and question count
- Error rates and types
- Popular follow-up questions
- Include privacy-conscious implementation
- Set up custom events for course-specific metrics
```

### 10. Performance Monitoring
```
Add monitoring and logging for:
- API response times
- Cache hit/miss rates
- Claude API usage and costs
- Error tracking and alerting
- User engagement metrics
- Peak usage patterns
- Create a simple dashboard for key metrics
```

## Deployment & Production Prompts

### 11. Production Deployment
```
Set up production deployment with:
- Environment variable configuration for Vercel
- Proper error handling and fallbacks
- Performance optimizations (caching, compression)
- Security headers and CORS policies
- Monitoring and alerting setup
- Backup and recovery procedures for data
```

### 12. Cost Optimization
```
Implement cost optimization strategies:
- Aggressive response caching (identical questions)
- Request deduplication for concurrent identical requests
- Graceful degradation when budget limits approached
- Monitoring and alerts for unexpected usage spikes
- Rate limiting to prevent abuse
- Efficient embedding search algorithms
```

## Usage Instructions for Cursor

1. **Copy the relevant prompt** for the component you're building
2. **Paste into Cursor** and let it generate the initial implementation
3. **Iterate and refine** using follow-up prompts
4. **Test incrementally** as each component is built
5. **Use the planning docs** as context for any questions

## Pro Tips for Cursor

- Reference the project overview and architecture when asking for modifications
- Ask Cursor to explain its implementation decisions
- Request code comments for complex logic
- Ask for alternative approaches when stuck
- Use Cursor to generate test data and mock responses