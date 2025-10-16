Transport Layer | modelcontextprotocol/python-sdk | DeepWiki

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

# Transport Layer

Relevant source files

- [src/mcp/server/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py)
- [tests/shared/test\_sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py)

The transport layer provides the foundational communication mechanisms that enable MCP clients and servers to exchange JSON-RPC messages. This layer abstracts away the underlying network protocols and provides consistent interfaces for different communication patterns including HTTP-based streaming, WebSockets, and process-based communication.

For detailed protocol message handling, see [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md). For client-side transport usage, see [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md). For server-side transport security, see [Transport Security](#5.5.md).

## Transport Architecture Overview

The MCP SDK supports multiple transport mechanisms, each optimized for different deployment scenarios and communication patterns:

```
```

**Sources:** [src/mcp/server/streamable\_http.py122-902](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http.py#L122-L902) [src/mcp/server/sse.py64-250](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L64-L250) [src/mcp/server/transport\_security.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py) [tests/shared/test\_streamable\_http.py1-1600](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_streamable_http.py#L1-L1600)

## Transport Types and Use Cases

| Transport          | Primary Use Case             | Features                                                   | Implementation                                                                                    |
| ------------------ | ---------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **StreamableHTTP** | Production web deployment    | Session management, resumability, stateful/stateless modes | [StreamableHTTPServerTransport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md)  |
| **SSE**            | Real-time notifications      | Lightweight streaming, ASGI integration                    | [SseServerTransport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md) |
| **STDIO**          | Local development, CLI tools | Process spawning, simple setup                             | [stdio\_server/client](modelcontextprotocol/python-sdk/5.3-stdio-transport.md)                    |
| **WebSocket**      | Interactive applications     | Full-duplex, low latency                                   | [websocket\_server/client](modelcontextprotocol/python-sdk/5.4-transport-security.md)             |

## Core Transport Classes

### Server Transport Interfaces

The server-side transports share common patterns but implement different communication mechanisms:

#### SSE Transport Architecture

```
```

**Sources:** [src/mcp/server/sse.py64-250](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L64-L250) [tests/shared/test\_sse.py83-104](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L83-L104)

The `SseServerTransport` class provides two ASGI applications:

- `connect_sse()`: Handles GET requests to establish SSE streams
- `handle_post_message()`: Handles POST requests containing client messages

Key implementation details:

- Endpoint validation prevents full URLs, requiring relative paths like `/messages/`
- Session management using UUID4 for unique session identification
- Request context propagation through `ServerMessageMetadata`
- DNS rebinding protection via `TransportSecurityMiddleware`

### Client Transport Interfaces

Client transports provide consistent async context manager interfaces:

```
```

**Sources:** [src/mcp/client/streamable\_http.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py) [src/mcp/client/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py) [src/mcp/client/stdio.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio.py) [src/mcp/client/websocket.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/websocket.py)

## Message Flow Architecture

All transports follow a common message flow pattern using anyio memory streams, with SSE implementing a specific dual-channel approach:

### General Message Flow

```
```

### SSE-Specific Message Flow

```
```

**Sources:** [src/mcp/server/sse.py121-250](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L121-L250) [src/mcp/client/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py) [tests/shared/test\_sse.py183-214](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L183-L214)

The SSE transport uses a unique dual-channel approach:

- **GET channel**: Establishes SSE stream for server-to-client messages
- **POST channel**: Handles client-to-server messages with session correlation
- **Session correlation**: UUID-based session matching between channels
- **Request context**: Each POST request includes full request context via `ServerMessageMetadata`

## Transport Security Features

All HTTP-based transports implement comprehensive security measures including endpoint validation and DNS rebinding protection:

### Security Validation Flow

```
```

**Sources:** [src/mcp/server/sse.py106-119](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py#L106-L119) [src/mcp/server/transport\_security.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py) [tests/shared/test\_sse.py488-513](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py#L488-L513)

### SSE Endpoint Security

The `SseServerTransport` enforces strict endpoint validation to prevent security vulnerabilities:

- **Relative Path Requirement**: Endpoints must be relative paths (e.g., `/messages/`) not full URLs
- **URL Component Rejection**: Rejects endpoints containing `://`, `//`, `?`, or `#`
- **Path Normalization**: Automatically adds leading `/` if missing
- **Security Rationale**: Prevents cross-origin requests and ensures clients connect to the same origin

```
```

## Transport Selection Guidelines

Choose the appropriate transport based on your deployment requirements:

- **StreamableHTTP**: Best for production web applications requiring session persistence and resumability
- **SSE**: Ideal for lightweight real-time updates with simple setup
- **STDIO**: Perfect for local development, CLI tools, and process-based architectures
- **WebSocket**: Optimal for interactive applications requiring low-latency bidirectional communication

Each transport is covered in detail in the following sections: [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md), [SSE Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md), [STDIO Transport](modelcontextprotocol/python-sdk/5.3-stdio-transport.md), [WebSocket Transport](modelcontextprotocol/python-sdk/5.4-transport-security.md), and [Transport Security](#5.5.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Transport Layer](#transport-layer.md)
- [Transport Architecture Overview](#transport-architecture-overview.md)
- [Transport Types and Use Cases](#transport-types-and-use-cases.md)
- [Core Transport Classes](#core-transport-classes.md)
- [Server Transport Interfaces](#server-transport-interfaces.md)
- [SSE Transport Architecture](#sse-transport-architecture.md)
- [Client Transport Interfaces](#client-transport-interfaces.md)
- [Message Flow Architecture](#message-flow-architecture.md)
- [General Message Flow](#general-message-flow.md)
- [SSE-Specific Message Flow](#sse-specific-message-flow.md)
- [Transport Security Features](#transport-security-features.md)
- [Security Validation Flow](#security-validation-flow.md)
- [SSE Endpoint Security](#sse-endpoint-security.md)
- [Transport Selection Guidelines](#transport-selection-guidelines.md)
