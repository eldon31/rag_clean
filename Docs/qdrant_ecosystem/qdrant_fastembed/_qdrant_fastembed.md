qdrant/fastembed | DeepWiki

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

# Overview

Relevant source files

- [.pre-commit-config.yaml](https://github.com/qdrant/fastembed/blob/b785640b/.pre-commit-config.yaml)
- [README.md](https://github.com/qdrant/fastembed/blob/b785640b/README.md)
- [docs/examples/FastEmbed\_GPU.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb)
- [fastembed/\_\_init\_\_.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/__init__.py)
- [pyproject.toml](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml)
- [tests/test\_late\_interaction\_multimodal.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_late_interaction_multimodal.py)

FastEmbed is a lightweight, fast Python library designed for generating high-quality embeddings from text and images. It focuses on performance optimization through ONNX Runtime integration, providing a more efficient alternative to traditional embedding libraries like PyTorch-based Sentence Transformers.

This overview introduces the core concepts, architecture, and components of FastEmbed. For installation instructions, see [Installation and Setup](qdrant/fastembed/2-installation-and-setup.md).

Sources: [README.md1-14](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L1-L14) [pyproject.toml1-12](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L1-L12)

## Core Features

FastEmbed offers several key advantages over other embedding libraries:

1. **Lightweight**: Minimal external dependencies, making it suitable for resource-constrained environments like serverless functions

2. **Fast**: ONNX Runtime integration and data parallelism for efficient embedding generation, providing significant performance gains over PyTorch-based alternatives

3. **Accurate**: Support for state-of-the-art embedding models that deliver performance comparable to or better than commercial options like OpenAI's Ada-002

4. **Versatile**: Support for multiple embedding strategies including dense, sparse, late interaction, and multimodal approaches

5. **GPU Acceleration**: Optional GPU support through the `fastembed-gpu` package

Sources: [README.md7-14](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L7-L14) [pyproject.toml13-34](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L13-L34) [docs/examples/FastEmbed\_GPU.ipynb9-21](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L9-L21)

## System Architecture

FastEmbed is organized around a modular architecture with specialized classes for different embedding approaches and modalities.

### Core Components Diagram

```
```

Sources: [fastembed/\_\_init\_\_.py1-22](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/__init__.py#L1-L22)

### Embedding Process Flow

```
```

Sources: [README.md28-190](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L28-L190)

## Core Components

FastEmbed provides specialized classes for different embedding approaches, each optimized for specific use cases:

| Component                            | Description                                                | Primary Use Cases                             |
| ------------------------------------ | ---------------------------------------------------------- | --------------------------------------------- |
| `TextEmbedding`                      | Dense text embeddings, supports various pooling strategies | Semantic search, document similarity          |
| `SparseTextEmbedding`                | Sparse text embeddings (SPLADE, BM25, BM42)                | Hybrid search, traditional search integration |
| `LateInteractionTextEmbedding`       | Token-level embeddings (ColBERT)                           | Advanced retrieval with token matching        |
| `ImageEmbedding`                     | CLIP and similar image embeddings                          | Image search, visual similarity               |
| `LateInteractionMultimodalEmbedding` | Multimodal token-level embeddings (ColPali)                | Document image search, multimodal retrieval   |
| `TextCrossEncoder`                   | Text pair scoring for reranking                            | Search result refinement, question-answering  |

Sources: [README.md49-190](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L49-L190) [fastembed/\_\_init\_\_.py3-22](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/__init__.py#L3-L22)

### Text Embeddings

The `TextEmbedding` class is the most commonly used component, providing dense vector representations for text:

```
```

Key features:

- Default model is "BAAI/bge-small-en-v1.5", a performant English embedding model
- Automatic model downloading and caching
- Parallel processing for large batches of documents
- Optional GPU acceleration with the `fastembed-gpu` package

Sources: [README.md28-47](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L28-L47)

### Sparse Text Embeddings

The `SparseTextEmbedding` class provides sparse vector representations:

```
```

These sparse embeddings are particularly useful for hybrid search approaches that combine traditional term-based retrieval with semantic search.

Sources: [README.md87-99](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L87-L99)

### Late Interaction Models

The `LateInteractionTextEmbedding` class implements ColBERT-style embeddings with token-level representations:

```
```

These models produce a matrix of embeddings per document (one vector per token), enabling more sophisticated matching during retrieval.

Sources: [README.md119-136](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L119-L136)

### Image Embeddings

The `ImageEmbedding` class provides embedding generation for images:

```
```

This class supports both file paths and PIL Image objects as input.

Sources: [README.md140-154](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L140-L154)

### Multimodal Embeddings

The `LateInteractionMultimodalEmbedding` class enables token-level embeddings for both text and images:

```
```

This allows for sophisticated cross-modal retrieval between text queries and document images.

Sources: [README.md158-176](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L158-L176) [tests/test\_late\_interaction\_multimodal.py1-83](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_late_interaction_multimodal.py#L1-L83)

### Text Cross Encoder for Reranking

The `TextCrossEncoder` class provides text pair scoring for reranking search results:

```
```

This is useful for refining search results after initial retrieval.

Sources: [README.md180-207](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L180-L207)

## Performance Optimization

FastEmbed focuses on performance through several key optimizations:

1. **ONNX Runtime**: Uses ONNX models for efficient inference without requiring PyTorch/TensorFlow
2. **Parallel Processing**: Automatically distributes embedding generation across CPU cores
3. **GPU Acceleration**: Optional GPU support through `fastembed-gpu` package
4. **Model Caching**: Automatic downloading and caching of models
5. **Batching**: Efficient batching of inputs for optimized throughput

A simple benchmark comparing CPU vs GPU performance shows orders of magnitude improvement:

```
CPU execution time: 4.33s (500 documents)
GPU execution time: 43.4ms (500 documents)
```

Sources: [docs/examples/FastEmbed\_GPU.ipynb390-511](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L390-L511)

## Integration with Qdrant

FastEmbed is maintained by Qdrant and has native integration with the Qdrant vector database:

```
```

For more details on using FastEmbed with Qdrant, see [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md).

Sources: [README.md232-281](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L232-L281)

## Supported Models

FastEmbed supports a wide range of embedding models:

1. **Dense Text Models**: BGE embeddings, Sentence Transformers, CLIP text models
2. **Sparse Text Models**: SPLADE, BM25, BM42
3. **Late Interaction Models**: ColBERT, Jina ColBERT
4. **Image Models**: CLIP vision models
5. **Multimodal Models**: ColPali

For a complete list of supported models and their configuration details, see [Supported Models](qdrant/fastembed/6-supported-models.md).

The library also supports extending with custom models through API methods like `TextEmbedding.add_custom_model()`.

Sources: [README.md66-82](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L66-L82) [README.md196-207](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L196-L207)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Overview](#overview.md)
- [Core Features](#core-features.md)
- [System Architecture](#system-architecture.md)
- [Core Components Diagram](#core-components-diagram.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Core Components](#core-components.md)
- [Text Embeddings](#text-embeddings.md)
- [Sparse Text Embeddings](#sparse-text-embeddings.md)
- [Late Interaction Models](#late-interaction-models.md)
- [Image Embeddings](#image-embeddings.md)
- [Multimodal Embeddings](#multimodal-embeddings.md)
- [Text Cross Encoder for Reranking](#text-cross-encoder-for-reranking.md)
- [Performance Optimization](#performance-optimization.md)
- [Integration with Qdrant](#integration-with-qdrant.md)
- [Supported Models](#supported-models.md)
