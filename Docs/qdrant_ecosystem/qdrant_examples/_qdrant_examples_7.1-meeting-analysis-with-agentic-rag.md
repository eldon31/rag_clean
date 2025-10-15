Meeting Analysis with Agentic RAG | qdrant/examples | DeepWiki

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

# Meeting Analysis with Agentic RAG

Relevant source files

- [agentic\_rag\_zoom\_crewai/.env.example](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/.env.example)
- [agentic\_rag\_zoom\_crewai/data/user\_1NMxS3qhkROnLEsHmf0XiJ.txt](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_1NMxS3qhkROnLEsHmf0XiJ.txt)
- [agentic\_rag\_zoom\_crewai/data/user\_1rydFrQocHdttmKsA0OhkV.txt](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_1rydFrQocHdttmKsA0OhkV.txt)
- [agentic\_rag\_zoom\_crewai/data/user\_2ibz7AAZ0cPTlw584CMT3K.txt](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_2ibz7AAZ0cPTlw584CMT3K.txt)
- [agentic\_rag\_zoom\_crewai/readme.md](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md)
- [agentic\_rag\_zoom\_crewai/tutorial.md](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/tutorial.md)
- [agentic\_rag\_zoom\_crewai/vector/crew.py](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py)

## Purpose and Scope

This system demonstrates an Agentic RAG (Retrieval-Augmented Generation) implementation that analyzes meeting recordings using a combination of vector search and AI agents. The system processes meeting transcripts, stores them as embeddings in Qdrant, and uses CrewAI to orchestrate specialized agents that can search, analyze, and synthesize insights from meeting content.

For basic RAG patterns without agent orchestration, see [Self-Query Systems with LangChain](qdrant/examples/8.1-self-query-systems-with-langchain.md). For graph-enhanced retrieval approaches, see [Graph-Enhanced RAG with Neo4j](qdrant/examples/6.2-graph-enhanced-rag-with-neo4j.md).

## System Architecture

The system operates as a multi-agent workflow where specialized AI agents coordinate to process natural language queries about meeting content through vector search and analysis.

```
```

**Sources:** [agentic\_rag\_zoom\_crewai/vector/crew.py1-206](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L1-L206) [agentic\_rag\_zoom\_crewai/readme.md9-34](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L9-L34)

## Data Processing Pipeline

The system processes meeting data through a structured pipeline that converts raw meeting transcripts into searchable vector embeddings.

### Meeting Data Structure

The system expects meeting data in a specific JSON format with user information and recording arrays:

| Field                   | Type   | Description              |
| ----------------------- | ------ | ------------------------ |
| `userid`                | string | Unique user identifier   |
| `firstname`, `lastname` | string | User names               |
| `email`                 | string | User email address       |
| `recordings`            | array  | Array of meeting objects |

Each recording contains:

- `uuid` - Meeting identifier
- `topic` - Meeting subject
- `start_time` - ISO timestamp
- `duration` - Meeting length in minutes
- `vtt_content` - Timestamped transcript
- `summary` - AI-generated summary with structured details

