Medical Image Search with Vision Transformers | qdrant/examples | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/examples](https://github.com/qdrant/examples "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 26 June 2025 ([b3c4b2](https://github.com/qdrant/examples/commits/b3c4b28f))

- [Overview](qdrant/examples/1-overview.md)
- [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md)
- [Text Data Applications](qdrant/examples/3-text-data-applications.md)
- [Code Search with Dual Embeddings](qdrant/examples/3.1-code-search-with-dual-embeddings.md)
- [Extractive Question Answering](qdrant/examples/3.2-extractive-question-answering.md)
- [Movie Recommendations with Sparse Vectors](qdrant/examples/3.3-movie-recommendations-with-sparse-vectors.md)
- [Image Data Applications](qdrant/examples/4-image-data-applications.md)
- [E-commerce Reverse Image Search](qdrant/examples/4.1-e-commerce-reverse-image-search.md)
- [Medical Image Search with Vision Transformers](qdrant/examples/4.2-medical-image-search-with-vision-transformers.md)
- [Audio Data Applications](qdrant/examples/5-audio-data-applications.md)
- [Music Recommendation Engine](qdrant/examples/5.1-music-recommendation-engine.md)
- [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md)
- [Multivector RAG with DSPy](qdrant/examples/6.1-multivector-rag-with-dspy.md)
- [Graph-Enhanced RAG with Neo4j](qdrant/examples/6.2-graph-enhanced-rag-with-neo4j.md)
- [PDF Retrieval at Scale](qdrant/examples/6.3-pdf-retrieval-at-scale.md)
- [Agentic Systems with CrewAI](qdrant/examples/7-agentic-systems-with-crewai.md)
- [Meeting Analysis with Agentic RAG](qdrant/examples/7.1-meeting-analysis-with-agentic-rag.md)
- [Additional Use Cases](qdrant/examples/8-additional-use-cases.md)
- [Self-Query Systems with LangChain](qdrant/examples/8.1-self-query-systems-with-langchain.md)
- [Development Environment Setup](qdrant/examples/8.2-development-environment-setup.md)

Menu

# Medical Image Search with Vision Transformers

Relevant source files

- [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb)
- [qdrant\_101\_image\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md)

## Purpose and Scope

This document describes the medical image search system that enables healthcare professionals to find similar skin lesion images using semantic search powered by Vision Transformers and Qdrant vector database. The system processes medical images to extract visual embeddings and provides similarity-based retrieval with advanced filtering capabilities for demographic and diagnostic criteria.

For general image search applications in e-commerce contexts, see [E-commerce Reverse Image Search](qdrant/examples/4.1-e-commerce-reverse-image-search.md). For foundational Qdrant concepts, see [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md).

## System Architecture Overview

The medical image search system combines computer vision models with vector database technology to enable semantic similarity search across dermatological images.

### Core System Components

```
```

Sources: [qdrant\_101\_image\_data/README.md1-984](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L1-L984)

### Data Flow Pipeline

```
```

Sources: [qdrant\_101\_image\_data/README.md295-398](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L295-L398) [qdrant\_101\_image\_data/README.md453-520](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L453-L520)

## Vision Transformer Implementation

The system utilizes Facebook's DINO Vision Transformer model for extracting meaningful visual features from medical images.

### Model Configuration

| Component         | Specification                                               |
| ----------------- | ----------------------------------------------------------- |
| Processor         | `ViTImageProcessor.from_pretrained('facebook/dino-vits16')` |
| Model             | `ViTModel.from_pretrained('facebook/dino-vits16')`          |
| Input Size        | 224x224 pixels (3 channels)                                 |
| Output Dimensions | 384-dimensional embeddings                                  |
| Patch Processing  | 197 patches per image                                       |
| Pooling Method    | Mean pooling across patches                                 |

The embedding extraction process transforms raw medical images into dense vector representations that capture visual similarities relevant for diagnostic comparison.

Sources: [qdrant\_101\_image\_data/README.md203-207](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L203-L207) [qdrant\_101\_image\_data/README.md295-302](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L295-L302)

### Dataset Structure

The system processes a comprehensive skin lesion dataset with the following metadata schema:

```
```

Sources: [qdrant\_101\_image\_data/README.md23-34](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L23-L34) [qdrant\_101\_image\_data/README.md332-360](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L332-L360)

## Qdrant Vector Database Integration

The system leverages Qdrant for efficient similarity search and metadata filtering across medical image embeddings.

### Collection Configuration

```
```

Sources: [qdrant\_101\_image\_data/README.md95-100](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L95-L100) [qdrant\_101\_image\_data/README.md379-398](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L379-L398)

## Advanced Search Capabilities

The system provides sophisticated search functionality tailored for medical diagnostic applications.

### Filter Types and Use Cases

| Filter Type | Purpose                             | Example Implementation                                                     |
| ----------- | ----------------------------------- | -------------------------------------------------------------------------- |
| Demographic | Age/gender-based filtering          | `FieldCondition(key="sex", match=MatchValue(value="female"))`              |
| Diagnostic  | Disease category filtering          | `FieldCondition(key="dx", match=MatchExcept(except=["melanoma"]))`         |
| Anatomical  | Body location filtering             | `FieldCondition(key="localization", match=MatchAny(any=["face", "neck"]))` |
| ID-based    | Specific sample inclusion/exclusion | `HasIdCondition(has_id=range_list)`                                        |
| Score-based | Similarity threshold filtering      | `score_threshold=0.92`                                                     |

### Search Query Patterns

```
```

Sources: [qdrant\_101\_image\_data/README.md484-520](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L484-L520) [qdrant\_101\_image\_data/README.md632-704](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L632-L704) [qdrant\_101\_image\_data/README.md872-900](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L872-L900)

## Streamlit User Interface

The system includes a web-based interface that enables medical professionals to upload images and retrieve similar cases from the database.

### Application Components

```
```

Sources: [qdrant\_101\_image\_data/README.md928-964](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L928-L964)

## Implementation Details

### Key Functions and Methods

| Function                     | Purpose                                   | Location                                                                                                                                |
| ---------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `get_embeddings(batch)`      | Extract ViT embeddings from image batches | [qdrant\_101\_image\_data/README.md296-302](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L296-L302) |
| `see_images(results, top_k)` | Visualize search results with metadata    | [qdrant\_101\_image\_data/README.md532-548](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L532-L548) |
| `client.search()`            | Execute similarity search with filters    | [qdrant\_101\_image\_data/README.md454-458](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L454-L458) |
| `client.search_batch()`      | Process multiple search requests          | [qdrant\_101\_image\_data/README.md896-900](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L896-L900) |

### Performance Considerations

The system processes 9,577 medical images with the following specifications:

- Batch processing: 16 images per batch for embedding extraction
- Storage efficiency: 384-dimensional vectors with cosine similarity
- Upsert batching: 1,000 vectors per database transaction
- Query performance: Filtered search across demographic and diagnostic criteria

Sources: [qdrant\_101\_image\_data/README.md306-307](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L306-L307) [qdrant\_101\_image\_data/README.md380-398](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L380-L398)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Medical Image Search with Vision Transformers](#medical-image-search-with-vision-transformers.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Architecture Overview](#system-architecture-overview.md)
- [Core System Components](#core-system-components.md)
- [Data Flow Pipeline](#data-flow-pipeline.md)
- [Vision Transformer Implementation](#vision-transformer-implementation.md)
- [Model Configuration](#model-configuration.md)
- [Dataset Structure](#dataset-structure.md)
- [Qdrant Vector Database Integration](#qdrant-vector-database-integration.md)
- [Collection Configuration](#collection-configuration.md)
- [Advanced Search Capabilities](#advanced-search-capabilities.md)
- [Filter Types and Use Cases](#filter-types-and-use-cases.md)
- [Search Query Patterns](#search-query-patterns.md)
- [Streamlit User Interface](#streamlit-user-interface.md)
- [Application Components](#application-components.md)
- [Implementation Details](#implementation-details.md)
- [Key Functions and Methods](#key-functions-and-methods.md)
- [Performance Considerations](#performance-considerations.md)
