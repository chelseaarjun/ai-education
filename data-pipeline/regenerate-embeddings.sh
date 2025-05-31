#!/bin/bash

# Script to regenerate embeddings with section-level chunking

echo "==========================================="
echo "  Regenerating Embeddings with Section-Level Chunking"
echo "==========================================="

# 1. Extract structured content
echo "[1/3] Extracting structured content..."
cd "$(dirname "$0")"
python extraction/extract-structured-content.py

# 2. Check if extraction was successful
if [ ! -f "data/structured-content.json" ]; then
    echo "Error: Failed to extract structured content."
    exit 1
fi

# 3. Generate embeddings with OpenAI and store in Supabase
echo "[2/3] Generating embeddings with section-level chunking..."
python embeddings/generate-supabase-openai-embeddings.py --setup-db --clear-data

# 4. Verify embeddings were generated
echo "[3/3] Verifying embeddings in Supabase..."
python embeddings/test_openai_supabase.py

echo "==========================================="
echo "  Embedding Generation Complete"
echo "==========================================="
echo "The AI Education chatbot now uses section-level chunking"
echo "for improved answer quality and context retention." 