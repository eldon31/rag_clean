Command Line Interface | docling-project/docling | DeepWiki

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

# Command Line Interface

Relevant source files

- [.github/SECURITY.md](https://github.com/docling-project/docling/blob/f7244a43/.github/SECURITY.md)
- [CHANGELOG.md](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md)
- [CITATION.cff](https://github.com/docling-project/docling/blob/f7244a43/CITATION.cff)
- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [pyproject.toml](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml)
- [uv.lock](https://github.com/docling-project/docling/blob/f7244a43/uv.lock)

This document covers Docling's command-line interface tools for document conversion and model management. The CLI provides access to Docling's document processing capabilities through two main commands: the primary `docling` command for document conversion and the `docling-tools` command for model artifact management.

For information about using Docling programmatically, see [Python SDK](docling-project/docling/7-python-sdk.md). For details about the underlying processing pipelines, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md).

## Overview

Docling provides two CLI entry points defined in [pyproject.toml86-88](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L86-L88):

- **`docling`** - Main document conversion interface supporting batch processing of various document formats
- **`docling-tools`** - Utility for downloading and managing AI model artifacts

Both tools are built using the Typer framework and provide comprehensive help through the `--help` flag.

**CLI Entry Points Architecture**

```
```

Sources: [pyproject.toml86-88](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L86-L88) [docling/cli/main.py136-141](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L136-L141)

## Document Conversion Command

The primary `docling convert` command processes documents through a comprehensive interface supporting multiple input/output formats, processing pipelines, and configuration options.

### Core Parameters

The CLI accepts the following main parameter categories:

**Input/Output Configuration:**

- `input_sources` - File paths, directories, or URLs to process
- `--from` - Input format filtering ([docling/cli/main.py303-307](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L303-L307))
- `--to` - Output format selection ([docling/cli/main.py308-310](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L308-L310))
- `--output` - Output directory ([docling/cli/main.py432-434](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L432-L434))

**Processing Pipeline Options:**

- `--pipeline` - Choose between `standard`, `vlm`, or `asr` pipelines ([docling/cli/main.py330-333](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L330-L333))
- `--vlm-model` - VLM model selection for vision-language processing ([docling/cli/main.py334-337](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L334-L337))
- `--asr-model` - ASR model for audio processing ([docling/cli/main.py338-341](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L338-L341))

**OCR Configuration:**

- `--ocr/--no-ocr` - Enable/disable OCR processing ([docling/cli/main.py342-347](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L342-L347))
- `--force-ocr` - Replace existing text with OCR ([docling/cli/main.py348-354](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L348-L354))
- `--ocr-engine` - OCR engine selection ([docling/cli/main.py355-365](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L355-L365))
- `--ocr-lang` - Language configuration ([docling/cli/main.py366-372](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L366-L372))

### Processing Pipeline Selection

**Pipeline Processing Flow**

```
```

Sources: [docling/cli/main.py330-333](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L330-L333) [docling/datamodel/pipeline\_options.py347-351](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L347-L351)

### Format Support and Export Options

The CLI supports multiple input formats through the `FormatToExtensions` mapping and provides various export options:

**Supported Output Formats:**

- **JSON** - Complete document structure with metadata ([docling/cli/main.py207-212](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L207-L212))
- **HTML** - Web-viewable format with optional split-page view ([docling/cli/main.py215-246](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L215-L246))
- **Markdown** - Human-readable text format ([docling/cli/main.py259-264](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L259-L264))
- **TXT** - Plain text extraction ([docling/cli/main.py249-256](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L249-L256))
- **DocTags** - Document token format ([docling/cli/main.py267-270](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L267-L270))

**Image Export Modes:** The `--image-export-mode` parameter controls how images are handled in exports ([docling/cli/main.py323-329](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L323-L329)):

- `PLACEHOLDER` - Mark image positions only
- `EMBEDDED` - Base64 encoded images inline
- `REFERENCED` - External PNG files with references

### Advanced Configuration

**PDF Processing Options:**

- `--pdf-backend` - Backend selection (DLPARSE\_V4, DLPARSE\_V2, PYPDFIUM2) ([docling/cli/main.py373-375](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L373-L375))
- `--table-mode` - Table structure model mode (FAST/ACCURATE) ([docling/cli/main.py376-379](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L376-L379))
- `--enrich-code` - Enable code enrichment ([docling/cli/main.py380-383](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L380-L383))
- `--enrich-formula` - Enable formula enrichment ([docling/cli/main.py384-387](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L384-L387))

**Performance and Resource Control:**

- `--num-threads` - Threading configuration ([docling/cli/main.py478](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L478-L478))
- `--device` - Accelerator device selection ([docling/cli/main.py479-481](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L479-L481))
- `--document-timeout` - Per-document timeout ([docling/cli/main.py471-477](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L471-L477))
- `--abort-on-error` - Error handling behavior ([docling/cli/main.py424-431](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L424-L431))

Sources: [docling/cli/main.py294-500](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L294-L500) [docling/datamodel/pipeline\_options.py232-239](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L232-L239)

## CLI Processing Workflow

The main processing workflow in the `convert` command follows this pattern:

**CLI Processing Implementation**

```
```

Sources: [docling/cli/main.py294-500](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L294-L500) [docling/cli/main.py186-285](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L186-L285)

## Command Examples

**Basic Document Conversion:**

```
```

**Batch Processing with VLM Pipeline:**

```
```

**OCR Configuration:**

```
```

**Advanced PDF Processing:**

```
```

Sources: [docling/cli/main.py294-500](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L294-L500)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Command Line Interface](#command-line-interface.md)
- [Overview](#overview.md)
- [Document Conversion Command](#document-conversion-command.md)
- [Core Parameters](#core-parameters.md)
- [Processing Pipeline Selection](#processing-pipeline-selection.md)
- [Format Support and Export Options](#format-support-and-export-options.md)
- [Advanced Configuration](#advanced-configuration.md)
- [CLI Processing Workflow](#cli-processing-workflow.md)
- [Command Examples](#command-examples.md)
