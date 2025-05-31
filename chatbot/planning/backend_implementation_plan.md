# Chatbot Backend Implementation Plan

## Overview

This document outlines the detailed implementation plan for the AI Education chatbot backend, focusing on the Node.js API endpoint, Anthropic Claude 3.5 Haiku integration, and ChromaDB retrieval system.

## Technical Stack

- **Runtime**: Node.js with Express.js
- **LLM Provider**: Anthropic Claude 3.5 Haiku
- **Vector Database**: ChromaDB (already implemented)
- **Deployment**: Vercel Serverless Functions

## API Design

### Endpoint Structure

```
POST /api/chat
```

### Request Format

```json
{
  "message": "User's current question",
  "conversationHistory": [
    {"role": "user", "content": "Previous user message"},
    {"role": "assistant", "content": "Previous assistant response"}
  ],
  "proficiencyLevel": "Beginner|Intermediate|Expert",
  "conversationSummary": "Optional summary of earlier conversation"
}
```

### Response Format

Using Anthropic's Tools API for structured output:

```json
{
  "answer": {
    "text": "The response content",
    "citations": [
      {"id": 1, "text": "Source text", "location": "pages/llm.html#section-2"}
    ]
  },
  "followUpQuestions": [
    "What is prompt engineering?",
    "How do LLMs handle context?"
  ],
  "conversationSummary": "Updated conversation summary"
}
```

## Conversation Management

### History Handling

- **Client-side storage**: Session storage maintains latest exchanges
- **Transmission**: Send only last 3 exchanges (6 messages) with each request
- **Conversation summary**: Keep a running summary of earlier conversation

### Summary Generation

1. After 3+ exchanges, generate a summary of the conversation
2. Send summary with future requests to maintain context
3. Update summary with each new exchange to maintain relevance

### Implementation

```javascript
// After receiving a response
if (conversationHistory.length > 6) { // 3 exchanges (user+assistant pairs)
  // Keep latest 3 exchanges (6 messages)
  const recentMessages = conversationHistory.slice(-6);
  // Store summary + recent messages
  sessionStorage.setItem('conversationHistory', JSON.stringify(recentMessages));
  sessionStorage.setItem('conversationSummary', summary);
}
```

## Retrieval Augmented Generation (RAG)

### Retrieval Strategy

- **Hybrid approach**:
  1. Attempt direct answer using conversation context
  2. If uncertainty detected, perform retrieval
  3. For what/how/why questions, preemptively retrieve content

- **Top-k retrieval**: Get top 4 most relevant chunks from ChromaDB
- **Filtering**: 
  - Apply importance threshold based on proficiency level
  - Relevance score weighted higher for more specific questions

### Implementation

```javascript
async function retrieveRelevantContent(question, proficiencyLevel) {
  // Set minimum importance threshold based on proficiency
  const importanceThreshold = {
    "Beginner": 0.7,
    "Intermediate": 0.5,
    "Expert": 0.3
  }[proficiencyLevel];

  const chromaClient = new ChromaClient();
  const collection = await chromaClient.getCollection("course_content");
  
  // Query with filtering
  return collection.query({
    queryTexts: [question],
    n: 4,
    where: { importance: { $gte: importanceThreshold } }
  });
}
```

## Structured Response Generation

### Tools API Implementation

Using Anthropic's Tools API to enforce response structure:

```javascript
// Define response schema
const responseSchema = {
  type: "object",
  properties: {
    answer: {
      type: "object",
      properties: {
        text: { type: "string" },
        citations: {
          type: "array",
          items: {
            type: "object",
            properties: {
              id: { type: "number" },
              text: { type: "string" },
              location: { type: "string" }
            },
            required: ["id", "text", "location"]
          }
        }
      },
      required: ["text"]
    },
    followUpQuestions: {
      type: "array",
      items: { type: "string" },
      minItems: 1,
      maxItems: 3
    },
    conversationSummary: { type: "string" }
  },
  required: ["answer", "followUpQuestions"]
};

// API call with tools
const response = await anthropic.messages.create({
  model: "claude-3-haiku-20240307",
  max_tokens: 1024,
  messages: [
    { role: "system", content: systemPrompt },
    ...conversationHistory,
    { role: "user", content: userQuestion }
  ],
  tools: [{
    name: "response_formatter",
    description: "Formats the response with answer, citations, and follow-up questions",
    input_schema: responseSchema
  }],
  tool_choice: { type: "tool", name: "response_formatter" }
});

// Extract the structured response
const structuredOutput = response.content[0].tool_calls[0].input;
```

