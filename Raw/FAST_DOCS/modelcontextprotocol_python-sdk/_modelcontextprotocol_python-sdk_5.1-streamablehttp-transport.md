StreamableHTTP Transport | modelcontextprotocol/python-sdk | DeepWiki

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

# StreamableHTTP Transport

Relevant source files

- [src/mcp/client/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py)
- [src/mcp/client/streamable\_http.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py)
- [src/mcp/server/streamable\_http.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py)
- [src/mcp/server/streamable\_http\_manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py)
- [tests/client/test\_notification\_response.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_notification_response.py)
- [tests/server/test\_streamable\_http\_manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_streamable_http_manager.py)
- [tests/shared/test\_streamable\_http.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_streamable_http.py)

The StreamableHTTP Transport provides HTTP-based bidirectional communication for MCP using POST requests and Server-Sent Events (SSE) streaming. This transport enables stateful session management, optional resumability, and authentication support for both clients and servers.

For SSE-only transport functionality, see [Server-Sent Events (SSE) Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md). For stdio-based process communication, see [STDIO Transport](modelcontextprotocol/python-sdk/5.3-stdio-transport.md). For WebSocket communication, see [WebSocket Transport](modelcontextprotocol/python-sdk/5.4-transport-security.md).

## Overview

StreamableHTTP transport implements the MCP protocol over HTTP using a hybrid approach: clients send messages via HTTP POST requests, while servers respond using either JSON responses or SSE streams. The transport supports both stateful sessions with resumability and stateless request-response patterns.

**Key Features:**

- HTTP POST requests for client-to-server communication
- SSE streaming for server-to-client communication
- Session management with unique session IDs
- Optional resumability via `EventStore` interface
- Authentication support through `httpx.Auth`
- DNS rebinding protection via `TransportSecurityMiddleware`
- Both stateful and stateless operation modes

Sources: [src/mcp/client/streamable\_http.py1-8](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L1-L8) [src/mcp/server/streamable\_http.py1-8](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L1-L8)

## Architecture Overview

```
```

**StreamableHTTP Transport Architecture**

Sources: [src/mcp/client/streamable\_http.py74-108](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L74-L108) [src/mcp/server/streamable\_http.py122-175](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L122-L175) [src/mcp/server/streamable\_http\_manager.py29-79](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L29-L79)

## Client-Side Implementation

The client-side implementation centers around the `StreamableHTTPTransport` class and the `streamablehttp_client` async context manager.

### StreamableHTTPTransport Class

The `StreamableHTTPTransport` class handles the client-side HTTP communication with session management and protocol negotiation:

| Component          | Responsibility                                  |
| ------------------ | ----------------------------------------------- |
| Session Management | Tracks session ID and protocol version          |
| Request Handling   | Manages POST requests and SSE responses         |
| Authentication     | Integrates with `httpx.Auth` for authentication |
| Resumption         | Supports request resumption with event IDs      |

**Key Methods:**

- `post_writer()` - Handles outgoing requests via HTTP POST
- `handle_get_stream()` - Manages incoming SSE streams from server
- `terminate_session()` - Explicitly terminates session via DELETE request
- `_handle_post_request()` - Processes individual POST requests
- `_handle_resumption_request()` - Handles resumption with `Last-Event-ID`

**Key Attributes:**

- `session_id` - Current session identifier
- `protocol_version` - Negotiated protocol version
- `request_headers` - Base headers for all requests

### Message Flow Patterns

```
```

**StreamableHTTP Message Flow**

Sources: [src/mcp/client/streamable\_http.py366-422](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L366-L422) [src/mcp/client/streamable\_http.py192-218](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L192-L218) [src/mcp/client/streamable\_http.py423-438](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L423-L438) [src/mcp/server/streamable\_http.py309-507](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L309-L507) [src/mcp/server/streamable\_http.py508-599](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L508-L599) [src/mcp/server/streamable\_http.py600-622](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L600-L622)

