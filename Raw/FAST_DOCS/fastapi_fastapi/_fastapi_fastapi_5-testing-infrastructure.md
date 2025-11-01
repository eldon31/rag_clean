Testing Infrastructure | fastapi/fastapi | DeepWiki

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

# Testing Infrastructure

Relevant source files

- [.pre-commit-config.yaml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml)
- [requirements-tests.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt)
- [tests/test\_tutorial/test\_cookie\_param\_models/test\_tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_cookie_param_models/test_tutorial002.py)
- [tests/test\_tutorial/test\_sql\_databases/test\_tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_sql_databases/test_tutorial002.py)
- [tests/test\_typing\_python39.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_typing_python39.py)
- [tests/test\_union\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_body.py)
- [tests/test\_union\_inherited\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_inherited_body.py)
- [tests/utils.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/utils.py)

This document covers FastAPI's comprehensive testing infrastructure, including the test framework setup, code quality tools, and automated quality assurance processes. The testing infrastructure ensures code reliability through automated testing, linting, type checking, and pre-commit validation hooks.

For information about specific test framework usage patterns and TestClient implementation, see [Test Framework and Tools](fastapi/fastapi/5.1-test-framework-and-tools.md). For details about linting, formatting, and pre-commit hook configuration, see [Code Quality and Pre-commit](fastapi/fastapi/5.2-code-quality-and-pre-commit.md).

## Overview

FastAPI's testing infrastructure is built around `pytest` as the primary testing framework, with `TestClient` providing HTTP request simulation capabilities. The system includes comprehensive code quality tools, version compatibility testing, and automated validation through pre-commit hooks.

**Testing Framework Architecture**

```
```

