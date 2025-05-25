# Module 3: Building AI Agents - Hands-On Lab Plan

## Lab Overview

**Title**: Personal Assistant ChatBot Agent for Course Website  
**Duration**: 60 minutes  
**Format**: Single comprehensive Jupyter notebook  
**Implementation Approach**: Raw/from-scratch (no agent frameworks)

### Learning Objectives
By the end of this lab, students will:
1. Understand practical agent orchestration patterns
2. Implement two complementary tools with different patterns
3. Integrate episodic memory into agent decision cycles
4. Experience the difference between LLM applications and agentic applications
5. Prepare tools for MCP (Model Context Protocol) conversion in Module 4

---

## Technical Architecture

### Core Components
```
Agent Architecture:
├── Orchestration Engine (Raw Python)
├── Tool 1: Content Search (FAISS + Bedrock Titan Embeddings)  
├── Tool 2: Follow-up Question Generator (Claude-as-tool)
├── Episodic Memory (Simple conversation history)
└── LLM Interface (AWS Bedrock Claude-3-Sonnet)
```

### AWS Services Used
- **Amazon Bedrock**: 
  - Claude-3-Sonnet for orchestration and question generation
  - Titan Embeddings for content vectorization
- **No additional AWS services required**

### Python Dependencies
```
boto3>=1.34.0
faiss-cpu>=1.7.4
beautifulsoup4>=4.12.0
html2text>=2020.1.16
numpy>=1.24.0
pandas>=2.0.0
json
datetime
typing
```

---

## Lab Content Structure

### Data Preparation Strategy

#### Content Source
All HTML files in the course website:
```
ai-education/
├── index.html           # Main course homepage  
└── pages/              # All lesson pages
    ├── llms.html        # Module 1: Large Language Models
    ├── prompts.html     # Module 2: Prompt Engineering  
    ├── agents.html      # Module 3: Introduction to Agents
    └── [additional pages]
```

#### Text Extraction Pipeline
1. **HTML to Text**: Use `html2text` library for clean conversion
2. **Semantic Chunking**: Split by `<section>` elements for logical content units
3. **Embedding Generation**: Pre-compute using Bedrock Titan Embeddings
4. **Vector Storage**: Students create FAISS index from pre-built embeddings

#### Data Structure
```python
# Pre-built embeddings format
{
    "chunks": [
        {
            "content": "Clean text content of the section",
            "source": "pages/llms.html", 
            "section_id": "fundamentals",
            "title": "LLM Fundamentals",
            "embedding": [0.1, 0.2, ...]  # 1536-dim vector
        }
    ],
    "metadata": {
        "embedding_model": "amazon.titan-embed-text-v1",
        "chunk_count": 45,
        "total_tokens": 12500
    }
}
```

---

## Tool Implementations

### Tool 1: Content Search
**Purpose**: Search course materials using semantic similarity

```python
def search_content_tool(query: str, top_k: int = 3) -> str:
    """
    Search course content using vector similarity
    Clean, well-structured interface design
    """
    # 1. Generate query embedding
    # 2. Search FAISS index  
    # 3. Return formatted results with sources
```

**Key Features**:
- Semantic search using cosine similarity
- Returns content + source citations
- Configurable result count
- Clean, typed interface (good software engineering practice)

### Tool 2: Follow-up Question Generator  
**Purpose**: Generate contextual learning questions

```python
def generate_followup_questions_tool(current_topic: str, conversation_context: str = "") -> str:
    """
    Generate 3 relevant follow-up questions using Claude
    Demonstrates LLM-as-tool pattern
    """
    # Uses Claude to generate educational follow-up questions
```

**Orchestration Logic**:
- **Hybrid trigger approach**:
  1. User explicitly requests: "what else should I know?"
  2. Agent offers after successful answers: "💡 Want me to suggest follow-up questions?"
  3. Agent decides contextually based on conversation flow

**Key Features**:
- Educational focus (promotes deeper learning)
- Context-aware generation
- Smart triggering (not automatic/annoying)
- LLM-calling-LLM demonstration

---

## Memory Implementation

### Episodic Memory Design
**Approach**: Developer-controlled (not LLM-controlled) for simplicity

```python
class EpisodicMemory:
    def __init__(self):
        self.conversations = []  # Simple list storage
    
    def store_interaction(self, user_input: str, agent_response: str):
        """Store conversation turn with timestamp"""
        
    def get_recent_context(self, max_turns: int = 3) -> str:
        """Retrieve recent conversation for context"""
```

**Integration Pattern**:
- Developer logic always includes recent context in LLM prompts
- Memory automatically stored after each interaction
- Simple, reliable, educational

**Future Enhancement Ideas** (documented, not implemented):
- LLM-controlled memory retrieval decisions
- Semantic search over conversation history
- User preference storage
- Tool usage tracking

---

## Agent Orchestration

### Decision Cycle Implementation
```python
class CourseAssistantAgent:
    def __init__(self):
        self.tools = {
            "search_content": search_content_tool,
            "generate_followup_questions": generate_followup_questions_tool
        }
        self.memory = EpisodicMemory()
    
    def decide_and_act(self, user_input: str) -> str:
        """
        Main orchestration logic:
        1. Check for explicit follow-up requests
        2. Search content for relevant information  
        3. Generate response with memory context
        4. Decide whether to offer follow-up questions
        5. Store interaction in memory
        """
```

### Decision Logic Flow
1. **Parse user intent**: Follow-up request vs new question
2. **Tool selection**: Search first, then optionally generate follow-ups
3. **Context building**: Include memory when relevant
4. **Response generation**: Combine search results + LLM reasoning
5. **Memory update**: Store interaction for future context

