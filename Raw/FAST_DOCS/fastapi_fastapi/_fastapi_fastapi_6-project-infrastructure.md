Project Infrastructure | fastapi/fastapi | DeepWiki

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

# Project Infrastructure

Relevant source files

- [pyproject.toml](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml)

This document covers the fundamental project infrastructure of FastAPI, including the build system, packaging configuration, dependency management, and development tool configurations. The infrastructure serves as the foundation that enables FastAPI's development workflow, testing, and distribution.

For information about the documentation build system, see [Documentation System](fastapi/fastapi/6.1-documentation-system.md). For CI/CD automation workflows, see [CI/CD Pipeline](fastapi/fastapi/6.2-cicd-pipeline.md). For development scripts and contributor workflows, see [Development Workflow](fastapi/fastapi/6.3-development-workflow.md).

## Build System and Packaging

FastAPI uses a modern Python packaging approach centered around PDM (Python Dependency Manager) as the build backend. The project configuration is entirely defined in `pyproject.toml`, following PEP 518 standards.

### Build Configuration

```
```

**Build System Configuration**

The build system is configured in [pyproject.toml1-3](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L1-L3) specifying PDM as the backend. The `pdm.backend` handles all packaging operations, from source distribution to wheel creation.

**Dynamic Versioning**

Version management is handled dynamically through [pyproject.toml127-128](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L127-L128) extracting the version from [fastapi/\_\_init\_\_.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py) This ensures the package version stays synchronized with the codebase version without manual updates.

**Source Distribution Includes**

The build includes additional directories beyond the core package [pyproject.toml132-139](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L132-L139):

- `tests/` - Test suite for distribution validation
- `docs_src/` - Documentation source examples
- `scripts/` - Development and utility scripts
- `requirements*.txt` - Dependency specifications
- `docs/en/docs/img/favicon.png` - Required for testing

Sources: [pyproject.toml1-139](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L1-L139)

### Package Metadata and Dependencies

```
```

**Core Dependencies**

FastAPI maintains minimal core dependencies [pyproject.toml45-49](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L45-L49):

- `starlette` - ASGI framework foundation
- `pydantic` - Data validation and serialization
- `typing-extensions` - Enhanced type hints

**Optional Dependency Sets**

Three optional dependency sets provide different installation profiles [pyproject.toml58-122](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L58-L122):

| Set                             | Purpose                        | Key Components                                      |
| ------------------------------- | ------------------------------ | --------------------------------------------------- |
| `standard`                      | Common web app features        | CLI, HTTP client, templates, file uploads           |
| `standard-no-fastapi-cloud-cli` | Standard without FastAPI Cloud | Same as standard minus cloud CLI                    |
| `all`                           | Complete feature set           | All standard features plus JSON, sessions, settings |

**CLI Entry Point**

The package provides a command-line interface through [pyproject.toml124-125](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L124-L125) mapping the `fastapi` command to `fastapi.cli:main`.

Sources: [pyproject.toml5-125](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L5-L125)

## Development Tool Configuration

FastAPI integrates multiple development tools through centralized configuration, ensuring consistent code quality and development experience across the project.

### Type Checking and Linting

```
```

**MyPy Type Checking**

Strict type checking is enabled globally [pyproject.toml144-145](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L144-L145) with targeted overrides for specific modules:

- `fastapi.concurrency` - Relaxed import checking due to threading complexity
- `fastapi.tests.*` - Allow missing imports for test isolation
- `docs_src.*` - Relaxed rules for documentation examples

**Ruff Linting and Formatting**

Comprehensive linting rules [pyproject.toml211-226](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L211-L226) cover:

- Code style enforcement (pycodestyle)
- Import organization (isort)
- Bug prevention (flake8-bugbear)
- Code modernization (pyupgrade)

Extensive per-file overrides [pyproject.toml228-258](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L228-L258) accommodate documentation examples and tutorial code that intentionally demonstrates specific patterns.

Sources: [pyproject.toml144-266](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L144-L266)

### Testing and Coverage Configuration

```
```

**Pytest Configuration**

Test execution is configured for strict validation [pyproject.toml163-170](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L163-L170):

- Strict configuration prevents typos in pytest options
- Strict markers require all test markers to be registered
- Documentation source is excluded from test discovery
- XFail strict mode prevents accidentally passing expected failures

**Coverage Tracking**

Comprehensive coverage configuration [pyproject.toml189-210](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L189-L210) enables:

- Parallel test execution with data aggregation
- Source tracking across `fastapi`, `tests`, and `docs_src`
- Dynamic context tracking per test function
- HTML reports with test context display

**Warning Filters**

Extensive warning filters [pyproject.toml171-187](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L171-L187) handle known issues:

- Framework deprecation warnings (Starlette, SQLAlchemy)
- Library compatibility warnings (passlib, trio)
- Python version-specific warnings

Sources: [pyproject.toml163-210](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L163-L210)

## Project Metadata and Distribution

The project maintains comprehensive metadata for PyPI distribution and ecosystem integration.

### Package Classification and Compatibility

```
```

**Compatibility Matrix**

FastAPI supports a broad compatibility matrix [pyproject.toml36-41](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L36-L41):

- Python versions: 3.8 through 3.13
- Framework integrations: AsyncIO, Pydantic v1/v2
- Operating systems: Platform independent
- Development status: Beta (stable API, active development)

**Project URLs and Resources**

The package provides comprehensive resource links [pyproject.toml51-56](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L51-L56):

| Resource      | URL                   |
| ------------- | --------------------- |
| Homepage      | GitHub repository     |
| Documentation | Official docs site    |
| Issues        | GitHub issue tracker  |
| Changelog     | Release notes section |

Sources: [pyproject.toml14-56](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L14-L56)

## Slim Package Variant

FastAPI supports a minimal distribution variant for specialized deployment scenarios.

### Slim Build Configuration

The project includes configuration for generating a `fastapi-slim` package [pyproject.toml141-142](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L141-L142) through the `tiangolo._internal-slim-build` tool. This variant likely excludes optional dependencies and development tools for reduced installation size.

This configuration enables:

- Lightweight container deployments
- Minimal dependency installations
- Specialized distribution channels

Sources: [pyproject.toml141-142](https://github.com/fastapi/fastapi/blob/3e2dbf91/pyproject.toml#L141-L142)

The project infrastructure provides a robust foundation for FastAPI's development, testing, and distribution processes. The configuration balances strict quality standards with practical development needs, supporting both core maintainers and the broader contributor community through comprehensive tooling and clear dependency management.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Project Infrastructure](#project-infrastructure.md)
- [Build System and Packaging](#build-system-and-packaging.md)
- [Build Configuration](#build-configuration.md)
- [Package Metadata and Dependencies](#package-metadata-and-dependencies.md)
- [Development Tool Configuration](#development-tool-configuration.md)
- [Type Checking and Linting](#type-checking-and-linting.md)
- [Testing and Coverage Configuration](#testing-and-coverage-configuration.md)
- [Project Metadata and Distribution](#project-metadata-and-distribution.md)
- [Package Classification and Compatibility](#package-classification-and-compatibility.md)
- [Slim Package Variant](#slim-package-variant.md)
- [Slim Build Configuration](#slim-build-configuration.md)
