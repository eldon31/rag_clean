Text Data Applications | qdrant/examples | DeepWiki

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

# Text Data Applications

Relevant source files

- [README.md](https://github.com/qdrant/examples/blob/b3c4b28f/README.md)
- [code-search/code-search.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb)
- [qdrant\_101\_audio\_data/03\_qdrant\_101\_audio.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/03_qdrant_101_audio.ipynb)
- [qdrant\_101\_audio\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md)
- [qdrant\_101\_text\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data\_files/qdrant\_and\_text\_data\_25\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data_files/qdrant_and_text_data_25_0.png)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data\_files/qdrant\_and\_text\_data\_28\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data_files/qdrant_and_text_data_28_0.png)
- [sparse-vectors-movies-reco/recommend-movies.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb)

This page covers text processing, embedding generation, and various text-based search and recommendation systems using Qdrant. It demonstrates how to transform textual data into vector representations and build semantic search capabilities for different domains including news articles, code repositories, and collaborative filtering systems.

For audio data applications, see [Audio Data Applications](qdrant/examples/5-audio-data-applications.md). For advanced RAG implementations that combine text processing with generation, see [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md).

## Core Text Processing Pipeline

The foundation of text applications involves transforming raw text into numerical vector representations that capture semantic meaning. This process enables similarity search and recommendation systems.

```
```

**Text Processing Pipeline Architecture**

Sources: [qdrant\_101\_text\_data/README.md1-100](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md#L1-L100) [code-search/code-search.ipynb1-50](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L1-L50) [sparse-vectors-movies-reco/recommend-movies.ipynb1-50](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L1-L50)

## Embedding Generation Approaches

### Dense Text Embeddings

The primary approach uses transformer models to generate dense vector representations. The `embed_text` function demonstrates the core embedding pipeline:

```
```

**Dense Embedding Generation Flow**

The `mean_pooling` function handles attention-weighted averaging to convert token-level embeddings to sentence-level representations:

Sources: [qdrant\_101\_text\_data/README.md378-415](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md#L378-L415)

### Code-Specific Text Processing

For code search applications, the `textify` function normalizes code structures into human-readable descriptions:

```
```

**Code Search Dual Embedding Architecture**

Sources: [code-search/code-search.ipynb125-191](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L125-L191) [code-search/code-search.ipynb333-349](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L333-L349)

### Sparse Vector Representations

For collaborative filtering, user preferences are encoded as sparse vectors where indices represent items and values represent ratings:

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb417-429](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L417-L429)

## Qdrant Collection Management

### Collection Configuration

Different text applications require specific collection configurations based on the embedding approach:

| Application           | Vector Config             | Distance Metric | Dimensions |
| --------------------- | ------------------------- | --------------- | ---------- |
| News Articles         | Dense only                | Cosine          | 768        |
| Code Search           | Named vectors (text/code) | Cosine          | 384/768    |
| Movie Recommendations | Sparse vectors only       | Dot Product     | Dynamic    |

### Data Upload Patterns

The `upsert` operation loads embeddings with structured payloads:

```
```

**Qdrant Data Upload Flow**

Sources: [qdrant\_101\_text\_data/README.md574-583](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md#L574-L583) [code-search/code-search.ipynb387-414](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L387-L414)

## Search and Recommendation Systems

### Semantic Search Implementation

The search functionality uses vector similarity to find relevant documents:

```
```

**Semantic Search Architecture**

Sources: [qdrant\_101\_text\_data/README.md680-690](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md#L680-L690)

### Recommendation API Usage

The recommendation system finds similar items using positive and negative examples:

```
```

**Recommendation System Flow**

Sources: [qdrant\_101\_text\_data/README.md726-750](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md#L726-L750)

### Code Search Query Processing

Code search supports both natural language and code-specific queries using named vectors:

Sources: [code-search/code-search.ipynb504-518](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L504-L518) [code-search/code-search.ipynb554-568](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L554-L568)

## Advanced Text Applications

### Collaborative Filtering with Sparse Vectors

Movie recommendation uses sparse vectors where each dimension represents a movie and values represent normalized ratings. The `user_sparse_vectors` structure efficiently encodes user preferences:

```
```

**Collaborative Filtering Architecture**

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb403-409](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L403-L409) [sparse-vectors-movies-reco/recommend-movies.ipynb420-429](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L420-L429) [sparse-vectors-movies-reco/recommend-movies.ipynb527-535](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L527-L535)

### Multi-Model Code Search

The code search system demonstrates how to combine different embedding approaches for comprehensive search capabilities. The `points` structure uses named vectors to store both text and code representations simultaneously.

Sources: [code-search/code-search.ipynb387-398](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L387-L398)

## Implementation Examples

### Basic Text Collection Setup

```
```

### Named Vector Configuration

```
```

### Sparse Vector Setup

```
```

Sources: [qdrant\_101\_text\_data/README.md539-544](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md#L539-L544) [code-search/code-search.ipynb336-349](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L336-L349) [sparse-vectors-movies-reco/recommend-movies.ipynb463-469](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L463-L469)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Text Data Applications](#text-data-applications.md)
- [Core Text Processing Pipeline](#core-text-processing-pipeline.md)
- [Embedding Generation Approaches](#embedding-generation-approaches.md)
- [Dense Text Embeddings](#dense-text-embeddings.md)
- [Code-Specific Text Processing](#code-specific-text-processing.md)
- [Sparse Vector Representations](#sparse-vector-representations.md)
- [Qdrant Collection Management](#qdrant-collection-management.md)
- [Collection Configuration](#collection-configuration.md)
- [Data Upload Patterns](#data-upload-patterns.md)
- [Search and Recommendation Systems](#search-and-recommendation-systems.md)
- [Semantic Search Implementation](#semantic-search-implementation.md)
- [Recommendation API Usage](#recommendation-api-usage.md)
- [Code Search Query Processing](#code-search-query-processing.md)
- [Advanced Text Applications](#advanced-text-applications.md)
- [Collaborative Filtering with Sparse Vectors](#collaborative-filtering-with-sparse-vectors.md)
- [Multi-Model Code Search](#multi-model-code-search.md)
- [Implementation Examples](#implementation-examples.md)
- [Basic Text Collection Setup](#basic-text-collection-setup.md)
- [Named Vector Configuration](#named-vector-configuration.md)
- [Sparse Vector Setup](#sparse-vector-setup.md)
