DocumentConverter API | docling-project/docling | DeepWiki

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

# DocumentConverter API

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

The DocumentConverter API provides the primary programmatic interface for converting documents using Docling. This API orchestrates the entire conversion process from input documents to structured `DoclingDocument` representations, handling format detection, backend selection, pipeline execution, and error management.

For information about the underlying processing pipelines, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md). For details about the output document structure, see [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md). For command-line usage, see [Command Line Interface](docling-project/docling/6-command-line-interface.md).

## Core DocumentConverter Class

The `DocumentConverter` class serves as the central orchestrator for all document conversion operations. It manages format options, initializes processing pipelines, and coordinates the conversion workflow from input to output.

### Class Architecture

```
```

Sources: [docling/document\_converter.py180-429](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L180-L429) [docling/datamodel/document.py104-192](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L104-L192) [docling/datamodel/document.py198-216](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L216) [docling/datamodel/base\_models.py39-46](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L39-L46)

### Initialization and Configuration

The `DocumentConverter` constructor accepts format restrictions and custom format options:

| Parameter         | Type                                        | Description                                       |
| ----------------- | ------------------------------------------- | ------------------------------------------------- |
| `allowed_formats` | `Optional[List[InputFormat]]`               | Restricts which document formats can be processed |
| `format_options`  | `Optional[Dict[InputFormat, FormatOption]]` | Custom backend/pipeline configurations per format |

When no custom options are provided, the converter uses default configurations defined in `_get_default_option()` which maps each `InputFormat` to appropriate backend and pipeline combinations.

Sources: [docling/document\_converter.py183-201](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L183-L201) [docling/document\_converter.py131-178](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L131-L178)

## Input and Output Models

### InputDocument Model

The `InputDocument` class represents a validated input document ready for processing:

```
```

Sources: [docling/datamodel/document.py104-192](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L104-L192) [docling/datamodel/base\_models.py57-74](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L57-L74)

### ConversionResult Model

The `ConversionResult` class encapsulates the complete output of a conversion operation:

| Field        | Type                       | Description                              |
| ------------ | -------------------------- | ---------------------------------------- |
| `input`      | `InputDocument`            | Original input document metadata         |
| `status`     | `ConversionStatus`         | Success/failure status                   |
| `errors`     | `List[ErrorItem]`          | Error details if conversion failed       |
| `document`   | `DoclingDocument`          | Final structured document representation |
| `timings`    | `Dict[str, ProfilingItem]` | Performance metrics per processing stage |
| `confidence` | `ConfidenceReport`         | Quality confidence scores                |

Sources: [docling/datamodel/document.py198-216](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L216)

## Format Options and Backend Selection

### Format Option System

Format options define how each input format should be processed by specifying the backend parser and processing pipeline:

```
```

Sources: [docling/document\_converter.py61-130](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L61-L130) [docling/document\_converter.py131-178](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L131-L178)

### Built-in Format Options

| Format Option Class    | Input Format | Backend                         | Pipeline              |
| ---------------------- | ------------ | ------------------------------- | --------------------- |
| `PdfFormatOption`      | PDF          | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` |
| `WordFormatOption`     | DOCX         | `MsWordDocumentBackend`         | `SimplePipeline`      |
| `ExcelFormatOption`    | XLSX         | `MsExcelDocumentBackend`        | `SimplePipeline`      |
| `HTMLFormatOption`     | HTML         | `HTMLDocumentBackend`           | `SimplePipeline`      |
| `MarkdownFormatOption` | MD           | `MarkdownDocumentBackend`       | `SimplePipeline`      |
| `ImageFormatOption`    | IMAGE        | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` |
| `AudioFormatOption`    | AUDIO        | `NoOpBackend`                   | `AsrPipeline`         |

Sources: [docling/document\_converter.py71-129](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L71-L129)

## Conversion Methods

### Primary Conversion Methods

The `DocumentConverter` provides three main conversion entry points:

#### convert()

Processes a single document and returns a `ConversionResult`:

```
```

Sources: [docling/document\_converter.py223-242](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L223-L242)

