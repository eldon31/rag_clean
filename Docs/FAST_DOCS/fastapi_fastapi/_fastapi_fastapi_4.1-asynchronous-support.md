Asynchronous Support | fastapi/fastapi | DeepWiki

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

# Asynchronous Support

Relevant source files

- [docs/de/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/de/docs/async.md)
- [docs/em/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/em/docs/async.md)
- [docs/en/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/async.md)
- [docs/es/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/es/docs/async.md)
- [docs/fa/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/fa/docs/async.md)
- [docs/fr/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/fr/docs/async.md)
- [docs/ja/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/ja/docs/async.md)
- [docs/ko/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/ko/docs/async.md)
- [docs/pt/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/pt/docs/async.md)
- [docs/ru/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/ru/docs/async.md)
- [docs/tr/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/tr/docs/async.md)
- [docs/zh/docs/async.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/zh/docs/async.md)

This document explains how FastAPI handles asynchronous code execution, including the use of `async def` functions, concurrency patterns, and the differences between synchronous and asynchronous path operation functions.

## Purpose and Scope

This page covers:

- How FastAPI supports both synchronous and asynchronous code
- When to use `async def` vs regular `def` functions
- How FastAPI handles different function types internally
- Performance considerations for I/O-bound vs CPU-bound operations

## Overview of Asynchronous Support in FastAPI

FastAPI provides native asynchronous support through Python's `async`/`await` syntax, built on top of Starlette's ASGI foundation. This architecture enables efficient handling of concurrent requests, particularly for I/O-bound operations such as database queries, API calls, and file operations.

### FastAPI Async Architecture

```
```

### Request Processing Flow

```
```

Sources: \[docs/en/docs/async.md:1-55], \[docs/en/docs/async.md:366-372], \[docs/en/docs/async.md:415-423]

## When to Use Async Functions

The decision to use `async def` or regular `def` for your path operation functions depends on what your function does:

| Use `async def` when...                    | Use `def` when...                                     |
| ------------------------------------------ | ----------------------------------------------------- |
| Calling other async functions with `await` | Using synchronous libraries (most database libraries) |
| Making async network calls                 | Performing CPU-intensive operations                   |
| Using async database drivers               | Not making any I/O operations                         |
| Not doing CPU-intensive work               | Not sure what to use                                  |

FastAPI will handle both types correctly, but following these guidelines allows for performance optimizations.

```
```

Sources: \[docs/en/docs/async.md:5-55]

## How FastAPI Handles Async and Sync Functions

### Path Operation Function Execution

FastAPI's handling of path operation functions depends on their declaration:

```
```

**For `async def` path operations:**

