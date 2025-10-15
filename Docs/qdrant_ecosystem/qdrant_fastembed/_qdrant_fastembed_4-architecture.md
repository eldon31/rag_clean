Architecture | qdrant/fastembed | DeepWiki

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

# Architecture

Relevant source files

- [fastembed/common/model\_management.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py)
- [fastembed/common/onnx\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py)
- [fastembed/parallel\_processor.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py)
- [fastembed/rerank/cross\_encoder/onnx\_text\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py)
- [fastembed/text/text\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py)

This page provides a detailed overview of FastEmbed's architecture, outlining the core components, their interactions, and the embedding generation process flow. The document covers the high-level design patterns, component responsibilities, and implementation details that enable FastEmbed's efficient embedding generation capabilities.

For information about model management specifics, see [Model Management](qdrant/fastembed/4.1-model-management.md). For details on ONNX Runtime integration, see [ONNX Runtime Integration](qdrant/fastembed/4.2-onnx-runtime-integration.md). For parallel processing implementation, see [Parallel Processing](qdrant/fastembed/4.3-parallel-processing.md).

## Core Components Overview

FastEmbed's architecture is built around several key components that work together to provide high-performance embedding generation:

```
```

Sources: [fastembed/common/model\_management.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py) [fastembed/common/onnx\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py) [fastembed/parallel\_processor.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py) [fastembed/text/text\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py)

## Model Management System

The model management system is responsible for model discovery, downloading, and caching. It ensures models are available locally for embedding operations, handling various sources (HuggingFace, Google Cloud Storage) and verifying model integrity.

```
```

Sources: [fastembed/common/model\_management.py24-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L24-L458)

The `ModelManagement` class provides methods for:

- Listing supported models (`list_supported_models`)
- Adding custom models (`add_custom_model`)
- Downloading models from various sources (`download_model`)
- Verifying model integrity through metadata validation

## ONNX Runtime Integration

FastEmbed leverages ONNX Runtime for optimized inference, providing significant performance improvements over traditional PyTorch/TensorFlow implementations.

```
```

Sources: [fastembed/common/onnx\_model.py19-137](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L19-L137) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py21-146](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L21-L146)

The `OnnxModel` class:

- Manages ONNX session creation with appropriate execution providers
- Handles model loading, input preprocessing, and output post-processing
- Supports CPU and GPU (CUDA) execution
- Provides a generic interface for different types of embeddings

## Parallel Processing Framework

FastEmbed implements efficient parallel processing through a worker pool design, enabling multi-process execution of embedding tasks for improved throughput.

```
```

Sources: [fastembed/parallel\_processor.py20-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L20-L253) [fastembed/common/onnx\_model.py114-137](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L114-L137)

The parallel processing framework provides:

- A worker pool that manages multiple processes for embedding computation
- Process-safe queues for input/output communication
- Work distribution and result collection mechanisms
- Support for ordered results (maintaining input sequence order)
- Device management for GPU acceleration

## Embedding Process Flow

The following diagram illustrates the typical flow for generating embeddings in FastEmbed:

```
```

Sources: [fastembed/text/text\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py#L8-L60) [fastembed/common/onnx\_model.py26-112](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L26-L112) [fastembed/parallel\_processor.py91-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L91-L253)

## Class Hierarchy

FastEmbed organizes its functionality through a clear class hierarchy:

```
```

Sources: [fastembed/common/model\_management.py24-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L24-L458) [fastembed/common/onnx\_model.py26-137](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L26-L137) [fastembed/parallel\_processor.py26-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L26-L253) [fastembed/text/text\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py#L8-L60) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py21-170](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L21-L170)

## Implementation Details

### Model Loading Process

The model loading process in FastEmbed follows these steps:

1. Model description is retrieved from the supported models list
2. Model is downloaded from the appropriate source (HuggingFace or GCS)
3. Model files are verified for integrity through metadata validation
4. ONNX session is created with the appropriate execution provider
5. Additional resources (like tokenizers) are loaded

Key implementations:

- `download_model()` in `ModelManagement` [fastembed/common/model\_management.py378-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L378-L458)
- `_load_onnx_model()` in `OnnxModel` [fastembed/common/onnx\_model.py46-106](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L46-L106)

### Parallel Processing Implementation

FastEmbed's parallel processing is implemented using Python's multiprocessing module:

1. A worker pool is created with a specified number of processes
2. Each worker process is initialized with the model and necessary resources
3. Input data is batched and distributed through a queue
4. Workers process batches in parallel
5. Results are collected, reordered, and returned to the user

Key implementations:

- `ParallelWorkerPool` class [fastembed/parallel\_processor.py91-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L91-L253)
- `_worker()` function [fastembed/parallel\_processor.py35-88](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L35-L88)
- `ordered_map()` method [fastembed/parallel\_processor.py142-151](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L142-L151)

### ONNX Provider Selection

FastEmbed automatically selects the appropriate ONNX execution provider based on:

| Provider         | Condition                     | Implementation                                 |
| ---------------- | ----------------------------- | ---------------------------------------------- |
| Custom Providers | Explicitly provided by user   | User-specified list of providers               |
| CUDA             | `cuda=True` in initialization | CUDAExecutionProvider with optional device\_id |
| CPU              | Default fallback              | CPUExecutionProvider                           |

Key implementation in `_load_onnx_model()` [fastembed/common/onnx\_model.py46-106](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L46-L106)

## Interface to Implementation Mapping

This table shows how the user-facing embedding classes map to their implementations:

| User API Class                     | Base Class                   | Implementation Classes                                        |
| ---------------------------------- | ---------------------------- | ------------------------------------------------------------- |
| TextEmbedding                      | TextEmbeddingBase, OnnxModel | PooledEmbedding, PooledNormalizedEmbedding, CLIPOnnxEmbedding |
| SparseTextEmbedding                | TextEmbeddingBase, OnnxModel | SpladePP, Bm25, Bm42                                          |
| LateInteractionTextEmbedding       | TextEmbeddingBase, OnnxModel | Colbert, JinaColbert                                          |
| ImageEmbedding                     | OnnxModel                    | OnnxImageEmbedding                                            |
| LateInteractionMultimodalEmbedding | OnnxModel                    | ColPali                                                       |
| TextCrossEncoder                   | OnnxModel                    | OnnxTextCrossEncoder                                          |

Sources: [fastembed/text/text\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py#L8-L60) [fastembed/common/onnx\_model.py26-137](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L26-L137) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py21-170](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L21-L170)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Architecture](#architecture.md)
- [Core Components Overview](#core-components-overview.md)
- [Model Management System](#model-management-system.md)
- [ONNX Runtime Integration](#onnx-runtime-integration.md)
- [Parallel Processing Framework](#parallel-processing-framework.md)
- [Embedding Process Flow](#embedding-process-flow.md)
- [Class Hierarchy](#class-hierarchy.md)
- [Implementation Details](#implementation-details.md)
- [Model Loading Process](#model-loading-process.md)
- [Parallel Processing Implementation](#parallel-processing-implementation.md)
- [ONNX Provider Selection](#onnx-provider-selection.md)
- [Interface to Implementation Mapping](#interface-to-implementation-mapping.md)
