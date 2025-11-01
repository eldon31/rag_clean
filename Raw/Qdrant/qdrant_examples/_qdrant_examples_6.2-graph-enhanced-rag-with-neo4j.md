Graph-Enhanced RAG with Neo4j | qdrant/examples | DeepWiki

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

# Graph-Enhanced RAG with Neo4j

Relevant source files

- [graphrag\_neo4j/readme.md](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md)

## Purpose and Scope

This page documents the Graph-Enhanced Retrieval-Augmented Generation (RAG) system that integrates Neo4j, Qdrant, and OpenAI's GPT models. The system extracts structured graph relationships from unstructured text, stores them in a Neo4j graph database, and combines these graph relationships with vector search from Qdrant to enhance the context provided to language models. This approach allows for more precise and relationship-aware responses compared to traditional RAG systems that rely solely on vector similarity.

For information about other RAG implementations, see [Recency-Aware RAG with LlamaIndex](qdrant/examples/6.1-multivector-rag-with-dspy.md).

Sources: [graphrag\_neo4j/readme.md1-12](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L1-L12)

## System Architecture

The Graph-Enhanced RAG system implements a pipeline in `graphrag.py` that coordinates three main technologies: `neo4j-graphrag[qdrant]` for graph operations, Qdrant for vector search, and OpenAI for both extraction and generation.

```
```

**Diagram: Graph-Enhanced RAG System Architecture with Code Components**

Sources: [graphrag\_neo4j/readme.md5-11](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L5-L11) [graphrag\_neo4j/readme.md72-90](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L72-L90) [graphrag\_neo4j/readme.md144-146](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L144-L146)

## Key Components

### 1. Graph Extraction

The Graph Extraction component uses OpenAI's GPT models to parse unstructured text and identify entities and relationships between them. This process transforms raw text into a structured graph representation.

```
```

**Diagram: Graph Extraction Process**

The extraction process creates a JSON structure containing source entities, target entities, and the relationships between them. This structured data forms the basis for the graph database.

Sources: [graphrag\_neo4j/readme.md96-107](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L96-L107)

### 2. Neo4j Integration

The Neo4j integration component ingests the extracted graph components into a Neo4j graph database, enabling advanced graph queries.

```
```

**Diagram: Neo4j Data Ingestion**

Neo4j stores nodes labeled as `Entity` and creates relationships between them based on the extracted data. This graph structure allows for traversing relationships and finding connections between entities that might not be apparent in raw text.

Sources: [graphrag\_neo4j/readme.md108-115](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L108-L115)

### 3. Qdrant Vector Search

The Qdrant component handles the vector search functionality, enabling semantic search based on text embeddings.

```
```

**Diagram: Qdrant Vector Search Process**

The system computes embeddings for text segments using OpenAI's embedding models and stores these vectors in a Qdrant collection. When a query is received, it's similarly embedded and matched against the stored vectors to find semantically similar content.

Sources: [graphrag\_neo4j/readme.md116-123](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L116-L123)

### 4. Retrieval-Augmented Generation

The RAG component combines the results from both the vector search and graph database to provide comprehensive context for the language model.

```
```

**Diagram: Retrieval-Augmented Generation Process**

This integrated approach provides several advantages:

- Vector search finds relevant text passages based on semantic similarity
- Graph context provides structured relationship information
- Combined context enables the language model to generate more accurate and insightful responses

Sources: [graphrag\_neo4j/readme.md124-131](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L124-L131)

## Implementation Details

The system is implemented in `graphrag.py` which integrates multiple Python packages and external APIs through a structured pipeline.

### Python Dependencies and Integration

```
```

**Diagram: Python Dependencies and Pipeline Integration**

### Pipeline Execution Steps

The `graphrag.py` script executes the following sequence:

1. **Environment Initialization** - Uses `python-dotenv` to load API credentials from `.env`
2. **Graph Extraction** - Leverages `openai` package and `pydantic` for structured JSON parsing
3. **Data Ingestion** - Uses `neo4j-graphrag[qdrant]` to insert into both databases simultaneously
4. **Retrieval & Graph Querying** - Combines Qdrant vector search with Neo4j graph traversal
5. **RAG Generation** - Merges contexts and generates responses via OpenAI GPT

Sources: [graphrag\_neo4j/readme.md72-90](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L72-L90) [graphrag\_neo4j/readme.md134-149](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L134-L149)

## Configuration and Setup

The system requires configuration for three external services:

