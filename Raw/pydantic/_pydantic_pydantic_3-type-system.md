Type System | pydantic/pydantic | DeepWiki

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

# Type System

Relevant source files

- [pydantic/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py)
- [pydantic/\_internal/\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py)
- [pydantic/errors.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/errors.py)
- [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)
- [pydantic/functional\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py)
- [pydantic/networks.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py)
- [pydantic/plugin/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py)
- [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)
- [pydantic/root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py)
- [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py)
- [pydantic/types.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py)
- [pydantic/validate\_call\_decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py)
- [pydantic/validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validators.py)
- [tests/test\_networks.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py)
- [tests/test\_plugins.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py)
- [tests/test\_type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py)
- [tests/test\_types.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_types.py)
- [tests/test\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py)

Pydantic's type system provides specialized types for data validation, offers constrainable versions of standard Python types, and implements network-related and other utility types. This document explains the architecture and components of Pydantic's type system, how to use built-in types, and how to extend the system with custom types.

For information about validation and serialization using these types, see [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md). For details about the schema generation process, see [Schema Generation](pydantic/pydantic/5-schema-generation.md).

## Type System Architecture

Pydantic's type system extends Python's built-in type system to provide additional validation capabilities. It consists of several key components:

```
```

Sources: [pydantic/types.py1-110](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L1-L110), [pydantic/networks.py1-67](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L1-L67)

## Core Type Concepts

### Constrained Types and Annotations

Pydantic supports two approaches for adding constraints to types:

1. **Constrained Type Functions**: Functions like `conint()`, `constr()`, etc.
2. **Annotated with Field Constraints**: Using Python's `Annotated` with field constraints

```
```

Sources: [pydantic/types.py111-146](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L111-L146) [pydantic/types.py147-219](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L147-L219) [pydantic/types.py661-685](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L661-L685)

The two approaches serve the same purpose with different syntax:

```
# Using constrained type function
from pydantic import BaseModel, conint

class Model(BaseModel):
    value: conint(gt=0, lt=100)

# Using Annotated with Field
from typing import Annotated
from pydantic import BaseModel, Field

class Model(BaseModel):
    value: Annotated[int, Field(gt=0, lt=100)]
```

The latter approach using `Annotated` is recommended for better support with static analysis tools.

### Strict Mode

Pydantic allows enforcing strict type checking using the `Strict` class:

```
```

Sources: [pydantic/types.py113-146](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L113-L146)

## Constrained Types

### Numeric Types

Pydantic provides constrained versions of numeric types with validation rules:

| Type               | Description                      | Constraints                                              |
| ------------------ | -------------------------------- | -------------------------------------------------------- |
| `conint()`         | Constrained integer              | `gt`, `ge`, `lt`, `le`, `multiple_of`                    |
| `PositiveInt`      | Integer > 0                      | Equivalent to `Annotated[int, Gt(0)]`                    |
| `NegativeInt`      | Integer < 0                      | Equivalent to `Annotated[int, Lt(0)]`                    |
| `NonNegativeInt`   | Integer >= 0                     | Equivalent to `Annotated[int, Ge(0)]`                    |
| `NonPositiveInt`   | Integer <= 0                     | Equivalent to `Annotated[int, Le(0)]`                    |
| `confloat()`       | Constrained float                | `gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan`   |
| `PositiveFloat`    | Float > 0                        | Equivalent to `Annotated[float, Gt(0)]`                  |
| `NegativeFloat`    | Float < 0                        | Equivalent to `Annotated[float, Lt(0)]`                  |
| `NonNegativeFloat` | Float >= 0                       | Equivalent to `Annotated[float, Ge(0)]`                  |
| `NonPositiveFloat` | Float <= 0                       | Equivalent to `Annotated[float, Le(0)]`                  |
| `FiniteFloat`      | Float that is not `inf` or `nan` | Equivalent to `Annotated[float, AllowInfNan(False)]`     |
| `condecimal()`     | Constrained decimal              | Similar to `confloat()` + `max_digits`, `decimal_places` |

Sources: [pydantic/types.py147-362](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L147-L362) [pydantic/types.py386-645](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L386-L645)

### String Types

Pydantic offers string constraints through `constr()` and `StringConstraints`:

```
```

Sources: [pydantic/types.py690-828](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L690-L828)

Similar constraints exist for bytes with `conbytes()`.

### Collection Types

Pydantic provides constrained collection types:

| Type             | Description           | Constraints                             |
| ---------------- | --------------------- | --------------------------------------- |
| `conlist()`      | Constrained list      | `item_type`, `min_length`, `max_length` |
| `conset()`       | Constrained set       | `item_type`, `min_length`, `max_length` |
| `confrozenset()` | Constrained frozenset | `item_type`, `min_length`, `max_length` |

