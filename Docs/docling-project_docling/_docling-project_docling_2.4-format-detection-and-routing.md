Format Detection and Routing | docling-project/docling | DeepWiki

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

# Format Detection and Routing

Relevant source files

- [docling/backend/abstract\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py)
- [docling/backend/docling\_parse\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py)
- [docling/backend/docling\_parse\_v2\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py)
- [docling/backend/docling\_parse\_v4\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py)
- [docling/backend/pypdfium2\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py)
- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [docling/utils/layout\_postprocessor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/layout_postprocessor.py)
- [docling/utils/locks.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/locks.py)
- [tests/test\_backend\_docling\_parse\_v4.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse_v4.py)

This document describes how Docling automatically detects the format of input documents and routes them to the appropriate backend and pipeline for processing. For information about pipeline execution itself, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md). For backend implementation details, see [Document Backends](docling-project/docling/3-document-backends.md).

## Overview

Format detection and routing is the critical orchestration layer that connects user inputs to the correct processing strategy. The system performs three main operations:

1. **Format Detection**: Analyzes input files using MIME types, file extensions, and content inspection to determine the `InputFormat`
2. **Backend Selection**: Maps the detected format to a document backend class that can parse that format
3. **Pipeline Selection**: Routes the format to a processing pipeline with appropriate configuration options

These operations ensure that each document type receives optimal processing with format-specific parsing and model application strategies.

## Format Detection Architecture

The format detection system uses a multi-strategy approach to reliably identify document types, even when file extensions are missing or misleading.

```
```

**Sources:** [docling/datamodel/document.py280-490](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L280-L490) [docling/datamodel/base\_models.py83-139](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L83-L139)

### Detection Strategy Priority

The `_guess_format()` method implements a waterfall detection strategy:

1. **Primary MIME detection**: Uses `filetype` library to guess MIME type from file magic bytes
2. **Extension fallback**: If MIME detection fails, derives MIME from file extension using `_mime_from_extension()`
3. **Content-based refinement**: For ambiguous formats (e.g., `application/zip` could be DOCX/XLSX/PPTX), reads file content to disambiguate
4. **Specialized detectors**: Applies format-specific detection for complex types like METS archives, USPTO patents, JATS articles

**Key Code Locations:**

- Main detection entry point: [docling/datamodel/document.py280-338](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L280-L338)
- MIME-to-format mapping: [docling/datamodel/base\_models.py135-139](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L135-L139)
- Extension-to-format mapping: [docling/datamodel/base\_models.py83-99](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L83-L99)

## Format Routing System

Once a format is detected, the `DocumentConverter` uses the `FormatOption` model to route documents to the correct backend and pipeline combination.

```
```

**Sources:** [docling/document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L184-L433)

### FormatOption Model

The `FormatOption` class is the central routing data structure that pairs each `InputFormat` with its processing strategy:

| Field              | Type                            | Purpose                              |
| ------------------ | ------------------------------- | ------------------------------------ |
| `backend`          | `Type[AbstractDocumentBackend]` | Backend class for parsing the format |
| `pipeline_cls`     | `Type[BasePipeline]`            | Pipeline class for processing        |
| `pipeline_options` | `PipelineOptions`               | Configuration for the pipeline       |

Specialized subclasses exist for convenience:

- `PdfFormatOption`: Routes PDFs to `StandardPdfPipeline` with `DoclingParseV4DocumentBackend`
- `WordFormatOption`: Routes DOCX to `SimplePipeline` with `MsWordDocumentBackend`
- `AudioFormatOption`: Routes audio to `AsrPipeline` with `NoOpBackend`

**Sources:** [docling/document\_converter.py62-130](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L62-L130)

### Default Routing Table

The `_get_default_option()` function defines the default backend-pipeline pairing for each format:

