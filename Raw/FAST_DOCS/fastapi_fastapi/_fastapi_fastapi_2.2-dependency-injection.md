Dependency Injection | fastapi/fastapi | DeepWiki

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

# Dependency Injection

Relevant source files

- [docs/en/docs/alternatives.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/alternatives.md)
- [docs/en/docs/tutorial/body.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/body.md)
- [docs/en/docs/tutorial/dependencies/classes-as-dependencies.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md)
- [docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md)
- [docs/en/docs/tutorial/dependencies/index.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/index.md)
- [docs/en/docs/tutorial/dependencies/sub-dependencies.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/sub-dependencies.md)
- [docs/en/docs/tutorial/path-params-numeric-validations.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/path-params-numeric-validations.md)
- [docs/en/docs/tutorial/query-params-str-validations.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md)
- [fastapi/applications.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/applications.py)
- [fastapi/dependencies/models.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py)
- [fastapi/dependencies/utils.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py)
- [fastapi/encoders.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/encoders.py)
- [fastapi/openapi/constants.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/constants.py)
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
- [tests/test\_get\_request\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_get_request_body.py)
- [tests/test\_jsonable\_encoder.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_jsonable_encoder.py)

This document covers FastAPI's dependency injection system, which provides automatic resolution and injection of dependencies into path operation functions. The system analyzes function signatures to identify dependencies, validates parameters, and manages the lifecycle of dependency instances including caching and cleanup.

For information about parameter validation and handling, see [Parameter Validation and Handling](fastapi/fastapi/2.3-parameter-validation-and-handling.md). For security-specific dependency injection, see [Security Components](fastapi/fastapi/2.5-security-components.md).

## System Architecture

FastAPI's dependency injection system consists of three main components: dependency analysis, dependency resolution, and lifecycle management. The system automatically discovers dependencies through function signature inspection and resolves them recursively during request processing.

### Dependency Injection Architecture

```
```

Sources: [fastapi/routing.py292-299](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L292-L299) [fastapi/dependencies/utils.py572-695](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L572-L695) [fastapi/dependencies/models.py15-37](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L15-L37)

## Core Components

### Dependant Model

The `Dependant` dataclass represents the dependency structure of a function, containing categorized parameters and sub-dependencies. Each dependant tracks parameter types, security requirements, and caching behavior.

| Field                   | Type                        | Purpose                             |
| ----------------------- | --------------------------- | ----------------------------------- |
| `path_params`           | `List[ModelField]`          | Path parameter definitions          |
| `query_params`          | `List[ModelField]`          | Query parameter definitions         |
| `header_params`         | `List[ModelField]`          | Header parameter definitions        |
| `cookie_params`         | `List[ModelField]`          | Cookie parameter definitions        |
| `body_params`           | `List[ModelField]`          | Request body parameter definitions  |
| `dependencies`          | `List[Dependant]`           | Nested dependency structures        |
| `security_requirements` | `List[SecurityRequirement]` | Security-related dependencies       |
| `call`                  | `Optional[Callable]`        | The actual function to call         |
| `use_cache`             | `bool`                      | Whether to cache dependency results |

Sources: [fastapi/dependencies/models.py15-37](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L15-L37)

### Depends Mechanism

The `Depends` class marks function parameters as dependencies, triggering automatic resolution by the dependency injection system.

```
```

The `dependency` parameter specifies the callable to invoke, while `use_cache` controls whether results should be cached for the request duration.

