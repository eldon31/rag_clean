Application and Routing System | fastapi/fastapi | DeepWiki

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

# Application and Routing System

Relevant source files

- [docs/en/docs/advanced/additional-responses.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/additional-responses.md)
- [docs/en/docs/advanced/behind-a-proxy.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/behind-a-proxy.md)
- [docs/en/docs/advanced/custom-response.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/custom-response.md)
- [docs/en/docs/advanced/path-operation-advanced-configuration.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/path-operation-advanced-configuration.md)
- [docs/en/docs/advanced/response-directly.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/response-directly.md)
- [docs/en/docs/advanced/settings.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md)
- [docs/en/docs/deployment/https.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/deployment/https.md)
- [docs/en/docs/release-notes.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/release-notes.md)
- [docs\_src/additional\_responses/tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/additional_responses/tutorial001.py)
- [docs\_src/behind\_a\_proxy/tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/behind_a_proxy/tutorial001_01.py)
- [docs\_src/custom\_response/tutorial001b.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial001b.py)
- [docs\_src/custom\_response/tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial009c.py)
- [docs\_src/custom\_response/tutorial010.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial010.py)
- [fastapi/\_\_init\_\_.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py)
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
- [tests/test\_tutorial/test\_behind\_a\_proxy/test\_tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_behind_a_proxy/test_tutorial001_01.py)
- [tests/test\_tutorial/test\_custom\_response/test\_tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_response/test_tutorial009c.py)

This document covers FastAPI's application and routing system, including the core `FastAPI` application class, route organization through `APIRouter`, individual route handling via `APIRoute` and `APIWebSocketRoute`, and the request processing pipeline. For information about dependency injection mechanics, see [Dependency Injection](fastapi/fastapi/2.2-dependency-injection.md). For details about parameter validation and handling, see [Parameter Validation and Handling](fastapi/fastapi/2.3-parameter-validation-and-handling.md).

## FastAPI Application Class

The `FastAPI` class serves as the main application entry point, inheriting from Starlette's `Starlette` class while adding FastAPI-specific functionality including automatic API documentation, dependency injection, and enhanced routing capabilities.

### Application Structure

```
```

The `FastAPI` constructor accepts extensive configuration options for OpenAPI documentation, CORS, middleware, and routing behavior. Key configuration includes `title`, `description`, `version` for API metadata, `docs_url` and `redoc_url` for documentation endpoints, and `default_response_class` for response handling.

