RootModel and Computed Fields | pydantic/pydantic | DeepWiki

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

# RootModel and Computed Fields

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

This page documents two distinct but complementary features: **RootModel** for validating root-level values, and **Computed Fields** for adding dynamic, read-only properties to models that appear during serialization.

For basic model functionality, see [BaseModel](pydantic/pydantic/2.1-basemodel.md). For field configuration and metadata, see [Field System](pydantic/pydantic/2.2-field-system.md). For serialization customization, see [Serializers](pydantic/pydantic/4.2-serializers.md).

---

## Overview

**RootModel** enables validation of types that don't naturally fit into Pydantic's field-based structure. Instead of defining multiple fields, a RootModel wraps a single root value of any type (primitives, collections, custom types, etc.).

**Computed Fields** are dynamic properties decorated with `@computed_field` that are calculated on-access and automatically included in serialization output. Unlike regular properties, computed fields appear in `model_dump()`, `model_dump_json()`, and JSON schema generation.

---

## RootModel

### Purpose and Design

RootModel provides a way to validate and serialize root-level values that are not traditional models with named fields. This is useful for:

- Wrapping primitive types with validation logic
- Validating collection types (lists, dicts) at the root level
- Creating type aliases with custom validation
- Building discriminated union handlers
- Parsing configuration formats where the entire structure is a single type

**Sources:** [pydantic/root\_model.py1-155](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L1-L155)

### Core Architecture

```
```

**Sources:** [pydantic/root\_model.py32-155](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L32-L155) [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)

### Basic Usage

The `root` field contains the validated value. RootModel can be instantiated with either a positional argument or keyword arguments:

```
```

**Sources:** [pydantic/root\_model.py60-69](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L60-L69) [tests/test\_root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_root_model.py)

### Key Characteristics

| Characteristic     | Behavior                                             | Rationale                                  |
| ------------------ | ---------------------------------------------------- | ------------------------------------------ |
| Single field       | Only `root` field exists                             | RootModel represents a single value        |
| Extra fields       | Not supported (`model_config['extra']` raises error) | Would conflict with root-level validation  |
| Private attributes | Set to `None`                                        | Root models don't support `_private` attrs |
| Initialization     | Accepts positional or keyword args                   | Flexible instantiation patterns            |
| Validation         | Applied to `root` value                              | Standard validation pipeline               |
| Serialization      | Returns root value directly in `model_dump()`        | Not wrapped in a dict                      |

**Sources:** [pydantic/root\_model.py52-58](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L52-L58) [pydantic/root\_model.py60-69](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L60-L69)

### Initialization Flow

```
```

**Sources:** [pydantic/root\_model.py60-69](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L60-L69) [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)

### Construction and Copying

RootModel provides special methods for construction and copying:

**model\_construct**: Creates instances without validation

```
```

**Copy operations**: Shallow and deep copy support via `__copy__` and `__deepcopy__`

**Pickle support**: Via `__getstate__` and `__setstate__` for serialization

**Sources:** [pydantic/root\_model.py72-114](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L72-L114) [tests/test\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_construction.py)

### Serialization Behavior

Unlike regular models, RootModel's `model_dump()` returns the root value directly, not a dictionary:

```
```

This behavior is controlled by the model's serialization schema and differs from BaseModel to match the semantic meaning of a "root" value.

**Sources:** [pydantic/root\_model.py116-144](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L116-L144) [tests/test\_root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_root_model.py)

---

## Computed Fields

### Purpose and Design

Computed fields are dynamic properties that:

1. Are calculated on-access (not stored in `__dict__`)
2. Automatically appear in serialization (`model_dump()`, `model_dump_json()`)
3. Generate JSON schema with `readOnly: true`
4. Can have custom serializers applied
5. Support property setters and deleters

They bridge the gap between regular properties (not serialized) and model fields (stored and validated).

**Sources:** [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py) [tests/test\_computed\_fields.py27-66](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L27-L66)

### Core Components

```
```

**Sources:** [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py) [pydantic/\_internal/\_decorators.py427](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L427-L427) [tests/test\_computed\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py)

### Basic Usage

The `@computed_field` decorator can be used directly or with the `@property` decorator:

```
```

**Sources:** [tests/test\_computed\_fields.py27-66](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L27-L66)

### Field Metadata and Configuration

Computed fields support the same metadata as regular fields:

| Parameter           | Type   | Purpose                                 | Example                         |
| ------------------- | ------ | --------------------------------------- | ------------------------------- |
| `title`             | `str`  | JSON schema title                       | `title='Area'`                  |
| `description`       | `str`  | Documentation                           | `description='Calculated area'` |
| `examples`          | `list` | Example values                          | `examples=[100, 200]`           |
| `json_schema_extra` | `dict` | Additional JSON schema properties       | `json_schema_extra={'foo': 42}` |
| `alias`             | `str`  | Serialization alias                     | `alias='the_area'`              |
| `repr`              | `bool` | Include in `__repr__` (default: `True`) | `repr=False`                    |
| `return_type`       | `type` | Override inferred return type           | `return_type=float`             |

**Sources:** [tests/test\_computed\_fields.py68-121](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L68-L121) [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)

### Computed Field Lifecycle

```
```

**Sources:** [tests/test\_computed\_fields.py27-66](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L27-L66) [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)

### Property Setters and Deleters

Computed fields can have setters and deleters like regular properties:

```
```

