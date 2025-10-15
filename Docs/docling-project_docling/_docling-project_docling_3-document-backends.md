Document Backends | docling-project/docling | DeepWiki

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

# Document Backends

Relevant source files

- [docling/backend/abstract\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py)
- [docling/backend/docling\_parse\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py)
- [docling/backend/docling\_parse\_v2\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py)
- [docling/backend/docling\_parse\_v4\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py)
- [docling/backend/html\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py)
- [docling/backend/pypdfium2\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py)
- [docling/utils/layout\_postprocessor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/layout_postprocessor.py)
- [docling/utils/locks.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/locks.py)
- [tests/data/groundtruth/docling\_v2/example\_06.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_06.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.json)
- [tests/data/groundtruth/docling\_v2/example\_06.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.md)
- [tests/data/groundtruth/docling\_v2/example\_09.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_09.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.json)
- [tests/data/groundtruth/docling\_v2/example\_09.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.md)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.itxt)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.json)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.md)
- [tests/test\_backend\_docling\_parse\_v4.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse_v4.py)
- [tests/test\_backend\_html.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_html.py)

This document covers the backend architecture in Docling that handles parsing and initial processing of different document formats. Document backends are responsible for extracting raw content and structure from input files before they enter the AI/ML processing pipeline.

For information about the complete document conversion process, see [Document Conversion Process](docling-project/docling/2.1-document-conversion-flow.md). For details about pipeline processing that occurs after backend parsing, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md).

## Backend Architecture Overview

The backend system uses a hierarchical class structure to handle different document types with specialized parsing logic. All backends inherit from abstract base classes that define common interfaces for document processing.

```
```

**Backend Class Hierarchy**

The architecture distinguishes between two main backend categories:

- **PaginatedDocumentBackend**: Backends that process documents page-by-page, typically for PDFs and images
- **DeclarativeDocumentBackend**: Backends that can directly convert structured documents to `DoclingDocument` format

