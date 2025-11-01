Middleware System | jlowin/fastmcp | DeepWiki

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

# Middleware System

Relevant source files

- [src/fastmcp/cli/install/gemini\_cli.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/gemini_cli.py)
- [src/fastmcp/server/middleware/error\_handling.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/error_handling.py)
- [src/fastmcp/server/middleware/logging.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/logging.py)
- [src/fastmcp/server/middleware/rate\_limiting.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/rate_limiting.py)
- [src/fastmcp/server/middleware/timing.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/timing.py)
- [src/fastmcp/utilities/logging.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/logging.py)
- [tests/server/middleware/test\_error\_handling.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_error_handling.py)
- [tests/server/middleware/test\_logging.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_logging.py)
- [tests/server/middleware/test\_timing.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_timing.py)
- [tests/utilities/test\_logging.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/test_logging.py)

The FastMCP middleware system provides a flexible framework for intercepting, monitoring, and modifying MCP message processing. This system allows developers to add cross-cutting concerns like logging, timing, error handling, and rate limiting without modifying core server logic.

This document covers the middleware architecture, built-in middleware implementations, and patterns for creating custom middleware. For authentication-specific middleware functionality, see [Authentication and Security](jlowin/fastmcp/4.1-authentication-and-security.md). For HTTP server deployment patterns, see [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md).

## Core Middleware Architecture

The middleware system is built around a pipeline pattern where each middleware can inspect, modify, or handle MCP messages before passing control to the next middleware in the chain.

### Middleware Pipeline Flow

```
```

