Getting Started with Qdrant | qdrant/examples | DeepWiki

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

# Getting Started with Qdrant

Relevant source files

- [qdrant\_101\_getting\_started/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md)
- [qdrant\_101\_getting\_started/getting\_started.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb)
- [qdrant\_101\_text\_data/02\_qdrant\_101\_text\_files/02\_qdrant\_101\_text\_22\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/02_qdrant_101_text_files/02_qdrant_101_text_22_0.png)
- [qdrant\_101\_text\_data/02\_qdrant\_101\_text\_files/02\_qdrant\_101\_text\_25\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/02_qdrant_101_text_files/02_qdrant_101_text_25_0.png)

This document provides a foundational introduction to Qdrant vector database concepts, installation, and core operations. It covers basic vector database operations including collection management, point manipulation, similarity search, and recommendation systems. For more advanced text processing applications, see [Text Data Applications](qdrant/examples/3-text-data-applications.md). For specialized retrieval patterns, see [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md).

## Overview

Qdrant is a vector database designed for similarity search and recommendation systems. This tutorial demonstrates core concepts through practical examples using a music recommendation scenario with dummy data. The key components covered include:

- **Collections**: Container for vectors with specified dimensions and distance metrics
- **Points**: Individual records containing vectors, IDs, and optional metadata payloads
- **Search Operations**: Similarity search and recommendation queries
- **Filtering**: Payload-based filtering for refined results

## Architecture Overview

```
```

**Qdrant System Architecture**: Shows the relationship between client components, server infrastructure, and data model classes used in vector operations.

Sources: [qdrant\_101\_getting\_started/README.md67-75](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L67-L75) [qdrant\_101\_getting\_started/getting\_started.ipynb127-135](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L127-L135)

## Installation and Setup

### Docker Installation

Qdrant runs as a Docker container with persistent storage:

```
```

### Python Dependencies

Required packages for client operations:

```
```

### Client Initialization

The `QdrantClient` supports both remote server connections and in-memory instances:

```
```

Sources: [qdrant\_101\_getting\_started/README.md25-96](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L25-L96) [qdrant\_101\_getting\_started/getting\_started.ipynb76-174](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L76-L174)

## Collection Management

### Collection Creation

Collections define vector dimensions and distance metrics. The `recreate_collection()` method creates or overwrites existing collections:

```
```

### Supported Distance Metrics

- **Cosine Similarity**: `models.Distance.COSINE`
- **Dot Product**: `models.Distance.DOT`
- **Euclidean Distance**: `models.Distance.EUCLIDEAN`

### Collection Health Monitoring

The `get_collection()` method returns status information:

```
```

Sources: [qdrant\_101\_getting\_started/README.md99-173](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L99-L173) [qdrant\_101\_getting\_started/getting\_started.ipynb181-276](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L181-L276)

## Point Operations

### Point Structure and Data Model

```
```

**Point Data Model**: Illustrates the structure of points and the two main patterns for adding data to collections.

Sources: [qdrant\_101\_getting\_started/README.md177-185](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L177-L185) [qdrant\_101\_getting\_started/getting\_started.ipynb313-327](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L313-L327)

### Adding Points in Batches

The `upsert()` method with `models.Batch` efficiently adds multiple points:

```
```

### Adding Individual Points

Single point insertion using `models.PointStruct`:

```
```

### Point Retrieval and Deletion

```
```

Sources: [qdrant\_101\_getting\_started/README.md186-344](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L186-L344) [qdrant\_101\_getting\_started/getting\_started.ipynb334-588](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L334-L588)

## Payload Management

### Payload Structure

Payloads store metadata as JSON objects alongside vectors. Example payload for music recommendation:

```
```

### Adding Points with Payloads

```
```

### Payload Manipulation

```
```

Sources: [qdrant\_101\_getting\_started/README.md345-588](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L345-L588) [qdrant\_101\_getting\_started/getting\_started.ipynb595-991](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L595-L991)

## Search Operations

### Basic Similarity Search

The `search()` method (legacy) or `query_points()` method performs vector similarity search:

```
```

### Filtered Search Operations

```
```

**Search Filtering Workflow**: Shows how filter conditions are constructed and applied to search operations.

### Implementing Filtered Search

```
```

Sources: [qdrant\_101\_getting\_started/README.md489-577](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L489-L577) [qdrant\_101\_getting\_started/getting\_started.ipynb833-991](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L833-L991)

## Recommendation Systems

### Recommendation API

Qdrant's recommendation system uses positive and negative examples to find similar items:

```
```

### Advanced Recommendation Features

```
```

### Score Threshold Usage

