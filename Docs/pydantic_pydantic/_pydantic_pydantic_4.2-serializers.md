Serializers | pydantic/pydantic | DeepWiki

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

# Serializers

Relevant source files

- [pydantic/\_internal/\_decorators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py)
- [pydantic/\_internal/\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py)
- [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)
- [pydantic/functional\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py)
- [pydantic/plugin/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py)
- [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)
- [pydantic/root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py)
- [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py)
- [pydantic/validate\_call\_decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py)
- [tests/test\_computed\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py)
- [tests/test\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_construction.py)
- [tests/test\_plugins.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py)
- [tests/test\_serialize.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py)
- [tests/test\_type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py)
- [tests/test\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py)
- [tests/test\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py)

Pydantic's serialization system converts model instances into serializable formats such as Python dictionaries or JSON strings. This page explains how serializers work in Pydantic, including field serializers, model serializers, and functional serializers. For information about validators (which handle input data validation), see [Validators](pydantic/pydantic/4.1-validators.md).

## Overview of the Serialization System

In Pydantic, serialization is the process of converting a model instance into a simplified representation suitable for storage or transmission. While validation transforms input data into model instances, serialization converts model instances back into primitive data types.

```
```

Sources:

- [tests/test\_serialize.py1-29](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L1-L29)
- [pydantic/functional\_serializers.py1-20](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L1-L20)

## Core Serialization Components

Pydantic offers several components for customizing serialization behavior:

```
```

Sources:

- [pydantic/functional\_serializers.py18-165](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L18-L165)
- [pydantic/\_internal/\_decorators.py90-130](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L90-L130)

### Serialization Modes

Serializers can operate in two modes:

1. **Plain mode**: The serializer receives the value and returns a transformed value
2. **Wrap mode**: The serializer receives the value and a handler function, allowing for more complex transformations

Additionally, serializers can be configured to run in specific scenarios using the `when_used` parameter:

| `when_used` value    | Python serialization | JSON serialization | When value is None |
| -------------------- | -------------------- | ------------------ | ------------------ |
| `"always"` (default) | Yes                  | Yes                | Yes                |
| `"json"`             | No                   | Yes                | Yes                |
| `"unless-none"`      | Yes                  | Yes                | No                 |
| `"json-unless-none"` | No                   | Yes                | No                 |

Sources:

- [tests/test\_serialize.py82-197](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L82-L197)
- [pydantic/functional\_serializers.py45-52](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L45-L52)

## Field Serializers

Field serializers allow you to customize the serialization of individual model fields. They can be applied using the `@field_serializer` decorator.

```
```

### Using the field\_serializer Decorator

The `@field_serializer` decorator is used to define custom serialization logic for specific fields:

```
```

The decorator accepts the following parameters:

- `field`: Field name(s) to which the serializer should be applied
- `mode`: Serialization mode (`"plain"` or `"wrap"`)
- `when_used`: When the serializer should be applied (`"always"`, `"json"`, `"unless-none"`, or `"json-unless-none"`)
- `return_type`: The return type of the serializer function (optional)

Sources:

- [tests/test\_serialize.py148-197](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L148-L197)
- [tests/test\_serialize.py225-271](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L225-L271)
- [pydantic/\_internal/\_decorators.py90-111](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L90-L111)

### Field Serializer Signature

Field serializers can have several valid function signatures:

```
```

The `info` parameter provides context about the serialization process, including the field name and serialization mode.

Sources:

- [tests/test\_serialize.py225-271](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L225-L271)
- [pydantic/\_internal/\_decorators.py90-111](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L90-L111)

## Functional Serializers

Functional serializers are used with the `Annotated` type to define custom serialization logic for specific types. This allows you to reuse serialization logic across multiple models.

```
```

Pydantic provides two main types of functional serializers:

1. **PlainSerializer**: Applies a transformation function directly to the value
2. **WrapSerializer**: Provides both the value and a handler function for more complex transformations

### PlainSerializer

```
```

The `PlainSerializer` class accepts:

- `func`: The serializer function
- `return_type`: The return type of the serializer (optional)
- `when_used`: When the serializer should be applied (optional)

Sources:

- [tests/test\_serialize.py82-102](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L82-L102)
- [pydantic/functional\_serializers.py18-86](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L18-L86)

### WrapSerializer

```
```

The `WrapSerializer` class accepts:

- `func`: The serializer function (which receives both a value and a handler)
- `return_type`: The return type of the serializer (optional)
- `when_used`: When the serializer should be applied (optional)

Sources:

- [tests/test\_serialize.py104-129](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L104-L129)
- [pydantic/functional\_serializers.py89-247](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L89-L247)

## Model Serializers

Model serializers allow you to customize the serialization of an entire model. This is useful when you need complete control over the serialization process.

```
```

### Using the model\_serializer Decorator

The `@model_serializer` decorator is used to define custom serialization logic for an entire model:

```
```

The decorator accepts:

- `mode`: Serialization mode (`"plain"` or `"wrap"`)
- `when_used`: When the serializer should be applied
- `return_type`: The return type of the serializer function (optional)

Sources:

- [tests/test\_serialize.py374-464](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L374-L464)
- [pydantic/\_internal/\_decorators.py113-130](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L113-L130)

### Model Serializer Modes

Model serializers can operate in two modes:

1. **Plain mode**: The serializer has complete control over the serialization process

   ```
   ```

2. **Wrap mode**: The serializer receives the standard serialized output and can modify it

   ```
   ```

In wrap mode, the handler function performs the standard serialization, allowing you to modify the result before returning it.

Sources:

- [tests/test\_serialize.py374-422](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L374-L422)
- [tests/test\_serialize.py423-464](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L423-L464)

## Serialization Process

