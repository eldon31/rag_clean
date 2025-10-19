Testing Framework | pydantic/pydantic | DeepWiki

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

# Testing Framework

Relevant source files

- [tests/conftest.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py)

## Purpose and Scope

This document covers Pydantic's testing infrastructure, including pytest configuration, test fixtures, module creation utilities, and validation helpers. The framework provides tools for dynamic module creation, JSON schema validation, schema generation monitoring, and thread safety management across the test suite.

For information about CI/CD pipelines and automation, see [CI/CD Pipeline](pydantic/pydantic/7.2-cicd-pipeline.md). For documentation building and testing, see [Documentation System](pydantic/pydantic/7.3-documentation-system.md).

---

## Test Configuration Architecture

The testing framework is built on pytest and configured through `tests/conftest.py`. The configuration system provides command-line options, session-wide settings, and automatic test collection hooks.

```
```

**Sources:** [tests/conftest.py25-28](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L25-L28) [tests/conftest.py57-62](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L57-L62) [tests/conftest.py198-203](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L198-L203)

### Command-Line Options

The framework defines custom pytest options through the `pytest_addoption` hook:

| Option          | Purpose                         | Usage                  |
| --------------- | ------------------------------- | ---------------------- |
| `--test-mypy`   | Enable mypy type checking tests | `pytest --test-mypy`   |
| `--update-mypy` | Update mypy test baselines      | `pytest --update-mypy` |

**Sources:** [tests/conftest.py25-28](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L25-L28)

### Session-Wide Configuration

The `disable_error_urls` fixture runs once per test session and sets an environment variable to prevent Pydantic from including documentation URLs in error messages during tests. This prevents version-specific URLs from appearing in test outputs that would need frequent updating.

**Sources:** [tests/conftest.py57-62](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L57-L62)

---

## Test Fixtures

Pydantic's test suite provides several specialized fixtures for common testing patterns. These fixtures handle module creation, subprocess execution, schema generation monitoring, and JSON schema validation.

```
```

**Sources:** [tests/conftest.py64-182](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L64-L182)

### Fixture Catalog

| Fixture                 | Scope    | Purpose                                        |
| ----------------------- | -------- | ---------------------------------------------- |
| `disable_error_urls`    | session  | Disables error URL generation globally         |
| `create_module`         | function | Creates and imports Python modules dynamically |
| `subprocess_run_code`   | function | Executes code in isolated subprocess           |
| `generate_schema_calls` | function | Monitors and counts schema generation calls    |
| `validate_json_schemas` | function | Validates generated JSON schemas automatically |

**Sources:** [tests/conftest.py57-182](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L57-L182)

---

## Dynamic Module Creation

The `create_module` fixture enables tests to create and import Python modules on-the-fly from source code strings or function bodies. This is essential for testing import-time behaviors, module-level validation, and schema caching.

### Module Creation Pipeline

```
```

**Sources:** [tests/conftest.py30-103](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L30-L103)

### Function Source Code Extraction

The `_extract_source_code_from_function` helper extracts the body of a test function, enabling a decorator-like pattern for module creation:

```
```

The function:

1. Validates that the function has no arguments ([tests/conftest.py31-32](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L31-L32))
2. Uses `inspect.getsource()` to get source code ([tests/conftest.py36](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L36-L36))
3. Skips the `def` line ([tests/conftest.py37-39](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L37-L39))
4. Dedents and returns the body ([tests/conftest.py43](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L43-L43))

**Sources:** [tests/conftest.py30-44](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L30-L44)

### Module File Creation

The `_create_module_file` function handles platform-specific file creation:

| Concern            | Implementation                                                                                                                          |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Path length limits | Maximum 240 characters on Windows ([tests/conftest.py48](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L48-L48)) |
| Invalid characters | Sanitizes `<>:"/\|?*` characters ([tests/conftest.py50](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L50-L50))  |
| Name collisions    | Appends 5-byte random hex token ([tests/conftest.py51](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L51-L51))   |
| File extension     | Always uses `.py` extension ([tests/conftest.py52](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L52-L52))       |

**Sources:** [tests/conftest.py46-54](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L46-L54)

### Assertion Rewriting

When `rewrite_assertions=True` (default), the fixture uses pytest's `AssertionRewritingHook` to enable detailed assertion failure messages. This hook rewrites Python assert statements at import time to provide better debugging information.

**Sources:** [tests/conftest.py91-96](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L91-L96)

---

## Subprocess Code Execution

The `subprocess_run_code` fixture provides process-isolated code execution, essential for testing import-time side effects, environment isolation, and subprocess-specific behaviors.

```
```

**Sources:** [tests/conftest.py105-119](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L105-L119)

The fixture creates a temporary `test.py` file and executes it with `subprocess.check_output`, returning the captured stdout as a UTF-8 string. This ensures complete process isolation between test execution and the code being tested.

---

## Schema Generation Monitoring

The `generate_schema_calls` fixture tracks how many times schema generation occurs, useful for testing caching behaviors and performance optimizations.

### Call Counter Implementation

```
```

**Sources:** [tests/conftest.py144-161](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L144-L161)

The fixture uses a depth counter to handle recursive `GenerateSchema.generate_schema` calls - only root-level calls increment the counter. This prevents double-counting when schema generation triggers nested schema generation.

**Data Structures:**

- `CallCounter` dataclass with `count` field and `reset()` method ([tests/conftest.py136-142](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L136-L142))
- `depth` variable tracks recursion level ([tests/conftest.py148](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L148-L148))

**Sources:** [tests/conftest.py136-161](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L136-L161)

---

## JSON Schema Validation

