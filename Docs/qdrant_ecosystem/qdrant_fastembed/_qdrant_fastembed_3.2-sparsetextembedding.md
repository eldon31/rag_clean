SparseTextEmbedding | qdrant/fastembed | DeepWiki

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

# SparseTextEmbedding

Relevant source files

- [fastembed/sparse/bm25.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py)
- [fastembed/sparse/bm42.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm42.py)
- [fastembed/sparse/sparse\_text\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py)
- [fastembed/sparse/splade\_pp.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py)
- [tests/test\_attention\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py)
- [tests/test\_sparse\_embeddings.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py)

## Purpose and Scope

This document covers the `SparseTextEmbedding` class, which provides functionality for generating sparse text embeddings from documents and queries. Sparse embeddings represent text as high-dimensional, sparse vectors where each dimension corresponds to a specific token/term with an associated importance score. Unlike dense embeddings (covered in [TextEmbedding](qdrant/fastembed/3.1-textembedding.md)), sparse embeddings explicitly capture lexical information and enable efficient hybrid search capabilities.

This page explains how to use the `SparseTextEmbedding` class and the different sparse embedding models it supports (SpladePP, Bm25, and Bm42).

Sources: [fastembed/sparse/sparse\_text\_embedding.py16-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L16-L130)

## Overview

`SparseTextEmbedding` serves as a unified interface to different sparse embedding models. It selects the appropriate implementation based on the model name provided, allowing users to easily switch between sparse embedding approaches without changing their code.

```
```

Sources: [fastembed/sparse/sparse\_text\_embedding.py16-91](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L16-L91)

## Supported Models

`SparseTextEmbedding` supports the following sparse embedding models:

| Model                                   | Implementation | Description                                      | Use Case                                           |
| --------------------------------------- | -------------- | ------------------------------------------------ | -------------------------------------------------- |
| prithivida/Splade\_PP\_en\_v1           | SpladePP       | Neural sparse embedding model based on SPLADE++  | General-purpose sparse embeddings for English      |
| Qdrant/bm25                             | Bm25           | Traditional BM25 as sparse vectors               | Classic lexical search with IDF weighting          |
| Qdrant/bm42-all-minilm-l6-v2-attentions | Bm42           | BM25-inspired model using transformer attentions | Better handling of short documents and rare tokens |

You can list all supported models with:

```
```

