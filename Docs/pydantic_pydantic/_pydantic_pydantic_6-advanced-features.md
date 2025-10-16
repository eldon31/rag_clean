Advanced Features | pydantic/pydantic | DeepWiki

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

# Advanced Features

Relevant source files

- [pydantic/\_internal/\_dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py)
- [pydantic/\_internal/\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py)
- [pydantic/\_internal/\_generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generics.py)
- [pydantic/\_internal/\_typing\_extra.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_typing_extra.py)
- [pydantic/\_internal/\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py)
- [pydantic/dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py)
- [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)
- [pydantic/functional\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py)
- [pydantic/generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/generics.py)
- [pydantic/plugin/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py)
- [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)
- [pydantic/root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py)
- [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py)
- [pydantic/validate\_call\_decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py)
- [tests/test\_dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py)
- [tests/test\_forward\_ref.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_forward_ref.py)
- [tests/test\_generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_generics.py)
- [tests/test\_plugins.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py)
- [tests/test\_type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py)
- [tests/test\_typing.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_typing.py)
- [tests/test\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py)

This page documents advanced Pydantic features that extend beyond basic models. We cover enhanced dataclasses, function validation, root models with computed fields, and the plugin system for customizing validation behavior.

## Dataclass Support

Pydantic provides the `@pydantic.dataclasses.dataclass` decorator that enhances Python's standard dataclasses with validation capabilities while maintaining compatibility with the standard library's `dataclasses` module.

```
```

### Creating Pydantic Dataclasses

The `@pydantic.dataclasses.dataclass` decorator wraps the standard library `dataclasses.dataclass` and adds validation:

```
```

The decorator creates a custom `__init__` that validates input using a `__pydantic_validator__` attribute. The actual dataclass creation happens via `dataclasses.dataclass()` after field processing.

Sources: [pydantic/dataclasses.py98-250](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L98-L250) [pydantic/\_internal/\_dataclasses.py85-190](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L85-L190)

### Configuration Options

Dataclass configuration is provided via the `config` parameter, which accepts a `ConfigDict`:

| Configuration             | Description                                                            |
| ------------------------- | ---------------------------------------------------------------------- |
| `validate_assignment`     | When `True`, validates field values on assignment after initialization |
| `frozen`                  | Creates immutable dataclass instances                                  |
| `str_max_length`          | Maximum string length for all string fields                            |
| `arbitrary_types_allowed` | Allows arbitrary types that don't have Pydantic validation             |

The `frozen` parameter can be set on both the decorator and in config. The decorator value takes precedence.

Sources: [pydantic/dataclasses.py99-221](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L99-L221) [tests/test\_dataclasses.py108-130](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L108-L130)

### Converting Standard Dataclasses

Existing standard library dataclasses can be wrapped to add validation without modifying the original class:

```
```

When wrapping a standard dataclass, Pydantic creates a new subclass (not modifying the original) and processes it through the same field collection and schema generation pipeline as regular Pydantic dataclasses.

Sources: [pydantic/dataclasses.py194-206](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L194-L206) [tests/test\_dataclasses.py807-840](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L807-L840)

### Field Collection

Pydantic dataclasses collect fields using `collect_dataclass_fields()`, which:

1. Iterates through the dataclass MRO (Method Resolution Order) in reverse
2. Processes `__dataclass_fields__` from each dataclass in the hierarchy
3. Evaluates field annotations using the namespace resolver
4. Creates `FieldInfo` instances for each field
5. Applies typevars mapping for generic dataclasses

The process respects both `dataclasses.field()` and `pydantic.Field()` for defining field metadata.

