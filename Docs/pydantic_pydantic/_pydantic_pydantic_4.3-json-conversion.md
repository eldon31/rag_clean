JSON Conversion | pydantic/pydantic | DeepWiki

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

# JSON Conversion

Relevant source files

- [pydantic/json.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json.py)
- [tests/test\_json.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py)

## Purpose and Scope

This document details how Pydantic handles the conversion of Python objects to and from JSON. It covers both the serialization (Python → JSON) and deserialization (JSON → Python) processes, including the core architecture, built-in serialization behavior for various data types, and customization options.

For information about validators, see [Validators](pydantic/pydantic/4.1-validators.md). For information about the broader serialization system including Python dict serialization, see [Serializers](pydantic/pydantic/4.2-serializers.md).

## Serialization and Deserialization Architecture

```
```

Sources: [tests/test\_json.py92-94](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L92-L94) [tests/test\_json.py134-137](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L134-L137) [tests/test\_json.py234-236](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L234-L236)

## JSON Serialization Methods

Pydantic provides two primary ways to serialize objects to JSON:

1. `BaseModel.model_dump_json()` - For serializing model instances
2. `TypeAdapter.dump_json()` - For serializing arbitrary types

```
```

Sources: [tests/test\_json.py134-137](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L134-L137) [tests/test\_json.py92-94](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L92-L94)

### BaseModel Serialization

The `model_dump_json()` method converts a model instance to a JSON string:

```
```

The method accepts the same parameters as `model_dump()`, plus JSON-specific parameters:

| Parameter          | Type       | Description                          |
| ------------------ | ---------- | ------------------------------------ |
| `indent`           | `int`      | Number of spaces for indentation     |
| `exclude`          | `set[str]` | Fields to exclude                    |
| `include`          | `set[str]` | Fields to include (excluding others) |
| `by_alias`         | `bool`     | Whether to use field aliases         |
| `exclude_unset`    | `bool`     | Exclude fields not explicitly set    |
| `exclude_defaults` | `bool`     | Exclude fields with default values   |
| `exclude_none`     | `bool`     | Exclude None fields                  |

Sources: [tests/test\_json.py134-137](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L134-L137) [tests/test\_json.py226](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L226-L226) [tests/test\_json.py368-369](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L368-L369)

### TypeAdapter Serialization

The `TypeAdapter` class provides a way to serialize arbitrary types to JSON:

```
```

Sources: [tests/test\_json.py92-94](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L92-L94)

## JSON Deserialization Methods

Pydantic provides corresponding methods for deserializing JSON:

1. `BaseModel.model_validate_json()` - For deserializing to model instances
2. `TypeAdapter.validate_json()` - For deserializing to arbitrary types

```
```

Sources: [tests/test\_json.py234-236](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L234-L236) [tests/test\_json.py251](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L251-L251)

## Type Handling in JSON Serialization

Pydantic provides special handling for various Python types when serializing to JSON:

```
```

Sources: [tests/test\_json.py61-91](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L61-L91)

### Built-in Type Serialization

| Python Type                       | JSON Representation        | Example                                  |
| --------------------------------- | -------------------------- | ---------------------------------------- |
| `str`                             | string                     | `"text"`                                 |
| `int`/`float`                     | number                     | `123`, `3.14`                            |
| `bool`                            | boolean                    | `true`, `false`                          |
| `None`                            | null                       | `null`                                   |
| `list`/`tuple`/`set`              | array                      | `[1, 2, 3]`                              |
| `dict`                            | object                     | `{"key": "value"}`                       |
| `UUID`                            | string                     | `"ebcdab58-6eb8-46fb-a190-d07a33e9eac8"` |
| `datetime`                        | string (ISO 8601)          | `"2032-01-01T01:01:00"`                  |
| `date`                            | string (ISO 8601)          | `"2032-01-01"`                           |
| `time`                            | string (ISO 8601)          | `"12:34:56"`                             |
| `timedelta`                       | string (ISO 8601 duration) | `"P12DT34.000056S"`                      |
| `bytes`                           | string (UTF-8)             | `"this is bytes"`                        |
| `Decimal`                         | string                     | `"12.34"`                                |
| `Enum`                            | string/number              | `"bar"`                                  |
| `Pattern`                         | string                     | `"^regex$"`                              |
| `SecretStr`/`SecretBytes`         | string (masked)            | `"**********"`                           |
| `IPv4Address`/`IPv6Address`       | string                     | `"192.168.0.1"`                          |
| `Path`/`FilePath`/`DirectoryPath` | string                     | `"/path/to/file"`                        |