Sources: [fastembed/sparse/sparse\_text\_embedding.py19-50](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L19-L50) [fastembed/sparse/splade\_pp.py14-32](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L14-L32) [fastembed/sparse/bm25.py46-58](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py#L46-L58) [fastembed/sparse/bm42.py20-36](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm42.py#L20-L36)

## Sparse vs. Dense Embeddings

```
```

**Key differences:**

- **Dense embeddings**: Fixed-size vectors where every dimension contains a value and the meaning of each dimension is not interpretable
- **Sparse embeddings**: High-dimensional vectors (vocabulary size) where most values are zero and each dimension corresponds to a specific token

Sources: [tests/test\_sparse\_embeddings.py10-46](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L10-L46)

## Embedding Process Flow

```
```

Sources: [fastembed/sparse/splade\_pp.py37-52](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L37-L52) [fastembed/sparse/bm25.py61-146](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py#L61-L146) [fastembed/sparse/bm42.py39-251](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm42.py#L39-L251)

## Usage

### Initialization

To create a `SparseTextEmbedding` instance, specify the model name and optional parameters:

```
```

Common initialization parameters:

| Parameter   | Description                                 | Default               |
| ----------- | ------------------------------------------- | --------------------- |
| model\_name | The name of the model to use                | Required              |
| cache\_dir  | Path to cache directory                     | System temp directory |
| threads     | Number of threads to use for inference      | None (auto)           |
| cuda        | Whether to use CUDA for inference           | False                 |
| device\_ids | List of device IDs for multi-GPU processing | None                  |
| lazy\_load  | Whether to load the model only when needed  | False                 |
| parallel    | Number of parallel processes for embedding  | None                  |

Sources: [fastembed/sparse/sparse\_text\_embedding.py52-91](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L52-L91)

### Document Embedding

To generate sparse embeddings for documents:

```
```

The `embed()` method accepts the following parameters:

| Parameter   | Description                                                  | Default  |
| ----------- | ------------------------------------------------------------ | -------- |
| documents   | String or iterable of strings to embed                       | Required |
| batch\_size | Batch size for processing                                    | 256      |
| parallel    | Number of parallel processes (None, int, or 0 for all cores) | None     |

Sources: [fastembed/sparse/sparse\_text\_embedding.py93-115](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L93-L115)

### Query Embedding

For search applications, you can generate embeddings for queries:

```
```

Note that different sparse models may handle queries differently:

- SpladePP treats queries the same as documents
- Bm25 and Bm42 use simplified query representations (token hashing with value 1.0)

Sources: [fastembed/sparse/sparse\_text\_embedding.py117-129](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L117-L129) [fastembed/sparse/bm25.py298-316](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py#L298-L316) [fastembed/sparse/bm42.py312-333](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm42.py#L312-L333)

## Model Details

### SpladePP

SpladePP (SPLADE++) implements a neural network approach to sparse embeddings. It:

1. Tokenizes input text
2. Processes through a transformer model
3. Applies ReLU and log transformations to produce sparse representations
4. Extracts non-zero values and their corresponding token indices

The resulting sparse embeddings have the following characteristics:

- Non-zero values typically represent 0.1-5% of the vocabulary
- Value magnitude indicates token importance
- Each token dimension corresponds to a specific token in the vocabulary

Sources: [fastembed/sparse/splade\_pp.py36-52](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/splade_pp.py#L36-L52)

### Bm25

Bm25 implements the classic BM25 ranking function as sparse embeddings. It:

1. Tokenizes input text
2. Applies stemming and removes stopwords
3. Calculates term frequency for each token
4. Applies BM25 formula to compute token importance
5. Hashes tokens to create token IDs

The BM25 formula used is:

```
score(q, d) = SUM[ IDF(q_i) * (f(q_i, d) * (k + 1)) / (f(q_i, d) + k * (1 - b + b * (|d| / avg_len))) ]
```

Where:

- IDF is computed on Qdrant's side using the `idf` modifier
- f(q\_i, d) is the term frequency
- k and b are configurable parameters (defaults: k=1.2, b=0.75)
- avg\_len is the average document length (default: 256.0)

Note: Bm25 supports multiple languages through different stemmers.

Sources: [fastembed/sparse/bm25.py61-146](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py#L61-L146) [fastembed/sparse/bm25.py264-291](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py#L264-L291)

### Bm42

Bm42 is an extension of BM25 that leverages transformer attention weights. It:

1. Tokenizes input text
2. Processes through a transformer model to get attention weights
3. Reconstructs subword tokens into words
4. Applies stemming and removes stopwords
5. Uses attention weights to evaluate token importance
6. Hashes tokens to create token IDs

Key advantages:

- Works better with short documents where term frequency is less informative
- Better handles rare tokens
- Leverages semantic understanding from the transformer model

Sources: [fastembed/sparse/bm42.py39-250](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm42.py#L39-L250)

## Parallel Processing

All sparse embedding models support parallel processing for faster embedding generation with large datasets:

```
```

Sources: [fastembed/sparse/sparse\_text\_embedding.py93-115](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L93-L115) [tests/test\_sparse\_embeddings.py96-124](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L96-L124)

## Implementation Architecture

```
```

Sources: [fastembed/sparse/sparse\_text\_embedding.py16-91](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_text_embedding.py#L16-L91) [fastembed/sparse/sparse\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/sparse_embedding_base.py)

## Integration with Vector Databases

Sparse embeddings are particularly useful for hybrid search when combined with vector databases. For example, with Qdrant:

```
```

Note: The Bm25 and Bm42 models are designed to be used with the `idf` modifier in Qdrant to fully implement the BM25/BM42 scoring function.

Sources: [fastembed/sparse/bm25.py62-74](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm25.py#L62-L74) [fastembed/sparse/bm42.py52-56](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/sparse/bm42.py#L52-L56)

## Performance and Memory Considerations

Sparse embeddings offer several advantages over dense embeddings:

1. **Storage efficiency** for large vocabularies since only non-zero values are stored
2. **Interpretability** as each dimension corresponds to a specific token
3. **Exact term matching** which can be important for specialized terms

However, they also have some considerations:

1. **Processing overhead** for generating sparse vectors (especially for neural models)
2. **Index size** can be larger than dense embeddings in some cases
3. **Model selection** should match your data characteristics (e.g., document length)

Sources: [tests/test\_sparse\_embeddings.py52-94](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_sparse_embeddings.py#L52-L94) [tests/test\_attention\_embeddings.py10-96](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_attention_embeddings.py#L10-L96)

## Related Pages

- For dense text embeddings, see [TextEmbedding](qdrant/fastembed/3.1-textembedding.md)
- For late interaction embeddings, see [LateInteractionTextEmbedding](qdrant/fastembed/3.3-lateinteractiontextembedding.md)
- For more details on implementation, see [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md)
- For integration with Qdrant, see [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [SparseTextEmbedding](#sparsetextembedding.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Supported Models](#supported-models.md)
- [Sparse vs. Dense Embeddings](#sparse-vs-dense-embeddings.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Usage](#usage.md)
- [Initialization](#initialization.md)
- [Document Embedding](#document-embedding.md)
- [Query Embedding](#query-embedding.md)
- [Model Details](#model-details.md)
- [SpladePP](#spladepp.md)
- [Bm25](#bm25.md)
- [Bm42](#bm42.md)
- [Parallel Processing](#parallel-processing.md)
- [Implementation Architecture](#implementation-architecture.md)
- [Integration with Vector Databases](#integration-with-vector-databases.md)
- [Performance and Memory Considerations](#performance-and-memory-considerations.md)
- [Related Pages](#related-pages.md)
