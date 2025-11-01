Extraction Pipeline | docling-project/docling | DeepWiki

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

# Extraction Pipeline

Relevant source files

- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/datamodel/pipeline\_options\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py)
- [docling/datamodel/vlm\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/api\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py)
- [docling/models/base\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py)
- [docling/models/utils/hf\_model\_download.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/utils/hf_model_download.py)
- [docling/models/vlm\_models\_inline/hf\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py)
- [docling/models/vlm\_models\_inline/mlx\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/models/vlm\_models\_inline/vllm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)

The Extraction Pipeline provides schema-based structured data extraction from documents using Vision-Language Models. Unlike the VlmPipeline (see [5.3](docling-project/docling/5.3-vlm-pipeline.md)) which performs full document conversion, `ExtractionVlmPipeline` focuses on extracting specific fields defined by user-provided templates, returning JSON-structured data rather than a complete `DoclingDocument`.

This pipeline is currently experimental and supports PDF and image formats only. It uses the NuExtract model, which is specifically designed for structured information extraction from visual documents.

**Related pages**: For full document conversion with VLM models, see [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md). For general pipeline architecture, see [Base Pipeline Architecture](docling-project/docling/5.6-base-pipeline-architecture.md). For the public API, see [DocumentExtractor API](docling-project/docling/7.2-documentextractor-api.md).

## Architecture Overview

The extraction system consists of three main layers: the API layer (`DocumentExtractor`), the pipeline layer (`ExtractionVlmPipeline`), and the model layer (`NuExtractTransformersModel`).

```
```

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py32-46](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L46) [docling/document\_extractor.py88-119](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L119) [docling/pipeline/base\_extraction\_pipeline.py15-30](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L15-L30)

### Class Hierarchy

```
```

**Sources**: [docling/pipeline/base\_extraction\_pipeline.py15-72](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L15-L72) [docling/pipeline/extraction\_vlm\_pipeline.py32-198](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L198) [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py107-160](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L107-L160)

## Pipeline Initialization

`ExtractionVlmPipeline` is initialized with `VlmExtractionPipelineOptions` and creates a `NuExtractTransformersModel` instance. Unlike conversion pipelines, extraction pipelines do not build document structure—they only extract data.

### Configuration

```
```

**Sources**: [docling/datamodel/vlm\_model\_specs.py288-302](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L288-L302) [docling/pipeline/extraction\_vlm\_pipeline.py33-46](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L33-L46)

The default configuration uses the `numind/NuExtract-2.0-2B` model with the following settings:

| Parameter             | Default Value             | Description                    |
| --------------------- | ------------------------- | ------------------------------ |
| `repo_id`             | `numind/NuExtract-2.0-2B` | Hugging Face model identifier  |
| `torch_dtype`         | `bfloat16`                | Model precision                |
| `inference_framework` | `TRANSFORMERS`            | Uses Hugging Face Transformers |
| `response_format`     | `PLAINTEXT`               | Returns JSON as plain text     |
| `scale`               | `2.0`                     | Image scaling factor           |
| `temperature`         | `0.0`                     | Deterministic generation       |
| `max_new_tokens`      | `4096`                    | Maximum response length        |

**Sources**: [docling/datamodel/vlm\_model\_specs.py288-302](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L288-L302) [docling/datamodel/pipeline\_options\_vlm\_model.py54-85](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L54-L85)

## Extraction Process Flow

The extraction process follows a three-phase pattern: image loading, template serialization, and VLM inference.

```
```

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py48-126](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L48-L126) [docling/document\_extractor.py239-289](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L239-L289) [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py161-290](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L161-L290)

### Image Extraction from Backend

The pipeline extracts images from the document backend, respecting page range limits:

```
```

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py135-171](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L135-L171)

The method follows the same page range filtering logic as `PaginatedPipeline`, processing only pages within `[start_page-1, end_page-1]` (0-indexed). This ensures consistent behavior across all pipelines.

## Template Serialization

The extraction pipeline supports multiple template formats and converts them to JSON strings for the NuExtract model.

### Supported Template Types

| Template Type          | Description             | Example                         |
| ---------------------- | ----------------------- | ------------------------------- |
| `str`                  | Direct JSON or text     | `'{"name": "", "date": ""}'`    |
| `dict`                 | Python dictionary       | `{"name": "", "date": ""}`      |
| `BaseModel` (instance) | Pydantic model instance | `Invoice(customer="", total=0)` |
| `Type[BaseModel]`      | Pydantic model class    | `Invoice` (class itself)        |

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py173-193](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L173-L193) [docling/datamodel/extraction.py38-39](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py#L38-L39)

### Serialization Process

```
```

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py173-193](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L173-L193)

When a Pydantic class (not instance) is provided, the pipeline uses `polyfactory.ModelFactory` to generate an example instance with:

- `__use_examples__=True`: Prefers `Field(examples=...)` values when present
- `__use_defaults__=True`: Uses field defaults instead of random values

This allows users to define extraction schemas as Pydantic classes with example values that guide the VLM's output structure.

**Example**:

```
```

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py182-191](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L182-L191)

