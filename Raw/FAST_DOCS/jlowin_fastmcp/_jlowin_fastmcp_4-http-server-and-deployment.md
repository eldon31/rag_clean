HTTP Server and Deployment | jlowin/fastmcp | DeepWiki

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

# HTTP Server and Deployment

Relevant source files

- [src/fastmcp/server/auth/\_\_init\_\_.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/__init__.py)
- [src/fastmcp/server/auth/auth.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/auth.py)
- [src/fastmcp/server/dependencies.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/dependencies.py)
- [src/fastmcp/server/http.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py)
- [tests/server/auth/test\_remote\_auth\_provider.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/test_remote_auth_provider.py)
- [tests/server/auth/test\_static\_token\_verifier.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/test_static_token_verifier.py)
- [tests/server/http/test\_bearer\_auth\_backend.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/http/test_bearer_auth_backend.py)

This page covers the HTTP server architecture and deployment patterns in FastMCP. It explains how FastMCP servers expose MCP protocols over HTTP using Starlette/ASGI applications, including support for Server-Sent Events (SSE) and Streamable HTTP transports. For client-side HTTP communication, see [Transport Mechanisms](jlowin/fastmcp/3.1-transport-mechanisms.md). For authentication and security configuration, see [Authentication and Security](jlowin/fastmcp/4.1-authentication-and-security.md).

## HTTP Server Architecture

FastMCP provides HTTP server functionality through ASGI applications built on Starlette. The system supports two primary HTTP transport mechanisms for the MCP protocol: SSE (Server-Sent Events) and Streamable HTTP.

```
```

Sources: [src/fastmcp/server/http.py98-123](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L98-L123) [src/fastmcp/server/http.py126-228](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L126-L228) [src/fastmcp/server/http.py231-321](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L231-L321)

## Transport Mechanisms

### SSE (Server-Sent Events) Transport

SSE transport provides real-time bidirectional communication using Server-Sent Events for server-to-client messages and HTTP POST for client-to-server messages.

```
```

Sources: [src/fastmcp/server/http.py126-228](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L126-L228) [src/fastmcp/server/http.py152-163](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L152-L163)

### Streamable HTTP Transport

Streamable HTTP transport provides session-based communication over standard HTTP requests with optional JSON response formatting.

```
```

Sources: [src/fastmcp/server/http.py231-321](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L231-L321) [src/fastmcp/server/http.py261-267](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L261-L267) [src/fastmcp/server/http.py304-314](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L304-L314)

## ASGI Application Structure

### Base Application Factory

The `create_base_app()` function creates the foundational Starlette application with common middleware and routing.

| Component                  | Purpose                                       | Implementation                                                                                                            |
| -------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `StarletteWithLifespan`    | Extended Starlette app with lifespan property | [src/fastmcp/server/http.py67-71](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L67-L71)     |
| `RequestContextMiddleware` | Stores HTTP request in context variable       | [src/fastmcp/server/http.py82-95](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L82-L95)     |
| Route configuration        | Custom routes with MCP endpoints              | [src/fastmcp/server/http.py98-123](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L98-L123)   |
| Middleware stack           | Authentication and custom middleware          | [src/fastmcp/server/http.py115-116](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L115-L116) |

### Request Context System

FastMCP maintains HTTP request context through context variables for dependency injection in tools and resources.

```
```

