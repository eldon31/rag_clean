Standard PDF Pipeline | docling-project/docling | DeepWiki

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

# Standard PDF Pipeline

Relevant source files

- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/base\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py)
- [docling/models/code\_formula\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py)
- [docling/models/document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py)
- [docling/models/easyocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py)
- [docling/models/layout\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py)
- [docling/models/page\_assemble\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py)
- [docling/models/page\_preprocessing\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py)
- [docling/models/table\_structure\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)
- [tests/test\_document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py)
- [tests/test\_options.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py)

## Purpose and Scope

The `StandardPdfPipeline` implements a sequential, single-threaded processing pipeline for PDF documents that orchestrates five specialized model stages to extract and structure document content. This pipeline processes pages one batch at a time, applying OCR, layout analysis, table structure detection, and assembly operations in sequence.

For multi-threaded parallel processing with improved performance, see [Threaded PDF Pipeline](docling-project/docling/5.2-threaded-pdf-pipeline.md). For end-to-end vision-language model processing, see [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md). For the base pipeline architecture and three-phase execution model, see [Base Pipeline Architecture](docling-project/docling/5.6-base-pipeline-architecture.md).

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py1-243](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L1-L243)

---

## Pipeline Architecture

### Class Hierarchy

The `StandardPdfPipeline` inherits from `PaginatedPipeline`, which provides page-by-page iteration and backend management:

```
```

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py34-35](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L34-L35) [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133) [docling/pipeline/base\_pipeline.py184-320](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L184-L320)

### Pipeline Components

The pipeline initializes two model sequences during construction:

```
```

