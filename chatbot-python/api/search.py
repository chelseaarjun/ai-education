from fastapi import FastAPI, Request, HTTPException
from sentence_transformers import SentenceTransformer
import os
import json
import time
from supabase import create_client, Client
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# Initialize Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

# Initialize model - will be loaded on first request
model = None

@app.get("/")
def read_root():
    return {"message": "AI Education Search API"}

@app.post("/")
async def search(request: Request):
    global model
    
    # Parse request
    try:
        data = await request.json()
        query = data.get("query")
        num_results = int(data.get("num_results", 5))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
        
    # Initialize model if not already loaded
    if model is None:
        start_time = time.time()
        try:
            model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print(f"Model loaded in {time.time() - start_time:.2f} seconds")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
    
    # Initialize Supabase client
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Supabase: {str(e)}")
    
    # Generate embedding
    try:
        start_time = time.time()
        embedding = model.encode(query).tolist()
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