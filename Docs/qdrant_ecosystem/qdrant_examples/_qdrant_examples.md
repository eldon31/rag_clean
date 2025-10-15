qdrant/examples | DeepWiki

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

# Overview

Relevant source files

- [.gitignore](https://github.com/qdrant/examples/blob/b3c4b28f/.gitignore)
- [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb)
- [README.md](https://github.com/qdrant/examples/blob/b3c4b28f/README.md)
- [code-search/code-search.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb)
- [multivector-representation/multivector\_representation\_qdrant.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb)
- [sparse-vectors-movies-reco/recommend-movies.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb)

This wiki provides documentation for the [Qdrant Examples](<https://github.com/qdrant/examples/blob/b3c4b28f/Qdrant Examples>) repository, a collection of tutorials, demos, and how-to guides demonstrating the use of Qdrant vector database and adjacent technologies for various applications. From basic similarity search to advanced retrieval-augmented generation (RAG) systems, these examples showcase real-world implementations across different data modalities (text, images, audio) and use cases.

Sources: [README.md1-3](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L1-L3)

## Purpose and Scope

The Qdrant Examples repository aims to demonstrate practical implementations of vector search technology using Qdrant. The examples progress from basic vector database operations to sophisticated AI applications, serving both educational and reference purposes for developers.

Key aspects covered:

- Basic vector operations and similarity search
- Domain-specific applications for text, image, and audio data
- Advanced AI integrations such as RAG systems and agentic frameworks
- Integration patterns with other technologies (OpenAI, Cohere, CLIP, etc.)

For specifics on getting started with basic Qdrant functionality, see [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md).

Sources: [README.md3-17](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L3-L17)

## Repository Structure

The repository is organized into categories based on complexity and data modality, allowing users to find relevant examples for their specific needs.

```
```

Sources: [README.md5-17](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L5-L17)

## Example Types and Progression

The examples in the repository follow a progression from basic to advanced, demonstrating increasingly sophisticated applications of vector search technology.

| Level        | Example Type                  | Technologies                              | Examples                                                    |
| ------------ | ----------------------------- | ----------------------------------------- | ----------------------------------------------------------- |
| Basic        | Fundamental vector operations | Qdrant, NumPy, Faker                      | Qdrant 101 Getting Started                                  |
| Intermediate | Domain-specific applications  | Transformers, CLIP, Sentence-Transformers | Code Search, E-commerce Image Search, Movie Recommendations |
| Advanced     | AI integration systems        | OpenAI, LlamaIndex, Cohere, CrewAI        | Recency-Aware RAG, Graph-Enhanced RAG, Agentic Systems      |

Sources: [README.md5-17](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L5-L17)

## Core Processing Pipeline

Most examples in the repository follow a similar data processing pattern despite addressing different domains and use cases.

```
```

Sources: [README.md5-17](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L5-L17) [code-search/code-search.ipynb6-9](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L6-L9) [sparse-vectors-movies-reco/recommend-movies.ipynb7-25](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L7-L25)

## Vector Search Implementations

The repository demonstrates various vector search implementations across different data modalities:

### Text Data Applications

Text-based examples showcase how to build search applications for natural language, code, and structured text data using embeddings.

```
```

Key text applications include:

- Code search using dual embeddings (general-purpose and code-specific)
- Extractive question answering
- Movie recommendations using collaborative filtering with sparse vectors

Sources: [README.md9-10](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L9-L10) [README.md16](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L16-L16) [code-search/code-search.ipynb6-9](https://github.com/qdrant/examples/blob/b3c4b28f/code-search/code-search.ipynb#L6-L9) [sparse-vectors-movies-reco/recommend-movies.ipynb7-25](https://github.com/qdrant/examples/blob/b3c4b28f/sparse-vectors-movies-reco/recommend-movies.ipynb#L7-L25)

### Image Data Applications

Image-based examples demonstrate how to build visual search systems across domains:

```
```

Key image applications include:

- E-commerce reverse image search using CLIP embeddings
- Medical image similarity search with vision transformers

Sources: [README.md12](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L12-L12) [README.md4](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L4-L4)

### Audio Data Applications

Audio examples showcase music recommendation and audio similarity search:

```
```

Key audio applications include:

- Music recommendation systems using audio feature embeddings

Sources: [README.md11](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L11-L11) [README.md5](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L5-L5)

## Advanced AI Integrations

The repository includes advanced examples integrating Qdrant with modern AI frameworks:

### Retrieval-Augmented Generation (RAG) Systems

```
```

Key RAG examples include:

- Recency-aware RAG with LlamaIndex
- Graph-enhanced RAG with Neo4j integration
- Basic RAG pipelines with various LLM providers

Sources: [README.md8-9](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L8-L9) [README.md6](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L6-L6)

### Agentic Systems

```
```

Key agentic examples include:

- Multi-agent systems using CrewAI for orchestration
- Meeting analysis with agentic RAG

Sources: [README.md7](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L7-L7)

## Integration Technologies

The examples in the repository integrate with various AI and data processing technologies:

| Category         | Technologies                                  | Purpose                                     |
| ---------------- | --------------------------------------------- | ------------------------------------------- |
| Embedding Models | SentenceTransformers, CLIP, OpenL3, FastEmbed | Converting data to vector representations   |
| Language Models  | OpenAI, Cohere, Hugging Face                  | Text generation, reranking, embeddings      |
| Frameworks       | LlamaIndex, LangChain, CrewAI                 | Building LLM applications and agent systems |
| Infrastructure   | AWS Lambda, Hugging Face Spaces               | Deployment and hosting                      |
| Databases        | Neo4j, Qdrant                                 | Graph data, vector storage                  |

Sources: [README.md5-17](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L5-L17)

## Starting with the Examples

Each example in the repository is self-contained and includes the necessary code and documentation to understand and run the implementation. To get started:

1. Clone the repository: `git clone https://github.com/qdrant/examples.git`
2. Navigate to the specific example directory
3. Follow the README or notebook instructions within each example

For fundamental Qdrant concepts and operations, see [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md).

Sources: [README.md3-4](https://github.com/qdrant/examples/blob/b3c4b28f/README.md#L3-L4)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Overview](#overview.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Repository Structure](#repository-structure.md)
- [Example Types and Progression](#example-types-and-progression.md)
- [Core Processing Pipeline](#core-processing-pipeline.md)
- [Vector Search Implementations](#vector-search-implementations.md)
- [Text Data Applications](#text-data-applications.md)
- [Image Data Applications](#image-data-applications.md)
- [Audio Data Applications](#audio-data-applications.md)
- [Advanced AI Integrations](#advanced-ai-integrations.md)
- [Retrieval-Augmented Generation (RAG) Systems](#retrieval-augmented-generation-rag-systems.md)
- [Agentic Systems](#agentic-systems.md)
- [Integration Technologies](#integration-technologies.md)
- [Starting with the Examples](#starting-with-the-examples.md)
