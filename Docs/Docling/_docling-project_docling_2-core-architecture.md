Core Architecture | docling-project/docling | DeepWiki

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

# Core Architecture

Relevant source files

- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)

This document provides an architectural overview of Docling's core system design, including its three-layer architecture, key abstractions, and how components interact during document processing. For details on specific subsystems, see [Document Conversion Flow](docling-project/docling/2.1-document-conversion-flow.md), [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md), [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md), and [Format Detection and Routing](docling-project/docling/2.4-format-detection-and-routing.md).

## System Overview

Docling implements a three-layer architecture that separates user interfaces, orchestration logic, and processing pipelines:

### Three-Layer Architecture

```
```

**Sources:** [docling/document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L433) [docling/document\_extractor.py88-326](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L326) [docling/cli/main.py298-816](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L298-L816) [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133)

### Layer Responsibilities

| Layer                    | Components                               | Responsibility                                                      |
| ------------------------ | ---------------------------------------- | ------------------------------------------------------------------- |
| **User Interfaces**      | CLI, SDK, MCP                            | Accept user input, parse arguments, invoke core APIs                |
| **Core Orchestration**   | `DocumentConverter`, `DocumentExtractor` | Route documents to appropriate pipelines, manage pipeline lifecycle |
| **Processing Pipelines** | `BasePipeline` subclasses                | Execute multi-stage document processing (build, assemble, enrich)   |
| **Document Backends**    | `AbstractDocumentBackend` subclasses     | Provide format-specific document reading and parsing                |
| **Output**               | `DoclingDocument`                        | Unified document representation with export capabilities            |

**Sources:** [docling/document\_converter.py184-206](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L206) [docling/pipeline/base\_pipeline.py43-85](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L85)

## Key Abstractions

### DocumentConverter and DocumentExtractor

The system provides two primary entry points for different use cases:

```
```

