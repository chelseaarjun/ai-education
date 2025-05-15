##Architecture

---

### 1. MCP System Overview

#### High-Level Architecture: Host, Client, and Server

MCP is built on a modular, client-server architecture with three main roles:

- **Host:**  
  The **central application** that manages all connections, enforces security, and coordinates LLM interactions.  
  - Typically, the host is an application that interacts with an **LLM** (e.g., an AI-powered IDE, chat platform, or assistant interface).
  - The host **creates and manages multiple clients**—each client connects to a different server for a specific capability (such as code search or documentation lookup).
  - The host is responsible for **user consent, security enforcement, and orchestration** of all interactions.
  - **Example:** An AI-powered IDE that lets users ask questions about their code and documentation. The IDE (**host**) uses the LLM to interpret user's request and decide which tools (**servers**) are used to answer the user's query.

- **Client:**  
  A **connector** within the host that establishes and manages a session with a specific server.  
  - Each client maintains a **1:1 relationship** with a server and handles **protocol and capability negotiation, message routing, and capability exchange**.
  - Clients act as **secure bridges**, maintaining strict boundaries—each client only communicates with its assigned server and only has access to the data and capabilities the host allows.
  - **Example:** In the IDE, one client connects to the code search server, another to the documentation server. The code search client cannot access documentation data, and vice versa.

- **Server:**  
  A **service** that provides specialized context, tools, or prompts to the client.  
  - Servers can be **local or remote**, and are focused on specific capabilities.
  - Servers operate **independently**, exposing resources, tools, or prompts via the MCP protocol, and must respect security constraints set by the host.
  - **Examples:**  
    - A **code search server** that indexes and searches code repositories.
    - A **documentation server** that retrieves API documentation.

---

### MCP Design Principles

MCP is built on several key design principles that guide its architecture and implementation:

- **Servers should be extremely easy to build:**
  - Host applications handle complex orchestration responsibilities, allowing servers to focus on specific, well-defined capabilities with simple interfaces and maintainable code.
- **Servers should be highly composable:**
  - Each server provides focused functionality in isolation, but multiple servers can be combined seamlessly. The shared protocol enables interoperability and modular, extensible design.
- **Servers should not be able to read the whole conversation, nor "see into" other servers:**
  - Servers receive only the necessary contextual information, with full conversation history staying with the host. Each server connection is isolated, and cross-server interactions are controlled by the host to enforce security boundaries.
- **Features can be added to servers and clients progressively:**
  - The core protocol provides minimal required functionality, but additional capabilities can be negotiated and added as needed. Servers and clients can evolve independently, with the protocol designed for future extensibility and backwards compatibility.

---

#### How It Works (At a Glance): Practical Example

**Scenario:**  
A user is interacting with an **AI-powered productivity assistant (the host)** that integrates both a **calendar tool** and a **weather tool**.

**Flow (as shown in the diagram):**

```
[User] → [Host Application]
                ↓
         [Client Connector] ←→ [Server 1: Calendar Tool]
                ↓
         [Client Connector] ←→ [Server 2: Weather Tool]
```

1. **User** asks the AI assistant: "Do I have any meetings this afternoon, and what's the weather forecast for that time?"
2. The **Host Application** uses the LLM to interpret the user's request and determines it needs to:
    - Check the user's calendar for meetings this afternoon (**calendar tool**)
    - Get the weather forecast for the meeting time (**weather tool**)
3. The host:
    - Uses **Client 1** to connect to **Server 1 (Calendar Tool)**, which returns:  
      "You have a meeting at 3:00 PM."
    - Uses **Client 2** to connect to **Server 2 (Weather Tool)**, which returns:  
      "The forecast at 3:00 PM is sunny, 75°F."
4. Each client only communicates with its assigned server. The calendar server never sees weather data, and vice versa.
5. The **Host aggregates the results** and presents:
    - "You have a meeting at 3:00 PM. The weather at that time is expected to be sunny, 75°F."