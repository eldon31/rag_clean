Validation and Serialization | pydantic/pydantic | DeepWiki

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

# Validation and Serialization

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

This page provides an overview of Pydantic's validation and serialization architecture, explaining how data is validated when creating models and serialized when outputting data. For information on schema generation, see [Schema Generation](pydantic/pydantic/5-schema-generation.md).

## Overview

At the core of Pydantic's functionality are two fundamental processes:

1. **Validation**: Converting and validating input data against model schema definitions
2. **Serialization**: Converting validated models into standard formats like Python dictionaries and JSON

These processes work together to ensure that data flowing into and out of your application is consistent, type-safe, and properly formatted.

```
```

Sources: [pydantic/functional\_validators.py27-323](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py#L27-L323) [pydantic/functional\_serializers.py19-89](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L19-L89)

## Validation Architecture

Validation ensures that input data conforms to the defined model schema. Pydantic leverages a layered architecture that processes data through several validation stages.

### Core Validation Components

```
```

Sources: [pydantic/functional\_validators.py27-156](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py#L27-L156) [pydantic/\_internal/\_decorators.py30-154](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L30-L154)

### Validator Types and Functions

Pydantic offers several types of validators that can be applied at different stages of the validation process:

1. **Field Validators**: Apply to specific fields using the `@field_validator` decorator
2. **Model Validators**: Apply to the entire model using the `@model_validator` decorator
3. **Functional Validators**: Used with `Annotated` types to apply validation to specific types

The functional validators include:

- **BeforeValidator**: Executes before the standard validation
- **AfterValidator**: Executes after the standard validation
- **PlainValidator**: Replaces the standard validation
- **WrapValidator**: Wraps around the standard validation, providing access to both the input and the standard validation function

```
```

Sources: [pydantic/functional\_validators.py70-327](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py#L70-L327) [tests/test\_validators.py51-156](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L51-L156)

### Validation Process

When validating data, Pydantic follows this general process:

1. Apply any `BeforeValidator` or `WrapValidator` functions
2. Perform standard type coercion and validation
3. Apply any `AfterValidator` functions
4. Apply model-level validators
5. Construct the validated model

This pipeline allows for powerful and flexible validation at different stages.

```
```

Sources: [tests/test\_validators.py87-156](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L87-L156) [tests/test\_validators.py192-300](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L192-L300)

## Serialization Architecture

Serialization converts validated Pydantic models into Python dictionaries, JSON, or other formats. Like validation, serialization uses a modular architecture.

### Core Serialization Components

```
```

Sources: [pydantic/functional\_serializers.py19-195](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L19-L195) [tests/test\_serialize.py33-109](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L33-L109)

### Serializer Types

Pydantic offers several types of serializers:

1. **Field Serializers**: Customize serialization for specific fields using the `@field_serializer` decorator
2. **Model Serializers**: Customize serialization for the entire model using the `@model_serializer` decorator
3. **Functional Serializers**: Used with `Annotated` types to apply serialization to specific types

The functional serializers include:

- **PlainSerializer**: Directly determines the serialized output
- **WrapSerializer**: Wraps around the standard serialization, providing access to both the input and the standard serialization function

```
```

Sources: [pydantic/functional\_serializers.py19-89](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L19-L89) [pydantic/functional\_serializers.py89-195](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py#L89-L195)

### Serialization Process

When serializing data, Pydantic follows this general process:

1. Determine the serialization mode (Python, JSON)
2. Apply field-specific serializers
3. Apply model-level serializers
4. Convert to the target format (dict, JSON string)

This pipeline allows for customizable serialization at different levels.

```
```

Sources: [tests/test\_serialize.py82-109](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L82-L109) [tests/test\_serialize.py148-198](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L148-L198)

## TypeAdapter Integration

The `TypeAdapter` class extends validation and serialization capabilities to arbitrary Python types, not just Pydantic models.

```
```

TypeAdapter leverages the same core validation and serialization mechanisms as Pydantic models, but applies them to arbitrary types:

```
```

Sources: [pydantic/type\_adapter.py69-476](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L69-L476) [tests/test\_type\_adapter.py42-112](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py#L42-L112)

## Validation and Serialization with Dataclasses

Pydantic's validation and serialization also work with dataclasses through the `@pydantic.dataclasses.dataclass` decorator.

```
```

The dataclass implementation uses the same validation and serialization mechanism as regular Pydantic models:

```
```

Sources: [pydantic/dataclasses.py98-282](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L98-L282) [pydantic/\_internal/\_dataclasses.py64-112](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L64-L112) [tests/test\_dataclasses.py62-147](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L62-L147)

## Common Validation and Serialization Scenarios

### Field-Level Validation

```
```

### Model-Level Validation

```
```

### Custom Serialization

```
```

Sources: [tests/test\_validators.py192-216](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L192-L216) [tests/test\_serialize.py148-170](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L148-L170)

## Using Annotated for Validation and Serialization

Pydantic supports using the `Annotated` type to attach validators and serializers directly to type annotations:

```
```

This approach allows for reusable validation and serialization logic that can be applied to multiple fields across different models.

Sources: [tests/test\_validators.py51-87](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L51-L87) [tests/test\_serialize.py82-96](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L82-L96)

## Validation and Serialization Modes

Both validation and serialization offer different modes:

### Validation Modes:

- **Standard**: Regular field-by-field validation
- **Strict**: Enforces exact type matches without coercion

### Serialization Modes:

- **python**: Serializes to Python native types (dict, list, etc.)
- **json**: Serializes to JSON-compatible Python types
- **json string**: Directly serializes to a JSON string

```
```

Sources: [tests/test\_serialize.py82-109](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L82-L109) [tests/test\_serialize.py171-197](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py#L171-L197)

## Conclusion

Pydantic's validation and serialization systems provide a robust foundation for ensuring data quality and consistency. The architecture allows for customization at various levels, from field-specific validators to model-wide serializers. These systems work together to provide a seamless flow from raw input data to validated models and then to serialized output.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Validation and Serialization](#validation-and-serialization.md)
- [Overview](#overview.md)
- [Validation Architecture](#validation-architecture.md)
- [Core Validation Components](#core-validation-components.md)
- [Validator Types and Functions](#validator-types-and-functions.md)
- [Validation Process](#validation-process.md)
- [Serialization Architecture](#serialization-architecture.md)
- [Core Serialization Components](#core-serialization-components.md)
- [Serializer Types](#serializer-types.md)
- [Serialization Process](#serialization-process.md)
- [TypeAdapter Integration](#typeadapter-integration.md)
- [Validation and Serialization with Dataclasses](#validation-and-serialization-with-dataclasses.md)
- [Common Validation and Serialization Scenarios](#common-validation-and-serialization-scenarios.md)
- [Field-Level Validation](#field-level-validation.md)
- [Model-Level Validation](#model-level-validation.md)
- [Custom Serialization](#custom-serialization.md)
- [Using Annotated for Validation and Serialization](#using-annotated-for-validation-and-serialization.md)
- [Validation and Serialization Modes](#validation-and-serialization-modes.md)
- [Validation Modes:](#validation-modes.md)
- [Serialization Modes:](#serialization-modes.md)
- [Conclusion](#conclusion.md)
