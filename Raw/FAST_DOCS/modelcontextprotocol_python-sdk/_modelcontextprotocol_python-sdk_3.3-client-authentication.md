Client Authentication | modelcontextprotocol/python-sdk | DeepWiki

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

# Client Authentication

Relevant source files

- [src/mcp/client/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py)
- [src/mcp/server/auth/handlers/register.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py)
- [src/mcp/server/auth/routes.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py)
- [src/mcp/shared/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py)
- [tests/client/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py)
- [tests/shared/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_auth.py)

This page covers the OAuth 2.0 client authentication implementation in the MCP Python SDK. It provides comprehensive OAuth 2.0 support including PKCE flows, automatic discovery, dynamic client registration, and token management for MCP clients.

For server-side authentication, see [OAuth 2.0 Server](#7.2.md). For general ClientSession usage, see [ClientSession](modelcontextprotocol/python-sdk/4.1-protocol-types-and-json-rpc.md).

## Overview

The client authentication system implements OAuth 2.0 Authorization Code flow with PKCE (Proof Key for Code Exchange) for secure authentication with MCP servers. It supports both modern RFC 9728 protected resource architecture and legacy authorization server patterns for backwards compatibility.

**Key Components:**

- `OAuthClientProvider` - Main authentication provider implementing `httpx.Auth`
- `OAuthContext` - Stateful context managing OAuth flow data
- `PKCEParameters` - PKCE parameter generation and validation
- `TokenStorage` - Protocol for persistent token storage

Sources: [src/mcp/client/auth.py1-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L1-L552) [tests/client/test\_auth.py1-900](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L1-L900)

## Architecture Overview

```
```

Sources: [src/mcp/client/auth.py179-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L179-L552) [src/mcp/client/auth.py84-177](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L84-L177)

## Core Components

### OAuthClientProvider

The `OAuthClientProvider` class is the main entry point for OAuth authentication, implementing the `httpx.Auth` interface for seamless integration with HTTP clients.

| Component            | Purpose                          | Key Methods                                               |
| -------------------- | -------------------------------- | --------------------------------------------------------- |
| **Initialization**   | Setup OAuth context and handlers | `__init__()`                                              |
| **Discovery**        | Find authorization endpoints     | `_discover_protected_resource()`, `_get_discovery_urls()` |
| **Registration**     | Register OAuth client            | `_register_client()`                                      |
| **Authorization**    | Perform PKCE flow                | `_perform_authorization()`                                |
| **Token Management** | Exchange and refresh tokens      | `_exchange_token()`, `_refresh_token()`                   |
| **Integration**      | HTTPX auth flow                  | `async_auth_flow()`                                       |

**Key Configuration:**

```
```

Sources: [src/mcp/client/auth.py179-206](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L179-L206) [src/mcp/client/auth.py485-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L485-L552)

### OAuthContext

The `OAuthContext` dataclass maintains all state during the OAuth flow, including discovered metadata, client information, and current tokens.

**State Management:**

- **Discovery metadata**: `protected_resource_metadata`, `oauth_metadata`
- **Client registration**: `client_info`
- **Token state**: `current_tokens`, `token_expiry_time`
- **Thread safety**: `lock` (anyio.Lock)

**Key Methods:**

- `is_token_valid()` - Check token validity and expiration
- `can_refresh_token()` - Determine if refresh is possible
- `get_resource_url()` - Calculate RFC 8707 resource parameter
- `should_include_resource_param()` - Protocol version-aware parameter inclusion

Sources: [src/mcp/client/auth.py84-177](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L84-L177)

### PKCEParameters

Implements PKCE (Proof Key for Code Exchange) parameter generation following RFC 7636 for enhanced security.

**Generation Process:**

- **Code verifier**: 128-character random string using `[A-Za-z0-9-._~]`
- **Code challenge**: SHA256 hash of verifier, base64url-encoded (no padding)
- **Challenge method**: Always "S256"

```
```

Sources: [src/mcp/client/auth.py49-62](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L49-L62) [tests/client/test\_auth.py82-107](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L82-L107)

## Authentication Flow

### Complete OAuth Flow Sequence

```
```

Sources: [src/mcp/client/auth.py485-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L485-L552) [tests/client/test\_auth.py575-701](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L575-L701)

### Discovery Mechanisms

The client implements multiple discovery mechanisms for maximum compatibility:

**1. RFC 9728 Protected Resource Discovery**

- Extracts resource metadata URL from `WWW-Authenticate` header
- Falls back to `/.well-known/oauth-protected-resource`
- Discovers authorization server URLs

**2. OAuth Metadata Discovery with Fallback** The client tries multiple discovery URLs in order:

1. `/.well-known/oauth-authorization-server{path}` (RFC 8414 path-aware)
2. `/.well-known/oauth-authorization-server` (OAuth root)
3. `/.well-known/openid-configuration{path}` (OIDC path-aware)
4. `{server_url}/.well-known/openid-configuration` (OIDC fallback)

```
```

Sources: [src/mcp/client/auth.py254-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L254-L279) [src/mcp/client/auth.py231-253](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L231-L253) [tests/client/test\_auth.py252-365](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L252-L365)

### WWW-Authenticate Header Parsing

Supports RFC 9728 resource metadata discovery via `WWW-Authenticate` header parsing:

```
```

**Supported Header Formats:**

- `Bearer resource_metadata="https://api.example.com/.well-known/oauth-protected-resource"`
- `Bearer resource_metadata=https://api.example.com/metadata`
- `Bearer realm="api", resource_metadata="https://api.example.com/metadata", error="insufficient_scope"`

Sources: [src/mcp/client/auth.py207-229](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L207-L229) [tests/client/test\_auth.py782-900](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L782-L900)

## Token Management

### Token Lifecycle

```
```

### Token Validation and Refresh

**Token Validity Checking:**

```
```

**Automatic Refresh Logic:** The provider automatically attempts token refresh when:

1. Current token is expired but refresh token exists
2. Client information is available for authentication
3. Refresh fails trigger full re-authentication

Sources: [src/mcp/client/auth.py127-143](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L127-L143) [src/mcp/client/auth.py494-502](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L494-L502) [src/mcp/client/auth.py411-462](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L411-L462)

### Resource Parameter Handling

Implements RFC 8707 resource parameter inclusion based on protocol version and protected resource metadata:

```
```

**Resource URL Calculation:**

- Uses protected resource metadata if available and valid
- Falls back to canonical server URL derived from MCP endpoint
- Validates hierarchical resource relationships

Sources: [src/mcp/client/auth.py159-177](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L159-L177) [src/mcp/client/auth.py144-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L144-L158) [tests/client/test\_auth.py459-534](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L459-L534)

## Token Storage

### TokenStorage Protocol

The `TokenStorage` protocol defines the interface for persistent token storage:

```
```

**Implementation Requirements:**

- **Persistence**: Tokens should survive application restarts
- **Security**: Secure storage with appropriate encryption
- **Concurrency**: Thread-safe access patterns
- **Cleanup**: Automatic removal of expired tokens

**Example Storage Implementation:**

```
```

Sources: [src/mcp/client/auth.py64-82](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L64-L82) [tests/client/test\_auth.py17-35](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L17-L35)

## Error Handling

### Exception Hierarchy

| Exception                | Usage                        | Common Causes                          |
| ------------------------ | ---------------------------- | -------------------------------------- |
| `OAuthFlowError`         | Base OAuth flow errors       | Network issues, invalid configuration  |
| `OAuthTokenError`        | Token-specific errors        | Invalid tokens, expired refresh tokens |
| `OAuthRegistrationError` | Client registration failures | Invalid metadata, server rejection     |

**Error Recovery Strategies:**

- **Network errors**: Automatic retry with exponential backoff
- **Invalid tokens**: Clear stored tokens and restart OAuth flow
- **Registration failures**: Log error details for debugging
- **Authorization failures**: Clear state and prompt re-authentication

```
```

Sources: [src/mcp/client/auth.py37-47](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L37-L47) [src/mcp/client/auth.py388-410](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L388-L410) [src/mcp/client/auth.py442-462](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L442-L462)

## Integration Examples

### Basic Usage with HTTP Client

```
```

### Transport Integration

The authentication provider integrates seamlessly with all MCP transports:

- **StreamableHTTP**: Built-in OAuth support via `httpx.AsyncClient`
- **SSE**: Authentication headers added to SSE connections
- **WebSocket**: OAuth tokens passed in connection headers
- **stdio**: Not applicable (local process communication)

Sources: [examples/clients/simple-auth-client/](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-auth-client/) [src/mcp/client/auth.py485-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L485-L552)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Authentication](#client-authentication.md)
- [Overview](#overview.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Components](#core-components.md)
- [OAuthClientProvider](#oauthclientprovider.md)
- [OAuthContext](#oauthcontext.md)
- [PKCEParameters](#pkceparameters.md)
- [Authentication Flow](#authentication-flow.md)
- [Complete OAuth Flow Sequence](#complete-oauth-flow-sequence.md)
- [Discovery Mechanisms](#discovery-mechanisms.md)
- [WWW-Authenticate Header Parsing](#www-authenticate-header-parsing.md)
- [Token Management](#token-management.md)
- [Token Lifecycle](#token-lifecycle.md)
- [Token Validation and Refresh](#token-validation-and-refresh.md)
- [Resource Parameter Handling](#resource-parameter-handling.md)
- [Token Storage](#token-storage.md)
- [TokenStorage Protocol](#tokenstorage-protocol.md)
- [Error Handling](#error-handling.md)
- [Exception Hierarchy](#exception-hierarchy.md)
- [Integration Examples](#integration-examples.md)
- [Basic Usage with HTTP Client](#basic-usage-with-http-client.md)
- [Transport Integration](#transport-integration.md)
