Component System Architecture | jlowin/fastmcp | DeepWiki

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

# Component System Architecture

Relevant source files

- [docs/patterns/tool-transformation.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/patterns/tool-transformation.mdx)
- [src/fastmcp/prompts/prompt.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt.py)
- [src/fastmcp/prompts/prompt\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt_manager.py)
- [src/fastmcp/resources/resource.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource.py)
- [src/fastmcp/resources/resource\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource_manager.py)
- [src/fastmcp/resources/template.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/template.py)
- [src/fastmcp/resources/types.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/types.py)
- [src/fastmcp/tools/tool.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool.py)
- [src/fastmcp/tools/tool\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py)
- [src/fastmcp/tools/tool\_transform.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_transform.py)
- [src/fastmcp/utilities/components.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/components.py)
- [tests/prompts/test\_prompt.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/prompts/test_prompt.py)
- [tests/prompts/test\_prompt\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/prompts/test_prompt_manager.py)
- [tests/resources/test\_function\_resources.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/resources/test_function_resources.py)
- [tests/resources/test\_resource\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/resources/test_resource_manager.py)
- [tests/resources/test\_resource\_template.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/resources/test_resource_template.py)
- [tests/resources/test\_resources.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/resources/test_resources.py)
- [tests/server/test\_server\_interactions.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/test_server_interactions.py)
- [tests/tools/test\_tool.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/tools/test_tool.py)
- [tests/tools/test\_tool\_manager.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/tools/test_tool_manager.py)
- [tests/tools/test\_tool\_transform.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/tools/test_tool_transform.py)

This document covers the FastMCP component system, which provides a unified framework for managing Tools, Resources, Prompts, and Resource Templates. It explains how these components are created, registered, managed, and composed within FastMCP servers.

For information about server composition and mounting mechanisms, see [Server Composition and Proxying](jlowin/fastmcp/2.3-server-composition-and-proxying.md). For details about dependency injection and the Context system, see [Context System and Dependencies](jlowin/fastmcp/2.2-context-system-and-dependencies.md).

## Component Type Hierarchy

FastMCP organizes all server capabilities into four main component types, each sharing common functionality through a base class architecture.

### Component Class Structure

```
```

