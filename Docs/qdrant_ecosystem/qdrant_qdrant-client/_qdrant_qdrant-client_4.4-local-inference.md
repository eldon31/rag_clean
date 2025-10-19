Local Inference | qdrant/qdrant-client | DeepWiki

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

# Local Inference

Relevant source files

- [qdrant\_client/embed/common.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/common.py)
- [qdrant\_client/embed/embedder.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py)
- [qdrant\_client/embed/model\_embedder.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py)
- [qdrant\_client/fastembed\_common.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py)
- [tests/embed\_tests/test\_local\_inference.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py)

## Purpose and Scope

This document describes the Local Inference system in qdrant-client, which enables automatic embedding of documents and images directly within the client application, without requiring an external embedding service. This system allows seamless integration of embedding models into vector search workflows by automatically detecting and processing objects that require inference.

For information about the FastEmbed integration, which provides pre-configured models, see [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md).

## Overview

The Local Inference system transparently converts high-level objects like text documents and images into vector embeddings that can be stored and searched in Qdrant. When you provide a `Document` or `Image` object to methods like `upsert()` or `query_points()`, the system automatically:

1. Detects fields requiring embedding
2. Loads the appropriate model
3. Generates embeddings
4. Replaces the original objects with their vector representations

**Local Inference System Architecture**

```
```

Sources: [qdrant\_client/embed/model\_embedder.py42-444](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L42-L444) [qdrant\_client/embed/embedder.py29-388](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L29-L388) [qdrant\_client/fastembed\_common.py36-267](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L36-L267)

## Core Components

### ModelEmbedder

The `ModelEmbedder` class is the primary entry point for local inference. It coordinates the inspection, batching, and embedding processes:

**Core Classes and Methods**

```
```

Sources: [qdrant\_client/embed/model\_embedder.py21-444](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L21-L444) [qdrant\_client/embed/embedder.py23-388](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L23-L388) [qdrant\_client/fastembed\_common.py36-267](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L36-L267)

### Embedder

The `Embedder` class manages embedding models and performs the actual inference:

- Maintains a registry of initialized models
- Provides methods to embed text and images
- Supports various model types (dense, sparse, late interaction, multimodal)
- Handles model sharing and caching

Sources: [qdrant\_client/embed/embedder.py32-385](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L32-L385)

### Type Inspection System

The type inspection system identifies fields in models that require inference:

```
```

