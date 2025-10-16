Low-Level Server Implementation | modelcontextprotocol/python-sdk | DeepWiki

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

# Low-Level Server Implementation

Relevant source files

- [README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md)
- [src/mcp/server/\_\_init\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/__init__.py)
- [src/mcp/server/\_\_main\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/__main__.py)
- [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py)
- [src/mcp/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py)

This document covers the low-level `Server` class that provides direct access to the MCP protocol implementation. This is the foundation layer that handles raw MCP requests and notifications with minimal abstraction. For high-level server development using decorators and automatic schema generation, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For details on session management and client connections, see [ServerSession Implementation](modelcontextprotocol/python-sdk/6.2-serversession-implementation.md).

## Server Class Overview

The `Server` class in [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py) provides a decorator-based framework for implementing MCP servers with direct control over protocol message handling. Unlike FastMCP's automatic introspection, the low-level server requires explicit handler registration and manual schema definition.

```
```

Sources: [src/mcp/server/lowlevel/server.py133-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L133-L158) [src/mcp/server/lowlevel/server.py152-155](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L152-L155) [src/mcp/types.py82-103](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L82-L103)

The `Server` class is generic over two type parameters: `LifespanResultT` for lifespan context data and `RequestT` for request-specific data. It maintains separate dictionaries for request handlers and notification handlers, automatically routing incoming messages based on their type.

## Handler Registration System

Request and notification handlers are registered using decorator methods that map protocol message types to handler functions. Each decorator enforces specific function signatures while providing flexibility in implementation.

```
```

Sources: [src/mcp/server/lowlevel/server.py409-438](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L409-L438) [src/mcp/server/lowlevel/server.py245-255](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L245-L255) [src/mcp/server/lowlevel/func\_inspection.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/func_inspection.py)

Handler functions can return either the specific result type (e.g., `ListToolsResult`) or the legacy format (e.g., `list[Tool]`). The server automatically wraps legacy returns in the appropriate result container for backward compatibility.

## Tool Management and Validation

The server implements sophisticated tool management including input/output validation and result processing. Tools are cached to avoid repeated calls to `list_tools()` and support both structured and unstructured content output.

| Feature               | Implementation                 | Purpose                                            |
| --------------------- | ------------------------------ | -------------------------------------------------- |
| Tool Caching          | `_tool_cache: dict[str, Tool]` | Avoid repeated tool list requests                  |
| Input Validation      | `jsonschema.validate()`        | Validate arguments against `inputSchema`           |
| Output Validation     | `jsonschema.validate()`        | Validate structured results against `outputSchema` |
| Content Normalization | `CombinationContent` handling  | Support both structured and unstructured outputs   |

```
```

Sources: [src/mcp/server/lowlevel/server.py465-547](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L465-L547) [src/mcp/server/lowlevel/server.py99-102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L99-L102) [src/mcp/server/lowlevel/server.py449-463](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L449-L463)

The `call_tool()` decorator accepts a `validate_input` parameter to control input validation. Output validation is automatically performed when `outputSchema` is defined in the tool definition.

## Request Context System

The server uses Python's `contextvars` module to provide request-scoped context accessible throughout the handler call stack. This context includes session information, lifespan data, and request metadata.

```
```

Sources: [src/mcp/server/lowlevel/server.py105](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L105-L105) [src/mcp/server/lowlevel/server.py232-236](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L232-L236) [src/mcp/server/lowlevel/server.py677-685](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L677-L685) [src/mcp/shared/context.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/context.py)

## Message Processing Architecture

The server's main `run()` method establishes a session and processes incoming messages through a task group, ensuring proper error handling and response delivery.

```
```

Sources: [src/mcp/server/lowlevel/server.py598-636](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L598-L636) [src/mcp/server/lowlevel/server.py637-655](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L637-L655) [src/mcp/server/lowlevel/server.py656-713](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L656-L713)

## Capabilities Discovery

The server automatically generates `ServerCapabilities` based on registered handlers, allowing clients to discover available functionality without manual configuration.

```
```

Sources: [src/mcp/server/lowlevel/server.py188-229](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L188-L229) [src/mcp/types.py317-332](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L317-L332) [src/mcp/server/lowlevel/server.py159-186](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L159-L186)

The `NotificationOptions` class controls whether the server supports change notifications for prompts, resources, and tools, which are reflected in the generated capabilities.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Low-Level Server Implementation](#low-level-server-implementation.md)
- [Server Class Overview](#server-class-overview.md)
- [Handler Registration System](#handler-registration-system.md)
- [Tool Management and Validation](#tool-management-and-validation.md)
- [Request Context System](#request-context-system.md)
- [Message Processing Architecture](#message-processing-architecture.md)
- [Capabilities Discovery](#capabilities-discovery.md)
