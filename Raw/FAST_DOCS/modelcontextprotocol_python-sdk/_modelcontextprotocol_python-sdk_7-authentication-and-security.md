Authentication & Security | modelcontextprotocol/python-sdk | DeepWiki

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

# Authentication & Security

Relevant source files

- [src/mcp/client/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py)
- [src/mcp/server/auth/handlers/register.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py)
- [src/mcp/server/auth/routes.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py)
- [src/mcp/shared/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py)
- [tests/client/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py)
- [tests/shared/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_auth.py)

This document covers the OAuth 2.0 authentication system implemented in the MCP Python SDK for securing communication between MCP clients and servers. The authentication system provides both client-side authentication (for MCP clients connecting to protected servers) and server-side authentication (for MCP servers that need to authenticate clients).

The OAuth system integrates seamlessly with MCP's core components:

- **ClientSession**: Automatically handles OAuth authentication when connecting to protected MCP servers
- **FastMCP servers**: Can optionally expose OAuth authorization server endpoints
- **Transport layer**: OAuth authentication works across all transport mechanisms (stdio, SSE, StreamableHTTP)

For detailed OAuth implementation specifics, see [OAuth 2.0 System](modelcontextprotocol/python-sdk/7.1-oauth-2.0-system.md). For transport-level security features like DNS rebinding protection, see [Transport Security](modelcontextprotocol/python-sdk/5.4-transport-security.md). For the overall client framework, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md).

## MCP Authentication Integration

```
```

**Sources:** [src/mcp/client/auth.py179-206](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L179-L206) [src/mcp/server/auth/routes.py68-146](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L68-L146) [src/mcp/client/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/session.py) [src/mcp/server/fastmcp/](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/)

## OAuth 2.0 Client Authentication

The MCP SDK provides a complete OAuth 2.0 client implementation centered around the `OAuthClientProvider` class, which integrates with httpx to provide transparent authentication for HTTP requests.

### Core Client Components Architecture

```
```

The `OAuthClientProvider` implements the `httpx.Auth` interface, allowing it to be used as an authentication handler for any HTTP client that supports httpx auth providers. The class is instantiated with server URL, client metadata, token storage, and callback handlers for user interaction.

**Sources:** [src/mcp/client/auth.py179-206](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L179-L206) [src/mcp/shared/auth.py6-25](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L6-L25) [src/mcp/shared/auth.py37-91](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L37-L91) [src/mcp/shared/auth.py93-103](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L93-L103)

### OAuth Flow Implementation

The client authentication follows the OAuth 2.0 authorization code flow with PKCE (Proof Key for Code Exchange) for enhanced security. The entire flow is implemented in the `async_auth_flow()` method:

```
```

The flow includes several key security features implemented in specific methods:

- **PKCE (RFC 7636)**: `PKCEParameters.generate()` prevents authorization code interception attacks
- **State parameter**: `_perform_authorization()` prevents CSRF attacks during authorization
- **Dynamic Client Registration (RFC 7591)**: `_register_client()` enables automatic client registration
- **Protected Resource Discovery (RFC 9728)**: `_discover_protected_resource()` enables automatic authorization server discovery

**Sources:** [src/mcp/client/auth.py485-551](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L485-L551) [src/mcp/client/auth.py312-356](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L312-L356) [src/mcp/client/auth.py49-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L49-L61) [src/mcp/client/auth.py231-252](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L231-L252)

### Token Management and Storage

The SDK provides a flexible token storage system through the `TokenStorage` protocol interface:

| Method              | Purpose                      | Parameters                   | Return Type                          |
| ------------------- | ---------------------------- | ---------------------------- | ------------------------------------ |
| `get_tokens()`      | Retrieve stored tokens       | None                         | `OAuthToken \| None`                 |
| `set_tokens()`      | Store new tokens             | `OAuthToken`                 | `None`                               |
| `get_client_info()` | Retrieve client registration | None                         | `OAuthClientInformationFull \| None` |
| `set_client_info()` | Store client registration    | `OAuthClientInformationFull` | `None`                               |

Token validation and refresh logic is handled automatically in `async_auth_flow()`:

```
```

The `OAuthContext` class manages token expiry using the `update_token_expiry()` method, which calculates wall-clock time based on the `expires_in` field from token responses. Token validation is performed by `is_token_valid()` which checks both token presence and expiry time.