Sources: [pydantic/types.py836-903](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L836-L903)

## Network Types

Pydantic includes a rich set of network-related types defined in `networks.py`:

```
```

Sources: [pydantic/networks.py70-526](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L70-L526) [pydantic/networks.py534-669](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L534-L669)

Network types provide specialized validation:

- URL types validate and normalize URLs with various schemes
- Email types validate email addresses
- IP types validate IPv4 and IPv6 addresses, networks, and interfaces

These network types can be directly used in models:

```
```

## Special Types

### Path Types

Path-related types provide validation for file system paths:

| Type            | Description                               |
| --------------- | ----------------------------------------- |
| `FilePath`      | Path that points to an existing file      |
| `DirectoryPath` | Path that points to an existing directory |
| `NewPath`       | Path that does not currently exist        |
| `SocketPath`    | Path pointing to a Unix socket            |

Sources: [pydantic/\_\_init\_\_.py73-77](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py#L73-L77) [pydantic/\_\_init\_\_.py357-359](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py#L357-L359)

### Secret Types

Secret types provide special handling for sensitive data:

| Type          | Description                            |
| ------------- | -------------------------------------- |
| `SecretStr`   | String that hides its contents in repr |
| `SecretBytes` | Bytes that hides its contents in repr  |
| `Secret`      | Generic version of secret types        |

Sources: [pydantic/\_\_init\_\_.py78-80](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py#L78-L80) [pydantic/\_\_init\_\_.py348-350](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py#L348-L350)

### ImportString Type

`ImportString` provides a way to import Python objects from strings:

```
```

Sources: [pydantic/types.py906-1028](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L906-L1028)

## Type Adapter

The `TypeAdapter` class provides a way to use Pydantic's validation system outside of models:

```
```

Sources: [pydantic/\_\_init\_\_.py380](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py#L380-L380)

The TypeAdapter makes it easy to apply Pydantic validation to standalone types:

```
```

## Working with Annotated Types

Pydantic provides special handling for Python's `Annotated` type:

```
```

Sources: [pydantic/\_internal/\_known\_annotated\_metadata.py1-42](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_known_annotated_metadata.py#L1-L42)

`Annotated` provides a clean way to combine type information with metadata:

```
```

## Creating Custom Types

Pydantic allows for creation of custom types by implementing `__get_pydantic_core_schema__` method:

```
```

Sources: [pydantic/\_internal/\_validators.py66-127](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validators.py#L66-L127)

## Internal Validation Process

The type system works with Pydantic's validation engine:

```
```

Sources: [pydantic/\_internal/\_core\_utils.py43-66](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_utils.py#L43-L66) [pydantic/\_internal/\_validators.py66-127](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validators.py#L66-L127)

## Constraints Reference

| Type Category | Available Constraints                                                                       |
| ------------- | ------------------------------------------------------------------------------------------- |
| String        | `min_length`, `max_length`, `pattern`, `strip_whitespace`, `to_lower`, `to_upper`, `strict` |
| Bytes         | `min_length`, `max_length`, `strict`                                                        |
| List          | `min_length`, `max_length`, `strict`, `fail_fast`                                           |
| Set           | `min_length`, `max_length`, `strict`, `fail_fast`                                           |
| Dict          | `min_length`, `max_length`, `strict`                                                        |
| Float         | `gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan`, `strict`                            |
| Integer       | `gt`, `ge`, `lt`, `le`, `multiple_of`, `strict`                                             |
| Decimal       | `gt`, `ge`, `lt`, `le`, `multiple_of`, `max_digits`, `decimal_places`, `strict`             |

Sources: [pydantic/\_internal/\_known\_annotated\_metadata.py18-64](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_known_annotated_metadata.py#L18-L64)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Type System](#type-system.md)
- [Type System Architecture](#type-system-architecture.md)
- [Core Type Concepts](#core-type-concepts.md)
- [Constrained Types and Annotations](#constrained-types-and-annotations.md)
- [Strict Mode](#strict-mode.md)
- [Constrained Types](#constrained-types.md)
- [Numeric Types](#numeric-types.md)
- [String Types](#string-types.md)
- [Collection Types](#collection-types.md)
- [Network Types](#network-types.md)
- [Special Types](#special-types.md)
- [Path Types](#path-types.md)
- [Secret Types](#secret-types.md)
- [ImportString Type](#importstring-type.md)
- [Type Adapter](#type-adapter.md)
- [Working with Annotated Types](#working-with-annotated-types.md)
- [Creating Custom Types](#creating-custom-types.md)
- [Internal Validation Process](#internal-validation-process.md)
- [Constraints Reference](#constraints-reference.md)
