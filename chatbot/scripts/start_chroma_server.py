#!/usr/bin/env python3
"""
Start ChromaDB server for version 1.0.12
"""
import os
import sys
import uvicorn
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Start ChromaDB server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--path", default=None, help="Path to ChromaDB data")
    args = parser.parse_args()
    
    # Set environment variables for ChromaDB
    if args.path:
        chroma_path = Path(args.path).resolve()
        print(f"Setting ChromaDB path to: {chroma_path}")
        os.environ["PERSIST_DIRECTORY"] = str(chroma_path)
        os.environ["IS_PERSISTENT"] = "True"
    
    # Import here after setting environment variables
    from chromadb.app import app
    
    print(f"Starting ChromaDB server on {args.host}:{args.port}")
    # Start server
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main() 