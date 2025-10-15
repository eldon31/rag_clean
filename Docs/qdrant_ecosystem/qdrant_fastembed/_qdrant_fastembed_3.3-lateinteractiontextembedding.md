LateInteractionTextEmbedding | qdrant/fastembed | DeepWiki

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

# LateInteractionTextEmbedding

Relevant source files

- [fastembed/late\_interaction/colbert.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py)
- [fastembed/late\_interaction/jina\_colbert.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py)
- [fastembed/late\_interaction/late\_interaction\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py)
- [fastembed/late\_interaction/late\_interaction\_text\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py)
- [fastembed/sparse/utils/tokenizer.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/utils/tokenizer.py)

## Purpose and Scope

The `LateInteractionTextEmbedding` class provides access to late-interaction embedding models in FastEmbed. Unlike traditional dense embeddings that aggregate text into a single vector, late-interaction models preserve token-level embeddings, enabling more precise matching between queries and documents. This page documents the implementation, architecture, and usage of `LateInteractionTextEmbedding` and its associated components.

For information about dense text embeddings (single vector representation), see [TextEmbedding](qdrant/fastembed/3.1-textembedding.md). For sparse text embeddings, see [SparseTextEmbedding](qdrant/fastembed/3.2-sparsetextembedding.md).

## Overview

Late-interaction models represent documents and queries as sequences of token-level embeddings rather than single vectors. These models defer the interaction between query and document tokens until retrieval time, allowing for more fine-grained matching that can capture local context more effectively than global embeddings.

```
```

