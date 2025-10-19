Function Validation | pydantic/pydantic | DeepWiki

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

# Function Validation

Relevant source files

- [pydantic/\_internal/\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py)
- [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)
- [pydantic/functional\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py)
- [pydantic/plugin/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py)
- [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)
- [pydantic/root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py)
- [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py)
- [pydantic/validate\_call\_decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py)
- [tests/test\_plugins.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py)
- [tests/test\_type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py)
- [tests/test\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py)

## Overview

Function validation in Pydantic enables automatic validation of function arguments and return values using the `@validate_call` decorator. This system extends Pydantic's validation capabilities beyond models to regular Python functions, methods, and lambdas by transforming function signatures into validation schemas and wrapping function calls with validation logic.

For field-level validation within models, see [Validators](pydantic/pydantic/4.1-validators.md). For model-level validation, see [Model Configuration](pydantic/pydantic/2.3-model-configuration.md).

**Sources:** [pydantic/validate\_call\_decorator.py1-117](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L1-L117)

## Decorator Interface

The `@validate_call` decorator is the primary entry point for function validation. It can be applied either as a bare decorator or with configuration options:

```
```

### Decorator Parameters

| Parameter         | Type               | Description                                                      |
| ----------------- | ------------------ | ---------------------------------------------------------------- |
| `func`            | Callable or None   | The function to validate (when used as bare decorator)           |
| `config`          | ConfigDict or None | Configuration dictionary for validation behavior                 |
| `validate_return` | bool               | Whether to validate the function's return value (default: False) |

The decorator supports various callable types defined in `VALIDATE_CALL_SUPPORTED_TYPES`:

- Regular functions
- Methods (instance, class, static)
- Lambda functions
- `functools.partial` objects

**Sources:** [pydantic/validate\_call\_decorator.py72-117](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L72-L117) [tests/test\_validate\_call.py28-59](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L28-L59)

## Validation Flow Architecture

```
```

**Sources:** [pydantic/validate\_call\_decorator.py24-70](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L24-L70) [pydantic/\_internal/\_validate\_call.py49-141](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L49-L141)

## ValidateCallWrapper Implementation

The `ValidateCallWrapper` class handles the core logic of function validation. It wraps the original function and intercepts all calls to perform validation.

### Core Components

```
```

### Initialization Process

The wrapper is initialized in `__init__` with the following steps:

1. **Extract function metadata**: Store the function, extract its module and qualname
2. **Create namespace resolver**: Build `NsResolver` to handle forward references in type annotations
3. **Configure wrapper**: Create `ConfigWrapper` from provided config
4. **Conditional schema building**: If `defer_build` is not enabled, immediately create validators; otherwise defer until first call

**Sources:** [pydantic/\_internal/\_validate\_call.py65-90](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L65-L90)

### Validator Creation

The `_create_validators` method generates schemas and validators:

```
```

**Sources:** [pydantic/\_internal/\_validate\_call.py91-131](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L91-L131)

### Call Interception

When the wrapped function is called, the `__call__` method:

1. **Lazy validation setup**: If validators weren't created during initialization (deferred build), create them now
2. **Package arguments**: Wrap positional and keyword arguments in `ArgsKwargs` object
3. **Validate arguments**: Pass through `__pydantic_validator__`
4. **Execute function**: Call the validated function with validated args
5. **Validate return** (optional): Pass return value through `__return_pydantic_validator__` if configured

**Sources:** [pydantic/\_internal/\_validate\_call.py132-141](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L132-L141)

## Function Schema Generation

Function signatures are transformed into pydantic-core schemas through the `GenerateSchema` class. This enables the same validation logic used for models to work with functions.

### Argument Types and Schema Mapping

| Argument Kind                 | Schema Type                                   | Example                                   |
| ----------------------------- | --------------------------------------------- | ----------------------------------------- |
| Positional-only (`/`)         | `arguments_schema` with positional parameters | `def f(a, /, b): ...`                     |
| Keyword-only (`*`)            | `arguments_schema` with keyword parameters    | `def f(*, a, b): ...`                     |
| Variable positional (`*args`) | `arguments_schema` with var\_args\_schema     | `def f(*args): ...`                       |
| Variable keyword (`**kwargs`) | `arguments_schema` with var\_kwargs\_schema   | `def f(**kwargs): ...`                    |
| Mixed                         | Combined `arguments_schema`                   | `def f(a, /, b, *args, c, **kwargs): ...` |

### Special Handling: TypedDict Unpacking

When using `Unpack[TypedDict]` for `**kwargs`, the decorator validates kwargs against the TypedDict schema:

```
```

The implementation checks for overlaps between regular parameters and TypedDict keys, raising `PydanticUserError` if positional-or-keyword parameters conflict with TypedDict keys.

