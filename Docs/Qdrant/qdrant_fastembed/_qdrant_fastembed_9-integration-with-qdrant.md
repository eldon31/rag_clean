Integration with Qdrant | qdrant/fastembed | DeepWiki

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

# Integration with Qdrant

Relevant source files

- [README.md](https://github.com/qdrant/fastembed/blob/b785640b/README.md)
- [docs/examples/FastEmbed\_GPU.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb)

## Purpose and Scope

This document explains how to integrate the FastEmbed library with Qdrant, a vector database designed for efficient similarity search. FastEmbed generates embeddings, and Qdrant stores and searches them. This integration allows for seamless vector search capabilities in your applications, combining FastEmbed's efficient embedding generation with Qdrant's optimized vector storage and retrieval.

## Overview of the Integration

FastEmbed and Qdrant work together to provide an end-to-end solution for vector search. FastEmbed generates high-quality embeddings from your data, and Qdrant efficiently stores and searches these embeddings.

```
```

Sources: [README.md230-281](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L230-L281)

## Installation

To use FastEmbed with Qdrant, you need to install the Qdrant client with FastEmbed support:

```
```

On some shells like zsh, you might need to use quotes:

```
```

Sources: [README.md236-246](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L236-L246)

## Basic Usage

### Initializing the Client

```
```

### Adding Documents with Automatic Embedding

The integration provides a simplified workflow where Qdrant client handles embedding generation internally:

```
```

Code example:

```
```

### Searching for Similar Documents

```
```

Sources: [README.md247-281](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L247-L281)

## Model Configuration

By default, the integration uses FastEmbed's default embedding model. You can customize this:

```
```

Sources: [README.md263-265](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L263-L265)

## Integration Architecture

The following diagram illustrates how the integration works at a technical level:

```
```

Sources: [README.md230-281](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L230-L281)

## Performance Considerations

### GPU Acceleration

If you're working with large datasets or need real-time embedding generation, you can use GPU acceleration:

1. Install with GPU support: `pip install qdrant-client[fastembed-gpu]`
2. Ensure you have the proper CUDA drivers installed

See the [FastEmbed GPU documentation](qdrant/fastembed/8-performance-optimization.md) for more details on GPU setup and requirements.

Note: GPU acceleration can significantly improve embedding generation performance, as shown in the comparison below:

| Platform | Processing Time for 500 Documents |
| -------- | --------------------------------- |
| CPU      | \~4.33 seconds                    |
| GPU      | \~43.4 milliseconds               |

This represents approximately a 100x speedup when using GPU acceleration.

Sources: [docs/examples/FastEmbed\_GPU.ipynb20-33](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L20-L33) [docs/examples/FastEmbed\_GPU.ipynb411-512](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L411-L512)

## Working with Different Embedding Types

The integration supports all embedding types available in FastEmbed:

```
```

### Dense Text Embeddings

Works with standard dense vector collections in Qdrant.

### Sparse Text Embeddings

For sparse embeddings (like SPLADE++), Qdrant stores them as sparse vectors.

### Late Interaction Models

For late interaction models (like ColBERT), Qdrant uses a multi-vector approach where multiple vectors represent a single document.

### Image Embeddings

Image embeddings are stored as dense vectors similar to text embeddings.

Sources: [README.md49-156](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L49-L156)

## Conclusion

The integration between FastEmbed and Qdrant provides a seamless way to implement vector search in your applications. By leveraging FastEmbed's efficient embedding generation and Qdrant's optimized vector storage and search capabilities, you can build powerful semantic search, recommendation systems, and other AI-powered applications.

For more information on specific embedding models, see [Supported Models](qdrant/fastembed/6-supported-models.md).

For examples of using different embedding types, see [Usage Examples](qdrant/fastembed/7-usage-examples.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Integration with Qdrant](#integration-with-qdrant.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview of the Integration](#overview-of-the-integration.md)
- [Installation](#installation.md)
- [Basic Usage](#basic-usage.md)
- [Initializing the Client](#initializing-the-client.md)
- [Adding Documents with Automatic Embedding](#adding-documents-with-automatic-embedding.md)
- [Searching for Similar Documents](#searching-for-similar-documents.md)
- [Model Configuration](#model-configuration.md)
- [Integration Architecture](#integration-architecture.md)
- [Performance Considerations](#performance-considerations.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Working with Different Embedding Types](#working-with-different-embedding-types.md)
- [Dense Text Embeddings](#dense-text-embeddings.md)
- [Sparse Text Embeddings](#sparse-text-embeddings.md)
- [Late Interaction Models](#late-interaction-models.md)
- [Image Embeddings](#image-embeddings.md)
- [Conclusion](#conclusion.md)
