Security Components | fastapi/fastapi | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[fastapi/fastapi](https://github.com/fastapi/fastapi "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 5 September 2025 ([3e2dbf](https://github.com/fastapi/fastapi/commits/3e2dbf91))

- [FastAPI Overview](fastapi/fastapi/1-fastapi-overview.md)
- [Core Architecture](fastapi/fastapi/2-core-architecture.md)
- [Application and Routing System](fastapi/fastapi/2.1-application-and-routing-system.md)
- [Dependency Injection](fastapi/fastapi/2.2-dependency-injection.md)
- [Parameter Validation and Handling](fastapi/fastapi/2.3-parameter-validation-and-handling.md)
- [Response Handling](fastapi/fastapi/2.4-response-handling.md)
- [Security Components](fastapi/fastapi/2.5-security-components.md)
- [Settings Management](fastapi/fastapi/2.6-settings-management.md)
- [Error Handling](fastapi/fastapi/2.7-error-handling.md)
- [API Documentation System](fastapi/fastapi/3-api-documentation-system.md)
- [OpenAPI Schema Generation](fastapi/fastapi/3.1-openapi-schema-generation.md)
- [Customizing API Documentation UI](fastapi/fastapi/3.2-customizing-api-documentation-ui.md)
- [Advanced Features](fastapi/fastapi/4-advanced-features.md)
- [Asynchronous Support](fastapi/fastapi/4.1-asynchronous-support.md)
- [Database Integration](fastapi/fastapi/4.2-database-integration.md)
- [Background Tasks](fastapi/fastapi/4.3-background-tasks.md)
- [Deployment and Production Considerations](fastapi/fastapi/4.4-deployment-and-production-considerations.md)
- [Testing Infrastructure](fastapi/fastapi/5-testing-infrastructure.md)
- [Test Framework and Tools](fastapi/fastapi/5.1-test-framework-and-tools.md)
- [Code Quality and Pre-commit](fastapi/fastapi/5.2-code-quality-and-pre-commit.md)
- [Project Infrastructure](fastapi/fastapi/6-project-infrastructure.md)
- [Documentation System](fastapi/fastapi/6.1-documentation-system.md)
- [CI/CD Pipeline](fastapi/fastapi/6.2-cicd-pipeline.md)
- [Development Workflow](fastapi/fastapi/6.3-development-workflow.md)
- [Community Ecosystem](fastapi/fastapi/7-community-ecosystem.md)
- [Contributors and Experts Management](fastapi/fastapi/7.1-contributors-and-experts-management.md)
- [Translation Management](fastapi/fastapi/7.2-translation-management.md)
- [External Resources and Sponsorship](fastapi/fastapi/7.3-external-resources-and-sponsorship.md)
- [Community Automation](fastapi/fastapi/7.4-community-automation.md)

Menu

# Security Components

Relevant source files

- [docs/en/docs/tutorial/background-tasks.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md)
- [docs/en/docs/tutorial/extra-data-types.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/extra-data-types.md)
- [docs/en/docs/tutorial/handling-errors.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md)
- [docs/en/docs/tutorial/security/first-steps.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/first-steps.md)
- [docs/en/docs/tutorial/security/oauth2-jwt.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/oauth2-jwt.md)
- [docs/en/docs/tutorial/security/simple-oauth2.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/simple-oauth2.md)
- [docs/en/docs/tutorial/sql-databases.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md)
- [docs/ja/docs/tutorial/security/oauth2-jwt.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/ja/docs/tutorial/security/oauth2-jwt.md)
- [docs/pt/docs/tutorial/cookie-param-models.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/pt/docs/tutorial/cookie-param-models.md)
- [docs/zh/docs/tutorial/sql-databases.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/zh/docs/tutorial/sql-databases.md)
- [fastapi/applications.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/applications.py)
- [fastapi/dependencies/models.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py)
- [fastapi/dependencies/utils.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py)
- [fastapi/encoders.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/encoders.py)
- [fastapi/openapi/models.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/models.py)
- [fastapi/openapi/utils.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/utils.py)
- [fastapi/param\_functions.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/param_functions.py)
- [fastapi/params.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/params.py)
- [fastapi/routing.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py)
- [fastapi/security/api\_key.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/api_key.py)
- [fastapi/security/http.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/http.py)
- [fastapi/security/oauth2.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/oauth2.py)
- [fastapi/security/open\_id\_connect\_url.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/open_id_connect_url.py)
- [fastapi/utils.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/utils.py)
- [tests/test\_datetime\_custom\_encoder.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_datetime_custom_encoder.py)
- [tests/test\_jsonable\_encoder.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_jsonable_encoder.py)

This document covers FastAPI's security infrastructure, including authentication schemes (OAuth2, HTTP Basic/Bearer, API Key, OpenID Connect), security dependencies, and permission scopes. For broader API documentation concepts, see [API Documentation System](fastapi/fastapi/3-api-documentation-system.md). For error handling in security contexts, see [Error Handling](fastapi/fastapi/2.7-error-handling.md).

## Overview

FastAPI provides a comprehensive security system with multiple authentication schemes integrated into the dependency injection framework. The security components handle authentication, authorization, token validation, and scope-based permissions through a collection of base classes, concrete implementations, and utilities that automatically integrate with OpenAPI documentation generation.

## Security Component Architecture

```
```

Sources: [fastapi/security/base.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/base.py) [fastapi/security/oauth2.py308-441](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/oauth2.py#L308-L441) [fastapi/security/http.py69-340](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/http.py#L69-L340) [fastapi/security/api\_key.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/api_key.py) [fastapi/dependencies/models.py8-12](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L8-L12) [fastapi/openapi/utils.py78-92](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/utils.py#L78-L92)

## Base Security Classes

### SecurityBase

The `SecurityBase` class serves as the foundation for all security schemes in FastAPI. It provides the basic interface that all authentication mechanisms inherit from and ensures consistent integration with the dependency injection system.

Sources: [fastapi/security/base.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/base.py)

### SecurityRequirement

The `SecurityRequirement` dataclass represents security requirements for operations, containing a reference to the security scheme and any required scopes:

| Field             | Type                      | Description                  |
| ----------------- | ------------------------- | ---------------------------- |
| `security_scheme` | `SecurityBase`            | The security scheme instance |
| `scopes`          | `Optional[Sequence[str]]` | Required permission scopes   |

Sources: [fastapi/dependencies/models.py8-12](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L8-L12)

## Authentication Schemes

### OAuth2 Components

#### OAuth2

The `OAuth2` class implements OAuth2 authentication flows. It accepts flow configurations and integrates with OpenAPI documentation generation.

```
```

Key initialization parameters:

- `flows` - OAuth2 flow definitions (`OAuthFlowsModel`)
- `scheme_name` - Security scheme name for OpenAPI
- `description` - Security scheme description
- `auto_error` - Whether to automatically raise errors for missing auth

Sources: [fastapi/security/oauth2.py308-441](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/oauth2.py#L308-L441)

#### OAuth2PasswordRequestForm

The `OAuth2PasswordRequestForm` class handles login form data according to OAuth2 password flow specifications:

| Field           | Type  | Required | Description            |
| --------------- | ----- | -------- | ---------------------- |
| `username`      | `str` | Yes      | User identifier        |
| `password`      | `str` | Yes      | User password          |
| `scope`         | `str` | No       | Space-separated scopes |
| `grant_type`    | `str` | No       | OAuth2 grant type      |
| `client_id`     | `str` | No       | OAuth2 client ID       |
| `client_secret` | `str` | No       | OAuth2 client secret   |

The form data is automatically parsed from request form fields and made available as a dependency.

Sources: [fastapi/security/oauth2.py16-149](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/oauth2.py#L16-L149)

### HTTP Authentication Components

#### HTTPBasic

The `HTTPBasic` class implements HTTP Basic authentication, extracting and validating Base64-encoded credentials from the `Authorization` header.

```
```

Returns `HTTPBasicCredentials` containing `username` and `password` fields.

Sources: [fastapi/security/http.py97-217](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/http.py#L97-L217)

#### HTTPBearer

The `HTTPBearer` class implements HTTP Bearer token authentication, extracting tokens from the `Authorization` header.

Returns `HTTPAuthorizationCredentials` containing:

- `scheme` - The authorization scheme (e.g., "Bearer")
- `credentials` - The token value

Sources: [fastapi/security/http.py220-340](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/http.py#L220-L340)

### API Key Authentication

FastAPI provides three API key authentication classes for different token locations:

| Class          | Token Location  | Usage                   |
| -------------- | --------------- | ----------------------- |
| `APIKeyQuery`  | Query parameter | `?api_key=token`        |
| `APIKeyHeader` | HTTP header     | `X-API-Key: token`      |
| `APIKeyCookie` | HTTP cookie     | `Cookie: api_key=token` |

All API key classes inherit from `APIKeyBase` and return the extracted key value as a string.

Sources: [fastapi/security/api\_key.py23-237](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/api_key.py#L23-L237)

### OpenID Connect

The `OpenIdConnect` class implements OpenID Connect authentication with a configurable OpenID Connect URL.

Key parameter:

- `openIdConnectUrl` - The OpenID Connect discovery endpoint URL

Sources: [fastapi/security/open\_id\_connect\_url.py11-77](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/open_id_connect_url.py#L11-L77)

## Security Dependency Integration

### Dependency Resolution Flow

```
```

The dependency system processes security components through several key functions:

1. **`get_sub_dependant()`** - Creates `SecurityRequirement` objects from `params.Security` annotations
2. **`solve_dependencies()`** - Resolves security dependencies and populates `SecurityScopes`
3. **Security scheme `__call__`** - Executes authentication logic during request processing

Sources: [fastapi/dependencies/utils.py142-171](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L142-L171) [fastapi/routing.py292-298](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L292-L298)

### SecurityScopes Integration

The `SecurityScopes` class aggregates all security scopes required by a request's dependency tree. It is automatically injected when security dependencies are present:

```
```

Key attributes:

- `scopes` - List of all required scope strings
- `scope_str` - Space-separated scope string for WWW-Authenticate headers

Sources: [fastapi/security/oauth2.py57](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/security/oauth2.py#L57-L57) [fastapi/dependencies/utils.py685-687](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L685-L687)

## OpenAPI Security Documentation

### Security Schema Generation

FastAPI automatically generates OpenAPI security schemas through the `get_openapi_security_definitions()` function:

```
```

The function processes security requirements to generate:

- **Security Definitions**: OpenAPI security scheme objects
- **Operation Security**: Per-operation security requirements with scopes

Sources: [fastapi/openapi/utils.py78-92](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/utils.py#L78-L92)

### Security Schema Integration

Security schemes are integrated into the OpenAPI specification through several key areas:

| OpenAPI Section                    | Content                             | Source                             |
| ---------------------------------- | ----------------------------------- | ---------------------------------- |
| `components.securitySchemes`       | Security scheme definitions         | Security scheme `model` attributes |
| `paths.{path}.{method}.security`   | Per-operation security requirements | `SecurityRequirement.scopes`       |
| `paths.{path}.{method}.parameters` | Security parameters (API keys)      | Parameter extraction logic         |

The integration ensures that interactive documentation (Swagger UI, ReDoc) displays proper authentication interfaces and security requirements.

Sources: [fastapi/openapi/utils.py282-288](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/utils.py#L282-L288) [fastapi/openapi/utils.py534-537](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/utils.py#L534-L537)

## Token Validation Pipeline

```
```

The token validation pipeline processes authentication through multiple stages:

1. **Token Extraction**: `OAuth2PasswordBearer` extracts Bearer token from Authorization header
2. **Token Validation**: Decode and verify JWT signature and expiration
3. **Scope Extraction**: Parse scopes from token payload
4. **User Resolution**: Look up user details from token subject
5. **Scope Authorization**: Validate token scopes against required scopes via `SecurityScopes`
6. **User Status**: Verify user account is active and permitted

Sources: [docs/en/docs/tutorial/security/oauth2-jwt.md158-166](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/oauth2-jwt.md#L158-L166) [docs/en/docs/advanced/security/oauth2-scopes.md155-192](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/security/oauth2-scopes.md#L155-L192)

## Integration with Dependency Injection

Security components integrate seamlessly with FastAPI's dependency injection system through several mechanisms:

| Component                   | Integration Method   | Purpose                          |
| --------------------------- | -------------------- | -------------------------------- |
| `OAuth2PasswordBearer`      | `Depends()`          | Token extraction and validation  |
| `OAuth2PasswordRequestForm` | `Depends()`          | Login form parsing               |
| `Security()`                | Dependency decorator | Scope-aware authorization        |
| `SecurityScopes`            | Dependency parameter | Scope aggregation and validation |

```
```

The dependency system automatically:

- Injects `SecurityScopes` with aggregated scope requirements
- Resolves `OAuth2PasswordBearer` to extract and return tokens
- Validates dependency chains for proper security configuration
- Documents security requirements in OpenAPI schema

Sources: [docs/en/docs/advanced/security/oauth2-scopes.md194-234](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/security/oauth2-scopes.md#L194-L234) [fastapi/\_\_init\_\_.py20](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py#L20-L20)

## OpenAPI Security Documentation

FastAPI automatically generates OpenAPI security documentation from security components:

```
```

The security documentation includes:

- OAuth2 flow definitions and token URLs
- Available scopes with descriptions
- Security requirements for each endpoint
- Interactive authentication forms in documentation UI

Sources: [docs/en/docs/tutorial/security/first-steps.md177-185](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/first-steps.md#L177-L185) [docs/en/docs/advanced/security/oauth2-scopes.md76-83](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/security/oauth2-scopes.md#L76-L83)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Security Components](#security-components.md)
- [Overview](#overview.md)
- [Security Component Architecture](#security-component-architecture.md)
- [Base Security Classes](#base-security-classes.md)
- [SecurityBase](#securitybase.md)
- [SecurityRequirement](#securityrequirement.md)
- [Authentication Schemes](#authentication-schemes.md)
- [OAuth2 Components](#oauth2-components.md)
- [OAuth2](#oauth2.md)
- [OAuth2PasswordRequestForm](#oauth2passwordrequestform.md)
- [HTTP Authentication Components](#http-authentication-components.md)
- [HTTPBasic](#httpbasic.md)
- [HTTPBearer](#httpbearer.md)
- [API Key Authentication](#api-key-authentication.md)
- [OpenID Connect](#openid-connect.md)
- [Security Dependency Integration](#security-dependency-integration.md)
- [Dependency Resolution Flow](#dependency-resolution-flow.md)
- [SecurityScopes Integration](#securityscopes-integration.md)
- [OpenAPI Security Documentation](#openapi-security-documentation.md)
- [Security Schema Generation](#security-schema-generation.md)
- [Security Schema Integration](#security-schema-integration.md)
- [Token Validation Pipeline](#token-validation-pipeline.md)
- [Integration with Dependency Injection](#integration-with-dependency-injection.md)
- [OpenAPI Security Documentation](#openapi-security-documentation-1.md)
