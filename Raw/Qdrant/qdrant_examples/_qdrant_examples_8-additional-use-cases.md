Additional Use Cases | qdrant/examples | DeepWiki

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

# Additional Use Cases

Relevant source files

- [llama\_index\_recency/.gitignore](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/.gitignore)
- [llama\_index\_recency/images/RankFocus.png](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/images/RankFocus.png)
- [llama\_index\_recency/images/RerankFocus.png](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/images/RerankFocus.png)
- [llama\_index\_recency/images/SetupFocus.png](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/images/SetupFocus.png)
- [llama\_index\_recency/pyproject.toml](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/pyproject.toml)
- [self-query/self-query.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb)
- [self-query/winemag-data-130k-v2.csv](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/winemag-data-130k-v2.csv)

This section covers specialized applications and advanced query patterns that extend beyond the core Qdrant functionality. These use cases demonstrate sophisticated query translation capabilities and development best practices for building production-ready vector search applications.

For foundational Qdrant concepts and basic operations, see [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md). For comprehensive text processing applications, see [Text Data Applications](qdrant/examples/3-text-data-applications.md). For advanced RAG implementations using multiple frameworks, see [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md).

## Self-Query Systems with LangChain

Self-query systems enable natural language queries to be automatically translated into structured vector searches with metadata filters. This approach bridges the gap between user intent expressed in natural language and the precise filtering capabilities of vector databases.

### Architecture Overview

The self-query pattern implements a translation layer that converts natural language queries into structured search operations. The system parses user intent to extract both semantic search terms and metadata constraints.

```
```

Sources: [self-query/self-query.ipynb392-455](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L392-L455)

### Data Structure and Ingestion

The wine reviews dataset demonstrates structured metadata alongside vector content. Each document contains both textual descriptions for semantic search and categorical/numerical attributes for filtering.

```
```

Sources: [self-query/self-query.ipynb237-295](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L237-L295)

### LangChain Integration Components

The integration leverages several LangChain components to create a seamless natural language to structured query translation pipeline.

| Component                     | Type        | Purpose                                           |
| ----------------------------- | ----------- | ------------------------------------------------- |
| `SelfQueryRetriever`          | Retriever   | Orchestrates query translation and execution      |
| `ChatOpenAI`                  | LLM         | Translates natural language to structured queries |
| `AttributeInfo`               | Schema      | Defines metadata field types and descriptions     |
| `QdrantVectorStore`           | VectorStore | Provides Qdrant integration for LangChain         |
| `HuggingFaceEmbeddings`       | Embeddings  | Generates vectors for semantic search             |
| `StructuredQueryOutputParser` | Parser      | Validates and parses LLM output                   |

Sources: [self-query/self-query.ipynb397-455](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L397-L455)

### Query Translation Process

The system transforms natural language into structured filter expressions using a standardized syntax. The LLM receives structured prompts with examples and schema definitions to ensure consistent output format.

```
```

Sources: [self-query/self-query.ipynb525-627](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L525-L627)

### Metadata Schema Definition

The `AttributeInfo` schema provides the LLM with context about available metadata fields, their types, and semantic meanings. This enables accurate query translation.

```
```

Sources: [self-query/self-query.ipynb424-445](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L424-L445)

### Filter Expression Syntax

The system uses a standardized filter syntax that supports logical operations and comparisons. Complex queries can combine multiple conditions using `and`, `or`, and `not` operators.

| Operator                 | Purpose               | Example                                                        |
| ------------------------ | --------------------- | -------------------------------------------------------------- |
| `eq(field, value)`       | Equality              | `eq("country", "US")`                                          |
| `gt(field, value)`       | Greater than          | `gt("points", 90)`                                             |
| `gte(field, value)`      | Greater than or equal | `gte("price", 15)`                                             |
| `lt(field, value)`       | Less than             | `lt("price", 100)`                                             |
| `lte(field, value)`      | Less than or equal    | `lte("price", 30)`                                             |
| `and(expr1, expr2, ...)` | Logical AND           | `and(eq("country", "US"), gt("points", 90))`                   |
| `or(expr1, expr2, ...)`  | Logical OR            | `or(eq("variety", "Pinot Noir"), eq("variety", "Chardonnay"))` |

Sources: [self-query/self-query.ipynb534-596](https://github.com/qdrant/examples/blob/b3c4b28f/self-query/self-query.ipynb#L534-L596)

## Development Environment Setup

Development environments for Qdrant applications require specific tooling configurations to ensure code quality, dependency management, and consistent development practices across team members.

### Project Configuration Structure

The development setup uses modern Python tooling for code formatting, linting, and dependency management. The configuration emphasizes consistency and maintainability.

```
```

Sources: [llama\_index\_recency/pyproject.toml1-6](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/pyproject.toml#L1-L6)

### Tool Configuration

The `pyproject.toml` configuration standardizes code formatting and linting rules across the development environment.

```
```

This configuration ensures:

- Consistent line length limits for readability
- Uniform code formatting across team members
- Automated style enforcement in development workflows

Sources: [llama\_index\_recency/pyproject.toml1-6](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/pyproject.toml#L1-L6)

### Development Workflow Integration

The tooling configuration supports integration with various development environments and CI/CD pipelines. The standardized line length of 110 characters balances readability with modern screen resolutions.

| Tool             | Purpose            | Configuration               |
| ---------------- | ------------------ | --------------------------- |
| `black`          | Code formatting    | Line length: 110 characters |
| `ruff`           | Fast Python linter | Line length: 110 characters |
| `pyproject.toml` | Centralized config | Tool-specific sections      |

### Best Practices

Development environments should include:

- Pre-commit hooks for automatic formatting
- IDE integration for real-time linting
- Consistent dependency versions across environments
- Documentation generation from code comments
- Testing frameworks for vector search validation

Sources: [llama\_index\_recency/pyproject.toml1-6](https://github.com/qdrant/examples/blob/b3c4b28f/llama_index_recency/pyproject.toml#L1-L6)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Additional Use Cases](#additional-use-cases.md)
- [Self-Query Systems with LangChain](#self-query-systems-with-langchain.md)
- [Architecture Overview](#architecture-overview.md)
- [Data Structure and Ingestion](#data-structure-and-ingestion.md)
- [LangChain Integration Components](#langchain-integration-components.md)
- [Query Translation Process](#query-translation-process.md)
- [Metadata Schema Definition](#metadata-schema-definition.md)
- [Filter Expression Syntax](#filter-expression-syntax.md)
- [Development Environment Setup](#development-environment-setup.md)
- [Project Configuration Structure](#project-configuration-structure.md)
- [Tool Configuration](#tool-configuration.md)
- [Development Workflow Integration](#development-workflow-integration.md)
- [Best Practices](#best-practices.md)
