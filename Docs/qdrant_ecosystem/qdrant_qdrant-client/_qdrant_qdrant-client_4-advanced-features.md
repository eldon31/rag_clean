Advanced Features | qdrant/qdrant-client | DeepWiki

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

# Advanced Features

Relevant source files

- [qdrant\_client/async\_qdrant\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py)
- [qdrant\_client/qdrant\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py)
- [tests/test\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_fastembed.py)
- [tools/async\_client\_generator/fastembed\_generator.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tools/async_client_generator/fastembed_generator.py)

This document covers the advanced functionality of the qdrant-client Python library, including embedding integration, batch processing, and specialized search capabilities. These features extend the basic client operations to provide higher-level abstractions for common vector database workflows.

For basic client operations and collection management, see [Core Operations](qdrant/qdrant-client/3-core-operations.md). For implementation details of filtering and type inspection systems, see [Implementation Details](qdrant/qdrant-client/5-implementation-details.md).

## FastEmbed Integration

The qdrant-client provides seamless integration with FastEmbed for automatic text and image embedding generation through the `QdrantFastembedMixin` and `AsyncQdrantFastembedMixin` classes.

```
```

The `QdrantFastembedMixin` class provides several key methods for model management:

| Method                 | Purpose                          | Returns                           |
| ---------------------- | -------------------------------- | --------------------------------- |
| `set_model()`          | Configure dense embedding model  | None                              |
| `set_sparse_model()`   | Configure sparse embedding model | None                              |
| `list_text_models()`   | List available text models       | `dict[str, tuple[int, Distance]]` |
| `list_sparse_models()` | List available sparse models     | `dict[str, dict[str, Any]]`       |
| `get_embedding_size()` | Get model embedding dimensions   | `int`                             |

The embedding models are managed through the `ModelEmbedder` class, which handles both dense and sparse embeddings. The default dense model is `BAAI/bge-small-en`, as defined in the `DEFAULT_EMBEDDING_MODEL` constant.

**Sources:** [qdrant\_client/qdrant\_fastembed.py31-157](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L31-L157) [qdrant\_client/async\_qdrant\_fastembed.py37-212](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py#L37-L212)

## Batch Operations

The client provides efficient batch processing capabilities for high-volume data ingestion through the `add()` method and underlying batch uploaders.

```
```

The batch processing system handles several key operations:

1. **Document Embedding**: The `_embed_documents()` method processes documents in batches using the configured embedding model
2. **Sparse Embedding**: The `_sparse_embed_documents()` method generates sparse vectors for hybrid search
3. **Point Construction**: The `_points_iterator()` method combines embeddings with metadata to create `PointStruct` objects
4. **Parallel Upload**: The `upload_points()` method handles efficient batch upload with configurable parallelism

Key parameters for batch operations:

| Parameter            | Default | Purpose                          |
| -------------------- | ------- | -------------------------------- |
| `batch_size`         | 32      | Documents per batch              |
| `parallel`           | None    | Parallel workers for embedding   |
| `DEFAULT_BATCH_SIZE` | 8       | Default batch size for embedding |

**Sources:** [qdrant\_client/qdrant\_fastembed.py518-610](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L518-L610) [qdrant\_client/qdrant\_fastembed.py270-318](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L270-L318)

## Hybrid Search

The client supports hybrid search combining dense and sparse vectors through reciprocal rank fusion (RRF). This is implemented in the `query()` and `query_batch()` methods.

```
```

The hybrid search process involves:

1. **Dual Embedding**: Query text is embedded using both dense and sparse models
2. **Parallel Search**: Both dense and sparse searches are executed via `search_batch()`
3. **Result Fusion**: Results are combined using `reciprocal_rank_fusion()` from the `qdrant_client.hybrid.fusion` module
4. **Response Formatting**: Results are converted to `QueryResponse` objects

Vector field naming follows a consistent pattern:

- Dense vectors: `"fast-{model_name}"` (e.g., `"fast-bge-small-en"`)
- Sparse vectors: `"fast-sparse-{model_name}"` (e.g., `"fast-sparse-splade_pp_en_v1"`)

**Sources:** [qdrant\_client/qdrant\_fastembed.py612-696](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L612-L696) [qdrant\_client/qdrant\_fastembed.py18](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L18-L18)

## Local Inference

The client provides local inference capabilities through the `ModelEmbedder` class and related inference object detection systems.

```
```

The local inference system provides several key capabilities:

1. **Query Resolution**: The `_resolve_query()` method handles various query types including inference objects
2. **Model Embedding**: The `_embed_models()` and `_embed_models_strict()` methods process Pydantic models with embedded inference objects
3. **Type Detection**: The system uses `INFERENCE_OBJECT_TYPES` to identify objects requiring inference
4. **Schema Parsing**: The `ModelSchemaParser` analyzes model schemas to identify inference fields

Supported inference object types include:

- `models.Document` - Text documents for embedding
- `models.Image` - Images for vision model embedding
- `models.InferenceObject` - Generic inference objects

The system integrates with both synchronous and asynchronous workflows, with the `AsyncQdrantFastembedMixin` providing the same interface for async operations.

**Sources:** [qdrant\_client/qdrant\_fastembed.py789-892](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L789-L892) [qdrant\_client/qdrant\_fastembed.py16](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L16-L16) [qdrant\_client/qdrant\_fastembed.py36-40](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L36-L40)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Advanced Features](#advanced-features.md)
- [FastEmbed Integration](#fastembed-integration.md)
- [Batch Operations](#batch-operations.md)
- [Hybrid Search](#hybrid-search.md)
- [Local Inference](#local-inference.md)