Sources: [src/fastmcp/server/middleware/middleware.py1-200](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/middleware.py#L1-L200) [tests/server/middleware/test\_logging.py506-775](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_logging.py#L506-L775)

### Core Middleware Components

```
```

Sources: [src/fastmcp/server/middleware/middleware.py11-50](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/middleware.py#L11-L50)

The `Middleware` base class provides hook methods for different MCP operations. The `MiddlewareContext[T]` carries message data and metadata through the pipeline, while `CallNext[T, R]` represents the continuation of the middleware chain.

## Built-in Middleware Types

FastMCP includes several production-ready middleware implementations for common server needs.

### Logging Middleware

The logging system provides two complementary approaches for request monitoring and debugging.

```
```

Sources: [src/fastmcp/server/middleware/logging.py143-196](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/logging.py#L143-L196) [src/fastmcp/server/middleware/logging.py198-246](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/logging.py#L198-L246)

| Middleware                    | Logger Name          | Output Format   | Use Case                     |
| ----------------------------- | -------------------- | --------------- | ---------------------------- |
| `LoggingMiddleware`           | `fastmcp.requests`   | Key-value pairs | Development, human debugging |
| `StructuredLoggingMiddleware` | `fastmcp.structured` | JSON objects    | Production, log aggregation  |

Key features include payload serialization via `default_serializer()` using `pydantic_core.to_json()`, token estimation at approximately 4 characters per token, and configurable payload truncation via `max_payload_length`.

### Timing and Performance Middleware

Performance monitoring middleware provides request timing and operation-specific measurements.

```
```

Sources: [src/fastmcp/server/middleware/timing.py10-58](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/timing.py#L10-L58) [src/fastmcp/server/middleware/timing.py60-157](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/timing.py#L60-L157)

Both middleware use `time.perf_counter()` for high-precision timing measurements and log results in milliseconds with 2 decimal precision.

### Error Handling and Retry Middleware

Error management middleware provides consistent error transformation and automatic retry capabilities.

```
```

Sources: [src/fastmcp/server/middleware/error\_handling.py15-124](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/error_handling.py#L15-L124) [src/fastmcp/server/middleware/error\_handling.py126-207](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/error_handling.py#L126-L207)

The `ErrorHandlingMiddleware` transforms Python exceptions into MCP-compliant `McpError` instances with appropriate error codes, while `RetryMiddleware` implements exponential backoff retry logic for transient failures.

### Rate Limiting Middleware

Rate limiting middleware protects servers from abuse using token bucket and sliding window algorithms.

```
```

Sources: [src/fastmcp/server/middleware/rate\_limiting.py92-168](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/rate_limiting.py#L92-L168) [src/fastmcp/server/middleware/rate\_limiting.py170-232](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/rate_limiting.py#L170-L232)

Both implementations support per-client rate limiting via `get_client_id` functions and use `asyncio.Lock()` for thread-safe operation.

## Custom Middleware Development

Creating custom middleware involves extending the `Middleware` base class and implementing the appropriate hook methods.

### Middleware Hook Methods

| Hook Method          | Trigger               | Context Type          | Use Case                          |
| -------------------- | --------------------- | --------------------- | --------------------------------- |
| `on_message()`       | All messages          | Generic               | Universal logging, authentication |
| `on_request()`       | Request messages      | Generic               | Timing, rate limiting             |
| `on_notification()`  | Notification messages | Generic               | Event tracking                    |
| `on_call_tool()`     | Tool execution        | `CallToolRequest`     | Tool-specific logic               |
| `on_read_resource()` | Resource access       | `ReadResourceRequest` | Resource security                 |
| `on_get_prompt()`    | Prompt retrieval      | `GetPromptRequest`    | Prompt customization              |

Sources: [src/fastmcp/server/middleware/middleware.py11-200](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/middleware/middleware.py#L11-L200)

### Custom Middleware Example Pattern

```
```

Sources: [tests/server/middleware/test\_logging.py110-141](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_logging.py#L110-L141) [tests/server/middleware/test\_timing.py47-70](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_timing.py#L47-L70)

Custom middleware should call `await call_next(context)` to continue the pipeline and can modify the context or result before/after the call.

## Integration with FastMCP Server

Middleware integration occurs through the `FastMCP.add_middleware()` method, which builds the middleware pipeline in registration order.

### Middleware Registration and Execution

```
```

Sources: [tests/server/middleware/test\_logging.py543-575](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_logging.py#L543-L575) [tests/server/middleware/test\_timing.py192-224](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_timing.py#L192-L224)

Middleware executes in the order registered, forming a chain where each middleware can inspect, modify, or terminate request processing. The system supports both synchronous and asynchronous middleware operations through the `CallNext` continuation pattern.

## Middleware Configuration Patterns

Production deployments typically combine multiple middleware types for comprehensive server monitoring and protection.

### Common Middleware Stack Configuration

```
```

Sources: [tests/server/middleware/test\_error\_handling.py589-624](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_error_handling.py#L589-L624) [tests/server/middleware/test\_logging.py710-744](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/middleware/test_logging.py#L710-L744)

This ordering ensures that rate limiting occurs first to protect server resources, followed by comprehensive monitoring and error handling capabilities. The middleware system's flexibility allows for custom combinations based on specific deployment requirements.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Middleware System](#middleware-system.md)
- [Core Middleware Architecture](#core-middleware-architecture.md)
- [Middleware Pipeline Flow](#middleware-pipeline-flow.md)
- [Core Middleware Components](#core-middleware-components.md)
- [Built-in Middleware Types](#built-in-middleware-types.md)
- [Logging Middleware](#logging-middleware.md)
- [Timing and Performance Middleware](#timing-and-performance-middleware.md)
- [Error Handling and Retry Middleware](#error-handling-and-retry-middleware.md)
- [Rate Limiting Middleware](#rate-limiting-middleware.md)
- [Custom Middleware Development](#custom-middleware-development.md)
- [Middleware Hook Methods](#middleware-hook-methods.md)
- [Custom Middleware Example Pattern](#custom-middleware-example-pattern.md)
- [Integration with FastMCP Server](#integration-with-fastmcp-server.md)
- [Middleware Registration and Execution](#middleware-registration-and-execution.md)
- [Middleware Configuration Patterns](#middleware-configuration-patterns.md)
- [Common Middleware Stack Configuration](#common-middleware-stack-configuration.md)