Sources: [fastapi/applications.py48-640](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/applications.py#L48-L640) [fastapi/\_\_init\_\_.py7](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py#L7-L7)

### Route Definition Methods

The `FastAPI` class provides HTTP method decorators that create `APIRoute` instances:

```
```

Each decorator method creates an `APIRoute` instance with the specified HTTP method, path, and endpoint function, then adds it to the application's router.

Sources: [fastapi/applications.py697-1007](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/applications.py#L697-L1007)

## APIRouter System

The `APIRouter` class enables modular route organization by grouping related path operations that can be included in the main application or other routers.

### Router Hierarchy

```
```

The `APIRouter` constructor accepts parameters including `prefix` for path prefixing, `tags` for OpenAPI organization, `dependencies` for shared dependencies, and `default_response_class` for response handling.

Sources: [fastapi/routing.py596-621](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L596-L621) [fastapi/routing.py623-740](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L623-L740)

### Router Registration

The `include_router` method merges an `APIRouter` into the application by copying its routes and applying prefix, tag, and dependency transformations:

| Parameter      | Purpose                           | Example                       |
| -------------- | --------------------------------- | ----------------------------- |
| `router`       | APIRouter instance to include     | `user_router`                 |
| `prefix`       | Path prefix for all routes        | `"/api/v1"`                   |
| `tags`         | OpenAPI tags to apply             | `["users"]`                   |
| `dependencies` | Dependencies to add to all routes | `[Depends(get_current_user)]` |

Sources: [fastapi/applications.py1009-1106](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/applications.py#L1009-L1106)

## Route Classes

### APIRoute

The `APIRoute` class represents individual HTTP endpoints, handling path compilation, dependency analysis, and request processing setup.

```
```

The `APIRoute` constructor analyzes the endpoint function signature using `get_dependant()` to extract parameter information and build the dependency tree.

Sources: [fastapi/routing.py429-593](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L429-L593)

### APIWebSocketRoute

The `APIWebSocketRoute` class handles WebSocket connections with similar dependency resolution but different connection lifecycle:

```
```

Sources: [fastapi/routing.py389-427](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L389-L427)

## Request Processing Pipeline

### Request Handler Creation

The `get_request_handler` function creates the actual ASGI application that processes HTTP requests:

```
```

Sources: [fastapi/routing.py218-358](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L218-L358)

### Request Flow

The generated request handler follows this processing sequence:

```
```

Sources: [fastapi/routing.py241-356](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L241-L356) [fastapi/dependencies/utils.py572-689](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L572-L689)

## Route Registration Process

### Route Creation and Registration

When routes are defined using decorators, the following process occurs:

```
```

The route registration process includes path compilation using Starlette's `compile_path`, dependency analysis via `get_dependant`, and OpenAPI schema preparation.

Sources: [fastapi/routing.py430-571](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L430-L571) [fastapi/dependencies/utils.py265-314](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L265-L314)

### Dependency Tree Construction

The `get_dependant` function recursively builds a dependency tree by analyzing function signatures:

| Component       | Purpose                  | Location                  |
| --------------- | ------------------------ | ------------------------- |
| `path_params`   | URL path parameters      | `dependant.path_params`   |
| `query_params`  | Query string parameters  | `dependant.query_params`  |
| `header_params` | HTTP header parameters   | `dependant.header_params` |
| `cookie_params` | Cookie parameters        | `dependant.cookie_params` |
| `body_params`   | Request body parameters  | `dependant.body_params`   |
| `dependencies`  | Sub-dependency functions | `dependant.dependencies`  |

Sources: [fastapi/dependencies/utils.py265-314](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L265-L314) [fastapi/dependencies/models.py15-37](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L15-L37)

## OpenAPI Integration

### Schema Generation

The routing system automatically generates OpenAPI schemas through the `get_openapi_path` function:

```
```

Each `APIRoute` contributes to the OpenAPI schema by providing operation metadata, parameter schemas, request/response body schemas, and security definitions.

Sources: [fastapi/openapi/utils.py254-439](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/utils.py#L254-L439)

### Route Matching

The route matching process uses Starlette's routing system with FastAPI enhancements:

```
```

The `matches` method on `APIRoute` and `APIWebSocketRoute` determines if a route should handle a specific request based on path pattern and HTTP method.

Sources: [fastapi/routing.py589-593](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L589-L593) [fastapi/routing.py422-426](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L422-L426)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Application and Routing System](#application-and-routing-system.md)
- [FastAPI Application Class](#fastapi-application-class.md)
- [Application Structure](#application-structure.md)
- [Route Definition Methods](#route-definition-methods.md)
- [APIRouter System](#apirouter-system.md)
- [Router Hierarchy](#router-hierarchy.md)
- [Router Registration](#router-registration.md)
- [Route Classes](#route-classes.md)
- [APIRoute](#apiroute.md)
- [APIWebSocketRoute](#apiwebsocketroute.md)
- [Request Processing Pipeline](#request-processing-pipeline.md)
- [Request Handler Creation](#request-handler-creation.md)
- [Request Flow](#request-flow.md)
- [Route Registration Process](#route-registration-process.md)
- [Route Creation and Registration](#route-creation-and-registration.md)
- [Dependency Tree Construction](#dependency-tree-construction.md)
- [OpenAPI Integration](#openapi-integration.md)
- [Schema Generation](#schema-generation.md)
- [Route Matching](#route-matching.md)
