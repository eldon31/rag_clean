TextEmbedding | qdrant/fastembed | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/fastembed](https://github.com/qdrant/fastembed "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 20 April 2025 ([b78564](https://github.com/qdrant/fastembed/commits/b785640b))

- [Overview](qdrant/fastembed/1-overview.md)
- [Installation and Setup](qdrant/fastembed/2-installation-and-setup.md)
- [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md)
- [TextEmbedding](qdrant/fastembed/3.1-textembedding.md)
- [SparseTextEmbedding](qdrant/fastembed/3.2-sparsetextembedding.md)
- [LateInteractionTextEmbedding](qdrant/fastembed/3.3-lateinteractiontextembedding.md)
- [ImageEmbedding](qdrant/fastembed/3.4-imageembedding.md)
- [LateInteractionMultimodalEmbedding](qdrant/fastembed/3.5-lateinteractionmultimodalembedding.md)
- [TextCrossEncoder](qdrant/fastembed/3.6-textcrossencoder.md)
- [Architecture](qdrant/fastembed/4-architecture.md)
- [Model Management](qdrant/fastembed/4.1-model-management.md)
- [ONNX Runtime Integration](qdrant/fastembed/4.2-onnx-runtime-integration.md)
- [Parallel Processing](qdrant/fastembed/4.3-parallel-processing.md)
- [Implementation Details](qdrant/fastembed/5-implementation-details.md)
- [Dense Text Embeddings](qdrant/fastembed/5.1-dense-text-embeddings.md)
- [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md)
- [Late Interaction Models](qdrant/fastembed/5.3-late-interaction-models.md)
- [Multimodal Models](qdrant/fastembed/5.4-multimodal-models.md)
- [Supported Models](qdrant/fastembed/6-supported-models.md)
- [Usage Examples](qdrant/fastembed/7-usage-examples.md)
- [Basic Text Embedding](qdrant/fastembed/7.1-basic-text-embedding.md)
- [Sparse and Hybrid Search](qdrant/fastembed/7.2-sparse-and-hybrid-search.md)
- [ColBERT and Late Interaction](qdrant/fastembed/7.3-colbert-and-late-interaction.md)
- [Image Embedding](qdrant/fastembed/7.4-image-embedding.md)
- [Performance Optimization](qdrant/fastembed/8-performance-optimization.md)
- [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md)
- [Development Guide](qdrant/fastembed/10-development-guide.md)

Menu

# TextEmbedding

Relevant source files

- [docs/Getting Started.ipynb](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb>)
- [docs/index.md](https://github.com/qdrant/fastembed/blob/b785640b/docs/index.md)
- [fastembed/embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/embedding.py)
- [fastembed/text/text\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py)
- [tests/test\_text\_onnx\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_text_onnx_embeddings.py)

The `TextEmbedding` class is the primary entry point for generating dense vector representations (embeddings) from text in the FastEmbed library. It provides a unified interface to multiple underlying embedding implementations while maintaining high performance through ONNX Runtime integration.

For sparse text embeddings, see [SparseTextEmbedding](qdrant/fastembed/3.2-sparsetextembedding.md), and for late interaction models, see [LateInteractionTextEmbedding](qdrant/fastembed/3.3-lateinteractiontextembedding.md).

## Class Architecture

```
```

Sources: [fastembed/text/text\_embedding.py16-25](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L16-L25) [fastembed/text/text\_embedding.py79-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L79-L130)

## Initialization and Configuration

The `TextEmbedding` class can be initialized with various parameters to control model selection and runtime behavior:

```
```

Key initialization parameters:

| Parameter    | Type                               | Default                  | Description                                |
| ------------ | ---------------------------------- | ------------------------ | ------------------------------------------ |
| `model_name` | str                                | "BAAI/bge-small-en-v1.5" | Model identifier                           |
| `cache_dir`  | Optional\[str]                     | None                     | Directory to store downloaded models       |
| `threads`    | Optional\[int]                     | None                     | Number of threads for ONNX Runtime         |
| `providers`  | Optional\[Sequence\[OnnxProvider]] | None                     | ONNX Runtime providers                     |
| `cuda`       | bool                               | False                    | Whether to use CUDA for acceleration       |
| `device_ids` | Optional\[list\[int]]              | None                     | CUDA device IDs to use                     |
| `lazy_load`  | bool                               | False                    | Whether to load the model only when needed |

Sources: [fastembed/text/text\_embedding.py79-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L79-L130) [docs/Getting Started.ipynb68-86](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb#L68-L86>)

## Embedding Generation Process

```
```

Sources: [fastembed/text/text\_embedding.py111-126](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L111-L126) [fastembed/text/text\_embedding.py131-153](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L131-L153)

## Core Methods

### Embedding Documents

The primary method for generating embeddings is `embed()`, which accepts documents and returns an iterator of embedding vectors:

```
```

The method signature is:

```
```

Parameters:

- `documents`: A single text document or an iterable of documents
- `batch_size`: Number of documents to process at once (default: 256)
- `parallel`: Number of parallel processes to use (if > 0)

Sources: [fastembed/text/text\_embedding.py131-153](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L131-L153) [docs/Getting Started.ipynb116-121](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb#L116-L121>)

### Query and Passage Embedding

For retrieval tasks, `TextEmbedding` provides specialized methods for queries and passages:

```
```

These methods are particularly useful for models that have different embedding strategies for queries versus passages.

Sources: [fastembed/text/text\_embedding.py155-180](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L155-L180) [docs/index.md27-36](https://github.com/qdrant/fastembed/blob/b785640b/docs/index.md#L27-L36)

### Model Management

The `TextEmbedding` class provides methods to list supported models and add custom models:

```
```

Sources: [fastembed/text/text\_embedding.py26-77](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding.py#L26-L77)

## Advanced Usage Patterns

### Batch Processing

For large datasets, you can process documents in batches to conserve memory:

```
```

### Parallel Processing

To speed up embedding generation, you can use parallel processing:

```
```

Sources: [tests/test\_text\_onnx\_embeddings.py119-139](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_text_onnx_embeddings.py#L119-L139)

### Lazy Loading

To conserve memory when working with multiple models, you can use lazy loading, which only loads the model when it's first used:

```
```

Sources: [tests/test\_text\_onnx\_embeddings.py142-158](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_text_onnx_embeddings.py#L142-L158)

## Supported Models

`TextEmbedding` supports a wide range of models, including:

| Model Category        | Examples                                                                                            |
| --------------------- | --------------------------------------------------------------------------------------------------- |
| BGE Embeddings        | BAAI/bge-small-en-v1.5, BAAI/bge-base-en, BAAI/bge-large-en-v1.5                                    |
| Sentence Transformers | sentence-transformers/all-MiniLM-L6-v2, sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
| Jina AI Models        | jinaai/jina-embeddings-v2-base-en, jinaai/jina-embeddings-v3                                        |
| Nomic AI Models       | nomic-ai/nomic-embed-text-v1, nomic-ai/nomic-embed-text-v1.5                                        |
| Others                | thenlper/gte-large, mixedbread-ai/mxbai-embed-large-v1, snowflake/snowflake-arctic-embed models     |

Each model produces embeddings of different dimensions and with different characteristics. The default model (BAAI/bge-small-en-v1.5) produces 384-dimensional vectors.

Sources: [tests/test\_text\_onnx\_embeddings.py10-70](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_text_onnx_embeddings.py#L10-L70) [docs/Getting Started.ipynb150-162](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb#L150-L162>)

## Integration with Vector Databases

`TextEmbedding` is designed to work seamlessly with vector databases like Qdrant. For detailed examples, see [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md).

```
```

Sources: [docs/index.md39-75](https://github.com/qdrant/fastembed/blob/b785640b/docs/index.md#L39-L75)

## Performance Considerations

The `TextEmbedding` class is designed for high performance through:

1. **ONNX Runtime**: All models are converted to ONNX format for efficient inference
2. **Batch Processing**: Documents are processed in batches for memory efficiency
3. **Parallel Processing**: Multiple CPU cores can be used for faster processing
4. **Lazy Loading**: Models are loaded only when needed
5. **Model Quantization**: Some models have quantized versions for faster inference

For more details on optimizing performance, see [Performance Optimization](qdrant/fastembed/8-performance-optimization.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [TextEmbedding](#textembedding.md)
- [Class Architecture](#class-architecture.md)
- [Initialization and Configuration](#initialization-and-configuration.md)
- [Embedding Generation Process](#embedding-generation-process.md)
- [Core Methods](#core-methods.md)
- [Embedding Documents](#embedding-documents.md)
- [Query and Passage Embedding](#query-and-passage-embedding.md)
- [Model Management](#model-management.md)
- [Advanced Usage Patterns](#advanced-usage-patterns.md)
- [Batch Processing](#batch-processing.md)
- [Parallel Processing](#parallel-processing.md)
- [Lazy Loading](#lazy-loading.md)
- [Supported Models](#supported-models.md)
- [Integration with Vector Databases](#integration-with-vector-databases.md)
- [Performance Considerations](#performance-considerations.md)
