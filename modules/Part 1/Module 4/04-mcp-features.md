### Features

MCP enables applications to leverage a variety of powerful features by connecting to different types of servers. These features allow AI-powered assistants to perform useful actions, retrieve information, and interact with external systems in a standardized way.

---

#### What is a Feature in MCP?

A **feature** in MCP is a specific capability that a server can provide and a client can use. Features are declared and negotiated during the connection setup, so both sides know what is available for the session.

---

#### Common MCP Features

- **Resources:**  
  Structured data or contextual information that a server can provide to the client.  
  *Examples:*  
  - A list of files in a project  
  - User profile data  
  - Search results from a database

- **Tools:**  
  Functions or actions that the AI assistant can invoke via the MCP protocol.  
  *Examples:*  
  - Running a code formatter  
  - Executing a database query  
  - Sending a notification

- **Prompts:**  
  Templated messages or workflows that guide the LLM’s behavior or user interactions.  
  *Examples:*  
  - A prompt template for summarizing a document  
  - A workflow for onboarding a new user

- **Sampling:**  
  The process where the server can request the LLM to generate or “sample” a response, often as part of a multi-step workflow.  
  *Examples:*  
  - Generating a summary for a report  
  - Creating a draft email

---

#### How Features Work

- **Declaration & Negotiation:**  
  During the initialization phase, both clients and servers declare which features they support. Only features supported by both sides are enabled for the session.
- **Server Support:**  
  A single MCP server can support multiple features. For example, a server might provide both a resource (list of files) and a tool (file search function).
- **Client Support:**  
  A client “supports” a feature if it can handle the protocol flows and message types required for that feature—not just calling a server, but also processing responses, notifications, or requests as needed.

---

**Key Points:**
- Features are the core capabilities that MCP enables between clients and servers.
- Not all features are supported by both sides; some are server-only, some client-only, and some require both.
- Features are modular and composable, allowing for flexible and extensible integrations.