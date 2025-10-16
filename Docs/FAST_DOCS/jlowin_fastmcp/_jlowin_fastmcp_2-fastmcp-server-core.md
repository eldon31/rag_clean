FastMCP Server Core | jlowin/fastmcp | DeepWiki

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

# FastMCP Server Core

Relevant source files

- [src/fastmcp/\_\_init\_\_.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/__init__.py)
- [src/fastmcp/server/server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py)
- [src/fastmcp/settings.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/settings.py)
- [tests/server/test\_import\_server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py)
- [tests/server/test\_mount.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py)
- [tests/server/test\_server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server.py)

## Purpose and Scope

The FastMCP Server Core is the central orchestrating component of the FastMCP framework, implemented primarily in the `FastMCP` class. This document covers the core server architecture, component management, MCP protocol integration, server composition patterns, and lifecycle management.

For information about individual component types (Tools, Resources, Prompts), see [Component System Architecture](jlowin/fastmcp/2.1-component-system-architecture.md). For client-side interaction with FastMCP servers, see [FastMCP Client System](jlowin/fastmcp/3-fastmcp-client-system.md). For HTTP deployment and authentication, see [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md).

## Core Server Architecture

The `FastMCP` class serves as the primary interface for creating MCP servers, providing a high-level, Pythonic API that wraps the low-level MCP protocol implementation.

### FastMCP Server Structure

```
```

The `FastMCP` class maintains three specialized managers for different component types, wraps a low-level MCP server for protocol handling, and supports server composition through mounting and importing.

**Sources:** [src/fastmcp/server/server.py125-202](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L125-L202) [src/fastmcp/server/server.py176-188](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L176-L188)

### Component Registration Flow

```
```

Component registration flows from high-level decorators through component creation to manager-specific storage dictionaries.

