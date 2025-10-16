Versioning and Dependencies | pydantic/pydantic | DeepWiki

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

# Versioning and Dependencies

Relevant source files

- [CITATION.cff](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff)
- [HISTORY.md](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md)
- [pydantic/version.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py)
- [uv.lock](https://github.com/pydantic/pydantic/blob/76ef0b08/uv.lock)

This document covers Pydantic's version management system, dependency compatibility checking, and version information utilities. It focuses on the tight coupling between `pydantic` and `pydantic-core`, the version enforcement mechanisms, and tools for debugging version-related issues.

For information about the overall development infrastructure and CI/CD, see [CI/CD Pipeline](pydantic/pydantic/7.2-cicd-pipeline.md). For release automation and documentation deployment, see [Documentation System](pydantic/pydantic/7.3-documentation-system.md).

## Overview

Pydantic enforces strict version compatibility between the pure Python `pydantic` package and the Rust-based `pydantic-core` package. This ensures that the schema generation logic in Python remains synchronized with the validation engine in Rust.

The version management system includes:

- A single source of truth for the current version
- Runtime checks to prevent version mismatches
- Utilities for debugging version information
- Special handling for development environments

Sources: [pydantic/version.py1-114](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L1-L114)

## Version Constants

### VERSION Constant

The `VERSION` constant in [pydantic/version.py11](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L11) holds the current version string and serves as the single source of truth for Pydantic's version:

```
```

This string follows the [PEP 440](https://peps.python.org/pep-0440/) version specifier format, supporting:

- Release versions: `2.11.0`
- Pre-release versions: `2.12.0b1` (beta), `2.12.0a1` (alpha)
- Development versions: `2.12.0b1+dev`

The version constant is also synchronized with [CITATION.cff47](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff#L47-L47) for academic citations.

Sources: [pydantic/version.py11-19](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L19) [CITATION.cff47](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff#L47-L47)

### Compatible Pydantic-Core Version

The `_COMPATIBLE_PYDANTIC_CORE_VERSION` constant defines the exact `pydantic-core` version required:

```
```

This constant must be kept in sync with the dependency constraint in `pyproject.toml`.

Sources: [pydantic/version.py21-22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L21-L22)

## Version Compatibility System

```
```

Sources: [pydantic/version.py77-99](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L77-L99)

### Runtime Version Checking

The `check_pydantic_core_version()` function performs a simple equality check:

```
```

This function is called by `_ensure_pydantic_core_version()` during module initialization to prevent Pydantic from loading with an incompatible `pydantic-core` version.

Sources: [pydantic/version.py77-79](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L77-L79)

### Error Handling and Editable Installs

The `_ensure_pydantic_core_version()` function raises a `SystemError` if versions don't match, except for editable installs in development:

| Condition                      | Python Version | Behavior                      |
| ------------------------------ | -------------- | ----------------------------- |
| Versions match                 | Any            | Load successfully             |
| Editable install               | 3.13+          | Skip check, load successfully |
| Version mismatch               | < 3.13         | Raise `SystemError`           |
| Version mismatch, not editable | 3.13+          | Raise `SystemError`           |

The editable install detection uses Python 3.13's `origin.dir_info.editable` property from `importlib.metadata.distribution()`.

Sources: [pydantic/version.py82-99](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L82-L99)

## Version Information Utilities

### version\_short()

Returns the `major.minor` portion of the version string:

```
```

Sources: [pydantic/version.py25-30](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L25-L30)

### version\_info()

The `version_info()` function collects comprehensive version information for debugging:

```
```

Sources: [pydantic/version.py33-74](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L33-L74)

The function searches for related packages in the environment:

```
```

Output format example:

```
               pydantic version: 2.12.0b1+dev
          pydantic-core version: 2.40.1
            pydantic-core build: release
                 python version: 3.11.5
                       platform: Linux-5.15.0-86-generic-x86_64
               related packages: fastapi-0.104.1 mypy-1.17.0 ...
                         commit: abc123def456
```

Sources: [pydantic/version.py44-74](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L44-L74)

## Mypy Version Parsing

The `parse_mypy_version()` utility parses mypy version strings, handling development versions:

```
```

This function is used by the mypy plugin to handle version-specific behavior.

Sources: [pydantic/version.py101-114](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L101-L114)

## Dependency Management

### Core Dependencies

```
```

Sources: [pydantic/version.py21-22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L21-L22) [uv.lock1-4](https://github.com/pydantic/pydantic/blob/76ef0b08/uv.lock#L1-L4)

### Version Update Process

When updating `pydantic-core`:

1. **Update `_COMPATIBLE_PYDANTIC_CORE_VERSION`** in [pydantic/version.py22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L22-L22)
2. **Update dependency constraint** in `pyproject.toml`
3. **Lock dependencies** with `uv lock`
4. **Update HISTORY.md** with the version bump note

Example from [HISTORY.md15](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L15-L15):

```
```

Sources: [pydantic/version.py21-22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L21-L22) [HISTORY.md15](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L15-L15)

### Related Package Ecosystem

The version info system tracks these related packages:

| Package                | Purpose                    |
| ---------------------- | -------------------------- |
| `email-validator`      | Email validation support   |
| `fastapi`              | Web framework integration  |
| `mypy`                 | Static type checking       |
| `pydantic-extra-types` | Additional type validators |
| `pydantic-settings`    | Settings management        |
| `pyright`              | Static type checking       |
| `typing_extensions`    | Backported typing features |

Sources: [pydantic/version.py44-52](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L44-L52)

## Development Workflow

### Version Checking During Development

```
```

Sources: [pydantic/version.py82-99](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L82-L99)

### Git Revision Tracking

The `version_info()` function attempts to determine the current git commit:

```
```

This helps identify the exact code version during development and debugging.

Sources: [pydantic/version.py60-63](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L60-L63)

## Release Version Management

### Version Evolution

The [HISTORY.md](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md) file documents version progression:

```
```

Sources: [HISTORY.md1-125](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L1-L125)

### Pydantic-Core Synchronization

Each Pydantic release is paired with a specific pydantic-core version:

| Pydantic Version | Pydantic-Core Version | Release Date |
| ---------------- | --------------------- | ------------ |
| v2.12.0b1        | v2.40.1               | 2025-10-03   |
| v2.12.0a1        | v2.35.1               | 2025-07-26   |
| v2.11.0          | v2.33.0               | 2025-03-27   |
| v2.10.0          | v2.27.0               | 2024-11-20   |

Sources: [HISTORY.md15](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L15-L15) [HISTORY.md101](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L101-L101) [HISTORY.md234](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L234-L234) [HISTORY.md641](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L641-L641)

### Version Bump Process

Based on [HISTORY.md](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md) version bumps include:

1. **Update VERSION constant** in [pydantic/version.py11](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L11)
2. **Update CITATION.cff** with new version and date [CITATION.cff47-48](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff#L47-L48)
3. **Bump pydantic-core dependency** [pydantic/version.py22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L22-L22)
4. **Document changes** in HISTORY.md
5. **Create GitHub release**

Sources: [pydantic/version.py11](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L11) [CITATION.cff47-48](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff#L47-L48) [HISTORY.md1-125](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md#L1-L125)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Versioning and Dependencies](#versioning-and-dependencies.md)
- [Overview](#overview.md)
- [Version Constants](#version-constants.md)
- [VERSION Constant](#version-constant.md)
- [Compatible Pydantic-Core Version](#compatible-pydantic-core-version.md)
- [Version Compatibility System](#version-compatibility-system.md)
- [Runtime Version Checking](#runtime-version-checking.md)
- [Error Handling and Editable Installs](#error-handling-and-editable-installs.md)
- [Version Information Utilities](#version-information-utilities.md)
- [version\_short()](#version_short.md)
- [version\_info()](#version_info.md)
- [Mypy Version Parsing](#mypy-version-parsing.md)
- [Dependency Management](#dependency-management.md)
- [Core Dependencies](#core-dependencies.md)
- [Version Update Process](#version-update-process.md)
- [Related Package Ecosystem](#related-package-ecosystem.md)
- [Development Workflow](#development-workflow.md)
- [Version Checking During Development](#version-checking-during-development.md)
- [Git Revision Tracking](#git-revision-tracking.md)
- [Release Version Management](#release-version-management.md)
- [Version Evolution](#version-evolution.md)
- [Pydantic-Core Synchronization](#pydantic-core-synchronization.md)
- [Version Bump Process](#version-bump-process.md)
