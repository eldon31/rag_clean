Background Tasks | fastapi/fastapi | DeepWiki

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

# Background Tasks

Relevant source files

- [docs/en/docs/advanced/additional-responses.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/additional-responses.md)
- [docs/en/docs/advanced/behind-a-proxy.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/behind-a-proxy.md)
- [docs/en/docs/advanced/custom-response.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/custom-response.md)
- [docs/en/docs/advanced/path-operation-advanced-configuration.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/path-operation-advanced-configuration.md)
- [docs/en/docs/advanced/response-directly.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/response-directly.md)
- [docs/en/docs/advanced/settings.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md)
- [docs/en/docs/deployment/https.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/deployment/https.md)
- [docs/en/docs/release-notes.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/release-notes.md)
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
- [docs\_src/additional\_responses/tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/additional_responses/tutorial001.py)
- [docs\_src/behind\_a\_proxy/tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/behind_a_proxy/tutorial001_01.py)
- [docs\_src/custom\_response/tutorial001b.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial001b.py)
- [docs\_src/custom\_response/tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial009c.py)
- [docs\_src/custom\_response/tutorial010.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial010.py)
- [fastapi/\_\_init\_\_.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py)
- [tests/test\_tutorial/test\_behind\_a\_proxy/test\_tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_behind_a_proxy/test_tutorial001_01.py)
- [tests/test\_tutorial/test\_custom\_response/test\_tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_response/test_tutorial009c.py)

This document covers FastAPI's background task system, which allows executing functions after an HTTP response has been sent to the client. This system is useful for operations like sending emails, processing files, or logging that don't need to block the response.

For information about asynchronous programming concepts in FastAPI, see [4.1](fastapi/fastapi/4.1-asynchronous-support.md). For dependency injection patterns, see [2.2](fastapi/fastapi/2.2-dependency-injection.md).

## Purpose and Core Concepts

Background tasks in FastAPI enable deferred execution of functions after the HTTP response has been sent to the client. This pattern allows for better user experience by avoiding blocking operations while ensuring important side effects still occur.

The system is built on top of Starlette's background task implementation and integrates seamlessly with FastAPI's dependency injection system.

### Request-Response with Background Tasks Flow

```
```

Sources: [docs/en/docs/tutorial/background-tasks.md1-87](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L1-L87)

## Core Architecture

### BackgroundTasks Class Integration

```
```

The `BackgroundTasks` class is imported directly from Starlette but re-exported through FastAPI's main module for convenience. This design allows FastAPI to leverage Starlette's proven implementation while providing a unified import interface.

Sources: [fastapi/\_\_init\_\_.py8](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py#L8-L8) [docs/en/docs/tutorial/background-tasks.md66-74](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L66-L74)

### Task Function Types and Execution

FastAPI's background task system supports both synchronous and asynchronous task functions:

| Function Type | Declaration             | Execution Context |
| ------------- | ----------------------- | ----------------- |
| Synchronous   | `def task_func()`       | Thread pool       |
| Asynchronous  | `async def task_func()` | Event loop        |

```
```

Sources: [docs/en/docs/tutorial/background-tasks.md28-34](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L28-L34)

## Implementation Patterns

### Basic Usage Pattern

The most common pattern involves three steps:

1. **Import and declare**: Import `BackgroundTasks` and declare it as a parameter
2. **Create task function**: Define the function to execute in the background
3. **Add task**: Use `.add_task()` to queue the function

```
```

### Task Function Parameter Handling

```
```

The `.add_task()` method accepts:

- A callable function as the first argument
- Any positional arguments to pass to the function
- Any keyword arguments to pass to the function

Sources: [docs/en/docs/tutorial/background-tasks.md42-46](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L42-L46)

## Dependency Injection Integration

### Multi-Level Background Task Usage

```
```

FastAPI automatically reuses the same `BackgroundTasks` instance across all dependency levels within a single request, ensuring all background tasks are collected and executed together.

### Dependency Injection Example Flow

```
```

Sources: [docs/en/docs/tutorial/background-tasks.md48-63](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L48-L63)

## Technical Implementation Details

### Starlette Integration

FastAPI's background task system is a thin wrapper around Starlette's implementation:

| Component   | FastAPI                               | Starlette                                          |
| ----------- | ------------------------------------- | -------------------------------------------------- |
| Import Path | `from fastapi import BackgroundTasks` | `from starlette.background import BackgroundTasks` |
| Class       | Re-exported reference                 | Original implementation                            |
| Alternative | `BackgroundTask` (single)             | `BackgroundTask` (single)                          |

The key difference is that FastAPI provides `BackgroundTasks` (plural) as a dependency injection parameter, while `BackgroundTask` (singular) requires manual instantiation and response handling.

### Response Integration Mechanism

```
```

When `BackgroundTasks` is used as a parameter, FastAPI automatically attaches the queued tasks to the response object, ensuring they execute after the response is sent.

Sources: [docs/en/docs/tutorial/background-tasks.md66-74](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L66-L74)

## Use Cases and Limitations

### Appropriate Use Cases

Background tasks are suitable for:

- Email notifications after user actions
- File processing that can be asynchronous
- Logging and analytics
- Cache warming
- Cleanup operations

### Performance Considerations

```
```

For heavy computational tasks or distributed processing, external task queue systems like Celery are recommended over FastAPI's built-in background tasks.

### Memory and Resource Sharing

Background tasks in FastAPI:

- Run in the same process as the web application
- Have access to shared memory and variables
- Are suitable for lightweight operations
- Should not be used for long-running or resource-intensive tasks

Sources: [docs/en/docs/tutorial/background-tasks.md76-87](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md#L76-L87)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Background Tasks](#background-tasks.md)
- [Purpose and Core Concepts](#purpose-and-core-concepts.md)
- [Request-Response with Background Tasks Flow](#request-response-with-background-tasks-flow.md)
- [Core Architecture](#core-architecture.md)
- [BackgroundTasks Class Integration](#backgroundtasks-class-integration.md)
- [Task Function Types and Execution](#task-function-types-and-execution.md)
- [Implementation Patterns](#implementation-patterns.md)
- [Basic Usage Pattern](#basic-usage-pattern.md)
- [Task Function Parameter Handling](#task-function-parameter-handling.md)
- [Dependency Injection Integration](#dependency-injection-integration.md)
- [Multi-Level Background Task Usage](#multi-level-background-task-usage.md)
- [Dependency Injection Example Flow](#dependency-injection-example-flow.md)
- [Technical Implementation Details](#technical-implementation-details.md)
- [Starlette Integration](#starlette-integration.md)
- [Response Integration Mechanism](#response-integration-mechanism.md)
- [Use Cases and Limitations](#use-cases-and-limitations.md)
- [Appropriate Use Cases](#appropriate-use-cases.md)
- [Performance Considerations](#performance-considerations.md)
- [Memory and Resource Sharing](#memory-and-resource-sharing.md)
