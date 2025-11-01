Usage Examples | docling-project/docling | DeepWiki

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

# Usage Examples

Relevant source files

- [README.md](https://github.com/docling-project/docling/blob/f7244a43/README.md)
- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [docs/examples/minimal\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py)
- [docs/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md)
- [docs/usage/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md)
- [docs/usage/mcp.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md)
- [docs/usage/vision\_models.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md)
- [mkdocs.yml](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml)

This page provides comprehensive, practical code examples for using the Docling Python SDK. It demonstrates common usage patterns, configuration options, and integration approaches for the `DocumentConverter` and `DocumentExtractor` classes.

For API reference details, see [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md) and [DocumentExtractor API](docling-project/docling/7.2-documentextractor-api.md). For CLI usage, see [Document Conversion CLI](docling-project/docling/6.1-document-conversion-cli.md).

## Basic Document Conversion

The simplest conversion workflow uses `DocumentConverter` with default settings:

```
```

**Key Components:**

- `DocumentConverter`: Main orchestrator for document conversion [document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L184-L433)
- `ConversionResult`: Container for conversion output, status, and errors [datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L198-L215)
- `DoclingDocument`: Unified document representation from docling-core

The converter automatically detects the input format and selects the appropriate pipeline and backend based on MIME type and file extension [datamodel/document.py280-338](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L280-L338)

**Conversion Flow Diagram:**

```
```

Sources: [document\_converter.py227-245](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L227-L245) [document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L351-L378) [document\_converter.py404-432](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L404-L432)

## Batch Processing

For processing multiple documents efficiently, use `convert_all()` which returns an iterator:

```
```

**Document Limits and Error Handling:**

| Parameter         | Type  | Purpose                                                        |
| ----------------- | ----- | -------------------------------------------------------------- |
| `raises_on_error` | bool  | If True, raises on first error; if False, yields error results |
| `max_num_pages`   | int   | Skip documents exceeding this page count                       |
| `max_file_size`   | int   | Skip documents exceeding this byte size                        |
| `page_range`      | tuple | Specify page range to process (start, end)                     |

The `convert_all()` method supports concurrent processing via `settings.perf.doc_batch_concurrency` for improved throughput [document\_converter.py327-349](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L327-L349)

Sources: [document\_converter.py247-283](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L247-L283) [datamodel/settings.py](https://github.com/docling-project/docling/blob/f7244a43/datamodel/settings.py) [datamodel/document.py104-191](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L104-L191)

## Customizing Pipeline Options

### PDF Pipeline Configuration

Customize PDF processing with `PdfPipelineOptions`:

```
```

**Pipeline Options Hierarchy:**

```
```

Sources: [datamodel/pipeline\_options.py273-363](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L273-L363) [datamodel/pipeline\_options.py334-363](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L334-L363)

### OCR Configuration

Configure OCR engines and languages:

```
```

**OCR Engine Selection:**

| Engine    | Class                 | Best For                     | Platform   |
| --------- | --------------------- | ---------------------------- | ---------- |
| Auto      | `OcrAutoOptions`      | Automatic fallback selection | All        |
| RapidOCR  | `RapidOcrOptions`     | Fast, multilingual, ONNX     | All        |
| Tesseract | `TesseractOcrOptions` | Accurate, widely supported   | All        |
| EasyOCR   | `EasyOcrOptions`      | Deep learning, 80+ languages | All        |
| OcrMac    | `OcrMacOptions`       | Native macOS OCR             | macOS only |

The `OcrAutoModel` automatically selects the best available engine in this order: OcrMac (Darwin), RapidOCR (ONNX), EasyOCR, RapidOCR (Torch), Tesseract [models/ocr/ocr\_auto\_model.py](https://github.com/docling-project/docling/blob/f7244a43/models/ocr/ocr_auto_model.py)

Sources: [datamodel/pipeline\_options.py74-198](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L74-L198) [cli/main.py599-611](https://github.com/docling-project/docling/blob/f7244a43/cli/main.py#L599-L611)

### Enrichment Models

Enable content enrichment for code, formulas, and figures:

```
```

Enrichment models run after document assembly on individual items, not pages [pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/pipeline/base_pipeline.py)

Sources: [datamodel/pipeline\_options.py201-245](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L201-L245) [datamodel/pipeline\_options.py283-298](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L283-L298)

## Using Vision Language Models

### Local VLM Processing

Use vision-language models for end-to-end document understanding:

```
```

### VLM Model Selection

**Available Models:**

| Model Spec Constant           | Model ID                                  | Framework    | Device       | Output Format |
| ----------------------------- | ----------------------------------------- | ------------ | ------------ | ------------- |
| `GRANITEDOCLING_TRANSFORMERS` | ibm-granite/granite-docling-258M          | Transformers | CPU/CUDA/MPS | DocTags       |
| `GRANITEDOCLING_MLX`          | ibm-granite/granite-docling-258M-mlx-bf16 | MLX          | MPS          | DocTags       |
| `SMOLDOCLING_TRANSFORMERS`    | ds4sd/SmolDocling-256M-preview            | Transformers | CPU/CUDA/MPS | DocTags       |
| `SMOLDOCLING_MLX`             | ds4sd/SmolDocling-256M-preview-mlx-bf16   | MLX          | MPS          | DocTags       |
| `GRANITE_VISION_TRANSFORMERS` | ibm-granite/granite-vision-3.2-2b         | Transformers | CPU/CUDA/MPS | Markdown      |
| `GOT2_TRANSFORMERS`           | ucaslcl/GOT-OCR2\_0                       | Transformers | CPU/CUDA     | HTML          |

For Apple Silicon, MLX models provide significantly faster inference (\~17x faster than Transformers) [docs/usage/vision\_models.md46-58](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L46-L58)

```
```

**VLM Pipeline Flow:**

```
```

Sources: [docs/examples/minimal\_vlm\_pipeline.py1-71](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py#L1-L71) [datamodel/vlm\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/datamodel/vlm_model_specs.py) [docs/usage/vision\_models.md1-124](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L1-L124)

### Remote VLM via API

Connect to VLM services via OpenAI-compatible API:

```
```

The API client sends page images as base64-encoded content and parses the response [models/vlm/api\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/models/vlm/api_vlm_model.py)

Sources: [datamodel/pipeline\_options\_vlm\_model.py29-69](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options_vlm_model.py#L29-L69) [docs/usage/vision\_models.md116-124](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L116-L124)

### Custom VLM Configuration

Define custom VLM models:

```
```

Sources: [docs/usage/vision\_models.md88-113](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L88-L113) [datamodel/pipeline\_options\_vlm\_model.py71-167](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options_vlm_model.py#L71-L167)

## Backend Selection

### PDF Backend Options

Choose between different PDF backends for varying performance and compatibility:

```
```

**Backend Comparison:**

| Backend                       | Text Extraction                   | Coordinate System | Layout Postprocessing |
| ----------------------------- | --------------------------------- | ----------------- | --------------------- |
| DoclingParseV4DocumentBackend | docling-parse (chars/words/lines) | Native            | Yes                   |
| DoclingParseV2DocumentBackend | docling-parse (sanitized)         | Native            | Yes                   |
| DoclingParseDocumentBackend   | docling-parse (legacy)            | Native            | No                    |
| PyPdfiumDocumentBackend       | pypdfium2 only                    | Custom transform  | No                    |

DoclingParseV4Backend is recommended for best quality and performance [backend/docling\_parse\_v4\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/backend/docling_parse_v4_backend.py)

Sources: [cli/main.py645-655](https://github.com/docling-project/docling/blob/f7244a43/cli/main.py#L645-L655) [document\_converter.py132-181](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L132-L181)

### Office and Specialized Formats

Docling automatically selects appropriate backends for different formats:

```
```

**Format-Specific Backends:**

| Input Format | Backend Class                                  | Library Used  |
| ------------ | ---------------------------------------------- | ------------- |
| DOCX         | `MsWordDocumentBackend`                        | python-docx   |
| XLSX         | `MsExcelDocumentBackend`                       | openpyxl      |
| PPTX         | `MsPowerpointDocumentBackend`                  | python-pptx   |
| HTML         | `HTMLDocumentBackend`                          | BeautifulSoup |
| MD           | `MarkdownDocumentBackend`                      | marko         |
| XML\_JATS    | `JatsDocumentBackend`                          | xml.etree     |
| XML\_USPTO   | `PatentUsptoDocumentBackend`                   | xml.etree     |
| METS\_GBS    | `MetsGbsDocumentBackend`                       | tarfile + xml |
| CSV          | `CsvDocumentBackend`                           | csv           |
| AUDIO        | `NoOpBackend` (AsrPipeline handles processing) | -             |

Sources: [document\_converter.py72-181](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L72-L181) [cli/main.py678-697](https://github.com/docling-project/docling/blob/f7244a43/cli/main.py#L678-L697)

## Output and Export

### Export Formats

Export `DoclingDocument` to various formats:

```
```

**Image Reference Modes:**

| Mode          | Description                                 | Use Case                     |
| ------------- | ------------------------------------------- | ---------------------------- |
| `EMBEDDED`    | Base64-encoded images in document           | Self-contained output        |
| `REFERENCED`  | Images saved separately, referenced by path | Large documents, web serving |
| `PLACEHOLDER` | Position markers only, no image data        | Text-only workflows          |

Sources: [cli/main.py191-289](https://github.com/docling-project/docling/blob/f7244a43/cli/main.py#L191-L289) [docling\_core exported via datamodel/document.py](<https://github.com/docling-project/docling/blob/f7244a43/docling_core exported via datamodel/document.py>)

### Extracting Tables and Figures

Access structured elements from the document:

```
```

Sources: [docling\_core.types.doc via datamodel/document.py24-32](<https://github.com/docling-project/docling/blob/f7244a43/docling_core.types.doc via datamodel/document.py#L24-L32>)

### Page-by-Page Processing

Access page-level data for progressive processing:

```
```

Sources: [datamodel/base\_models.py269-328](https://github.com/docling-project/docling/blob/f7244a43/datamodel/base_models.py#L269-L328)

## Advanced Configuration

### Accelerator Options

Control device placement and threading:

```
```

**Device Selection:**

| Device | Description                               | Environment Variable  |
| ------ | ----------------------------------------- | --------------------- |
| `AUTO` | Automatic selection based on availability | `DOCLING_DEVICE=auto` |
| `CPU`  | CPU-only processing                       | `DOCLING_DEVICE=cpu`  |
| `CUDA` | NVIDIA GPU acceleration                   | `DOCLING_DEVICE=cuda` |
| `MPS`  | Apple Metal Performance Shaders           | `DOCLING_DEVICE=mps`  |

The `AUTO` device selects: MPS (macOS) > CUDA (if available) > CPU [datamodel/accelerator\_options.py](https://github.com/docling-project/docling/blob/f7244a43/datamodel/accelerator_options.py)

Sources: [datamodel/accelerator\_options.py](https://github.com/docling-project/docling/blob/f7244a43/datamodel/accelerator_options.py) [datamodel/pipeline\_options.py276-281](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L276-L281)

### Document Limits and Timeouts

Enforce processing constraints:

```
```

Sources: [datamodel/settings.py](https://github.com/docling-project/docling/blob/f7244a43/datamodel/settings.py) [document\_converter.py233-244](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L233-L244)

### Pipeline Caching

The converter automatically caches pipeline instances based on `(pipeline_class, options_hash)` to avoid redundant model loading:

```
```

**Pipeline Cache Key:**

```
```

This caching is thread-safe and significantly improves performance when processing multiple documents with identical configurations [document\_converter.py207-217](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L207-L217) [document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L351-L378)

Sources: [document\_converter.py203-210](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L203-L210) [document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L351-L378)

### Performance Tuning

Control batch sizes and concurrency for optimal performance:

```
```

The threaded PDF pipeline uses a stage graph with bounded queues to process pages in parallel across multiple stages (preprocess → OCR → layout → table → assemble) [pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/pipeline/threaded_standard_pdf_pipeline.py)

Sources: [datamodel/settings.py](https://github.com/docling-project/docling/blob/f7244a43/datamodel/settings.py) [datamodel/pipeline\_options.py371-384](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L371-L384)

## Integration Patterns

### Custom Format Options

Create custom format configurations:

```
```

Sources: [document\_converter.py62-70](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L62-L70) [datamodel/base\_models.py36-42](https://github.com/docling-project/docling/blob/f7244a43/datamodel/base_models.py#L36-L42)

### Error Handling and Logging

Implement robust error handling:

```
```

**Error Components:**

| Component Type     | Description                    |
| ------------------ | ------------------------------ |
| `DOCUMENT_BACKEND` | Backend parsing errors         |
| `MODEL`            | AI model inference errors      |
| `DOC_ASSEMBLER`    | Document assembly errors       |
| `USER_INPUT`       | Invalid input or configuration |

Sources: [datamodel/base\_models.py147-157](https://github.com/docling-project/docling/blob/f7244a43/datamodel/base_models.py#L147-L157) [datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L198-L215)

### Working with Streams

Convert documents from in-memory streams:

```
```

Sources: [document\_converter.py285-311](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L285-L311) [datamodel/base\_models.py16](https://github.com/docling-project/docling/blob/f7244a43/datamodel/base_models.py#L16-L16)

### Profiling and Performance Metrics

Access timing information from conversion results:

```
```

**Quality Grades:**

| Grade     | Score Range | Description                |
| --------- | ----------- | -------------------------- |
| EXCELLENT | ≥ 0.9       | High-quality conversion    |
| GOOD      | 0.8 - 0.9   | Good conversion quality    |
| FAIR      | 0.5 - 0.8   | Acceptable but with issues |
| POOR      | < 0.5       | Low quality, review needed |

Sources: [datamodel/document.py206-207](https://github.com/docling-project/docling/blob/f7244a43/datamodel/document.py#L206-L207) [datamodel/base\_models.py366-453](https://github.com/docling-project/docling/blob/f7244a43/datamodel/base_models.py#L366-L453)

## Complete Example: Production Pipeline

Here's a comprehensive example combining multiple features:

```
```

Sources: [document\_converter.py184-433](https://github.com/docling-project/docling/blob/f7244a43/document_converter.py#L184-L433) [datamodel/pipeline\_options.py334-363](https://github.com/docling-project/docling/blob/f7244a43/datamodel/pipeline_options.py#L334-L363) [cli/main.py299-816](https://github.com/docling-project/docling/blob/f7244a43/cli/main.py#L299-L816)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Usage Examples](#usage-examples.md)
- [Basic Document Conversion](#basic-document-conversion.md)
- [Batch Processing](#batch-processing.md)
- [Customizing Pipeline Options](#customizing-pipeline-options.md)
- [PDF Pipeline Configuration](#pdf-pipeline-configuration.md)
- [OCR Configuration](#ocr-configuration.md)
- [Enrichment Models](#enrichment-models.md)
- [Using Vision Language Models](#using-vision-language-models.md)
- [Local VLM Processing](#local-vlm-processing.md)
- [VLM Model Selection](#vlm-model-selection.md)
- [Remote VLM via API](#remote-vlm-via-api.md)
- [Custom VLM Configuration](#custom-vlm-configuration.md)
- [Backend Selection](#backend-selection.md)
- [PDF Backend Options](#pdf-backend-options.md)
- [Office and Specialized Formats](#office-and-specialized-formats.md)
- [Output and Export](#output-and-export.md)
- [Export Formats](#export-formats.md)
- [Extracting Tables and Figures](#extracting-tables-and-figures.md)
- [Page-by-Page Processing](#page-by-page-processing.md)
- [Advanced Configuration](#advanced-configuration.md)
- [Accelerator Options](#accelerator-options.md)
- [Document Limits and Timeouts](#document-limits-and-timeouts.md)
- [Pipeline Caching](#pipeline-caching.md)
- [Performance Tuning](#performance-tuning.md)
- [Integration Patterns](#integration-patterns.md)
- [Custom Format Options](#custom-format-options.md)
- [Error Handling and Logging](#error-handling-and-logging.md)
- [Working with Streams](#working-with-streams.md)
- [Profiling and Performance Metrics](#profiling-and-performance-metrics.md)
- [Complete Example: Production Pipeline](#complete-example-production-pipeline.md)
