Development Guide | qdrant/mcp-server-qdrant | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 20 April 2025 ([a3ab0b](https://github.com/qdrant/mcp-server-qdrant/commits/a3ab0b96))

- [Overview](qdrant/mcp-server-qdrant/1-overview.md)
- [Architecture](qdrant/mcp-server-qdrant/2-architecture.md)
- [Core Components](qdrant/mcp-server-qdrant/2.1-core-components.md)
- [Embedding System](qdrant/mcp-server-qdrant/2.2-embedding-system.md)
- [Configuration System](qdrant/mcp-server-qdrant/2.3-configuration-system.md)
- [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md)
- [Configuration Options](qdrant/mcp-server-qdrant/3.1-configuration-options.md)
- [Client Integration](qdrant/mcp-server-qdrant/3.2-client-integration.md)
- [API Reference](qdrant/mcp-server-qdrant/4-api-reference.md)
- [qdrant-store Tool](qdrant/mcp-server-qdrant/4.1-qdrant-store-tool.md)
- [qdrant-find Tool](qdrant/mcp-server-qdrant/4.2-qdrant-find-tool.md)
- [QdrantConnector Reference](qdrant/mcp-server-qdrant/5-qdrantconnector-reference.md)
- [Embedding Providers](qdrant/mcp-server-qdrant/6-embedding-providers.md)
- [Development Guide](qdrant/mcp-server-qdrant/7-development-guide.md)

Menu

# Development Guide

Relevant source files

- [.gitignore](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/.gitignore)
- [pyproject.toml](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml)
- [tests/\_\_init\_\_.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/__init__.py)
- [tests/test\_fastembed\_integration.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py)
- [tests/test\_qdrant\_integration.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py)

This guide provides essential information for developers who want to contribute to the mcp-server-qdrant project. It covers setting up a development environment, testing procedures, code quality tools, and contribution workflows. For information about using the server as an end-user, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md).

## 1. Development Environment Setup

### 1.1 Prerequisites

Before beginning development, ensure you have the following prerequisites:

- Python 3.10 or higher
- Git for version control
- uv (optional but recommended for dependency management)

### 1.2 Setting Up Your Environment

```
```

Sources: [pyproject.toml1-28](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L1-L28)

## 2. Project Structure

The codebase follows a modular structure to separate concerns and maintain clean architecture.

```
```

Key directories and files:

- `mcp_server_qdrant/`: Main package with the server implementation
- `mcp_server_qdrant/embeddings/`: Embedding providers implementation
- `tests/`: Test suite for the project
- `pyproject.toml`: Project configuration and dependencies

Sources: [pyproject.toml1-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L1-L37) [tests/\_\_init\_\_.py1-2](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/__init__.py#L1-L2)

## 3. Testing

The project uses pytest with asyncio support for testing. Tests are primarily integration tests that verify the functionality of key components like QdrantConnector and FastEmbedProvider.

### 3.1 Running Tests

```
```

### 3.2 Test Structure

```
```

### 3.3 Testing Patterns

The codebase follows several key testing patterns:

1. **Fixtures for Component Setup**: Test fixtures are used to create isolated instances of components for testing.

   ```
   ```

2. **Randomized Collection Names**: Tests use UUIDs to create unique collection names, ensuring tests don't interfere with each other.

3. **In-memory Database**: Tests use Qdrant's in-memory mode (`:memory:`) instead of connecting to a real server.

4. **Asynchronous Testing**: All tests use `@pytest.mark.asyncio` to handle async functions.

Sources: [tests/test\_qdrant\_integration.py9-32](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L9-L32) [tests/test\_fastembed\_integration.py8-16](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py#L8-L16) [pyproject.toml33-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L33-L37)

## 4. Code Quality Tools

The project uses several tools to maintain code quality:

| Tool       | Purpose                      | Configuration             |
| ---------- | ---------------------------- | ------------------------- |
| isort      | Sort imports                 | From `pyproject.toml`     |
| mypy       | Static type checking         | From `pyproject.toml`     |
| pyright    | Static type checking         | From `pyproject.toml`     |
| ruff       | Fast Python linter           | From `pyproject.toml`     |
| pre-commit | Git hooks to enforce quality | `.pre-commit-config.yaml` |

### 4.1 Running Code Quality Checks

```
```

Sources: [pyproject.toml20-28](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L20-L28)

## 5. Writing Tests

When writing new tests for the project, follow these guidelines:

### 5.1 QdrantConnector Testing

QdrantConnector tests should verify:

- Storing entries with various content and metadata
- Searching for entries with different queries
- Handling of multiple collections
- Error handling and edge cases

Example pattern for QdrantConnector test:

```
```

### 5.2 EmbeddingProvider Testing

EmbeddingProvider tests should verify:

- Successful model initialization
- Consistent embedding generation
- Correct vector dimensions
- Handling of different input types

Example pattern for EmbeddingProvider test:

```
```

Sources: [tests/test\_qdrant\_integration.py32-239](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L32-L239) [tests/test\_fastembed\_integration.py8-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py#L8-L64)

## 6. Contribution Workflow

### 6.1 Git Workflow

```
```

1. **Fork the Repository**: Create a fork of the main repository
2. **Create a Feature Branch**: Work on features in isolated branches
3. **Implement and Test**: Add your changes with appropriate tests
4. **Submit a Pull Request**: Create a PR against the main repository
5. **Code Review**: Address feedback from maintainers
6. **Merge**: Once approved, your changes will be merged

### 6.2 Pull Request Guidelines

- Ensure all tests pass
- Include new tests for new functionality
- Maintain or improve code coverage
- Follow the project's code style
- Include a clear description of the changes

## 7. Building and Packaging

The project uses hatchling for building Python packages.

### 7.1 Building the Package

```
```

### 7.2 Local Installation for Testing

```
```

### 7.3 Version Management

Version numbers are defined in `pyproject.toml`. Follow semantic versioning principles:

- MAJOR version for incompatible API changes
- MINOR version for added functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

Sources: [pyproject.toml2-3](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L2-L3) [pyproject.toml15-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L15-L17)

## 8. Dependency Management

### 8.1 Runtime Dependencies

The project uses several key dependencies:

- `mcp[cli]`: Core MCP protocol implementation
- `fastembed`: Fast embedding generation library
- `qdrant-client`: Client for interacting with Qdrant vector database
- `pydantic`: Data validation and settings management

### 8.2 Adding New Dependencies

When adding new dependencies:

1. Add them to `pyproject.toml` in the appropriate section
2. Document the reason for adding the dependency
3. Consider compatibility with existing dependencies
4. Update development environments with the new dependency

Sources: [pyproject.toml8-13](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L8-L13) [pyproject.toml20-28](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L20-L28)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development Guide](#development-guide.md)
- [1. Development Environment Setup](#1-development-environment-setup.md)
- [1.1 Prerequisites](#11-prerequisites.md)
- [1.2 Setting Up Your Environment](#12-setting-up-your-environment.md)
- [2. Project Structure](#2-project-structure.md)
- [3. Testing](#3-testing.md)
- [3.1 Running Tests](#31-running-tests.md)
- [3.2 Test Structure](#32-test-structure.md)
- [3.3 Testing Patterns](#33-testing-patterns.md)
- [4. Code Quality Tools](#4-code-quality-tools.md)
- [4.1 Running Code Quality Checks](#41-running-code-quality-checks.md)
- [5. Writing Tests](#5-writing-tests.md)
- [5.1 QdrantConnector Testing](#51-qdrantconnector-testing.md)
- [5.2 EmbeddingProvider Testing](#52-embeddingprovider-testing.md)
- [6. Contribution Workflow](#6-contribution-workflow.md)
- [6.1 Git Workflow](#61-git-workflow.md)
- [6.2 Pull Request Guidelines](#62-pull-request-guidelines.md)
- [7. Building and Packaging](#7-building-and-packaging.md)
- [7.1 Building the Package](#71-building-the-package.md)
- [7.2 Local Installation for Testing](#72-local-installation-for-testing.md)
- [7.3 Version Management](#73-version-management.md)
- [8. Dependency Management](#8-dependency-management.md)
- [8.1 Runtime Dependencies](#81-runtime-dependencies.md)
- [8.2 Adding New Dependencies](#82-adding-new-dependencies.md)
