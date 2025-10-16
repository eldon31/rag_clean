Response Handling | fastapi/fastapi | DeepWiki

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

# Response Handling

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

This document covers how FastAPI processes and serializes responses from path operation functions into HTTP responses. It explains the default response behavior, serialization pipeline, response model validation, and custom response classes. For information about request handling and parameter validation, see [Parameter Validation and Handling](fastapi/fastapi/2.3-parameter-validation-and-handling.md). For error handling mechanisms, see [Error Handling](fastapi/fastapi/2.7-error-handling.md).

## Default Response Behavior

FastAPI automatically converts path operation return values into HTTP responses using `JSONResponse` as the default response class. When a path operation function returns data, FastAPI applies the following default behavior:

- **Automatic JSON Conversion**: Return values are serialized to JSON using the `jsonable_encoder`
- **Content-Type Headers**: HTTP headers are automatically set to `application/json`
- **Status Codes**: Default status code is 200, unless explicitly specified
- **Response Model Validation**: If a `response_model` is declared, the return value is validated against it

The default response class can be overridden at the application level or per-route using the `response_class` parameter.

Sources: [fastapi/applications.py354-373](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/applications.py#L354-L373) [fastapi/routing.py454-456](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L454-L456)

## Response Serialization Pipeline

### Response Content Preparation

```
```

The `_prepare_response_content` function handles the initial content preparation by recursively processing different data types and applying serialization rules based on the `exclude_unset`, `exclude_defaults`, and `exclude_none` parameters.

Sources: [fastapi/routing.py80-124](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L80-L124)

### JSON Encoding Process

```
```

The `jsonable_encoder` provides comprehensive type conversion with support for custom encoders, Pydantic models, dataclasses, and various Python built-in types including datetime, UUID, Enum, and Path objects.

Sources: [fastapi/encoders.py102-343](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/encoders.py#L102-L343)

## Response Model Validation

### Response Field Creation

When a path operation declares a `response_model`, FastAPI creates response fields during route initialization:

```
```

The cloned field ensures that Pydantic submodel inheritance doesn't bypass validation, preventing security issues where a subclass with additional fields might be returned directly.

Sources: [fastapi/routing.py507-530](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L507-L530)

### Response Validation Process

```
```

The `serialize_response` function validates response content against the declared response model, ensuring type safety and proper serialization. It handles both Pydantic v1 and v2 compatibility through the `hasattr(field, "serialize")` check.

Sources: [fastapi/routing.py144-203](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L144-L203)

## Custom Response Classes

### Response Class Hierarchy

FastAPI supports various response classes that inherit from Starlette's `Response`:

| Response Class      | Media Type         | Use Case                              |
| ------------------- | ------------------ | ------------------------------------- |
| `JSONResponse`      | `application/json` | Default, automatic JSON serialization |
| `ORJSONResponse`    | `application/json` | High-performance JSON with `orjson`   |
| `HTMLResponse`      | `text/html`        | HTML content                          |
| `PlainTextResponse` | `text/plain`       | Plain text responses                  |
| `RedirectResponse`  | N/A                | HTTP redirects                        |
| `FileResponse`      | Based on file      | File downloads                        |
| `StreamingResponse` | Custom             | Streaming content                     |

### Custom Response Integration

```
```

When a path operation returns a `Response` instance directly, FastAPI bypasses the serialization pipeline. Otherwise, it uses the declared `response_class` to wrap the serialized content.

Sources: [fastapi/routing.py307-342](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L307-L342) [docs/en/docs/advanced/custom-response.md1-86](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/custom-response.md#L1-L86)

## Response Generation Flow

### Complete Request-Response Cycle

```
```

### Response Handler Implementation

The `get_request_handler` function orchestrates the complete response generation process:

1. **Endpoint Execution**: Calls the path operation function via `run_endpoint_function`
2. **Response Type Check**: Determines if return value is already a `Response` instance
3. **Content Serialization**: Applies `serialize_response` with response model validation
4. **Response Construction**: Creates response instance with proper status codes and headers
5. **Background Tasks**: Attaches any background tasks to the response
6. **Body Validation**: Ensures response body is allowed for the status code

Sources: [fastapi/routing.py241-356](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L241-L356)

### Status Code and Header Management

```
```

FastAPI automatically manages status codes based on the hierarchy of explicit parameters, route defaults, and response class defaults. It also validates that response bodies are appropriate for the status code (e.g., no body for 204 No Content).

Sources: [fastapi/routing.py317-342](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/routing.py#L317-L342) [fastapi/utils.py42-56](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/utils.py#L42-L56)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Response Handling](#response-handling.md)
- [Default Response Behavior](#default-response-behavior.md)
- [Response Serialization Pipeline](#response-serialization-pipeline.md)
- [Response Content Preparation](#response-content-preparation.md)
- [JSON Encoding Process](#json-encoding-process.md)
- [Response Model Validation](#response-model-validation.md)
- [Response Field Creation](#response-field-creation.md)
- [Response Validation Process](#response-validation-process.md)
- [Custom Response Classes](#custom-response-classes.md)
- [Response Class Hierarchy](#response-class-hierarchy.md)
- [Custom Response Integration](#custom-response-integration.md)
- [Response Generation Flow](#response-generation-flow.md)
- [Complete Request-Response Cycle](#complete-request-response-cycle.md)
- [Response Handler Implementation](#response-handler-implementation.md)
- [Status Code and Header Management](#status-code-and-header-management.md)
