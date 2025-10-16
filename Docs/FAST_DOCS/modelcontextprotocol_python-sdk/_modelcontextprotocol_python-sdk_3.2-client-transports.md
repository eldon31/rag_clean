Client Transports | modelcontextprotocol/python-sdk | DeepWiki

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

# Client Transports

Relevant source files

- [src/mcp/client/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py)
- [src/mcp/client/stdio/\_\_init\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py)
- [src/mcp/client/streamable\_http.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py)
- [tests/client/test\_notification\_response.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_notification_response.py)
- [tests/client/test\_stdio.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_stdio.py)
- [tests/issues/test\_1027\_win\_unreachable\_cleanup.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_1027_win_unreachable_cleanup.py)
- [tests/shared/test\_win32\_utils.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_win32_utils.py)

This document covers the client-side transport implementations in the MCP Python SDK that enable communication between MCP clients and servers. Client transports handle the low-level protocol communication, message serialization, and connection management for different communication channels.

For information about the high-level `ClientSession` that uses these transports, see [ClientSession Core](modelcontextprotocol/python-sdk/3.1-clientsession-core.md). For server-side transport implementations, see the Transport Layer sections [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md), [Server-Sent Events (SSE) Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md), and [STDIO Transport](modelcontextprotocol/python-sdk/5.3-stdio-transport.md).

## Transport Architecture Overview

The MCP client framework provides three primary transport implementations, each designed for different deployment scenarios and communication patterns.

```
```

Sources: [src/mcp/client/streamable\_http.py1-514](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L1-L514) [src/mcp/client/sse.py1-145](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L1-L145) [src/mcp/client/stdio/\_\_init\_\_.py1-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L1-L279)

## StreamableHTTP Transport

The `StreamableHTTPTransport` is the most sophisticated client transport, supporting bidirectional HTTP communication with session management, resumption capabilities, and both JSON and Server-Sent Events responses.

### Core Components

The transport consists of the main `StreamableHTTPTransport` class and the `streamablehttp_client` async context manager:

| Component                 | Purpose                   | Location                                                                                                                                                  |
| ------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `StreamableHTTPTransport` | Core transport logic      | [src/mcp/client/streamable\_http.py74-442](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L74-L442)   |
| `streamablehttp_client`   | Client context manager    | [src/mcp/client/streamable\_http.py445-514](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L445-L514) |
| `RequestContext`          | Request operation context | [src/mcp/client/streamable\_http.py62-72](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L62-L72)     |

### Message Flow Architecture

```
```

Sources: [src/mcp/client/streamable\_http.py366-422](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L366-L422) [src/mcp/client/streamable\_http.py192-219](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L192-L219) [src/mcp/client/streamable\_http.py254-295](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L254-L295)

### Session Management

The StreamableHTTP transport implements sophisticated session management with resumption support:

- **Session ID Extraction**: Automatically extracts session IDs from response headers [src/mcp/client/streamable\_http.py126-135](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L126-L135)
- **Protocol Version Negotiation**: Parses and stores protocol version from initialization responses [src/mcp/client/streamable\_http.py136-150](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L136-L150)
- **Request Header Preparation**: Adds session ID and protocol version to subsequent requests [src/mcp/client/streamable\_http.py109-117](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L109-L117)
- **Session Termination**: Sends DELETE requests to clean up server resources [src/mcp/client/streamable\_http.py423-438](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L423-L438)

### Resumption Capabilities

The transport supports resumption of interrupted sessions using resumption tokens:

```
```

Sources: [src/mcp/client/streamable\_http.py220-253](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L220-L253) [src/mcp/client/streamable\_http.py151-191](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L151-L191)

## SSE Transport

The `sse_client` provides a simpler transport focused on real-time communication using Server-Sent Events for server-to-client messages and HTTP POST for client-to-server messages.

### Architecture

```
```

Sources: [src/mcp/client/sse.py24-145](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L24-L145) [src/mcp/client/sse.py68-113](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L68-L113) [src/mcp/client/sse.py114-133](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L114-L133)

### Endpoint Discovery

The SSE transport implements a discovery mechanism where the server provides the POST endpoint URL via SSE events:

1. **Initial Connection**: Client connects to SSE endpoint via GET request [src/mcp/client/sse.py60-67](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L60-L67)
2. **Endpoint Event**: Server sends `endpoint` event with POST URL [src/mcp/client/sse.py75-92](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L75-L92)
3. **Security Validation**: Client validates endpoint origin matches connection origin [src/mcp/client/sse.py79-90](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L79-L90)
4. **Post Writer Activation**: POST writer task starts with discovered endpoint [src/mcp/client/sse.py134-136](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L134-L136)

## STDIO Transport

The `stdio_client` manages communication with MCP servers running as separate processes, using standard input/output streams for JSON-RPC message exchange.

### Process Lifecycle

