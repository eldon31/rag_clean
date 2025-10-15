ImageEmbedding | qdrant/fastembed | DeepWiki

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

# ImageEmbedding

Relevant source files

- [README.md](https://github.com/qdrant/fastembed/blob/b785640b/README.md)
- [docs/examples/FastEmbed\_GPU.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb)
- [fastembed/image/onnx\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py)

## Purpose and Scope

The `ImageEmbedding` class provides a high-level interface for generating vector representations (embeddings) from images. These embeddings can be used for various tasks including image search, image similarity, and multimodal applications. The class offers a simplified API while leveraging ONNX Runtime for efficient inference.

For text embedding functionality, see [TextEmbedding](qdrant/fastembed/3.1-textembedding.md). For multimodal embedding that combines both text and images, see [LateInteractionMultimodalEmbedding](qdrant/fastembed/3.5-lateinteractionmultimodalembedding.md).

Sources: [README.md137-156](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L137-L156)

## Architecture Overview

`ImageEmbedding` serves as an entry point class that abstracts the underlying implementation details of image embedding models. The class follows FastEmbed's pattern of providing a clean, user-friendly interface while leveraging optimized implementations underneath.

### Class Hierarchy

```
```

Sources: [fastembed/image/onnx\_embedding.py1-10](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L1-L10)

## Supported Models

`ImageEmbedding` supports several pre-trained models optimized for ONNX runtime:

| Model                       | Dimensions | Description                              | Year | License    |
| --------------------------- | ---------- | ---------------------------------------- | ---- | ---------- |
| Qdrant/clip-ViT-B-32-vision | 512        | Multimodal (text & image)                | 2021 | MIT        |
| Qdrant/resnet50-onnx        | 2048       | Unimodal (image only)                    | 2016 | Apache-2.0 |
| Qdrant/Unicom-ViT-B-16      | 768        | Multimodal with detailed representations | 2023 | Apache-2.0 |
| Qdrant/Unicom-ViT-B-32      | 512        | Multimodal (text & image)                | 2023 | Apache-2.0 |
| jinaai/jina-clip-v1         | 768        | Multimodal (text & image)                | 2024 | Apache-2.0 |

Sources: [fastembed/image/onnx\_embedding.py13-59](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L13-L59)

## Basic Usage

Using `ImageEmbedding` is straightforward:

```
```

Sources: [README.md137-156](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L137-L156)

## Embedding Process

The image embedding process consists of several steps:

```
```

Sources: [fastembed/image/onnx\_embedding.py148-181](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L148-L181)

## Class Initialization Parameters

When initializing an `ImageEmbedding` instance, you can customize its behavior with several parameters:

```
```

### Key Parameters

- `model_name`: The name of the embedding model to use
- `cache_dir`: Custom location for storing downloaded models
- `providers`: ONNX runtime providers (e.g., "CUDAExecutionProvider" for GPU)
- `cuda`: Enable CUDA for inference
- `device_ids`: List of GPU device IDs for parallel processing

Sources: [fastembed/image/onnx\_embedding.py63-96](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L63-L96)

## GPU Acceleration

`ImageEmbedding` supports GPU acceleration through ONNX Runtime's CUDA Execution Provider. To use GPU acceleration:

1. Install the GPU version of FastEmbed:

   ```
   ```

2. Initialize the model with GPU support:

   ```
   ```

Sources: [docs/examples/FastEmbed\_GPU.ipynb1-108](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L1-L108) [docs/examples/FastEmbed\_GPU.ipynb184-229](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L184-L229)

## Embedding Method Parameters

The `embed` method accepts several parameters to control the embedding process:

```
```

### Key Parameters

- `images`: List of image paths or image objects to embed

- `batch_size`: Number of images to process in a single batch (higher values use more memory)

- `parallel`: Number of parallel workers for data-parallel processing

  - If > 1, that many workers will be used
  - If 0, all available cores will be used
  - If None, parallel processing is disabled

Sources: [fastembed/image/onnx\_embedding.py148-169](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L148-L169)

## Implementation Details

### Embedding Process Flow

```
```

Sources: [fastembed/image/onnx\_embedding.py148-181](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L148-L181) [fastembed/image/onnx\_embedding.py125-136](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L125-L136) [fastembed/image/onnx\_embedding.py187-197](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L187-L197)

### Normalization

After obtaining raw embeddings from the model, they are normalized to unit length to ensure consistent similarity calculations.

Sources: [fastembed/image/onnx\_embedding.py196-197](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L196-L197)

## Integration with Qdrant

FastEmbed's `ImageEmbedding` can be easily integrated with Qdrant vector database for image search applications:

```
```

For more detailed information on using FastEmbed with Qdrant, see [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md).

Sources: [README.md232-280](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L232-L280)

## Performance Considerations

- **Batch Size**: Larger batch sizes generally improve throughput but increase memory usage.
- **Parallel Processing**: For large datasets, enabling parallel processing (`parallel > 0`) can significantly improve performance.
- **GPU Acceleration**: Using GPU acceleration can provide substantial speedups, especially for batch processing.
- **Model Selection**: Different models offer different trade-offs between accuracy, embedding dimension, and speed.

Sources: [docs/examples/FastEmbed\_GPU.ipynb398-512](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L398-L512)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [ImageEmbedding](#imageembedding.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Architecture Overview](#architecture-overview.md)
- [Class Hierarchy](#class-hierarchy.md)
- [Supported Models](#supported-models.md)
- [Basic Usage](#basic-usage.md)
- [Embedding Process](#embedding-process.md)
- [Class Initialization Parameters](#class-initialization-parameters.md)
- [Key Parameters](#key-parameters.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Embedding Method Parameters](#embedding-method-parameters.md)
- [Key Parameters](#key-parameters-1.md)
- [Implementation Details](#implementation-details.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Normalization](#normalization.md)
- [Integration with Qdrant](#integration-with-qdrant.md)
- [Performance Considerations](#performance-considerations.md)