**Sources:** [src/fastmcp/server/server.py858-881](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L858-L881) [src/fastmcp/server/server.py945-1058](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L945-L1058) [tests/server/test\_server.py141-151](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server.py#L141-L151)

## MCP Protocol Integration

FastMCP integrates with the Model Context Protocol by wrapping a `LowLevelServer` and implementing the required MCP handlers.

### Protocol Handler Architecture

```
```

The protocol integration uses a two-layer approach: MCP handlers that manage protocol specifics and internal handlers that apply middleware and delegate to component managers.

**Sources:** [src/fastmcp/server/server.py387-396](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L387-L396) [src/fastmcp/server/server.py522-533](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L522-L533) [src/fastmcp/server/server.py701-727](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L701-L727)

### Handler Registration Process

During server initialization, the `_setup_handlers()` method registers protocol handlers with the underlying `LowLevelServer`:

| Handler Method        | MCP Operation    | Component Type |
| --------------------- | ---------------- | -------------- |
| `_mcp_list_tools`     | `tools/list`     | Tools          |
| `_mcp_call_tool`      | `tools/call`     | Tools          |
| `_mcp_list_resources` | `resources/list` | Resources      |
| `_mcp_read_resource`  | `resources/read` | Resources      |
| `_mcp_list_prompts`   | `prompts/list`   | Prompts        |
| `_mcp_get_prompt`     | `prompts/get`    | Prompts        |

**Sources:** [src/fastmcp/server/server.py387-396](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L387-L396)

## Server Composition and Mounting

FastMCP supports two patterns for combining multiple servers: **mounting** (live delegation) and **importing** (static copying).

### Mount vs Import Architecture

```
```

Mounting creates live links to other servers, while importing creates static copies of components.

**Sources:** [src/fastmcp/server/server.py175](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L175-L175) [tests/server/test\_mount.py19-47](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py#L19-L47) [tests/server/test\_import\_server.py10-34](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py#L10-L34)

### Component Prefixing Behavior

When servers are mounted or imported with prefixes, component names are prefixed according to these patterns:

| Component Type     | Prefix Format                      | Example                 |
| ------------------ | ---------------------------------- | ----------------------- |
| Tools              | `{prefix}_{tool_name}`             | `api_get_data`          |
| Resources          | `{protocol}://{prefix}/{path}`     | `data://api/users`      |
| Resource Templates | `{protocol}://{prefix}/{template}` | `users://api/{user_id}` |
| Prompts            | `{prefix}_{prompt_name}`           | `api_greeting`          |

**Sources:** [src/fastmcp/server/server.py1395-1420](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1395-L1420) [tests/server/test\_mount.py978-1024](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py#L978-L1024)

## Middleware System

FastMCP implements a middleware system that allows request processing to be modified through a chain of middleware functions.

### Middleware Execution Flow

```
```

Middleware functions receive a `MiddlewareContext` and a `call_next` function, allowing them to process requests before and after the main handler.

**Sources:** [src/fastmcp/server/server.py397-406](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L397-L406) [src/fastmcp/server/server.py553-564](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L553-L564)

### MiddlewareContext Structure

The `MiddlewareContext` provides access to:

- `message`: The MCP request parameters
- `source`: Request source ("client")
- `type`: Request type ("request")
- `method`: MCP method name (e.g., "tools/call")
- `fastmcp_context`: Current FastMCP context object

**Sources:** [src/fastmcp/server/server.py555-561](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L555-L561)

## Lifecycle Management

FastMCP servers support lifecycle management through lifespan context managers, similar to FastAPI applications.

### Lifespan Context Pattern

```
```

Lifespan functions allow setup and cleanup operations to be performed when servers start and stop.

**Sources:** [src/fastmcp/server/server.py93-123](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L93-L123) [src/fastmcp/server/server.py191-202](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L191-L202)

## Configuration and Settings

FastMCP server behavior is controlled through the global `Settings` object and constructor parameters.

### Key Configuration Areas

| Setting Category    | Key Parameters                 | Purpose                               |
| ------------------- | ------------------------------ | ------------------------------------- |
| Component Filtering | `include_tags`, `exclude_tags` | Control which components are exposed  |
| Error Handling      | `mask_error_details`           | Control error information disclosure  |
| Resource Prefixing  | `resource_prefix_format`       | Control URI prefixing behavior        |
| Authentication      | `server_auth`                  | Automatic auth provider configuration |
| Metadata            | `include_fastmcp_meta`         | Control FastMCP metadata inclusion    |

**Sources:** [src/fastmcp/settings.py293-333](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/settings.py#L293-L333) [src/fastmcp/server/server.py126-169](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L126-L169)

### Component Enablement Logic

The `_should_enable_component()` method determines whether components are exposed based on:

1. Component `enabled` status
2. Global `include_tags` filtering (if any component tags match)
3. Global `exclude_tags` filtering (if any component tags match)

Components are enabled if they pass all filtering criteria.

**Sources:** [src/fastmcp/server/server.py1507-1530](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1507-L1530)

## Transport Integration

FastMCP servers can run over multiple transport protocols through the `run()` and `run_async()` methods.

### Supported Transports

```
```

The transport is selected via the `transport` parameter to `run()` or `run_async()`.

**Sources:** [src/fastmcp/server/server.py336-364](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L336-L364) [src/fastmcp/server/server.py1567-1583](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1567-L1583)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [FastMCP Server Core](#fastmcp-server-core.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Core Server Architecture](#core-server-architecture.md)
- [FastMCP Server Structure](#fastmcp-server-structure.md)
- [Component Registration Flow](#component-registration-flow.md)
- [MCP Protocol Integration](#mcp-protocol-integration.md)
- [Protocol Handler Architecture](#protocol-handler-architecture.md)
- [Handler Registration Process](#handler-registration-process.md)
- [Server Composition and Mounting](#server-composition-and-mounting.md)
- [Mount vs Import Architecture](#mount-vs-import-architecture.md)
- [Component Prefixing Behavior](#component-prefixing-behavior.md)
- [Middleware System](#middleware-system.md)
- [Middleware Execution Flow](#middleware-execution-flow.md)
- [MiddlewareContext Structure](#middlewarecontext-structure.md)
- [Lifecycle Management](#lifecycle-management.md)
- [Lifespan Context Pattern](#lifespan-context-pattern.md)
- [Configuration and Settings](#configuration-and-settings.md)
- [Key Configuration Areas](#key-configuration-areas.md)
- [Component Enablement Logic](#component-enablement-logic.md)
- [Transport Integration](#transport-integration.md)
- [Supported Transports](#supported-transports.md)