The `score_threshold` parameter filters results below a minimum similarity score, preventing low-quality recommendations:

```
```

Sources: [qdrant\_101\_getting\_started/README.md590-700](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L590-L700) [qdrant\_101\_getting\_started/getting\_started.ipynb998-1163](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L998-L1163)

## Storage and Persistence

### Storage Options

Qdrant supports two storage modes:

| Storage Type  | Description                             | Use Case                            |
| ------------- | --------------------------------------- | ----------------------------------- |
| **In-memory** | Stores vectors in RAM                   | Highest speed, temporary data       |
| **Memmap**    | Virtual address space with disk backing | Persistent storage, larger datasets |

### Storage Directory Structure

```
qdrant_storage/
├── aliases/
│   └── data.json
├── collections/
│   └── first_collection/
└── raft_state/
```

The `qdrant_storage` directory is created when running the Docker container and persists all collection data and metadata.

Sources: [qdrant\_101\_getting\_started/README.md154-171](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L154-L171) [qdrant\_101\_getting\_started/getting\_started.ipynb284-305](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L284-L305)

## Key Methods Reference

### Collection Operations

| Method                  | Purpose                    | Parameters                          |
| ----------------------- | -------------------------- | ----------------------------------- |
| `recreate_collection()` | Create/recreate collection | `collection_name`, `vectors_config` |
| `create_collection()`   | Create new collection only | `collection_name`, `vectors_config` |
| `get_collection()`      | Retrieve collection info   | `collection_name`                   |
| `count()`               | Count points in collection | `collection_name`, `exact`          |

### Point Operations

| Method            | Purpose             | Parameters                               |
| ----------------- | ------------------- | ---------------------------------------- |
| `upsert()`        | Add/update points   | `collection_name`, `points`              |
| `retrieve()`      | Get specific points | `collection_name`, `ids`, `with_vectors` |
| `delete()`        | Remove points       | `collection_name`, `points_selector`     |
| `clear_payload()` | Remove payload data | `collection_name`, `points_selector`     |

### Search Operations

| Method           | Purpose                  | Parameters                                                 |
| ---------------- | ------------------------ | ---------------------------------------------------------- |
| `query_points()` | Modern search/recommend  | `collection_name`, `query`, `query_filter`, `limit`        |
| `search()`       | Legacy similarity search | `collection_name`, `query_vector`, `query_filter`, `limit` |
| `recommend()`    | Legacy recommendation    | `collection_name`, `positive`, `negative`, `limit`         |

Sources: [qdrant\_101\_getting\_started/README.md1-720](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/README.md#L1-L720) [qdrant\_101\_getting\_started/getting\_started.ipynb1-1237](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_getting_started/getting_started.ipynb#L1-L1237)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Getting Started with Qdrant](#getting-started-with-qdrant.md)
- [Overview](#overview.md)
- [Architecture Overview](#architecture-overview.md)
- [Installation and Setup](#installation-and-setup.md)
- [Docker Installation](#docker-installation.md)
- [Python Dependencies](#python-dependencies.md)
- [Client Initialization](#client-initialization.md)
- [Collection Management](#collection-management.md)
- [Collection Creation](#collection-creation.md)
- [Supported Distance Metrics](#supported-distance-metrics.md)
- [Collection Health Monitoring](#collection-health-monitoring.md)
- [Point Operations](#point-operations.md)
- [Point Structure and Data Model](#point-structure-and-data-model.md)
- [Adding Points in Batches](#adding-points-in-batches.md)
- [Adding Individual Points](#adding-individual-points.md)
- [Point Retrieval and Deletion](#point-retrieval-and-deletion.md)
- [Payload Management](#payload-management.md)
- [Payload Structure](#payload-structure.md)
- [Adding Points with Payloads](#adding-points-with-payloads.md)
- [Payload Manipulation](#payload-manipulation.md)
- [Search Operations](#search-operations.md)
- [Basic Similarity Search](#basic-similarity-search.md)
- [Filtered Search Operations](#filtered-search-operations.md)
- [Implementing Filtered Search](#implementing-filtered-search.md)
- [Recommendation Systems](#recommendation-systems.md)
- [Recommendation API](#recommendation-api.md)
- [Advanced Recommendation Features](#advanced-recommendation-features.md)
- [Score Threshold Usage](#score-threshold-usage.md)
- [Storage and Persistence](#storage-and-persistence.md)
- [Storage Options](#storage-options.md)
- [Storage Directory Structure](#storage-directory-structure.md)
- [Key Methods Reference](#key-methods-reference.md)
- [Collection Operations](#collection-operations.md)
- [Point Operations](#point-operations-1.md)
- [Search Operations](#search-operations-1.md)
