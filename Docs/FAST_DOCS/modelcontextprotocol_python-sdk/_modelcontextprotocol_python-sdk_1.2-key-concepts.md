Key Concepts | modelcontextprotocol/python-sdk | DeepWiki

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

# Key Concepts

Relevant source files

- [README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md)
- [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py)
- [src/mcp/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py)

This document explains the fundamental concepts of the Model Context Protocol (MCP) Python SDK. It covers the core entities, protocol mechanics, and architectural patterns that developers need to understand when building MCP servers and clients. For specific implementation guidance on building servers, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For client-side development, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md).

## MCP Protocol Overview

The Model Context Protocol enables standardized communication between Large Language Models and external systems. The protocol defines how clients (typically LLM applications) can discover and interact with servers that expose tools, data, and interaction patterns.

```
```

**MCP Core Architecture**

Sources: [README.md84-194](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L84-L194) [src/mcp/types.py8-34](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L8-L34)

## Servers and Clients

### MCP Servers

Servers expose functionality and data to LLM applications. The MCP Python SDK provides two server implementation approaches:

- **FastMCP**: High-level decorator-based framework using `FastMCP` class
- **Low-level Server**: Direct protocol implementation using `Server` class

```
```

**Server Implementation Architecture**

Sources: [src/mcp/server/lowlevel/server.py1-66](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L1-L66) [README.md198-265](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L198-L265)

### MCP Clients

Clients connect to servers and facilitate communication with LLMs. The primary client implementation is `ClientSession`, which handles protocol negotiation, message routing, and connection management.

Sources: [README.md84-92](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L84-L92)

## Core MCP Entities

### Tools

Tools are executable functions that LLMs can call to perform actions or computations. They are defined using the `@tool` decorator in FastMCP or the `call_tool()` handler in low-level servers.

```
```

**Tool Lifecycle and Processing**

Tools support both structured and unstructured output. The `CallToolResult` type includes both `content` (unstructured) and `structuredContent` (structured) fields for maximum compatibility.

Sources: [README.md297-384](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L297-L384) [src/mcp/server/lowlevel/server.py465-547](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L465-L547) [src/mcp/types.py869-922](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L869-L922)

### Resources

Resources provide read-only access to data that LLMs can consume. They are identified by URIs and can return text, binary data, or multiple content blocks.

```
```

**Resource Architecture and Content Types**

Sources: [README.md266-296](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L266-L296) [src/mcp/types.py431-554](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L431-L554) [src/mcp/server/lowlevel/server.py311-367](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L311-L367)

### Prompts

Prompts are reusable templates that help structure LLM interactions. They can include parameters and return formatted message sequences.

```
```

**Prompt Template System**

Sources: [README.md490-517](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L490-L517) [src/mcp/types.py630-812](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L630-L812)

## Protocol and Message Flow

The MCP protocol uses JSON-RPC 2.0 for message exchange. Communication follows a request-response pattern with support for notifications.

```
```

**MCP Protocol Message Flow**

The protocol supports several core message types defined in `types.py`:

- **Requests**: `ClientRequest`, `ServerRequest` - expect responses
- **Notifications**: `ClientNotification`, `ServerNotification` - no response expected
- **Results**: `ClientResult`, `ServerResult` - responses to requests

Sources: [src/mcp/types.py82-348](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L82-L348) [README.md25-194](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L25-L194)

## Transport Layer

MCP supports multiple transport mechanisms for client-server communication:

```
```

**Transport Layer Architecture**

Each transport provides bidirectional communication with different characteristics:

- **stdio**: Process-based communication via stdin/stdout
- **SSE**: HTTP-based with server-sent events for real-time updates
- **StreamableHTTP**: Advanced HTTP transport with session management and resumability

Sources: [src/mcp/types.py124-193](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/types.py#L124-L193) Transport architecture from overview diagrams

## Server Implementations

### FastMCP Framework

`FastMCP` provides a decorator-based approach for rapid server development. It automatically handles protocol compliance, schema generation, and message routing.

```
```

**FastMCP Internal Architecture**

### Low-level Server

The `Server` class provides direct access to the MCP protocol with explicit handler registration using decorators like `list_tools()`, `call_tool()`, etc.

Sources: [src/mcp/server/lowlevel/server.py133-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/lowlevel/server.py#L133-L158) FastMCP concepts from overview diagrams

## Context and Session Management

### Request Context

The `Context` object provides access to MCP capabilities and request metadata within tool and resource functions.

```
```

**Context and Session Architecture**

The context system enables:

- **Logging**: Send log messages to clients via `LoggingMessageNotification`
- **Progress**: Report operation progress via `ProgressNotification`
- **Resource Access**: Read other resources via `ReadResourceRequest`
- **User Interaction**: Request additional information via `ElicitRequest`
- **LLM Sampling**: Generate text via `CreateMessageRequest`

### Session Lifecycle

Both `ClientSession` and `ServerSession` manage connection state, protocol version negotiation, and message routing throughout the connection lifetime.

Sources: [README.md580-646](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/README.md#L580-L646) [src/mcp/shared/context.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/context.py) (referenced), [src/mcp/server/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py) (referenced)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Key Concepts](#key-concepts.md)
- [MCP Protocol Overview](#mcp-protocol-overview.md)
- [Servers and Clients](#servers-and-clients.md)
- [MCP Servers](#mcp-servers.md)
- [MCP Clients](#mcp-clients.md)
- [Core MCP Entities](#core-mcp-entities.md)
- [Tools](#tools.md)
- [Resources](#resources.md)
- [Prompts](#prompts.md)
- [Protocol and Message Flow](#protocol-and-message-flow.md)
- [Transport Layer](#transport-layer.md)
- [Server Implementations](#server-implementations.md)
- [FastMCP Framework](#fastmcp-framework.md)
- [Low-level Server](#low-level-server.md)
- [Context and Session Management](#context-and-session-management.md)
- [Request Context](#request-context.md)
- [Session Lifecycle](#session-lifecycle.md)
