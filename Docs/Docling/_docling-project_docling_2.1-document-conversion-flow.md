Document Conversion Flow | docling-project/docling | DeepWiki

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

# Document Conversion Flow

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

This document describes the end-to-end process of converting an input document to a structured `DoclingDocument` representation. It covers format detection, backend/pipeline routing, the three-phase execution model, and output generation.

For configuration of pipeline options and format-specific settings, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md). For details on the `DoclingDocument` data structure, see [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md). For backend implementations, see [Document Backends](docling-project/docling/3-document-backends.md).

---

## Overview

The document conversion flow orchestrates multiple components to transform raw documents (PDF, DOCX, HTML, etc.) into structured `DoclingDocument` objects. The process follows these stages:

1. **Input Processing**: Format detection and `InputDocument` creation
2. **Routing**: Backend and pipeline selection based on format
3. **Pipeline Execution**: Three-phase processing (build, assemble, enrich)
4. **Output Generation**: `ConversionResult` with embedded `DoclingDocument`

The central orchestrator is `DocumentConverter`, which manages format-to-pipeline mappings, pipeline caching, and execution.

---

## Entry Points and Initialization

### DocumentConverter Initialization

The `DocumentConverter` class serves as the primary entry point for document conversion:

```
```

**Key responsibilities:**

- Maintain `format_to_options` mapping: `Dict[InputFormat, FormatOption]`
- Cache initialized pipelines: `Dict[Tuple[Type[BasePipeline], str], BasePipeline]`
- Coordinate batch processing with concurrency control

**Entry Point Diagram**

```
```

**Sources:** [docling/document\_converter.py184-205](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L205) [docling/cli/main.py299-816](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L299-L816)

### Conversion Methods

The API provides two methods:

| Method                | Description                | Return Type                  |
| --------------------- | -------------------------- | ---------------------------- |
| `convert(source)`     | Convert single document    | `ConversionResult`           |
| `convert_all(source)` | Convert multiple documents | `Iterator[ConversionResult]` |

Both methods accept:

- `source`: `Path`, `str` (URL), or `DocumentStream` (BytesIO)
- `headers`: Optional HTTP headers for URL sources
- `raises_on_error`: Control error propagation
- `max_num_pages`, `max_file_size`: Document limits
- `page_range`: Tuple of (start\_page, end\_page)

**Sources:** [docling/document\_converter.py228-283](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L228-L283)

---

## Format Detection and Input Processing

### Format Detection Mechanism

Format detection is handled by `_DocumentConversionInput._guess_format()`, which uses a three-tier strategy:

#### Format Detection Strategy

```
```

**Sources:** [docling/datamodel/document.py280-489](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L280-L489)

#### Tier 1: MIME Type Detection

Uses `filetype.guess_mime()` on file path or first 8KB of stream:

- For `Path`: Reads file signature
- For `DocumentStream`: Reads first 8KB, seeks back to 0

Special cases:

- `application/zip` → Infer DOCX/XLSX/PPTX from file extension
- `application/gzip` → Check for METS metadata via `_detect_mets_gbs()`

**Sources:** [docling/datamodel/document.py285-323](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L285-L323)

#### Tier 2: Extension Mapping

If MIME detection fails, use extension-based lookup:

```
```

Mappings defined in `FormatToMimeType` dictionary.

**Sources:** [docling/datamodel/document.py376-400](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L376-L400) [docling/datamodel/base\_models.py101-133](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L101-L133)

#### Tier 3: Content Analysis

For ambiguous formats (e.g., `application/xml`), parse DOCTYPE declarations:

| DOCTYPE Pattern                            | Format                  |
| ------------------------------------------ | ----------------------- |
| `us-patent-application-v4`, `us-grant-025` | `InputFormat.XML_USPTO` |
| `JATS-journalpublishing`, `JATS-archive`   | `InputFormat.XML_JATS`  |
| `PATN\r\n` (plain text)                    | `InputFormat.XML_USPTO` |

**Sources:** [docling/datamodel/document.py341-374](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L341-L374)

### InputDocument Creation

Once format is detected, `_DocumentConversionInput.docs()` creates `InputDocument` instances:

