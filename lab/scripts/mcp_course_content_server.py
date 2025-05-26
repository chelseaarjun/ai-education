#!/usr/bin/env python3
"""
MCP Server for Course Content Search

This server exposes the course content search functionality via the Model Context Protocol.
It provides a standardized interface for searching through AI/ML course materials using
semantic similarity with FAISS and AWS Bedrock embeddings.

Usage:
    python course_content_server.py

For development/testing:
    mcp dev course_content_server.py
"""

import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# MCP imports
from mcp.server.fastmcp import FastMCP

# Course content search dependencies
import boto3
import numpy as np
import faiss

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
AWS_REGION = "us-west-2"
EMBEDDINGS_FILE = "../embeddings/course_embeddings.json"  # Relative path from lab directory
EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"

@dataclass
class SearchResult:
    """Data structure for search results"""
    content: str
    title: str
    source: str
    relevance_score: float

class CourseContentSearcher:
    """
    Handles the actual course content searching using the same logic from the agents lab.
    This class encapsulates all the FAISS and embedding functionality.
    """
    
    def __init__(self):
        self.bedrock_client = None
        self.search_index = None
        self.content_chunks = []
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the search system by loading embeddings and creating FAISS index.
        Returns True if successful, False otherwise.
        """
        try:
            # Initialize AWS Bedrock client
            self.bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
            logger.info("✅ Connected to AWS Bedrock")
            
            # Load embeddings data
            embeddings_data = self._load_embeddings()
            if not embeddings_data:
                return False
            
            # Create search index
            self.search_index, self.content_chunks = self._create_search_index(embeddings_data)
            if not self.search_index:
                return False
            
            self.is_initialized = True
            logger.info(f"✅ Course content searcher initialized with {len(self.content_chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize searcher: {e}")
            return False
    
    def _load_embeddings(self) -> Dict[str, Any]:
        """Load embeddings from JSON file"""
        try:
            embeddings_path = Path(EMBEDDINGS_FILE)
            
            if not embeddings_path.exists():
                logger.error(f"❌ Embeddings file not found: {EMBEDDINGS_FILE}")
                logger.error("Please ensure the course embeddings file is available from the agents lab")
                return {}
            
            with open(embeddings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"✅ Loaded embeddings from {EMBEDDINGS_FILE}")
            return data
            
        except Exception as e:
            logger.error(f"❌ Error loading embeddings: {e}")
            return {}
    
    def _create_search_index(self, embeddings_data: Dict[str, Any]) -> tuple:
        """Create FAISS index from embeddings data"""
        try:
            if not embeddings_data:
                return None, []
            
            chunks = embeddings_data['chunks']
            
            # Extract embeddings as numpy array
            embeddings_matrix = np.array([chunk['embedding'] for chunk in chunks], dtype=np.float32)
            
            # Create FAISS index (using Inner Product for cosine similarity)
            dimension = embeddings_matrix.shape[1]
            index = faiss.IndexFlatIP(dimension)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings_matrix)
            
            # Add embeddings to index
            index.add(embeddings_matrix)
            
            logger.info(f"✅ Created FAISS index with {index.ntotal} vectors, dimension {dimension}")
            return index, chunks
            
        except Exception as e:
            logger.error(f"❌ Error creating search index: {e}")
            return None, []
    
    def search(self, query: str, max_results: int = 3) -> List[SearchResult]:
        """
        Search course content using semantic similarity
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of SearchResult objects
        """
        if not self.is_initialized:
            logger.error("❌ Searcher not initialized")
            return []
        
        if not query.strip():
            logger.warning("⚠️ Empty query provided")
            return []
        
        try:
            # Create query embedding
            response = self.bedrock_client.invoke_model(
                modelId=EMBEDDING_MODEL,
                body=json.dumps({"inputText": query})
            )
            query_embedding = json.loads(response['body'].read())['embedding']
            
            # Convert to numpy and normalize for cosine similarity
            query_vector = np.array([query_embedding], dtype=np.float32)
            faiss.normalize_L2(query_vector)
            
            # Search for similar content
            scores, indices = self.search_index.search(query_vector, max_results)
            
            # Format results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if score > 0.3:  # Only include reasonably relevant results
                    chunk = self.content_chunks[idx]
                    results.append(SearchResult(
                        content=chunk['content'][:500] + "..." if len(chunk['content']) > 500 else chunk['content'],
                        title=chunk['title'],
                        source=chunk['source'],
                        relevance_score=float(score)
                    ))
            
            logger.info(f"🔍 Found {len(results)} results for query: '{query[:50]}...'")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error during search: {e}")
            return []

# Initialize the global searcher instance
searcher = CourseContentSearcher()

# Create the MCP server
mcp = FastMCP("course-content-server")

@mcp.tool()
def search_content(query: str, max_results: int = 3) -> str:
    """
    Search course content using semantic similarity
    
    This tool searches through AI/ML course materials to find relevant content
    based on the provided query. It uses vector embeddings and semantic similarity
    to return the most relevant sections.
    
    Args:
        query: The search query - what you want to find in the course content
        max_results: Maximum number of results to return (default: 3, max: 10)
    
    Returns:
        Formatted search results with titles, sources, and content snippets
    """
    
    # Input validation
    if not query or not query.strip():
        return "Error: Search query cannot be empty"
    
    # Limit max_results to prevent excessive responses
    max_results = min(max(1, max_results), 10)
    
    # Check if searcher is initialized
    if not searcher.is_initialized:
        return "Error: Course content search system not initialized. Please check server logs."
    
    try:
        # Perform the search
        results = searcher.search(query.strip(), max_results)
        
        if not results:
            return f"No relevant content found for query: '{query}'"
        
        # Format output for the requesting agent/client
        output = f"Found {len(results)} relevant content sections for '{query}':\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"{i}. **{result.title}** (Relevance: {result.relevance_score:.3f})\n"
            output += f"   Source: {result.source}\n"
            output += f"   Content: {result.content}\n\n"
        
        return output
        
    except Exception as e:
        logger.error(f"❌ Error in search_content tool: {e}")
        return f"Error during search: {str(e)}"

@mcp.tool()
def get_server_status() -> str:
    """
    Get the current status of the course content server
    
    Returns information about the server state, including whether it's properly
    initialized and ready to handle search requests.
    
    Returns:
        Server status information
    """
    
    try:
        status = {
            "server_name": "course-content-server",
            "initialized": searcher.is_initialized,
            "content_chunks": len(searcher.content_chunks) if searcher.is_initialized else 0,
            "aws_region": AWS_REGION,
            "embedding_model": EMBEDDING_MODEL
        }
        
        if searcher.is_initialized:
            status_msg = "✅ Server Status: READY\n"
            status_msg += f"📊 Content chunks loaded: {status['content_chunks']}\n"
            status_msg += f"🌎 AWS Region: {status['aws_region']}\n"
            status_msg += f"🧠 Embedding Model: {status['embedding_model']}\n"
            status_msg += "🔍 Ready to handle search requests"
        else:
            status_msg = "⚠️ Server Status: NOT READY\n"
            status_msg += "❌ Content search system not initialized\n"
            status_msg += "Please check server logs for initialization errors"
        
        return status_msg
        
    except Exception as e:
        logger.error(f"❌ Error getting server status: {e}")
        return f"Error getting status: {str(e)}"

def main():
    """
    Main entry point for the MCP server
    """
    try:
        # Initialize the course content searcher
        logger.info("🚀 Starting course content MCP server...")
        
        if not searcher.initialize():
            logger.error("❌ Failed to initialize course content searcher")
            logger.error("Please ensure:")
            logger.error("  1. AWS credentials are configured")
            logger.error("  2. Course embeddings file is available")
            logger.error("  3. Required dependencies are installed")
            sys.exit(1)
        
        logger.info("✅ Course content searcher initialized successfully")
        logger.info("🎯 Server ready to handle MCP requests")
        
        # Run the MCP server
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
