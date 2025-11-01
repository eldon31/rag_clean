VLM Pipeline | docling-project/docling | DeepWiki

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

# VLM Pipeline

Relevant source files

- [README.md](https://github.com/docling-project/docling/blob/f7244a43/README.md)
- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)
- [docs/examples/minimal\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py)
- [docs/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md)
- [docs/usage/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md)
- [docs/usage/mcp.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md)
- [docs/usage/vision\_models.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md)
- [mkdocs.yml](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml)

The VLM Pipeline provides vision-language model based document processing capabilities for converting documents (primarily PDFs) into structured formats using AI models that can understand both text and images. This pipeline leverages various VLM backends including local models via HuggingFace Transformers, MLX for Apple Silicon optimization, VLLM for high-throughput inference, and remote API services.

For traditional PDF processing without VLM capabilities, see [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md). For base pipeline architecture and common functionality, see [Base Pipeline Architecture](docling-project/docling/5.3-vlm-pipeline.md).

## Architecture Overview

The VLM Pipeline architecture centers around the `VlmPipeline` class which orchestrates different VLM model implementations to process document pages as images and generate structured output.

### VLM Pipeline System Architecture

```
```

Sources: [docling/pipeline/vlm\_pipeline.py50-125](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L125) [docling/datamodel/pipeline\_options\_vlm\_model.py11-101](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L11-L101)

### VLM Model Class Hierarchy

```
```

Sources: [docling/models/base\_model.py40-120](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L40-L120) [docling/models/vlm\_models\_inline/hf\_transformers\_model.py32](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L32-L32) [docling/models/vlm\_models\_inline/mlx\_model.py30](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L30-L30) [docling/models/api\_vlm\_model.py13](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L13-L13)

## VLM Model Implementations

The VLM Pipeline supports multiple backend implementations for different use cases and hardware configurations.

### HuggingFace Transformers Model

The `HuggingFaceTransformersVlmModel` provides local inference using the HuggingFace Transformers library with support for various model architectures.

**Key Features:**

- Supports multiple `TransformersModelType`: `AUTOMODEL`, `AUTOMODEL_VISION2SEQ`, `AUTOMODEL_CAUSALLM`, `AUTOMODEL_IMAGETEXTTOTEXT`
- Batch processing with proper padding and attention handling
- Flash Attention 2 support for CUDA devices
- Quantization support via `BitsAndBytesConfig`
- Multiple prompt styles: `CHAT`, `RAW`, `NONE`

**Configuration Options:**

- `repo_id`: HuggingFace model repository identifier
- `quantized`: Enable 8-bit quantization
- `torch_dtype`: Specify torch data type
- `stop_strings`: Custom stopping criteria
- `max_new_tokens`: Maximum generation length

Sources: [docling/models/vlm\_models\_inline/hf\_transformers\_model.py32-315](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L32-L315) [docling/datamodel/pipeline\_options\_vlm\_model.py52-84](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L52-L84)

### MLX Model Implementation

The `HuggingFaceMlxModel` provides optimized inference for Apple Silicon using the MLX framework.

**Key Features:**

- Thread-safe with global locking mechanism (`_MLX_GLOBAL_LOCK`)
- Stream generation with token-level processing
- Optimized for Apple Silicon hardware
- Support for stop string termination
- Token-level logprob tracking

**Thread Safety:**

```
```

Sources: [docling/models/vlm\_models\_inline/mlx\_model.py25-261](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L25-L261)

### API-Based VLM Model

The `ApiVlmModel` enables integration with remote VLM services through standardized chat completion APIs.

**Key Features:**

- Concurrent processing with `ThreadPoolExecutor`
- Configurable timeout and concurrency limits
- Custom headers and parameters support
- Compatible with OpenAI-style chat completion APIs

**Configuration Example:**

- `url`: API endpoint (default: `http://localhost:11434/v1/chat/completions`)
- `params`: API-specific parameters (model, temperature, etc.)
- `headers`: Authentication and custom headers
- `concurrency`: Maximum concurrent requests

Sources: [docling/models/api\_vlm\_model.py13-73](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L13-L73) [docling/datamodel/pipeline\_options\_vlm\_model.py90-101](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L90-L101)

## Response Formats and Processing

The VLM Pipeline supports multiple response formats, each processed differently to generate the final `DoclingDocument`.

### Response Format Processing Flow

```
```

Sources: [docling/pipeline/vlm\_pipeline.py148-392](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L148-L392)

### DocTags Format Processing

DocTags format provides the most structured output with precise bounding box information and element classification.

**Key Features:**

- Direct conversion to `DoclingDocument` via `DocTagsDocument.from_doctags_and_image_pairs()`
- Preserves spatial relationships and element types
- Optional backend text extraction with `force_backend_text`
- Support for picture image generation

