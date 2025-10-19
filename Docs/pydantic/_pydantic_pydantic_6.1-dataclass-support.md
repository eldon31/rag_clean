Dataclass Support | pydantic/pydantic | DeepWiki

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

# Dataclass Support

Relevant source files

- [pydantic/\_internal/\_dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py)
- [pydantic/\_internal/\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py)
- [pydantic/\_internal/\_generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generics.py)
- [pydantic/\_internal/\_typing\_extra.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_typing_extra.py)
- [pydantic/dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py)
- [pydantic/generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/generics.py)
- [tests/test\_dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py)
- [tests/test\_forward\_ref.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_forward_ref.py)
- [tests/test\_generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_generics.py)
- [tests/test\_typing.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_typing.py)

## Purpose and Scope

This page documents Pydantic's enhanced dataclass functionality, which provides validation capabilities to Python dataclasses through the `@pydantic.dataclasses.dataclass` decorator. Pydantic dataclasses integrate seamlessly with the standard library `dataclasses` module while adding runtime validation, serialization, and schema generation.

For information about Pydantic's core model system, see [BaseModel](pydantic/pydantic/2.1-basemodel.md). For general field configuration, see [Field System](pydantic/pydantic/2.2-field-system.md). For validation logic, see [Validators](pydantic/pydantic/4.1-validators.md).

## Decorator API and Core Types

### The `dataclass` Decorator

The `@pydantic.dataclasses.dataclass` decorator wraps standard Python dataclasses with Pydantic validation. It accepts all standard dataclass parameters plus Pydantic-specific configuration.

```
```

**Sources:** [pydantic/dataclasses.py98-313](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L98-L313)

### Decorator Parameters

| Parameter          | Type                         | Default | Description                                          |
| ------------------ | ---------------------------- | ------- | ---------------------------------------------------- |
| `init`             | `Literal[False]`             | `False` | Must be `False`; Pydantic provides custom `__init__` |
| `repr`             | `bool`                       | `True`  | Include field in `__repr__`                          |
| `eq`               | `bool`                       | `True`  | Generate `__eq__` method                             |
| `order`            | `bool`                       | `False` | Generate comparison methods                          |
| `unsafe_hash`      | `bool`                       | `False` | Generate `__hash__` method                           |
| `frozen`           | `bool \| None`               | `None`  | Make dataclass immutable                             |
| `config`           | `ConfigDict \| type \| None` | `None`  | Pydantic configuration                               |
| `validate_on_init` | `bool \| None`               | `None`  | Deprecated; always validates                         |
| `kw_only`          | `bool`                       | `False` | Require keyword-only arguments (Python 3.10+)        |
| `slots`            | `bool`                       | `False` | Use `__slots__` (Python 3.10+)                       |

**Sources:** [pydantic/dataclasses.py29-96](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L29-L96)

### PydanticDataclass Protocol

Once decorated, a class gains the `PydanticDataclass` protocol attributes:

```
```

**Sources:** [pydantic/\_internal/\_dataclasses.py40-63](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L40-L63)

## Dataclass Creation and Lifecycle

### Creation Flow

```
```

**Sources:** [pydantic/dataclasses.py153-313](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L153-L313) [pydantic/\_internal/\_dataclasses.py85-190](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L85-L190)

### The `create_dataclass` Function

The internal `create_dataclass` function orchestrates the transformation:

1. **Validation**: Ensures class is not already a `BaseModel` ([pydantic/dataclasses.py164-168](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L164-L168))
2. **Configuration**: Merges decorator config with `__pydantic_config__` attribute ([pydantic/dataclasses.py184-187](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L184-L187))
3. **Vanilla Handling**: Subclasses stdlib dataclasses to add validation ([pydantic/dataclasses.py194-206](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L194-L206))
4. **Field Conversion**: Wraps `Field()` calls with `dataclasses.field()` ([pydantic/dataclasses.py228-234](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L228-L234))
5. **Stdlib Application**: Applies `@dataclasses.dataclass` decorator ([pydantic/dataclasses.py239-249](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L239-L249))
6. **Completion**: Builds schema and validators ([pydantic/dataclasses.py310](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L310-L310))

**Sources:** [pydantic/dataclasses.py153-313](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L153-L313)

### Field Patching System

The `patch_base_fields` context manager temporarily modifies parent dataclass fields:

```
```

This ensures that `kw_only` and `repr` attributes from `Field()` are recognized by the stdlib `@dataclass` decorator during class construction.

**Sources:** [pydantic/\_internal/\_dataclasses.py229-315](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L229-L315)

## Field Collection

### Dataclass Field Collection

Field collection for dataclasses differs from models because fields are already processed by stdlib:

```
```

