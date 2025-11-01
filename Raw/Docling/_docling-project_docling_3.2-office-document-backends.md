Office Document Backends | docling-project/docling | DeepWiki

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

# Office Document Backends

Relevant source files

- [docling/backend/msword\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py)
- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [tests/data/docx/textbox.docx](https://github.com/docling-project/docling/blob/f7244a43/tests/data/docx/textbox.docx)
- [tests/data/docx/unit\_test\_formatting.docx](https://github.com/docling-project/docling/blob/f7244a43/tests/data/docx/unit_test_formatting.docx)
- [tests/data/groundtruth/docling\_v2/unit\_test\_formatting.docx.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/unit_test_formatting.docx.itxt)
- [tests/data/groundtruth/docling\_v2/unit\_test\_formatting.docx.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/unit_test_formatting.docx.json)
- [tests/data/groundtruth/docling\_v2/unit\_test\_formatting.docx.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/unit_test_formatting.docx.md)
- [tests/test\_backend\_msword.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msword.py)

This document covers the backend implementations for Microsoft Office document formats in Docling, specifically Word (DOCX) and Excel (XLSX) processing. These backends parse declarative document formats into the universal `DoclingDocument` representation.

For PDF document processing, see [PDF Processing Backends](docling-project/docling/3.1-pdf-processing-backends.md). For web and text format backends, see [Web and Text Document Backends](docling-project/docling/3.3-web-and-markup-backends.md).

## Overview

Docling's office document backends handle structured document formats that contain explicit markup and formatting information. Unlike PDF documents that require AI/ML models for layout analysis, office documents can be processed directly through their XML structure and metadata.

```
```

Sources: [docling/backend/msword\_backend.py32-40](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L32-L40) [docling/backend/msexcel\_backend.py28-31](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L28-L31)

## Microsoft Word Backend

The `MsWordDocumentBackend` processes DOCX files by parsing their Office Open XML structure using the python-docx library and custom XML processing.

### Core Architecture

```
```

Sources: [docling/backend/msword\_backend.py40-92](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L40-L92) [docling/backend/msword\_backend.py170-281](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L170-L281)

### Document Element Processing

The Word backend processes various document elements through specialized handlers:

| Element Type | Handler Method                | Key Features                             |
| ------------ | ----------------------------- | ---------------------------------------- |
| Paragraphs   | `_handle_text_elements()`     | Style detection, formatting, hyperlinks  |
| Tables       | `_handle_tables()`            | Cell extraction, merged cells, structure |
| Images       | `_handle_pictures()`          | Inline images, relationship parsing      |
| Textboxes    | `_handle_textbox_content()`   | Position-aware text extraction           |
| Equations    | `_handle_equations_in_text()` | OMML to LaTeX conversion                 |
| Lists        | `_add_list_item()`            | Numbered and bulleted lists              |

Sources: [docling/backend/msword\_backend.py801-944](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L801-L944) [docling/backend/msword\_backend.py1074-1197](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L1074-L1197)

### List Processing

The backend handles complex list structures with proper nesting and numbering:

```
```

Sources: [docling/backend/msword\_backend.py335-421](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L335-L421) [docling/backend/msword\_backend.py1405-1485](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L1405-L1485)

## Microsoft Excel Backend

The `MsExcelDocumentBackend` processes Excel workbooks by treating each worksheet as a separate page and extracting data tables and images.

### Core Architecture

```
```

Sources: [docling/backend/msexcel\_backend.py89-176](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L89-L176) [docling/backend/msexcel\_backend.py177-226](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L177-L226)

### Table Detection Algorithm

The Excel backend uses a sophisticated algorithm to detect and extract data tables:

```
```

Sources: [docling/backend/msexcel\_backend.py293-394](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L293-L394) [docling/backend/msexcel\_backend.py320-478](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L320-L478)

### Page and Size Management

Excel worksheets are converted to document pages with proper sizing:

| Feature          | Implementation               | Purpose                           |
| ---------------- | ---------------------------- | --------------------------------- |
| Page Numbers     | `workbook.index(sheet) + 1`  | Sequential page numbering         |
| Page Size        | `_find_page_size()`          | Calculate bounding box dimensions |
| Cell Coordinates | `(col, row)` tuples          | 0-based indexing system           |
| Content Layers   | `_get_sheet_content_layer()` | Mark invisible sheets             |

Sources: [docling/backend/msexcel\_backend.py194-205](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L194-L205) [docling/backend/msexcel\_backend.py526-552](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L526-L552)

## Integration with Document Converter

Both office document backends integrate with the main document conversion pipeline through the format detection and backend selection system:

```
```

Sources: [docling/backend/msword\_backend.py111-112](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L111-L112) [docling/backend/msexcel\_backend.py146-147](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L146-L147)

## Common Features and Patterns

### Declarative Document Processing

Both backends inherit from `DeclarativeDocumentBackend`, which provides:

- Direct structural parsing without AI/ML models
- Format-specific input validation
- Standardized conversion interface
- Error handling and cleanup

Sources: [docling/backend/abstract\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py) [docling/backend/msword\_backend.py32](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L32-L32) [docling/backend/msexcel\_backend.py29](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L29-L29)

### Document Structure Creation

Both backends create hierarchical document structures using:

- Parent-child relationships through `parents` dictionary
- Group labels for semantic organization
- Provenance information for element positioning
- Content layer management for visibility

Sources: [docling/backend/msword\_backend.py56-67](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L56-L67) [docling/backend/msexcel\_backend.py105-109](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L105-L109)

### Error Handling and Validation

The backends implement robust error handling:

```
```

Sources: [docling/backend/msword\_backend.py81-91](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py#L81-L91) [docling/backend/msexcel\_backend.py112-125](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msexcel_backend.py#L112-L125)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Office Document Backends](#office-document-backends.md)
- [Overview](#overview.md)
- [Microsoft Word Backend](#microsoft-word-backend.md)
- [Core Architecture](#core-architecture.md)
- [Document Element Processing](#document-element-processing.md)
- [List Processing](#list-processing.md)
- [Microsoft Excel Backend](#microsoft-excel-backend.md)
- [Core Architecture](#core-architecture-1.md)
- [Table Detection Algorithm](#table-detection-algorithm.md)
- [Page and Size Management](#page-and-size-management.md)
- [Integration with Document Converter](#integration-with-document-converter.md)
- [Common Features and Patterns](#common-features-and-patterns.md)
- [Declarative Document Processing](#declarative-document-processing.md)
- [Document Structure Creation](#document-structure-creation.md)
- [Error Handling and Validation](#error-handling-and-validation.md)