Sources: [requirements-tests.txt1-17](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L1-L17) [tests/utils.py1-35](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/utils.py#L1-L35)

## Testing Dependencies and Requirements

The testing infrastructure relies on a carefully curated set of dependencies defined in `requirements-tests.txt`. These dependencies support various testing scenarios including async operations, database interactions, and security features.

| Category       | Package           | Version          | Purpose                     |
| -------------- | ----------------- | ---------------- | --------------------------- |
| Core Testing   | `pytest`          | `>=7.1.3,<9.0.0` | Primary testing framework   |
| Coverage       | `coverage[toml]`  | `>= 6.5.0,< 8.0` | Test coverage measurement   |
| Type Checking  | `mypy`            | `==1.8.0`        | Static type analysis        |
| Assertions     | `dirty-equals`    | `==0.9.0`        | Flexible assertion matching |
| Snapshots      | `inline-snapshot` | `>=0.21.1`       | Snapshot testing            |
| Database       | `sqlmodel`        | `==0.0.24`       | Database model testing      |
| Async          | `anyio[trio]`     | `>=3.2.1,<5.0.0` | Async testing support       |
| Security       | `PyJWT`           | `==2.8.0`        | JWT token testing           |
| Authentication | `passlib[bcrypt]` | `>=1.7.2,<2.0.0` | Password hashing testing    |

Sources: [requirements-tests.txt1-17](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L1-L17)

## Version Compatibility Testing

The testing infrastructure includes sophisticated version compatibility utilities to ensure FastAPI works across different Python and Pydantic versions.

**Version Compatibility System**

```
```

The `tests/utils.py` module provides version-specific testing utilities:

- `needs_py39`: Skips tests requiring Python 3.9+
- `needs_py310`: Skips tests requiring Python 3.10+
- `needs_pydanticv1`: Skips tests requiring Pydantic v1
- `needs_pydanticv2`: Skips tests requiring Pydantic v2
- `pydantic_snapshot()`: Provides version-specific snapshot testing

Sources: [tests/utils.py7-34](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/utils.py#L7-L34)

## Pre-commit Quality Assurance

The testing infrastructure includes automated code quality checks through pre-commit hooks configured in `.pre-commit-config.yaml`.

**Pre-commit Hook Pipeline**

```
```

Sources: [.pre-commit-config.yaml1-26](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml#L1-L26)

## Test Patterns and Utilities

FastAPI tests follow consistent patterns for HTTP testing, OpenAPI schema validation, and cross-version compatibility.

**Common Testing Patterns**

```
```

Key testing utilities include:

- **TestClient**: HTTP client for simulating requests [tests/test\_union\_inherited\_body.py24](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_inherited_body.py#L24-L24)
- **dirty-equals**: Flexible assertion matching [tests/test\_union\_inherited\_body.py89-98](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_inherited_body.py#L89-L98)
- **inline-snapshot**: Snapshot testing for OpenAPI schemas [tests/test\_tutorial/test\_sql\_databases/test\_tutorial002.py71-73](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_sql_databases/test_tutorial002.py#L71-L73)
- **Parametrized fixtures**: Version compatibility testing [tests/test\_tutorial/test\_cookie\_param\_models/test\_tutorial002.py17-36](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_cookie_param_models/test_tutorial002.py#L17-L36)

Sources: [tests/test\_union\_inherited\_body.py1-137](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_inherited_body.py#L1-L137) [tests/test\_tutorial/test\_sql\_databases/test\_tutorial002.py1-482](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_sql_databases/test_tutorial002.py#L1-L482) [tests/test\_tutorial/test\_cookie\_param\_models/test\_tutorial002.py1-244](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_cookie_param_models/test_tutorial002.py#L1-L244)

## Type Checking Integration

The testing infrastructure includes `mypy` for static type analysis, ensuring type safety across the codebase. Type checking is integrated with specific type stub packages for external dependencies.

**Type Checking Dependencies**

| Package        | Version             | Purpose               |
| -------------- | ------------------- | --------------------- |
| `mypy`         | `==1.8.0`           | Static type checker   |
| `types-ujson`  | `==5.10.0.20240515` | Type stubs for ujson  |
| `types-orjson` | `==3.6.2`           | Type stubs for orjson |

Advanced type testing includes support for Python 3.10+ syntax using generics like `list[int]` and `dict[str, list[int]]` as demonstrated in the type compatibility tests.

Sources: [requirements-tests.txt14-16](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L14-L16) [tests/test\_typing\_python39.py1-25](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_typing_python39.py#L1-L25)

## Test Organization Structure

Tests are organized by feature area with consistent naming conventions and import patterns. The test suite covers core functionality, tutorial examples, and edge cases across different Python and Pydantic versions.

**Test File Categories**

- **Core functionality tests**: `tests/test_*.py`
- **Tutorial tests**: `tests/test_tutorial/*/test_*.py`
- **Version-specific tests**: Files with `_py39`, `_py310`, `_an` suffixes
- **Pydantic compatibility**: Files with `_pv1` suffixes

Each test file follows the pattern of importing required dependencies, creating a FastAPI app and TestClient, and implementing test functions with descriptive names and comprehensive assertions.

Sources: [tests/test\_union\_inherited\_body.py1-8](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_inherited_body.py#L1-L8) [tests/test\_tutorial/test\_sql\_databases/test\_tutorial002.py1-13](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_sql_databases/test_tutorial002.py#L1-L13) [tests/test\_tutorial/test\_cookie\_param\_models/test\_tutorial002.py1-14](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_cookie_param_models/test_tutorial002.py#L1-L14)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Testing Infrastructure](#testing-infrastructure.md)
- [Overview](#overview.md)
- [Testing Dependencies and Requirements](#testing-dependencies-and-requirements.md)
- [Version Compatibility Testing](#version-compatibility-testing.md)
- [Pre-commit Quality Assurance](#pre-commit-quality-assurance.md)
- [Test Patterns and Utilities](#test-patterns-and-utilities.md)
- [Type Checking Integration](#type-checking-integration.md)
- [Test Organization Structure](#test-organization-structure.md)
