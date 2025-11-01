Python SDK | docling-project/docling | DeepWiki

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

# Python SDK

Relevant source files

- [README.md](https://github.com/docling-project/docling/blob/f7244a43/README.md)
- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [docs/examples/minimal\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py)
- [docs/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md)
- [docs/usage/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md)
- [docs/usage/mcp.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md)
- [docs/usage/vision\_models.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md)
- [mkdocs.yml](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml)

The Python SDK provides programmatic interfaces for document processing through Docling's document AI capabilities. The SDK exposes two primary classes for different use cases:

- **`DocumentConverter`**: Converts documents to the unified `DoclingDocument` format with comprehensive structure and content extraction
- **`DocumentExtractor`**: Performs structured data extraction from documents using schema-based templates

This page provides an overview of both APIs and common integration patterns. For detailed documentation, see:

- [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md) - Full conversion API reference
- [DocumentExtractor API](docling-project/docling/7.2-documentextractor-api.md) - Structured extraction API reference
- [Usage Examples](docling-project/docling/7.3-usage-examples.md) - Code examples and integration patterns

For command-line usage, see [Command Line Interface](docling-project/docling/6-command-line-interface.md).

## DocumentConverter Overview

The `DocumentConverter` class is the primary interface for converting documents into the unified `DoclingDocument` format. It handles format detection, backend initialization, and pipeline orchestration automatically.

**Basic Usage:**

```
```

**Key Capabilities:**

```
```

**Core Methods:**

| Method                            | Purpose                                           | Returns                      |
| --------------------------------- | ------------------------------------------------- | ---------------------------- |
| `convert(source)`                 | Convert single document from path, URL, or stream | `ConversionResult`           |
| `convert_all(sources)`            | Convert multiple documents with streaming results | `Iterator[ConversionResult]` |
| `convert_string(content, format)` | Convert in-memory string content (HTML, Markdown) | `ConversionResult`           |
| `initialize_pipeline(format)`     | Pre-load pipeline for specified format            | None                         |

The `ConversionResult` object contains:

- `document`: The converted `DoclingDocument`
- `status`: Success/failure status (`ConversionStatus`)
- `errors`: List of errors if any occurred (`List[ErrorItem]`)
- `pages`: Raw page-level data (`List[Page]`)
- `timings`: Performance profiling data

See [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md) for detailed documentation of configuration options, error handling, and advanced usage patterns.

Sources: [docling/document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L433)

## DocumentExtractor Overview

The `DocumentExtractor` class provides structured data extraction from documents using schema-based templates. It uses vision-language models (VLMs) to extract specific fields according to user-defined schemas.

**Basic Usage:**

```
```

**Template Types:**

The extractor supports three template formats:

```
```

1. **String Template**: Natural language description of desired extraction
2. **Dictionary Template**: Key-value pairs with field names and descriptions
3. **Pydantic Model**: Strongly-typed schema with validation

**Extraction Result:**

The `ExtractionResult` contains:

- `data`: Extracted structured data matching the template schema
- `confidence`: Model confidence score for the extraction
- `source`: Original source document information

**Use Cases:**

- Metadata extraction (titles, authors, dates)
- Form data extraction
- Invoice/receipt parsing
- Scientific paper metadata
- Custom field extraction from any document type

See [DocumentExtractor API](docling-project/docling/7.2-documentextractor-api.md) for detailed documentation including template design, model configuration, and advanced extraction patterns.

Sources: [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py) [docling/datamodel/pipeline\_options.py328-332](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L328-L332)

## Configuration and Integration Patterns

Both `DocumentConverter` and `DocumentExtractor` share common configuration patterns through `FormatOption` classes that map input formats to processing pipelines.

**Format Configuration:**

```
```

**Supported Format Configurations:**

| FormatOption             | InputFormat | Backend                         | Default Pipeline      |
| ------------------------ | ----------- | ------------------------------- | --------------------- |
| `PdfFormatOption`        | PDF         | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` |
| `ImageFormatOption`      | IMAGE       | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` |
| `WordFormatOption`       | DOCX        | `MsWordDocumentBackend`         | `SimplePipeline`      |
| `ExcelFormatOption`      | XLSX        | `MsExcelDocumentBackend`        | `SimplePipeline`      |
| `PowerpointFormatOption` | PPTX        | `MsPowerpointDocumentBackend`   | `SimplePipeline`      |
| `HTMLFormatOption`       | HTML        | `HTMLDocumentBackend`           | `SimplePipeline`      |
| `MarkdownFormatOption`   | MD          | `MarkdownDocumentBackend`       | `SimplePipeline`      |
| `AudioFormatOption`      | AUDIO       | `NoOpBackend`                   | `AsrPipeline`         |

**Common Configuration Pattern:**

```
```

Sources: [docling/document\_converter.py62-182](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L62-L182) [docling/datamodel/pipeline\_options.py273-384](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L273-L384)

## Integration with AI Frameworks

The SDK's `DoclingDocument` output integrates seamlessly with popular AI frameworks and RAG pipelines.

**Framework Integration Pattern:**

```
```

**LangChain Integration:**

```
```

**LlamaIndex Integration:**

```
```

**Document Chunking:**

Docling provides specialized chunkers for optimal RAG performance:

- `HybridChunker`: Combines semantic and structural chunking
- `MetaChunker`: Preserves metadata and hierarchical structure
- `DocChunks`: Native chunk representation with provenance

See [Chunking](docling-project/docling/8.2-document-chunking.md) for detailed chunking strategies and [Framework Integrations](docling-project/docling/8.3-framework-integrations.md) for specific framework examples.

Sources: [docling\_core.transforms.chunker](https://github.com/docling-project/docling/blob/f7244a43/docling_core.transforms.chunker) [examples/rag\_langchain.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_langchain.ipynb) [examples/rag\_llamaindex.ipynb](https://github.com/docling-project/docling/blob/f7244a43/examples/rag_llamaindex.ipynb)

## Input Handling and Validation

Both APIs support multiple input types and provide comprehensive validation for reliable processing.

**Supported Input Types:**

```
```

**Format Detection:**

The SDK automatically detects document formats using:

1. MIME type detection (`filetype.guess_mime()`)
2. File extension analysis
3. Content inspection for ambiguous formats
4. Special handling for compressed archives (METS, etc.)

**Validation Configuration:**

```
```

**DocumentStream for In-Memory Processing:**

```
```

Sources: [docling/datamodel/document.py236-490](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L236-L490) [docling/datamodel/base\_models.py16](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L16-L16)

## Performance and Caching

The SDK implements intelligent caching and batch processing for optimal performance.

**Pipeline Caching:**

```
```

**Key Caching Features:**

- Pipelines cached by `(pipeline_class, options_hash)` tuple
- Thread-safe initialization with `_PIPELINE_CACHE_LOCK`
- Shared across multiple documents with same configuration
- Automatic model loading and reuse

**Batch Processing:**

```
```

**Performance Settings:**

The SDK respects global performance settings from `settings.perf`:

- `doc_batch_size`: Number of documents per batch
- `doc_batch_concurrency`: Parallel document processing threads
- `page_batch_size`: Pages processed per batch in pipelines

Sources: [docling/document\_converter.py203-379](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L203-L379) [docling/datamodel/settings.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/settings.py#LNaN-LNaN)

## Configuration Validation and Limits

The SDK provides comprehensive validation through `DocumentLimits` to prevent resource exhaustion and ensure predictable processing behavior.

**DocumentLimits Configuration:**

- `max_file_size`: Maximum file size in bytes
- `max_num_pages`: Maximum pages for paginated documents
- `page_range`: Tuple specifying page range to process

**Validation Points:**

1. **File size check**: Before document parsing
2. **Page count check**: After backend initialization
3. **Page range validation**: Ensures valid range specification
4. **Format validation**: Against allowed formats list

```
```

Sources: [docling/datamodel/settings.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/settings.py#LNaN-LNaN) [docling/datamodel/document.py108-168](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L108-L168)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Python SDK](#python-sdk.md)
- [DocumentConverter Overview](#documentconverter-overview.md)
- [DocumentExtractor Overview](#documentextractor-overview.md)
- [Configuration and Integration Patterns](#configuration-and-integration-patterns.md)
- [Integration with AI Frameworks](#integration-with-ai-frameworks.md)
- [Input Handling and Validation](#input-handling-and-validation.md)
- [Performance and Caching](#performance-and-caching.md)
- [Configuration Validation and Limits](#configuration-validation-and-limits.md)
