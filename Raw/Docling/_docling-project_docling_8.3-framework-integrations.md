Framework Integrations | docling-project/docling | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[docling-project/docling](https://github.com/docling-project/docling "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 12 October 2025 ([f7244a](https://github.com/docling-project/docling/commits/f7244a43))

- [Overview](docling-project/docling/1-overview.md)
- [Installation](docling-project/docling/1.1-installation.md)
- [Quick Start](docling-project/docling/1.2-quick-start.md)
- [Core Architecture](docling-project/docling/2-core-architecture.md)
- [Document Conversion Flow](docling-project/docling/2.1-document-conversion-flow.md)
- [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md)
- [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md)
- [Format Detection and Routing](docling-project/docling/2.4-format-detection-and-routing.md)
- [Document Backends](docling-project/docling/3-document-backends.md)
- [PDF Processing Backends](docling-project/docling/3.1-pdf-processing-backends.md)
- [Office Document Backends](docling-project/docling/3.2-office-document-backends.md)
- [Web and Markup Backends](docling-project/docling/3.3-web-and-markup-backends.md)
- [AI/ML Models](docling-project/docling/4-aiml-models.md)
- [OCR Models](docling-project/docling/4.1-ocr-models.md)
- [Layout and Table Structure Models](docling-project/docling/4.2-layout-and-table-structure-models.md)
- [Vision Language Models](docling-project/docling/4.3-vision-language-models.md)
- [Inline VLM Models](docling-project/docling/4.3.1-inline-vlm-models.md)
- [API-Based VLM Models](docling-project/docling/4.3.2-api-based-vlm-models.md)
- [Enrichment Models](docling-project/docling/4.4-enrichment-models.md)
- [Processing Pipelines](docling-project/docling/5-processing-pipelines.md)
- [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md)
- [Threaded PDF Pipeline](docling-project/docling/5.2-threaded-pdf-pipeline.md)
- [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md)
- [Extraction Pipeline](docling-project/docling/5.4-extraction-pipeline.md)
- [ASR Pipeline](docling-project/docling/5.5-asr-pipeline.md)
- [Base Pipeline Architecture](docling-project/docling/5.6-base-pipeline-architecture.md)
- [Command Line Interface](docling-project/docling/6-command-line-interface.md)
- [Document Conversion CLI](docling-project/docling/6.1-document-conversion-cli.md)
- [Model Management CLI](docling-project/docling/6.2-model-management-cli.md)
- [Python SDK](docling-project/docling/7-python-sdk.md)
- [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md)
- [DocumentExtractor API](docling-project/docling/7.2-documentextractor-api.md)
- [Usage Examples](docling-project/docling/7.3-usage-examples.md)
- [Output and Integration](docling-project/docling/8-output-and-integration.md)
- [Export Formats](docling-project/docling/8.1-export-formats.md)
- [Document Chunking](docling-project/docling/8.2-document-chunking.md)
- [Framework Integrations](docling-project/docling/8.3-framework-integrations.md)
- [Development and Testing](docling-project/docling/9-development-and-testing.md)
- [Testing Framework](docling-project/docling/9.1-testing-framework.md)
- [Ground Truth Data](docling-project/docling/9.2-ground-truth-data.md)
- [CI/CD and Development Workflow](docling-project/docling/9.3-cicd-and-development-workflow.md)
- [Deployment](docling-project/docling/10-deployment.md)
- [Docker Deployment](docling-project/docling/10.1-docker-deployment.md)
- [Model Artifacts Management](docling-project/docling/10.2-model-artifacts-management.md)

Menu

# Framework Integrations

Relevant source files

- [.github/SECURITY.md](https://github.com/docling-project/docling/blob/f7244a43/.github/SECURITY.md)
- [CHANGELOG.md](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md)
- [CITATION.cff](https://github.com/docling-project/docling/blob/f7244a43/CITATION.cff)
- [README.md](https://github.com/docling-project/docling/blob/f7244a43/README.md)
- [docs/examples/minimal\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py)
- [docs/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md)
- [docs/usage/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md)
- [docs/usage/mcp.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md)
- [docs/usage/vision\_models.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md)
- [mkdocs.yml](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml)
- [pyproject.toml](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml)
- [uv.lock](https://github.com/docling-project/docling/blob/f7244a43/uv.lock)

## Purpose and Scope

This page documents how Docling integrates with AI development frameworks, vector databases, data processing pipelines, and agentic systems. It covers the architectural patterns, export formats, and protocols that enable seamless integration with the broader GenAI ecosystem.

For information about export format options and serialization, see [Export Formats](docling-project/docling/8.1-export-formats.md). For chunking strategies used in retrieval pipelines, see [Document Chunking](docling-project/docling/8.2-document-chunking.md).

---

## Integration Architecture Overview

Docling's integration strategy is built on three foundational principles:

1. **Unified Representation**: The `DoclingDocument` class provides a consistent document model that all downstream systems consume
2. **Multiple Export Formats**: Support for Markdown, JSON, HTML, and DocTags enables compatibility with diverse framework requirements
3. **Standardized Protocols**: MCP (Model Context Protocol) support for agentic AI systems

```
```

**Diagram: Docling Integration Architecture**

Sources: [pyproject.toml1-280](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L280) [README.md109-113](https://github.com/docling-project/docling/blob/f7244a43/README.md#L109-L113) [mkdocs.yml128-155](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L128-L155)

---

## DoclingDocument as Integration Foundation

The `DoclingDocument` class serves as the universal interchange format for all integrations. It provides:

- **Hierarchical Structure**: Nested document elements with parent-child relationships
- **Content Layers**: Separation of body content from furniture elements (headers, footers, page numbers)
- **Rich Metadata**: Provenance information, bounding boxes, confidence scores
- **Multiple Serialization**: JSON, Markdown, HTML, and DocTags output

### Key Export Methods

| Method                 | Output Format | Primary Use Case                     | Framework Compatibility         |
| ---------------------- | ------------- | ------------------------------------ | ------------------------------- |
| `export_to_markdown()` | Markdown      | RAG pipelines, LLM consumption       | LangChain, LlamaIndex, Haystack |
| `export_to_json()`     | JSON          | Structured data processing           | All frameworks                  |
| `export_to_html()`     | HTML          | Web display, rich formatting         | Custom applications             |
| DocTags                | Custom XML    | VLM training, fine-grained structure | Research, model development     |

```
```

**Diagram: DoclingDocument Structure and Export Pathways**

Sources: [README.md26-27](https://github.com/docling-project/docling/blob/f7244a43/README.md#L26-L27) [docs/index.md26-27](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md#L26-L27) [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47)

---

## Model Context Protocol (MCP) Integration

The Model Context Protocol (MCP) is an emerging standard for connecting AI applications to external tools and data sources. Docling provides a dedicated MCP server that enables agentic AI systems to access document processing capabilities.

### MCP Server Architecture

```
```

**Diagram: MCP Server Integration Flow**

### Configuration Example

MCP clients connect to the Docling server through a configuration file specifying the command and arguments:

```
```

This configuration is used in:

- **Claude Desktop**: `claude_desktop_config.json`
- **LM Studio**: `mcp.json`
- **Custom clients**: Any MCP-compatible client

The MCP server exposes Docling's document conversion and extraction capabilities as tools that AI agents can invoke autonomously. This enables use cases such as:

- Document Q\&A with automatic parsing
- Multi-document synthesis workflows
- Automated data extraction from forms and tables
- Document-based reasoning chains

Sources: [docs/usage/mcp.md1-31](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md#L1-L31) [README.md41-42](https://github.com/docling-project/docling/blob/f7244a43/README.md#L41-L42)

---

## AI Framework Integrations

### LangChain Integration

LangChain integration leverages Docling's Markdown export and chunking capabilities for RAG (Retrieval-Augmented Generation) pipelines.

**Integration Pattern:**

1. Convert documents using `DocumentConverter`
2. Export to Markdown with `export_to_markdown()`
3. Apply chunking via `HybridChunker` from `docling-core`
4. Create LangChain `Document` objects
5. Index in vector store (Milvus, Qdrant, etc.)

```
```

**Diagram: LangChain RAG Pipeline with Docling**

**Key Dependencies:**

- `langchain-huggingface>=0.0.3` - Embedding models
- `langchain-milvus~=0.1` - Milvus vector store
- `langchain-text-splitters~=0.2` - Text splitting utilities

Sources: [pyproject.toml144-146](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L144-L146) [mkdocs.yml134](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L134-L134)

---

### LlamaIndex Integration

LlamaIndex integration follows a similar pattern but uses LlamaIndex-specific abstractions for document loading and indexing.

**Integration Components:**

| Component    | Purpose            | Docling Interface                 |
| ------------ | ------------------ | --------------------------------- |
| Reader       | Document ingestion | `DocumentConverter.convert()`     |
| Node Parser  | Chunking           | `HybridChunker` from docling-core |
| Vector Store | Embedding storage  | Weaviate, MongoDB, etc.           |
| Query Engine | Retrieval          | Standard LlamaIndex query         |

```
```

**Diagram: LlamaIndex Integration Architecture**

Sources: [mkdocs.yml136](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L136-L136) [mkdocs.yml109](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L109-L109)

---

### Haystack Integration

Haystack integration uses Docling as a document converter within Haystack pipelines, enabling preprocessing before RAG or search operations.

**Typical Haystack Pipeline:**

1. `DocumentConverter` as preprocessing step
2. Export to structured format
3. Pass to Haystack `Pipeline`
4. Route to retriever or generator components

**Supported Vector Stores:**

- OpenSearch
- Azure Cognitive Search

Sources: [mkdocs.yml133](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L133-L133) [mkdocs.yml123](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L123-L123)

---

### Agentic AI Frameworks

Multiple agentic frameworks integrate Docling to provide document understanding capabilities to autonomous agents:

| Framework           | Integration Type | Key Feature                    |
| ------------------- | ---------------- | ------------------------------ |
| Crew AI             | Tool             | Document parsing as crew task  |
| Bee Agent Framework | Tool             | Multi-agent document workflows |
| Langflow            | Node             | Visual pipeline integration    |
| txtai               | Pipeline         | Embedded document processing   |

```
```

**Diagram: Agentic Framework Integration Patterns**

Sources: [mkdocs.yml131-137](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L131-L137) [README.md29](https://github.com/docling-project/docling/blob/f7244a43/README.md#L29-L29)

---

## Vector Database Integrations

Docling's chunking and embedding-friendly output formats enable integration with major vector databases for semantic search and RAG applications.

### Supported Vector Databases

| Vector DB    | Primary Framework | Integration Path                |
| ------------ | ----------------- | ------------------------------- |
| Milvus       | LangChain         | `langchain-milvus` connector    |
| Qdrant       | LangChain, Direct | Python client, LangChain loader |
| Weaviate     | LlamaIndex        | Weaviate vector store           |
| MongoDB      | LlamaIndex        | MongoDB Atlas vector search     |
| OpenSearch   | Haystack          | OpenSearch document store       |
| Azure Search | Haystack          | Azure Cognitive Search          |

**General Integration Flow:**

1. Process document with `DocumentConverter`
2. Extract text via `export_to_markdown()` or iterate over elements
3. Apply `HybridChunker` for semantic chunking
4. Generate embeddings (typically with sentence-transformers or OpenAI)
5. Store in vector database with metadata

```
```

**Diagram: Vector Database Integration Flow**

Sources: [mkdocs.yml122-125](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L122-L125) [pyproject.toml145](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L145-L145)

---

## Data Processing Framework Integrations

Beyond real-time RAG, Docling integrates with data processing frameworks for batch document processing, training data preparation, and enterprise workflows.

### Data Prep Kit (DPK)

Data Prep Kit is a framework for large-scale data preparation pipelines. Docling integration enables:

- **Batch Processing**: Convert thousands of documents in parallel
- **Transform Pipelines**: Clean, chunk, and tokenize documents
- **Training Data Generation**: Prepare datasets for model fine-tuning

**Example Pipeline:**

```
Ingest → Docling Convert → DPK Transform → Chunk → Tokenize → Store
```

Sources: [mkdocs.yml140](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L140-L140) [mkdocs.yml119](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L119-L119)

---

### InstructLab Integration

InstructLab uses Docling for preparing training data from documents in knowledge base construction workflows.

**Integration Points:**

- Document parsing for instruction-tuning datasets
- Structured extraction of Q\&A pairs
- Metadata preservation for provenance tracking

Sources: [mkdocs.yml141](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L141-L141)

---

### Enterprise & Production Integrations

| Integration | Category            | Purpose                                    |
| ----------- | ------------------- | ------------------------------------------ |
| Apify Actor | Cloud Platform      | Serverless document processing             |
| Prodigy     | Annotation          | Active learning for document understanding |
| spaCy       | NLP Pipeline        | Entity extraction from parsed documents    |
| RHEL AI     | Enterprise Platform | On-premises AI deployments                 |
| NVIDIA      | GPU Acceleration    | Optimized VLM inference                    |
| Quarkus     | Java Framework      | JVM-based microservices                    |

```
```

**Diagram: Enterprise Integration Landscape**

Sources: [mkdocs.yml139-155](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L139-L155) [README.md109-113](https://github.com/docling-project/docling/blob/f7244a43/README.md#L109-L113)

---

## Integration Development Patterns

### Common Integration Pattern

Most integrations follow this general structure:

1. **Initialization**: Create `DocumentConverter` with appropriate options
2. **Conversion**: Call `convert()` or `convert_all()` for batch processing
3. **Export**: Use `export_to_markdown()`, `export_to_json()`, or iterate over elements
4. **Transform**: Apply framework-specific transformations (chunking, embedding, etc.)
5. **Downstream Processing**: Pass to framework-specific components

### Code Structure Example

```
```

### Export Format Selection

| Use Case              | Recommended Format | Rationale                       |
| --------------------- | ------------------ | ------------------------------- |
| RAG with LLMs         | Markdown           | Readable, preserves structure   |
| Structured extraction | JSON               | Programmatic access to elements |
| Web display           | HTML               | Styled rendering                |
| Model training        | DocTags            | Fine-grained structure labels   |
| Search indexing       | Markdown or JSON   | Depends on search engine        |

Sources: [README.md69-78](https://github.com/docling-project/docling/blob/f7244a43/README.md#L69-L78) [docs/usage/index.md1-46](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L1-L46)

---

## Environment Variables and Configuration

Several environment variables control integration behavior:

| Variable              | Purpose                                | Default        |
| --------------------- | -------------------------------------- | -------------- |
| `DOCLING_DEVICE`      | Accelerator device (CPU/CUDA/MPS/AUTO) | AUTO           |
| `OMP_NUM_THREADS`     | Thread count for CPU models            | System default |
| `DOCLING_NUM_THREADS` | Alternative thread control             | System default |

These settings affect model inference performance in integration scenarios, particularly for VLM-based pipelines and OCR operations.

Sources: [pyproject.toml1-280](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L280)

---

## Installation for Integrations

To use Docling with specific integrations, install with appropriate extras:

| Extra         | Frameworks Enabled                      | Install Command                  |
| ------------- | --------------------------------------- | -------------------------------- |
| `[vlm]`       | Vision models (Transformers, MLX, vLLM) | `pip install docling[vlm]`       |
| `[easyocr]`   | EasyOCR engine                          | `pip install docling[easyocr]`   |
| `[tesserocr]` | Tesseract OCR                           | `pip install docling[tesserocr]` |
| `[asr]`       | Audio transcription (Whisper)           | `pip install docling[asr]`       |

**Example Dependencies in `pyproject.toml`:**

- VLM support: `transformers>=4.46.0`, `accelerate>=1.2.1`, `mlx-vlm>=0.3.0`, `vllm>=0.10.0`
- Chunking: `docling-core[chunking]>=2.48.2`

Sources: [pyproject.toml91-111](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L91-L111) [README.md56-65](https://github.com/docling-project/docling/blob/f7244a43/README.md#L56-L65)

---

## Summary

Docling's integration ecosystem is built on:

1. **DoclingDocument**: Universal document representation
2. **Flexible Export**: Multiple formats for different use cases
3. **MCP Protocol**: Standard interface for agentic AI
4. **Framework Adapters**: Native support for LangChain, LlamaIndex, Haystack
5. **Chunking API**: Semantic document segmentation via `docling-core`
6. **Batch Processing**: Efficient handling of document collections

The integration architecture prioritizes **modularity** (components can be mixed and matched), **extensibility** (new integrations follow established patterns), and **interoperability** (standard formats and protocols).

For specific integration examples, see the [Examples](docling-project/docling/7.3-usage-examples.md) section. For details on export format options, see [Export Formats](docling-project/docling/8.1-export-formats.md). For chunking strategies, see [Document Chunking](docling-project/docling/8.2-document-chunking.md).

Sources: [README.md1-161](https://github.com/docling-project/docling/blob/f7244a43/README.md#L1-L161) [docs/index.md1-70](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md#L1-L70) [mkdocs.yml128-162](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L128-L162) [pyproject.toml1-280](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L280)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Framework Integrations](#framework-integrations.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Integration Architecture Overview](#integration-architecture-overview.md)
- [DoclingDocument as Integration Foundation](#doclingdocument-as-integration-foundation.md)
- [Key Export Methods](#key-export-methods.md)
- [Model Context Protocol (MCP) Integration](#model-context-protocol-mcp-integration.md)
- [MCP Server Architecture](#mcp-server-architecture.md)
- [Configuration Example](#configuration-example.md)
- [AI Framework Integrations](#ai-framework-integrations.md)
- [LangChain Integration](#langchain-integration.md)
- [LlamaIndex Integration](#llamaindex-integration.md)
- [Haystack Integration](#haystack-integration.md)
- [Agentic AI Frameworks](#agentic-ai-frameworks.md)
- [Vector Database Integrations](#vector-database-integrations.md)
- [Supported Vector Databases](#supported-vector-databases.md)
- [Data Processing Framework Integrations](#data-processing-framework-integrations.md)
- [Data Prep Kit (DPK)](#data-prep-kit-dpk.md)
- [InstructLab Integration](#instructlab-integration.md)
- [Enterprise & Production Integrations](#enterprise-production-integrations.md)
- [Integration Development Patterns](#integration-development-patterns.md)
- [Common Integration Pattern](#common-integration-pattern.md)
- [Code Structure Example](#code-structure-example.md)
- [Export Format Selection](#export-format-selection.md)
- [Environment Variables and Configuration](#environment-variables-and-configuration.md)
- [Installation for Integrations](#installation-for-integrations.md)
- [Summary](#summary.md)
