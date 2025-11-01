Agentic Systems with CrewAI | qdrant/examples | DeepWiki

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

# Agentic Systems with CrewAI

Relevant source files

- [agentic\_rag\_zoom\_crewai/.env.example](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/.env.example)
- [agentic\_rag\_zoom\_crewai/data/user\_1NMxS3qhkROnLEsHmf0XiJ.txt](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_1NMxS3qhkROnLEsHmf0XiJ.txt)
- [agentic\_rag\_zoom\_crewai/data/user\_1rydFrQocHdttmKsA0OhkV.txt](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_1rydFrQocHdttmKsA0OhkV.txt)
- [agentic\_rag\_zoom\_crewai/data/user\_2ibz7AAZ0cPTlw584CMT3K.txt](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_2ibz7AAZ0cPTlw584CMT3K.txt)
- [agentic\_rag\_zoom\_crewai/readme.md](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md)
- [agentic\_rag\_zoom\_crewai/tutorial.md](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/tutorial.md)
- [agentic\_rag\_zoom\_crewai/vector/crew.py](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py)

This document covers the advanced agentic RAG implementation using the CrewAI framework for multi-agent orchestration and collaborative intelligence. The system demonstrates how to build sophisticated AI workflows that combine vector search capabilities with specialized agent teams to analyze and extract insights from meeting recordings.

For basic RAG implementations, see [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md). For self-querying approaches, see [Self-Query Systems with LangChain](qdrant/examples/8.1-self-query-systems-with-langchain.md).

## System Overview

The agentic RAG system represents an evolution from traditional retrieval-augmented generation by introducing multiple specialized AI agents that collaborate to process complex queries. Rather than a single model handling both retrieval and generation, this architecture employs distinct agents with specific roles and capabilities working in coordinated workflows.

The implementation focuses on meeting analysis, where agents can search through vectorized meeting transcripts, perform calculations on meeting data, and generate comprehensive insights using advanced language models. This approach enables more nuanced reasoning and multi-step problem solving compared to conventional RAG systems.

## Architecture Components

### Multi-Agent Workflow Architecture

```
```

Sources: [agentic\_rag\_zoom\_crewai/vector/crew.py1-206](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L1-L206) [agentic\_rag\_zoom\_crewai/readme.md1-192](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L1-L192)

### Agent Roles and Responsibilities

The system implements a two-agent architecture where each agent has distinct responsibilities:

| Agent         | Role                    | Tools Available                                               | Primary Function                           |
| ------------- | ----------------------- | ------------------------------------------------------------- | ------------------------------------------ |
| `researcher`  | Research Assistant      | `CalculatorTool`, `SearchMeetingsTool`, `MeetingAnalysisTool` | Information gathering and initial analysis |
| `synthesizer` | Information Synthesizer | None (processes research results)                             | Response generation and insight synthesis  |

The research agent handles the computational and retrieval aspects, while the synthesis agent focuses on creating coherent, actionable responses from the gathered information.

Sources: [agentic\_rag\_zoom\_crewai/vector/crew.py143-159](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L143-L159)

## Core Implementation

### Agent Tool System

The tool-based architecture enables agents to perform specific operations through well-defined interfaces:

#### Calculator Tool Implementation

```
```

#### Vector Search Tool Implementation

```
```

#### Analysis Tool Implementation

```
```

Sources: [agentic\_rag\_zoom\_crewai/vector/crew.py45-135](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L45-L135)

### Vector Search Integration

The system integrates with Qdrant through the `SearchMeetingsTool`, which converts natural language queries into vector embeddings and performs semantic search:

```
```

The search process uses OpenAI's `text-embedding-ada-002` model to maintain consistency with the data ingestion pipeline and applies a score threshold of 0.7 to ensure result quality.

Sources: [agentic\_rag\_zoom\_crewai/vector/crew.py61-85](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L61-L85)

### Task Orchestration

The CrewAI framework coordinates agent activities through structured tasks with defined expectations:

#### Research Task Configuration

```
```

#### Synthesis Task Configuration

```
```

Sources: [agentic\_rag\_zoom\_crewai/vector/crew.py162-184](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L162-L184)

## Data Processing Pipeline

### Meeting Data Structure