**Backend Text Extraction:** When `force_backend_text=True` and `response_format=ResponseFormat.DOCTAGS`, the pipeline extracts actual text from the PDF backend using predicted bounding boxes instead of relying on VLM-generated text.

Sources: [docling/pipeline/vlm\_pipeline.py200-238](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L200-L238)

### Markdown and HTML Processing

Both Markdown and HTML formats follow similar processing patterns, using respective document backends for conversion.

**Processing Steps:**

1. Extract content from code blocks (triple backticks)
2. Create temporary `BytesIO` stream with extracted content
3. Use `MarkdownDocumentBackend` or `HTMLDocumentBackend` for conversion
4. Generate page structure with image dimensions
5. Add provenance information with placeholder bounding boxes

Sources: [docling/pipeline/vlm\_pipeline.py240-392](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L240-L392)

## Pipeline Configuration

The VLM Pipeline uses `VlmPipelineOptions` for configuration, which includes VLM-specific options and general pipeline settings.

### Configuration Class Hierarchy

```
```

Sources: [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py) [docling/datamodel/pipeline\_options\_vlm\_model.py11-101](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L11-L101)

### Key Configuration Parameters

| Parameter                 | Type             | Description                                  |
| ------------------------- | ---------------- | -------------------------------------------- |
| `vlm_options`             | `BaseVlmOptions` | VLM model configuration (inline or API)      |
| `force_backend_text`      | `bool`           | Extract text from backend vs VLM response    |
| `generate_page_images`    | `bool`           | Generate page images for processing          |
| `generate_picture_images` | `bool`           | Generate cropped images for picture elements |
| `images_scale`            | `float`          | Image scaling factor                         |
| `enable_remote_services`  | `bool`           | Allow API-based VLM calls                    |

Sources: [docling/pipeline/vlm\_pipeline.py51-77](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L51-L77)

## Pipeline Execution Flow

The VLM Pipeline follows the standard pipeline execution pattern with VLM-specific customizations.

### VLM Pipeline Execution Sequence

```
```

Sources: [docling/pipeline/base\_pipeline.py39-61](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L39-L61) [docling/pipeline/vlm\_pipeline.py126-198](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L126-L198)

### Page Initialization Process

The `initialize_page()` method prepares pages for VLM processing:

1. **Backend Loading**: Load page backend via `conv_res.input._backend.load_page(page.page_no)`
2. **Size Calculation**: Set `page.size` from backend dimensions
3. **Conditional Text Extraction**: If `force_backend_text=True`, extract `parsed_page` for prompt construction

**Backend Text Extraction Logic:**

```
```

Sources: [docling/pipeline/vlm\_pipeline.py126-135](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L126-L135)

## Integration with Base Pipeline

The VLM Pipeline extends `PaginatedPipeline` and integrates with the base pipeline architecture through standardized interfaces.

### Pipeline Integration Points

```
```

Sources: [docling/pipeline/base\_pipeline.py32-105](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L32-L105) [docling/pipeline/vlm\_pipeline.py50-401](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L401)

### Backend Compatibility

The VLM Pipeline supports specific backend types through the `is_backend_supported()` method:

```
```

Currently, only `PdfDocumentBackend` instances are supported, limiting VLM processing to PDF documents.

Sources: [docling/pipeline/vlm\_pipeline.py398-400](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L398-L400)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [VLM Pipeline](#vlm-pipeline.md)
- [Architecture Overview](#architecture-overview.md)
- [VLM Pipeline System Architecture](#vlm-pipeline-system-architecture.md)
- [VLM Model Class Hierarchy](#vlm-model-class-hierarchy.md)
- [VLM Model Implementations](#vlm-model-implementations.md)
- [HuggingFace Transformers Model](#huggingface-transformers-model.md)
- [MLX Model Implementation](#mlx-model-implementation.md)
- [API-Based VLM Model](#api-based-vlm-model.md)
- [Response Formats and Processing](#response-formats-and-processing.md)
- [Response Format Processing Flow](#response-format-processing-flow.md)
- [DocTags Format Processing](#doctags-format-processing.md)
- [Markdown and HTML Processing](#markdown-and-html-processing.md)
- [Pipeline Configuration](#pipeline-configuration.md)
- [Configuration Class Hierarchy](#configuration-class-hierarchy.md)
- [Key Configuration Parameters](#key-configuration-parameters.md)
- [Pipeline Execution Flow](#pipeline-execution-flow.md)
- [VLM Pipeline Execution Sequence](#vlm-pipeline-execution-sequence.md)
- [Page Initialization Process](#page-initialization-process.md)
- [Integration with Base Pipeline](#integration-with-base-pipeline.md)
- [Pipeline Integration Points](#pipeline-integration-points.md)
- [Backend Compatibility](#backend-compatibility.md)
