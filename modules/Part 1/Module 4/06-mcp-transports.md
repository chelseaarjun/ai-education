# Transport Protocols

---

## Transport Protocols in MCP

MCP supports two main transport protocols for communication between clients and servers:

- **stdio:**  
  The client launches the MCP server as a subprocess and exchanges messages using standard input and output streams. This is fast, local, and ideal for tools running on the same machine.

- **Streamable HTTP:**  
  The client and server communicate over HTTP using POST and GET requests, with specific headers to manage content and sessions:
  - **POST:**  
    - The client sends one or more JSON-RPC messages in a POST request with `Content-Type: application/json`.
    - The `Accept` header should include both `application/json` and `text/event-stream` to indicate the client can handle either a single response or a streaming response.
    - The server responds with `Content-Type: application/json` for a single response, or `Content-Type: text/event-stream` for streaming multiple messages.
    - If a session is established, both client and server include the `Mcp-Session-Id` header in their requests and responses.
  - **GET:**  
    - The client can open a persistent connection by sending a GET request with `Accept: text/event-stream`, allowing the server to push messages as events occur.
    - The server responds with `Content-Type: text/event-stream` to confirm a streaming connection.
    - The `Mcp-Session-Id` header is also used if a session is active.

This approach enables both single-response and real-time, streaming communication, making MCP suitable for a wide range of use cases.

> For more details, see the [MCP Transports documentation](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).

---

## Authorization in MCP (2025-03-26 Spec)

- **Authorization is optional in MCP, but for HTTP-based transports, it is strongly recommended (SHOULD) for security, especially in production environments.**
- OAuth 2.1 is the recommended method for secure authorization and access control.
- For local (stdio) transports, credentials are typically managed via the environment.
- **Further reading:** See the [MCP Authorization documentation](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) for full details and best practices.

---

## Session Management in MCP

- MCP supports session management to maintain stateful interactions between clients and servers.
- When using Streamable HTTP, the server may assign a unique session ID during initialization (via the `Mcp-Session-Id` header).
- The client must include this session ID in all subsequent requests for the session's duration.
- Sessions can be explicitly terminated by the client or server, ensuring clean resource management and robust error handling.

> For more, see [Session Management in the MCP spec](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#session-management).
