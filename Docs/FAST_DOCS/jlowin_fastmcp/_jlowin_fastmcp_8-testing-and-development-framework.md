Testing and Development Framework | jlowin/fastmcp | DeepWiki

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

# Testing and Development Framework

Relevant source files

- [src/fastmcp/utilities/tests.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/tests.py)
- [tests/client/auth/test\_oauth\_client.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/auth/test_oauth_client.py)
- [tests/client/test\_openapi\_experimental.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_openapi_experimental.py)
- [tests/client/test\_openapi\_legacy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_openapi_legacy.py)
- [tests/client/test\_sse.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_sse.py)
- [tests/client/test\_streamable\_http.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_streamable_http.py)
- [tests/conftest.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/conftest.py)
- [tests/contrib/test\_bulk\_tool\_caller.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/contrib/test_bulk_tool_caller.py)
- [tests/server/auth/providers/test\_descope.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/providers/test_descope.py)
- [tests/server/auth/providers/test\_workos.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/providers/test_workos.py)
- [tests/server/auth/test\_jwt\_provider.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/test_jwt_provider.py)
- [tests/server/http/test\_http\_dependencies.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/http/test_http_dependencies.py)

This document covers FastMCP's comprehensive testing infrastructure, development utilities, and testing patterns. It explains the testing utilities, fixtures, and methodologies used to test FastMCP servers, clients, transports, and integrations.

For information about deployment and production configuration, see [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md). For development workflow tools like the CLI, see [Command Line Interface](jlowin/fastmcp/5-command-line-interface.md).

## Testing Infrastructure Overview

FastMCP provides a robust testing framework designed to handle the complexities of testing distributed MCP systems, including process isolation, network communication, authentication flows, and transport mechanisms.

```
```

**Testing Framework Architecture**

