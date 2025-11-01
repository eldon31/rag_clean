Music Recommendation Engine | qdrant/examples | DeepWiki

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

# Music Recommendation Engine

Relevant source files

- [qdrant\_101\_audio\_data/03\_qdrant\_101\_audio.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/03_qdrant_101_audio.ipynb)
- [qdrant\_101\_audio\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md)
- [qdrant\_101\_text\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data\_files/qdrant\_and\_text\_data\_25\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data_files/qdrant_and_text_data_25_0.png)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data\_files/qdrant\_and\_text\_data\_28\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data_files/qdrant_and_text_data_28_0.png)

This system demonstrates how to build a music recommendation engine using audio embeddings and Qdrant vector database. The implementation covers the complete pipeline from audio data preprocessing through embedding generation to building a web-based recommendation interface using the Ludwig Music Dataset.

For information about other recommendation systems in this repository, see [Movie Recommendations with Sparse Vectors](qdrant/examples/3.3-movie-recommendations-with-sparse-vectors.md).

## System Architecture

The music recommendation system follows a multi-stage pipeline that transforms raw audio files into searchable vector representations:

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md1-1300](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L1-L1300)

## Data Pipeline

### Dataset Structure

The system uses the Ludwig Music Dataset containing over 10,000 songs across multiple genres:

| Component     | Description                               | Location              |
| ------------- | ----------------------------------------- | --------------------- |
| `mp3/`        | Audio files organized by genre            | Genre subdirectories  |
| `labels.json` | Track metadata (artist, genre, subgenres) | Root directory        |
| `spectogram/` | Visual frequency representations          | Optional for analysis |
| `mfccs/`      | Mel-frequency cepstral coefficients       | Alternative features  |

**Sources:** [qdrant\_101\_audio\_data/README.md21-37](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L21-L37)

### Data Preprocessing

The preprocessing pipeline transforms raw audio data into structured formats:

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md133-617](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L133-L617)

## Embedding Generation

### Multiple Model Approaches

The system supports three different audio embedding approaches, each with distinct characteristics:

| Model    | Library           | Dimensions | Use Case             | Performance       |
| -------- | ----------------- | ---------- | -------------------- | ----------------- |
| PANNs    | `panns_inference` | 2048       | Music classification | Fast inference    |
| OpenL3   | `openl3`          | 512        | General audio        | High quality      |
| Wav2Vec2 | `transformers`    | 768        | Speech-focused       | Research baseline |

**Sources:** [qdrant\_101\_audio\_data/README.md631-640](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L631-L640)

### PANNs Implementation

The primary embedding approach uses PANNs (Pre-trained Audio Neural Networks):

```
```

The `get_panns_embs` function processes audio in batches:

**Sources:** [qdrant\_101\_audio\_data/README.md715-810](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L715-L810)

## Vector Database Configuration

### Qdrant Collection Setup

The system creates a dedicated collection with specific parameters:

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md115-125](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L115-L125) [qdrant\_101\_audio\_data/README.md910-925](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L910-L925)

### Payload Structure

Each vector point contains rich metadata for filtering and display:

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md594-617](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L594-L617)

## Query Operations

### Search Functionality

The system provides semantic similarity search using vector queries:

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md964-1100](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L964-L1100)

### Recommendation System

The recommendation API uses positive and negative examples:

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md1085-1220](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L1085-L1220)

## Performance Characteristics

### Model Comparison

Based on the implementation, the different embedding approaches offer distinct trade-offs:

| Aspect           | PANNs     | OpenL3          | Wav2Vec2        |
| ---------------- | --------- | --------------- | --------------- |
| Inference Speed  | Fast      | Slowest         | Medium          |
| Music Quality    | Excellent | Excellent       | Poor            |
| Model Size       | Large     | Medium          | Large           |
| GPU Support      | Yes       | Yes             | Yes             |
| Batch Processing | Efficient | Manual batching | Manual batching |

### Collection Statistics

The tutorial demonstrates performance with a Latin music subset:

- **Dataset Size**: 979 songs (subset of full dataset)
- **Vector Dimensions**: 2048 (PANNs embeddings)
- **Distance Metric**: Cosine similarity
- **Search Speed**: Real-time for interactive use

**Sources:** [qdrant\_101\_audio\_data/README.md707-896](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L707-L896)

## Integration Examples

### Basic Search Example

```
```

### Filtered Recommendation

```
```

**Sources:** [qdrant\_101\_audio\_data/README.md1052-1220](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L1052-L1220)

## Usage Patterns

The system supports multiple interaction patterns:

1. **Content-Based Similarity**: Find songs similar to a given track using `client.search()`
2. **Collaborative Filtering**: Use recommendation API with positive/negative feedback
3. **Filtered Discovery**: Combine vector search with metadata filters for genre-specific recommendations
4. **Interactive Exploration**: Web interface for real-time music discovery

This implementation provides a foundation for building production music recommendation systems with Qdrant's vector database capabilities.

**Sources:** [qdrant\_101\_audio\_data/README.md898-1220](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L898-L1220)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Music Recommendation Engine](#music-recommendation-engine.md)
- [System Architecture](#system-architecture.md)
- [Data Pipeline](#data-pipeline.md)
- [Dataset Structure](#dataset-structure.md)
- [Data Preprocessing](#data-preprocessing.md)
- [Embedding Generation](#embedding-generation.md)
- [Multiple Model Approaches](#multiple-model-approaches.md)
- [PANNs Implementation](#panns-implementation.md)
- [Vector Database Configuration](#vector-database-configuration.md)
- [Qdrant Collection Setup](#qdrant-collection-setup.md)
- [Payload Structure](#payload-structure.md)
- [Query Operations](#query-operations.md)
- [Search Functionality](#search-functionality.md)
- [Recommendation System](#recommendation-system.md)
- [Performance Characteristics](#performance-characteristics.md)
- [Model Comparison](#model-comparison.md)
- [Collection Statistics](#collection-statistics.md)
- [Integration Examples](#integration-examples.md)
- [Basic Search Example](#basic-search-example.md)
- [Filtered Recommendation](#filtered-recommendation.md)
- [Usage Patterns](#usage-patterns.md)