Sources: [docling/backend/abstract\_backend.py13-64](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py#L13-L64) [docling/document\_converter.py16-29](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L16-L29)

## Format Detection and Backend Selection

The system automatically detects document formats and selects appropriate backends through a sophisticated detection process implemented in `_DocumentConversionInput`.

```
```

**Format Detection and Backend Selection Flow**

The detection process handles complex scenarios like ZIP-based Office formats and ambiguous MIME types through multi-stage analysis.

Sources: [docling/datamodel/document.py280-374](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L280-L374) [docling/datamodel/base\_models.py85-139](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L85-L139)

## PDF Processing Backends

PDF backends represent the most sophisticated document processing capabilities in Docling, with multiple implementation options for different use cases.

### DoclingParseV4DocumentBackend

The primary PDF backend using the latest version of the docling-parse library for advanced PDF processing.

```
```

**DoclingParseV4 Backend Processing Flow**

Sources: [docling/backend/docling\_parse\_v4\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py) (referenced but not shown in files), [docling/document\_converter.py118-124](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L118-L124)

### PyPdfiumDocumentBackend

A fallback PDF backend using the pypdfium2 library for basic PDF text extraction and rendering.

| Feature         | DoclingParseV4                   | PyPdfium2                      |
| --------------- | -------------------------------- | ------------------------------ |
| Text extraction | Advanced with normalized content | Basic text boundary extraction |
| Cell merging    | Built-in intelligent merging     | Manual horizontal cell merging |
| Image detection | Native image region detection    | PyPdfium2 object enumeration   |
| Performance     | Optimized for document AI        | General-purpose PDF rendering  |
| Dependencies    | docling-parse library            | pypdfium2 only                 |

Sources: [docling/backend/pypdfium2\_backend.py101-400](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L101-L400) [docling/backend/pypdfium2\_backend.py156-252](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L156-L252)

### Legacy DoclingParse Backends

The system maintains backward compatibility with older docling-parse versions through dedicated backend implementations.

Sources: [docling/backend/docling\_parse\_backend.py200-238](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py#L200-L238) [docling/backend/docling\_parse\_v2\_backend.py228-277](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L228-L277)

## Office Document Backends

Office document backends handle Microsoft Office formats through direct parsing of the underlying XML structures.

```
```

**Office Document Backend Processing**

Office backends extend `DeclarativeDocumentBackend` and implement direct conversion to `DoclingDocument` without requiring AI/ML pipeline processing.

Sources: [docling/document\_converter.py76-88](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L76-L88) [docling/document\_converter.py132-144](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L132-L144)

## Web and Text Document Backends

Web and text backends handle various markup and plain text formats through specialized parsers.

### HTML and Markdown Backends

| Backend                   | Parser Library | Supported Formats | Key Features                      |
| ------------------------- | -------------- | ----------------- | --------------------------------- |
| `HTMLDocumentBackend`     | BeautifulSoup  | HTML, XHTML       | DOM parsing, tag preservation     |
| `MarkdownDocumentBackend` | marko          | Markdown, MD      | CommonMark compliance, extensions |
| `AsciiDocBackend`         | Custom parser  | AsciiDoc, ADOC    | Structured document markup        |

### Structured Data Backends

```
```

**Structured Data Backend Processing**

Sources: [docling/document\_converter.py71-74](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L71-L74) [docling/document\_converter.py169-171](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L169-L171)

## Specialized Format Backends

Specialized backends handle domain-specific document formats with custom parsing logic.

### XML-based Scientific Documents

```
```

**Specialized XML Backend Hierarchy**

### Audio Processing Backend

The `NoOpBackend` serves as a placeholder for audio files, which are processed entirely through the ASR pipeline rather than traditional document parsing.

Sources: [docling/document\_converter.py126-129](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L126-L129) [docling/document\_converter.py154-172](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L154-L172)

## Backend Lifecycle and Integration

Document backends follow a structured lifecycle within the conversion process, managed by the `DocumentConverter` class.

```
```

**Backend Lifecycle in Document Conversion**

The lifecycle ensures proper resource management and error handling throughout the conversion process.

Sources: [docling/datamodel/document.py183-191](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L183-L191) [docling/document\_converter.py376-428](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L376-L428)

## Backend Configuration and Options

Each backend type is configured through corresponding `FormatOption` classes that specify both the backend implementation and associated pipeline.

| InputFormat | Backend Class                   | Pipeline Class        | FormatOption Class  |
| ----------- | ------------------------------- | --------------------- | ------------------- |
| `PDF`       | `DoclingParseV4DocumentBackend` | `StandardPdfPipeline` | `PdfFormatOption`   |
| `DOCX`      | `MsWordDocumentBackend`         | `SimplePipeline`      | `WordFormatOption`  |
| `HTML`      | `HTMLDocumentBackend`           | `SimplePipeline`      | `HTMLFormatOption`  |
| `CSV`       | `CsvDocumentBackend`            | `SimplePipeline`      | `CsvFormatOption`   |
| `AUDIO`     | `NoOpBackend`                   | `AsrPipeline`         | `AudioFormatOption` |

The `DocumentConverter` uses these configurations to automatically select and initialize the appropriate backend and pipeline combination for each input format.

Sources: [docling/document\_converter.py61-178](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L61-L178) [docling/datamodel/base\_models.py39-46](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L39-L46)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Document Backends](#document-backends.md)
- [Backend Architecture Overview](#backend-architecture-overview.md)
- [Format Detection and Backend Selection](#format-detection-and-backend-selection.md)
- [PDF Processing Backends](#pdf-processing-backends.md)
- [DoclingParseV4DocumentBackend](#doclingparsev4documentbackend.md)
- [PyPdfiumDocumentBackend](#pypdfiumdocumentbackend.md)
- [Legacy DoclingParse Backends](#legacy-doclingparse-backends.md)
- [Office Document Backends](#office-document-backends.md)
- [Web and Text Document Backends](#web-and-text-document-backends.md)
- [HTML and Markdown Backends](#html-and-markdown-backends.md)
- [Structured Data Backends](#structured-data-backends.md)
- [Specialized Format Backends](#specialized-format-backends.md)
- [XML-based Scientific Documents](#xml-based-scientific-documents.md)
- [Audio Processing Backend](#audio-processing-backend.md)
- [Backend Lifecycle and Integration](#backend-lifecycle-and-integration.md)
- [Backend Configuration and Options](#backend-configuration-and-options.md)
