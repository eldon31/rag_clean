Migration and Compatibility | pydantic/pydantic | DeepWiki

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

# Backward Compatibility and Migration

Relevant source files

- [.pre-commit-config.yaml](https://github.com/pydantic/pydantic/blob/76ef0b08/.pre-commit-config.yaml)
- [docs/concepts/config.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/config.md)
- [docs/concepts/dataclasses.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/dataclasses.md)
- [docs/concepts/json.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/json.md)
- [docs/concepts/json\_schema.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/json_schema.md)
- [docs/concepts/models.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/models.md)
- [docs/concepts/performance.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/performance.md)
- [docs/concepts/serialization.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/serialization.md)
- [docs/concepts/validators.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/validators.md)
- [docs/contributing.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/contributing.md)
- [docs/examples/custom\_validators.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/examples/custom_validators.md)
- [docs/integrations/aws\_lambda.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/integrations/aws_lambda.md)
- [docs/integrations/llms.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/integrations/llms.md)
- [docs/migration.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md)
- [pydantic/schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py)
- [pydantic/typing.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py)
- [pydantic/utils.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py)
- [release/README.md](https://github.com/pydantic/pydantic/blob/76ef0b08/release/README.md)
- [tests/test\_utils.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py)

This document explains Pydantic's approach to backward compatibility and provides guidance for migrating from Pydantic V1 to V2. It covers compatibility mechanisms, migration tools, common migration patterns, and best practices for handling Pydantic version transitions smoothly. For information on specific deprecated features, see [Deprecated Features](pydantic/pydantic/8.2-backported-modules.md).

## Overview

Pydantic V2 introduces significant architectural changes and improvements over V1, including performance enhancements, new features, and API refinements. While these changes introduced breaking changes, Pydantic provides several mechanisms to ease the transition between versions.

```
```

Sources: [docs/migration.md1-78](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L1-L78)

## Installations and Versions

### Installing Pydantic V2

Pydantic V2 is the current production release and can be installed with:

```
```

### Using Pydantic V1

If you need to use Pydantic V1 for any reason, you can install it with:

```
```

Alternatively, if you are using Pydantic V2 but need access to V1 features, you can use the `pydantic.v1` namespace:

```
```

Sources: [docs/migration.md10-76](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L10-L76)

## Compatibility Mechanisms

Pydantic implements several mechanisms to ensure backward compatibility:

```
```

Sources: [docs/migration.md79-124](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L79-L124) [tests/test\_deprecated.py35-111](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_deprecated.py#L35-L111)

### Using the `pydantic.v1` Namespace

Starting from `pydantic>=1.10.17`, the `pydantic.v1` namespace can be used to access V1 functionality even when using V2. This allows for gradual migration:

```
```

Sources: [docs/migration.md78-124](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L78-L124)

### Deprecation Warnings

Pydantic V2 issues deprecation warnings for features that have been renamed or removed. These warnings provide guidance on the recommended replacements:

```
```

In tests, the deprecation warnings are being handled explicitly:

```
```

Sources: [tests/test\_deprecated.py27-50](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_deprecated.py#L27-L50) [tests/test\_deprecated.py277-296](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_deprecated.py#L277-L296)

## Migration Tool

To help automate the migration process, Pydantic provides a code transformation tool called `bump-pydantic`.

### Installation and Usage

```
```

This tool attempts to automatically transform your code to use V2 patterns and APIs.

Sources: [docs/migration.md25-47](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L25-L47)

## Key Breaking Changes and Migration Paths

### Model API Changes

The following table shows the most important method/attribute name changes in `BaseModel`:

| Pydantic V1              | Pydantic V2              |
| ------------------------ | ------------------------ |
| `__fields__`             | `model_fields`           |
| `__private_attributes__` | `__pydantic_private__`   |
| `__validators__`         | `__pydantic_validator__` |
| `construct()`            | `model_construct()`      |
| `copy()`                 | `model_copy()`           |
| `dict()`                 | `model_dump()`           |
| `json_schema()`          | `model_json_schema()`    |
| `json()`                 | `model_dump_json()`      |
| `parse_obj()`            | `model_validate()`       |
| `parse_raw()`            | `model_validate_json()`  |
| `update_forward_refs()`  | `model_rebuild()`        |

Many V1 methods are retained with deprecation warnings to ease migration.

Sources: [docs/migration.md126-169](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L126-L169) [tests/test\_deprecated.py319-346](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_deprecated.py#L319-L346)

### Config Changes

Configuration in V2 uses a dictionary called `model_config` instead of a nested `Config` class:

```
```

Many config settings have been renamed or removed in V2.

Sources: [docs/migration.md321-357](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L321-L357) [docs/concepts/config.md1-85](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/config.md#L1-L85)

### Validator Changes

V2 replaces the decorators `@validator` and `@root_validator` with `@field_validator` and `@model_validator`, which provide new features and improvements:

```
```

The decorator `@validate_arguments` has been renamed to `@validate_call`.

Sources: [docs/migration.md359-403](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L359-L403) [docs/concepts/validators.md1-161](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/validators.md#L1-L161)

### Generic Models

`GenericModel` has been removed. Instead, create generic models by adding `Generic` as a parent class to a `BaseModel`:

```
```

Sources: [docs/migration.md256-275](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L256-L275)

### Type System Changes

V2 introduces `TypeAdapter` to replace V1's `parse_obj_as` and related functions:

```
```

Sources: [docs/migration.md730-768](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L730-L768) [docs/concepts/type\_adapter.md1-16](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/type_adapter.md#L1-L16)

### Custom Types

The way custom types are defined has changed in V2:

```
```

For custom types, replace:

- `__get_validators__` with `__get_pydantic_core_schema__`
- `__modify_schema__` with `__get_pydantic_json_schema__`

V2 also supports `typing.Annotated` to add validation logic to existing types.

Sources: [docs/migration.md771-792](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L771-L792) [docs/concepts/types.md65-138](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/types.md#L65-L138)

### Required, Optional, and Nullable Fields

V2 changes how optional and required fields work:

| State                                          | Field Definition            |
| ---------------------------------------------- | --------------------------- |
| Required, cannot be `None`                     | `f1: str`                   |
| Not required, cannot be `None`, has default    | `f2: str = 'abc'`           |
| Required, can be `None`                        | `f3: Optional[str]`         |
| Not required, can be `None`, default is `None` | `f4: Optional[str] = None`  |
| Not required, can be `None`, has default       | `f5: Optional[str] = 'abc'` |

A field annotated as `Optional[T]` will be required but allow `None` values, unlike in V1 where it implicitly had a default of `None`.

Sources: [docs/migration.md647-696](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L647-L696)

## Forward Compatibility Techniques

When writing code that needs to work with both V1 and V2, consider these approaches:

### Compatible Import Pattern

```
```

### Feature Detection

```
```

Sources: [docs/migration.md78-124](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L78-L124)

## Common Migration Issues and Solutions

### Equality Behavior

The `__eq__` method has changed for models in V2:

- Models can only be equal to other `BaseModel` instances
- They must have the same type, field values, extra values, and private attribute values
- Models are no longer equal to dicts containing their data

### Input Type Preservation

V2 no longer preserves input types for generic collections, except for subclasses of `BaseModel` and dataclasses:

```
```

Sources: [docs/migration.md498-615](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L498-L615)

### Default Value Validation

In V2, validators marked with `always=True` will cause standard type validation to be applied to default values:

```
```

Sources: [docs/migration.md372-396](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L372-L396)

## Best Practices

1. **Update incrementally**: Start by installing V2 and using the `pydantic.v1` namespace for incompatible code.
2. **Address deprecation warnings**: Run your tests with deprecation warnings enabled to catch and fix deprecated usage.
3. **Use type annotations**: Proper type annotations will help tools and error messages guide you during migration.
4. **Test thoroughly**: Ensure your tests cover edge cases as V2's validation behavior differs in some subtle ways.
5. **Use modern Python features**: Prefer modern Python typing features like `list[int]` over `List[int]`.

## Conclusion

Migrating from Pydantic V1 to V2 involves several significant changes, but the provided compatibility mechanisms, migration tools, and incremental migration paths make the transition manageable. By understanding the key changes and following the recommended migration patterns, you can successfully update your code to take advantage of the improvements in Pydantic V2.

Sources: [docs/migration.md1-10](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L1-L10)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Backward Compatibility and Migration](#backward-compatibility-and-migration.md)
- [Overview](#overview.md)
- [Installations and Versions](#installations-and-versions.md)
- [Installing Pydantic V2](#installing-pydantic-v2.md)
- [Using Pydantic V1](#using-pydantic-v1.md)
- [Compatibility Mechanisms](#compatibility-mechanisms.md)
- [Using the \`pydantic.v1\` Namespace](#using-the-pydanticv1-namespace.md)
- [Deprecation Warnings](#deprecation-warnings.md)
- [Migration Tool](#migration-tool.md)
- [Installation and Usage](#installation-and-usage.md)
- [Key Breaking Changes and Migration Paths](#key-breaking-changes-and-migration-paths.md)
- [Model API Changes](#model-api-changes.md)
- [Config Changes](#config-changes.md)
- [Validator Changes](#validator-changes.md)
- [Generic Models](#generic-models.md)
- [Type System Changes](#type-system-changes.md)
- [Custom Types](#custom-types.md)
- [Required, Optional, and Nullable Fields](#required-optional-and-nullable-fields.md)
- [Forward Compatibility Techniques](#forward-compatibility-techniques.md)
- [Compatible Import Pattern](#compatible-import-pattern.md)
- [Feature Detection](#feature-detection.md)
- [Common Migration Issues and Solutions](#common-migration-issues-and-solutions.md)
- [Equality Behavior](#equality-behavior.md)
- [Input Type Preservation](#input-type-preservation.md)
- [Default Value Validation](#default-value-validation.md)
- [Best Practices](#best-practices.md)
- [Conclusion](#conclusion.md)