### Client Context Manager Usage

The primary client interface is the `streamablehttp_client` async context manager:

```
```

Sources: [src/mcp/client/streamable\_http.py444-514](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L444-L514)

## Server-Side Implementation

The server-side implementation provides two main components: `StreamableHTTPServerTransport` for individual connections and `StreamableHTTPSessionManager` for managing multiple sessions.

### StreamableHTTPServerTransport

The `StreamableHTTPServerTransport` class handles individual HTTP connections with support for both SSE streaming and JSON responses:

**Operating Modes:**

- **SSE Mode** (default): Responses are streamed via Server-Sent Events
- **JSON Mode**: Single JSON responses for each request (controlled by `is_json_response_enabled`)

**HTTP Method Handling:**

- `POST` - Processes JSON-RPC messages via `_handle_post_request()`
- `GET` - Establishes SSE streams for server-initiated messages via `_handle_get_request()`
- `DELETE` - Terminates sessions explicitly via `_handle_delete_request()`

**Key Features:**

- Session ID validation using `SESSION_ID_PATTERN`
- Request stream management with `_request_streams` dictionary
- Event storage integration via `EventStore` interface
- Security validation through `TransportSecurityMiddleware`
- Memory stream cleanup with `_clean_up_memory_streams()`

### Session Management Architecture

```
```

**Session Management Components**

Sources: [src/mcp/server/streamable\_http\_manager.py70-79](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L70-L79) [src/mcp/server/streamable\_http\_manager.py146-194](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L146-L194) [src/mcp/server/streamable\_http\_manager.py195-280](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L195-L280)

### Stateful vs Stateless Modes

The session manager supports two operation modes:

| Mode      | Session Tracking | State Persistence | Use Case                         |
| --------- | ---------------- | ----------------- | -------------------------------- |
| Stateful  | Yes              | Between requests  | Long-lived connections           |
| Stateless | No               | None              | Serverless/stateless deployments |

**Stateful Mode:** Sessions are tracked with UUIDs, allowing resumption and persistent state. **Stateless Mode:** Each request creates a fresh transport instance with no state retention.

Sources: [src/mcp/server/streamable\_http\_manager.py54-68](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L54-L68)

## Event Storage and Resumability

StreamableHTTP transport supports optional resumability through the `EventStore` interface, allowing clients to reconnect and receive missed events.

### EventStore Interface

```
```

**Event Storage Architecture**

**Resumption Flow:**

1. Client includes `Last-Event-ID` header in GET request via `LAST_EVENT_ID_HEADER`
2. Server calls `EventStore.replay_events_after()` in `_replay_events()`
3. Missed events are replayed via SSE using `_create_event_data()`
4. New events continue from current point with automatic event ID generation

**Stream Management:**

- Events are stored per `StreamId` (either request ID or `GET_STREAM_KEY`)
- Message router distributes events to appropriate streams based on request correlation
- Event IDs are generated by the `EventStore` implementation

Sources: [src/mcp/server/streamable\_http.py84-120](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L84-L120) [src/mcp/server/streamable\_http.py728-798](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L728-L798) [src/mcp/server/streamable\_http.py829-880](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L829-L880)

## Security Features

StreamableHTTP transport includes DNS rebinding protection through the `TransportSecurityMiddleware`.

### Security Validation

The transport validates incoming requests against security policies via `TransportSecurityMiddleware`:

| Validation     | Scope         | Purpose                                      |
| -------------- | ------------- | -------------------------------------------- |
| Host Header    | All requests  | Prevent DNS rebinding attacks                |
| Origin Header  | CORS requests | Validate request origin                      |
| Content-Type   | POST requests | Ensure proper JSON content                   |
| Accept Headers | POST requests | Validate client accepts required media types |

**Security Integration:**

- `TransportSecurityMiddleware` is instantiated in `StreamableHTTPServerTransport.__init__()`
- Validation occurs in `handle_request()` via `_security.validate_request()`
- Failed validation returns error responses before processing