Sources: [fastembed/late\_interaction/late\_interaction\_text\_embedding.py107-119](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py#L107-L119) [fastembed/late\_interaction/late\_interaction\_embedding\_base.py30-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py#L30-L60)

## Architecture

`LateInteractionTextEmbedding` serves as a facade over specific late-interaction model implementations, currently supporting ColBERT and Jina ColBERT models.

```
```

Sources: [fastembed/late\_interaction/late\_interaction\_text\_embedding.py14-15](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py#L14-L15) [fastembed/late\_interaction/late\_interaction\_embedding\_base.py8-9](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py#L8-L9) [fastembed/late\_interaction/colbert.py39](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L39) [fastembed/late\_interaction/jina\_colbert.py21](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L21-L21)

## Key Components

### LateInteractionTextEmbedding

The main entry point class that users interact with to access late-interaction embedding functionality. It:

- Provides a unified interface for various late-interaction model implementations
- Delegates embedding operations to the appropriate model implementation based on the model name
- Supports listing available models and their metadata

Sources: [fastembed/late\_interaction/late\_interaction\_text\_embedding.py14-120](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_text_embedding.py#L14-L120)

### LateInteractionTextEmbeddingBase

The abstract base class that defines the contract for late-interaction embedding implementations. It:

- Inherits from `ModelManagement` to handle model downloading and caching
- Defines abstract methods that implementations must provide (`embed`, `query_embed`)
- Provides a default implementation for `passage_embed` that routes to `embed`

Sources: [fastembed/late\_interaction/late\_interaction\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/late_interaction_embedding_base.py#L8-L60)

### Specific Model Implementations

#### Colbert

Implementation for the ColBERT late-interaction model. It:

- Handles tokenization and ONNX model loading
- Processes documents and queries differently (with different marker tokens)
- Performs token-level normalization for document embeddings
- Supports query augmentation with mask tokens

Sources: [fastembed/late\_interaction/colbert.py39-204](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L204)

#### JinaColbert

Extended implementation of ColBERT for Jina AI's variant. It:

- Uses different marker token IDs
- Applies special attention mask handling for queries
- Supports longer context lengths (up to 8192 tokens)

Sources: [fastembed/late\_interaction/jina\_colbert.py21-48](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L21-L48)

## Embedding Process

The late-interaction embedding process differs between queries and documents:

```
```

Sources: [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65) [fastembed/late\_interaction/colbert.py67-77](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L67-L77) [fastembed/late\_interaction/colbert.py79-104](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L79-L104)

## Supported Models

The `LateInteractionTextEmbedding` class currently supports the following models:

| Model Name                            | Dimension | Description                                                                                   | License      | Size (GB) |
| ------------------------------------- | --------- | --------------------------------------------------------------------------------------------- | ------------ | --------- |
| colbert-ir/colbertv2.0                | 128       | Late interaction model                                                                        | MIT          | 0.44      |
| answerdotai/answerai-colbert-small-v1 | 96        | Text embeddings, Unimodal (text), Multilingual (\~100 languages), 512 input tokens truncation | Apache-2.0   | 0.13      |
| jinaai/jina-colbert-v2                | 128       | Multilingual model with 8192 context length                                                   | cc-by-nc-4.0 | 2.24      |

Sources: [fastembed/late\_interaction/colbert.py17-36](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L17-L36) [fastembed/late\_interaction/jina\_colbert.py7-18](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L7-L18)

## Usage

### Basic Usage

```
```

### Advanced Usage with Parameters

```
```

## Implementation Details

### Special Token Handling

Late-interaction models like ColBERT use special marker tokens to differentiate between queries and documents:

| Model        | Query Marker Token ID | Document Marker Token ID | Mask Token |
| ------------ | --------------------- | ------------------------ | ---------- |
| ColBERT      | 1                     | 2                        | \[MASK]    |
| Jina ColBERT | 250002                | 250003                   | \<mask>    |

These markers are inserted at the beginning of the token sequence to inform the model about the input type.

Sources: [fastembed/late\_interaction/colbert.py40-43](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L40-L43) [fastembed/late\_interaction/jina\_colbert.py22-25](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/jina_colbert.py#L22-L25)

### Query Augmentation

For queries shorter than a minimum length (31 tokens for ColBERT), the implementation pads the query with mask tokens. This query augmentation technique improves retrieval performance by providing additional context signals.

Sources: [fastembed/late\_interaction/colbert.py86-104](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L86-L104)

### Token-level Normalization

For document embeddings, the implementation:

1. Applies the attention mask to zero out padding and punctuation tokens
2. Normalizes each token embedding to unit length (L2 normalization)

This ensures that similarity calculations during retrieval focus on meaningful tokens and are properly scaled.

Sources: [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65)

### Parallel Processing

For large-scale embedding tasks, the implementation supports parallel processing using worker processes, each with its own ONNX runtime session. This significantly improves throughput when processing large document collections.

Sources: [fastembed/late\_interaction/colbert.py211-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L211-L253) [fastembed/late\_interaction/colbert.py256-263](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L256-L263)

## Performance Considerations

- Late-interaction models produce token-level embeddings, resulting in larger storage requirements compared to dense embeddings
- The fine-grained matching requires specialized retrieval algorithms (not covered by this class, which handles only the embedding generation)
- Setting appropriate batch sizes and enabling parallel processing can significantly improve throughput for large document collections

## Related Components

For more information about other embedding approaches in FastEmbed:

- [TextEmbedding](qdrant/fastembed/3.1-textembedding.md) - Dense text embeddings
- [SparseTextEmbedding](qdrant/fastembed/3.2-sparsetextembedding.md) - Sparse text embeddings
- [LateInteractionMultimodalEmbedding](qdrant/fastembed/3.5-lateinteractionmultimodalembedding.md) - Late interaction for text and images

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [LateInteractionTextEmbedding](#lateinteractiontextembedding.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Architecture](#architecture.md)
- [Key Components](#key-components.md)
- [LateInteractionTextEmbedding](#lateinteractiontextembedding-1.md)
- [LateInteractionTextEmbeddingBase](#lateinteractiontextembeddingbase.md)
- [Specific Model Implementations](#specific-model-implementations.md)
- [Colbert](#colbert.md)
- [JinaColbert](#jinacolbert.md)
- [Embedding Process](#embedding-process.md)
- [Supported Models](#supported-models.md)
- [Usage](#usage.md)
- [Basic Usage](#basic-usage.md)
- [Advanced Usage with Parameters](#advanced-usage-with-parameters.md)
- [Implementation Details](#implementation-details.md)
- [Special Token Handling](#special-token-handling.md)
- [Query Augmentation](#query-augmentation.md)
- [Token-level Normalization](#token-level-normalization.md)
- [Parallel Processing](#parallel-processing.md)
- [Performance Considerations](#performance-considerations.md)
- [Related Components](#related-components.md)
