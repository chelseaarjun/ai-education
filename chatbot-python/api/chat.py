from fastapi import FastAPI, Request, HTTPException
from sentence_transformers import SentenceTransformer
import os
import json
import time
from supabase import create_client, Client
from dotenv import load_dotenv
from anthropic import Anthropic

app = FastAPI()
load_dotenv()

# Initialize clients
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

# Initialize model - will be loaded on first request
model = None
anthropic = None

@app.get("/")
def read_root():
    return {"message": "AI Education Chat API"}

async def retrieve_relevant_content(query, proficiency_level="Intermediate", num_results=5):
    """Retrieve relevant content from Supabase based on the query"""
    global model
    
    # Initialize model if not already loaded
    if model is None:
        start_time = time.time()
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print(f"Model loaded in {time.time() - start_time:.2f} seconds")
    
    # Set minimum relevance threshold based on proficiency
    relevance_threshold = {
        "Beginner": 0.7,
        "Intermediate": 0.5,
        "Expert": 0.3
    }.get(proficiency_level, 0.5)
    
    try:
        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Generate embedding for the query
        embedding = model.encode(query).tolist()
        
        # Search Supabase
        response = supabase.rpc(
            'match_course_content',
            {
                'query_embedding': embedding,
                'match_threshold': relevance_threshold,
                'match_count': num_results
            }
        ).execute()
        
        if hasattr(response, 'error') and response.error:
            raise Exception(response.error)
        
        # Format results for prompt
        return [
            {
                "content": item.get("content", ""),
                "source": item.get("title", "Unknown"),
                "location": item.get("url", "Unknown")
            }
            for item in response.data
        ]
    except Exception as e:
        print(f"Error retrieving content: {str(e)}")
        # Return fallback data
        return [
            {
                "content": "Large Language Models (LLMs) are sophisticated AI systems trained on vast amounts of text data to understand and generate human-like language.",
                "source": "AI Foundations",
                "location": "module1/llms.html"
            },
            {
                "content": "LLMs work through a process called transformer architecture, which allows them to process text in parallel and learn complex relationships between words and concepts.",
                "source": "AI Technical Concepts",
                "location": "module2/transformers.html"
            }
        ]

def generate_prompt(question, proficiency_level, conversation_history, conversation_summary, retrieved_content):
    """Generate the system prompt with context and retrieved content"""
    formatted_content = "\n\n".join([
        f"[{i+1}] {item['content']}\nSource: {item['source']} ({item['location']})"
        for i, item in enumerate(retrieved_content)
    ])
    
    return f"""
You are an AI assistant for the AI Education course. Your purpose is to help students understand AI concepts.

CONVERSATION CONTEXT:
{conversation_summary or "This is a new conversation."}

PROFICIENCY LEVEL GUIDELINES:
- Beginner: Use very simple english words without any jargons like explaining to my grandmother who is tech illiterate. Focus on explaining the fundamentals, using analogies and simple examples. Avoid technical implementation details. Keep responses under 150 words.
- Intermediate: Use moderate technical terminology with brief explanations of complex concepts like explaining to a freshman in college. Include practical examples. Responses can be 150-250 words.
- Expert: Use precise technical language and industry terminology. Include implementation considerations, tradeoffs, and edge cases. Can reference advanced concepts without extensive explanation. Responses can be 200-300 words.

The user's current proficiency level is: {proficiency_level}

GUIDELINES:
- Answer questions only related to the course content
- For off-topic questions, politely redirect to course material
- If uncertain, indicate when you need more information
- If technical explanations are needed, provide examples
- Use your general knowledge of AI and ML to provide accurate information

COURSE KNOWLEDGE:
{formatted_content or "No specific course content available for this query."}

ANSWER FORMAT:
1. Provide a clear, direct answer to the question
2. Suggest at least 1 to max 3 relevant follow-up questions

IMPORTANT: Do not cite specific sources in your responses. You MUST use the response_formatter tool to structure your response with the exact JSON schema provided.
Your answer should have 'answer.text', 'followUpQuestions', and 'conversationSummary'.
"""

def format_conversation_history(history):
    """Format conversation history for the Anthropic API"""
    if not history or not isinstance(history, list):
        return []
    
    return [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in history
    ]

@app.post("/")
async def chat(request: Request):
    """Main chat handler function"""
    global anthropic
    
    try:
        # Parse request
        data = await request.json()
        message = data.get("message")
        conversation_history = data.get("conversationHistory", [])
        proficiency_level = data.get("proficiencyLevel", "Intermediate")
        conversation_summary = data.get("conversationSummary", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Initialize Anthropic client if not already loaded
        if anthropic is None and anthropic_api_key:
            anthropic = Anthropic(api_key=anthropic_api_key)
        
        # Retrieve relevant content
        retrieved_content = await retrieve_relevant_content(
            message, 
            proficiency_level
        )
        
        # Generate system prompt
        system_prompt = generate_prompt(
            message,
            proficiency_level,
            conversation_history,
            conversation_summary,
            retrieved_content
        )
        
        # Format conversation history
        formatted_history = format_conversation_history(conversation_history)
        
        # Response schema
        response_schema = {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"}
                    },
                    "required": ["text"]
                },
                "followUpQuestions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 3
                },
                "conversationSummary": {"type": "string"}
            },
            "required": ["answer", "followUpQuestions"]
        }
        
        # Generate response with Claude if API key is available
        if anthropic:
            # Create messages for Anthropic
            messages = [{"role": "user", "content": message}]
            
            # Add conversation history if available
            if formatted_history and len(formatted_history) > 0:
                messages = formatted_history + messages
            
            # Call Anthropic API with Tools
            response = anthropic.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=1000,
                system=system_prompt,
                messages=messages,
                tools=[{
                    "name": "response_formatter",
                    "input_schema": response_schema
                }],
                tool_choice={
                    "type": "tool",
                    "name": "response_formatter"
                }
            )
            
            # Extract structured data
            if (response.content and 
                response.content[0].type == 'tool_use' and 
                response.content[0].name == 'response_formatter'):
                
                structured_response = response.content[0].input
                return structured_response
            else:
                # Fallback to mock response if extraction fails
                return get_fallback_response("Could not parse model response")
        else:
            # Return mock response if Anthropic API key is not available
            return get_fallback_response("API key not configured")
    
    except Exception as e:
        print(f"Error in chat handler: {str(e)}")
        return get_fallback_response(f"Error: {str(e)}")

def get_fallback_response(reason):
    """Get a fallback response when structured response parsing fails"""
    return {
        "answer": {
            "text": f"I'm sorry, I couldn't generate a proper response. {reason}. Please try again."
        },
        "followUpQuestions": [
            "What are Large Language Models?",
            "How does AI help in education?",
            "What are the basics of machine learning?"
        ],
        "conversationSummary": "Conversation about AI education topics."
    } 