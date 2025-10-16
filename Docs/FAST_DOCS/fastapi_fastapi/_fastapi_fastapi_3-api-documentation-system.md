API Documentation System | fastapi/fastapi | DeepWiki

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

# API Documentation System

Relevant source files

- [docs/de/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/de/docs/how-to/custom-docs-ui-assets.md)
- [docs/en/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/how-to/custom-docs-ui-assets.md)
- [docs/es/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/es/docs/how-to/custom-docs-ui-assets.md)
- [docs/pt/docs/how-to/custom-docs-ui-assets.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/pt/docs/how-to/custom-docs-ui-assets.md)
- [docs\_src/custom\_docs\_ui/tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py)
- [fastapi/openapi/docs.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py)
- [tests/test\_local\_docs.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_local_docs.py)
- [tests/test\_tutorial/test\_custom\_docs\_ui/test\_tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py)

## Purpose and Scope

The API Documentation System generates and serves interactive API documentation interfaces for FastAPI applications. This system specifically handles the creation of Swagger UI and ReDoc interfaces that allow users to explore, test, and interact with API endpoints directly in the browser.

This document covers the automatic generation of documentation HTML pages, asset management (JavaScript/CSS files), and customization options for the documentation UI. For information about OpenAPI schema generation that powers these interfaces, see [OpenAPI Schema Generation](fastapi/fastapi/3.1-openapi-schema-generation.md). For broader documentation infrastructure including MkDocs and multi-language support, see [Documentation System](fastapi/fastapi/6.1-documentation-system.md).

## System Overview

The API Documentation System operates as a bridge between FastAPI's OpenAPI schema generation and web-based documentation interfaces. It provides HTML generation functions that create fully functional documentation pages served directly by FastAPI applications.

```
```

**Documentation UI Generation Flow** The system generates HTML responses containing JavaScript that initializes documentation interfaces using OpenAPI specifications.

Sources: [fastapi/openapi/docs.py1-345](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L1-L345)

## Core Components

The documentation system centers around three primary HTML generation functions that create complete documentation interfaces with embedded JavaScript and CSS.

```
```

**Core Function Architecture** Each documentation interface is generated by a dedicated function that assembles HTML with proper asset references and configuration.

### Primary Generation Functions

The `get_swagger_ui_html()` function creates the main interactive documentation interface. It accepts parameters for customizing the OpenAPI URL, title, asset URLs, and Swagger UI configuration through the `swagger_ui_parameters` parameter.

Sources: [fastapi/openapi/docs.py26-158](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L26-L158)

The `get_redoc_html()` function generates an alternative documentation interface using ReDoc. It provides a different visual style and interaction model compared to Swagger UI, with options for Google Fonts integration and custom styling.

Sources: [fastapi/openapi/docs.py161-253](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L161-L253)

The `get_swagger_ui_oauth2_redirect_html()` function handles OAuth2 authentication flow redirects specifically for Swagger UI. This enables authentication testing directly within the documentation interface.

Sources: [fastapi/openapi/docs.py256-344](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L256-L344)

### Default Configuration

The system provides sensible defaults through `swagger_ui_default_parameters` which includes DOM targeting, layout configuration, and feature toggles for the Swagger UI interface.

| Parameter              | Default Value   | Purpose                            |
| ---------------------- | --------------- | ---------------------------------- |
| `dom_id`               | `"#swagger-ui"` | Target DOM element for UI mounting |
| `layout`               | `"BaseLayout"`  | Swagger UI layout configuration    |
| `deepLinking`          | `True`          | Enable URL-based navigation        |
| `showExtensions`       | `True`          | Display OpenAPI extensions         |
| `showCommonExtensions` | `True`          | Display common vendor extensions   |

Sources: [fastapi/openapi/docs.py8-23](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L8-L23)

## Asset Management

The documentation system supports three asset delivery modes: CDN-based (default), custom CDN, and self-hosted static files. Each mode provides different trade-offs between simplicity, control, and offline functionality.

### CDN-Based Assets (Default)

By default, the system loads assets from jsdelivr CDN with these default URLs:

- Swagger UI JavaScript: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js`
- Swagger UI CSS: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css`
- ReDoc JavaScript: `https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js`
- Favicon: `https://fastapi.tiangolo.com/img/favicon.png`

