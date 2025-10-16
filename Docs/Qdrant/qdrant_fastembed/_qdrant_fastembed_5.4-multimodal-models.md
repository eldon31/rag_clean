Multimodal Models | qdrant/fastembed | DeepWiki

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

# Multimodal Models

Relevant source files

- [fastembed/late\_interaction\_multimodal/colpali.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py)
- [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py)
- [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding_base.py)
- [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py)

This document provides a detailed explanation of the multimodal embedding capabilities in FastEmbed. Multimodal models in FastEmbed enable the creation of embeddings from both text and image inputs within a compatible embedding space, making them ideal for cross-modal retrieval tasks. This page focuses specifically on the implementation of late interaction multimodal models, which process text and images separately but in alignment.

For information about text-only late interaction models, see [Late Interaction Models](qdrant/fastembed/5.3-late-interaction-models.md).

## Architecture Overview

The multimodal embedding functionality in FastEmbed is built around the `LateInteractionMultimodalEmbedding` class, which serves as the main entry point for users. This class is backed by specific implementations such as `ColPali`, which provide the actual embedding capabilities for both text and images.

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py14-16](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L14-L16) [fastembed/late\_interaction\_multimodal/colpali.py34-44](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L34-L44) [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py20-44](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L20-L44)

## Supported Models

Currently, FastEmbed supports the following multimodal model:

| Model                    | Dimensions | Description                                                           | License | Size   |
| ------------------------ | ---------- | --------------------------------------------------------------------- | ------- | ------ |
| Qdrant/colpali-v1.3-fp16 | 128        | Text and image embeddings, English, 50 tokens query length truncation | MIT     | 6.5 GB |

ColPali is a multimodal embedding model that combines the strengths of ColBERT architecture with multimodal capabilities, allowing for effective cross-modal retrieval between text and images.

Sources: [fastembed/late\_interaction\_multimodal/colpali.py20-31](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L20-L31)

## Implementation Details

### Class Hierarchy

The multimodal embedding functionality in FastEmbed follows a clear inheritance hierarchy:

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding\_base.py10-67](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding_base.py#L10-L67) [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py20-82](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L20-L82) [fastembed/late\_interaction\_multimodal/colpali.py34-281](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L34-L281)

### The ColPali Implementation

The `ColPali` class is the current implementation of multimodal embedding in FastEmbed. It implements both the `LateInteractionMultimodalEmbeddingBase` and `OnnxMultimodalModel` interfaces, providing functionality for:

1. Text embedding using special tokens and processing
2. Image embedding using a specialized vision encoder
3. Unified embedding space for cross-modal retrieval

Key implementation details include:

- Special token handling for query prefixing: `QUERY_PREFIX = "Query: "` and `BOS_TOKEN = "<s>"`
- Specialized preprocessing for multimodal inputs
- Processing of text with image placeholders and images with text placeholders
- Post-processing to ensure compatible embedding dimensions

Sources: [fastembed/late\_interaction\_multimodal/colpali.py35-45](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L35-L45) [fastembed/late\_interaction\_multimodal/colpali.py162-206](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L162-L206)

## Embedding Process Flow

The embedding process for multimodal models follows a similar pattern for both text and images:

```
```

Sources: [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py86-224](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L86-L224) [fastembed/late\_interaction\_multimodal/colpali.py162-173](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L162-L173) [fastembed/late\_interaction\_multimodal/colpali.py208-272](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L208-L272)

## Key Components of Multimodal Processing

### Text Preprocessing

When embedding text, ColPali:

1. Prefixes queries with `QUERY_PREFIX` and `BOS_TOKEN`
2. Tokenizes the text
3. Adds query marker tokens
4. Adds empty image placeholders to ensure the model handles text-only input correctly

```
```

Sources: [fastembed/late\_interaction\_multimodal/colpali.py162-166](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L162-L166) [fastembed/late\_interaction\_multimodal/colpali.py172-186](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L172-L186)

### Image Preprocessing

When embedding images, ColPali:

1. Processes the images using the image processor
2. Adds empty text placeholders to ensure the model handles image-only input correctly

```
```

Sources: [fastembed/late\_interaction\_multimodal/colpali.py189-204](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L189-L204) [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py162-174](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L162-L174)

## Parallel Processing Support

Multimodal embedding supports efficient parallel processing for large datasets:

1. When `parallel` parameter is set, the system creates a `ParallelWorkerPool`
2. For text embedding, it uses `ColPaliTextEmbeddingWorker` workers
3. For image embedding, it uses `ColPaliImageEmbeddingWorker` workers
4. Each worker processes a batch of inputs in parallel, significantly improving throughput

Sources: [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py152-160](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L152-L160) [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py215-223](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L215-L223) [fastembed/late\_interaction\_multimodal/colpali.py283-300](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L283-L300)

## Usage Example

Here's how to use the multimodal embedding functionality:

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py86-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L86-L130)

## Integration with Vector Databases

The multimodal embeddings produced by FastEmbed are compatible with vector database systems like Qdrant. The embeddings from both text and images can be stored in the same collection, enabling cross-modal search (finding images with text queries or finding text with image queries).

For more information on integrating FastEmbed with Qdrant, see [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md).

Sources: [fastembed/late\_interaction\_multimodal/colpali.py22-30](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L22-L30)

## Future Development

The architecture of FastEmbed's multimodal implementation is designed for extensibility. New multimodal models can be added by:

1. Creating a new class that extends `LateInteractionMultimodalEmbeddingBase` and `OnnxMultimodalModel`
2. Implementing the required methods for text and image embedding
3. Adding the new class to the `EMBEDDINGS_REGISTRY` in `LateInteractionMultimodalEmbedding`

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py15-16](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L15-L16) [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py66-79](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L66-L79)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Multimodal Models](#multimodal-models.md)
- [Architecture Overview](#architecture-overview.md)
- [Supported Models](#supported-models.md)
- [Implementation Details](#implementation-details.md)
- [Class Hierarchy](#class-hierarchy.md)
- [The ColPali Implementation](#the-colpali-implementation.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Key Components of Multimodal Processing](#key-components-of-multimodal-processing.md)
- [Text Preprocessing](#text-preprocessing.md)
- [Image Preprocessing](#image-preprocessing.md)
- [Parallel Processing Support](#parallel-processing-support.md)
- [Usage Example](#usage-example.md)
- [Integration with Vector Databases](#integration-with-vector-databases.md)
- [Future Development](#future-development.md)
