/**
 * Chat API handler for AI Education Chatbot
 */
const { Anthropic } = require('@anthropic-ai/sdk');
const path = require('path');

// Initialize Anthropic client
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || 'dummy-key-for-development',
});

/**
 * Gets the ChromaDB collection from global variables
 * This is initialized at server startup
 */
async function getChromaClient() {
  // Just return the global collection
  return { collection: global.courseContentCollection };
}

/**
 * Retrieves relevant content based on user question and proficiency level
 */
async function retrieveRelevantContent(question, proficiencyLevel) {
  try {
    console.log(`Retrieving content for question: "${question}" at proficiency: ${proficiencyLevel}`);
    const { collection } = await getChromaClient();
    
    // Set minimum relevance threshold based on proficiency
    const relevanceThreshold = {
      "Beginner": 0.7,
      "Intermediate": 0.5,
      "Expert": 0.3
    }[proficiencyLevel] || 0.5;
    
    console.log(`Using relevance threshold: ${relevanceThreshold}`);
    
    // Query ChromaDB for relevant content
    if (global.usingMockData) {
      console.log("Querying mock ChromaDB");
    } else {
      console.log("Querying real ChromaDB collection");
    }
    
    const result = await collection.query({
      queryTexts: [question],
      nResults: 4
    });
    
    console.log("Query completed successfully");
    
    // Process and format the results
    if (result && result.documents && result.documents[0]) {
      const docs = result.documents[0];
      const metadatas = result.metadatas ? result.metadatas[0] : [];
      
      console.log(`Found ${docs.length} relevant documents`);
      
      // Combine documents with their metadata for context
      return docs.map((doc, i) => {
        const metadata = metadatas[i] || {};
        return {
          content: doc,
          source: metadata.source || "Unknown",
          location: metadata.location || "Unknown"
        };
      });
    }
    
    console.log("No relevant documents found");
    return [];
  } catch (error) {
    console.error("Error retrieving content:", error);
    console.log("Returning fallback data");
    
    // Return fallback data if retrieval fails
    return [
      {
        content: "Large Language Models (LLMs) are sophisticated AI systems trained on vast amounts of text data to understand and generate human-like language.",
        source: "AI Foundations",
        location: "module1/llms.html"
      },
      {
        content: "LLMs work through a process called transformer architecture, which allows them to process text in parallel and learn complex relationships between words and concepts.",
        source: "AI Technical Concepts",
        location: "module2/transformers.html"
      }
    ];
  }
}

/**
 * Generates the system prompt with user context and retrieved content
 */
function generatePrompt(question, proficiencyLevel, conversationHistory, conversationSummary, retrievedContent) {
  // Format retrieved content for inclusion in prompt
  const formattedContent = retrievedContent.map((item, index) => {
    return `[${index + 1}] ${item.content}\nSource: ${item.source} (${item.location})`;
  }).join('\n\n');
  
  // Build the system prompt
  return `
You are an AI assistant for the AI Education course. Your purpose is to help students understand AI concepts.

CONVERSATION CONTEXT:
${conversationSummary || "This is a new conversation."}

PROFICIENCY LEVEL GUIDELINES:
- Beginner: Use very simple english words without any jargons like explaining to my grandmother who is tech illiterate. Focus on explaining the fundamentals, using analogies and simple examples. Avoid technical implementation details. Keep responses under 150 words.
- Intermediate: Use moderate technical terminology with brief explanations of complex concepts like explaining to a freshman in college. Include practical examples. Responses can be 150-250 words.
- Expert: Use precise technical language and industry terminology. Include implementation considerations, tradeoffs, and edge cases. Can reference advanced concepts without extensive explanation. Responses can be 200-300 words.

The user's current proficiency level is: ${proficiencyLevel}

GUIDELINES:
- Answer questions only related to the course content
- For off-topic questions, politely redirect to course material
- If uncertain, indicate when you need more information
- If technical explanations are needed, provide examples
- Use your general knowledge of AI and ML to provide accurate information 

COURSE KNOWLEDGE:
${formattedContent || "No specific course content available for this query."}

ANSWER FORMAT:
1. Provide a clear, direct answer to the question
2. Suggest at least 1 to max 3 relevant follow-up questions

IMPORTANT: Do not cite specific sources in your responsesYou MUST use the response_formatter tool to structure your response with the exact JSON schema provided.
Your answer should have 'answer.text', 'followUpQuestions', and 'conversationSummary'.
`;
}

