FastMCP Server Architecture | modelcontextprotocol/python-sdk | DeepWiki

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

# FastMCP Server Architecture

Relevant source files

- [src/mcp/server/fastmcp/\_\_init\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/__init__.py)
- [src/mcp/server/fastmcp/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py)
- [src/mcp/server/fastmcp/utilities/func\_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py)
- [src/mcp/server/fastmcp/utilities/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/types.py)
- [tests/server/fastmcp/test\_func\_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_func_metadata.py)
- [tests/server/fastmcp/test\_server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_server.py)

This document explains the internal architecture of the FastMCP server framework, including its core components, managers, function introspection system, and transport integration. FastMCP provides a high-level, decorator-based interface for building MCP servers that automatically handles schema generation, validation, and protocol compliance.

For information about using FastMCP decorators and APIs, see [Tool Management](modelcontextprotocol/python-sdk/2.2-tool-management.md) and [Resource & Prompt Management](modelcontextprotocol/python-sdk/2.3-resource-and-prompt-management.md). For details about the underlying protocol implementation, see [Low-Level Server Architecture](modelcontextprotocol/python-sdk/6.1-low-level-server-architecture.md).

## Core Architecture Overview

FastMCP implements a layered architecture that wraps the low-level MCP server with higher-level abstractions and automatic introspection capabilities.

```
```

**Sources:** [src/mcp/server/fastmcp/server.py122-206](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L122-L206) [src/mcp/server/fastmcp/utilities/func\_metadata.py62-67](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L62-L67)

## FastMCP Main Server Class

The `FastMCP` class serves as the primary entry point and orchestrator for the entire server framework. It manages settings, coordinates managers, and provides the decorator interface.

### Core Components

The `FastMCP` class initializes and coordinates several key subsystems:

- **Settings Management**: Uses `Settings` class with environment variable support (prefix `FASTMCP_`)
- **Manager Coordination**: Initializes `ToolManager`, `ResourceManager`, and `PromptManager`
- **Protocol Integration**: Wraps the low-level `MCPServer` with enhanced functionality
- **Transport Apps**: Generates transport-specific applications (stdio, SSE, StreamableHTTP)

```
```

**Sources:** [src/mcp/server/fastmcp/server.py152-209](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L152-L209) [src/mcp/server/fastmcp/server.py268-280](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L268-L280)

### Decorator Interface

FastMCP provides three primary decorators that automatically handle function registration and introspection:

| Decorator     | Manager           | Purpose                                      |
| ------------- | ----------------- | -------------------------------------------- |
| `@tool()`     | `ToolManager`     | Register functions as callable tools         |
| `@resource()` | `ResourceManager` | Register functions as resources or templates |
| `@prompt()`   | `PromptManager`   | Register functions as prompt generators      |

Each decorator uses the same underlying pattern: function introspection → manager registration → protocol handler binding.

**Sources:** [src/mcp/server/fastmcp/server.py393-451](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L393-L451) [src/mcp/server/fastmcp/server.py479-578](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L479-L578) [src/mcp/server/fastmcp/server.py588-641](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L588-L641)

## Manager Subsystem Architecture

The manager subsystem handles registration, validation, and execution of user-defined functions through a consistent interface pattern.

```
```

**Sources:** [src/mcp/server/fastmcp/tools.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools.py) [src/mcp/server/fastmcp/resources.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources.py) [src/mcp/server/fastmcp/prompts.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts.py)

### Function Registration Flow

All managers follow a consistent registration pattern:

1. **Function Analysis**: Extract signature, docstring, and type annotations
2. **Schema Generation**: Create Pydantic models for inputs and outputs
3. **Metadata Creation**: Build `Tool`, `Resource`, or `Prompt` objects
4. **Storage**: Register in manager's internal dictionary
5. **Validation**: Check for duplicates and conflicts

**Sources:** [src/mcp/server/fastmcp/utilities/func\_metadata.py166-284](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L166-L284)

## Function Introspection System

The function introspection system (`func_metadata`) is the core of FastMCP's automatic schema generation and validation capabilities.

### FuncMetadata Components

```
```

**Sources:** [src/mcp/server/fastmcp/utilities/func\_metadata.py62-120](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L62-L120)

### Structured Output Detection

FastMCP automatically determines whether a function should have structured output based on its return type annotation:

| Return Type                          | Output Handling                | Wrapping    |
| ------------------------------------ | ------------------------------ | ----------- |
| `BaseModel` subclass                 | Direct schema generation       | No wrapping |
| Primitive types (`str`, `int`, etc.) | Wrapped in `{"result": value}` | Yes         |
| `dict[str, T]`                       | RootModel generation           | No wrapping |
| Generic types (`list[T]`, `Union`)   | Wrapped in `{"result": value}` | Yes         |
| Unannotated classes                  | No structured output           | N/A         |

**Sources:** [src/mcp/server/fastmcp/utilities/func\_metadata.py287-371](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L287-L371)

## Context Injection System

FastMCP provides automatic context injection that gives functions access to request-specific information and MCP capabilities.

```
```

**Sources:** [src/mcp/server/fastmcp/utilities/context\_injection.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/context_injection.py) [src/mcp/shared/context.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/context.py)

## Transport Integration Architecture

FastMCP integrates with multiple transport protocols by generating transport-specific ASGI applications that wrap the core MCP server functionality.

```
```

**Sources:** [src/mcp/server/fastmcp/server.py687-725](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L687-L725) [src/mcp/server/fastmcp/server.py752-884](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L752-L884) [src/mcp/server/fastmcp/server.py885-984](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L885-L984)

### Transport Application Generation

Each transport type requires different ASGI application structure:

1. **stdio**: Direct async function for process communication
2. **SSE**: Starlette app with GET/POST endpoints and optional authentication
3. **StreamableHTTP**: Session-managed app with resumable connections

The `FastMCP` class generates these applications on-demand, configuring middleware, authentication, and routing based on server settings.

**Sources:** [src/mcp/server/fastmcp/server.py752-883](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L752-L883)

## Request Processing Flow

The following diagram shows how requests flow through the FastMCP architecture from transport to function execution:

```
```

**Sources:** [src/mcp/server/fastmcp/server.py308-312](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L308-L312) [src/mcp/server/fastmcp/utilities/func\_metadata.py68-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L68-L89)

This architecture enables FastMCP to provide a high-level, decorator-based interface while maintaining full compatibility with the MCP protocol and supporting multiple transport mechanisms.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [FastMCP Server Architecture](#fastmcp-server-architecture.md)
- [Core Architecture Overview](#core-architecture-overview.md)
- [FastMCP Main Server Class](#fastmcp-main-server-class.md)
- [Core Components](#core-components.md)
- [Decorator Interface](#decorator-interface.md)
- [Manager Subsystem Architecture](#manager-subsystem-architecture.md)
- [Function Registration Flow](#function-registration-flow.md)
- [Function Introspection System](#function-introspection-system.md)
- [FuncMetadata Components](#funcmetadata-components.md)
- [Structured Output Detection](#structured-output-detection.md)
- [Context Injection System](#context-injection-system.md)
- [Transport Integration Architecture](#transport-integration-architecture.md)
- [Transport Application Generation](#transport-application-generation.md)
- [Request Processing Flow](#request-processing-flow.md)
