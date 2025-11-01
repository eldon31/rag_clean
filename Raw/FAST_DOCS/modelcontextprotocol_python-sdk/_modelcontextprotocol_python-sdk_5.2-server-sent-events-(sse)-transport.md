Server-Sent Events (SSE) Transport | modelcontextprotocol/python-sdk | DeepWiki

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

# Server-Sent Events (SSE) Transport

Relevant source files

- [src/mcp/client/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py)
- [src/mcp/client/streamable\_http.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py)
- [src/mcp/server/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py)
- [tests/client/test\_notification\_response.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_notification_response.py)
- [tests/shared/test\_sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py)

This document covers the Server-Sent Events (SSE) transport implementation for MCP servers, which enables real-time bidirectional communication through a combination of SSE streaming for server-to-client messages and HTTP POST requests for client-to-server messages.

For information about the client-side SSE implementation, see [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md). For HTTP-based transports with session management, see [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md). For security features across all transports, see [Transport Security](modelcontextprotocol/python-sdk/5.4-transport-security.md).

## Architecture Overview

The SSE transport provides a hybrid communication model that combines the real-time capabilities of Server-Sent Events with the reliability of HTTP POST requests for bidirectional MCP communication.

### SSE Transport Architecture

```
```

Sources: [src/mcp/server/sse.py64-250](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L64-L250) [tests/shared/test\_sse.py83-104](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L83-L104)

### Message Flow Architecture

```
```

Sources: [src/mcp/server/sse.py121-249](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L121-L249) [tests/shared/test\_sse.py183-195](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L183-L195)

## SSE Server Transport Implementation

The `SseServerTransport` class provides the core SSE transport functionality through two main ASGI applications.

### Core Components

| Component               | Purpose                        | Implementation                                                                                                                   |
| ----------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `SseServerTransport`    | Main transport class           | [src/mcp/server/sse.py64-79](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L64-L79)     |
| `connect_sse()`         | Handles SSE connection setup   | [src/mcp/server/sse.py122-199](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L122-L199) |
| `handle_post_message()` | Processes client POST requests | [src/mcp/server/sse.py201-249](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L201-L249) |
| Memory Streams          | Internal message passing       | [src/mcp/server/sse.py135-142](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L135-L142) |
| Security Middleware     | Request validation             | [src/mcp/server/sse.py118](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L118-L118)     |

### Transport Initialization

The transport requires an endpoint configuration and optional security settings:

```
```

The endpoint validation ensures only relative paths are accepted to prevent security issues [src/mcp/server/sse.py105-115](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L105-L115)

Sources: [src/mcp/server/sse.py80-120](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L80-L120) [tests/shared/test\_sse.py86-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L86-L89)

### ASGI Integration Pattern

```
```

Sources: [src/mcp/server/sse.py6-37](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L6-L37) [tests/shared/test\_sse.py97-104](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L97-L104)

## Session Management

The SSE transport implements session-based communication using UUID session identifiers and memory streams for message routing.

### Session Lifecycle

1. **Session Creation**: Generated during `connect_sse()` call [src/mcp/server/sse.py144-146](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L144-L146)
2. **Stream Setup**: Memory object streams created for bidirectional communication [src/mcp/server/sse.py135-142](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L135-L142)
3. **Endpoint Communication**: Client receives POST endpoint via initial SSE event [src/mcp/server/sse.py161-168](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L161-L168)
4. **Message Routing**: POST requests routed to correct session via session\_id [src/mcp/server/sse.py216-228](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L216-L228)
5. **Cleanup**: Streams closed when SSE connection terminates [src/mcp/server/sse.py191-193](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L191-L193)

### Session Storage and Routing

```
```

Sources: [src/mcp/server/sse.py77](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L77-L77) [src/mcp/server/sse.py144-146](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L144-L146) [src/mcp/server/sse.py216-228](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L216-L228)

## Security Features

The SSE transport includes built-in security measures to prevent common web vulnerabilities.

### Request Validation

The transport uses `TransportSecurityMiddleware` for DNS rebinding protection and origin validation:

- **Host Header Validation**: Ensures requests target allowed hosts [src/mcp/server/sse.py129](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L129-L129)
- **Origin Header Checking**: Validates request origins for POST requests [src/mcp/server/sse.py206](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L206-L206)
- **Relative Path Enforcement**: Prevents absolute URLs in endpoint configuration [src/mcp/server/sse.py106-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L106-L110)

### Error Handling

The transport provides comprehensive error responses with specific HTTP status codes and messages:

| Error Type          | Status Code | Response Message             | Scenario                                                                                                                                                      |
| ------------------- | ----------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Missing session\_id | 400         | "session\_id is required"    | POST without session parameter [src/mcp/server/sse.py213](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L213-L213)   |
| Invalid session\_id | 400         | "Invalid session ID"         | Malformed UUID in request [src/mcp/server/sse.py221](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L221-L221)        |
| Session not found   | 404         | "Could not find session"     | Request for non-existent session [src/mcp/server/sse.py227](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L227-L227) |
| Parse error         | 400         | "Could not parse message"    | Invalid JSON in message body [src/mcp/server/sse.py238](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L238-L238)     |
| Validation failure  | Variable    | Security middleware response | DNS rebinding protection [src/mcp/server/sse.py129-132](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L129-L132)     |

