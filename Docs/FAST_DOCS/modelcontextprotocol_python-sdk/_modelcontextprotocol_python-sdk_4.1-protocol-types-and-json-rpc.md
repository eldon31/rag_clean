Protocol Types & JSON-RPC | modelcontextprotocol/python-sdk | DeepWiki

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

# Protocol Types & JSON-RPC

Relevant source files

- [README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md)
- [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py)
- [src/mcp/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py)

This document covers the core protocol type definitions and JSON-RPC message handling that form the foundation of the Model Context Protocol (MCP) Python SDK. It explains the type system defined in `mcp.types`, JSON-RPC message structure, and how these types enable protocol compliance and message validation.

For information about session management and bidirectional communication patterns, see [Session Management](modelcontextprotocol/python-sdk/4.2-session-management.md). For transport-level message handling, see [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md).

## JSON-RPC Message Foundation

The MCP protocol is built on JSON-RPC 2.0, with all communication following JSON-RPC message patterns. The SDK defines base message types that all protocol messages inherit from.

### Core JSON-RPC Types

```
```

**Sources:** [src/mcp/types.py124-192](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L124-L192)

The `JSONRPCMessage` union type allows the system to handle any valid JSON-RPC message, while the generic `Request` and `Notification` base classes provide type-safe parameter handling for specific MCP protocol messages.

### Message Structure and Metadata

All MCP messages support a `_meta` field for protocol-level metadata, including progress tokens for long-running operations:

| Component                          | Type             | Purpose                                    |
| ---------------------------------- | ---------------- | ------------------------------------------ |
| `RequestParams.Meta.progressToken` | `ProgressToken`  | Enables out-of-band progress notifications |
| `Result.meta`                      | `dict[str, Any]` | General metadata for responses             |
| `NotificationParams.Meta`          | `BaseModel`      | Metadata for notifications                 |

**Sources:** [src/mcp/types.py43-75](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L43-L75)

## MCP Protocol Type Hierarchy

The MCP protocol defines specific message types for each capability, organized into client requests, server requests, and bidirectional notifications.

### Protocol Message Categories

```
```

**Sources:** [src/mcp/types.py248-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L248-L1349)

### Core Entity Types

The protocol defines entity types that represent the primary MCP capabilities:

```
```

**Sources:** [src/mcp/types.py425-890](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L425-L890)

## Message Flow Patterns

MCP follows specific request/response and notification patterns that define how clients and servers communicate.

### Request/Response Cycles

```
```

**Sources:** [src/mcp/server/lowlevel/server.py598-714](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L598-L714)

### Server Message Handling

The low-level server processes messages through a type-safe dispatch system:

```
```

**Sources:** [src/mcp/server/lowlevel/server.py637-714](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L637-L714)

## Type System Integration

The MCP type system ensures protocol compliance through Pydantic model validation and structured message handling.

### Protocol Version Management

The SDK supports protocol versioning with negotiation between client and server:

| Constant                     | Value          | Purpose                            |
| ---------------------------- | -------------- | ---------------------------------- |
| `LATEST_PROTOCOL_VERSION`    | `"2025-06-18"` | Most recent protocol version       |
| `DEFAULT_NEGOTIATED_VERSION` | `"2025-03-26"` | Fallback when no version specified |

**Sources:** [src/mcp/types.py26-34](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L26-L34)

### Union Types and Message Routing

Protocol messages use Pydantic `RootModel` unions for type-safe message routing:

```
```

**Sources:** [src/mcp/types.py1248-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1248-L1349) [src/mcp/server/lowlevel/server.py152-156](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L152-L156)

### Structured Output and Validation

The protocol supports structured output validation for tools using JSON Schema:

```
```

**Sources:** [src/mcp/server/lowlevel/server.py488-542](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L488-L542)

The type system ensures that all protocol messages are validated against their schemas, enabling reliable communication and early error detection. This foundation supports the higher-level abstractions in FastMCP and client sessions while maintaining strict protocol compliance.

**Sources:** [src/mcp/types.py1-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1-L1349) [src/mcp/server/lowlevel/server.py465-547](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L465-L547)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Protocol Types & JSON-RPC](#protocol-types-json-rpc.md)
- [JSON-RPC Message Foundation](#json-rpc-message-foundation.md)
- [Core JSON-RPC Types](#core-json-rpc-types.md)
- [Message Structure and Metadata](#message-structure-and-metadata.md)
- [MCP Protocol Type Hierarchy](#mcp-protocol-type-hierarchy.md)
- [Protocol Message Categories](#protocol-message-categories.md)
- [Core Entity Types](#core-entity-types.md)
- [Message Flow Patterns](#message-flow-patterns.md)
- [Request/Response Cycles](#requestresponse-cycles.md)
- [Server Message Handling](#server-message-handling.md)
- [Type System Integration](#type-system-integration.md)
- [Protocol Version Management](#protocol-version-management.md)
- [Union Types and Message Routing](#union-types-and-message-routing.md)
- [Structured Output and Validation](#structured-output-and-validation.md)