| InputFormat    | Backend                         | Pipeline              | Notes                                 |
| -------------- | ------------------------------- | --------------------- | ------------------------------------- |
| `PDF`          | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` | Default PDF processing with v4 parser |
| `IMAGE`        | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` | Images treated as single-page PDFs    |
| `DOCX`         | `MsWordDocumentBackend`         | `SimplePipeline`      | Office Open XML documents             |
| `XLSX`         | `MsExcelDocumentBackend`        | `SimplePipeline`      | Excel spreadsheets                    |
| `PPTX`         | `MsPowerpointDocumentBackend`   | `SimplePipeline`      | PowerPoint presentations              |
| `HTML`         | `HTMLDocumentBackend`           | `SimplePipeline`      | Web content                           |
| `MD`           | `MarkdownDocumentBackend`       | `SimplePipeline`      | Markdown documents                    |
| `ASCIIDOC`     | `AsciiDocBackend`               | `SimplePipeline`      | AsciiDoc format                       |
| `CSV`          | `CsvDocumentBackend`            | `SimplePipeline`      | Comma-separated values                |
| `METS_GBS`     | `MetsGbsDocumentBackend`        | `StandardPdfPipeline` | Google Books METS archives            |
| `XML_JATS`     | `JatsDocumentBackend`           | `SimplePipeline`      | Scientific article format             |
| `XML_USPTO`    | `PatentUsptoDocumentBackend`    | `SimplePipeline`      | USPTO patent format                   |
| `JSON_DOCLING` | `DoclingJSONBackend`            | `SimplePipeline`      | Native DoclingDocument JSON           |
| `AUDIO`        | `NoOpBackend`                   | `AsrPipeline`         | Audio transcription                   |
| `VTT`          | `WebVTTDocumentBackend`         | `SimplePipeline`      | Subtitle format                       |

**Sources:** [docling/document\_converter.py132-182](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L132-L182)

### Pipeline Caching Mechanism

To avoid redundant model loading, `DocumentConverter` caches pipeline instances based on a composite key:

```
```

**Caching Logic:**

1. Hash the serialized `pipeline_options` to create a stable fingerprint
2. Use `(pipeline_class, options_hash)` as the cache key
3. Thread-safe access using `_PIPELINE_CACHE_LOCK`
4. Pipelines with identical configurations share the same instance across all documents

This approach is critical for performance when processing batches of documents with the same pipeline configuration, as it avoids reloading models (OCR engines, layout models, table models, etc.) for each document.

**Sources:** [docling/document\_converter.py212-218](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L212-L218) [docling/document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L351-L378)

## Detailed Format Detection Mechanisms

### MIME Type and Extension Detection

The system uses two complementary approaches for basic format detection:

**MIME Type Detection** ([docling/datamodel/document.py285-304](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L285-L304)):

- For `Path` inputs: Uses `filetype.guess_mime()` on file path
- For `DocumentStream` inputs: Reads first 8KB and uses `filetype.guess_mime()` on content
- Maps detected MIME to `InputFormat` via `MimeTypeToFormat` dictionary

**Extension-Based Detection** ([docling/datamodel/document.py377-400](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L377-L400)):

- Fallback when MIME detection fails
- Extracts file extension and looks up corresponding MIME type
- Uses `FormatToMimeType` and `FormatToExtensions` mappings

### Office Document Disambiguation

Office Open XML formats (DOCX, XLSX, PPTX) all use `application/zip` as their MIME type, requiring special handling:

```
```

**Implementation:** [docling/datamodel/document.py292-318](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L292-L318)

### Specialized Content-Based Detection

For formats that cannot be reliably detected by MIME or extension alone, the system reads file content and applies pattern matching.

#### METS Archive Detection

METS (Metadata Encoding and Transmission Standard) archives from Google Books use `.tar.gz` extension but need special handling:

**Detection Process:**

1. Detect `application/gzip` MIME type
2. Open tarball and scan member files
3. Look for XML files containing `http://www.loc.gov/METS/` namespace
4. If found, classify as `InputFormat.METS_GBS`

**Sources:** [docling/datamodel/document.py320-322](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L320-L322) [docling/datamodel/document.py471-489](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L471-L489)

#### HTML/XHTML/XML Detection

The `_detect_html_xhtml()` method analyzes document preambles to distinguish between similar markup formats:

**Detection Rules:**

1. Remove XML comments from content

2. Check for XML declaration (`<?xml`)

   - If contains "xhtml": `application/xhtml+xml`
   - Otherwise: `application/xml`

3. Check for HTML5/4 markers: `<!doctype html>`, `<html>`, `<head>`, `<body>`

4. Check for XML doctype with matching root element

**Sources:** [docling/datamodel/document.py402-439](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L402-L439)

#### CSV Detection

Uses Python's `csv.Sniffer` to detect CSV characteristics:

**Detection Rules:**

1. Check for newline presence (multi-line requirement)
2. Apply `csv.Sniffer().sniff()` to detect dialect
3. Verify delimiter is common (`,`, `;`, `\t`, `|`)

