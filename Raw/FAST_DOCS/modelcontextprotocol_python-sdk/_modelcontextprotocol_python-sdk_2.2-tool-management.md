Tool Management | modelcontextprotocol/python-sdk | DeepWiki

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

# Tool Management

Relevant source files

- [src/mcp/server/fastmcp/\_\_init\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/__init__.py)
- [src/mcp/server/fastmcp/tools/base.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py)
- [src/mcp/server/fastmcp/tools/tool\_manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py)
- [src/mcp/server/fastmcp/utilities/func\_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py)
- [src/mcp/server/fastmcp/utilities/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/types.py)
- [tests/server/fastmcp/test\_func\_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_func_metadata.py)
- [tests/server/fastmcp/test\_tool\_manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_tool_manager.py)

FastMCP's tool management system enables developers to register Python functions as MCP tools using the `@tool` decorator and execute them through the `ToolManager`. The system automatically handles argument validation, context injection, and structured output generation.

The tool management system consists of three main components: the `ToolManager` for centralized tool registration and execution, the `Tool` class for wrapping functions with metadata, and the `FuncMetadata` system for function introspection and validation.

## Tool Registration with @tool Decorator

Tools are registered using the `@tool` decorator, which automatically converts Python functions into MCP tools. The decorator analyzes function signatures, creates validation schemas, and registers the tool with the `ToolManager`.

### Tool Registration Flow

```
```

Sources: [src/mcp/server/fastmcp/tools/tool\_manager.py45-71](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L45-L71) [src/mcp/server/fastmcp/tools/base.py42-84](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L42-L84)

### Function Metadata Extraction

The `func_metadata()` function performs deep introspection of Python functions to extract type information and create validation models.

```
```

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py166-207](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L166-L207)

The `func_metadata()` function performs deep introspection of Python functions to create a `FuncMetadata` object containing:

- **arg\_model**: A Pydantic model representing function arguments with validation
- **output\_schema**: JSON schema for structured output (if enabled)
- **output\_model**: Pydantic model for return type validation
- **wrap\_output**: Whether to wrap primitive returns in `{"result": value}`

### Argument Processing Pipeline

The `FuncMetadata.call_fn_with_arg_validation()` method processes raw arguments through validation and type conversion before function execution.

```
```

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py68-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L68-L89) [src/mcp/server/fastmcp/utilities/func\_metadata.py121-159](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L121-L159) [src/mcp/server/fastmcp/utilities/func\_metadata.py44-55](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L44-L55)

**Argument Processing Features:**

| Stage            | Implementation               | Purpose                              | Example                                  |
| ---------------- | ---------------------------- | ------------------------------------ | ---------------------------------------- |
| JSON Pre-parsing | `pre_parse_json()`           | Parse JSON strings to Python objects | `"[1,2,3]"` → `[1,2,3]`                  |
| Type Validation  | `arg_model.model_validate()` | Validate against Pydantic model      | `str` parameter rejects `int`            |
| Alias Resolution | `model_dump_one_level()`     | Map aliases to parameter names       | Field aliases → function parameter names |
| Default Handling | Pydantic `Field()`           | Apply default values                 | Optional parameters get defaults         |
| Complex Types    | Nested model support         | Handle complex structures            | `BaseModel`, `TypedDict`, dataclasses    |

**JSON Pre-parsing Logic:**

The `pre_parse_json()` method handles cases where MCP clients send complex data as JSON strings instead of native types:

```
```

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py121-159](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L121-L159)

## Tool Registration System

Tools are registered through the `Tool` class and the `@mcp.tool` decorator, which provides a high-level interface for function-to-tool conversion.

### Tool Class Structure

The `Tool` class encapsulates all information needed to execute a function as an MCP tool, including metadata, validation models, and execution logic.

```
```

Sources: [src/mcp/server/fastmcp/tools/tool\_manager.py19-35](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L19-L35) [src/mcp/server/fastmcp/tools/base.py22-39](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L22-L39) [src/mcp/server/fastmcp/utilities/func\_metadata.py62-66](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L62-L66)

### Tool Creation Process

The `Tool.from_function()` method creates a `Tool` instance from a Python function by extracting metadata and creating validation schemas.

```
```

Sources: [src/mcp/server/fastmcp/tools/base.py42-84](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L42-L84)

### Context Parameter Detection and Injection

The system automatically detects `Context` parameters in function signatures and excludes them from the tool schema while injecting them during execution.

**Context Detection in find\_context\_parameter():**

```
```

**Context Injection During Execution:**

```
```

The context parameter is excluded from the `func_metadata()` call via the `skip_names` parameter and injected separately during execution.

Sources: [src/mcp/server/fastmcp/tools/base.py63-69](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L63-L69) [src/mcp/server/fastmcp/tools/base.py94-99](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L94-L99) [src/mcp/server/fastmcp/utilities/context\_injection.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/context_injection.py)

## Tool Execution System