/**
 * Formats conversation history for the Anthropic API
 */
function formatConversationHistory(history) {
  if (!history || !Array.isArray(history)) {
    return [];
  }
  
  return history.map(msg => ({
    role: msg.role,
    content: msg.content
  }));
}

/**
 * Generates a response using Anthropic Claude API
 */
async function generateResponse(systemPrompt, formattedHistory, userQuestion) {
  const responseSchema = {
    type: "object",
    properties: {
      answer: {
        type: "object",
        properties: {
          text: { type: "string" }
        },
        required: ["text"]
      },
      followUpQuestions: {
        type: "array",
        items: { type: "string" },
        minItems: 1,
        maxItems: 3
      },
      conversationSummary: { type: "string" }
    },
    required: ["answer", "followUpQuestions"]
  };

  try {
    console.log("System prompt to Claude:", systemPrompt);
    console.log("Generating response with Claude");
    
    // Use the real Claude API if we have an API key and not in mock mode
    if (!global.usingMockData && process.env.ANTHROPIC_API_KEY && process.env.ANTHROPIC_API_KEY !== 'dummy-key-for-development') {
      console.log("Using real Claude API");
      
      // Create messages for Anthropic
      const messages = [
        {
          role: 'user',
          content: userQuestion
        }
      ];
      
      // Add conversation history if available
      if (formattedHistory && formattedHistory.length > 0) {
        messages.unshift(...formattedHistory);
      }
      
      try {
        // Log the request parameters for debugging
        console.log("Sending request to Claude with parameters:", {
          model: 'claude-3-5-haiku-latest',
          maxTokens: 1000,
          systemPromptLength: systemPrompt.length,
          messages: messages.length,
          toolsConfigured: true
        });
        
        // Call Anthropic API with Tools
        const response = await anthropic.messages.create({
          model: 'claude-3-5-haiku-latest',
          max_tokens: 1000,
          system: systemPrompt,
          messages: messages,
          tools: [{
            name: "response_formatter",
            input_schema: responseSchema
          }],
          tool_choice: {
            type: "tool",
            name: "response_formatter"
          }
        });
        
        console.log("Raw Claude response received, extracting structured data");
        
        // Detailed response logging
        console.log("Response structure:", {
          hasContent: !!response.content,
          contentLength: response.content?.length,
          firstItemType: response.content?.[0]?.type,
          firstItemName: response.content?.[0]?.name,
          hasInput: !!response.content?.[0]?.input
        });
        
        // Extract structured data directly
        if (response?.content?.[0]?.type === 'tool_use' && 
            response.content?.[0]?.name === 'response_formatter') {
          
          const responseData = response.content[0].input;
          
          // Return in a standardized format that matches both real and mock
          if (responseData) {
            console.log("Successfully extracted structured data from Claude response");
            return responseData;
          } else {
            console.error("Claude returned tool_use but no input data");
          }
        } else {
          console.error("Claude did not return expected tool_use format");
          console.log("Response content:", JSON.stringify(response.content, null, 2));
        }
        
        // If we get here, something went wrong with extraction, return the full response
        // to let parseResponse handle it
        return response;
      } catch (claudeError) {
        console.error("Error calling Claude API:", claudeError);
        console.log("Error details:", claudeError.message, claudeError.stack);
        
        if (claudeError.status) {
          console.log("API Status Code:", claudeError.status);
        }
        
        console.log("Falling back to mock response");
      }
    }
    
    // Use mock response for development/testing or if real API call failed
    console.log("Using mock Claude response");
    
    // Return a structured mock response in the expected format
    // Note: This matches the format we extract from the real API
    return {
      answer: {
        text: "Large Language Models (LLMs) are sophisticated AI systems trained on vast amounts of text data to understand and generate human-like language. They work by predicting the next word in a sequence based on patterns learned during training."
      },
      followUpQuestions: [
        "How do LLMs work?",
        "What are some examples of LLMs?",
        "What are the limitations of current LLMs?"
      ],
      conversationSummary: "Discussion about Large Language Models and their capabilities."
    };
  } catch (error) {
    console.error("Error generating response:", error);
    throw new Error("Failed to generate response");
  }
}

