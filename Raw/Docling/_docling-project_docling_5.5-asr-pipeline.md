ASR Pipeline | docling-project/docling | DeepWiki

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

# ASR Pipeline

Relevant source files

- [.github/SECURITY.md](https://github.com/docling-project/docling/blob/f7244a43/.github/SECURITY.md)
- [CHANGELOG.md](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md)
- [CITATION.cff](https://github.com/docling-project/docling/blob/f7244a43/CITATION.cff)
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
- [pyproject.toml](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml)
- [uv.lock](https://github.com/docling-project/docling/blob/f7244a43/uv.lock)

The ASR (Automatic Speech Recognition) Pipeline provides audio transcription capabilities within Docling, converting audio files into text-based `DoclingDocument` representations. This pipeline uses OpenAI's Whisper models to transcribe speech and generates structured output with optional timestamps and word-level segmentation.

For information about other pipeline types, see:

- Standard PDF processing: [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md)
- Vision-based document processing: [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md)
- Structured data extraction: [Extraction Pipeline](docling-project/docling/5.4-extraction-pipeline.md)

## Overview

The ASR Pipeline differs fundamentally from other Docling pipelines in several ways:

1. **No page-based processing**: Audio files are not paginated, so the pipeline inherits directly from `BasePipeline` rather than `PaginatedPipeline`
2. **Backend architecture**: Uses `NoOpBackend` since audio files don't require document parsing like PDFs
3. **Output format**: Produces text-based `DoclingDocument` with conversation items containing transcribed text and optional timing information
4. **Model dependency**: Requires the `openai-whisper` package (installable via `pip install openai-whisper` or `uv sync --extra asr`)

Sources: [docling/pipeline/asr\_pipeline.py1-270](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L1-L270)

## Architecture

```
```

**Figure 1: ASR Pipeline Component Architecture**

The ASR Pipeline follows a streamlined architecture compared to document processing pipelines:

- **NoOpBackend** provides access to the audio file path or stream without parsing
- **\_NativeWhisperModel** handles the actual transcription using Whisper
- **\_ConversationItem** structures represent transcribed segments with metadata
- Final output is a `DoclingDocument` populated with `TextItem` elements

Sources: [docling/pipeline/asr\_pipeline.py1-50](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L1-L50) [docling/pipeline/asr\_pipeline.py232-270](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L232-L270)

## Pipeline Initialization

### Class Hierarchy

```
```

**Figure 2: ASR Pipeline Class Hierarchy**

The `AsrPipeline` class inherits directly from `BasePipeline` (not `PaginatedPipeline`) because audio files are not paginated.

Sources: [docling/pipeline/asr\_pipeline.py232-270](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L232-L270) [docling/pipeline/base\_pipeline.py43-133](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L43-L133)

### Initialization Process

The pipeline is initialized in `AsrPipeline.__init__()`:

| Component          | Purpose                                   | Configuration Source          |
| ------------------ | ----------------------------------------- | ----------------------------- |
| `pipeline_options` | Contains ASR model configuration          | `AsrPipelineOptions`          |
| `keep_backend`     | Set to `True` to retain backend reference | Fixed value                   |
| `_model`           | Whisper transcription model wrapper       | `_NativeWhisperModel`         |
| `artifacts_path`   | Model download/cache location             | Inherited from `BasePipeline` |

The initialization delegates model setup to `_NativeWhisperModel`:

```
AsrPipeline.__init__()
  ├── super().__init__(pipeline_options)
  │   └── Sets artifacts_path from options or settings
  ├── self.keep_backend = True
  └── self._model = _NativeWhisperModel(...)
      ├── Import whisper package
      ├── Set device (CPU/CUDA/MPS) based on accelerator_options
      ├── Load Whisper model with name from asr_options.repo_id
      └── Configure transcription parameters (verbose, timestamps, word_timestamps)
```

Sources: [docling/pipeline/asr\_pipeline.py233-251](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L233-L251) [docling/pipeline/asr\_pipeline.py99-149](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L99-L149)

## Audio Processing Flow

```
```

**Figure 3: ASR Pipeline Execution Sequence**

Sources: [docling/pipeline/asr\_pipeline.py260-265](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L260-L265) [docling/pipeline/asr\_pipeline.py150-230](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L150-L230)

### Step-by-Step Processing

1. **Pipeline Entry** ([asr\_pipeline.py260-265](https://github.com/docling-project/docling/blob/f7244a43/asr_pipeline.py#L260-L265)):

   - `AsrPipeline._build_document()` is called by the base pipeline's `execute()` method
   - Delegates immediately to `_NativeWhisperModel.run()`

2. **Input Handling** ([asr\_pipeline.py150-169](https://github.com/docling-project/docling/blob/f7244a43/asr_pipeline.py#L150-L169)):

   - Accesses `path_or_stream` from the `NoOpBackend`
   - For `BytesIO` inputs, creates a temporary file (Whisper requires file paths)
   - For `Path` inputs, uses the path directly

3. **Transcription** ([asr\_pipeline.py171-189](https://github.com/docling-project/docling/blob/f7244a43/asr_pipeline.py#L171-L189)):

   - Calls `_NativeWhisperModel.transcribe()` which invokes the Whisper model
   - Whisper returns segments with text, start time, end time, and optionally word-level timestamps

4. **Document Assembly** ([asr\_pipeline.py174-188](https://github.com/docling-project/docling/blob/f7244a43/asr_pipeline.py#L174-L188)):

   - Creates a `DoclingDocument` with proper `DocumentOrigin` metadata
   - Iterates through conversation items
   - Each item is added as a `TextItem` with `DocItemLabel.TEXT`

5. **Cleanup** ([asr\_pipeline.py197-205](https://github.com/docling-project/docling/blob/f7244a43/asr_pipeline.py#L197-L205)):

   - Removes temporary files if created from `BytesIO` input

Sources: [docling/pipeline/asr\_pipeline.py150-230](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L150-L230)

## Whisper Model Integration

### Model Wrapper: \_NativeWhisperModel

The `_NativeWhisperModel` class encapsulates Whisper model loading and inference:

| Property          | Type          | Purpose                       |
| ----------------- | ------------- | ----------------------------- |
| `enabled`         | `bool`        | Whether model is active       |
| `device`          | `str`         | Compute device (cpu/cuda/mps) |
| `model`           | Whisper model | Loaded Whisper model instance |
| `max_tokens`      | `int`         | Maximum tokens per generation |
| `temperature`     | `float`       | Sampling temperature          |
| `verbose`         | `bool`        | Enable Whisper logging        |
| `timestamps`      | `bool`        | Include segment timestamps    |
| `word_timestamps` | `bool`        | Include word-level timestamps |

### Model Loading Logic

```
```

**Figure 4: Whisper Model Loading Flow**

Sources: [docling/pipeline/asr\_pipeline.py99-149](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L99-L149)

### Device Selection

The model automatically selects the appropriate device using `decide_device()`:

1. Checks `accelerator_options.device` setting
2. Validates against `asr_options.supported_devices`
3. Falls back to CPU if CUDA/MPS unavailable
4. Logs the selected device for debugging

Sources: [docling/pipeline/asr\_pipeline.py126-130](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L126-L130)

### Transcription Output Structure

The `transcribe()` method returns a list of `_ConversationItem` objects:

```
```

Each conversation item can be formatted as:

```
[time: 0.0-5.2] [speaker:speaker-1] Transcribed text goes here
```

Sources: [docling/pipeline/asr\_pipeline.py50-97](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L50-L97) [docling/pipeline/asr\_pipeline.py207-229](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L207-L229)

## Configuration Options

### AsrPipelineOptions

The `AsrPipelineOptions` class (defined in the options module, referenced in the code) configures the ASR pipeline:

```
```

### InlineAsrNativeWhisperOptions

Model-specific configuration for native Whisper:

| Option              | Type        | Default                 | Purpose                                              |
| ------------------- | ----------- | ----------------------- | ---------------------------------------------------- |
| `repo_id`           | `str`       | e.g., "base"            | Whisper model variant (tiny/base/small/medium/large) |
| `max_new_tokens`    | `int`       | -                       | Maximum tokens to generate                           |
| `temperature`       | `float`     | -                       | Sampling temperature                                 |
| `verbose`           | `bool`      | `False`                 | Enable detailed logging                              |
| `timestamps`        | `bool`      | `True`                  | Include segment timestamps                           |
| `word_timestamps`   | `bool`      | `False`                 | Include word-level timestamps                        |
| `supported_devices` | `list[str]` | \["cuda", "cpu", "mps"] | Allowed compute devices                              |

Sources: [docling/pipeline/asr\_pipeline.py105-148](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L105-L148)

### Default Options

```
```

This provides default configuration when no options are explicitly specified.

Sources: [docling/pipeline/asr\_pipeline.py256-258](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L256-L258)

## Backend Integration

### NoOpBackend Usage

The ASR pipeline uses `NoOpBackend` which provides minimal functionality:

```
```

**Figure 5: NoOpBackend Role**

The backend's role is limited to:

1. Storing the `path_or_stream` reference
2. Providing file metadata (name, size, etc.)
3. No parsing or structure extraction (unlike PDF backends)

The `is_backend_supported()` method validates this:

```
```

Sources: [docling/pipeline/asr\_pipeline.py268-269](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L268-L269) [docling/backend/noop\_backend.py1-20](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/noop_backend.py#L1-L20) (referenced but not shown)

### Input Handling: Path vs BytesIO

The pipeline handles two input types:

| Input Type | Handling                  | Cleanup Required         |
| ---------- | ------------------------- | ------------------------ |
| `Path`     | Used directly by Whisper  | No                       |
| `BytesIO`  | Written to temporary file | Yes (in `finally` block) |

**Temporary File Creation**:

```
```

This approach is necessary because the Whisper library requires file paths for audio processing.

Sources: [docling/pipeline/asr\_pipeline.py154-169](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L154-L169)

## Output Format

### DoclingDocument Structure

The ASR pipeline creates a simple `DoclingDocument` structure:

```
```

**Figure 6: ASR Output Document Structure**

Unlike PDF documents, ASR output:

- Has no page structure
- No layout elements (headings, tables, figures)
- Only text items with optional timestamps
- No bounding boxes or provenance information

Sources: [docling/pipeline/asr\_pipeline.py174-188](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L174-L188)

### Text Formatting

Each conversation item is formatted using `_ConversationItem.to_string()`:

```
```

Example output:

```
[time: 0.0-5.234] This is the first transcribed segment
[time: 5.234-10.512] This is the second segment with more text
[time: 10.512-15.801] And this is the third segment
```

Sources: [docling/pipeline/asr\_pipeline.py86-96](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L86-L96)

## Error Handling

### Exception Management

```
```

**Figure 7: ASR Error Handling Flow**

Error handling includes:

1. **Import errors**: Caught during initialization if `openai-whisper` not installed
2. **Transcription errors**: Logged and set `status = FAILURE`
3. **Cleanup guarantees**: Temporary files deleted in `finally` block
4. **Graceful degradation**: Failed conversions return `ConversionResult` with `FAILURE` status

Sources: [docling/pipeline/asr\_pipeline.py171-205](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L171-L205)

### Status Determination

```
```

The ASR pipeline uses a simple status determination: if `_build_document()` completes without raising an exception, the status is `SUCCESS`. Unlike PDF pipelines, there's no concept of partial success (no page-level validation).

Sources: [docling/pipeline/asr\_pipeline.py252-254](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L252-L254)

## Usage Example

```
```

## Integration with DocumentConverter

The ASR pipeline is automatically selected by `DocumentConverter` when processing audio formats:

```
```

**Figure 8: ASR Pipeline Selection in DocumentConverter**

The format-to-pipeline mapping is configured in `DocumentConverter.format_to_options`:

- Audio formats (MP3, WAV, etc.) → `AsrPipeline`
- Uses `AudioBackend` or `NoOpBackend` for file access
- Pipeline options can be customized per format

Sources: [docling/pipeline/asr\_pipeline.py232-270](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L232-L270) [docling/document\_converter.py1-500](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L1-L500) (referenced but not shown in detail)

## Key Differences from Other Pipelines

| Aspect           | ASR Pipeline       | PDF Pipelines         | VLM Pipeline          |
| ---------------- | ------------------ | --------------------- | --------------------- |
| Base class       | `BasePipeline`     | `PaginatedPipeline`   | `PaginatedPipeline`   |
| Backend type     | `NoOpBackend`      | `PdfDocumentBackend`  | `PdfDocumentBackend`  |
| Processing unit  | Entire audio file  | Individual pages      | Individual pages      |
| Primary model    | Whisper (external) | Layout, Table, OCR    | Vision-Language Model |
| Output structure | Sequential text    | Hierarchical document | Structured document   |
| Temporal data    | Timestamps         | Page numbers          | Page numbers          |

Sources: [docling/pipeline/asr\_pipeline.py232-270](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py#L232-L270) [docling/pipeline/base\_pipeline.py184-320](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L184-L320) [docling/pipeline/vlm\_pipeline.py50-389](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L50-L389)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [ASR Pipeline](#asr-pipeline.md)
- [Overview](#overview.md)
- [Architecture](#architecture.md)
- [Pipeline Initialization](#pipeline-initialization.md)
- [Class Hierarchy](#class-hierarchy.md)
- [Initialization Process](#initialization-process.md)
- [Audio Processing Flow](#audio-processing-flow.md)
- [Step-by-Step Processing](#step-by-step-processing.md)
- [Whisper Model Integration](#whisper-model-integration.md)
- [Model Wrapper: \_NativeWhisperModel](#model-wrapper-_nativewhispermodel.md)
- [Model Loading Logic](#model-loading-logic.md)
- [Device Selection](#device-selection.md)
- [Transcription Output Structure](#transcription-output-structure.md)
- [Configuration Options](#configuration-options.md)
- [AsrPipelineOptions](#asrpipelineoptions.md)
- [InlineAsrNativeWhisperOptions](#inlineasrnativewhisperoptions.md)
- [Default Options](#default-options.md)
- [Backend Integration](#backend-integration.md)
- [NoOpBackend Usage](#noopbackend-usage.md)
- [Input Handling: Path vs BytesIO](#input-handling-path-vs-bytesio.md)
- [Output Format](#output-format.md)
- [DoclingDocument Structure](#doclingdocument-structure.md)
- [Text Formatting](#text-formatting.md)
- [Error Handling](#error-handling.md)
- [Exception Management](#exception-management.md)
- [Status Determination](#status-determination.md)
- [Usage Example](#usage-example.md)
- [Integration with DocumentConverter](#integration-with-documentconverter.md)
- [Key Differences from Other Pipelines](#key-differences-from-other-pipelines.md)
