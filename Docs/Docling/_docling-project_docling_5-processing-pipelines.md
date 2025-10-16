Processing Pipelines | docling-project/docling | DeepWiki

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

# Processing Pipelines

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

Processing pipelines form the core orchestration layer in Docling that coordinates document backends, AI/ML models, and configuration options to convert raw documents into structured `DoclingDocument` representations. This page covers the pipeline architecture, available pipeline types, and how models are orchestrated within pipelines.

For information about specific pipeline implementations, see [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md) and [VLM Pipeline](docling-project/docling/5.2-threaded-pdf-pipeline.md). For details about the models used within pipelines, see [AI/ML Models](docling-project/docling/4-aiml-models.md). For configuration of pipeline behavior, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md).

## Pipeline Architecture Overview

Docling provides two main pipeline hierarchies: conversion pipelines for document processing and extraction pipelines for structured data extraction. Each pipeline type is designed for specific document formats and processing requirements.

### Pipeline Base Architecture

```
```

Sources: [docling/pipeline/base\_pipeline.py43-184](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L184) [docling/pipeline/vlm\_pipeline.py50](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L50) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L296) [docling/pipeline/simple\_pipeline.py16](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L16-L16) [docling/pipeline/asr\_pipeline.py204](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L204-L204) [docling/pipeline/base\_extraction\_pipeline.py15](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py#L15-L15) [docling/pipeline/extraction\_vlm\_pipeline.py32](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L32)

# Processing Pipelines

Processing pipelines form the core orchestration layer in Docling that coordinates document backends, AI/ML models, and configuration options to convert raw documents into structured `DoclingDocument` representations. This page covers the pipeline architecture, available pipeline types, and how models are orchestrated within pipelines.

For information about specific pipeline implementations, see [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md) and [VLM Pipeline](docling-project/docling/5.2-threaded-pdf-pipeline.md). For details about the models used within pipelines, see [AI/ML Models](docling-project/docling/4-aiml-models.md). For configuration of pipeline behavior, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md).

## Pipeline Architecture Overview

Pipelines in Docling implement the `PaginatedPipeline` base class and orchestrate multiple processing models in sequence. Each pipeline type is designed for specific document formats and processing requirements.

### Pipeline Base Architecture

```
```

Sources: [docling/pipeline/base\_pipeline.py29-106](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L29-L106) [docling/pipeline/standard\_pdf\_pipeline.py39-42](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L39-L42) [docling/pipeline/vlm\_pipeline.py50-53](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L53)

## Pipeline Types and Backend Compatibility

Different pipeline types are designed for specific document formats and processing approaches. The `DocumentConverter` selects pipelines based on backend compatibility using the `is_backend_supported()` method.

### Pipeline Type Selection

```
```

Sources: [docling/pipeline/threaded\_standard\_pdf\_pipeline.py636-637](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L636-L637) [docling/pipeline/vlm\_pipeline.py386-388](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L386-L388) [docling/pipeline/simple\_pipeline.py54-55](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L54-L55) [docling/pipeline/asr\_pipeline.py240-241](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L240-L241)

## Pipeline Implementations

Docling provides five main pipeline implementations for different document processing needs:

1. **ThreadedStandardPdfPipeline**: High-performance parallel PDF processing with multi-stage AI models
2. **VlmPipeline**: Vision-Language Model based processing for document understanding
3. **SimplePipeline**: Direct conversion for declarative document formats
4. **AsrPipeline**: Audio transcription using Whisper models
5. **ExtractionVlmPipeline**: Structured data extraction using vision-language models

### ThreadedStandardPdfPipeline Architecture

The `ThreadedStandardPdfPipeline` uses a sophisticated queue-based architecture with parallel processing stages. Each stage runs in its own thread with bounded queues for back-pressure control.

```
```

Sources: [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296-427](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L427) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py96-163](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L96-L163)

### ThreadedQueue Implementation

The threaded pipeline uses custom queue implementation with explicit close semantics and timeout support.

```
```

Sources: [docling/pipeline/threaded\_standard\_pdf\_pipeline.py59-94](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L59-L94) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py96-163](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L96-L163)

### VlmPipeline and ExtractionVlmPipeline

The `VlmPipeline` processes documents using Vision-Language Models with different inference frameworks and response formats. The `ExtractionVlmPipeline` specializes in structured data extraction from documents.

```
```