The serialization process in Pydantic involves converting model instances to Python dictionaries or JSON strings. This is handled by the `model_dump()` and `model_dump_json()` methods.

```
```

### Core Serialization Methods

Pydantic models provide two main methods for serialization:

1. **model\_dump()**: Converts a model instance to a Python dictionary
2. **model\_dump\_json()**: Converts a model instance to a JSON string

These methods accept various parameters:

- `mode`: Serialization mode (`"python"` or `"json"`)
- `include`: Fields to include in the output
- `exclude`: Fields to exclude from the output
- `by_alias`: Whether to use field aliases
- `exclude_unset`: Whether to exclude unset fields
- `exclude_defaults`: Whether to exclude fields with default values
- `exclude_none`: Whether to exclude None values
- `round_trip`: Whether to preserve exact types for round-trip conversions

Sources:

- [tests/test\_serialize.py33-79](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L33-L79)
- [pydantic/type\_adapter.py376-535](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L376-L535)

### Serialization in TypeAdapter

The `TypeAdapter` class provides similar serialization functionality for arbitrary types:

- `dump_python()`: Serializes a value to a Python object
- `dump_json()`: Serializes a value to a JSON string

These methods have similar parameters to the model serialization methods.

Sources:

- [pydantic/type\_adapter.py519-584](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L519-L584)

### Serialization with Computed Fields

Computed fields (defined using the `@computed_field` decorator) are included in serialization by default:

```
```

When serializing a `Rectangle` instance, the `area` field will be included in the output.

Sources:

- [tests/test\_computed\_fields.py27-66](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L27-L66)

## Advanced Serialization Techniques

### Conditional Serialization

You can conditionally apply serializers based on the serialization mode:

```
```

In this example, the serializer is only applied when serializing to JSON.

Sources:

- [tests/test\_serialize.py171-182](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L171-L182)

### Serialization in Dataclasses

Pydantic's dataclasses support the same serialization features as models:

```
```

Sources:

- [pydantic/dataclasses.py170-180](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L170-L180)
- [tests/test\_dataclasses.py1220-1272](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L1220-L1272)

### Root Model Serialization

`RootModel` instances are serialized to their root value rather than a dictionary:

```
```

Sources:

- [pydantic/root\_model.py119-146](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L119-L146)

## Integration with pydantic-core

Pydantic uses `pydantic-core` for the actual serialization logic. The `SchemaSerializer` class from `pydantic-core` handles the serialization process.

```
```

During model definition, Pydantic generates a serialization schema that incorporates all custom serializers. This schema is then used by `pydantic-core` to perform the actual serialization.

Sources:

- [pydantic/\_internal/\_schema\_generation\_shared.py1-142](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_schema_generation_shared.py#L1-L142)
- [pydantic/\_internal/\_mock\_val\_ser.py1-69](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_mock_val_ser.py#L1-L69)

### Deferred Building and Mocking

Pydantic supports deferred building of serializers. When `defer_build=True` is set in the config, Pydantic creates mock serializers that are replaced with real serializers when needed.

This allows for forward references and circular dependencies in models:

```
```

Sources:

- [pydantic/\_internal/\_mock\_val\_ser.py70-110](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_mock_val_ser.py#L70-L110)
- [pydantic/\_internal/\_dataclasses.py128-134](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L128-L134)

## Best Practices for Serializers

1. **Choose the right serializer type**:

   - Use field serializers for customizing individual fields
   - Use model serializers for complex model-level serialization
   - Use functional serializers for reusable serialization logic

2. **Respect the serialization mode**:

   - Use the `info.mode` parameter to adjust behavior based on the serialization mode
   - Use `when_used` to apply serializers only in specific scenarios

3. **Be mindful of performance**:

   - Use plain serializers for simple transformations
   - Use wrap serializers when you need to modify the default serialization behavior

4. **Handle None values appropriately**:

   - Use `when_used='unless-none'` to skip serialization of None values
   - Explicitly handle None values in your serializers to avoid errors

5. **Provide return types**:

   - Specify the `return_type` parameter to ensure correct JSON schema generation
   - Use type annotations in your serializer functions for better IDE support

Sources:

- [tests/test\_serialize.py171-197](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L171-L197)
- [pydantic/functional\_serializers.py18-52](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L18-L52)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Serializers](#serializers.md)
- [Overview of the Serialization System](#overview-of-the-serialization-system.md)
- [Core Serialization Components](#core-serialization-components.md)
- [Serialization Modes](#serialization-modes.md)
- [Field Serializers](#field-serializers.md)
- [Using the field\_serializer Decorator](#using-the-field_serializer-decorator.md)
- [Field Serializer Signature](#field-serializer-signature.md)
- [Functional Serializers](#functional-serializers.md)
- [PlainSerializer](#plainserializer.md)
- [WrapSerializer](#wrapserializer.md)
- [Model Serializers](#model-serializers.md)
- [Using the model\_serializer Decorator](#using-the-model_serializer-decorator.md)
- [Model Serializer Modes](#model-serializer-modes.md)
- [Serialization Process](#serialization-process.md)
- [Core Serialization Methods](#core-serialization-methods.md)
- [Serialization in TypeAdapter](#serialization-in-typeadapter.md)
- [Serialization with Computed Fields](#serialization-with-computed-fields.md)
- [Advanced Serialization Techniques](#advanced-serialization-techniques.md)
- [Conditional Serialization](#conditional-serialization.md)
- [Serialization in Dataclasses](#serialization-in-dataclasses.md)
- [Root Model Serialization](#root-model-serialization.md)
- [Integration with pydantic-core](#integration-with-pydantic-core.md)
- [Deferred Building and Mocking](#deferred-building-and-mocking.md)
- [Best Practices for Serializers](#best-practices-for-serializers.md)
