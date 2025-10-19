CI/CD Pipeline | pydantic/pydantic | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[pydantic/pydantic](https://github.com/pydantic/pydantic "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 11 October 2025 ([76ef0b](https://github.com/pydantic/pydantic/commits/76ef0b08))

- [Overview](pydantic/pydantic/1-overview.md)
- [Core Model System](pydantic/pydantic/2-core-model-system.md)
- [BaseModel](pydantic/pydantic/2.1-basemodel.md)
- [Field System](pydantic/pydantic/2.2-field-system.md)
- [Model Configuration](pydantic/pydantic/2.3-model-configuration.md)
- [Type System](pydantic/pydantic/3-type-system.md)
- [Constrained Types](pydantic/pydantic/3.1-constrained-types.md)
- [Network Types](pydantic/pydantic/3.2-network-types.md)
- [TypeAdapter](pydantic/pydantic/3.3-typeadapter.md)
- [Generics and Forward References](pydantic/pydantic/3.4-generics-and-forward-references.md)
- [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md)
- [Validators](pydantic/pydantic/4.1-validators.md)
- [Serializers](pydantic/pydantic/4.2-serializers.md)
- [JSON Conversion](pydantic/pydantic/4.3-json-conversion.md)
- [Schema Generation](pydantic/pydantic/5-schema-generation.md)
- [Core Schema Generation](pydantic/pydantic/5.1-core-schema-generation.md)
- [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md)
- [Advanced Features](pydantic/pydantic/6-advanced-features.md)
- [Dataclass Support](pydantic/pydantic/6.1-dataclass-support.md)
- [Function Validation](pydantic/pydantic/6.2-function-validation.md)
- [RootModel and Computed Fields](pydantic/pydantic/6.3-rootmodel-and-computed-fields.md)
- [Plugin System](pydantic/pydantic/6.4-plugin-system.md)
- [Development and Deployment](pydantic/pydantic/7-development-and-deployment.md)
- [Testing Framework](pydantic/pydantic/7.1-testing-framework.md)
- [CI/CD Pipeline](pydantic/pydantic/7.2-cicd-pipeline.md)
- [Documentation System](pydantic/pydantic/7.3-documentation-system.md)
- [Versioning and Dependencies](pydantic/pydantic/7.4-versioning-and-dependencies.md)
- [Migration and Compatibility](pydantic/pydantic/8-migration-and-compatibility.md)
- [V1 to V2 Migration](pydantic/pydantic/8.1-v1-to-v2-migration.md)
- [Backported Modules](pydantic/pydantic/8.2-backported-modules.md)

Menu

# CI/CD Pipeline

Relevant source files

- [.github/labels/default\_pass.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/labels/default_pass.yml)
- [.github/labels/first\_pass.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/labels/first_pass.yml)
- [.github/workflows/ci.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml)
- [.github/workflows/codspeed.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/codspeed.yml)
- [.github/workflows/dependencies-check.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/dependencies-check.yml)
- [.github/workflows/docs-update.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml)
- [.github/workflows/integration.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/integration.yml)
- [.github/workflows/labeler.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/labeler.yml)
- [.github/workflows/third-party.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml)
- [.github/workflows/update-pydantic-people.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/update-pydantic-people.yml)
- [.github/workflows/upload-previews.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/upload-previews.yml)
- [build-docs.sh](https://github.com/pydantic/pydantic/blob/76ef0b08/build-docs.sh)

This document provides a detailed overview of the Continuous Integration and Continuous Deployment (CI/CD) pipeline used in the Pydantic project. It covers the GitHub Actions workflows, testing strategies, and release processes. For information about the testing framework and approach, see [Testing Framework](pydantic/pydantic/7.1-testing-framework.md).

## Pipeline Overview

Pydantic employs a comprehensive CI/CD pipeline implemented with GitHub Actions to ensure code quality, maintain compatibility across different environments, and automate releases. The pipeline consists of multiple workflows that handle different aspects of the development lifecycle.

```
```

Sources: [.github/workflows/ci.yml3-14](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L3-L14) [.github/workflows/docs-update.yml3-12](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L3-L12) [.github/workflows/third-party.yml11-20](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml#L11-L20) [.github/workflows/dependencies-check.yml3-7](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/dependencies-check.yml#L3-L7) [.github/workflows/integration.yml3-6](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/integration.yml#L3-L6)

## Main CI Workflow

The primary CI workflow is defined in `.github/workflows/ci.yml` and consists of multiple jobs that run in parallel to verify different aspects of the codebase.

### Triggering Events

The main CI workflow is triggered by the following events:

- Pushes to the `main` branch
- Any tag pushes (used for releases)
- Pull requests

### Jobs Structure

```
```

Sources: [.github/workflows/ci.yml16-448](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L16-L448)

### Linting and Static Analysis

The `lint` job runs a series of checks on the codebase:

- Runs on multiple Python versions (3.9 through 3.13)
- Uses the pre-commit framework to run linters
- Checks code style, formatting, and other quality gates

Sources: [.github/workflows/ci.yml17-40](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L17-L40) [.pre-commit-config.yaml1-32](https://github.com/pydantic/pydantic/blob/76ef0b08/.pre-commit-config.yaml#L1-L32)

### Documentation Build

The `docs-build` job:

- Builds the documentation using MkDocs
- Ensures all documentation is valid and renders correctly
- Creates symbolic links for extra modules

Sources: [.github/workflows/ci.yml42-66](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L42-L66) [build-docs.sh1-26](https://github.com/pydantic/pydantic/blob/76ef0b08/build-docs.sh#L1-L26)

## Test Matrix

The testing strategy employs a comprehensive matrix to ensure Pydantic works correctly across different environments:

```
```

The test job runs tests:

1. Without optional dependencies
2. With all extra dependencies installed
3. With different configurations on each platform

Sources: [.github/workflows/ci.yml84-154](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L84-L154) [Makefile64-67](https://github.com/pydantic/pydantic/blob/76ef0b08/Makefile#L64-L67)

### Memory Testing

The `test-memray` job uses the memray profiler to detect memory leaks and inefficient memory usage patterns.

Sources: [.github/workflows/ci.yml68-82](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L68-L82)

### Type Checking

The CI includes dedicated jobs for mypy integration testing and type checking:

- `test-mypy`: Runs the mypy integration tests with different mypy versions
- `test-typechecking-integration`: Tests typechecking with both Mypy and Pyright

Sources: [.github/workflows/ci.yml182-249](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L182-L249) [Makefile41-62](https://github.com/pydantic/pydantic/blob/76ef0b08/Makefile#L41-L62)

### Coverage Tracking

The `coverage-combine` job:

- Collects coverage data from all test runs
- Combines them into a unified coverage report
- Creates both HTML and data files for analysis

For pull requests, the `coverage-pr-comment` job posts a comment with coverage information.

Sources: [.github/workflows/ci.yml251-316](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L251-L316) [.github/workflows/upload-previews.yml1-37](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/upload-previews.yml#L1-L37)

## Release Process

Pydantic uses a tag-based release process that is fully automated through the CI/CD pipeline:

```
```

The release process consists of the following steps:

1. A tag is pushed that matches the version in `pydantic/version.py`
2. The CI workflow runs all tests and checks
3. If successful, the `release` job builds and publishes the package to PyPI
4. The `send-tweet` job posts a release announcement on Twitter
5. The `docs-update` workflow updates the documentation site

Sources: [.github/workflows/ci.yml365-448](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L365-L448) [.github/workflows/docs-update.yml56-113](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L56-L113)

## Additional Workflows

### Third-Party Integration Tests

The `third-party.yml` workflow tests Pydantic with popular libraries that depend on it:

| Library               | Description                            |
| --------------------- | -------------------------------------- |
| FastAPI               | Web framework based on Pydantic models |
| SQLModel              | ORM using Pydantic models              |
| Beanie                | MongoDB ODM                            |
| ODMantic              | Alternative MongoDB ODM                |
| Pandera               | Data validation for pandas             |
| OpenAPI Python Client | Client generator                       |
| Polar, BentoML, etc.  | Other significant dependencies         |

This workflow runs on a schedule and can be triggered manually to detect compatibility issues before they affect users.

Sources: [.github/workflows/third-party.yml1-611](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml#L1-L611)

### Dependency Checking

The `dependencies-check.yml` workflow:

- Identifies first and last versions of dependencies
- Tests Pydantic with these versions across Python versions
- Ensures compatibility across the supported dependency range

Sources: [.github/workflows/dependencies-check.yml1-54](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/dependencies-check.yml#L1-L54)

### Performance Testing

The `codspeed.yml` workflow:

- Runs benchmarks to measure performance
- Reports results to CodSpeed
- Helps detect performance regressions

Sources: [.github/workflows/codspeed.yml1-81](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/codspeed.yml#L1-L81)

### Family Integration

The `integration.yml` workflow tests integration with other Pydantic family libraries:

- pydantic-settings
- pydantic-extra-types

Sources: [.github/workflows/integration.yml1-26](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/integration.yml#L1-L26) [tests/test\_pydantic\_extra\_types.sh1-15](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_pydantic_extra_types.sh#L1-L15)

## Development Workflow Integration

The CI/CD pipeline integrates with local development through several mechanisms:

### Makefile Commands

The Makefile provides commands that mirror CI checks:

| Command          | Description                     |
| ---------------- | ------------------------------- |
| `make test`      | Runs the test suite             |
| `make testcov`   | Runs tests with coverage report |
| `make lint`      | Runs linting checks             |
| `make typecheck` | Runs type checking              |
| `make format`    | Auto-formats code               |
| `make docs`      | Builds documentation            |
| `make all`       | Runs the standard CI checks     |

Sources: [Makefile1-140](https://github.com/pydantic/pydantic/blob/76ef0b08/Makefile#L1-L140)

### Pre-commit Hooks

Pre-commit hooks run checks before code is committed:

- Prevent direct commits to main branch
- Check YAML/TOML syntax
- Fix file endings and whitespace
- Run linters and type checkers

Sources: [.pre-commit-config.yaml1-32](https://github.com/pydantic/pydantic/blob/76ef0b08/.pre-commit-config.yaml#L1-L32)

## Project Specific Customizations

### Testing Environment Variables

Several environment variables control test behavior:

- `COLUMNS`: Set to 150 for consistent output formatting
- `UV_FROZEN`: Ensures dependency freezing with uv
- `FORCE_COLOR`: Enables colored test output
- `NUM_THREADS`: Controls parallel test execution

Sources: [.github/workflows/ci.yml11-14](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L11-L14) [Makefile3](https://github.com/pydantic/pydantic/blob/76ef0b08/Makefile#L3-L3)

### Dependency Management

The CI/CD pipeline uses `uv` for Python dependency management:

- Fast, deterministic package installation
- Supports lockfiles for reproducible environments
- Used consistently across all workflows

Sources: [.github/workflows/ci.yml27-35](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L27-L35) [Makefile14-17](https://github.com/pydantic/pydantic/blob/76ef0b08/Makefile#L14-L17)

## Continuous Documentation

Documentation is continuously built and published:

1. For every push to main, a development version is published
2. For releases, the documentation is updated with version aliases
3. The search index is updated for Algolia search integration

Sources: [.github/workflows/docs-update.yml56-113](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L56-L113)

By following this comprehensive approach to CI/CD, Pydantic ensures high code quality, broad compatibility, and a smooth release process, all while maintaining excellent documentation.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [CI/CD Pipeline](#cicd-pipeline.md)
- [Pipeline Overview](#pipeline-overview.md)
- [Main CI Workflow](#main-ci-workflow.md)
- [Triggering Events](#triggering-events.md)
- [Jobs Structure](#jobs-structure.md)
- [Linting and Static Analysis](#linting-and-static-analysis.md)
- [Documentation Build](#documentation-build.md)
- [Test Matrix](#test-matrix.md)
- [Memory Testing](#memory-testing.md)
- [Type Checking](#type-checking.md)
- [Coverage Tracking](#coverage-tracking.md)
- [Release Process](#release-process.md)
- [Additional Workflows](#additional-workflows.md)
- [Third-Party Integration Tests](#third-party-integration-tests.md)
- [Dependency Checking](#dependency-checking.md)
- [Performance Testing](#performance-testing.md)
- [Family Integration](#family-integration.md)
- [Development Workflow Integration](#development-workflow-integration.md)
- [Makefile Commands](#makefile-commands.md)
- [Pre-commit Hooks](#pre-commit-hooks.md)
- [Project Specific Customizations](#project-specific-customizations.md)
- [Testing Environment Variables](#testing-environment-variables.md)
- [Dependency Management](#dependency-management.md)
- [Continuous Documentation](#continuous-documentation.md)
