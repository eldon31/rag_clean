ONNX Runtime Integration | qdrant/fastembed | DeepWiki

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

# ONNX Runtime Integration

Relevant source files

- [fastembed/common/onnx\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py)
- [fastembed/image/onnx\_image\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_image_model.py)
- [fastembed/parallel\_processor.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py)
- [fastembed/rerank/cross\_encoder/onnx\_text\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py)
- [fastembed/text/onnx\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py)
- [fastembed/text/onnx\_text\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_text_model.py)

This document explains how FastEmbed leverages ONNX Runtime to achieve efficient inference for embedding generation. ONNX Runtime integration is a core component of FastEmbed's architecture that enables high-performance model execution across different hardware configurations and model types.

For information about parallel processing capabilities, see [Parallel Processing](qdrant/fastembed/4.3-parallel-processing.md).

## Overview of ONNX in FastEmbed

FastEmbed uses ONNX Runtime as its underlying inference engine for all embedding models. This provides substantial performance benefits over traditional PyTorch or TensorFlow implementations while maintaining compatibility with models originally trained in those frameworks.

```
```

Sources: [fastembed/common/onnx\_model.py26-109](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L26-L109) [fastembed/text/onnx\_text\_model.py17-91](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_text_model.py#L17-L91) [fastembed/image/onnx\_image\_model.py21-79](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_image_model.py#L21-L79) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py21-77](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L21-L77)

## ONNX Model Hierarchy

FastEmbed implements a hierarchical structure for its ONNX-based models, with a common base class and specialized subclasses for different modalities.

### Base Class: OnnxModel

The `OnnxModel` class serves as the foundation for all ONNX-based models in FastEmbed. It provides:

- Generic ONNX session management
- Provider configuration
- Common input/output processing interfaces
- Base methods for model loading and inference

```
```

Sources: [fastembed/common/onnx\_model.py26-112](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L26-L112) [fastembed/text/onnx\_text\_model.py17-91](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_text_model.py#L17-L91) [fastembed/image/onnx\_image\_model.py21-79](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_image_model.py#L21-L79) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py21-146](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L21-L146)

## ONNX Session Configuration

FastEmbed offers flexible configuration of ONNX Runtime sessions, enabling users to optimize for their specific hardware and performance requirements.

### Provider Selection

The library allows specifying which ONNX Runtime execution providers to use:

```
```

Sources: [fastembed/common/onnx\_model.py46-106](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L46-L106)

### Session Options and Optimization

FastEmbed applies several optimizations to the ONNX Runtime session:

- Sets graph optimization level to `ORT_ENABLE_ALL`
- Configures thread counts for intra-op and inter-op parallelism when specified
- Validates providers against available execution providers in the runtime

```
```

Sources: [fastembed/common/onnx\_model.py86-95](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L86-L95)

## Inference Pipeline

The ONNX-based inference pipeline in FastEmbed follows a consistent pattern across different model types, with modality-specific preprocessing and postprocessing steps.

```
```

Sources: [fastembed/text/onnx\_text\_model.py62-90](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_text_model.py#L62-L90) [fastembed/image/onnx\_image\_model.py63-79](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_image_model.py#L63-L79) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py66-77](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L66-L77)

### Text Model Inference

For text models, the inference process includes:

1. Tokenization of input text documents
2. Conversion of tokens to input tensors (input\_ids, attention\_mask, etc.)
3. Model inference via ONNX Runtime
4. Post-processing of output embeddings (first token extraction, normalization)

```
```

Sources: [fastembed/text/onnx\_text\_model.py65-90](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_text_model.py#L65-L90) [fastembed/text/onnx\_embedding.py298-315](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L298-L315)

### Image Model Inference

For image models, the inference process includes:

1. Loading and preprocessing images
2. Building ONNX input dictionary
3. Model inference via ONNX Runtime
4. Reshaping and post-processing output embeddings

Sources: [fastembed/image/onnx\_image\_model.py63-79](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/image/onnx_image_model.py#L63-L79)

## GPU Acceleration

FastEmbed provides support for GPU acceleration through ONNX Runtime's CUDA execution provider.

### CUDA Configuration

Users can enable CUDA execution by:

1. Setting the `cuda=True` parameter during model initialization
2. Specifying `device_id` for particular GPU selection
3. Providing multiple `device_ids` for parallel processing

```
```

Sources: [fastembed/common/onnx\_model.py58-73](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L58-L73)

### Multi-GPU Support

For parallel processing across multiple GPUs, FastEmbed provides:

1. Device ID specification through `device_ids` parameter
2. Worker process allocation to specific GPUs
3. Load balancing across available GPUs

```
```

Sources: [fastembed/parallel\_processor.py120-126](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L120-L126)

## Supported Models and Formats

FastEmbed supports various ONNX-optimized embedding models with different dimensions and purposes.

| Model                               | Dimension | Description               | Type  |
| ----------------------------------- | --------- | ------------------------- | ----- |
| BAAI/bge-small-en-v1.5              | 384       | English text embeddings   | Dense |
| BAAI/bge-base-en-v1.5               | 768       | English text embeddings   | Dense |
| BAAI/bge-large-en-v1.5              | 1024      | English text embeddings   | Dense |
| snowflake/snowflake-arctic-embed-\* | 384-1024  | English text embeddings   | Dense |
| jinaai/jina-clip-v1                 | 768       | Multimodal (text & image) | Dense |
| ... and others                      |           |                           |       |

Sources: [fastembed/text/onnx\_embedding.py10-183](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L10-L183)

## Implementation Details

### Model Loading and Caching

The ONNX model loading process includes:

1. Model download and caching
2. Loading the ONNX model file
3. Setting up the ONNX Runtime session with appropriate providers
4. Loading supporting components (tokenizers, image processors)

Sources: [fastembed/text/onnx\_embedding.py248-325](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L248-L325)

### Lazy Loading

FastEmbed supports lazy loading of ONNX models, which defers model loading until the first inference request. This is particularly useful for multi-GPU scenarios where models should be loaded in worker processes.

```
```

Sources: [fastembed/text/onnx\_embedding.py256-258](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L256-L258)

### Error Handling

FastEmbed includes error handling for ONNX Runtime provider configuration:

1. Validation of requested providers against available providers
2. Warning for CUDA provider failures
3. Suggestion for CUDA 12.x compatibility

```
```

Sources: [fastembed/common/onnx\_model.py96-105](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L96-L105)

## Integration with Embedding Classes

The ONNX Runtime integration is exposed through higher-level embedding classes that provide user-friendly interfaces for generating embeddings:

```
```

Sources: [fastembed/text/onnx\_embedding.py186-340](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L186-L340) [fastembed/common/onnx\_model.py114-136](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L114-L136) [fastembed/parallel\_processor.py26-34](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L26-L34)

## Conclusion

The ONNX Runtime integration in FastEmbed provides significant performance benefits through:

1. Hardware-specific optimizations via execution providers
2. Efficient model loading and caching
3. Support for parallel and distributed processing
4. Consistent API across different model types and modalities

By leveraging ONNX Runtime's capabilities, FastEmbed achieves faster inference speeds compared to traditional embedding frameworks, making it suitable for production environments where performance is critical.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [ONNX Runtime Integration](#onnx-runtime-integration.md)
- [Overview of ONNX in FastEmbed](#overview-of-onnx-in-fastembed.md)
- [ONNX Model Hierarchy](#onnx-model-hierarchy.md)
- [Base Class: OnnxModel](#base-class-onnxmodel.md)
- [ONNX Session Configuration](#onnx-session-configuration.md)
- [Provider Selection](#provider-selection.md)
- [Session Options and Optimization](#session-options-and-optimization.md)
- [Inference Pipeline](#inference-pipeline.md)
- [Text Model Inference](#text-model-inference.md)
- [Image Model Inference](#image-model-inference.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [CUDA Configuration](#cuda-configuration.md)
- [Multi-GPU Support](#multi-gpu-support.md)
- [Supported Models and Formats](#supported-models-and-formats.md)
- [Implementation Details](#implementation-details.md)
- [Model Loading and Caching](#model-loading-and-caching.md)
- [Lazy Loading](#lazy-loading.md)
- [Error Handling](#error-handling.md)
- [Integration with Embedding Classes](#integration-with-embedding-classes.md)
- [Conclusion](#conclusion.md)
