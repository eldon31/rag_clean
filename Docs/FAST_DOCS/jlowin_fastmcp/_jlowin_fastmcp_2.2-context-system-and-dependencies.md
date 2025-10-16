Context System and Dependencies | jlowin/fastmcp | DeepWiki

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

# Context System and Dependencies

Relevant source files

- [examples/get\_file.py](https://github.com/jlowin/fastmcp/blob/66221ed3/examples/get_file.py)
- [src/fastmcp/server/context.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py)
- [src/fastmcp/utilities/types.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py)
- [tests/server/test\_context.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_context.py)
- [tests/utilities/test\_types.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/test_types.py)

This section covers the Context object system and dependency injection mechanisms in FastMCP. The `Context` class provides tools and resources with access to MCP protocol capabilities like logging, sampling, and resource reading, while the dependency injection system automatically provides these capabilities to user functions based on type annotations.

For information about how components (tools, resources, prompts) are created and managed, see [Component System Architecture](jlowin/fastmcp/2.1-component-system-architecture.md). For details about server composition and mounting, see [Server Composition and Proxying](jlowin/fastmcp/2.3-server-composition-and-proxying.md).

## Context Object Architecture

The `Context` class serves as the primary interface between user-defined tools/resources and the underlying MCP protocol capabilities. It provides a clean, Pythonic API for accessing server session functionality.

```
```

**Sources:** [src/fastmcp/server/context.py79-123](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L79-L123) [src/fastmcp/server/context.py159-169](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L159-L169)

### Context Lifecycle Management

The `Context` object implements async context manager semantics with inheritance-based state management:

```
```

**Sources:** [src/fastmcp/server/context.py53](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L53-L53) [src/fastmcp/server/context.py138-157](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L138-L157) [src/fastmcp/server/context.py584-590](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L584-L590)

## Dependency Injection System

FastMCP uses type annotation-based dependency injection to automatically provide `Context` objects and other dependencies to user functions.

```
```

**Sources:** [src/fastmcp/utilities/types.py152-176](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L152-L176) [src/fastmcp/utilities/types.py130-149](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L130-L149)

### Type Annotation Processing

The system handles complex type annotations including unions, forward references, and `Annotated` types:

| Type Pattern      | Example                                  | Processing                            |
| ----------------- | ---------------------------------------- | ------------------------------------- |
| Direct Type       | `ctx: Context`                           | Direct match via `issubclass_safe()`  |
| Union Type        | `ctx: Context \| None`                   | Check each union member               |
| Annotated Type    | `ctx: Annotated[Context, "description"]` | Extract base type from first argument |
| Forward Reference | `ctx: "Context"`                         | Resolve via `get_type_hints()`        |

**Sources:** [src/fastmcp/utilities/types.py120-128](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L120-L128) [src/fastmcp/utilities/types.py54-117](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L54-L117)

## MCP Capabilities Access

The `Context` object provides access to core MCP protocol capabilities through a clean interface:

### Logging and Progress

```
```

**Sources:** [src/fastmcp/server/context.py57-67](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L57-L67) [src/fastmcp/server/context.py210-234](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L210-L234) [src/fastmcp/server/context.py170-195](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L170-L195)

### AI Sampling and Elicitation

```
```

**Sources:** [src/fastmcp/server/context.py361-442](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L361-L442) [src/fastmcp/server/context.py444-567](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L444-L567)

### Session and Resource Management

```
```

**Sources:** [src/fastmcp/server/context.py250-292](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L250-L292) [src/fastmcp/server/context.py197-208](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L197-L208) [src/fastmcp/server/context.py344-347](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L344-L347)

## State Management

The Context system provides request-scoped state management with inheritance semantics:

```
```

**Sources:** [src/fastmcp/server/context.py113-117](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L113-L117) [src/fastmcp/server/context.py140-144](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/context.py#L140-L144) [tests/server/test\_context.py134-180](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_context.py#L134-L180)

## Type System Integration

FastMCP's type system supports the Context dependency injection through several utility functions:

### Type Adapter Caching

```
```

**Sources:** [src/fastmcp/utilities/types.py44-117](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L44-L117) [tests/utilities/test\_types.py624-695](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/test_types.py#L624-L695)

### Helper Type Classes

FastMCP provides helper classes for common content types that integrate with the Context system:

| Class   | Purpose                | Key Methods                                  |
| ------- | ---------------------- | -------------------------------------------- |
| `Image` | Image content handling | `to_image_content()` → `ImageContent`        |
| `Audio` | Audio content handling | `to_audio_content()` → `AudioContent`        |
| `File`  | File resource handling | `to_resource_content()` → `EmbeddedResource` |

**Sources:** [src/fastmcp/utilities/types.py178-379](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L178-L379) [examples/get\_file.py4](https://github.com/jlowin/fastmcp/blob/66221ed3/examples/get_file.py#L4-L4) [examples/get\_file.py15](https://github.com/jlowin/fastmcp/blob/66221ed3/examples/get_file.py#L15-L15) [examples/get\_file.py27](https://github.com/jlowin/fastmcp/blob/66221ed3/examples/get_file.py#L27-L27)

### Type Replacement System

```
```

**Sources:** [src/fastmcp/utilities/types.py381-415](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#L381-L415) [tests/utilities/test\_types.py598-622](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/test_types.py#L598-L622)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Context System and Dependencies](#context-system-and-dependencies.md)
- [Context Object Architecture](#context-object-architecture.md)
- [Context Lifecycle Management](#context-lifecycle-management.md)
- [Dependency Injection System](#dependency-injection-system.md)
- [Type Annotation Processing](#type-annotation-processing.md)
- [MCP Capabilities Access](#mcp-capabilities-access.md)
- [Logging and Progress](#logging-and-progress.md)
- [AI Sampling and Elicitation](#ai-sampling-and-elicitation.md)
- [Session and Resource Management](#session-and-resource-management.md)
- [State Management](#state-management.md)
- [Type System Integration](#type-system-integration.md)
- [Type Adapter Caching](#type-adapter-caching.md)
- [Helper Type Classes](#helper-type-classes.md)
- [Type Replacement System](#type-replacement-system.md)
