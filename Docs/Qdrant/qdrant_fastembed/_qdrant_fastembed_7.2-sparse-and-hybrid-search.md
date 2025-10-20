Sparse and Hybrid Search | qdrant/fastembed | DeepWiki

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

# Sparse and Hybrid Search

Relevant source files

- [tests/test\_attention\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py)
- [tests/test\_sparse\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py)

This page provides a comprehensive guide to implementing sparse embeddings and hybrid search using FastEmbed. While [TextEmbedding](qdrant/fastembed/3.1-textembedding.md) creates dense vector representations, sparse embeddings offer a different approach with unique advantages that complement dense embeddings in search applications.

## Understanding Sparse Embeddings and Hybrid Search

Sparse embeddings represent text as high-dimensional, sparse vectors where most elements are zero. Unlike dense embeddings, sparse vectors only store the non-zero elements through indices and corresponding values.

```
```

Sources: [tests/test\_sparse\_embeddings.py10-47](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L10-L47)

## Sparse Embedding Models in FastEmbed

FastEmbed provides several sparse embedding models through the `SparseTextEmbedding` class:

```
```

Sources: [tests/test\_sparse\_embeddings.py6-7](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L6-L7) [tests/test\_attention\_embeddings.py6](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L6-L6)

### Supported Models

FastEmbed supports multiple types of sparse embedding models:

1. **SPLADE Models**: Sparse Lexical and Expansion models (e.g., "prithivida/Splade\_PP\_en\_v1")
2. **BM25**: Classical lexical retrieval algorithm based on term frequency-inverse document frequency
3. **BM42**: Attention-based sparse embeddings that combine neural and lexical features

Each model produces sparse embeddings with different characteristics suitable for various search tasks.

Sources: [tests/test\_sparse\_embeddings.py52](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L52-L52) [tests/test\_attention\_embeddings.py10](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L10-L10)

## Using Sparse Embeddings

### Basic Usage

The `SparseTextEmbedding` class provides a straightforward interface for generating sparse embeddings:

```
```

Sources: [tests/test\_sparse\_embeddings.py57-65](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L57-L65)

### Query vs. Passage Embeddings

For search applications, FastEmbed allows you to generate specialized embeddings for queries and passages:

```
```

This distinction is important for asymmetric search scenarios where queries and documents may need different processing.

Sources: [tests/test\_sparse\_embeddings.py84-86](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L84-L86)

### Language Support and Special Characters

BM25 models support multiple languages and handle special characters effectively:

```
```

The language parameter affects tokenization and stemming behavior, optimizing for language-specific features.

Sources: [tests/test\_attention\_embeddings.py104-111](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L104-L111) [tests/test\_attention\_embeddings.py125-144](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L125-L144)

## Sparse Embedding Structure

Sparse embeddings in FastEmbed are represented with two components:

1. **Indices**: Integer array indicating which dimensions have non-zero values
2. **Values**: Corresponding importance/weight for each non-zero dimension

```
```

This format allows for efficient storage and processing of high-dimensional sparse vectors.

Sources: [tests/test\_sparse\_embeddings.py10-47](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L10-L47)

## Implementing Hybrid Search

Hybrid search combines the strengths of sparse and dense embeddings to improve search quality. Here's how to implement it:

```
```

### Implementation Steps:

1. Generate both sparse and dense embeddings for your document collection

2. For each query, generate both sparse and dense query embeddings

3. Perform separate searches with each embedding type

4. Combine and re-rank the results using strategies like:

   - Score normalization and weighted combination
   - Reciprocal rank fusion
   - Taking the union of top results from both methods

Sources: [tests/test\_sparse\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py) [tests/test\_attention\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py)

## Performance Optimization

FastEmbed provides several performance optimizations for sparse embeddings:

### Batch Processing

Process multiple documents efficiently:

```
```

Sources: [tests/test\_sparse\_embeddings.py98-102](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L98-L102)

### Parallel Execution

Enable parallel processing to utilize multiple CPU cores:

```
```

Sources: [tests/test\_sparse\_embeddings.py98-121](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L98-L121) [tests/test\_attention\_embeddings.py74-95](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L74-L95)

### Lazy Loading

Defer model loading until first use to conserve memory:

```
```

Sources: [tests/test\_sparse\_embeddings.py189-206](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L189-L206) [tests/test\_attention\_embeddings.py147-159](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L147-L159)

## BM25 Configuration

The BM25 model offers additional configuration options:

### Stemming and Stopwords

```
```

Stemming reduces words to their root form, while stopword removal filters out common words. These techniques can significantly impact search quality.

Sources: [tests/test\_sparse\_embeddings.py136-186](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L136-L186)

## Summary

Sparse embeddings provide a complementary approach to dense embeddings, capturing lexical and token-level information that can improve search relevance. FastEmbed's `SparseTextEmbedding` class offers a flexible and efficient way to generate these embeddings with various models, including SPLADE, BM25, and BM42.

Hybrid search, combining sparse and dense approaches, leverages the strengths of both methods to deliver more comprehensive search results, particularly beneficial for complex search scenarios where both semantic and lexical matching are important.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Sparse and Hybrid Search](#sparse-and-hybrid-search.md)
- [Understanding Sparse Embeddings and Hybrid Search](#understanding-sparse-embeddings-and-hybrid-search.md)
- [Sparse Embedding Models in FastEmbed](#sparse-embedding-models-in-fastembed.md)
- [Supported Models](#supported-models.md)
- [Using Sparse Embeddings](#using-sparse-embeddings.md)
- [Basic Usage](#basic-usage.md)
- [Query vs. Passage Embeddings](#query-vs-passage-embeddings.md)
- [Language Support and Special Characters](#language-support-and-special-characters.md)
- [Sparse Embedding Structure](#sparse-embedding-structure.md)
- [Implementing Hybrid Search](#implementing-hybrid-search.md)
- [Implementation Steps:](#implementation-steps.md)
- [Performance Optimization](#performance-optimization.md)
- [Batch Processing](#batch-processing.md)
- [Parallel Execution](#parallel-execution.md)
- [Lazy Loading](#lazy-loading.md)
- [BM25 Configuration](#bm25-configuration.md)
- [Stemming and Stopwords](#stemming-and-stopwords.md)
- [Summary](#summary.md)
