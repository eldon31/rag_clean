JSON Schema Generation | pydantic/pydantic | DeepWiki

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

# JSON Schema Generation

Relevant source files

- [pydantic/\_internal/\_core\_metadata.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_metadata.py)
- [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)
- [pydantic/json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py)
- [pyproject.toml](https://github.com/pydantic/pydantic/blob/76ef0b08/pyproject.toml)
- [tests/test\_datetime.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_datetime.py)
- [tests/test\_json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py)

This document explains how Pydantic generates JSON Schema from models and types. JSON Schema is a vocabulary that allows you to annotate and validate JSON documents, which is useful for API documentation, client code generation, and validation in different environments. For information about internal core schema generation, see [Core Schema Generation](pydantic/pydantic/5.1-core-schema-generation.md).

## Overview

Pydantic provides built-in JSON Schema generation capabilities for its models and types. The generated JSON Schema documents describe the expected structure, types, constraints, and other metadata for validation and serialization purposes.

```
```

Sources: [pydantic/json\_schema.py216-427](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L216-L427)

## Architecture

The JSON Schema generation system centers around the `GenerateJsonSchema` class, which handles the entire process of converting Pydantic core schemas into standard JSON Schema documents.

```
```

Sources: [pydantic/json\_schema.py216-390](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L216-L390)

### Key Components

1. **GenerateJsonSchema**: The main class responsible for converting core schemas to JSON Schema documents
2. **Reference Management System**: Handles schema references to avoid duplication and circular dependencies
3. **Schema Mode Handling**: Supports both 'validation' and 'serialization' modes
4. **Type Mapping**: Converts Pydantic types to their JSON Schema equivalents

### JSON Schema Generation Flow

```
```

Sources: [pydantic/json\_schema.py378-425](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L378-L425)

## Reference System

The JSON Schema generator uses a sophisticated reference system to handle complex type references, avoid duplication, and manage circular dependencies.

```
```

Sources: [pydantic/json\_schema.py119-139](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L119-L139) [pydantic/json\_schema.py258-264](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L258-L264)

When Pydantic encounters the same type multiple times (such as a model used in different places), it creates a schema definition and uses references to avoid duplication:

1. **CoreRef**: Internal identifier for a core schema
2. **DefsRef**: Name of the type in the definitions dictionary
3. **JsonRef**: JSON Schema `$ref` value (e.g., `#/$defs/User`)

### Reference Template

By default, references use the format `#/$defs/{model}`, but this can be customized with the `ref_template` parameter:

```
```

Sources: [pydantic/json\_schema.py116-117](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L116-L117) [tests/test\_json\_schema.py143-178](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L143-L178)

## Schema Modes

Pydantic supports two modes for JSON Schema generation:

| Mode            | Description                  | Use Case                                    |
| --------------- | ---------------------------- | ------------------------------------------- |
| `validation`    | Schema for input validation  | Describes what input data should look like  |
| `serialization` | Schema for serialized output | Describes what model.model\_dump() produces |

The modes are important because some types have different representations for validation vs. serialization:

```
```

Sources: [pydantic/json\_schema.py79-87](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L79-L87) [tests/test\_json\_schema.py524-542](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L524-L542)

## Customizing JSON Schema Generation

Pydantic offers several ways to customize the generated JSON Schema:

### Model Configuration

Use the `model_config` with `json_schema_extra` to add custom attributes to the schema:

```
```

Sources: [tests/test\_json\_schema.py448-457](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L448-L457)

### Field Customization

Fields support various JSON Schema attributes directly:

```
```

Sources: [tests/test\_json\_schema.py226-245](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L226-L245)

### Type-Level Customization

Custom types can implement `__get_pydantic_json_schema__` to control their schema representation:

```
```

Sources: [tests/test\_json\_schema.py292-330](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L292-L330)

## Common JSON Schema Features

### Field Aliases

When using field aliases, schemas can be generated by alias or by attribute name:

```
```

Sources: [tests/test\_json\_schema.py125-142](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L125-L142) [tests/test\_json\_schema.py253-259](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L253-L259)

### Nested Models

When a model contains other models, those models are included in the `$defs` section and referenced:

```
```

Sources: [tests/test\_json\_schema.py195-223](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L195-L223) [tests/test\_json\_schema.py546-565](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L546-L565)

### Enums

Enum classes are represented with their possible values:

```
```

Sources: [tests/test\_json\_schema.py261-289](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L261-L289)

## Integration with Core Schema Generation

JSON Schema generation works in tandem with core schema generation:

```
```

During core schema generation, metadata can be attached for later use in JSON Schema generation:

1. `pydantic_js_functions`: For defining custom JSON Schema handlers
2. `pydantic_js_updates`: For adding or updating JSON Schema properties
3. `pydantic_js_extra`: For adding complete JSON Schema objects

Sources: [pydantic/\_internal/\_core\_metadata.py13-46](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_metadata.py#L13-L46) [pydantic/\_internal/\_generate\_schema.py668-713](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L668-L713)

## API Reference

Here are the main functions and classes for JSON Schema generation:

| Name                            | Description                                  |
| ------------------------------- | -------------------------------------------- |
| `BaseModel.model_json_schema()` | Generate JSON Schema for a model             |
| `TypeAdapter.json_schema()`     | Generate JSON Schema for any type            |
| `models_json_schema()`          | Generate JSON Schema for multiple models     |
| `GenerateJsonSchema`            | Class for customizing JSON Schema generation |

Sources: [pydantic/json\_schema.py216-224](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L216-L224) [tests/test\_json\_schema.py669-670](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py#L669-L670)

## Advanced Features

### Schema Dialect

By default, Pydantic uses the JSON Schema draft 2020-12 dialect, but this can be customized by extending `GenerateJsonSchema`:

```
```

Sources: [pydantic/json\_schema.py250-251](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L250-L251)

### Warning Management

The JSON Schema generator can emit warnings for issues like non-serializable defaults or skipped discriminators:

```
```

Sources: [pydantic/json\_schema.py101-106](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L101-L106) [pydantic/json\_schema.py252-254](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L252-L254)

### Advanced Reference Management

For complex schemas with many references, Pydantic attempts to simplify reference names by removing redundancy while avoiding collisions:

```
```

Sources: [pydantic/json\_schema.py135-186](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L135-L186)

## Performance Considerations

For models with many related types, JSON Schema generation may be expensive. Consider:

1. Caching generated schemas when appropriate
2. Only generating schemas when needed, not during startup
3. Using `TypeAdapter` for simpler types that don't need full model capabilities

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [JSON Schema Generation](#json-schema-generation.md)
- [Overview](#overview.md)
- [Architecture](#architecture.md)
- [Key Components](#key-components.md)
- [JSON Schema Generation Flow](#json-schema-generation-flow.md)
- [Reference System](#reference-system.md)
- [Reference Template](#reference-template.md)
- [Schema Modes](#schema-modes.md)
- [Customizing JSON Schema Generation](#customizing-json-schema-generation.md)
- [Model Configuration](#model-configuration.md)
- [Field Customization](#field-customization.md)
- [Type-Level Customization](#type-level-customization.md)
- [Common JSON Schema Features](#common-json-schema-features.md)
- [Field Aliases](#field-aliases.md)
- [Nested Models](#nested-models.md)
- [Enums](#enums.md)
- [Integration with Core Schema Generation](#integration-with-core-schema-generation.md)
- [API Reference](#api-reference.md)
- [Advanced Features](#advanced-features.md)
- [Schema Dialect](#schema-dialect.md)
- [Warning Management](#warning-management.md)
- [Advanced Reference Management](#advanced-reference-management.md)
- [Performance Considerations](#performance-considerations.md)
