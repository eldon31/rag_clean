Customizing API Documentation UI | fastapi/fastapi | DeepWiki

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

# Customizing API Documentation UI

Relevant source files

- [docs/de/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/de/docs/how-to/custom-docs-ui-assets.md)
- [docs/en/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/how-to/custom-docs-ui-assets.md)
- [docs/es/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/es/docs/how-to/custom-docs-ui-assets.md)
- [docs/pt/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/pt/docs/how-to/custom-docs-ui-assets.md)
- [docs\_src/custom\_docs\_ui/tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py)
- [fastapi/openapi/docs.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py)
- [tests/test\_local\_docs.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_local_docs.py)
- [tests/test\_tutorial/test\_custom\_docs\_ui/test\_tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py)

This document covers the customization of FastAPI's interactive API documentation interfaces, specifically Swagger UI and ReDoc. It explains how to modify asset loading, customize appearance parameters, and implement self-hosted documentation assets.

For information about the automatic generation of OpenAPI schemas that power these documentation interfaces, see [OpenAPI Schema Generation](fastapi/fastapi/3.1-openapi-schema-generation.md).

## Documentation UI Architecture

FastAPI provides two built-in documentation interfaces that consume OpenAPI schemas to generate interactive API documentation. The system allows flexible customization of both the visual presentation and asset delivery.

```
```

**Documentation UI Generation Flow**

Sources: [fastapi/openapi/docs.py26-158](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L26-L158) [fastapi/openapi/docs.py161-253](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L161-L253)

## Core Documentation Functions

The documentation system centers around three primary functions that generate HTML responses for different documentation interfaces.

### Swagger UI Generation

The `get_swagger_ui_html()` function creates the complete HTML page for Swagger UI documentation. It accepts multiple customization parameters and generates a self-contained HTML response.

```
```

**Swagger UI Parameter Flow**

Sources: [fastapi/openapi/docs.py26-158](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L26-L158) [fastapi/openapi/docs.py8-23](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L8-L23)

### ReDoc Generation

The `get_redoc_html()` function provides an alternative documentation interface with different styling and layout characteristics.

| Parameter           | Type   | Default         | Purpose                 |
| ------------------- | ------ | --------------- | ----------------------- |
| `openapi_url`       | `str`  | Required        | OpenAPI schema endpoint |
| `title`             | `str`  | Required        | HTML page title         |
| `redoc_js_url`      | `str`  | CDN URL         | ReDoc JavaScript bundle |
| `redoc_favicon_url` | `str`  | FastAPI favicon | Page favicon            |
| `with_google_fonts` | `bool` | `True`          | Load Google Fonts CSS   |

Sources: [fastapi/openapi/docs.py161-253](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L161-L253)

## Asset Delivery Strategies

FastAPI supports three primary approaches for delivering documentation assets: default CDN, custom CDN, and self-hosting.

### Default CDN Configuration

By default, FastAPI loads documentation assets from public CDNs:

- Swagger UI JavaScript: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js`
- Swagger UI CSS: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css`
- ReDoc JavaScript: `https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js`

Sources: [fastapi/openapi/docs.py56](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L56-L56) [fastapi/openapi/docs.py66](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L66-L66) [fastapi/openapi/docs.py191](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L191-L191)

### Custom CDN Implementation

To use alternative CDNs, applications must disable default documentation endpoints and create custom path operations.

```
```

**Custom CDN Setup Flow**

Sources: [docs\_src/custom\_docs\_ui/tutorial001.py8](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L8-L8) [docs\_src/custom\_docs\_ui/tutorial001.py11-19](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L11-L19) [docs\_src/custom\_docs\_ui/tutorial001.py27-33](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L27-L33)

### Self-Hosting Static Files

Self-hosting involves serving documentation assets directly from the FastAPI application using `StaticFiles` mounting.

Required static files:

- `swagger-ui-bundle.js`
- `swagger-ui.css`
- `redoc.standalone.js`

Sources: [docs/en/docs/how-to/custom-docs-ui-assets.md94-101](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/how-to/custom-docs-ui-assets.md#L94-L101)

## Swagger UI Configuration Parameters

The `swagger_ui_default_parameters` dictionary defines the base configuration for Swagger UI behavior and appearance.

### Default Configuration

```
```

**Swagger UI Parameter Merging**

Sources: [fastapi/openapi/docs.py17-23](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L17-L23) [fastapi/openapi/docs.py113-115](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L113-L115)

### OAuth2 Integration

OAuth2 authentication requires special handling through the redirect mechanism and initialization parameters.

| Component                               | Function                    | Purpose                             |
| --------------------------------------- | --------------------------- | ----------------------------------- |
| `oauth2_redirect_url`                   | OAuth2 callback handling    | Processes authentication responses  |
| `init_oauth`                            | OAuth2 client configuration | Configures OAuth2 client parameters |
| `get_swagger_ui_oauth2_redirect_html()` | Redirect page generation    | Handles OAuth2 authorization flow   |

Sources: [fastapi/openapi/docs.py75-82](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L75-L82) [fastapi/openapi/docs.py84-90](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L84-L90) [fastapi/openapi/docs.py256-344](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L256-L344)

## Implementation Patterns

### Disabling Default Documentation

To implement custom documentation, applications must first disable the default endpoints by setting them to `None` during FastAPI instantiation.

Sources: [docs\_src/custom\_docs\_ui/tutorial001.py8](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L8-L8)

### Custom Path Operations

Custom documentation requires creating new path operations that call the documentation generation functions with custom parameters.

The standard pattern includes three endpoints:

- Main documentation endpoint (`/docs`)
- Alternative documentation endpoint (`/redoc`)
- OAuth2 redirect endpoint (`/docs/oauth2-redirect`)

Sources: [docs\_src/custom\_docs\_ui/tutorial001.py11-24](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L11-L24) [docs\_src/custom\_docs\_ui/tutorial001.py27-33](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L27-L33)

### Testing Documentation Customization

The test infrastructure validates that custom URLs appear in the generated HTML responses and that OAuth2 redirect functionality operates correctly.

Key test validations:

- Custom asset URLs in HTML content
- OAuth2 redirect JavaScript presence
- API endpoint functionality

Sources: [tests/test\_tutorial/test\_custom\_docs\_ui/test\_tutorial001.py20-42](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py#L20-L42) [tests/test\_local\_docs.py18-32](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_local_docs.py#L18-L32)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Customizing API Documentation UI](#customizing-api-documentation-ui.md)
- [Documentation UI Architecture](#documentation-ui-architecture.md)
- [Core Documentation Functions](#core-documentation-functions.md)
- [Swagger UI Generation](#swagger-ui-generation.md)
- [ReDoc Generation](#redoc-generation.md)
- [Asset Delivery Strategies](#asset-delivery-strategies.md)
- [Default CDN Configuration](#default-cdn-configuration.md)
- [Custom CDN Implementation](#custom-cdn-implementation.md)
- [Self-Hosting Static Files](#self-hosting-static-files.md)
- [Swagger UI Configuration Parameters](#swagger-ui-configuration-parameters.md)
- [Default Configuration](#default-configuration.md)
- [OAuth2 Integration](#oauth2-integration.md)
- [Implementation Patterns](#implementation-patterns.md)
- [Disabling Default Documentation](#disabling-default-documentation.md)
- [Custom Path Operations](#custom-path-operations.md)
- [Testing Documentation Customization](#testing-documentation-customization.md)
