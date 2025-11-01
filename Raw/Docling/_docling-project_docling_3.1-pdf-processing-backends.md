PDF Processing Backends | docling-project/docling | DeepWiki

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

# PDF Processing Backends

Relevant source files

- [docling/backend/abstract\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py)
- [docling/backend/docling\_parse\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py)
- [docling/backend/docling\_parse\_v2\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py)
- [docling/backend/docling\_parse\_v4\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py)
- [docling/backend/pypdfium2\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py)
- [docling/models/base\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py)
- [docling/models/code\_formula\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py)
- [docling/models/document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py)
- [docling/models/easyocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py)
- [docling/models/layout\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py)
- [docling/models/page\_assemble\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py)
- [docling/models/page\_preprocessing\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py)
- [docling/models/table\_structure\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py)
- [docling/pipeline/standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py)
- [docling/utils/layout\_postprocessor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/layout_postprocessor.py)
- [docling/utils/locks.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/locks.py)
- [tests/test\_backend\_docling\_parse\_v4.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse_v4.py)
- [tests/test\_document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py)
- [tests/test\_options.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py)

## Purpose and Scope

This page documents the PDF backend implementations in Docling, which are responsible for extracting text, images, and layout information from PDF documents. PDF backends provide the low-level document reading interface that supplies data to the processing pipelines.

For information about how backends are selected and used in the conversion flow, see [Format Detection and Routing](docling-project/docling/2.4-format-detection-and-routing.md). For details on pipeline processing that operates on backend data, see [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md).

## Overview

Docling provides four PDF backend implementations, each with different capabilities and use cases:

| Backend                         | Status              | Text Extraction  | Granularity              | Use Case                                           |
| ------------------------------- | ------------------- | ---------------- | ------------------------ | -------------------------------------------------- |
| `DoclingParseV4DocumentBackend` | **Current default** | docling-parse v4 | Characters, words, lines | High-quality text extraction with fine granularity |
| `DoclingParseV2DocumentBackend` | Stable              | docling-parse v2 | Text lines               | Sanitized format, good for most documents          |
| `DoclingParseDocumentBackend`   | Legacy              | docling-parse v1 | Text lines               | Backward compatibility                             |
| `PyPdfiumDocumentBackend`       | Alternative         | pypdfium2 only   | Text lines (merged)      | Pure pypdfium2, no docling-parse dependency        |

All backends use `pypdfium2` for PDF rendering and page image generation. The DoclingParse variants add sophisticated text extraction capabilities through the `docling-parse` library.

