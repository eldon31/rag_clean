Testing Framework | docling-project/docling | DeepWiki

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

# Testing Framework

Relevant source files

- [docling/backend/html\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py)
- [docling/models/tesseract\_ocr\_cli\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_cli_model.py)
- [docling/models/tesseract\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_model.py)
- [tests/data/groundtruth/docling\_v2/example\_06.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_06.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.json)
- [tests/data/groundtruth/docling\_v2/example\_06.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.md)
- [tests/data/groundtruth/docling\_v2/example\_09.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_09.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.json)
- [tests/data/groundtruth/docling\_v2/example\_09.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.md)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.itxt)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.json)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.md)
- [tests/data\_scanned/sample\_with\_rotation\_mismatch.pdf](https://github.com/docling-project/docling/blob/f7244a43/tests/data_scanned/sample_with_rotation_mismatch.pdf)
- [tests/test\_backend\_docling\_parse.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse.py)
- [tests/test\_backend\_docling\_parse\_v2.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse_v2.py)
- [tests/test\_backend\_html.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_html.py)
- [tests/test\_backend\_pdfium.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_pdfium.py)
- [tests/test\_e2e\_ocr\_conversion.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_e2e_ocr_conversion.py)

This document covers Docling's comprehensive testing infrastructure, including verification utilities, ground truth data management, and test patterns for document backends. For information about CI/CD workflows and development processes, see [CI/CD and Development Workflow](docling-project/docling/9.3-cicd-and-development-workflow.md). For details on ground truth data formats and schema evolution, see [Ground Truth Data](docling-project/docling/9.2-ground-truth-data.md).

## Architecture Overview

The testing framework provides systematic verification of document conversion results across multiple formats and backends. It compares conversion outputs against versioned ground truth data using both exact and fuzzy matching techniques.

### Core Testing Flow

```
```

Sources: [tests/verify\_utils.py1-510](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L1-L510) [tests/test\_backend\_msexcel.py1-101](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L1-L101)

### Testing Infrastructure Components

```
```

Sources: [tests/verify\_utils.py1-510](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L1-L510) [tests/test\_backend\_msexcel.py1-101](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L1-L101) [tests/test\_backend\_csv.py1-88](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L1-L88)

## Core Verification Functions

### Text and String Verification

The framework provides sophisticated text comparison with support for fuzzy matching using Levenshtein distance:

```
```

The `verify_text()` function at [tests/verify\_utils.py55-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L55-L62) handles both exact and fuzzy text matching. The Levenshtein distance implementation at [tests/verify\_utils.py31-52](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L52) provides efficient edit distance calculation for OCR-based fuzzy matching.

Sources: [tests/verify\_utils.py31-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L62)

### Document Structure Verification

Document structure verification ensures that converted documents maintain proper hierarchical organization:

| Function                    | Purpose                         | Key Validations                                         |
| --------------------------- | ------------------------------- | ------------------------------------------------------- |
| `verify_docitems()`         | Validates DoclingDocument items | Text content, table structure, picture data, provenance |
| `verify_cells()`            | Validates page cell data        | Cell count, text content, bounding boxes                |
| `verify_table_v2()`         | Validates table structure       | Row/column counts, cell properties, headers             |
| `verify_picture_image_v2()` | Validates image data            | Size, mode, binary content                              |

The `verify_docitems()` function at [tests/verify\_utils.py230-291](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L230-L291) performs comprehensive validation of document items including type checking, provenance verification, and content validation.

Sources: [tests/verify\_utils.py65-96](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L65-L96) [tests/verify\_utils.py170-211](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L170-L211) [tests/verify\_utils.py214-221](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L214-L221) [tests/verify\_utils.py230-291](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L230-L291)

## Ground Truth Data Management

### Versioned Ground Truth System

The framework supports multiple ground truth versions to accommodate schema evolution:

```
```

Ground truth data is organized with precision controls defined by constants:

- `COORD_PREC = 2` for coordinate decimal places
- `CONFID_PREC = 3` for confidence decimal places

Sources: [tests/verify\_utils.py27-28](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L27-L28) [tests/verify\_utils.py302-386](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L302-L386) [tests/verify\_utils.py388-478](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L388-L478)

### Ground Truth Generation and Validation

The framework supports both generation and validation modes controlled by the `generate` parameter:

```
```

The `verify_conversion_result_v2()` function at [tests/verify\_utils.py388-478](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L388-L478) demonstrates this dual-mode operation with comprehensive file handling for all supported export formats.

Sources: [tests/verify\_utils.py421-448](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L421-L448) [tests/verify\_utils.py449-478](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L449-L478) [tests/verify\_utils.py481-495](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L481-L495)

## Test Backend Patterns

### Standard Test Backend Structure

All backend test files follow a consistent pattern for systematic testing:

```
```

Example implementation pattern from Excel backend testing at [tests/test\_backend\_msexcel.py58-73](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L58-L73):

| Step | Function                       | Purpose                                  |
| ---- | ------------------------------ | ---------------------------------------- |
| 1    | `get_excel_paths()`            | Discover `.xlsx` and `.xlsm` files       |
| 2    | `get_converter()`              | Create converter with `InputFormat.XLSX` |
| 3    | `test_e2e_excel_conversions()` | Execute end-to-end validation            |
| 4    | `verify_export()`              | Validate Markdown and indented text      |
| 5    | `verify_document()`            | Validate JSON document structure         |

Sources: [tests/test\_backend\_msexcel.py19-32](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L19-L32) [tests/test\_backend\_msexcel.py58-73](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L58-L73) [tests/test\_backend\_csv.py15-31](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L15-L31)

### Backend-Specific Testing Features

Different backends have specialized testing requirements:

```
```

The Excel backend includes specialized page validation at [tests/test\_backend\_msexcel.py75-100](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L75-L100) that verifies page counts and cell dimensions. The CSV backend at [tests/test\_backend\_csv.py42-50](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L42-L50) demonstrates warning handling for inconsistent column data.

Sources: [tests/test\_backend\_msexcel.py75-100](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msexcel.py#L75-L100) [tests/test\_backend\_csv.py42-50](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L42-L50) [tests/test\_backend\_patent\_uspto.py91-134](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_patent_uspto.py#L91-L134) [tests/test\_backend\_jats.py28-54](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_jats.py#L28-L54)

## Fuzzy Matching and OCR Testing

### Fuzzy Matching Implementation

The framework provides sophisticated fuzzy matching for OCR-based tests where exact text matching is impractical:

```
```

The Levenshtein algorithm at [tests/verify\_utils.py31-52](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L52) uses optimized memory usage by ensuring the shorter string is processed first and uses row buffering for efficient computation.

Default fuzzy threshold is set to 0.4 (40% difference tolerance) at [tests/verify\_utils.py55-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L55-L62) making it suitable for OCR output validation where minor character recognition errors are expected.

Sources: [tests/verify\_utils.py31-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L62) [tests/verify\_utils.py159-161](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L159-L161) [tests/verify\_utils.py190-194](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L190-L194)

### OCR Engine Testing

The framework accommodates different OCR engines through engine-specific suffixes in ground truth filenames:

| OCR Engine | Suffix Pattern | Example                   |
| ---------- | -------------- | ------------------------- |
| Default    | None           | `document.json`           |
| Tesseract  | `.tesseract`   | `document.tesseract.json` |
| EasyOCR    | `.easyocr`     | `document.easyocr.json`   |
| RapidOCR   | `.rapidocr`    | `document.rapidocr.json`  |

Engine-specific ground truth handling is implemented at [tests/verify\_utils.py322-333](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L322-L333) for v1 format and [tests/verify\_utils.py408-419](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L408-L419) for v2 format.

Sources: [tests/verify\_utils.py322-333](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L322-L333) [tests/verify\_utils.py408-419](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L408-L419)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Testing Framework](#testing-framework.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Testing Flow](#core-testing-flow.md)
- [Testing Infrastructure Components](#testing-infrastructure-components.md)
- [Core Verification Functions](#core-verification-functions.md)
- [Text and String Verification](#text-and-string-verification.md)
- [Document Structure Verification](#document-structure-verification.md)
- [Ground Truth Data Management](#ground-truth-data-management.md)
- [Versioned Ground Truth System](#versioned-ground-truth-system.md)
- [Ground Truth Generation and Validation](#ground-truth-generation-and-validation.md)
- [Test Backend Patterns](#test-backend-patterns.md)
- [Standard Test Backend Structure](#standard-test-backend-structure.md)
- [Backend-Specific Testing Features](#backend-specific-testing-features.md)
- [Fuzzy Matching and OCR Testing](#fuzzy-matching-and-ocr-testing.md)
- [Fuzzy Matching Implementation](#fuzzy-matching-implementation.md)
- [OCR Engine Testing](#ocr-engine-testing.md)
