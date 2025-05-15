### Features

MCP enables applications to leverage a variety of powerful features by connecting to different types of servers and clients. These features allow AI-powered assistants to perform useful actions, retrieve information, and interact with external systems in a standardized way.

---

#### Server Features

- **Resources:**  
  Structured data or contextual information that a server can provide to the client.  
  - **Local or Remote:** Resources can come from local files, databases, or remote/cloud services—any data source the server can access.
  - **How it works:** The server exposes data (e.g., files, database tables, API results) as resources, which the client/LLM can browse, reference, or subscribe to for updates.
  *Examples:*  
  - Exposing a list of files in a local project folder  
  - Presenting customer records from a remote database as a resource

- **Tools:**  
  Functions or actions that the AI assistant can invoke via the MCP protocol.  
  - **How it works:** Tools are interactive operations—such as running a query, formatting code, or sending a notification—that the LLM can call with specific parameters.
  *Examples:*  
  - A "searchDatabase" tool lets the LLM request "find all customers in California" and get results on demand.

> **Tip:**  
> Use a resource for static or subscribable data; use a tool for dynamic, parameterized queries or actions.

- **Prompts:**  
  Templated messages or workflows provided by the server to guide the LLM's behavior or user interactions.  
  - **How it works:** Prompts standardize and streamline common tasks, ensuring consistency and best practices in how the LLM interacts with users or data.
  *Examples:*  
  - A prompt template for summarizing a document  
  - A workflow for onboarding a new user

---

#### Client Features

- **Sampling:**  
  The ability for the server to request the client to generate a completion or response from the LLM (i.e., to "sample" text or data).  
  - **How it works:** Sampling enables advanced workflows where the server can leverage the client's LLM access for tasks like summarization, drafting, or decision-making—without needing its own LLM API keys.
  *Examples:*  
  - A server asks the client to use its LLM to summarize a document or generate a draft email as part of a larger workflow.

- **Roots:**  
  A way for the client to define and expose the boundaries of accessible directories and files to the server.  
  - **How it works:** Roots provide fine-grained control over what parts of the filesystem a server can access, enhancing security and privacy.
  *Examples:*  
  - A client exposes only the "/projects/my-app" directory to a code analysis server, preventing access to other files.
---