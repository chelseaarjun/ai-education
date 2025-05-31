# AI Education Chatbot

This is a conversational AI assistant for the AI Education course. It uses ChromaDB for vector search and Anthropic Claude for generating responses.

## Setup

1. Make sure you have Node.js (v14+) and Python (3.8+) installed
2. Install dependencies:
   ```
   # Install Node.js dependencies
   npm install
   
   # Install Python dependencies (in a conda environment)
   conda env create -f environment.yml
   # Or with pip
   pip install chromadb uvicorn
   ```

3. Set up environment variables:
   Create a `.env` file with:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Running the Chatbot

The chatbot requires two components to run:

### 1. Start the ChromaDB Server

First, start the ChromaDB server:

```bash
# Activate the conda environment (if using conda)
conda activate ai-education-chatbot

# Start the ChromaDB server
python scripts/start_chroma_server.py
```

This will start ChromaDB server on http://localhost:8000

### 2. Start the Node.js Server

In a separate terminal, start the Node.js server:

```bash
node server.js
```

This will start the API server on http://localhost:3000

## API Usage

The main API endpoint is:

```
POST /api/chat
```

Request format:
```json
{
  "message": "What are large language models?",
  "conversationHistory": [
    {"role": "user", "content": "Previous user message"},
    {"role": "assistant", "content": "Previous assistant response"}
  ],
  "proficiencyLevel": "Beginner",
  "conversationSummary": "Optional summary of conversation"
}
```

Response format:
```json
{
  "answer": {
    "text": "Large Language Models are...",
    "citations": [
      {"id": 1, "text": "Source text", "location": "module/section"}
    ]
  },
  "followUpQuestions": [
    "What are some examples of LLMs?",
    "How do LLMs work?"
  ],
  "conversationSummary": "Updated conversation summary"
}
```

## Development Mode

If no ChromaDB server is detected or if there are connection issues, the system will fall back to using mock data.

You can also test the API using:
```
GET /api/health
GET /api/test-chroma
```

## Features

- Express.js backend with API endpoints for chat functionality
- Integration with Anthropic Claude for natural language processing
- RAG (Retrieval-Augmented Generation) implementation with ChromaDB
- Mock data fallback for development

## API Endpoints

- `POST /api/chat` - Chat endpoint with RAG functionality
- `GET /api/health` - Health check endpoint
- `GET /api/test-chroma` - Test ChromaDB query endpoint
- `GET /api/chroma-info` - Get information about the ChromaDB setup

## Testing

You can test the API with curl:

```bash
# Health check
curl http://localhost:3000/api/health

# Test ChromaDB
curl http://localhost:3000/api/test-chroma

# Get ChromaDB info
curl http://localhost:3000/api/chroma-info

# Test chat API
curl -X POST -H "Content-Type: application/json" -d '{"message":"What are LLMs?","proficiencyLevel":"Beginner"}' http://localhost:3000/api/chat
```

## Troubleshooting

### ChromaDB Connection Issues

If you see "Using mock data" in the logs, it means the server couldn't connect to ChromaDB. Make sure:

1. You have started the ChromaDB server on port 8000
2. The ChromaDB server has access to the data in `data/chroma_db`
3. There are valid collections in the database

### Inspecting ChromaDB

You can use the inspection script to check the state of your ChromaDB:

```bash
node scripts/inspect_chroma.js
```

## License

[MIT License](LICENSE) 