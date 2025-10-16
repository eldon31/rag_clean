Advanced RAG Systems | qdrant/examples | DeepWiki

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

# Advanced RAG Systems

Relevant source files

- [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb)
- [graphrag\_neo4j/readme.md](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md)
- [multivector-representation/multivector\_representation\_qdrant.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb)
- [pdf-retrieval-at-scale/ColPali\_ColQwen2\_Tutorial.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb)

This page provides an overview of sophisticated Retrieval-Augmented Generation (RAG) systems implemented in the Qdrant examples repository. While basic RAG systems enhance Large Language Models (LLMs) with relevant context retrieved from a vector database, advanced RAG systems incorporate additional techniques such as multivector search, graph relationships, and specialized document processing to improve retrieval quality and response accuracy.

The scope of this document covers:

- Multivector RAG with DSPy framework for medical applications
- Graph-enhanced RAG using Neo4j for relationship-aware retrieval
- PDF retrieval at scale using visual document understanding models

For information about basic vector operations, see [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md). For specific text applications that use simpler RAG, see [Text Data Applications](qdrant/examples/3-text-data-applications.md).

Sources: [multivector-representation/multivector\_representation\_qdrant.ipynb8-23](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L8-L23) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb20-29](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L20-L29) [graphrag\_neo4j/readme.md3-12](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L3-L12) [pdf-retrieval-at-scale/ColPali\_ColQwen2\_Tutorial.ipynb8-27](https://github.com/qdrant/examples/blob/b3c4b28f/pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb#L8-L27)

## Architecture Overview of Advanced RAG Systems

Advanced RAG systems extend the basic RAG architecture by incorporating sophisticated retrieval techniques that go beyond simple vector similarity search. These enhancements address common limitations in traditional RAG systems, such as the inability to capture complex relationships between entities, fine-grained token-level matching, or visual document understanding.

**Advanced RAG System Architecture**

```
```

The key distinguishing factors of advanced RAG systems include multivector search capabilities, graph-enhanced context, and framework-based orchestration for complex reasoning tasks.

Sources: [multivector-representation/multivector\_representation\_qdrant.ipynb207-225](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L207-L225) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb552-571](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L552-L571) [graphrag\_neo4j/readme.md7-11](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L7-L11)

### Comparison of Basic vs Advanced RAG

| Feature                          | Basic RAG                             | Advanced RAG                                                                      |
| -------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------- |
| Context Source                   | Direct document retrieval             | Enhanced with graph relationships, multivector reranking, or visual understanding |
| Retrieval Method                 | Single embedding similarity search    | Hybrid approaches: prefetch + rerank, graph + vector, visual + textual            |
| Vector Representations           | Single dense vector per document      | Multiple vectors: dense + ColBERT, visual + textual                               |
| Response Quality                 | Good for simple factual questions     | Better for complex, relationship-based, or multimodal queries                     |
| Implementation Complexity        | Lower                                 | Higher                                                                            |
| Handling of Token-level Matching | Limited to document-level similarity  | Fine-grained token interactions via ColBERT                                       |
| Understanding of Relationships   | Limited to what's in single documents | Can traverse complex entity relationships via graph databases                     |
| Framework Integration            | Basic LLM calls                       | Sophisticated frameworks like DSPy with guardrails and reasoning                  |

Sources: [multivector-representation/multivector\_representation\_qdrant.ipynb337-354](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L337-L354) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb785-794](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L785-L794) [graphrag\_neo4j/readme.md5-12](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L5-L12)

## Multivector RAG with DSPy

Multivector RAG combines dense embeddings for efficient retrieval with ColBERT multivectors for fine-grained reranking. This approach addresses limitations of single-vector systems by enabling token-level interactions while maintaining search efficiency.

**Multivector RAG Architecture**

```
```

### Key Components

1. **Dual Embedding Models**:

   - `BAAI/bge-small-en` for dense embeddings (384 dimensions)
   - `colbert-ir/colbertv2.0` for late-interaction multivectors (128 dimensions)