**Sources:** [pydantic/\_internal/\_fields.py460-524](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#L460-L524)

### Field Collection Process

The `collect_dataclass_fields` function:

1. Iterates through `__mro__` in reverse to respect inheritance
2. Accesses `__dataclass_fields__` from each base
3. Evaluates type annotations using namespace resolver
4. Filters out `ClassVar` annotations
5. Handles `InitVar` types specially
6. Creates `FieldInfo` instances from dataclass field metadata

**Sources:** [pydantic/\_internal/\_fields.py460-524](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#L460-L524)

### FieldInfo from Dataclass Field

```
```

**Sources:** [pydantic/\_internal/\_fields.py508-524](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#L508-L524)

## Integration with Standard Library Dataclasses

### Converting Vanilla Dataclasses

Pydantic can enhance existing stdlib dataclasses:

```
```

When converting, Pydantic:

1. Subclasses the original to avoid mutation
2. Preserves generics by including `Generic[*params]` in bases
3. Maintains original `__doc__` (if not default)
4. Forwards frozen/order/etc parameters

**Sources:** [pydantic/dataclasses.py194-206](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L194-L206) [tests/test\_dataclasses.py807-840](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L807-L840)

### Inheritance from Vanilla Dataclasses

```
```

**Sources:** [tests/test\_dataclasses.py941-958](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L941-L958) [pydantic/\_internal/\_fields.py488-499](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py#L488-L499)

### Field Compatibility

Both `dataclasses.field()` and `pydantic.Field()` work in Pydantic dataclasses:

| Feature                | `dataclasses.field()` | `pydantic.Field()` |
| ---------------------- | --------------------- | ------------------ |
| `default`              | ✓                     | ✓                  |
| `default_factory`      | ✓                     | ✓                  |
| `init`                 | ✓                     | ✓                  |
| `repr`                 | ✓                     | ✓                  |
| `kw_only`              | ✓                     | ✓                  |
| `metadata`             | ✓                     | ✓                  |
| Validation constraints | ✗                     | ✓                  |
| Alias                  | ✗                     | ✓                  |
| JSON schema metadata   | ✗                     | ✓                  |

**Sources:** [tests/test\_dataclasses.py573-591](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L573-L591) [pydantic/dataclasses.py228-234](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L228-L234)

## Validation and Initialization

### Custom `__init__` Injection

Pydantic replaces the dataclass `__init__` with validation logic:

```
```

**Sources:** [pydantic/\_internal/\_dataclasses.py118-122](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L118-L122)

### Validation Modes

```
```

**Sources:** [pydantic/\_internal/\_dataclasses.py118-122](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L118-L122) [tests/test\_dataclasses.py270-283](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L270-L283)

### Validate Assignment

With `validate_assignment=True`, field assignments are validated:

```
```

**Sources:** [pydantic/dataclasses.py251-268](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L251-L268) [tests/test\_dataclasses.py120-130](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L120-L130)

## Dataclass Completion

### The `complete_dataclass` Function

This function builds the schema and creates validators/serializers:

```
```

**Sources:** [pydantic/\_internal/\_dataclasses.py85-190](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L85-L190)

### Deferred Building

When `defer_build=True` in config:

1. Mock validator/serializer are installed
2. Schema building is skipped
3. `__pydantic_complete__ = False`
4. First validation attempt triggers rebuild

**Sources:** [pydantic/\_internal/\_dataclasses.py130-132](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L130-L132)

### Rebuilding Dataclasses

The `rebuild_dataclass` function handles forward reference resolution:

```
```

**Sources:** [pydantic/dataclasses.py340-398](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L340-L398)

## Advanced Features

### InitVar Support

`InitVar` fields are passed to `__init__` but not stored:

```
```

**Sources:** [tests/test\_dataclasses.py673-702](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L673-L702)

### `__post_init__` Hook

Called after validation completes:

1. All fields are validated and set
2. `__post_init__(*initvars)` is called
3. Can modify fields (unless frozen)
4. Can perform additional validation
5. `InitVar` parameters are passed as arguments

**Sources:** [tests/test\_dataclasses.py270-283](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L270-L283) [tests/test\_dataclasses.py380-396](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L380-L396)

### Frozen Dataclasses

```
```

The `frozen` parameter can be set via decorator or config. Decorator takes priority.

**Sources:** [pydantic/dataclasses.py209-220](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L209-L220) [tests/test\_dataclasses.py108-118](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L108-L118)

### Computed Fields

Computed fields work in dataclasses:

```
```

- Not included in validation schema
- Included in serialization schema
- Appear in `model_dump()` output

**Sources:** [tests/test\_dataclasses.py1285-1328](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L1285-L1328)

## Schema Generation

### Core Schema Generation

Dataclasses use the `dataclass_schema` core schema type:

```
```

**Sources:** [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py) (referenced but not in provided files)

### JSON Schema Generation

JSON schemas for dataclasses:

| Mode            | Schema Representation            |
| --------------- | -------------------------------- |
| `validation`    | Object with required fields      |
| `serialization` | Object including computed fields |

Nested dataclasses become `$ref` definitions.

**Sources:** [tests/test\_dataclasses.py607-645](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L607-L645) [tests/test\_dataclasses.py648-670](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L648-L670)

## Utility Functions

### `is_pydantic_dataclass`

Type guard to check if a class is a Pydantic dataclass:

```
```

Checks both the Pydantic marker and stdlib dataclass status.

**Sources:** [pydantic/dataclasses.py401-413](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L401-L413)

### `is_stdlib_dataclass`

Internal function to identify stdlib-only dataclasses:

```
```

Used during dataclass creation to detect vanilla dataclasses for subclassing.

**Sources:** [pydantic/\_internal/\_dataclasses.py193-205](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L193-L205)

### `set_dataclass_mocks`

Installs placeholder validator/serializer when building is deferred:

```
```

**Sources:** [pydantic/\_internal/\_dataclasses.py131](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py#L131-L131)

## Configuration and ConfigDict

Dataclasses support the same `ConfigDict` as models:

| Config Option             | Effect in Dataclasses                                     |
| ------------------------- | --------------------------------------------------------- |
| `validate_assignment`     | Enable validation on field assignment                     |
| `frozen`                  | Make dataclass immutable (alternative to decorator param) |
| `arbitrary_types_allowed` | Allow non-Pydantic types                                  |
| `str_max_length`          | String length validation                                  |
| `extra`                   | Handling of extra attributes during assignment            |
| `revalidate_instances`    | Revalidate dataclass instances                            |

**Sources:** [tests/test\_dataclasses.py120-149](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L120-L149) [tests/test\_dataclasses.py515-540](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py#L515-L540)

### Config Priority

1. Decorator `config` parameter (highest)
2. Class `__pydantic_config__` attribute
3. Default Pydantic config (lowest)

Warnings are issued if both decorator and attribute are specified.

**Sources:** [pydantic/dataclasses.py175-181](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py#L175-L181)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Dataclass Support](#dataclass-support.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Decorator API and Core Types](#decorator-api-and-core-types.md)
- [The \`dataclass\` Decorator](#the-dataclass-decorator.md)
- [Decorator Parameters](#decorator-parameters.md)
- [PydanticDataclass Protocol](#pydanticdataclass-protocol.md)
- [Dataclass Creation and Lifecycle](#dataclass-creation-and-lifecycle.md)
- [Creation Flow](#creation-flow.md)
- [The \`create\_dataclass\` Function](#the-create_dataclass-function.md)
- [Field Patching System](#field-patching-system.md)
- [Field Collection](#field-collection.md)
- [Dataclass Field Collection](#dataclass-field-collection.md)
- [Field Collection Process](#field-collection-process.md)
- [FieldInfo from Dataclass Field](#fieldinfo-from-dataclass-field.md)
- [Integration with Standard Library Dataclasses](#integration-with-standard-library-dataclasses.md)
- [Converting Vanilla Dataclasses](#converting-vanilla-dataclasses.md)
- [Inheritance from Vanilla Dataclasses](#inheritance-from-vanilla-dataclasses.md)
- [Field Compatibility](#field-compatibility.md)
- [Validation and Initialization](#validation-and-initialization.md)
- [Custom \`\_\_init\_\_\` Injection](#custom-__init__-injection.md)
- [Validation Modes](#validation-modes.md)
- [Validate Assignment](#validate-assignment.md)
- [Dataclass Completion](#dataclass-completion.md)
- [The \`complete\_dataclass\` Function](#the-complete_dataclass-function.md)
- [Deferred Building](#deferred-building.md)
- [Rebuilding Dataclasses](#rebuilding-dataclasses.md)
- [Advanced Features](#advanced-features.md)
- [InitVar Support](#initvar-support.md)
- [\`\_\_post\_init\_\_\` Hook](#__post_init__-hook.md)
- [Frozen Dataclasses](#frozen-dataclasses.md)
- [Computed Fields](#computed-fields.md)
- [Schema Generation](#schema-generation.md)
- [Core Schema Generation](#core-schema-generation.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [Utility Functions](#utility-functions.md)
- [\`is\_pydantic\_dataclass\`](#is_pydantic_dataclass.md)
- [\`is\_stdlib\_dataclass\`](#is_stdlib_dataclass.md)
- [\`set\_dataclass\_mocks\`](#set_dataclass_mocks.md)
- [Configuration and ConfigDict](#configuration-and-configdict.md)
- [Config Priority](#config-priority.md)
