Late Interaction Models | qdrant/fastembed | DeepWiki

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

# Late Interaction Models

Relevant source files

- [fastembed/late\_interaction/colbert.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py)
- [fastembed/late\_interaction/jina\_colbert.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py)
- [fastembed/late\_interaction/late\_interaction\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py)
- [fastembed/late\_interaction/late\_interaction\_text\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py)
- [fastembed/sparse/utils/tokenizer.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/utils/tokenizer.py)

This page documents the Late Interaction Models in FastEmbed, which provide a specialized approach to text embeddings that differs from the standard dense embedding methods covered in [Dense Text Embeddings](qdrant/fastembed/5.1-dense-text-embeddings.md) and sparse embeddings described in [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md).

Late interaction models generate token-level embeddings rather than a single vector per document, preserving word-level semantics for more precise matching during retrieval. This approach enables a finer-grained comparison between queries and documents at search time.

## Overview of Late Interaction Models

Late interaction models, like ColBERT, create separate embeddings for each token in a document or query rather than pooling them into a single vector. This approach allows the model to perform "late interaction" - comparing query and document token embeddings at retrieval time rather than comparing single document/query vectors.

```
```

Sources: [fastembed/late\_interaction/late\_interaction\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py#L8-L60) [fastembed/late\_interaction/colbert.py39-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L65)

## Architecture

The late interaction models in FastEmbed are organized in a hierarchical structure:

```
```

Sources: [fastembed/late\_interaction/late\_interaction\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py#L8-L60) [fastembed/late\_interaction/late\_interaction\_text\_embedding.py14-119](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py#L14-L119) [fastembed/late\_interaction/colbert.py39-255](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L255) [fastembed/late\_interaction/jina\_colbert.py21-58](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L21-L58)

The main classes are:

1. **LateInteractionTextEmbeddingBase**: The abstract base class that defines the interface for late interaction models.
2. **LateInteractionTextEmbedding**: A facade class that selects the appropriate implementation based on the model name.
3. **Colbert**: Implementation of the ColBERT model.
4. **JinaColbert**: Extension of the ColBERT model with Jina-specific enhancements.

## Supported Models

FastEmbed supports the following late interaction models:

| Model                                 | Dimension | Description                                                                                   | License      | Size (GB) |
| ------------------------------------- | --------- | --------------------------------------------------------------------------------------------- | ------------ | --------- |
| colbert-ir/colbertv2.0                | 128       | Late interaction model                                                                        | MIT          | 0.44      |
| answerdotai/answerai-colbert-small-v1 | 96        | Text embeddings, Unimodal (text), Multilingual (\~100 languages), 512 input tokens truncation | Apache-2.0   | 0.13      |
| jinaai/jina-colbert-v2                | 128       | Multilingual model with context length of 8192                                                | CC-BY-NC-4.0 | 2.24      |

Sources: [fastembed/late\_interaction/colbert.py17-36](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L17-L36) [fastembed/late\_interaction/jina\_colbert.py7-18](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L7-L18)

## Implementation Details

### ColBERT Processing Flow

The ColBERT and JinaColBERT models implement a specific processing flow for queries and documents:

```
```

Sources: [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65) [fastembed/late\_interaction/colbert.py67-77](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L67-L77) [fastembed/late\_interaction/colbert.py79-108](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L79-L108)

### Key Implementation Features

1. **Different Marker Tokens for Queries and Documents**:

   - Colbert uses `QUERY_MARKER_TOKEN_ID = 1` for queries and `DOCUMENT_MARKER_TOKEN_ID = 2` for documents
   - JinaColbert uses `QUERY_MARKER_TOKEN_ID = 250002` for queries and `DOCUMENT_MARKER_TOKEN_ID = 250003` for documents

2. **Query Augmentation**:

   - Queries are padded with mask tokens to a minimum length (`MIN_QUERY_LENGTH = 31`) to improve performance

3. **Document Token Processing**:

   - Punctuation tokens are masked out (`skip_list`)
   - Remaining token embeddings are L2-normalized

4. **Worker Classes for Parallel Processing**:

   - `ColbertEmbeddingWorker` and `JinaColbertEmbeddingWorker` enable parallel embedding generation

Sources: [fastembed/late\_interaction/colbert.py39-44](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L44) [fastembed/late\_interaction/jina\_colbert.py22-25](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L22-L25) [fastembed/late\_interaction/colbert.py86-104](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L86-L104) [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65) [fastembed/late\_interaction/colbert.py256-263](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L256-L263)

## Usage Example

The late interaction models can be used through the `LateInteractionTextEmbedding` class. The key difference from regular embedding models is the separate methods for query and document embedding:

```
```

The model provides:

1. **embed()** - For embedding documents
2. **query\_embed()** - For embedding queries
3. **passage\_embed()** - Alternative name for embed() to maintain API consistency

Sources: [fastembed/late\_interaction/late\_interaction\_text\_embedding.py83-119](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py#L83-L119) [fastembed/late\_interaction/late\_interaction\_embedding\_base.py21-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py#L21-L60)

## Implementation Details: Colbert Class

The `Colbert` class is the central implementation of the ColBERT model in FastEmbed:

```
```

Sources: [fastembed/late\_interaction/colbert.py39-255](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L255) [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65) [fastembed/late\_interaction/colbert.py67-77](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L67-L77) [fastembed/late\_interaction/colbert.py79-108](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L79-L108) [fastembed/late\_interaction/colbert.py239-249](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L239-L249)

Key methods in the `Colbert` class:

1. **\_post\_process\_onnx\_output()**: Different processing for documents (with masking and normalization) and queries
2. **\_preprocess\_onnx\_input()**: Adds marker tokens based on whether the input is a document or query
3. **tokenize()**: Handles tokenization differently for documents and queries
4. **\_tokenize\_query()**: Pads shorter queries with mask tokens for query augmentation
5. **load\_onnx\_model()**: Initializes the ONNX model and sets up tokenization parameters
6. **embed()** and **query\_embed()**: Public interface methods for embedding documents and queries

## JinaColbert Extensions

`JinaColbert` extends the base `Colbert` class with specific enhancements:

1. Different special token IDs:

   - `QUERY_MARKER_TOKEN_ID = 250002`
   - `DOCUMENT_MARKER_TOKEN_ID = 250003`
   - `MASK_TOKEN = "<mask>"` (vs. "\[MASK]" in Colbert)

2. Modified preprocessing for queries:

   - Sets all attention mask values to 1 for queries

3. Support for longer contexts:

   - Context length up to 8192 tokens (vs. the standard 512)

4. Multilingual capabilities:

   - Support for multiple languages vs. primarily English in the original ColBERT

Sources: [fastembed/late\_interaction/jina\_colbert.py21-48](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L21-L48)

## Parallel Processing Support

Late interaction models in FastEmbed support parallel processing for efficient embedding generation:

```
```

Sources: [fastembed/late\_interaction/colbert.py211-237](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L211-L237) [fastembed/late\_interaction/colbert.py256-263](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L256-L263) [fastembed/late\_interaction/jina\_colbert.py51-58](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L51-L58)

The worker classes (`ColbertEmbeddingWorker` and `JinaColbertEmbeddingWorker`) handle embedding generation in separate processes, allowing for efficient utilization of multiple CPU cores or GPUs.

## Conclusion

Late interaction models in FastEmbed provide a powerful alternative to traditional dense embeddings. By generating token-level representations and postponing the interaction between query and document until search time, these models enable more precise matching and retrieval.

The implementation in FastEmbed offers efficient processing through ONNX runtime integration and parallel processing capabilities, making it suitable for production environments where performance is critical.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Late Interaction Models](#late-interaction-models.md)
- [Overview of Late Interaction Models](#overview-of-late-interaction-models.md)
- [Architecture](#architecture.md)
- [Supported Models](#supported-models.md)
- [Implementation Details](#implementation-details.md)
- [ColBERT Processing Flow](#colbert-processing-flow.md)
- [Key Implementation Features](#key-implementation-features.md)
- [Usage Example](#usage-example.md)
- [Implementation Details: Colbert Class](#implementation-details-colbert-class.md)
- [JinaColbert Extensions](#jinacolbert-extensions.md)
- [Parallel Processing Support](#parallel-processing-support.md)
- [Conclusion](#conclusion.md)