2. **Qdrant Configuration**:

   - Dense vector with HNSW indexing enabled for fast retrieval
   - ColBERT multivector with indexing disabled (`hnsw_config=models.HnswConfigDiff(m=0)`) for reranking

3. **DSPy Framework Integration**:

   - `QdrantRM` retrieval module for DSPy integration
   - `dspy.ChainOfThought` for structured reasoning
   - Guardrails for domain-specific constraints

4. **Two-Stage Retrieval Process**:

   - Prefetch candidates using dense vector search
   - Rerank using ColBERT multivector with MaxSim comparator

### Implementation Details

The multivector system uses Qdrant's native support for multiple vector types per document:

```
```

The retrieval process combines both vector types in a single query:

```
```

Sources: [multivector-representation/multivector\_representation\_qdrant.ipynb207-225](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L207-L225) [multivector-representation/multivector\_representation\_qdrant.ipynb292-302](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L292-L302) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb222-252](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L222-L252) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb376-383](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L376-L383)

## Graph-Enhanced RAG with Neo4j

Graph-Enhanced RAG combines traditional vector-based retrieval with graph database capabilities to capture and utilize relationships between entities in the data. This approach significantly improves response quality for queries that require understanding complex relationships.

**Graph-Enhanced RAG Architecture**

```
```

### Key Components

1. **Graph Extraction Pipeline**:

   - Uses OpenAI's GPT models to parse raw text and extract structured entities and relationships
   - Outputs graph components in a structured JSON format, including node-relationship-node triples

2. **Dual Storage System**:

   - **Qdrant**: Stores text embeddings for semantic search
   - **Neo4j**: Stores graph structure (entities as nodes, connections as edges)

3. **Hybrid Query Processing**:

   - Vector search in Qdrant identifies relevant text passages
   - Graph queries in Neo4j retrieve related entities and their relationships
   - Both results are combined to form a comprehensive context

4. **Enhanced Context Generation**:

   - The enriched context contains both relevant text and graph relationships
   - Provides the language model with structured information about connections between entities

### Implementation Details

The implementation follows these steps:

1. **Environment Initialization**: Loads API keys and database credentials from environment variables

2. **Graph Extraction**:

   - Uses OpenAI to convert unstructured text into a structured graph
   - The output includes entities (nodes) and their relationships (edges)

3. **Data Ingestion**:

   - Neo4j: Inserts extracted nodes labeled as `Entity` and their relationships
   - Qdrant: Computes embeddings for text segments and uploads them to a collection

4. **Retrieval & Graph Querying**:

   - Performs vector search in Qdrant to find relevant text
   - Queries Neo4j to fetch related graph context
   - Combines both results to enrich the prompt

5. **Response Generation**:

   - Uses the enriched context to generate detailed answers via OpenAI's GPT

Sources: [graphrag\_neo4j/readme.md5-130](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L5-L130)

## PDF Retrieval at Scale

PDF retrieval at scale addresses the challenge of efficiently searching large collections of visual documents using Vision Language Models (VLLMs) like ColPali and ColQwen2. These models work directly with PDF pages as images, avoiding complex OCR and text extraction pipelines.

**PDF Retrieval at Scale Architecture**

```
```

### Key Components

1. **Vision Language Models**:

   - **ColPali**: Generates \~1,024 vectors per PDF page
   - **ColQwen2**: Generates \~700 vectors per page (dynamically adjusted)

2. **Scaling Challenge**:

   - Building HNSW index with full vectors requires \~49 million comparisons per page
   - For 20,000 pages, this becomes computationally prohibitive

3. **Optimization Strategy**:

   - Apply mean pooling to reduce vectors (e.g., 1,024 patches → 32 vectors)
   - Use compressed vectors for first-stage retrieval
   - Keep full vectors for precise reranking

4. **Two-Stage Process**:

   - **Stage 1**: Fast retrieval using mean-pooled vectors
   - **Stage 2**: Rerank top candidates using original full-resolution vectors