| Service | Required Configuration                          |
| ------- | ----------------------------------------------- |
| Qdrant  | API key and URL for Qdrant instance             |
| Neo4j   | Connection URI, username, and password          |
| OpenAI  | API key for accessing GPT models and embeddings |

These configurations should be stored in a `.env` file in the project root directory.

### Environment Setup

Create a `.env` file based on `.env.sample`:

```
# Qdrant configuration
QDRANT_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_instance_url

# Neo4j configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password

# OpenAI configuration
OPENAI_API_KEY=your_openai_api_key
```

### Dependencies and Project Structure

| File               | Purpose                                                                                |
| ------------------ | -------------------------------------------------------------------------------------- |
| `graphrag.py`      | Main pipeline implementation containing all graph extraction, ingestion, and RAG logic |
| `requirements.txt` | Python package dependencies                                                            |
| `.env.sample`      | Template for environment variables configuration                                       |
| `.env`             | Actual environment variables (created from sample)                                     |

**Required Python Packages:**

- `neo4j-graphrag[qdrant]` - Integrated graph and vector database operations
- `python-dotenv` - Environment variable loading
- `pydantic` - Data validation for JSON extraction
- `openai` - GPT models and embeddings API

Sources: [graphrag\_neo4j/readme.md14-60](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L14-L60) [graphrag\_neo4j/readme.md134-149](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L134-L149)

## Usage

### Running the System

Execute the complete pipeline with:

```
```

### Pipeline Operations

The `graphrag.py` script performs these operations in sequence:

| Step | Operation                  | Technical Details                                                             |
| ---- | -------------------------- | ----------------------------------------------------------------------------- |
| 1    | Environment Initialization | Loads credentials from `.env` using `python-dotenv`                           |
| 2    | Graph Extraction           | Uses OpenAI GPT to parse text into structured JSON with `pydantic` validation |
| 3    | Neo4j Ingestion            | Creates `Entity` nodes and relationship edges via `neo4j-graphrag`            |
| 4    | Qdrant Ingestion           | Generates embeddings with OpenAI API and stores in Qdrant collection          |
| 5    | Vector Search              | Performs semantic search against Qdrant embeddings                            |
| 6    | Graph Querying             | Executes Neo4j queries to find related entities and relationships             |
| 7    | RAG Generation             | Merges vector and graph contexts for OpenAI GPT response generation           |

### Console Output

The script provides detailed logging for:

- Graph extraction progress and JSON validation
- Database ingestion status for both Neo4j and Qdrant
- Vector search results and similarity scores
- Graph query results and relationship traversals
- Final generated responses with context sources

Sources: [graphrag\_neo4j/readme.md64-90](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L64-L90)

## Advantages of Graph-Enhanced RAG

The integration of graph databases with vector search offers several benefits over traditional RAG systems:

| Feature                | Benefit                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| Relationship awareness | Captures explicit relationships between entities that may not be apparent in raw text        |
| Structured context     | Provides language models with structured information about how entities relate to each other |
| Improved reasoning     | Enables more accurate responses for queries that require understanding relationships         |
| Fact verification      | Graph data can serve as a structured knowledge base to verify generated content              |
| Complex query support  | Supports multi-hop relationship queries that would be difficult with vector search alone     |

This approach represents an evolution of RAG systems by combining the strengths of vector search (finding semantically similar content) with graph databases (understanding relationships between entities).

Sources: [graphrag\_neo4j/readme.md3-11](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L3-L11)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Graph-Enhanced RAG with Neo4j](#graph-enhanced-rag-with-neo4j.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Architecture](#system-architecture.md)
- [Key Components](#key-components.md)
- [1. Graph Extraction](#1-graph-extraction.md)
- [2. Neo4j Integration](#2-neo4j-integration.md)
- [3. Qdrant Vector Search](#3-qdrant-vector-search.md)
- [4. Retrieval-Augmented Generation](#4-retrieval-augmented-generation.md)
- [Implementation Details](#implementation-details.md)
- [Python Dependencies and Integration](#python-dependencies-and-integration.md)
- [Pipeline Execution Steps](#pipeline-execution-steps.md)
- [Configuration and Setup](#configuration-and-setup.md)
- [Environment Setup](#environment-setup.md)
- [Dependencies and Project Structure](#dependencies-and-project-structure.md)
- [Usage](#usage.md)
- [Running the System](#running-the-system.md)
- [Pipeline Operations](#pipeline-operations.md)
- [Console Output](#console-output.md)
- [Advantages of Graph-Enhanced RAG](#advantages-of-graph-enhanced-rag.md)
