from fastapi import FastAPI, Request, HTTPException
import os
import json
import time
import openai
from supabase import create_client, Client
from dotenv import load_dotenv
from anthropic import Anthropic
from tenacity import retry, wait_exponential, stop_after_attempt

app = FastAPI()
load_dotenv()

# Initialize clients
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize anthropic
anthropic = None if not anthropic_api_key else Anthropic(api_key=anthropic_api_key)

# Initialize Supabase client - will be loaded on first request
supabase = None

@app.on_event("startup")
async def startup():
    """Initialize Supabase client on startup."""
    global supabase
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"Connected to Supabase: {SUPABASE_URL}")
    except Exception as e:
        print(f"Error initializing Supabase: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "AI Education Chat API"}

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

async def retrieve_relevant_content(query, proficiency_level="Intermediate", num_results=5):
    """Retrieve relevant content from Supabase based on the query"""
    global supabase
    
    # Set minimum relevance threshold based on proficiency
    relevance_threshold = {
        "Beginner": 0.7,
        "Intermediate": 0.5,
        "Expert": 0.3
    }.get(proficiency_level, 0.5)
    
    try:
        # Initialize Supabase client if not already loaded
        if supabase is None:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Generate embedding using OpenAI
        embedding = generate_embedding(query)
        
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
        
        # Format results for prompt and citations
        sources = []
        for i, item in enumerate(response.data):
            sources.append({
                "id": i + 1,  # 1-based indexing for citations
                "content": item.get("content", ""),
                "title": item.get("title", "Unknown"),
                "url": item.get("url", "Unknown"),
                "relevance_score": item.get("similarity", 0.0),
                "section_title": item.get("title", "")  # Use title as section_title
            })
        
        return sources
    except Exception as e:
        print(f"Error retrieving content: {str(e)}")
        # Return fallback data
        return [
            {
                "id": 1,
                "content": "Large Language Models (LLMs) are sophisticated AI systems trained on vast amounts of text data to understand and generate human-like language.",
                "title": "AI Foundations",
                "url": "module1/llms.html",
                "relevance_score": 0.85,
                "section_title": "Introduction to LLMs"
            },
            {
                "id": 2,
                "content": "LLMs work through a process called transformer architecture, which allows them to process text in parallel and learn complex relationships between words and concepts.",
                "title": "AI Technical Concepts",
                "url": "module2/transformers.html",
                "relevance_score": 0.75,
                "section_title": "Transformer Architecture"
            }
        ]

def generate_prompt(question, proficiency_level, conversation_history, conversation_summary, retrieved_content):
    """Generate the system prompt with context and retrieved content"""
    formatted_content = "\n\n".join([
        f"[{item['id']}] {item['content']}\nSource: {item['title']} ({item['url']})"
        for item in retrieved_content
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

CITATION INSTRUCTIONS:
- When using information from the provided course content, cite your sources using numbered references: [1], [2], etc.
- If answering from your general knowledge, explicitly state "Based on my general knowledge:"
- Only cite course materials that directly inform your answer
- For each citation number, indicate the exact source being referenced
- You MUST cite sources when directly using course content

COURSE KNOWLEDGE:
{formatted_content or "No specific course content available for this query."}

ANSWER FORMAT:
1. Provide a clear, direct answer to the question
2. Include numbered citations [1], [2], etc. where appropriate
3. Suggest at least 1 to max 3 relevant follow-up questions

IMPORTANT: You MUST use the response_formatter tool to structure your response with the exact JSON schema provided.
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
    
    try:
        # Parse request
        data = await request.json()
        message = data.get("message")
        conversation_history = data.get("conversationHistory", [])
        proficiency_level = data.get("proficiencyLevel", "Intermediate")
        conversation_summary = data.get("conversationSummary", "")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
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
            
            try:
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
                    
                    # Ensure we have proper JSON structure
                    if isinstance(structured_response, str):
                        try:
                            structured_response = json.loads(structured_response)
                        except json.JSONDecodeError:
                            print(f"Error parsing response as JSON: {structured_response}")
                            return get_fallback_response("Invalid response format")
                    
                    # Add sources information to the response
                    structured_response["sources"] = [
                        {
                            "id": source["id"],
                            "title": source["title"],
                            "url": source["url"],
                            "section_title": source.get("section_title", ""),
                            "relevance_score": source.get("relevance_score", 0.0)
                        }
                        for source in retrieved_content
                    ]
                    
                    return structured_response
                else:
                    # Fallback to mock response if extraction fails
                    return get_fallback_response("Could not parse model response")
            except Exception as e:
                print(f"Error calling Anthropic API: {str(e)}")
                return get_fallback_response(f"API error: {str(e)}")
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