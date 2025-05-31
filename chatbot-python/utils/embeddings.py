import os
import time
from sentence_transformers import SentenceTransformer

# Singleton pattern to share model instance
_model_instance = None

def get_model():
    """Get or initialize the embedding model"""
    global _model_instance
    
    if _model_instance is None:
        start_time = time.time()
        print("Loading sentence-transformers model...")
        
        try:
            _model_instance = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print(f"Model loaded in {time.time() - start_time:.2f} seconds")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    return _model_instance

def generate_embedding(text):
    """Generate embeddings for the given text"""
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    
    model = get_model()
    
    try:
        start_time = time.time()
        embedding = model.encode(text).tolist()
        print(f"Embedding generated in {time.time() - start_time:.2f} seconds")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        raise

def batch_generate_embeddings(texts, batch_size=32):
    """Generate embeddings for a batch of texts"""
    if not texts or not isinstance(texts, list):
        raise ValueError("Texts must be a non-empty list of strings")
    
    model = get_model()
    
    try:
        start_time = time.time()
        embeddings = model.encode(texts, batch_size=batch_size).tolist()
        print(f"Batch embeddings generated in {time.time() - start_time:.2f} seconds")
        return embeddings
    except Exception as e:
        print(f"Error generating batch embeddings: {str(e)}")
        raise 