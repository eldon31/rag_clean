Session Management | modelcontextprotocol/python-sdk | DeepWiki

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

# Session Management

Relevant source files

- [src/mcp/client/\_\_main\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/__main__.py)
- [src/mcp/client/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py)
- [src/mcp/server/models.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/models.py)
- [src/mcp/server/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py)
- [src/mcp/shared/memory.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/memory.py)
- [src/mcp/shared/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py)
- [tests/client/test\_logging\_callback.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_logging_callback.py)
- [tests/client/test\_session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_session.py)
- [tests/server/test\_session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_session.py)

Session management in the MCP Python SDK provides the foundational infrastructure for maintaining communication state between clients and servers. This system handles message correlation, request/response tracking, protocol initialization, and connection lifecycle management. For specific client-side session usage, see [ClientSession Core](modelcontextprotocol/python-sdk/3.1-clientsession-core.md). For protocol message types and JSON-RPC implementation details, see [Protocol Types & JSON-RPC](modelcontextprotocol/python-sdk/4.1-protocol-types-and-json-rpc.md).

## BaseSession Architecture

The `BaseSession` class forms the core of MCP's session management system, providing message correlation, stream management, and request/response tracking for both client and server implementations.

### Message Correlation System

```
```

The BaseSession maintains request correlation through a sophisticated tracking system that maps request IDs to response streams, ensuring that responses are delivered to the correct waiting coroutines even in highly concurrent scenarios.

Sources: [src/mcp/shared/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py) [tests/shared/test\_session.py36-46](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_session.py#L36-L46) [tests/client/test\_resource\_cleanup.py12-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_resource_cleanup.py#L12-L61)

### Stream Management and Cleanup

BaseSession manages memory object streams for bidirectional communication, with automatic cleanup to prevent resource leaks:

```
```

The session ensures proper stream cleanup even when exceptions occur during request transmission, preventing memory leaks in long-running connections.

Sources: [tests/client/test\_resource\_cleanup.py13-56](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_resource_cleanup.py#L13-L56) [src/mcp/shared/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py)

## ServerSession Implementation

The `ServerSession` class extends BaseSession to provide server-specific functionality, including initialization state management, client capability checking, and various notification methods.

### Initialization State Flow

```
```

The ServerSession enforces a strict initialization protocol where most requests are blocked until the initialization handshake completes, with ping requests being the only exception.

Sources: [src/mcp/server/session.py58-62](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L58-L62) [src/mcp/server/session.py167-179](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L167-L179) [tests/server/test\_session.py219-283](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_session.py#L219-L283)

### Client Capability Checking

ServerSession provides a comprehensive capability checking system that allows servers to adapt their behavior based on client capabilities:

| Capability Type | Check Method                | Purpose                      |
| --------------- | --------------------------- | ---------------------------- |
| `roots`         | `check_client_capability()` | File system root access      |
| `sampling`      | `check_client_capability()` | LLM sampling support         |
| `elicitation`   | `check_client_capability()` | User input elicitation       |
| `experimental`  | `check_client_capability()` | Custom experimental features |

```
```

Sources: [src/mcp/server/session.py105-136](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L105-L136) [src/mcp/server/session.py8-34](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L8-L34)

## Session Communication Methods

ServerSession provides specialized methods for different types of server-to-client communication:

### Notification Methods

| Method                         | Purpose                | Message Type                      |
| ------------------------------ | ---------------------- | --------------------------------- |
| `send_log_message()`           | Server logging         | `LoggingMessageNotification`      |
| `send_resource_updated()`      | Resource change events | `ResourceUpdatedNotification`     |
| `send_progress_notification()` | Operation progress     | `ProgressNotification`            |
| `send_resource_list_changed()` | Resource list updates  | `ResourceListChangedNotification` |
| `send_tool_list_changed()`     | Tool list updates      | `ToolListChangedNotification`     |
| `send_prompt_list_changed()`   | Prompt list updates    | `PromptListChangedNotification`   |

### Request Methods

ServerSession can also send requests to clients for advanced capabilities:

| Method             | Purpose           | Result Type           |
| ------------------ | ----------------- | --------------------- |
| `create_message()` | LLM sampling      | `CreateMessageResult` |
| `list_roots()`     | File system roots | `ListRootsResult`     |
| `elicit()`         | User input        | `ElicitResult`        |
| `send_ping()`      | Connection health | `EmptyResult`         |

Sources: [src/mcp/server/session.py181-323](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L181-L323)

## Request Cancellation and Error Handling

The session management system provides robust cancellation and error handling capabilities:

```
```

The cancellation system ensures that servers remain functional after request cancellations and that pending requests are properly cleaned up when connections are lost.

Sources: [tests/shared/test\_session.py48-123](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_session.py#L48-L123) [tests/server/test\_cancel\_handling.py25-111](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_cancel_handling.py#L25-L111) [tests/shared/test\_session.py125-171](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_session.py#L125-L171)

## Integration with Server Framework

ServerSession integrates closely with the broader MCP server framework:

```
```

ServerSession serves as the communication bridge between the protocol layer and application logic, handling the low-level details of message transmission while providing a clean interface for server implementations.

Sources: [src/mcp/server/session.py83-100](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py#L83-L100) [src/mcp/server/models.py13-18](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/models.py#L13-L18) [tests/server/test\_session.py32-81](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_session.py#L32-L81)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Session Management](#session-management.md)
- [BaseSession Architecture](#basesession-architecture.md)
- [Message Correlation System](#message-correlation-system.md)
- [Stream Management and Cleanup](#stream-management-and-cleanup.md)
- [ServerSession Implementation](#serversession-implementation.md)
- [Initialization State Flow](#initialization-state-flow.md)
- [Client Capability Checking](#client-capability-checking.md)
- [Session Communication Methods](#session-communication-methods.md)
- [Notification Methods](#notification-methods.md)
- [Request Methods](#request-methods.md)
- [Request Cancellation and Error Handling](#request-cancellation-and-error-handling.md)
- [Integration with Server Framework](#integration-with-server-framework.md)
