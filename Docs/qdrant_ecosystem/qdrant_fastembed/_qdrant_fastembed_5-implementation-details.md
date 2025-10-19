Implementation Details | qdrant/fastembed | DeepWiki

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

# Implementation Details

Relevant source files

- [fastembed/late\_interaction/colbert.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py)
- [fastembed/sparse/sparse\_text\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py)
- [fastembed/sparse/splade\_pp.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py)
- [fastembed/text/clip\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py)
- [fastembed/text/pooled\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py)
- [fastembed/text/pooled\_normalized\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py)

This page provides an in-depth examination of how FastEmbed implements various embedding models. We focus on the core implementation approaches for dense, sparse, and late interaction embedding models. For high-level architecture information, see [Architecture](qdrant/fastembed/4-architecture.md), and for detailed model support, see [Supported Models](qdrant/fastembed/6-supported-models.md).

## Implementation Architecture Overview

FastEmbed uses a consistent implementation pattern across all embedding types, with specialized classes extending base classes that provide common functionality. The implementation is designed around ONNX Runtime for optimized inference.

```
```

Sources: [fastembed/text/pooled\_embedding.py93-120](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L93-L120) [fastembed/text/pooled\_normalized\_embedding.py127-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L127-L147) [fastembed/text/clip\_embedding.py24-39](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py#L24-L39) [fastembed/sparse/splade\_pp.py36-52](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L36-L52) [fastembed/late\_interaction/colbert.py39-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L65)

## Embedding Processing Flow

All embedding types follow a general embedding process flow, with variations in their pre-processing and post-processing steps:

```
```

Sources: [fastembed/text/pooled\_embedding.py113-119](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L113-L119) [fastembed/text/pooled\_normalized\_embedding.py141-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L141-L147) [fastembed/sparse/splade\_pp.py37-52](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L37-L52) [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65)

## Dense Text Embeddings

FastEmbed implements two primary dense text embedding approaches:

### Pooled Embedding

The `PooledEmbedding` class provides basic mean pooling over token embeddings:

1. Tokenize input text and create attention masks
2. Run ONNX model to get token-level embeddings
3. Apply mean pooling, weighted by attention mask

The core implementation centers around the mean pooling operation:

```
```

Sources: [fastembed/text/pooled\_embedding.py93-119](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L93-L119)

### Pooled Normalized Embedding

The `PooledNormalizedEmbedding` class extends `PooledEmbedding` with an additional normalization step:

1. Perform mean pooling as in the base class
2. Apply L2 normalization to the resulting embeddings

This implementation is particularly useful for models where cosine similarity is the preferred distance metric.

Sources: [fastembed/text/pooled\_normalized\_embedding.py127-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L127-L147)

## Sparse Text Embeddings

### SPLADE++ Implementation

The `SpladePP` class implements the SPLADE++ algorithm for sparse embeddings:

1. Tokenize input text and run ONNX model
2. Apply ReLU and log transformation to output scores
3. Apply attention mask to handle variable-length inputs
4. Take maximum value for each vocabulary term across all tokens
5. Extract non-zero values and indices as sparse embedding

```
```

The resulting sparse embeddings contain only non-zero values and their corresponding indices, significantly reducing memory requirements.

Sources: [fastembed/sparse/splade\_pp.py37-52](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L37-L52)

## Late Interaction Models

### ColBERT Implementation

The `Colbert` class implements the ColBERT late interaction approach:

1. Different processing for queries and documents:

   - For queries: Insert a query marker token and pad with mask tokens
   - For documents: Insert a document marker token

2. For document embeddings:

   - Apply attention mask
   - Zero out punctuation token embeddings
   - Normalize token embeddings to unit length

```
```

The ColBERT implementation includes several specialized components:

- Special marker tokens for queries (ID=1) and documents (ID=2)
- Query augmentation with mask tokens to a minimum length
- Excluding punctuation tokens from document embeddings
- L2 normalization of per-token embeddings

Sources: [fastembed/late\_interaction/colbert.py39-204](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L204)

## Implementation Optimizations

### ONNX Runtime Integration

All embeddings in FastEmbed leverage ONNX Runtime for optimized inference:

- Models are exported and optimized for the ONNX format
- Support for CPU and GPU acceleration
- Optimized operator fusion and graph optimization

### Parallel Processing

FastEmbed implements efficient parallel processing:

- Worker processes handle subsets of data in parallel
- Each implementation has its worker class (e.g., `PooledEmbeddingWorker`, `SpladePPEmbeddingWorker`, `ColbertEmbeddingWorker`)
- Workers can be distributed across multiple GPUs

```
```

Sources: [fastembed/text/pooled\_embedding.py122-134](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L122-L134) [fastembed/sparse/splade\_pp.py169-181](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L169-L181) [fastembed/late\_interaction/colbert.py252-263](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L252-L263)

### Lazy Loading

Models can be lazily loaded to optimize resource usage:

1. Models are only loaded when needed for inference
2. Particularly useful in multi-GPU setups where each worker loads its own model copy
3. Controlled via the `lazy_load` parameter in model constructors

This optimization is implemented across all embedding classes through a common pattern:

```
```

Sources: [fastembed/text/pooled\_embedding.py122-134](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L122-L134) [fastembed/sparse/splade\_pp.py122-133](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L122-L133) [fastembed/late\_interaction/colbert.py183-204](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L183-L204)

## Model Registration System

FastEmbed uses a registry system to maintain lists of supported models for each embedding type:

```
```

Each embedding type registers supported models in class variables, along with model metadata such as:

- Embedding dimension
- Model description
- License information
- Model size
- Source locations

Sources: [fastembed/sparse/sparse\_text\_embedding.py16-68](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L16-L68) [fastembed/sparse/splade\_pp.py14-33](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L14-L33) [fastembed/text/pooled\_embedding.py12-90](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L12-L90) [fastembed/text/pooled\_normalized\_embedding.py11-124](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L11-L124) [fastembed/late\_interaction/colbert.py17-36](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L17-L36)

## Conclusion

FastEmbed's implementation details showcase a well-designed architecture that balances flexibility, performance, and ease of use. The library provides specialized implementations for different embedding types while maintaining consistent interfaces and optimizations across the board. The use of ONNX Runtime, parallel processing, and other performance optimizations enables FastEmbed to deliver high-performance embedding generation for various applications.

For specific model support information, see [Supported Models](qdrant/fastembed/6-supported-models.md), and for usage examples, see [Usage Examples](qdrant/fastembed/7-usage-examples.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Implementation Details](#implementation-details.md)
- [Implementation Architecture Overview](#implementation-architecture-overview.md)
- [Embedding Processing Flow](#embedding-processing-flow.md)
- [Dense Text Embeddings](#dense-text-embeddings.md)
- [Pooled Embedding](#pooled-embedding.md)
- [Pooled Normalized Embedding](#pooled-normalized-embedding.md)
- [Sparse Text Embeddings](#sparse-text-embeddings.md)
- [SPLADE++ Implementation](#splade-implementation.md)
- [Late Interaction Models](#late-interaction-models.md)
- [ColBERT Implementation](#colbert-implementation.md)
- [Implementation Optimizations](#implementation-optimizations.md)
- [ONNX Runtime Integration](#onnx-runtime-integration.md)
- [Parallel Processing](#parallel-processing.md)
- [Lazy Loading](#lazy-loading.md)
- [Model Registration System](#model-registration-system.md)
- [Conclusion](#conclusion.md)
