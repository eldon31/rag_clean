Supported Models | qdrant/fastembed | DeepWiki

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

# Supported Models

Relevant source files

- [NOTICE](https://github.com/qdrant/fastembed/blob/b785640b/NOTICE)
- [docs/examples/Supported\_Models.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb)
- [fastembed/late\_interaction\_multimodal/\_\_init\_\_.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/__init__.py)

This page provides a comprehensive list of all embedding models supported by FastEmbed, organized by model type. FastEmbed offers a diverse range of pre-trained models for various embedding tasks, including dense text embedding, sparse text embedding, late interaction models, image embedding, and cross-encoder reranking.

## Model Types Overview

FastEmbed supports five main types of embedding models, each with specific use cases and implementations.

```
```

Sources: [docs/examples/Supported\_Models.ipynb35-45](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L35-L45)

## Dense Text Embedding Models

Dense text embedding models generate fixed-length vector representations of text, capturing semantic meaning. These models are typically used for semantic search and measuring text similarity.

```
```

Sources: [docs/examples/Supported\_Models.ipynb64-72](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L64-L72)

FastEmbed supports a wide range of dense text embedding models, from small, efficient models to large, high-performance ones:

| Model Size | Example Models                                                                       | Dimension | Size (GB)  | Primary Use                                          |
| ---------- | ------------------------------------------------------------------------------------ | --------- | ---------- | ---------------------------------------------------- |
| Small      | BAAI/bge-small-en-v1.5, jinaai/jina-embeddings-v2-small-en                           | 384-512   | 0.067-0.13 | Efficient semantic search with low resource usage    |
| Medium     | BAAI/bge-base-en, nomic-ai/nomic-embed-text-v1.5, snowflake/snowflake-arctic-embed-m | 768       | 0.21-0.54  | Balanced performance and resource usage              |
| Large      | BAAI/bge-large-en-v1.5, thenlper/gte-large, intfloat/multilingual-e5-large           | 1024      | 1.0-2.24   | Highest quality embeddings for critical applications |

The full list includes 25 dense text embedding models with diverse characteristics:

- BGE models (small/base/large variants)
- Snowflake Arctic models (xs/s/m/l variants)
- Sentence Transformers models
- Jina AI embedding models
- Nomic AI embedding models
- CLIP text models
- Multilingual models (Chinese, German, etc.)

These models can be accessed through the `TextEmbedding` class using the `model_name` parameter:

```
```

Sources: [docs/examples/Supported\_Models.ipynb64-129](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L64-L129)

## Sparse Text Embedding Models

Sparse embedding models generate high-dimensional, sparse vector representations where most values are zero. These models excel at lexical matching and are often used in hybrid search systems alongside dense embeddings.

```
```

Sources: [docs/examples/Supported\_Models.ipynb386-392](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L386-L392)

FastEmbed supports the following sparse text embedding models:

| Model                                   | Vocab Size | Description                                          | Size (GB) | Requires IDF |
| --------------------------------------- | ---------- | ---------------------------------------------------- | --------- | ------------ |
| Qdrant/bm25                             | -          | BM25 as sparse embeddings                            | 0.01      | Yes          |
| Qdrant/bm42-all-minilm-l6-v2-attentions | 30,522     | Light sparse embedding model using attention weights | 0.09      | Yes          |
| prithivida/Splade\_PP\_en\_v1           | 30,522     | SPLADE++ Model for sparse retrieval                  | 0.532     | No           |

These models can be accessed through the `SparseTextEmbedding` class:

```
```

Sources: [docs/examples/Supported\_Models.ipynb386-478](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L386-L478)

## Late Interaction Text Embedding Models

Late interaction models defer the computation of relevance scores until query time, preserving token-level representations instead of pooling them into a single vector. This approach provides higher precision at the cost of more complex retrieval.

```
```

Sources: [docs/examples/Supported\_Models.ipynb510-516](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L510-L516)

FastEmbed supports the following late interaction text embedding models:

| Model                                 | Dimension | Description                         | License      | Size (GB) |
| ------------------------------------- | --------- | ----------------------------------- | ------------ | --------- |
| answerdotai/answerai-colbert-small-v1 | 96        | Multilingual late interaction model | apache-2.0   | 0.13      |
| colbert-ir/colbertv2.0                | 128       | Late interaction model              | mit          | 0.44      |
| jinaai/jina-colbert-v2                | 128       | Enhanced ColBERT capabilities       | cc-by-nc-4.0 | 2.24      |

These models can be accessed through the `LateInteractionTextEmbedding` class:

```
```

Sources: [docs/examples/Supported\_Models.ipynb510-590](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L510-L590)

## Image Embedding Models

Image embedding models generate vector representations from images, enabling visual similarity search and multimodal applications.

```
```

Sources: [docs/examples/Supported\_Models.ipynb622-628](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L622-L628)

FastEmbed supports the following image embedding models:

| Model                       | Dimension | Description                     | License    | Size (GB) |
| --------------------------- | --------- | ------------------------------- | ---------- | --------- |
| Qdrant/resnet50-onnx        | 2048      | Image embeddings (2016)         | apache-2.0 | 0.10      |
| Qdrant/clip-ViT-B-32-vision | 512       | CLIP vision embeddings          | mit        | 0.34      |
| Qdrant/Unicom-ViT-B-32      | 512       | Unicom image embeddings         | apache-2.0 | 0.48      |
| Qdrant/Unicom-ViT-B-16      | 768       | Higher detail Unicom embeddings | apache-2.0 | 0.82      |

These models can be accessed through the `ImageEmbedding` class:

```
```

Sources: [docs/examples/Supported\_Models.ipynb622-704](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L622-L704)

## Multimodal Late Interaction Models

FastEmbed also supports multimodal late interaction models, such as ColPali, which enable matching between text and images using token-level representations.

```
```

Sources: [fastembed/late\_interaction\_multimodal/\_\_init\_\_.py1-6](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction_multimodal/__init__.py#L1-L6) [NOTICE16-18](https://github.com/qdrant/fastembed/blob/b785640b/NOTICE#L16-L18)

Currently, FastEmbed supports the following multimodal late interaction model:

| Model               | Description                                               | License |
| ------------------- | --------------------------------------------------------- | ------- |
| vidore/colpali-v1.3 | Multimodal late interaction model for text-image matching | gemma   |

This model can be accessed through the `LateInteractionMultimodalEmbedding` class.

Sources: [NOTICE16-19](https://github.com/qdrant/fastembed/blob/b785640b/NOTICE#L16-L19)

## Cross-Encoder Models for Reranking

Cross-encoder models evaluate text pairs together rather than encoding them separately, providing more accurate relevance scores for reranking search results.

```
```

Sources: [docs/examples/Supported\_Models.ipynb732-738](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L732-L738)

FastEmbed supports the following cross-encoder models for reranking:

| Model                                     | Description                   | License      | Size (GB) |
| ----------------------------------------- | ----------------------------- | ------------ | --------- |
| Xenova/ms-marco-MiniLM-L-6-v2             | MiniLM-L-6-v2 for reranking   | apache-2.0   | 0.08      |
| Xenova/ms-marco-MiniLM-L-12-v2            | MiniLM-L-12-v2 for reranking  | apache-2.0   | 0.12      |
| jinaai/jina-reranker-v1-tiny-en           | Fast reranker with 8K context | apache-2.0   | 0.13      |
| jinaai/jina-reranker-v1-turbo-en          | Fast reranker with 8K context | apache-2.0   | 0.15      |
| BAAI/bge-reranker-base                    | BGE reranker base model       | mit          | 1.04      |
| jinaai/jina-reranker-v2-base-multilingual | Multilingual reranker         | cc-by-nc-4.0 | 1.11      |

These models can be accessed through the `TextCrossEncoder` class:

```
```

Sources: [docs/examples/Supported\_Models.ipynb732-826](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb#L732-L826)

## Model Selection Guide

When choosing a model for your application, consider these factors:

```
```

Sources: [docs/examples/Supported\_Models.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Supported_Models.ipynb)

## License Considerations

When using FastEmbed models, be aware of licensing restrictions:

- Most models are available under permissive licenses (MIT, Apache-2.0)

- Some Jina AI models have non-commercial licenses (cc-by-nc-4.0):

  - jinaai/jina-colbert-v2
  - jinaai/jina-reranker-v2-base-multilingual
  - jinaai/jina-embeddings-v3

- The ColPali model (vidore/colpali-v1.3) is subject to the Gemma Terms of Use

Always check the license information before using a model in production applications, especially for commercial use.

Sources: [NOTICE1-23](https://github.com/qdrant/fastembed/blob/b785640b/NOTICE#L1-L23)

For more detailed information about using these models with FastEmbed, see the [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md) and [Usage Examples](qdrant/fastembed/7-usage-examples.md) sections.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Supported Models](#supported-models.md)
- [Model Types Overview](#model-types-overview.md)
- [Dense Text Embedding Models](#dense-text-embedding-models.md)
- [Sparse Text Embedding Models](#sparse-text-embedding-models.md)
- [Late Interaction Text Embedding Models](#late-interaction-text-embedding-models.md)
- [Image Embedding Models](#image-embedding-models.md)
- [Multimodal Late Interaction Models](#multimodal-late-interaction-models.md)
- [Cross-Encoder Models for Reranking](#cross-encoder-models-for-reranking.md)
- [Model Selection Guide](#model-selection-guide.md)
- [License Considerations](#license-considerations.md)
