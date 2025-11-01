Parameter Validation and Handling | fastapi/fastapi | DeepWiki

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

# Parameter Validation and Handling

Relevant source files

- [docs/en/docs/advanced/additional-responses.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/additional-responses.md)
- [docs/en/docs/advanced/behind-a-proxy.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/behind-a-proxy.md)
- [docs/en/docs/advanced/custom-response.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/custom-response.md)
- [docs/en/docs/advanced/path-operation-advanced-configuration.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/path-operation-advanced-configuration.md)
- [docs/en/docs/advanced/response-directly.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/response-directly.md)
- [docs/en/docs/advanced/settings.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md)
- [docs/en/docs/alternatives.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/alternatives.md)
- [docs/en/docs/deployment/https.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/deployment/https.md)
- [docs/en/docs/release-notes.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/release-notes.md)
- [docs/en/docs/tutorial/body.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/body.md)
- [docs/en/docs/tutorial/dependencies/classes-as-dependencies.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md)
- [docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md)
- [docs/en/docs/tutorial/dependencies/index.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/index.md)
- [docs/en/docs/tutorial/dependencies/sub-dependencies.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/dependencies/sub-dependencies.md)
- [docs/en/docs/tutorial/path-params-numeric-validations.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/path-params-numeric-validations.md)
- [docs/en/docs/tutorial/query-params-str-validations.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md)
- [docs/en/docs/tutorial/response-status-code.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/response-status-code.md)
- [docs\_src/additional\_responses/tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/additional_responses/tutorial001.py)
- [docs\_src/behind\_a\_proxy/tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/behind_a_proxy/tutorial001_01.py)
- [docs\_src/custom\_response/tutorial001b.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial001b.py)
- [docs\_src/custom\_response/tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial009c.py)
- [docs\_src/custom\_response/tutorial010.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial010.py)
- [fastapi/\_\_init\_\_.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py)
- [fastapi/openapi/constants.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/openapi/constants.py)
- [tests/\_\_init\_\_.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/__init__.py)
- [tests/main.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/main.py)
- [tests/test\_application.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_application.py)
- [tests/test\_get\_request\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_get_request_body.py)
- [tests/test\_path.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_path.py)
- [tests/test\_query.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_query.py)
- [tests/test\_tutorial/test\_behind\_a\_proxy/test\_tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_behind_a_proxy/test_tutorial001_01.py)
- [tests/test\_tutorial/test\_custom\_response/test\_tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_response/test_tutorial009c.py)

This document covers FastAPI's comprehensive parameter validation and handling system, which automatically validates, converts, and documents request parameters including query parameters, path parameters, request bodies, form data, files, headers, and cookies. For information about dependency injection and parameter sharing, see [Dependency Injection](fastapi/fastapi/2.2-dependency-injection.md). For details about response handling and serialization, see [Response Handling](fastapi/fastapi/2.4-response-handling.md).

## Core Parameter Types

FastAPI provides specialized functions for declaring and validating different types of request parameters. Each parameter type has its own dedicated function that handles validation, type conversion, and OpenAPI documentation generation.

### Parameter Declaration Functions

The main parameter declaration functions are exported from the root FastAPI module:

- `Query()` - Query string parameters
- `Path()` - URL path parameters
- `Body()` - Request body content
- `Form()` - HTML form data
- `File()` - File uploads
- `Header()` - HTTP headers
- `Cookie()` - HTTP cookies

