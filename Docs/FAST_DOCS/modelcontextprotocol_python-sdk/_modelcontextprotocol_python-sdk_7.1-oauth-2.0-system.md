OAuth 2.0 System | modelcontextprotocol/python-sdk | DeepWiki

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

# OAuth 2.0 System

Relevant source files

- [examples/clients/simple-auth-client/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-auth-client/README.md)
- [examples/clients/simple-auth-client/mcp\_simple\_auth\_client/main.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-auth-client/mcp_simple_auth_client/main.py)
- [examples/servers/simple-auth/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-auth/README.md)
- [examples/servers/simple-auth/mcp\_simple\_auth/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-auth/mcp_simple_auth/server.py)
- [src/mcp/client/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py)
- [src/mcp/server/auth/handlers/register.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py)
- [src/mcp/server/auth/routes.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py)
- [src/mcp/shared/auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py)
- [tests/client/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py)
- [tests/shared/test\_auth.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_auth.py)

This document covers the comprehensive OAuth 2.0 authentication and authorization implementation in the MCP Python SDK. The OAuth 2.0 system provides secure authentication for both client and server components, implementing RFC 6749 (OAuth 2.0), RFC 7636 (PKCE), RFC 8414 (Authorization Server Metadata), and RFC 9728 (Protected Resource Metadata).