Sources: [src/fastmcp/utilities/tests.py1-200](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/tests.py#L1-L200) [tests/conftest.py1-60](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/conftest.py#L1-L60)

## Core Testing Utilities

### Process Management

The `run_server_in_process()` function provides isolated server testing by running FastMCP servers in separate processes:

```
```

**Process Isolation for Server Testing**

The utility handles server lifecycle, port allocation, and cleanup automatically:

| Function                  | Purpose                                | Key Parameters                          |
| ------------------------- | -------------------------------------- | --------------------------------------- |
| `run_server_in_process()` | Spawns server in separate process      | `server_fn`, `host`, `port`, `**kwargs` |
| Socket readiness check    | Waits for server to accept connections | `max_attempts=30`                       |
| Process cleanup           | Terminates server process              | `timeout=5` for graceful, then `kill()` |

Sources: [src/fastmcp/utilities/tests.py74-140](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/tests.py#L74-L140)

### Settings Override System

The `temporary_settings()` context manager allows safe modification of FastMCP configuration during tests:

```
```

Sources: [src/fastmcp/utilities/tests.py24-55](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/tests.py#L24-L55)

### Authentication Testing

The `HeadlessOAuth` class simulates OAuth flows without browser interaction:

```
```

**Headless OAuth Flow for Testing**

The implementation bypasses browser interaction by making direct HTTP requests and parsing redirect responses:

| Method               | Purpose                          | Returns              |
| -------------------- | -------------------------------- | -------------------- |
| `redirect_handler()` | Makes HTTP request to auth URL   | Stores response      |
| `callback_handler()` | Extracts auth code from redirect | `(auth_code, state)` |

Sources: [src/fastmcp/utilities/tests.py154-200](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/tests.py#L154-L200)

## Test Fixtures and Configuration

### Port Management

FastMCP provides utilities for managing network ports in test environments:

```
```

The `free_port_factory` tracks used ports to prevent conflicts in parallel test execution.

Sources: [tests/conftest.py34-59](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/conftest.py#L34-L59)

### Integration Test Marking

Tests are automatically categorized based on their location:

```
```

Sources: [tests/conftest.py8-13](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/conftest.py#L8-L13)

## Transport Testing Patterns

### HTTP Transport Testing

FastMCP tests HTTP transports using real server instances with comprehensive scenarios:

```
```

**HTTP Transport Testing Architecture**

Key test patterns include:

- **Parameterized testing**: Tests run against both stateless and stateful HTTP modes
- **Header propagation**: Verification that client headers reach server components
- **Timeout handling**: Testing both client-level and operation-level timeouts
- **Progress reporting**: Async progress updates during long-running operations

Sources: [tests/client/test\_streamable\_http.py21-248](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_streamable_http.py#L21-L248)

### SSE Transport Testing

Server-Sent Events transport testing follows similar patterns with transport-specific considerations:

| Test Category      | Key Features                       | Example Test                                  |
| ------------------ | ---------------------------------- | --------------------------------------------- |
| Basic connectivity | Ping, list operations              | `test_ping()`                                 |
| Header handling    | Client header propagation          | `test_http_headers()`                         |
| Timeout behavior   | Platform-specific timeout handling | `TestTimeout` class                           |
| Nested routing     | Complex URL path resolution        | `test_nested_sse_server_resolves_correctly()` |

Sources: [tests/client/test\_sse.py19-167](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_sse.py#L19-L167)

## Authentication Testing Framework

### JWT Provider Testing

FastMCP includes comprehensive JWT testing with both RSA and symmetric key scenarios:

```
```

**JWT Authentication Testing Framework**

The testing framework provides helpers for various JWT scenarios:

- **RSA key management**: `RSAKeyPair.generate()` creates test key pairs
- **Symmetric keys**: `SymmetricKeyHelper` for HMAC algorithms
- **Token validation**: Comprehensive issuer, audience, and scope testing
- **JWKS mocking**: HTTP mocking for JWKS URI endpoints

Sources: [tests/server/auth/test\_jwt\_provider.py14-871](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/test_jwt_provider.py#L14-L871)

### OAuth Provider Testing

OAuth providers are tested using integration patterns with real HTTP servers:

```
```

Sources: [tests/server/auth/providers/test\_descope.py121-141](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/providers/test_descope.py#L121-L141) [tests/server/auth/providers/test\_workos.py160-178](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/providers/test_workos.py#L160-L178)

## Component Testing Patterns

### Tool Testing with BulkToolCaller

The `BulkToolCaller` provides patterns for testing tool execution at scale:

```
```

**Bulk Tool Testing Framework**

Key testing patterns include:

- **Live server integration**: Tests use actual `FastMCP` instances with registered tools
- **Error propagation**: Testing both fail-fast and continue-on-error modes
- **Result validation**: Snapshot testing for consistent output verification

Sources: [tests/contrib/test\_bulk\_tool\_caller.py70-289](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/contrib/test_bulk_tool_caller.py#L70-L289)

### HTTP Dependencies Testing

FastMCP tests dependency injection in HTTP contexts across multiple transports:

| Component            | Test Pattern                 | Verification                        |
| -------------------- | ---------------------------- | ----------------------------------- |
| `get_http_request()` | Tool, Resource, Prompt usage | Header extraction from HTTP request |
| StreamableHttp       | Direct header propagation    | Client headers in server context    |
| SSE                  | Event stream headers         | Header preservation across SSE      |

Sources: [tests/server/http/test\_http\_dependencies.py13-124](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/http/test_http_dependencies.py#L13-L124)

## Development Workflow Testing

### OpenAPI Integration Testing

FastMCP tests OpenAPI server generation with both legacy and experimental parsers:

```
```

The testing verifies:

- **Route mapping**: HTTP routes to MCP components
- **Header propagation**: Client and server headers through proxy chains
- **Resource templates**: Dynamic URI pattern matching

Sources: [tests/client/test\_openapi\_legacy.py13-47](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_openapi_legacy.py#L13-L47) [tests/client/test\_openapi\_experimental.py14-46](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_openapi_experimental.py#L14-L46)

## Best Practices and Patterns

### Test Organization

FastMCP follows these testing organization principles:

1. **Fixture-based setup**: Reusable server and client configurations
2. **Process isolation**: Each test gets clean server instances
3. **Transport agnostic**: Tests run across multiple transport types
4. **Integration marking**: Automatic categorization of integration vs unit tests
5. **Parallel execution**: xdist compatibility with port management

### Error Testing Patterns

```
```

### Authentication Test Patterns

```
```

Sources: [tests/client/test\_streamable\_http.py222-248](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/test_streamable_http.py#L222-L248) [tests/server/auth/providers/test\_descope.py156-164](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/providers/test_descope.py#L156-L164)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Testing and Development Framework](#testing-and-development-framework.md)
- [Testing Infrastructure Overview](#testing-infrastructure-overview.md)
- [Core Testing Utilities](#core-testing-utilities.md)
- [Process Management](#process-management.md)
- [Settings Override System](#settings-override-system.md)
- [Authentication Testing](#authentication-testing.md)
- [Test Fixtures and Configuration](#test-fixtures-and-configuration.md)
- [Port Management](#port-management.md)
- [Integration Test Marking](#integration-test-marking.md)
- [Transport Testing Patterns](#transport-testing-patterns.md)
- [HTTP Transport Testing](#http-transport-testing.md)
- [SSE Transport Testing](#sse-transport-testing.md)
- [Authentication Testing Framework](#authentication-testing-framework.md)
- [JWT Provider Testing](#jwt-provider-testing.md)
- [OAuth Provider Testing](#oauth-provider-testing.md)
- [Component Testing Patterns](#component-testing-patterns.md)
- [Tool Testing with BulkToolCaller](#tool-testing-with-bulktoolcaller.md)
- [HTTP Dependencies Testing](#http-dependencies-testing.md)
- [Development Workflow Testing](#development-workflow-testing.md)
- [OpenAPI Integration Testing](#openapi-integration-testing.md)
- [Best Practices and Patterns](#best-practices-and-patterns.md)
- [Test Organization](#test-organization.md)
- [Error Testing Patterns](#error-testing-patterns.md)
- [Authentication Test Patterns](#authentication-test-patterns.md)