**Sources**: [src/fastmcp/utilities/components.py28-125](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/components.py#L28-L125) [src/fastmcp/tools/tool.py105-240](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool.py#L105-L240) [src/fastmcp/resources/resource.py34-219](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource.py#L34-L219) [src/fastmcp/resources/template.py53-314](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/template.py#L53-L314) [src/fastmcp/prompts/prompt.py65-262](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt.py#L65-L262)

### Base Component Properties

All FastMCP components inherit from `FastMCPComponent` and share these properties:

| Property      | Type                     | Purpose                                                |
| ------------- | ------------------------ | ------------------------------------------------------ |
| `name`        | `str`                    | Unique identifier for the component                    |
| `title`       | `str \| None`            | Display title for UI purposes                          |
| `description` | `str \| None`            | Human-readable description                             |
| `tags`        | `set[str]`               | Categorization tags for filtering                      |
| `meta`        | `dict[str, Any] \| None` | Additional metadata                                    |
| `enabled`     | `bool`                   | Whether component is active                            |
| `key`         | `str`                    | Internal bookkeeping identifier (may include prefixes) |

**Sources**: [src/fastmcp/utilities/components.py28-69](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/components.py#L28-L69)

## Component Manager Architecture

Each component type has a dedicated manager class that handles registration, retrieval, and execution. The managers follow a consistent pattern and support server composition through mounting.

### Manager System Overview

```
```

**Sources**: [src/fastmcp/tools/tool\_manager.py25-255](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py#L25-L255) [src/fastmcp/resources/resource\_manager.py28-344](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource_manager.py#L28-L344) [src/fastmcp/prompts/prompt\_manager.py21-204](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt_manager.py#L21-L204)

### Manager Responsibilities

Each manager provides these core operations:

| Operation           | Tool Manager           | Resource Manager               | Prompt Manager              |
| ------------------- | ---------------------- | ------------------------------ | --------------------------- |
| **Add Component**   | `add_tool(tool)`       | `add_resource(resource)`       | `add_prompt(prompt)`        |
| **Get Component**   | `get_tool(key)`        | `read_resource(uri)`           | `get_prompt(key)`           |
| **List Components** | `list_tools()`         | `list_resources()`             | `list_prompts()`            |
| **Execute/Use**     | `call_tool(key, args)` | Templates: `create_resource()` | `render_prompt(name, args)` |

**Sources**: [src/fastmcp/tools/tool\_manager.py108-254](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py#L108-L254) [src/fastmcp/resources/resource\_manager.py275-344](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource_manager.py#L275-L344) [src/fastmcp/prompts/prompt\_manager.py91-204](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt_manager.py#L91-L204)

## Component Creation from Functions

FastMCP provides a consistent pattern for creating components from Python functions using static factory methods.

### Function-to-Component Creation Flow

```
```

**Sources**: [src/fastmcp/tools/tool.py354-491](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool.py#L354-L491) [src/fastmcp/resources/resource.py168-219](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource.py#L168-L219) [src/fastmcp/prompts/prompt.py156-262](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt.py#L156-L262) [src/fastmcp/resources/template.py214-313](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/template.py#L214-L313)

### Context Injection

All function-based components support automatic Context injection for accessing server capabilities:

```
```

The parameter detection uses `find_kwarg_by_type()` to identify Context parameters and excludes them from the component's public schema.

**Sources**: [src/fastmcp/utilities/types.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/types.py#LNaN-LNaN) [src/fastmcp/tools/tool.py407-412](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool.py#L407-L412) [src/fastmcp/resources/template.py245-246](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/template.py#L245-L246)

## Tool Transformation System

Tools can be transformed to create modified versions with different schemas, argument mappings, or custom behavior. This enables adaptation without code duplication.

### Tool Transformation Architecture

```
```

**Sources**: [src/fastmcp/tools/tool\_transform.py232-517](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_transform.py#L232-L517) [src/fastmcp/tools/tool\_transform.py37-91](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_transform.py#L37-L91) [src/fastmcp/tools/tool\_transform.py93-207](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_transform.py#L93-L207)

### Argument Transformation Options

The `ArgTransform` class provides fine-grained control over individual arguments:

| Transform Type      | Purpose                   | Example                               |
| ------------------- | ------------------------- | ------------------------------------- |
| **Rename**          | Change argument name      | `name="new_name"`                     |
| **Hide**            | Remove from public schema | `hide=True, default="constant"`       |
| **Default Value**   | Add/change default        | `default=42`                          |
| **Default Factory** | Dynamic defaults          | `default_factory=lambda: time.time()` |
| **Type Change**     | Modify expected type      | `type=str`                            |
| **Make Required**   | Remove default value      | `required=True`                       |

**Sources**: [src/fastmcp/tools/tool\_transform.py93-207](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_transform.py#L93-L207)

## Server Composition and Component Mounting

Managers support mounting other servers to create hierarchical component structures. This enables composition of multiple FastMCP servers into larger systems.

### Component Loading Paths

```
```

**Sources**: [src/fastmcp/tools/tool\_manager.py55-101](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool_manager.py#L55-L101) [src/fastmcp/resources/resource\_manager.py72-190](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource_manager.py#L72-L190) [src/fastmcp/prompts/prompt\_manager.py49-89](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt_manager.py#L49-L89)

## Component Lifecycle Management

Components support enable/disable operations and automatic notifications to trigger list change events in the MCP protocol.

### Component State Management

Each component can be enabled or disabled, and state changes automatically notify the Context system:

```
```

This ensures that MCP clients receive updated component lists when components are dynamically enabled or disabled.

**Sources**: [src/fastmcp/tools/tool.py123-137](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/tools/tool.py#L123-L137) [src/fastmcp/resources/resource.py53-67](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/resource.py#L53-L67) [src/fastmcp/prompts/prompt.py72-86](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/prompts/prompt.py#L72-L86) [src/fastmcp/resources/template.py72-86](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/resources/template.py#L72-L86)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Component System Architecture](#component-system-architecture.md)
- [Component Type Hierarchy](#component-type-hierarchy.md)
- [Component Class Structure](#component-class-structure.md)
- [Base Component Properties](#base-component-properties.md)
- [Component Manager Architecture](#component-manager-architecture.md)
- [Manager System Overview](#manager-system-overview.md)
- [Manager Responsibilities](#manager-responsibilities.md)
- [Component Creation from Functions](#component-creation-from-functions.md)
- [Function-to-Component Creation Flow](#function-to-component-creation-flow.md)
- [Context Injection](#context-injection.md)
- [Tool Transformation System](#tool-transformation-system.md)
- [Tool Transformation Architecture](#tool-transformation-architecture.md)
- [Argument Transformation Options](#argument-transformation-options.md)
- [Server Composition and Component Mounting](#server-composition-and-component-mounting.md)
- [Component Loading Paths](#component-loading-paths.md)
- [Component Lifecycle Management](#component-lifecycle-management.md)
- [Component State Management](#component-state-management.md)