The system processes structured meeting data with the following schema:

```
```

Sources: [agentic\_rag\_zoom\_crewai/readme.md17-34](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L17-L34) [agentic\_rag\_zoom\_crewai/data/user\_1rydFrQocHdttmKsA0OhkV.txt1-64](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_1rydFrQocHdttmKsA0OhkV.txt#L1-L64)

### Vector Embedding Process

The data loading pipeline converts meeting content into searchable vectors:

1. **Text Preparation**: Combines meeting topic, VTT content, and summary into structured text
2. **Embedding Generation**: Uses OpenAI's embedding model for vector creation
3. **Batch Processing**: Uploads data in batches of 100 for efficiency
4. **Collection Management**: Maintains the `zoom_recordings` collection in Qdrant

The embedding process creates comprehensive representations that capture both the semantic content and structured metadata of each meeting.

Sources: [agentic\_rag\_zoom\_crewai/readme.md94-108](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L94-L108)

## Usage Patterns

### Query Processing Workflow

The system handles various query types through intelligent tool selection:

```
```

### Example Query Types

The system supports various analytical queries:

- **Computational**: "What's the average duration of marketing meetings?"
- **Search-based**: "Find meetings about product launches"
- **Analytical**: "Analyze the key themes from executive meetings"
- **Hybrid**: "Compare meeting patterns across different departments"

Each query type triggers appropriate tool combinations, with the research agent determining the optimal workflow path.

Sources: [agentic\_rag\_zoom\_crewai/readme.md136-143](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L136-L143)

### Response Generation

The synthesis agent creates structured responses that include:

- Direct answers to user queries
- Supporting evidence from vector search results
- Explanations of the analysis process
- Actionable insights derived from meeting data

This approach ensures transparency in the reasoning process while providing comprehensive answers to complex queries.

Sources: [agentic\_rag\_zoom\_crewai/vector/crew.py175-184](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L175-L184)

## Technical Integration

### Environment Configuration

The system requires multiple API credentials and service endpoints:

```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

### Service Dependencies

The implementation integrates with several external services:

- **Qdrant Cloud**: Vector database for meeting storage and search
- **OpenAI API**: Embedding generation and potential model fallbacks
- **Anthropic Claude**: Advanced language understanding and response generation
- **CrewAI Framework**: Agent orchestration and workflow management

Sources: [agentic\_rag\_zoom\_crewai/.env.example1-4](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/.env.example#L1-L4) [agentic\_rag\_zoom\_crewai/vector/crew.py15-28](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L15-L28)

The agentic approach demonstrates how specialized AI agents can collaborate to handle complex analytical tasks that require both retrieval capabilities and sophisticated reasoning, representing a significant advancement over traditional single-model RAG implementations.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Agentic Systems with CrewAI](#agentic-systems-with-crewai.md)
- [System Overview](#system-overview.md)
- [Architecture Components](#architecture-components.md)
- [Multi-Agent Workflow Architecture](#multi-agent-workflow-architecture.md)
- [Agent Roles and Responsibilities](#agent-roles-and-responsibilities.md)
- [Core Implementation](#core-implementation.md)
- [Agent Tool System](#agent-tool-system.md)
- [Calculator Tool Implementation](#calculator-tool-implementation.md)
- [Vector Search Tool Implementation](#vector-search-tool-implementation.md)
- [Analysis Tool Implementation](#analysis-tool-implementation.md)
- [Vector Search Integration](#vector-search-integration.md)
- [Task Orchestration](#task-orchestration.md)
- [Research Task Configuration](#research-task-configuration.md)
- [Synthesis Task Configuration](#synthesis-task-configuration.md)
- [Data Processing Pipeline](#data-processing-pipeline.md)
- [Meeting Data Structure](#meeting-data-structure.md)
- [Vector Embedding Process](#vector-embedding-process.md)
- [Usage Patterns](#usage-patterns.md)
- [Query Processing Workflow](#query-processing-workflow.md)
- [Example Query Types](#example-query-types.md)
- [Response Generation](#response-generation.md)
- [Technical Integration](#technical-integration.md)
- [Environment Configuration](#environment-configuration.md)
- [Service Dependencies](#service-dependencies.md)
