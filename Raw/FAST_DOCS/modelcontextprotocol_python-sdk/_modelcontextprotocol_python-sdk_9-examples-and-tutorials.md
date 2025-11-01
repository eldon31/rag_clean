Examples & Tutorials | modelcontextprotocol/python-sdk | DeepWiki

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

# Examples & Tutorials

Relevant source files

- [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py)
- [examples/servers/simple-resource/mcp\_simple\_resource/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py)
- [examples/servers/simple-tool/mcp\_simple\_tool/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py)

This document provides practical examples and tutorials for building MCP servers and clients using the Python SDK. It demonstrates both low-level server implementations and high-level patterns, showing how to create functional MCP servers that expose tools, resources, and prompts to clients.

For detailed FastMCP framework usage with decorators, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For client implementation patterns, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md). For low-level protocol details, see [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md).

## Overview of Example Categories

The MCP Python SDK includes several reference implementations that demonstrate core functionality:

| Example Type        | Purpose                      | Key Components                                 |
| ------------------- | ---------------------------- | ---------------------------------------------- |
| **Resource Server** | Expose data and content      | `list_resources()`, `read_resource()` handlers |
| **Tool Server**     | Provide executable functions | `list_tools()`, `call_tool()` handlers         |
| **Prompt Server**   | Offer prompt templates       | `list_prompts()`, `get_prompt()` handlers      |

All examples support multiple transport protocols (stdio, SSE) and follow consistent patterns using the low-level `Server` class from `mcp.server.lowlevel`.

## Low-Level Server Implementation Patterns

### Basic Server Structure

The foundation of all MCP servers follows this pattern:

```
```

**Sources:** [examples/servers/simple-resource/mcp\_simple\_resource/server.py34-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L34-L93) [examples/servers/simple-tool/mcp\_simple\_tool/server.py30-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L30-L93) [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py42-112](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L42-L112)

### Resource Server Example

The resource server demonstrates how to expose readable data sources through the MCP protocol:

```
```

**Key Implementation Details:**

- **Resource Registry**: [examples/servers/simple-resource/mcp\_simple\_resource/server.py9-22](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L9-L22) defines `SAMPLE_RESOURCES` dictionary containing static content
- **List Handler**: [examples/servers/simple-resource/mcp\_simple\_resource/server.py36-47](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L36-L47) creates `types.Resource` objects with `FileUrl` URIs
- **Read Handler**: [examples/servers/simple-resource/mcp\_simple\_resource/server.py49-58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L49-L58) parses URIs and returns `ReadResourceContents`

**Sources:** [examples/servers/simple-resource/mcp\_simple\_resource/server.py9-58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L9-L58)

### Tool Server Example

The tool server shows how to expose executable functions that clients can invoke:

```
```

**Key Implementation Details:**

- **Tool Function**: [examples/servers/simple-tool/mcp\_simple\_tool/server.py11-18](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L11-L18) implements `fetch_website()` with `create_mcp_http_client`
- **Schema Definition**: [examples/servers/simple-tool/mcp\_simple\_tool/server.py47-56](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L47-L56) defines JSON schema for `url` parameter
- **Tool Execution**: [examples/servers/simple-tool/mcp\_simple\_tool/server.py32-38](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L32-L38) validates arguments and calls core function

**Sources:** [examples/servers/simple-tool/mcp\_simple\_tool/server.py11-58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L11-L58)

### Prompt Server Example

The prompt server demonstrates how to create parameterized prompt templates:

**Key Implementation Details:**

- **Message Creation**: [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py8-30](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L8-L30) implements `create_messages()` function with optional context and topic
- **Prompt Registration**: [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py44-64](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L44-L64) defines `types.Prompt` with `types.PromptArgument` specifications
- **Template Logic**: [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py66-77](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L66-L77) processes arguments and returns `types.GetPromptResult`

**Sources:** [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py8-77](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L8-L77)

## Transport Configuration Patterns

All example servers support dual transport modes using a consistent CLI pattern:

### Transport Selection Logic

```
```

**Implementation Details:**

- **CLI Setup**: [examples/servers/simple-resource/mcp\_simple\_resource/server.py25-32](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L25-L32) defines consistent command-line interface
- **stdio Transport**: [examples/servers/simple-resource/mcp\_simple\_resource/server.py84-91](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L84-L91) uses `stdio_server()` context manager with `anyio.run()`
- **SSE Transport**: [examples/servers/simple-resource/mcp\_simple\_resource/server.py60-83](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L60-L83) integrates `SseServerTransport` with Starlette ASGI application

**Sources:** [examples/servers/simple-resource/mcp\_simple\_resource/server.py25-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L25-L93) [examples/servers/simple-tool/mcp\_simple\_tool/server.py21-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L21-L93) [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py33-112](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L33-L112)

## Common Development Patterns

### Error Handling

All examples implement consistent error handling patterns:

- Resource servers validate URIs and check resource existence [examples/servers/simple-resource/mcp\_simple\_resource/server.py50-56](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L50-L56)
- Tool servers validate tool names and required arguments [examples/servers/simple-tool/mcp\_simple\_tool/server.py34-37](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L34-L37)
- Prompt servers validate prompt names before processing [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py68-69](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L68-L69)

### Type System Integration

Examples demonstrate proper use of MCP type system:

- Import `mcp.types` for protocol types [examples/servers/simple-resource/mcp\_simple\_resource/server.py3](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L3-L3)
- Use `types.Resource`, `types.Tool`, `types.Prompt` for metadata [examples/servers/simple-resource/mcp\_simple\_resource/server.py39-45](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L39-L45)
- Return appropriate content types like `ReadResourceContents` and `TextContent` [examples/servers/simple-resource/mcp\_simple\_resource/server.py58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L58-L58)

For more advanced server implementations using the FastMCP framework, see [Server Examples](modelcontextprotocol/python-sdk/9.1-server-examples.md). For client usage examples, see [Client Examples](modelcontextprotocol/python-sdk/9.2-client-examples.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Examples & Tutorials](#examples-tutorials.md)
- [Overview of Example Categories](#overview-of-example-categories.md)
- [Low-Level Server Implementation Patterns](#low-level-server-implementation-patterns.md)
- [Basic Server Structure](#basic-server-structure.md)
- [Resource Server Example](#resource-server-example.md)
- [Tool Server Example](#tool-server-example.md)
- [Prompt Server Example](#prompt-server-example.md)
- [Transport Configuration Patterns](#transport-configuration-patterns.md)
- [Transport Selection Logic](#transport-selection-logic.md)
- [Common Development Patterns](#common-development-patterns.md)
- [Error Handling](#error-handling.md)
- [Type System Integration](#type-system-integration.md)
