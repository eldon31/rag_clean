Transport Security | modelcontextprotocol/python-sdk | DeepWiki

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

# Transport Security

Relevant source files

- [src/mcp/client/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py)
- [src/mcp/server/auth/handlers/register.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py)
- [src/mcp/server/auth/routes.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py)
- [src/mcp/server/sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/sse.py)
- [src/mcp/shared/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py)
- [tests/client/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py)
- [tests/shared/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_auth.py)
- [tests/shared/test\_sse.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_sse.py)

This document covers the security features implemented for MCP transport layers, focusing on DNS rebinding protection and request validation middleware. The security system provides configurable protection against malicious cross-origin requests targeting locally-hosted MCP servers.

For information about specific transport implementations, see [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md), [SSE Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md), and [WebSocket Transport](modelcontextprotocol/python-sdk/5.4-transport-security.md). For authentication mechanisms, see [Authentication & Security](modelcontextprotocol/python-sdk/7-authentication-and-security.md).

## Security Architecture Overview

The transport security system implements a middleware-based architecture that validates incoming HTTP requests before they reach the MCP protocol handlers. The system is designed to prevent DNS rebinding attacks while maintaining compatibility with legitimate client connections.

```
```

Sources: [src/mcp/server/transport\_security.py37-128](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L37-L128) [src/mcp/server/streamable\_http\_manager.py24-68](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L24-L68)

## DNS Rebinding Protection

DNS rebinding attacks occur when malicious websites trick browsers into making requests to local servers using specially crafted DNS responses. The MCP security system prevents these attacks by validating request headers that browsers automatically include.

### Threat Model

| Attack Vector         | Validation Method         | HTTP Status | Error Message                 |
| --------------------- | ------------------------- | ----------- | ----------------------------- |
| Malicious Host header | Host whitelist validation | 421         | "Invalid Host header"         |
| Cross-origin requests | Origin header validation  | 400         | "Invalid Origin header"       |
| Wrong content type    | Content-Type validation   | 400         | "Invalid Content-Type header" |

```
```

Sources: [src/mcp/server/transport\_security.py45-66](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L45-L66) [tests/server/test\_streamable\_http\_security.py110-136](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_streamable_http_security.py#L110-L136)

## Configuration Settings

The `TransportSecuritySettings` class provides flexible configuration for security features:

### Basic Configuration

```
```

### Wildcard Port Patterns

The system supports wildcard port patterns for development environments:

| Pattern                | Matches               | Example                            |
| ---------------------- | --------------------- | ---------------------------------- |
| `"localhost:*"`        | Any port on localhost | `localhost:3000`, `localhost:8080` |
| `"127.0.0.1:*"`        | Any port on 127.0.0.1 | `127.0.0.1:5000`, `127.0.0.1:9999` |
| `"http://localhost:*"` | Any port in origins   | `http://localhost:3000`            |

```
```

Sources: [src/mcp/server/transport\_security.py12-35](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L12-L35) [src/mcp/server/transport\_security.py56-63](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L56-L63) [tests/server/test\_sse\_security.py226-256](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_sse_security.py#L226-L256)

## Security Middleware Implementation

The `TransportSecurityMiddleware` class implements the core validation logic:

### Validation Methods

| Method                     | Purpose                                 | Returns    |
| -------------------------- | --------------------------------------- | ---------- |
| `_validate_host()`         | Validates Host header against whitelist | `bool`     |
| `_validate_origin()`       | Validates Origin header (optional)      | `bool`     |
| `_validate_content_type()` | Ensures JSON content type for POST      | `bool`     |
| `validate_request()`       | Main validation entry point             | \`Response |

### Validation Flow

```
```

Sources: [src/mcp/server/transport\_security.py102-128](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L102-L128) [src/mcp/server/transport\_security.py89-101](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L89-L101)

## Transport Integration

Security middleware integrates with multiple transport types through a common pattern:

### StreamableHTTP Integration

The `StreamableHTTPSessionManager` accepts security settings and passes them to transport instances:

```
```

### SSE Integration

The `SseServerTransport` similarly integrates security validation:

| Transport Type | Security Integration Point                  | Error Handling                    |
| -------------- | ------------------------------------------- | --------------------------------- |
| StreamableHTTP | `StreamableHTTPServerTransport` constructor | Middleware returns error response |
| SSE            | `SseServerTransport` constructor            | Validation in `connect_sse()`     |
| WebSocket      | Not implemented                             | N/A                               |
| STDIO          | Not applicable                              | Local process communication       |

Sources: [src/mcp/server/streamable\_http\_manager.py62-68](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L62-L68) [src/mcp/server/streamable\_http\_manager.py224-229](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/streamable_http_manager.py#L224-L229) [tests/server/test\_sse\_security.py45-58](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_sse_security.py#L45-L58)

## Default Security Behavior

The security system uses conservative defaults to maintain backward compatibility:

### Default Settings

| Setting                           | Default Value                             | Rationale                     |
| --------------------------------- | ----------------------------------------- | ----------------------------- |
| `enable_dns_rebinding_protection` | `True` in settings, `False` in middleware | Backwards compatibility       |
| `allowed_hosts`                   | `[]` (empty list)                         | Must be explicitly configured |
| `allowed_origins`                 | `[]` (empty list)                         | Must be explicitly configured |

### Backward Compatibility

```
```

Sources: [src/mcp/server/transport\_security.py40-43](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L40-L43) [src/mcp/server/transport\_security.py114-115](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/transport_security.py#L114-L115)

## Testing and Validation

The security system includes comprehensive tests covering various attack scenarios and configuration options:

### Test Coverage

| Test Category           | File                               | Key Test Cases                               |
| ----------------------- | ---------------------------------- | -------------------------------------------- |
| StreamableHTTP Security | `test_streamable_http_security.py` | Host/Origin validation, Content-Type checks  |
| SSE Security            | `test_sse_security.py`             | GET/POST validation, wildcard patterns       |
| Integration             | Both files                         | Real server processes, multiprocessing tests |

### Security Test Scenarios

```
```

Sources: [tests/server/test\_streamable\_http\_security.py85-294](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_streamable_http_security.py#L85-L294) [tests/server/test\_sse\_security.py78-294](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_sse_security.py#L78-L294)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Transport Security](#transport-security.md)
- [Security Architecture Overview](#security-architecture-overview.md)
- [DNS Rebinding Protection](#dns-rebinding-protection.md)
- [Threat Model](#threat-model.md)
- [Configuration Settings](#configuration-settings.md)
- [Basic Configuration](#basic-configuration.md)
- [Wildcard Port Patterns](#wildcard-port-patterns.md)
- [Security Middleware Implementation](#security-middleware-implementation.md)
- [Validation Methods](#validation-methods.md)
- [Validation Flow](#validation-flow.md)
- [Transport Integration](#transport-integration.md)
- [StreamableHTTP Integration](#streamablehttp-integration.md)
- [SSE Integration](#sse-integration.md)
- [Default Security Behavior](#default-security-behavior.md)
- [Default Settings](#default-settings.md)
- [Backward Compatibility](#backward-compatibility.md)
- [Testing and Validation](#testing-and-validation.md)
- [Test Coverage](#test-coverage.md)
- [Security Test Scenarios](#security-test-scenarios.md)