---

## Lab Timeline & Structure

### Section 1: Setup & Data Loading (10 minutes)
**Objectives**: 
- Understand the data pipeline
- Load pre-built embeddings
- Create FAISS index

**Activities**:
- Install dependencies
- Load course content embeddings
- Build vector search index
- Test basic search functionality

**Code Provided**:
- Complete data loading functions
- FAISS index creation
- Sample search demonstrations

### Section 2: Tool Implementation (20 minutes)
**Objectives**:
- Implement content search tool
- Implement follow-up question generator
- Understand tool design principles

**Activities**:
- Review and test content search tool
- Implement follow-up question generation
- Test tools independently
- Understand clean tool design principles

**Code Provided**:
- Complete content search implementation
- Follow-up question generator with prompts
- Tool testing cells

### Section 3: Basic Agent (15 minutes)
**Objectives**:
- Build agent orchestration logic
- Integrate tools with decision cycle
- Experience agentic vs non-agentic behavior

**Activities**:
- Implement agent orchestration class
- Test basic question answering
- Demonstrate tool selection logic
- Interactive agent conversation

**Code Provided**:
- Complete agent orchestration
- Decision logic implementation
- Interactive demo cells

### Section 4: Adding Memory (15 minutes)
**Objectives**:
- Implement episodic memory
- Integrate memory with agent decisions
- Compare behavior with/without memory

**Activities**:
- Add memory to agent
- Test multi-turn conversations
- Compare responses with/without memory context
- Understand memory integration patterns

**Code Provided**:
- Complete memory implementation
- Before/after comparison demonstrations
- Multi-turn conversation examples

---

## Key Learning Moments

### 1. Tool Design Patterns
- **Retrieval Tool** (Content Search): External data access
- **Generative Tool** (Follow-up Questions): LLM-as-tool pattern
- **Clean Interfaces**: Well-structured tool design for maintainability

### 2. Orchestration Complexity
- **When to use which tool**: Decision logic demonstration
- **Tool combination**: Using search results to inform question generation
- **Error handling**: Graceful degradation when tools fail

### 3. Memory Integration
- **Developer vs LLM control**: Different autonomy levels
- **Context building**: How memory enhances responses
- **Conversation continuity**: Multi-turn interaction patterns

### 4. Agent vs LLM Application
- **Static workflow** vs **dynamic orchestration**
- **Context awareness** vs **stateless processing**
- **Tool autonomy** vs **predetermined tool usage**

---

## Assessment & Validation

### Success Criteria
Students should be able to:
- [ ] Successfully run all notebook cells without errors
- [ ] Explain when the agent chooses each tool
- [ ] Demonstrate memory-enhanced conversations
- [ ] Modify tool parameters and see different results
- [ ] Understand clean tool interface design principles

### Expected Outputs
1. **Working agent** that answers course content questions
2. **Follow-up questions** generated contextually  
3. **Memory demonstration** showing conversation continuity
4. **Understanding** of orchestration vs simple LLM usage

### Extension Opportunities
- Add more tools (calculator, current time, etc.)
- Implement user preference storage
- Create multi-agent scenarios
- Add human-in-the-loop approval workflows

---

## Teacher Notes: Module 4 Preparation

> **Note**: This section is for instructor reference only. Students will not see MCP-related content during Module 3.

### Content Search Tool - Module 4 Readiness
The content search tool is designed with future extensibility in mind:

```python
# Clean, typed interface (ready for future modularization)
@dataclass
class SearchRequest:
    query: str
    max_results: int = 3
    
@dataclass  
class SearchResult:
    content: str
    source: str
    relevance_score: float

def search_content_tool(request: SearchRequest) -> List[SearchResult]:
    # Implementation with clean separation of concerns
```

### Module 4 Transition Strategy
In Module 4 (Model Context Protocol), this foundation enables:
1. Tool extraction and modularization concepts
2. Same agent, distributed tools demonstration  
3. Building on familiar agent architecture
4. Tool reusability and sharing principles

---

## Production Considerations (Educational Notes)

### Areas for Future Development
1. **Error Handling**: Retry logic, graceful degradation
2. **Performance**: Caching, async operations, cost optimization
3. **Security**: Input validation, access controls, audit logging
4. **Monitoring**: Decision tracking, tool usage metrics, performance monitoring
5. **Scalability**: Vector database alternatives, distributed processing

### Best Practices Demonstrated
- Clean tool interfaces for maintainability and reusability
- Typed data structures for reliability
- Modular design for extensibility
- Clear separation of concerns
- Educational code documentation
- Error handling and graceful degradation

---

## Files & Resources

### Notebook Structure
```
Module3_Agent_Lab.ipynb       # Single comprehensive notebook
├── data/
│   ├── course_embeddings.json    # Pre-built embeddings
│   ├── sample_conversations.json # Example interactions
│   └── requirements.txt           # Python dependencies
└── README.md                     # Setup instructions
```

### AWS Configuration Requirements
- Bedrock access in us-east-1 (or configured region)
- Claude-3-Sonnet model access
- Titan Embeddings model access
- Appropriate IAM permissions

### Student Prerequisites
- Basic Python programming knowledge
- AWS account with Bedrock access configured
- Jupyter notebook environment
- Understanding of Modules 1-2 concepts (LLMs, Prompt Engineering)

---

This lab plan provides a complete blueprint for implementing the hands-on Module 3 agent experience, balancing educational value with practical implementation while preparing students for Module 4's MCP concepts.