Sources: [fastapi/params.py1-774](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/params.py#L1-L774)

## Dependency Analysis Process

### Function Signature Analysis

The `get_dependant` function analyzes function signatures to extract dependency information, categorizing parameters by their types and annotations.

```
```

Sources: [fastapi/dependencies/utils.py265-314](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L265-L314) [fastapi/dependencies/utils.py348-511](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L348-L511)

### Parameter Classification

The `analyze_param` function classifies function parameters into dependency types based on annotations and default values:

- **Explicit Dependencies**: Parameters with `Depends()` annotations
- **Request Objects**: `Request`, `WebSocket`, `Response`, `BackgroundTasks` types
- **Path Parameters**: Parameters matching path template variables
- **Query Parameters**: Scalar types without special annotations
- **Body Parameters**: Complex types or explicit `Body()` annotations
- **Header/Cookie Parameters**: Parameters with `Header()` or `Cookie()` annotations

Sources: [fastapi/dependencies/utils.py348-511](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L348-L511) [fastapi/dependencies/utils.py317-338](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L317-L338)

## Dependency Resolution

### Resolution Algorithm

The `solve_dependencies` function recursively resolves dependencies using a depth-first approach with caching and lifecycle management.

```
```

Sources: [fastapi/dependencies/utils.py572-695](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L572-L695)

### SolvedDependency Result

The dependency resolution process returns a `SolvedDependency` object containing all resolved values and metadata:

| Field              | Type              | Purpose                            |
| ------------------ | ----------------- | ---------------------------------- |
| `values`           | `Dict[str, Any]`  | Resolved dependency values         |
| `errors`           | `List[Any]`       | Validation errors encountered      |
| `background_tasks` | `BackgroundTasks` | Background task manager            |
| `response`         | `Response`        | Response object for headers/status |
| `dependency_cache` | `Dict`            | Cache of resolved dependencies     |

Sources: [fastapi/dependencies/utils.py563-570](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L563-L570)

## Advanced Features

### Dependency Caching

Dependencies are cached by default using a cache key derived from the function and security scopes. Caching prevents redundant computations when the same dependency is used multiple times in a request.

```
```

Cache behavior is controlled by the `use_cache` parameter in `Depends()` and can be disabled for dependencies that should be called multiple times.

Sources: [fastapi/dependencies/models.py36-37](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L36-L37) [fastapi/dependencies/utils.py631-644](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L631-L644)

### Generator Dependencies

Generator dependencies support resource management with automatic cleanup using context managers. The system distinguishes between sync and async generators:

- **Sync Generators**: Wrapped with `contextmanager_in_threadpool`
- **Async Generators**: Used directly as async context managers

Sources: [fastapi/dependencies/utils.py553-560](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L553-L560) [fastapi/dependencies/utils.py633-636](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L633-L636)

### Security Dependencies

Security dependencies integrate with FastAPI's security system through `SecurityRequirement` objects, which specify security schemes and required scopes.

Sources: [fastapi/dependencies/models.py9-11](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/models.py#L9-L11) [fastapi/dependencies/utils.py150-171](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L150-L171)

## Integration with Routing

### Route Handler Integration

The routing system integrates dependency injection through the `get_request_handler` function, which creates request handlers that automatically resolve dependencies.

```
```

The route analysis phase extracts dependency information and creates optimized structures for runtime resolution.

Sources: [fastapi/routing.py555-561](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L555-L561) [fastapi/routing.py292-299](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L292-L299) [fastapi/routing.py218-358](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L218-L358)

### Dependency Overrides

The system supports dependency overrides through the `dependency_overrides_provider`, allowing replacement of dependencies during testing or runtime configuration.

Sources: [fastapi/dependencies/utils.py599-613](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/dependencies/utils.py#L599-L613)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Dependency Injection](#dependency-injection.md)
- [System Architecture](#system-architecture.md)
- [Dependency Injection Architecture](#dependency-injection-architecture.md)
- [Core Components](#core-components.md)
- [Dependant Model](#dependant-model.md)
- [Depends Mechanism](#depends-mechanism.md)
- [Dependency Analysis Process](#dependency-analysis-process.md)
- [Function Signature Analysis](#function-signature-analysis.md)
- [Parameter Classification](#parameter-classification.md)
- [Dependency Resolution](#dependency-resolution.md)
- [Resolution Algorithm](#resolution-algorithm.md)
- [SolvedDependency Result](#solveddependency-result.md)
- [Advanced Features](#advanced-features.md)
- [Dependency Caching](#dependency-caching.md)
- [Generator Dependencies](#generator-dependencies.md)
- [Security Dependencies](#security-dependencies.md)
- [Integration with Routing](#integration-with-routing.md)
- [Route Handler Integration](#route-handler-integration.md)
- [Dependency Overrides](#dependency-overrides.md)