**Sources:** [tests/test\_validate\_call.py286-417](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L286-L417)

## Function Type Validation

The `_check_function_type` function validates that the decorated object is a supported callable type:

```
```

**Sources:** [pydantic/validate\_call\_decorator.py24-70](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L24-L70)

## Advanced Features

### Return Value Validation

When `validate_return=True`, the decorator validates the function's return value against its return type annotation:

```
```

The implementation creates a separate validator for the return type and wraps the result in an appropriate handler (async or sync).

**Sources:** [pydantic/\_internal/\_validate\_call.py105-128](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L105-L128)

### Async Function Support

The wrapper detects coroutine functions using `inspect.iscoroutinefunction` and creates appropriate wrappers:

- For regular functions: Direct validation wrapper
- For async functions: Async wrapper that awaits the coroutine before/after validation

The `update_wrapper_attributes` function ensures the wrapper preserves the async nature of the original function.

**Sources:** [pydantic/\_internal/\_validate\_call.py28-46](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L28-L46)

### Configuration Options

All `ConfigDict` options are supported:

```
```

**Sources:** [tests/test\_validate\_call.py730-776](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L730-L776)

### Field-Level Annotations

Function parameters support Pydantic's `Field` and `Annotated` for additional validation:

```
```

**Sources:** [tests/test\_validate\_call.py419-436](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L419-L436) [tests/test\_validate\_call.py778-796](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L778-L796)

## Integration with Plugin System

The `validate_call` decorator integrates with Pydantic's plugin system through the `create_schema_validator` function. When plugins are installed, they receive notifications about function validation:

```
```

Plugins receive:

- `schema_kind='validate_call'`
- `schema_type`: The original function
- `schema_type_path`: Module and qualname of the function

**Sources:** [pydantic/\_internal/\_validate\_call.py96-104](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L96-L104) [tests/test\_plugins.py410-447](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L410-L447)

## JSON Schema Generation

Functions decorated with `@validate_call` can generate JSON schemas through `TypeAdapter`:

```
```

The schema generation handles:

- Positional-only arguments → array schema with `prefixItems`
- Keyword-only arguments → object schema with `properties`
- Mixed argument types → raises `PydanticInvalidForJsonSchema`
- Variable arguments (`*args`) → array schema with `items`
- Variable keyword arguments (`**kwargs`) → object schema with `additionalProperties`

**Sources:** [tests/test\_validate\_call.py626-707](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L626-L707)

## Error Handling and Validation Errors

Validation errors from `@validate_call` decorated functions follow the same structure as model validation errors:

```
```

Common error types:

- `missing_argument`: Required argument not provided
- `unexpected_positional_argument`: Too many positional args
- `unexpected_keyword_argument`: Unknown keyword arg
- `multiple_argument_values`: Argument provided both positionally and by keyword
- `missing_positional_only_argument`: Positional-only arg passed as keyword
- `missing_keyword_only_argument`: Keyword-only arg passed positionally

**Sources:** [tests/test\_validate\_call.py152-201](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L152-L201)

## Wrapper Attribute Preservation

The `update_wrapper_attributes` function ensures the decorated function preserves key attributes:

```
```

For `partial` objects, special handling generates names like `partial(func_name)`.

**Sources:** [pydantic/\_internal/\_validate\_call.py18-46](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L18-L46) [tests/test\_validate\_call.py28-53](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L28-L53)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Function Validation](#function-validation.md)
- [Overview](#overview.md)
- [Decorator Interface](#decorator-interface.md)
- [Decorator Parameters](#decorator-parameters.md)
- [Validation Flow Architecture](#validation-flow-architecture.md)
- [ValidateCallWrapper Implementation](#validatecallwrapper-implementation.md)
- [Core Components](#core-components.md)
- [Initialization Process](#initialization-process.md)
- [Validator Creation](#validator-creation.md)
- [Call Interception](#call-interception.md)
- [Function Schema Generation](#function-schema-generation.md)
- [Argument Types and Schema Mapping](#argument-types-and-schema-mapping.md)
- [Special Handling: TypedDict Unpacking](#special-handling-typeddict-unpacking.md)
- [Function Type Validation](#function-type-validation.md)
- [Advanced Features](#advanced-features.md)
- [Return Value Validation](#return-value-validation.md)
- [Async Function Support](#async-function-support.md)
- [Configuration Options](#configuration-options.md)
- [Field-Level Annotations](#field-level-annotations.md)
- [Integration with Plugin System](#integration-with-plugin-system.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [Error Handling and Validation Errors](#error-handling-and-validation-errors.md)
- [Wrapper Attribute Preservation](#wrapper-attribute-preservation.md)
