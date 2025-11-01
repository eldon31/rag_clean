Low-Level Server Architecture | modelcontextprotocol/python-sdk | DeepWiki

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

# Low-Level Server Architecture

Relevant source files

- [README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md)
- [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py)
- [examples/servers/simple-resource/mcp\_simple\_resource/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py)
- [examples/servers/simple-tool/mcp\_simple\_tool/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py)
- [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py)
- [src/mcp/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py)

This document covers the low-level `Server` class implementation in the MCP Python SDK, which provides the foundational layer for building MCP servers. This class handles protocol message dispatching, request validation, and the core server lifecycle without the convenience abstractions provided by FastMCP.

For high-level server development using decorators and automatic schema generation, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For details about session management and client communication, see [ServerSession Implementation](modelcontextprotocol/python-sdk/6.2-serversession-implementation.md).

## Server Class Overview

The `Server` class in [src/mcp/server/lowlevel/server.py133-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L133-L158) serves as the foundation for all MCP server implementations. It manages handler registration, request dispatching, and protocol compliance.

```
```

**Server Initialization and Configuration**

The `Server` constructor takes essential metadata and an optional lifespan context manager:

| Parameter      | Type                       | Purpose                                    |
| -------------- | -------------------------- | ------------------------------------------ |
| `name`         | `str`                      | Server identifier                          |
| `version`      | `str \| None`              | Server version                             |
| `instructions` | `str \| None`              | Usage instructions for clients             |
| `website_url`  | `str \| None`              | Server website                             |
| `icons`        | `list[types.Icon] \| None` | UI display icons                           |
| `lifespan`     | `Callable`                 | Async context manager for startup/shutdown |

Sources: [src/mcp/server/lowlevel/server.py134-157](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L134-L157)

## Handler Registration System

The Server class uses a decorator-based system to register handlers for different MCP request types. Each decorator corresponds to a specific MCP protocol message type.

```
```

**Handler Registration Process**

Each decorator method follows a consistent pattern:

1. Creates a wrapper function that adapts the user function to the expected signature
2. Stores the wrapper in `request_handlers` with the request type as key
3. Returns the original function unchanged

For example, the `list_tools` decorator at [src/mcp/server/lowlevel/server.py409-437](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L409-L437) registers handlers for `types.ListToolsRequest` and manages the tool cache.

Sources: [src/mcp/server/lowlevel/server.py238-596](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L238-L596)

## Request Processing Architecture

The Server processes incoming requests through a multi-stage pipeline that includes message handling, context setup, and response generation.

```
```

**Message Handling Flow**

The main request processing occurs in `_handle_request` at [src/mcp/server/lowlevel/server.py656-712](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L656-L712):

1. **Handler Lookup**: Finds handler by request type in `request_handlers`
2. **Context Setup**: Creates and sets `RequestContext` with session and lifespan data
3. **Handler Execution**: Calls the registered handler function
4. **Error Handling**: Catches exceptions and converts to appropriate error responses
5. **Context Cleanup**: Resets the request context using `contextvars`

Sources: [src/mcp/server/lowlevel/server.py598-723](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L598-L723)

## Tool System Architecture

The Server implements a sophisticated tool handling system with caching, validation, and structured output support.

```
```

**Tool Caching and Validation**

The Server maintains a tool cache (`_tool_cache`) that stores `Tool` definitions for input/output validation. The cache is populated when `list_tools` handlers are called, as shown in [src/mcp/server/lowlevel/server.py418-433](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L418-L433)

**Tool Call Processing**

The `call_tool` decorator at [src/mcp/server/lowlevel/server.py465-547](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L465-L547) implements comprehensive tool call handling:

1. **Input Validation**: Uses `jsonschema` to validate arguments against `inputSchema`

2. **Tool Execution**: Calls the registered tool function

3. **Output Normalization**: Handles three output types:

   - `UnstructuredContent`: Raw content blocks
   - `StructuredContent`: JSON objects
   - `CombinationContent`: Both structured and unstructured

4. **Output Validation**: Validates structured output against `outputSchema` if defined

Sources: [src/mcp/server/lowlevel/server.py449-547](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L449-L547) [src/mcp/server/lowlevel/server.py99-102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L99-L102)

## Context Management

The Server uses Python's `contextvars` module to provide request-scoped context accessible throughout the request processing pipeline.

```
```

**Request Context Structure**

The `RequestContext` is created in `_handle_request` at [src/mcp/server/lowlevel/server.py677-684](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L677-L684) with:

- Request ID and metadata from the message
- `ServerSession` instance for client communication
- Lifespan context from the server's lifespan manager
- Optional request-specific data

**Context Access**

Handlers can access the current request context via the `request_context` property at [src/mcp/server/lowlevel/server.py232-236](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L232-L236) which retrieves the context variable or raises `LookupError` if called outside a request.

Sources: [src/mcp/server/lowlevel/server.py105](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L105-L105) [src/mcp/shared/context.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/context.py) [src/mcp/server/lowlevel/server.py677-702](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L677-L702)

## Integration with Transport Layer

The Server integrates with various transport mechanisms through the `ServerSession` and stream-based communication.

```
```

**Server Run Method**

The `run` method at [src/mcp/server/lowlevel/server.py598-635](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L598-L635) orchestrates the server lifecycle:

1. **Lifespan Management**: Enters the async context manager for startup/shutdown
2. **Session Creation**: Creates `ServerSession` with provided streams and options
3. **Message Processing**: Iterates over incoming messages and spawns handlers
4. **Graceful Shutdown**: Ensures proper cleanup of resources

**Transport Examples**

The example servers demonstrate different transport integrations:

- **stdio**: Direct process communication via stdin/stdout
- **SSE**: HTTP Server-Sent Events with Starlette ASGI integration
- **HTTP**: Full bidirectional HTTP with session management

Sources: [src/mcp/server/lowlevel/server.py598-635](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L598-L635) [examples/servers/simple-resource/mcp\_simple\_resource/server.py60-91](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L60-L91) [examples/servers/simple-tool/mcp\_simple\_tool/server.py60-91](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L60-L91) [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py79-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L79-L110)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Low-Level Server Architecture](#low-level-server-architecture.md)
- [Server Class Overview](#server-class-overview.md)
- [Handler Registration System](#handler-registration-system.md)
- [Request Processing Architecture](#request-processing-architecture.md)
- [Tool System Architecture](#tool-system-architecture.md)
- [Context Management](#context-management.md)
- [Integration with Transport Layer](#integration-with-transport-layer.md)
