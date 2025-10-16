Server Composition and Proxying | jlowin/fastmcp | DeepWiki

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

# Server Composition and Proxying

Relevant source files

- [src/fastmcp/\_\_init\_\_.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/__init__.py)
- [src/fastmcp/client/client.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/client.py)
- [src/fastmcp/client/transports.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py)
- [src/fastmcp/mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/mcp_config.py)
- [src/fastmcp/server/proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py)
- [src/fastmcp/server/server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py)
- [src/fastmcp/settings.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/settings.py)
- [src/fastmcp/utilities/mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/mcp_config.py)
- [tests/client/test\_client.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_client.py)
- [tests/client/test\_stdio.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_stdio.py)
- [tests/server/test\_import\_server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py)
- [tests/server/test\_mount.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py)
- [tests/server/test\_server.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server.py)

Server composition and proxying enables FastMCP servers to combine functionality from multiple other servers, either through live delegation (mounting) or static copying (importing). This system allows complex applications to be built by composing smaller, focused servers while maintaining clean separation of concerns.

For information about the core FastMCP server architecture, see [2](jlowin/fastmcp/2-fastmcp-server-core.md). For details about component management and registration, see [2.1](jlowin/fastmcp/2.1-component-system-architecture.md).

## Overview

FastMCP provides three primary mechanisms for server composition:

- **Mounting** - Live delegation to child servers with automatic prefix handling
- **Importing** - Static copying of components from other servers
- **Proxying** - Transparent forwarding to remote MCP-compliant servers

All composition methods support automatic prefixing of component names to avoid conflicts and provide clear namespacing.

## Mount System Architecture

The mount system enables live delegation to child FastMCP servers. When a component is requested, the parent server forwards the request to the appropriate mounted server in real-time.

### Mount System Core Components

```
```

**Sources:** [src/fastmcp/server/server.py175](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L175-L175) [src/fastmcp/server/server.py1260-1332](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1260-L1332)

### Mount Method Implementation

The `mount` method in `FastMCP` registers child servers for live delegation:

```
```

**Sources:** [src/fastmcp/server/server.py1260-1332](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1260-L1332) [tests/server/test\_mount.py16-68](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py#L16-L68)

## Import System Architecture

The import system performs static copying of components from other servers. Components are copied once at import time and become part of the importing server.

### Import vs Mount Comparison

```
```

**Sources:** [src/fastmcp/server/server.py1334-1421](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1334-L1421) [tests/server/test\_import\_server.py10-34](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py#L10-L34)

### Import Method Implementation

The `import_server` method copies components with prefix handling:

```
```

**Sources:** [src/fastmcp/server/server.py1334-1421](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1334-L1421) [tests/server/test\_import\_server.py61-89](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py#L61-L89)

## Proxy System Architecture

The proxy system enables FastMCP servers to act as transparent proxies to remote MCP-compliant servers. This is implemented through specialized managers and components.

### Proxy System Core Components

```
```

**Sources:** [src/fastmcp/server/proxy.py454-519](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py#L454-L519) [src/fastmcp/server/proxy.py69-121](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py#L69-L121)

### FastMCPProxy Creation Methods

FastMCP provides two ways to create proxy servers:

```
```

**Sources:** [src/fastmcp/server/server.py1555-1610](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1555-L1610) [src/fastmcp/server/proxy.py460-508](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py#L460-L508)

## Prefix Handling System

All composition methods support automatic prefixing to avoid component name conflicts. The prefix handling varies by component type.

### Prefix Application Rules

```
```

**Sources:** [src/fastmcp/server/server.py1423-1553](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L1423-L1553) [src/fastmcp/server/server.py2157-2205](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L2157-L2205)

### Resource Prefix Utilities

FastMCP provides utility functions for resource prefix manipulation:

| Function                   | Purpose                    | Example                               |
| -------------------------- | -------------------------- | ------------------------------------- |
| `add_resource_prefix()`    | Add prefix to resource URI | `data://users` → `data://api/users`   |
| `remove_resource_prefix()` | Remove prefix from URI     | `data://api/users` → `data://users`   |
| `has_resource_prefix()`    | Check if URI has prefix    | Returns `True` for `data://api/users` |

**Sources:** [src/fastmcp/server/server.py2157-2205](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L2157-L2205) [tests/server/test\_server.py22-26](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server.py#L22-L26)

## Component Request Flow

The following diagram shows how requests flow through the composition system:

```
```

**Sources:** [src/fastmcp/server/server.py729-752](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/server.py#L729-L752) [src/fastmcp/server/proxy.py107-121](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py#L107-L121) [src/fastmcp/server/proxy.py280-296](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py#L280-L296)

## Advanced Composition Patterns

### Multi-Level Composition

Servers can be composed in multiple levels, with prefixes accumulating:

```
```

**Sources:** [tests/server/test\_import\_server.py249-283](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py#L249-L283) [tests/server/test\_mount.py466-509](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py#L466-L509)

### Mixed Composition Strategies

A single parent server can use multiple composition strategies simultaneously:

```
```

**Sources:** [tests/server/test\_mount.py210-238](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_mount.py#L210-L238) [tests/server/test\_import\_server.py36-58](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_import_server.py#L36-L58) [src/fastmcp/server/proxy.py454-519](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/proxy.py#L454-L519)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Server Composition and Proxying](#server-composition-and-proxying.md)
- [Overview](#overview.md)
- [Mount System Architecture](#mount-system-architecture.md)
- [Mount System Core Components](#mount-system-core-components.md)
- [Mount Method Implementation](#mount-method-implementation.md)
- [Import System Architecture](#import-system-architecture.md)
- [Import vs Mount Comparison](#import-vs-mount-comparison.md)
- [Import Method Implementation](#import-method-implementation.md)
- [Proxy System Architecture](#proxy-system-architecture.md)
- [Proxy System Core Components](#proxy-system-core-components.md)
- [FastMCPProxy Creation Methods](#fastmcpproxy-creation-methods.md)
- [Prefix Handling System](#prefix-handling-system.md)
- [Prefix Application Rules](#prefix-application-rules.md)
- [Resource Prefix Utilities](#resource-prefix-utilities.md)
- [Component Request Flow](#component-request-flow.md)
- [Advanced Composition Patterns](#advanced-composition-patterns.md)
- [Multi-Level Composition](#multi-level-composition.md)
- [Mixed Composition Strategies](#mixed-composition-strategies.md)