/**
 * Parses the structured response from Anthropic
 */
function parseResponse(response) {
  try {
    console.log("Parsing structured response");
    
    if (!response || !response.content) {
      console.error("Response or response.content is missing");
      return getFallbackResponse("Missing response structure");
    }
    
    console.log("Response content type:", typeof response.content);
    console.log("Response content length:", response.content.length);
    
    // Detailed logging for debugging
    if (response.content && response.content.length > 0) {
      console.log("First content item type:", response.content[0]?.type);
      
      // More detailed logging
      if (response.content[0]?.type === 'tool_use') {
        console.log("Tool use name:", response.content[0]?.name);
        console.log("Tool use input available:", !!response.content[0]?.input);
      }
    }
    
    // Check for the tool_use response format from Claude API
    // The properties are directly in the content item, not nested under tool_use
    if (response?.content?.[0]?.type === 'tool_use' && 
        response.content?.[0]?.name === 'response_formatter') {
      
      const toolUseInput = response.content[0]?.input;
      
      if (toolUseInput) {
        console.log("Found structured tool_use response");
        return toolUseInput;
      }
    }
    
    // Enhanced debugging for unrecognized response format
    console.log("Response structure not recognized. Full response:", JSON.stringify(response, null, 2));
    
    // Fallback if tool response is not structured correctly
    console.log("Structured response not found, using fallback");
    return getFallbackResponse("Response format incorrect");
  } catch (error) {
    console.error("Error parsing response:", error);
    return getFallbackResponse("Error: " + error.message);
  }
}

/**
 * Gets a fallback response when structured response parsing fails
 */
function getFallbackResponse(reason) {
  return {
    answer: {
      text: `I'm sorry, I couldn't generate a proper response. ${reason}. Please try again.`
    },
    followUpQuestions: [
      "What are Large Language Models?",
      "How does AI help in education?",
      "What are the basics of machine learning?"
    ],
    conversationSummary: "Conversation about AI education topics."
  };
}

/**
 * Main chat handler function
 */
async function chatHandler(req, res) {
  try {
    console.log("Handling chat request");
    const { message, conversationHistory, proficiencyLevel, conversationSummary } = req.body;
    
    // Validate required parameters
    if (!message) {
      console.log("Missing message parameter");
      return res.status(400).json({ error: "Message is required" });
    }
    
    // Retrieve relevant content
    const retrievedContent = await retrieveRelevantContent(
      message, 
      proficiencyLevel || "Intermediate"
    );
    
    // Generate system prompt
    const systemPrompt = generatePrompt(
      message,
      proficiencyLevel || "Intermediate",
      conversationHistory || [],
      conversationSummary || "",
      retrievedContent
    );
    
    // Format conversation history
    const formattedHistory = formatConversationHistory(conversationHistory || []);
    
    // Generate response using Claude
    const response = await generateResponse(systemPrompt, formattedHistory, message);
    
    // Check if response needs parsing (old format) or is already parsed (new format)
    let parsedResponse;
    if (response.content) {
      // Old format - needs parsing
      console.log("Response in old format, parsing structured response");
      parsedResponse = parseResponse(response);
    } else if (response.answer) {
      // New format - already structured
      console.log("Response already in structured format");
      parsedResponse = response;
    } else {
      // Unknown format
      console.log("Unknown response format, using fallback");
      parsedResponse = getFallbackResponse("Unexpected response format");
    }
    
    // Return the response
    console.log("Sending response to client");
    res.json(parsedResponse);
    
  } catch (error) {
    console.error("Error in chat handler:", error);
    res.status(500).json({ 
      error: "Failed to process request",
      message: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}

module.exports = chatHandler; 