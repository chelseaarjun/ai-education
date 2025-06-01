# Rate Limiting Implementation Plan

## Overview

This document outlines a plan for implementing IP-based rate limiting for the AI Education API to prevent abuse and ensure fair usage of resources, particularly the Claude API which has quota limitations.

## Requirements

- Limit requests based on client IP address
- Apply different limits to different endpoints (stricter for `/api/chat` than `/api/search`)
- Support for whitelisting certain IPs (e.g., for testing)
- Configurable limits via environment variables
- Clear error responses when limits are exceeded

## Implementation Options

### Option 1: FastAPI Middleware with `slowapi`

**Recommended approach** - Uses the `slowapi` library, which is a rate limiter specifically designed for FastAPI and based on the popular Flask extension `flask-limiter`.

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create limiter
limiter = Limiter(key_func=get_remote_address)

# Apply to app
app = FastAPI(title="AI Education API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply different limits to different routes
@app.get("/api/search")
@limiter.limit("30/minute")
async def search_endpoint():
    # ...

@app.get("/api/chat")
@limiter.limit("10/minute")
async def chat_endpoint():
    # ...
```

### Option 2: Custom Middleware

Create a custom middleware that tracks request counts in an in-memory store or Redis:

```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # Check if client has exceeded rate limit
    # ...
    
    response = await call_next(request)
    return response
```

## Implementation Details

### Where to Implement

Since the API is structured with mounted sub-applications, we have two options:

1. **Main Application Level**: Implement in `server.py` to apply to all routes
2. **Sub-Application Level**: Implement in each sub-application (`chat.py` and `search.py`) for more granular control

For simplicity and consistency, implementing at the main application level is recommended.

### Storage Options

1. **In-Memory Store**: Simple but not suitable for multi-instance deployments
2. **Redis**: Better option for distributed systems, supports expiring keys
3. **Database**: More overhead but provides persistence and analytics capabilities

For the initial implementation, Redis is recommended due to its performance and built-in support for expiring keys.

### Configuration

Add the following environment variables:

```
RATE_LIMIT_ENABLED=true
RATE_LIMIT_CHAT_MINUTE=10
RATE_LIMIT_SEARCH_MINUTE=30
RATE_LIMIT_GLOBAL_HOUR=300
RATE_LIMIT_WHITELIST=127.0.0.1,192.168.1.1
```

### Error Handling

When a client exceeds the rate limit:
- Return HTTP status code 429 (Too Many Requests)
- Include a clear error message
- Include headers with rate limit information:
  - `X-RateLimit-Limit`: Maximum requests allowed in the period
  - `X-RateLimit-Remaining`: Requests remaining in the current period
  - `X-RateLimit-Reset`: Seconds until the limit resets

## Implementation Steps

1. Add `slowapi` to requirements.txt
2. Modify `server.py` to implement the rate limiter
3. Configure environment variables for rate limits
4. Add error handling for rate limit exceeded
5. Add monitoring and logging for rate limit events
6. Test with different request rates and verify behavior

## Considerations for Production

- Monitor rate limit events to adjust limits as needed
- Consider more sophisticated rate limiting based on user authentication
- For high traffic, implement a distributed rate limiter with Redis
- Add graceful degradation for when the system is under heavy load

## Future Enhancements

- User-based rate limiting (after authentication is implemented)
- Dynamic rate limiting based on system load
- Rate limit based on specific API parameters (e.g., complexity of queries)
- Analytics dashboard for rate limit events 