**Configuration Example:**

```
```

Sources: [src/mcp/server/streamable\_http.py27-30](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L27-L30) [src/mcp/server/streamable\_http.py166](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L166-L166) [src/mcp/server/streamable\_http.py268-272](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L268-L272)

## Protocol Implementation Details

### Session ID Management

Session IDs are validated against a strict pattern to ensure security:

- **Pattern:** Visible ASCII characters (0x21-0x7E)
- **Generation:** UUID hex format (32 characters)
- **Validation:** `SESSION_ID_PATTERN.fullmatch()` check

### Protocol Version Negotiation

The transport negotiates protocol versions during initialization:

1. Client sends `initialize` request
2. Server responds with `InitializeResult` containing `protocolVersion`
3. Subsequent requests include `mcp-protocol-version` header

### Headers and Content Types

| Header                 | Constant                      | Purpose                | Example                               |
| ---------------------- | ----------------------------- | ---------------------- | ------------------------------------- |
| `mcp-session-id`       | `MCP_SESSION_ID_HEADER`       | Session identification | `abc123def456...`                     |
| `mcp-protocol-version` | `MCP_PROTOCOL_VERSION_HEADER` | Protocol version       | `2025-03-26`                          |
| `last-event-id`        | `LAST_EVENT_ID_HEADER`        | Resumption token       | `event-123`                           |
| `content-type`         | `CONTENT_TYPE`                | Request format         | `application/json`                    |
| `accept`               | `ACCEPT`                      | Response formats       | `application/json, text/event-stream` |

**Content Type Constants:**

- `CONTENT_TYPE_JSON` = `"application/json"`
- `CONTENT_TYPE_SSE` = `"text/event-stream"`
- `JSON` = `"application/json"` (client)
- `SSE` = `"text/event-stream"` (client)

**Session ID Validation:**

- Pattern: `SESSION_ID_PATTERN` validates visible ASCII characters (0x21-0x7E)
- Generated using `uuid4().hex` for new sessions
- Validated on transport initialization and request processing

Sources: [src/mcp/server/streamable\_http.py50-64](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L50-L64) [src/mcp/client/streamable\_http.py42-51](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L42-L51) [src/mcp/server/streamable\_http.py62-64](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L62-L64)

## Integration with ASGI

StreamableHTTP transport integrates with ASGI applications through the session manager:

```
```

The session manager's `run()` method provides lifecycle management for all sessions and can only be called once per instance.

Sources: [src/mcp/server/streamable\_http\_manager.py80-120](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L80-L120) [src/mcp/server/streamable\_http\_manager.py121-145](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L121-L145)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [StreamableHTTP Transport](#streamablehttp-transport.md)
- [Overview](#overview.md)
- [Architecture Overview](#architecture-overview.md)
- [Client-Side Implementation](#client-side-implementation.md)
- [StreamableHTTPTransport Class](#streamablehttptransport-class.md)
- [Message Flow Patterns](#message-flow-patterns.md)
- [Client Context Manager Usage](#client-context-manager-usage.md)
- [Server-Side Implementation](#server-side-implementation.md)
- [StreamableHTTPServerTransport](#streamablehttpservertransport.md)
- [Session Management Architecture](#session-management-architecture.md)
- [Stateful vs Stateless Modes](#stateful-vs-stateless-modes.md)
- [Event Storage and Resumability](#event-storage-and-resumability.md)
- [EventStore Interface](#eventstore-interface.md)
- [Security Features](#security-features.md)
- [Security Validation](#security-validation.md)
- [Protocol Implementation Details](#protocol-implementation-details.md)
- [Session ID Management](#session-id-management.md)
- [Protocol Version Negotiation](#protocol-version-negotiation.md)
- [Headers and Content Types](#headers-and-content-types.md)
- [Integration with ASGI](#integration-with-asgi.md)
