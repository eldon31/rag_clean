Dense Text Embeddings | qdrant/fastembed | DeepWiki

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

# Dense Text Embeddings

Relevant source files

- [fastembed/text/clip\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py)
- [fastembed/text/onnx\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py)
- [fastembed/text/pooled\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py)
- [fastembed/text/pooled\_normalized\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py)

Dense text embeddings are fixed-size vector representations of text that capture semantic meaning in a continuous vector space. In FastEmbed, dense text embeddings are implemented through several specialized classes that leverage ONNX Runtime for high-performance inference. This page details the implementation of dense text embedding models in the FastEmbed library.

For information about sparse text embeddings, see [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md). For late interaction models, see [Late Interaction Models](qdrant/fastembed/5.3-late-interaction-models.md).

## Architecture Overview

FastEmbed implements dense text embeddings through a hierarchy of specialized classes, each handling different embedding strategies and post-processing techniques.

```
```

Sources: [fastembed/text/onnx\_embedding.py186-326](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L186-L326) [fastembed/text/pooled\_embedding.py93-120](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L93-L120) [fastembed/text/pooled\_normalized\_embedding.py127-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L127-L147) [fastembed/text/clip\_embedding.py24-40](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py#L24-L40)

## Core Implementation Classes

The FastEmbed library implements dense text embeddings through four primary classes, each catering to different embedding strategies and post-processing techniques.

### OnnxTextEmbedding

`OnnxTextEmbedding` serves as the foundational class for ONNX-based text embeddings. It provides the base implementation for model loading, inference, and embedding generation.

Key features:

- Leverages ONNX Runtime for optimized inference
- Supports parallel processing with multiple workers
- Handles model downloading and caching
- Implements a flexible post-processing pipeline

This class supports models like BGE, Snowflake Arctic, and MXBai embeddings.

Sources: [fastembed/text/onnx\_embedding.py186-326](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L186-L326)

### PooledEmbedding

`PooledEmbedding` extends `OnnxTextEmbedding` and implements mean pooling for models that produce token-level embeddings. Mean pooling aggregates token embeddings weighted by attention mask values.

Key features:

- Implements mean pooling across token dimensions
- Preserves semantic information from all tokens
- Returns non-normalized embeddings

This class supports models like Nomic Embed, multilingual sentence transformers, and E5 models.

Sources: [fastembed/text/pooled\_embedding.py93-120](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L93-L120)

### PooledNormalizedEmbedding

`PooledNormalizedEmbedding` extends `PooledEmbedding` and adds L2 normalization to the pooled embeddings. Normalization ensures all embedding vectors have the same magnitude, which is particularly useful for cosine similarity comparisons.

Key features:

- Applies mean pooling like its parent class
- Adds L2 normalization to the embeddings
- Optimized for cosine similarity use cases

This class supports models like MiniLM, Jina Embeddings V2, and GTE models.

Sources: [fastembed/text/pooled\_normalized\_embedding.py127-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L127-L147)

### CLIPOnnxEmbedding

`CLIPOnnxEmbedding` extends `OnnxTextEmbedding` and is specialized for CLIP text encoder models. It handles the unique output format of CLIP models without additional pooling.

Key features:

- Specialized for CLIP text encoders
- Works with multimodal embedding spaces
- Compatible with corresponding image encoders

This class specifically supports the CLIP ViT-B-32 text encoder.

Sources: [fastembed/text/clip\_embedding.py24-40](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py#L24-L40)

## Embedding Process Flow

The process of generating dense text embeddings involves several steps, from input preprocessing to the final vector representation.

```
```

Sources: [fastembed/text/onnx\_embedding.py260-294](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L260-L294) [fastembed/text/onnx\_embedding.py306-315](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L306-L315) [fastembed/text/pooled\_embedding.py113-119](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L113-L119) [fastembed/text/pooled\_normalized\_embedding.py141-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L141-L147) [fastembed/text/clip\_embedding.py38-39](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py#L38-L39)

## Post-Processing Techniques

The different embedding classes implement various post-processing techniques:

1. **CLS Token Extraction**: `OnnxTextEmbedding` extracts the first token (CLS) embedding for models that encode sentence meaning in this special token.

```
```

2. **Mean Pooling**: `PooledEmbedding` applies mean pooling across token embeddings, weighted by the attention mask.

```
```

3. **Normalized Pooling**: `PooledNormalizedEmbedding` applies mean pooling followed by L2 normalization.

```
```

4. **CLIP Processing**: `CLIPOnnxEmbedding` passes through the model output directly as it's already in the desired format.

Sources: [fastembed/text/onnx\_embedding.py306-315](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L306-L315) [fastembed/text/pooled\_embedding.py99-102](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L99-L102) [fastembed/text/pooled\_normalized\_embedding.py141-147](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L141-L147) [fastembed/text/clip\_embedding.py38-39](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py#L38-L39)

## Supported Models

FastEmbed supports a wide range of dense text embedding models across different implementations:

### OnnxTextEmbedding Models

| Model                               | Dimension | Language | Context Length | License    |
| ----------------------------------- | --------- | -------- | -------------- | ---------- |
| BAAI/bge-small-en-v1.5              | 384       | English  | 512            | MIT        |
| BAAI/bge-base-en-v1.5               | 768       | English  | 512            | MIT        |
| BAAI/bge-large-en-v1.5              | 1024      | English  | 512            | MIT        |
| BAAI/bge-small-zh-v1.5              | 512       | Chinese  | 512            | MIT        |
| mixedbread-ai/mxbai-embed-large-v1  | 1024      | English  | 512            | Apache-2.0 |
| snowflake/snowflake-arctic-embed-\* | 384-1024  | English  | 512-2048       | Apache-2.0 |
| jinaai/jina-clip-v1                 | 768       | English  | -              | Apache-2.0 |

### PooledEmbedding Models

| Model                                            | Dimension | Language                   | Context Length | License    |
| ------------------------------------------------ | --------- | -------------------------- | -------------- | ---------- |
| nomic-ai/nomic-embed-text-v1.5                   | 768       | English                    | 8192           | Apache-2.0 |
| sentence-transformers/paraphrase-multilingual-\* | 384-768   | Multilingual (\~50 langs)  | 384-512        | Apache-2.0 |
| intfloat/multilingual-e5-large                   | 1024      | Multilingual (\~100 langs) | 512            | MIT        |

### PooledNormalizedEmbedding Models

| Model                                  | Dimension | Language          | Context Length | License    |
| -------------------------------------- | --------- | ----------------- | -------------- | ---------- |
| sentence-transformers/all-MiniLM-L6-v2 | 384       | English           | 256            | Apache-2.0 |
| jinaai/jina-embeddings-v2-base-en      | 768       | English           | 8192           | Apache-2.0 |
| jinaai/jina-embeddings-v2-small-en     | 512       | English           | 8192           | Apache-2.0 |
| jinaai/jina-embeddings-v2-base-\*      | 768       | Various languages | 8192           | Apache-2.0 |
| thenlper/gte-base                      | 768       | English           | 512            | MIT        |
| thenlper/gte-large                     | 1024      | English           | 512            | MIT        |

### CLIPOnnxEmbedding Models

| Model                     | Dimension | Language | Context Length | License |
| ------------------------- | --------- | -------- | -------------- | ------- |
| Qdrant/clip-ViT-B-32-text | 512       | English  | 77             | MIT     |

Sources: [fastembed/text/onnx\_embedding.py10-183](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L10-L183) [fastembed/text/pooled\_embedding.py12-90](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L12-L90) [fastembed/text/pooled\_normalized\_embedding.py11-124](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L11-L124) [fastembed/text/clip\_embedding.py8-21](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/clip_embedding.py#L8-L21)

## Model Selection Guide

When choosing a dense text embedding model, consider the following factors:

```
```

Sources: [fastembed/text/onnx\_embedding.py10-183](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L10-L183) [fastembed/text/pooled\_embedding.py12-90](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_embedding.py#L12-L90) [fastembed/text/pooled\_normalized\_embedding.py11-124](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/pooled_normalized_embedding.py#L11-L124)

## Integration with FastEmbed API

The dense text embedding classes are accessible through the main `TextEmbedding` class, which serves as the public API for all dense text embedding functionality in FastEmbed.

```
```

Internally, `TextEmbedding` instantiates the appropriate implementation class (e.g., `OnnxTextEmbedding`, `PooledEmbedding`, etc.) based on the specified model name.

For more examples and detailed usage, see [Basic Text Embedding](qdrant/fastembed/7.1-basic-text-embedding.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Dense Text Embeddings](#dense-text-embeddings.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Implementation Classes](#core-implementation-classes.md)
- [OnnxTextEmbedding](#onnxtextembedding.md)
- [PooledEmbedding](#pooledembedding.md)
- [PooledNormalizedEmbedding](#poolednormalizedembedding.md)
- [CLIPOnnxEmbedding](#cliponnxembedding.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Post-Processing Techniques](#post-processing-techniques.md)
- [Supported Models](#supported-models.md)
- [OnnxTextEmbedding Models](#onnxtextembedding-models.md)
- [PooledEmbedding Models](#pooledembedding-models.md)
- [PooledNormalizedEmbedding Models](#poolednormalizedembedding-models.md)
- [CLIPOnnxEmbedding Models](#cliponnxembedding-models.md)
- [Model Selection Guide](#model-selection-guide.md)
- [Integration with FastEmbed API](#integration-with-fastembed-api.md)
