Core Model System | pydantic/pydantic | DeepWiki

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

# Core Model System

Relevant source files

- [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)
- [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)
- [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)
- [tests/test\_create\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py)
- [tests/test\_edge\_cases.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py)
- [tests/test\_main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py)
- [tests/test\_private\_attributes.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_private_attributes.py)

## Purpose and Scope

This document covers the foundational model system that powers Pydantic's validation and serialization capabilities. The Core Model System encompasses `BaseModel` (the base class for all Pydantic models), the metaclass-based model construction pipeline, field collection and management, and the model lifecycle from instantiation through validation to serialization.

For information about specific field types and constraints, see [Type System](pydantic/pydantic/3-type-system.md). For details on validators and serializers that customize the data transformation pipeline, see [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md). For schema generation internals, see [Schema Generation](pydantic/pydantic/5-schema-generation.md).

---

## System Overview

The Core Model System is built on three foundational components that work together to provide Pydantic's declarative validation framework:

**BaseModel Class Hierarchy**

```
```

Sources: [pydantic/main.py118-239](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L118-L239) [pydantic/\_internal/\_model\_construction.py79-277](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L79-L277)

---

## BaseModel Class

`BaseModel` is the foundational class that all Pydantic models inherit from. It provides the core validation, serialization, and model management capabilities.

### Class Attributes

The `BaseModel` class maintains several class-level attributes that define model structure and behavior:

| Attribute                      | Type                                          | Purpose                                             |
| ------------------------------ | --------------------------------------------- | --------------------------------------------------- |
| `model_config`                 | `ConfigDict`                                  | Configuration dictionary controlling model behavior |
| `__pydantic_fields__`          | `dict[str, FieldInfo]`                        | Field definitions and metadata                      |
| `__pydantic_computed_fields__` | `dict[str, ComputedFieldInfo]`                | Computed field definitions                          |
| `__pydantic_decorators__`      | `DecoratorInfos`                              | Collected validators and serializers                |
| `__pydantic_validator__`       | `SchemaValidator \| PluggableSchemaValidator` | pydantic-core validator instance                    |
| `__pydantic_serializer__`      | `SchemaSerializer`                            | pydantic-core serializer instance                   |
| `__pydantic_core_schema__`     | `CoreSchema`                                  | Generated validation schema                         |
| `__private_attributes__`       | `dict[str, ModelPrivateAttr]`                 | Private attribute definitions                       |
| `__class_vars__`               | `set[str]`                                    | Names of class variables                            |

Sources: [pydantic/main.py151-219](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L151-L219)

### Instance Attributes

Each `BaseModel` instance maintains these attributes:

| Attribute                 | Type                     | Purpose                                              |
| ------------------------- | ------------------------ | ---------------------------------------------------- |
| `__dict__`                | `dict[str, Any]`         | Field values                                         |
| `__pydantic_fields_set__` | `set[str]`               | Names of fields explicitly set during initialization |
| `__pydantic_extra__`      | `dict[str, Any] \| None` | Extra fields (when `extra='allow'`)                  |
| `__pydantic_private__`    | `dict[str, Any] \| None` | Private attribute values                             |

Sources: [pydantic/main.py211-218](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L211-L218)

### Core Methods

**BaseModel Method Mapping**

```
```

Sources: [pydantic/main.py240-782](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L782)

#### Initialization: `__init__`

The `__init__` method validates input data and creates a model instance:

```
```

- Takes keyword arguments as input data
- Delegates to `__pydantic_validator__.validate_python()`
- Returns `self` after validation
- Raises `ValidationError` if validation fails

Sources: [pydantic/main.py240-260](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L260)

#### Construction Without Validation: `model_construct`

`model_construct` creates instances from trusted data without validation:

```
```

- Respects `model_config.extra` setting
- Handles field aliases (both `alias` and `validation_alias`)
- Applies default values for missing fields
- Useful for creating instances from database records or API responses
- Calls `model_post_init()` if defined

Sources: [pydantic/main.py304-382](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L304-L382)

#### Validation Methods

Three validation methods handle different input formats:

| Method                           | Input Type                             | Use Case                        |
| -------------------------------- | -------------------------------------- | ------------------------------- |
| `model_validate(obj)`            | Python objects (dict, model instances) | General validation              |
| `model_validate_json(json_data)` | JSON strings/bytes                     | API request parsing             |
| `model_validate_strings(obj)`    | String-valued dictionaries             | URL query parameters, form data |

