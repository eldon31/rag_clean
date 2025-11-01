Code Quality and Pre-commit | fastapi/fastapi | DeepWiki

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

# Code Quality and Pre-commit

Relevant source files

- [.pre-commit-config.yaml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml)
- [requirements-tests.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt)
- [requirements.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements.txt)
- [scripts/format.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh)
- [scripts/lint.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh)
- [scripts/test-cov-html.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test-cov-html.sh)
- [scripts/test.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh)
- [tests/test\_tutorial/test\_cookie\_param\_models/test\_tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_cookie_param_models/test_tutorial002.py)
- [tests/test\_tutorial/test\_sql\_databases/test\_tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_sql_databases/test_tutorial002.py)
- [tests/test\_typing\_python39.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_typing_python39.py)
- [tests/test\_union\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_body.py)
- [tests/test\_union\_inherited\_body.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_union_inherited_body.py)
- [tests/utils.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/utils.py)

This document covers the code quality infrastructure and pre-commit hook system used in the FastAPI repository. It details the configuration and usage of linting, formatting, type checking, and automated quality gates that ensure code consistency and reliability.

For information about the actual test framework and testing utilities, see [Test Framework and Tools](fastapi/fastapi/5.1-test-framework-and-tools.md). For CI/CD automation that runs these quality checks, see [CI/CD Pipeline](fastapi/fastapi/6.2-cicd-pipeline.md).

## Pre-commit Hook System

FastAPI uses a comprehensive pre-commit hook system to enforce code quality standards before commits are made to the repository. The configuration is defined in [.pre-commit-config.yaml1-26](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml#L1-L26)

### Hook Configuration

The pre-commit system is configured with Python 3.10 as the default language version and includes two main repository sources:

```
```

The system includes validation hooks for file formats and content, plus automated code quality enforcement through Ruff.

**Sources:** [.pre-commit-config.yaml1-26](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml#L1-L26)

### Pre-commit.ci Integration

The configuration includes integration with pre-commit.ci for automated maintenance:

| Feature              | Configuration                                              | Description                            |
| -------------------- | ---------------------------------------------------------- | -------------------------------------- |
| Auto-fix Messages    | `🎨 [pre-commit.ci] Auto format from pre-commit.com hooks` | Commit messages for automatic fixes    |
| Auto-update Messages | `⬆ [pre-commit.ci] pre-commit autoupdate`                  | Commit messages for dependency updates |

**Sources:** [.pre-commit-config.yaml24-25](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml#L24-L25)

## Code Linting and Formatting with Ruff

FastAPI uses Ruff as its primary tool for both code linting and formatting, replacing multiple traditional tools with a single, fast implementation.

### Ruff Configuration

The Ruff configuration includes two main hooks:

```
```

**Sources:** [.pre-commit-config.yaml16-22](https://github.com/fastapi/fastapi/blob/3e2dbf91/.pre-commit-config.yaml#L16-L22) [scripts/lint.sh7-8](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L7-L8) [scripts/format.sh4-5](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh#L4-L5)

### Manual Code Quality Scripts

The repository provides several scripts for manual execution of code quality tools:

| Script              | Purpose                       | Commands                                            |
| ------------------- | ----------------------------- | --------------------------------------------------- |
| `scripts/lint.sh`   | Run linting and type checking | `mypy fastapi`, `ruff check`, `ruff format --check` |
| `scripts/format.sh` | Apply code formatting         | `ruff check --fix`, `ruff format`                   |

**Sources:** [scripts/lint.sh1-9](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L1-L9) [scripts/format.sh1-6](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh#L1-L6)

## Type Checking with mypy

FastAPI uses mypy for static type checking to ensure type safety across the codebase.

### mypy Configuration

The mypy version is pinned in the test requirements and executed as part of the linting process:

```
```

**Sources:** [requirements-tests.txt5](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L5-L5) [scripts/lint.sh6](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L6-L6)

## Test Coverage Infrastructure

The repository includes comprehensive test coverage tracking using the `coverage` tool.

### Coverage Configuration

```
```

The test execution includes setting `PYTHONPATH=./docs_src` to include documentation source code in the test environment.

**Sources:** [requirements-tests.txt3-4](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L3-L4) [scripts/test.sh6-7](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh#L6-L7) [scripts/test-cov-html.sh6-9](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test-cov-html.sh#L6-L9)

## Testing Infrastructure Dependencies

The testing infrastructure includes several specialized testing libraries and utilities:

| Dependency        | Version          | Purpose                   |
| ----------------- | ---------------- | ------------------------- |
| `pytest`          | `>=7.1.3,<9.0.0` | Main testing framework    |
| `coverage[toml]`  | `>= 6.5.0,< 8.0` | Test coverage measurement |
| `mypy`            | `==1.8.0`        | Static type checking      |
| `dirty-equals`    | `==0.9.0`        | Flexible equality testing |
| `inline-snapshot` | `>=0.21.1`       | Snapshot testing          |

**Sources:** [requirements-tests.txt3-6](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L3-L6) [requirements-tests.txt13](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-tests.txt#L13-L13)

### Testing Utilities and Patterns

The repository includes specialized testing utilities for handling different Python versions and Pydantic versions:

```
```

The `pydantic_snapshot` function enables version-specific snapshot testing for maintaining compatibility across Pydantic versions.

**Sources:** [tests/utils.py7-12](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/utils.py#L7-L12) [tests/utils.py15-34](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/utils.py#L15-L34)

## Quality Assurance Integration

The code quality system integrates with the broader development workflow through standardized scripts and dependency management:

### Development Dependencies

The main requirements file includes pre-commit as a development dependency:

```
```

**Sources:** [requirements.txt1-7](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements.txt#L1-L7)

### Script Integration Patterns

The quality assurance scripts follow consistent patterns for error handling and output:

| Script Feature    | Implementation                 | Purpose                      |
| ----------------- | ------------------------------ | ---------------------------- |
| Error Handling    | `set -e`                       | Exit on any command failure  |
| Verbose Output    | `set -x`                       | Display executed commands    |
| Environment Setup | `export PYTHONPATH=./docs_src` | Include docs in Python path  |
| Parameter Passing | `${@}`                         | Forward all script arguments |

**Sources:** [scripts/test.sh3-4](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh#L3-L4) [scripts/lint.sh3-4](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L3-L4) [scripts/format.sh2](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh#L2-L2)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Code Quality and Pre-commit](#code-quality-and-pre-commit.md)
- [Pre-commit Hook System](#pre-commit-hook-system.md)
- [Hook Configuration](#hook-configuration.md)
- [Pre-commit.ci Integration](#pre-commitci-integration.md)
- [Code Linting and Formatting with Ruff](#code-linting-and-formatting-with-ruff.md)
- [Ruff Configuration](#ruff-configuration.md)
- [Manual Code Quality Scripts](#manual-code-quality-scripts.md)
- [Type Checking with mypy](#type-checking-with-mypy.md)
- [mypy Configuration](#mypy-configuration.md)
- [Test Coverage Infrastructure](#test-coverage-infrastructure.md)
- [Coverage Configuration](#coverage-configuration.md)
- [Testing Infrastructure Dependencies](#testing-infrastructure-dependencies.md)
- [Testing Utilities and Patterns](#testing-utilities-and-patterns.md)
- [Quality Assurance Integration](#quality-assurance-integration.md)
- [Development Dependencies](#development-dependencies.md)
- [Script Integration Patterns](#script-integration-patterns.md)
