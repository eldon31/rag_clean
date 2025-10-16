jlowin/fastmcp | DeepWiki

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

# FastMCP Overview

Relevant source files

- [README.md](https://github.com/jlowin/fastmcp/blob/66221ed3/README.md)
- [docs/docs.json](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/docs.json)
- [docs/getting-started/welcome.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/getting-started/welcome.mdx)
- [src/fastmcp/\_\_init\_\_.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/__init__.py)
- [src/fastmcp/server/server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py)
- [src/fastmcp/settings.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/settings.py)
- [tests/server/test\_import\_server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py)
- [tests/server/test\_mount.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py)
- [tests/server/test\_server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server.py)

This document provides a high-level introduction to the FastMCP framework architecture, covering its core purpose, major system components, and how they work together to enable production-ready Model Context Protocol (MCP) applications.

For detailed server implementation patterns, see [FastMCP Server Core](jlowin/fastmcp/2-fastmcp-server-core.md). For client usage and transport mechanisms, see [FastMCP Client System](jlowin/fastmcp/3-fastmcp-client-system.md). For deployment and configuration specifics, see [Configuration Management](jlowin/fastmcp/7-configuration-management.md).

## What is FastMCP?

FastMCP is a comprehensive Python framework for building production-ready MCP servers and clients. The Model Context Protocol (MCP) is a standardized way to connect LLMs to tools and data sources, and FastMCP provides the infrastructure to make these connections robust, secure, and scalable.

At its core, FastMCP wraps the low-level MCP protocol with a high-level, Pythonic interface. The framework handles protocol details, authentication, deployment, and advanced patterns like server composition and proxying.

Sources: [src/fastmcp/server/server.py1-84](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1-L84) [README.md37-54](https://github.com/jlowin/fastmcp/blob/66221ed3/README.md#L37-L54) [docs/getting-started/welcome.mdx21-57](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/getting-started/welcome.mdx#L21-L57)

## Core Architecture Overview

FastMCP follows a layered architecture with clear separation between the high-level developer interface, protocol implementation, and transport layers.

### FastMCP System Components

```
```

Sources: [src/fastmcp/server/server.py125-266](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L125-L266) [src/fastmcp/\_\_init\_\_.py15-20](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/__init__.py#L15-L20) [src/fastmcp/server/low\_level.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/low_level.py) [src/fastmcp/tools/tool\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py) [src/fastmcp/resources/resource\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource_manager.py) [src/fastmcp/prompts/prompt\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt_manager.py)

### Request Flow Architecture

```
```

Sources: [src/fastmcp/server/server.py701-752](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L701-L752) [src/fastmcp/server/server.py397-406](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L397-L406) [src/fastmcp/tools/tool\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py)

## FastMCP Server Components

The `FastMCP` class serves as the central orchestrator, managing three core component types and their lifecycle.

### Component Manager System

| Component | Manager Class     | Decorator          | Key Methods                         |
| --------- | ----------------- | ------------------ | ----------------------------------- |
| Tools     | `ToolManager`     | `@server.tool`     | `add_tool()`, `call_tool()`         |
| Resources | `ResourceManager` | `@server.resource` | `add_resource()`, `read_resource()` |
| Prompts   | `PromptManager`   | `@server.prompt`   | `add_prompt()`, `render_prompt()`   |

The server initializes these managers in its constructor:

```
```

Sources: [src/fastmcp/server/server.py176-188](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L176-L188) [src/fastmcp/tools/tool\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py) [src/fastmcp/resources/resource\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource_manager.py) [src/fastmcp/prompts/prompt\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt_manager.py)

### Protocol Handler Registration

FastMCP registers MCP protocol handlers during initialization via `_setup_handlers()`:

```
```

Sources: [src/fastmcp/server/server.py387-395](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L387-L395) [src/fastmcp/server/low\_level.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/low_level.py)

## Transport and Client Architecture

FastMCP supports multiple transport mechanisms for different deployment scenarios:

### Transport Types

| Transport          | Use Case                      | Implementation                                     |
| ------------------ | ----------------------------- | -------------------------------------------------- |
| `stdio`            | Local development, CLI tools  | `stdio_server()` from MCP SDK                      |
| `http`/`sse`       | Web deployment, remote access | `create_sse_app()`, `create_streamable_http_app()` |
| `FastMCPTransport` | In-memory testing, embedding  | Direct server instance connection                  |

### Client Transport Resolution

The client automatically selects appropriate transports via `infer_transport()` based on the connection target:

```
```

Sources: [src/fastmcp/client/transports.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py) [src/fastmcp/server/http.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py) [src/fastmcp/client/client.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py)

## Advanced Server Patterns

FastMCP provides sophisticated patterns for building complex applications:

### Server Composition

FastMCP supports two composition patterns:

1. **Mounting (`mount`)**: Live delegation to child servers
2. **Importing (`import_server`)**: Static copying of components

```
```

### Proxy Servers

The `FastMCP.as_proxy()` method creates servers that act as intermediaries:

```
```

Sources: [tests/server/test\_mount.py19-67](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py#L19-L67) [tests/server/test\_import\_server.py10-34](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py#L10-L34) [src/fastmcp/server/proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py)

## Configuration and Settings

FastMCP uses a hierarchical settings system with environment variable support:

### Settings Structure

The `Settings` class provides configuration via environment variables prefixed with `FASTMCP_`:

- `FASTMCP_LOG_LEVEL`: Logging configuration
- `FASTMCP_SERVER_AUTH`: Authentication provider class path
- `FASTMCP_INCLUDE_TAGS`/`FASTMCP_EXCLUDE_TAGS`: Component filtering
- `FASTMCP_HOST`/`FASTMCP_PORT`: HTTP server configuration

### Global Settings Instance

FastMCP maintains a global settings instance accessible via `fastmcp.settings`:

```
```

Sources: [src/fastmcp/settings.py80-381](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/settings.py#L80-L381) [src/fastmcp/\_\_init\_\_.py8](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/__init__.py#L8-L8)

## Authentication and Security

FastMCP provides enterprise-grade authentication through the `AuthProvider` system:

### Authentication Providers

The framework includes built-in providers for major identity systems:

- `GoogleProvider`
- `GitHubProvider`
- `AzureProvider`
- `Auth0Provider`
- `WorkOSProvider`
- `JWTVerifier`

### Auth Integration

Authentication providers integrate with the server at initialization:

```
```

Sources: [src/fastmcp/server/server.py204-211](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L204-L211) [src/fastmcp/server/auth/](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/) [src/fastmcp/settings.py363-380](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/settings.py#L363-L380)

## Testing and Development Framework

FastMCP provides comprehensive testing utilities through direct server instance connections:

### In-Memory Testing

The `FastMCPTransport` enables efficient testing without process management:

```
```

### Test Utilities

The framework includes testing helpers in `fastmcp.utilities.tests`:

- `caplog_for_fastmcp()`: FastMCP-specific log capture
- `temporary_settings()`: Settings isolation for tests

Sources: [tests/server/test\_server.py14-67](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server.py#L14-L67) [src/fastmcp/utilities/tests.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/tests.py) [src/fastmcp/client/transports.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [FastMCP Overview](#fastmcp-overview.md)
- [What is FastMCP?](#what-is-fastmcp.md)
- [Core Architecture Overview](#core-architecture-overview.md)
- [FastMCP System Components](#fastmcp-system-components.md)
- [Request Flow Architecture](#request-flow-architecture.md)
- [FastMCP Server Components](#fastmcp-server-components.md)
- [Component Manager System](#component-manager-system.md)
- [Protocol Handler Registration](#protocol-handler-registration.md)
- [Transport and Client Architecture](#transport-and-client-architecture.md)
- [Transport Types](#transport-types.md)
- [Client Transport Resolution](#client-transport-resolution.md)
- [Advanced Server Patterns](#advanced-server-patterns.md)
- [Server Composition](#server-composition.md)
- [Proxy Servers](#proxy-servers.md)
- [Configuration and Settings](#configuration-and-settings.md)
- [Settings Structure](#settings-structure.md)
- [Global Settings Instance](#global-settings-instance.md)
- [Authentication and Security](#authentication-and-security.md)
- [Authentication Providers](#authentication-providers.md)
- [Auth Integration](#auth-integration.md)
- [Testing and Development Framework](#testing-and-development-framework.md)
- [In-Memory Testing](#in-memory-testing.md)
- [Test Utilities](#test-utilities.md)
