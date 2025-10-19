pydantic/pydantic | DeepWiki

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

# Overview

Relevant source files

- [.pre-commit-config.yaml](https://github.com/pydantic/pydantic/blob/76ef0b08/.pre-commit-config.yaml)
- [CITATION.cff](https://github.com/pydantic/pydantic/blob/76ef0b08/CITATION.cff)
- [HISTORY.md](https://github.com/pydantic/pydantic/blob/76ef0b08/HISTORY.md)
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
- [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)
- [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)
- [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)
- [pydantic/version.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py)
- [release/README.md](https://github.com/pydantic/pydantic/blob/76ef0b08/release/README.md)
- [tests/test\_create\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py)
- [tests/test\_edge\_cases.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py)
- [tests/test\_main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py)
- [tests/test\_private\_attributes.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_private_attributes.py)
- [uv.lock](https://github.com/pydantic/pydantic/blob/76ef0b08/uv.lock)

This document provides a high-level introduction to Pydantic's architecture, core concepts, and design philosophy. It explains what Pydantic is, its relationship with pydantic-core, and how the major systems interact.

For detailed information about specific subsystems, see:

- Model system details: [Core Model System](pydantic/pydantic/2-core-model-system.md)
- Type system details: [Type System](pydantic/pydantic/3-type-system.md)
- Validation and serialization: [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md)
- Schema generation: [Schema Generation](pydantic/pydantic/5-schema-generation.md)

## What is Pydantic

Pydantic is a data validation library for Python that uses Python type hints to validate, parse, and serialize data. It provides runtime type checking and data conversion, ensuring that data conforms to specified types and constraints.

The library's primary goal is to guarantee that the output data structure precisely conforms to the applied type hints, rather than simply checking input validity. This means Pydantic can coerce input data (e.g., converting string `"123"` to integer `123`) while ensuring the resulting instance meets all type requirements.

**Sources:** [pydantic/main.py1-70](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L1-L70) [docs/concepts/models.md1-52](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/models.md#L1-L52)

## Core Architecture

Pydantic's architecture consists of three main layers: user-facing APIs, schema generation, and the validation/serialization engine.

### System Overview

```
```

**Sources:** [pydantic/main.py1-238](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L1-L238) [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py) [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)

### User-Facing APIs

Pydantic provides four primary entry points for validation:

| API              | Purpose                        | Primary Use Case                                       |
| ---------------- | ------------------------------ | ------------------------------------------------------ |
| `BaseModel`      | Class-based models with fields | Domain models, API schemas, configuration              |
| `TypeAdapter`    | Validate arbitrary types       | One-off validation, generic types, non-model scenarios |
| `@dataclass`     | Enhanced dataclasses           | Dataclass-style models with validation                 |
| `@validate_call` | Function argument validation   | Validating function inputs and outputs                 |

All four APIs converge on the same schema generation and validation pipeline, ensuring consistent behavior across different usage patterns.

**Sources:** [pydantic/main.py118-238](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L118-L238) [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py) [pydantic/dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py) [pydantic/decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py)

### Pydantic-Core Integration

Pydantic's performance-critical validation and serialization logic is implemented in `pydantic-core`, a separate Rust library. The relationship is strictly versioned:

```
```

The version compatibility is enforced at import time:

- **Current Pydantic version:** `2.12.0b1+dev` [pydantic/version.py11](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L11-L11)
- **Required pydantic-core version:** `2.40.1` [pydantic/version.py22](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L22-L22)
- **Compatibility check:** `_ensure_pydantic_core_version()` [pydantic/version.py82-98](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L82-L98)

**Sources:** [pydantic/version.py1-114](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/version.py#L1-L114) [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)

## Main Workflows

### Validation Pipeline

The validation process transforms raw input data into validated model instances through multiple stages:

```
```

Key validation entry points:

- `BaseModel.__init__(self, **data)` [pydantic/main.py240-257](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L257)
- `BaseModel.model_validate(cls, obj)` [pydantic/main.py653-699](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L653-L699)
- `BaseModel.model_validate_json(cls, json_data)` [pydantic/main.py702-743](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L702-L743)
- `TypeAdapter.validate_python(obj)` and `TypeAdapter.validate_json(json_data)`

The actual validation is delegated to `SchemaValidator` from pydantic-core:

- Stored in `cls.__pydantic_validator__` [pydantic/main.py197-198](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L197-L198)
- Called via `validate_python()`, `validate_json()`, or `validate_strings()` methods

**Sources:** [pydantic/main.py240-781](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L781) [docs/concepts/validators.md1-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/validators.md#L1-L50)

### Serialization Pipeline

Serialization converts validated model instances into dictionaries or JSON strings:

```
```

Key serialization methods:

- `model_dump(mode='python'|'json')` [pydantic/main.py418-474](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L418-L474)
- `model_dump_json()` [pydantic/main.py476-534](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L476-L534)

The serialization is handled by `SchemaSerializer` from pydantic-core:

- Stored in `cls.__pydantic_serializer__` [pydantic/main.py194-195](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L194-L195)
- Called via `to_python()` or `to_json()` methods

**Sources:** [pydantic/main.py418-534](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L418-L534) [docs/concepts/serialization.md1-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/serialization.md#L1-L50)

### Schema Generation Flow

Schema generation is a two-stage process: first generating CoreSchema for validation, then optionally generating JSON Schema for documentation:

```
```

The schema generation process:

1. **Type Analysis:** Python type annotations are analyzed using `GenerateSchema` class [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)
2. **CoreSchema Creation:** Types are converted to CoreSchema format understood by pydantic-core
3. **Validator/Serializer Creation:** CoreSchema is used to build `SchemaValidator` and `SchemaSerializer` instances
4. **JSON Schema Generation:** Optionally, CoreSchema is converted to JSON Schema for API documentation

**Sources:** [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py) [pydantic/json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py) [docs/concepts/json\_schema.md1-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/json_schema.md#L1-L50)

## Field and Configuration System

### Field Definition

Fields are defined using `FieldInfo` instances, which store metadata and constraints:

```
```

Fields can be defined in three ways:

1. Bare annotation: `field_name: int` [pydantic/fields.py295-351](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L295-L351)
2. With default: `field_name: int = 10` [pydantic/fields.py354-447](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L354-L447)
3. Using `Field()`: `field_name: int = Field(default=10, gt=0)` [pydantic/fields.py267-292](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L267-L292)

**Sources:** [pydantic/fields.py98-733](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L98-L733) [pydantic/\_internal/\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py)

### Configuration Hierarchy

Configuration can be specified at multiple levels:

| Level | Syntax                           | Priority |
| ----- | -------------------------------- | -------- |
| Model | `model_config = ConfigDict(...)` | Lowest   |
| Field | `Field(frozen=True, ...)`        | Medium   |
| Type  | `Annotated[int, Strict()]`       | Highest  |

Configuration is processed by `ConfigWrapper` [pydantic/\_internal/\_config.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py) and merged during schema generation.

**Sources:** [pydantic/config.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py) [pydantic/\_internal/\_config.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py) [docs/concepts/config.md1-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/config.md#L1-L50)

## Model Lifecycle

The lifecycle of a Pydantic model class from definition to usage:

```
```

Key lifecycle steps:

1. **Metaclass invocation:** `ModelMetaclass.__new__()` [pydantic/\_internal/\_model\_construction.py80-276](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L80-L276)
2. **Namespace inspection:** `inspect_namespace()` identifies fields vs class vars [pydantic/\_internal/\_model\_construction.py520-642](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L520-L642)
3. **Field collection:** `set_model_fields()` creates `FieldInfo` instances [pydantic/\_internal/\_model\_construction.py299-331](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L299-L331)
4. **Schema generation:** `complete_model_class()` builds validation/serialization schemas [pydantic/\_internal/\_model\_construction.py387-518](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L387-L518)
5. **Completion:** Model marked as complete in `__pydantic_complete__` [pydantic/main.py167-168](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L167-L168)

Models can be rebuilt after definition using `model_rebuild()` [pydantic/main.py593-650](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L593-L650) if forward references need resolution.

**Sources:** [pydantic/\_internal/\_model\_construction.py79-277](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L79-L277) [pydantic/\_internal/\_model\_construction.py387-518](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L387-L518) [pydantic/main.py593-650](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L593-L650)

## Class Attributes Reference

Every `BaseModel` subclass has these key class attributes:

| Attribute                      | Type                           | Description                                                                                                                                 |
| ------------------------------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_config`                 | `ConfigDict`                   | Configuration dictionary [pydantic/main.py153-156](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L153-L156)           |
| `__pydantic_core_schema__`     | `CoreSchema`                   | Core validation schema [pydantic/main.py170-171](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L170-L171)             |
| `__pydantic_validator__`       | `SchemaValidator`              | Validation engine instance [pydantic/main.py197-198](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L197-L198)         |
| `__pydantic_serializer__`      | `SchemaSerializer`             | Serialization engine instance [pydantic/main.py194-195](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L194-L195)      |
| `__pydantic_fields__`          | `dict[str, FieldInfo]`         | Field definitions [pydantic/main.py200-203](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L200-L203)                  |
| `__pydantic_computed_fields__` | `dict[str, ComputedFieldInfo]` | Computed field definitions [pydantic/main.py208-209](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L208-L209)         |
| `__pydantic_decorators__`      | `DecoratorInfos`               | Validator/serializer decorators [pydantic/main.py177-179](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L177-L179)    |
| `__pydantic_complete__`        | `bool`                         | Whether model building is complete [pydantic/main.py167-168](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L167-L168) |

**Sources:** [pydantic/main.py118-238](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L118-L238)

## Instance Attributes Reference

Every `BaseModel` instance has these instance attributes:

| Attribute                 | Type                     | Description                                                                                                                                |
| ------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `__dict__`                | `dict[str, Any]`         | Field values storage                                                                                                                       |
| `__pydantic_fields_set__` | `set[str]`               | Fields explicitly set during init [pydantic/main.py214-215](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L214-L215) |
| `__pydantic_extra__`      | `dict[str, Any] \| None` | Extra fields when `extra='allow'` [pydantic/main.py211-212](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L211-L212) |
| `__pydantic_private__`    | `dict[str, Any] \| None` | Private attribute values [pydantic/main.py217-218](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L217-L218)          |

**Sources:** [pydantic/main.py211-238](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L211-L238)

## Project Structure

The Pydantic codebase is organized into several key directories:

```
pydantic/
├── main.py              # BaseModel implementation
├── fields.py            # FieldInfo and Field() function
├── config.py            # ConfigDict definition
├── types.py             # Custom types (URL, Email, etc.)
├── type_adapter.py      # TypeAdapter implementation
├── dataclasses.py       # Enhanced dataclass support
├── json_schema.py       # JSON Schema generation
├── functional_validators.py    # Validator decorators
├── functional_serializers.py   # Serializer decorators
└── _internal/
    ├── _model_construction.py  # ModelMetaclass
    ├── _generate_schema.py     # GenerateSchema class
    ├── _fields.py              # Field collection logic
    ├── _decorators.py          # Decorator processing
    ├── _config.py              # ConfigWrapper
    └── _namespace_utils.py     # Type resolution
```

**Sources:** [pydantic/main.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L1-L1) [pydantic/fields.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L1-L1) [pydantic/\_internal/\_model\_construction.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L1-L1)

## Migration from V1

Pydantic V2 represents a major rewrite with significant API changes. The key differences:

| V1 API           | V2 API                    | Notes                |
| ---------------- | ------------------------- | -------------------- |
| `parse_obj()`    | `model_validate()`        | Method renamed       |
| `parse_raw()`    | `model_validate_json()`   | Specialized for JSON |
| `dict()`         | `model_dump()`            | Method renamed       |
| `json()`         | `model_dump_json()`       | Method renamed       |
| `__fields__`     | `model_fields`            | Now a property       |
| `__validators__` | `__pydantic_decorators__` | Structure changed    |

A V1 compatibility layer is available through `pydantic.v1` imports for gradual migration.

**Sources:** [docs/migration.md1-150](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/migration.md#L1-L150) [pydantic/\_migration.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_migration.py)

## Performance Considerations

Pydantic V2's performance characteristics:

1. **Rust-based validation:** Core validation logic runs in Rust for significant speedup
2. **Schema caching:** Validators and serializers are cached on the class [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)
3. **JSON parsing:** `model_validate_json()` is faster than `model_validate(json.loads())` [docs/concepts/performance.md5-16](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/performance.md#L5-L16)
4. **Deferred building:** Models can defer schema generation with `defer_build=True` config

**Sources:** [docs/concepts/performance.md1-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/concepts/performance.md#L1-L50) [pydantic/\_internal/\_model\_construction.py247-258](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L247-L258)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Overview](#overview.md)
- [What is Pydantic](#what-is-pydantic.md)
- [Core Architecture](#core-architecture.md)
- [System Overview](#system-overview.md)
- [User-Facing APIs](#user-facing-apis.md)
- [Pydantic-Core Integration](#pydantic-core-integration.md)
- [Main Workflows](#main-workflows.md)
- [Validation Pipeline](#validation-pipeline.md)
- [Serialization Pipeline](#serialization-pipeline.md)
- [Schema Generation Flow](#schema-generation-flow.md)
- [Field and Configuration System](#field-and-configuration-system.md)
- [Field Definition](#field-definition.md)
- [Configuration Hierarchy](#configuration-hierarchy.md)
- [Model Lifecycle](#model-lifecycle.md)
- [Class Attributes Reference](#class-attributes-reference.md)
- [Instance Attributes Reference](#instance-attributes-reference.md)
- [Project Structure](#project-structure.md)
- [Migration from V1](#migration-from-v1.md)
- [Performance Considerations](#performance-considerations.md)
