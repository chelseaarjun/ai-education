# Module 4: Model Context Protocol (MCP) Lab - Detailed Outline

## 🎯 Learning Objectives
By the end of this lab, students will:
1. **Implement MCP Server** - Create a server exposing tools using MCP Python SDK
2. **Build MCP Client** - Develop client that communicates with server via stdio transport
3. **Integrate with Host** - Transform direct tool usage to MCP protocol
4. **Experience Protocol Benefits** - See standardization, modularity, and security boundaries in action
5. **Understand When to Use MCP** - Know the tradeoffs between direct tools vs MCP protocol

## 🏗️ What We're Building

**The Transformation Journey:**
```
BEFORE: Direct Tool Integration
┌─────────────────┐
│ CourseAssistant │──► search_content_tool()
│ Agent           │
└─────────────────┘

AFTER: MCP Protocol Integration  
┌─────────────────┐    ┌──────────┐    ┌──────────┐
│ CourseAssistant │◄──►│   MCP    │◄──►│   MCP    │
│ Agent (Host)    │    │ Client   │    │ Server   │
└─────────────────┘    └──────────┘    └──────────┘
                                            │
                                       search_content_tool()
```

**Components We'll Build:**
- **MCP Server**: Pre-built server exposing course content search (provided + explained)
- **MCP Client**: Hands-on development of client for protocol communication (main focus)
- **Host Application**: CourseAssistantAgent using MCP instead of direct tools (main focus)

## ⏱️ Lab Timeline (60 minutes)
- **Section 1**: Setup & Understanding MCP (10 min)
- **Section 2**: Server Overview & Startup (10 min) 
- **Section 3**: Building MCP Client (20 min)
- **Section 4**: Host Integration (15 min)
- **Section 5**: Testing & Benefits Reflection (5 min)

---

## 📋 Detailed Section Breakdown

### Section 1: Setup & Understanding MCP (10 min)
**Status: ❌ Incomplete**

**Content:**
- Install MCP Python SDK and dependencies
- Load course content embeddings (reuse from agents concepts)
- **MCP Mental Model**: Protocol vs Direct Integration analogy
- **Key Question**: Why add complexity of a protocol?

**Key Concepts:**
- MCP as "Universal Tool API" - like USB for AI tools
- Three roles: Host (orchestrator), Client (protocol handler), Server (tool provider)
- Benefits preview: modularity, standardization, security

**Deliverables:**
- ✅ Working environment with MCP SDK
- ✅ Course embeddings loaded and indexed
- ✅ Clear understanding of MCP value proposition

### Section 2: Server Overview & Startup (10 min)
**Status: ❌ Incomplete**

**Content:**
- **Pre-built Server Walkthrough**: Complete `course_content_server.py` provided to students
- **Code Explanation**: Understanding FastMCP server implementation patterns  
- **Server Startup**: Command to run server: `python course_content_server.py`
- **What's Happening**: Process isolation, stdio transport, tool exposure
- **Optional Testing**: Using MCP inspector: `mcp dev course_content_server.py`

**Key Concepts:**
- Server as isolated process providing standardized tool interface
- FastMCP decorator patterns and automatic schema generation
- Tool vs Resource distinction (conceptual understanding)
- Server capability advertisement and protocol compliance
- **Pre-built approach**: Understanding vs building from scratch

**Code Structure:**
```python
# Pre-provided course_content_server.py
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("course-content-server")

@mcp.tool()
def search_content(query: str, max_results: int = 3) -> str:
    """Search course content using semantic similarity"""
    # Implementation using existing search logic from agents lab
    return search_results

# Server startup
if __name__ == "__main__":
    mcp.run()
```

**Deliverables:**
- ✅ Understanding of MCP server architecture and patterns
- ✅ Working server running in separate process
- ✅ Clear grasp of tool implementation using FastMCP
- ✅ Foundation ready for client development (main learning focus)

### Section 3: Building MCP Client (20 min)
**Status: ❌ Incomplete**

**Content:**
- **MCP Client Role**: Protocol translator between host and server processes
- **Transport Setup**: Stdio transport configuration connecting to running server
- **Protocol Flow**: Capability negotiation, tool discovery, request/response patterns
- **Client Implementation**: **Main hands-on building section** using MCP SDK
- **Error Handling**: Connection failures, timeout, server unavailability, malformed responses
- **Testing Client**: Verify connection and tool invocation with running server

**Key Concepts:**
- Client as protocol abstraction layer
- Transport independence (stdio now, HTTP/SSE for production)
- Capability negotiation and tool discovery lifecycle
- **Async communication patterns (important difference from direct tool calls)**
- Process boundary communication and error handling

