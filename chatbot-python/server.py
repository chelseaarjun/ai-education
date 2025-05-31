import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.chat import app as chat_app
from api.search import app as search_app

# Load environment variables
load_dotenv()

# Create main app
app = FastAPI(title="AI Education API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-applications
app.mount("/api/chat", chat_app)
app.mount("/api/search", search_app)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "AI Education API", "version": "1.0.0"}

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 3000))
    
    # Run the server
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True  # Enable auto-reload during development
    ) 