## NuExtract Model Integration

The `NuExtractTransformersModel` implements the NuExtract-specific input format and inference logic.

### Model Architecture

```
```

**Sources**: [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py107-160](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L107-L160) [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py161-290](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L161-L290)

### NuExtract Input Format

NuExtract requires a specific input structure that differs from standard VLM prompts:

```
```

**Sources**: [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py207-249](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L207-L249)

The key differences:

1. **Document wrapper**: Images are wrapped in `{type: "image", image: PIL}` format
2. **Template parameter**: The schema is passed as a `template` parameter to `apply_chat_template`, not as part of the prompt
3. **Vision processing**: Uses `process_all_vision_info` from `qwen-vl-utils` to extract images from the message structure

### Batch Processing

```
```

**Sources**: [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py161-290](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L161-L290)

## Output Structure

The extraction pipeline produces `ExtractionResult` objects containing per-page extracted data.

### Data Models

```
```

**Sources**: [docling/datamodel/extraction.py1-40](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py#L1-L40)

### Extraction Result Processing

The pipeline attempts to parse the VLM response as JSON. If parsing fails, the raw text is still preserved:

```
```

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py82-107](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L82-L107)

### Status Determination

The pipeline sets the final status based on page-level errors:

| Condition                          | Status    |
| ---------------------------------- | --------- |
| All pages extracted without errors | `SUCCESS` |
| At least one page has errors       | `FAILURE` |
| No pages processed                 | `FAILURE` |

**Sources**: [docling/pipeline/extraction\_vlm\_pipeline.py128-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L128-L133)

This differs from conversion pipelines which can have `PARTIAL_SUCCESS` status. Extraction is more binary: either data is extracted cleanly or it fails.

## Comparison with VlmPipeline

The extraction and conversion pipelines serve different purposes and have distinct architectures:

```
```

**Key Differences**:

| Aspect               | VlmPipeline                             | ExtractionVlmPipeline             |
| -------------------- | --------------------------------------- | --------------------------------- |
| **Base class**       | `PaginatedPipeline` → `ConvertPipeline` | `BaseExtractionPipeline`          |
| **Purpose**          | Full document conversion                | Schema-based data extraction      |
| **Input**            | Document only                           | Document + template               |
| **VLM model**        | GraniteDocling, SmolDocling, etc.       | NuExtract-2.0                     |
| **Response format**  | DOCTAGS, Markdown, HTML                 | JSON (plain text)                 |
| **Output**           | `DoclingDocument` with full structure   | `ExtractionResult` with JSON data |
| **Phases**           | build → assemble → enrich               | extract only                      |
| **Template support** | No                                      | Yes (str/dict/Pydantic)           |

**Sources**: [docling/pipeline/vlm\_pipeline.py50-113](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L113) [docling/pipeline/extraction\_vlm\_pipeline.py32-46](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L46) [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133) [docling/pipeline/base\_extraction\_pipeline.py15-72](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L15-L72)

## Usage Patterns

The extraction pipeline is accessed through the `DocumentExtractor` API, which mirrors the `DocumentConverter` API but targets extraction workflows.

### Basic Extraction

```
```

**Example workflow**:

1. Create `DocumentExtractor` with desired formats and options
2. Define extraction template (dict, Pydantic class, etc.)
3. Call `extract()` or `extract_all()` with source and template
4. Receive `ExtractionResult` with per-page extracted data

**Sources**: [docling/document\_extractor.py88-193](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L193)

### Pipeline Caching

The extractor caches pipeline instances by `(pipeline_class, options_hash)` to avoid redundant model loading:

```
```

**Sources**: [docling/document\_extractor.py291-317](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L291-L317)

This pattern matches the `DocumentConverter` caching strategy, ensuring that multiple extraction calls with identical configurations reuse the same model instance, avoiding expensive reloads.

**Sources**: [docling/document\_converter.py229-248](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L229-L248) (converter equivalent)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Extraction Pipeline](#extraction-pipeline.md)
- [Architecture Overview](#architecture-overview.md)
- [Class Hierarchy](#class-hierarchy.md)
- [Pipeline Initialization](#pipeline-initialization.md)
- [Configuration](#configuration.md)
- [Extraction Process Flow](#extraction-process-flow.md)
- [Image Extraction from Backend](#image-extraction-from-backend.md)
- [Template Serialization](#template-serialization.md)
- [Supported Template Types](#supported-template-types.md)
- [Serialization Process](#serialization-process.md)
- [NuExtract Model Integration](#nuextract-model-integration.md)
- [Model Architecture](#model-architecture.md)
- [NuExtract Input Format](#nuextract-input-format.md)
- [Batch Processing](#batch-processing.md)
- [Output Structure](#output-structure.md)
- [Data Models](#data-models.md)
- [Extraction Result Processing](#extraction-result-processing.md)
- [Status Determination](#status-determination.md)
- [Comparison with VlmPipeline](#comparison-with-vlmpipeline.md)
- [Usage Patterns](#usage-patterns.md)
- [Basic Extraction](#basic-extraction.md)
- [Pipeline Caching](#pipeline-caching.md)