Sources: [qdrant\_client/embed/type\_inspector.py12-149](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py#L12-L149) [qdrant\_client/embed/embed\_inspector.py13-176](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embed_inspector.py#L13-L176) [qdrant\_client/embed/schema\_parser.py29-305](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/schema_parser.py#L29-L305)

## Inference Workflow

**Local Inference Processing Flow**

```
```

Sources: [qdrant\_client/embed/model\_embedder.py124-156](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L124-L156) [qdrant\_client/embed/embedder.py222-267](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L222-L267) [tests/embed\_tests/test\_local\_inference.py133-237](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L133-L237)

## Supported Model Types

The Local Inference system supports several types of embedding models:

| Model Type                  | Description                                 | Input Type     |
| --------------------------- | ------------------------------------------- | -------------- |
| Dense Text                  | Standard text embedding models              | Text           |
| Sparse Text                 | Sparse vector text models                   | Text           |
| Late Interaction Text       | Models that generate token-level embeddings | Text           |
| Image                       | Image embedding models                      | Images         |
| Late Interaction Multimodal | Models that can embed both text and images  | Text or Images |

Sources: [qdrant\_client/fastembed\_common.py28-78](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L28-L78)

## Supported Inference Objects

**Inference Object Types**

```
```

The constant `INFERENCE_OBJECT_NAMES` contains the string names: `{"Document", "Image", "InferenceObject"}` and `INFERENCE_OBJECT_TYPES` is a Union type used throughout the system for type checking.

Sources: [qdrant\_client/embed/common.py5-6](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/common.py#L5-L6)

## Using Local Inference

### Basic Usage

Local inference happens automatically when you provide `Document` or `Image` objects to client methods:

```
```

Sources: [tests/embed\_tests/test\_local\_inference.py133-165](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L133-L165)

### Named Vectors

You can also use local inference with named vectors:

```
```

Sources: [tests/embed\_tests/test\_local\_inference.py166-237](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L166-L237)

### Query-Time Inference

The system distinguishes between document and query embedding for models that have different embedding methods for documents and queries:

```
```

Sources: [qdrant\_client/embed/embedder.py278-287](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L278-L287) [tests/embed\_tests/test\_local\_inference.py352-581](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L352-L581)

## Advanced Features

### Model Configuration Options

You can pass additional options to the embedding models:

```
```

Sources: [qdrant\_client/embed/embedder.py61-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L61-L67) [tests/embed\_tests/test\_local\_inference.py916-976](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L916-L976)

### Parallel Processing

For large batches of documents, you can use parallel processing:

```
```

Sources: [qdrant\_client/embed/model\_embedder.py75-123](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L75-L123) [tests/embed\_tests/test\_local\_inference.py310-350](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L310-L350)

## Integration with Client Operations

Local inference is integrated with various client operations:

| Operation             | Description                                              | Test Coverage                                                                                                                                                    |
| --------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `upsert`              | Embeds documents/images before upserting                 | [tests/embed\_tests/test\_local\_inference.py133-237](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L133-L237) |
| `upload_points`       | Embeds documents/images when uploading points in batches | [tests/embed\_tests/test\_local\_inference.py240-350](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L240-L350) |
| `upload_collection`   | Embeds vectors when uploading a collection               | [tests/embed\_tests/test\_local\_inference.py295-350](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L295-L350) |
| `query_points`        | Embeds query documents/images before searching           | [tests/embed\_tests/test\_local\_inference.py352-515](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L352-L515) |
| `query_points_groups` | Embeds query documents/images for grouped searches       | [tests/embed\_tests/test\_local\_inference.py584-682](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L584-L682) |
| `query_batch_points`  | Embeds documents/images in batch queries                 | [tests/embed\_tests/test\_local\_inference.py684-743](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L684-L743) |
| `batch_update_points` | Embeds documents/images in batch updates                 | [tests/embed\_tests/test\_local\_inference.py745-857](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L745-L857) |
| `update_vectors`      | Embeds new documents/images when updating vectors        | [tests/embed\_tests/test\_local\_inference.py859-914](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L859-L914) |

Sources: [tests/embed\_tests/test\_local\_inference.py133-914](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L133-L914)

## Internal Architecture

### Object Detection and Processing

The system uses a multi-step process to detect and process objects requiring inference:

1. **Model Processing**: The `ModelEmbedder._process_model()` method traverses model structures to find inference objects.
2. **Object Accumulation**: The `_accumulate()` method collects `Document`, `Image`, and `InferenceObject` instances into batches grouped by model name.
3. **Batch Embedding**: The `_embed_accumulator()` method calls `Embedder.embed()` to generate embeddings for accumulated objects.
4. **Model Resolution**: The `_resolve_inference_object()` method converts `InferenceObject` instances to `Document` or `Image` objects.
5. **Replacement**: The `_drain_accumulator()` method replaces original objects with their vector representations.

**Processing Pipeline**

```
```

Sources: [qdrant\_client/embed/model\_embedder.py141-156](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L141-L156) [qdrant\_client/embed/model\_embedder.py247-275](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L247-L275) [qdrant\_client/embed/model\_embedder.py277-317](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/model_embedder.py#L277-L317)

### Model Management

The `Embedder` class efficiently manages embedding models through `ModelInstance` containers:

- **Model Caching**: Each model type has its own dictionary (e.g., `embedding_models`, `sparse_embedding_models`) storing lists of `ModelInstance[T]` objects
- **Configuration Tracking**: `ModelInstance` objects store model instances with their initialization options and deprecation status
- **Lazy Loading**: Models are loaded only when first requested via `get_or_init_*` methods
- **Option Matching**: Multiple instances of the same model with different configurations are supported by comparing options dictionaries
- **Model Validation**: `FastEmbedMisc` provides validation methods for all supported model types

**Model Instance Management**

```
```

Sources: [qdrant\_client/embed/embedder.py23-27](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L23-L27) [qdrant\_client/embed/embedder.py29-44](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L29-L44) [qdrant\_client/embed/embedder.py46-221](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/embedder.py#L46-L221)

## Compatibility

The Local Inference system is designed to work with:

- **Local in-memory Qdrant instances**: `QdrantClient(":memory:")`
- **Local persistent Qdrant instances**: `QdrantClient(path="/path/to/db")`
- **Remote Qdrant servers**: `QdrantClient(host="localhost", port=6333)`

The system automatically handles embedding generation regardless of the backend, with the same API working across all deployment modes.

Sources: [tests/embed\_tests/test\_local\_inference.py134](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L134-L134) [tests/embed\_tests/test\_local\_inference.py256-259](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L256-L259)

## Limitations

- The FastEmbed library must be installed to use Local Inference
- Not all embedding models are supported, only those available in FastEmbed
- Embedding large batches may require significant memory

Sources: [tests/embed\_tests/test\_local\_inference.py134-136](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/embed_tests/test_local_inference.py#L134-L136) [qdrant\_client/fastembed\_common.py8-25](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/fastembed_common.py#L8-L25)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Local Inference](#local-inference.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Core Components](#core-components.md)
- [ModelEmbedder](#modelembedder.md)
- [Embedder](#embedder.md)
- [Type Inspection System](#type-inspection-system.md)
- [Inference Workflow](#inference-workflow.md)
- [Supported Model Types](#supported-model-types.md)
- [Supported Inference Objects](#supported-inference-objects.md)
- [Using Local Inference](#using-local-inference.md)
- [Basic Usage](#basic-usage.md)
- [Named Vectors](#named-vectors.md)
- [Query-Time Inference](#query-time-inference.md)
- [Advanced Features](#advanced-features.md)
- [Model Configuration Options](#model-configuration-options.md)
- [Parallel Processing](#parallel-processing.md)
- [Integration with Client Operations](#integration-with-client-operations.md)
- [Internal Architecture](#internal-architecture.md)
- [Object Detection and Processing](#object-detection-and-processing.md)
- [Model Management](#model-management.md)
- [Compatibility](#compatibility.md)
- [Limitations](#limitations.md)