**Sources:** [agentic\_rag\_zoom\_crewai/readme.md17-34](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L17-L34) [agentic\_rag\_zoom\_crewai/data/user\_1rydFrQocHdttmKsA0OhkV.txt1-64](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/data/user_1rydFrQocHdttmKsA0OhkV.txt#L1-L64)

### Vector Embedding Process

```
```

The `data_loader.py` script constructs text representations by concatenating meeting topic, VTT content, and summary data before generating embeddings.

**Sources:** [agentic\_rag\_zoom\_crewai/tutorial.md134-154](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/tutorial.md#L134-L154) [agentic\_rag\_zoom\_crewai/readme.md94-101](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L94-L101)

## Agent System Components

### Core Agents

The system employs two specialized agents that work in sequence:

```
```

The `researcher` agent handles information gathering and analysis, while the `synthesizer` agent creates structured responses from the research results.

**Sources:** [agentic\_rag\_zoom\_crewai/vector/crew.py143-159](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L143-L159) [agentic\_rag\_zoom\_crewai/vector/crew.py162-184](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L162-L184)

### Tool System

The agents utilize three specialized tools for different operations:

```
```

**Sources:** [agentic\_rag\_zoom\_crewai/vector/crew.py45-135](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L45-L135)

#### SearchMeetingsTool Implementation

The vector search tool performs semantic search against the meeting collection:

```
```

The tool returns structured results with meeting metadata including topic, start time, duration, and summary overview.

**Sources:** [agentic\_rag\_zoom\_crewai/vector/crew.py61-85](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L61-L85)

#### MeetingAnalysisTool Implementation

The analysis tool leverages Anthropic Claude for deep meeting analysis:

```
```

The tool provides structured analysis including key discussion points, decisions, patterns, and recommendations.

**Sources:** [agentic\_rag\_zoom\_crewai/vector/crew.py92-134](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L92-L134)

## User Interface Architecture

The Streamlit application provides an interactive chat interface with real-time processing feedback:

```
```

The interface maintains conversation history and provides configurable settings for search behavior and analysis depth.

**Sources:** [agentic\_rag\_zoom\_crewai/tutorial.md227-313](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/tutorial.md#L227-L313) [agentic\_rag\_zoom\_crewai/readme.md124-143](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/readme.md#L124-L143)

### Real-time Processing Feedback

The `ConsoleOutput` class provides buffered real-time updates during agent processing:

```
```

This enables users to see agent reasoning and tool execution in real-time.

**Sources:** [agentic\_rag\_zoom\_crewai/tutorial.md258-270](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/tutorial.md#L258-L270)

## Configuration and Environment

The system requires four environment variables for external service integration:

| Variable            | Service      | Purpose                 |
| ------------------- | ------------ | ----------------------- |
| `OPENAI_API_KEY`    | OpenAI       | Embedding generation    |
| `ANTHROPIC_API_KEY` | Anthropic    | Meeting analysis        |
| `QDRANT_URL`        | Qdrant Cloud | Vector database URL     |
| `QDRANT_API_KEY`    | Qdrant Cloud | Database authentication |

Environment variables are loaded from `.env.local` using the `dotenv` library.

**Sources:** [agentic\_rag\_zoom\_crewai/.env.example1-4](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/.env.example#L1-L4) [agentic\_rag\_zoom\_crewai/vector/crew.py15-17](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L15-L17)

## Execution Flow

The complete system execution follows this sequence:

```
```

The system maintains real-time feedback throughout this process, showing users the agent reasoning and tool execution steps.

**Sources:** [agentic\_rag\_zoom\_crewai/vector/crew.py136-194](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/vector/crew.py#L136-L194) [agentic\_rag\_zoom\_crewai/tutorial.md274-286](https://github.com/qdrant/examples/blob/b3c4b28f/agentic_rag_zoom_crewai/tutorial.md#L274-L286)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Meeting Analysis with Agentic RAG](#meeting-analysis-with-agentic-rag.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Architecture](#system-architecture.md)
- [Data Processing Pipeline](#data-processing-pipeline.md)
- [Meeting Data Structure](#meeting-data-structure.md)
- [Vector Embedding Process](#vector-embedding-process.md)
- [Agent System Components](#agent-system-components.md)
- [Core Agents](#core-agents.md)
- [Tool System](#tool-system.md)
- [SearchMeetingsTool Implementation](#searchmeetingstool-implementation.md)
- [MeetingAnalysisTool Implementation](#meetinganalysistool-implementation.md)
- [User Interface Architecture](#user-interface-architecture.md)
- [Real-time Processing Feedback](#real-time-processing-feedback.md)
- [Configuration and Environment](#configuration-and-environment.md)
- [Execution Flow](#execution-flow.md)