The `validate_json_schemas` fixture automatically validates all generated JSON schemas against the Draft 2020-12 specification. This runs for every test unless explicitly disabled.

### Validation Flow

```
```

**Sources:** [tests/conftest.py163-182](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L163-L182)

### Opting Out of Validation

Tests can disable automatic JSON schema validation using the `skip_json_schema_validation` marker:

```
```

The marker is checked via `request.node.get_closest_marker()` ([tests/conftest.py169](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L169-L169)), and validation is skipped if found.

**Sources:** [tests/conftest.py169-177](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L169-L177)

---

## Thread Safety Management

The test framework includes sophisticated thread safety detection to prevent race conditions when running tests in parallel with `pytest-run-parallel`.

### Thread-Unsafe Fixtures

```
```

**Sources:** [tests/conftest.py184-203](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L184-L203)

### Thread-Unsafe Fixture List

The following fixtures are marked as thread-unsafe:

| Fixture                 | Reason                                         |
| ----------------------- | ---------------------------------------------- |
| `generate_schema_calls` | Monkeypatches global Pydantic code             |
| `benchmark`             | Fixture cannot be reused across threads        |
| `tmp_path` / `tmpdir`   | Risk of duplicate path creation                |
| `copy_method`           | Uses `pytest.warns()` which is not thread-safe |
| `reset_plugins`         | Monkeypatches global state                     |

**Sources:** [tests/conftest.py184-191](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L184-L191)

### Collection Hook Timing

The thread safety marker is added in `pytest_itemcollected`, which is critical because:

- `pytest-run-parallel` also implements this hook
- Pydantic's hook runs before the parallel plugin's hook
- Markers must be applied before the parallel plugin analyzes tests
- Using later hooks like `pytest_collection_modifyitems` would be too late

**Sources:** [tests/conftest.py194-198](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L194-L198)

---

## Test Utility Classes

The testing framework provides utility dataclasses for common testing patterns.

### Err Dataclass

```
```

**Sources:** [tests/conftest.py121-134](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L121-L134)

The `Err` dataclass represents expected validation errors in tests:

| Field     | Type          | Purpose                             |
| --------- | ------------- | ----------------------------------- |
| `message` | `str`         | Expected error message text         |
| `errors`  | `Any \| None` | Optional detailed error information |

**Methods:**

- `__repr__()`: Custom string representation ([tests/conftest.py126-130](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L126-L130))
- `message_escaped()`: Returns regex-escaped message for pattern matching ([tests/conftest.py132-133](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L132-L133))

**Sources:** [tests/conftest.py121-134](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L121-L134)

### CallCounter Dataclass

```
```

**Sources:** [tests/conftest.py136-142](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L136-L142)

The `CallCounter` dataclass provides a simple mutable counter:

| Field   | Type  | Default | Purpose                  |
| ------- | ----- | ------- | ------------------------ |
| `count` | `int` | `0`     | Number of calls recorded |

**Methods:**

- `reset()`: Resets count to zero ([tests/conftest.py140-141](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L140-L141))

This is used by the `generate_schema_calls` fixture to track schema generation invocations.

**Sources:** [tests/conftest.py136-142](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L136-L142)

---

## Summary

The Pydantic testing framework provides a comprehensive infrastructure for testing validation logic, schema generation, and type handling:

| Component            | Purpose                                | Key Classes/Functions                                                        |
| -------------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| pytest configuration | Command-line options and session setup | `pytest_addoption`, `disable_error_urls`                                     |
| Module creation      | Dynamic module import for testing      | `create_module`, `_extract_source_code_from_function`, `_create_module_file` |
| Subprocess execution | Process-isolated code testing          | `subprocess_run_code`                                                        |
| Schema monitoring    | Track schema generation calls          | `generate_schema_calls`, `CallCounter`                                       |
| JSON validation      | Automatic schema validation            | `validate_json_schemas`, `Draft202012Validator`                              |
| Thread safety        | Parallel test execution safety         | `pytest_itemcollected`, `_thread_unsafe_fixtures`                            |
| Utilities            | Common test patterns                   | `Err`, `CallCounter`                                                         |

**Sources:** [tests/conftest.py1-203](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/conftest.py#L1-L203)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Testing Framework](#testing-framework.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Test Configuration Architecture](#test-configuration-architecture.md)
- [Command-Line Options](#command-line-options.md)
- [Session-Wide Configuration](#session-wide-configuration.md)
- [Test Fixtures](#test-fixtures.md)
- [Fixture Catalog](#fixture-catalog.md)
- [Dynamic Module Creation](#dynamic-module-creation.md)
- [Module Creation Pipeline](#module-creation-pipeline.md)
- [Function Source Code Extraction](#function-source-code-extraction.md)
- [Module File Creation](#module-file-creation.md)
- [Assertion Rewriting](#assertion-rewriting.md)
- [Subprocess Code Execution](#subprocess-code-execution.md)
- [Schema Generation Monitoring](#schema-generation-monitoring.md)
- [Call Counter Implementation](#call-counter-implementation.md)
- [JSON Schema Validation](#json-schema-validation.md)
- [Validation Flow](#validation-flow.md)
- [Opting Out of Validation](#opting-out-of-validation.md)
- [Thread Safety Management](#thread-safety-management.md)
- [Thread-Unsafe Fixtures](#thread-unsafe-fixtures.md)
- [Thread-Unsafe Fixture List](#thread-unsafe-fixture-list.md)
- [Collection Hook Timing](#collection-hook-timing.md)
- [Test Utility Classes](#test-utility-classes.md)
- [Err Dataclass](#err-dataclass.md)
- [CallCounter Dataclass](#callcounter-dataclass.md)
- [Summary](#summary.md)
