Ground Truth Data | docling-project/docling | DeepWiki

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

# Ground Truth Data

Relevant source files

- [docling/backend/msword\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/msword_backend.py)
- [tests/data/docx/textbox.docx](https://github.com/docling-project/docling/blob/f7244a43/tests/data/docx/textbox.docx)
- [tests/data/docx/unit\_test\_formatting.docx](https://github.com/docling-project/docling/blob/f7244a43/tests/data/docx/unit_test_formatting.docx)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.md)
- [tests/data/groundtruth/docling\_v2/2206.01062.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2206.01062.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.json)
- [tests/data/groundtruth/docling\_v2/2305.03393v1.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2305.03393v1.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2305.03393v1.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2305.03393v1.json)
- [tests/data/groundtruth/docling\_v2/multi\_page.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/multi_page.json)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.doctags.txt)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.md)
- [tests/data/groundtruth/docling\_v2/unit\_test\_formatting.docx.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/unit_test_formatting.docx.itxt)
- [tests/data/groundtruth/docling\_v2/unit\_test\_formatting.docx.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/unit_test_formatting.docx.json)
- [tests/data/groundtruth/docling\_v2/unit\_test\_formatting.docx.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/unit_test_formatting.docx.md)
- [tests/test\_backend\_msword.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msword.py)

This document describes the ground truth data system used in Docling for testing and validation of document conversion results. The ground truth data provides reference outputs for verifying that document processing pipelines produce expected results across different input formats and output representations.

For information about the testing framework that uses this ground truth data, see [Testing Framework](docling-project/docling/9.1-testing-framework.md).

## Purpose and Structure

The ground truth data system serves as the foundation for Docling's test suite, providing expected outputs for document conversion operations. It enables regression testing, accuracy validation, and ensures consistent behavior across different document formats and processing pipelines.

```
```

Sources: [tests/verify\_utils.py1-510](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L1-L510) [tests/data/groundtruth/docling\_v2/](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/) [tests/test\_backend\_csv.py41-68](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L41-L68)

## Directory Organization

The ground truth data follows a structured directory layout that mirrors the test data organization:

```
```

The ground truth files are organized under `tests/data/groundtruth/` with separate subdirectories for different format versions. Each input document has corresponding ground truth files with extensions indicating the output format.

Sources: [tests/verify\_utils.py324-328](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L324-L328) [tests/verify\_utils.py410-414](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L410-L414) [tests/test\_backend\_csv.py41](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L41-L41)

## Ground Truth File Formats

### DoclingDocument JSON Format

The primary ground truth format stores complete `DoclingDocument` objects as JSON files with precise coordinate and confidence precision controlled by `COORD_PREC=2` and `CONFID_PREC=3` constants:

```
```

The JSON format preserves all document structure with the following key sections:

| Property      | Type   | Description                                       |
| ------------- | ------ | ------------------------------------------------- |
| `schema_name` | string | Always "DoclingDocument"                          |
| `version`     | string | Schema version (e.g., "1.7.0")                    |
| `origin`      | object | Source metadata: mimetype, binary\_hash, filename |
| `body`        | object | Root node for main document content               |
| `furniture`   | object | Root node for metadata elements (headers/footers) |
| `texts`       | array  | All TextItem objects with references              |
| `tables`      | array  | All TableItem objects with data grids             |
| `pictures`    | array  | All PictureItem objects with image data           |
| `groups`      | array  | All GroupItem objects (lists, sections)           |

Each element contains:

- `self_ref`: JSON pointer to itself (e.g., `#/texts/0`)
- `parent`: Reference to parent element
- `children`: Array of references to child elements
- `prov`: Array of provenance data with page numbers and bounding boxes
- Content-specific fields (text, label, data, etc.)

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json1-100](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L1-L100) [tests/verify\_utils.py27-28](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L27-L28) [tests/verify\_utils.py438-440](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L438-L440)

### Markdown Export Format

Markdown ground truth files (`.md` extension) contain the exported markdown representation of documents, generated using `DoclingDocument.export_to_markdown()`:

```
```

Key characteristics:

- Section headers use `##` for level 1, `###` for level 2, etc.
- Tables rendered as markdown tables with alignment
- Images marked with `<!-- image -->` comments
- Lists use `-` for unordered, `1.` for ordered
- Preserves text formatting where possible