**Code Structure:**
```python
# MCP Client connecting to running server
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",
    args=["course_content_server.py"]
)

class CourseContentMCPClient:
    def __init__(self, server_params):
        self.server_params = server_params
    
    async def search_content(self, query: str, max_results: int = 3) -> str:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("search_content", 
                                               {"query": query, "max_results": max_results})
                return result
```

**Deliverables:**
- ✅ **Working MCP client that connects to and communicates with server**
- ✅ **Understanding of protocol communication flow and async patterns**
- ✅ **Experience with tool discovery and invocation via MCP protocol**
- ✅ **Client ready for integration into host application**

### Section 4: Host Integration (15 min)
**Status: ❌ Incomplete**

**Content:**
- **Transform CourseAssistantAgent**: Replace direct tool calls with MCP client integration
- **Orchestration Patterns**: How agent orchestrates MCP protocol vs direct function calls
- **Async Integration**: Adapting agent patterns to work with async MCP client
- **Error Handling**: Graceful degradation when MCP server unavailable
- **Side-by-Side Comparison**: Direct tool approach vs MCP protocol approach
- **Benefits Demonstration**: Modularity and standardization in practice

**Key Concepts:**
- Host responsibility for orchestration and tool selection
- Protocol abstraction benefits in practice
- Maintaining clean agent architecture with MCP integration
- **Async patterns vs sync function calls from agents lab**
- Tool availability discovery and fallback patterns
- **Agent transformation**: Same capabilities, different integration approach

**Code Structure:**
```python
class MCPCourseAssistantAgent:
    def __init__(self, server_params):
        self.server_params = server_params
        
    async def decide_and_act(self, user_input: str) -> str:
        # Use MCP client to connect and call tools
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Tool discovery
                tools = await session.list_tools()
                
                # Tool invocation via protocol
                search_results = await session.call_tool("search_content", 
                                                       {"query": user_input})
                
                # Generate response using LLM + search results (same as agents lab)
                response = self._call_llm(response_prompt)
                return response

# Compare with original direct approach
class DirectCourseAssistantAgent:
    def decide_and_act(self, user_input: str) -> str:
        # Direct function call (from agents lab)
        search_results = search_content_tool(user_input)
        response = self._call_llm(response_prompt)
        return response
```

**Deliverables:**
- ✅ **CourseAssistantAgent working with MCP protocol instead of direct tools**
- ✅ **Clear understanding of host orchestration patterns with MCP**
- ✅ **Experience with async agent patterns and error handling**
- ✅ **Practical comparison of protocol vs direct integration approaches**

### Section 5: Testing & Benefits Reflection (5 min)
**Status: ❌ Incomplete**

**Content:**
- **End-to-End Testing**: Host → Client → Server → Tool flow
- **Performance Comparison**: Direct vs MCP approach
- **Benefits Realized**: Modularity, standardization, security boundaries
- **Production Notes**: HTTP transport, OAuth 2.1, deployment scaling

**Key Concepts:**
- System integration testing approaches
- Protocol overhead vs benefits analysis
- Real-world deployment considerations
- When to choose MCP vs direct integration

**Deliverables:**
- ✅ Working end-to-end MCP system
- ✅ Clear understanding of MCP value proposition
- ✅ Production deployment awareness

---

## 🔑 Key Learning Outcomes

**Technical Skills:**
- ✅ **MCP client development with Python SDK (primary focus)**
- ✅ MCP server understanding through code walkthrough
- ✅ **Host application integration patterns (primary focus)**
- ✅ Protocol debugging and async error handling

**Conceptual Understanding:**
- ✅ MCP architecture and separation of concerns
- ✅ Tool standardization benefits and implementation costs
- ✅ **Protocol vs direct integration decision framework**
- ✅ Security and modularity through process boundaries

**Real-World Applications:**
- ✅ When to use MCP vs direct tools in production systems
- ✅ **Integration patterns for existing applications (main practical skill)**
- ✅ Protocol evolution and future-proofing strategies

## 🧠 Key Mental Models Students Will Gain

**1. MCP as "Universal USB for AI Tools"**
- Standardized interface for tool integration
- Tool providers and consumers can evolve independently
- Protocol ensures compatibility across different systems

**2. Three-Layer Architecture**
- **Host**: Orchestration and decision-making (your agent)
- **Client**: Protocol handling and communication
- **Server**: Tool implementation and execution

**3. Benefits Triangle**
- **Modularity**: Tools can be developed and deployed independently
- **Standardization**: Common interface reduces integration complexity
- **Security**: Clear boundaries and controlled communication

## 📚 Prerequisites
- Basic understanding of AI agents and tool usage (conceptual)
- Python programming fundamentals
- Basic async/await concepts
- JSON and API familiarity

*Note: This lab is standalone - students do not need to complete the previous agents lab, though the concepts build naturally on those foundations.*