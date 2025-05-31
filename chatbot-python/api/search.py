from fastapi import FastAPI, Request, HTTPException
import os
import json
import time
import openai
from supabase import create_client, Client
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

app = FastAPI()
load_dotenv()

# Initialize Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
openai.api_key = OPENAI_API_KEY

# Initialize clients - will be loaded on first request
supabase = None

@app.on_event("startup")
async def startup():
    """Initialize Supabase client on startup."""
    global supabase
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "AI Education Search API"}

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def generate_embedding(text):
    """Generate embedding using OpenAI API with retries."""
    try:
        response = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        raise

@app.post("/")
async def search(request: Request):
    global supabase
    
    # Parse request
    try:
        data = await request.json()
        query = data.get("query")
        num_results = int(data.get("num_results", 5))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    # Initialize Supabase client if not already loaded
    if supabase is None:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to connect to Supabase: {str(e)}")
    
    # Generate embedding using OpenAI
    try:
        start_time = time.time()
        embedding = generate_embedding(query)
        print(f"Embedding generated in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")
    
    # Search in Supabase
    try:
        start_time = time.time()
        response = supabase.rpc(
            'match_course_content',
            {
                'query_embedding': embedding,
                'match_threshold': 0.5,
                'match_count': num_results
            }
        ).execute()
        print(f"Supabase search completed in {time.time() - start_time:.2f} seconds")
        
        if hasattr(response, 'error') and response.error:
            raise Exception(response.error)
            
        return {
            "results": response.data,
            "query": query,
            "count": len(response.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}") 