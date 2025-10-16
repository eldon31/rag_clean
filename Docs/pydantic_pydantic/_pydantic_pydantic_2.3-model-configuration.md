Model Configuration | pydantic/pydantic | DeepWiki

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

# Model Configuration

Relevant source files

- [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)
- [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)
- [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)
- [tests/test\_create\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py)
- [tests/test\_edge\_cases.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py)
- [tests/test\_main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py)
- [tests/test\_private\_attributes.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_private_attributes.py)

Model Configuration in Pydantic allows you to customize the behavior of your models, including validation rules, serialization formats, and schema generation. This page documents the configuration system and how specific settings affect model behavior.

## Overview

In Pydantic, model configuration is primarily managed through the `ConfigDict` class, which provides a centralized way to control various aspects of model behavior. Configuration options influence everything from how strictly types are validated to how extra fields are handled and how data is serialized.

```
```

Sources: [pydantic/config.py36-1113](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L36-L1113)

## Defining Configuration

There are multiple ways to specify configuration for models in Pydantic:

### Using `model_config`

The recommended and most common approach is to use the `model_config` class variable with `ConfigDict`:

```
```

### Configuration Inheritance

When a model inherits from another model, its configuration is merged with the parent's configuration:

```
```

Sources: [tests/test\_config.py491-519](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_config.py#L491-L519)

### Class Initialization Arguments

Some configuration options can also be specified as parameters to the class itself:

```
```

Sources: [tests/test\_config.py110-126](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_config.py#L110-L126)

### With `with_config` Decorator

For non-BaseModel types like TypedDict and dataclasses, you can use the `with_config` decorator:

```
```

Sources: [pydantic/config.py1144-1210](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L1144-L1210)

## Configuration Processing Flow

When a model is created, its configuration is processed through several steps:

```
```

Sources: [pydantic/\_internal/\_config.py94-228](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py#L94-L228)

## Major Configuration Options

Pydantic offers many configuration options that affect different aspects of model behavior.

### Validation Behavior

These options control how validation works:

| Option                    | Default    | Description                                                           |
| ------------------------- | ---------- | --------------------------------------------------------------------- |
| `strict`                  | `False`    | Enforces strict type checking with no coercion                        |
| `validate_assignment`     | `False`    | Validates values when attributes are assigned after creation          |
| `frozen`                  | `False`    | Makes model instances immutable                                       |
| `extra`                   | `'ignore'` | Controls how extra fields are handled: 'allow', 'ignore', or 'forbid' |
| `arbitrary_types_allowed` | `False`    | Allows fields with arbitrary Python types                             |
| `revalidate_instances`    | `'never'`  | Controls when model instances are revalidated                         |

Sources: [pydantic/config.py158-590](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L158-L590)

### Field and Alias Handling

These options control how fields and their aliases are used:

| Option              | Default | Description                                                |
| ------------------- | ------- | ---------------------------------------------------------- |
| `validate_by_alias` | `True`  | Allow validation using field aliases                       |
| `validate_by_name`  | `False` | Allow validation using field attribute names               |
| `populate_by_name`  | `False` | (Deprecated) Allow field population by both name and alias |
| `alias_generator`   | `None`  | Function to generate field aliases                         |
| `loc_by_alias`      | `True`  | Use alias instead of field name in error locations         |

Sources: [pydantic/config.py358-419](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L358-L419) [pydantic/config.py1038-1112](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L1038-L1112)

### String Processing

These options control how string values are processed:

| Option                 | Default | Description                          |
| ---------------------- | ------- | ------------------------------------ |
| `str_strip_whitespace` | `False` | Strip whitespace from strings        |
| `str_to_lower`         | `False` | Convert strings to lowercase         |
| `str_to_upper`         | `False` | Convert strings to uppercase         |
| `str_min_length`       | `0`     | Minimum length for string validation |
| `str_max_length`       | `None`  | Maximum length for string validation |

Sources: [pydantic/config.py48-61](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L48-L61)

### Serialization

These options control how models are serialized:

| Option               | Default     | Description                             |
| -------------------- | ----------- | --------------------------------------- |
| `serialize_by_alias` | `False`     | Serialize using field aliases           |
| `use_enum_values`    | `False`     | Use enum values instead of enum members |
| `ser_json_bytes`     | `'utf8'`    | Encoding for bytes in JSON              |
| `ser_json_timedelta` | `'iso8601'` | Format for timedeltas in JSON           |
| `ser_json_inf_nan`   | `'null'`    | How to serialize infinity and NaN       |

Sources: [pydantic/config.py592-628](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L592-L628) [pydantic/config.py1114-1138](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L1114-L1138)

### Performance Options

These options affect performance:

| Option          | Default        | Description                               |
| --------------- | -------------- | ----------------------------------------- |
| `defer_build`   | `False`        | Defer building validators until first use |
| `cache_strings` | `True`         | Cache strings to improve performance      |
| `regex_engine`  | `'rust-regex'` | Engine for regex validation               |

Sources: [pydantic/config.py775-837](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L775-L837) [pydantic/config.py931-944](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L931-L944) [pydantic/config.py1019-1037](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L1019-L1037)

## Config Integration with the Pydantic Core

The configuration system interacts with Pydantic's core components to control validation and serialization behavior:

```
```

Sources: [pydantic/\_internal/\_config.py158-228](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py#L158-L228)

## Common Configuration Use Cases

### Handling Extra Fields

The `extra` option controls how Pydantic handles fields not declared in the model:

```
```

Sources: [pydantic/config.py63-156](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L63-L156)

### Strict Validation

The `strict` option enforces strict type checking:

```
```

Sources: [pydantic/config.py444-469](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L444-L469)

### Alias Handling

Control how aliases are used for validation and serialization:

```
```

Sources: [pydantic/config.py1038-1138](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L1038-L1138)

### Frozen Models

Create immutable models with `frozen=True`:

```
```

Sources: [pydantic/config.py158-166](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L158-L166)

### Validation on Assignment

Enable validation when attributes are assigned after creation:

```
```

Sources: [pydantic/config.py246-296](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L246-L296)

## Working with Deferred Schema Building

For large model hierarchies, you can improve startup performance with `defer_build=True`:

```
```

Sources: [pydantic/config.py775-784](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L775-L784)

## Advanced Configuration Use Cases

### Custom Alias Generation

Generate aliases automatically with a function:

```
```

Sources: [pydantic/config.py361-418](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L361-L418)

### Custom JSON Encoding

Control how special values are serialized:

```
```

Sources: [pydantic/config.py592-628](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L592-L628)

## Best Practices

1. **Be consistent with configuration** across related models to prevent surprising behavior
2. **Document your configuration choices** in your codebase
3. **Consider validation strictness** based on your application's requirements
4. **Use `defer_build=True`** for large model hierarchies that aren't immediately used
5. **Choose appropriate `extra` handling** based on your API contract requirements
6. **Prefer `model_config`** over the deprecated class-based `Config` approach

Sources: [pydantic/\_internal/\_config.py31-32](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py#L31-L32)

## Configuration Defaults

All configuration options have sensible defaults that are used when not explicitly set:

```
```

Sources: [pydantic/\_internal/\_config.py261-307](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py#L261-L307)

The full list of configuration options and their default values can be found in the `config_defaults` dictionary in [pydantic/\_internal/\_config.py261-307](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py#L261-L307)

## Configuring Non-BaseModel Types

In addition to configuring `BaseModel` subclasses, you can also apply Pydantic configurations to other types:

### TypedDict

```
```

Sources: [pydantic/config.py1157-1182](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L1157-L1182)

### Dataclasses

```
```

Sources: [tests/test\_config.py738-760](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_config.py#L738-L760)

By effectively using Pydantic's configuration system, you can fine-tune validation, serialization, and schema generation to meet your application's specific requirements.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Model Configuration](#model-configuration.md)
- [Overview](#overview.md)
- [Defining Configuration](#defining-configuration.md)
- [Using \`model\_config\`](#using-model_config.md)
- [Configuration Inheritance](#configuration-inheritance.md)
- [Class Initialization Arguments](#class-initialization-arguments.md)
- [With \`with\_config\` Decorator](#with-with_config-decorator.md)
- [Configuration Processing Flow](#configuration-processing-flow.md)
- [Major Configuration Options](#major-configuration-options.md)
- [Validation Behavior](#validation-behavior.md)
- [Field and Alias Handling](#field-and-alias-handling.md)
- [String Processing](#string-processing.md)
- [Serialization](#serialization.md)
- [Performance Options](#performance-options.md)
- [Config Integration with the Pydantic Core](#config-integration-with-the-pydantic-core.md)
- [Common Configuration Use Cases](#common-configuration-use-cases.md)
- [Handling Extra Fields](#handling-extra-fields.md)
- [Strict Validation](#strict-validation.md)
- [Alias Handling](#alias-handling.md)
- [Frozen Models](#frozen-models.md)
- [Validation on Assignment](#validation-on-assignment.md)
- [Working with Deferred Schema Building](#working-with-deferred-schema-building.md)
- [Advanced Configuration Use Cases](#advanced-configuration-use-cases.md)
- [Custom Alias Generation](#custom-alias-generation.md)
- [Custom JSON Encoding](#custom-json-encoding.md)
- [Best Practices](#best-practices.md)
- [Configuration Defaults](#configuration-defaults.md)
- [Configuring Non-BaseModel Types](#configuring-non-basemodel-types.md)
- [TypedDict](#typeddict.md)
- [Dataclasses](#dataclasses.md)
