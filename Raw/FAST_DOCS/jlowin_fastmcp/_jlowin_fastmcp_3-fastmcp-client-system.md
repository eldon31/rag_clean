FastMCP Client System | jlowin/fastmcp | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[jlowin/fastmcp](https://github.com/jlowin/fastmcp "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 30 September 2025 ([66221e](https://github.com/jlowin/fastmcp/commits/66221ed3))

- [FastMCP Overview](jlowin/fastmcp/1-fastmcp-overview.md)
- [Installation and Setup](jlowin/fastmcp/1.1-installation-and-setup.md)
- [FastMCP Server Core](jlowin/fastmcp/2-fastmcp-server-core.md)
- [Component System Architecture](jlowin/fastmcp/2.1-component-system-architecture.md)
- [Context System and Dependencies](jlowin/fastmcp/2.2-context-system-and-dependencies.md)
- [Server Composition and Proxying](jlowin/fastmcp/2.3-server-composition-and-proxying.md)
- [FastMCP Client System](jlowin/fastmcp/3-fastmcp-client-system.md)
- [Transport Mechanisms](jlowin/fastmcp/3.1-transport-mechanisms.md)
- [Client Authentication](jlowin/fastmcp/3.2-client-authentication.md)
- [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md)
- [Authentication and Security](jlowin/fastmcp/4.1-authentication-and-security.md)
- [Middleware System](jlowin/fastmcp/4.2-middleware-system.md)
- [Command Line Interface](jlowin/fastmcp/5-command-line-interface.md)
- [OpenAPI Integration](jlowin/fastmcp/6-openapi-integration.md)
- [Configuration Management](jlowin/fastmcp/7-configuration-management.md)
- [Testing and Development Framework](jlowin/fastmcp/8-testing-and-development-framework.md)
- [Project Infrastructure](jlowin/fastmcp/9-project-infrastructure.md)
- [Documentation and Updates](jlowin/fastmcp/10-documentation-and-updates.md)

Menu

# FastMCP Client System

Relevant source files

- [docs/clients/client.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/clients/client.mdx)
- [docs/clients/transports.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/clients/transports.mdx)
- [docs/servers/composition.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/servers/composition.mdx)
- [docs/servers/proxy.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/servers/proxy.mdx)
- [examples/in\_memory\_proxy\_example.py](https://github.com/jlowin/fastmcp/blob/66221ed3/examples/in_memory_proxy_example.py)
- [src/fastmcp/client/client.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py)
- [src/fastmcp/client/transports.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py)
- [src/fastmcp/mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/mcp_config.py)
- [src/fastmcp/server/proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py)
- [src/fastmcp/utilities/mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/mcp_config.py)
- [tests/client/test\_client.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_client.py)
- [tests/client/test\_stdio.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_stdio.py)

The FastMCP Client System provides a programmatic interface for interacting with Model Context Protocol (MCP) servers through a well-typed, Pythonic API. This system handles protocol operations, connection management, and session lifecycle while abstracting away transport-specific implementation details.

For information about creating and configuring MCP servers, see [FastMCP Server Core](jlowin/fastmcp/2-fastmcp-server-core.md). For details about HTTP server deployment and authentication, see [HTTP Server and Deployment](jlowin/fastmcp/6-openapi-integration.md).

## Core Architecture

The FastMCP Client System implements a separation of concerns between protocol handling and connection management through two primary components:

| Component     | Responsibility                                                 | Key Classes                                                                                        |
| ------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Client**    | MCP protocol operations, session management, callback handling | `Client`                                                                                           |
| **Transport** | Connection establishment, communication channel management     | `ClientTransport`, `SSETransport`, `StreamableHttpTransport`, `StdioTransport`, `FastMCPTransport` |

### Client-Transport Relationship

```
```

**Sources**: [src/fastmcp/client/client.py90-149](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L90-L149) [src/fastmcp/client/transports.py71-115](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L71-L115)

The `Client` class uses generic typing to preserve specific transport types, enabling transport-specific configuration while maintaining a consistent protocol interface.

### Transport Inference

The client automatically selects appropriate transports based on input type:

```
```

**Sources**: [src/fastmcp/client/transports.py888-924](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L888-L924) [src/fastmcp/client/client.py150-221](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L150-L221)

## Client Session Management

The `Client` implements a sophisticated session management system supporting reentrant context managers and concurrent usage patterns.

### Session State Architecture

```
```

**Sources**: [src/fastmcp/client/client.py73-88](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L73-L88) [src/fastmcp/client/client.py451-474](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L451-L474)

### Connection Lifecycle

The client manages connection lifecycle through reference counting and background session management:

```
```

**Sources**: [src/fastmcp/client/client.py367-411](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L367-L411) [src/fastmcp/client/client.py413-449](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L413-L449)

## Transport System

### Transport Interface

All transports implement the `ClientTransport` abstract base class:

```
```

**Sources**: [src/fastmcp/client/transports.py71-115](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L71-L115) [src/fastmcp/client/transports.py301-417](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L301-L417)

### STDIO Transport Environment Management

STDIO transports implement environment isolation for security:

```
```

**Sources**: [src/fastmcp/client/transports.py301-417](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L301-L417) [src/fastmcp/client/transports.py465-508](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L465-L508)

## Client Protocol Operations

The `Client` class provides methods for all MCP protocol operations, with both raw protocol and convenience variants:

### Tool Operations

| Method             | Return Type                 | Description                       |
| ------------------ | --------------------------- | --------------------------------- |
| `list_tools()`     | `list[mcp.types.Tool]`      | List available tools              |
| `list_tools_mcp()` | `mcp.types.ListToolsResult` | Raw MCP protocol result           |
| `call_tool()`      | `CallToolResult`            | Execute tool with type conversion |
| `call_tool_mcp()`  | `mcp.types.CallToolResult`  | Raw MCP tool execution            |

**Sources**: [src/fastmcp/client/client.py763-895](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L763-L895)

### Resource Operations

| Method                      | Return Type                                                    | Description              |
| --------------------------- | -------------------------------------------------------------- | ------------------------ |
| `list_resources()`          | `list[mcp.types.Resource]`                                     | List available resources |
| `list_resource_templates()` | `list[mcp.types.ResourceTemplate]`                             | List URI templates       |
| `read_resource()`           | `list[mcp.types.TextResourceContents \| BlobResourceContents]` | Read resource contents   |

**Sources**: [src/fastmcp/client/client.py525-636](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L525-L636)

### Prompt Operations

| Method           | Return Type                 | Description                  |
| ---------------- | --------------------------- | ---------------------------- |
| `list_prompts()` | `list[mcp.types.Prompt]`    | List available prompts       |
| `get_prompt()`   | `mcp.types.GetPromptResult` | Render prompt with arguments |

**Sources**: [src/fastmcp/client/client.py639-716](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L639-L716)

### Tool Result Processing

The client provides structured result handling through the `CallToolResult` dataclass:

```
```

**Sources**: [src/fastmcp/client/client.py826-894](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L826-L894) [src/fastmcp/client/client.py897-903](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L897-L903)

## Client Configuration and Handlers

### Handler System

The client supports multiple callback handlers for server interactions:

| Handler Type      | Purpose                          | Interface                                  |
| ----------------- | -------------------------------- | ------------------------------------------ |
| `LogHandler`      | Process server log messages      | `(LogMessage) -> Awaitable[None]`          |
| `ProgressHandler` | Monitor operation progress       | `(float, float?, str?) -> Awaitable[None]` |
| `SamplingHandler` | Respond to LLM sampling requests | Complex sampling interface                 |
| `RootsHandler`    | Provide filesystem roots         | `() -> RootsList`                          |

**Sources**: [src/fastmcp/client/client.py210-267](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L210-L267)

### Client Factory Pattern

The client constructor uses overloaded signatures to support transport inference while maintaining type safety:

```
```

**Sources**: [src/fastmcp/client/client.py150-221](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py#L150-L221) [src/fastmcp/client/transports.py888-924](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L888-L924)

## Integration with Server Composition

The client system integrates with FastMCP's server composition patterns through several mechanisms:

### Proxy Client Usage

```
```

**Sources**: [docs/servers/proxy.mdx278-329](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/servers/proxy.mdx#L278-L329) [examples/in\_memory\_proxy\_example.py40-50](https://github.com/jlowin/fastmcp/blob/66221ed3/examples/in_memory_proxy_example.py#L40-L50)

### Multi-Server Configuration

The `MCPConfigTransport` enables single-client access to multiple servers through automatic composition:

```
```

**Sources**: [src/fastmcp/client/transports.py817-887](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py#L817-L887) [docs/clients/client.mdx124-142](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/clients/client.mdx#L124-L142)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [FastMCP Client System](#fastmcp-client-system.md)
- [Core Architecture](#core-architecture.md)
- [Client-Transport Relationship](#client-transport-relationship.md)
- [Transport Inference](#transport-inference.md)
- [Client Session Management](#client-session-management.md)
- [Session State Architecture](#session-state-architecture.md)
- [Connection Lifecycle](#connection-lifecycle.md)
- [Transport System](#transport-system.md)
- [Transport Interface](#transport-interface.md)
- [STDIO Transport Environment Management](#stdio-transport-environment-management.md)
- [Client Protocol Operations](#client-protocol-operations.md)
- [Tool Operations](#tool-operations.md)
- [Resource Operations](#resource-operations.md)
- [Prompt Operations](#prompt-operations.md)
- [Tool Result Processing](#tool-result-processing.md)
- [Client Configuration and Handlers](#client-configuration-and-handlers.md)
- [Handler System](#handler-system.md)
- [Client Factory Pattern](#client-factory-pattern.md)
- [Integration with Server Composition](#integration-with-server-composition.md)
- [Proxy Client Usage](#proxy-client-usage.md)
- [Multi-Server Configuration](#multi-server-configuration.md)