## Prompt Engineering

### System Prompt Template

```
You are an AI assistant for the AI Education course. Your purpose is to help students understand AI concepts.

CONVERSATION CONTEXT:
{conversationSummary}

PROFICIENCY LEVEL GUIDELINES:
- Beginner: Use simple explanations without jargon. Focus on fundamentals and analogies. Avoid technical implementation details. Keep responses under 150 words.
- Intermediate: Use moderate technical terminology with brief explanations of complex concepts. Include practical examples. Responses can be 150-250 words.
- Expert: Use precise technical language and industry terminology. Include implementation considerations, tradeoffs, and edge cases. Can reference advanced concepts without extensive explanation. Responses can be 200-300 words.

The user's current proficiency level is: {proficiencyLevel}

GUIDELINES:
- Answer questions only related to the course content
- For off-topic questions, politely redirect to course material
- If uncertain, indicate when you need more information
- If technical explanations are needed, provide examples
- Include citations when referencing specific content

COURSE KNOWLEDGE:
{retrievedContent}

ANSWER FORMAT:
1. Provide a clear, direct answer to the question
2. Include citations where appropriate
3. Suggest 1-3 relevant follow-up questions
```

### Citation Implementation

- Number citations in response text: [1], [2], etc.
- Include source metadata from ChromaDB
- Link to specific sections in the course material

## Error Handling

### API Errors

- Handle Anthropic API timeouts and errors
- Implement exponential backoff for retries
- Return friendly error messages to frontend

### Input Validation

- Validate request parameters
- Ensure conversation history is properly formatted
- Handle malformed requests gracefully

### Off-Topic Questions

- Detect off-topic questions using prompt engineering
- Provide friendly redirection to course content
- Suggest relevant course topics

## Performance Optimization

### Latency Management

- **Target**: <2s P99.9 latency
- **Strategies**:
  - Parallel retrieval and context preparation
  - Response caching for duplicate questions
  - Efficient prompt construction

### Memory Usage

- Limit response size to avoid memory issues
- Batch ChromaDB queries for efficient processing
- Clean up resources after request completion

npm run dev## Local Testing Strategy

### Local Development Environment

1. **Express.js Server Setup**:
   ```javascript
   // server.js
   const express = require('express');
   const cors = require('cors');
   const bodyParser = require('body-parser');
   const app = express();
   
   app.use(cors());
   app.use(bodyParser.json());
   
   // Chat endpoint
   app.post('/api/chat', require('./api/chat'));
   
   const PORT = process.env.PORT || 3000;
   app.listen(PORT, () => {
     console.log(`Server running on port ${PORT}`);
   });
   ```

2. **Environment Configuration**:
   ```
   # .env
   ANTHROPIC_API_KEY=your_api_key
   CHROMA_DB_PATH=./data/chroma_db
   NODE_ENV=development
   ```

3. **Run Locally**:
   ```bash
   npm install
   node server.js
   ```

### Unit Testing Framework

Using Jest for unit testing:

```javascript
// chat.test.js
const { processMessage, generatePrompt, parseResponse } = require('../api/chat');

describe('Chat API', () => {
  test('generates correct prompt based on proficiency level', () => {
    const prompt = generatePrompt('What are LLMs?', 'Beginner', [], '');
    expect(prompt).toContain('Beginner');
    expect(prompt).toContain('simple explanations without jargon');
  });
  
  test('correctly parses structured response', () => {
    const mockResponse = {
      content: [{
        tool_calls: [{
          input: {
            answer: { text: 'Test answer' },
            followUpQuestions: ['Q1', 'Q2']
          }
        }]
      }]
    };
    
    const parsed = parseResponse(mockResponse);
    expect(parsed.answer.text).toBe('Test answer');
    expect(parsed.followUpQuestions).toHaveLength(2);
  });
});
```

