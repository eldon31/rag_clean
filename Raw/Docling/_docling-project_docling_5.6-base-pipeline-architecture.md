Base Pipeline Architecture | docling-project/docling | DeepWiki

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

# Base Pipeline Architecture

Relevant source files

- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)

This document covers the foundational pipeline framework in Docling that enables extensible document processing workflows. The base pipeline architecture defines abstract interfaces, execution patterns, model integration points, and caching mechanisms that allow different processing strategies to be implemented consistently.

The key architectural components include:

- `BasePipeline`: Abstract base class defining the three-phase execution model (build, assemble, enrich)
- `ConvertPipeline`: Specialization that adds enrichment model support
- `PaginatedPipeline`: Specialization that adds page-by-page processing for paginated formats
- Pipeline caching: Instance reuse based on pipeline class and options hash to avoid redundant model loading

For information about specific pipeline implementations like PDF processing, see page 5.1 (Standard PDF Pipeline) and page 5.3 (VLM Pipeline). For document backends that pipelines operate on, see page 3 (Document Backends).

## Pipeline Hierarchy

The Docling pipeline architecture is built around a hierarchy of abstract base classes that define different processing paradigms:

```
```

**Sources:** [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133) [docling/pipeline/base\_pipeline.py135-182](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L135-L182) [docling/pipeline/base\_pipeline.py184-319](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L184-L319) [docling/pipeline/simple\_pipeline.py16-56](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L16-L56) [docling/pipeline/vlm\_pipeline.py50-389](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L389) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296-648](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L648) [docling/pipeline/asr\_pipeline.py204-242](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L204-L242) [docling/pipeline/extraction\_vlm\_pipeline.py32-198](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L198) [docling/pipeline/base\_extraction\_pipeline.py15-73](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L15-L73)

## Core Pipeline Execution Flow

The `BasePipeline.execute()` method defines the standard three-phase execution pattern that all pipelines follow. This method serves as a template, delegating to abstract methods that subclasses implement:

```
```

The execution flow guarantees that `_unload()` is called in the `finally` block to clean up resources regardless of success or failure.

**Sources:** [docling/pipeline/base\_pipeline.py62-84](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L62-L84)

## Pipeline Processing Phases

The three-phase execution model provides clear separation of concerns during document processing:

### Phase 1: Build (\_build\_document)

The `_build_document()` abstract method is responsible for extracting and processing raw content from the input document. This is where format-specific parsing occurs:

| Pipeline Type       | Build Strategy                                                                |
| ------------------- | ----------------------------------------------------------------------------- |
| `SimplePipeline`    | Directly calls `backend.convert()` for declarative formats (DOCX, HTML, etc.) |
| `PaginatedPipeline` | Processes pages in batches through a sequential model pipeline                |
| `VlmPipeline`       | Generates VLM predictions for each page image                                 |
| `AsrPipeline`       | Transcribes audio using Whisper models                                        |

The build phase populates `conv_res.pages` with raw predictions from models (layout, tables, OCR, etc.) but does not yet construct the final document hierarchy.

**Sources:** [docling/pipeline/base\_pipeline.py86-88](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L86-L88) [docling/pipeline/simple\_pipeline.py26-41](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L26-L41) [docling/pipeline/base\_pipeline.py197-283](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L197-L283) [docling/pipeline/vlm\_pipeline.py114-123](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L114-L123) [docling/pipeline/asr\_pipeline.py260-265](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L260-L265)

### Phase 2: Assemble (\_assemble\_document)

The `_assemble_document()` method takes processed content and constructs the final `DoclingDocument` structure. The base implementation is a no-op, but subclasses override it to:

- Construct document hierarchy from page-level predictions
- Generate page images at configured scale
- Crop element images for pictures and tables
- Determine reading order
- Convert VLM outputs (DOCTAGS/Markdown/HTML) into `DoclingDocument`

**Sources:** [docling/pipeline/base\_pipeline.py90-91](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L90-L91) [docling/pipeline/vlm\_pipeline.py136-186](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L136-L186) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py535-628](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L535-L628)

### Phase 3: Enrich (\_enrich\_document)

The `_enrich_document()` method applies enrichment models to enhance the document content after assembly. This phase operates on the `DoclingDocument` structure, iterating through items and applying models from `enrichment_pipe`:

```
```

Enrichment models include:

- `CodeFormulaModel`: Extracts LaTeX from code/formula images
- `DocumentPictureClassifier`: Classifies figure types
- `PictureDescriptionVlmModel` or `PictureDescriptionApiModel`: Generates image captions

**Sources:** [docling/pipeline/base\_pipeline.py93-115](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L93-L115)

## ConvertPipeline Specialization

The `ConvertPipeline` class extends `BasePipeline` to add enrichment model support. It is the base class for most document conversion pipelines (excluding extraction pipelines):

```
```

**Title:** ConvertPipeline and Its Options

`ConvertPipeline.__init__()` initializes the `enrichment_pipe` with two models:

1. `DocumentPictureClassifier`: Classifies pictures into categories (Chart, Table, Natural Image, etc.)
2. Picture description model (either `PictureDescriptionVlmModel` or `PictureDescriptionApiModel` based on `picture_description_options.kind`)

The picture description model is instantiated using a plugin factory system, allowing third-party plugins to register custom implementations.

