Core Schema Generation | pydantic/pydantic | DeepWiki

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

# Core Schema Generation

Relevant source files

- [pydantic/\_internal/\_core\_metadata.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_metadata.py)
- [pydantic/\_internal/\_generate\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py)
- [pydantic/json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py)
- [pyproject.toml](https://github.com/pydantic/pydantic/blob/76ef0b08/pyproject.toml)
- [tests/test\_datetime.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_datetime.py)
- [tests/test\_json\_schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_json_schema.py)

Core Schema Generation is the foundational system in Pydantic that converts Python type annotations into schema representations that can be used for validation, serialization, and documentation. This process is essential for Pydantic's type validation capabilities and forms the bridge between Python's type system and Pydantic's runtime validation logic. For information about how these schemas are then converted to JSON Schema, see [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md).

## Overview

At its heart, Core Schema Generation takes Python type annotations and transforms them into a structured schema representation that pydantic-core (Pydantic's underlying validation engine written in Rust) can understand and use for validation. This transformation enables Pydantic to perform efficient validation while maintaining Python's type hinting semantics.

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py318-342](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L318-L342)
- [pydantic/\_internal/\_generate\_schema.py679-716](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L679-L716)

## The GenerateSchema Class

The `GenerateSchema` class is the central component responsible for transforming Python types into core schemas. It provides methods for handling different Python types and constructing appropriate schema representations.

```
```

The `generate_schema` method is the main entry point that dispatches to type-specific handlers based on the input object. The class also maintains state such as a stack of models being processed (to handle recursive references) and definitions being generated.

Sources:

- [pydantic/\_internal/\_generate\_schema.py318-342](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L318-L342)
- [pydantic/\_internal/\_generate\_schema.py679-716](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L679-L716)
- [pydantic/\_internal/\_generate\_schema.py366-377](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L366-L377)

## Schema Generation Process

The schema generation process follows several steps to convert Python types into a complete core schema:

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py679-716](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L679-L716)
- [pydantic/\_internal/\_generate\_schema.py843-889](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L843-L889)
- [pydantic/\_internal/\_generate\_schema.py718-843](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L718-L843)

## Core Schema Types

Pydantic uses a variety of schema types to represent different Python types and validation rules. These schemas form a hierarchy with specialized validations for each type.

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py366-419](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L366-L419)
- [pydantic/\_internal/\_generate\_schema.py449-482](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L449-L482)
- [pydantic/\_internal/\_generate\_schema.py565-602](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L565-L602)

## Type-Specific Schema Generation

Different Python types require specialized schema generation logic. Here are some key schema generation methods:

### Primitive Types

For primitive types like strings, integers, and floats, the schema generation is relatively straightforward, with additions for constraints like minimum/maximum values or string patterns.

### Container Types

For container types like lists, dictionaries, and sets, the schema generation recursively processes the contained types:

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py366-377](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L366-L377)

### Special Types

Special types like IP addresses, paths, and fractions have custom schema generation logic:

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py450-481](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L450-L481)
- [pydantic/\_internal/\_generate\_schema.py482-539](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L482-L539)
- [pydantic/\_internal/\_generate\_schema.py604-619](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L604-L619)

### Models

For Pydantic models, the schema generation process is more complex, involving:

1. Collecting field information
2. Processing validators and serializers
3. Handling inheritance and generics
4. Creating the appropriate model schema

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py718-842](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L718-L842)

## Handling Discriminated Unions

Pydantic supports discriminated unions, which are unions of models that can be distinguished by a "discriminator" field. This enables more efficient validation and better error messages.

```
```

Sources:

- [pydantic/\_internal/\_discriminated\_union.py34-68](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_discriminated_union.py#L34-L68)
- [pydantic/\_internal/\_discriminated\_union.py140-168](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_discriminated_union.py#L140-L168)
- [tests/test\_discriminated\_union.py94-141](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_discriminated_union.py#L94-L141)

## Metadata Processing

Type annotations can include metadata that affects schema generation. This is particularly relevant for `Annotated` types and field constraints.

```
```

Metadata can come from various sources:

- Field constraints (min\_length, max\_length, etc.)
- Validators (before, after, wrap validators)
- Field descriptions and examples
- Custom schema transformations

Sources:

- [pydantic/\_internal/\_known\_annotated\_metadata.py168-329](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_known_annotated_metadata.py#L168-L329)
- [tests/test\_annotated.py28-134](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_annotated.py#L28-L134)

## Reference Handling

Core schema generation deals with references between types, which is especially important for recursive or self-referential models.

```
```

Sources:

- [pydantic/\_internal/\_core\_utils.py67-102](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_utils.py#L67-L102)
- [pydantic/\_internal/\_generate\_schema.py722-736](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L722-L736)
- [tests/test\_internal.py23-139](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_internal.py#L23-L139)

## Schema Cleaning and Finalization

Before the schema is used, it undergoes cleaning and finalization processes:

1. Resolving definition references
2. Validating the schema structure
3. Removing unnecessary complexities
4. Optimizing for performance

```
```

Sources:

- [pydantic/\_internal/\_generate\_schema.py664-666](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L664-L666)
- [pydantic/\_internal/\_core\_utils.py112-115](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_core_utils.py#L112-L115)

## Integration with JSON Schema Generation

Once a core schema is generated, it can be used to create a JSON Schema representation. This is a separate process handled by the `GenerateJsonSchema` class and is covered in [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md).

```
```

Sources:

- [pydantic/json\_schema.py216-426](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/json_schema.py#L216-L426)
- [pydantic/\_internal/\_generate\_schema.py706-716](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L706-L716)

## Customizing Core Schema Generation

Types can customize their core schema generation by implementing the `__get_pydantic_core_schema__` method, which allows for complete control over how a type is validated and serialized.

```
```

Sources:

- [tests/test\_annotated.py198-249](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_annotated.py#L198-L249)
- [pydantic/\_internal/\_generate\_schema.py843-889](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generate_schema.py#L843-L889)

## Conclusion

Core Schema Generation is the fundamental process that enables Pydantic's validation capabilities. By converting Python types into a structured schema representation, it creates a bridge between Python's static type system and runtime validation logic. This system is highly extensible, allowing for custom validation rules, serialization behaviors, and schema transformations.

The generated core schemas are used throughout Pydantic for validation, serialization, and documentation generation, making this system central to Pydantic's functionality.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Core Schema Generation](#core-schema-generation.md)
- [Overview](#overview.md)
- [The GenerateSchema Class](#the-generateschema-class.md)
- [Schema Generation Process](#schema-generation-process.md)
- [Core Schema Types](#core-schema-types.md)
- [Type-Specific Schema Generation](#type-specific-schema-generation.md)
- [Primitive Types](#primitive-types.md)
- [Container Types](#container-types.md)
- [Special Types](#special-types.md)
- [Models](#models.md)
- [Handling Discriminated Unions](#handling-discriminated-unions.md)
- [Metadata Processing](#metadata-processing.md)
- [Reference Handling](#reference-handling.md)
- [Schema Cleaning and Finalization](#schema-cleaning-and-finalization.md)
- [Integration with JSON Schema Generation](#integration-with-json-schema-generation.md)
- [Customizing Core Schema Generation](#customizing-core-schema-generation.md)
- [Conclusion](#conclusion.md)
