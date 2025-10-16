Error Handling | fastapi/fastapi | DeepWiki

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

# Error Handling

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
- [fastapi/exception\_handlers.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exception_handlers.py)
- [fastapi/exceptions.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py)
- [tests/test\_multi\_body\_errors.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_multi_body_errors.py)
- [tests/test\_multi\_query\_errors.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_multi_query_errors.py)
- [tests/test\_put\_no\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_put_no_body.py)
- [tests/test\_tutorial/test\_handling\_errors/test\_tutorial003.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_handling_errors/test_tutorial003.py)
- [tests/test\_tutorial/test\_handling\_errors/test\_tutorial004.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_handling_errors/test_tutorial004.py)
- [tests/test\_tutorial/test\_handling\_errors/test\_tutorial005.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_handling_errors/test_tutorial005.py)
- [tests/test\_tutorial/test\_handling\_errors/test\_tutorial006.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_handling_errors/test_tutorial006.py)
- [tests/test\_ws\_router.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_ws_router.py)

FastAPI implements a comprehensive exception hierarchy and handler system that manages errors from request validation, application logic, and WebSocket connections. The system centers around specific exception classes and handler functions that process different error types while maintaining automatic OpenAPI documentation integration.

For information about parameter validation that triggers errors, see [Parameter Validation and Handling](fastapi/fastapi/2.3-parameter-validation-and-handling.md). For broader request processing context, see [Application and Routing System](fastapi/fastapi/2.1-application-and-routing-system.md).

## Exception Class Hierarchy

FastAPI defines a complete exception hierarchy that extends Starlette's base exceptions while adding framework-specific error handling capabilities.

### Core Exception Classes

```
```

**FastAPI Exception Class Hierarchy with Code Entity Names** Sources: [fastapi/exceptions.py9-177](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L9-L177)

The `HTTPException` class [fastapi/exceptions.py9-66](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L9-L66) extends Starlette's version to accept any JSON-serializable data in the `detail` field, while `WebSocketException` [fastapi/exceptions.py68-137](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L68-L137) provides WebSocket-specific error handling with RFC 6455 compliant close codes.

### Validation Exception Architecture

```
```

**Validation Exception Structure with Actual Class Methods** Sources: [fastapi/exceptions.py149-177](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L149-L177)

The `ValidationException` base class [fastapi/exceptions.py149-155](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L149-L155) provides the `errors()` method interface, while `RequestValidationError` [fastapi/exceptions.py157-161](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L157-L161) and `ResponseValidationError` [fastapi/exceptions.py167-177](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exceptions.py#L167-L177) store the invalid request/response body for debugging purposes.

## Exception Handlers

FastAPI provides default exception handlers for framework exceptions and enables registration of custom handlers for application-specific error processing.

### Default Exception Handler Functions

```
```

**Default Exception Handler Function Signatures** Sources: [fastapi/exception\_handlers.py11-35](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exception_handlers.py#L11-L35)

The `http_exception_handler` [fastapi/exception\_handlers.py11-18](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exception_handlers.py#L11-L18) uses `is_body_allowed_for_status_code()` to determine response format, while `request_validation_exception_handler` [fastapi/exception\_handlers.py20-27](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exception_handlers.py#L20-L27) returns 422 status with `jsonable_encoder(exc.errors())`. WebSocket validation errors [fastapi/exception\_handlers.py29-35](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exception_handlers.py#L29-L35) close the connection with `WS_1008_POLICY_VIOLATION`.

### Custom Exception Handler Registration

```
```

**Exception Handler Registration with Actual Import Paths** Sources: [docs/en/docs/tutorial/handling-errors.md82-102](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L82-L102) [docs/en/docs/tutorial/handling-errors.md249-256](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L249-L256)

Custom handlers are registered with `@app.exception_handler()` and can import default handlers from `fastapi.exception_handlers` for reuse. Registering handlers for Starlette exceptions catches both FastAPI and Starlette internal exceptions.

### WebSocket Exception Handling

```
```

**WebSocket Exception Handling Flow with Status Codes** Sources: [tests/test\_ws\_router.py210-272](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_ws_router.py#L210-L272) [fastapi/exception\_handlers.py29-35](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/exception_handlers.py#L29-L35)

WebSocket validation errors trigger `WS_1008_POLICY_VIOLATION` close codes, while custom WebSocket exception handlers [tests/test\_ws\_router.py257-272](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_ws_router.py#L257-L272) can define custom close codes and reasons. WebSocket middleware can catch dependency errors [tests/test\_ws\_router.py236-255](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_ws_router.py#L236-L255)

## Error Response Integration

Error handling integrates with FastAPI's broader request processing pipeline and OpenAPI documentation generation.

### Error Flow in Request Processing Pipeline

```
```

**Error Handling Integration with Request Processing** Sources: [docs/en/docs/tutorial/handling-errors.md1-256](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L1-L256) [docs/en/docs/tutorial/dependencies/index.md32-42](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/index.md#L32-L42)

Errors can occur at multiple stages of request processing: during parameter validation, dependency injection, or within path operation functions. Each error type is handled by appropriate handlers that can be customized or extended while maintaining the overall request processing flow.

### Exception Handler Inheritance and Reuse

```
```

**Exception Handler Reuse Pattern** Sources: [docs/en/docs/tutorial/handling-errors.md249-256](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L249-L256)

FastAPI provides importable default exception handlers from `fastapi.exception_handlers` that can be reused within custom exception handling logic. This allows developers to add custom processing (like logging) while maintaining standard error response formats.

## OpenAPI Documentation Integration

Error responses declared in exception handlers and path operations are automatically included in the generated OpenAPI schema, providing comprehensive API documentation that includes both success and error scenarios.

```
```

**Error Documentation Generation Flow** Sources: [docs/en/docs/tutorial/handling-errors.md1-256](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L1-L256) [docs/en/docs/tutorial/query-params-str-validations.md104-109](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L104-L109)

The framework automatically generates OpenAPI documentation for validation errors (422 responses) and incorporates custom error responses defined in path operations. This ensures that API consumers have complete information about both successful and error response formats.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Error Handling](#error-handling.md)
- [Exception Class Hierarchy](#exception-class-hierarchy.md)
- [Core Exception Classes](#core-exception-classes.md)
- [Validation Exception Architecture](#validation-exception-architecture.md)
- [Exception Handlers](#exception-handlers.md)
- [Default Exception Handler Functions](#default-exception-handler-functions.md)
- [Custom Exception Handler Registration](#custom-exception-handler-registration.md)
- [WebSocket Exception Handling](#websocket-exception-handling.md)
- [Error Response Integration](#error-response-integration.md)
- [Error Flow in Request Processing Pipeline](#error-flow-in-request-processing-pipeline.md)
- [Exception Handler Inheritance and Reuse](#exception-handler-inheritance-and-reuse.md)
- [OpenAPI Documentation Integration](#openapi-documentation-integration.md)
