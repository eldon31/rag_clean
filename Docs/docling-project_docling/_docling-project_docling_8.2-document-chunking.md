Document Chunking | docling-project/docling | DeepWiki

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

# Document Chunking

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

Document chunking is the process of breaking down large documents into smaller, semantically meaningful segments that can be efficiently processed by downstream systems. In Docling, chunking operates on `DoclingDocument` objects after conversion is complete, transforming the hierarchical document structure into manageable chunks suitable for retrieval-augmented generation (RAG), vector database indexing, and other AI/ML workflows.

This page covers:

- Chunking architecture and placement in the Docling workflow
- The `HierarchicalChunker` from `docling-core[chunking]`
- Hybrid chunking strategies that combine structural and text-based approaches
- Integration patterns with retrieval systems and vector databases

For information about document conversion and the `DoclingDocument` format, see [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md). For export formats that precede chunking, see [Export Formats](docling-project/docling/8.1-export-formats.md). For framework-specific integrations that consume chunks, see [Framework Integrations](docling-project/docling/8.3-framework-integrations.md).

Sources: [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47) [mkdocs.yml77-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L77-L103)

## Chunking in the Docling Workflow

Chunking is a post-conversion operation that transforms the unified `DoclingDocument` representation into smaller segments. The following diagram illustrates where chunking fits in the overall processing pipeline:

```
```

**Chunking Workflow Position**

The chunking layer operates after document conversion is complete and before downstream consumption. It accepts a `DoclingDocument` as input and produces a list of chunks, each containing:

- Text content
- Metadata (source location, document structure context)
- Optional embeddings (when integrated with embedding models)

Sources: [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47) Diagram 1 and 2 from high-level overview

## Chunking Dependencies

Docling's chunking functionality is provided by the `docling-core` library with the `chunking` extra:

```
```

This dependency includes:

- `HierarchicalChunker` - structure-aware chunking based on document hierarchy
- `HybridChunker` - combines hierarchical and text-based chunking
- Tokenizer integration for precise chunk size control
- Metadata preservation for provenance tracking

Sources: [pyproject.toml47](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L47-L47)

## Chunking Strategies

Docling supports multiple chunking strategies through the `docling-core` library. The primary strategies are:

### Document Structure-Based Chunking

| Strategy              | Description                                                       | Use Case                                               |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------------------------ |
| **Hierarchical**      | Chunks based on document structure (sections, paragraphs, tables) | Preserving document semantics, maintaining context     |
| **Hybrid**            | Combines hierarchical structure with text-based splitting         | Balancing structure preservation with size constraints |
| **Metadata-Enriched** | Includes provenance and structural metadata in each chunk         | Retrieval systems requiring context attribution        |

### Chunking Parameters

```
```

**Configuration Parameters**

- `max_tokens`: Maximum number of tokens per chunk (typical: 512, 1024, 2048)
- `overlap`: Number of overlapping tokens between adjacent chunks (typical: 50-200)
- `tokenizer`: Tokenization method (e.g., `tiktoken` for GPT models, `transformers` tokenizers)
- `merge_peers`: Whether to merge sibling elements in the document hierarchy

Sources: [mkdocs.yml102-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L102-L103)

## HierarchicalChunker Implementation

The `HierarchicalChunker` from `docling-core` is the primary chunking mechanism. It respects document structure while enforcing size constraints:

### Chunking Process Flow

```
```

**Hierarchical Chunking Algorithm**

1. **Traverse Document Tree**: Walk the `DoclingDocument` hierarchy depth-first
2. **Respect Boundaries**: Avoid splitting structural elements (tables, figures) when possible
3. **Size Enforcement**: Split text elements that exceed `max_tokens`
4. **Metadata Preservation**: Each chunk maintains links to its source location
5. **Overlap Generation**: Create overlapping tokens between chunks for context continuity

Sources: Examples in [mkdocs.yml102-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L102-L103)

## Hybrid Chunking

Hybrid chunking combines the benefits of structure-aware and text-based chunking strategies:

```
```

**Hybrid Chunking Workflow**

The hybrid approach uses the `HybridChunker` from `docling-core`, which:

