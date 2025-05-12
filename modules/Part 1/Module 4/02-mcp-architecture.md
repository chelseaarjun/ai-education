## MCP Architecture and Protocol Specification

---

### 1. MCP System Overview

#### High-Level Architecture: Host, Client, and Server

MCP is built on a modular, client-server architecture with three main roles:

- **Host:**  
  The **central application** that manages all connections, enforces security, and coordinates LLM interactions.  
  - Typically, the host is an application that interacts with an **LLM** (e.g., an AI-powered IDE, chat platform, or assistant interface).
  - The host **creates and manages multiple clients**—each client connects to a different server for a specific capability (such as code search or documentation lookup).
  - The host is responsible for **user consent, security, and orchestration** of all interactions.
  - **Example:** An AI-powered IDE that lets users ask questions about their code and documentation. The IDE (**host**) manages which tools (**servers**) are used to answer the user's query.

- **Client:**  
  A **connector** within the host that establishes and manages a session with a specific server.  
  - Each client maintains a **1:1 relationship** with a server and handles **protocol negotiation, message routing, and capability exchange**.
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

#### How It Works (At a Glance): Practical Example

**Scenario:**  
A developer is using an **AI-powered IDE (the host)** that integrates both a **code search tool** and a **documentation lookup tool**.

**Flow (as shown in the diagram):**

```
[User] → [Host Application]
                ↓
         [Client Connector] ←→ [Server 1: Code Search]
                ↓
         [Client Connector] ←→ [Server 2: Documentation]
```

1. **User** asks the AI assistant in the IDE: "Find where the function `processOrder` is defined and show me the related documentation."
2. **Host Application** receives the request and determines it needs to use two different capabilities: **code search** and **documentation lookup**.
3. The host uses:
   - **Client 1** to connect to **Server 1 (Code Search)**, which returns the location of `processOrder`.
   - **Client 2** to connect to **Server 2 (Documentation)**, which returns the relevant documentation.
4. Each client only communicates with its assigned server, ensuring that **code search data** and **documentation data** remain **isolated and secure**.
5. The host **aggregates the results** and presents them to the user, maintaining control over what data is shared and how tools are used.

**Key Points:**
- The **host** manages user consent, security, and orchestration.
- **Clients** act as secure bridges, each handling a specific capability and maintaining strict boundaries.
- **Servers** provide focused, composable capabilities and never have access to the full user context or each other's data.

---