```
```

Sources: [src/mcp/client/stdio/\_\_init\_\_.py106-217](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L106-L217) [src/mcp/client/stdio/\_\_init\_\_.py235-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L235-L279) [src/mcp/client/stdio/\_\_init\_\_.py139-165](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L139-L165)

### Platform-Specific Process Management

The STDIO transport implements platform-specific process creation and termination:

| Platform | Process Creation                            | Termination Strategy                       |
| -------- | ------------------------------------------- | ------------------------------------------ |
| Unix     | `start_new_session=True` for process groups | `os.killpg()` for atomic group termination |
| Windows  | Job Objects via `create_windows_process`    | Job Object termination for child cleanup   |

Sources: [src/mcp/client/stdio/\_\_init\_\_.py235-260](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L235-L260) [src/mcp/client/stdio/\_\_init\_\_.py262-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L262-L279)

### Message Processing

The transport handles JSON-RPC message processing with robust error handling:

- **Line-based Parsing**: Buffers input and splits on newlines [src/mcp/client/stdio/\_\_init\_\_.py144-153](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L144-L153)
- **JSON Validation**: Validates each line as JSON-RPC message [src/mcp/client/stdio/\_\_init\_\_.py154-162](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L154-L162)
- **Encoding Support**: Configurable text encoding and error handling [src/mcp/client/stdio/\_\_init\_\_.py89-103](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L89-L103)

## Transport Selection and Usage Patterns

### Transport Comparison

| Transport      | Use Case                                | Pros                                     | Cons                          |
| -------------- | --------------------------------------- | ---------------------------------------- | ----------------------------- |
| StreamableHTTP | Web services, production deployments    | Session management, resumption, scalable | Complex, requires HTTP server |
| SSE            | Real-time applications, event-driven    | Simple, real-time events                 | Limited to web contexts       |
| STDIO          | CLI tools, development, local processes | Direct process control, simple setup     | Process management complexity |

### Integration with ClientSession

All client transports follow the same interface pattern for integration with `ClientSession`:

```
```

Sources: [src/mcp/client/streamable\_http.py453-459](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L453-L459) [src/mcp/client/sse.py45-49](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L45-L49) [src/mcp/client/stdio/\_\_init\_\_.py111-115](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L111-L115)

## Error Handling and Resilience

### Connection Error Patterns

Each transport implements specific error handling strategies:

- **StreamableHTTP**: HTTP status code handling, session termination on 404, resumption error recovery [src/mcp/client/streamable\_http.py266-277](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L266-L277)
- **SSE**: Connection error recovery, origin validation errors [src/mcp/client/sse.py108-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L108-L110)
- **STDIO**: Process creation failures, graceful shutdown with timeout escalation [src/mcp/client/stdio/\_\_init\_\_.py191-217](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L191-L217)

### Timeout Management

Transport-specific timeout configurations:

| Transport      | Timeout Type        | Default   | Configuration                 |
| -------------- | ------------------- | --------- | ----------------------------- |
| StreamableHTTP | HTTP operations     | 30s       | `timeout` parameter           |
| StreamableHTTP | SSE read            | 5 minutes | `sse_read_timeout` parameter  |
| SSE            | HTTP operations     | 5s        | `timeout` parameter           |
| SSE            | SSE read            | 5 minutes | `sse_read_timeout` parameter  |
| STDIO          | Process termination | 2s        | `PROCESS_TERMINATION_TIMEOUT` |

Sources: [src/mcp/client/streamable\_http.py77-100](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/streamable_http.py#L77-L100) [src/mcp/client/sse.py27-28](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/sse.py#L27-L28) [src/mcp/client/stdio/\_\_init\_\_.py47-48](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L47-L48)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Transports](#client-transports.md)
- [Transport Architecture Overview](#transport-architecture-overview.md)
- [StreamableHTTP Transport](#streamablehttp-transport.md)
- [Core Components](#core-components.md)
- [Message Flow Architecture](#message-flow-architecture.md)
- [Session Management](#session-management.md)
- [Resumption Capabilities](#resumption-capabilities.md)
- [SSE Transport](#sse-transport.md)
- [Architecture](#architecture.md)
- [Endpoint Discovery](#endpoint-discovery.md)
- [STDIO Transport](#stdio-transport.md)
- [Process Lifecycle](#process-lifecycle.md)
- [Platform-Specific Process Management](#platform-specific-process-management.md)
- [Message Processing](#message-processing.md)
- [Transport Selection and Usage Patterns](#transport-selection-and-usage-patterns.md)
- [Transport Comparison](#transport-comparison.md)
- [Integration with ClientSession](#integration-with-clientsession.md)
- [Error Handling and Resilience](#error-handling-and-resilience.md)
- [Connection Error Patterns](#connection-error-patterns.md)
- [Timeout Management](#timeout-management.md)