**Sources:** [docling/datamodel/document.py441-468](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L441-L468)

#### Scientific Format Detection

For XML-based scientific formats, the system inspects DOCTYPE declarations:

**USPTO Patent Detection:**

- Checks for DOCTYPE containing: `us-patent-application-v4`, `us-patent-grant-v4`, `us-grant-025`, `patent-application-publication`
- Also detects plain text format starting with `PATN\r\n`

**JATS Article Detection:**

- Checks for DOCTYPE containing: `JATS-journalpublishing`, `JATS-archive`

**Sources:** [docling/datamodel/document.py340-374](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L340-L374)

## CLI Format Configuration

The CLI provides extensive control over format routing through command-line arguments:

```
```

**Key CLI Options:**

| Option          | Purpose                      | Example                      |
| --------------- | ---------------------------- | ---------------------------- |
| `--from`        | Filter allowed input formats | `--from pdf --from docx`     |
| `--pipeline`    | Select processing pipeline   | `--pipeline vlm`             |
| `--pdf-backend` | Choose PDF backend           | `--pdf-backend dlparse_v4`   |
| `--ocr-engine`  | Select OCR engine            | `--ocr-engine tesseract`     |
| `--vlm-model`   | Choose VLM model             | `--vlm-model granitedocling` |

**Sources:** [docling/cli/main.py308-697](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L308-L697)

### Pipeline-Specific Routing

The CLI constructs different `FormatOption` configurations based on the `--pipeline` argument:

**Standard Pipeline** ([docling/cli/main.py619-697](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L619-L697)):

- Creates `PdfPipelineOptions` with OCR, table, and enrichment settings
- Instantiates `PdfFormatOption` with selected backend
- Creates `ConvertPipelineOptions` for simple formats (DOCX, HTML, etc.)

**VLM Pipeline** ([docling/cli/main.py699-748](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L699-L748)):

- Creates `VlmPipelineOptions` with selected VLM model
- Routes only PDF and IMAGE formats
- Automatically selects MLX backend on Darwin platform if available

**ASR Pipeline** ([docling/cli/main.py750-781](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L750-L781)):

- Creates `AsrPipelineOptions` with selected Whisper model
- Routes only AUDIO format
- Uses `NoOpBackend` since audio parsing happens in pipeline

## Complete Detection and Routing Flow

```
```

**Sources:** [docling/document\_converter.py313-350](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L313-L350) [docling/datamodel/document.py241-279](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L241-L279)

## Error Handling and Validation

The format detection system includes robust error handling:

**Invalid Format Handling:**

- If detected format is not in `allowed_formats`, creates `ConversionResult` with status `SKIPPED`
- If no backend can be selected, uses `_DummyBackend` to mark document as invalid
- Logs error messages with detected format and allowed formats for debugging

**Backend Validation:**

- Each backend implements `is_valid()` to verify successful initialization
- If backend initialization fails, `InputDocument.valid` is set to `False`
- Invalid documents are caught before pipeline execution

**Sources:** [docling/datamodel/document.py251-278](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L251-L278) [docling/document\_converter.py380-432](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L380-L432)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Format Detection and Routing](#format-detection-and-routing.md)
- [Overview](#overview.md)
- [Format Detection Architecture](#format-detection-architecture.md)
- [Detection Strategy Priority](#detection-strategy-priority.md)
- [Format Routing System](#format-routing-system.md)
- [FormatOption Model](#formatoption-model.md)
- [Default Routing Table](#default-routing-table.md)
- [Pipeline Caching Mechanism](#pipeline-caching-mechanism.md)
- [Detailed Format Detection Mechanisms](#detailed-format-detection-mechanisms.md)
- [MIME Type and Extension Detection](#mime-type-and-extension-detection.md)
- [Office Document Disambiguation](#office-document-disambiguation.md)
- [Specialized Content-Based Detection](#specialized-content-based-detection.md)
- [METS Archive Detection](#mets-archive-detection.md)
- [HTML/XHTML/XML Detection](#htmlxhtmlxml-detection.md)
- [CSV Detection](#csv-detection.md)
- [Scientific Format Detection](#scientific-format-detection.md)
- [CLI Format Configuration](#cli-format-configuration.md)
- [Pipeline-Specific Routing](#pipeline-specific-routing.md)
- [Complete Detection and Routing Flow](#complete-detection-and-routing-flow.md)
- [Error Handling and Validation](#error-handling-and-validation.md)
