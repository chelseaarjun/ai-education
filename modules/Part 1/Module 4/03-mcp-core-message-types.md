##Message Types

---

### Overview

JSON-RPC 2.0 is a lightweight, stateless remote procedure call (RPC) protocol that uses JSON for encoding messages and is widely used for structured communication between distributed systems.

The Model Context Protocol (MCP) uses a set of standardized message types, based on the JSON-RPC 2.0 protocol, to enable structured, reliable, and extensible communication between hosts, clients, and servers. Understanding these message types is essential for building and integrating MCP-compliant tools and applications.

---

### Main Message Types

MCP defines four primary message types:

- **Request**
- **Response**
- **Error**
- **Notification**

Each type serves a specific purpose in the protocol and follows a well-defined structure.
---

#### Request
- Used to ask another component to perform an action or provide information.
- **Required fields:**
  - `id`: MUST be a unique identifier for the request (number or string).
  - `method`: MUST be a string specifying the operation to invoke.
  - `params`: MAY be included (object or array), depending on the method.
- Always expects a corresponding response.
- **Example:**
  ```json
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "resources/read",
    "params": { "id": "abc123" }
  }
  ```

#### Response
- Sent in reply to a request, containing the result of the requested action.
- **Required fields:**
  - `id`: MUST match the `id` of the original request.
  - `result`: MUST be included if the request was successful (result MAY follow JSON structure).
  - `error`: MUST NOT be included if `result` is present.
- **Example:**
  ```json
  {
    "jsonrpc": "2.0",
    "id": 1,
    "result": { "id": "abc123", "name": "Resource Name", "data": "..." }
  }
  ```

#### Error
- Sent if a request cannot be fulfilled due to an error (e.g., invalid parameters, method not found).
- **Required fields:**
  - `id`: MUST match the `id` of the original request.
  - `error`: MUST be an object with at least `code` (number) and `message` (string).
  - `result`: MUST NOT be included if `error` is present.
- Includes an error code and message for debugging and handling.
- **Common error codes:**
  - `-32700` ParseError: Invalid JSON was received by the server.
  - `-32600` InvalidRequest: The JSON sent is not a valid Request object.
  - `-32601` MethodNotFound: The method does not exist or is not available.
  - `-32602` InvalidParams: Invalid method parameter(s).
  - `-32603` InternalError: Internal JSON-RPC error.
  - (MCP and applications may define additional codes above `-32000` for custom errors.)
- **Example:**
  ```json
  {
    "jsonrpc": "2.0",
    "id": 1,
    "error": { "code": -32601, "message": "Method not found" }
  }
  ```

#### Notification
- One-way message that does not expect a response.
- **Required fields:**
  - `jsonrpc`: MUST be the string "2.0".
  - `method`: MUST be a string specifying the event or action.
  - `params`: MAY be included (object or array), depending on the method.
  - `id`: MUST NOT be included.
- Used for events or updates (e.g., resource changed, progress update).
- **Example:**
  ```json
  {
    "jsonrpc": "2.0",
    "method": "notifications/resources/updated",
    "params": { "resourceId": "abc123" }
  }
  ```

---

### Additional Notes

- **Batching:** MCP (via JSON-RPC 2.0) supports sending multiple requests or notifications in a single batch for efficiency.
- **Cancellation:** MCP supports cancelling in-progress requests using a special notification (e.g., `"notifications/cancelled`), allowing clients or servers to request that a long-running operation be stopped if it is no longer needed. [Learn more](https://modelcontextprotocol.io/specification/2025-03-26/basic/utilities/cancellation)
- **Extensibility:** Custom methods and parameters can be defined as long as they adhere to the protocol's structure.

---

**References:**
- [MCP Specification: Core Message Types](https://modelcontextprotocol.io/specification/2025-03-26)
- [MCP Protocol Schema on GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/main/schema)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)