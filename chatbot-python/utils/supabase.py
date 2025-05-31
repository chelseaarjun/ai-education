import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseManager:
    """Utility class for Supabase operations"""
    
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")
        self.client = None
        
    def connect(self):
        """Initialize Supabase client connection"""
        if not self.client:
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("Supabase URL and Key must be set in environment variables")
            
            self.client = create_client(self.supabase_url, self.supabase_key)
        
        return self.client
    
    def similarity_search(self, embedding, match_threshold=0.5, match_count=5):
        """Search for similar content using embeddings"""
        client = self.connect()
        
        try:
            response = client.rpc(
                'match_course_content',
                {
                    'query_embedding': embedding,
                    'match_threshold': match_threshold,
                    'match_count': match_count
                }
            ).execute()
            
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Supabase error: {response.error}")
                
            return response.data
        except Exception as e:
            print(f"Error in similarity search: {str(e)}")
            raise
    
    def save_interaction(self, user_id, query, response, metadata=None):
        """Save user interaction for analytics and improvement"""
        client = self.connect()
        
        try:
            interaction_data = {
                "user_id": user_id,
                "query": query,
                "response": response
            }
            
            # Add any additional metadata
            if metadata and isinstance(metadata, dict):
                interaction_data.update(metadata)
                
            # Insert into interactions table
            response = client.table("interactions").insert(interaction_data).execute()
            
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to save interaction: {response.error}")
                
            return response.data
        except Exception as e:
            print(f"Error saving interaction: {str(e)}")
            # Don't raise - we don't want to break the user experience if logging fails
            return None 