Sources: [src/fastmcp/server/http.py61-79](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L61-L79) [src/fastmcp/server/dependencies.py42-53](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/dependencies.py#L42-L53) [src/fastmcp/server/dependencies.py56-99](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/dependencies.py#L56-L99)

## Authentication Integration

### Auth Provider Routes

Authentication providers integrate with HTTP apps through route and middleware systems.

```
```

Sources: [src/fastmcp/server/auth/auth.py81-119](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/auth.py#L81-L119) [src/fastmcp/server/auth/auth.py121-133](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/auth.py#L121-L133) [src/fastmcp/server/http.py166-189](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L166-L189)

### Route Configuration with Authentication

| Auth Type            | Route Creation              | Middleware                                    | Protected Endpoints       |
| -------------------- | --------------------------- | --------------------------------------------- | ------------------------- |
| No Auth              | Direct route creation       | `RequestContextMiddleware` only               | None                      |
| `TokenVerifier`      | Base routes + protected MCP | `BearerAuthBackend` + `AuthContextMiddleware` | MCP endpoint              |
| `RemoteAuthProvider` | Protected resource metadata | Same as TokenVerifier                         | MCP + metadata endpoints  |
| `OAuthProvider`      | Full OAuth server routes    | Same as TokenVerifier                         | All OAuth + MCP endpoints |

Sources: [src/fastmcp/server/http.py190-207](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L190-L207) [src/fastmcp/server/http.py273-284](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L273-L284) [src/fastmcp/server/auth/auth.py225-252](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/auth.py#L225-L252)

## Deployment Patterns

### Standalone ASGI Deployment

FastMCP HTTP apps can be deployed directly with ASGI servers:

```
```

### Parent ASGI Application Integration

FastMCP apps can be mounted within larger ASGI applications like FastAPI:

```
```

Sources: [src/fastmcp/server/http.py29-58](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L29-L58) [src/fastmcp/server/http.py304-314](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L304-L314)

## Error Handling and Diagnostics

### Streamable HTTP Task Group Error

The `StreamableHTTPASGIApp` provides detailed error messages for common deployment issues:

| Error Condition              | Root Cause                          | Error Message                                                           | Solution                                      |
| ---------------------------- | ----------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------- |
| Task group not initialized   | Parent app doesn't use MCP lifespan | "FastMCP's StreamableHTTPSessionManager task group was not initialized" | Set `lifespan=mcp_app.lifespan` in parent app |
| Runtime error during request | MCP library internal error          | Original error message preserved                                        | Check MCP library documentation               |
| General ASGI errors          | Various deployment issues           | Standard ASGI error handling                                            | Review ASGI server logs                       |

Sources: [src/fastmcp/server/http.py35-58](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/http.py#L35-L58)

### Request Context Errors

| Function             | Error Condition           | Exception          | Solution                                    |
| -------------------- | ------------------------- | ------------------ | ------------------------------------------- |
| `get_http_request()` | No active HTTP request    | `RuntimeError`     | Ensure called within HTTP request context   |
| `get_http_headers()` | No active HTTP request    | Returns empty dict | Check for HTTP context before using headers |
| `get_context()`      | No active FastMCP context | `RuntimeError`     | Ensure called within FastMCP tool/resource  |

Sources: [src/fastmcp/server/dependencies.py42-53](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/dependencies.py#L42-L53) [src/fastmcp/server/dependencies.py56-99](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/dependencies.py#L56-L99) [src/fastmcp/server/dependencies.py30-36](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/dependencies.py#L30-L36)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [HTTP Server and Deployment](#http-server-and-deployment.md)
- [HTTP Server Architecture](#http-server-architecture.md)
- [Transport Mechanisms](#transport-mechanisms.md)
- [SSE (Server-Sent Events) Transport](#sse-server-sent-events-transport.md)
- [Streamable HTTP Transport](#streamable-http-transport.md)
- [ASGI Application Structure](#asgi-application-structure.md)
- [Base Application Factory](#base-application-factory.md)
- [Request Context System](#request-context-system.md)
- [Authentication Integration](#authentication-integration.md)
- [Auth Provider Routes](#auth-provider-routes.md)
- [Route Configuration with Authentication](#route-configuration-with-authentication.md)
- [Deployment Patterns](#deployment-patterns.md)
- [Standalone ASGI Deployment](#standalone-asgi-deployment.md)
- [Parent ASGI Application Integration](#parent-asgi-application-integration.md)
- [Error Handling and Diagnostics](#error-handling-and-diagnostics.md)
- [Streamable HTTP Task Group Error](#streamable-http-task-group-error.md)
- [Request Context Errors](#request-context-errors.md)
