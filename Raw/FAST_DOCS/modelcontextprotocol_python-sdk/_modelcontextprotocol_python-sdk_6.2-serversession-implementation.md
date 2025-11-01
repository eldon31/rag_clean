ServerSession Implementation | modelcontextprotocol/python-sdk | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 27 September 2025 ([146d7e](https://github.com/modelcontextprotocol/python-sdk/commits/146d7efb))

- [Overview](modelcontextprotocol/python-sdk/1-overview.md)
- [Installation & Dependencies](modelcontextprotocol/python-sdk/1.1-installation-and-dependencies.md)
- [Key Concepts](modelcontextprotocol/python-sdk/1.2-key-concepts.md)
- [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md)
- [FastMCP Server Architecture](modelcontextprotocol/python-sdk/2.1-fastmcp-server-architecture.md)
- [Tool Management](modelcontextprotocol/python-sdk/2.2-tool-management.md)
- [Resource & Prompt Management](modelcontextprotocol/python-sdk/2.3-resource-and-prompt-management.md)
- [Function Introspection & Structured Output](modelcontextprotocol/python-sdk/2.4-function-introspection-and-structured-output.md)
- [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md)
- [ClientSession Core](modelcontextprotocol/python-sdk/3.1-clientsession-core.md)
- [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md)
- [Client Authentication](modelcontextprotocol/python-sdk/3.3-client-authentication.md)
- [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md)
- [Protocol Types & JSON-RPC](modelcontextprotocol/python-sdk/4.1-protocol-types-and-json-rpc.md)
- [Session Management](modelcontextprotocol/python-sdk/4.2-session-management.md)
- [Context & Progress Reporting](modelcontextprotocol/python-sdk/4.3-context-and-progress-reporting.md)
- [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md)
- [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md)
- [Server-Sent Events (SSE) Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md)
- [STDIO Transport](modelcontextprotocol/python-sdk/5.3-stdio-transport.md)
- [Transport Security](modelcontextprotocol/python-sdk/5.4-transport-security.md)
- [Low-Level Server Implementation](modelcontextprotocol/python-sdk/6-low-level-server-implementation.md)
- [Low-Level Server Architecture](modelcontextprotocol/python-sdk/6.1-low-level-server-architecture.md)
- [ServerSession Implementation](modelcontextprotocol/python-sdk/6.2-serversession-implementation.md)
- [Authentication & Security](modelcontextprotocol/python-sdk/7-authentication-and-security.md)
- [OAuth 2.0 System](modelcontextprotocol/python-sdk/7.1-oauth-2.0-system.md)
- [Development Tools & CLI](modelcontextprotocol/python-sdk/8-development-tools-and-cli.md)
- [MCP CLI Commands](modelcontextprotocol/python-sdk/8.1-mcp-cli-commands.md)
- [Development Environment](modelcontextprotocol/python-sdk/8.2-development-environment.md)
- [Claude Desktop Integration](modelcontextprotocol/python-sdk/8.3-claude-desktop-integration.md)
- [Examples & Tutorials](modelcontextprotocol/python-sdk/9-examples-and-tutorials.md)
- [Server Examples](modelcontextprotocol/python-sdk/9.1-server-examples.md)
- [Client Examples](modelcontextprotocol/python-sdk/9.2-client-examples.md)

Menu

# ServerSession Implementation

Relevant source files

- [src/mcp/server/models.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/models.py)
- [src/mcp/server/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py)
- [tests/server/test\_session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_session.py)

The ServerSession class provides the core session management functionality for MCP servers, handling individual client connections and managing bidirectional communication between servers and clients. It serves as the low-level foundation that higher-level server frameworks like FastMCP build upon for managing protocol-compliant client interactions.

For information about the high-level FastMCP framework that uses ServerSession internally, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For details about the underlying BaseSession architecture, see [Session Management](modelcontextprotocol/python-sdk/4.2-session-management.md).

## Architecture Overview

ServerSession extends the BaseSession class with server-specific functionality, implementing the server side of the MCP protocol communication pattern.

```
```

Sources: [src/mcp/server/session.py71-79](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L71-L79) [src/mcp/server/session.py58-62](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L58-L62) [src/mcp/server/models.py14-21](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/models.py#L14-L21)

## Session Lifecycle and Initialization

ServerSession manages a strict initialization protocol that ensures proper MCP handshake before allowing most operations.

### Initialization States

The session progresses through three distinct states during its lifecycle:

| State            | Description                                   | Allowed Operations             |
| ---------------- | --------------------------------------------- | ------------------------------ |
| `NotInitialized` | Initial state before any client communication | Ping requests only             |
| `Initializing`   | During initialization handshake               | Ping requests only             |
| `Initialized`    | Ready for full MCP protocol operations        | All requests and notifications |

```
```

Sources: [src/mcp/server/session.py58-62](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L58-L62) [src/mcp/server/session.py142-171](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L142-L171) [src/mcp/server/session.py173-181](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L173-L181)

### Initialization Protocol

The initialization process follows the MCP specification:

1. **Client sends InitializeRequest**: Contains protocol version, capabilities, and client info
2. **Server responds with InitializeResult**: Confirms protocol version and advertises server capabilities
3. **Client sends InitializedNotification**: Signals readiness to begin normal operations

```
```

Sources: [src/mcp/server/session.py144-165](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L144-L165) [src/mcp/server/session.py177-178](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L177-L178)

## Client Capability Management

ServerSession provides capability checking to ensure servers only use features supported by the connected client.

### Capability Checking Logic

The `check_client_capability()` method validates whether a client supports specific MCP capabilities:

```
```

Sources: [src/mcp/server/session.py105-136](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L105-L136)

## Message Processing Architecture

ServerSession handles both incoming messages from clients and outgoing messages to clients through dedicated processing pipelines.

### Incoming Message Flow

```
```

Sources: [src/mcp/server/session.py138-140](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L138-L140) [src/mcp/server/session.py326-327](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L326-L327) [src/mcp/server/session.py329-333](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L329-L333)

### Request Validation

All incoming requests except ping are validated against the initialization state:

```
```

Sources: [src/mcp/server/session.py169-171](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L169-L171)

## Server-to-Client Communication Methods

ServerSession provides a comprehensive set of methods for servers to communicate with clients, covering all major MCP protocol operations.

### Notification Methods

| Method                         | Purpose                      | MCP Notification Type             |
| ------------------------------ | ---------------------------- | --------------------------------- |
| `send_log_message()`           | Send log entries to client   | `LoggingMessageNotification`      |
| `send_resource_updated()`      | Notify resource changes      | `ResourceUpdatedNotification`     |
| `send_progress_notification()` | Report operation progress    | `ProgressNotification`            |
| `send_resource_list_changed()` | Signal resource list updates | `ResourceListChangedNotification` |
| `send_tool_list_changed()`     | Signal tool list updates     | `ToolListChangedNotification`     |
| `send_prompt_list_changed()`   | Signal prompt list updates   | `PromptListChangedNotification`   |

Sources: [src/mcp/server/session.py183-202](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L183-L202) [src/mcp/server/session.py204-212](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L204-L212) [src/mcp/server/session.py291-312](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L291-L312) [src/mcp/server/session.py314-324](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L314-L324)

### Request Methods

ServerSession can initiate requests to clients for advanced MCP operations:

```
```

Sources: [src/mcp/server/session.py214-247](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L214-L247) [src/mcp/server/session.py249-254](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L249-L254) [src/mcp/server/session.py256-282](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L256-L282) [src/mcp/server/session.py284-289](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L284-L289)

## Integration with MCP Protocol

ServerSession implements the server side of the complete MCP protocol specification, handling message routing and protocol compliance.

### Protocol Message Types

```
```

Sources: [src/mcp/server/session.py71-79](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L71-L79)

### Stateless Mode Support

ServerSession supports stateless operation for scenarios where session persistence is not required:

```
```

In stateless mode, the session immediately transitions to `Initialized` state, bypassing the normal MCP initialization handshake.

Sources: [src/mcp/server/session.py88-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L88-L93)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [ServerSession Implementation](#serversession-implementation.md)
- [Architecture Overview](#architecture-overview.md)
- [Session Lifecycle and Initialization](#session-lifecycle-and-initialization.md)
- [Initialization States](#initialization-states.md)
- [Initialization Protocol](#initialization-protocol.md)
- [Client Capability Management](#client-capability-management.md)
- [Capability Checking Logic](#capability-checking-logic.md)
- [Message Processing Architecture](#message-processing-architecture.md)
- [Incoming Message Flow](#incoming-message-flow.md)
- [Request Validation](#request-validation.md)
- [Server-to-Client Communication Methods](#server-to-client-communication-methods.md)
- [Notification Methods](#notification-methods.md)
- [Request Methods](#request-methods.md)
- [Integration with MCP Protocol](#integration-with-mcp-protocol.md)
- [Protocol Message Types](#protocol-message-types.md)
- [Stateless Mode Support](#stateless-mode-support.md)
