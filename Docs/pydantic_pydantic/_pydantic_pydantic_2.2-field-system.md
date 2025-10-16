Field System | pydantic/pydantic | DeepWiki

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

# Field System

Relevant source files

- [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)
- [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)
- [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)
- [tests/test\_create\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py)
- [tests/test\_edge\_cases.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py)
- [tests/test\_main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py)
- [tests/test\_private\_attributes.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_private_attributes.py)

The Pydantic Field System provides the foundation for defining, validating, and customizing fields within Pydantic models. This page explains how fields are defined, their internal representation, and how they interact with the model validation and serialization processes. For information about validators that operate on fields, see [Validators](pydantic/pydantic/4.1-validators.md). For model configuration options affecting fields, see [Model Configuration](pydantic/pydantic/2.3-model-configuration.md).

## Overview

The Field System consists of several key components:

1. **Field Definition**: How fields are declared in model classes using type annotations and the `Field()` function
2. **FieldInfo**: The internal class that stores field metadata and configuration
3. **Field Processing**: How declared fields are processed during model creation
4. **Field Lifecycle**: How fields behave during validation, access, and serialization

```
```

Sources: [pydantic/fields.py99-206](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L99-L206) [pydantic/main.py203-206](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L203-L206)

## Defining Fields

Fields in Pydantic models are defined through type annotations, with optional default values and field customizations.

### Basic Field Definition

The simplest way to define a field is with a type annotation:

```
```

Fields without default values are **required** fields, while fields with default values are **optional**.

Sources: [tests/test\_main.py56-65](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L56-L65) [tests/test\_main.py519-533](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L519-L533)

### Field Customization with Field()

For more advanced field configuration, use the `Field()` function:

```
```

The `Field()` function accepts numerous parameters to customize field behavior, including:

- **default**: Default value for the field
- **default\_factory**: Callable that returns a default value
- **alias**: Alternative name for the field during parsing
- **validation\_alias**: Alias used during validation
- **serialization\_alias**: Alias used during serialization
- **title**, **description**: Documentation metadata
- **examples**: Example values for documentation
- **exclude**: Whether to exclude in serialization
- **Validation constraints**: gt, ge, lt, le, multiple\_of, min\_length, max\_length, pattern, etc.

Sources: [pydantic/fields.py209-290](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L209-L290) [tests/test\_main.py154-166](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L154-L166)

## Field Information (FieldInfo)

The `FieldInfo` class is the internal representation of field metadata in Pydantic. Each field defined in a model is represented by a `FieldInfo` instance.

```
```

Sources: [pydantic/fields.py99-187](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L99-L187) [pydantic/fields.py589-673](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L589-L673)

### Key FieldInfo Attributes

- **annotation**: The field's type annotation
- **default**: The default value for the field
- **default\_factory**: Callable that returns a default value
- **alias**: Alternative name for the field (used for both validation and serialization)
- **validation\_alias/serialization\_alias**: Specific aliases for validation and serialization
- **metadata**: List of constraints and validation rules

### Accessing Field Information

Model fields can be accessed through the `model_fields` class attribute:

```
```

Sources: [pydantic/main.py266-286](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L266-L286) [tests/test\_main.py110-112](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L110-L112)

## Field Processing Flow

When a Pydantic model is defined, the fields go through a processing flow to collect and validate field definitions.

```
```

Sources: [pydantic/\_internal/\_model\_construction.py363-455](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L363-L455) [pydantic/\_internal/\_model\_construction.py221-224](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L221-L224)

### Field Collection Process

1. During model class creation, the `ModelMetaclass` processes class attributes
2. Type annotations from `__annotations__` are analyzed
3. Attributes with type annotations become model fields
4. `Field()` instances are processed to collect metadata
5. Other attributes without annotations are checked for possible field intent (with warnings)
6. Fields are stored in the class's `__pydantic_fields__` attribute

Sources: [pydantic/\_internal/\_model\_construction.py80-258](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L80-L258) [pydantic/fields.py291-366](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L291-L366)

## Field Types and Validation

Pydantic supports a wide range of field types, each with appropriate validation:

| Type Category     | Examples                           | Validation Behavior                                       |
| ----------------- | ---------------------------------- | --------------------------------------------------------- |
| Simple Types      | `int`, `float`, `str`, `bool`      | Type coercion and standard validation                     |
| Collection Types  | `list`, `set`, `tuple`, `dict`     | Item-by-item validation with inner type checking          |
| Complex Types     | `datetime`, `UUID`, custom classes | Type-specific validation logic                            |
| Union Types       | `Union[str, int]`, `Optional[str]` | Try each type in sequence                                 |
| Constrained Types | `conint`, `constr`                 | Apply additional constraints                              |
| Custom Types      | User-defined classes               | Validate using schema from `__get_pydantic_core_schema__` |

Fields can have validators defined at several levels:

- Standard type validation
- Constraints defined in `Field()`
- Model-level validators (see [Validators](pydantic/pydantic/4.1-validators.md))

