Development Guide | qdrant/fastembed | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/fastembed](https://github.com/qdrant/fastembed "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 20 April 2025 ([b78564](https://github.com/qdrant/fastembed/commits/b785640b))

- [Overview](qdrant/fastembed/1-overview.md)
- [Installation and Setup](qdrant/fastembed/2-installation-and-setup.md)
- [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md)
- [TextEmbedding](qdrant/fastembed/3.1-textembedding.md)
- [SparseTextEmbedding](qdrant/fastembed/3.2-sparsetextembedding.md)
- [LateInteractionTextEmbedding](qdrant/fastembed/3.3-lateinteractiontextembedding.md)
- [ImageEmbedding](qdrant/fastembed/3.4-imageembedding.md)
- [LateInteractionMultimodalEmbedding](qdrant/fastembed/3.5-lateinteractionmultimodalembedding.md)
- [TextCrossEncoder](qdrant/fastembed/3.6-textcrossencoder.md)
- [Architecture](qdrant/fastembed/4-architecture.md)
- [Model Management](qdrant/fastembed/4.1-model-management.md)
- [ONNX Runtime Integration](qdrant/fastembed/4.2-onnx-runtime-integration.md)
- [Parallel Processing](qdrant/fastembed/4.3-parallel-processing.md)
- [Implementation Details](qdrant/fastembed/5-implementation-details.md)
- [Dense Text Embeddings](qdrant/fastembed/5.1-dense-text-embeddings.md)
- [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md)
- [Late Interaction Models](qdrant/fastembed/5.3-late-interaction-models.md)
- [Multimodal Models](qdrant/fastembed/5.4-multimodal-models.md)
- [Supported Models](qdrant/fastembed/6-supported-models.md)
- [Usage Examples](qdrant/fastembed/7-usage-examples.md)
- [Basic Text Embedding](qdrant/fastembed/7.1-basic-text-embedding.md)
- [Sparse and Hybrid Search](qdrant/fastembed/7.2-sparse-and-hybrid-search.md)
- [ColBERT and Late Interaction](qdrant/fastembed/7.3-colbert-and-late-interaction.md)
- [Image Embedding](qdrant/fastembed/7.4-image-embedding.md)
- [Performance Optimization](qdrant/fastembed/8-performance-optimization.md)
- [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md)
- [Development Guide](qdrant/fastembed/10-development-guide.md)

Menu

# Development Guide

Relevant source files

- [.github/workflows/python-tests.yml](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml)
- [.pre-commit-config.yaml](https://github.com/qdrant/fastembed/blob/b785640b/.pre-commit-config.yaml)
- [pyproject.toml](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml)

This guide outlines the process and best practices for contributing to FastEmbed. It covers the development environment setup, code organization, testing, and contribution workflow. For information about using FastEmbed in your applications, refer to the [Usage Examples](qdrant/fastembed/7-usage-examples.md).

## Setting Up the Development Environment

This section explains how to set up your development environment to contribute to FastEmbed.

### Prerequisites

- Python 3.9 or higher
- Git
- Poetry (for dependency management)

### Installation Steps for Development

1. Clone the repository:

   ```
   ```

2. Install dependencies with Poetry:

   ```
   ```

3. Install pre-commit hooks:

   ```
   ```

Sources: [pyproject.toml1-64](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L1-L64) [.pre-commit-config.yaml1-10](https://github.com/qdrant/fastembed/blob/b785640b/.pre-commit-config.yaml#L1-L10)

## Project Structure

FastEmbed follows a modular architecture with multiple embedding strategies and implementations. Understanding this structure is important for contributors.

### Code Organization

```
```

### From Interface to Implementation

```
```

Sources: System architecture diagrams

## Development Workflow

Following the proper development workflow ensures your contributions can be efficiently reviewed and merged.

### Step 1: Create a Feature Branch

```
```

### Step 2: Implement Your Changes

When implementing features or fixes, ensure you:

- Follow the code style guidelines
- Add appropriate tests
- Update documentation if necessary

### Step 3: Run Tests Locally

```
```

### Step 4: Submit a Pull Request

- Push your branch to GitHub
- Create a PR against the `main` branch
- Provide a clear description of the changes

### Continuous Integration

FastEmbed uses GitHub Actions for CI, which automatically runs tests on:

- Multiple Python versions (3.9 to 3.13)
- Multiple operating systems (Linux, macOS, Windows)

```
```

Sources: [.github/workflows/python-tests.yml1-48](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml#L1-L48)

## Code Style and Quality

FastEmbed maintains strict code quality standards to ensure maintainability and readability.

### Formatting and Linting

FastEmbed uses Ruff for both formatting and linting:

- Line length limit: 99 characters
- Enforced through pre-commit hooks

### Type Checking

Type hints are required for all function parameters and return values:

- FastEmbed uses Pyright in strict mode
- Type checking can be run with: `poetry run pyright`

### Common Patterns

When adding new features, follow these common patterns:

1. **New Embedding Types**: Extend appropriate base classes
2. **New Models**: Follow the OnnxModel pattern for consistent interface
3. **Utilities**: Place in appropriate utility modules to ensure reusability

Sources: [pyproject.toml59-63](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L59-L63) [.pre-commit-config.yaml1-10](https://github.com/qdrant/fastembed/blob/b785640b/.pre-commit-config.yaml#L1-L10)

## Testing Guidelines

Tests are crucial for maintaining FastEmbed's reliability. All new features and bug fixes should include appropriate tests.

### Test Organization

Tests are organized to mirror the project structure:

```
```

### Writing Tests

1. **Unit Tests**: Focus on testing a single function or method in isolation
2. **Integration Tests**: Test how components work together
3. **Model Tests**: Verify model-specific functionality and correctness

### Running Tests

```
```

Sources: [.github/workflows/python-tests.yml44-48](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml#L44-L48)

## Documentation

Good documentation is essential for both users and contributors.

### Docstrings

Use descriptive docstrings for all public classes and methods:

- Include parameter descriptions
- Specify return types and values
- Provide examples where appropriate

### API Documentation

API documentation is generated from docstrings. When updating or adding new features, ensure the documentation is updated.

### Building Documentation

FastEmbed uses MkDocs with Material theme for documentation:

```
```

Sources: [pyproject.toml44-49](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L44-L49)

## Adding New Models

Adding a new embedding model to FastEmbed typically involves these steps:

```
```

### Model Implementation Pattern

1. Determine the embedding type (dense, sparse, late interaction)
2. Extend the appropriate base class
3. Implement the required methods for tokenization and inference
4. Add model configuration to model registry if applicable

### ONNX Export Considerations

When adding support for new models:

1. Ensure the model can be properly exported to ONNX format
2. Test inference with ONNX Runtime
3. Optimize the model if necessary for better performance

## Dependency Management

FastEmbed uses Poetry for dependency management. When adding new dependencies or updating existing ones:

1. Use Poetry's commands to add dependencies:

   ```
   ```

2. Update dependency constraints in pyproject.toml if necessary

3. Test compatibility across Python versions

Sources: [pyproject.toml13-33](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L13-L33)

## Release Process

The release process for FastEmbed follows these steps:

1. **Version Bump**: Update version in pyproject.toml
2. **Changelog Update**: Ensure CHANGELOG.md is updated with all changes
3. **Documentation Update**: Make sure documentation is up-to-date
4. **Create Release PR**: Submit a PR with these changes
5. **Tag Release**: After PR is merged, tag the release
6. **Publish Package**: The CI pipeline will publish to PyPI

```
```

Sources: [pyproject.toml1-5](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L1-L5)

## Troubleshooting Common Issues

This section covers common issues encountered during development and their solutions.

### Environment Setup Issues

- **Poetry Installation Problems**: Ensure you're using a compatible Python version
- **Dependency Conflicts**: Try refreshing your virtual environment

### Testing Issues

- **Test Failures on Specific OS**: Check OS-specific dependencies
- **Model Download Failures**: Ensure you have proper internet connectivity and HF\_TOKEN if needed

### Contribution Issues

- **Pre-commit Hooks Failing**: Run pre-commit manually to see detailed errors
- **CI Pipeline Failures**: Check the specific test that failed and reproduce locally

## Conclusion

This development guide provides an overview of the contribution process for FastEmbed. By following these guidelines, you can help maintain and improve this high-performance embedding library.

For questions or help with contributions, please reach out through GitHub issues or pull requests.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development Guide](#development-guide.md)
- [Setting Up the Development Environment](#setting-up-the-development-environment.md)
- [Prerequisites](#prerequisites.md)
- [Installation Steps for Development](#installation-steps-for-development.md)
- [Project Structure](#project-structure.md)
- [Code Organization](#code-organization.md)
- [From Interface to Implementation](#from-interface-to-implementation.md)
- [Development Workflow](#development-workflow.md)
- [Step 1: Create a Feature Branch](#step-1-create-a-feature-branch.md)
- [Step 2: Implement Your Changes](#step-2-implement-your-changes.md)
- [Step 3: Run Tests Locally](#step-3-run-tests-locally.md)
- [Step 4: Submit a Pull Request](#step-4-submit-a-pull-request.md)
- [Continuous Integration](#continuous-integration.md)
- [Code Style and Quality](#code-style-and-quality.md)
- [Formatting and Linting](#formatting-and-linting.md)
- [Type Checking](#type-checking.md)
- [Common Patterns](#common-patterns.md)
- [Testing Guidelines](#testing-guidelines.md)
- [Test Organization](#test-organization.md)
- [Writing Tests](#writing-tests.md)
- [Running Tests](#running-tests.md)
- [Documentation](#documentation.md)
- [Docstrings](#docstrings.md)
- [API Documentation](#api-documentation.md)
- [Building Documentation](#building-documentation.md)
- [Adding New Models](#adding-new-models.md)
- [Model Implementation Pattern](#model-implementation-pattern.md)
- [ONNX Export Considerations](#onnx-export-considerations.md)
- [Dependency Management](#dependency-management.md)
- [Release Process](#release-process.md)
- [Troubleshooting Common Issues](#troubleshooting-common-issues.md)
- [Environment Setup Issues](#environment-setup-issues.md)
- [Testing Issues](#testing-issues.md)
- [Contribution Issues](#contribution-issues.md)
- [Conclusion](#conclusion.md)
