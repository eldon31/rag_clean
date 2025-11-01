Protocol & Message System | modelcontextprotocol/python-sdk | DeepWiki

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

# Protocol & Message System

Relevant source files

- [README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md)
- [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py)
- [src/mcp/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py)

This page documents the core Model Context Protocol (MCP) message system, JSON-RPC foundation, and type system that enables communication between MCP clients and servers. This covers the fundamental protocol layer that underlies all MCP interactions.

For high-level server development using decorators and simplified APIs, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For transport-specific implementations like stdio, SSE, and StreamableHTTP, see [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md). For client-side message handling, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md).

## JSON-RPC Foundation

MCP is built on JSON-RPC 2.0, providing a standardized request-response and notification messaging pattern. The protocol defines four core message types that form the foundation of all MCP communication.

```
```

**Sources:** [src/mcp/types.py124-193](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L124-L193) [src/mcp/shared/message.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/message.py)

The base JSON-RPC types define the message structure:

- `JSONRPCRequest`: Request expecting a response, includes `id`, `method`, and `params`
- `JSONRPCResponse`: Successful response with `id` and `result`
- `JSONRPCError`: Error response with `id` and `error` containing code, message, and optional data
- `JSONRPCNotification`: One-way message with `method` and `params`, no response expected

## Protocol Message Hierarchy

MCP defines a structured hierarchy of message types that inherit from the JSON-RPC foundation, creating type-safe request and response patterns.

```
```

**Sources:** [src/mcp/types.py82-122](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L82-L122) [src/mcp/types.py335-365](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L335-L365) [src/mcp/types.py815-922](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L815-L922)

Each protocol operation follows this pattern:

1. **Request class**: Defines the method name and parameter structure
2. **Parameter class**: Strongly-typed parameters extending `RequestParams`
3. **Result class**: Response structure extending `Result`
4. **Specialized handling**: Pagination, metadata, and protocol-specific features

## Core Protocol Operations

MCP defines several categories of protocol operations, each with specific request-response patterns and capabilities.

```
```

**Sources:** [src/mcp/types.py345-365](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L345-L365) [src/mcp/types.py419-554](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L419-L554) [src/mcp/types.py815-922](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L815-L922) [src/mcp/types.py630-802](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L630-L802) [src/mcp/types.py1061-1081](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1061-L1081)

## Message Processing Architecture

The server processes incoming messages through a structured handler system that maps message types to handler functions and manages the request lifecycle.

```
```

**Sources:** [src/mcp/server/lowlevel/server.py625-723](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L625-L723) [src/mcp/server/lowlevel/server.py152-155](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L152-L155) [src/mcp/server/lowlevel/server.py238-259](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L238-L259)

The `Server` class maintains handler registries that map message types to handler functions:

- `request_handlers`: Maps request types to async handler functions
- `notification_handlers`: Maps notification types to async handler functions
- Decorator pattern for handler registration (e.g., `@server.list_tools()`)

## Content and Structured Output System

MCP supports both unstructured content and structured data in responses, enabling rich tool outputs and backward compatibility.

```
```

**Sources:** [src/mcp/types.py688-782](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L688-L782) [src/mcp/types.py914-922](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L914-L922) [src/mcp/server/lowlevel/server.py100-102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L100-L102)

The content system supports:

- **Unstructured content**: Human-readable content blocks (text, images, audio, resources)
- **Structured content**: Machine-readable JSON data with optional schema validation
- **Combination output**: Both structured and unstructured content in the same response
- **Schema validation**: Optional `outputSchema` validation for structured content

## Protocol Versioning and Capabilities

MCP uses semantic versioning and capability negotiation to ensure compatibility between clients and servers with different feature sets.

```
```

**Sources:** [src/mcp/types.py26-34](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L26-L34) [src/mcp/types.py265-332](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L265-L332) [src/mcp/types.py335-365](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L335-L365)

Capability negotiation enables:

- **Protocol versioning**: Semantic version strings for compatibility checking
- **Feature detection**: Clients and servers declare supported capabilities
- **Graceful degradation**: Optional features can be disabled if not supported
- **Extension points**: Experimental capabilities for new features

## Error Handling and Status Codes

MCP defines standardized error codes and error handling patterns based on JSON-RPC 2.0 specifications.

```
```

**Sources:** [src/mcp/types.py149-179](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L149-L179) [src/mcp/server/lowlevel/server.py440-447](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L440-L447) [src/mcp/shared/exceptions.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/exceptions.py)

Error handling includes:

- **Standard JSON-RPC codes**: Parse, request, method, and parameter errors
- **MCP-specific codes**: Connection and transport-related errors
- **Structured error data**: Code, message, and optional additional data
- **Exception mapping**: Python exceptions converted to MCP error responses

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Protocol & Message System](#protocol-message-system.md)
- [JSON-RPC Foundation](#json-rpc-foundation.md)
- [Protocol Message Hierarchy](#protocol-message-hierarchy.md)
- [Core Protocol Operations](#core-protocol-operations.md)
- [Message Processing Architecture](#message-processing-architecture.md)
- [Content and Structured Output System](#content-and-structured-output-system.md)
- [Protocol Versioning and Capabilities](#protocol-versioning-and-capabilities.md)
- [Error Handling and Status Codes](#error-handling-and-status-codes.md)
