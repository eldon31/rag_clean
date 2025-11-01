Audio Data Applications | qdrant/examples | DeepWiki

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

# Audio Data Applications

Relevant source files

- [qdrant\_101\_audio\_data/03\_qdrant\_101\_audio.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/03_qdrant_101_audio.ipynb)
- [qdrant\_101\_audio\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md)
- [qdrant\_101\_text\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/README.md)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data\_files/qdrant\_and\_text\_data\_25\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data_files/qdrant_and_text_data_25_0.png)
- [qdrant\_101\_text\_data/qdrant\_and\_text\_data\_files/qdrant\_and\_text\_data\_28\_0.png](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_text_data/qdrant_and_text_data_files/qdrant_and_text_data_28_0.png)

This document covers audio data processing and music recommendation systems using Qdrant vector database. The implementation demonstrates how to extract embeddings from audio files and build semantic search and recommendation engines for music discovery.

For text-based search and recommendations, see [Text Data Applications](qdrant/examples/3-text-data-applications.md). For image-based similarity search, see [Image Data Applications](qdrant/examples/4-image-data-applications.md).

## Overview

The audio data applications showcase a complete pipeline for processing music files and building recommendation systems. The implementation uses the Ludwig Music Dataset containing over 10,000 songs across different genres and subgenres, demonstrating three different approaches to audio embedding generation and their integration with Qdrant's vector search capabilities.

**Audio Processing Pipeline**

```
```

Sources: [qdrant\_101\_audio\_data/README.md1-52](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L1-L52) [qdrant\_101\_audio\_data/README.md620-642](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L620-L642)

## Dataset and Data Preparation

The system processes the Ludwig Music Dataset, which provides a comprehensive collection for music information retrieval (MIR). The dataset structure includes multiple data modalities and metadata for each track.

**Dataset Structure**

| Component     | Description                         | Purpose                                   |
| ------------- | ----------------------------------- | ----------------------------------------- |
| `mp3/`        | Audio files by genre                | Raw audio data for embedding generation   |
| `labels.json` | Track metadata                      | Artist, genre, subgenre, name information |
| `spectogram/` | Visual frequency representations    | Alternative data representation           |
| `mfccs/`      | Mel-frequency cepstral coefficients | Audio feature representations             |

**Data Processing Components**

```
```

The data preparation pipeline extracts unique identifiers from audio file paths and processes the complex nested metadata structure from `labels.json`. The `get_metadata()` function normalizes artist, genre, name, and subgenre information, while `get_vals()` flattens the subgenre lists for easier processing.

Sources: [qdrant\_101\_audio\_data/README.md131-617](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L131-L617) [qdrant\_101\_audio\_data/README.md196-235](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L196-L235)

## Audio Embedding Generation

The system implements three distinct approaches for generating audio embeddings, each with different characteristics and use cases. The embeddings capture important audio features such as pitch, timbre, and spatial characteristics of sound.

**Embedding Architecture Comparison**

```
```

### OpenL3 Implementation

OpenL3 provides pre-trained models specifically designed for audio processing tasks. The implementation uses the music-specific model with mel128 input representation.

**Key Functions:**

- `get_open_embs()`: Batch processing function for embedding extraction
- `openl3.models.load_audio_embedding_model()`: Model initialization with specific parameters
- Mean pooling over timestamp dimension for fixed-size embeddings

### PANNS Inference Implementation

The PANNS (PANNs: Large-Scale Pretrained Audio Neural Networks) approach offers the best performance for music classification tasks and is used as the primary method in the tutorial.

**Core Components:**

- `AudioTagging` class initialization with automatic checkpoint download
- `at.inference()` method for batch processing
- Direct 2048-dimensional embedding output without additional pooling

### Transformers Wav2Vec2 Implementation

The Wav2Vec2 approach demonstrates transformer architecture adaptation for audio, though optimized for speech rather than music.

**Processing Pipeline:**

- Audio resampling to 16kHz for model compatibility
- `AutoFeatureExtractor` for input preprocessing
- `mean_pooling()` function for sequence-to-vector conversion