### Client-Side Error Handling

The SSE client implements robust error handling for various failure scenarios:

- **Origin Mismatch**: Raises `ValueError` when endpoint origin doesn't match connection origin [src/mcp/client/sse.py85-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L85-L89)
- **Message Parsing**: Catches exceptions during JSON parsing and forwards to error stream [src/mcp/client/sse.py99-102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L99-L102)
- **Connection Failures**: Automatically propagates HTTP connection errors through the read stream [src/mcp/client/sse.py108-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L108-L110)
- **Timeout Handling**: Configurable `sse_read_timeout` for SSE event reading [src/mcp/client/sse.py28](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L28-L28)

Sources: [src/mcp/server/sse.py210-241](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L210-L241) [src/mcp/client/sse.py85-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L85-L110)

## Client Integration

The SSE transport integrates with the client-side `sse_client` function to provide seamless MCP communication through a sophisticated endpoint discovery and validation process.

### SSE Client Architecture

```
```

Sources: [src/mcp/client/sse.py24-144](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L24-L144) [src/mcp/client/sse.py68-112](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L68-L112)

### Endpoint Discovery and Security

The SSE client implements a secure endpoint discovery process to prevent cross-origin attacks:

1. **Initial Connection**: Client establishes SSE connection to server endpoint [src/mcp/client/sse.py60-66](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L60-L66)
2. **Endpoint Event**: Server sends `endpoint` event with POST URL [src/mcp/client/sse.py75-76](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L75-L76)
3. **Origin Validation**: Client validates endpoint origin matches connection origin [src/mcp/client/sse.py79-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L79-L89)
4. **URL Construction**: Client constructs POST endpoint using `urljoin` for proper path resolution [src/mcp/client/sse.py76](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L76-L76)

### Client Connection Pattern

```
```

### Task Management

The `sse_client` function creates two concurrent tasks for bidirectional communication:

| Task          | Purpose                                   | Implementation                                                                                                                   |
| ------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `sse_reader`  | Handles SSE events and endpoint discovery | [src/mcp/client/sse.py68-112](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L68-L112)   |
| `post_writer` | Sends client messages via POST requests   | [src/mcp/client/sse.py114-132](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L114-L132) |

The reader task processes different SSE event types:

- `endpoint`: Establishes POST endpoint URL with security validation
- `message`: Forwards server messages to the client session
- Unknown events: Logged as warnings for debugging

Sources: [src/mcp/client/sse.py74-107](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L74-L107)

### Request Context Propagation

The transport preserves request context from the initial SSE connection and makes it available to MCP handlers:

```
```

Sources: [tests/shared/test\_sse.py183-201](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L183-L201) [tests/shared/test\_sse.py404-433](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L404-L433) [src/mcp/server/sse.py244-245](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L244-L245)

## Usage Examples

### Basic Starlette Integration

```
```

### Mounted Application Support

The transport supports deployment under path prefixes using Starlette's `Mount`:

```
```

The transport automatically handles path prefix resolution using ASGI scope's `root_path` [src/mcp/server/sse.py152-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L152-L158)

Sources: [src/mcp/server/sse.py6-37](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L6-L37) [tests/shared/test\_sse.py83-104](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L83-L104) [tests/shared/test\_sse.py289-300](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L289-L300)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Server-Sent Events (SSE) Transport](#server-sent-events-sse-transport.md)
- [Architecture Overview](#architecture-overview.md)
- [SSE Transport Architecture](#sse-transport-architecture.md)
- [Message Flow Architecture](#message-flow-architecture.md)
- [SSE Server Transport Implementation](#sse-server-transport-implementation.md)
- [Core Components](#core-components.md)
- [Transport Initialization](#transport-initialization.md)
- [ASGI Integration Pattern](#asgi-integration-pattern.md)
- [Session Management](#session-management.md)
- [Session Lifecycle](#session-lifecycle.md)
- [Session Storage and Routing](#session-storage-and-routing.md)
- [Security Features](#security-features.md)
- [Request Validation](#request-validation.md)
- [Error Handling](#error-handling.md)
- [Client-Side Error Handling](#client-side-error-handling.md)
- [Client Integration](#client-integration.md)
- [SSE Client Architecture](#sse-client-architecture.md)
- [Endpoint Discovery and Security](#endpoint-discovery-and-security.md)
- [Client Connection Pattern](#client-connection-pattern.md)
- [Task Management](#task-management.md)
- [Request Context Propagation](#request-context-propagation.md)
- [Usage Examples](#usage-examples.md)
- [Basic Starlette Integration](#basic-starlette-integration.md)
- [Mounted Application Support](#mounted-application-support.md)
