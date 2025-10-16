OpenAPI Integration | jlowin/fastmcp | DeepWiki

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

# OpenAPI Integration

Relevant source files

- [src/fastmcp/server/openapi.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py)
- [src/fastmcp/utilities/openapi.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py)
- [tests/server/openapi/test\_optional\_parameters.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/openapi/test_optional_parameters.py)
- [tests/utilities/openapi/test\_openapi.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/openapi/test_openapi.py)
- [tests/utilities/openapi/test\_openapi\_advanced.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/openapi/test_openapi_advanced.py)
- [tests/utilities/openapi/test\_openapi\_fastapi.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/openapi/test_openapi_fastapi.py)

FastMCP's OpenAPI integration enables automatic generation of FastMCP servers from OpenAPI specifications, converting HTTP API definitions into MCP Tools, Resources, and ResourceTemplates. This system parses OpenAPI schemas and creates appropriate MCP components based on configurable route mapping rules.

For general FastMCP server functionality, see [FastMCP Server Core](jlowin/fastmcp/2-fastmcp-server-core.md). For HTTP server deployment, see [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md). For client-side API consumption, see [FastMCP Client System](jlowin/fastmcp/3-fastmcp-client-system.md).

## Architecture Overview

The OpenAPI integration consists of three main layers: schema parsing, route mapping, and component generation. The system transforms OpenAPI specifications into FastMCP components through an intermediate representation.

```
```

**Sources:** [src/fastmcp/server/openapi.py1-100](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L1-L100) [src/fastmcp/utilities/openapi.py200-250](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L200-L250)

## Core Components

### FastMCPOpenAPI Server Class

The `FastMCPOpenAPI` class extends `FastMCP` to provide OpenAPI-based server creation. It parses OpenAPI specifications and automatically generates appropriate MCP components.

```
```

**Sources:** [src/fastmcp/server/openapi.py696-831](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L696-L831) [src/fastmcp/server/openapi.py833-887](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L833-L887)

### OpenAPI Component Types

Three specialized component classes handle different types of HTTP endpoints:

| Component                 | Purpose               | HTTP Methods             | Use Case                       |
| ------------------------- | --------------------- | ------------------------ | ------------------------------ |
| `OpenAPITool`             | Executable operations | POST, PUT, PATCH, DELETE | API actions, data modification |
| `OpenAPIResource`         | Static data endpoints | GET (no path params)     | Fixed data retrieval           |
| `OpenAPIResourceTemplate` | Parameterized data    | GET (with path params)   | Dynamic data retrieval         |

**Sources:** [src/fastmcp/server/openapi.py229-521](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L229-L521) [src/fastmcp/server/openapi.py523-640](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L523-L640) [src/fastmcp/server/openapi.py642-694](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L642-L694)

## Route Mapping System

### MCPType Enumeration

The `MCPType` enum defines the target component types for HTTP routes:

```
```

**Sources:** [src/fastmcp/server/openapi.py78-94](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L78-L94)

### RouteMap Configuration

`RouteMap` objects define mapping rules from HTTP routes to MCP component types:

```
```

**Sources:** [src/fastmcp/server/openapi.py110-182](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L110-L182) [src/fastmcp/server/openapi.py184-227](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L184-L227)

### Default Route Mapping

By default, all routes are converted to Tools unless custom mappings specify otherwise:

```
```

**Sources:** [src/fastmcp/server/openapi.py177-181](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L177-L181)

## Schema Parsing System

### HTTPRoute Intermediate Representation

The parsing system converts OpenAPI specifications into `HTTPRoute` objects that capture all necessary information for component generation:

```
```

**Sources:** [src/fastmcp/utilities/openapi.py201-253](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L201-L253) [src/fastmcp/utilities/openapi.py379-477](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L379-L477) [src/fastmcp/utilities/openapi.py479-543](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L479-L543)

### Parameter Processing

The system handles complex parameter scenarios including location conflicts and array formatting:

| Parameter Location | Handling                   | Example              |
| ------------------ | -------------------------- | -------------------- |
| `path`             | Required, URL substitution | `/users/{userId}`    |
| `query`            | Optional, query string     | `?limit=10&offset=0` |
| `header`           | Optional, HTTP headers     | `X-API-Key: secret`  |
| `cookie`           | Optional, cookie values    | `session=abc123`     |