### Mathematical Foundation

The scaling problem is quantified in the computational complexity:

For ColQwen2 with \~700 vectors per page and HNSW `ef_construct=100`:

- Comparisons per page: `700 × 700 × 100 = 49,000,000`
- For a 20,000 page collection: `49M × 20,000 = 980 trillion comparisons`

Mean pooling reduces this by organizing patches into a grid and averaging within groups:

- ColPali: `1,024 patches → 32×32 grid → 32 pooled vectors`
- Reduction factor: `1,024 / 32 = 32x` fewer vectors

### Implementation Approach

The system processes PDF pages as visual documents:

1. **PDF Page Processing**: Convert each page to an image representation
2. **Multivector Generation**: Use ColPali/ColQwen2 to generate patch-based embeddings
3. **Mean Pooling**: Group patches by spatial location and average embeddings
4. **Dual Storage**: Store both compressed (indexed) and full (non-indexed) vectors
5. **Query Processing**: First retrieve with compressed vectors, then rerank with full vectors

Sources: [pdf-retrieval-at-scale/ColPali\_ColQwen2\_Tutorial.ipynb36-67](https://github.com/qdrant/examples/blob/b3c4b28f/pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb#L36-L67) [pdf-retrieval-at-scale/ColPali\_ColQwen2\_Tutorial.ipynb40-53](https://github.com/qdrant/examples/blob/b3c4b28f/pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb#L40-L53)

## When to Use Each Advanced RAG Approach

| Aspect                        | Multivector RAG                                          | Graph-Enhanced RAG                                            | PDF Retrieval at Scale                                  |
| ----------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------- |
| **Best For**                  | Fine-grained text matching                               | Relationship-heavy domains                                    | Visual document collections                             |
| **Ideal Use Cases**           | Medical Q\&A, technical documentation, precise retrieval | Knowledge graphs, organizational data, entity-centric domains | Academic papers, reports, forms, mixed-format documents |
| **Key Strength**              | Token-level similarity                                   | Entity relationships                                          | Visual understanding without OCR                        |
| **Vector Types**              | Dense + ColBERT multivectors                             | Dense embeddings + graph structure                            | Visual multivectors (ColPali/ColQwen2)                  |
| **Implementation Complexity** | Moderate                                                 | High                                                          | High                                                    |
| **Required Infrastructure**   | Qdrant with multivector support                          | Qdrant + Neo4j                                                | Qdrant with optimization strategies                     |
| **Computational Overhead**    | Medium (reranking)                                       | Medium-High (graph queries)                                   | High (but optimized with pooling)                       |
| **Framework Integration**     | DSPy, FastEmbed                                          | OpenAI GPT, custom extractors                                 | Vision Language Models                                  |

### Decision Guide

Choose **Multivector RAG** when:

- You need precise token-level matching beyond document similarity
- Your domain requires fine-grained retrieval (medical, legal, technical)
- You want to combine fast retrieval with accurate reranking

Choose **Graph-Enhanced RAG** when:

- Your domain involves complex relationships between entities
- Queries require understanding connections across multiple documents
- You need structured knowledge representation alongside vector search

Choose **PDF Retrieval at Scale** when:

- You have large collections of visual documents (PDFs, forms, reports)
- OCR quality is poor or documents contain complex layouts
- You need to search both text and visual elements in documents

These approaches can be combined for maximum effectiveness in complex domains requiring multiple types of understanding.

Sources: [multivector-representation/multivector\_representation\_qdrant.ipynb346-354](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L346-L354) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb785-794](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L785-L794) [graphrag\_neo4j/readme.md96-130](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L96-L130) [pdf-retrieval-at-scale/ColPali\_ColQwen2\_Tutorial.ipynb55-67](https://github.com/qdrant/examples/blob/b3c4b28f/pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb#L55-L67)

## Implementation Considerations

When implementing advanced RAG systems in your own applications, consider these factors:

1. **Data Preparation**:

   - **Multivector RAG**: Ensure quality document chunking and consider computational costs of ColBERT encoding
   - **Graph-Enhanced RAG**: Invest in high-quality entity extraction and relationship modeling
   - **PDF Retrieval**: Prepare visual documents and consider mean pooling strategies for large collections

2. **Infrastructure Requirements**:

   - **Multivector RAG**: Qdrant with multivector support and sufficient storage for multiple embeddings per document
   - **Graph-Enhanced RAG**: Qdrant + Neo4j with appropriate connection handling and graph query optimization
   - **PDF Retrieval**: High-memory systems for processing visual models and storage for both compressed and full vectors

3. **Performance Optimization**:

   - **Multivector systems**: Use indexing strategies (HNSW for dense, disabled for reranking vectors)
   - **Graph systems**: Limit graph traversal depth and implement caching for frequent entity queries
   - **PDF systems**: Implement two-stage retrieval with mean pooling to manage computational complexity

4. **Framework Integration**:

   - **DSPy Integration**: Use `QdrantRM` for seamless integration with DSPy modules and chain-of-thought reasoning
   - **Guardrails**: Implement domain-specific validation (e.g., medical question filtering)
   - **Error Handling**: Robust handling of embedding failures and graph query timeouts

5. **Evaluation Metrics**:

   - **Multivector**: Measure both retrieval recall and reranking precision improvements
   - **Graph-Enhanced**: Evaluate relationship accuracy and context completeness
   - **PDF Retrieval**: Assess visual understanding quality and computational efficiency gains

### Code Integration Patterns

Key implementation patterns from the examples:

```
```

Sources: [multivector-representation/multivector\_representation\_qdrant.ipynb207-225](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L207-L225) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb552-571](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L552-L571) [graphrag\_neo4j/readme.md15-21](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L15-L21) [pdf-retrieval-at-scale/ColPali\_ColQwen2\_Tutorial.ipynb55-67](https://github.com/qdrant/examples/blob/b3c4b28f/pdf-retrieval-at-scale/ColPali_ColQwen2_Tutorial.ipynb#L55-L67)

## Conclusion

Advanced RAG systems represent a significant evolution beyond basic retrieval-augmented generation. By incorporating time awareness or graph relationships, these systems can provide more contextually rich and accurate responses, especially for complex or time-sensitive queries.

The Qdrant examples repository demonstrates two powerful approaches:

1. **Recency-Aware RAG** with LlamaIndex for time-sensitive applications
2. **Graph-Enhanced RAG** with Neo4j for relationship-rich domains

These implementations showcase how vector databases like Qdrant can be extended and integrated with other systems to create more sophisticated knowledge retrieval architectures.

Sources: [graphrag\_neo4j/readme.md3-12](https://github.com/qdrant/examples/blob/b3c4b28f/graphrag_neo4j/readme.md#L3-L12)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Advanced RAG Systems](#advanced-rag-systems.md)
- [Architecture Overview of Advanced RAG Systems](#architecture-overview-of-advanced-rag-systems.md)
- [Comparison of Basic vs Advanced RAG](#comparison-of-basic-vs-advanced-rag.md)
- [Multivector RAG with DSPy](#multivector-rag-with-dspy.md)
- [Key Components](#key-components.md)
- [Implementation Details](#implementation-details.md)
- [Graph-Enhanced RAG with Neo4j](#graph-enhanced-rag-with-neo4j.md)
- [Key Components](#key-components-1.md)
- [Implementation Details](#implementation-details-1.md)
- [PDF Retrieval at Scale](#pdf-retrieval-at-scale.md)
- [Key Components](#key-components-2.md)
- [Mathematical Foundation](#mathematical-foundation.md)
- [Implementation Approach](#implementation-approach.md)
- [When to Use Each Advanced RAG Approach](#when-to-use-each-advanced-rag-approach.md)
- [Decision Guide](#decision-guide.md)
- [Implementation Considerations](#implementation-considerations.md)
- [Code Integration Patterns](#code-integration-patterns.md)
- [Conclusion](#conclusion.md)
