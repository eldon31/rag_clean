Configuration and Pipeline Options | docling-project/docling | DeepWiki

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

# Configuration and Pipeline Options

Relevant source files

- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [docling/models/base\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py)
- [docling/models/code\_formula\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py)
- [docling/models/document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py)
- [docling/models/easyocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py)
- [docling/models/layout\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py)
- [docling/models/page\_assemble\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py)
- [docling/models/page\_preprocessing\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py)
- [docling/models/table\_structure\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py)
- [docling/pipeline/standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py)
- [tests/test\_document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py)
- [tests/test\_options.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py)

## Purpose and Scope

This page documents Docling's configuration system, explaining how options are structured, cascaded, and applied throughout the document conversion process. It covers the options hierarchy (`PipelineOptions`, `PdfPipelineOptions`, `VlmPipelineOptions`, etc.), configuration sources (CLI arguments, environment variables, programmatic API), and how options control pipeline behavior and model initialization.

For information about specific pipeline implementations, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md). For details on model configuration and plugin discovery, see [AI/ML Models](docling-project/docling/4-aiml-models.md).

---

## Options Architecture Overview

Docling uses a hierarchical options system built on Pydantic models, providing type safety, validation, and serialization. Options flow from configuration sources (CLI, environment variables, or code) through the `DocumentConverter` to pipelines and finally to individual models.

```
```

**Sources:** [docling/datamodel/pipeline\_options.py1-384](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L1-L384) [docling/document\_converter.py62-181](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L62-L181)

---

## Base Options Classes

### BaseOptions

All options classes inherit from `BaseOptions`, which provides a common `kind` field used for factory-based selection (e.g., OCR engine selection).

```
```

**Sources:** [docling/datamodel/pipeline\_options.py49-52](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L49-L52)

### PipelineOptions

The root options class for all pipelines, defining common configuration applicable to any pipeline:

| Field                    | Type                 | Default                | Description                                               |
| ------------------------ | -------------------- | ---------------------- | --------------------------------------------------------- |
| `document_timeout`       | `Optional[float]`    | `None`                 | Maximum time (seconds) for processing a single document   |
| `accelerator_options`    | `AcceleratorOptions` | `AcceleratorOptions()` | Device and threading configuration                        |
| `enable_remote_services` | `bool`               | `False`                | Allow models that connect to remote APIs (security flag)  |
| `allow_external_plugins` | `bool`               | `False`                | Enable loading third-party plugin modules                 |
| `artifacts_path`         | `Optional[Path]`     | `None`                 | Custom path for model artifacts (overrides default cache) |

**Sources:** [docling/datamodel/pipeline\_options.py273-281](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L273-L281)

### ConvertPipelineOptions

Extends `PipelineOptions` with enrichment capabilities used by `SimplePipeline` and its descendants:

```
```

**Sources:** [docling/datamodel/pipeline\_options.py283-292](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L283-L292)

### PaginatedPipelineOptions

Adds image generation controls for pipelines processing paginated documents:

```
```

**Sources:** [docling/datamodel/pipeline\_options.py294-298](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L294-L298)

---

## Pipeline-Specific Options

### PdfPipelineOptions

The most comprehensive options class, controlling all aspects of PDF processing in `StandardPdfPipeline` and `ThreadedStandardPdfPipeline`:

```
```

**Key fields:**

