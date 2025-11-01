Self-Query Systems with LangChain | qdrant/examples | DeepWiki

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

# Self-Query Systems with LangChain

Relevant source files

- [self-query/self-query.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb)
- [self-query/winemag-data-130k-v2.csv](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/winemag-data-130k-v2.csv)

This document covers the implementation of self-querying retrieval systems using LangChain's `SelfQueryRetriever` with Qdrant vector database. The system translates natural language queries into structured vector searches with metadata filtering, enabling more precise and contextually relevant information retrieval.

For information about other advanced RAG patterns, see [Multivector RAG with DSPy](qdrant/examples/6.1-multivector-rag-with-dspy.md), [Graph-Enhanced RAG with Neo4j](qdrant/examples/6.2-graph-enhanced-rag-with-neo4j.md), and [Agentic Systems with CrewAI](qdrant/examples/7-agentic-systems-with-crewai.md).

## System Overview

The self-query system addresses a fundamental challenge in vector search: translating complex natural language queries that contain both semantic content and structured constraints into appropriate vector searches with metadata filters. Instead of embedding the entire query (including filter criteria), the system separates semantic content from metadata constraints.

```
```

**Sources**: [self-query/self-query.ipynb396-455](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L396-L455)

## Data Preparation and Embedding Pipeline

The system processes wine review data into a structured format suitable for both vector search and metadata filtering. Each document contains semantic content (wine descriptions) and structured metadata (country, price, points, variety).

### Document Structure and Schema

```
```

**Sources**: [self-query/self-query.ipynb237-295](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L237-L295)

### Embedding and Collection Setup

The system uses `SentenceTransformer` with the "all-MiniLM-L6-v2" model for generating embeddings and stores them in a Qdrant collection with cosine distance similarity.

| Component             | Configuration            | Purpose                             |
| --------------------- | ------------------------ | ----------------------------------- |
| `SentenceTransformer` | "all-MiniLM-L6-v2"       | Generate 384-dimensional embeddings |
| `QdrantClient`        | Remote/local connection  | Vector database operations          |
| Collection            | "wine\_reviews"          | Store embeddings and metadata       |
| Distance Metric       | `models.Distance.COSINE` | Similarity calculation              |
| Vector Size           | 384 dimensions           | Embedding dimensionality            |

**Sources**: [self-query/self-query.ipynb16-31](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L16-L31) [self-query/self-query.ipynb215-228](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L215-L228)

## Self-Query Retriever Architecture

The `SelfQueryRetriever` serves as the core component that orchestrates query translation and retrieval. It requires metadata field definitions, document content descriptions, and an LLM for query parsing.

### Metadata Schema Definition

```
```

**Sources**: [self-query/self-query.ipynb424-454](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L424-L454)

## Query Translation Process

The self-query system transforms natural language into structured queries through a multi-step process involving prompt engineering, LLM reasoning, and structured output parsing.

### Translation Pipeline

```
```

**Sources**: [self-query/self-query.ipynb525-627](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L525-L627)

### Filter Construction

The system translates natural language constraints into Qdrant filter objects using logical operators and field conditions:

| Natural Language | Generated Filter                     | Qdrant Implementation                                                                 |
| ---------------- | ------------------------------------ | ------------------------------------------------------------------------------------- |
| "US wines"       | `eq("country", "US")`                | `models.FieldCondition(key="metadata.country", match=models.MatchValue(value="US"))`  |
| "between $15-30" | `gte("price", 15), lte("price", 30)` | `models.FieldCondition(key="metadata.price", range=models.Range(gte=15.0, lte=30.0))` |
| "90+ points"     | `gt("points", 90)`                   | `models.FieldCondition(key="metadata.points", range=models.Range(gte=90))`            |

**Sources**: [self-query/self-query.ipynb369-385](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L369-L385)

## Implementation Example

The following demonstrates a complete query flow from natural language to structured results:

### Query Execution Flow

```
```

**Sources**: [self-query/self-query.ipynb477-514](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L477-L514)

## System Configuration and Dependencies

### Core Dependencies

| Component               | Version/Model      | Purpose                        |
| ----------------------- | ------------------ | ------------------------------ |
| `qdrant-client`         | Latest             | Vector database client         |
| `sentence-transformers` | "all-MiniLM-L6-v2" | Text embedding generation      |
| `langchain`             | Latest             | Self-query retriever framework |
| `langchain-openai`      | ChatOpenAI         | Query translation LLM          |
| `langchain-qdrant`      | QdrantVectorStore  | Vector store integration       |
| `pandas`                | Latest             | Data manipulation              |

### Environment Setup

The system requires API keys and connection configuration for external services:

```
```

**Sources**: [self-query/self-query.ipynb16-31](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L16-L31) [self-query/self-query.ipynb396-415](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L396-L415)

## Performance and Tracing

The system includes tracing capabilities to monitor query translation and execution:

### Query Tracing Output

The `ConsoleCallbackHandler` provides detailed visibility into the query construction process, showing:

- Prompt template construction
- LLM query processing with token usage
- Filter generation and parsing
- Final query execution

**Sources**: [self-query/self-query.ipynb525-627](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L525-L627)

This self-query implementation demonstrates how to bridge natural language interfaces with structured vector search systems, enabling more intuitive and precise information retrieval while maintaining the performance benefits of vector similarity search combined with efficient metadata filtering.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Self-Query Systems with LangChain](#self-query-systems-with-langchain.md)
- [System Overview](#system-overview.md)
- [Data Preparation and Embedding Pipeline](#data-preparation-and-embedding-pipeline.md)
- [Document Structure and Schema](#document-structure-and-schema.md)
- [Embedding and Collection Setup](#embedding-and-collection-setup.md)
- [Self-Query Retriever Architecture](#self-query-retriever-architecture.md)
- [Metadata Schema Definition](#metadata-schema-definition.md)
- [Query Translation Process](#query-translation-process.md)
- [Translation Pipeline](#translation-pipeline.md)
- [Filter Construction](#filter-construction.md)
- [Implementation Example](#implementation-example.md)
- [Query Execution Flow](#query-execution-flow.md)
- [System Configuration and Dependencies](#system-configuration-and-dependencies.md)
- [Core Dependencies](#core-dependencies.md)
- [Environment Setup](#environment-setup.md)
- [Performance and Tracing](#performance-and-tracing.md)
- [Query Tracing Output](#query-tracing-output.md)