### Mocking External Dependencies

1. **Mock Anthropic API**:
   ```javascript
   // __mocks__/@anthropic-ai/sdk.js
   const mockResponse = {
     content: [{
       tool_calls: [{
         input: {
           answer: {
             text: "LLMs are large language models trained on vast amounts of text data.",
             citations: []
           },
           followUpQuestions: [
             "How do LLMs work?",
             "What are some examples of LLMs?"
           ],
           conversationSummary: "Discussion about LLMs"
         }
       }]
     }]
   };
   
   const Anthropic = jest.fn().mockImplementation(() => {
     return {
       messages: {
         create: jest.fn().mockResolvedValue(mockResponse)
       }
     };
   });
   
   module.exports = { Anthropic };
   ```

2. **Mock ChromaDB**:
   ```javascript
   // __mocks__/chromadb.js
   const mockCollection = {
     query: jest.fn().mockResolvedValue({
       ids: [["doc1", "doc2"]],
       documents: [["Content about LLMs", "More content about AI"]],
       metadatas: [[
         { source_page_title: "LLM Guide", source_section_title: "Introduction" },
         { source_page_title: "AI Concepts", source_section_title: "Key Ideas" }
       ]]
     }),
     count: jest.fn().mockResolvedValue(100)
   };
   
   const PersistentClient = jest.fn().mockImplementation(() => {
     return {
       getCollection: jest.fn().mockResolvedValue(mockCollection)
     };
   });
   
   module.exports = { PersistentClient };
   ```

### Integration Testing

Test the complete flow with real ChromaDB but mocked Anthropic API:

```javascript
// integration.test.js
const request = require('supertest');
const app = require('../server');

// Only mock Anthropic, use real ChromaDB
jest.mock('@anthropic-ai/sdk');

describe('API Integration Tests', () => {
  test('POST /api/chat returns properly structured response', async () => {
    const res = await request(app)
      .post('/api/chat')
      .send({
        message: 'What are large language models?',
        conversationHistory: [],
        proficiencyLevel: 'Beginner'
      });
      
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('answer');
    expect(res.body).toHaveProperty('followUpQuestions');
  });
});
```

### Manual Testing Tools

1. **Postman Collection**:
   Create a Postman collection with test requests for different scenarios:
   - Basic questions
   - Follow-up questions with history
   - Different proficiency levels
   - Edge cases (very long questions, etc.)

