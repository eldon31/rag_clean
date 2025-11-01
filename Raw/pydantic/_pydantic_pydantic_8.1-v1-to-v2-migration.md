V1 to V2 Migration | pydantic/pydantic | DeepWiki

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

# V1 to V2 Migration

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
- [release/README.md](https://github.com/pydantic/pydantic/blob/76ef0b08/release/README.md)

This document provides a comprehensive guide for migrating Pydantic code from V1 to V2. It covers breaking changes, API modifications, and migration strategies. For specific documentation on V2 features like validators, serializers, or model configuration, see the respective pages in sections 2-4 of this wiki.

## Overview and Installation

### Installing Pydantic V2

Pydantic V2 is the current production release and can be installed from PyPI:

```
```

For users who need to continue using V1 features, the V1 API is accessible through the `pydantic.v1` namespace when using Pydantic V2. Alternatively, Pydantic V1 can be installed directly with `pip install "pydantic==1.*"`.

Sources: [docs/migration.md10-76](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L10-L76)

### Migration Tool: bump-pydantic

The `bump-pydantic` tool automates much of the migration process:

```
```

This tool handles common migration patterns including method renames, config updates, and validator syntax changes. Use the `--dry-run` flag to preview changes without modifying files.

Sources: [docs/migration.md25-47](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L25-L47)

```
```

**Migration Workflow with bump-pydantic Tool**

Sources: [docs/migration.md25-47](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L25-L47)

## BaseModel API Changes

### Method Name Changes

Pydantic V2 standardizes method naming with `model_*` and `__*pydantic*__` patterns. Deprecated V1 method names remain available but emit deprecation warnings.

| Pydantic V1              | Pydantic V2              | Purpose                                            |
| ------------------------ | ------------------------ | -------------------------------------------------- |
| `__fields__`             | `model_fields`           | Field definitions                                  |
| `__private_attributes__` | `__pydantic_private__`   | Private attributes                                 |
| `__validators__`         | `__pydantic_validator__` | Validator functions                                |
| `construct()`            | `model_construct()`      | Create without validation                          |
| `copy()`                 | `model_copy()`           | Copy model instance                                |
| `dict()`                 | `model_dump()`           | Serialize to dictionary                            |
| `json_schema()`          | `model_json_schema()`    | Generate JSON schema                               |
| `json()`                 | `model_dump_json()`      | Serialize to JSON string                           |
| `parse_obj()`            | `model_validate()`       | Validate Python object                             |
| `parse_raw()`            | Deprecated               | Use `model_validate_json()`                        |
| `parse_file()`           | Deprecated               | Load data then validate                            |
| `from_orm()`             | Deprecated               | Use `model_validate()` with `from_attributes=True` |
| `update_forward_refs()`  | `model_rebuild()`        | Rebuild schema                                     |

Sources: [docs/migration.md129-149](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L129-L149)

### Equality Behavior Changes

In V2, model equality checking has stricter rules:

- Models can only equal other `BaseModel` instances
- Both instances must have the same type (or non-parametrized generic origin)
- Field values, extra values, and private attribute values must all match
- Models are no longer equal to dictionaries containing their data

Sources: [docs/migration.md152-162](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L152-L162)

### RootModel Replaces `__root__`

The `__root__` field pattern for custom root models has been replaced with the `RootModel` class:

```
```

`RootModel` types do not support `arbitrary_types_allowed` configuration.

Sources: [docs/migration.md163-166](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L163-L166) [docs/concepts/models.md1-100](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/models.md#L1-L100)

```
```

**BaseModel Method Migration Mapping**

Sources: [docs/migration.md135-146](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L135-L146)

## Field and Configuration Changes

### Field Function Updates

Several `Field()` parameters have been removed or renamed:

| V1 Parameter     | V2 Replacement     | Notes                                |
| ---------------- | ------------------ | ------------------------------------ |
| `const`          | Removed            | Use `Literal` type instead           |
| `min_items`      | `min_length`       | Renamed for consistency              |
| `max_items`      | `max_length`       | Renamed for consistency              |
| `unique_items`   | Removed            |                                      |
| `allow_mutation` | `frozen`           | Inverse logic                        |
| `regex`          | `pattern`          | Renamed                              |
| `final`          | Use `typing.Final` | Type hint instead of field parameter |

Field constraints no longer automatically propagate to generic type parameters. Use `Annotated` for item-level validation:

```
```

The `alias` property now returns `None` when no alias is set (V1 returned the field name).

Sources: [docs/migration.md275-294](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L275-L294)

### Model Configuration Migration

V2 introduces `model_config` with `ConfigDict` replacing the V1 `Config` class:

```
```

Configuration can also be specified as class arguments for better type checking:

```
```

Sources: [docs/migration.md319-329](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L319-L329) [docs/concepts/config.md9-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/config.md#L9-L50)

### Configuration Options Removed/Renamed

**Removed Options:**

- `allow_mutation` → use `frozen` (inverse logic)
- `error_msg_templates`
- `fields` → use `Annotated` for field modifications
- `getter_dict` → removed with `orm_mode`
- `smart_union` → default behavior in V2
- `underscore_attrs_are_private` → always `True` in V2
- `json_loads`, `json_dumps`
- `copy_on_model_validation`
- `post_init_call`

**Renamed Options:**

| V1 Name                          | V2 Name                                           |
| -------------------------------- | ------------------------------------------------- |
| `allow_population_by_field_name` | `populate_by_name` or `validate_by_name` (v2.11+) |
| `anystr_lower`                   | `str_to_lower`                                    |
| `anystr_strip_whitespace`        | `str_strip_whitespace`                            |
| `anystr_upper`                   | `str_to_upper`                                    |
| `keep_untouched`                 | `ignored_types`                                   |
| `max_anystr_length`              | `str_max_length`                                  |
| `min_anystr_length`              | `str_min_length`                                  |
| `orm_mode`                       | `from_attributes`                                 |
| `schema_extra`                   | `json_schema_extra`                               |
| `validate_all`                   | `validate_default`                                |

Sources: [docs/migration.md330-356](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L330-L356)

```
```

**Configuration Migration Pattern**

Sources: [docs/migration.md319-356](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L319-L356)

## Validator and Serializer Changes

### Decorator Migration

V2 introduces new validator and serializer decorators with enhanced functionality:

**Validator Migration:**

| V1                | V2                 | Key Changes                                         |
| ----------------- | ------------------ | --------------------------------------------------- |
| `@validator`      | `@field_validator` | No `each_item` parameter; use `Annotated` for items |
| `@root_validator` | `@model_validator` | May receive model instance instead of dict          |

The `@field_validator` decorator requires explicit mode specification and uses different argument patterns:

```
```

Sources: [docs/migration.md360-434](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L360-L434) [docs/concepts/validators.md29-463](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/validators.md#L29-L463)

### Validator Argument Changes

V2 validators no longer accept `field` and `config` keyword arguments. Use `ValidationInfo` instead:

- `config` → `info.config` (now a dict, not a class)
- `field` → `cls.model_fields[info.field_name]` (no longer `ModelField` object)

The `allow_reuse` keyword argument is no longer needed due to improved reuse detection.

Sources: [docs/migration.md404-488](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L404-L488)

### TypeError Handling

In V1, `TypeError` raised in validators was converted to `ValidationError`. In V2, `TypeError` is raised directly:

```
```

Sources: [docs/migration.md436-464](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L436-L464)

### Serializer Introduction

V2 adds `@field_serializer` and `@model_serializer` decorators for custom serialization, replacing the deprecated `json_encoders` config option:

```
```

Sources: [docs/migration.md167-175](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L167-L175) [docs/concepts/serialization.md218-420](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/serialization.md#L218-L420)

```
```

**Validator Decorator Migration**

Sources: [docs/migration.md360-434](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L360-L434) [docs/concepts/validators.md29-463](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/validators.md#L29-L463)

## Dataclass Changes

### Initialization and Validation

In V2, the `__post_init__` method is called *after* validation rather than before. The `__post_init_post_parse__` method has been removed as it's now redundant.

Pydantic dataclasses no longer support `extra='allow'` with attribute storage. Only `extra='ignore'` is supported for ignoring unexpected fields.

Sources: [docs/migration.md295-307](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L295-L307)

### Schema Access Changes

Pydantic dataclasses no longer have a `__pydantic_model__` attribute. To access validation and schema functionality, wrap the dataclass with `TypeAdapter`:

```
```

Sources: [docs/migration.md307-317](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L307-L317) [docs/concepts/dataclasses.md1-80](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/dataclasses.md#L1-L80)

### Configuration Inheritance

In V1, vanilla dataclasses used as fields would inherit the parent type's config. In V2, this no longer occurs. Use the `config` parameter on the `@dataclass` decorator to override configuration:

```
```

Sources: [docs/migration.md313-318](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L313-L318) [docs/concepts/dataclasses.md85-118](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/dataclasses.md#L85-L118)

## Type System Changes

### GenericModel Removal

`pydantic.generics.GenericModel` has been removed. Create generic models by inheriting directly from `BaseModel` and `Generic`:

```
```

Avoid using parametrized generics in `isinstance()` checks. For such checks, create concrete subclasses:

```
```

Sources: [docs/migration.md255-273](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L255-L273)

### Input Type Preservation

V1 attempted to preserve input types for generic collections (e.g., `Counter` → `Counter`). V2 only guarantees output types match annotations, typically converting to standard types:

```
```

To preserve input types, use a custom validator with `WrapValidator`:

```
```

V2 preserves types for `BaseModel` subclasses and dataclasses.

Sources: [docs/migration.md498-611](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L498-L611)

### Union Type Behavior

V2 preserves input types when they match a union member, even if another type would also validate:

```
```

To revert to V1's left-to-right behavior, use `Field(union_mode='left_to_right')`.

Sources: [docs/migration.md620-644](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L620-L644)

### Required vs Optional Fields

V2 aligns with dataclasses behavior for `Optional` fields:

| Pattern                   | V1 Behavior                | V2 Behavior                           |
| ------------------------- | -------------------------- | ------------------------------------- |
| `f: str`                  | Required, cannot be None   | Same                                  |
| `f: str = 'default'`      | Optional, cannot be None   | Same                                  |
| `f: Optional[str]`        | Optional, defaults to None | **Required**, can be None             |
| `f: Optional[str] = None` | Optional, defaults to None | Same                                  |
| `f: Any`                  | Optional, defaults to None | **Required**, can be None or any type |
| `f: Any = None`           | Optional, defaults to None | Same                                  |

**Breaking Change:** `Optional[T]` fields are now required by default unless a default value is provided.

Sources: [docs/migration.md645-694](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L645-L694)

### Float to Integer Coercion

V2 only allows float-to-int coercion when the decimal part is zero:

```
```

Sources: [docs/migration.md708-733](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L708-L733)

### Regex Engine Change

V2 uses Rust's regex engine instead of Python's, providing linear-time matching but without lookarounds and backreferences. Use `regex_engine` config to revert to Python's engine if needed:

```
```

Sources: [docs/migration.md696-706](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L696-L706)

```
```

**Key Type System Behavior Changes**

Sources: [docs/migration.md613-733](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L613-L733)

## TypeAdapter Introduction

V2 introduces `TypeAdapter` for validating and serializing arbitrary types outside `BaseModel`. This replaces V1's `parse_obj_as` and `schema_of` functions:

```
```

`TypeAdapter` provides methods for:

- `validate_python()` - Validate Python objects
- `validate_json()` - Validate JSON strings
- `dump_python()` - Serialize to Python objects
- `dump_json()` - Serialize to JSON strings
- `json_schema()` - Generate JSON schema

For proper typing with generic parameters, specify the type explicitly:

```
```

Sources: [docs/migration.md735-768](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L735-L768) [docs/concepts/type\_adapter.md1-100](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/type_adapter.md#L1-L100)

## Custom Types and Schema Generation

### Custom Type Hooks

V2 completely overhauls custom type definition:

| V1 Method            | V2 Replacement                 |
| -------------------- | ------------------------------ |
| `__get_validators__` | `__get_pydantic_core_schema__` |
| `__modify_schema__`  | `__get_pydantic_json_schema__` |

These hooks can also be provided via `Annotated` metadata rather than modifying the type directly:

```
```

Sources: [docs/migration.md769-791](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L769-L791) [docs/concepts/types.md1-100](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/types.md#L1-L100)

### JSON Schema Generation

V2 introduces `GenerateJsonSchema` class for customizable JSON schema generation:

**Key Changes:**

- Default target is JSON Schema Draft 2020-12 (was Draft 7 in V1)
- `Optional` fields now indicate `null` is allowed
- `Decimal` serialized as string (was number in V1)
- Namedtuples no longer preserved in schema
- Schema mode can be `'validation'` or `'serialization'`

Customize schema generation by subclassing `GenerateJsonSchema`:

```
```

Sources: [docs/migration.md793-824](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L793-L824) [docs/concepts/json\_schema.md1-100](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/json_schema.md#L1-L100)

## Relocated and Removed Features

### BaseSettings Migration

`BaseSettings` has moved to the separate `pydantic-settings` package:

```
```

```
```

The `parse_env_var` classmethod has been removed. Use customized settings sources instead.

Sources: [docs/migration.md825-834](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L825-L834)

### Moved to pydantic-extra-types

The following types have moved to `pydantic-extra-types`:

- Color types (Color, etc.)
- Payment card numbers (PaymentCardNumber, etc.)

Install with:

```
```

Sources: [docs/migration.md835-843](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L835-L843)

### URL and DSN Types

`AnyUrl` and related URL/DSN types no longer inherit from `str` in V2. They are built on `Url` and `MultiHostUrl` classes using `Annotated`.

To use as strings, call `str(url)` explicitly:

```
```

Sources: [docs/migration.md844-851](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L844-L851)

```
```

**Package Reorganization in V2**

Sources: [docs/migration.md825-851](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L825-L851)

## Function Validation

The `@validate_arguments` decorator has been renamed to `@validate_call`:

```
```

V1's validator function attributes (`raw_function`, `validate`) are no longer available in V2.

Sources: [docs/migration.md489-497](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L489-L497)

## Migration Checklist

```
```

**Recommended Migration Process**

Sources: [docs/migration.md1-851](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L1-L851)

### Key Migration Steps

1. **Install Tools**: Install `bump-pydantic` and run it on your codebase
2. **Update BaseModel Methods**: Replace deprecated method names with V2 equivalents
3. **Migrate Configuration**: Convert `Config` classes to `model_config` with `ConfigDict`
4. **Update Validators**: Replace `@validator` and `@root_validator` with new decorators
5. **Fix Field Definitions**: Update field parameters and use `Annotated` for constraints
6. **Review Type Behavior**: Test Optional fields, unions, and numeric coercion
7. **Update Dataclasses**: Replace `__pydantic_model__` usage with `TypeAdapter`
8. **Migrate Custom Types**: Implement `__get_pydantic_core_schema__` hooks
9. **Test Thoroughly**: Run comprehensive tests and type checking

Sources: [docs/migration.md1-851](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L1-L851) [docs/contributing.md1-272](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/contributing.md#L1-L272)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [V1 to V2 Migration](#v1-to-v2-migration.md)
- [Overview and Installation](#overview-and-installation.md)
- [Installing Pydantic V2](#installing-pydantic-v2.md)
- [Migration Tool: bump-pydantic](#migration-tool-bump-pydantic.md)
- [BaseModel API Changes](#basemodel-api-changes.md)
- [Method Name Changes](#method-name-changes.md)
- [Equality Behavior Changes](#equality-behavior-changes.md)
- [RootModel Replaces \`\_\_root\_\_\`](#rootmodel-replaces-__root__.md)
- [Field and Configuration Changes](#field-and-configuration-changes.md)
- [Field Function Updates](#field-function-updates.md)
- [Model Configuration Migration](#model-configuration-migration.md)
- [Configuration Options Removed/Renamed](#configuration-options-removedrenamed.md)
- [Validator and Serializer Changes](#validator-and-serializer-changes.md)
- [Decorator Migration](#decorator-migration.md)
- [Validator Argument Changes](#validator-argument-changes.md)
- [TypeError Handling](#typeerror-handling.md)
- [Serializer Introduction](#serializer-introduction.md)
- [Dataclass Changes](#dataclass-changes.md)
- [Initialization and Validation](#initialization-and-validation.md)
- [Schema Access Changes](#schema-access-changes.md)
- [Configuration Inheritance](#configuration-inheritance.md)
- [Type System Changes](#type-system-changes.md)
- [GenericModel Removal](#genericmodel-removal.md)
- [Input Type Preservation](#input-type-preservation.md)
- [Union Type Behavior](#union-type-behavior.md)
- [Required vs Optional Fields](#required-vs-optional-fields.md)
- [Float to Integer Coercion](#float-to-integer-coercion.md)
- [Regex Engine Change](#regex-engine-change.md)
- [TypeAdapter Introduction](#typeadapter-introduction.md)
- [Custom Types and Schema Generation](#custom-types-and-schema-generation.md)
- [Custom Type Hooks](#custom-type-hooks.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [Relocated and Removed Features](#relocated-and-removed-features.md)
- [BaseSettings Migration](#basesettings-migration.md)
- [Moved to pydantic-extra-types](#moved-to-pydantic-extra-types.md)
- [URL and DSN Types](#url-and-dsn-types.md)
- [Function Validation](#function-validation.md)
- [Migration Checklist](#migration-checklist.md)
- [Key Migration Steps](#key-migration-steps.md)
