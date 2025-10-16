Document Conversion CLI | docling-project/docling | DeepWiki

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

# Document Conversion CLI

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

## Purpose and Scope

The Document Conversion CLI provides a command-line interface for converting documents using Docling. The primary command is `docling convert`, which accepts various flags to control conversion behavior, model selection, and output formats. This page documents the CLI arguments, their corresponding configuration options, and usage patterns.

For programmatic document conversion using Python, see [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md). For model artifact management via CLI, see [Model Management CLI](docling-project/docling/6.2-model-management-cli.md).

## Basic Usage

The CLI is invoked with the `docling` command followed by the `convert` subcommand:

```
```

By default, the CLI:

- Processes all supported input formats
- Uses the standard PDF pipeline with DoclingParseV2 backend
- Outputs Markdown to the current directory
- Enables OCR and table structure extraction

Sources: [README.md84-98](https://github.com/docling-project/docling/blob/f7244a43/README.md#L84-L98) [docs/usage/index.md26-39](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L26-L39)

## Command Structure

```
```

Sources: [docling/cli/main.py141-146](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L141-L146) [docling/cli/main.py298-514](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L298-L514)

## Input Sources

The `input_sources` argument accepts one or more paths or URLs:

| Input Type | Example                            | Behavior                                          |
| ---------- | ---------------------------------- | ------------------------------------------------- |
| Local file | `document.pdf`                     | Converts single file                              |
| Directory  | `./documents/`                     | Recursively finds files matching `--from` formats |
| URL        | `https://example.com/file.pdf`     | Downloads and converts                            |
| Multiple   | `file1.pdf file2.docx https://...` | Processes all inputs                              |

The CLI uses `resolve_source_to_path()` to handle URLs and stores temporary files in a `TemporaryDirectory`:

**Directory Processing Logic**

When a directory is provided, the CLI:

1. Iterates through `from_formats` (defaults to all `InputFormat` values)
2. Uses `Path.glob(f"**/*.{ext}")` for each extension
3. Filters out temporary Word files (names starting with `~$`)
4. Builds a list of `input_doc_paths`

Sources: [docling/cli/main.py300-307](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L300-L307) [docling/cli/main.py538-588](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L538-L588)

## Format Selection

### Input Formats (`--from`)

Specifies which input formats to process:

```
```

The `--from` flag maps to `InputFormat` enum values:

| Format  | Extensions               | MIME Types                                                                |
| ------- | ------------------------ | ------------------------------------------------------------------------- |
| `pdf`   | pdf                      | application/pdf                                                           |
| `docx`  | docx, dotx, docm, dotm   | application/vnd.openxmlformats-officedocument.wordprocessingml.document   |
| `pptx`  | pptx, potx, ppsx, pptm   | application/vnd.openxmlformats-officedocument.presentationml.presentation |
| `xlsx`  | xlsx, xlsm               | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet         |
| `html`  | html, htm, xhtml         | text/html, application/xhtml+xml                                          |
| `md`    | md                       | text/markdown                                                             |
| `image` | jpg, png, tif, bmp, webp | image/png, image/jpeg, image/tiff                                         |
| `audio` | wav, mp3                 | audio/wav, audio/mp3                                                      |

Sources: [docling/cli/main.py308-312](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L308-L312) [docling/datamodel/base\_models.py54-72](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L54-L72) [docling/datamodel/base\_models.py83-99](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L83-L99)

### Output Formats (`--to`)

Specifies output format(s):

```
```

Available output formats:

| Flag              | OutputFormat      | File Extension | Description          |
| ----------------- | ----------------- | -------------- | -------------------- |
| `md`              | MARKDOWN          | .md            | Markdown text        |
| `json`            | JSON              | .json          | DoclingDocument JSON |
| `html`            | HTML              | .html          | HTML output          |
| `html_split_page` | HTML\_SPLIT\_PAGE | .html          | HTML with page views |
| `text`            | TEXT              | .txt           | Plain text           |
| `doctags`         | DOCTAGS           | .doctags       | DocTags format       |

Sources: [docling/cli/main.py313-315](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L313-L315) [docling/cli/main.py589-597](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L589-L597) [docling/datamodel/base\_models.py74-80](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L74-L80)

## Pipeline Selection

### Pipeline Types

The `--pipeline` flag selects the processing pipeline:

```
```

**ProcessingPipeline Enum Mapping**

```
```

Sources: [docling/cli/main.py335-338](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L335-L338) [docling/datamodel/pipeline\_options.py365-368](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L365-L368) [docling/cli/main.py619-781](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L619-L781)

## OCR Configuration

### OCR Options

```
```

**OCR Engine Factory and Options Creation**

The CLI uses `get_ocr_factory()` to create the appropriate `OcrOptions` subclass:

```
```

Sources: [docling/cli/main.py347-384](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L347-L384) [docling/cli/main.py599-611](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L599-L611) [docling/datamodel/pipeline\_options.py74-199](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L74-L199)

## PDF Processing Options

### PDF Backend Selection

```
```

**Backend Mapping**

| CLI Flag     | PdfBackend Enum        | Backend Class                 |
| ------------ | ---------------------- | ----------------------------- |
| `dlparse_v1` | PdfBackend.DLPARSE\_V1 | DoclingParseDocumentBackend   |
| `dlparse_v2` | PdfBackend.DLPARSE\_V2 | DoclingParseV2DocumentBackend |
| `dlparse_v4` | PdfBackend.DLPARSE\_V4 | DoclingParseV4DocumentBackend |
| `pypdfium2`  | PdfBackend.PYPDFIUM2   | PyPdfiumDocumentBackend       |

Sources: [docling/cli/main.py392-394](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L392-L394) [docling/cli/main.py645-655](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L645-L655) [docling/datamodel/pipeline\_options.py249-256](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L249-L256)

### Table Structure Options

```
```

The `--table-mode` flag maps to `TableFormerMode` enum:

- `fast`: Faster processing with potentially lower accuracy
- `accurate`: Higher accuracy with more computation

Sources: [docling/cli/main.py360-366](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L360-L366) [docling/cli/main.py395-398](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L395-L398) [docling/datamodel/pipeline\_options.py55-59](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L55-L59)

## VLM Options

When using `--pipeline vlm`, select a vision-language model:

```
```

**VLM Model Type Mapping**

```
```

The CLI automatically selects MLX variants on macOS with MPS when `mlx_vlm` is installed.

Sources: [docling/cli/main.py339-342](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L339-L342) [docling/cli/main.py699-739](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L699-L739) [docling/datamodel/vlm\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py)

## ASR Options

When using `--pipeline asr`, select an ASR model:

```
```

**ASR Model Mapping**

| CLI Flag         | AsrModelType                 | Model Spec      |
| ---------------- | ---------------------------- | --------------- |
| `whisper_tiny`   | AsrModelType.WHISPER\_TINY   | WHISPER\_TINY   |
| `whisper_base`   | AsrModelType.WHISPER\_BASE   | WHISPER\_BASE   |
| `whisper_small`  | AsrModelType.WHISPER\_SMALL  | WHISPER\_SMALL  |
| `whisper_medium` | AsrModelType.WHISPER\_MEDIUM | WHISPER\_MEDIUM |
| `whisper_large`  | AsrModelType.WHISPER\_LARGE  | WHISPER\_LARGE  |
| `whisper_turbo`  | AsrModelType.WHISPER\_TURBO  | WHISPER\_TURBO  |

Sources: [docling/cli/main.py343-346](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L343-L346) [docling/cli/main.py750-777](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L750-L777) [docling/datamodel/asr\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/asr_model_specs.py)

## Enrichment Options

Enrichment models operate on assembled document items to add additional features:

```
```

**Enrichment Flag Mapping**

```
```

Sources: [docling/cli/main.py399-417](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L399-L417) [docling/cli/main.py627-630](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L627-L630) [docling/datamodel/pipeline\_options.py334-349](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L334-L349)

## Output Configuration

### Output Directory

```
```

Sources: [docling/cli/main.py451-453](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L451-L453)

### Image Export Mode

Controls how images are handled in exported formats:

```
```

The `image_export_mode` parameter affects page image generation:

```
```

Sources: [docling/cli/main.py328-334](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L328-L334) [docling/cli/main.py638-643](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L638-L643)

### Layout Visualization

```
```

When `--show-layout` is enabled with `html_split_page` output, the CLI uses `LayoutVisualizer` to overlay bounding boxes on page images.

Sources: [docling/cli/main.py316-322](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L316-L322) [docling/cli/main.py231-251](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L231-L251)

## Hardware Acceleration

### Device Selection

```
```

**AcceleratorDevice Enum**

The `--device` flag maps to `AcceleratorDevice` enum values and is passed to all models via `AcceleratorOptions`.

Sources: [docling/cli/main.py498-500](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L498-L500) [docling/cli/main.py613](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L613-L613) [docling/datamodel/accelerator\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/accelerator_options.py)

### Thread Configuration

```
```

The `--num-threads` flag sets `OMP_NUM_THREADS` for model inference and can also be controlled via environment variables:

- `DOCLING_NUM_THREADS`
- `OMP_NUM_THREADS`

Sources: [docling/cli/main.py497](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L497-L497) [docling/cli/main.py613](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L613-L613)

### Batch Size Configuration

```
```

The `--page-batch-size` flag controls how many pages are processed in one batch. Default is `settings.perf.page_batch_size`.

Sources: [docling/cli/main.py507-513](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L507-L513) [docling/cli/main.py528](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L528-L528)

## Debugging Options

### Visualization Flags

```
```

These flags set corresponding fields in `settings.debug`:

```
```

Sources: [docling/cli/main.py463-480](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L463-L480) [docling/cli/main.py524-527](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L524-L527)

### Verbosity Levels

```
```

Sources: [docling/cli/main.py454-462](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L454-L462) [docling/cli/main.py515-522](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L515-L522)

## Advanced Options

### Artifacts Path

Specify a custom location for model artifacts:

```
```

The artifacts path is set on `pipeline_options.artifacts_path` and affects where models are loaded from.

Sources: [docling/cli/main.py418-421](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L418-L421) [docling/cli/main.py783-784](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L783-L784)

### Remote Services

Enable connections to remote model inference services:

```
```

This flag must be enabled when using API-based VLM models or other remote services.

Sources: [docling/cli/main.py422-427](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L422-L427) [docling/cli/main.py622](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L622-L622)

### External Plugins

Allow loading third-party OCR engine plugins:

```
```

When `--allow-external-plugins` is enabled, the OCR factory discovers plugins via entry points.

Sources: [docling/cli/main.py428-442](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L428-L442) [docling/cli/main.py599-611](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L599-L611)

### Timeout Configuration

Set a per-document timeout:

```
```

Sources: [docling/cli/main.py490-496](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L490-L496) [docling/cli/main.py631](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L631-L631)

### HTTP Headers

Provide custom HTTP headers for URL sources:

```
```

The headers are parsed as JSON and passed to `resolve_source_to_path()`.

Sources: [docling/cli/main.py323-327](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L323-L327) [docling/cli/main.py533-536](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L533-L536)

### Error Handling

```
```

Sources: [docling/cli/main.py443-450](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L443-L450) [docling/cli/main.py796](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L796-L796)

## Options Construction Flow

**CLI to Options Object Pipeline**

```
```

Sources: [docling/cli/main.py613-790](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L613-L790)

## Pipeline-Specific Option Configuration

### Standard Pipeline Path

For `--pipeline standard`:

1. Creates `AcceleratorOptions` with `device` and `num_threads`

2. Creates `OcrOptions` using OCR factory with `ocr_engine`, `force_ocr`, `ocr_lang`, `psm`

3. Creates `PdfPipelineOptions` with:

   - `do_ocr`, `ocr_options`
   - `do_table_structure`, table mode via `table_structure_options.mode`
   - Enrichment flags: `do_code_enrichment`, `do_formula_enrichment`, `do_picture_description`, `do_picture_classification`
   - `document_timeout`

4. Selects backend class based on `--pdf-backend`

5. Creates `PdfFormatOption` with pipeline options and backend

6. Creates `ConvertPipelineOptions` for simple formats (DOCX, HTML, etc.)

7. Builds `format_options` dictionary mapping each `InputFormat` to its `FormatOption`

Sources: [docling/cli/main.py619-697](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L619-L697)

### VLM Pipeline Path

For `--pipeline vlm`:

1. Creates `VlmPipelineOptions` with `enable_remote_services`

2. Selects VLM model spec based on `--vlm-model`:

   - Maps `VlmModelType` enum to specific model spec constants
   - Automatically selects MLX variants on macOS when available

3. Sets `pipeline_options.vlm_options` to selected model spec

4. Creates `PdfFormatOption` with `pipeline_cls=VlmPipeline`

5. Builds `format_options` for PDF and IMAGE formats only

Sources: [docling/cli/main.py699-748](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L699-L748)

### ASR Pipeline Path

For `--pipeline asr`:

1. Creates `AsrPipelineOptions`
2. Selects ASR model spec based on `--asr-model`:
   - Maps `AsrModelType` enum to Whisper model specs
3. Sets `pipeline_options.asr_options` to selected model spec
4. Creates `AudioFormatOption` with `pipeline_cls=AsrPipeline`
5. Builds `format_options` for AUDIO format only

Sources: [docling/cli/main.py750-781](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L750-L781)

## Export Documents Function

The `export_documents()` function handles writing output files:

**Export Logic Flow**

```
```

Sources: [docling/cli/main.py191-289](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L191-L289)

## Common Usage Examples

### Example 1: Basic PDF Conversion

```
```

This uses:

- `ProcessingPipeline.STANDARD`
- `PdfBackend.DLPARSE_V2`
- OCR enabled with auto engine selection
- Table structure extraction enabled
- Output: `document.md` in current directory

### Example 2: Batch Processing with Custom Output

```
```

### Example 3: High-Quality PDF Processing

```
```

### Example 4: VLM Pipeline with MLX

```
```

### Example 5: Audio Transcription

```
```

### Example 6: Enriched Document Processing

```
```

### Example 7: Multi-Format Batch with Filtering

```
```

### Example 8: Debug Visualization

```
```

### Example 9: Referenced Images

```
```

### Example 10: Remote API Processing

```
```

Sources: [README.md84-98](https://github.com/docling-project/docling/blob/f7244a43/README.md#L84-L98) [docs/usage/index.md26-39](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L26-L39) [docs/usage/vision\_models.md13-37](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L13-L37)

## Version and Help Commands

```
```

The version callback displays:

- Docling version
- Docling Core version
- Docling IBM Models version
- Docling Parse version
- Python implementation and version
- Platform information

Sources: [docling/cli/main.py155-170](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L155-L170) [docling/cli/main.py173-188](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L173-L188) [docling/cli/main.py481-489](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L481-L489)

## Implementation Details

### CLI Application Structure

The CLI is built with Typer:

```
```

The main command is decorated with `@app.command()` and contains extensive parameter definitions using `typer.Option()` and `typer.Argument()`.

Sources: [docling/cli/main.py141-146](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L141-L146)

### Temporary File Handling

URL sources are downloaded into a temporary directory:

```
```

The temporary directory is automatically cleaned up after processing.

Sources: [docling/cli/main.py538-546](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L538-L546)

### Conversion Execution

After building `format_options`, the CLI:

1. Creates `DocumentConverter` with allowed formats and format options
2. Calls `converter.convert_all()` with input paths
3. Calls `export_documents()` to write outputs
4. Logs total processing time

Sources: [docling/cli/main.py787-815](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L787-L815)

### Click Compatibility

The Typer app is converted to a Click app for compatibility:

```
```

This allows integration with Click-based tools.

Sources: [docling/cli/main.py818](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L818-L818)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Document Conversion CLI](#document-conversion-cli.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Basic Usage](#basic-usage.md)
- [Command Structure](#command-structure.md)
- [Input Sources](#input-sources.md)
- [Format Selection](#format-selection.md)
- [Input Formats (\`--from\`)](#input-formats---from.md)
- [Output Formats (\`--to\`)](#output-formats---to.md)
- [Pipeline Selection](#pipeline-selection.md)
- [Pipeline Types](#pipeline-types.md)
- [OCR Configuration](#ocr-configuration.md)
- [OCR Options](#ocr-options.md)
- [PDF Processing Options](#pdf-processing-options.md)
- [PDF Backend Selection](#pdf-backend-selection.md)
- [Table Structure Options](#table-structure-options.md)
- [VLM Options](#vlm-options.md)
- [ASR Options](#asr-options.md)
- [Enrichment Options](#enrichment-options.md)
- [Output Configuration](#output-configuration.md)
- [Output Directory](#output-directory.md)
- [Image Export Mode](#image-export-mode.md)
- [Layout Visualization](#layout-visualization.md)
- [Hardware Acceleration](#hardware-acceleration.md)
- [Device Selection](#device-selection.md)
- [Thread Configuration](#thread-configuration.md)
- [Batch Size Configuration](#batch-size-configuration.md)
- [Debugging Options](#debugging-options.md)
- [Visualization Flags](#visualization-flags.md)
- [Verbosity Levels](#verbosity-levels.md)
- [Advanced Options](#advanced-options.md)
- [Artifacts Path](#artifacts-path.md)
- [Remote Services](#remote-services.md)
- [External Plugins](#external-plugins.md)
- [Timeout Configuration](#timeout-configuration.md)
- [HTTP Headers](#http-headers.md)
- [Error Handling](#error-handling.md)
- [Options Construction Flow](#options-construction-flow.md)
- [Pipeline-Specific Option Configuration](#pipeline-specific-option-configuration.md)
- [Standard Pipeline Path](#standard-pipeline-path.md)
- [VLM Pipeline Path](#vlm-pipeline-path.md)
- [ASR Pipeline Path](#asr-pipeline-path.md)
- [Export Documents Function](#export-documents-function.md)
- [Common Usage Examples](#common-usage-examples.md)
- [Example 1: Basic PDF Conversion](#example-1-basic-pdf-conversion.md)
- [Example 2: Batch Processing with Custom Output](#example-2-batch-processing-with-custom-output.md)
- [Example 3: High-Quality PDF Processing](#example-3-high-quality-pdf-processing.md)
- [Example 4: VLM Pipeline with MLX](#example-4-vlm-pipeline-with-mlx.md)
- [Example 5: Audio Transcription](#example-5-audio-transcription.md)
- [Example 6: Enriched Document Processing](#example-6-enriched-document-processing.md)
- [Example 7: Multi-Format Batch with Filtering](#example-7-multi-format-batch-with-filtering.md)
- [Example 8: Debug Visualization](#example-8-debug-visualization.md)
- [Example 9: Referenced Images](#example-9-referenced-images.md)
- [Example 10: Remote API Processing](#example-10-remote-api-processing.md)
- [Version and Help Commands](#version-and-help-commands.md)
- [Implementation Details](#implementation-details.md)
- [CLI Application Structure](#cli-application-structure.md)
- [Temporary File Handling](#temporary-file-handling.md)
- [Conversion Execution](#conversion-execution.md)
- [Click Compatibility](#click-compatibility.md)
