Project Setup | qdrant/qdrant-client | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant-client](https://github.com/qdrant/qdrant-client "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 9 July 2025 ([ac6f6c](https://github.com/qdrant/qdrant-client/commits/ac6f6cd2))

- [Overview](qdrant/qdrant-client/1-overview.md)
- [Client Architecture](qdrant/qdrant-client/2-client-architecture.md)
- [Client Interface](qdrant/qdrant-client/2.1-client-interface.md)
- [Local Mode](qdrant/qdrant-client/2.2-local-mode.md)
- [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md)
- [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md)
- [Core Operations](qdrant/qdrant-client/3-core-operations.md)
- [Search Operations](qdrant/qdrant-client/3.1-search-operations.md)
- [Collection Management](qdrant/qdrant-client/3.2-collection-management.md)
- [Point Operations](qdrant/qdrant-client/3.3-point-operations.md)
- [Advanced Features](qdrant/qdrant-client/4-advanced-features.md)
- [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md)
- [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md)
- [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md)
- [Local Inference](qdrant/qdrant-client/4.4-local-inference.md)
- [Implementation Details](qdrant/qdrant-client/5-implementation-details.md)
- [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md)
- [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md)
- [Expression Evaluation](qdrant/qdrant-client/5.3-expression-evaluation.md)
- [Development & Testing](qdrant/qdrant-client/6-development-and-testing.md)
- [Project Setup](qdrant/qdrant-client/6.1-project-setup.md)
- [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md)
- [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md)

Menu

# Project Setup

Relevant source files

- [.github/workflows/integration-tests.yml](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml)
- [poetry.lock](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/poetry.lock)
- [pyproject.toml](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml)
- [tests/integration-tests.sh](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh)

This document covers the project configuration, dependency management, build system, and development environment setup for the qdrant-client Python library. It explains how Poetry is used to manage dependencies, testing frameworks, and the continuous integration pipeline.

For information about the testing framework and test execution, see [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md). For documentation generation and maintenance, see [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md).

## Build System Architecture

The qdrant-client project uses Poetry as its primary build system and dependency manager, with configuration centralized in `pyproject.toml`. The build system supports multiple Python versions and provides optional feature sets through extras.

```
```

**Sources:** [pyproject.toml1-79](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L1-L79) [pyproject.toml64-66](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L64-L66)

## Dependency Management

The project manages dependencies through Poetry's sophisticated dependency resolution system, supporting different Python versions with conditional dependencies and optional feature sets.

### Core Dependencies

| Dependency    | Version Constraint                 | Purpose                                  |
| ------------- | ---------------------------------- | ---------------------------------------- |
| `httpx`       | `>=0.20.0` with `http2` extras     | HTTP client for REST API communication   |
| `numpy`       | Version-specific constraints       | Numerical operations and vector handling |
| `pydantic`    | `>=1.10.8,!=2.0.*,!=2.1.*,!=2.2.0` | Data validation and serialization        |
| `grpcio`      | `>=1.41.0`                         | gRPC communication protocol              |
| `protobuf`    | `>=3.20.0`                         | Protocol buffer serialization            |
| `urllib3`     | `>=1.26.14,<3`                     | HTTP utilities                           |
| `portalocker` | `^2.7.0`                           | File locking for local storage           |

**Sources:** [pyproject.toml16-35](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L16-L35)

### Python Version Support

The project supports Python 3.9 through 3.13 with version-specific numpy constraints:

```
```

**Sources:** [pyproject.toml17-24](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L17-L24) [.github/workflows/integration-tests.yml16-21](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L16-L21)

### Optional Dependencies

The project provides optional extras for embedding functionality:

- **`fastembed`**: Enables text and image embedding through the FastEmbed library
- **`fastembed-gpu`**: Provides GPU-accelerated embedding capabilities

**Sources:** [pyproject.toml30-35](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L30-L35) [pyproject.toml60-62](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L60-L62)

## Development Environment Setup

### Initial Setup

1. **Install Poetry**: The project requires Poetry for dependency management
2. **Configure Virtual Environment**: Poetry can be configured to create or skip virtual environments
3. **Install Dependencies**: Install all dependency groups including optional extras

```
```

**Sources:** [.github/workflows/integration-tests.yml36-39](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L36-L39)

### Development Tools Configuration

The project includes several development tools with specific configurations:

| Tool         | Configuration                      | Purpose                         |
| ------------ | ---------------------------------- | ------------------------------- |
| `pytest`     | Custom markers for fastembed tests | Test execution and organization |
| `pyright`    | Strict type checking mode          | Static type analysis            |
| `ruff`       | Version 0.4.3                      | Code linting and formatting     |
| `autoflake`  | Version ^2.2.1                     | Unused import removal           |
| `pre-commit` | Version ^4.2.0                     | Git hook automation             |

**Sources:** [pyproject.toml37-46](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L37-L46) [pyproject.toml68-79](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L68-L79)

## Configuration Files

### pyproject.toml Structure

The main configuration file is organized into several sections:

```
```

**Sources:** [pyproject.toml1-79](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L1-L79)

### Package Metadata

The package is configured with the following metadata:

- **Name**: `qdrant-client`
- **Version**: `1.14.3`
- **License**: `Apache-2.0`
- **Package Structure**: Single package `qdrant_client` with gRPC stub exclusions

**Sources:** [pyproject.toml1-14](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L1-L14)

## Testing Infrastructure

### Test Execution Framework

The project uses a comprehensive testing setup with multiple test types:

```
```

**Sources:** [tests/integration-tests.sh1-51](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L1-L51) [.github/workflows/integration-tests.yml40-76](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L40-L76)

### Test Execution Script

The integration test script (`tests/integration-tests.sh`) manages the complete test lifecycle:

1. **Docker Setup**: Launches Qdrant service with specific port configuration
2. **Service Health Check**: Waits for service availability
3. **Test Execution**: Runs appropriate test suites based on configuration
4. **Cleanup**: Ensures proper Docker container shutdown

**Sources:** [tests/integration-tests.sh23-46](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L23-L46)

### Test Configuration

Pytest is configured with custom markers for handling optional dependencies:

- **`fastembed`**: Tests requiring FastEmbed package
- **`no_fastembed`**: Tests that don't require FastEmbed package

**Sources:** [pyproject.toml71-75](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L71-L75)

## CI/CD Pipeline

### GitHub Actions Workflow

The continuous integration pipeline runs comprehensive tests across multiple Python versions:

```
```

**Sources:** [.github/workflows/integration-tests.yml1-77](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L1-L77)

### Test Environment Configuration

The CI pipeline configures specific environment variables and test conditions:

- **`QDRANT_VERSION`**: Controls which Qdrant version to test against
- **`IGNORE_CONGRUENCE_TESTS`**: Skips local vs remote consistency tests
- **`HF_TOKEN`**: Provides access to Hugging Face models for FastEmbed tests

**Sources:** [tests/integration-tests.sh14-44](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L14-L44) [.github/workflows/integration-tests.yml60-69](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L60-L69)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Project Setup](#project-setup.md)
- [Build System Architecture](#build-system-architecture.md)
- [Dependency Management](#dependency-management.md)
- [Core Dependencies](#core-dependencies.md)
- [Python Version Support](#python-version-support.md)
- [Optional Dependencies](#optional-dependencies.md)
- [Development Environment Setup](#development-environment-setup.md)
- [Initial Setup](#initial-setup.md)
- [Development Tools Configuration](#development-tools-configuration.md)
- [Configuration Files](#configuration-files.md)
- [pyproject.toml Structure](#pyprojecttoml-structure.md)
- [Package Metadata](#package-metadata.md)
- [Testing Infrastructure](#testing-infrastructure.md)
- [Test Execution Framework](#test-execution-framework.md)
- [Test Execution Script](#test-execution-script.md)
- [Test Configuration](#test-configuration.md)
- [CI/CD Pipeline](#cicd-pipeline.md)
- [GitHub Actions Workflow](#github-actions-workflow.md)
- [Test Environment Configuration](#test-environment-configuration.md)