- **`DocumentConverter`** ([document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L184-L433)): Converts documents to `DoclingDocument` format for downstream processing, search, or archival
- **`DocumentExtractor`** ([document\_extractor.py88-326](https://github.com/docling-project/docling/blob/f7244a43/document_extractor.py#L88-L326)): Extracts structured data from documents according to a template (experimental feature)

Both classes share a similar architecture with format routing and pipeline caching but serve different end goals.

**Sources:** [docling/document\_converter.py184-206](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L206) [docling/document\_extractor.py88-120](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L120)

### FormatOption: The Routing Mechanism

The `FormatOption` class pairs each `InputFormat` with its appropriate pipeline and backend:

```
```

The `DocumentConverter` maintains a `format_to_options: Dict[InputFormat, FormatOption]` mapping that determines how each format is processed. This is configured during initialization and can be customized per format.

**Sources:** [docling/document\_converter.py62-131](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L62-L131) [docling/datamodel/base\_models.py36-42](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L36-L42)

### Pipeline Hierarchy

Pipelines implement the `BasePipeline` abstract class, which defines a three-phase processing model:

```
```

**Key Methods:**

- `execute()` ([base\_pipeline.py62-84](https://github.com/docling-project/docling/blob/f7244a43/base_pipeline.py#L62-L84)): Entry point that orchestrates the three-phase processing
- `_build_document()`: Extract raw structure from the document backend
- `_assemble_document()`: Construct hierarchical document structure
- `_enrich_document()`: Apply enrichment models (code detection, picture classification, etc.)

**Sources:** [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133) [docling/pipeline/base\_pipeline.py135-182](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L135-L182) [docling/pipeline/base\_pipeline.py184-320](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L184-L320)

### Backend System

Backends provide format-specific document reading capabilities:

```
```

- **`PaginatedDocumentBackend`** ([backend/abstract\_backend.py58-88](https://github.com/docling-project/docling/blob/f7244a43/backend/abstract_backend.py#L58-L88)): Supports page-by-page iteration, used by PDF/image formats
- **`DeclarativeDocumentBackend`** ([backend/abstract\_backend.py91-101](https://github.com/docling-project/docling/blob/f7244a43/backend/abstract_backend.py#L91-L101)): Directly outputs `DoclingDocument`, used by DOCX/HTML/Markdown formats

**Sources:** [docling/backend/abstract\_backend.py13-101](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py#L13-L101) [docling/backend/pdf\_backend.py1-100](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pdf_backend.py#L1-L100)

## Conversion Flow Architecture

The document conversion process follows a consistent pattern across all pipelines:

```
```

**Sources:** [docling/document\_converter.py227-284](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L227-L284) [docling/document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L351-L378) [docling/pipeline/base\_pipeline.py62-84](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L62-L84)

### Pipeline Caching Mechanism

The `DocumentConverter` caches pipeline instances to avoid redundant model loading:

```
```

**Caching Logic** ([document\_converter.py212-217](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L212-L217) [document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L351-L378)):

1. Compute MD5 hash of `pipeline_options.model_dump()`
2. Create composite key: `(pipeline_cls, options_hash)`
3. Check cache with thread lock (`_PIPELINE_CACHE_LOCK`)
4. Initialize and store if not found
5. Return cached instance if found

This optimization is critical for performance when processing multiple documents with identical configurations, as it prevents re-initialization of heavy ML models.

**Sources:** [docling/document\_converter.py203-217](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L203-L217) [docling/document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L351-L378)

## Pipeline Processing Phases

All pipelines inherit the three-phase processing model from `BasePipeline`:

### Phase 1: Build Document

```
```

- **StandardPdfPipeline**: Sequential model execution for PDF/image processing
- **SimplePipeline**: Direct backend conversion for structured formats (DOCX, HTML)
- **VlmPipeline**: Vision-language model inference for end-to-end processing

**Sources:** [docling/pipeline/base\_pipeline.py86-91](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L86-L91) [docling/pipeline/simple\_pipeline.py26-41](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L26-L41) [docling/pipeline/vlm\_pipeline.py136-186](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L136-L186)

### Phase 2: Assemble Document

This phase constructs the hierarchical `DoclingDocument` structure from extracted elements. The implementation varies by pipeline:

- **StandardPdfPipeline**: Combines page-level elements into document structure
- **VlmPipeline**: Converts VLM output (DOCTAGS/Markdown/HTML) into `DoclingDocument`
- **SimplePipeline**: Uses pre-assembled structure from backend

**Sources:** [docling/pipeline/base\_pipeline.py90-91](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L90-L91) [docling/pipeline/vlm\_pipeline.py136-186](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L136-L186)

### Phase 3: Enrich Document

Enrichment models operate on the assembled `DoclingDocument` to add additional information:

```
```

Each enrichment model:

1. Calls `prepare_element()` to filter relevant document items
2. Processes items in batches
3. Updates the `DoclingDocument` in-place

**Sources:** [docling/pipeline/base\_pipeline.py93-115](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L93-L115) [docling/pipeline/base\_pipeline.py136-176](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L136-L176)

## Configuration Architecture

The configuration system is hierarchical, with options cascading from top-level `PipelineOptions` to model-specific configurations:

```
```

For detailed configuration information, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md).

**Sources:** [docling/datamodel/pipeline\_options.py273-384](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L273-L384)

## Input Document and Backend Lifecycle

The `InputDocument` class manages document validation and backend initialization:

```
```

**Key Lifecycle Points:**

1. **Validation** ([datamodel/document.py131-182](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L131-L182)): Check file size and page count against `DocumentLimits`
2. **Backend Initialization** ([datamodel/document.py183-191](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L183-L191)): Create backend instance with document reference
3. **Page Loading** (in pipelines): Lazy page loading via `backend.load_page(page_no)`
4. **Resource Cleanup** ([pipeline/base\_pipeline.py285-293](https://github.com/docling-project/docling/blob/f7244a43/pipeline/base_pipeline.py#L285-L293)): Unload backends after processing

**Sources:** [docling/datamodel/document.py104-191](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L104-L191) [docling/pipeline/base\_pipeline.py285-293](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L285-L293)

## ThreadedStandardPdfPipeline Architecture

For high-performance PDF processing, `ThreadedStandardPdfPipeline` implements a multi-threaded stage graph:

```
```

**Key Features:**

- **ThreadedQueue** ([threaded\_standard\_pdf\_pipeline.py96-163](https://github.com/docling-project/docling/blob/f7244a43/threaded_standard_pdf_pipeline.py#L96-L163)): Bounded queue with blocking `put()`/`get_batch()` and explicit `close()` semantics
- **ThreadedPipelineStage** ([threaded\_standard\_pdf\_pipeline.py165-280](https://github.com/docling-project/docling/blob/f7244a43/threaded_standard_pdf_pipeline.py#L165-L280)): Each stage runs in its own thread, processes batches, and handles errors
- **Backpressure Control**: Queue size limits prevent memory overflow from fast producers
- **Deterministic Shutdown**: `close()` propagates downstream so stages terminate cleanly

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py1-296](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L1-L296) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py379-427](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L379-L427)

## Document Format Detection

Format detection uses a multi-strategy approach implemented in `_DocumentConversionInput._guess_format()`:

```
```

For detailed format detection logic, see [Format Detection and Routing](docling-project/docling/2.4-format-detection-and-routing.md).

**Sources:** [docling/datamodel/document.py280-374](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L280-L374)

## Output and Export

All pipelines converge on `DoclingDocument` as the unified representation:

```
```

The `DoclingDocument` class (from `docling-core`) provides:

- Hierarchical document structure with provenance tracking
- Multiple export formats with configurable image handling
- Item iteration with `iterate_items()` for traversal

For details on the data model, see [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md). For export format details, see [Export Formats](docling-project/docling/8.1-export-formats.md).

**Sources:** [docling/cli/main.py191-290](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L191-L290) [docling/datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L215)

## Summary

Docling's architecture achieves separation of concerns through:

1. **Clear layer boundaries**: User interfaces, orchestration, pipelines, backends, and output
2. **Pluggable components**: Pipeline and backend selection via `FormatOption` mappings
3. **Performance optimization**: Pipeline caching prevents redundant model initialization
4. **Consistent processing model**: Three-phase execution (build, assemble, enrich) across all pipelines
5. **Unified output**: All pipelines produce `DoclingDocument` for consistent downstream processing

This design allows Docling to handle diverse document formats with format-specific optimizations while maintaining a consistent external API.

**Sources:** [docling/document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L433) [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133) [docling/datamodel/document.py104-191](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L104-L191)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Core Architecture](#core-architecture.md)
- [System Overview](#system-overview.md)
- [Three-Layer Architecture](#three-layer-architecture.md)
- [Layer Responsibilities](#layer-responsibilities.md)
- [Key Abstractions](#key-abstractions.md)
- [DocumentConverter and DocumentExtractor](#documentconverter-and-documentextractor.md)
- [FormatOption: The Routing Mechanism](#formatoption-the-routing-mechanism.md)
- [Pipeline Hierarchy](#pipeline-hierarchy.md)
- [Backend System](#backend-system.md)
- [Conversion Flow Architecture](#conversion-flow-architecture.md)
- [Pipeline Caching Mechanism](#pipeline-caching-mechanism.md)
- [Pipeline Processing Phases](#pipeline-processing-phases.md)
- [Phase 1: Build Document](#phase-1-build-document.md)
- [Phase 2: Assemble Document](#phase-2-assemble-document.md)
- [Phase 3: Enrich Document](#phase-3-enrich-document.md)
- [Configuration Architecture](#configuration-architecture.md)
- [Input Document and Backend Lifecycle](#input-document-and-backend-lifecycle.md)
- [ThreadedStandardPdfPipeline Architecture](#threadedstandardpdfpipeline-architecture.md)
- [Document Format Detection](#document-format-detection.md)
- [Output and Export](#output-and-export.md)
- [Summary](#summary.md)
