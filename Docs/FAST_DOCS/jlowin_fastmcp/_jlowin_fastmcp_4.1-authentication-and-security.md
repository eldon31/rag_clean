Authentication and Security | jlowin/fastmcp | DeepWiki

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

# Authentication and Security

Relevant source files

- [docs/servers/auth/oauth-proxy.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/servers/auth/oauth-proxy.mdx)
- [src/fastmcp/server/auth/oauth\_proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py)
- [src/fastmcp/server/auth/providers/azure.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/azure.py)
- [src/fastmcp/server/auth/providers/github.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/github.py)
- [src/fastmcp/server/auth/providers/google.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/google.py)
- [src/fastmcp/server/auth/providers/workos.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/workos.py)
- [src/fastmcp/utilities/storage.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/storage.py)
- [tests/server/auth/test\_oauth\_proxy.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/server/auth/test_oauth_proxy.py)

This document covers FastMCP's comprehensive authentication and security system, including OAuth integration, token verification, and security mechanisms. The system enables FastMCP servers to authenticate with traditional OAuth providers (GitHub, Google, Azure, etc.) while maintaining compatibility with MCP's Dynamic Client Registration requirements.

For HTTP server deployment patterns, see [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md). For middleware-based security features like rate limiting and request validation, see [Middleware System](jlowin/fastmcp/4.2-middleware-system.md).

## Architecture Overview

FastMCP's authentication system centers around the **OAuth Proxy** pattern, which bridges the gap between traditional OAuth providers (that require pre-registered applications) and MCP clients (that expect Dynamic Client Registration). The system consists of several key components working together to provide secure, transparent authentication.

### Core Authentication Flow

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py125-231](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L125-L231) [src/fastmcp/server/auth/providers/github.py167-193](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/github.py#L167-L193) [src/fastmcp/server/auth/providers/google.py183-209](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/google.py#L183-L209)

## OAuth Proxy System

The `OAuthProxy` class is the cornerstone of FastMCP's authentication system, implementing a transparent proxy that presents a DCR-compliant interface to MCP clients while using pre-registered credentials with upstream OAuth providers.

### OAuth Proxy Architecture

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py125-371](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L125-L371) [src/fastmcp/server/auth/oauth\_proxy.py464-559](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L464-L559)

### Dynamic Client Registration Implementation

The proxy implements local DCR through the `ProxyDCRClient` class, which validates redirect URIs against configurable patterns while maintaining compatibility with upstream providers that only accept fixed redirect URIs.

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py60-115](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L60-L115) [src/fastmcp/server/auth/oauth\_proxy.py396-459](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L396-L459)

### Authorization Code Exchange

The proxy implements a dual-layer authorization flow that maintains security while bridging DCR requirements with traditional OAuth constraints.

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py464-669](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L464-L669) [src/fastmcp/server/auth/oauth\_proxy.py876-1061](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L876-L1061)

## Token Verification System

FastMCP supports multiple token verification strategies through the `TokenVerifier` base class and provider-specific implementations that handle different token formats and validation mechanisms.

### Token Verifier Architecture

```
```

Sources: [src/fastmcp/server/auth/providers/jwt.py1-200](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/jwt.py#L1-L200) [src/fastmcp/server/auth/providers/github.py62-165](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/github.py#L62-L165) [src/fastmcp/server/auth/providers/google.py64-181](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/google.py#L64-L181)

### Access Token Structure

The `AccessToken` class provides a unified representation of validated tokens across all providers:

```
```

Sources: [src/fastmcp/server/auth/auth.py50-85](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/auth.py#L50-L85) [src/fastmcp/server/auth/providers/github.py144-157](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/github.py#L144-L157) [src/fastmcp/server/auth/providers/google.py152-173](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/google.py#L152-L173)

## Built-in Provider Implementations

FastMCP includes ready-to-use provider implementations for major OAuth services, each handling provider-specific requirements and token formats.

### Provider Class Hierarchy

```
```

Sources: [src/fastmcp/server/auth/providers/github.py167-284](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/github.py#L167-L284) [src/fastmcp/server/auth/providers/google.py183-303](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/google.py#L183-L303) [src/fastmcp/server/auth/providers/azure.py118-266](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/azure.py#L118-L266) [src/fastmcp/server/auth/providers/workos.py128-262](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/providers/workos.py#L128-L262)

## Security Features

FastMCP implements multiple layers of security to protect OAuth flows and ensure secure token handling.

### PKCE (Proof Key for Code Exchange)

The proxy implements dual-layer PKCE protection, maintaining security between client-to-proxy and proxy-to-provider connections:

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py377-391](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L377-L391) [src/fastmcp/server/auth/oauth\_proxy.py481-530](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L481-L530)

### Redirect URI Validation

The `ProxyDCRClient` class implements configurable redirect URI validation to prevent authorization code interception while maintaining DCR compatibility:

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py60-115](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L60-L115) [src/fastmcp/server/auth/redirect\_validation.py1-50](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/redirect_validation.py#L1-L50)

### Token Management and Revocation

The proxy maintains comprehensive token lifecycle management with cleanup and revocation capabilities:

```
```

Sources: [src/fastmcp/server/auth/oauth\_proxy.py775-818](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L775-L818) [src/fastmcp/server/auth/oauth\_proxy.py674-753](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L674-L753)

## Storage and Persistence

FastMCP provides pluggable storage backends for persisting OAuth client registrations and maintaining session state across server restarts.

### Storage Architecture

```
```

Sources: [src/fastmcp/utilities/storage.py16-205](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/storage.py#L16-L205) [src/fastmcp/server/auth/oauth\_proxy.py345-349](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/server/auth/oauth_proxy.py#L345-L349)

The authentication system provides a robust, secure foundation for FastMCP servers while maintaining compatibility with both traditional OAuth providers and MCP's Dynamic Client Registration requirements. The modular design allows for easy extension with new providers and verification methods as needed.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Authentication and Security](#authentication-and-security.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Authentication Flow](#core-authentication-flow.md)
- [OAuth Proxy System](#oauth-proxy-system.md)
- [OAuth Proxy Architecture](#oauth-proxy-architecture.md)
- [Dynamic Client Registration Implementation](#dynamic-client-registration-implementation.md)
- [Authorization Code Exchange](#authorization-code-exchange.md)
- [Token Verification System](#token-verification-system.md)
- [Token Verifier Architecture](#token-verifier-architecture.md)
- [Access Token Structure](#access-token-structure.md)
- [Built-in Provider Implementations](#built-in-provider-implementations.md)
- [Provider Class Hierarchy](#provider-class-hierarchy.md)
- [Security Features](#security-features.md)
- [PKCE (Proof Key for Code Exchange)](#pkce-proof-key-for-code-exchange.md)
- [Redirect URI Validation](#redirect-uri-validation.md)
- [Token Management and Revocation](#token-management-and-revocation.md)
- [Storage and Persistence](#storage-and-persistence.md)
- [Storage Architecture](#storage-architecture.md)
