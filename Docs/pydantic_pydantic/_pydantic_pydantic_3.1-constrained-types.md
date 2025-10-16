Constrained Types | pydantic/pydantic | DeepWiki

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

# Constrained Types

Relevant source files

- [pydantic/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py)
- [pydantic/errors.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/errors.py)
- [pydantic/networks.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py)
- [pydantic/types.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py)
- [pydantic/validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validators.py)
- [tests/test\_networks.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py)
- [tests/test\_types.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_types.py)

Constrained Types in Pydantic provide a way to define additional restrictions on basic Python types, such as strings, integers, floats, and collections. These types ensure that values not only match the expected type but also comply with specific constraints like minimum/maximum values, string patterns, or collection lengths.

This page explains the various constrained types available in Pydantic, how they are implemented, and how to use them effectively. For information about custom types and validators, see [Type System](pydantic/pydantic/3-type-system.md).

## Constrained Types Overview

Constrained types are a key part of Pydantic's validation system. They extend basic Python types with additional validation requirements that are checked during model instantiation.

```
```

Sources: [pydantic/types.py149-832](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L149-L832) [pydantic/types.py836-904](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L836-L904)

The constrained types in Pydantic come in two forms:

1. **Constraint Functions**: Functions like `constr()`, `conint()` that return a constrained version of a type
2. **Predefined Constrained Types**: Ready-to-use types like `PositiveInt`, `StrictStr`, etc.

Since Pydantic v2, the recommended approach is to use Python's `Annotated` type with field constraints rather than the legacy constraint functions.

## Numeric Constrained Types

Pydantic provides constrained types for integers, floats, and decimals with various validation rules.

### Integer Constraints

```
```

Sources: [pydantic/types.py151-235](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L151-L235) [pydantic/types.py238-363](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L238-L363)

The `conint` function creates a constrained integer type with the following parameters:

- `strict`: When True, input must be an actual integer (not float or string)
- `gt`: Greater than (exclusive lower bound)
- `ge`: Greater than or equal (inclusive lower bound)
- `lt`: Less than (exclusive upper bound)
- `le`: Less than or equal (inclusive upper bound)
- `multiple_of`: Input must be a multiple of this value

Pydantic also provides several predefined integer constrained types:

| Type             | Description                      | Implementation                          |
| ---------------- | -------------------------------- | --------------------------------------- |
| `PositiveInt`    | Integer > 0                      | `Annotated[int, annotated_types.Gt(0)]` |
| `NegativeInt`    | Integer < 0                      | `Annotated[int, annotated_types.Lt(0)]` |
| `NonNegativeInt` | Integer ≥ 0                      | `Annotated[int, annotated_types.Ge(0)]` |
| `NonPositiveInt` | Integer ≤ 0                      | `Annotated[int, annotated_types.Le(0)]` |
| `StrictInt`      | Integer validated in strict mode | `Annotated[int, Strict()]`              |

### Float Constraints

```
```

Sources: [pydantic/types.py411-497](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L411-L497) [pydantic/types.py500-645](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L500-L645)

The `confloat` function creates a constrained float type with the same parameters as `conint`, plus:

- `allow_inf_nan`: When True, allows infinity and NaN values

Predefined float constrained types include:

| Type               | Description                    | Implementation                            |
| ------------------ | ------------------------------ | ----------------------------------------- |
| `PositiveFloat`    | Float > 0                      | `Annotated[float, annotated_types.Gt(0)]` |
| `NegativeFloat`    | Float < 0                      | `Annotated[float, annotated_types.Lt(0)]` |
| `NonNegativeFloat` | Float ≥ 0                      | `Annotated[float, annotated_types.Ge(0)]` |
| `NonPositiveFloat` | Float ≤ 0                      | `Annotated[float, annotated_types.Le(0)]` |
| `StrictFloat`      | Float validated in strict mode | `Annotated[float, Strict(True)]`          |
| `FiniteFloat`      | Float that must be finite      | `Annotated[float, AllowInfNan(False)]`    |

## String Constrained Types

Pydantic provides string constraints through the `constr` function and `StringConstraints` class.

```
```

Sources: [pydantic/types.py693-829](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L693-L829) [pydantic/types.py831-832](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L831-L832)

The `constr` function creates a constrained string type with the following parameters:

- `strip_whitespace`: When True, strips leading and trailing whitespace
- `to_upper`: When True, converts the string to uppercase
- `to_lower`: When True, converts the string to lowercase
- `strict`: When True, input must be an actual string
- `min_length`: Minimum string length
- `max_length`: Maximum string length
- `pattern`: Regex pattern that the string must match

In Pydantic v2, the recommended approach is to use `Annotated` with `StringConstraints` instead of `constr`:

```
```

## Collection Constrained Types

Pydantic provides constrained types for various collection types: lists, sets, frozensets, and bytes.

```
```

Sources: [pydantic/types.py663-684](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L663-L684) [pydantic/types.py839-904](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L839-L904)

### Bytes Constraints

The `conbytes` function creates a constrained bytes type with parameters:

- `min_length`: Minimum length in bytes
- `max_length`: Maximum length in bytes
- `strict`: When True, input must be an actual bytes object

### List Constraints

The `conlist` function creates a constrained list type with parameters:

- `item_type`: The type of items in the list
- `min_length`: Minimum number of items
- `max_length`: Maximum number of items

### Set and FrozenSet Constraints

The `conset` and `confrozenset` functions create constrained set and frozenset types with similar parameters:

- `item_type`: The type of items in the set
- `min_length`: Minimum number of items
- `max_length`: Maximum number of items

## Usage Patterns

### Using Constrained Types in Models

```
```

### Modern Approach with Annotated

```
```

## Integration with Schema Generation

Constrained types automatically generate appropriate schema information that is used for validation and JSON Schema generation.

```
```

Sources: [pydantic/types.py151-235](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L151-L235) [pydantic/types.py411-497](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L411-L497) [pydantic/types.py750-828](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py#L750-L828)

When a constrained type is used in a Pydantic model:

1. The constraint is transformed into an `Annotated` type during schema generation
2. The Pydantic validation engine uses these constraints to validate inputs
3. JSON Schema generation includes the constraints in the resulting schema

## Best Practices

### Prefer Annotated over Constraint Functions

Pydantic recommends using `Annotated` with constraints rather than the legacy constraint functions:

```
```

The `conX` functions will be deprecated in Pydantic 3.0 in favor of the `Annotated` approach, which provides better static type checking and IDE support.

### Common Use Cases

1. **Validation with Transformation**:

   ```
   ```

2. **Numeric Ranges**:

   ```
   ```

3. **Pattern Matching**:

   ```
   ```

## Testing Constrained Types

When testing models with constrained types, it's important to test both valid and invalid inputs to ensure constraints are applied correctly:

```
```

Sources: [tests/test\_types.py741-821](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_types.py#L741-L821) [tests/test\_types.py246-347](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_types.py#L246-L347)

## Related Features

Constrained types work well with other Pydantic features:

- **Field validators**: Apply custom validation logic beyond built-in constraints
- **Type adapters**: Use constrained types with `TypeAdapter` for validation outside of models
- **JSON Schema**: Constrained types generate appropriate JSON schema representations

For more information on related features, see:

- [Field System](pydantic/pydantic/2.2-field-system.md) for details on field configuration and validators
- [Type Adapter](pydantic/pydantic/3.3-typeadapter.md) for using constrained types outside of models
- [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md) for how constraints appear in JSON schemas

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Constrained Types](#constrained-types.md)
- [Constrained Types Overview](#constrained-types-overview.md)
- [Numeric Constrained Types](#numeric-constrained-types.md)
- [Integer Constraints](#integer-constraints.md)
- [Float Constraints](#float-constraints.md)
- [String Constrained Types](#string-constrained-types.md)
- [Collection Constrained Types](#collection-constrained-types.md)
- [Bytes Constraints](#bytes-constraints.md)
- [List Constraints](#list-constraints.md)
- [Set and FrozenSet Constraints](#set-and-frozenset-constraints.md)
- [Usage Patterns](#usage-patterns.md)
- [Using Constrained Types in Models](#using-constrained-types-in-models.md)
- [Modern Approach with Annotated](#modern-approach-with-annotated.md)
- [Integration with Schema Generation](#integration-with-schema-generation.md)
- [Best Practices](#best-practices.md)
- [Prefer Annotated over Constraint Functions](#prefer-annotated-over-constraint-functions.md)
- [Common Use Cases](#common-use-cases.md)
- [Testing Constrained Types](#testing-constrained-types.md)
- [Related Features](#related-features.md)
