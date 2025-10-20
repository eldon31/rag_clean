LateInteractionMultimodalEmbedding | qdrant/fastembed | DeepWiki

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

# LateInteractionMultimodalEmbedding

Relevant source files

- [fastembed/\_\_init\_\_.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/__init__.py)
- [fastembed/late\_interaction\_multimodal/colpali.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py)
- [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py)
- [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding_base.py)
- [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py)
- [tests/test\_late\_interaction\_multimodal.py](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_late_interaction_multimodal.py)

## Purpose and Overview

The `LateInteractionMultimodalEmbedding` class provides a unified interface for generating and working with late interaction embeddings across multiple modalities (specifically text and images). Late interaction embedding models produce token-level embeddings rather than single dense vectors, enabling more precise matching between queries and documents. The multimodal capability allows for cross-modal retrieval applications like searching images with text queries or vice versa.

For text-only late interaction embeddings, see [LateInteractionTextEmbedding](qdrant/fastembed/3.3-lateinteractiontextembedding.md).

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py1-131](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L1-L131) [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding\_base.py1-68](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding_base.py#L1-L68)

## Architecture

The `LateInteractionMultimodalEmbedding` system is designed with a factory pattern that delegates to specialized implementations based on the selected model. Currently, the system supports the ColPali model, but the architecture allows for easy extension with additional multimodal late interaction models.

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py14-16](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L14-L16) [fastembed/late\_interaction\_multimodal/colpali.py34-131](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L34-L131) [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py20-83](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L20-L83)

## Embedding Process Flow

The late interaction multimodal embedding process uses specialized token-level encoders for both text and images, combining the power of late interaction with multimodal capabilities.

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py86-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L86-L130) [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py86-223](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L86-L223)

## Supported Models

Currently, the `LateInteractionMultimodalEmbedding` class supports the following model:

| Model                    | Dimensions | Description                                                                            | License | Size   |
| ------------------------ | ---------- | -------------------------------------------------------------------------------------- | ------- | ------ |
| Qdrant/colpali-v1.3-fp16 | 128        | Text embeddings, Multimodal (text & image), English, 50 tokens query length truncation | MIT     | 6.5 GB |

The ColPali model is designed for late interaction retrieval between text and images, enabling efficient cross-modal search capabilities.

Sources: [fastembed/late\_interaction\_multimodal/colpali.py20-31](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L20-L31)

## Implementation Details

### ColPali

The ColPali implementation uses an ONNX-optimized model architecture that captures token-level embeddings for both text and images. It has several important components:

1. **Text Processing**:

   - Adds specific prefix and tokens to text queries
   - Tokenizes text with a specialized tokenizer
   - Preprocesses tokenized text for ONNX inference

2. **Image Processing**:

   - Uses a standardized image preprocessor
   - Converts images to the expected format (3x448x448)
   - Adds placeholders for text when processing images

3. **Model Output**:

   - Token-level embeddings rather than a single vector
   - Preserves contextual information for more precise matching

Sources: [fastembed/late\_interaction\_multimodal/colpali.py34-190](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L34-L190)

### Parallel Processing Support

The system supports parallel processing for both text and image embedding to improve throughput when dealing with large datasets:

```
```

Sources: [fastembed/late\_interaction\_multimodal/onnx\_multimodal\_model.py113-223](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/onnx_multimodal_model.py#L113-L223) [fastembed/late\_interaction\_multimodal/colpali.py275-300](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L275-L300)

## Usage

### Initializing the Embedder

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py54-84](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L54-L84)

### Embedding Text

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py86-107](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L86-L107)

### Embedding Images

```
```

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py109-130](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L109-L130) [tests/test\_late\_interaction\_multimodal.py40-45](https://github.com/qdrant/fastembed/blob/b785640b/tests/test_late_interaction_multimodal.py#L40-L45)

## Key Parameters

| Parameter    | Description                                        | Default                 |
| ------------ | -------------------------------------------------- | ----------------------- |
| `model_name` | The name of the multimodal model to use            | Required                |
| `cache_dir`  | Directory to cache downloaded models               | System temp directory   |
| `threads`    | Number of threads for single ONNX session          | None (auto)             |
| `cuda`       | Whether to use CUDA for inference                  | False                   |
| `device_ids` | List of device IDs for parallel processing         | None                    |
| `lazy_load`  | Whether to load the model on demand                | False                   |
| `batch_size` | Number of items to process together                | 256 (text), 16 (images) |
| `parallel`   | Number of worker processes for parallel processing | None                    |

Sources: [fastembed/late\_interaction\_multimodal/late\_interaction\_multimodal\_embedding.py54-84](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/late_interaction_multimodal_embedding.py#L54-L84) [fastembed/late\_interaction\_multimodal/colpali.py46-78](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L46-L78)

## Notes on Token-Level Embeddings

Unlike traditional dense embeddings that produce a single vector per input, late interaction models like ColPali produce token-level embeddings. This means:

1. Each token in the text or image gets its own embedding vector
2. The output shape is (batch\_size, sequence\_length, embedding\_dimension)
3. These token-level embeddings enable more fine-grained matching between queries and documents

For multimodal late interaction, this token-level approach allows precise matching between text tokens and image regions, enabling more accurate cross-modal retrieval.

Sources: [fastembed/late\_interaction\_multimodal/colpali.py129-160](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/colpali.py#L129-L160)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [LateInteractionMultimodalEmbedding](#lateinteractionmultimodalembedding.md)
- [Purpose and Overview](#purpose-and-overview.md)
- [Architecture](#architecture.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Supported Models](#supported-models.md)
- [Implementation Details](#implementation-details.md)
- [ColPali](#colpali.md)
- [Parallel Processing Support](#parallel-processing-support.md)
- [Usage](#usage.md)
- [Initializing the Embedder](#initializing-the-embedder.md)
- [Embedding Text](#embedding-text.md)
- [Embedding Images](#embedding-images.md)
- [Key Parameters](#key-parameters.md)
- [Notes on Token-Level Embeddings](#notes-on-token-level-embeddings.md)
