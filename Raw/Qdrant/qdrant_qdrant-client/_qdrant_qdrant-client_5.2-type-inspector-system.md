Type Inspector System | qdrant/qdrant-client | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant-client](https://github.com/qdrant/qdrant-client "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 9 July 2025 ([ac6f6c](https://github.com/qdrant/qdrant-client/commits/ac6f6cd2))

- [Overview](qdrant/qdrant-client/1-overview.md)
- [Client Architecture](qdrant/qdrant-client/2-client-architecture.md)
- [Client Interface](qdrant/qdrant-client/2.1-client-interface.md)
- [Local Mode](qdrant/qdrant-client/2.2-local-mode.md)
- [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md)
- [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md)
- [Core Operations](qdrant/qdrant-client/3-core-operations.md)
- [Search Operations](qdrant/qdrant-client/3.1-search-operations.md)
- [Collection Management](qdrant/qdrant-client/3.2-collection-management.md)
- [Point Operations](qdrant/qdrant-client/3.3-point-operations.md)
- [Advanced Features](qdrant/qdrant-client/4-advanced-features.md)
- [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md)
- [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md)
- [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md)
- [Local Inference](qdrant/qdrant-client/4.4-local-inference.md)
- [Implementation Details](qdrant/qdrant-client/5-implementation-details.md)
- [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md)
- [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md)
- [Expression Evaluation](qdrant/qdrant-client/5.3-expression-evaluation.md)
- [Development & Testing](qdrant/qdrant-client/6-development-and-testing.md)
- [Project Setup](qdrant/qdrant-client/6.1-project-setup.md)
- [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md)
- [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md)

Menu

# Type Inspector System

Relevant source files

- [qdrant\_client/\_pydantic\_compat.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/_pydantic_compat.py)
- [qdrant\_client/embed/embed\_inspector.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embed_inspector.py)
- [qdrant\_client/embed/schema\_parser.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py)
- [qdrant\_client/embed/type\_inspector.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py)
- [tools/populate\_inspection\_cache.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tools/populate_inspection_cache.py)

The Type Inspector System is responsible for detecting objects requiring inference (embeddings) within Pydantic models used in the Qdrant client. It analyzes model schemas to identify paths to `Document`, `Image`, and `InferenceObject` types, enabling automatic embedding generation during data operations. The system includes schema parsing, type detection, and caching mechanisms to optimize performance.

For information about the actual embedding generation process, see [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md). For details about local inference model management, see [Local Inference](qdrant/qdrant-client/4.4-local-inference.md).

## Core Components

The Type Inspector System consists of three main components that work together to detect inference objects in Pydantic models:

```
```

**Sources:** [qdrant\_client/embed/type\_inspector.py12-23](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L12-L23) [qdrant\_client/embed/schema\_parser.py29-69](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L29-L69) [qdrant\_client/embed/embed\_inspector.py13-21](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embed_inspector.py#L13-L21)

## Schema Parsing System

The `ModelSchemaParser` class analyzes Pydantic model JSON schemas to identify paths to inference objects. It maintains internal state including definitions, recursive references, and cached paths:

```
```

**Sources:** [qdrant\_client/embed/schema\_parser.py238-287](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L238-L287) [qdrant\_client/embed/schema\_parser.py91-151](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L91-L151) [qdrant\_client/embed/schema\_parser.py153-236](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L153-L236)

## Type Detection Process

The `Inspector` class performs the actual detection of inference objects within model instances. It uses a recursive traversal approach to examine nested structures:

| Component                 | Purpose                                | Key Methods                               |
| ------------------------- | -------------------------------------- | ----------------------------------------- |
| `Inspector.inspect()`     | Main entry point for detection         | Returns `bool` if inference objects found |
| `_inspect_model()`        | Examine individual BaseModel instances | Checks against `INFERENCE_OBJECT_TYPES`   |
| `_inspect_inner_models()` | Traverse nested structures             | Handles lists, dicts, and nested models   |

```
```

**Sources:** [qdrant\_client/embed/type\_inspector.py24-50](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L24-L50) [qdrant\_client/embed/type\_inspector.py52-66](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L52-L66) [qdrant\_client/embed/type\_inspector.py68-149](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L68-L149)

## Caching and Performance Optimization

The system implements a comprehensive caching strategy to avoid repeated schema parsing and path computation:

### Cache Structure

| Cache Component   | Storage Format               | Purpose                               |
| ----------------- | ---------------------------- | ------------------------------------- |
| `_cache`          | `dict[str, list[str]]`       | String paths to inference objects     |
| `path_cache`      | `dict[str, list[FieldPath]]` | Structured path objects for traversal |
| `_defs`           | `dict[str, dict]`            | Schema definitions from `$defs`       |
| `_recursive_refs` | `set[str]`                   | Detected recursive references         |

### Cache Population

The inspection cache is pre-populated using the `populate_inspection_cache.py` tool, which processes all Pydantic models in the `qdrant_client.models` module:

```
```

**Sources:** [tools/populate\_inspection\_cache.py34-76](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tools/populate_inspection_cache.py#L34-L76) [qdrant\_client/embed/schema\_parser.py74-89](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L74-L89) [qdrant\_client/embed/schema\_parser.py289-305](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L289-L305)

## Pydantic Compatibility Layer

The system supports both Pydantic v1 and v2 through a compatibility layer that abstracts version-specific functionality:

| Function              | Pydantic v1            | Pydantic v2                 | Purpose                     |
| --------------------- | ---------------------- | --------------------------- | --------------------------- |
| `model_fields_set()`  | `model.__fields_set__` | `model.model_fields_set`    | Get set model fields        |
| `model_json_schema()` | `model.schema_json()`  | `model.model_json_schema()` | Extract JSON schema         |
| `model_fields()`      | `model.__fields__`     | `model.model_fields`        | Get model field definitions |

**Sources:** [qdrant\_client/\_pydantic\_compat.py44-62](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/_pydantic_compat.py#L44-L62) [qdrant\_client/embed/type\_inspector.py73](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L73-L73) [qdrant\_client/embed/schema\_parser.py254](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L254-L254)

## Integration with FastEmbed System

The Type Inspector System integrates with the FastEmbed system by providing two inspection modes:

### Detection Mode (`Inspector`)

Used to determine if any inference objects are present in a model, triggering embedding generation when needed.

### Collection Mode (`InspectorEmbed`)

Used to collect all paths to inference objects for batch processing and embedding replacement.

```
```

**Sources:** [qdrant\_client/embed/type\_inspector.py12-23](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L12-L23) [qdrant\_client/embed/embed\_inspector.py13-21](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embed_inspector.py#L13-L21) [qdrant\_client/embed/embed\_inspector.py23-47](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embed_inspector.py#L23-L47)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Type Inspector System](#type-inspector-system.md)
- [Core Components](#core-components.md)
- [Schema Parsing System](#schema-parsing-system.md)
- [Type Detection Process](#type-detection-process.md)
- [Caching and Performance Optimization](#caching-and-performance-optimization.md)
- [Cache Structure](#cache-structure.md)
- [Cache Population](#cache-population.md)
- [Pydantic Compatibility Layer](#pydantic-compatibility-layer.md)
- [Integration with FastEmbed System](#integration-with-fastembed-system.md)
- [Detection Mode (\`Inspector\`)](#detection-mode-inspector.md)
- [Collection Mode (\`InspectorEmbed\`)](#collection-mode-inspectorembed.md)
