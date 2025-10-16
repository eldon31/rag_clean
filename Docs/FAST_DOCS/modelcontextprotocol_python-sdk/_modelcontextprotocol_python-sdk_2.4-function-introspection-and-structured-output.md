Function Introspection & Structured Output | modelcontextprotocol/python-sdk | DeepWiki

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

# Function Introspection & Structured Output

Relevant source files

- [examples/snippets/servers/direct\_execution.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/direct_execution.py)
- [examples/snippets/servers/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/structured_output.py)
- [src/mcp/server/fastmcp/\_\_init\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/__init__.py)
- [src/mcp/server/fastmcp/utilities/func\_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py)
- [src/mcp/server/fastmcp/utilities/types.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/types.py)
- [tests/server/fastmcp/test\_func\_metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_func_metadata.py)
- [tests/server/fastmcp/test\_integration.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_integration.py)

This document explains how FastMCP automatically analyzes Python functions to generate JSON schemas for their arguments and return values, enabling automatic validation and structured output generation. This system allows FastMCP to seamlessly bridge between Python function signatures and the MCP protocol's JSON-based communication.

For information about how tools are registered and managed, see [Tool Management](modelcontextprotocol/python-sdk/2.2-tool-management.md). For details about the FastMCP server architecture, see [FastMCP Server Architecture](modelcontextprotocol/python-sdk/2.1-fastmcp-server-architecture.md).

## Purpose and Scope

The function introspection system serves two primary purposes:

1. **Automatic Schema Generation**: Converts Python function signatures into JSON schemas that can be used by MCP clients to understand tool parameters
2. **Structured Output Support**: Enables tools to return structured data with schemas, allowing for richer client interactions

The system is built around the `func_metadata` function and `FuncMetadata` class, which analyze function signatures using Python's `inspect` module and Pydantic models to create validation and conversion pipelines.

## Function Introspection Architecture

The introspection system follows a pipeline from Python functions to validated execution:

```
```

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py166-284](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L166-L284) [src/mcp/server/fastmcp/utilities/func\_metadata.py62-164](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L62-L164)

## Argument Model Generation

The `func_metadata` function creates Pydantic models from function signatures to enable automatic validation:

### Core Process

```
```

### Parameter Handling Rules

| Parameter Type                    | Treatment                            | Example                           |
| --------------------------------- | ------------------------------------ | --------------------------------- |
| Typed parameters                  | Direct mapping                       | `name: str` → `str` field         |
| Untyped parameters                | Mapped to `Any` with string schema   | `value` → `Any` field             |
| Parameters with `None` annotation | Mapped to null type                  | `x: None` → null field            |
| Parameters starting with `_`      | Rejected (raises `InvalidSignature`) | `_private: str` → Error           |
| Parameters in `skip_names`        | Excluded from model                  | Skipped entirely                  |
| BaseModel attribute conflicts     | Uses aliases                         | `model_dump: str` → aliased field |

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py208-258](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L208-L258) [src/mcp/server/fastmcp/utilities/func\_metadata.py240-252](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L240-L252)

## Structured Output System

FastMCP supports structured output based on function return type annotations. The system automatically detects whether a function should return structured or unstructured output:

### Return Type Handling

```
```

### Structured Output Examples

| Return Type       | Model Strategy                | Schema Generation                |
| ----------------- | ----------------------------- | -------------------------------- |
| `str`             | Wrapped as `{"result": str}`  | Simple object schema             |
| `BaseModel`       | Used directly                 | Full model schema                |
| `dict[str, int]`  | RootModel for dict            | Object with additionalProperties |
| `dict[int, str]`  | Wrapped as `{"result": dict}` | Wrapped object schema            |
| `TypedDict`       | Converted to BaseModel        | Object with typed properties     |
| `list[str]`       | Wrapped as `{"result": list}` | Array in wrapped object          |
| Annotated class   | Converted to BaseModel        | Object with class fields         |
| Unannotated class | No structured output          | Returns None                     |

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py287-371](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L287-L371) [examples/snippets/servers/structured\_output.py1-98](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/snippets/servers/structured_output.py#L1-L98)

## JSON Schema Generation

The system generates JSON schemas using Pydantic's schema generation with strict validation:

### Schema Generation Pipeline

```
```

The `StrictJsonSchema` class raises exceptions instead of emitting warnings, allowing the system to detect non-serializable types and gracefully fall back to unstructured output.

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py30-38](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L30-L38) [src/mcp/server/fastmcp/utilities/func\_metadata.py355-371](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L355-L371)

## Input Validation & Pre-parsing

The validation system includes sophisticated JSON pre-parsing to handle common client behavior:

### Pre-parsing Logic

```
```

### Pre-parsing Examples

| Input          | Field Type  | Pre-parsed Result | Reason                      |
| -------------- | ----------- | ----------------- | --------------------------- |
| `'["a", "b"]'` | `list[str]` | `["a", "b"]`      | JSON array parsed           |
| `'"hello"'`    | `str`       | `'"hello"'`       | JSON string kept as string  |
| `'{"x": 1}'`   | `SomeModel` | `{"x": 1}`        | JSON object parsed          |
| `'123'`        | `int`       | `'123'`           | Simple value kept as string |
| `'invalid'`    | `list[str]` | `'invalid'`       | Invalid JSON kept as string |

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py121-159](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L121-L159) [tests/server/fastmcp/test\_func\_metadata.py463-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_func_metadata.py#L463-L552)

## Output Conversion

The `convert_result` method handles converting function return values to the appropriate format for MCP responses:

### Conversion Flow

```
```

### Content Conversion Rules

| Return Value Type | Conversion Result                  |
| ----------------- | ---------------------------------- |
| `None`            | Empty list `[]`                    |
| `ContentBlock`    | Single-item list `[ContentBlock]`  |
| `Image`           | `[ImageContent]`                   |
| `Audio`           | `[AudioContent]`                   |
| `list/tuple`      | Flattened list of converted items  |
| Other types       | JSON-serialized as `[TextContent]` |

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py91-119](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L91-L119) [src/mcp/server/fastmcp/utilities/func\_metadata.py489-523](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L489-L523)

## Integration with FastMCP

The function introspection system integrates seamlessly with FastMCP's tool registration:

```
```

This system enables FastMCP to provide rich, type-safe tool interfaces while maintaining compatibility with the MCP protocol's JSON-based communication model.

Sources: [src/mcp/server/fastmcp/utilities/func\_metadata.py68-89](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/func_metadata.py#L68-L89) [tests/server/fastmcp/test\_integration.py666-700](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/fastmcp/test_integration.py#L666-L700)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Function Introspection & Structured Output](#function-introspection-structured-output.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Function Introspection Architecture](#function-introspection-architecture.md)
- [Argument Model Generation](#argument-model-generation.md)
- [Core Process](#core-process.md)
- [Parameter Handling Rules](#parameter-handling-rules.md)
- [Structured Output System](#structured-output-system.md)
- [Return Type Handling](#return-type-handling.md)
- [Structured Output Examples](#structured-output-examples.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [Schema Generation Pipeline](#schema-generation-pipeline.md)
- [Input Validation & Pre-parsing](#input-validation-pre-parsing.md)
- [Pre-parsing Logic](#pre-parsing-logic.md)
- [Pre-parsing Examples](#pre-parsing-examples.md)
- [Output Conversion](#output-conversion.md)
- [Conversion Flow](#conversion-flow.md)
- [Content Conversion Rules](#content-conversion-rules.md)
- [Integration with FastMCP](#integration-with-fastmcp.md)