**Sources:** [tests/test\_computed\_fields.py123-176](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L123-L176)

### Serialization Customization

Computed fields can be customized with `@field_serializer`:

```
```

**Sources:** [tests/test\_computed\_fields.py123-150](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L123-L150) [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)

### Cached Properties

Computed fields work with `functools.cached_property` for performance:

```
```

**Sources:** [tests/test\_computed\_fields.py178-214](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L178-L214)

### JSON Schema Generation

Computed fields appear in JSON schema with `readOnly: true`:

```
```

The `readOnly` flag indicates that the field is computed during serialization and cannot be provided during validation.

**Sources:** [tests/test\_computed\_fields.py68-121](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L68-L121) [pydantic/json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py)

### Include/Exclude Behavior

Computed fields respect include/exclude parameters in serialization:

```
```

**Sources:** [tests/test\_computed\_fields.py287-309](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L287-L309) [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)

---

## Storage and Access Patterns

### Field vs Computed Field Comparison

```
```

| Feature              | Regular Field | Computed Field | Regular Property |
| -------------------- | ------------- | -------------- | ---------------- |
| Validated at init    | ✓             | ✗              | ✗                |
| Stored in `__dict__` | ✓             | ✗              | ✗                |
| In `model_dump()`    | ✓             | ✓              | ✗                |
| In JSON schema       | ✓             | ✓ (readOnly)   | ✗                |
| Can have setter      | ✗             | ✓              | ✓                |
| Cached by default    | ✓             | ✗              | ✗                |
| Computed on access   | ✗             | ✓              | ✓                |

**Sources:** [tests/test\_computed\_fields.py27-66](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L27-L66) [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)

---

## Integration with Validation and Serialization

### Computed Fields in Validation Pipeline

Computed fields are **not** part of the validation pipeline. They are only evaluated during serialization or when accessed as properties.

```
```

**Sources:** [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py) [tests/test\_computed\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py)

### Decorator Processing Flow

```
```

**Sources:** [pydantic/\_internal/\_decorators.py427](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L427-L427) [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py) [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)

---

## Code Entity Reference

### RootModel Implementation

| Class/Function                | Location                                                                                                          | Purpose                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `RootModel`                   | [pydantic/root\_model.py32](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L32-L32)    | Main RootModel class definition |
| `RootModel.__init__`          | [pydantic/root\_model.py60-69](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L60-L69) | Initialize with root value      |
| `RootModel.model_construct`   | [pydantic/root\_model.py72-86](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L72-L86) | Construct without validation    |
| `RootModel.__init_subclass__` | [pydantic/root\_model.py52-58](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L52-L58) | Check extra config not set      |
| `_RootModelMetaclass`         | [pydantic/root\_model.py25](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L25-L25)    | Metaclass for RootModel         |

**Sources:** [pydantic/root\_model.py1-155](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py#L1-L155)

### Computed Field Implementation

| Class/Function                   | Location                                                                                                                                 | Purpose                                |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `@computed_field`                | [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)                                              | Decorator for computed fields          |
| `ComputedFieldInfo`              | [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)                                              | Metadata container for computed fields |
| `DecoratorInfos.computed_fields` | [pydantic/\_internal/\_decorators.py427](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py#L427-L427) | Storage in decorator info              |
| `model_computed_fields`          | [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)                                                  | ClassVar dict of computed fields       |

**Sources:** [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py) [pydantic/\_internal/\_decorators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_decorators.py)

### Schema Generation

| Function                          | Location                                                                                                                               | Purpose                            |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `computed_field_schema()`         | [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py) | Generate schema for computed field |
| `_computed_field_common_schema()` | [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py) | Common schema logic                |

**Sources:** [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [RootModel and Computed Fields](#rootmodel-and-computed-fields.md)
- [Overview](#overview.md)
- [RootModel](#rootmodel.md)
- [Purpose and Design](#purpose-and-design.md)
- [Core Architecture](#core-architecture.md)
- [Basic Usage](#basic-usage.md)
- [Key Characteristics](#key-characteristics.md)
- [Initialization Flow](#initialization-flow.md)
- [Construction and Copying](#construction-and-copying.md)
- [Serialization Behavior](#serialization-behavior.md)
- [Computed Fields](#computed-fields.md)
- [Purpose and Design](#purpose-and-design-1.md)
- [Core Components](#core-components.md)
- [Basic Usage](#basic-usage-1.md)
- [Field Metadata and Configuration](#field-metadata-and-configuration.md)
- [Computed Field Lifecycle](#computed-field-lifecycle.md)
- [Property Setters and Deleters](#property-setters-and-deleters.md)
- [Serialization Customization](#serialization-customization.md)
- [Cached Properties](#cached-properties.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [Include/Exclude Behavior](#includeexclude-behavior.md)
- [Storage and Access Patterns](#storage-and-access-patterns.md)
- [Field vs Computed Field Comparison](#field-vs-computed-field-comparison.md)
- [Integration with Validation and Serialization](#integration-with-validation-and-serialization.md)
- [Computed Fields in Validation Pipeline](#computed-fields-in-validation-pipeline.md)
- [Decorator Processing Flow](#decorator-processing-flow.md)
- [Code Entity Reference](#code-entity-reference.md)
- [RootModel Implementation](#rootmodel-implementation.md)
- [Computed Field Implementation](#computed-field-implementation.md)
- [Schema Generation](#schema-generation.md)
