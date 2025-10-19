Core Embedding Classes | qdrant/fastembed | DeepWiki

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

# Core Embedding Classes

Relevant source files

- [NOTICE](https://github.com/qdrant/fastembed/blob/b785640b/NOTICE)
- [README.md](https://github.com/qdrant/fastembed/blob/b785640b/README.md)
- [docs/examples/FastEmbed\_GPU.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb)
- [docs/examples/Supported\_Models.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb)
- [fastembed/embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/embedding.py)
- [fastembed/late\_interaction\_multimodal/\_\_init\_\_.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/__init__.py)

This page provides an overview of the main embedding classes in FastEmbed, which serve as primary interfaces for generating embeddings from different types of data. Each class is designed for a specific embedding strategy, offering a balance of simplicity and performance through ONNX Runtime integration.

For detailed information about how to use each class with specific examples, see [Usage Examples](qdrant/fastembed/7-usage-examples.md).

## Class Hierarchy

The FastEmbed library is built around a hierarchical architecture of embedding classes, providing specialized functionality for different embedding strategies and data types.

```
```

Sources: [fastembed/embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/embedding.py)

## Overview of Core Classes

The core embedding classes in FastEmbed can be categorized based on the type of embeddings they generate and the modalities they support:

| Class                              | Embedding Type   | Input Type    | Primary Use Cases                             |
| ---------------------------------- | ---------------- | ------------- | --------------------------------------------- |
| TextEmbedding                      | Dense            | Text          | Semantic search, document retrieval           |
| SparseTextEmbedding                | Sparse           | Text          | Lexical search, hybrid search                 |
| LateInteractionTextEmbedding       | Token-level      | Text          | Precise text matching, complex queries        |
| ImageEmbedding                     | Dense            | Images        | Image search, visual similarity               |
| LateInteractionMultimodalEmbedding | Token-level      | Text & Images | Cross-modal search, visual question answering |
| TextCrossEncoder                   | Relevance scores | Text pairs    | Result reranking, relevance judgment          |

Sources: [README.md49-156](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L49-L156)

## Dense Text Embeddings with TextEmbedding

The `TextEmbedding` class is the primary interface for generating dense vector representations of text. It creates fixed-length vectors that capture semantic meaning.

```
```

### Key Features

- Supports various embedding models with different dimensions and language capabilities
- Automatically handles model downloading and caching
- Provides parallel processing capabilities for handling large datasets
- Supports GPU acceleration through ONNX Runtime

### Basic Usage Example

```
```

For detailed usage examples, see [Basic Text Embedding](qdrant/fastembed/7.1-basic-text-embedding.md).

Sources: [README.md29-47](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L29-L47) [docs/examples/Supported\_Models.ipynb56-129](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L56-L129)

## Sparse Text Embeddings with SparseTextEmbedding

The `SparseTextEmbedding` class generates sparse vector representations where most values are zero, making them efficient for large vocabularies and well-suited for lexical matching.

```
```

### Key Features

- Returns sparse embeddings as pairs of indices (token IDs) and values (weights)
- Supports both neural sparse models (SPLADE) and statistical approaches (BM25)
- Complements dense embeddings for hybrid search scenarios
- Some models (BM25, BM42) require IDF statistics for optimal performance

### Basic Usage Example

```
```

For detailed usage examples, see [Sparse and Hybrid Search](qdrant/fastembed/7.2-sparse-and-hybrid-search.md).

Sources: [README.md85-99](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L85-L99) [docs/examples/Supported\_Models.ipynb370-413](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L370-L413)

## Late Interaction Text Embeddings with LateInteractionTextEmbedding

The `LateInteractionTextEmbedding` class implements the ColBERT approach, which creates token-level embeddings to enable fine-grained matching between queries and documents.

```
```

### Key Features

- Generates a sequence of embeddings for each token rather than a single vector
- Allows for more precise matching by comparing individual token representations
- Maintains context through token-level embeddings
- Typically used with specialized retrieval approaches

### Basic Usage Example

```
```

For detailed usage examples, see [ColBERT and Late Interaction](qdrant/fastembed/7.3-colbert-and-late-interaction.md).

Sources: [README.md117-136](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L117-L136) [docs/examples/Supported\_Models.ipynb492-600](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L492-L600)

## Image Embeddings with ImageEmbedding

The `ImageEmbedding` class generates vector representations of images, allowing for image similarity search and visual retrieval.

```
```

### Key Features

- Supports loading images from file paths or PIL Image objects
- Automatically handles image preprocessing (resizing, normalization)
- Integrates with vision-language models like CLIP
- Returns fixed-length vector representations of images

### Basic Usage Example

```
```

For detailed usage examples, see [Image Embedding](qdrant/fastembed/7.4-image-embedding.md).

Sources: [README.md138-155](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L138-L155) [docs/examples/Supported\_Models.ipynb603-714](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L603-L714)

## Multimodal Embeddings with LateInteractionMultimodalEmbedding

The `LateInteractionMultimodalEmbedding` class enables cross-modal retrieval through models that can embed both text and images in a compatible latent space.

```
```

### Key Features

- Supports both text and image inputs through separate embedding methods
- Uses late interaction approach similar to ColBERT
- Primarily implements the ColPali model for multimodal retrieval
- Enables complex queries involving both textual and visual elements

### Basic Usage Example

```
```

Sources: [README.md157-176](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L157-L176) [NOTICE16-19](https://github.com/qdrant/fastembed/blob/b785640b/NOTICE#L16-L19) [fastembed/late\_interaction\_multimodal/\_\_init\_\_.py1-5](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/__init__.py#L1-L5)

## Text Cross-Encoder with TextCrossEncoder

The `TextCrossEncoder` class implements cross-encoder models for reranking search results by directly scoring the relevance of query-document pairs.

```
```

### Key Features

- Returns relevance scores for query-document pairs instead of embeddings
- Designed specifically for reranking results after initial retrieval
- More accurate but computationally expensive compared to embedding similarity
- Efficient implementation through ONNX Runtime

### Basic Usage Example

```
```

Sources: [README.md178-208](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L178-L208) [docs/examples/Supported\_Models.ipynb717-836](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L717-L836)

## GPU Acceleration

All the core embedding classes support GPU acceleration through ONNX Runtime's CUDA execution provider, which can significantly improve performance, especially for batch processing.

### Enabling GPU Support

To use GPU acceleration:

1. Install the GPU-enabled version of FastEmbed:

   ```
   ```

2. Specify the CUDA execution provider when initializing the embedding model:

   ```
   ```

For detailed GPU setup instructions and troubleshooting, see [FastEmbed GPU](qdrant/fastembed/8-performance-optimization.md).

Sources: [README.md210-230](https://github.com/qdrant/fastembed/blob/b785640b/README.md#L210-L230) [docs/examples/FastEmbed\_GPU.ipynb1-42](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L1-L42) [docs/examples/FastEmbed\_GPU.ipynb90-108](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_GPU.ipynb#L90-L108)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Core Embedding Classes](#core-embedding-classes.md)
- [Class Hierarchy](#class-hierarchy.md)
- [Overview of Core Classes](#overview-of-core-classes.md)
- [Dense Text Embeddings with TextEmbedding](#dense-text-embeddings-with-textembedding.md)
- [Key Features](#key-features.md)
- [Basic Usage Example](#basic-usage-example.md)
- [Sparse Text Embeddings with SparseTextEmbedding](#sparse-text-embeddings-with-sparsetextembedding.md)
- [Key Features](#key-features-1.md)
- [Basic Usage Example](#basic-usage-example-1.md)
- [Late Interaction Text Embeddings with LateInteractionTextEmbedding](#late-interaction-text-embeddings-with-lateinteractiontextembedding.md)
- [Key Features](#key-features-2.md)
- [Basic Usage Example](#basic-usage-example-2.md)
- [Image Embeddings with ImageEmbedding](#image-embeddings-with-imageembedding.md)
- [Key Features](#key-features-3.md)
- [Basic Usage Example](#basic-usage-example-3.md)
- [Multimodal Embeddings with LateInteractionMultimodalEmbedding](#multimodal-embeddings-with-lateinteractionmultimodalembedding.md)
- [Key Features](#key-features-4.md)
- [Basic Usage Example](#basic-usage-example-4.md)
- [Text Cross-Encoder with TextCrossEncoder](#text-cross-encoder-with-textcrossencoder.md)
- [Key Features](#key-features-5.md)
- [Basic Usage Example](#basic-usage-example-5.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Enabling GPU Support](#enabling-gpu-support.md)
