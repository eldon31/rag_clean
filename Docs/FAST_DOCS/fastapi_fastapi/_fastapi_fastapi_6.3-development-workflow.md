Development Workflow | fastapi/fastapi | DeepWiki

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

# Development Workflow

Relevant source files

- [pyproject.toml](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml)
- [requirements.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements.txt)
- [scripts/format.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh)
- [scripts/lint.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh)
- [scripts/test-cov-html.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test-cov-html.sh)
- [scripts/test.sh](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh)

This document covers the local development workflow, tooling, and scripts used for contributing to the FastAPI codebase. It explains how developers use the project's build system, development scripts, and quality tools during the development process.

For information about automated CI/CD pipelines, see [CI/CD Pipeline](fastapi/fastapi/6.2-cicd-pipeline.md). For details about code quality tools configuration, see [Code Quality and Pre-commit](fastapi/fastapi/5.2-code-quality-and-pre-commit.md). For testing patterns and frameworks, see [Test Framework and Tools](fastapi/fastapi/5.1-test-framework-and-tools.md).

## Build System and Project Configuration

FastAPI uses PDM (Python Dependency Management) as its build system, configured through `pyproject.toml`. The project follows modern Python packaging standards with comprehensive tooling configuration.

### Build System Configuration

The build system is configured using PDM backend with dynamic versioning:

```
```

**PDM Build System Configuration**

The build system specifies PDM as the backend and includes development sources in the distribution package.

Sources: [pyproject.toml1-3](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L1-L3) [pyproject.toml127-140](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L127-L140)

### Dependency Management

FastAPI defines multiple dependency groups for different use cases:

| Dependency Group  | Purpose                        | Key Packages                                             |
| ----------------- | ------------------------------ | -------------------------------------------------------- |
| Core Dependencies | Essential runtime requirements | `starlette`, `pydantic`, `typing-extensions`             |
| `standard`        | Standard FastAPI installation  | `fastapi-cli`, `httpx`, `jinja2`, `uvicorn`              |
| `all`             | Complete feature set           | All standard plus `orjson`, `ujson`, `pydantic-settings` |
| Development       | Local development tools        | `pre-commit`, `playwright`                               |

Sources: [pyproject.toml45-48](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L45-L48) [pyproject.toml60-77](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L60-L77) [pyproject.toml98-122](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L98-L122) [requirements.txt1-7](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements.txt#L1-L7)

## Development Scripts Overview

The project provides shell scripts in the `scripts/` directory to standardize common development tasks:

```
```

**Development Script Ecosystem**

Each script serves a specific purpose in the development workflow, with clear separation of concerns.

Sources: [scripts/test.sh1-8](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh#L1-L8) [scripts/lint.sh1-9](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L1-L9) [scripts/format.sh1-6](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh#L1-L6) [scripts/test-cov-html.sh1-10](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test-cov-html.sh#L1-L10)

## Local Development Workflow

The typical development workflow follows this sequence:

```
```

**Local Development Process Flow**

The workflow ensures code quality through multiple validation stages before committing changes.

Sources: [scripts/format.sh1-6](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh#L1-L6) [scripts/lint.sh1-9](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L1-L9) [scripts/test.sh1-8](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh#L1-L8) [requirements.txt4](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements.txt#L4-L4)

### Development Environment Setup

1. **Dependency Installation**: Install using the development requirements which include all optional dependencies and development tools
2. **Pre-commit Setup**: Install pre-commit hooks to enforce quality checks before commits
3. **Script Permissions**: Ensure shell scripts have execute permissions

Sources: [requirements.txt1-7](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements.txt#L1-L7)

## Code Quality Workflow

The code quality workflow uses multiple tools orchestrated through shell scripts:

### Formatting Workflow

The `scripts/format.sh` script performs automatic code formatting:

```
```

This two-step process first applies automatic fixes for linting violations, then formats the code according to style guidelines.

Sources: [scripts/format.sh4-5](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/format.sh#L4-L5)

### Linting Workflow

The `scripts/lint.sh` script runs comprehensive code quality checks:

```
```

This validates type annotations with MyPy, checks code quality with Ruff, and verifies formatting compliance.

Sources: [scripts/lint.sh6-8](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/lint.sh#L6-L8)

### Tool Configuration Integration

```
```

**Tool Configuration Architecture**

All development tools are configured centrally in `pyproject.toml` with tool-specific sections.

Sources: [pyproject.toml144-270](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L144-L270)

## Testing Workflow

The testing workflow uses pytest with coverage tracking and custom configuration:

### Test Execution

The `scripts/test.sh` script sets up the testing environment:

```
```

This configures the Python path to include documentation source code and runs tests with coverage tracking.

Sources: [scripts/test.sh6-7](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test.sh#L6-L7)

### Test Configuration

Key pytest configuration elements:

| Configuration         | Purpose                                        |
| --------------------- | ---------------------------------------------- |
| `--strict-config`     | Enforce strict configuration validation        |
| `--strict-markers`    | Require marker registration                    |
| `--ignore=docs_src`   | Exclude documentation code from test discovery |
| `xfail_strict = true` | Treat expected failures strictly               |
| `filterwarnings`      | Suppress specific deprecation warnings         |

Sources: [pyproject.toml163-187](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L163-L187)

## Coverage Reporting

The coverage system tracks code coverage across multiple contexts:

```
```

**Coverage Reporting Pipeline**

Coverage data is collected during test runs and can be combined and reported in multiple formats.

### Coverage Configuration

The coverage system is configured for parallel execution and comprehensive source tracking:

- **Data Collection**: Tracks `docs_src`, `tests`, and `fastapi` directories
- **Context Tracking**: Uses dynamic context based on test functions
- **Parallel Support**: Enables parallel test execution with data aggregation
- **HTML Reports**: Generates detailed HTML reports with context information

Sources: [pyproject.toml189-210](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L189-L210) [scripts/test-cov-html.sh6-9](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test-cov-html.sh#L6-L9)

### Coverage Output

The `scripts/test-cov-html.sh` script generates comprehensive coverage reports:

1. **Combine**: Merges parallel coverage data files
2. **Report**: Displays terminal coverage summary with missing lines
3. **HTML**: Creates interactive HTML coverage report

Sources: [scripts/test-cov-html.sh7-9](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/test-cov-html.sh#L7-L9)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development Workflow](#development-workflow.md)
- [Build System and Project Configuration](#build-system-and-project-configuration.md)
- [Build System Configuration](#build-system-configuration.md)
- [Dependency Management](#dependency-management.md)
- [Development Scripts Overview](#development-scripts-overview.md)
- [Local Development Workflow](#local-development-workflow.md)
- [Development Environment Setup](#development-environment-setup.md)
- [Code Quality Workflow](#code-quality-workflow.md)
- [Formatting Workflow](#formatting-workflow.md)
- [Linting Workflow](#linting-workflow.md)
- [Tool Configuration Integration](#tool-configuration-integration.md)
- [Testing Workflow](#testing-workflow.md)
- [Test Execution](#test-execution.md)
- [Test Configuration](#test-configuration.md)
- [Coverage Reporting](#coverage-reporting.md)
- [Coverage Configuration](#coverage-configuration.md)
- [Coverage Output](#coverage-output.md)
