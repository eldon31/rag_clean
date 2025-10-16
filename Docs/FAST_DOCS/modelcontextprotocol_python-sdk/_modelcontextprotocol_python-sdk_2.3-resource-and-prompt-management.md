Resource & Prompt Management | modelcontextprotocol/python-sdk | DeepWiki

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

# Resource & Prompt Management

Relevant source files

- [.gitattribute](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.gitattribute)
- [.gitignore](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.gitignore)
- [src/mcp/server/auth/handlers/authorize.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/authorize.py)
- [src/mcp/server/fastmcp/prompts/base.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/base.py)
- [src/mcp/server/fastmcp/prompts/manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/manager.py)
- [src/mcp/server/fastmcp/resources/base.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/base.py)
- [src/mcp/server/fastmcp/resources/resource\_manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/resource_manager.py)
- [src/mcp/server/fastmcp/resources/templates.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/templates.py)
- [src/mcp/server/fastmcp/resources/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/types.py)
- [src/mcp/server/fastmcp/utilities/context\_injection.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/context_injection.py)

The resource and prompt management system in FastMCP provides structured access to data sources and conversation templates for MCP servers. Resources represent data that can be read (files, HTTP endpoints, databases), while prompts are message templates that can be rendered with parameters for LLM interactions.

For tool execution functionality, see [Tool Management](modelcontextprotocol/python-sdk/2.2-tool-management.md). For low-level protocol handling, see [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md).

## Resource Management Architecture

The resource system provides a unified interface for accessing various data sources through the `Resource` base class and supporting infrastructure.

### Resource Class Hierarchy

```
```

**Sources:** [src/mcp/server/fastmcp/resources/base.py19-49](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/base.py#L19-L49) [src/mcp/server/fastmcp/resources/types.py20-200](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/types.py#L20-L200)

### Resource Management Flow

```
```

**Sources:** [src/mcp/server/fastmcp/resources/resource\_manager.py77-98](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/resource_manager.py#L77-L98) [src/mcp/server/fastmcp/resources/templates.py84-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/templates.py#L84-L110)

## Resource Types and Implementation

### Static Resource Types

The system provides several concrete resource implementations for common data sources:

| Resource Type       | Purpose             | Key Methods                  | File Location                                                                                          |
| ------------------- | ------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| `TextResource`      | Static text content | `read() -> str`              | [types.py20-27](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/types.py#L20-L27)     |
| `BinaryResource`    | Static binary data  | `read() -> bytes`            | [types.py30-37](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/types.py#L30-L37)     |
| `FileResource`      | File system access  | `read() -> str\|bytes`       | [types.py105-145](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/types.py#L105-L145) |
| `HttpResource`      | HTTP endpoint data  | `read() -> str\|bytes`       | [types.py148-159](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/types.py#L148-L159) |
| `DirectoryResource` | Directory listings  | `list_files() -> list[Path]` | [types.py162-199](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/types.py#L162-L199) |

**Sources:** [src/mcp/server/fastmcp/resources/types.py1-200](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/types.py#L1-L200)

### Function Resources and Templates

`FunctionResource` enables lazy loading by wrapping functions that return data only when accessed:

```
```

**Sources:** [src/mcp/server/fastmcp/resources/types.py40-102](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/types.py#L40-L102) [src/mcp/server/fastmcp/resources/templates.py22-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/templates.py#L22-L110)

## Prompt Management System

The prompt system provides template-based message generation for LLM interactions with parameter validation and context injection.

### Prompt Architecture

```
```

**Sources:** [src/mcp/server/fastmcp/prompts/base.py22-184](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/base.py#L22-L184) [src/mcp/server/fastmcp/prompts/manager.py18-60](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/manager.py#L18-L60)

### Prompt Rendering Process

```
```

**Sources:** [src/mcp/server/fastmcp/prompts/base.py137-183](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/base.py#L137-L183) [src/mcp/server/fastmcp/prompts/manager.py49-60](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/manager.py#L49-L60)

## Context Injection System

Both resources and prompts support context injection for accessing request-specific information during execution.

### Context Parameter Discovery

```
```

**Sources:** [src/mcp/server/fastmcp/utilities/context\_injection.py11-46](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/context_injection.py#L11-L46)

### Integration Points

The context injection system integrates with both resource templates and prompts:

| Component                            | Context Usage                                   | Implementation                                                                                                              |
| ------------------------------------ | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `ResourceTemplate.create_resource()` | Access request context during resource creation | [templates.py92-93](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/templates.py#L92-L93)                  |
| `Prompt.render()`                    | Access session/request context during rendering | [base.py153](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/base.py#L153-L153)                            |
| `inject_context()`                   | Generic context injection utility               | [context\_injection.py49-68](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/context_injection.py#L49-L68) |

**Sources:** [src/mcp/server/fastmcp/resources/templates.py84-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/templates.py#L84-L110) [src/mcp/server/fastmcp/prompts/base.py137-183](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/base.py#L137-L183) [src/mcp/server/fastmcp/utilities/context\_injection.py49-68](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/context_injection.py#L49-L68)

## Manager Registration and Lifecycle

Both `ResourceManager` and `PromptManager` provide registration APIs for adding resources and prompts to FastMCP servers:

### Resource Registration

```
```

### Prompt Registration

The `PromptManager` maintains a simple dictionary mapping prompt names to `Prompt` instances, with optional duplicate warnings.

**Sources:** [src/mcp/server/fastmcp/resources/resource\_manager.py22-108](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/resource_manager.py#L22-L108) [src/mcp/server/fastmcp/prompts/manager.py18-60](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/manager.py#L18-L60)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Resource & Prompt Management](#resource-prompt-management.md)
- [Resource Management Architecture](#resource-management-architecture.md)
- [Resource Class Hierarchy](#resource-class-hierarchy.md)
- [Resource Management Flow](#resource-management-flow.md)
- [Resource Types and Implementation](#resource-types-and-implementation.md)
- [Static Resource Types](#static-resource-types.md)
- [Function Resources and Templates](#function-resources-and-templates.md)
- [Prompt Management System](#prompt-management-system.md)
- [Prompt Architecture](#prompt-architecture.md)
- [Prompt Rendering Process](#prompt-rendering-process.md)
- [Context Injection System](#context-injection-system.md)
- [Context Parameter Discovery](#context-parameter-discovery.md)
- [Integration Points](#integration-points.md)
- [Manager Registration and Lifecycle](#manager-registration-and-lifecycle.md)
- [Resource Registration](#resource-registration.md)
- [Prompt Registration](#prompt-registration.md)
