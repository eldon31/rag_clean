Image Embedding | qdrant/fastembed | DeepWiki

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

# Image Embedding

Relevant source files

- [README.md](https://github.com/qdrant/fastembed/blob/b785640b/README.md)
- [docs/examples/FastEmbed\_GPU.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb)
- [fastembed/image/onnx\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py)

This page documents the image embedding capabilities of the FastEmbed library. FastEmbed provides efficient mechanisms for generating vector representations (embeddings) from images using optimized ONNX models. For text embedding functionality, see [TextEmbedding](qdrant/fastembed/3.1-textembedding.md), and for multimodal embedding, see [LateInteractionMultimodalEmbedding](qdrant/fastembed/3.5-lateinteractionmultimodalembedding.md).

## Overview

The `ImageEmbedding` class is a high-level interface for generating embeddings from images. It leverages ONNX Runtime for efficient inference and supports various vision models. Image embeddings can be used for image search, similarity comparison, and as input to multimodal systems.

```
```

Sources: [fastembed/image/onnx\_embedding.py62-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L62-L65)

## Supported Models

FastEmbed supports several vision models for image embedding, each with different characteristics, dimensions, and applications:

| Model Name                  | Dimensions | Type       | Year | Description                                  |
| --------------------------- | ---------- | ---------- | ---- | -------------------------------------------- |
| Qdrant/clip-ViT-B-32-vision | 512        | Multimodal | 2021 | Image embeddings from CLIP model             |
| Qdrant/resnet50-onnx        | 2048       | Unimodal   | 2016 | Image-only embeddings using ResNet50         |
| Qdrant/Unicom-ViT-B-16      | 768        | Multimodal | 2023 | Detailed image embeddings, higher resolution |
| Qdrant/Unicom-ViT-B-32      | 512        | Multimodal | 2023 | Efficient image embeddings                   |
| jinaai/jina-clip-v1         | 768        | Multimodal | 2024 | Recent multimodal embedding model            |

```
```

Sources: [fastembed/image/onnx\_embedding.py13-59](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L13-L59)

## Image Embedding Process

The image embedding process in FastEmbed follows several steps from input to embedding generation:

```
```

Sources: [fastembed/image/onnx\_embedding.py148-181](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L148-L181)

## Basic Usage

You can generate image embeddings with just a few lines of code:

```
```

The `embed()` method returns a generator that yields numpy arrays, which can be converted to a list as shown above.

Sources: [README.md137-155](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L137-L155)

## Configuration Options

The `ImageEmbedding` class provides several configuration options:

```
```

Key parameters include:

- `model_name`: Name of the model to use (required)
- `cache_dir`: Directory to store downloaded models (optional)
- `threads`: Number of threads for inference (optional)
- `providers`: ONNX Runtime execution providers (optional)
- `cuda`: Whether to use CUDA for inference (optional)
- `device_ids`: List of device IDs for parallel processing (optional)
- `lazy_load`: Whether to defer model loading until needed (optional)

The `embed()` method also accepts parameters:

- `images`: Images to embed (required)
- `batch_size`: Number of images to process at once (default: 16)
- `parallel`: Number of worker processes for parallelization (optional)

Sources: [fastembed/image/onnx\_embedding.py63-96](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L63-L96) [fastembed/image/onnx\_embedding.py148-166](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L148-L166)

## GPU Acceleration

For faster image embedding, FastEmbed supports GPU acceleration through ONNX Runtime:

1. Install with GPU support:

   ```
   ```

2. Specify CUDA execution provider:

   ```
   ```

GPU acceleration can significantly improve performance, especially for large batches of images.

Sources: [README.md210-230](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L210-L230) [docs/examples/FastEmbed\_GPU.ipynb1-193](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L1-L193)

## Integration with Qdrant

FastEmbed's image embedding can be easily integrated with Qdrant vector database:

```
```

Sources: [README.md232-281](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L232-L281)

## Implementation Details

The `OnnxImageEmbedding` class inherits from both `ImageEmbeddingBase` and `OnnxImageModel[NumpyArray]`. It manages model downloading, caching, and inference operations. The actual embedding generation is delegated to ONNX Runtime, which provides efficient execution on both CPU and GPU.

For parallel processing, the class utilizes `OnnxImageEmbeddingWorker`, which initializes separate model instances in worker processes to handle embedding generation in parallel.

The embedding vectors are normalized after model inference to ensure they have unit length, which is important for cosine similarity calculations in vector search.

Sources: [fastembed/image/onnx\_embedding.py62-198](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_embedding.py#L62-L198)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Image Embedding](#image-embedding.md)
- [Overview](#overview.md)
- [Supported Models](#supported-models.md)
- [Image Embedding Process](#image-embedding-process.md)
- [Basic Usage](#basic-usage.md)
- [Configuration Options](#configuration-options.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Integration with Qdrant](#integration-with-qdrant.md)
- [Implementation Details](#implementation-details.md)