**Sources:** [src/fastmcp/utilities/openapi.py124-135](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L124-L135) [src/fastmcp/server/openapi.py264-418](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L264-L418)

## Component Creation Process

### Schema Combination

The `_combine_schemas` function merges parameter schemas with request body schemas, handling name collisions by suffixing parameter names with their location:

```
```

**Sources:** [src/fastmcp/utilities/openapi.py892-1050](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L892-L1050)

### Name Generation and Collision Handling

The system generates unique component names using operation IDs, summaries, or path-based naming with collision detection:

```
```

**Sources:** [src/fastmcp/server/openapi.py833-856](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L833-L856) [src/fastmcp/server/openapi.py858-886](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L858-L886) [src/fastmcp/server/openapi.py44-64](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L44-L64)

## HTTP Request Execution

### Parameter Serialization

OpenAPI components handle complex parameter serialization including arrays, objects, and style-specific formatting:

```
```

**Sources:** [src/fastmcp/server/openapi.py288-417](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L288-L417) [src/fastmcp/utilities/openapi.py41-121](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L41-L121)

### Response Processing

The system handles various response types and content negotiation:

| Content Type       | Processing                      | Output                               |
| ------------------ | ------------------------------- | ------------------------------------ |
| `application/json` | JSON parsing, structured output | `ToolResult(structured_content=...)` |
| `text/*`           | Text content                    | `ToolResult(content=...)`            |
| `application/xml`  | Text content                    | `ToolResult(content=...)`            |
| Binary             | Raw bytes                       | `ToolResult(content=...)`            |

**Sources:** [src/fastmcp/server/openapi.py482-502](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L482-L502) [src/fastmcp/server/openapi.py614-621](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L614-L621)

## Advanced Features

### Custom Route Mapping Functions

Advanced route mapping through `route_map_fn` and `mcp_component_fn` callbacks:

```
```

**Sources:** [src/fastmcp/server/openapi.py798-812](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L798-L812) [src/fastmcp/server/openapi.py930-939](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L930-L939)

### Output Schema Generation

The system extracts output schemas from OpenAPI response definitions for structured tool results:

```
```

**Sources:** [src/fastmcp/utilities/openapi.py1098-1200](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/openapi.py#L1098-L1200)

### Error Handling

Comprehensive error handling for HTTP requests, parameter validation, and schema resolution:

- **Parameter Validation**: Missing required path parameters raise `ToolError`
- **HTTP Errors**: 4xx/5xx responses converted to `ValueError` with detailed messages
- **Schema Resolution**: External references raise clear error messages
- **Connection Errors**: Network issues converted to `ValueError`

**Sources:** [src/fastmcp/server/openapi.py504-520](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L504-L520) [src/fastmcp/server/openapi.py623-639](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/openapi.py#L623-L639) [tests/utilities/openapi/test\_openapi\_advanced.py655-665](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/openapi/test_openapi_advanced.py#L655-L665)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [OpenAPI Integration](#openapi-integration.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Components](#core-components.md)
- [FastMCPOpenAPI Server Class](#fastmcpopenapi-server-class.md)
- [OpenAPI Component Types](#openapi-component-types.md)
- [Route Mapping System](#route-mapping-system.md)
- [MCPType Enumeration](#mcptype-enumeration.md)
- [RouteMap Configuration](#routemap-configuration.md)
- [Default Route Mapping](#default-route-mapping.md)
- [Schema Parsing System](#schema-parsing-system.md)
- [HTTPRoute Intermediate Representation](#httproute-intermediate-representation.md)
- [Parameter Processing](#parameter-processing.md)
- [Component Creation Process](#component-creation-process.md)
- [Schema Combination](#schema-combination.md)
- [Name Generation and Collision Handling](#name-generation-and-collision-handling.md)
- [HTTP Request Execution](#http-request-execution.md)
- [Parameter Serialization](#parameter-serialization.md)
- [Response Processing](#response-processing.md)
- [Advanced Features](#advanced-features.md)
- [Custom Route Mapping Functions](#custom-route-mapping-functions.md)
- [Output Schema Generation](#output-schema-generation.md)
- [Error Handling](#error-handling.md)