All support common parameters: `strict`, `extra`, `from_attributes`, `context`, `by_alias`, `by_name`.

Sources: [pydantic/main.py652-781](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L652-L781)

#### Serialization Methods

| Method                      | Output Format | Parameters                                                                |
| --------------------------- | ------------- | ------------------------------------------------------------------------- |
| `model_dump(mode='python')` | Python dict   | `include`, `exclude`, `exclude_unset`, `exclude_defaults`, `exclude_none` |
| `model_dump_json()`         | JSON string   | Same as `model_dump` plus `indent`, `ensure_ascii`                        |

Both methods delegate to `__pydantic_serializer__` with configurable filtering and formatting options.

Sources: [pydantic/main.py418-534](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L418-L534)

---

## Model Construction Pipeline

The model construction process is orchestrated by `ModelMetaclass`, which transforms a class definition into a fully-functional Pydantic model.

### ModelMetaclass Pipeline

```
```

Sources: [pydantic/\_internal/\_model\_construction.py80-277](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L80-L277)

### Namespace Inspection

The `inspect_namespace` function processes the class namespace to identify and categorize attributes:

**Namespace Inspection Flow**

```
```

Sources: [pydantic/\_internal/\_model\_construction.py384-518](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L384-L518)

### Field Collection

The `collect_model_fields` function (in `_internal/_fields.py`) processes type annotations to build the field dictionary:

1. **Gather annotations** from the class and its bases
2. **Resolve forward references** using the namespace resolver
3. **Create FieldInfo instances** via `FieldInfo.from_annotation()` or `FieldInfo.from_annotated_attribute()`
4. **Apply type variable substitutions** for generic models
5. **Identify class variables** (annotated with `ClassVar`)
6. **Validate field names** (no leading underscores except for private attrs)

