Client Framework | modelcontextprotocol/python-sdk | DeepWiki

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

# Client Framework

Relevant source files

- [src/mcp/client/\_\_main\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/__main__.py)
- [src/mcp/client/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py)
- [src/mcp/shared/memory.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/memory.py)
- [src/mcp/shared/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py)
- [tests/client/test\_logging\_callback.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_logging_callback.py)
- [tests/client/test\_session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_session.py)

The Client Framework provides the core client-side components for connecting to and interacting with MCP servers. This framework handles session management, protocol communication, request/response patterns, and server capability discovery. It abstracts the underlying transport mechanisms while providing a high-level API for MCP operations.

For information about server-side implementations, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md) and [Low-Level Server Implementation](modelcontextprotocol/python-sdk/6-low-level-server-implementation.md). For transport-specific client implementations, see [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md). For authentication details, see [Client Authentication](modelcontextprotocol/python-sdk/3.3-client-authentication.md).

## ClientSession Architecture

The `ClientSession` class serves as the primary interface for MCP client applications, built on top of the `BaseSession` foundation for session management and message handling.

```
```

**Sources:** [src/mcp/client/session.py101-136](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L101-L136) [src/mcp/shared/session.py159-200](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L159-L200)

## Session Lifecycle and Initialization

The client session follows a structured initialization process to establish protocol compatibility and exchange capability information with the server.

```
```

**Sources:** [src/mcp/client/session.py137-174](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L137-L174) [tests/client/test\_session.py30-114](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_session.py#L30-L114)

## Request and Response Handling

The framework implements a sophisticated request/response system with progress tracking, timeout management, and structured validation.

### Core Request Methods

| Method             | Purpose                      | Request Type           | Response Type         |
| ------------------ | ---------------------------- | ---------------------- | --------------------- |
| `call_tool()`      | Execute server tools         | `CallToolRequest`      | `CallToolResult`      |
| `list_tools()`     | Discover available tools     | `ListToolsRequest`     | `ListToolsResult`     |
| `read_resource()`  | Access server resources      | `ReadResourceRequest`  | `ReadResourceResult`  |
| `list_resources()` | Discover available resources | `ListResourcesRequest` | `ListResourcesResult` |
| `get_prompt()`     | Retrieve prompt templates    | `GetPromptRequest`     | `GetPromptResult`     |
| `complete()`       | Get completion suggestions   | `CompleteRequest`      | `CompleteResult`      |

**Sources:** [src/mcp/client/session.py270-297](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L270-L297) [src/mcp/client/session.py366-383](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L366-L383)

### Tool Output Validation

The client automatically validates structured tool outputs against server-provided schemas:

```
```

**Sources:** [src/mcp/client/session.py298-319](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L298-L319) [src/mcp/client/session.py377-381](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L377-L381)

## Progress and Notification System

The client framework supports bidirectional progress reporting and server-initiated notifications through callback functions and progress tokens.

### Progress Callback Integration

```
```

**Sources:** [src/mcp/shared/session.py242-253](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L242-L253) [src/mcp/shared/session.py389-399](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L389-L399)

### Server Request Handling

The client can handle server-initiated requests through configurable callback functions:

| Callback Type       | Purpose                       | Default Behavior              |
| ------------------- | ----------------------------- | ----------------------------- |
| `SamplingFnT`       | Handle LLM sampling requests  | Returns "not supported" error |
| `ElicitationFnT`    | Handle content elicitation    | Returns "not supported" error |
| `ListRootsFnT`      | Handle root directory listing | Returns "not supported" error |
| `LoggingFnT`        | Handle server log messages    | No-op (silent)                |
| `MessageHandlerFnT` | Handle all incoming messages  | No-op checkpoint              |

**Sources:** [src/mcp/client/session.py21-96](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L21-L96) [src/mcp/client/session.py388-434](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L388-L434)

## Transport Integration

The client framework abstracts transport details through stream-based interfaces, allowing it to work with various transport mechanisms.

```
```

**Sources:** [src/mcp/client/session.py110-128](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L110-L128) [src/mcp/client/\_\_main\_\_.py36-64](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/__main__.py#L36-L64)

## Testing and Development Utilities

The framework includes memory-based transport utilities for testing and development scenarios.

### Memory Transport Factory

The `create_connected_server_and_client_session()` function provides a complete testing environment with in-memory communication:

```
```

**Sources:** [src/mcp/shared/memory.py28-50](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/memory.py#L28-L50) [src/mcp/shared/memory.py53-99](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/memory.py#L53-L99)

### Error Handling and Exception Management

The client framework provides comprehensive error handling for various failure scenarios:

| Error Type                  | Source                    | Handling                                     |
| --------------------------- | ------------------------- | -------------------------------------------- |
| `TimeoutError`              | Request timeout           | Converted to `McpError` with timeout details |
| `JSONRPCError`              | Server error response     | Converted to `McpError` with server error    |
| `ValidationError`           | Tool output validation    | Runtime error with validation details        |
| `anyio.ClosedResourceError` | Transport closure         | Graceful session termination                 |
| `RuntimeError`              | Protocol version mismatch | Immediate session failure                    |

**Sources:** [src/mcp/shared/session.py273-283](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L273-L283) [src/mcp/shared/session.py416-436](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/session.py#L416-L436) [src/mcp/client/session.py314-318](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py#L314-L318)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Framework](#client-framework.md)
- [ClientSession Architecture](#clientsession-architecture.md)
- [Session Lifecycle and Initialization](#session-lifecycle-and-initialization.md)
- [Request and Response Handling](#request-and-response-handling.md)
- [Core Request Methods](#core-request-methods.md)
- [Tool Output Validation](#tool-output-validation.md)
- [Progress and Notification System](#progress-and-notification-system.md)
- [Progress Callback Integration](#progress-callback-integration.md)
- [Server Request Handling](#server-request-handling.md)
- [Transport Integration](#transport-integration.md)
- [Testing and Development Utilities](#testing-and-development-utilities.md)
- [Memory Transport Factory](#memory-transport-factory.md)
- [Error Handling and Exception Management](#error-handling-and-exception-management.md)