- FastAPI calls the function directly using `await`
- Execution remains in the main event loop
- Can use `await` for other async operations
- Example: [docs/en/docs/async.md17-22](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/async.md#L17-L22)

**For `def` path operations:**

- FastAPI wraps the call in `run_in_threadpool()`
- Execution moves to an external thread
- Cannot use `await` inside the function
- Example: [docs/en/docs/async.md34-39](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/async.md#L34-L39)

### Dependencies and Sub-dependencies

The same execution model applies to the dependency injection system:

| Dependency Type      | Execution Method | Can Use `await`? |
| -------------------- | ---------------- | ---------------- |
| `async def get_db()` | Direct await     | ✅ Yes            |
| `def get_db()`       | ThreadPool       | ❌ No             |

Dependencies can be mixed freely - FastAPI handles each according to its type. Sub-dependencies follow the same pattern, allowing complex dependency trees with mixed execution models.

Sources: \[docs/en/docs/async.md:415-423], \[docs/en/docs/async.md:424-431]

## Concurrency vs Parallelism

FastAPI's asynchronous support is based on concurrency, which is different from parallelism:

```
```

- **Concurrency**: Handling multiple tasks by switching between them when waiting occurs
- **Parallelism**: Executing multiple tasks simultaneously on different processors

FastAPI excels at concurrency, which is ideal for web applications that spend most of their time waiting for I/O operations.

Sources: \[docs/en/docs/async.md:96-261]

## I/O-Bound vs CPU-Bound Operations

Understanding the difference between I/O-bound and CPU-bound operations helps in choosing the right approach:

| I/O-Bound Operations             | CPU-Bound Operations       |
| -------------------------------- | -------------------------- |
| Network requests                 | Complex calculations       |
| Database queries                 | Image/audio processing     |
| File system operations           | Machine learning           |
| API calls                        | Data transformations       |
| **Best with**: Async/concurrency | **Best with**: Parallelism |

For web APIs, most operations are I/O-bound, making async a good default choice.

Sources: \[docs/en/docs/async.md:77-89], \[docs/en/docs/async.md:262-301]

## Technical Implementation Details

FastAPI's asynchronous capabilities are built on a carefully designed stack that provides compatibility and performance:

### Async Stack Architecture

```
```

### Coroutine and ThreadPool Management

FastAPI uses different execution strategies based on function signatures:

```
```

### AnyIO Integration

FastAPI leverages AnyIO's structured concurrency features:

- Compatible with both `asyncio` and `trio` backends
- Provides unified async abstraction layer
- Enables advanced concurrency patterns
- Supports context managers and cancellation

The `run_in_threadpool()` function prevents blocking the main event loop when executing synchronous code, ensuring the server remains responsive to other requests.

Sources: \[docs/en/docs/async.md:366-372], \[docs/en/docs/async.md:415-423], \[docs/en/docs/async.md:418-420]

## Performance Considerations

Choosing the right function type directly impacts FastAPI application performance:

### Performance Matrix

| Operation Type     | Library Support       | Recommended Function Type | Execution Method | Performance Impact |
| ------------------ | --------------------- | ------------------------- | ---------------- | ------------------ |
| Database queries   | `asyncpg`, `motor`    | `async def`               | Direct await     | ⚡ Optimal          |
| Database queries   | `psycopg2`, `pymongo` | `def`                     | ThreadPool       | ✅ Good             |
| HTTP requests      | `httpx`, `aiohttp`    | `async def`               | Direct await     | ⚡ Optimal          |
| HTTP requests      | `requests`            | `def`                     | ThreadPool       | ✅ Good             |
| File I/O           | `aiofiles`            | `async def`               | Direct await     | ⚡ Optimal          |
| File I/O           | Built-in `open()`     | `def`                     | ThreadPool       | ✅ Good             |
| CPU computation    | Any                   | `def`                     | ThreadPool       | ⚠️ Limited         |
| Trivial operations | N/A                   | `async def`               | Direct           | ⚡ Optimal          |

### ThreadPool Behavior

When FastAPI encounters a `def` function, it automatically:

```
```

### FastAPI-Specific Optimizations

Unlike some other async frameworks, FastAPI optimizations include:

- **Automatic threadpool management**: No need to manually configure thread pools
- **Smart function detection**: Analyzes function signatures at startup
- **Mixed execution support**: Seamlessly combines async and sync dependencies
- **Zero-copy where possible**: Minimal overhead for async operations

For compute-only operations (no I/O), `async def` performs better in FastAPI due to reduced threadpool overhead - approximately 100 nanoseconds saved per call compared to other frameworks.

Sources: \[docs/en/docs/async.md:415-423], \[docs/en/docs/async.md:418-420]

## Writing Your Own Async Code

If you need to write custom asynchronous code beyond FastAPI's built-in functionality, you can use:

1. **AnyIO**: The library that powers Starlette and FastAPI
2. **Asyncer**: A thin layer on top of AnyIO with improved type annotations
3. **Standard asyncio**: Python's built-in asynchronous library

These tools can help you implement more advanced concurrency patterns in your FastAPI applications.

Sources: \[docs/en/docs/async.md:366-372]

## Conclusion

FastAPI's support for both synchronous and asynchronous code provides flexibility while maintaining high performance. By understanding when to use each approach, you can optimize your application for different types of operations.

Remember:

- Use `async def` when working with other async code or I/O-bound operations
- Use regular `def` when working with synchronous libraries or CPU-bound tasks
- FastAPI will handle both correctly, but following these guidelines allows for better performance

The asynchronous capabilities of FastAPI, powered by Starlette and AnyIO, contribute significantly to its impressive performance compared to other Python web frameworks.

Sources: \[docs/en/docs/async.md:394-403]

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Asynchronous Support](#asynchronous-support.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview of Asynchronous Support in FastAPI](#overview-of-asynchronous-support-in-fastapi.md)
- [FastAPI Async Architecture](#fastapi-async-architecture.md)
- [Request Processing Flow](#request-processing-flow.md)
- [When to Use Async Functions](#when-to-use-async-functions.md)
- [How FastAPI Handles Async and Sync Functions](#how-fastapi-handles-async-and-sync-functions.md)
- [Path Operation Function Execution](#path-operation-function-execution.md)
- [Dependencies and Sub-dependencies](#dependencies-and-sub-dependencies.md)
- [Concurrency vs Parallelism](#concurrency-vs-parallelism.md)
- [I/O-Bound vs CPU-Bound Operations](#io-bound-vs-cpu-bound-operations.md)
- [Technical Implementation Details](#technical-implementation-details.md)
- [Async Stack Architecture](#async-stack-architecture.md)
- [Coroutine and ThreadPool Management](#coroutine-and-threadpool-management.md)
- [AnyIO Integration](#anyio-integration.md)
- [Performance Considerations](#performance-considerations.md)
- [Performance Matrix](#performance-matrix.md)
- [ThreadPool Behavior](#threadpool-behavior.md)
- [FastAPI-Specific Optimizations](#fastapi-specific-optimizations.md)
- [Writing Your Own Async Code](#writing-your-own-async-code.md)
- [Conclusion](#conclusion.md)
