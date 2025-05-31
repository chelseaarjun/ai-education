/**
 * Tests for the chat API
 */
const chatHandler = require('../api/chat');

// Mock the Anthropic SDK
jest.mock('@anthropic-ai/sdk', () => {
  const mockResponse = {
    content: [{
      type: 'tool_use',
      tool_use: {
        name: 'response_formatter',
        input: {
          answer: {
            text: "LLMs are large language models trained on vast amounts of text data.",
            citations: []
          },
          followUpQuestions: [
            "How do LLMs work?",
            "What are some examples of LLMs?"
          ],
          conversationSummary: "Discussion about LLMs"
        }
      }
    }]
  };

  return {
    Anthropic: jest.fn().mockImplementation(() => {
      return {
        messages: {
          create: jest.fn().mockResolvedValue(mockResponse)
        }
      };
    })
  };
});

// Mock ChromaDB
jest.mock('chromadb', () => {
  const mockResult = {
    ids: [["doc1", "doc2"]],
    documents: [["Content about LLMs", "More content about AI"]],
    metadatas: [[
      { source: "AI Basics", location: "module1/llms.html" },
      { source: "AI Concepts", location: "module2/concepts.html" }
    ]]
  };

  const mockCollection = {
    query: jest.fn().mockImplementation(({ queryTexts, nResults }) => {
      console.log(`Test mock query with: ${queryTexts}, results: ${nResults}`);
      return Promise.resolve(mockResult);
    })
  };

  return {
    PersistentClient: jest.fn().mockImplementation(() => {
      return {
        getCollection: jest.fn().mockImplementation((name) => {
          console.log(`Test mock getCollection: ${name}`);
          return Promise.resolve(mockCollection);
        }),
        createCollection: jest.fn().mockImplementation(({ name }) => {
          console.log(`Test mock createCollection: ${name}`);
          return Promise.resolve(mockCollection);
        })
      };
    })
  };
});

// Make sure global variables exist for tests
global.chromaClient = {};
global.courseContentCollection = {
  query: jest.fn().mockResolvedValue({
    ids: [["doc1", "doc2"]],
    documents: [["Test content about AI", "More test content"]],
    metadatas: [[
      { source: "Test Source", location: "test/location.html" },
      { source: "Test Source 2", location: "test/location2.html" }
    ]]
  })
};

describe('Chat API', () => {
  // Mock Express request and response
  let req;
  let res;
  
  beforeEach(() => {
    req = {
      body: {
        message: 'What are LLMs?',
        conversationHistory: [],
        proficiencyLevel: 'Beginner'
      }
    };
    
    res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
    
    // Clear console logs for cleaner test output
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });
  
  afterEach(() => {
    jest.restoreAllMocks();
  });
  
  test('should return a properly structured response', async () => {
    await chatHandler(req, res);
    
    // Check that the response was called with a JSON object
    expect(res.json).toHaveBeenCalled();
    
    // Extract the argument that res.json was called with
    const response = res.json.mock.calls[0][0];
    
    // Verify response structure
    expect(response).toHaveProperty('answer');
    expect(response.answer).toHaveProperty('text');
    expect(response).toHaveProperty('followUpQuestions');
    expect(Array.isArray(response.followUpQuestions)).toBe(true);
  });
  
  test('should handle missing message parameter', async () => {
    req.body.message = '';
    
    await chatHandler(req, res);
    
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({
      error: expect.any(String)
    }));
  });
  
  test('should use default proficiency level if not provided', async () => {
    delete req.body.proficiencyLevel;
    
    await chatHandler(req, res);
    
    expect(res.json).toHaveBeenCalled();
  });
  
  test('should handle conversation history properly', async () => {
    req.body.conversationHistory = [
      { role: 'user', content: 'What is AI?' },
      { role: 'assistant', content: 'AI is artificial intelligence.' }
    ];
    
    await chatHandler(req, res);
    
    expect(res.json).toHaveBeenCalled();
  });
}); 