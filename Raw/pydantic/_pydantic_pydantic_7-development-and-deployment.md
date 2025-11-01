Development and Deployment | pydantic/pydantic | DeepWiki

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

# Development and Deployment

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
- [CITATION.cff](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff)
- [HISTORY.md](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md)
- [README.md](https://github.com/pydantic/pydantic/blob/76ef0b08/README.md)
- [build-docs.sh](https://github.com/pydantic/pydantic/blob/76ef0b08/build-docs.sh)
- [docs/extra/tweaks.css](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/extra/tweaks.css)
- [docs/index.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/index.md)
- [docs/install.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/install.md)
- [docs/theme/main.html](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/theme/main.html)
- [docs/why.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/why.md)
- [mkdocs.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml)
- [pydantic/version.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py)
- [tests/conftest.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py)
- [uv.lock](https://github.com/pydantic/pydantic/blob/76ef0b08/uv.lock)

This document describes the development infrastructure, testing framework, continuous integration/deployment pipeline, and release processes for Pydantic. It covers how the codebase is tested, versioned, documented, and deployed to users.

For information about the core model system and validation logic, see [Core Model System](pydantic/pydantic/2-core-model-system.md). For schema generation internals, see [Schema Generation](pydantic/pydantic/5-schema-generation.md).

## Overview

Pydantic's development and deployment infrastructure encompasses:

- **Version Management**: Strict version compatibility checks between `pydantic` and `pydantic-core`
- **Testing Framework**: Comprehensive test suite with pytest fixtures and utilities
- **CI/CD Pipeline**: GitHub Actions workflows for linting, testing, and deployment
- **Documentation System**: MkDocs-based documentation with versioning via mike
- **Release Process**: Automated PyPI publishing with trusted publishing and changelog generation

The infrastructure ensures quality through multi-platform testing, third-party integration testing, and automated version compatibility validation.

## Version Management and Compatibility

### Version Constants and Checking

Pydantic maintains strict version compatibility between the pure Python package (`pydantic`) and the Rust-based validation core (`pydantic-core`).

```
```

**Sources**: [pydantic/version.py11](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L11) [pydantic/version.py22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L22-L22) [pydantic/version.py77-99](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L77-L99)

| Component                           | Description                          | Location                                                                                                   |
| ----------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `VERSION`                           | Current Pydantic version string      | [pydantic/version.py11](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L11)    |
| `_COMPATIBLE_PYDANTIC_CORE_VERSION` | Required pydantic-core version       | [pydantic/version.py22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L22-L22)    |
| `check_pydantic_core_version()`     | Validates core version match         | [pydantic/version.py77-79](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L77-L79) |
| `_ensure_pydantic_core_version()`   | Raises SystemError on mismatch       | [pydantic/version.py82-98](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L82-L98) |
| `version_info()`                    | Returns detailed version information | [pydantic/version.py33-74](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L33-L74) |

The version check occurs at import time and raises a `SystemError` if the installed `pydantic-core` version doesn't match the expected version, unless Pydantic is installed in editable mode (development).

### Version Information Utility

The `version_info()` function provides comprehensive environment information:

```
```

Returns information including:

- Pydantic version
- pydantic-core version and build profile
- Python version and platform
- Related package versions (FastAPI, mypy, pyright, etc.)
- Git commit hash (if in git repository)

**Sources**: [pydantic/version.py33-74](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L33-L74)

## Testing Infrastructure

### Test Organization and Fixtures

```
```

**Sources**: [tests/conftest.py1-203](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L1-L203)

### Key Testing Fixtures

| Fixture                 | Purpose                                                          | Lines                                                                                                      |
| ----------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `create_module`         | Dynamically creates and imports Python modules for testing       | [tests/conftest.py65-102](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L65-L102)   |
| `subprocess_run_code`   | Executes code in a subprocess and captures output                | [tests/conftest.py106-118](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L106-L118) |
| `generate_schema_calls` | Tracks GenerateSchema.generate\_schema call counts               | [tests/conftest.py145-160](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L145-L160) |
| `validate_json_schemas` | Auto-validates generated JSON schemas against Draft 2020-12 spec | [tests/conftest.py164-181](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L164-L181) |
| `disable_error_urls`    | Disables error URLs in output (for stable docs)                  | [tests/conftest.py57-61](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L57-L61)     |

### Module Creation Fixture

The `create_module` fixture enables dynamic module creation for testing:

```
```

This fixture:

1. Extracts source code from functions or uses provided strings
2. Creates temporary Python files with unique names
3. Imports modules with optional assertion rewriting
4. Returns executable module objects for testing

**Sources**: [tests/conftest.py65-102](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L65-L102) [tests/conftest.py30-43](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L30-L43) [tests/conftest.py46-54](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L46-L54)

### Thread Safety Markers

Tests using certain fixtures are automatically marked as `thread_unsafe`:

- `generate_schema_calls` - Monkeypatches Pydantic code
- `benchmark` - Cannot be reused across threads
- `tmp_path`/`tmpdir` - Duplicate paths/dirs
- `copy_method` - Uses `pytest.warns()`
- `reset_plugins` - Monkeypatching

**Sources**: [tests/conftest.py184-202](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L184-L202)

## CI/CD Pipeline

### Main CI Workflow

```
```

**Sources**: [.github/workflows/ci.yml1-436](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L1-L436)

### CI Jobs Breakdown

| Job                             | Purpose                             | Triggers                 | Matrix                   |
| ------------------------------- | ----------------------------------- | ------------------------ | ------------------------ |
| `lint`                          | Pre-commit hooks, ruff, type checks | All pushes/PRs           | Python 3.9-3.14          |
| `docs-build`                    | Validate documentation builds       | All pushes/PRs           | Single Python 3.12       |
| `test`                          | Core test suite                     | All pushes/PRs           | 4 OS × 8 Python versions |
| `test-memray`                   | Memory profiling tests              | All pushes/PRs           | Python 3.12              |
| `test-mypy`                     | Mypy plugin tests                   | All pushes/PRs           | Python 3.13              |
| `test-plugin`                   | Pydantic plugin system tests        | All pushes/PRs           | Python 3.12              |
| `test-typechecking-integration` | Pyright/mypy integration            | All pushes/PRs           | Python 3.12              |
| `coverage-combine`              | Aggregate coverage                  | After tests              | N/A                      |
| `coverage-pr-comment`           | Post coverage to PRs                | After coverage-combine   | N/A                      |
| `release`                       | Publish to PyPI                     | Tags only                | N/A                      |
| `send-tweet`                    | Announce release                    | After successful release | N/A                      |

**Sources**: [.github/workflows/ci.yml17-435](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L17-L435)

### Test Matrix Configuration

The main test job runs across multiple platforms and Python versions:

```
```

Additional PyPy versions tested on Ubuntu only:

- `pypy3.9`
- `pypy3.10`
- `pypy3.11`

**Sources**: [.github/workflows/ci.yml86-111](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L86-L111)

### Coverage Workflow

```
```

**Sources**: [.github/workflows/ci.yml238-303](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L238-L303)

Coverage files are:

1. Generated in each test job with unique filenames
2. Downloaded and combined using `coverage combine`
3. Uploaded as artifacts
4. Used to generate PR comments with coverage percentage

### Release Process

```
```

**Sources**: [.github/workflows/ci.yml352-384](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L352-L384)

The release job:

1. Waits for all CI checks to pass
2. Validates version in `pydantic/version.py` matches git tag
3. Builds distribution using `python -m build`
4. Publishes to PyPI using trusted publishing (OIDC)

**Sources**: [.github/workflows/ci.yml352-384](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L352-L384)

## Third-Party Integration Testing

```
```

**Sources**: [.github/workflows/third-party.yml1-506](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml#L1-L506)

### Third-Party Test Strategy

Each third-party test:

1. Checks out the external project's repository
2. Checks out Pydantic from current branch to `pydantic-latest` path
3. Installs project dependencies
4. Uninstalls locked Pydantic version
5. Installs Pydantic from `pydantic-latest` path in editable mode
6. Runs the project's test suite

Example pattern:

```
```

**Sources**: [.github/workflows/third-party.yml48-73](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml#L48-L73)

### Tested Projects

| Project               | Repository                                 | Python Versions | Special Requirements          |
| --------------------- | ------------------------------------------ | --------------- | ----------------------------- |
| FastAPI               | `fastapi/fastapi`                          | 3.9-3.13        | PYTHONPATH includes docs\_src |
| SQLModel              | `fastapi/sqlmodel`                         | 3.9-3.13        | None                          |
| Beanie                | `BeanieODM/beanie`                         | 3.13 only       | MongoDB service               |
| openapi-python-client | `openapi-generators/openapi-python-client` | 3.9-3.13        | PDM package manager           |
| Pandera               | `unionai-oss/pandera`                      | 3.9-3.12        | Multiple extra dependencies   |
| ODMantic              | `sydney-runkle/odmantic`                   | 3.9-3.11        | MongoDB service               |
| Polar                 | `polarsource/polar`                        | 3.9-3.13        | PostgreSQL, MinIO, Node.js    |
| BentoML               | `bentoml/BentoML`                          | 3.9, 3.11-3.12  | PDM package manager           |
| Semantic Kernel       | `microsoft/semantic-kernel`                | 3.10-3.12       | Poetry package manager        |

**Sources**: [.github/workflows/third-party.yml35-506](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml#L35-L506)

## Documentation System

### MkDocs Configuration

```
```

**Sources**: [mkdocs.yml1-338](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L1-L338) [build-docs.sh1-26](https://github.com/pydantic/pydantic/blob/76ef0b08/build-docs.sh#L1-L26) [.github/workflows/docs-update.yml1-113](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L1-L113)

### Documentation Structure

| Component    | Purpose                                 | Configuration                                                                                         |
| ------------ | --------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Theme        | Material for MkDocs with custom styling | [mkdocs.yml6-47](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L6-L47)                |
| Navigation   | Hierarchical documentation structure    | [mkdocs.yml90-191](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L90-L191)            |
| Mike         | Documentation versioning                | [mkdocs.yml220-222](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L220-L222)          |
| mkdocstrings | API documentation from docstrings       | [mkdocs.yml248-264](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L248-L264)          |
| llmstxt      | LLM-friendly documentation export       | [mkdocs.yml224-241](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L224-L241)          |
| Algolia      | Search integration                      | Custom JS in [mkdocs.yml81-83](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L81-L83) |

**Sources**: [mkdocs.yml1-338](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L1-L338)

### Documentation Build Process

```
```

**Sources**: [.github/workflows/docs-update.yml56-113](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L56-L113)

### Documentation Deployment

The `docs-update.yml` workflow:

1. Triggers on pushes to `main`, `docs-update` branch, or tags

2. Runs lint and test jobs first

3. Checks out `docs-site` branch (orphan branch for built docs)

4. Builds documentation using `mike` for versioning

5. Deploys to `docs-site` branch:

   - `dev` version from `main` branch
   - `X.Y` and `latest` versions from tags

6. Uploads to Algolia for search indexing

**Sources**: [.github/workflows/docs-update.yml1-113](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L1-L113)

### Build Script Symlinks

The build process creates symlinks to provide better source locations in documentation:

```
```

This results in documentation source links like:

- `pydantic_core/core_schema.py`
- Instead of: `.venv/lib/python3.10/site-packages/pydantic_core/core_schema.py`

**Sources**: [build-docs.sh15-22](https://github.com/pydantic/pydantic/blob/76ef0b08/build-docs.sh#L15-L22) [.github/workflows/docs-update.yml84-88](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L84-L88)

## Dependency Management

### UV Lock File and Synchronization

Pydantic uses `uv` for dependency management with a lock file:

- Lock file: `uv.lock` (1+ revision)
- Sync command: `uv sync` with various groups
- Frozen mode: `UV_FROZEN=true` in CI to prevent updates

**Sources**: [uv.lock1-3](https://github.com/pydantic/pydantic/blob/76ef0b08/uv.lock#L1-L3) [.github/workflows/ci.yml13](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L13-L13)

### Dependency Groups

| Group           | Purpose                         | Usage                    |
| --------------- | ------------------------------- | ------------------------ |
| `linting`       | Pre-commit, ruff, type checkers | CI lint job              |
| `docs`          | MkDocs, material theme, plugins | Documentation builds     |
| `docs-upload`   | Algolia upload tools            | Documentation deployment |
| `testing-extra` | pytest, memray, coverage        | Full test suite          |
| `typechecking`  | mypy, pyright, type stubs       | Type checking tests      |
| `all`           | All development dependencies    | Local development        |

**Sources**: [.github/workflows/ci.yml34](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L34-L34) [.github/workflows/docs-update.yml75](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L75-L75)

### Dependency Version Testing

```
```

**Sources**: [.github/workflows/dependencies-check.yml1-54](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/dependencies-check.yml#L1-L54)

The `dependencies-check.yml` workflow:

1. Runs on a schedule (Wednesday and Saturday)
2. Uses `samuelcolvin/list-python-dependencies` to find first and last versions of each dependency
3. Tests Pydantic with both minimum and maximum dependency versions
4. Ensures compatibility across the supported version range

**Sources**: [.github/workflows/dependencies-check.yml1-54](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/dependencies-check.yml#L1-L54)

### Pydantic Family Integration

```
```

**Sources**: [.github/workflows/integration.yml1-40](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/integration.yml#L1-L40)

The integration workflow tests Pydantic with related packages:

- `pydantic-settings`: Settings management library
- `pydantic-extra-types`: Additional type implementations

Both use the `make` targets which likely checkout and test these repositories with the current Pydantic code.

**Sources**: [.github/workflows/integration.yml1-40](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/integration.yml#L1-L40)

## Additional CI Workflows

### Performance Benchmarking (CodSpeed)

```
```

**Sources**: [.github/workflows/codspeed.yml1-83](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/codspeed.yml#L1-L83)

The CodSpeed workflow:

1. Resolves the `pydantic-core` version from `pyproject.toml`
2. Checks out `pydantic-core` at that version
3. Builds `pydantic-core` with PGO (Profile-Guided Optimization) and debug symbols
4. Runs benchmarks using CodSpeed for performance tracking

**Sources**: [.github/workflows/codspeed.yml1-83](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/codspeed.yml#L1-L83)

### Coverage Upload (Smokeshow)

```
```

**Sources**: [.github/workflows/upload-previews.yml1-37](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/upload-previews.yml#L1-L37)

The upload-previews workflow:

1. Triggers after CI workflow completion
2. Downloads coverage HTML artifacts
3. Uploads to Smokeshow for preview hosting
4. Posts coverage percentage to PR as GitHub status with threshold of 91%

**Sources**: [.github/workflows/upload-previews.yml1-37](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/upload-previews.yml#L1-L37)

### Automated Labeling

```
```

**Sources**: [.github/workflows/labeler.yml1-27](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/labeler.yml#L1-L27)

Label configurations:

- `first_pass.yml`: Labels based on branch name patterns (fix, feature, docs, change, performance, packaging)
- `default_pass.yml`: Adds `relnotes-fix` if no labels were applied

This ensures all PRs are properly categorized for changelog generation.

**Sources**: [.github/workflows/labeler.yml1-27](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/labeler.yml#L1-L27) [.github/labels/first\_pass.yml1-18](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/labels/first_pass.yml#L1-L18) [.github/labels/default\_pass.yml1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/labels/default_pass.yml#L1-L5)

## Summary

Pydantic's development and deployment infrastructure provides:

1. **Rigorous Version Control**: Strict compatibility checking between `pydantic` and `pydantic-core`
2. **Comprehensive Testing**: Multi-platform test matrix, third-party integration tests, and specialized testing for memory, type checking, and plugins
3. **Automated CI/CD**: GitHub Actions workflows handle linting, testing, coverage tracking, and deployment
4. **Documentation Excellence**: Versioned documentation with MkDocs, automated deployment, and LLM-friendly exports
5. **Quality Assurance**: Dependency version testing, performance benchmarking, and automated labeling for release notes

The infrastructure ensures that Pydantic maintains high quality standards while supporting a wide range of Python versions, platforms, and downstream packages.

**Sources**: [pydantic/version.py1-114](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L1-L114) [.github/workflows/ci.yml1-436](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/ci.yml#L1-L436) [.github/workflows/third-party.yml1-506](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/third-party.yml#L1-L506) [mkdocs.yml1-338](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L1-L338) [.github/workflows/docs-update.yml1-113](https://github.com/pydantic/pydantic/blob/76ef0b08/.github/workflows/docs-update.yml#L1-L113)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Development and Deployment](#development-and-deployment.md)
- [Overview](#overview.md)
- [Version Management and Compatibility](#version-management-and-compatibility.md)
- [Version Constants and Checking](#version-constants-and-checking.md)
- [Version Information Utility](#version-information-utility.md)
- [Testing Infrastructure](#testing-infrastructure.md)
- [Test Organization and Fixtures](#test-organization-and-fixtures.md)
- [Key Testing Fixtures](#key-testing-fixtures.md)
- [Module Creation Fixture](#module-creation-fixture.md)
- [Thread Safety Markers](#thread-safety-markers.md)
- [CI/CD Pipeline](#cicd-pipeline.md)
- [Main CI Workflow](#main-ci-workflow.md)
- [CI Jobs Breakdown](#ci-jobs-breakdown.md)
- [Test Matrix Configuration](#test-matrix-configuration.md)
- [Coverage Workflow](#coverage-workflow.md)
- [Release Process](#release-process.md)
- [Third-Party Integration Testing](#third-party-integration-testing.md)
- [Third-Party Test Strategy](#third-party-test-strategy.md)
- [Tested Projects](#tested-projects.md)
- [Documentation System](#documentation-system.md)
- [MkDocs Configuration](#mkdocs-configuration.md)
- [Documentation Structure](#documentation-structure.md)
- [Documentation Build Process](#documentation-build-process.md)
- [Documentation Deployment](#documentation-deployment.md)
- [Build Script Symlinks](#build-script-symlinks.md)
- [Dependency Management](#dependency-management.md)
- [UV Lock File and Synchronization](#uv-lock-file-and-synchronization.md)
- [Dependency Groups](#dependency-groups.md)
- [Dependency Version Testing](#dependency-version-testing.md)
- [Pydantic Family Integration](#pydantic-family-integration.md)
- [Additional CI Workflows](#additional-ci-workflows.md)
- [Performance Benchmarking (CodSpeed)](#performance-benchmarking-codspeed.md)
- [Coverage Upload (Smokeshow)](#coverage-upload-smokeshow.md)
- [Automated Labeling](#automated-labeling.md)
- [Summary](#summary.md)