The `build_pipe` processes pages sequentially through five stages ([standard\_pdf\_pipeline.py51-75](https://github.com/docling-project/docling/blob/f7244a43/standard_pdf_pipeline.py#L51-L75)), while the `enrichment_pipe` operates on individual document items after assembly ([standard\_pdf\_pipeline.py77-90](https://github.com/docling-project/docling/blob/f7244a43/standard_pdf_pipeline.py#L77-L90)).

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py51-90](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L51-L90) [docling/pipeline/base\_pipeline.py135-177](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L135-L177)

---

## Five-Stage Processing

The `build_pipe` sequence implements a fixed order of operations. Each model receives an `Iterable[Page]` and must yield the same pages after processing.

### Stage 1: Page Preprocessing

**Class:** `PagePreprocessingModel`\
**Location:** [docling/models/page\_preprocessing\_model.py25-146](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py#L25-L146)

Responsibilities:

- Generate page images at requested scales (`page.get_image(scale)`)
- Extract text cells from PDF backend (`page._backend.get_segmented_page()`)
- Calculate parse quality scores using text heuristics
- Store results in `page.parsed_page` and `page._image_cache`

The preprocessing model populates page images at multiple scales and extracts programmatic text cells from the backend:

```
```

Configuration via `PagePreprocessingOptions`:

- `images_scale`: Output image resolution multiplier
- `skip_cell_extraction`: Skip cell parsing for VLM-only workflows

**Sources:** [docling/models/page\_preprocessing\_model.py37-118](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py#L37-L118) [docling/pipeline/standard\_pdf\_pipeline.py53-57](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L53-L57)

### Stage 2: OCR (Optical Character Recognition)

**Class:** `BaseOcrModel` (abstract)\
**Implementations:** `RapidOcrModel`, `EasyOcrModel`, `TesseractOcrModel`, `OcrAutoModel`\
**Location:** [docling/models/base\_ocr\_model.py24-228](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L24-L228)

Responsibilities:

- Detect bitmap-heavy regions using `get_ocr_rects()` ([base\_ocr\_model.py40-112](https://github.com/docling-project/docling/blob/f7244a43/base_ocr_model.py#L40-L112))
- Run OCR engine on high-resolution crops of bitmap areas
- Filter OCR results to avoid duplicating programmatic text
- Append new `TextCell` objects to `page.parsed_page.textline_cells`

OCR processing workflow:

```
```

The OCR model factory selects the appropriate implementation based on `OcrOptions`:

| Option Type           | Model Class         | Engine                         |
| --------------------- | ------------------- | ------------------------------ |
| `OcrAutoOptions`      | `OcrAutoModel`      | Auto-selects based on platform |
| `RapidOcrOptions`     | `RapidOcrModel`     | ONNX or PyTorch backend        |
| `EasyOcrOptions`      | `EasyOcrModel`      | Deep learning OCR              |
| `TesseractOcrOptions` | `TesseractOcrModel` | Tesseract binding or CLI       |

**Sources:** [docling/models/base\_ocr\_model.py40-217](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L40-L217) [docling/pipeline/standard\_pdf\_pipeline.py49-59](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L49-L59) [docling/models/easyocr\_model.py28-201](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py#L28-L201)

### Stage 3: Layout Analysis

**Class:** `LayoutModel`\
**Model:** Heron (DocLayoutModel for legacy)\
**Location:** [docling/models/layout\_model.py28-238](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L28-L238)

Responsibilities:

- Predict bounding boxes and labels for document elements
- Apply `LayoutPostprocessor` to resolve overlaps and refine clusters
- Assign confidence scores to predictions
- Store results in `page.predictions.layout` as `LayoutPrediction`

The layout model identifies document structure using computer vision:

```
```

Detected element labels (from `DocItemLabel`):

- **Text elements**: `TEXT`, `SECTION_HEADER`, `LIST_ITEM`, `CODE`, `FORMULA`, `CAPTION`, `FOOTNOTE`
- **Page decorations**: `PAGE_HEADER`, `PAGE_FOOTER`
- **Figures**: `PICTURE`
- **Tables**: `TABLE`, `DOCUMENT_INDEX`
- **Containers**: `FORM`, `KEY_VALUE_REGION`

Each cluster contains matched cells from earlier stages, enabling text extraction per element.

**Sources:** [docling/models/layout\_model.py148-237](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L148-L237) [docling/pipeline/standard\_pdf\_pipeline.py60-65](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L60-L65)

### Stage 4: Table Structure Detection

**Class:** `TableStructureModel`\
**Model:** TableFormer (FAST or ACCURATE mode)\
**Location:** [docling/models/table\_structure\_model.py29-305](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L29-L305)

Responsibilities:

- Extract table structure for clusters labeled `TABLE` or `DOCUMENT_INDEX`
- Run TableFormer model on table crops at 144 DPI (2x scale)
- Parse OTSL sequences and cell coordinates
- Match cells to table grid using word-level tokens when available
- Store results in `page.predictions.tablestructure.table_map`

Table processing workflow:

```
```

The model supports two modes via `TableFormerMode`:

- **FAST**: Faster inference, lower accuracy
- **ACCURATE**: Slower inference, higher accuracy

Cell matching can be toggled via `do_cell_matching` option:

- `True`: Match predicted cells to source tokens (default)
- `False`: Extract text directly from predicted bounding boxes

**Sources:** [docling/models/table\_structure\_model.py170-304](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L170-L304) [docling/pipeline/standard\_pdf\_pipeline.py66-72](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L66-L72)

### Stage 5: Page Assembly

**Class:** `PageAssembleModel`\
**Location:** [docling/models/page\_assemble\_model.py30-157](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py#L30-L157)

Responsibilities:

- Convert layout clusters into typed `PageElement` objects
- Assemble text from cells within each cluster
- Handle text sanitization (dehyphenation, Unicode normalization)
- Populate `page.assembled` with categorized elements (body, headers)

Assembly creates structured elements:

```
```

Element types created:

- `TextElement`: Text blocks, headers, captions, formulas, code
- `Table`: Tables with structure (OTSL, cells, grid dimensions)
- `FigureElement`: Images and diagrams
- `ContainerElement`: Forms and key-value regions

**Sources:** [docling/models/page\_assemble\_model.py67-156](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py#L67-L156) [docling/pipeline/standard\_pdf\_pipeline.py73-75](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L73-L75)

---

## Model Integration

### Pipeline Construction

The `StandardPdfPipeline.__init__()` method initializes models with shared configuration:

```
```

Configuration flow:

```
```

All models receive `AcceleratorOptions` to control device placement (CPU/CUDA/MPS) and thread counts.

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py35-90](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L35-L90) [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)

### OCR Model Selection

The OCR model is created via factory pattern:

```
```

The factory uses `OcrOptions.kind` to select the implementation. `OcrAutoModel` provides platform-specific fallbacks.

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py115-124](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L115-L124) [docling/models/factories.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/factories.py)

### Artifact Management

Models download artifacts from HuggingFace if `artifacts_path` is not provided:

```
```

Artifacts are cached at `settings.cache_dir / "models"` by default. The pipeline passes `self.artifacts_path` to all models, which is resolved from `PipelineOptions.artifacts_path` or environment variable.

**Sources:** [docling/pipeline/base\_pipeline.py50-60](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L50-L60) [docling/models/table\_structure\_model.py92-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L92-L101) [docling/models/layout\_model.py90-102](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L90-L102)

---

## Document Assembly

### Cross-Page Aggregation

After all pages complete the build pipeline, `_assemble_document()` aggregates results:

```
```

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py134-234](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L134-L234)

### Reading Order Construction

The `ReadingOrderModel` constructs the final `DoclingDocument` hierarchy from assembled elements. It applies heuristics to determine document structure (sections, lists, hierarchical nesting).

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py153](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L153-L153) [docling/models/readingorder\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/readingorder_model.py)

### Image Generation

The pipeline can generate embedded images for visualization:

| Option                    | Target                   | Scale          |
| ------------------------- | ------------------------ | -------------- |
| `generate_page_images`    | Full page images         | `images_scale` |
| `generate_picture_images` | Cropped picture elements | `images_scale` |
| `generate_table_images`   | Cropped table elements   | `images_scale` |

Images are cropped from `page.image` using element provenance bounding boxes:

```
```

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py156-203](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L156-L203)

### Confidence Scoring

The pipeline aggregates confidence metrics from page-level predictions:

```
```

- `layout_score`: Mean confidence from layout model predictions
- `parse_score`: 10th percentile of text quality scores (emphasizes problems)
- `table_score`: Mean table structure confidence
- `ocr_score`: Mean OCR confidence (only for OCR'd cells)

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py204-232](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L204-L232)

---

## Configuration and Options

### PdfPipelineOptions

The `PdfPipelineOptions` class (inherits from `PaginatedPipelineOptions`) controls all aspects of the pipeline:

```
```

**Sources:** [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py) [docling/pipeline/standard\_pdf\_pipeline.py35-38](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L35-L38)

### Usage Example

```
```

**Sources:** [tests/test\_options.py98-105](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L98-L105) [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)

---

## Comparison with Other Pipelines

### StandardPdfPipeline vs ThreadedStandardPdfPipeline

| Aspect          | StandardPdfPipeline              | ThreadedStandardPdfPipeline                 |
| --------------- | -------------------------------- | ------------------------------------------- |
| **Processing**  | Sequential (one batch at a time) | Parallel (pipeline stages run concurrently) |
| **Threading**   | Single-threaded                  | Multi-threaded with `ThreadedQueue` buffers |
| **Performance** | Simpler, predictable timing      | Higher throughput for multi-page documents  |
| **Memory**      | Lower peak memory                | Higher due to queues and concurrent pages   |
| **Debugging**   | Easier to debug                  | More complex due to concurrency             |
| **Use case**    | Small documents, debugging       | Production, large documents                 |

The threaded variant ([threaded\_standard\_pdf\_pipeline.py296-648](https://github.com/docling-project/docling/blob/f7244a43/threaded_standard_pdf_pipeline.py#L296-L648)) maintains the same five-stage model sequence but wraps each in a `ThreadedPipelineStage` with worker threads and bounded queues.

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py34](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L34-L34) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296-648](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L648)

### StandardPdfPipeline vs VlmPipeline

| Aspect       | StandardPdfPipeline                       | VlmPipeline                       |
| ------------ | ----------------------------------------- | --------------------------------- |
| **Approach** | Multi-model stages (OCR + layout + table) | End-to-end vision-language model  |
| **Models**   | Heron, TableFormer, OCR engine            | GraniteDocling, SmolDocling, etc. |
| **Output**   | Rich `DoclingDocument` with structure     | DOCTAGS, Markdown, or HTML        |
| **Accuracy** | High for structured documents             | Best for complex visual layouts   |
| **Speed**    | Moderate (5 stages)                       | Varies by VLM model size          |
| **Requires** | PDF backend with text                     | Only images                       |

VLM pipeline ([vlm\_pipeline.py50-389](https://github.com/docling-project/docling/blob/f7244a43/vlm_pipeline.py#L50-L389)) bypasses traditional document understanding models in favor of large vision-language models that directly generate structured output.

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py34](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L34-L34) [docling/pipeline/vlm\_pipeline.py50-389](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L389)

### Backend Support

The `StandardPdfPipeline` requires a `PdfDocumentBackend`:

```
```

Supported backends:

- `DoclingParseV4DocumentBackend` (default) - Character/word/line granularity
- `DoclingParseV2DocumentBackend` - Sanitized format
- `DoclingParseDocumentBackend` (legacy) - v1 format
- `PyPdfiumDocumentBackend` - Pure pypdfium2

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py240-243](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L240-L243) [docling/backend/pdf\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/pdf_backend.py)

---

## Processing Flow Summary

The complete end-to-end flow for a single document:

```
```

**Sources:** [docling/pipeline/base\_pipeline.py197-283](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L197-L283) [docling/pipeline/standard\_pdf\_pipeline.py126-234](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L126-L234) [docling/pipeline/base\_pipeline.py93-115](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L93-L115)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Standard PDF Pipeline](#standard-pdf-pipeline.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Pipeline Architecture](#pipeline-architecture.md)
- [Class Hierarchy](#class-hierarchy.md)
- [Pipeline Components](#pipeline-components.md)
- [Five-Stage Processing](#five-stage-processing.md)
- [Stage 1: Page Preprocessing](#stage-1-page-preprocessing.md)
- [Stage 2: OCR (Optical Character Recognition)](#stage-2-ocr-optical-character-recognition.md)
- [Stage 3: Layout Analysis](#stage-3-layout-analysis.md)
- [Stage 4: Table Structure Detection](#stage-4-table-structure-detection.md)
- [Stage 5: Page Assembly](#stage-5-page-assembly.md)
- [Model Integration](#model-integration.md)
- [Pipeline Construction](#pipeline-construction.md)
- [OCR Model Selection](#ocr-model-selection.md)
- [Artifact Management](#artifact-management.md)
- [Document Assembly](#document-assembly.md)
- [Cross-Page Aggregation](#cross-page-aggregation.md)
- [Reading Order Construction](#reading-order-construction.md)
- [Image Generation](#image-generation.md)
- [Confidence Scoring](#confidence-scoring.md)
- [Configuration and Options](#configuration-and-options.md)
- [PdfPipelineOptions](#pdfpipelineoptions.md)
- [Usage Example](#usage-example.md)
- [Comparison with Other Pipelines](#comparison-with-other-pipelines.md)
- [StandardPdfPipeline vs ThreadedStandardPdfPipeline](#standardpdfpipeline-vs-threadedstandardpdfpipeline.md)
- [StandardPdfPipeline vs VlmPipeline](#standardpdfpipeline-vs-vlmpipeline.md)
- [Backend Support](#backend-support.md)
- [Processing Flow Summary](#processing-flow-summary.md)
