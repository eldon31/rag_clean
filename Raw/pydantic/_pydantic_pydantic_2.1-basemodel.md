BaseModel | pydantic/pydantic | DeepWiki

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

# BaseModel

Relevant source files

- [pydantic/\_internal/\_model\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py)
- [pydantic/fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/fields.py)
- [pydantic/main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py)
- [tests/test\_create\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py)
- [tests/test\_edge\_cases.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py)
- [tests/test\_main.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py)
- [tests/test\_private\_attributes.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_private_attributes.py)

BaseModel is the cornerstone of Pydantic's data validation system. It provides a declarative way to define data models with type annotations, enabling automatic validation, serialization, and documentation of data structures. This page covers the core functionality, architecture, and usage patterns of the BaseModel class.

For information about model configuration options, see [Model Configuration](pydantic/pydantic/2.3-model-configuration.md). For details on how fields work within models, see [Field System](pydantic/pydantic/2.2-field-system.md).

## Purpose and Functionality

BaseModel serves as the foundation for creating validated data models in Pydantic. Key functionality includes:

- Validation of input data against defined types
- Automatic type coercion where possible
- JSON serialization and deserialization
- Schema generation for documentation
- Data manipulation utilities
- Configuration customization

Models are defined by creating classes that inherit from BaseModel, with fields specified using Python type annotations.

Sources: [pydantic/main.py121-152](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L121-L152)

## BaseModel Architecture

**BaseModel Class Structure**

```
```

BaseModel is implemented with `ModelMetaclass` (defined in [pydantic/\_internal/\_model\_construction.py79](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L79-L79)) as its metaclass. During class definition, `ModelMetaclass.__new__` processes type annotations, collects field information from the class and its bases, generates core schemas, and creates the `SchemaValidator` and `SchemaSerializer` instances from pydantic-core.

Sources:

- [pydantic/main.py118-238](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L118-L238)
- [pydantic/\_internal/\_model\_construction.py79-276](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L79-L276)

## Model Lifecycle

**Model Definition and Instantiation Flow**

```
```

### Model Definition Phase

When a class inheriting from `BaseModel` is defined, `ModelMetaclass.__new__` is invoked:

1. **Field Collection** ([pydantic/\_internal/\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#LNaN-LNaN)): Annotations are inspected and converted to `FieldInfo` objects stored in `__pydantic_fields__`
2. **Schema Generation** ([pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#LNaN-LNaN)): A `CoreSchema` is generated from field definitions and decorators
3. **Validator/Serializer Creation**: `SchemaValidator` and `SchemaSerializer` instances from pydantic-core are created from the core schema
4. **Class Attributes Set**: `__pydantic_validator__`, `__pydantic_serializer__`, and `__pydantic_core_schema__` are assigned to the class

### Model Instantiation Phase

When instantiating a model with `MyModel(**data)`:

1. ****init** Entry** ([pydantic/main.py240](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L240)): `BaseModel.__init__` receives keyword arguments as `**data`
2. **Validation** ([pydantic/main.py250](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L250-L250)): Calls `self.__pydantic_validator__.validate_python(data, self_instance=self)`
3. **Rust Validation**: pydantic-core (Rust) validates and coerces data according to the core schema
4. **Instance Attributes**: The validated data is set on `__dict__`, `__pydantic_fields_set__` is populated with explicitly provided fields
5. **Post-Init** ([pydantic/main.py369-370](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L369-L370)): If `__pydantic_post_init__` is set, `model_post_init(context)` is called
6. **Private Attributes** ([pydantic/\_internal/\_model\_construction.py354-369](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L354-L369)): `__pydantic_private__` is initialized with default values

Sources:

- [pydantic/main.py240-260](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L260)
- [pydantic/\_internal/\_model\_construction.py80-258](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L80-L258)
- [pydantic/\_internal/\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#LNaN-LNaN)
- [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#LNaN-LNaN)

## Core Instance Attributes

BaseModel instances maintain several internal attributes for validation and serialization:

### Class-Level Attributes

| Attribute                      | Type                           | Description                                            |
| ------------------------------ | ------------------------------ | ------------------------------------------------------ |
| `__pydantic_fields__`          | `Dict[str, FieldInfo]`         | Field definitions (name → FieldInfo)                   |
| `__pydantic_computed_fields__` | `Dict[str, ComputedFieldInfo]` | Computed field definitions                             |
| `__pydantic_decorators__`      | `DecoratorInfos`               | Collected validator/serializer decorators              |
| `__pydantic_validator__`       | `SchemaValidator`              | pydantic-core validator instance                       |
| `__pydantic_serializer__`      | `SchemaSerializer`             | pydantic-core serializer instance                      |
| `__pydantic_core_schema__`     | `CoreSchema`                   | Generated core schema                                  |
| `__pydantic_complete__`        | `bool`                         | Whether model building is complete                     |
| `__pydantic_custom_init__`     | `bool`                         | Whether `__init__` was overridden                      |
| `__pydantic_post_init__`       | `str \| None`                  | Name of post-init method ('model\_post\_init' or None) |
| `__class_vars__`               | `Set[str]`                     | Class variable names                                   |
| `__private_attributes__`       | `Dict[str, ModelPrivateAttr]`  | Private attribute metadata                             |

### Instance-Level Attributes

| Attribute                 | Type                     | Description                                 |
| ------------------------- | ------------------------ | ------------------------------------------- |
| `__dict__`                | `Dict[str, Any]`         | Regular field values                        |
| `__pydantic_fields_set__` | `Set[str]`               | Fields explicitly set during initialization |
| `__pydantic_extra__`      | `Dict[str, Any] \| None` | Extra fields (when `extra='allow'`)         |
| `__pydantic_private__`    | `Dict[str, Any] \| None` | Private attribute values                    |

### Properties

| Property                | Returns                        | Description                                             |
| ----------------------- | ------------------------------ | ------------------------------------------------------- |
| `model_fields`          | `Dict[str, FieldInfo]`         | Alias for `__pydantic_fields__` (class method)          |
| `model_computed_fields` | `Dict[str, ComputedFieldInfo]` | Alias for `__pydantic_computed_fields__` (class method) |
| `model_fields_set`      | `Set[str]`                     | Fields explicitly set (instance property)               |
| `model_extra`           | `Dict[str, Any] \| None`       | Extra fields dict (instance property)                   |

Sources:

- [pydantic/main.py153-219](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L153-L219)
- [pydantic/main.py262-302](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L262-L302)

## Validation Methods

**Validation Method Flow**

```
```

### **init** (Primary Validation)

The primary validation method is model instantiation via `__init__`:

```
```

**Implementation**: [pydantic/main.py240-260](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L260)

- Receives `**data` as keyword arguments
- Calls `self.__pydantic_validator__.validate_python(data, self_instance=self)`
- Returns the validated instance or raises `ValidationError`

### model\_validate

Validates a Python object (typically a dict) and returns a model instance:

```
```

**Implementation**: [pydantic/main.py652-699](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L652-L699)

**Parameters**:

- `obj`: The object to validate (dict, model instance, object with attributes)
- `strict`: Enforce strict type checking without coercion
- `extra`: Override model config for extra field handling ('ignore', 'allow', 'forbid')
- `from_attributes`: Extract data from object attributes instead of dict keys
- `context`: Additional context passed to validators
- `by_alias`: Use field aliases for input matching
- `by_name`: Use field names for input matching (cannot both be False with `by_alias`)

### model\_validate\_json

Validates JSON data directly without intermediate Python dict:

```
```

**Implementation**: [pydantic/main.py701-743](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L701-L743)

**Parameters**: Same as `model_validate`, plus:

- `json_data`: String, bytes, or bytearray containing JSON

**Note**: Uses pydantic-core's native JSON parser for better performance than `json.loads()` + `model_validate()`

### model\_validate\_strings

Validates data where values are strings that need parsing:

```
```

**Implementation**: [pydantic/main.py745-781](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L745-L781)

Useful for parsing query parameters or form data where all values are strings.

Sources:

- [pydantic/main.py240-260](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L240-L260)
- [pydantic/main.py652-781](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L652-L781)

## Serialization Methods

**Serialization Flow**

```
```

### model\_dump

Serializes the model to a Python dictionary.

**Implementation**: [pydantic/main.py418-474](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L418-L474)

```
```

**Key Parameters**:

| Parameter          | Type                   | Description                                                               |
| ------------------ | ---------------------- | ------------------------------------------------------------------------- |
| `mode`             | `'python'` \| `'json'` | Output mode: Python objects or JSON-serializable types                    |
| `include`          | `IncEx`                | Fields to include (set, dict with nesting)                                |
| `exclude`          | `IncEx`                | Fields to exclude (set, dict with nesting)                                |
| `by_alias`         | `bool`                 | Use field aliases as dict keys                                            |
| `exclude_unset`    | `bool`                 | Exclude fields not explicitly set during initialization                   |
| `exclude_defaults` | `bool`                 | Exclude fields with default values                                        |
| `exclude_none`     | `bool`                 | Exclude fields with `None` values                                         |
| `round_trip`       | `bool`                 | Enable round-trip serialization for special types                         |
| `warnings`         | `bool \| str`          | Handle serialization errors: `True`/`'warn'`, `False`/`'none'`, `'error'` |
| `serialize_as_any` | `bool`                 | Use duck-typing serialization                                             |

**Calls**: `self.__pydantic_serializer__.to_python(self, **options)` [pydantic/main.py460-474](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L460-L474)

### model\_dump\_json

Serializes the model directly to a JSON string using pydantic-core's native JSON serializer.

**Implementation**: [pydantic/main.py476-534](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L476-L534)

```
```

**Additional Parameters**:

| Parameter      | Type          | Description                       |
| -------------- | ------------- | --------------------------------- |
| `indent`       | `int \| None` | JSON indentation (None = compact) |
| `ensure_ascii` | `bool`        | Escape non-ASCII characters       |

**Calls**: `self.__pydantic_serializer__.to_json(self, **options).decode()` [pydantic/main.py519-534](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L519-L534)

**Performance**: More efficient than `json.dumps(model.model_dump())` because it serializes directly to JSON without intermediate Python dict.

Sources:

- [pydantic/main.py418-534](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L418-L534)
- [tests/test\_serialize.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_serialize.py)

## Model Construction and Copying

### model\_construct

Creates a model instance bypassing validation. Useful for trusted or pre-validated data.

**Implementation**: [pydantic/main.py304-382](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L304-L382)

```
```

**Behavior**:

1. Creates instance with `cls.__new__(cls)` (no `__init__`)
2. Processes field aliases (both `alias` and `validation_alias`)
3. Sets default values for missing fields via `field.get_default(call_default_factory=True)`
4. Directly sets `__dict__`, `__pydantic_fields_set__`, `__pydantic_extra__`
5. Calls `model_post_init(None)` if defined
6. Initializes `__pydantic_private__` with defaults

**Key Parameters**:

- `_fields_set`: Optional set of field names to mark as explicitly set. If `None`, uses all provided field names.
- `**values`: Field values and extra fields (if `extra='allow'`)

**Notes**:

- Respects `model_config.extra` setting for handling extra fields
- With `extra='allow'`, extra values go to `__pydantic_extra__`
- With `extra='ignore'` or `extra='forbid'`, extra values are ignored (no error in construct)
- Default factory functions are called
- Validators are NOT executed

Sources:

- [pydantic/main.py304-382](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L304-L382)
- [tests/test\_construction.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_construction.py)

### model\_copy

Creates a shallow or deep copy of a model instance with optional updates.

**Implementation**: [pydantic/main.py384-416](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L384-L416)

```
```

**Parameters**:

- `update`: Dictionary of field updates to apply (not validated)
- `deep`: If `True`, performs deep copy; otherwise shallow copy

**Behavior**:

1. Calls `self.__deepcopy__()` or `self.__copy__()` based on `deep` parameter

2. If `update` provided:

   - For models with `extra='allow'`: Updates regular fields in `__dict__` and extra fields in `__pydantic_extra__`
   - Otherwise: Updates `__dict__` directly

3. Updates `__pydantic_fields_set__` with keys from `update`

**Warning**: The copied instance's `__dict__` is copied, which may include unexpected items like cached property values.

Sources:

- [pydantic/main.py384-416](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L384-L416)
- [tests/test\_edge\_cases.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py)

## Schema Generation

BaseModel provides methods for generating JSON schemas:

```
```

This can be used for:

- Documentation
- Integration with other tools
- Client-side validation
- Code generation

Sources:

- [pydantic/main.py535-557](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L535-L557)

## Field Access and Modification

### **setattr** Behavior

BaseModel customizes `__setattr__` to support validation, frozen fields, and private attributes.

**Implementation**: [pydantic/main.py815-908](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L815-L908)

****setattr** Routing Table** (`__pydantic_setattr_handlers__`):

```
```

**Flow**:

1. `__setattr__` looks up the attribute name in `__pydantic_setattr_handlers__`
2. Calls the appropriate handler function
3. For unknown attributes: checks if extra allowed, private attr, or raises error

### Field Assignment

**Without validate\_assignment** (default):

```
```

**With validate\_assignment=True**:

```
```

Calls `__pydantic_validator__.validate_assignment(self, name, value)` [pydantic/main.py111](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L111-L111)

### Frozen Fields

**Model-level frozen**:

```
```

**Field-level frozen**:

```
```

Frozen check: [pydantic/main.py81-91](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L81-L91)

### Field Tracking with model\_fields\_set

The `model_fields_set` property returns fields explicitly set during initialization:

```
```

**Implementation**: [pydantic/main.py293-301](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L293-L301)

Sources:

- [pydantic/main.py81-115](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L81-L115)
- [pydantic/main.py815-908](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L815-L908)
- [tests/test\_main.py535-610](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L535-L610)

## Extra Fields Handling

The `extra` config controls how fields not defined in the model are handled.

### Configuration Options

| Value      | Behavior                                                                 |
| ---------- | ------------------------------------------------------------------------ |
| `'ignore'` | Extra fields are silently ignored (default)                              |
| `'allow'`  | Extra fields stored in `__pydantic_extra__` and accessible as attributes |
| `'forbid'` | Extra fields raise `ValidationError` with type `'extra_forbidden'`       |

### extra='allow'

```
```

**Attribute Access**: Extra fields are accessible via `__getattr__` [pydantic/main.py910-924](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L910-L924)

**Serialization**: Extra fields are included in `model_dump()` output [pydantic/main.py211-212](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L211-L212)

**Assignment After Init**:

```
```

### extra='forbid'

```
```

### extra='ignore'

```
```

Sources:

- [pydantic/main.py211-212](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L211-L212)
- [pydantic/main.py910-924](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L910-L924)
- [tests/test\_main.py266-414](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L266-L414)

## validate\_assignment Configuration

When `validate_assignment=True`, field assignments are validated after model initialization.

**Configuration**:

```
```

**Behavior**:

```
```

**Implementation**: [pydantic/main.py111](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L111-L111)

- Calls `__pydantic_validator__.validate_assignment(model, name, value)`
- Runs full validation pipeline (field validators, type coercion, constraints)
- Updates `__dict__[name]` and adds `name` to `__pydantic_fields_set__`

**Performance Note**: Adds validation overhead to every field assignment. Only use when runtime data integrity is required.

Sources:

- [pydantic/main.py111](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L111-L111)
- [tests/test\_main.py754-803](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L754-L803)

## Private Attributes

Private attributes (prefix `_`) are not validated or serialized. They are managed separately from regular fields.

### Defining Private Attributes

**With PrivateAttr**:

```
```

**With annotation only**:

```
```

**Implicit** (unannotated):

```
```

### Storage and Access

Private attributes are stored in `__pydantic_private__` dict:

```
```

**Initialization**: [pydantic/\_internal/\_model\_construction.py354-369](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L354-L369)

- `__pydantic_private__` is initialized in `init_private_attributes()`
- Called from wrapped `model_post_init()` if private attrs exist
- Default values are set from `__private_attributes__` metadata

### Characteristics

| Aspect               | Behavior                                                                                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Validation**       | None - not validated on init or assignment                                                                                                                 |
| **Serialization**    | Excluded from `model_dump()` and `model_dump_json()`                                                                                                       |
| **model\_construct** | Can be set via `**values` after model\_post\_init [pydantic/main.py371-375](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L371-L375) |
| **Naming**           | Must start with single `_` (not `__` dunder)                                                                                                               |
| **Access**           | Normal Python attribute access                                                                                                                             |

Sources:

- [pydantic/main.py217](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L217-L217)
- [pydantic/\_internal/\_model\_construction.py354-369](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L354-L369)
- [pydantic/\_internal/\_model\_construction.py418-517](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L418-L517)
- [tests/test\_private\_attributes.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_private_attributes.py)

## Computed Fields

Computed fields are properties included in model serialization, defined with the `@computed_field` decorator.

### Definition

```
```

### Characteristics

| Aspect            | Behavior                                                  |
| ----------------- | --------------------------------------------------------- |
| **Validation**    | Not validated on input; computed from other fields        |
| **Serialization** | Included in `model_dump()` and `model_dump_json()` output |
| **Schema**        | Included in JSON schema as read-only property             |
| **Access**        | Read-only property access (unless setter defined)         |
| **Storage**       | Stored in `__pydantic_computed_fields__` class attribute  |

### Serialization

```
```

### With cached\_property

```
```

**Note**: Cached values are stored in `__dict__`, not `__pydantic_private__`

Sources:

- [pydantic/main.py208-209](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L208-L209)
- [pydantic/main.py243-245](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L243-L245)
- [tests/test\_computed\_fields.py27-66](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_computed_fields.py#L27-L66)

## Model Rebuilding

The `model_rebuild()` class method regenerates a model's schema when forward references couldn't be resolved initially.

### When to Use

Forward references that can't be resolved during class definition:

```
```

### Implementation

**Method signature**: [pydantic/main.py593-650](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L593-L650)

```
```

**Parameters**:

- `force`: Rebuild even if `__pydantic_complete__=True`
- `raise_errors`: Raise exceptions on schema generation errors
- `_parent_namespace_depth`: Frame depth for namespace resolution
- `_types_namespace`: Explicit namespace for type resolution

**Returns**:

- `None`: Schema was already complete and rebuild skipped
- `True`: Rebuild succeeded
- `False`: Rebuild failed (only when `raise_errors=False`)

### Rebuild Process

1. **Check Completion**: If `__pydantic_complete__=True` and `force=False`, returns `None`
2. **Clear Schema Artifacts**: Deletes `__pydantic_core_schema__`, `__pydantic_validator__`, `__pydantic_serializer__`
3. **Resolve Namespace**: Gets parent frame namespace for type resolution
4. **Complete Model**: Calls `complete_model_class()` to regenerate schema

**Note**: Not thread-safe. Concurrent rebuilds can cause issues with shared validator/serializer instances.

Sources:

- [pydantic/main.py593-650](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L593-L650)
- [pydantic/\_internal/\_model\_construction.py619-650](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L619-L650)

## Dynamic Model Creation

The `create_model()` function creates BaseModel subclasses at runtime.

**Function signature**: [pydantic/main.py1083-1228](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L1083-L1228)

```
```

### Field Definition Formats

| Format            | Description               | Example                         |
| ----------------- | ------------------------- | ------------------------------- |
| `(type, default)` | Type with default value   | `field1=(str, 'default')`       |
| `(type, ...)`     | Required field            | `field2=(int, ...)`             |
| `type`            | Required, annotation-only | `field3=str`                    |
| `FieldInfo`       | From Field() function     | `field4=Field(default=0, gt=0)` |

### Special Parameters

| Parameter        | Description                                         |
| ---------------- | --------------------------------------------------- |
| `__config__`     | ConfigDict for model configuration                  |
| `__base__`       | Base class or tuple of base classes                 |
| `__module__`     | Set `__module__` attribute (affects pickling, repr) |
| `__validators__` | Validators dict (V1-style, deprecated)              |
| `__cls_kwargs__` | Kwargs passed to ModelMetaclass                     |
| `__doc__`        | Docstring for the model class                       |

### Usage Examples

**With inheritance**:

```
```

**With validators** (V2 style):

```
```

Sources:

- [pydantic/main.py1083-1228](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L1083-L1228)
- [tests/test\_create\_model.py20-124](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_create_model.py#L20-L124)

## Customization Hooks

### Custom **init**

Override `__init__` to customize pre-validation behavior:

```
```

**Note**: `__pydantic_custom_init__` class attribute is set to `True` when `__init__` is overridden [pydantic/\_internal/\_model\_construction.py165](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L165-L165)

### model\_post\_init

Hook called after validation and instance creation:

```
```

**Signature**: [pydantic/main.py587-590](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L587-L590)

```
```

**Parameters**:

- `__context`: Context passed from validators or `None`

**When called**:

- After `__pydantic_validator__.validate_python()` completes
- Before `__init__` returns
- Also called from `model_construct()` with `context=None`

**Special behavior**:

- If private attributes exist, ModelMetaclass wraps `model_post_init` to initialize `__pydantic_private__` first [pydantic/\_internal/\_model\_construction.py133-147](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L133-L147)

### **pydantic\_init\_subclass**

Hook for subclass customization:

```
```

**Called from**: [pydantic/\_internal/\_model\_construction.py266](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L266-L266)

Sources:

- [pydantic/main.py587-590](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/main.py#L587-L590)
- [pydantic/\_internal/\_model\_construction.py133-147](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L133-L147)
- [pydantic/\_internal/\_model\_construction.py165-168](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L165-L168)
- [pydantic/\_internal/\_model\_construction.py266](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_model_construction.py#L266-L266)

## Integration with Validators

BaseModel works closely with Pydantic validators to allow field-level and model-level validation:

```
```

This topic is covered in depth in the Validators documentation.

Sources:

- [tests/test\_validators.py192-215](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validators.py#L192-L215)

## Usage Examples

### Basic Model Definition

```
```

### Validation from Different Sources

```
```

### Serialization Patterns

```
```

### Model Construction and Copying

```
```

### Working with Extra Fields

```
```

Sources:

- [tests/test\_main.py56-115](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L56-L115)
- [tests/test\_edge\_cases.py62-124](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_edge_cases.py#L62-L124)

## Error Handling

When validation fails, BaseModel raises a `ValidationError` with detailed information:

```
```

Error information includes:

- Error type
- Error location (field)
- Error message
- Invalid input value
- Context-specific details

Sources:

- [tests/test\_main.py87-103](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L87-L103)

## Performance Considerations

- Use `model_construct` for trusted data to skip validation
- Consider `frozen=True` for immutable models (enables hashing)
- Use `exclude_unset=True` when serializing to minimize output
- Be mindful of deep validation in complex nested models

Sources:

- [tests/test\_construction.py15-35](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_construction.py#L15-L35)
- [tests/test\_main.py613-643](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_main.py#L613-L643)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [BaseModel](#basemodel.md)
- [Purpose and Functionality](#purpose-and-functionality.md)
- [BaseModel Architecture](#basemodel-architecture.md)
- [Model Lifecycle](#model-lifecycle.md)
- [Model Definition Phase](#model-definition-phase.md)
- [Model Instantiation Phase](#model-instantiation-phase.md)
- [Core Instance Attributes](#core-instance-attributes.md)
- [Class-Level Attributes](#class-level-attributes.md)
- [Instance-Level Attributes](#instance-level-attributes.md)
- [Properties](#properties.md)
- [Validation Methods](#validation-methods.md)
- [\_\_init\_\_ (Primary Validation)](#__init__-primary-validation.md)
- [model\_validate](#model_validate.md)
- [model\_validate\_json](#model_validate_json.md)
- [model\_validate\_strings](#model_validate_strings.md)
- [Serialization Methods](#serialization-methods.md)
- [model\_dump](#model_dump.md)
- [model\_dump\_json](#model_dump_json.md)
- [Model Construction and Copying](#model-construction-and-copying.md)
- [model\_construct](#model_construct.md)
- [model\_copy](#model_copy.md)
- [Schema Generation](#schema-generation.md)
- [Field Access and Modification](#field-access-and-modification.md)
- [\_\_setattr\_\_ Behavior](#__setattr__-behavior.md)
- [Field Assignment](#field-assignment.md)
- [Frozen Fields](#frozen-fields.md)
- [Field Tracking with model\_fields\_set](#field-tracking-with-model_fields_set.md)
- [Extra Fields Handling](#extra-fields-handling.md)
- [Configuration Options](#configuration-options.md)
- [extra='allow'](#extraallow.md)
- [extra='forbid'](#extraforbid.md)
- [extra='ignore'](#extraignore.md)
- [validate\_assignment Configuration](#validate_assignment-configuration.md)
- [Private Attributes](#private-attributes.md)
- [Defining Private Attributes](#defining-private-attributes.md)
- [Storage and Access](#storage-and-access.md)
- [Characteristics](#characteristics.md)
- [Computed Fields](#computed-fields.md)
- [Definition](#definition.md)
- [Characteristics](#characteristics-1.md)
- [Serialization](#serialization.md)
- [With cached\_property](#with-cached_property.md)
- [Model Rebuilding](#model-rebuilding.md)
- [When to Use](#when-to-use.md)
- [Implementation](#implementation.md)
- [Rebuild Process](#rebuild-process.md)
- [Dynamic Model Creation](#dynamic-model-creation.md)
- [Field Definition Formats](#field-definition-formats.md)
- [Special Parameters](#special-parameters.md)
- [Usage Examples](#usage-examples.md)
- [Customization Hooks](#customization-hooks.md)
- [Custom \_\_init\_\_](#custom-__init__.md)
- [model\_post\_init](#model_post_init.md)
- [\_\_pydantic\_init\_subclass\_\_](#__pydantic_init_subclass__.md)
- [Integration with Validators](#integration-with-validators.md)
- [Usage Examples](#usage-examples-1.md)
- [Basic Model Definition](#basic-model-definition.md)
- [Validation from Different Sources](#validation-from-different-sources.md)
- [Serialization Patterns](#serialization-patterns.md)
- [Model Construction and Copying](#model-construction-and-copying-1.md)
- [Working with Extra Fields](#working-with-extra-fields.md)
- [Error Handling](#error-handling.md)
- [Performance Considerations](#performance-considerations.md)
