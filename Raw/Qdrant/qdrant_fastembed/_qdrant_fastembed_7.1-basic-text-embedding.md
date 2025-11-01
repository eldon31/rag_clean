Basic Text Embedding | qdrant/fastembed | DeepWiki

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

# Basic Text Embedding

Relevant source files

- [docs/Getting Started.ipynb](<https://github.com/qdrant/fastembed/blob/b785640b/docs/Getting Started.ipynb>)
- [docs/examples/ColBERT\_with\_FastEmbed.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb)
- [docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_vs_HF_Comparison.ipynb)
- [docs/examples/Hybrid\_Search.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb)
- [docs/index.md](https://github.com/qdrant/fastembed/blob/b785640b/docs/index.md)
- [docs/qdrant/Retrieval\_with\_FastEmbed.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/qdrant/Retrieval_with_FastEmbed.ipynb)

This page covers the fundamentals of text embedding using FastEmbed's `TextEmbedding` class. Text embedding is the process of converting text into numerical vector representations that capture semantic meaning, enabling computers to understand and compare text documents mathematically.

For sparse embedding techniques, see [Sparse and Hybrid Search](qdrant/fastembed/7.2-sparse-and-hybrid-search.md), and for late interaction embedding models, see [ColBERT and Late Interaction](qdrant/fastembed/7.3-colbert-and-late-interaction.md).

## TextEmbedding Class Overview

The `TextEmbedding` class serves as the primary entry point for dense text embedding operations in FastEmbed. It provides a simple, high-performance interface to generate vector representations from text documents.

```
```

Sources: docs/Getting Started.ipynb, docs/index.md

## Initialization and Basic Usage

### Initializing TextEmbedding

You can initialize the `TextEmbedding` class with either default settings or custom model parameters:

```
```

The initialization process requires minimal code:

```
```

Sources: docs/Getting Started.ipynb:68-80, docs/Getting Started.ipynb:185-187

### Generating Embeddings

Once initialized, you can generate embeddings for a list of text documents:

```
```

The following example demonstrates basic embedding generation:

```
```

Sources: docs/Getting Started.ipynb:68-86, docs/Getting Started.ipynb:116-120

## Understanding Embedding Output

The embeddings produced by `TextEmbedding` are NumPy arrays with dimensions determined by the model used. For example:

| Model                          | Embedding Dimension |
| ------------------------------ | ------------------- |
| BAAI/bge-small-en-v1.5         | 384                 |
| BAAI/bge-large-en-v1.5         | 1024                |
| intfloat/multilingual-e5-large | 1024                |

You can process the embeddings in various ways:

```
```

Sources: docs/Getting Started.ipynb:98-120, docs/Getting Started.ipynb:140-143

## Advanced Features

### Query vs. Passage Embeddings

FastEmbed distinguishes between query and passage embeddings to improve search relevance:

```
```

Using specialized methods for queries and documents significantly improves retrieval performance:

```
```

Sources: docs/qdrant/Retrieval\_with\_FastEmbed.ipynb:88-90, docs/qdrant/Retrieval\_with\_FastEmbed.ipynb:112, docs/Getting Started.ipynb:152-159

### Format for Document Prefixes

When performing retrieval tasks with the default model, you can add special prefixes to improve performance:

- **Queries**: Add "query:" at the beginning of each query string
- **Passages**: Add "passage:" at the beginning of each passage string

This is handled automatically by the `query_embed()` and `passage_embed()` methods, but can also be added manually when using the general `embed()` method.

Sources: docs/Getting Started.ipynb:152-159

### Parallel Processing

FastEmbed automatically leverages parallel processing for efficiency:

```
```

This parallel processing significantly reduces the time needed to generate embeddings for large datasets, providing much better performance compared to traditional embedding libraries.

Sources: docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb:252-278

### Supported Models

TextEmbedding supports various pre-trained models that can be specified during initialization:

```
```

Some commonly used models include:

- BAAI/bge-small-en-v1.5 (default)
- BAAI/bge-large-en-v1.5
- intfloat/multilingual-e5-large
- sentence-transformers/all-mpnet-base-v2

Sources: docs/Getting Started.ipynb:159-162, docs/Getting Started.ipynb:185-187

## Example Use Cases

### Basic Retrieval

One common use case for text embeddings is semantic search:

```
```

This example shows how to perform basic retrieval using cosine similarity between the query and document embeddings.

Sources: docs/qdrant/Retrieval\_with\_FastEmbed.ipynb:111-123

### Integration with Vector Databases

FastEmbed integrates smoothly with vector databases like Qdrant:

```
```

Sources: docs/index.md:49-73

## Performance Advantages

FastEmbed is designed for high performance through several optimizations:

1. **ONNX Runtime**: Uses optimized inference engine for speed
2. **Quantized Models**: Reduced model size without significant accuracy loss
3. **Parallel Processing**: Automatic multi-threading for batch operations

These optimizations make FastEmbed significantly faster than traditional implementations:

| Metric             | FastEmbed | Hugging Face Transformers |
| ------------------ | --------- | ------------------------- |
| Avg Time per Batch | 0.044s    | 0.047s                    |
| Max Time           | 0.057s    | 0.066s                    |
| Min Time           | 0.043s    | 0.043s                    |
| Characters/Second  | \~1200    | \~1100                    |

Sources: docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb:274-345

## Summary

Basic text embedding with FastEmbed through the `TextEmbedding` class provides:

1. A simple interface for generating high-quality vector representations of text
2. Specialized methods for query and passage embedding to improve search relevance
3. High performance through ONNX optimization and parallel processing
4. Support for multiple pre-trained models
5. Easy integration with vector databases and retrieval systems

These capabilities make FastEmbed an excellent choice for applications requiring semantic text understanding, including search, classification, clustering, and recommendation systems.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Basic Text Embedding](#basic-text-embedding.md)
- [TextEmbedding Class Overview](#textembedding-class-overview.md)
- [Initialization and Basic Usage](#initialization-and-basic-usage.md)
- [Initializing TextEmbedding](#initializing-textembedding.md)
- [Generating Embeddings](#generating-embeddings.md)
- [Understanding Embedding Output](#understanding-embedding-output.md)
- [Advanced Features](#advanced-features.md)
- [Query vs. Passage Embeddings](#query-vs-passage-embeddings.md)
- [Format for Document Prefixes](#format-for-document-prefixes.md)
- [Parallel Processing](#parallel-processing.md)
- [Supported Models](#supported-models.md)
- [Example Use Cases](#example-use-cases.md)
- [Basic Retrieval](#basic-retrieval.md)
- [Integration with Vector Databases](#integration-with-vector-databases.md)
- [Performance Advantages](#performance-advantages.md)
- [Summary](#summary.md)
