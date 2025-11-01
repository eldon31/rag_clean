modelcontextprotocol/python-sdk | DeepWiki

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

# Overview

Relevant source files

- [README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md)
- [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py)
- [src/mcp/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py)

The Model Context Protocol (MCP) Python SDK is a comprehensive framework for building servers and clients that enable Large Language Models to access external tools, data, and services in a standardized way. This SDK implements the complete MCP specification, providing both high-level developer-friendly APIs and low-level protocol implementations.

The SDK enables developers to create MCP servers that expose resources (data), tools (functions), and prompts (templates) to LLM applications, as well as MCP clients that can discover and interact with these servers. For detailed implementation guidance on building servers, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For client development, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md). For protocol-level details, see [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md).

## System Architecture

The MCP Python SDK is organized into several distinct layers, each serving specific roles in the protocol implementation:

```
```

**Sources:** [README.md1-1770](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L1-L1770) [src/mcp/server/lowlevel/server.py1-727](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L1-L727) [src/mcp/types.py1-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1-L1349)

## Core Components

### Protocol Foundation

The MCP SDK is built on JSON-RPC 2.0 messaging with well-defined protocol types. The `mcp.types` module contains all protocol message definitions, including requests, responses, and notifications that flow between clients and servers.

```
```

**Sources:** [src/mcp/types.py124-192](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L124-L192) [src/mcp/types.py1248-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1248-L1349)

### Server Implementations

The SDK provides two primary approaches for building MCP servers:

**FastMCP Framework** - A decorator-based high-level framework that automatically handles protocol compliance, schema generation, and transport integration. Users define tools, resources, and prompts using Python decorators.

**Low-Level Server** - Direct protocol implementation providing full control over message handling, lifecycle management, and custom protocol extensions.

```
```

**Sources:** [README.md138-170](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L138-L170) [src/mcp/server/lowlevel/server.py133-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L133-L158)

### Client Framework

The client framework centers around `ClientSession` which provides high-level methods for discovering and interacting with MCP servers. It handles transport abstraction, authentication, and protocol message management.

```
```

**Sources:** [README.md660-733](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L660-L733)

### Transport Layer

The SDK supports three transport mechanisms for MCP communication, each suited for different deployment scenarios:

| Transport         | Use Case                           | Implementation                         |
| ----------------- | ---------------------------------- | -------------------------------------- |
| `stdio`           | Process-based servers, development | `mcp.server.stdio`, `mcp.client.stdio` |
| `sse`             | Real-time web applications         | `mcp.server.sse`, `mcp.client.sse`     |
| `streamable-http` | Production HTTP deployments        | `mcp.server.streamablehttp`            |

**Sources:** [README.md1104-1217](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L1104-L1217)

## Development Workflow

The SDK includes comprehensive development tools accessible through the `mcp` CLI:

```
```

**Sources:** [README.md1027-1102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L1027-L1102)

For specific implementation details on each component, refer to the dedicated sections: [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md) for high-level server development, [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md) for client implementation, [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md) for communication mechanisms, and [Development Tools & CLI](modelcontextprotocol/python-sdk/8-development-tools-and-cli.md) for development workflow.

# Overview

The Model Context Protocol (MCP) Python SDK is a comprehensive framework for building servers and clients that enable Large Language Models to access external tools, data, and services in a standardized way. This SDK implements the complete MCP specification, providing both high-level developer-friendly APIs and low-level protocol implementations.

The SDK enables developers to create MCP servers that expose resources (data), tools (functions), and prompts (templates) to LLM applications, as well as MCP clients that can discover and interact with these servers. For detailed implementation guidance on building servers, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For client development, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md). For protocol-level details, see [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md).

## System Architecture

The MCP Python SDK is organized into several distinct layers, each serving specific roles in the protocol implementation:

```
```

**Sources:** [README.md1-1770](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L1-L1770) [src/mcp/server/lowlevel/server.py1-727](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L1-L727) [src/mcp/types.py1-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1-L1349)

## Core Components

### Protocol Foundation

The MCP SDK is built on JSON-RPC 2.0 messaging with well-defined protocol types. The `mcp.types` module contains all protocol message definitions, including requests, responses, and notifications that flow between clients and servers.

```
```

**Sources:** [src/mcp/types.py124-192](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L124-L192) [src/mcp/types.py1248-1349](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L1248-L1349)

### Server Implementations

The SDK provides two primary approaches for building MCP servers:

**FastMCP Framework** - A decorator-based high-level framework that automatically handles protocol compliance, schema generation, and transport integration. Users define tools, resources, and prompts using Python decorators.

**Low-Level Server** - Direct protocol implementation providing full control over message handling, lifecycle management, and custom protocol extensions.

```
```

**Sources:** [README.md138-170](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L138-L170) [src/mcp/server/lowlevel/server.py133-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L133-L158)

### Client Framework

The client framework centers around `ClientSession` which provides high-level methods for discovering and interacting with MCP servers. It handles transport abstraction, authentication, and protocol message management.

```
```

**Sources:** [README.md660-733](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L660-L733)

### Transport Layer

The SDK supports three transport mechanisms for MCP communication, each suited for different deployment scenarios:

| Transport         | Use Case                           | Implementation                         |
| ----------------- | ---------------------------------- | -------------------------------------- |
| `stdio`           | Process-based servers, development | `mcp.server.stdio`, `mcp.client.stdio` |
| `sse`             | Real-time web applications         | `mcp.server.sse`, `mcp.client.sse`     |
| `streamable-http` | Production HTTP deployments        | `mcp.server.streamablehttp`            |

**Sources:** [README.md1104-1217](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L1104-L1217)

## Development Workflow

The SDK includes comprehensive development tools accessible through the `mcp` CLI:

```
```

**Sources:** [README.md1027-1102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L1027-L1102)

For specific implementation details on each component, refer to the dedicated sections: [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md) for high-level server development, [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md) for client implementation, [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md) for communication mechanisms, and [Development Tools & CLI](modelcontextprotocol/python-sdk/8-development-tools-and-cli.md) for development workflow.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Overview](#overview.md)
- [System Architecture](#system-architecture.md)
- [Core Components](#core-components.md)
- [Protocol Foundation](#protocol-foundation.md)
- [Server Implementations](#server-implementations.md)
- [Client Framework](#client-framework.md)
- [Transport Layer](#transport-layer.md)
- [Development Workflow](#development-workflow.md)
- [Overview](#overview-1.md)
- [System Architecture](#system-architecture-1.md)
- [Core Components](#core-components-1.md)
- [Protocol Foundation](#protocol-foundation-1.md)
- [Server Implementations](#server-implementations-1.md)
- [Client Framework](#client-framework-1.md)
- [Transport Layer](#transport-layer-1.md)
- [Development Workflow](#development-workflow-1.md)
