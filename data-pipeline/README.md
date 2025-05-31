# AI Education Data Pipeline

This directory contains the data processing pipeline for the AI Education chatbot. It handles content extraction, embedding generation, and Supabase vector database setup.

## Directory Structure

- `extraction/`: Scripts for extracting structured content from website
- `embeddings/`: Scripts for generating embeddings from content
- `supabase/`: Setup scripts and schema for Supabase
- `utils/`: Utility functions for embeddings and processing
- `data/`: Output directory for extracted content

## Setup

1. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your Supabase credentials and configuration.

2. Install dependencies:
   ```bash
   # Set up conda environment
   conda env create -f environment.yml
   conda activate ai-education-data-pipeline
   
   # For Node.js scripts
   npm install
   ```

## Usage

### 1. Extract Content

Extract structured content from the website:

```bash
cd extraction
python extract-structured-content.py
```

This creates a `structured-content.json` file in the `data` directory.

### 2. Generate Embeddings

Generate embeddings and store them in Supabase:

```bash
cd embeddings
python generate-supabase-embeddings.py --setup-db
```

### 3. Set Up Supabase Manually

If you need to set up Supabase manually:

```bash
cd supabase
node setup.js
```

## Configuration Options

You can customize the pipeline through environment variables:

- `MODEL_NAME`: Embedding model name (default: all-MiniLM-L6-v2)
- `BATCH_SIZE`: Batch size for embedding generation
- `MAX_TOKENS`: Maximum tokens per content chunk
- `ROOT_DIR`: Path to the AI Education website root
- `OUTPUT_DIR`: Path to save extracted content

## Pipeline Workflow

1. **Content Extraction**: Extract structured content from HTML files
2. **Content Chunking**: Split content into appropriate chunks
3. **Embedding Generation**: Generate vector embeddings for each chunk
4. **Supabase Storage**: Store content and embeddings in Supabase

## Integration with Chatbot

The data in Supabase is used by the chatbot service for vector search and retrieval. 