For information about client transport integration, see [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md). For server-side transport security, see [Transport Security](#5.5.md).

## OAuth 2.0 Architecture Overview

The OAuth 2.0 system consists of client-side authentication components and server-side authorization infrastructure, supporting both acting as OAuth clients and providing OAuth authorization services.

```
```

**Sources:** [src/mcp/client/auth.py179-552](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L179-L552) [src/mcp/shared/auth.py1-156](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L1-L156) [src/mcp/server/auth/routes.py68-187](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L68-L187)

## Client Authentication System

The `OAuthClientProvider` class implements the OAuth 2.0 authorization code flow with PKCE as an httpx authentication provider, enabling automatic token management for MCP clients. The provider sets `requires_response_body = True` to access response bodies for OAuth error handling and token processing.

### OAuthClientProvider Implementation

```
```

**Sources:** [src/mcp/client/auth.py179-206](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L179-L206) [src/mcp/client/auth.py485-551](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L485-L551) [src/mcp/client/auth.py185](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L185-L185)

### PKCE Implementation

The system implements Proof Key for Code Exchange (PKCE) as specified in RFC 7636 to enhance security for OAuth flows.

| Component        | Implementation                                                                                                                 | Purpose                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| `PKCEParameters` | [src/mcp/client/auth.py49-62](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L49-L62) | Generates cryptographically secure code verifier and challenge |
| Code Verifier    | 128-character random string                                                                                                    | Client-side secret for authorization code exchange             |
| Code Challenge   | SHA256 + Base64URL encoding                                                                                                    | Server-verifiable challenge derived from verifier              |
| Challenge Method | S256                                                                                                                           | SHA256-based challenge method (required by RFC)                |

**Sources:** [src/mcp/client/auth.py49-62](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L49-L62) [tests/client/test\_auth.py82-107](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L82-L107)

### Token Storage Protocol

The `TokenStorage` protocol enables persistent token management across client sessions:

```
```

**Sources:** [src/mcp/client/auth.py64-82](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L64-L82) [tests/client/test\_auth.py17-35](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L17-L35)

## OAuth Flow Implementation

The complete OAuth 2.0 authorization code flow with PKCE is implemented as an asynchronous generator that integrates with httpx's authentication system.

### Authorization Code Flow Sequence

```
```

**Sources:** [src/mcp/client/auth.py485-551](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L485-L551) [tests/client/test\_auth.py616-714](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L616-L714)

### OAuth Discovery and Fallback

The client implements comprehensive discovery mechanisms with fallback support for legacy servers. The `_get_discovery_urls()` method generates an ordered list of discovery URLs:

| Discovery Type                    | Endpoint Pattern                                | RFC Reference | Implementation                   |
| --------------------------------- | ----------------------------------------------- | ------------- | -------------------------------- |
| Protected Resource                | `/.well-known/oauth-protected-resource`         | RFC 9728      | `_discover_protected_resource()` |
| Authorization Server (Path-aware) | `/.well-known/oauth-authorization-server{path}` | RFC 8414      | `_get_discovery_urls()`          |
| Authorization Server (Root)       | `/.well-known/oauth-authorization-server`       | RFC 8414      | Fallback in ordered list         |
| OpenID Configuration (Path-aware) | `/.well-known/openid-configuration{path}`       | RFC 8414 §5   | Path-aware discovery             |
| OpenID Configuration (Legacy)     | `{server}/.well-known/openid-configuration`     | OIDC 1.0      | Legacy fallback                  |

The discovery process includes protocol version header injection (`MCP_PROTOCOL_VERSION`) and WWW-Authenticate header parsing for enhanced resource metadata discovery.

**Sources:** [src/mcp/client/auth.py254-279](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L254-L279) [src/mcp/client/auth.py231-240](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L231-L240) [src/mcp/client/auth.py474-475](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L474-L475) [tests/client/test\_auth.py252-261](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L252-L261)

## Server Authorization System

The server-side OAuth implementation provides a complete authorization server that can issue tokens for MCP resources.

### Authorization Server Routes

```
```

**Sources:** [src/mcp/server/auth/routes.py68-147](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L68-L147) [src/mcp/server/auth/routes.py189-227](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L189-L227)

### Client Registration Handler

The `RegistrationHandler` implements RFC 7591 Dynamic Client Registration:

| Validation               | Implementation                                    | Error Response            |
| ------------------------ | ------------------------------------------------- | ------------------------- |
| Metadata Validation      | Pydantic `OAuthClientMetadata`                    | `invalid_client_metadata` |
| Scope Validation         | `ClientRegistrationOptions.valid_scopes`          | `invalid_client_metadata` |
| Grant Type Validation    | Must be `["authorization_code", "refresh_token"]` | `invalid_client_metadata` |
| Client Secret Generation | `secrets.token_hex(32)` for non-public clients    | N/A                       |

**Sources:** [src/mcp/server/auth/handlers/register.py34-120](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/register.py#L34-L120)

## Token Management

The OAuth system provides comprehensive token lifecycle management including validation, refresh, and expiration handling.

### OAuthToken Model

```
```

**Sources:** [src/mcp/shared/auth.py6-25](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L6-L25) [src/mcp/client/auth.py120-142](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L120-L142)

### Token Refresh Flow and Resource Parameter Support

The client automatically refreshes expired tokens using stored refresh tokens and includes RFC 8707 resource parameter support:

| Condition                         | Action              | Fallback                         | Resource Parameter                              |
| --------------------------------- | ------------------- | -------------------------------- | ----------------------------------------------- |
| Token Valid                       | Use existing token  | N/A                              | N/A                                             |
| Token Expired + Refresh Available | Automatic refresh   | Full re-authorization on failure | Included if PRM exists or protocol ≥ 2025-06-18 |
| Token Expired + No Refresh        | Full OAuth flow     | N/A                              | Included in authorization/token requests        |
| Refresh Fails                     | Clear stored tokens | Full OAuth flow                  | N/A                                             |

The `should_include_resource_param()` method determines when to include the resource parameter based on:

- Presence of Protected Resource Metadata (always include)
- MCP-Protocol-Version ≥ 2025-06-18 (include for newer protocols)

**Sources:** [src/mcp/client/auth.py411-462](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L411-L462) [src/mcp/client/auth.py159-176](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L159-L176) [src/mcp/client/auth.py431-433](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L431-L433) [tests/client/test\_auth.py443-465](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L443-L465) [tests/client/test\_auth.py471-525](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L471-L525)

## Discovery and Metadata Systems

The OAuth implementation supports comprehensive metadata discovery for both authorization servers and protected resources.

### Authorization Server Metadata

The `OAuthMetadata` model implements RFC 8414 Authorization Server Metadata:

```
```

**Sources:** [src/mcp/shared/auth.py105-132](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L105-L132) [src/mcp/server/auth/routes.py149-186](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L149-L186)

### Protected Resource Metadata

RFC 9728 Protected Resource Metadata enables resource servers to advertise their authorization requirements:

| Field                      | Purpose                    | MCP Implementation                              | Default Value  |
| -------------------------- | -------------------------- | ----------------------------------------------- | -------------- |
| `resource`                 | Resource server identifier | MCP server URL                                  | Server URL     |
| `authorization_servers`    | List of trusted AS URLs    | AS that can issue tokens for this resource      | Required field |
| `scopes_supported`         | Available scopes           | MCP-specific scopes (tools, resources, prompts) | Optional       |
| `bearer_methods_supported` | Token presentation methods | `["header"]` (Authorization header only)        | `["header"]`   |
| `resource_name`            | Human-readable name        | Optional display name                           | Optional       |
| `resource_documentation`   | Documentation URL          | API documentation link                          | Optional       |

**Sources:** [src/mcp/shared/auth.py134-156](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/shared/auth.py#L134-L156) [src/mcp/server/auth/routes.py189-227](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L189-L227)

## Security Features

The OAuth 2.0 implementation includes comprehensive security measures following current best practices.

### HTTPS and Security Validation

```
```

**Sources:** [src/mcp/server/auth/routes.py23-47](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/routes.py#L23-L47) [src/mcp/client/auth.py49-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L49-L61) [src/mcp/client/auth.py347-353](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L347-L353)

### WWW-Authenticate Header Support

The client implements RFC 9728 WWW-Authenticate header parsing for enhanced discovery:

| Header Format  | Extraction Pattern        | Example                                                                                   |
| -------------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| Quoted URL     | `resource_metadata="URL"` | `Bearer resource_metadata="https://api.example.com/.well-known/oauth-protected-resource"` |
| Unquoted URL   | `resource_metadata=URL`   | `Bearer resource_metadata=https://api.example.com/.well-known/oauth-protected-resource`   |
| Complex Header | Multiple parameters       | `Bearer realm="api", resource_metadata="URL", error="insufficient_scope"`                 |

**Sources:** [src/mcp/client/auth.py207-229](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/auth.py#L207-L229) [tests/client/test\_auth.py844-906](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_auth.py#L844-L906)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [OAuth 2.0 System](#oauth-20-system.md)
- [OAuth 2.0 Architecture Overview](#oauth-20-architecture-overview.md)
- [Client Authentication System](#client-authentication-system.md)
- [OAuthClientProvider Implementation](#oauthclientprovider-implementation.md)
- [PKCE Implementation](#pkce-implementation.md)
- [Token Storage Protocol](#token-storage-protocol.md)
- [OAuth Flow Implementation](#oauth-flow-implementation.md)
- [Authorization Code Flow Sequence](#authorization-code-flow-sequence.md)
- [OAuth Discovery and Fallback](#oauth-discovery-and-fallback.md)
- [Server Authorization System](#server-authorization-system.md)
- [Authorization Server Routes](#authorization-server-routes.md)
- [Client Registration Handler](#client-registration-handler.md)
- [Token Management](#token-management.md)
- [OAuthToken Model](#oauthtoken-model.md)
- [Token Refresh Flow and Resource Parameter Support](#token-refresh-flow-and-resource-parameter-support.md)
- [Discovery and Metadata Systems](#discovery-and-metadata-systems.md)
- [Authorization Server Metadata](#authorization-server-metadata.md)
- [Protected Resource Metadata](#protected-resource-metadata.md)
- [Security Features](#security-features.md)
- [HTTPS and Security Validation](#https-and-security-validation.md)
- [WWW-Authenticate Header Support](#www-authenticate-header-support.md)
