# AI Education Chatbot API

A Python-based backend for the AI Education chatbot using OpenAI embeddings, Supabase for vector search, and Anthropic Claude for response generation.

## Setup

### Prerequisites
- Python 3.9+ or Conda (Anaconda or Miniconda)
- Supabase account with pgvector extension enabled
- OpenAI API key (for embeddings)
- Anthropic API key (optional, for Claude integration)

### Installation

1. Clone the repository
2. Create the conda environment:
```
conda env create -f environment.yml
```
3. Activate the environment:
```
conda activate ai-education-chatbot
```
4. Copy the example environment file and fill in your credentials:
```
cp env.example .env
```

## Development

Run the local development server:
```
python server.py
```

The API will be available at http://localhost:3000

## Testing

To test the search functionality with OpenAI embeddings:
```
python test_openai_supabase.py
```

## API Endpoints

### Search
- **URL:** `/api/search`
- **Method:** POST
- **Body:**
```json
{
  "query": "What are LLMs?",
  "num_results": 5
}
```

### Chat
- **URL:** `/api/chat`
- **Method:** POST
- **Body:**
```json
{
  "message": "Explain how LLMs work",
  "conversationHistory": [],
  "proficiencyLevel": "Intermediate",
  "conversationSummary": ""
}
```

## Deployment to Vercel

This project is configured for deployment to Vercel using serverless functions.

1. Install Vercel CLI:
```
npm install -g vercel
```

2. Deploy:
```
vercel
```

The `vercel.json` file contains the necessary configuration for Python serverless functions.

## Technical Notes

This application now uses OpenAI's embedding models (text-embedding-3-small by default) instead of sentence-transformers. The embedding dimension is 1536, which is compatible with the Supabase pgvector extension. The database schema has been updated to support these embeddings. 