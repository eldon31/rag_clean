TextCrossEncoder | qdrant/fastembed | DeepWiki

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

# TextCrossEncoder

Relevant source files

- [README.md](https://github.com/qdrant/fastembed/blob/b785640b/README.md)
- [docs/examples/FastEmbed\_GPU.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb)
- [fastembed/rerank/cross\_encoder/\_\_init\_\_.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/__init__.py)
- [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py)
- [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py)
- [fastembed/rerank/cross\_encoder/text\_cross\_encoder\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder_base.py)

## Purpose and Overview

The `TextCrossEncoder` class provides reranking functionality within the FastEmbed library. Unlike embedding models that convert text to vectors for similarity comparison, cross encoders directly score the relevance between a query and a document. This makes them particularly useful for improving search results by reranking candidate documents retrieved through initial vector similarity search.

For information about generating embeddings for retrieval, see [TextEmbedding](qdrant/fastembed/3.1-textembedding.md).

Sources: [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py15-164](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py#L15-L164) [README.md177-191](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L177-L191)

## Architecture

The `TextCrossEncoder` system follows a layered architecture that enables extensibility while maintaining a simple interface for users.

```
```

The key components are:

1. **TextCrossEncoder**: The main entry point class that users interact with. It acts as a façade to the underlying implementations.

2. **TextCrossEncoderBase**: An abstract base class that defines the interface for text cross encoders.

3. **OnnxTextCrossEncoder**: The primary implementation that uses ONNX Runtime for efficient inference.

4. **CustomTextCrossEncoder**: An implementation for user-defined custom models.

5. **TextRerankerWorker/TextCrossEncoderWorker**: Worker classes for parallel processing of reranking tasks.

Sources: [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py15-164](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py#L15-L164) [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py67-215](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py#L67-L215) [fastembed/rerank/cross\_encoder/text\_cross\_encoder\_base.py7-59](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder_base.py#L7-L59)

## Reranking Process

The reranking process in `TextCrossEncoder` involves several steps from initialization to scoring documents:

```
```

During reranking:

1. The query and documents are combined into pairs
2. These pairs are tokenized and processed in batches
3. Each batch is run through the cross-encoder model
4. The model outputs relevance scores for each query-document pair
5. Scores are returned to the user, with higher scores indicating greater relevance

Sources: [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py154-174](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py#L154-L174) [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py86-99](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py#L86-L99)

## Supported Models

The `TextCrossEncoder` class supports a variety of models optimized for reranking tasks:

| Model Name                                | Description                                                                 | Size (GB) | License      |
| ----------------------------------------- | --------------------------------------------------------------------------- | --------- | ------------ |
| Xenova/ms-marco-MiniLM-L-6-v2             | MiniLM-L-6-v2 model optimized for re-ranking tasks                          | 0.08      | apache-2.0   |
| Xenova/ms-marco-MiniLM-L-12-v2            | MiniLM-L-12-v2 model optimized for re-ranking tasks                         | 0.12      | apache-2.0   |
| BAAI/bge-reranker-base                    | BGE reranker base model for cross-encoder re-ranking                        | 1.04      | mit          |
| jinaai/jina-reranker-v1-tiny-en           | Blazing-fast re-ranking with 8K context length, fewer parameters than turbo | 0.13      | apache-2.0   |
| jinaai/jina-reranker-v1-turbo-en          | Blazing-fast re-ranking with 8K context length                              | 0.15      | apache-2.0   |
| jinaai/jina-reranker-v2-base-multilingual | Multi-lingual reranker with 1K context length and sliding window            | 1.11      | cc-by-nc-4.0 |

You can get a list of all supported models programmatically:

```
```

Sources: [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py15-63](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py#L15-L63) [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py21-51](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py#L21-L51)

## Usage Examples

### Basic Reranking

The most common use case is to rerank a list of documents based on a query:

```
```

### Scoring Text Pairs

You can also directly score pairs of texts for relevance:

```
```

### Batching and Parallelization

For large datasets, you can control the batch size and enable parallel processing:

```
```

Sources: [README.md177-191](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L177-L191) [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py86-132](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py#L86-L132)

## GPU Acceleration

`TextCrossEncoder` supports GPU acceleration through ONNX Runtime's CUDA execution provider. To enable GPU acceleration:

1. Install the GPU version of FastEmbed:

   ```
   ```

2. Specify the CUDA execution provider when initializing the cross encoder:

   ```
   ```

Alternatively, you can use the `cuda` parameter:

```
```

For systems with multiple GPUs, you can specify which devices to use:

```
```

Sources: [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py77-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py#L77-L130) [docs/examples/FastEmbed\_GPU.ipynb9-194](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L9-L194)

## Integration with Search Systems

```
```

A typical integration of `TextCrossEncoder` in a search system involves:

1. Using embeddings (e.g., `TextEmbedding`) to retrieve initial candidate documents based on vector similarity
2. Applying `TextCrossEncoder` to rerank these candidates based on their relevance to the query
3. Returning the reranked results to the user

This two-stage approach combines the efficiency of vector search for initial retrieval with the accuracy of cross-encoders for final ranking.

Sources: [README.md177-191](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L177-L191)

## Extending with Custom Models

You can add your own custom cross encoder models that aren't in the default supported list:

```
```

When adding a custom model, you need to provide:

- The model name identifier
- The model file path within the model directory
- The source of the model (typically Hugging Face repository)
- Optional metadata like description, license, and size

Sources: [fastembed/rerank/cross\_encoder/text\_cross\_encoder.py134-163](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/text_cross_encoder.py#L134-L163) [README.md193-208](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L193-L208)

## Technical Implementation

The underlying implementation of `TextCrossEncoder` relies on the ONNX Runtime for efficient inference. When a reranking operation is performed:

1. The model first tokenizes the input text pairs
2. The tokenized inputs are processed by the ONNX model
3. The model outputs relevance scores, which are then returned to the user

Unlike embedding models that produce vectors, cross encoders directly output a scalar relevance score for each input pair. This makes them more accurate for ranking tasks but less efficient for large-scale retrieval, which is why they're typically used in combination with embedding models in a two-stage retrieval system.

Currently, parallel execution with multiple GPUs is not fully supported for cross encoders, as noted in the warning message in the code:

> "Parallel execution is currently not supported for cross encoders, only the first device will be used for inference"

Sources: [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py119-123](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py#L119-L123) [fastembed/rerank/cross\_encoder/onnx\_text\_cross\_encoder.py199-200](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_cross_encoder.py#L199-L200)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [TextCrossEncoder](#textcrossencoder.md)
- [Purpose and Overview](#purpose-and-overview.md)
- [Architecture](#architecture.md)
- [Reranking Process](#reranking-process.md)
- [Supported Models](#supported-models.md)
- [Usage Examples](#usage-examples.md)
- [Basic Reranking](#basic-reranking.md)
- [Scoring Text Pairs](#scoring-text-pairs.md)
- [Batching and Parallelization](#batching-and-parallelization.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Integration with Search Systems](#integration-with-search-systems.md)
- [Extending with Custom Models](#extending-with-custom-models.md)
- [Technical Implementation](#technical-implementation.md)