**InputDocument Creation Flow**

```
```

**Key validation checks:**

- File size ≤ `limits.max_file_size`
- Page count ≤ `limits.max_num_pages`
- Page range within bounds: `limits.page_range`
- Backend validity: `backend.is_valid()`

If any check fails, `InputDocument.valid = False`.

**Sources:** [docling/datamodel/document.py104-191](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L104-L191) [docling/datamodel/document.py236-278](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L236-L278)

---

## Backend and Pipeline Routing

### FormatOption Mapping

The routing mechanism uses `FormatOption` objects that pair formats with pipelines and backends:

**FormatOption Structure**

```
```

**Sources:** [docling/document\_converter.py62-130](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L62-L130)

### Default Format Options

Default mappings are defined in `_get_default_option()`:

| InputFormat | Pipeline              | Backend                         |
| ----------- | --------------------- | ------------------------------- |
| `PDF`       | `StandardPdfPipeline` | `DoclingParseV4DocumentBackend` |
| `IMAGE`     | `StandardPdfPipeline` | `DoclingParseV4DocumentBackend` |
| `DOCX`      | `SimplePipeline`      | `MsWordDocumentBackend`         |
| `XLSX`      | `SimplePipeline`      | `MsExcelDocumentBackend`        |
| `PPTX`      | `SimplePipeline`      | `MsPowerpointDocumentBackend`   |
| `HTML`      | `SimplePipeline`      | `HTMLDocumentBackend`           |
| `MD`        | `SimplePipeline`      | `MarkdownDocumentBackend`       |
| `AUDIO`     | `AsrPipeline`         | `NoOpBackend`                   |

**Sources:** [docling/document\_converter.py132-182](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L132-L182)

### Pipeline Selection and Caching

Pipelines are cached by `(pipeline_class, options_hash)` to avoid redundant initialization:

**Pipeline Caching Flow**

```
```

**Cache key construction:**

1. Serialize `pipeline_options.model_dump()` to string
2. Compute MD5 hash: `hashlib.md5(options_str.encode("utf-8"))`
3. Create tuple: `(pipeline_class, options_hash)`

This ensures:

- Same pipeline class + options → Same pipeline instance
- Thread-safe via `_PIPELINE_CACHE_LOCK`
- Models loaded only once per unique configuration

**Sources:** [docling/document\_converter.py207-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L207-L378)

---

## Pipeline Execution Phases

All pipelines inherit from `BasePipeline` and implement a three-phase execution model:

**Three-Phase Execution Model**

```
```

**Sources:** [docling/pipeline/base\_pipeline.py62-123](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L62-L123)

### Phase 1: Build Document (\_build\_document)

Abstract method implemented by each pipeline. Responsibilities:

- Load document pages/content from backend
- Apply models (OCR, layout, tables) to extract structure
- Populate `ConversionResult.pages` with predictions

**Examples:**

- **PaginatedPipeline**: Iterate pages, apply sequential models via `build_pipe`
- **SimplePipeline**: Call `backend.convert()` directly to get `DoclingDocument`
- **VlmPipeline**: Generate page images, run VLM model for predictions
- **AsrPipeline**: Transcribe audio, create text-based document

**Sources:** [docling/pipeline/base\_pipeline.py86-88](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L86-L88) [docling/pipeline/simple\_pipeline.py26-41](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L26-L41)

### Phase 2: Assemble Document (\_assemble\_document)

Constructs the hierarchical `DoclingDocument` from page-level predictions:

**Assembly Process (PaginatedPipeline Example)**

```
```

**Key operations:**

- Convert page-level `Cluster`, `Table`, `FigureElement` to `DocItem` hierarchy
- Assign provenance metadata (page numbers, bounding boxes)
- Generate cropped images for `PictureItem`, `TableItem` if requested
- Clear page backends/caches if not needed downstream

**Sources:** [docling/pipeline/base\_pipeline.py90-91](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L90-L91)

### Phase 3: Enrich Document (\_enrich\_document)

Applies enrichment models to individual `NodeItem` elements in the `DoclingDocument`:

**Enrichment Pipeline Flow**

```
```

**Common enrichment models:**