#### convert\_all()

Processes multiple documents and returns an iterator of `ConversionResult` objects:

```
```

Sources: [docling/document\_converter.py243-280](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L243-L280)

#### convert\_string()

Converts string content directly without file I/O:

```
```

Currently supports `InputFormat.MD` and `InputFormat.HTML`.

Sources: [docling/document\_converter.py281-308](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L281-L308)

### Conversion Pipeline Flow

```
```

Sources: [docling/document\_converter.py309-345](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L309-L345) [docling/document\_converter.py376-428](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L376-L428) [docling/datamodel/document.py241-279](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L241-L279)

## Error Handling and Status

### ConversionStatus Enumeration

The conversion process tracks status through the `ConversionStatus` enum:

| Status            | Description                                   |
| ----------------- | --------------------------------------------- |
| `PENDING`         | Conversion not yet started                    |
| `STARTED`         | Conversion in progress                        |
| `SUCCESS`         | Conversion completed successfully             |
| `PARTIAL_SUCCESS` | Conversion completed with some issues         |
| `FAILURE`         | Conversion failed                             |
| `SKIPPED`         | Conversion skipped due to format restrictions |

Sources: [docling/datamodel/base\_models.py48-55](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L48-L55)

### Error Reporting

Errors are captured in `ErrorItem` objects that include:

| Field            | Type                   | Description                                |
| ---------------- | ---------------------- | ------------------------------------------ |
| `component_type` | `DoclingComponentType` | Which system component generated the error |
| `module_name`    | `str`                  | Specific module that failed                |
| `error_message`  | `str`                  | Human-readable error description           |

The `raises_on_error` parameter controls whether errors immediately raise exceptions or are captured in the `ConversionResult.errors` list.

Sources: [docling/datamodel/base\_models.py154-158](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L154-L158) [docling/datamodel/base\_models.py147-152](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L147-L152)

## Pipeline Integration

### Pipeline Caching and Reuse

The `DocumentConverter` maintains a cache of initialized pipelines to avoid expensive re-initialization:

```
```

The cache key combines the pipeline class and a hash of the pipeline options, allowing different configurations to coexist while reusing identical setups.

Sources: [docling/document\_converter.py347-374](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L347-L374) [docling/document\_converter.py208-214](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L208-L214)

### Pipeline Selection Logic

Format options determine which pipeline class processes each document type:

- **StandardPdfPipeline**: Advanced processing for PDFs and images with OCR, layout analysis, and table extraction
- **SimplePipeline**: Direct parsing for structured formats like DOCX, HTML, Markdown
- **AsrPipeline**: Speech recognition for audio formats

Sources: [docling/document\_converter.py61-69](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L61-L69) [docling/document\_converter.py215-222](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L215-L222)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [DocumentConverter API](#documentconverter-api.md)
- [Core DocumentConverter Class](#core-documentconverter-class.md)
- [Class Architecture](#class-architecture.md)
- [Initialization and Configuration](#initialization-and-configuration.md)
- [Input and Output Models](#input-and-output-models.md)
- [InputDocument Model](#inputdocument-model.md)
- [ConversionResult Model](#conversionresult-model.md)
- [Format Options and Backend Selection](#format-options-and-backend-selection.md)
- [Format Option System](#format-option-system.md)
- [Built-in Format Options](#built-in-format-options.md)
- [Conversion Methods](#conversion-methods.md)
- [Primary Conversion Methods](#primary-conversion-methods.md)
- [convert()](#convert.md)
- [convert\_all()](#convert_all.md)
- [convert\_string()](#convert_string.md)
- [Conversion Pipeline Flow](#conversion-pipeline-flow.md)
- [Error Handling and Status](#error-handling-and-status.md)
- [ConversionStatus Enumeration](#conversionstatus-enumeration.md)
- [Error Reporting](#error-reporting.md)
- [Pipeline Integration](#pipeline-integration.md)
- [Pipeline Caching and Reuse](#pipeline-caching-and-reuse.md)
- [Pipeline Selection Logic](#pipeline-selection-logic.md)
