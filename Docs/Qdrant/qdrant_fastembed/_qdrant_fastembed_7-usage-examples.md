Usage Examples | qdrant/fastembed | DeepWiki

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

# Usage Examples

Relevant source files

- [docs/Getting Started.ipynb](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb>)
- [docs/examples/ColBERT\_with\_FastEmbed.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb)
- [docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_vs_HF_Comparison.ipynb)
- [docs/examples/Hybrid\_Search.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb)
- [docs/index.md](https://github.com/qdrant/fastembed/blob/b785640b/docs/index.md)
- [docs/qdrant/Retrieval\_with\_FastEmbed.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/qdrant/Retrieval_with_FastEmbed.ipynb)

This page provides practical examples of using FastEmbed for various embedding tasks. It demonstrates how to generate and work with embeddings for different use cases including basic text embedding, sparse and hybrid search, late interaction models, and more. For installation and setup information, see [Installation and Setup](qdrant/fastembed/2-installation-and-setup.md).

## Basic Text Embedding

The most common use case for FastEmbed is generating dense text embeddings using the `TextEmbedding` class.

```
```

Each embedding is a numpy array with the default model's dimension (384 for BAAI/bge-small-en-v1.5):

```
```

### Using Different Models

FastEmbed supports various embedding models with different capabilities:

```
```

### Query vs Passage Embedding

For retrieval tasks, it's recommended to use specific embedding methods for queries and passages:

```
```

Sources: [docs/Getting Started.ipynb68-86](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb#L68-L86>) [docs/Getting Started.ipynb116-120](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb#L116-L120>) [docs/qdrant/Retrieval\_with\_FastEmbed.ipynb73-93](https://github.com/qdrant/fastembed/blob/b785640b/docs/qdrant/Retrieval_with_FastEmbed.ipynb#L73-L93) [docs/qdrant/Retrieval\_with\_FastEmbed.ipynb111-114](https://github.com/qdrant/fastembed/blob/b785640b/docs/qdrant/Retrieval_with_FastEmbed.ipynb#L111-L114)

## Sparse and Hybrid Search

FastEmbed supports sparse embeddings through the `SparseTextEmbedding` class, which is useful for hybrid search applications.

### Sparse Embedding Generation

```
```

Sparse embeddings contain indices and values, representing token positions and their weights:

```
```

### Hybrid Search with Qdrant

Combining dense and sparse embeddings enables hybrid search using Qdrant:

```
```

The hybrid search workflow:

```
```

Sources: [docs/examples/Hybrid\_Search.ipynb52-73](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb#L52-L73) [docs/examples/Hybrid\_Search.ipynb442-470](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb#L442-L470) [docs/examples/Hybrid\_Search.ipynb874-922](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb#L874-L922)

## ColBERT and Late Interaction Models

FastEmbed supports late interaction models through the `LateInteractionTextEmbedding` class, which enables more precise retrieval by preserving token-level interactions.

### Understanding Late Interaction

Late interaction models like ColBERT compute embeddings for each token in queries and documents, rather than pooling them into a single vector:

```
```

### Using ColBERT Model

```
```

### Maximal Similarity (MaxSim) Scoring

Late interaction models require a specific similarity computation called MaxSim:

```
```

The MaxSim operation workflow:

```
```

Sources: [docs/examples/ColBERT\_with\_FastEmbed.ipynb72-74](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb#L72-L74) [docs/examples/ColBERT\_with\_FastEmbed.ipynb168-205](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb#L168-L205) [docs/examples/ColBERT\_with\_FastEmbed.ipynb280-309](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb#L280-L309)

## Performance Comparison

FastEmbed is designed to be faster than traditional embedding libraries by utilizing ONNX Runtime for inference and optimized model implementations.

### Benchmarking with Hugging Face Transformers

The following benchmark compares FastEmbed with Hugging Face Transformers using the same model (BAAI/bge-small-en-v1.5):

```
```

A typical benchmark with a set of 12 documents shows FastEmbed is around 10-20% faster than Hugging Face Transformers:

| Framework       | Average (s) | Maximum (s) | Minimum (s) |
| --------------- | ----------- | ----------- | ----------- |
| HF Transformers | 0.047       | 0.066       | 0.043       |
| FastEmbed       | 0.044       | 0.057       | 0.043       |

For larger document sets, the performance gap increases due to FastEmbed's parallel processing capabilities.

### Parallelization Benefits

FastEmbed uses data parallelism to speed up embedding generation, significantly reducing processing time for large datasets. In testing with sparse embeddings, parallelization reduced processing time by approximately 50-60% on a multi-core system.

Sources: [docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb149-166](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_vs_HF_Comparison.ipynb#L149-L166) [docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb256-278](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_vs_HF_Comparison.ipynb#L256-L278)

## Integration with Qdrant

FastEmbed integrates seamlessly with Qdrant for vector search and retrieval:

```
```

The integration workflow:

```
```

Sources: [docs/index.md40-74](https://github.com/qdrant/fastembed/blob/b785640b/docs/index.md#L40-L74)

## Cross-Encoder Reranking

The `TextCrossEncoder` class can be used to rerank search results:

```
```

The reranking workflow:

```
```

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Usage Examples](#usage-examples.md)
- [Basic Text Embedding](#basic-text-embedding.md)
- [Using Different Models](#using-different-models.md)
- [Query vs Passage Embedding](#query-vs-passage-embedding.md)
- [Sparse and Hybrid Search](#sparse-and-hybrid-search.md)
- [Sparse Embedding Generation](#sparse-embedding-generation.md)
- [Hybrid Search with Qdrant](#hybrid-search-with-qdrant.md)
- [ColBERT and Late Interaction Models](#colbert-and-late-interaction-models.md)
- [Understanding Late Interaction](#understanding-late-interaction.md)
- [Using ColBERT Model](#using-colbert-model.md)
- [Maximal Similarity (MaxSim) Scoring](#maximal-similarity-maxsim-scoring.md)
- [Performance Comparison](#performance-comparison.md)
- [Benchmarking with Hugging Face Transformers](#benchmarking-with-hugging-face-transformers.md)
- [Parallelization Benefits](#parallelization-benefits.md)
- [Integration with Qdrant](#integration-with-qdrant.md)
- [Cross-Encoder Reranking](#cross-encoder-reranking.md)
