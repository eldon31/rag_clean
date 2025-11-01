DocumentExtractor API | docling-project/docling | DeepWiki

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

# DocumentExtractor API

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

## Purpose and Scope

The `DocumentExtractor` API provides structured data extraction from documents using vision-language models (VLMs) with user-defined templates. Unlike the `DocumentConverter` API (see [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md)) which converts documents to unified `DoclingDocument` format, `DocumentExtractor` extracts specific structured data based on schemas or prompts, returning `ExtractionResult` objects containing parsed JSON or raw text.

For details on the underlying extraction pipeline implementation, see [Extraction Pipeline](docling-project/docling/5.4-extraction-pipeline.md). For VLM model configuration, see [Vision Language Models](docling-project/docling/4.3-vision-language-models.md).

**Sources:** [docling/document\_extractor.py88-97](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L97)

## Core Architecture

### Class Hierarchy and Components

```
```

**Diagram: DocumentExtractor Architecture**

The `DocumentExtractor` class orchestrates extraction by mapping input formats to extraction pipelines through `ExtractionFormatOption` configurations. Each format option specifies both a pipeline class (defaulting to `ExtractionVlmPipeline`) and a backend for document reading (defaulting to `PyPdfiumDocumentBackend`).

**Sources:** [docling/document\_extractor.py88-120](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L120) [docling/document\_extractor.py46-64](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L46-L64) [docling/datamodel/extraction.py1-40](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py#L1-L40)

### DocumentExtractor Class

```
```

**Diagram: DocumentExtractor Class Structure**

The `DocumentExtractor` maintains a cache of initialized pipelines keyed by `(pipeline_class, options_hash)` to avoid redundant model loading across documents with identical configurations.

**Sources:** [docling/document\_extractor.py88-120](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L88-L120) [docling/document\_extractor.py291-317](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L291-L317)

## API Methods

### extract() - Single Document Extraction

```
```

**Diagram: extract() Method Flow**

The `extract()` method is a convenience wrapper around `extract_all()` that returns a single result. It internally calls `extract_all()` with a single-item list and returns the first (and only) result via `next()`.

**Sources:** [docling/document\_extractor.py123-143](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L123-L143) [docling/document\_extractor.py239-264](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L239-L264)

### extract\_all() - Batch Extraction

The `extract_all()` method processes multiple documents with optional concurrency:

| Parameter         | Type                                         | Default            | Description                                        |
| ----------------- | -------------------------------------------- | ------------------ | -------------------------------------------------- |
| `source`          | `Iterable[Union[Path, str, DocumentStream]]` | Required           | Documents to extract from                          |
| `template`        | `ExtractionTemplateType`                     | Required           | Extraction template (str, dict, or Pydantic model) |
| `headers`         | `Optional[Dict[str, str]]`                   | `None`             | HTTP headers for remote documents                  |
| `raises_on_error` | `bool`                                       | `True`             | Whether to raise on extraction failures            |
| `max_num_pages`   | `int`                                        | `sys.maxsize`      | Maximum pages to process per document              |
| `max_file_size`   | `int`                                        | `sys.maxsize`      | Maximum file size in bytes                         |
| `page_range`      | `PageRange`                                  | `(1, sys.maxsize)` | Page range to extract                              |

**Implementation Details:**

- Reuses `_DocumentConversionInput` for format detection and backend initialization
- Supports batch processing with configurable concurrency via `settings.perf.doc_batch_concurrency`
- Uses `ThreadPoolExecutor` when `doc_batch_concurrency > 1` and `doc_batch_size > 1`
- Pipeline caching prevents redundant model initialization

**Sources:** [docling/document\_extractor.py145-193](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L145-L193) [docling/document\_extractor.py196-237](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L196-L237)

## Template Types and Serialization

### Template Type Hierarchy

```
```

**Diagram: Template Type Serialization**

The `_serialize_template()` method in `ExtractionVlmPipeline` handles four template types:

1. **String templates**: Passed directly as prompts
2. **Dict templates**: Serialized via `json.dumps(template, indent=2)`
3. **Pydantic instances**: Serialized via `template.model_dump_json(indent=2)`
4. **Pydantic classes**: Instantiated via `polyfactory.ModelFactory.build()` (using field examples and defaults), then serialized

**Sources:** [docling/pipeline/extraction\_vlm\_pipeline.py173-193](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L173-L193)

### Template Serialization Example Flow

```
```

**Diagram: Template Serialization Decision Tree**

For Pydantic class templates, `polyfactory.ModelFactory` is configured with `__use_examples__=True` and `__use_defaults__=True` to prefer field examples over random values.

**Sources:** [docling/pipeline/extraction\_vlm\_pipeline.py173-193](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L173-L193)

## ExtractionResult Data Model

### Result Structure

```
```

**Diagram: ExtractionResult Class Hierarchy**

The `ExtractionResult` structure mirrors `ConversionResult` but focuses on extracted data rather than document structure:

- **`input`**: The `InputDocument` that was processed
- **`status`**: Overall extraction status (SUCCESS, FAILURE, PARTIAL\_SUCCESS)
- **`errors`**: Document-level errors (empty list if successful)
- **`pages`**: Per-page extraction results

**Sources:** [docling/datamodel/extraction.py25-36](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py#L25-L36)

### ExtractedPageData Structure

Each page in the `pages` list contains:

| Field            | Type                       | Description                                            |
| ---------------- | -------------------------- | ------------------------------------------------------ |
| `page_no`        | `int`                      | 1-indexed page number                                  |
| `extracted_data` | `Optional[Dict[str, Any]]` | Structured data parsed from VLM output (if valid JSON) |
| `raw_text`       | `Optional[str]`            | Raw VLM output text (always populated)                 |
| `errors`         | `List[str]`                | Page-specific extraction errors                        |

The `extracted_data` field is populated only if the VLM output can be parsed as valid JSON. If JSON parsing fails, `extracted_data` is `None` and `raw_text` contains the unparsed output.

**Sources:** [docling/datamodel/extraction.py11-23](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py#L11-L23) [docling/pipeline/extraction\_vlm\_pipeline.py84-98](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L84-L98)

## Pipeline Architecture

### Extraction Pipeline Hierarchy

```
```

**Diagram: Extraction Pipeline Class Hierarchy**

The `BaseExtractionPipeline` defines the extraction contract with three abstract methods:

- `_extract_data()`: Populates `ExtractionResult.pages` and `errors`
- `_determine_status()`: Returns `ConversionStatus` based on extraction results
- `get_default_options()`: Returns default `PipelineOptions`

**Sources:** [docling/pipeline/base\_extraction\_pipeline.py15-73](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L15-L73) [docling/pipeline/extraction\_vlm\_pipeline.py32-46](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L46)

### VLM Model Integration

```
```

**Diagram: VLM Model Processing Flow**

The `NuExtractTransformersModel` uses a specialized input format from the NuMind team:

- Documents are passed as `{"type": "image", "image": PIL_Image}`
- Templates are passed via the `template` parameter to `apply_chat_template()`
- Vision info is processed via `qwen_vl_utils.process_vision_info()`

**Sources:** [docling/pipeline/extraction\_vlm\_pipeline.py48-126](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L48-L126) [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py107-160](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L107-L160) [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py161-290](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py#L161-L290)

## Pipeline Caching Mechanism

### Cache Key Generation

```
```

**Diagram: Pipeline Caching Strategy**

The `_get_pipeline()` method caches pipelines using a composite key:

1. Pipeline class reference (e.g., `ExtractionVlmPipeline`)
2. MD5 hash of `pipeline_options.model_dump()` serialization

This ensures that documents with identical configurations reuse the same pipeline instance (and loaded models), avoiding redundant initialization.

**Thread Safety:** Pipeline retrieval is protected by `_PIPELINE_CACHE_LOCK` to prevent race conditions during concurrent document processing.

**Sources:** [docling/document\_extractor.py291-317](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L291-L317) [docling/document\_extractor.py319-325](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L319-L325)

## Format Support and Backend Configuration

### Default Format Options

```
```

**Diagram: Default Extraction Configuration**

The `_get_default_extraction_option()` function defines default extraction configurations:

- **PDF and Image formats**: Use `PyPdfiumDocumentBackend` for document reading
- **Pipeline**: Always `ExtractionVlmPipeline`
- **Model**: NuExtract-2.0-2B via `NuExtractTransformersModel`

Users can override these defaults via the `extraction_format_options` parameter in `DocumentExtractor.__init__()`.

**Experimental Status:** As of the current implementation, only PDF and Image formats are supported for extraction. The API warns users that it is experimental and may change.

**Sources:** [docling/document\_extractor.py66-85](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L66-L85) [docling/pipeline/extraction\_vlm\_pipeline.py32-46](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L46)

## Error Handling and Status Determination

### Status Decision Tree

```
```

**Diagram: Extraction Status Determination**

The `_determine_status()` method in `ExtractionVlmPipeline` uses a simple rule:

- **SUCCESS**: At least one page extracted AND no page errors
- **FAILURE**: No pages extracted OR any page has errors

Unlike `DocumentConverter`, extraction does not support `PARTIAL_SUCCESS` status—a document either fully succeeds or fails.

**Sources:** [docling/pipeline/extraction\_vlm\_pipeline.py128-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L128-L133)

### Error Propagation

```
```

**Diagram: Error Handling Flow**

The `raises_on_error` parameter controls error behavior at multiple levels:

1. **Document level**: Invalid formats, missing pipelines
2. **Page level**: Image loading failures, VLM processing errors

When `raises_on_error=False`, errors are captured in the `ExtractionResult` structure rather than raised as exceptions.

**Sources:** [docling/document\_extractor.py177-192](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py#L177-L192) [docling/pipeline/base\_extraction\_pipeline.py31-53](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L31-L53) [docling/pipeline/extraction\_vlm\_pipeline.py109-114](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L109-L114)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [DocumentExtractor API](#documentextractor-api.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Core Architecture](#core-architecture.md)
- [Class Hierarchy and Components](#class-hierarchy-and-components.md)
- [DocumentExtractor Class](#documentextractor-class.md)
- [API Methods](#api-methods.md)
- [extract() - Single Document Extraction](#extract---single-document-extraction.md)
- [extract\_all() - Batch Extraction](#extract_all---batch-extraction.md)
- [Template Types and Serialization](#template-types-and-serialization.md)
- [Template Type Hierarchy](#template-type-hierarchy.md)
- [Template Serialization Example Flow](#template-serialization-example-flow.md)
- [ExtractionResult Data Model](#extractionresult-data-model.md)
- [Result Structure](#result-structure.md)
- [ExtractedPageData Structure](#extractedpagedata-structure.md)
- [Pipeline Architecture](#pipeline-architecture.md)
- [Extraction Pipeline Hierarchy](#extraction-pipeline-hierarchy.md)
- [VLM Model Integration](#vlm-model-integration.md)
- [Pipeline Caching Mechanism](#pipeline-caching-mechanism.md)
- [Cache Key Generation](#cache-key-generation.md)
- [Format Support and Backend Configuration](#format-support-and-backend-configuration.md)
- [Default Format Options](#default-format-options.md)
- [Error Handling and Status Determination](#error-handling-and-status-determination.md)
- [Status Decision Tree](#status-decision-tree.md)
- [Error Propagation](#error-propagation.md)
