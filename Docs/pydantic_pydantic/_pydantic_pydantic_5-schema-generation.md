Schema Generation | pydantic/pydantic | DeepWiki

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

# Schema Generation

Relevant source files

- [pydantic/\_internal/\_core\_metadata.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_metadata.py)
- [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)
- [pydantic/json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py)
- [pyproject.toml](https://github.com/pydantic/pydantic/blob/76ef0b08/pyproject.toml)
- [tests/test\_datetime.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_datetime.py)
- [tests/test\_json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py)

Schema generation is the process that converts Python types and annotations into Pydantic's internal schema representation and JSON Schema. This page focuses on how Pydantic transforms type annotations into both core schemas (used internally for validation and serialization) and JSON schemas (for external documentation and compatibility).

For information about how to use JSON Schema with Pydantic models, see the relevant documentation section.

## Schema Generation Architecture

Pydantic's schema generation involves two main phases: core schema generation and JSON schema generation. The core schema is an internal representation used for validation and serialization, while the JSON schema follows the standard JSON Schema specification for external use.

```
```

Sources: [pydantic/\_internal/\_generate\_schema.py318-319](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L318-L319) [pydantic/json\_schema.py216-249](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L216-L249)

## Core Schema Generation

The core schema generation is handled by the `GenerateSchema` class, which converts Python types to pydantic-core schemas. It's a comprehensive system that supports a wide variety of Python types and provides the foundation for Pydantic's validation and serialization capabilities.

```
```

Sources: [pydantic/\_internal/\_generate\_schema.py318-343](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L318-L343) [pydantic/\_internal/\_generate\_schema.py679-702](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L679-L702)

### Type Matching and Schema Mapping

The core schema generation uses a type matching system to map Python types to appropriate schema generation methods. The `match_type` method contains the primary mapping logic:

```
```

Sources: [pydantic/\_internal/\_generate\_schema.py991-1042](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L991-L1042)

### Schema Generation Process

The main entry point for generating a core schema is the `generate_schema` method. The process involves:

1. Checking if the type implements `__get_pydantic_core_schema__` for custom handling
2. Resolving forward references and type variables
3. Mapping the type to an appropriate schema generation method
4. Recursively processing nested types
5. Adding metadata and customizations to the schema

Sources: [pydantic/\_internal/\_generate\_schema.py679-716](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L679-L716)

## JSON Schema Generation

Once the core schema is created, it can be converted to a JSON Schema using the `GenerateJsonSchema` class. This transformation enables compatibility with external tools and provides a standardized format for documentation.

```
```

Sources: [pydantic/json\_schema.py216-426](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L216-L426)

### JSON Schema Modes

The JSON schema generation supports two modes:

- **Validation**: Defines the schema for input validation, including constraints and requirements
- **Serialization**: Defines the schema for output serialization, potentially with different rules

```
```

Sources: [pydantic/json\_schema.py79-87](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L79-L87) [pydantic/json\_schema.py378-425](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L378-L425)

### JSON Schema Type Handlers

Similar to the core schema generation, the JSON schema generation maps different core schema types to appropriate JSON schema handlers:

```
```

Sources: [pydantic/json\_schema.py427-566](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L427-L566)

## Custom Schema Generation

Both the core schema generation and JSON schema generation support customization through various mechanisms:

### Custom Core Schema Generation

Custom types can define how they're converted to core schemas by implementing the `__get_pydantic_core_schema__` method:

```
```

Sources: [pydantic/\_internal/\_generate\_schema.py850-890](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L850-L890)

### Custom JSON Schema Generation

Similarly, custom types can define their JSON Schema representation by using core schema metadata or implementing custom hooks:

```
```

Sources: [pydantic/\_internal/\_core\_metadata.py13-45](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_metadata.py#L13-L45) [pydantic/json\_schema.py504-565](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L504-L565)

## Schema Reference Handling

Both schema generation systems handle references to avoid duplicating schemas for the same types. The core schema uses a definition registry, while JSON Schema uses standard `$ref` references:

```
```

The reference handling ensures efficient schema representation and prevents circular references from causing infinite recursion.

Sources: [pydantic/\_internal/\_generate\_schema.py723-736](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L723-L736) [pydantic/json\_schema.py140-214](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L140-L214)

## Working with Schema Generation

Schema generation is typically handled automatically by Pydantic, but understanding its mechanisms helps when:

1. Implementing custom types with specific validation or serialization behavior
2. Creating advanced validation rules that combine multiple types
3. Working with tools that consume JSON Schema (like API documentation tools)
4. Debugging validation and serialization issues

To directly access the schema generation functionality:

- **Core Schema**: Use `model.__pydantic_core_schema__` to access the core schema of a model
- **JSON Schema**: Use `model.model_json_schema()` to generate a JSON schema for a model

Sources: [pydantic/\_internal/\_generate\_schema.py679-716](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L679-L716) [pydantic/json\_schema.py378-425](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L378-L425)

## Schema Validation and Serialization

The generated schemas are used for both validation and serialization:

| Purpose        | Schema Type | Description                                                   |
| -------------- | ----------- | ------------------------------------------------------------- |
| Validation     | Core Schema | Used to create validators that check incoming data            |
| Serialization  | Core Schema | Used to create serializers that convert data to output format |
| Documentation  | JSON Schema | Provides standardized documentation of the data model         |
| External Tools | JSON Schema | Enables integration with tools that understand JSON Schema    |

Sources: [pydantic/\_internal/\_generate\_schema.py318-319](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L318-L319) [pydantic/json\_schema.py79-87](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L79-L87)

Schema generation is a fundamental part of Pydantic's functionality, serving as the bridge between Python's type system and the validation, serialization, and documentation capabilities that make Pydantic powerful.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Schema Generation](#schema-generation.md)
- [Schema Generation Architecture](#schema-generation-architecture.md)
- [Core Schema Generation](#core-schema-generation.md)
- [Type Matching and Schema Mapping](#type-matching-and-schema-mapping.md)
- [Schema Generation Process](#schema-generation-process.md)
- [JSON Schema Generation](#json-schema-generation.md)
- [JSON Schema Modes](#json-schema-modes.md)
- [JSON Schema Type Handlers](#json-schema-type-handlers.md)
- [Custom Schema Generation](#custom-schema-generation.md)
- [Custom Core Schema Generation](#custom-core-schema-generation.md)
- [Custom JSON Schema Generation](#custom-json-schema-generation.md)
- [Schema Reference Handling](#schema-reference-handling.md)
- [Working with Schema Generation](#working-with-schema-generation.md)
- [Schema Validation and Serialization](#schema-validation-and-serialization.md)