- `CodeFormulaModel`: Extract LaTeX from code/formula images
- `DocumentPictureClassifier`: Classify picture types
- `PictureDescriptionVlmModel`: Generate image captions

**Sources:** [docling/pipeline/base\_pipeline.py93-115](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L93-L115) [docling/pipeline/base\_pipeline.py135-177](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L135-L177)

---

## Complete Conversion Flow Sequence

The following diagram shows the complete end-to-end flow with all components:

**End-to-End Document Conversion Sequence**

```
```

**Sources:** [docling/document\_converter.py313-432](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L313-L432) [docling/pipeline/base\_pipeline.py62-123](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L62-L123)

---

## Output Generation

### ConversionResult Structure

The `ConversionResult` object encapsulates all conversion outputs:

| Field        | Type                       | Description                                     |
| ------------ | -------------------------- | ----------------------------------------------- |
| `input`      | `InputDocument`            | Original input metadata                         |
| `status`     | `ConversionStatus`         | `SUCCESS`, `FAILURE`, `PARTIAL_SUCCESS`         |
| `errors`     | `List[ErrorItem]`          | Error details per component                     |
| `pages`      | `List[Page]`               | Page-level data (may be cleared after assembly) |
| `document`   | `DoclingDocument`          | Final structured document                       |
| `timings`    | `Dict[str, ProfilingItem]` | Performance metrics                             |
| `confidence` | `ConfidenceReport`         | Quality scores per page/model                   |

**Sources:** [docling/datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L215)

### Export Formats

The `DoclingDocument` can be exported to multiple formats:

**Export Method Overview**

```
```

**Export options:**

- `image_mode`: `PLACEHOLDER`, `EMBEDDED` (base64), `REFERENCED` (separate PNG files)
- `strict_text`: Strip all formatting (for Markdown)
- `split_page_view`: Separate HTML page per document page

**Sources:** [docling/cli/main.py191-289](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L191-L289)

### Status Determination

The `_determine_status()` method evaluates conversion success:

**Status Resolution Logic**

```
```

**Implementation varies by pipeline:**

- **PaginatedPipeline**: Check each page backend validity
- **SimplePipeline**: Return `SUCCESS` if no exceptions raised
- **AsrPipeline**: Check transcription success

**Sources:** [docling/pipeline/base\_pipeline.py118-119](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L118-L119) [docling/pipeline/base\_pipeline.py295-314](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L295-L314)

---

## Batch Processing and Concurrency

The `DocumentConverter` supports concurrent document processing:

**Batch Processing Configuration**

| Setting                 | Environment Variable            | Default | Description              |
| ----------------------- | ------------------------------- | ------- | ------------------------ |
| `doc_batch_size`        | `DOCLING_DOC_BATCH_SIZE`        | 10      | Documents per batch      |
| `doc_batch_concurrency` | `DOCLING_DOC_BATCH_CONCURRENCY` | 1       | Worker threads           |
| `page_batch_size`       | `DOCLING_PAGE_BATCH_SIZE`       | 10      | Pages processed together |

**Concurrency Flow**

```
```

**Key design points:**

- Each document processes independently (no shared mutable state)
- Pipeline instances are cached and reused (thread-safe)
- Models are initialized once per pipeline (read-only access from workers)
- ThreadPoolExecutor manages worker threads automatically