**Sources:** [src/mcp/client/auth.py64-82](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L64-L82) [src/mcp/client/auth.py120-142](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L120-L142) [src/mcp/client/auth.py411-461](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L411-L461) [src/mcp/client/auth.py494-501](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L494-L501)

### Protected Resource Discovery

The client implements RFC 9728 for automatic discovery of authorization servers through several methods in `OAuthClientProvider`. The discovery process supports multiple fallback mechanisms:

1. **WWW-Authenticate Header**: `_extract_resource_metadata_from_www_auth()` extracts `resource_metadata` URL from 401 responses
2. **Well-known Resource Discovery**: `_discover_protected_resource()` falls back to `/.well-known/oauth-protected-resource`
3. **Authorization Server Discovery**: `_get_discovery_urls()` tries multiple OAuth metadata endpoints

```
```

The discovery flow uses regex pattern matching in `_extract_resource_metadata_from_www_auth()` to parse the WWW-Authenticate header: `resource_metadata=(?:"([^"]+)"|([^\s,]+))`. If no resource\_metadata is found, it constructs the well-known URL using `get_authorization_base_url()` and `urljoin()`.

**Sources:** [src/mcp/client/auth.py207-240](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L207-L240) [src/mcp/client/auth.py254-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L254-L279) [src/mcp/client/auth.py517-530](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L517-L530) [src/mcp/client/auth.py242-252](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L242-L252)

## OAuth 2.0 Server Implementation

The server-side authentication system provides a complete OAuth 2.0 authorization server implementation that MCP servers can use to authenticate clients. The system is built around the `create_auth_routes()` function and handler classes.

### Server Components Architecture

```
```

**Sources:** [src/mcp/server/auth/routes.py68-146](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L68-L146) [src/mcp/server/auth/handlers/](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/) [src/mcp/server/auth/middleware/client\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/middleware/client_auth.py) [src/mcp/server/auth/settings.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/settings.py)

### OAuth Metadata Generation

The server automatically generates RFC 8414 compliant OAuth metadata using the `build_metadata()` function based on configuration:

| Field                                   | Value                                     | Source                                    |
| --------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| `issuer`                                | Server base URL                           | `issuer_url` parameter                    |
| `authorization_endpoint`                | `{issuer}/authorize`                      | `AUTHORIZATION_PATH` constant             |
| `token_endpoint`                        | `{issuer}/token`                          | `TOKEN_PATH` constant                     |
| `registration_endpoint`                 | `{issuer}/register`                       | `REGISTRATION_PATH` constant (if enabled) |
| `revocation_endpoint`                   | `{issuer}/revoke`                         | `REVOCATION_PATH` constant (if enabled)   |
| `scopes_supported`                      | Valid scopes list                         | `ClientRegistrationOptions.valid_scopes`  |
| `grant_types_supported`                 | `["authorization_code", "refresh_token"]` | Fixed in `build_metadata()`               |
| `token_endpoint_auth_methods_supported` | `["client_secret_post"]`                  | Fixed in `build_metadata()`               |
| `code_challenge_methods_supported`      | `["S256"]`                                | Fixed in `build_metadata()`               |

The `build_metadata()` function constructs the complete `OAuthMetadata` object with proper URL validation through `validate_issuer_url()` and CORS support via `cors_middleware()`. The metadata is served by `MetadataHandler.handle()` at the well-known endpoint.

**Sources:** [src/mcp/server/auth/routes.py149-186](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L149-L186) [src/mcp/server/auth/routes.py23-47](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L23-L47) [src/mcp/server/auth/routes.py49-52](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L49-L52) [src/mcp/server/auth/handlers/metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/metadata.py)

### Dynamic Client Registration

The server supports RFC 7591 dynamic client registration through the `RegistrationHandler.handle()` method:

```
```

Key registration features implemented in `RegistrationHandler.handle()`:

- **Automatic client ID generation**: Uses `uuid4()` for unique client identifiers
- **Client secret generation**: Uses `secrets.token_hex(32)` for 32-byte cryptographically secure random hex string
- **Scope validation**: Ensures requested scopes are within `ClientRegistrationOptions.valid_scopes`
- **Grant type validation**: Only supports `authorization_code` and `refresh_token` grant types
- **Client secret expiry**: Configurable via `ClientRegistrationOptions.client_secret_expiry_seconds`

