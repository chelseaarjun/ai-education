# AI Education Chatbot Tests

This directory contains tests for the AI Education chatbot backend, organized into logical categories.

## Test Structure

```
tests/
├── unit/                  # Unit tests for isolated components
│   └── test_pydantic_models.py  # Tests for Pydantic model validation
├── integration/           # Integration tests requiring running services
│   ├── test_api.py        # Tests for API endpoints with server running
│   └── test_citations.py  # Tests for citation source detection (mock vs. real)
└── utils/                 # Utility tests for specific functionality
    ├── check_citations.py      # Command-line utility for citation checking
    ├── test_direct_parsing.py  # Tests for response parsing
    ├── test_migration.py      # Tests for database migration
    └── test_search.py         # Tests for search functionality
```

## Running Tests

### Running All Tests
```bash
python -m pytest tests/
```

### Running Specific Test Categories
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests (requires server to be running)
python -m pytest tests/integration/

# Run utility tests
python -m pytest tests/utils/
```

### Running Individual Test Files
```bash
python -m pytest tests/unit/test_pydantic_models.py
```

### Running Tests with Verbose Output
```bash
python -m pytest -v tests/unit/
```

## Test Requirements

- **Unit Tests**: No external services required
- **Integration Tests**: Requires the server to be running (`python server.py`)
- **Utility Tests**: May require specific environment variables or external services

## Environment Setup

Tests require environment variables to be set in a `.env` file or in your environment:

```
OPENAI_API_KEY=your_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=your_postgres_database_url
```

## Writing New Tests

When adding new tests:

1. Place them in the appropriate category folder
2. Follow the naming convention: `test_*.py`
3. Add proper documentation with docstrings
4. Update this README if adding new test categories 

## Citation Testing

The chatbot includes specialized tests to determine if citations are coming from Supabase (real) or from fallback mock data. This helps diagnose connectivity issues with the database.

### Running Citation Tests

```bash
# Run the integration test for citations
python -m pytest tests/integration/test_citations.py

# Use the command-line utility for a quick check
python -m tests.utils.check_citations
```

The `check_citations.py` utility provides a simple way to verify if your chatbot is using real or mock citations and can help diagnose connection issues.

## Testing with the Web Interface

To properly test the chatbot with the web interface:

1. Start the local server from the project root:
   ```bash
   cd chatbot-python
   python server.py
   ```

2. Open the test HTML page in a browser using a local server:
   ```bash
   # Using Python's built-in HTTP server (from project root)
   cd ..  # Go to the project root
   python -m http.server 8000
   ```

3. Access the test page at: http://localhost:8000/test-chatbot.html

### Important Notes About Web Testing

- **Direct File Opening**: Opening test-chatbot.html directly from the file system may cause it to use the production endpoint instead of your local server
- **CORS Issues**: If you encounter CORS errors, ensure your server is configured to allow requests from your local domain
- **Citation Verification**: When testing, you can verify real citations are being returned by checking:
  - The citation URLs (real citations should have URLs like `pages/llm.html#introduction`)
  - Using the browser's developer tools (F12) to inspect the network request to `/api/chat/` 