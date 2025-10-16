Client Authentication | jlowin/fastmcp | DeepWiki

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

# Client Authentication

Relevant source files

- [docs/integrations/auth0.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/integrations/auth0.mdx)
- [src/fastmcp/client/auth/oauth.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py)
- [src/fastmcp/server/auth/oidc\_proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oidc_proxy.py)
- [src/fastmcp/server/auth/providers/auth0.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/auth0.py)
- [tests/client/auth/test\_oauth\_token\_expiry.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/auth/test_oauth_token_expiry.py)
- [tests/server/auth/providers/test\_auth0.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/providers/test_auth0.py)
- [tests/server/auth/test\_oidc\_proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/test_oidc_proxy.py)

This page covers client-side authentication in FastMCP, focusing on OAuth flows, token storage, browser-based authentication, and integration with identity providers. This documentation explains how FastMCP clients authenticate with protected servers using industry-standard OAuth 2.0 and OpenID Connect protocols.

For server-side authentication configuration and identity providers, see [Authentication and Security](jlowin/fastmcp/4.1-authentication-and-security.md). For transport-specific authentication mechanisms, see [Transport Mechanisms](jlowin/fastmcp/3.1-transport-mechanisms.md).

## Overview

FastMCP client authentication is built around OAuth 2.0 with OpenID Connect support, providing secure token-based authentication for MCP clients connecting to protected servers. The authentication system handles the complete OAuth flow, from initial authorization to token refresh and storage.

### Client Authentication Architecture

```
```

Sources: [src/fastmcp/client/auth/oauth.py242-428](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L242-L428) [src/fastmcp/client/oauth\_callback.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/oauth_callback.py) [src/fastmcp/utilities/storage.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/storage.py)

## OAuth Flow Implementation

The `OAuth` class implements the complete OAuth 2.0 authorization code flow with PKCE support, handling dynamic client registration, browser-based authorization, and token management.

### OAuth Provider Class Structure

```
```

Sources: [src/fastmcp/client/auth/oauth.py242-311](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L242-L311) [src/fastmcp/client/auth/oauth.py322-374](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L322-L374) [src/fastmcp/client/auth/oauth.py376-427](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L376-L427)

### Authorization Flow Process

The OAuth authorization flow follows these steps:

| Step | Method               | Description                          | Error Handling                          |
| ---- | -------------------- | ------------------------------------ | --------------------------------------- |
| 1    | `redirect_handler()` | Pre-flight validation, opens browser | Detects stale client\_id (400 response) |
| 2    | `callback_handler()` | Starts local callback server         | 5-minute timeout with graceful shutdown |
| 3    | Token Exchange       | Exchanges auth code for tokens       | Automatic retry on client errors        |
| 4    | Token Storage        | Saves tokens with absolute expiry    | Validates token format and expiry       |

Sources: [src/fastmcp/client/auth/oauth.py322-341](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L322-L341) [src/fastmcp/client/auth/oauth.py343-374](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L343-L374)

## Token Storage and Management

FastMCP implements sophisticated token storage with automatic expiry handling, server isolation, and format validation through the `FileTokenStorage` class.

### Token Storage Architecture

```
```

Sources: [src/fastmcp/client/auth/oauth.py59-196](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L59-L196) [src/fastmcp/client/auth/oauth.py44-52](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L44-L52)

### Token Expiry Handling

The token storage system uses absolute timestamps rather than relative `expires_in` values to ensure accurate expiry checking across application restarts:

```
```