Sources: [fastapi/openapi/docs.py47-74](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L47-L74) [fastapi/openapi/docs.py182-199](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L182-L199)

### Custom CDN Configuration

Applications can specify alternative CDN URLs by passing custom `swagger_js_url`, `swagger_css_url`, and `redoc_js_url` parameters to the generation functions. This supports scenarios where default CDNs are blocked or alternative sources are preferred.

Sources: [docs/en/docs/how-to/custom-docs-ui-assets.md9-58](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/how-to/custom-docs-ui-assets.md#L9-L58) [docs\_src/custom\_docs\_ui/tutorial001.py11-33](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L11-L33)

### Self-Hosted Static Assets

For offline or airgapped deployments, applications can serve documentation assets locally by:

1. Downloading required JavaScript and CSS files
2. Serving them through FastAPI's `StaticFiles` mounting
3. Configuring documentation functions to use local URLs

The required files are:

- `swagger-ui-bundle.js` and `swagger-ui.css` for Swagger UI
- `redoc.standalone.js` for ReDoc

Sources: [docs/en/docs/how-to/custom-docs-ui-assets.md59-186](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/how-to/custom-docs-ui-assets.md#L59-L186)

## Integration with FastAPI Applications

FastAPI applications automatically configure documentation endpoints unless explicitly disabled. The system integrates through several application-level configurations and automatic endpoint registration.

### Automatic Documentation Endpoints

FastAPI applications automatically create documentation endpoints at `/docs` (Swagger UI) and `/redoc` (ReDoc) unless disabled by setting `docs_url=None` or `redoc_url=None` in the FastAPI constructor.

The automatic endpoints use these application attributes:

- `app.openapi_url` - URL for OpenAPI JSON schema
- `app.title` - Application title for documentation pages
- `app.swagger_ui_oauth2_redirect_url` - OAuth2 redirect handler URL

### Custom Documentation Endpoints

Applications requiring asset customization must disable automatic endpoints and create custom path operations that call the HTML generation functions with appropriate parameters.

```
```

Sources: [docs\_src/custom\_docs\_ui/tutorial001.py8-39](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_docs_ui/tutorial001.py#L8-L39)

### OAuth2 Integration

The system supports OAuth2 authentication flows through the redirect handler endpoint. Applications using OAuth2 security schemes can enable authentication testing directly within Swagger UI by configuring the `oauth2_redirect_url` and `init_oauth` parameters.

The OAuth2 redirect handler processes authentication callbacks and returns tokens to the Swagger UI interface, enabling full authentication testing within the documentation.

Sources: [fastapi/openapi/docs.py75-90](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L75-L90) [fastapi/openapi/docs.py256-344](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/docs.py#L256-L344)

## Testing and Validation

The documentation system includes comprehensive testing to ensure proper HTML generation, asset URL inclusion, and configuration parameter handling.

Test coverage includes:

- Default CDN URL inclusion in generated HTML
- Custom URL parameter handling
- OAuth2 redirect functionality
- Google Fonts configuration for ReDoc
- Static file serving integration

Sources: [tests/test\_local\_docs.py1-68](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_local_docs.py#L1-L68) [tests/test\_tutorial/test\_custom\_docs\_ui/test\_tutorial001.py1-43](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py#L1-L43)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [API Documentation System](#api-documentation-system.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Overview](#system-overview.md)
- [Core Components](#core-components.md)
- [Primary Generation Functions](#primary-generation-functions.md)
- [Default Configuration](#default-configuration.md)
- [Asset Management](#asset-management.md)
- [CDN-Based Assets (Default)](#cdn-based-assets-default.md)
- [Custom CDN Configuration](#custom-cdn-configuration.md)
- [Self-Hosted Static Assets](#self-hosted-static-assets.md)
- [Integration with FastAPI Applications](#integration-with-fastapi-applications.md)
- [Automatic Documentation Endpoints](#automatic-documentation-endpoints.md)
- [Custom Documentation Endpoints](#custom-documentation-endpoints.md)
- [OAuth2 Integration](#oauth2-integration.md)
- [Testing and Validation](#testing-and-validation.md)
