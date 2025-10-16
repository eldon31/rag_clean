Validators | pydantic/pydantic | DeepWiki

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

# Validators

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

Validators in Pydantic are powerful tools for customizing validation logic beyond simple type checking. They allow you to validate and transform data during model creation or when field values change, ensuring data meets specific requirements, enforcing business rules, and modifying values as needed.

For information about serializers, which handle converting data out of Pydantic models, see [Serializers](pydantic/pydantic/4.2-serializers.md).

## Validation Pipeline

The Pydantic validation process follows a structured pipeline to transform raw input data into validated model instances:

```
```

Sources:

- [tests/test\_validators.py312-384](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L312-L384)
- [tests/test\_validators.py192-215](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L192-L215)

## Field Validators

Field validators work on individual fields and are defined with the `@field_validator` decorator. They can validate or transform field values before or after standard validation.

### Basic Usage

```
```

When validators raise an error, Pydantic will include this in the `ValidationError` with contextual information about which field failed and why.

Sources:

- [tests/test\_validators.py192-215](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L192-L215)

### Validator Modes

Field validators can operate in different modes that determine when they run in the validation pipeline:

- `mode='before'`: Runs before type coercion, useful for custom parsing or transforming raw input data
- `mode='after'`: Runs after type coercion (default), for validating properly typed values
- `mode='plain'`: Similar to 'after' but with a simpler function signature
- `mode='wrap'`: Advanced mode that wraps around standard validation, giving access to both pre- and post-validation values

```
```

Sources:

- [tests/test\_validators.py313-329](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L313-L329)
- [pydantic/\_internal/\_decorators.py518-552](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L518-L552)

### Multi-field Validators

Validators can be applied to multiple fields at once:

```
```

The `info` parameter provides context about the current validation, including the field being validated and model data.

Sources:

- [tests/test\_validators.py486-518](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L486-L518)

### Wildcard Validators

Use `'*'` to apply a validator to all fields:

```
```

Sources:

- [tests/test\_validators.py860-869](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L860-L869)
- [tests/test\_validators.py728-759](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L728-L759)

### Validator Information

Validators can accept a `ValidationInfo` parameter to access additional context:

```
```

Sources:

- [tests/test\_validators.py462-483](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L462-L483)
- [tests/test\_validators.py394-406](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L394-L406)

## Model Validators

Model validators validate entire models, enabling validation logic that depends on multiple fields:

```
```

Model validators can run in three modes:

- `mode='before'`: Runs before field validation, useful for pre-processing raw input data
- `mode='after'`: Runs after field validation (default), for validating the model as a whole
- `mode='wrap'`: Wraps the validation process, giving full control over the validation pipeline

Sources:

- [pydantic/\_internal/\_decorators.py141-143](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L141-L143)

## Functional Validators

Functional validators are used with `Annotated` types and provide a reusable way to apply validation logic:

```
```

### Types of Functional Validators

- **BeforeValidator**: Runs before standard validation, useful for pre-processing input
- **AfterValidator**: Runs after standard validation, for additional checks on typed data
- **PlainValidator**: Direct validator without standard validation
- **WrapValidator**: Gives full control over the validation process

### Examples

```
```

Sources:

- [tests/test\_validators.py51-166](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L51-L166)

## Root Validators (Deprecated)

The `@root_validator` decorator from Pydantic v1 has been deprecated in favor of `@model_validator`. Root validators still work but will emit deprecation warnings.

```
```

Sources:

- [tests/test\_validators.py1046-1083](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L1046-L1083)
- [pydantic/\_internal/\_decorators.py76-88](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L76-L88)

## Validator Inheritance

Validators are inherited when subclassing models. If a subclass defines a validator with the same name as a parent class validator, the subclass validator overrides the parent's.

```
```

Sources:

- [tests/test\_validators.py820-927](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L820-L927)
- [tests/test\_validators.py995-1037](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L995-L1037)

## Advanced Usage

### Validating Collections

For validating each item in collections, the classic approach of using `each_item=True` with the `@validator` decorator is deprecated. Instead, use validator functions directly with the collection's item type:

```
```

Sources:

- [tests/test\_validators.py1086-1126](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L1086-L1126)

### Validation on Assignment

By default, validators only run during model initialization. To run them when values are assigned, set `validate_assignment=True` in model config:

```
```

Sources:

- [tests/test\_validators.py387-483](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L387-L483)

### Validators with Default Values

To validate default values, use `validate_default=True` in the field:

```
```

Sources:

- [tests/test\_validators.py637-653](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L637-L653)
- [tests/test\_validators.py678-695](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L678-L695)

## Core Internals

Internally, validators are processed by the Pydantic Core engine, which converts them into a validation schema:

```
```

Field validators and model validators are stored in specialized container classes (`DecoratorInfos`) during model creation and used to build the final validation schema.

Sources:

- [pydantic/\_internal/\_decorators.py412-515](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L412-L515)
- [pydantic/\_internal/\_core\_utils.py16-42](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_utils.py#L16-L42)

## Combining Validators with Constrained Types

Validators can be combined with constrained types from `annotated_types` for powerful, reusable validation:

```
```

Sources:

- [pydantic/\_internal/\_known\_annotated\_metadata.py168-347](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_known_annotated_metadata.py#L168-L347)
- [tests/test\_annotated.py51-62](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_annotated.py#L51-L62)

## Best Practices

1. Use `@field_validator` for field-specific validation
2. Use `@model_validator` for validations that involve multiple fields
3. Use functional validators with `Annotated` for reusable validation logic
4. Always use `@classmethod` when defining class-based validators
5. Return the value from validators to pass it to the next validator in the pipeline
6. Use `ValidationInfo` to access contextual information during validation

By combining these validator types, you can build complex validation rules while keeping your code modular and maintainable.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Validators](#validators.md)
- [Validation Pipeline](#validation-pipeline.md)
- [Field Validators](#field-validators.md)
- [Basic Usage](#basic-usage.md)
- [Validator Modes](#validator-modes.md)
- [Multi-field Validators](#multi-field-validators.md)
- [Wildcard Validators](#wildcard-validators.md)
- [Validator Information](#validator-information.md)
- [Model Validators](#model-validators.md)
- [Functional Validators](#functional-validators.md)
- [Types of Functional Validators](#types-of-functional-validators.md)
- [Examples](#examples.md)
- [Root Validators (Deprecated)](#root-validators-deprecated.md)
- [Validator Inheritance](#validator-inheritance.md)
- [Advanced Usage](#advanced-usage.md)
- [Validating Collections](#validating-collections.md)
- [Validation on Assignment](#validation-on-assignment.md)
- [Validators with Default Values](#validators-with-default-values.md)
- [Core Internals](#core-internals.md)
- [Combining Validators with Constrained Types](#combining-validators-with-constrained-types.md)
- [Best Practices](#best-practices.md)