- **Feature toggles**: `do_table_structure`, `do_ocr`, `do_code_enrichment`, `do_formula_enrichment`, `do_picture_classification`, `do_picture_description`
- **Nested configurations**: `table_structure_options`, `ocr_options`, `layout_options`
- **Image control**: `images_scale`, `generate_page_images`, `generate_picture_images`, `generate_table_images` (deprecated)
- **Text handling**: `force_backend_text` (use PDF's embedded text instead of VLM output)

**Sources:** [docling/datamodel/pipeline\_options.py334-363](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L334-L363)

### VlmPipelineOptions

Configuration for vision-language model-based processing:

```
```

The `vlm_options` field accepts either:

- `InlineVlmOptions`: For local model inference (HuggingFace Transformers, MLX, vLLM)
- `ApiVlmOptions`: For OpenAI-compatible API endpoints (Ollama, vLLM server)

**Sources:** [docling/datamodel/pipeline\_options.py300-309](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L300-L309) [docling/datamodel/pipeline\_options\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py)

### AsrPipelineOptions

Configuration for audio transcription:

```
```

The `asr_options` field specifies the Whisper model variant (TINY, BASE, SMALL, MEDIUM, LARGE, TURBO).

**Sources:** [docling/datamodel/pipeline\_options.py324-326](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L324-L326) [docling/datamodel/pipeline\_options\_asr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_asr_model.py)

### ThreadedPdfPipelineOptions

Extends `PdfPipelineOptions` with batch processing and concurrency controls:

```
```

These control the threaded pipeline's batching and backpressure mechanisms. See [Threaded PDF Pipeline](docling-project/docling/5.2-threaded-pdf-pipeline.md) for details.

**Sources:** [docling/datamodel/pipeline\_options.py371-384](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L371-L384)

---

## Model-Specific Options

### AcceleratorOptions

Controls hardware acceleration and parallelism across all models:

```
```

**Device selection logic:**

1. If `device == AUTO`, `decide_device()` probes available hardware
2. Priority order: CUDA → MPS (macOS) → CPU
3. Some models (e.g., TableStructureModel) override MPS to CPU for performance

**Environment variable precedence:**

- `DOCLING_DEVICE` overrides default but not explicit constructor argument
- `DOCLING_NUM_THREADS` takes precedence over `OMP_NUM_THREADS`
- Constructor arguments always take precedence over environment variables

**Sources:** [docling/datamodel/accelerator\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/accelerator_options.py) [docling/utils/accelerator\_utils.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/accelerator_utils.py) [tests/test\_options.py43-96](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L43-L96)

### OcrOptions Hierarchy

OCR options use a factory pattern with a polymorphic hierarchy:

```
```

**Factory usage pattern:**

```
```

**Key fields:**

- `lang`: Language codes (varies by engine: `["eng", "deu"]` for Tesseract, `["en", "de"]` for EasyOCR)
- `force_full_page_ocr`: Always OCR the entire page, ignoring bitmap detection
- `bitmap_area_threshold`: Minimum page area covered by bitmaps to trigger OCR (default: 0.05 = 5%)

**Sources:** [docling/datamodel/pipeline\_options.py74-199](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L74-L199) [docling/models/factories.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/factories.py) [docling/cli/main.py599-612](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L599-L612)

### TableStructureOptions

Controls the TableFormer model behavior:

```
```

**Mode comparison:**

| Mode       | Speed  | Accuracy | Model Path                             |
| ---------- | ------ | -------- | -------------------------------------- |
| `FAST`     | Higher | Lower    | `model_artifacts/tableformer/fast`     |
| `ACCURATE` | Lower  | Higher   | `model_artifacts/tableformer/accurate` |

When `do_cell_matching=True`, the model matches predicted table cells back to PDF text cells. Setting this to `False` makes the model define cells independently, which can be useful for PDFs with merged cells across columns.

**Sources:** [docling/datamodel/pipeline\_options.py62-72](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L62-L72) [docling/models/table\_structure\_model.py29-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L29-L101)

### LayoutOptions

Configuration for layout analysis:

```
```

**Model specifications available:**

- `DOCLING_LAYOUT_HERON` (default): Balanced performance
- `DOCLING_LAYOUT_EGRET_MEDIUM`, `DOCLING_LAYOUT_EGRET_LARGE`, `DOCLING_LAYOUT_EGRET_XLARGE`: Newer models with varying capacity
- `DOCLING_LAYOUT_V2`: Legacy model

Each `LayoutModelConfig` specifies:

- `repo_id`: HuggingFace repository
- `revision`: Git revision or tag
- `model_repo_folder`: Local folder name
- `model_path`: Path within the repository

**Sources:** [docling/datamodel/pipeline\_options.py311-322](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L311-L322) [docling/datamodel/layout\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/layout_model_specs.py)

### Picture Description Options

Enrichment models for describing images have two option types:

```
```

```
```

Pre-configured options:

- `smolvlm_picture_description`: Uses SmolVLM-256M-Instruct
- `granite_picture_description`: Uses IBM Granite Vision 3.3-2B

**Sources:** [docling/datamodel/pipeline\_options.py201-245](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L201-L245)

---

## Configuration Flow: CLI to Pipeline

The following diagram shows how CLI arguments transform into configured pipelines:

```
```

**Sources:** [docling/cli/main.py299-816](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L299-L816) [docling/document\_converter.py207-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L207-L378)

---

## Environment Variable Configuration

Environment variables provide an alternative to CLI arguments, useful for deployment scenarios:

| Environment Variable  | Type  | Default  | Affects                                     |
| --------------------- | ----- | -------- | ------------------------------------------- |
| `DOCLING_DEVICE`      | `str` | `"auto"` | `AcceleratorOptions.device`                 |
| `OMP_NUM_THREADS`     | `int` | `4`      | `AcceleratorOptions.num_threads` (fallback) |
| `DOCLING_NUM_THREADS` | `int` | `4`      | `AcceleratorOptions.num_threads` (primary)  |

**Precedence rules:**

1. Explicit constructor arguments (highest)
2. Environment variables
3. Default values (lowest)

**Example:**

```
```

**Sources:** [docling/datamodel/accelerator\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/accelerator_options.py) [tests/test\_options.py43-96](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L43-L96)

---

## FormatOption and Pipeline Mapping

The `DocumentConverter` uses `FormatOption` objects to map input formats to processing pipelines:

```
```

**Default format options:** The `_get_default_option()` function provides sensible defaults for all supported formats:

```
```

**Custom configuration example:**

```
```

**Sources:** [docling/document\_converter.py62-181](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L62-L181) [docling/datamodel/base\_models.py36-42](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L36-L42)

---

## Pipeline Caching and Options Hashing

To avoid redundant model loading, `DocumentConverter` caches pipeline instances based on a composite key of `(pipeline_class, options_hash)`:

```
```

**Key implications:**

- **Options must be hashable**: All fields are serialized to compute the hash
- **Options must be comparable**: Identical options produce identical hashes
- **Thread-safe**: Cache access is protected by `_PIPELINE_CACHE_LOCK`
- **Lifecycle**: Cache lives for the lifetime of the `DocumentConverter` instance

**Example scenario:**

```
```

**Sources:** [docling/document\_converter.py207-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L207-L378) [docling/cli/main.py787-790](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L787-L790)

---

## Common Configuration Patterns

### Pattern 1: Minimal OCR-Free PDF Processing

Fast processing without OCR or table extraction:

```
```

**Sources:** [tests/test\_options.py141-165](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L141-L165)

### Pattern 2: High-Accuracy Table Extraction

```
```

**Sources:** [tests/test\_options.py25-40](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L25-L40)

### Pattern 3: GPU-Accelerated Processing

```
```

**Sources:** [tests/test\_options.py43-78](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L43-L78)

### Pattern 4: Code and Formula Enrichment

```
```

**Sources:** [docling/models/code\_formula\_model.py70-116](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L70-L116)

### Pattern 5: Custom OCR Engine

```
```

**Sources:** [docling/cli/main.py599-612](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L599-L612)

### Pattern 6: Picture Classification and Description

```
```

**Sources:** [tests/test\_document\_picture\_classifier.py12-34](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py#L12-L34)

### Pattern 7: Custom Model Artifacts Path

```
```

This overrides the default cache location (`~/.cache/docling`) for model artifacts.

**Sources:** [docling/cli/main.py783-785](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L783-L785) [docling/datamodel/pipeline\_options.py280](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L280-L280)

---

## Options Validation and Type Safety

All options classes use Pydantic for validation:

```
```

**Protected fields:**

- `model_config = ConfigDict(extra="forbid")` prevents typos in field names
- `ClassVar` fields (like `kind`) are not included in serialization
- Optional fields with defaults enable gradual configuration

**Sources:** [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)

---

## Summary

Docling's configuration system provides:

1. **Hierarchical structure**: Base classes provide common fields, specialized classes add domain-specific controls
2. **Type safety**: Pydantic validation catches configuration errors early
3. **Multiple sources**: CLI, environment variables, and programmatic API all map to the same options classes
4. **Factory patterns**: OCR engines and other pluggable components use factories with options
5. **Efficient caching**: Pipeline instances are reused based on options hashing
6. **Sensible defaults**: Every option has a reasonable default value
7. **Extensibility**: New options can be added without breaking existing code

For pipeline-specific behavior, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md). For model initialization details, see [AI/ML Models](docling-project/docling/4-aiml-models.md).

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Configuration and Pipeline Options](#configuration-and-pipeline-options.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Options Architecture Overview](#options-architecture-overview.md)
- [Base Options Classes](#base-options-classes.md)
- [BaseOptions](#baseoptions.md)
- [PipelineOptions](#pipelineoptions.md)
- [ConvertPipelineOptions](#convertpipelineoptions.md)
- [PaginatedPipelineOptions](#paginatedpipelineoptions.md)
- [Pipeline-Specific Options](#pipeline-specific-options.md)
- [PdfPipelineOptions](#pdfpipelineoptions.md)
- [VlmPipelineOptions](#vlmpipelineoptions.md)
- [AsrPipelineOptions](#asrpipelineoptions.md)
- [ThreadedPdfPipelineOptions](#threadedpdfpipelineoptions.md)
- [Model-Specific Options](#model-specific-options.md)
- [AcceleratorOptions](#acceleratoroptions.md)
- [OcrOptions Hierarchy](#ocroptions-hierarchy.md)
- [TableStructureOptions](#tablestructureoptions.md)
- [LayoutOptions](#layoutoptions.md)
- [Picture Description Options](#picture-description-options.md)
- [Configuration Flow: CLI to Pipeline](#configuration-flow-cli-to-pipeline.md)
- [Environment Variable Configuration](#environment-variable-configuration.md)
- [FormatOption and Pipeline Mapping](#formatoption-and-pipeline-mapping.md)
- [Pipeline Caching and Options Hashing](#pipeline-caching-and-options-hashing.md)
- [Common Configuration Patterns](#common-configuration-patterns.md)
- [Pattern 1: Minimal OCR-Free PDF Processing](#pattern-1-minimal-ocr-free-pdf-processing.md)
- [Pattern 2: High-Accuracy Table Extraction](#pattern-2-high-accuracy-table-extraction.md)
- [Pattern 3: GPU-Accelerated Processing](#pattern-3-gpu-accelerated-processing.md)
- [Pattern 4: Code and Formula Enrichment](#pattern-4-code-and-formula-enrichment.md)
- [Pattern 5: Custom OCR Engine](#pattern-5-custom-ocr-engine.md)
- [Pattern 6: Picture Classification and Description](#pattern-6-picture-classification-and-description.md)
- [Pattern 7: Custom Model Artifacts Path](#pattern-7-custom-model-artifacts-path.md)
- [Options Validation and Type Safety](#options-validation-and-type-safety.md)
- [Summary](#summary.md)
