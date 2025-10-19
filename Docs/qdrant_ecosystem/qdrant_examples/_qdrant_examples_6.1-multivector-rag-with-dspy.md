Multivector RAG with DSPy | qdrant/examples | DeepWiki

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

# Multivector RAG with DSPy

Relevant source files

- [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb)
- [multivector-representation/multivector\_representation\_qdrant.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb)

## Purpose and Scope

This document covers the implementation of multivector retrieval-augmented generation (RAG) systems that combine dense and late-interaction embeddings with DSPy framework programming. The system demonstrates how to use Qdrant's multivector capabilities for efficient retrieval and reranking workflows, specifically applied to medical question-answering applications.

For basic Qdrant setup and operations, see [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md). For other RAG implementations, see [Graph-Enhanced RAG with Neo4j](qdrant/examples/6.2-graph-enhanced-rag-with-neo4j.md) and [PDF Retrieval at Scale](qdrant/examples/6.3-pdf-retrieval-at-scale.md).

## System Architecture

The multivector RAG system operates on a two-stage retrieval pipeline combining fast dense vector search with precise ColBERT reranking.

### Core Components Architecture

```
```

**Sources:** [multivector-representation/multivector\_representation\_qdrant.ipynb1-382](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L1-L382) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb1-801](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L1-L801)

### Multivector Configuration Details

The system uses distinct vector configurations optimized for different retrieval stages:

| Vector Type | Model                    | Size | Distance | Indexing              | Purpose                |
| ----------- | ------------------------ | ---- | -------- | --------------------- | ---------------------- |
| `dense`     | `BAAI/bge-small-en`      | 384  | COSINE   | HNSW enabled          | Fast initial retrieval |
| `colbert`   | `colbert-ir/colbertv2.0` | 128  | COSINE   | HNSW disabled (`m=0`) | Precise reranking      |

The ColBERT vector includes `MultiVectorConfig` with `MAX_SIM` comparator for token-level similarity computation.

**Sources:** [multivector-representation/multivector\_representation\_qdrant.ipynb206-225](https://github.com/qdrant/examples/blob/b3c4b28f/multivector-representation/multivector_representation_qdrant.ipynb#L206-L225) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb222-252](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L222-L252)

## DSPy Integration Architecture

### DSPy Component Mapping

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb375-389](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L375-L389) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb478-486](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L478-L486)

### MedicalAnswer Signature Structure

The `MedicalAnswer` signature defines the input-output contract for the DSPy system:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb478-486](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L478-L486)

## Medical Application Implementation

### Document Processing Pipeline

The medical bot processes documents from the MIRIAD dataset with dual embedding generation:

```
```

Documents are uploaded in batches with both vector types and structured payload:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb185-194](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L185-L194) [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb294-305](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L294-L305)

### Payload Indexing Configuration

The system creates specialized indexes for efficient filtering:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb241-252](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L241-L252)

## Query Pipeline Architecture

### Two-Stage Retrieval Process

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb414-450](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L414-L450)

### Reranking Implementation

The `rerank_with_colbert` function implements the complete retrieval pipeline:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb414-450](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L414-L450)

## Guardrail System

### Medical Question Classification

The `MedicalGuardrail` module provides input validation to ensure only medical questions are processed:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb515-524](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L515-L524)

### MedicalRAG Module Integration

The main `MedicalRAG` module coordinates guardrails, retrieval, and response generation:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb553-571](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L553-L571)

### Specialty Categories

The system supports filtering across 47 medical specialties including:

| Primary Specialties          | Surgical Specialties     | Research Areas                     |
| ---------------------------- | ------------------------ | ---------------------------------- |
| `Rheumatology`               | `General Surgery`        | `Medical Research & Methodology`   |
| `Cardiology`                 | `Orthopedic Surgery`     | `Public Health & Epidemiology`     |
| `Neurology`                  | `Neurosurgery`           | `Medical Ethics & Law`             |
| `Endocrinology & Metabolism` | `Cardiothoracic Surgery` | `Medical Technology & Informatics` |

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb624-637](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L624-L637)

## Performance Characteristics

### Multivector Benefits

The system achieves optimal performance through:

1. **Fast Initial Retrieval**: Dense vectors with HNSW indexing enable sub-millisecond candidate selection
2. **Precise Reranking**: ColBERT multivectors provide token-level MaxSim scoring without indexing overhead
3. **Memory Efficiency**: Disabled HNSW on ColBERT vectors (`m=0`) reduces storage requirements
4. **Single API Call**: Combined prefetch + rerank operations minimize network latency

### Batch Processing Configuration

Large-scale document processing uses batch uploads to handle ColBERT's \~1000 vectors per document:

```
```

**Sources:** [DSPy-medical-bot/medical\_bot\_DSPy\_Qdrant.ipynb290-316](https://github.com/qdrant/examples/blob/b3c4b28f/DSPy-medical-bot/medical_bot_DSPy_Qdrant.ipynb#L290-L316)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Multivector RAG with DSPy](#multivector-rag-with-dspy.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Architecture](#system-architecture.md)
- [Core Components Architecture](#core-components-architecture.md)
- [Multivector Configuration Details](#multivector-configuration-details.md)
- [DSPy Integration Architecture](#dspy-integration-architecture.md)
- [DSPy Component Mapping](#dspy-component-mapping.md)
- [MedicalAnswer Signature Structure](#medicalanswer-signature-structure.md)
- [Medical Application Implementation](#medical-application-implementation.md)
- [Document Processing Pipeline](#document-processing-pipeline.md)
- [Payload Indexing Configuration](#payload-indexing-configuration.md)
- [Query Pipeline Architecture](#query-pipeline-architecture.md)
- [Two-Stage Retrieval Process](#two-stage-retrieval-process.md)
- [Reranking Implementation](#reranking-implementation.md)
- [Guardrail System](#guardrail-system.md)
- [Medical Question Classification](#medical-question-classification.md)
- [MedicalRAG Module Integration](#medicalrag-module-integration.md)
- [Specialty Categories](#specialty-categories.md)
- [Performance Characteristics](#performance-characteristics.md)
- [Multivector Benefits](#multivector-benefits.md)
- [Batch Processing Configuration](#batch-processing-configuration.md)
