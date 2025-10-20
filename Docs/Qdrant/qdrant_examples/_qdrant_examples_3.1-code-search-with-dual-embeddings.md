Code Search with Dual Embeddings | qdrant/examples | DeepWiki

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

# Code Search with Dual Embeddings

Relevant source files

- [README.md](https://github.com/qdrant/examples/blob/b3c4b28f/README.md)
- [code-search/code-search.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb)
- [sparse-vectors-movies-reco/recommend-movies.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb)

This document describes the implementation of a semantic code search system that uses dual embedding approaches to enable both natural language and code-specific queries. The system leverages two different neural encoders to provide comprehensive search capabilities across a codebase.

For information about basic text processing and embedding generation, see [Text Data Applications](qdrant/examples/3-text-data-applications.md). For advanced retrieval patterns and multivector approaches, see [Multivector RAG with DSPy](qdrant/examples/6.1-multivector-rag-with-dspy.md).

## System Architecture

The code search system implements a dual embedding strategy using Qdrant's named vectors capability to store and query code structures using two different embedding models simultaneously.

```
```

Sources: [code-search/code-search.ipynb1-700](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L1-L700)

## Data Processing Pipeline

The system processes code structures through two parallel transformation pipelines to create embeddings suitable for different types of queries.

### Code Structure Format

Each code structure contains comprehensive metadata about code entities:

| Field               | Description          | Example                                 |
| ------------------- | -------------------- | --------------------------------------- |
| `name`              | Entity identifier    | `"InvertedIndexRam"`                    |
| `signature`         | Full code signature  | `"pub struct InvertedIndexRam { ... }"` |
| `code_type`         | Entity type          | `"Struct"`, `"Function"`                |
| `docstring`         | Documentation string | `"Inverted flatten index..."`           |
| `context.module`    | Module location      | `"inverted_index"`                      |
| `context.file_path` | Full file path       | `"lib/sparse/src/index/..."`            |
| `context.snippet`   | Raw code snippet     | Actual code with syntax                 |

Sources: [code-search/code-search.ipynb77-105](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L77-L105)

### Text Normalization Process

The `textify()` function converts code structures into natural language representations for general purpose embedding models.

```
```

Sources: [code-search/code-search.ipynb130-191](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L130-L191)

## Embedding Strategy Comparison

The dual embedding approach leverages the strengths of both general purpose and code-specific models:

| Aspect     | General Purpose Model                    | Code-Specific Model                   |
| ---------- | ---------------------------------------- | ------------------------------------- |
| Model      | `sentence-transformers/all-MiniLM-L6-v2` | `jinaai/jina-embeddings-v2-base-code` |
| Input      | Normalized text via `textify()`          | Raw code snippets                     |
| Dimension  | 384                                      | 768                                   |
| Query Type | Natural language descriptions            | Code syntax patterns                  |
| Use Case   | "How do I count points?"                 | Function signatures, structures       |

Sources: [code-search/code-search.ipynb114-191](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L114-L191) [code-search/code-search.ipynb282-287](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L282-L287)

## Collection Configuration

The Qdrant collection uses named vectors to store both embedding types in a single collection:

```
```

Sources: [code-search/code-search.ipynb336-348](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L336-L348) [code-search/code-search.ipynb387-399](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L387-L399)

## Query Processing Methods

The system supports multiple query processing approaches to balance relevance and diversity:

### Single Model Query

```
```

### Batch Query Processing

```
```

### Grouped Query for Diversity

```
```

Sources: [code-search/code-search.ipynb504-518](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L504-L518) [code-search/code-search.ipynb609-637](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L609-L637) [code-search/code-search.ipynb672-690](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L672-L690)

## Implementation Details

### Data Upload Process

The system uses `models.PointStruct` to create indexed points with dual embeddings:

```
```

Sources: [code-search/code-search.ipynb387-399](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L387-L399) [code-search/code-search.ipynb409-414](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L409-L414)

### Query Result Processing

Results from both embedding models are processed to extract relevant code entities:

| Result Field                          | Content          | Usage                      |
| ------------------------------------- | ---------------- | -------------------------- |
| `hit.score`                           | Similarity score | Ranking and filtering      |
| `hit.payload["context"]["module"]`    | Module name      | Grouping and organization  |
| `hit.payload["context"]["file_name"]` | File identifier  | Source location            |
| `hit.payload["signature"]`            | Code signature   | Display and identification |

Sources: [code-search/code-search.ipynb511-518](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L511-L518) [code-search/code-search.ipynb562-568](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L562-L568)

## Search Performance Characteristics

The dual embedding approach provides different search behaviors:

### General Purpose Model Results

- Higher semantic understanding of natural language queries
- Better handling of conceptual searches like "count points in collection"
- Returns broader, more conceptually related results

### Code-Specific Model Results

- More precise matching of code patterns and structures
- Better for searching specific function signatures or implementations
- Higher relevance for code syntax-based queries

Sources: [code-search/code-search.ipynb504-518](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L504-L518) [code-search/code-search.ipynb554-569](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L554-L569)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Code Search with Dual Embeddings](#code-search-with-dual-embeddings.md)
- [System Architecture](#system-architecture.md)
- [Data Processing Pipeline](#data-processing-pipeline.md)
- [Code Structure Format](#code-structure-format.md)
- [Text Normalization Process](#text-normalization-process.md)
- [Embedding Strategy Comparison](#embedding-strategy-comparison.md)
- [Collection Configuration](#collection-configuration.md)
- [Query Processing Methods](#query-processing-methods.md)
- [Single Model Query](#single-model-query.md)
- [Batch Query Processing](#batch-query-processing.md)
- [Grouped Query for Diversity](#grouped-query-for-diversity.md)
- [Implementation Details](#implementation-details.md)
- [Data Upload Process](#data-upload-process.md)
- [Query Result Processing](#query-result-processing.md)
- [Search Performance Characteristics](#search-performance-characteristics.md)
- [General Purpose Model Results](#general-purpose-model-results.md)
- [Code-Specific Model Results](#code-specific-model-results.md)
