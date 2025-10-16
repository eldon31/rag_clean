TypeAdapter | pydantic/pydantic | DeepWiki

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

# Type Adapter

Relevant source files

- [pydantic/\_internal/\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py)
- [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)
- [pydantic/functional\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py)
- [pydantic/plugin/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py)
- [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)
- [pydantic/root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py)
- [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py)
- [pydantic/validate\_call\_decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py)
- [tests/test\_plugins.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py)
- [tests/test\_type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py)
- [tests/test\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py)

TypeAdapter is a flexible component in Pydantic that allows you to apply validation and serialization to arbitrary Python types, not just Pydantic models. It bridges the gap between Python types and Pydantic's validation system, enabling you to use Pydantic's powerful data validation and conversion capabilities with standard Python types, dataclasses, TypedDict, and more.

For information about validating model fields, see [Field System](pydantic/pydantic/2.2-field-system.md). For information about customizing validation through validators, see [Validators](pydantic/pydantic/4.1-validators.md).

## Core Concepts

TypeAdapter wraps a Python type with Pydantic's validation and serialization functionality. It creates a core schema for the type, and uses this schema to validate input data and serialize output data.

```
```

Sources: [pydantic/type\_adapter.py69-107](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L69-L107)

- Container types (list, dict, tuple, etc.)
- Pydantic models
- dataclasses
- TypedDict
- Generic types
- Custom types

```
```

Sources: [pydantic/type\_adapter.py195-234](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L195-L234)"] ValidateMethod --> |"Input is invalid"| ValidationError\["ValidationError"]

```
    subgraph "Validation Parameters"
        Params["Parameters:
        - strict
        - context
        - from_attributes
        - by_alias
        - by_name
        - experimental_allow_partial"]
    end
    
    Params --> ValidateMethod
end
```

```

Sources: <FileRef file-url="https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L381-L430" min=381 max=430 file-path="pydantic/type_adapter.py">Hii</FileRef>"]
        end
        
        Params --> SerializeMethod
    end
```

Sources: [pydantic/type\_adapter.py532-586](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L532-L586) schema = adapter.json\_schema()

```

The `json_schema` method has parameters to control schema generation:

- `by_alias`: Whether to use alias names for field names
- `ref_template`: The format string for generating $ref strings
- `schema_generator`: The generator class for creating the schema
- `mode`: The mode to use for schema generation (validation or serialization)

Sources: <FileRef file-url="https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L647-L678" min=647 max=678 file-path="pydantic/type_adapter.py">Hii</FileRef>"] --> |"1. Initial creation"| CS["Mock CoreSchema"]
        CS --> |"2. Type needs resolution"| RebuildMethod["rebuild()"]
        RebuildMethod --> |"3. Resolves forward references"| FinalCS["Final CoreSchema"]
        FinalCS --> VS["SchemaValidator"]
        FinalCS --> SS["SchemaSerializer"]
    end
```

When using forward references, you may need to call `rebuild` explicitly to resolve them:

```
```

Sources: [pydantic/type\_adapter.py335-379](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L335-L379))

# This will fail due to strict validation

try: int\_list\_adapter.validate\_python(\["1", "2"]) except Exception as e: print(f"Validation failed: {e}")

```

However, you cannot provide a configuration when the type you're using has its own config that cannot be overridden (e.g., `BaseModel`, `TypedDict`, and `dataclass`).

Sources: <FileRef file-url="https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L198-L210" min=198 max=210 file-path="pydantic/type_adapter.py">Hii</FileRef>)

# Later, when SomeType is fully defined:
adapter.rebuild()
```

When `defer_build` is `True`, TypeAdapter sets mock objects for the core schema, validator, and serializer. These mocks will attempt to rebuild the schema when accessed.

Sources: [pydantic/type\_adapter.py317-331](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L317-L331) float\_adapter = TypeAdapter(float) str\_adapter = TypeAdapter(str) bool\_adapter = TypeAdapter(bool)

````

### Container Types

```python
list_adapter = TypeAdapter(list[int])
dict_adapter = TypeAdapter(dict[str, int])
tuple_adapter = TypeAdapter(tuple[str, int])
set_adapter = TypeAdapter(set[int])
````

### Pydantic Models

```
```

### Dataclasses

```
```

### TypedDict

```
```

### Union Types

```
```

### Generic Types

```
```

Sources: [tests/test\_type\_adapter.py42-65](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py#L42-L65)

try: int\_list\_adapter.validate\_python(\["1", "not\_an\_int"]) except ValidationError as e: print(f"Validation errors: {e.errors()}")

```

ValidationError provides detailed information about what failed, where the error occurred, and why.

Sources: <FileRef file-url="https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py#L194-L254" min=194 max=254 file-path="tests/test_type_adapter.py">Hii</FileRef> -> bool:
    """Returns whether the type has config."""
    type_ = _typing_extra.annotated_type(type_) or type_
    try:
        return issubclass(type_, BaseModel) or is_dataclass(type_) or is_typeddict(type_)
    except TypeError:
        # type is not a class
        return False
```

Sources: \[pydantic/type\_adapter.py:58-66]\(

## Technical Implementation Details

TypeAdapter uses a combination of:

1. Core schema generation via `GenerateSchema`
2. Validation via `SchemaValidator` or `PluggableSchemaValidator`
3. Serialization via `SchemaSerializer`
4. Namespace resolution for type resolution
5. Mock objects for deferred building

It also has special handling for generic types, forward references, and namespace management to ensure types are correctly resolved.

Sources: \[pydantic/type\_adapter.py:246-316]\(, \[pydantic/\_internal/\_namespace\_utils.py:143-293]\(, \[pydantic/\_internal/\_mock\_val\_ser.py:21-149]\(

## Summary

TypeAdapter is a powerful component that brings Pydantic's validation and serialization capabilities to any Python type. It's particularly useful for:

1. Validating simple types like integers and strings with Pydantic's conversion logic
2. Validating complex types like lists and dictionaries with nested validation
3. Working with non-model types like dataclasses and TypedDict
4. Applying validation to arbitrary types in a consistent way
5. Generating JSON schemas for arbitrary types
6. Serializing instances of arbitrary types consistently

By wrapping a type in a TypeAdapter, you can leverage Pydantic's robust validation and serialization features without having to create a full model class.

```
```

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Type Adapter](#type-adapter.md)
- [Core Concepts](#core-concepts.md)
- [Instantiating a TypeAdapter](#instantiating-a-typeadapter.md)
- [Validation Methods](#validation-methods.md)
- [Serialization Methods](#serialization-methods.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [Type Resolution and Forward References](#type-resolution-and-forward-references.md)
- [Integration with Pydantic Systems](#integration-with-pydantic-systems.md)
- [Configuration](#configuration.md)
- [Deferred Building](#deferred-building.md)
- [Working with Different Types](#working-with-different-types.md)
- [Primitive Types](#primitive-types.md)
- [Container Types](#container-types.md)
- [Pydantic Models](#pydantic-models.md)
- [Dataclasses](#dataclasses.md)
- [TypedDict](#typeddict.md)
- [Union Types](#union-types.md)
- [Generic Types](#generic-types.md)
- [Error Handling](#error-handling.md)
- [Type Detection](#type-detection.md)
- [Technical Implementation Details](#technical-implementation-details.md)
- [Summary](#summary.md)