**Sources:** [docling/backend/docling\_parse\_v4\_backend.py1-250](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L1-L250) [docling/backend/docling\_parse\_v2\_backend.py1-277](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L1-L277) [docling/backend/docling\_parse\_backend.py1-238](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py#L1-L238) [docling/backend/pypdfium2\_backend.py1-400](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L1-L400)

## Backend Architecture

```
```

Each backend consists of two classes:

- **Document Backend**: Manages the entire PDF document, handles loading/unloading, and creates page backends
- **Page Backend**: Provides access to individual page data including text cells, images, and rendering

**Sources:** [docling/backend/abstract\_backend.py1-64](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/abstract_backend.py#L1-L64) [docling/backend/docling\_parse\_v4\_backend.py191-250](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L191-L250) [docling/backend/docling\_parse\_v2\_backend.py228-277](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L228-L277)

## DoclingParseV4Backend (Current Default)

`DoclingParseV4DocumentBackend` is the current default backend, providing the highest quality text extraction with character, word, and line-level granularity.

### Key Features

- **Multi-level granularity**: Extracts characters, words, and text lines
- **Lazy parsing**: Page data is parsed on-demand via `_ensure_parsed()` method
- **Configurable extraction**: Options for `create_words`, `create_textlines`, `keep_chars`, `keep_lines`
- **Memory efficient**: Pages can be unloaded individually

### Implementation Details

```
```

The v4 backend uses the modern `docling-parse` API with `DoclingPdfParser` and `PdfDocument` classes. Text extraction happens lazily when `get_text_cells()` or `get_segmented_page()` is called:

[docling/backend/docling\_parse\_v4\_backend.py52-74](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L52-L74)

The `_ensure_parsed()` method retrieves character, word, and line cells from docling-parse, then converts them to top-left coordinate origin:

[docling/backend/docling\_parse\_v4\_backend.py66-74](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L66-L74)

### Usage Example

```
```

**Sources:** [docling/backend/docling\_parse\_v4\_backend.py24-189](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L24-L189) [tests/test\_backend\_docling\_parse\_v4.py18-26](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse_v4.py#L18-L26)

## DoclingParseV2Backend (Sanitized Format)

`DoclingParseV2DocumentBackend` provides a "sanitized" data format with structured arrays, offering a balance between quality and simplicity.

### Data Structure

V2 uses a structured format with separate header and data arrays:

[docling/backend/docling\_parse\_v2\_backend.py60-77](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L60-L77)

The sanitized format includes:

- `dimension`: Page width and height
- `cells`: Header array (field names) + data array (cell values)
- `images`: Bitmap locations

This structure allows efficient access to cell properties like `x0`, `y0`, `x1`, `y1`, `text` without parsing complex nested structures.

### Coordinate Scaling

V2 requires coordinate scaling from parser space to pypdfium2 space:

[docling/backend/docling\_parse\_v2\_backend.py84-92](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L84-L92)

The scaling factors are computed as:

```
scale_x = pypdfium_width / parser_width
scale_y = pypdfium_height / parser_height
```

**Sources:** [docling/backend/docling\_parse\_v2\_backend.py32-226](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L32-L226)

## DoclingParseBackend (Legacy v1)

`DoclingParseDocumentBackend` is the original implementation, maintained for backward compatibility.

### Differences from V2

The v1 backend uses a simpler, less structured format:

[docling/backend/docling\_parse\_backend.py54-67](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py#L54-L67)

Key differences:

- Direct access to `_dpage["cells"]` array without header/data separation
- Uses `content["rnormalized"]` for text content
- Similar coordinate scaling requirements

The v1 parser API is also different:

[docling/backend/docling\_parse\_backend.py207-220](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py#L207-L220)

V1 uses `pdf_parser_v1()` with methods like `load_document()` and `parse_pdf_from_key_on_page()`.

**Sources:** [docling/backend/docling\_parse\_backend.py26-238](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_backend.py#L26-L238)

## PyPdfiumBackend (Pure pypdfium2)

`PyPdfiumDocumentBackend` provides PDF reading without the `docling-parse` dependency, using only `pypdfium2`.

### Cell Extraction and Merging

PyPdfium2 produces highly fragmented text cells (often sub-word level). The backend implements sophisticated cell merging:

```
```

The merging algorithm:

[docling/backend/pypdfium2\_backend.py157-252](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L157-L252)

The algorithm:

1. **Groups rows** based on vertical alignment (top/bottom within 0.5× height threshold)
2. **Merges horizontally** within each row (gap < 1.0× average height)
3. **Re-extracts text** from merged bounding boxes to avoid concatenation errors

### Thread Safety

All pypdfium2 operations are protected by a global lock:

[docling/utils/locks.py1-3](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/locks.py#L1-L3)

This lock is used throughout pypdfium2 operations:

[docling/backend/pypdfium2\_backend.py122-124](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L122-L124) [docling/backend/pypdfium2\_backend.py348-349](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L348-L349)

**Sources:** [docling/backend/pypdfium2\_backend.py101-400](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L101-L400) [docling/utils/locks.py1-3](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/locks.py#L1-L3)

## Coordinate System Transformations

### Origins and Conventions

PDF and Docling use different coordinate systems:

```
```

### Transformation Implementation

All backends convert coordinates from bottom-left (PDF native) to top-left (Docling standard):

[docling/backend/docling\_parse\_v2\_backend.py84-92](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v2_backend.py#L84-L92)

The conversion formula for a bounding box:

```
l_new = l_old * scale_x
r_new = r_old * scale_x
t_new = (parser_height - t_old) * scale_y  # Flip Y-axis
b_new = (parser_height - b_old) * scale_y
```

### Scaling Operations

Backends support scaling for different DPI requirements:

[docling/backend/docling\_parse\_v4\_backend.py171-173](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L171-L173)

Common scaling factors:

- `scale=1.0`: Native 72 DPI
- `scale=1.67`: \~120 DPI (used by CodeFormulaModel)
- `scale=2.0`: 144 DPI (used by TableStructureModel)
- `scale=3.0`: 216 DPI (used by OCR models)

**Sources:** [docling/backend/docling\_parse\_v4\_backend.py135-169](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L135-L169) [docling/backend/pypdfium2\_backend.py327-361](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L327-L361)

## Text Extraction and Cell Processing

### Common Interface

All page backends implement these text extraction methods:

| Method                   | Purpose                      | Return Type                  |
| ------------------------ | ---------------------------- | ---------------------------- |
| `get_text_cells()`       | Get all text cells on page   | `Iterable[TextCell]`         |
| `get_segmented_page()`   | Get structured page data     | `Optional[SegmentedPdfPage]` |
| `get_text_in_rect(bbox)` | Extract text in bounding box | `str`                        |

### Text in Rect Implementation

The `get_text_in_rect()` method finds text cells that overlap with a given bounding box:

[docling/backend/docling\_parse\_v4\_backend.py79-105](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L79-L105)

The algorithm:

1. Iterate through all text cells on the page
2. Convert cell bbox to same coordinate system as query bbox
3. Calculate `intersection_over_self` ratio
4. Include cells with overlap > 0.5 (50% threshold)
5. Concatenate text with spaces

### SegmentedPdfPage Structure

The `SegmentedPdfPage` object contains:

```
```

DoclingParseV4 is the only backend that populates word and character cells.

**Sources:** [docling/backend/docling\_parse\_v4\_backend.py107-115](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L107-L115) [docling/backend/pypdfium2\_backend.py304-322](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L304-L322)

## Image Rendering and Cropping

### Page Image Generation

All backends implement `get_page_image()` with identical signatures:

[docling/backend/docling\_parse\_v4\_backend.py135-169](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L135-L169)

The rendering process:

1. Determine cropbox (defaults to full page)
2. Calculate padbox in bottom-left coordinates for pypdfium2
3. Render at 1.5× the requested scale for sharpness
4. Resize down to the target scale

This technique (render at higher resolution, then downsample) produces sharper images than rendering directly at the target scale.

### Bitmap Detection

The `get_bitmap_rects()` method identifies image regions:

[docling/backend/docling\_parse\_v4\_backend.py117-133](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L117-L133)

V4 uses docling-parse's bitmap resources, while PyPdfium2 uses pypdfium2's object API:

[docling/backend/pypdfium2\_backend.py254-289](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L254-L289)

PyPdfium2 handles page rotation (90°, 180°, 270°) by adjusting bitmap coordinates.

**Sources:** [docling/backend/pypdfium2\_backend.py327-361](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L327-L361) [docling/backend/docling\_parse\_v4\_backend.py135-169](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L135-L169)

## LayoutPostprocessor Integration

### Role in PDF Processing

`LayoutPostprocessor` is used by v2+ backends to refine layout predictions from the `LayoutModel`. While not directly part of the backend classes, it operates on data extracted by backends.

```
```

### Spatial Indexing

LayoutPostprocessor uses R-tree spatial indexing for efficient overlap detection:

[docling/utils/layout\_postprocessor.py50-106](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/layout_postprocessor.py#L50-L106)

Key features:

- 2D R-tree for spatial queries
- Interval trees for 1D overlap checks
- Combined strategy for finding overlap candidates

### Overlap Resolution

The postprocessor resolves overlapping clusters using Union-Find:

[docling/utils/layout\_postprocessor.py488-543](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/layout_postprocessor.py#L488-L543)

Process:

1. Build spatial index of clusters
2. Use UnionFind to group overlapping clusters
3. Select best cluster from each group based on rules
4. Merge cells from removed clusters into the selected cluster

**Sources:** [docling/utils/layout\_postprocessor.py155-256](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/layout_postprocessor.py#L155-L256) [docling/models/layout\_model.py208-212](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L208-L212)

## Thread Safety and Resource Management

### Lock Management

pypdfium2 operations require thread-safe access via a global lock:

[docling/utils/locks.py1-3](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/locks.py#L1-L3)

This lock is applied in all backends that use pypdfium2:

[docling/backend/pypdfium2\_backend.py376-378](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L376-L378)

### Resource Cleanup

All backends implement `unload()` for proper resource cleanup:

[docling/backend/docling\_parse\_v4\_backend.py181-188](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L181-L188)

The cleanup sequence:

1. **Page-level cleanup**: Unload individual pages from docling-parse
2. **Document-level cleanup**: Close pypdfium2 document with lock
3. **Stream cleanup**: Close BytesIO streams if applicable

Proper cleanup prevents memory leaks and file descriptor exhaustion, especially important in multi-threaded or batch processing scenarios.

### Page Caching in V4

DoclingParseV4 implements page-level unloading:

[docling/backend/docling\_parse\_v4\_backend.py181-184](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L181-L184)

This allows selective memory management - frequently accessed pages can remain loaded while others are unloaded to conserve memory.

**Sources:** [docling/backend/docling\_parse\_v4\_backend.py234-249](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L234-L249) [docling/backend/pypdfium2\_backend.py395-399](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pypdfium2_backend.py#L395-L399)

## Backend Selection and Configuration

### Selection via FormatOption

Backends are selected through `PdfFormatOption`:

```
```

### Testing Multiple Backends

The test suite verifies all backends work correctly:

[tests/test\_options.py141-165](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L141-L165)

This ensures API compatibility across all backend implementations.

**Sources:** [tests/test\_options.py141-165](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L141-L165) [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [PDF Processing Backends](#pdf-processing-backends.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Backend Architecture](#backend-architecture.md)
- [DoclingParseV4Backend (Current Default)](#doclingparsev4backend-current-default.md)
- [Key Features](#key-features.md)
- [Implementation Details](#implementation-details.md)
- [Usage Example](#usage-example.md)
- [DoclingParseV2Backend (Sanitized Format)](#doclingparsev2backend-sanitized-format.md)
- [Data Structure](#data-structure.md)
- [Coordinate Scaling](#coordinate-scaling.md)
- [DoclingParseBackend (Legacy v1)](#doclingparsebackend-legacy-v1.md)
- [Differences from V2](#differences-from-v2.md)
- [PyPdfiumBackend (Pure pypdfium2)](#pypdfiumbackend-pure-pypdfium2.md)
- [Cell Extraction and Merging](#cell-extraction-and-merging.md)
- [Thread Safety](#thread-safety.md)
- [Coordinate System Transformations](#coordinate-system-transformations.md)
- [Origins and Conventions](#origins-and-conventions.md)
- [Transformation Implementation](#transformation-implementation.md)
- [Scaling Operations](#scaling-operations.md)
- [Text Extraction and Cell Processing](#text-extraction-and-cell-processing.md)
- [Common Interface](#common-interface.md)
- [Text in Rect Implementation](#text-in-rect-implementation.md)
- [SegmentedPdfPage Structure](#segmentedpdfpage-structure.md)
- [Image Rendering and Cropping](#image-rendering-and-cropping.md)
- [Page Image Generation](#page-image-generation.md)
- [Bitmap Detection](#bitmap-detection.md)
- [LayoutPostprocessor Integration](#layoutpostprocessor-integration.md)
- [Role in PDF Processing](#role-in-pdf-processing.md)
- [Spatial Indexing](#spatial-indexing.md)
- [Overlap Resolution](#overlap-resolution.md)
- [Thread Safety and Resource Management](#thread-safety-and-resource-management.md)
- [Lock Management](#lock-management.md)
- [Resource Cleanup](#resource-cleanup.md)
- [Page Caching in V4](#page-caching-in-v4.md)
- [Backend Selection and Configuration](#backend-selection-and-configuration.md)
- [Selection via FormatOption](#selection-via-formatoption.md)
- [Testing Multiple Backends](#testing-multiple-backends.md)
