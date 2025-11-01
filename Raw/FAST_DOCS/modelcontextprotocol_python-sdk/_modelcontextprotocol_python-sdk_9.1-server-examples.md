Server Examples | modelcontextprotocol/python-sdk | DeepWiki

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

# Server Examples

Relevant source files

- [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py)
- [examples/servers/simple-resource/mcp\_simple\_resource/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py)
- [examples/servers/simple-streamablehttp-stateless/mcp\_simple\_streamablehttp\_stateless/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp-stateless/mcp_simple_streamablehttp_stateless/server.py)
- [examples/servers/simple-streamablehttp/mcp\_simple\_streamablehttp/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp/mcp_simple_streamablehttp/server.py)
- [examples/servers/simple-tool/mcp\_simple\_tool/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py)
- [examples/snippets/servers/direct\_execution.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/direct_execution.py)
- [examples/snippets/servers/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/structured_output.py)
- [tests/issues/test\_88\_random\_error.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_88_random_error.py)
- [tests/server/fastmcp/test\_integration.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_integration.py)

This document provides comprehensive examples of MCP server implementations using both the low-level `Server` class and the high-level `FastMCP` framework. These examples demonstrate various MCP capabilities including tools, resources, prompts, progress reporting, and different transport mechanisms.

For client-side examples and integration patterns, see [Client Examples](modelcontextprotocol/python-sdk/9.2-client-examples.md). For detailed FastMCP framework documentation, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md).

## Server Implementation Approaches

The MCP Python SDK provides two primary approaches for building servers, each suited for different use cases and complexity levels.

### Server Implementation Architecture

```
```

Sources: [examples/servers/simple-resource/mcp\_simple\_resource/server.py1-94](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L1-L94) [examples/servers/simple-tool/mcp\_simple\_tool/server.py1-94](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L1-L94) [examples/snippets/servers/structured\_output.py1-98](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/structured_output.py#L1-L98)

## Low-Level Server Examples

The low-level `Server` class provides direct control over MCP protocol handling and is suitable for complex server implementations requiring fine-grained control.

### Basic Resource Server

The simple resource server demonstrates fundamental resource serving capabilities using the low-level `Server` class.

```
```

Sources: [examples/servers/simple-resource/mcp\_simple\_resource/server.py34-58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L34-L58)

### Basic Tool Server

The simple tool server shows HTTP client functionality and tool execution patterns.

```
```

Sources: [examples/servers/simple-tool/mcp\_simple\_tool/server.py32-58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L32-L58)

### Basic Prompt Server

The simple prompt server demonstrates template-based prompt generation.

```
```

Sources: [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py44-77](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L44-L77)

## StreamableHTTP Transport Examples

StreamableHTTP transport enables bidirectional communication with session management and resumability features.

### StreamableHTTP with Event Store

```
```

Sources: [examples/servers/simple-streamablehttp/mcp\_simple\_streamablehttp/server.py47-165](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp/mcp_simple_streamablehttp/server.py#L47-L165)

### Stateless StreamableHTTP

```
```

Sources: [examples/servers/simple-streamablehttp-stateless/mcp\_simple\_streamablehttp\_stateless/server.py97-140](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp-stateless/mcp_simple_streamablehttp_stateless/server.py#L97-L140)

## FastMCP Framework Examples

FastMCP provides a decorator-based approach for rapid server development with automatic schema generation and simplified setup.

### Structured Output Example

```
```

Sources: [examples/snippets/servers/structured\_output.py9-98](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/structured_output.py#L9-L98)

### Direct Execution Example

```
```

Sources: [examples/snippets/servers/direct\_execution.py10-27](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/direct_execution.py#L10-L27)

## Feature-Specific Examples

The integration tests demonstrate various MCP features through focused example servers.

### Progress Reporting

```
```

Sources: [tests/server/fastmcp/test\_integration.py392-440](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_integration.py#L392-L440)

### Notification System

```
```

Sources: [tests/server/fastmcp/test\_integration.py524-569](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_integration.py#L524-L569)

### Sampling and Elicitation

```
```

Sources: [tests/server/fastmcp/test\_integration.py442-521](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_integration.py#L442-L521)

## Transport Configuration Patterns

All server examples support multiple transport configurations, allowing flexible deployment options.

### Universal Transport Pattern

```
```

Sources: [examples/servers/simple-resource/mcp\_simple\_resource/server.py60-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py#L60-L93) [examples/servers/simple-tool/mcp\_simple\_tool/server.py60-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py#L60-L93) [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py79-112](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py#L79-L112)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Server Examples](#server-examples.md)
- [Server Implementation Approaches](#server-implementation-approaches.md)
- [Server Implementation Architecture](#server-implementation-architecture.md)
- [Low-Level Server Examples](#low-level-server-examples.md)
- [Basic Resource Server](#basic-resource-server.md)
- [Basic Tool Server](#basic-tool-server.md)
- [Basic Prompt Server](#basic-prompt-server.md)
- [StreamableHTTP Transport Examples](#streamablehttp-transport-examples.md)
- [StreamableHTTP with Event Store](#streamablehttp-with-event-store.md)
- [Stateless StreamableHTTP](#stateless-streamablehttp.md)
- [FastMCP Framework Examples](#fastmcp-framework-examples.md)
- [Structured Output Example](#structured-output-example.md)
- [Direct Execution Example](#direct-execution-example.md)
- [Feature-Specific Examples](#feature-specific-examples.md)
- [Progress Reporting](#progress-reporting.md)
- [Notification System](#notification-system.md)
- [Sampling and Elicitation](#sampling-and-elicitation.md)
- [Transport Configuration Patterns](#transport-configuration-patterns.md)
- [Universal Transport Pattern](#universal-transport-pattern.md)