Sources: [pydantic/\_internal/\_fields.py460-539](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#L460-L539) [pydantic/\_internal/\_dataclasses.py65-83](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L65-L83)

### Dataclass-Specific Features

#### InitVar Support

Pydantic dataclasses support `dataclasses.InitVar` for initialization-only fields:

```
```

InitVar fields are validated during initialization but are not stored on the instance.

Sources: [tests/test\_dataclasses.py673-687](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L673-L687)

#### Post-Init Processing

The `__post_init__` method is called after validation completes, allowing for derived field computation:

```
```

Sources: [tests/test\_dataclasses.py689-702](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L689-L702)

#### Validate Assignment

When `validate_assignment=True`, field assignments after initialization are validated:

```
```

The implementation wraps `__setattr__` with validation logic that calls `__pydantic_validator__.validate_assignment()`.

Sources: [pydantic/dataclasses.py251-268](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L251-L268) [tests/test\_dataclasses.py120-149](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L120-L149)

### Schema Generation

Dataclass schemas are built by `complete_dataclass()`, which:

1. Collects fields via `set_dataclass_fields()`
2. Creates a `GenerateSchema` instance with the config wrapper
3. Generates the core schema
4. Creates `SchemaValidator` and `SchemaSerializer` instances
5. Sets completion attributes like `__pydantic_complete__`

If schema generation fails (e.g., due to undefined forward references), mock validators are set and `__pydantic_complete__` remains `False`.

Sources: [pydantic/\_internal/\_dataclasses.py85-191](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L85-L191)

## Function Validation

The `@validate_call` decorator validates function arguments and optionally return values against type annotations.

```
```

### The `@validate_call` Decorator

The decorator creates a `ValidateCallWrapper` that intercepts function calls:

```
```

The wrapper validates arguments using `ArgsKwargs` and converts them to match the function signature.

Sources: [pydantic/validate\_call\_decorator.py57-116](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L57-L116) [pydantic/\_internal/\_validate\_call.py49-90](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L49-L90)

### ValidateCallWrapper Implementation

The `ValidateCallWrapper` class implements the validation logic:

| Attribute                       | Purpose                                       |
| ------------------------------- | --------------------------------------------- |
| `function`                      | The original function being wrapped           |
| `validate_return`               | Whether to validate return values             |
| `__pydantic_validator__`        | SchemaValidator for arguments                 |
| `__return_pydantic_validator__` | SchemaValidator for return value (if enabled) |

The wrapper:

1. Creates a schema from the function signature
2. Validates input as `ArgsKwargs` containing positional and keyword arguments
3. Calls the original function with validated arguments
4. Optionally validates the return value

Sources: [pydantic/\_internal/\_validate\_call.py49-125](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L49-L125)

### Function Schema Generation

Schema generation for functions happens in `GenerateSchema.validate_call_schema()`:

1. Extracts function signature via `inspect.signature()`
2. Processes each parameter to create argument schemas
3. Handles special parameter types (VAR\_POSITIONAL, VAR\_KEYWORD)
4. Creates an `arguments_schema` for validation
5. Optionally creates a return schema if `validate_return=True`

The generated schema validates arguments as an `ArgsKwargs` structure that gets unpacked to call the function.

Sources: [pydantic/\_internal/\_generate\_schema.py1547-1651](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L1547-L1651)

### Validating Return Values

Enable return value validation with `validate_return=True`:

```
```

Return validation uses a separate `__return_pydantic_validator__` created from the return type annotation.

Sources: [pydantic/\_internal/\_validate\_call.py91-125](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L91-L125) [tests/test\_validate\_call.py547-575](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L547-L575)

### Configuration

Configuration is passed via the `config` parameter:

```
```

The configuration affects both argument and return value validation.

Sources: [pydantic/validate\_call\_decorator.py57-116](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L57-L116) [tests/test\_validate\_call.py618-641](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L618-L641)

### Supported Function Types

The decorator supports:

- Regular functions
- Async functions
- Methods (instance, class, static)
- Lambda functions
- `functools.partial` objects

It does not support:

- Built-in functions (e.g., `breakpoint`)
- Classes (use on `__init__` or `__new__` instead)
- Non-callable objects

Sources: [pydantic/validate\_call\_decorator.py24-95](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py#L24-L95) [tests/test\_validate\_call.py42-97](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L42-L97)

## RootModel and Computed Fields

### RootModel

The `RootModel` class validates a single root-level value rather than multiple fields. It's a `BaseModel` subclass with a single field named `root`.

**RootModel Validation Flow**

```
```

The `RootModel` class:

- Sets `__pydantic_root_model__ = True`
- Has a single field `root: RootModelRootType`
- Does not support `model_config['extra']`
- Accepts either positional or keyword arguments in `__init__`

Sources: [pydantic/root\_model.py32-86](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L32-L86)

#### Creating RootModels

```
```

The root type is specified as a generic parameter. The model validates that the input matches the root type.

Sources: [pydantic/root\_model.py32-69](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L32-L69)

#### Serialization

RootModel serialization methods return the root value directly:

| Method              | Returns                       |
| ------------------- | ----------------------------- |
| `model_dump()`      | Python representation of root |
| `model_dump_json()` | JSON string of root           |

```
```

Sources: [pydantic/root\_model.py109-158](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L109-L158)

### Computed Fields

The `@computed_field` decorator creates dynamic properties that appear in serialization but are not part of the model's validated fields.

**Computed Field Lifecycle**

```
```

Computed fields:

- Are evaluated during serialization, not validation
- Appear in `model_dump()` and `model_dump_json()` output
- Can be cached with `@cached_property`
- Support custom serializers via `@field_serializer`

Sources: [pydantic/fields.py745-894](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L745-L894)

#### Basic Usage

```
```

The `@computed_field` decorator must be applied to a `@property`. The computed value is included in serialization output.

Sources: [pydantic/fields.py745-810](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L745-L810)

#### JSON Schema

Computed fields appear in JSON schema with `readOnly: true` in serialization mode:

```
```

Sources: [tests/test\_dataclasses.py1285-1329](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L1285-L1329)

#### Return Type Annotation

Computed fields require return type annotations. The annotation determines the schema used for serialization:

```
```

Without a return type annotation, Pydantic cannot generate the correct schema.

Sources: [pydantic/fields.py745-810](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L745-L810)

## Plugin System

Pydantic provides a plugin system that allows you to customize validation, serialization, and other behaviors. This is particularly useful for integrating Pydantic with other libraries or adding custom validation logic.

```
```

### Creating a Plugin

```
```

### Validation Handlers

Plugins can provide handlers for different validation methods:

```
```

### Using Plugins

Plugins are configured through model config:

```
```

Sources: [pydantic/plugin/\_\_init\_\_.py38-71](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L38-L71) [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)

## Integration with Other Libraries

Pydantic integrates well with many Python libraries and frameworks. Here are some common integrations:

### FastAPI Integration

FastAPI leverages Pydantic models for request validation and OpenAPI schema generation:

```
```

### Dataframe Validation

Using TypeAdapter with pandas DataFrames:

```
```

### ORM Integration

Pydantic models can work with ORMs using `from_attributes`:

```
```

These integrations showcase Pydantic's versatility and how it can be used as a validation layer in various Python applications and frameworks.

Sources: [tests/test\_type\_adapter.py385-430](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py#L385-L430) [tests/test\_validate\_call.py385-430](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py#L385-L430)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Advanced Features](#advanced-features.md)
- [Dataclass Support](#dataclass-support.md)
- [Creating Pydantic Dataclasses](#creating-pydantic-dataclasses.md)
- [Configuration Options](#configuration-options.md)
- [Converting Standard Dataclasses](#converting-standard-dataclasses.md)
- [Field Collection](#field-collection.md)
- [Dataclass-Specific Features](#dataclass-specific-features.md)
- [InitVar Support](#initvar-support.md)
- [Post-Init Processing](#post-init-processing.md)
- [Validate Assignment](#validate-assignment.md)
- [Schema Generation](#schema-generation.md)
- [Function Validation](#function-validation.md)
- [The \`@validate\_call\` Decorator](#the-validate_call-decorator.md)
- [ValidateCallWrapper Implementation](#validatecallwrapper-implementation.md)
- [Function Schema Generation](#function-schema-generation.md)
- [Validating Return Values](#validating-return-values.md)
- [Configuration](#configuration.md)
- [Supported Function Types](#supported-function-types.md)
- [RootModel and Computed Fields](#rootmodel-and-computed-fields.md)
- [RootModel](#rootmodel.md)
- [Creating RootModels](#creating-rootmodels.md)
- [Serialization](#serialization.md)
- [Computed Fields](#computed-fields.md)
- [Basic Usage](#basic-usage.md)
- [JSON Schema](#json-schema.md)
- [Return Type Annotation](#return-type-annotation.md)
- [Plugin System](#plugin-system.md)
- [Creating a Plugin](#creating-a-plugin.md)
- [Validation Handlers](#validation-handlers.md)
- [Using Plugins](#using-plugins.md)
- [Integration with Other Libraries](#integration-with-other-libraries.md)
- [FastAPI Integration](#fastapi-integration.md)
- [Dataframe Validation](#dataframe-validation.md)
- [ORM Integration](#orm-integration.md)