2. **Simple HTML Test Page**:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <title>Chatbot Tester</title>
     <style>
       /* Minimal styling for the test page */
       body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
       .chat { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
       .controls { display: flex; gap: 10px; }
       select, button { padding: 8px; }
       input { flex-grow: 1; padding: 8px; }
     </style>
   </head>
   <body>
     <h1>Chatbot Test Interface</h1>
     <div class="chat" id="chat"></div>
     <div class="controls">
       <select id="proficiency">
         <option value="Beginner">Beginner</option>
         <option value="Intermediate">Intermediate</option>
         <option value="Expert">Expert</option>
       </select>
       <input type="text" id="message" placeholder="Type your message...">
       <button onclick="sendMessage()">Send</button>
     </div>
     
     <script>
       // Simple testing interface
       const chat = document.getElementById('chat');
       const message = document.getElementById('message');
       const proficiency = document.getElementById('proficiency');
       let history = [];
       
       async function sendMessage() {
         const text = message.value;
         if (!text) return;
         
         // Add user message to chat
         addMessage('user', text);
         message.value = '';
         
         // Call API
         try {
           const response = await fetch('http://localhost:3000/api/chat', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({
               message: text,
               conversationHistory: history,
               proficiencyLevel: proficiency.value
             })
           });
           
           const data = await response.json();
           
           // Add bot message to chat
           addMessage('bot', data.answer.text);
           
           // Update history
           history.push({ role: 'user', content: text });
           history.push({ role: 'assistant', content: data.answer.text });
           
           // Show follow-up questions
           if (data.followUpQuestions && data.followUpQuestions.length > 0) {
             const suggestions = document.createElement('div');
             suggestions.className = 'suggestions';
             data.followUpQuestions.forEach(q => {
               const btn = document.createElement('button');
               btn.textContent = q;
               btn.onclick = () => { message.value = q; sendMessage(); };
               suggestions.appendChild(btn);
             });
             chat.appendChild(suggestions);
           }
         } catch (error) {
           console.error(error);
           addMessage('system', 'Error: Could not get response');
         }
       }
       
       function addMessage(role, text) {
         const msg = document.createElement('div');
         msg.className = role;
         msg.textContent = role === 'user' ? `You: ${text}` : `Bot: ${text}`;
         chat.appendChild(msg);
         chat.scrollTop = chat.scrollHeight;
       }
     </script>
   </body>
   </html>
   ```

### End-to-End Testing

For complete end-to-end testing with real external services:

1. Create a `.env.test` file with real API keys (but use a separate ChromaDB collection)
2. Implement Playwright or Cypress tests for automated UI testing
3. Test realistic user flows and edge cases

## Test Cases to Cover

1. **Basic Functionality**:
   - Simple question answering
   - Proficiency level adaption
   - Follow-up question generation

2. **RAG Effectiveness**:
   - Retrieval accuracy for specific questions
   - Content relevance at different proficiency levels
   - Citations correctness

3. **Conversation Management**:
   - History handling and context maintenance
   - Summary generation and utilization
   - Multi-turn interactions

4. **Error Handling**:
   - Anthropic API failures
   - ChromaDB connection issues
   - Malformed requests

5. **Edge Cases**:
   - Very long questions
   - Offensive or off-topic questions
   - Questions requiring multiple knowledge sources

## Frontend Integration

### Required Frontend Changes

1. **Conversation Storage**:
   - Implement session storage for conversation history
   - Add logic for history truncation and summary management

2. **Proficiency Level**:
   - Pass proficiency level with each request
   - Store user preference across sessions

3. **Display Components**:
   - Render structured responses with citations
   - Display follow-up question suggestions
   - Add UI for streaming responses

### Integration Code Example

```javascript
// In chat-widget.js

async function sendMessage(message) {
  showThinking(); // Show typing indicator
  
  // Get conversation history from session storage
  const history = JSON.parse(sessionStorage.getItem('conversationHistory') || '[]');
  const summary = sessionStorage.getItem('conversationSummary') || '';
  
  // Get proficiency level
  const proficiencyLevel = getProficiencyLevel();
  
  // Prepare request
  const requestData = {
    message,
    conversationHistory: history.slice(-6), // Last 3 exchanges
    proficiencyLevel,
    conversationSummary: summary
  };
  
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData)
    });
    
    const data = await response.json();
    
    // Update UI with response
    displayResponse(data.answer.text);
    
    // Display citations if present
    if (data.answer.citations && data.answer.citations.length > 0) {
      displayCitations(data.answer.citations);
    }
    
    // Display follow-up questions
    displayFollowUpQuestions(data.followUpQuestions);
    
    // Update conversation history
    updateConversationHistory(message, data.answer.text);
    
    // Update conversation summary if provided
    if (data.conversationSummary) {
      sessionStorage.setItem('conversationSummary', data.conversationSummary);
    }
    
  } catch (error) {
    displayError("Sorry, there was an error processing your request.");
    console.error(error);
  }
}
```

## Implementation Phases

### Phase 1: Basic Backend (Week 1)

- Implement /api/chat endpoint
- Basic Claude integration
- Simple conversation history handling
- Initial prompt engineering

### Phase 2: RAG Integration (Week 1-2)

- Connect to ChromaDB
- Implement retrieval logic
- Add proficiency level adaptation
- Refine prompts with retrieved content

### Phase 3: Enhanced Features (Week 2-3)

- Implement structured responses with Tools API
- Add citation system
- Implement follow-up question generation
- Create conversation summary mechanism

### Phase 4: Optimization & Testing (Week 3-4)

- Performance optimization
- Error handling improvements
- End-to-end testing
- User acceptance testing

## Conclusion

This implementation plan provides a comprehensive roadmap for developing the AI Education chatbot backend. By following this approach, we will create a performant, user-friendly chatbot that effectively leverages the course content to provide tailored responses based on user proficiency levels. 