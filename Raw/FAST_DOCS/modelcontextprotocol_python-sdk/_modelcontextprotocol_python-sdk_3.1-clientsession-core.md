ClientSession Core | modelcontextprotocol/python-sdk | DeepWiki

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

# ClientSession Core

Relevant source files

- [src/mcp/client/\_\_main\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/__main__.py)
- [src/mcp/client/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py)
- [src/mcp/shared/memory.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/memory.py)
- [src/mcp/shared/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py)
- [tests/client/test\_logging\_callback.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_logging_callback.py)
- [tests/client/test\_session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_session.py)

The `ClientSession` class provides the high-level client interface for communicating with MCP servers. It manages the complete lifecycle of client-server communication, including session initialization, protocol negotiation, request/response handling, and server-initiated callbacks. This document covers the core session management architecture and message handling system.

For transport-specific client implementations, see [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md). For OAuth authentication in client sessions, see [Client Authentication](modelcontextprotocol/python-sdk/3.3-client-authentication.md).

## Session Architecture Overview

The client session architecture consists of layered components that handle different aspects of MCP communication:

```
```

Sources: [src/mcp/client/session.py101-434](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L101-L434) [src/mcp/shared/session.py159-471](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L159-L471)

## ClientSession Class Structure

The `ClientSession` class extends `BaseSession` with client-specific functionality and type parameters:

```
```

Sources: [src/mcp/client/session.py101-109](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L101-L109) [src/mcp/shared/session.py159-167](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L159-L167) [src/mcp/shared/session.py52-67](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L52-L67)

## Session Initialization Flow

The initialization process establishes communication and negotiates capabilities between client and server:

```
```

The `initialize` method [src/mcp/client/session.py137-174](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L137-L174) performs several key operations:

1. **Capability Advertisement**: Determines client capabilities based on provided callbacks
2. **Protocol Version**: Sends `LATEST_PROTOCOL_VERSION` and validates server response
3. **Initialization Request**: Sends `InitializeRequest` with client info and capabilities
4. **Version Validation**: Ensures server protocol version is in `SUPPORTED_PROTOCOL_VERSIONS`
5. **Completion Notification**: Sends `InitializedNotification` to complete handshake

Sources: [src/mcp/client/session.py137-174](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L137-L174) [tests/client/test\_session.py30-114](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_session.py#L30-L114)

## Request/Response Management

The session manages request/response pairs using a stream-based approach with timeout handling:

| Component             | Purpose                            | Key Methods                              |
| --------------------- | ---------------------------------- | ---------------------------------------- |
| `send_request`        | Send request and wait for response | Type-safe request/response matching      |
| `_response_streams`   | Track pending requests             | Maps request ID to response stream       |
| `_progress_callbacks` | Handle progress updates            | Maps progress token to callback function |
| `RequestResponder`    | Manage server-initiated requests   | Context manager for request lifecycle    |

```
```

The `send_request` method [src/mcp/shared/session.py220-294](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L220-L294) provides:

- **Type Safety**: Generic type parameters ensure request/response type matching
- **Progress Support**: Automatic progress token injection and callback registration
- **Timeout Management**: Request-specific and session-level timeout support
- **Error Handling**: Converts `JSONRPCError` responses to `McpError` exceptions

Sources: [src/mcp/shared/session.py220-294](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L220-L294) [src/mcp/shared/session.py331-436](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L331-L436)

## Server-Initiated Request Handling

The client handles four types of server-initiated requests through configurable callback functions:

```
```

The `_received_request` method [src/mcp/client/session.py388-417](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L388-L417) routes server requests to appropriate callbacks:

- **Sampling Requests**: Handle `CreateMessageRequest` for LLM message generation
- **Elicitation Requests**: Handle `ElicitRequest` for information extraction
- **List Roots Requests**: Handle `ListRootsRequest` for file system roots
- **Ping Requests**: Built-in handler returns `EmptyResult`

Each callback receives a `RequestContext` with session reference and request metadata.

Sources: [src/mcp/client/session.py388-417](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L388-L417) [src/mcp/client/session.py21-96](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L21-L96)

## Tool Calling with Validation

The client provides structured tool calling with automatic output schema validation:

```
```

The tool calling system [src/mcp/client/session.py270-319](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L270-L319) provides:

- **Progress Support**: Optional progress callback for long-running tools
- **Timeout Control**: Per-request timeout override capability
- **Schema Validation**: Automatic validation of structured content against tool output schemas
- **Schema Caching**: Maintains cache of tool output schemas from `list_tools` responses

The `_validate_tool_result` method ensures that tools returning structured content conform to their declared output schemas.

Sources: [src/mcp/client/session.py270-319](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L270-L319) [src/mcp/client/session.py366-382](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L366-L382)

## Notification Handling

The client processes various server notifications through the notification handling system:

| Notification Type            | Handler                  | Purpose                        |
| ---------------------------- | ------------------------ | ------------------------------ |
| `LoggingMessageNotification` | `_logging_callback`      | Process server log messages    |
| `ProgressNotification`       | Progress callback lookup | Update request progress        |
| `CancelledNotification`      | Request cancellation     | Cancel in-flight requests      |
| Generic notifications        | `_received_notification` | Custom notification processing |

```
```

The notification system [src/mcp/shared/session.py377-401](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L377-L401) handles:

- **Logging Notifications**: Forward to configurable logging callback
- **Progress Notifications**: Route to request-specific progress callbacks using progress tokens
- **Cancellation Notifications**: Cancel in-flight requests using `RequestResponder.cancel()`

Sources: [src/mcp/shared/session.py377-401](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L377-L401) [src/mcp/client/session.py426-433](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L426-L433)

## Capability Advertisement

The client dynamically advertises capabilities based on provided callback functions during initialization:

```
```

Capability detection logic [src/mcp/client/session.py137-161](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L137-L161):

- **Sampling**: Advertised if `sampling_callback` is not the default implementation
- **Elicitation**: Advertised if `elicitation_callback` is not the default implementation
- **Roots**: Advertised if `list_roots_callback` is not the default implementation
- **Experimental**: Currently always `None`

The `RootsCapability` includes `listChanged=True` to indicate support for root list change notifications.

Sources: [src/mcp/client/session.py137-161](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L137-L161) [tests/client/test\_session.py356-500](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_session.py#L356-L500)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [ClientSession Core](#clientsession-core.md)
- [Session Architecture Overview](#session-architecture-overview.md)
- [ClientSession Class Structure](#clientsession-class-structure.md)
- [Session Initialization Flow](#session-initialization-flow.md)
- [Request/Response Management](#requestresponse-management.md)
- [Server-Initiated Request Handling](#server-initiated-request-handling.md)
- [Tool Calling with Validation](#tool-calling-with-validation.md)
- [Notification Handling](#notification-handling.md)
- [Capability Advertisement](#capability-advertisement.md)