Sources: [qdrant\_101\_audio\_data/README.md644-897](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L644-L897) [qdrant\_101\_audio\_data/README.md746-800](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L746-L800)

## Qdrant Vector Database Integration

The audio embeddings are stored and managed using Qdrant vector database, configured specifically for audio similarity search and recommendation tasks.

**Database Configuration**

```
```

### Collection Configuration

The `music_collection` is configured with:

- **Vector dimension**: 2048 (matching PANNS output)
- **Distance metric**: COSINE similarity
- **Payload structure**: Artist, genre, name, subgenres, file URLs

### Payload Structure

The metadata payload contains structured information for each track:

```
```

Sources: [qdrant\_101\_audio\_data/README.md898-919](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L898-L919) [qdrant\_101\_audio\_data/README.md115-126](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L115-L126)

## Music Recommendation System

The recommendation system leverages Qdrant's search and recommendation APIs to provide semantic music discovery based on audio content similarity.

**Recommendation Architecture**

```
```

### Search Functionality

The system implements multiple search patterns:

1. **Vector Similarity Search**: Direct comparison using pre-computed embeddings
2. **Recommendation API**: Using positive and negative examples for refined results
3. **Filtered Search**: Combining semantic similarity with metadata constraints

### Example Usage Patterns

**Basic Similarity Search**:

- Query with embedding vector from existing track
- Returns top-k most similar tracks with similarity scores
- Includes full metadata payload for each result

**Recommendation with Preferences**:

- Specify positive examples (liked tracks)
- Optional negative examples (disliked tracks)
- Qdrant computes optimized recommendation vector

**Genre-Filtered Search**:

- Combine vector similarity with metadata filtering
- Use `models.Filter` and `models.FieldCondition` for constraints
- Example: Find similar tracks within "Business" or "Latin" genres

Sources: [qdrant\_101\_audio\_data/README.md920-1216](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L920-L1216) [qdrant\_101\_audio\_data/README.md1053-1091](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L1053-L1091)

## System Integration and Architecture

The complete audio processing system integrates multiple components into a cohesive music recommendation platform.

**End-to-End System Flow**

```
```

### Key Performance Characteristics

| Embedding Method | Dimensions | Quality | Speed  | Use Case            |
| ---------------- | ---------- | ------- | ------ | ------------------- |
| OpenL3           | 512        | High    | Slow   | Research/Accuracy   |
| PANNS Inference  | 2048       | Highest | Fast   | Production          |
| Wav2Vec2         | 768        | Lower   | Medium | Speech/Experimental |

### Scalability Considerations

The system architecture supports scaling through:

- **Batch Processing**: Efficient embedding generation for large datasets
- **Vector Database**: Qdrant's optimized storage and retrieval
- **Flexible Embedding**: Support for multiple embedding approaches
- **Metadata Integration**: Rich payload structure for complex queries

Sources: [qdrant\_101\_audio\_data/README.md1-52](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L1-L52) [qdrant\_101\_audio\_data/README.md898-1216](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_audio_data/README.md#L898-L1216)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Audio Data Applications](#audio-data-applications.md)
- [Overview](#overview.md)
- [Dataset and Data Preparation](#dataset-and-data-preparation.md)
- [Audio Embedding Generation](#audio-embedding-generation.md)
- [OpenL3 Implementation](#openl3-implementation.md)
- [PANNS Inference Implementation](#panns-inference-implementation.md)
- [Transformers Wav2Vec2 Implementation](#transformers-wav2vec2-implementation.md)
- [Qdrant Vector Database Integration](#qdrant-vector-database-integration.md)
- [Collection Configuration](#collection-configuration.md)
- [Payload Structure](#payload-structure.md)
- [Music Recommendation System](#music-recommendation-system.md)
- [Search Functionality](#search-functionality.md)
- [Example Usage Patterns](#example-usage-patterns.md)
- [System Integration and Architecture](#system-integration-and-architecture.md)
- [Key Performance Characteristics](#key-performance-characteristics.md)
- [Scalability Considerations](#scalability-considerations.md)
