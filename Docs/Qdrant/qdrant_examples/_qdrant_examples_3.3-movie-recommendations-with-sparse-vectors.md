Movie Recommendations with Sparse Vectors | qdrant/examples | DeepWiki

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

# Movie Recommendations with Sparse Vectors

Relevant source files

- [README.md](https://github.com/qdrant/examples/blob/b3c4b28f/README.md)
- [code-search/code-search.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb)
- [sparse-vectors-movies-reco/recommend-movies.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb)

## Purpose

This document explains how to implement a movie recommendation system using collaborative filtering with Qdrant's sparse vector capabilities. We'll demonstrate how to represent user preferences as sparse vectors, find similar users based on these vectors, and generate personalized movie recommendations. This approach is particularly efficient for recommendation systems with large, sparse feature spaces.

Sources: [README.md9-16](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L9-L16) [sparse-vectors-movies-reco/recommend-movies.ipynb6-25](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L6-L25)

## Overview

Collaborative filtering is a recommendation technique that finds patterns in user behavior to predict preferences. It works on the premise that if two users have similar tastes (rated similar movies similarly), they will likely have similar preferences for other movies. This example leverages Qdrant's sparse vector capabilities to implement a collaborative filtering system using the MovieLens dataset.

The key workflow is:

1. Represent each user's movie ratings as a sparse vector
2. Index these vectors in Qdrant
3. Find users with similar taste patterns
4. Recommend movies that similar users liked but the target user hasn't seen

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb6-25](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L6-L25)

## Sparse Vectors for Collaborative Filtering

### What are Sparse Vectors?

Sparse vectors contain mostly zero values, with only a few non-zero entries. In the context of movie recommendations:

- Each dimension represents a movie ID
- The value at that dimension represents the user's rating
- Most users rate only a tiny fraction of all available movies, making the vector sparse

Qdrant efficiently handles sparse vectors by only storing non-zero values (values and their indices), significantly reducing storage requirements and improving search performance for recommendation systems.

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb416-428](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L416-L428)

## Implementation Steps

### 1. Data Preparation

First, we load the MovieLens dataset, which contains:

- User information (demographics)
- Movie information (title, genres)
- User ratings for movies

```
```

The ratings are normalized to have a mean of 0 and standard deviation of 1. This normalization is particularly important for sparse vectors as it allows us to capture both positive and negative preferences.

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb210-408](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L210-L408)

### 2. Converting Ratings to Sparse Vectors

Each user's ratings are converted into a sparse vector format with two components:

- `values`: The normalized rating values
- `indices`: The corresponding movie IDs

```
```

This structure efficiently represents each user's preferences across the entire movie space by only storing the movies they've actually rated.

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb416-428](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L416-L428)

### 3. Setting Up Qdrant Collection

Unlike dense vector collections that require a pre-defined dimension, sparse vector collections in Qdrant don't need dimension specification since the dimensionality is determined by the indices in the data.

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb460-469](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L460-L469)

### 4. Indexing User Preference Vectors

Each user's sparse rating vector is uploaded to Qdrant along with their demographic information:

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb480-494](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L480-L494)

### 5. Querying Similar Users

To generate recommendations, we first create a sparse vector of our own movie preferences:

```
```

Then we search for similar users using Qdrant's vector similarity search:

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb510-554](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L510-L554)

### 6. Generating Recommendations

From the similar users' ratings, we identify movies they liked that the target user hasn't rated yet:

```
```

The final recommendations are generated by sorting movies by their aggregated scores:

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb562-603](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L562-L603)

## Advanced Features

### Filtered Recommendations

Qdrant allows filtering recommendations based on user demographics or other metadata. For example, you can find similar users within a specific age group:

```
```

This feature enables more personalized recommendations by leveraging both similarity in taste and demographic information.

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb622-649](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L622-L649)

## System Architecture

The overall architecture of the movie recommendation system is as follows:

```
```

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb6-649](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L6-L649)

## Performance Considerations

Sparse vectors are particularly efficient for collaborative filtering recommendation systems because:

1. **Storage Efficiency**: Only non-zero values are stored, greatly reducing memory requirements for large catalogs with millions of items.

2. **Computational Efficiency**: Similarity calculations only consider dimensions with non-zero values in at least one of the vectors.

3. **Interpretability**: The sparse approach maintains clear relationships between dimensions (movie IDs) and values (ratings), making the system more interpretable.

4. **Scalability**: The system can easily accommodate new movies without retraining, as they simply become new dimensions in the sparse vector space.

For production use cases, it's recommended to use a server-based Qdrant instance rather than the in-memory version shown in the example.

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb436-440](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L436-L440)

## Conclusion

This implementation demonstrates how Qdrant's sparse vector capabilities can be leveraged to build an effective collaborative filtering recommendation system. The approach is particularly suitable for domains with large, sparse feature spaces like movie recommendations, e-commerce product recommendations, or content suggestions.

By representing user preferences as sparse vectors and utilizing Qdrant's vector search capabilities, we can efficiently find similar users and generate personalized recommendations with minimal computational overhead.

Sources: [sparse-vectors-movies-reco/recommend-movies.ipynb6-649](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L6-L649) [README.md16](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L16-L16)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Movie Recommendations with Sparse Vectors](#movie-recommendations-with-sparse-vectors.md)
- [Purpose](#purpose.md)
- [Overview](#overview.md)
- [Sparse Vectors for Collaborative Filtering](#sparse-vectors-for-collaborative-filtering.md)
- [What are Sparse Vectors?](#what-are-sparse-vectors.md)
- [Implementation Steps](#implementation-steps.md)
- [1. Data Preparation](#1-data-preparation.md)
- [2. Converting Ratings to Sparse Vectors](#2-converting-ratings-to-sparse-vectors.md)
- [3. Setting Up Qdrant Collection](#3-setting-up-qdrant-collection.md)
- [4. Indexing User Preference Vectors](#4-indexing-user-preference-vectors.md)
- [5. Querying Similar Users](#5-querying-similar-users.md)
- [6. Generating Recommendations](#6-generating-recommendations.md)
- [Advanced Features](#advanced-features.md)
- [Filtered Recommendations](#filtered-recommendations.md)
- [System Architecture](#system-architecture.md)
- [Performance Considerations](#performance-considerations.md)
- [Conclusion](#conclusion.md)