**Sources:** [docling/pipeline/base\_pipeline.py135-182](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L135-L182) [docling/datamodel/pipeline\_options.py283-292](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L283-L292)

## Model Integration Architecture

Pipelines integrate with two main types of models:

### Page Processing Models (Build Phase)

Page models are stored in the `build_pipe` list and process pages sequentially during the build phase. Each model implements a callable interface `__call__(conv_res: ConversionResult, page_batch: Iterable[Page]) -> Iterable[Page]`:

```
```

**Title:** Page Processing Models

**Sources:** [docling/models/base\_model.py38-43](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L38-L43) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py318-336](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L318-L336)

### Enrichment Models (Enrich Phase)

Enrichment models are stored in the `enrichment_pipe` list and process document elements after assembly:

```
```

**Title:** Enrichment Models Hierarchy

**Sources:** [docling/models/base\_model.py131-148](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L131-L148) [docling/models/base\_model.py151-158](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L151-L158) [docling/models/base\_model.py160-211](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L160-L211) [docling/pipeline/base\_pipeline.py152-162](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L152-L162) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py339-352](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L339-L352)

## PaginatedPipeline Specialization

The `PaginatedPipeline` class extends `ConvertPipeline` to handle document formats that require page-by-page processing, such as PDFs. It introduces the abstract method `initialize_page(conv_res, page)` that subclasses must implement:

```
```

**Title:** PaginatedPipeline and Its Options

The `_build_document()` implementation processes pages in batches:

```
```

**Title:** PaginatedPipeline Build Flow

The `_apply_on_pages()` method chains models from `build_pipe`:

```
```

Each model receives the output of the previous model, forming a sequential processing pipeline.

**Sources:** [docling/pipeline/base\_pipeline.py184-319](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L184-L319)

## Pipeline Options and Configuration

Each pipeline class defines its configuration through options classes:

| Pipeline Class                | Options Class                  | Key Configuration                        |
| ----------------------------- | ------------------------------ | ---------------------------------------- |
| `SimplePipeline`              | `ConvertPipelineOptions`       | Picture description, classification      |
| `VlmPipeline`                 | `VlmPipelineOptions`           | VLM model, response format, backend text |
| `ThreadedStandardPdfPipeline` | `ThreadedPdfPipelineOptions`   | Batch sizes, queue sizes, timeouts       |
| `AsrPipeline`                 | `AsrPipelineOptions`           | ASR model, temperature, timestamps       |
| `ExtractionVlmPipeline`       | `VlmExtractionPipelineOptions` | Extraction VLM model, scale              |

**Sources:** [docling/pipeline/simple\_pipeline.py50-51](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L50-L51) [docling/pipeline/vlm\_pipeline.py383-384](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L383-L384) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py632-633](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L632-L633) [docling/pipeline/asr\_pipeline.py229-230](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L229-L230) [docling/pipeline/extraction\_vlm\_pipeline.py195-197](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L195-L197)

## Backend Compatibility

Each pipeline implementation defines which document backends it supports through the `is_backend_supported()` class method:

```
```

**Sources:** [docling/pipeline/simple\_pipeline.py54-55](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L54-L55) [docling/pipeline/vlm\_pipeline.py387-388](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L387-L388) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py636-637](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L636-L637) [docling/pipeline/asr\_pipeline.py240-241](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L240-L241)

## Error Handling and Status Determination

Pipelines implement different strategies for determining conversion status:

- **SimplePipeline**: Always returns `SUCCESS` if no exceptions occur
- **VlmPipeline**: Checks for valid pages and backend status
- **ThreadedStandardPdfPipeline**: Preserves status from threaded processing
- **AsrPipeline**: Always returns `SUCCESS` for valid transcription

All pipelines support graceful error handling through the `raises_on_error` parameter in `execute()`, allowing partial results to be returned instead of exceptions.

**Sources:** [docling/pipeline/simple\_pipeline.py43-47](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L43-L47) [docling/pipeline/base\_pipeline.py295-314](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L295-L314) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py639-640](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L639-L640) [docling/pipeline/asr\_pipeline.py224-226](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L224-L226) [docling/pipeline/base\_pipeline.py77-81](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L77-L81)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Base Pipeline Architecture](#base-pipeline-architecture.md)
- [Pipeline Hierarchy](#pipeline-hierarchy.md)
- [Core Pipeline Execution Flow](#core-pipeline-execution-flow.md)
- [Pipeline Processing Phases](#pipeline-processing-phases.md)
- [Phase 1: Build (\_build\_document)](#phase-1-build-_build_document.md)
- [Phase 2: Assemble (\_assemble\_document)](#phase-2-assemble-_assemble_document.md)
- [Phase 3: Enrich (\_enrich\_document)](#phase-3-enrich-_enrich_document.md)
- [ConvertPipeline Specialization](#convertpipeline-specialization.md)
- [Model Integration Architecture](#model-integration-architecture.md)
- [Page Processing Models (Build Phase)](#page-processing-models-build-phase.md)
- [Enrichment Models (Enrich Phase)](#enrichment-models-enrich-phase.md)
- [PaginatedPipeline Specialization](#paginatedpipeline-specialization.md)
- [Pipeline Options and Configuration](#pipeline-options-and-configuration.md)
- [Backend Compatibility](#backend-compatibility.md)
- [Error Handling and Status Determination](#error-handling-and-status-determination.md)