**Sources:** [docling/document\_converter.py313-349](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L313-L349) [docling/datamodel/settings.py1-82](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/settings.py#L1-L82)

---

## Error Handling and Recovery

### Error Capture

Errors are captured at multiple levels and stored in `ConversionResult.errors`:

| Component Type     | Module Examples                      | Typical Errors                 |
| ------------------ | ------------------------------------ | ------------------------------ |
| `DOCUMENT_BACKEND` | `DoclingParseV4DocumentBackend`      | Corrupt PDF, invalid format    |
| `MODEL`            | `LayoutModel`, `TableStructureModel` | Model inference failure        |
| `DOC_ASSEMBLER`    | `PageAssembleModel`                  | Hierarchy construction error   |
| `USER_INPUT`       | `DocumentConverter`                  | Invalid format, file not found |

**Error Item Structure:**

```
```

**Sources:** [docling/datamodel/base\_models.py147-158](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L147-L158)

### Raises vs Non-Raises Mode

Conversion behavior controlled by `raises_on_error` parameter:

**Error Handling Modes**

```
```

**Non-raises mode allows:**

- Processing multiple documents even if some fail
- Collecting all errors for batch analysis
- Partial success scenarios (some pages succeed)

**Sources:** [docling/document\_converter.py380-432](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L380-L432) [docling/pipeline/base\_pipeline.py62-84](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L62-L84)

---

## Summary

The document conversion flow implements a clean separation of concerns:

1. **Format Detection**: Multi-tier strategy (MIME → Extension → Content)
2. **Routing**: `FormatOption` maps formats to pipeline/backend pairs
3. **Caching**: Pipelines reused via `(class, options_hash)` keys
4. **Execution**: Three-phase model (build → assemble → enrich)
5. **Output**: Unified `DoclingDocument` with multiple export formats

The architecture enables:

- **Extensibility**: New formats add backend + pipeline + `FormatOption`
- **Performance**: Pipeline/model caching, batch processing, concurrency
- **Reliability**: Isolated execution, comprehensive error capture
- **Flexibility**: Per-format configuration, multiple output formats

**Key Code Entities:**

| Entity                     | Location                                                                                                                  | Role                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `DocumentConverter`        | [document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L184-L433) | Orchestrator                      |
| `_DocumentConversionInput` | [document.py236-489](https://github.com/docling-project/docling/blob/f7244a43/document.py#L236-L489)                      | Format detection, input parsing   |
| `InputDocument`            | [document.py104-191](https://github.com/docling-project/docling/blob/f7244a43/document.py#L104-L191)                      | Document metadata + backend       |
| `FormatOption`             | [document\_converter.py62-130](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L62-L130)   | Format → pipeline/backend mapping |
| `BasePipeline`             | [base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/base_pipeline.py#L43-L133)             | Three-phase execution model       |
| `ConversionResult`         | [document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/document.py#L198-L215)                      | Output container                  |

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Document Conversion Flow](#document-conversion-flow.md)
- [Overview](#overview.md)
- [Entry Points and Initialization](#entry-points-and-initialization.md)
- [DocumentConverter Initialization](#documentconverter-initialization.md)
- [Conversion Methods](#conversion-methods.md)
- [Format Detection and Input Processing](#format-detection-and-input-processing.md)
- [Format Detection Mechanism](#format-detection-mechanism.md)
- [Format Detection Strategy](#format-detection-strategy.md)
- [Tier 1: MIME Type Detection](#tier-1-mime-type-detection.md)
- [Tier 2: Extension Mapping](#tier-2-extension-mapping.md)
- [Tier 3: Content Analysis](#tier-3-content-analysis.md)
- [InputDocument Creation](#inputdocument-creation.md)
- [Backend and Pipeline Routing](#backend-and-pipeline-routing.md)
- [FormatOption Mapping](#formatoption-mapping.md)
- [Default Format Options](#default-format-options.md)
- [Pipeline Selection and Caching](#pipeline-selection-and-caching.md)
- [Pipeline Execution Phases](#pipeline-execution-phases.md)
- [Phase 1: Build Document (\_build\_document)](#phase-1-build-document-_build_document.md)
- [Phase 2: Assemble Document (\_assemble\_document)](#phase-2-assemble-document-_assemble_document.md)
- [Phase 3: Enrich Document (\_enrich\_document)](#phase-3-enrich-document-_enrich_document.md)
- [Complete Conversion Flow Sequence](#complete-conversion-flow-sequence.md)
- [Output Generation](#output-generation.md)
- [ConversionResult Structure](#conversionresult-structure.md)
- [Export Formats](#export-formats.md)
- [Status Determination](#status-determination.md)
- [Batch Processing and Concurrency](#batch-processing-and-concurrency.md)
- [Error Handling and Recovery](#error-handling-and-recovery.md)
- [Error Capture](#error-capture.md)
- [Raises vs Non-Raises Mode](#raises-vs-non-raises-mode.md)
- [Summary](#summary.md)