Sources: [tests/test\_edge\_cases.py62-176](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py#L62-L176) [tests/test\_edge\_cases.py177-295](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py#L177-L295)

## Field Lifecycle

Fields in Pydantic go through a complete lifecycle from definition to usage:

```
```

Sources: [pydantic/main.py243-261](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L243-L261) [pydantic/main.py421-477](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L421-L477)

### Model Instantiation

During model instantiation, Pydantic:

1. Takes input data and matches it to field names or aliases
2. Validates each field's value against its expected type and constraints
3. Stores successfully validated values in the model instance

### Field Access

Once a model is instantiated, fields can be accessed as normal attributes:

```
```

### Serialization

When a model is serialized (e.g., via `model_dump()` or `model_dump_json()`), fields are:

1. Converted to their serialized form (based on field type and serializers)
2. Included/excluded based on field configuration and serialization options
3. Named according to serialization aliases if defined

Sources: [pydantic/main.py421-533](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L421-L533) [tests/test\_json.py151-188](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L151-L188)

## Advanced Field Features

### Field Aliases

Aliases provide alternative names for fields, useful for mapping to external data formats:

```
```

- **alias**: Used for both validation and serialization
- **validation\_alias**: Used only during validation (parsing input)
- **serialization\_alias**: Used only during serialization (output)

Aliases can be simple strings or complex paths using dot notation (for nested data) or AliasPath objects.

Sources: [pydantic/fields.py231-235](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L231-L235) [tests/test\_main.py499-506](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L499-L506)

### Default Values and Factories

Fields can have static default values or dynamic defaults via factory functions:

```
```

When a default factory is provided:

- It's called when a field value isn't provided
- It can optionally use already validated data if the factory accepts a parameter

Sources: [pydantic/fields.py226-230](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L226-L230) [pydantic/fields.py609-645](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L609-L645)

### Field Constraints

Fields can have various constraints applied directly in the `Field()` function:

```
```

These constraints are stored in the field's metadata and applied during validation.

Sources: [pydantic/fields.py191-207](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L191-L207) [tests/test\_edge\_cases.py616-631](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py#L616-L631)

### Frozen Fields

Individual fields can be marked as immutable with `frozen=True`:

```
```

Attempts to modify a frozen field will raise a ValidationError.

Sources: [pydantic/fields.py247](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L247-L247) [tests/test\_main.py591-611](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L591-L611)

### Private Attributes

Private attributes are defined using underscore-prefixed names and aren't included in validation or serialization processes:

```
```

For more control, the `PrivateAttr` class can be used:

```
```

Sources: [tests/test\_create\_model.py64-72](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py#L64-L72) [pydantic/fields.py437-441](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L437-L441)

## Integration with Model System

The Field System integrates deeply with Pydantic's model system:

```
```

Sources: [pydantic/\_internal/\_model\_construction.py80-258](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L80-L258) [pydantic/main.py243-405](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L243-L405)

### Fields and Validation

During validation:

1. Input data is matched to fields by name or aliases
2. Each field's value is validated against its type and constraints
3. Default values are applied for missing fields
4. Validated values are stored in the model instance

### Fields and Serialization

During serialization:

1. Field values are retrieved from the model instance
2. Values are converted according to their serialization rules
3. Fields are included/excluded based on configuration and options
4. Field names are mapped to aliases if specified

## Practical Examples

### Complete Example with Various Field Types

```
```

### Example with Aliases

```
```

## Conclusion

The Field System is a fundamental part of Pydantic that enables type annotations to be transformed into powerful validation, documentation, and serialization tools. By leveraging the features of the Field System, you can create robust data models with precise validation rules and customized serialization behavior.

Key takeaways:

- Fields are defined using type annotations and the `Field()` function
- Each field has a corresponding `FieldInfo` object storing its metadata
- Fields support various validation constraints, aliases, and customization options
- The Field System integrates with Pydantic's validation and serialization processes

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Field System](#field-system.md)
- [Overview](#overview.md)
- [Defining Fields](#defining-fields.md)
- [Basic Field Definition](#basic-field-definition.md)
- [Field Customization with Field()](#field-customization-with-field.md)
- [Field Information (FieldInfo)](#field-information-fieldinfo.md)
- [Key FieldInfo Attributes](#key-fieldinfo-attributes.md)
- [Accessing Field Information](#accessing-field-information.md)
- [Field Processing Flow](#field-processing-flow.md)
- [Field Collection Process](#field-collection-process.md)
- [Field Types and Validation](#field-types-and-validation.md)
- [Field Lifecycle](#field-lifecycle.md)
- [Model Instantiation](#model-instantiation.md)
- [Field Access](#field-access.md)
- [Serialization](#serialization.md)
- [Advanced Field Features](#advanced-field-features.md)
- [Field Aliases](#field-aliases.md)
- [Default Values and Factories](#default-values-and-factories.md)
- [Field Constraints](#field-constraints.md)
- [Frozen Fields](#frozen-fields.md)
- [Private Attributes](#private-attributes.md)
- [Integration with Model System](#integration-with-model-system.md)
- [Fields and Validation](#fields-and-validation.md)
- [Fields and Serialization](#fields-and-serialization.md)
- [Practical Examples](#practical-examples.md)
- [Complete Example with Various Field Types](#complete-example-with-various-field-types.md)
- [Example with Aliases](#example-with-aliases.md)
- [Conclusion](#conclusion.md)
