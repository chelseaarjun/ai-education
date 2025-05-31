# AI Education Chatbot - Planning Documentation

## Project Overview

Building a course-focused chatbot for the AI Education website (ai-course.arjunasoknair.com) that:
- Answers questions about course content only
- Provides follow-up question suggestions
- Maintains conversation history within sessions
- Stays within $10/month budget
- Handles 100 DAU with 30 questions each

## Tech Stack

- **Frontend**: Vanilla JS popup widget
- **Backend**: Vercel Functions (Node.js)
- **LLM**: Claude Haiku via Anthropic API
- **Embeddings**: sentence-transformers (pre-computed)
- **Caching**: Vercel KV
- **Analytics**: PostHog
- **Deployment**: Vercel (auto-deploy from GitHub)

## Architecture

```
Frontend (Popup Widget)
    ↓
Vercel Function (/api/chat)
    ↓
[Rate Limiting] → [Cache Check] → [Content Search] → [Claude API] → [Cache Store]
    ↓
Response + Follow-up Questions
```

## Budget Breakdown & Controls
- **Claude Haiku**: ~$8-10/month (with usage controls)
- **Vercel KV**: Free tier (30k requests/month)
- **PostHog**: Free tier (20k events/month)
- **Total: ~$8-10/month**

### Budget Protection (Triple Layer)
1. **Anthropic Tier 1**: $10/month hard limit (automatic cutoff)
2. **Workspace Limits**: Set $10/month cap on chatbot workspace
3. **Code-Level Monitoring**: Daily usage tracking (~$0.33/day target)

## Security & Performance
- **API key management**: Secure storage with access controls
- **Environment variables**: Anthropic API key in Vercel environment only
- **Budget protection**: Anthropic Tier 1 limits + workspace caps + code monitoring
- **Rate limiting**: 5 questions/minute per IP (abuse prevention)
- **Response caching**: Identical questions cached for cost efficiency
- **Semantic search**: Pre-computed embeddings for fast, cost-effective content matching
- **Prompt injection protection**: Input validation and content filtering
- **Usage monitoring**: Real-time cost tracking via Anthropic Console

## File Structure

```
ai-education/
├── chatbot/
│   ├── planning/           # This folder
│   ├── frontend/
│   │   ├── chat-widget.js
│   │   ├── chat-widget.css
│   │   └── chat-icon.svg
│   ├── api/
│   │   ├── chat.js         # Main chat endpoint
│   │   └── health.js       # Health check
│   ├── tests/              # Chatbot test files
│   │   ├── integration/
│   │   ├── manual/
│   │   └── utils/
│   └── data/
│       ├── course-content.json
│       └── embeddings.json
├── scripts/
│   ├── generate-embeddings.py
│   └── extract-content.py
└── vercel.json            # Vercel configuration
```

## Implementation Phases

### Phase 1: Foundation
1. Vercel setup and basic API
2. Content extraction script
3. Embedding generation

### Phase 2: Core Features
1. Chat widget UI
2. Claude integration
3. Content search

### Phase 3: Polish
1. Rate limiting & caching
2. Analytics integration
3. Error handling

## Testing Strategy

**Lightweight but Effective:**
- Basic integration tests for API endpoints
- Manual testing for UI interactions
- Monitoring for production issues
- **No extensive unit testing** (keep it simple)

## Success Metrics
- Response accuracy for course questions
- Response time < 2 seconds
- Stay within budget
- Positive user feedback
- Handle peak traffic (500 concurrent users)