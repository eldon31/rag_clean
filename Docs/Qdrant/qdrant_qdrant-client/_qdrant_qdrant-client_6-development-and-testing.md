Development & Testing | qdrant/qdrant-client | DeepWiki

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

# Development & Testing

Relevant source files

- [.github/workflows/integration-tests.yml](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml)
- [poetry.lock](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/poetry.lock)
- [pyproject.toml](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml)
- [tests/integration-tests.sh](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh)

This document covers the development setup, testing frameworks, and CI/CD pipeline for the qdrant-client Python library. It explains how to set up a development environment, run tests, and contribute to the project.

For information about the overall project structure and client architecture, see [Client Architecture](qdrant/qdrant-client/2-client-architecture.md). For details about implementation internals, see [Implementation Details](qdrant/qdrant-client/5-implementation-details.md).

## Project Configuration and Dependencies

The qdrant-client project uses Poetry for dependency management and is configured through `pyproject.toml`. The project supports Python versions 3.9 through 3.13 and includes comprehensive development tooling.

### Core Dependencies

The project's main dependencies are defined in [pyproject.toml16-36](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L16-L36):

```
```

**Sources:** [pyproject.toml16-79](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L16-L79)

### Python Version Support Matrix

The project uses version-specific NumPy dependencies to ensure compatibility across Python versions:

| Python Version | NumPy Version |
| -------------- | ------------- |
| 3.9            | >=1.21,<2.1.0 |
| 3.10-3.11      | >=1.21        |
| 3.12           | >=1.26        |
| 3.13+          | >=2.1.0       |

**Sources:** [pyproject.toml19-24](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L19-L24)

### Development Tool Configuration

The project includes strict type checking and testing configurations:

```
```

**Sources:** [pyproject.toml68-75](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L68-L75)

## Testing Framework

The qdrant-client project implements a comprehensive testing strategy with multiple test types and CI/CD integration.

### Integration Test Infrastructure

The integration testing system uses Docker containers to test against real Qdrant instances:

```
```

**Sources:** [tests/integration-tests.sh1-51](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L1-L51)

### CI/CD Pipeline

The GitHub Actions workflow provides comprehensive testing across multiple Python versions and test types:

```
```

**Sources:** [.github/workflows/integration-tests.yml1-77](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L1-L77)

### Test Types and Execution

The testing framework includes several specialized test categories:

1. **Congruence Tests**: Verify that local and remote implementations produce identical results
2. **Integration Tests**: Test against live Qdrant service instances
3. **Async Client Tests**: Validate async client generation consistency
4. **Cache Tests**: Test inspection cache population and consistency
5. **Coverage Tests**: Ensure conversion layer coverage
6. **Docstring Tests**: Validate code examples in documentation
7. **Backward Compatibility Tests**: Test against older Qdrant versions

### Test Environment Configuration

The integration test script supports environment-based configuration:

| Environment Variable      | Default   | Purpose                     |
| ------------------------- | --------- | --------------------------- |
| `QDRANT_VERSION`          | `v1.14.1` | Qdrant Docker image version |
| `IGNORE_CONGRUENCE_TESTS` | `false`   | Skip congruence tests       |
| `REST_PORT`               | `6333`    | REST API port               |
| `GRPC_PORT`               | `6334`    | gRPC API port               |
| `P2P_PORT`                | `6335`    | P2P cluster port            |

**Sources:** [tests/integration-tests.sh14-21](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L14-L21)

### Backward Compatibility Testing

The project maintains backward compatibility through automated testing against multiple Qdrant versions:

```
```

When running backward compatibility tests, congruence tests are automatically skipped to focus on API compatibility rather than behavioral equivalence.

**Sources:** [tests/integration-tests.sh38-45](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L38-L45) [.github/workflows/integration-tests.yml65-70](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L65-L70)

## Documentation System

The project uses Sphinx for documentation generation with support for Jupyter notebooks and automated API documentation.

### Documentation Dependencies

The documentation system requires specific dependencies defined in `pyproject.toml`:

```
```

**Sources:** [pyproject.toml48-54](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L48-L54)

### Documentation Testing

The CI pipeline includes documentation testing through docstring validation:

```
```

This ensures that code examples in documentation remain functional and accurate.

**Sources:** [.github/workflows/integration-tests.yml56-58](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L56-L58)

## Development Workflow

The project follows a structured development workflow with automated checks and quality assurance.

### Code Quality Tools

The development environment includes several code quality tools:

- **Ruff**: Fast Python linter (pinned to version 0.4.3)
- **Autoflake**: Removes unused imports and variables
- **Pre-commit**: Git hooks for automated checks
- **Pyright**: Strict type checking
- **MyPy**: Additional type analysis

### Testing Workflow

1. **Local Development**: Run tests locally using pytest
2. **Pre-commit Hooks**: Automatic code quality checks
3. **CI Pipeline**: Comprehensive testing across Python versions
4. **Integration Testing**: Docker-based testing against Qdrant service
5. **Backward Compatibility**: Automated testing against older versions

### FastEmbed Integration Testing

The project includes specialized testing for FastEmbed integration:

```
```

This ensures the library works correctly both with and without the optional FastEmbed dependency.

**Sources:** [.github/workflows/integration-tests.yml71-76](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L71-L76)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development & Testing](#development-testing.md)
- [Project Configuration and Dependencies](#project-configuration-and-dependencies.md)
- [Core Dependencies](#core-dependencies.md)
- [Python Version Support Matrix](#python-version-support-matrix.md)
- [Development Tool Configuration](#development-tool-configuration.md)
- [Testing Framework](#testing-framework.md)
- [Integration Test Infrastructure](#integration-test-infrastructure.md)
- [CI/CD Pipeline](#cicd-pipeline.md)
- [Test Types and Execution](#test-types-and-execution.md)
- [Test Environment Configuration](#test-environment-configuration.md)
- [Backward Compatibility Testing](#backward-compatibility-testing.md)
- [Documentation System](#documentation-system.md)
- [Documentation Dependencies](#documentation-dependencies.md)
- [Documentation Testing](#documentation-testing.md)
- [Development Workflow](#development-workflow.md)
- [Code Quality Tools](#code-quality-tools.md)
- [Testing Workflow](#testing-workflow.md)
- [FastEmbed Integration Testing](#fastembed-integration-testing.md)
