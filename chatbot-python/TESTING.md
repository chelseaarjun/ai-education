# Testing the AI Education Chatbot

This document provides instructions for testing the AI Education chatbot backend.

## Test Structure

The tests are organized into three main categories:

1. **Unit Tests** (`tests/unit/`): Test individual components in isolation without requiring external services
2. **Integration Tests** (`tests/integration/`): Test the complete request-response cycle with a running server
3. **Utility Tests** (`tests/utils/`): Test specific functionality that may require external services

## Prerequisites

1. Install testing dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   DATABASE_URL=your_postgres_database_url
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Running Tests

### Running All Tests

```bash
python -m pytest
```

### Running Specific Test Categories

```bash
# Run unit tests only
python -m pytest tests/unit/

# Run integration tests only (requires server to be running)
python -m pytest tests/integration/

# Run utility tests only
python -m pytest tests/utils/
```

### Running Specific Test Files

```bash
python -m pytest tests/unit/test_pydantic_models.py
```

## Integration Test Setup

For integration tests, you need to have the server running:

1. Start the server in one terminal:
   ```bash
   python server.py
   ```

2. Run the integration tests in another terminal:
   ```bash
   python -m pytest tests/integration/
   ```

## Manual Testing with Test Scripts

Each test module can also be run directly as a script for manual testing:

```bash
# Test Pydantic models directly
python tests/unit/test_pydantic_models.py

# Test response parsing directly
python tests/utils/test_direct_parsing.py

# Test search functionality directly
python tests/utils/test_search.py
```

## Troubleshooting

### Common Issues

1. **Server connection failures**: Ensure the server is running on the expected port (default: 3000)

2. **API key issues**: Verify all API keys are correctly set in your `.env` file

3. **Database connection errors**: Check your DATABASE_URL and ensure PostgreSQL is running

### Debugging Tests

For more verbose output when debugging:

```bash
python -m pytest -vv tests/unit/
```

To see print statements during test execution:

```bash
python -m pytest -s tests/unit/
``` 