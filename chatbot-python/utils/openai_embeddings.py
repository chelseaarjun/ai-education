import os
import time
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment variables")

# Default model for embeddings
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

# Singleton pattern for client
_client = None

def get_client():
    """Get or initialize the OpenAI client"""
    global _client
    
    if _client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        try:
            _client = OpenAI(api_key=OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}")
            raise
    
    return _client

def generate_embedding(text, model=DEFAULT_EMBEDDING_MODEL):
    """Generate embeddings for the given text using OpenAI API"""
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    
    client = get_client()
    
    try:
        start_time = time.time()
        
        response = client.embeddings.create(
            input=text,
            model=model
        )
        
        embedding = response.data[0].embedding
        logger.info(f"Embedding generated in {time.time() - start_time:.2f} seconds")
        
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise

def batch_generate_embeddings(texts, model=DEFAULT_EMBEDDING_MODEL, batch_size=20):
    """Generate embeddings for a batch of texts using OpenAI API
    
    OpenAI allows batching multiple texts in a single API call, which is more efficient.
    However, there are rate limits, so we'll process in smaller batches if needed.
    """
    if not texts or not isinstance(texts, list):
        raise ValueError("Texts must be a non-empty list of strings")
    
    client = get_client()
    all_embeddings = []
    
    try:
        start_time = time.time()
        
        # Process in batches to handle rate limits
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            response = client.embeddings.create(
                input=batch,
                model=model
            )
            
            # Extract embeddings from response and add to results
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            
            # Sleep briefly between batches to avoid rate limits if processing many items
            if i + batch_size < len(texts):
                time.sleep(0.5)
        
        logger.info(f"Batch embeddings generated in {time.time() - start_time:.2f} seconds")
        return all_embeddings
    
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {str(e)}")
        raise 