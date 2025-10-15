FastEmbed Integration | qdrant/qdrant-client | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant-client](https://github.com/qdrant/qdrant-client "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 9 July 2025 ([ac6f6c](https://github.com/qdrant/qdrant-client/commits/ac6f6cd2))

- [Overview](qdrant/qdrant-client/1-overview.md)
- [Client Architecture](qdrant/qdrant-client/2-client-architecture.md)
- [Client Interface](qdrant/qdrant-client/2.1-client-interface.md)
- [Local Mode](qdrant/qdrant-client/2.2-local-mode.md)
- [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md)
- [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md)
- [Core Operations](qdrant/qdrant-client/3-core-operations.md)
- [Search Operations](qdrant/qdrant-client/3.1-search-operations.md)
- [Collection Management](qdrant/qdrant-client/3.2-collection-management.md)
- [Point Operations](qdrant/qdrant-client/3.3-point-operations.md)
- [Advanced Features](qdrant/qdrant-client/4-advanced-features.md)
- [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md)
- [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md)
- [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md)
- [Local Inference](qdrant/qdrant-client/4.4-local-inference.md)
- [Implementation Details](qdrant/qdrant-client/5-implementation-details.md)
- [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md)
- [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md)
- [Expression Evaluation](qdrant/qdrant-client/5.3-expression-evaluation.md)
- [Development & Testing](qdrant/qdrant-client/6-development-and-testing.md)
- [Project Setup](qdrant/qdrant-client/6.1-project-setup.md)
- [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md)
- [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md)

Menu

# FastEmbed Integration

Relevant source files

- [qdrant\_client/async\_qdrant\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py)
- [qdrant\_client/qdrant\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py)
- [tests/test\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_fastembed.py)
- [tools/async\_client\_generator/fastembed\_generator.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tools/async_client_generator/fastembed_generator.py)

This page documents the FastEmbed integration in Qdrant Client, which provides seamless vector embedding capabilities for text and images without requiring separate preprocessing steps. For information about other advanced embedding techniques, see [Local Inference](qdrant/qdrant-client/4.4-local-inference.md).

## Overview

FastEmbed integration allows you to:

- Automatically embed documents when adding them to Qdrant
- Search collections using natural language queries without manual embedding
- Use both dense and sparse embedding models for hybrid search
- Handle multiple embedding model types (text, sparse text, late interaction, image)
- Configure model parameters for optimal performance

FastEmbed Integration Architecture

```
```

Sources: [qdrant\_client/qdrant\_fastembed.py34-56](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L34-L56) [qdrant\_client/async\_qdrant\_fastembed.py43-65](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py#L43-L65) [qdrant\_client/embed/embedder.py32-56](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L32-L56)

## Installation and Setup

### Installing FastEmbed

FastEmbed is not included in the basic installation of Qdrant Client. You need to install it separately:

```
```

### Model Configuration

The `QdrantFastembedMixin` provides methods to configure embedding models:

| Method               | Purpose                          | Default Model         |
| -------------------- | -------------------------------- | --------------------- |
| `set_model()`        | Configure dense embedding model  | `"BAAI/bge-small-en"` |
| `set_sparse_model()` | Configure sparse embedding model | `None`                |

FastEmbed Installation Check Flow

```
```

The client stores model state in instance variables:

- `_embedding_model_name`: Current dense model name
- `_sparse_embedding_model_name`: Current sparse model name
- `_model_embedder`: `ModelEmbedder` instance managing actual embedding models

Sources: [qdrant\_client/qdrant\_fastembed.py36-42](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L36-L42) [qdrant\_client/qdrant\_fastembed.py99-208](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L99-L208) [qdrant\_client/fastembed\_common.py13-25](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L13-L25)

### Model Configuration Parameters

The `set_model()` and `set_sparse_model()` methods accept the following parameters:

| Parameter              | Type                               | Description                            | Default               |
| ---------------------- | ---------------------------------- | -------------------------------------- | --------------------- |
| `embedding_model_name` | `str`                              | Model identifier from supported models | `"BAAI/bge-small-en"` |
| `cache_dir`            | `Optional[str]`                    | Model cache directory path             | System temp dir       |
| `threads`              | `Optional[int]`                    | ONNX runtime threads                   | Auto-detected         |
| `providers`            | `Optional[Sequence[OnnxProvider]]` | ONNX execution providers               | Default providers     |
| `cuda`                 | `bool`                             | Enable CUDA acceleration               | `False`               |
| `device_ids`           | `Optional[list[int]]`              | GPU device IDs for multi-GPU           | `None`                |
| `lazy_load`            | `bool`                             | Load models on-demand                  | `False`               |

Model initialization uses the `_get_or_init_model()` and `_get_or_init_sparse_model()` methods which delegate to the `ModelEmbedder.embedder` component.

Sources: [qdrant\_client/qdrant\_fastembed.py99-157](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L99-L157) [qdrant\_client/qdrant\_fastembed.py159-208](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L159-L208) [qdrant\_client/qdrant\_fastembed.py230-268](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L230-L268)

## Working with Documents

### Adding Documents with Automatic Embedding

The most common way to use FastEmbed is through the `add()` method, which handles embedding automatically:

```
```

If the collection doesn't exist, it will be automatically created with appropriate vector configuration.

Document Addition Process with FastEmbed

```
```

The `_points_iterator()` method generates `models.PointStruct` objects with vector fields named by `get_vector_field_name()` and `get_sparse_vector_field_name()`.

Sources: [qdrant\_client/qdrant\_fastembed.py518-610](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L518-L610) [qdrant\_client/qdrant\_fastembed.py270-317](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L270-L317) [qdrant\_client/qdrant\_fastembed.py373-401](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L373-L401)

### Collection Configuration

When creating collections manually, you can use utility methods to get appropriate vector parameters:

```
```

Sources: [qdrant\_client/qdrant\_fastembed.py473-530](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L473-L530) [qdrant\_client/async\_qdrant\_fastembed.py444-494](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py#L444-L494)

## Searching with FastEmbed

### Query Operations

The `query()` method handles text embedding and search automatically:

```
```

Query Processing Flow

```
```

The `QueryResponse` objects contain:

- `id`: Point ID
- `document`: Original document text from payload
- `metadata`: Point payload
- `score`: Similarity score
- `embedding`: Dense vector (optional)
- `sparse_embedding`: Sparse vector (optional)

Sources: [qdrant\_client/qdrant\_fastembed.py612-696](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L612-L696) [qdrant\_client/qdrant\_fastembed.py339-371](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L339-L371) [qdrant\_client/fastembed\_common.py81-88](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L81-L88)

### Hybrid Search Implementation

When `sparse_embedding_model_name` is set, the `query()` method automatically performs hybrid search by creating separate `models.SearchRequest` objects for dense and sparse vectors:

Hybrid Search Request Creation

```
```

Sources: [qdrant\_client/qdrant\_fastembed.py647-696](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L647-L696) [qdrant\_client/qdrant\_fastembed.py319-337](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L319-L337) [qdrant\_client/hybrid/fusion.py1-50](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/fusion.py#L1-L50)

### Batch Querying

For efficiency, you can perform multiple queries at once:

```
```

Sources: [qdrant\_client/qdrant\_fastembed.py712-801](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L712-L801) [qdrant\_client/async\_qdrant\_fastembed.py656-730](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py#L656-L730)

## Advanced Features

### Vector Field Naming Convention

The `QdrantFastembedMixin` generates vector field names using model-specific conventions:

| Method                           | Format                       | Example                         |
| -------------------------------- | ---------------------------- | ------------------------------- |
| `get_vector_field_name()`        | `"fast-{model_name}"`        | `"fast-bge-small-en"`           |
| `get_sparse_vector_field_name()` | `"fast-sparse-{model_name}"` | `"fast-sparse-splade_pp_en_v1"` |

Vector Field Name Generation

```
```

These field names are used in:

- Collection creation via `get_fastembed_vector_params()`
- Point insertion via `_points_iterator()`
- Search operations via `models.NamedVector` and `models.NamedSparseVector`

Sources: [qdrant\_client/qdrant\_fastembed.py319-337](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L319-L337) [qdrant\_client/qdrant\_fastembed.py398-401](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L398-L401) [qdrant\_client/qdrant\_fastembed.py651-682](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L651-L682)

### Embedding Size Information

You can get the size of embeddings produced by a model:

```
```

Note that sparse embeddings don't have a fixed size, so calling this method with a sparse model name will raise an error.

Sources: [qdrant\_client/qdrant\_fastembed.py452-471](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L452-L471) [qdrant\_client/async\_qdrant\_fastembed.py426-442](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_fastembed.py#L426-L442)

### Supported Model Types

The `FastEmbedMisc` class provides methods to list available models:

| Model Type                  | List Method                                 | FastEmbed Class                      | Purpose                                |
| --------------------------- | ------------------------------------------- | ------------------------------------ | -------------------------------------- |
| Dense Text                  | `list_text_models()`                        | `TextEmbedding`                      | Standard vector search                 |
| Sparse Text                 | `list_sparse_models()`                      | `SparseTextEmbedding`                | BM25, SPLADE models for lexical search |
| Late Interaction Text       | `list_late_interaction_text_models()`       | `LateInteractionTextEmbedding`       | ColBERT-like token-level matching      |
| Late Interaction Multimodal | `list_late_interaction_multimodal_models()` | `LateInteractionMultimodalEmbedding` | Multimodal ColBERT models              |
| Image                       | `list_image_models()`                       | `ImageEmbedding`                     | Visual search embeddings               |

Model Parameter Retrieval

```
```

Special handling for sparse models includes IDF modifier detection for models like `"Qdrant/bm25"` and `"Qdrant/bm42-all-minilm-l6-v2-attentions"`.

Sources: [qdrant\_client/qdrant\_fastembed.py44-87](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L44-L87) [qdrant\_client/qdrant\_fastembed.py210-228](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py#L210-L228) [qdrant\_client/fastembed\_common.py25-27](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L25-L27)

## Complete Examples

### Basic Search Example

```
```

Sources: [tests/test\_fastembed.py10-49](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_fastembed.py#L10-L49)

### Hybrid Search Example

```
```

Sources: [tests/test\_fastembed.py52-78](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_fastembed.py#L52-L78)

### Batch Query Example

```
```

Sources: [tests/test\_fastembed.py80-113](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_fastembed.py#L80-L113)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [FastEmbed Integration](#fastembed-integration.md)
- [Overview](#overview.md)
- [Installation and Setup](#installation-and-setup.md)
- [Installing FastEmbed](#installing-fastembed.md)
- [Model Configuration](#model-configuration.md)
- [Model Configuration Parameters](#model-configuration-parameters.md)
- [Working with Documents](#working-with-documents.md)
- [Adding Documents with Automatic Embedding](#adding-documents-with-automatic-embedding.md)
- [Collection Configuration](#collection-configuration.md)
- [Searching with FastEmbed](#searching-with-fastembed.md)
- [Query Operations](#query-operations.md)
- [Hybrid Search Implementation](#hybrid-search-implementation.md)
- [Batch Querying](#batch-querying.md)
- [Advanced Features](#advanced-features.md)
- [Vector Field Naming Convention](#vector-field-naming-convention.md)
- [Embedding Size Information](#embedding-size-information.md)
- [Supported Model Types](#supported-model-types.md)
- [Complete Examples](#complete-examples.md)
- [Basic Search Example](#basic-search-example.md)
- [Hybrid Search Example](#hybrid-search-example.md)
- [Batch Query Example](#batch-query-example.md)
