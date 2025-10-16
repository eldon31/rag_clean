Output and Integration | docling-project/docling | DeepWiki

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

# Output and Integration

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

This document provides an overview of Docling's output capabilities and integration ecosystem. After documents are processed through pipelines and assembled into a `DoclingDocument` (see [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md)), they can be exported to multiple formats and integrated with downstream tools. This page covers:

1. **Export formats**: Markdown, JSON, HTML, and DOCTAGS serialization from `DoclingDocument`
2. **Document chunking**: Breaking documents into smaller segments for retrieval systems
3. **Framework integrations**: Connecting with LangChain, LlamaIndex, Haystack, vector databases, and AI agents via MCP

For detailed information on specific export format options and methods, see [Export Formats](docling-project/docling/8.1-export-formats.md). For chunking strategies and configuration, see [Document Chunking](docling-project/docling/8.2-document-chunking.md). For framework-specific integration patterns, see [Framework Integrations](docling-project/docling/8.3-framework-integrations.md).

Sources: [pyproject.toml1-280](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L280) [README.md1-161](https://github.com/docling-project/docling/blob/f7244a43/README.md#L1-L161) [mkdocs.yml54-162](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L54-L162)

---

## Output Architecture

The output subsystem is organized around the `DoclingDocument` as the central unified representation. All processed documents, regardless of their input format or processing pipeline, converge to this common structure before being exported or integrated with external systems.

### Export Flow Diagram

```
```

**Description**: This diagram illustrates how all processing pipelines converge on `DoclingDocument`, which serves as the single source for exports, chunking, and framework integrations. The export methods are direct serialization functions on the document object, while chunking produces `DocChunk` objects that can be fed into AI frameworks. Framework integrations can consume either the full `DoclingDocument` or chunked segments depending on the use case.

Sources: [README.md34-43](https://github.com/docling-project/docling/blob/f7244a43/README.md#L34-L43) [mkdocs.yml100-128](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L100-L128) [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47)

---

## Export Formats Overview

Docling provides four primary export formats, each accessed through methods on the `DoclingDocument` instance:

| Format       | Method                 | Primary Use Case                            | Output Type |
| ------------ | ---------------------- | ------------------------------------------- | ----------- |
| **Markdown** | `export_to_markdown()` | Human-readable text, LLM input              | `str`       |
| **JSON**     | `export_to_json()`     | Lossless serialization, programmatic access | `str`       |
| **HTML**     | `export_to_html()`     | Web display, visual rendering               | `str`       |
| **DOCTAGS**  | `export_to_doctags()`  | Structured markup, VLM training             | `str`       |

### Basic Export Example

```
```

Each export method supports format-specific options for controlling output behavior. For example, `export_to_markdown()` supports `image_mode` to control embedded image handling, and `export_to_json()` supports `indent` for pretty-printing.

**DOCTAGS Format**: A specialized structured markup format designed for vision-language model training and structured document representation. DOCTAGS uses XML-like tags to encode document structure hierarchically (e.g., `<document>`, `<page>`, `<section>`, `<table>`). This format is the preferred output for VLM pipelines that generate structured representations directly.

Sources: [README.md35](https://github.com/docling-project/docling/blob/f7244a43/README.md#L35-L35) [docs/index.md27](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md#L27-L27) [docs/usage/index.md10-20](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L10-L20)

---

## Document Chunking Overview

Chunking breaks `DoclingDocument` instances into smaller `DocChunk` segments suitable for retrieval-augmented generation (RAG) systems and vector databases. Docling leverages the `docling-core` library's `HybridChunker`, which implements hierarchical and hybrid chunking strategies.

### Chunking Workflow

```
```

**Description**: The chunking process transforms a `DoclingDocument` into a list of `DocChunk` objects. Each chunk contains the text content, metadata about the source document items (paragraphs, tables, etc.), and hierarchical path information (headings leading to the chunk). This metadata enables context-aware retrieval.

### Chunking Strategies

1. **Hierarchical Chunking**: Respects document structure (sections, subsections) and preserves heading context
2. **Hybrid Chunking**: Combines hierarchical structure with token/character limits to ensure chunks fit within model context windows
3. **Token-Based Splitting**: Uses tokenizers to enforce maximum chunk sizes while respecting document boundaries

The chunker configuration allows control over:

- Maximum chunk size (tokens or characters)
- Overlap between consecutive chunks
- Heading level depth for context preservation
- Tokenizer selection (for transformer models)

Sources: [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47) [mkdocs.yml100-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L100-L103)

---

## Framework Integration Architecture

Docling provides native integrations with popular AI development frameworks, enabling seamless incorporation into RAG pipelines, agentic workflows, and document processing applications.

### Integration Landscape Diagram

```
```

**Description**: Docling integrates with the AI ecosystem at multiple levels. Document loaders/readers provide framework-specific adapters for LangChain, LlamaIndex, and Haystack. These frameworks then connect to vector databases for retrieval. Separately, agentic frameworks like MCP, CrewAI, and Bee Agent consume `DoclingDocument` directly for agent-based workflows.

Sources: [mkdocs.yml130-155](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L130-L155) [README.md109-113](https://github.com/docling-project/docling/blob/f7244a43/README.md#L109-L113)

---

## Integration Patterns

### Pattern 1: Direct Framework Integration

Frameworks like LangChain and LlamaIndex provide native loaders/readers that accept `DoclingDocument` objects:

```
```

These loaders handle the conversion from `DoclingDocument` (or `DocChunk`) to framework-native document representations.

### Pattern 2: MCP Server for Agents

The Model Context Protocol (MCP) integration enables any MCP-compatible agent to access Docling's document processing capabilities as a service:

```
```

This configuration (placed in `claude_desktop_config.json` or `mcp.json` for LM Studio) exposes Docling as an MCP tool that agents can invoke for document conversion tasks.

### Pattern 3: Vector Database Ingestion

Chunked documents can be embedded and stored in vector databases for semantic search:

```
```

Sources: [docs/usage/mcp.md1-31](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md#L1-L31) [mkdocs.yml106-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L106-L127) [README.md37-42](https://github.com/docling-project/docling/blob/f7244a43/README.md#L37-L42)

---

## Export Method Reference

All export methods are instance methods on the `DoclingDocument` class. They serialize the unified document representation into format-specific string outputs:

```
```

**Description**: The `DoclingDocument` Pydantic model provides four export methods, each with format-specific options. Common options include `image_mode` for controlling image handling (placeholders, embedded data, or references), `strict_text` for enforcing plain text output, and `indent` for JSON pretty-printing.

### Export Method Signatures

```
```

These methods are implemented in the `docling-core` library, which `DoclingDocument` inherits from. The actual method implementations handle traversal of the document's hierarchical structure and serialization to each format.

Sources: [docs/usage/index.md10-20](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L10-L20) [README.md77](https://github.com/docling-project/docling/blob/f7244a43/README.md#L77-L77)

---

## Chunking Configuration

The chunking subsystem uses `HybridChunker` from `docling-core`, configurable through initialization parameters:

| Parameter                   | Type   | Default        | Description                       |
| --------------------------- | ------ | -------------- | --------------------------------- |
| `max_tokens`                | `int`  | 512            | Maximum tokens per chunk          |
| `tokenizer`                 | `str`  | "cl100k\_base" | Tokenizer for counting (tiktoken) |
| `include_heading_hierarchy` | `bool` | `True`         | Add heading context to chunks     |
| `overlap`                   | `int`  | 0              | Token overlap between chunks      |

### Chunking Method Flow

```
```

**Description**: The `HybridChunker.chunk()` method traverses the `DoclingDocument.body` items (paragraphs, tables, lists, etc.) and segments them into chunks respecting token limits. Each chunk is enriched with metadata including the hierarchical path (sequence of headings leading to the chunk) and references to source document items.

Sources: [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47) [mkdocs.yml100-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L100-L103)

---

## Integration Dependencies

Framework integrations are provided through optional dependency groups and separate integration packages:

### Core Dependencies

```
```

### Optional Integration Dependencies

```
```

### Framework Integration Packages

The integrations are maintained as separate packages:

- **LangChain**: `langchain-docling` package provides `DoclingLoader` and `DoclingPDFLoader`
- **LlamaIndex**: `llama-index-readers-docling` provides `DoclingReader`
- **Haystack**: `haystack-docling` provides `DoclingConverter`
- **MCP**: `docling-mcp` provides the MCP server implementation

This separation allows framework integrations to evolve independently from Docling core.

Sources: [pyproject.toml45-148](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L45-L148) [mkdocs.yml130-155](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L130-L155)

---

## Use Case: RAG Pipeline

A typical RAG pipeline using Docling follows this pattern:

```
```

**Description**: The complete RAG workflow starts with document conversion to `DoclingDocument`, followed by chunking into `DocChunk` objects. Chunks are embedded and stored in a vector database. At query time, relevant chunks are retrieved via similarity search and provided as context to an LLM for answer generation.

### Code Example Structure

```
```

Sources: [mkdocs.yml106-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L106-L127) [pyproject.toml144-148](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L144-L148)

---

## MCP Server Architecture

The MCP (Model Context Protocol) server provides a standardized interface for AI agents to access Docling's document conversion capabilities:

```
```

**Description**: The MCP server (`docling-mcp-server`) runs as a separate process and communicates with MCP clients via JSON-RPC over standard input/output. Clients (like Claude Desktop or LM Studio) can invoke Docling document conversion as a tool, passing document paths or URLs and receiving structured `DoclingDocument` representations in response.

### MCP Configuration Example

```
```

This configuration launches the MCP server using `uvx` (the uv package runner), which handles dependency installation and execution. The server then registers itself with the MCP client, making Docling tools available to the agent.

Sources: [docs/usage/mcp.md1-31](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md#L1-L31) [README.md41](https://github.com/docling-project/docling/blob/f7244a43/README.md#L41-L41)

---

## Export Format Comparison

Different export formats serve different downstream use cases:

| Format       | Structure Preservation       | Human Readable      | Lossless                | Primary Consumers          |
| ------------ | ---------------------------- | ------------------- | ----------------------- | -------------------------- |
| **Markdown** | ⭐⭐⭐ Heading hierarchy, lists | ⭐⭐⭐ Highly readable | ❌ No (styling lost)     | LLMs, humans, static sites |
| **JSON**     | ⭐⭐⭐ Full provenance          | ⭐ Programmatic      | ✅ Yes (complete)        | Applications, archival     |
| **HTML**     | ⭐⭐ Visual structure          | ⭐⭐ Web rendering    | ❌ No (formatting focus) | Web browsers, displays     |
| **DOCTAGS**  | ⭐⭐⭐ Semantic tags            | ⭐⭐ Structured text  | ⭐⭐ Partial              | VLMs, structured ML        |

### Format Selection Guide

**Use Markdown when:**

- Providing context to language models
- Creating human-readable documentation
- Generating static websites or wikis

**Use JSON when:**

- Preserving complete document structure for later processing
- Building document databases or archives
- Implementing document version control

**Use HTML when:**

- Rendering documents in web applications
- Creating interactive document viewers
- Generating print-ready outputs

**Use DOCTAGS when:**

- Training or fine-tuning vision-language models
- Creating structured datasets for ML
- Preserving semantic document structure with minimal tokens

Sources: [README.md35](https://github.com/docling-project/docling/blob/f7244a43/README.md#L35-L35) [docs/index.md27](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md#L27-L27)

---

## Summary

Docling's output and integration capabilities center around the `DoclingDocument` unified representation:

1. **Export**: Four serialization formats (`export_to_markdown()`, `export_to_json()`, `export_to_html()`, `export_to_doctags()`) provide format-specific outputs for different use cases

2. **Chunking**: The `HybridChunker` from `docling-core` segments documents into `DocChunk` objects with preserved hierarchical context for RAG systems

3. **Integration**: Native support for LangChain, LlamaIndex, Haystack via dedicated loader packages, plus MCP server for agent frameworks

All export and integration paths preserve the document's hierarchical structure and provenance metadata, enabling downstream systems to leverage Docling's advanced document understanding capabilities.

Sources: [README.md28-43](https://github.com/docling-project/docling/blob/f7244a43/README.md#L28-L43) [pyproject.toml45-148](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L45-L148) [mkdocs.yml54-162](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L54-L162)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Output and Integration](#output-and-integration.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Output Architecture](#output-architecture.md)
- [Export Flow Diagram](#export-flow-diagram.md)
- [Export Formats Overview](#export-formats-overview.md)
- [Basic Export Example](#basic-export-example.md)
- [Document Chunking Overview](#document-chunking-overview.md)
- [Chunking Workflow](#chunking-workflow.md)
- [Chunking Strategies](#chunking-strategies.md)
- [Framework Integration Architecture](#framework-integration-architecture.md)
- [Integration Landscape Diagram](#integration-landscape-diagram.md)
- [Integration Patterns](#integration-patterns.md)
- [Pattern 1: Direct Framework Integration](#pattern-1-direct-framework-integration.md)
- [Pattern 2: MCP Server for Agents](#pattern-2-mcp-server-for-agents.md)
- [Pattern 3: Vector Database Ingestion](#pattern-3-vector-database-ingestion.md)
- [Export Method Reference](#export-method-reference.md)
- [Export Method Signatures](#export-method-signatures.md)
- [Chunking Configuration](#chunking-configuration.md)
- [Chunking Method Flow](#chunking-method-flow.md)
- [Integration Dependencies](#integration-dependencies.md)
- [Core Dependencies](#core-dependencies.md)
- [Optional Integration Dependencies](#optional-integration-dependencies.md)
- [Framework Integration Packages](#framework-integration-packages.md)
- [Use Case: RAG Pipeline](#use-case-rag-pipeline.md)
- [Code Example Structure](#code-example-structure.md)
- [MCP Server Architecture](#mcp-server-architecture.md)
- [MCP Configuration Example](#mcp-configuration-example.md)
- [Export Format Comparison](#export-format-comparison.md)
- [Format Selection Guide](#format-selection-guide.md)
- [Summary](#summary.md)