Sources: [fastapi/\_\_init\_\_.py12-20](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py#L12-L20)

### Parameter Validation Flow

```
```

Sources: [docs/en/docs/tutorial/query-params-str-validations.md1-493](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L1-L493) [docs/en/docs/tutorial/path-params-numeric-validations.md1-165](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/path-params-numeric-validations.md#L1-L165)

## Query Parameter Validation

Query parameters are declared using the `Query()` function with the `Annotated` type hint syntax. The system supports string validation, numeric constraints, and custom validation functions.

### String Validation Constraints

Query parameters support various string validation rules:

- `min_length` - Minimum string length
- `max_length` - Maximum string length
- `pattern` - Regular expression pattern matching
- `alias` - Alternative parameter name for the URL

```
```

Sources: [docs/en/docs/tutorial/query-params-str-validations.md88-97](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L88-L97) [docs/en/docs/tutorial/query-params-str-validations.md188-222](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L188-L222)

### List and Multiple Value Handling

The `Query()` function supports receiving multiple values for the same parameter name, returning them as a Python `list`:

```
```

Sources: [docs/en/docs/tutorial/query-params-str-validations.md273-304](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L273-L304)

## Path Parameter Validation

Path parameters use the `Path()` function and support the same validation features as query parameters, plus numeric constraints for integer and float values.

### Numeric Validation Constraints

Path parameters support numeric validation rules:

- `gt` - Greater than
- `ge` - Greater than or equal
- `lt` - Less than
- `le` - Less than or equal

```
```

Sources: [docs/en/docs/tutorial/path-params-numeric-validations.md104-132](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/path-params-numeric-validations.md#L104-L132)

## Request Body Validation

Request body validation primarily uses Pydantic models, which provide comprehensive validation, type conversion, and documentation generation.

### Pydantic Model Integration

FastAPI automatically converts JSON request bodies to Pydantic model instances:

```
```

The validation system automatically:

- Validates data types
- Converts compatible types
- Generates clear error messages
- Creates OpenAPI schema documentation

Sources: [docs/en/docs/tutorial/body.md21-78](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/body.md#L21-L78)

### Validation Error Handling

```
```

Sources: [docs/en/docs/tutorial/handling-errors.md120-173](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L120-L173)

## Custom Validation

The system supports custom validation through Pydantic's validator functions, enabling complex business logic validation beyond basic type and constraint checking.

### AfterValidator Integration

Custom validators can be applied using Pydantic's `AfterValidator`:

```
```

Sources: [docs/en/docs/tutorial/query-params-str-validations.md409-440](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L409-L440)

## Parameter Function Architecture

```
```

Sources: [docs/en/docs/tutorial/path-params-numeric-validations.md144-164](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/path-params-numeric-validations.md#L144-L164)

## Type Conversion System

FastAPI automatically handles type conversion between HTTP string values and Python types, supporting complex data types beyond basic primitives.

### Supported Data Types

The system supports conversion for:

- Basic types: `int`, `float`, `str`, `bool`
- Date/time types: `datetime`, `date`, `time`, `timedelta`
- Complex types: `UUID`, `bytes`, `Decimal`
- Collections: `list`, `set`, `frozenset`

Sources: [docs/en/docs/tutorial/extra-data-types.md20-52](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/extra-data-types.md#L20-L52)

## OpenAPI Integration

All parameter validation rules are automatically reflected in the generated OpenAPI schema, providing accurate API documentation that matches the actual validation behavior.

### Schema Generation Flow

```
```

Sources: [docs/en/docs/tutorial/query-params-str-validations.md104-109](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L104-L109) [docs/en/docs/tutorial/path-params-numeric-validations.md21-33](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/path-params-numeric-validations.md#L21-L33)

## Error Response Format

Validation failures result in standardized HTTP 422 responses with detailed error information including field locations, error messages, and error types.

### RequestValidationError Structure

The error response contains:

- `detail` - Array of validation errors
- `loc` - Location of the error (path, query, body, etc.)
- `msg` - Human-readable error message
- `type` - Error type identifier

Sources: [docs/en/docs/tutorial/handling-errors.md122-156](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L122-L156)

## Advanced Configuration

### Parameter Exclusion and Documentation

Parameters can be excluded from OpenAPI documentation while maintaining validation:

```
```

Sources: [docs/en/docs/tutorial/query-params-str-validations.md403-407](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L403-L407) [docs/en/docs/tutorial/query-params-str-validations.md389-401](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L389-L401)

### Metadata and Documentation Enhancement

Parameters support rich metadata for enhanced documentation:

- `title` - Parameter title in documentation
- `description` - Detailed parameter description
- `example` - Example value for documentation

Sources: [docs/en/docs/tutorial/query-params-str-validations.md347-367](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/query-params-str-validations.md#L347-L367)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Parameter Validation and Handling](#parameter-validation-and-handling.md)
- [Core Parameter Types](#core-parameter-types.md)
- [Parameter Declaration Functions](#parameter-declaration-functions.md)
- [Parameter Validation Flow](#parameter-validation-flow.md)
- [Query Parameter Validation](#query-parameter-validation.md)
- [String Validation Constraints](#string-validation-constraints.md)
- [List and Multiple Value Handling](#list-and-multiple-value-handling.md)
- [Path Parameter Validation](#path-parameter-validation.md)
- [Numeric Validation Constraints](#numeric-validation-constraints.md)
- [Request Body Validation](#request-body-validation.md)
- [Pydantic Model Integration](#pydantic-model-integration.md)
- [Validation Error Handling](#validation-error-handling.md)
- [Custom Validation](#custom-validation.md)
- [AfterValidator Integration](#aftervalidator-integration.md)
- [Parameter Function Architecture](#parameter-function-architecture.md)
- [Type Conversion System](#type-conversion-system.md)
- [Supported Data Types](#supported-data-types.md)
- [OpenAPI Integration](#openapi-integration.md)
- [Schema Generation Flow](#schema-generation-flow.md)
- [Error Response Format](#error-response-format.md)
- [RequestValidationError Structure](#requestvalidationerror-structure.md)
- [Advanced Configuration](#advanced-configuration.md)
- [Parameter Exclusion and Documentation](#parameter-exclusion-and-documentation.md)
- [Metadata and Documentation Enhancement](#metadata-and-documentation-enhancement.md)