Sources: [docling/pipeline/vlm\_pipeline.py50-113](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L113) [docling/pipeline/vlm\_pipeline.py136-159](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L136-L159) [docling/pipeline/vlm\_pipeline.py188-380](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L188-L380) [docling/pipeline/extraction\_vlm\_pipeline.py32-126](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py#L32-L126)

### SimplePipeline and AsrPipeline

The `SimplePipeline` handles declarative document backends that can directly produce `DoclingDocument` objects. The `AsrPipeline` processes audio files using Whisper models.

```
```

Sources: [docling/pipeline/simple\_pipeline.py16-55](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py#L16-L55) [docling/pipeline/asr\_pipeline.py98-201](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L98-L201) [docling/pipeline/asr\_pipeline.py204-241](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L204-L241)

## Model Factory Integration

Pipelines use factory patterns to instantiate models with appropriate configurations. This allows for plugin support and model selection based on options.

### Factory-Based Model Creation

| Model Type          | Factory Method                      | Configuration Source                           | Plugin Support |
| ------------------- | ----------------------------------- | ---------------------------------------------- | -------------- |
| OCR Models          | `get_ocr_factory()`                 | `pipeline_options.ocr_options`                 | Yes            |
| Picture Description | `get_picture_description_factory()` | `pipeline_options.picture_description_options` | Yes            |
| Layout Analysis     | Direct instantiation                | `pipeline_options.layout_options`              | No             |
| Table Structure     | Direct instantiation                | `pipeline_options.table_structure_options`     | No             |
| VLM Models          | Conditional instantiation           | `pipeline_options.vlm_options`                 | No             |

```
```

Sources: [docling/pipeline/standard\_pdf\_pipeline.py150-173](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L150-L173) [docling/pipeline/vlm\_pipeline.py77-113](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L77-L113)

## Pipeline Execution Flow

Pipelines follow a common execution pattern with different implementations for page processing, document assembly, and enrichment. The base execution flow handles error management and resource cleanup.

### BasePipeline Execution Flow

```
```

Sources: [docling/pipeline/base\_pipeline.py62-123](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L62-L123) [docling/pipeline/base\_pipeline.py93-115](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L93-L115)

### PaginatedPipeline vs ThreadedPipeline Processing

```
```

Sources: [docling/pipeline/base\_pipeline.py197-283](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L197-L283) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py428-506](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L428-L506) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py226-272](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L226-L272)

### ThreadedStandardPdfPipeline Document Assembly

```
```

Sources: [docling/pipeline/threaded\_standard\_pdf\_pipeline.py535-627](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L535-L627) [docling/pipeline/vlm\_pipeline.py136-185](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L136-L185) [docling/pipeline/vlm\_pipeline.py188-303](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L188-L303)

## Configuration and Model Selection

Pipeline behavior is controlled through `PipelineOptions` classes that enable/disable models and configure their parameters. Models can be conditionally instantiated based on these options.

### Configuration-Driven Model Instantiation

```
```

Sources: [docling/pipeline/standard\_pdf\_pipeline.py42-134](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L42-L134) [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Processing Pipelines](#processing-pipelines.md)
- [Pipeline Architecture Overview](#pipeline-architecture-overview.md)
- [Pipeline Base Architecture](#pipeline-base-architecture.md)
- [Processing Pipelines](#processing-pipelines-1.md)
- [Pipeline Architecture Overview](#pipeline-architecture-overview-1.md)
- [Pipeline Base Architecture](#pipeline-base-architecture-1.md)
- [Pipeline Types and Backend Compatibility](#pipeline-types-and-backend-compatibility.md)
- [Pipeline Type Selection](#pipeline-type-selection.md)
- [Pipeline Implementations](#pipeline-implementations.md)
- [ThreadedStandardPdfPipeline Architecture](#threadedstandardpdfpipeline-architecture.md)
- [ThreadedQueue Implementation](#threadedqueue-implementation.md)
- [VlmPipeline and ExtractionVlmPipeline](#vlmpipeline-and-extractionvlmpipeline.md)
- [SimplePipeline and AsrPipeline](#simplepipeline-and-asrpipeline.md)
- [Model Factory Integration](#model-factory-integration.md)
- [Factory-Based Model Creation](#factory-based-model-creation.md)
- [Pipeline Execution Flow](#pipeline-execution-flow.md)
- [BasePipeline Execution Flow](#basepipeline-execution-flow.md)
- [PaginatedPipeline vs ThreadedPipeline Processing](#paginatedpipeline-vs-threadedpipeline-processing.md)
- [ThreadedStandardPdfPipeline Document Assembly](#threadedstandardpdfpipeline-document-assembly.md)
- [Configuration and Model Selection](#configuration-and-model-selection.md)
- [Configuration-Driven Model Instantiation](#configuration-driven-model-instantiation.md)