1. **Primary Pass**: Chunks based on document structure (sections, headings, lists)
2. **Secondary Pass**: For oversized structural chunks, applies text-based splitting
3. **Optimization**: Merges small adjacent chunks when they fit within size limits
4. **Metadata Merging**: Combines provenance data from merged elements

### Typical Usage Pattern

Example chunking configuration for hybrid strategy:

```
```

Sources: [mkdocs.yml102-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L102-L103) [README.md35](https://github.com/docling-project/docling/blob/f7244a43/README.md#L35-L35)

## Integration with Retrieval Systems

Document chunks serve as the input to retrieval systems. The typical integration pattern:

```
```

**Retrieval-Augmented Generation (RAG) Pipeline**

The standard RAG integration pattern with Docling chunking:

1. **Document Conversion**: Use `DocumentConverter` to parse source documents
2. **Chunking**: Apply `HierarchicalChunker` or `HybridChunker` to create semantically meaningful segments
3. **Embedding**: Generate vector embeddings for each chunk using embedding models
4. **Indexing**: Store chunks with embeddings in a vector database
5. **Retrieval**: Query the vector store to find relevant chunks
6. **Generation**: Pass retrieved chunks as context to an LLM for response generation

Sources: [mkdocs.yml107-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L107-L127) [README.md37](https://github.com/docling-project/docling/blob/f7244a43/README.md#L37-L37)

## Framework Integration Examples

Docling's chunking integrates seamlessly with popular AI frameworks:

### Integration Table

| Framework      | Chunk Consumer                                        | Example Location                                                                                                             |
| -------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **LangChain**  | `Document` objects with `page_content` and `metadata` | [examples/rag\_langchain.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_langchain.ipynb)       |
| **LlamaIndex** | `Document` nodes in `VectorStoreIndex`                | [examples/rag\_llamaindex.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_llamaindex.ipynb)     |
| **Haystack**   | `Document` objects for `DocumentStore`                | [examples/rag\_haystack.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_haystack.ipynb)         |
| **Milvus**     | Text chunks with vector embeddings                    | [examples/rag\_milvus.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_milvus.ipynb)             |
| **Weaviate**   | Objects with `text` property                          | [examples/rag\_weaviate.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_weaviate.ipynb)         |
| **OpenSearch** | Documents with `text` and `metadata` fields           | [examples/rag\_opensearch.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_opensearch.ipynb)     |
| **Qdrant**     | Points with payload containing chunk text             | [examples/retrieval\_qdrant.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/retrieval_qdrant.ipynb) |

Sources: [mkdocs.yml107-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L107-L127)

## Chunking with Metadata Preservation

Each chunk produced by Docling's chunkers includes rich metadata for provenance tracking:

```
```

**Metadata Fields in Chunks**

Each chunk's metadata enables:

- **Source Attribution**: Trace back to exact location in original document
- **Context Reconstruction**: Recover document structure around the chunk
- **Visual Grounding**: Link to bounding boxes for visual highlighting
- **Hierarchical Navigation**: Understand chunk's position in document outline

### Example Chunk Metadata

A chunk from a PDF document might have metadata like:

```
```

Sources: Based on docling-core chunking API patterns, [mkdocs.yml75-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L75-L103)

## Usage Patterns

### Basic Chunking Example

```
```

### Advanced Chunking Configuration

```
```

### Integration with Vector Databases

Example pattern for indexing chunks in a vector database:

```
```

Sources: [mkdocs.yml102-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L102-L127)

## Serialization and Chunking

Docling supports serializing chunks for storage and downstream processing. The relationship between serialization and chunking:

```
```

**Chunking vs Serialization**

- **Serialization** ([Export Formats](docling-project/docling/8.1-export-formats.md)): Converts entire `DoclingDocument` to a specific format (JSON, Markdown, HTML)
- **Chunking**: Breaks document into smaller pieces with preserved metadata
- **Combined Usage**: Often serialize chunks individually for vector database storage

Sources: [mkdocs.yml100-103](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L100-L103) [README.md35](https://github.com/docling-project/docling/blob/f7244a43/README.md#L35-L35)

## Advanced Chunking Examples

For detailed examples demonstrating chunking in real-world scenarios, refer to:

| Example                    | Description                                  | Location                                                                                                                                                             |
| -------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hybrid Chunking**        | Combining structural and text-based chunking | [examples/hybrid\_chunking.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/hybrid_chunking.ipynb)                                           |
| **Advanced Chunking**      | Custom chunking strategies and serialization | [examples/advanced\_chunking\_and\_serialization.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/advanced_chunking_and_serialization.ipynb) |
| **RAG with LangChain**     | Using chunks for retrieval in LangChain      | [examples/rag\_langchain.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_langchain.ipynb)                                               |
| **RAG with LlamaIndex**    | Indexing chunks in LlamaIndex                | [examples/rag\_llamaindex.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_llamaindex.ipynb)                                             |
| **Milvus Integration**     | Storing chunks in Milvus vector database     | [examples/rag\_milvus.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_milvus.ipynb)                                                     |
| **OpenSearch Integration** | Indexing chunks in OpenSearch                | [examples/rag\_opensearch.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_opensearch.ipynb)                                             |

Sources: [mkdocs.yml100-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L100-L127)

## Best Practices

### Chunk Size Selection

- **Small chunks (256-512 tokens)**: Better precision, more retrieval overhead
- **Medium chunks (512-1024 tokens)**: Balanced approach for most use cases
- **Large chunks (1024-2048 tokens)**: Better context, may lose precision

### Overlap Configuration

- **No overlap (0 tokens)**: Fastest processing, risk of splitting concepts
- **Small overlap (50-100 tokens)**: Minimal redundancy, some context preservation
- **Medium overlap (100-200 tokens)**: Recommended for most scenarios
- **Large overlap (200+ tokens)**: Maximum context continuity, higher storage cost

### Structure Preservation

- Use `HierarchicalChunker` when document structure is important (research papers, technical docs)
- Use `HybridChunker` for mixed content (long reports with varying section sizes)
- Set `merge_peers=True` to combine related small elements (list items, short paragraphs)

### Metadata Utilization

- Always preserve chunk metadata for provenance tracking
- Use `headings` metadata for context-aware retrieval
- Leverage `bbox` data for visual grounding in UI applications
- Store `doc_items` paths for reconstructing document structure

Sources: Based on chunking examples in [mkdocs.yml100-127](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L100-L127)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Document Chunking](#document-chunking.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Chunking in the Docling Workflow](#chunking-in-the-docling-workflow.md)
- [Chunking Dependencies](#chunking-dependencies.md)
- [Chunking Strategies](#chunking-strategies.md)
- [Document Structure-Based Chunking](#document-structure-based-chunking.md)
- [Chunking Parameters](#chunking-parameters.md)
- [HierarchicalChunker Implementation](#hierarchicalchunker-implementation.md)
- [Chunking Process Flow](#chunking-process-flow.md)
- [Hybrid Chunking](#hybrid-chunking.md)
- [Typical Usage Pattern](#typical-usage-pattern.md)
- [Integration with Retrieval Systems](#integration-with-retrieval-systems.md)
- [Framework Integration Examples](#framework-integration-examples.md)
- [Integration Table](#integration-table.md)
- [Chunking with Metadata Preservation](#chunking-with-metadata-preservation.md)
- [Example Chunk Metadata](#example-chunk-metadata.md)
- [Usage Patterns](#usage-patterns.md)
- [Basic Chunking Example](#basic-chunking-example.md)
- [Advanced Chunking Configuration](#advanced-chunking-configuration.md)
- [Integration with Vector Databases](#integration-with-vector-databases.md)
- [Serialization and Chunking](#serialization-and-chunking.md)
- [Advanced Chunking Examples](#advanced-chunking-examples.md)
- [Best Practices](#best-practices.md)
- [Chunk Size Selection](#chunk-size-selection.md)
- [Overlap Configuration](#overlap-configuration.md)
- [Structure Preservation](#structure-preservation.md)
- [Metadata Utilization](#metadata-utilization.md)