**Sources:** [src/mcp/server/auth/handlers/register.py34-121](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py#L34-L121) [src/mcp/server/auth/settings.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/settings.py) [src/mcp/server/auth/handlers/register.py51-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py#L51-L85)

### Protected Resource Metadata

The server can also act as a protected resource by exposing RFC 9728 metadata through `create_protected_resource_routes()`:

```
```

This enables automatic discovery by OAuth clients using `_discover_protected_resource()` and supports the separation of authorization servers from protected resources as defined in RFC 9728.

**Sources:** [src/mcp/server/auth/routes.py189-227](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L189-L227) [src/mcp/shared/auth.py134-156](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L134-L156) [src/mcp/server/auth/handlers/metadata.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/metadata.py)

## Security Features

### PKCE Implementation

The SDK implements PKCE (Proof Key for Code Exchange) as defined in RFC 7636 through the `PKCEParameters` class to prevent authorization code interception attacks:

```
```

PKCE parameters use cryptographically secure random generation in `PKCEParameters.generate()`:

- **Code verifier**: 128 characters from `secrets.choice(string.ascii_letters + string.digits + "-._~")`
- **Code challenge**: SHA256 hash of verifier, Base64URL encoded with `rstrip("=")` to remove padding
- **Challenge method**: Always `S256` (SHA256) as specified in OAuth server metadata

**Sources:** [src/mcp/client/auth.py49-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L49-L61) [src/mcp/client/auth.py324-325](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L324-L325) [src/mcp/client/auth.py374](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L374-L374) [src/mcp/client/auth.py56-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L56-L61)

### State Parameter Protection

The OAuth flow includes state parameter validation in `_perform_authorization()` to prevent CSRF attacks:

```
```

The `secrets.compare_digest()` function provides constant-time comparison to prevent timing attacks. The state parameter is included in the authorization URL and validated when the authorization code is returned via the `callback_handler`.

**Sources:** [src/mcp/client/auth.py325](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L325-L325) [src/mcp/client/auth.py349-350](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L349-L350) [src/mcp/client/auth.py347-353](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L347-L353)

### Token Security

Token management includes several security measures implemented across multiple methods:

- **Secure storage**: Tokens are stored through the `TokenStorage` protocol interface via `storage.set_tokens()`
- **Automatic expiry**: Tokens are validated in `is_token_valid()` against wall-clock expiry time from `update_token_expiry()`
- **Scope validation**: `_handle_token_response()` validates returned token scopes against requested scopes
- **Automatic refresh**: `_refresh_token()` and `_handle_refresh_response()` automatically refresh expired tokens when possible
- **Secure transport**: `validate_issuer_url()` ensures all token exchanges occur over HTTPS (with localhost HTTP exception for development)

The scope validation logic in `_handle_token_response()` prevents privilege escalation:

```
```

**Sources:** [src/mcp/client/auth.py398-403](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L398-L403) [src/mcp/client/auth.py120-133](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L120-L133) [src/mcp/server/auth/routes.py34-41](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L34-L41) [src/mcp/client/auth.py388-409](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L388-L409)

### Resource Parameter Support

The SDK implements RFC 8707 resource indicators for enhanced security:

```
```

The resource parameter helps prevent token confusion attacks by explicitly identifying the intended resource server.

**Sources:** [src/mcp/client/auth.py159-177](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L159-L177) [src/mcp/client/auth.py377-379](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L377-L379) [src/mcp/client/auth.py431-433](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L431-L433)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Authentication & Security](#authentication-security.md)
- [MCP Authentication Integration](#mcp-authentication-integration.md)
- [OAuth 2.0 Client Authentication](#oauth-20-client-authentication.md)
- [Core Client Components Architecture](#core-client-components-architecture.md)
- [OAuth Flow Implementation](#oauth-flow-implementation.md)
- [Token Management and Storage](#token-management-and-storage.md)
- [Protected Resource Discovery](#protected-resource-discovery.md)
- [OAuth 2.0 Server Implementation](#oauth-20-server-implementation.md)
- [Server Components Architecture](#server-components-architecture.md)
- [OAuth Metadata Generation](#oauth-metadata-generation.md)
- [Dynamic Client Registration](#dynamic-client-registration.md)
- [Protected Resource Metadata](#protected-resource-metadata.md)
- [Security Features](#security-features.md)
- [PKCE Implementation](#pkce-implementation.md)
- [State Parameter Protection](#state-parameter-protection.md)
- [Token Security](#token-security.md)
- [Resource Parameter Support](#resource-parameter-support.md)