This format validates the markdown export functionality through `verify_export()` function.

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.md1-50](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.md#L1-L50) [tests/verify\_utils.py294-295](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L294-L295)

### DocTags Format

The DocTags format (`.doctags.txt` extension) provides a structured tag-based representation with precise coordinate information, generated using `DoclingDocument.export_to_document_tokens()`:

```
<doctag><page_header><loc_15><loc_101><loc_30><loc_354>arXiv:2203.01017v2  [cs.CV]  11 Mar 2022</page_header>
<section_header_level_1><loc_79><loc_68><loc_408><loc_76>TableFormer: Table Structure Understanding with Transformers.</section_header_level_1>
<text><loc_116><loc_93><loc_370><loc_108>Ahmed Nassar, Nikolaos Livathinos...</text>
<otsl><loc_258><loc_146><loc_439><loc_191><ched>1<nl></otsl>
<picture><loc_257><loc_143><loc_439><loc_313><caption><loc_252><loc_325>Figure 1: Picture...</caption></picture>
<page_break>
```

DocTags format characteristics:

- Each line contains a complete element with opening and closing tags
- Coordinates use `<loc_X>` format where X is a normalized 0-500 scale
- Four coordinates represent left, top, right, bottom boundaries
- Element types include: `text`, `section_header_level_N`, `table`, `picture`, `page_header`, `page_footer`, `list_item`, `caption`
- Tables use OTSL (Optimized Table Structure Language) notation
- `<page_break>` markers separate pages
- Special tags like `<otsl>`, `<ched>`, `<fcel>`, `<lcel>` for table structure

Coordinate normalization formula:

```
normalized_x = int((x / page_width) * 500)
normalized_y = int((y / page_height) * 500)
```

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.doctags.txt1-20](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.doctags.txt#L1-L20) [tests/verify\_utils.py298-299](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L298-L299)

### Page Data Format

Page-level ground truth (`.pages.json` extension) stored as JSON arrays containing detailed page information from the PDF backend:

```
```

Page data components:

- `page_no`: Zero-based page index
- `size`: Page dimensions in points
- `parsed_page.dimension`: Page coordinate system information
- `parsed_page.char_cells`: Individual character bounding boxes and metadata
- `parsed_page.bitmap_resources`: Embedded images with base64-encoded data

This format captures low-level page parsing results for validation of PDF processing pipelines, particularly useful for testing OCR and layout analysis stages.

Sources: [tests/verify\_utils.py422-435](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L422-L435)

## Verification System

### Core Verification Functions

The verification system provides specialized functions for different types of content validation:

```
```

### Text Verification with Fuzzy Matching

The `verify_text()` function in [tests/verify\_utils.py55-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L55-L62) supports both exact and fuzzy text comparison using Levenshtein distance:

```
```

The Levenshtein distance calculation uses [tests/verify\_utils.py31-52](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L52):

- Computes minimum edit distance between two strings
- Used for fuzzy matching when `fuzzy=True`
- Default threshold of 0.4 (40% difference allowed)
- Useful for OCR output where minor errors are expected

Fuzzy matching is controlled per-test:

- Programmatic content (DOCX, HTML): `fuzzy=False` for exact matching
- OCR content (scanned PDFs): `fuzzy=True` with configurable threshold
- OCR engine parameter passed to determine expectations

Sources: [tests/verify\_utils.py31-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L62)

### Document Structure Validation

The `verify_docitems` function performs comprehensive validation of document structure:

1. **Text Elements**: Validates content, labels, and provenance information
2. **Table Elements**: Checks table structure, cell content, and headers
3. **Picture Elements**: Verifies image data and annotations
4. **Hierarchical Structure**: Ensures parent-child relationships are correct

The function iterates through document elements and validates each component against ground truth expectations.

Sources: [tests/verify\_utils.py230-291](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L230-L291)

### Coordinate Precision Control

The verification system maintains consistent coordinate precision across different formats:

| Constant      | Purpose                        | Value |
| ------------- | ------------------------------ | ----- |
| `COORD_PREC`  | Decimal places for coordinates | 2     |
| `CONFID_PREC` | Decimal places for confidence  | 3     |

These precision settings ensure reproducible ground truth generation and comparison.

Sources: [tests/verify\_utils.py27-28](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L27-L28) [tests/verify\_utils.py425-430](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L425-L430)

## Ground Truth Generation

### Generation Control

Ground truth generation is controlled through the `GEN_TEST_DATA` flag in [tests/test\_data\_gen\_flag.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_data_gen_flag.py) and the `generate` parameter in verification functions:

```
```

The `verify_conversion_result_v2()` function signature at [tests/verify\_utils.py388-396](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L388-L396):

```
```

Parameters:

- `generate`: If True, creates new ground truth files; if False, validates against existing
- `ocr_engine`: Optional OCR engine identifier used in ground truth path
- `fuzzy`: Enable fuzzy text matching for OCR content
- `verify_doctags`: If True, also generate/verify .doctags.txt format
- `indent`: JSON indentation level (default: 2)

Sources: [tests/test\_data\_gen\_flag.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_data_gen_flag.py) [tests/test\_backend\_msword.py16-19](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msword.py#L16-L19) [tests/verify\_utils.py388-396](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L388-L396)

### File Generation Process

The generation process in [tests/verify\_utils.py421-448](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L421-L448) creates multiple output formats for each input document:

```
```

File naming conventions:

- Base path: `tests/data/groundtruth/docling_v2/{input_filename}`
- Suffix pattern: `.{ocr_engine}` if OCR used (e.g., `.easyocr`)
- Extensions: `.json`, `.md`, `.doctags.txt`, `.pages.json`, `.itxt`

Example paths for `2203.01017v2.pdf`:

- `tests/data/groundtruth/docling_v2/2203.01017v2.json`
- `tests/data/groundtruth/docling_v2/2203.01017v2.md`
- `tests/data/groundtruth/docling_v2/2203.01017v2.doctags.txt`
- `tests/data/groundtruth/docling_v2/2203.01017v2.pages.json`

Sources: [tests/verify\_utils.py421-448](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L421-L448) [tests/verify\_utils.py27-28](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L27-L28)

## Test Integration

### Backend Test Integration

Each document backend test integrates with the ground truth system following a consistent pattern demonstrated in [tests/test\_backend\_msword.py84-112](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msword.py#L84-L112):

```
```

This pattern is replicated across backend tests:

- [tests/test\_backend\_csv.py41-68](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L41-L68) for CSV files
- [tests/test\_backend\_pptx.py28-56](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_pptx.py#L28-L56) for PowerPoint files
- [tests/test\_backend\_jats.py28-54](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_jats.py#L28-L54) for JATS XML files
- [tests/test\_backend\_html.py28-55](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_html.py#L28-L55) for HTML files

Common elements:

1. Get list of test files via `get_{format}_paths()`
2. Create converter via `get_converter()`
3. Construct ground truth path using parent.parent navigation
4. Convert document and extract `DoclingDocument`
5. Verify multiple export formats
6. Use `GENERATE` flag for regeneration mode

Sources: [tests/test\_backend\_msword.py84-112](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_msword.py#L84-L112) [tests/test\_backend\_csv.py41-68](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_csv.py#L41-L68)

### Legacy Format Support

The system maintains backward compatibility with legacy ground truth formats:

```
```

This ensures existing test data remains usable during format transitions.

Sources: [tests/verify\_utils.py302-386](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L302-L386)

## Error Handling and Fuzzy Matching

### Fuzzy Comparison Support

The verification system supports fuzzy matching for cases where exact comparison is inappropriate:

- **OCR Results**: Text extraction may have minor variations
- **Coordinate Precision**: Floating-point precision differences
- **Content Variations**: Expected differences in processed content

The fuzzy matching uses configurable thresholds and Levenshtein distance algorithms.

Sources: [tests/verify\_utils.py55-62](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L55-L62) [tests/verify\_utils.py31-52](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L31-L52)

### Table Structure Validation

Table verification includes comprehensive structure checking:

```
```

This ensures table extraction maintains structural integrity and content accuracy.

Sources: [tests/verify\_utils.py170-211](https://github.com/docling-project/docling/blob/f7244a43/tests/verify_utils.py#L170-L211)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Ground Truth Data](#ground-truth-data.md)
- [Purpose and Structure](#purpose-and-structure.md)
- [Directory Organization](#directory-organization.md)
- [Ground Truth File Formats](#ground-truth-file-formats.md)
- [DoclingDocument JSON Format](#doclingdocument-json-format.md)
- [Markdown Export Format](#markdown-export-format.md)
- [DocTags Format](#doctags-format.md)
- [Page Data Format](#page-data-format.md)
- [Verification System](#verification-system.md)
- [Core Verification Functions](#core-verification-functions.md)
- [Text Verification with Fuzzy Matching](#text-verification-with-fuzzy-matching.md)
- [Document Structure Validation](#document-structure-validation.md)
- [Coordinate Precision Control](#coordinate-precision-control.md)
- [Ground Truth Generation](#ground-truth-generation.md)
- [Generation Control](#generation-control.md)
- [File Generation Process](#file-generation-process.md)
- [Test Integration](#test-integration.md)
- [Backend Test Integration](#backend-test-integration.md)
- [Legacy Format Support](#legacy-format-support.md)
- [Error Handling and Fuzzy Matching](#error-handling-and-fuzzy-matching.md)
- [Fuzzy Comparison Support](#fuzzy-comparison-support.md)
- [Table Structure Validation](#table-structure-validation.md)
