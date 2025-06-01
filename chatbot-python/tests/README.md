# AI Education Chatbot Tests

This directory contains tests for the AI Education chatbot backend, organized into logical categories.

## Test Structure

```
tests/
├── unit/                  # Unit tests for isolated components
│   └── test_pydantic_models.py  # Tests for Pydantic model validation
├── integration/           # Integration tests requiring running services
│   └── test_api.py        # Tests for API endpoints with server running
└── utils/                 # Utility tests for specific functionality
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