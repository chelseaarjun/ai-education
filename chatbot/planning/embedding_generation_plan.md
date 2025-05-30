# Embedding Generation Plan

## Overview
This document outlines the approach for extracting content from the AI Education website and generating vector embeddings for use in the course chatbot. These embeddings will enable semantic search capabilities, allowing the chatbot to find relevant course content when answering user questions.

## Pipeline Architecture

We'll implement a three-step pipeline:
1. **Content Extraction** (`extract-content.py`): HTML -> JSON
2. **Embedding Generation** (`generate-embeddings.py`): JSON -> Vector Embeddings
3. **Index Creation** (part of `generate-embeddings.py`): Vector Embeddings -> ChromaDB

### Why a Multi-Step Approach?
- **Intermediate validation**: Allows inspection of extracted content before embedding
- **Modular maintenance**: Content extraction and embedding generation can be updated independently
- **Caching/reusability**: Content only needs to be extracted once; embeddings can be regenerated with different models
- **Separation of concerns**: Easier debugging and maintenance
- **Efficient retrieval**: Vector DB index enables fast similarity search at runtime

## Content Extraction (extract-content.py)

### Purpose
Extract relevant content from course pages to create a structured knowledge base.

### Input/Output
- **Input**: HTML files from website (pages/*.html)
- **Output**: `course-content.json` with organized course content

### Process
1. Parse HTML content from course pages using BeautifulSoup
2. Extract relevant text (excluding navigation, footers, etc.)
3. Structure data with metadata (page title, section, importance)
4. Save as JSON for further processing

### Content Structure
```json
{
  "pages": [
    {
      "id": "unique-page-id",
      "title": "Page Title",
      "url": "relative/path/to/page.html",
      "sections": [
        {
          "id": "section-id",
          "title": "Section Title",
          "content": "Full text content of the section...",
          "importance": 1.0  // 0.0-1.0 scale for content relevance
        }
      ]
    }
  ]
}
```

## Embedding Generation (generate-embeddings.py)

### Purpose
Convert extracted text content to vector embeddings for semantic search and create a searchable ChromaDB collection.

### Input/Output
- **Input**: Processed course content (`course-content.json`)
- **Output**: 
  - ChromaDB persistent collection (`data/chroma_db`)
  - Optional: Vector embeddings for each content chunk (`embeddings.json`) for inspection

### Process
1. Load content from JSON
2. Chunk content appropriately (paragraphs with overlap)
3. Generate embeddings for each chunk using sentence-transformers
4. Store chunks, embeddings, and metadata in ChromaDB
5. Save the ChromaDB collection for chatbot retrieval

### Technical Specifications
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
  - Good balance of speed/quality
  - 384-dimensional embeddings
  - Compact size (80MB) for local deployment
  - Strong performance on semantic search tasks

- **Chunking Strategy**: Paragraph-based (hybrid approach)
  - Base chunks: 150-word chunks with 20-word overlap
  - Special handling for complex sections with sentence-level chunking
  - Preserves context while allowing precise retrieval

- **Vector DB Technology**: ChromaDB
  - Simple, developer-friendly Python API
  - Persistent storage with automatic metadata management
  - Built-in filtering capabilities
  - Embeddings and metadata in a single system
  - Open source with active development

- **ChromaDB Structure**:
```
Document IDs: ["chunk-1", "chunk-2", ...]
Documents: ["Content of first chunk...", "Content of second chunk...", ...]
Metadata: [
  {
    "source_page": "page-id-1",
    "source_section": "section-id-1",
    "source_url": "relative/url1.html",
    "importance": 0.8
  },
  ...
]
Embeddings: [Automatically generated and stored]
```

## Vector Index Usage in Backend

### Loading and Querying ChromaDB
```python
import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to the persistent ChromaDB collection
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("course_content")

# Function to query the collection
def query_index(query_text, top_k=5, min_importance=0.5):
    # Search the collection
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        where={"importance": {"$gte": min_importance}},  # Optional filtering
    )
    
    # Return the corresponding content with metadata
    response = []
    for i, (doc, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        response.append({
            "text": doc,
            "source": metadata["source_url"],
            "section": metadata["source_section"],
            "distance": float(distance)
        })
    
    return response
```

### Advantages of ChromaDB
- **Simplified Architecture**: Embeddings and metadata in one system
- **Built-in Persistence**: No need to manually manage files
- **Rich Filtering**: Query by both semantic similarity and metadata filters
- **Easy Integration**: Clean, Pythonic API
- **Production Ready**: Suitable for both development and production
- **Future Scalability**: Supports distributed operation as needs grow

## Implementation Details

### Libraries
- BeautifulSoup4 for HTML parsing
- sentence-transformers for embedding generation
- NLTK for text processing and sentence splitting
- ChromaDB for vector storage and search

### Resource Requirements
- Memory: ~500MB (model + processing)
- Storage:
  - ~5-10MB for ChromaDB collection
  - ~5-10MB for optional embeddings JSON (for inspection)
- Processing time: ~5-10 minutes for entire site

### Error Handling
- Validate HTML structure before extraction
- Skip problematic pages/sections with appropriate logging
- Verify embedding generation quality with sample queries
- Include ChromaDB validation steps

## Testing Plan

### Content Extraction Testing
- Verify all important content is captured
- Check for HTML parsing errors
- Validate JSON structure
- Ensure proper metadata assignment

### Embedding Testing
- Test sample queries against embeddings
- Verify retrieval accuracy
- Benchmark performance (speed, memory usage)
- Compare against baseline methods

### ChromaDB Testing
- Test combined vector and metadata filtering
- Measure query latency
- Verify persistence (restart and query)
- Test various query patterns
- Check memory usage during operation

## Future Improvements
- Implement incremental updates (only re-embed changed content)
- Explore additional metadata for better retrieval
- Consider fine-tuning embeddings for domain-specific terminology
- Add support for non-text content (images, diagrams)
- Explore hybrid search (keyword + semantic)
- Add reranking of search results

## Conclusion
This approach balances efficiency, maintainability, and performance for the AI Education chatbot. Using ChromaDB provides a simplified architecture with built-in persistence and rich filtering capabilities, while the multi-step process ensures flexibility and proper validation at each stage. 