Tool execution involves argument validation, context injection, and result conversion.

### Tool Execution Pipeline

```
```

Sources: [src/mcp/server/fastmcp/tools/tool\_manager.py73-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L73-L85) [src/mcp/server/fastmcp/tools/base.py86-106](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L86-L106) [src/mcp/server/fastmcp/utilities/func\_metadata.py68-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L68-L89)

### Error Handling

Tool execution wraps exceptions in `ToolError` for consistent error reporting:

```
```

Sources: [src/mcp/server/fastmcp/tools/base.py97-110](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L97-L110)

## ToolManager - Centralized Tool Management

The `ToolManager` class provides centralized registration, retrieval, and execution of tools. It maintains a registry of `Tool` instances and handles tool lifecycle management.

### ToolManager Architecture

```
```

Sources: [src/mcp/server/fastmcp/tools/tool\_manager.py19-35](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L19-L35) [src/mcp/server/fastmcp/tools/tool\_manager.py45-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L45-L85)

### ToolManager API

| Method         | Purpose                     | Parameters                                                                        | Return Type    |
| -------------- | --------------------------- | --------------------------------------------------------------------------------- | -------------- |
| `add_tool()`   | Register function as tool   | `fn`, `name`, `title`, `description`, `annotations`, `icons`, `structured_output` | `Tool`         |
| `get_tool()`   | Retrieve tool by name       | `name: str`                                                                       | `Tool \| None` |
| `list_tools()` | Get all registered tools    | None                                                                              | `list[Tool]`   |
| `call_tool()`  | Execute tool with arguments | `name`, `arguments`, `context`, `convert_result`                                  | `Any`          |

Sources: [src/mcp/server/fastmcp/tools/tool\_manager.py37-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L37-L85)

### Tool Registration Workflow

```
```

Sources: [src/mcp/server/fastmcp/tools/tool\_manager.py45-71](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/tool_manager.py#L45-L71) [src/mcp/server/fastmcp/tools/base.py42-84](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L42-L84)

## Structured Output Support

Tools can return structured output with automatic schema generation and validation.

### Structured Output Types

```
```

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py287-371](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L287-L371) [src/mcp/server/fastmcp/utilities/func\_metadata.py425-449](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L425-L449)

### Output Conversion Process

The `convert_result()` method handles both unstructured and structured output:

**Dual Output Generation:**

```
```

**Content Conversion Logic:**

- **Unstructured**: Converts results to `ContentBlock` sequences (text, image, audio)
- **Structured**: Validates against output schema and serializes to JSON-compatible dict
- **Return**: Tuple of both formats for backwards compatibility

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py91-119](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L91-L119) [src/mcp/server/fastmcp/utilities/func\_metadata.py489-524](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L489-L524)

## Advanced Features

### Reserved Parameter Names

The system handles conflicts with Pydantic `BaseModel` methods by using aliases:

```
```

**Alias Resolution Process:**

```
```

This prevents Pydantic warnings about shadowing parent attributes while maintaining the original parameter names in the external API.

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py240-252](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L240-L252)

### Async Function Support

Both sync and async functions are supported with automatic detection:

```
```

Sources: [src/mcp/server/fastmcp/tools/base.py113-119](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L113-L119)

### Tool Annotations

Tools support optional metadata through `ToolAnnotations`:

- `title`: Human-readable title
- `readOnlyHint`: Indicates read-only operations
- `openWorldHint`: Indicates open-world assumptions

Sources: [src/mcp/server/fastmcp/tools/base.py34](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/tools/base.py#L34-L34)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Tool Management](#tool-management.md)
- [Tool Registration with @tool Decorator](#tool-registration-with-tool-decorator.md)
- [Tool Registration Flow](#tool-registration-flow.md)
- [Function Metadata Extraction](#function-metadata-extraction.md)
- [Argument Processing Pipeline](#argument-processing-pipeline.md)
- [Tool Registration System](#tool-registration-system.md)
- [Tool Class Structure](#tool-class-structure.md)
- [Tool Creation Process](#tool-creation-process.md)
- [Context Parameter Detection and Injection](#context-parameter-detection-and-injection.md)
- [Tool Execution System](#tool-execution-system.md)
- [Tool Execution Pipeline](#tool-execution-pipeline.md)
- [Error Handling](#error-handling.md)
- [ToolManager - Centralized Tool Management](#toolmanager---centralized-tool-management.md)
- [ToolManager Architecture](#toolmanager-architecture.md)
- [ToolManager API](#toolmanager-api.md)
- [Tool Registration Workflow](#tool-registration-workflow.md)
- [Structured Output Support](#structured-output-support.md)
- [Structured Output Types](#structured-output-types.md)
- [Output Conversion Process](#output-conversion-process.md)
- [Advanced Features](#advanced-features.md)
- [Reserved Parameter Names](#reserved-parameter-names.md)
- [Async Function Support](#async-function-support.md)
- [Tool Annotations](#tool-annotations.md)
