FastMCP Server Framework | modelcontextprotocol/python-sdk | DeepWiki

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

# FastMCP Server Framework

Relevant source files

- [src/mcp/server/fastmcp/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py)
- [tests/server/fastmcp/test\_server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_server.py)

FastMCP is a high-level, decorator-based framework for building Model Context Protocol (MCP) servers in Python. It provides an ergonomic interface that simplifies server development through automatic function introspection, context injection, and seamless integration with multiple transport protocols.

For low-level server implementation details, see [Low-Level Server Implementation](modelcontextprotocol/python-sdk/6-low-level-server-implementation.md). For client-side components, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md). For transport layer specifics, see [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md).

## Overview

FastMCP abstracts away the complexities of the MCP protocol by providing a decorator-based API that automatically converts Python functions into MCP tools, resources, and prompts. The framework handles JSON schema generation, input validation, output conversion, and protocol message handling.

### FastMCP Core Architecture

```
```

Sources: [src/mcp/server/fastmcp/server.py122-209](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L122-L209) [src/mcp/server/fastmcp/server.py268-280](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L268-L280)

## Core Components

### FastMCP Class

The `FastMCP` class serves as the central orchestrator, managing all server components and providing the decorator-based API. It wraps a low-level `MCPServer` instance while providing higher-level abstractions.

| Component  | Purpose                  | Key Methods                                     |
| ---------- | ------------------------ | ----------------------------------------------- |
| `FastMCP`  | Main server class        | `tool()`, `resource()`, `prompt()`, `run()`     |
| `Settings` | Configuration management | Environment variable integration                |
| `Context`  | Request context access   | `log()`, `report_progress()`, `read_resource()` |

### Manager Classes

FastMCP uses specialized manager classes to handle different types of MCP entities:

```
```

Sources: [src/mcp/server/fastmcp/server.py181-183](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L181-L183) [src/mcp/server/fastmcp/server.py270-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L270-L279)

## Decorator-Based API

### Tool Registration

The `@tool()` decorator converts Python functions into MCP tools with automatic schema generation:

```
```

The decorator supports several parameters for customization:

| Parameter           | Type           | Purpose                                      |
| ------------------- | -------------- | -------------------------------------------- |
| `name`              | `str \| None`  | Custom tool name (defaults to function name) |
| `title`             | `str \| None`  | Human-readable title                         |
| `description`       | `str \| None`  | Tool description                             |
| `structured_output` | `bool \| None` | Controls output schema generation            |

Sources: [src/mcp/server/fastmcp/server.py393-451](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L393-L451) [tests/server/fastmcp/test\_server.py146-153](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_server.py#L146-L153)

### Resource Registration

Resources can be registered as static resources or parameterized templates:

```
```

The framework automatically detects whether a resource should be treated as a template based on URI parameters and function signature.

Sources: [src/mcp/server/fastmcp/server.py479-578](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L479-L578) [tests/server/fastmcp/test\_server.py701-827](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_server.py#L701-L827)

### Prompt Registration

Prompts are registered using the `@prompt()` decorator and return message structures:

```
```

Sources: [src/mcp/server/fastmcp/server.py588-641](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L588-L641) [tests/server/fastmcp/test\_server.py1094-1284](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_server.py#L1094-L1284)

## Context System

### Context Injection

The `Context` class provides access to MCP capabilities and is automatically injected into functions that declare it as a parameter:

```
```

### Context Methods

The `Context` class provides several methods for interacting with the MCP session:

| Method              | Purpose                   | Parameters                        |
| ------------------- | ------------------------- | --------------------------------- |
| `log()`             | Send log messages         | `level`, `message`, `logger_name` |
| `report_progress()` | Report operation progress | `progress`, `total`, `message`    |
| `read_resource()`   | Access other resources    | `uri`                             |
| `elicit()`          | Request user input        | `message`, `schema`               |

Sources: [src/mcp/server/fastmcp/server.py1043-1223](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L1043-L1223) [tests/server/fastmcp/test\_server.py835-1092](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_server.py#L835-L1092)

## Transport Integration

FastMCP supports multiple transport protocols through dedicated application factories:

### Transport Applications

```
```

### Transport-Specific Features

Each transport provides specific capabilities:

| Transport          | Use Case                          | Key Features                                 |
| ------------------ | --------------------------------- | -------------------------------------------- |
| **stdio**          | Process-based communication       | Simple stdin/stdout JSON-RPC                 |
| **SSE**            | Web-based real-time communication | Server-sent events with HTTP POST            |
| **StreamableHTTP** | Resumable sessions                | Bidirectional streaming, session persistence |

Sources: [src/mcp/server/fastmcp/server.py687-724](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L687-L724) [src/mcp/server/fastmcp/server.py752-990](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L752-L990)

## Configuration and Settings

### Settings Management

The `Settings` class provides comprehensive configuration management with environment variable support:

```
```

Settings can be configured via:

- Environment variables with `FASTMCP_` prefix
- `.env` files
- Direct parameter passing

### Authentication Integration

FastMCP supports OAuth 2.0 authentication through integrated middleware:

```
```

Sources: [src/mcp/server/fastmcp/server.py56-108](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L56-L108) [src/mcp/server/fastmcp/server.py152-170](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L152-L170) [src/mcp/server/fastmcp/server.py792-982](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/server.py#L792-L982)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [FastMCP Server Framework](#fastmcp-server-framework.md)
- [Overview](#overview.md)
- [FastMCP Core Architecture](#fastmcp-core-architecture.md)
- [Core Components](#core-components.md)
- [FastMCP Class](#fastmcp-class.md)
- [Manager Classes](#manager-classes.md)
- [Decorator-Based API](#decorator-based-api.md)
- [Tool Registration](#tool-registration.md)
- [Resource Registration](#resource-registration.md)
- [Prompt Registration](#prompt-registration.md)
- [Context System](#context-system.md)
- [Context Injection](#context-injection.md)
- [Context Methods](#context-methods.md)
- [Transport Integration](#transport-integration.md)
- [Transport Applications](#transport-applications.md)
- [Transport-Specific Features](#transport-specific-features.md)
- [Configuration and Settings](#configuration-and-settings.md)
- [Settings Management](#settings-management.md)
- [Authentication Integration](#authentication-integration.md)
