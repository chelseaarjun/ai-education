#!/usr/bin/env python3
"""
Embedding Generation Script for AI Education Chatbot

This script loads extracted content from course-content.json, generates embeddings using
sentence-transformers, and stores them in a ChromaDB collection for efficient semantic search.
"""

import json
import nltk
nltk.download('punkt_tab')
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

# Download NLTK data for sentence tokenization (first time only)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Configuration
ROOT_DIR = Path(__file__).resolve().parents[2]  # ai-education root directory
DATA_DIR = ROOT_DIR / "chatbot" / "data"
INPUT_FILE = DATA_DIR / "course-content.json"
CHROMA_DIR = DATA_DIR / "chroma_db"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"  # Optional, for inspection
COLLECTION_NAME = "course_content"

# Chunking configuration
CHUNK_SIZE = 150  # words
CHUNK_OVERLAP = 20  # words
MIN_CHUNK_SIZE = 50  # words

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Model configuration
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_content():
    """Load extracted content from JSON file."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def split_into_sentences(text):
    """Split text into sentences using NLTK."""
    return nltk.sent_tokenize(text)

def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks of roughly chunk_size words."""
    # First, split into sentences
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_words = len(sentence.split())
        
        # If adding this sentence exceeds chunk size and we already have content,
        # finish current chunk and start a new one
        if current_size + sentence_words > chunk_size and current_size >= MIN_CHUNK_SIZE:
            # Join current chunk into text
            chunks.append(" ".join(current_chunk))
            
            # Start new chunk with overlap by keeping the last few sentences
            overlap_size = 0
            current_chunk = []
            
            # Add sentences from the end until we have enough overlap
            for prev_sentence in reversed(current_chunk):
                prev_sentence_words = len(prev_sentence.split())
                if overlap_size + prev_sentence_words <= overlap:
                    current_chunk.insert(0, prev_sentence)
                    overlap_size += prev_sentence_words
                else:
                    break
            
            # Add current sentence to the new chunk
            current_chunk.append(sentence)
            current_size = overlap_size + sentence_words
        else:
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_size += sentence_words
    
    # Add the last chunk if it's not empty and meets minimum size
    if current_chunk and current_size >= MIN_CHUNK_SIZE:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def process_content(content_data):
    """Process content data into chunks for embedding."""
    chunks = []
    
    for page in content_data["pages"]:
        page_id = page["id"]
        page_title = page["title"]
        page_url = page["url"]
        
        for section in page["sections"]:
            section_id = section["id"]
            section_title = section["title"]
            section_content = section["content"]
            importance = section["importance"]
            
            # Process longer sections into smaller chunks
            if len(section_content.split()) > CHUNK_SIZE:
                section_chunks = split_into_chunks(section_content)
            else:
                # Keep short sections as a single chunk
                section_chunks = [section_content]
            
            # Add each chunk with its metadata
            for i, chunk_text in enumerate(section_chunks):
                chunk_id = f"{section_id}-{i}"
                chunks.append({
                    "id": chunk_id,
                    "text": chunk_text,
                    "source_page": page_id,
                    "source_page_title": page_title,
                    "source_section": section_id,
                    "source_section_title": section_title,
                    "source_url": page_url,
                    "importance": importance
                })
    
    return chunks

def create_chroma_collection(chunks, model):
    """Create a ChromaDB collection from chunks."""
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    # Create or get collection
    try:
        # If collection exists, delete it to refresh
        chroma_client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    # Create sentence transformer embedding function
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=MODEL_NAME
    )
    
    # Create collection
    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={"model": MODEL_NAME}
    )
    
    # Prepare data for batch addition
    ids = []
    documents = []
    metadatas = []
    
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    # Process chunks in batches to avoid memory issues
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        batch_ids = []
        batch_documents = []
        batch_metadatas = []
        
        for chunk in batch:
            batch_ids.append(chunk["id"])
            batch_documents.append(chunk["text"])
            
            # Create metadata dict (excluding text and embedding)
            metadata = {k: v for k, v in chunk.items() 
                       if k not in ["id", "text", "embedding"]}
            
            # Ensure all values are strings or numbers for ChromaDB
            for key, value in metadata.items():
                if not isinstance(value, (str, int, float, bool)):
                    metadata[key] = str(value)
            
            batch_metadatas.append(metadata)
        
        # Add documents to collection
        collection.add(
            ids=batch_ids,
            documents=batch_documents,
            metadatas=batch_metadatas
        )
        
        print(f"Processed batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
    
    print(f"Created ChromaDB collection with {collection.count()} chunks")
    return collection

def save_embeddings_json(chunks, model):
    """Save embeddings to JSON file for inspection (optional)."""
    # Generate embeddings for all chunks
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Add embeddings to chunks
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()
    
    # Create output structure
    output = {
        "model": MODEL_NAME,
        "chunks": chunks
    }
    
    # Save to file
    with open(EMBEDDINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Saved embeddings to {EMBEDDINGS_FILE}")

def main():
    """Main function to generate embeddings and create vector database."""
    print(f"Loading content from {INPUT_FILE}")
    content_data = load_content()
    
    print(f"Processing content into chunks")
    chunks = process_content(content_data)
    
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    
    print(f"Creating ChromaDB collection")
    collection = create_chroma_collection(chunks, model)
    
    # Optionally save embeddings to JSON for inspection
    if True:  # Set to False to skip this step
        print(f"Saving embeddings to JSON for inspection")
        save_embeddings_json(chunks, model)
    
    print("\nEmbedding generation complete!")
    print(f"ChromaDB collection saved to {CHROMA_DIR}")
    print(f"Total chunks: {len(chunks)}")

    # Test query to verify collection works
    query = "What are Large Language Models?"
    print(f"\nTesting query: '{query}'")
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    
    print("\nTop 2 results:")
    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"{i+1}. {metadata['source_page_title']} - {metadata['source_section_title']}")
        print(f"   {doc[:100]}...\n")

if __name__ == "__main__":
    main() 