Sources: [src/fastmcp/client/auth/oauth.py132-147](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L132-L147) [src/fastmcp/client/auth/oauth.py96-130](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L96-L130) [tests/client/auth/test\_oauth\_token\_expiry.py13-164](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/client/auth/test_oauth_token_expiry.py#L13-L164)

## Browser-Based Authentication

FastMCP uses a browser-based OAuth flow that opens the user's default browser for authorization and runs a temporary local server to receive the OAuth callback.

### Browser Flow Implementation

```
```

Sources: [src/fastmcp/client/auth/oauth.py322-341](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L322-L341) [src/fastmcp/client/auth/oauth.py343-374](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L343-L374) [src/fastmcp/client/auth/oauth.py395-427](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L395-L427)

### Callback Server Configuration

The OAuth callback server uses dynamic port allocation and graceful shutdown:

| Configuration | Default                            | Description                              |
| ------------- | ---------------------------------- | ---------------------------------------- |
| Port          | `find_available_port()`            | Dynamically allocated available port     |
| Timeout       | 300 seconds                        | Maximum wait time for user authorization |
| Redirect URI  | `http://localhost:{port}/callback` | OAuth callback endpoint                  |
| Server Type   | `uvicorn.Server`                   | ASGI server for handling callbacks       |

Sources: [src/fastmcp/client/auth/oauth.py275-276](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L275-L276) [src/fastmcp/utilities/http.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/http.py) [src/fastmcp/client/oauth\_callback.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/oauth_callback.py)

## Identity Provider Integration

FastMCP supports multiple identity providers through standardized OAuth 2.0 and OpenID Connect protocols. The authentication system is provider-agnostic, requiring only standard OAuth endpoints.

### Provider Configuration

```
```

Sources: [src/fastmcp/server/auth/oidc\_proxy.py27-169](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oidc_proxy.py#L27-L169) [src/fastmcp/server/auth/providers/auth0.py36-175](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/auth0.py#L36-L175)

### Authentication Pre-flight Check

Before initiating OAuth flows, FastMCP can check if authentication is required:

```
```

This function tests the endpoint and returns `True` if authentication appears required based on HTTP status codes (401, 403) or WWW-Authenticate headers.

Sources: [src/fastmcp/client/auth/oauth.py212-240](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L212-L240)

## Configuration and Usage

### Basic OAuth Configuration

```
```

### Client Integration

```
```

### Token Storage Locations

The `FileTokenStorage` class stores tokens in server-specific files:

| File Type   | Path Pattern                         | Purpose                           |
| ----------- | ------------------------------------ | --------------------------------- |
| Tokens      | `{base_url}_tokens.json`             | Access/refresh tokens with expiry |
| Client Info | `{base_url}_client_info.json`        | OAuth client registration data    |
| Cache Dir   | `~/.fastmcp/oauth-mcp-client-cache/` | Default storage location          |

Sources: [src/fastmcp/client/auth/oauth.py250-311](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L250-L311) [src/fastmcp/client/auth/oauth.py55-86](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L55-L86)

### Error Handling and Recovery

The OAuth implementation includes automatic error recovery:

- **Stale Credentials**: Detects invalid client\_id and clears cache for retry
- **Token Expiry**: Automatically refreshes expired tokens
- **Network Errors**: Graceful handling of connection issues
- **Timeout Handling**: 5-minute timeout with user-friendly messages

Sources: [src/fastmcp/client/auth/oauth.py376-427](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L376-L427) [src/fastmcp/client/auth/oauth.py38-41](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/auth/oauth.py#L38-L41)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Authentication](#client-authentication.md)
- [Overview](#overview.md)
- [Client Authentication Architecture](#client-authentication-architecture.md)
- [OAuth Flow Implementation](#oauth-flow-implementation.md)
- [OAuth Provider Class Structure](#oauth-provider-class-structure.md)
- [Authorization Flow Process](#authorization-flow-process.md)
- [Token Storage and Management](#token-storage-and-management.md)
- [Token Storage Architecture](#token-storage-architecture.md)
- [Token Expiry Handling](#token-expiry-handling.md)
- [Browser-Based Authentication](#browser-based-authentication.md)
- [Browser Flow Implementation](#browser-flow-implementation.md)
- [Callback Server Configuration](#callback-server-configuration.md)
- [Identity Provider Integration](#identity-provider-integration.md)
- [Provider Configuration](#provider-configuration.md)
- [Authentication Pre-flight Check](#authentication-pre-flight-check.md)
- [Configuration and Usage](#configuration-and-usage.md)
- [Basic OAuth Configuration](#basic-oauth-configuration.md)
- [Client Integration](#client-integration.md)
- [Token Storage Locations](#token-storage-locations.md)
- [Error Handling and Recovery](#error-handling-and-recovery.md)