Sources: [tests/test\_json.py61-91](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L61-L91) [tests/test\_json.py107-120](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L107-L120)

### Special Cases

#### Infinity and NaN

By default, `float('inf')`, `float('-inf')`, and `float('nan')` values raise errors in JSON serialization. You can configure how they are handled:

```
```

With this configuration, these values become `"Infinity"`, `"-Infinity"`, and `"NaN"` in JSON.

Sources: [tests/test\_json.py508-538](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L508-L538)

#### Bytes

You can configure how bytes are serialized to JSON:

```
```

Options:

- `'utf8'` (default): Decode bytes as UTF-8
- `'base64'`: Encode bytes as base64
- `'hex'`: Encode bytes as hexadecimal

Sources: [tests/test\_json.py541-576](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L541-L576)

## Customizing JSON Serialization

Pydantic offers multiple ways to customize how types are serialized to JSON.

```
```

Sources: [tests/test\_json.py212-226](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L212-L226) [tests/test\_json.py400-414](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L400-L414) [tests/test\_json.py426-439](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L426-L439)

### Field Serializers

Field serializers allow customizing serialization for specific fields in a model:

```
```

The `when_used` parameter can be:

- `'always'` (default): Apply the serializer for all serializations
- `'json'`: Apply only when serializing to JSON
- `'unless-none'`: Apply only for non-None values

Sources: [tests/test\_json.py212-226](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L212-L226) [tests/test\_json.py292-332](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L292-L332)

### JSON Encoders

You can use the `json_encoders` configuration option to customize serialization for specific types:

```
```

JSON encoders are applied when serializing to JSON, not when creating Python dictionaries.

Sources: [tests/test\_json.py400-414](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L400-L414) [tests/test\_json.py426-439](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L426-L439) [tests/test\_json.py480-488](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L480-L488)

### Annotated Serializers

You can attach serializers to specific type annotations using `Annotated` and `PlainSerializer`:

```
```

Sources: [tests/test\_json.py442-450](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L442-L450)

## Integration with Standard JSON Module

Pydantic provides a compatibility function for use with the standard `json` module:

```
```

This allows serializing models and other Pydantic types using the standard `json` module.

Sources: [tests/test\_json.py120](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L120-L120) [tests/test\_json.py278-288](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L278-L288)

## Inheritance and JSON Serialization

In class inheritance, field serializers from parent classes are used, unless the child class provides its own serializer for the same field:

```
```

Note that `json_encoders` configurations are not inherited; child models must define their own.

Sources: [tests/test\_json.py254-268](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L254-L268) [tests/test\_json.py426-439](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L426-L439)

## JSON Schema and Conversion

For information about generating JSON Schema from Pydantic models, see [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md).

Sources: [tests/test\_json.py372-397](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json.py#L372-L397)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [JSON Conversion](#json-conversion.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Serialization and Deserialization Architecture](#serialization-and-deserialization-architecture.md)
- [JSON Serialization Methods](#json-serialization-methods.md)
- [BaseModel Serialization](#basemodel-serialization.md)
- [TypeAdapter Serialization](#typeadapter-serialization.md)
- [JSON Deserialization Methods](#json-deserialization-methods.md)
- [Type Handling in JSON Serialization](#type-handling-in-json-serialization.md)
- [Built-in Type Serialization](#built-in-type-serialization.md)
- [Special Cases](#special-cases.md)
- [Infinity and NaN](#infinity-and-nan.md)
- [Bytes](#bytes.md)
- [Customizing JSON Serialization](#customizing-json-serialization.md)
- [Field Serializers](#field-serializers.md)
- [JSON Encoders](#json-encoders.md)
- [Annotated Serializers](#annotated-serializers.md)
- [Integration with Standard JSON Module](#integration-with-standard-json-module.md)
- [Inheritance and JSON Serialization](#inheritance-and-json-serialization.md)
- [JSON Schema and Conversion](#json-schema-and-conversion.md)