Sources: [pydantic/\_internal/\_fields.py84-223](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#L84-L223)

### Schema Building and Completion

The `complete_model_class` function finalizes the model by:

1. Generating the core schema via `GenerateSchema`
2. Creating the `SchemaValidator` from the core schema
3. Creating the `SchemaSerializer` from the core schema
4. Generating the `__signature__` for `__init__`
5. Setting up computed fields
6. Configuring `__setattr__` handlers

**Schema and Validator Creation**

```
```

Sources: [pydantic/\_internal/\_model\_construction.py580-678](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L580-L678)

---

## Model Lifecycle

A model instance progresses through several stages from creation to serialization.

### Initialization Flow

```
```

Sources: [pydantic/main.py240-260](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L260) [pydantic/\_internal/\_model\_construction.py354-370](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L354-L370)

### Attribute Access and Assignment

`BaseModel` customizes attribute access through `__setattr__` and `__delattr__`:

**Setattr Handler Selection**

The model maintains `__pydantic_setattr_handlers__` mapping field names to handler functions:

| Handler Type            | Condition                           | Action                                                             |
| ----------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| `'model_field'`         | Regular field, no validation        | Set `__dict__[name] = val` and add to `__pydantic_fields_set__`    |
| `'validate_assignment'` | `validate_assignment=True`          | Call `__pydantic_validator__.validate_assignment(self, name, val)` |
| `'private'`             | Private attribute (starts with `_`) | Set in `__pydantic_private__` dict                                 |
| `'cached_property'`     | `functools.cached_property`         | Set in `__dict__` directly                                         |
| `'extra_known'`         | Extra field (when `extra='allow'`)  | Use `object.__setattr__`                                           |

The handler is selected and memoized in `__pydantic_setattr_handlers__` for performance.

Sources: [pydantic/main.py837-933](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L837-L933) [pydantic/main.py94-115](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L94-L115)

### Private Attributes

Private attributes (prefixed with `_`) are stored separately in `__pydantic_private__` and are not validated or serialized:

**Private Attribute Handling**

```
```

Sources: [pydantic/\_internal/\_model\_construction.py354-370](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L354-L370) [pydantic/main.py994-1019](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L994-L1019)

Private attributes support:

- Default values via `PrivateAttr(default=...)`
- Factory functions via `PrivateAttr(default_factory=...)`
- Descriptors implementing `__get__`, `__set__`, `__delete__`
- Type annotations without assignments

Sources: [pydantic/fields.py1128-1237](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L1128-L1237)

---

## Configuration System

Model behavior is controlled through `model_config`, a `ConfigDict` instance.

### Configuration Inheritance

Configuration is inherited and merged through the model hierarchy:

**Config Wrapper Creation**

```
```

Sources: [pydantic/\_internal/\_config.py71-121](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_config.py#L71-L121)

### Key Configuration Options

| Option                 | Default       | Effect on Model Construction                                                |
| ---------------------- | ------------- | --------------------------------------------------------------------------- |
| `strict`               | `False`       | Enables strict validation mode                                              |
| `extra`                | `'ignore'`    | Controls handling of extra fields: `'allow'`, `'ignore'`, `'forbid'`        |
| `frozen`               | `False`       | Makes instances immutable; raises `ValidationError` on attribute assignment |
| `validate_assignment`  | `False`       | Validates field values on attribute assignment                              |
| `validate_default`     | `False`       | Validates default values during model construction                          |
| `from_attributes`      | `False`       | Allows populating fields from object attributes (for ORM integration)       |
| `defer_build`          | `False`       | Delays schema building until first use                                      |
| `protected_namespaces` | `('model_',)` | Warns about field names conflicting with these prefixes                     |

Sources: [pydantic/config.py31-286](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/config.py#L31-L286)

---

## Model Field Management

### FieldInfo Structure

Each field is represented by a `FieldInfo` instance containing:

| Attribute             | Purpose                                            |
| --------------------- | -------------------------------------------------- |
| `annotation`          | The field's type annotation                        |
| `default`             | Default value (if not required)                    |
| `default_factory`     | Callable to generate default value                 |
| `alias`               | Alternative name for serialization                 |
| `validation_alias`    | Alternative name(s) for validation input           |
| `serialization_alias` | Alternative name for serialization output          |
| `title`               | Field title for JSON schema                        |
| `description`         | Field description for JSON schema                  |
| `metadata`            | List of metadata objects (constraints, validators) |
| `frozen`              | Whether field is immutable                         |
| `validate_default`    | Whether to validate the default value              |

Sources: [pydantic/fields.py98-265](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L98-L265)

### Field Creation Methods

`FieldInfo` instances are created through three factory methods:

**FieldInfo Factory Methods**

```
```

Sources: [pydantic/fields.py295-521](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L295-L521)

1. **`from_annotation(annotation)`**: For bare type annotations without default values
2. **`from_annotated_attribute(annotation, default)`**: For annotations with assigned values
3. **`_construct(metadata, **attr_overrides)`**: Merges multiple `FieldInfo` instances from `Annotated` metadata

### Field Metadata Collection

The `_collect_metadata` method transforms Field arguments into metadata objects:

| Argument                         | Metadata Type                          |
| -------------------------------- | -------------------------------------- |
| `gt`, `ge`, `lt`, `le`           | `annotated_types.Gt`, `Ge`, `Lt`, `Le` |
| `multiple_of`                    | `annotated_types.MultipleOf`           |
| `min_length`, `max_length`       | `annotated_types.MinLen`, `MaxLen`     |
| `strict`                         | `types.Strict`                         |
| `pattern`, `allow_inf_nan`, etc. | `PydanticGeneralMetadata`              |

Sources: [pydantic/fields.py622-649](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py#L622-L649)

---

## Advanced Topics

### Model Rebuilding

The `model_rebuild()` method regenerates the schema and validator when forward references couldn't be resolved during initial construction:

```
```

Process:

1. Check if model is already complete (skip if `force=False`)
2. Delete existing schema/validator/serializer
3. Resolve parent namespace
4. Call `complete_model_class()` again with namespace resolver

Sources: [pydantic/main.py593-650](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L593-L650)

### Dynamic Model Creation

The `create_model` function creates model classes programmatically:

```
```

The function:

1. Creates a new namespace dict
2. Processes field definitions into `FieldInfo` objects
3. Calls `ModelMetaclass.__new__` to construct the class
4. Optionally sets `__module__` for proper pickle support

Sources: [pydantic/main.py1367-1533](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L1367-L1533)

### Frozen Models and Hashing

When `frozen=True`, the metaclass automatically generates a `__hash__` method:

**Hash Function Generation**

```
```

The hash function:

- Uses `operator.itemgetter` to extract field values
- Hashes only the model fields (not extras or private attrs)
- Handles missing keys gracefully via `SafeGetItemProxy`

Sources: [pydantic/\_internal/\_model\_construction.py521-547](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L521-L547)

---

## Key Implementation Details

### Mock Validators and Serializers

Before schema building completes, models use mock validators/serializers that raise helpful errors:

```
```

This prevents instantiation of incomplete models and provides clear error messages.

Sources: [pydantic/main.py220-236](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L220-L236) [pydantic/\_internal/\_mock\_val\_ser.py1-100](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_mock_val_ser.py#L1-L100)

### Setattr Handler Memoization

For performance, `__setattr__` memoizes handler selection in `__pydantic_setattr_handlers__`:

```
```

This avoids repeated isinstance checks and configuration lookups.

Sources: [pydantic/main.py837-933](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L837-L933)

### Model Copy

The `model_copy()` method creates a shallow or deep copy:

```
```

- Copies `__dict__` (may have unexpected effects for cached properties)
- Optionally applies updates (not validated)
- Handles `extra='allow'` by distinguishing fields from extras

Sources: [pydantic/main.py384-416](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L384-L416)

---

## Summary

The Core Model System provides a comprehensive framework for declarative data validation through:

1. **`BaseModel`** - The base class with validation, serialization, and configuration
2. **`ModelMetaclass`** - The metaclass orchestrating field collection, schema generation, and model completion
3. **`FieldInfo`** - Rich field metadata supporting aliases, defaults, and constraints
4. **Private Attributes** - Separate storage for non-validated instance data
5. **Configuration** - Flexible behavior control through `ConfigDict`
6. **Model Lifecycle** - Well-defined stages from construction to validation to serialization

The system leverages `pydantic-core` (Rust) for the performance-critical validation and serialization operations, while the Python layer handles declarative schema definition and model construction.

For field-level customization through validators and serializers, see [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md). For understanding how Python types are converted to validation schemas, see [Schema Generation](pydantic/pydantic/5-schema-generation.md).

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Core Model System](#core-model-system.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Overview](#system-overview.md)
- [BaseModel Class](#basemodel-class.md)
- [Class Attributes](#class-attributes.md)
- [Instance Attributes](#instance-attributes.md)
- [Core Methods](#core-methods.md)
- [Initialization: \`\_\_init\_\_\`](#initialization-__init__.md)
- [Construction Without Validation: \`model\_construct\`](#construction-without-validation-model_construct.md)
- [Validation Methods](#validation-methods.md)
- [Serialization Methods](#serialization-methods.md)
- [Model Construction Pipeline](#model-construction-pipeline.md)
- [ModelMetaclass Pipeline](#modelmetaclass-pipeline.md)
- [Namespace Inspection](#namespace-inspection.md)
- [Field Collection](#field-collection.md)
- [Schema Building and Completion](#schema-building-and-completion.md)
- [Model Lifecycle](#model-lifecycle.md)
- [Initialization Flow](#initialization-flow.md)
- [Attribute Access and Assignment](#attribute-access-and-assignment.md)
- [Private Attributes](#private-attributes.md)
- [Configuration System](#configuration-system.md)
- [Configuration Inheritance](#configuration-inheritance.md)
- [Key Configuration Options](#key-configuration-options.md)
- [Model Field Management](#model-field-management.md)
- [FieldInfo Structure](#fieldinfo-structure.md)
- [Field Creation Methods](#field-creation-methods.md)
- [Field Metadata Collection](#field-metadata-collection.md)
- [Advanced Topics](#advanced-topics.md)
- [Model Rebuilding](#model-rebuilding.md)
- [Dynamic Model Creation](#dynamic-model-creation.md)
- [Frozen Models and Hashing](#frozen-models-and-hashing.md)
- [Key Implementation Details](#key-implementation-details.md)
- [Mock Validators and Serializers](#mock-validators-and-serializers.md)
- [Setattr Handler Memoization](#setattr-handler-memoization.md)
- [Model Copy](#model-copy.md)
- [Summary](#summary.md)
