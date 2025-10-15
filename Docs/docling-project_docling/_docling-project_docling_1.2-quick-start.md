Quick Start | docling-project/docling | DeepWiki

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

# Quick Start

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

This page provides simple, working code examples to get you started with Docling immediately. It covers the most common use cases: basic document conversion, using vision language models, and CLI usage. For detailed installation instructions, see [Installation](docling-project/docling/1.1-installation.md). For advanced configuration options, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md) and [Advanced Options](https://docling-project.github.io/docling/usage/advanced_options/).

## Prerequisites

Ensure Docling is installed before proceeding:

```
```

For VLM features or specific OCR engines, additional extras may be required. See [Installation](docling-project/docling/1.1-installation.md) for details.

## Basic Document Conversion

The simplest way to convert a document is to create a `DocumentConverter` and call `convert()`:

```
```

**What this does:**

1. `DocumentConverter` initializes with default format options for all supported formats
2. `convert()` detects the input format, selects the appropriate backend and pipeline
3. Returns a `ConversionResult` containing a `DoclingDocument`
4. `export_to_markdown()` serializes the document to Markdown format

### Conversion Flow Diagram

```
```

**Sources:** [docling/document\_converter.py228-245](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L228-L245) [docling/datamodel/document.py280-338](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L280-L338) [README.md69-77](https://github.com/docling-project/docling/blob/f7244a43/README.md#L69-L77)

## Output Formats

The `DoclingDocument` supports multiple export formats:

| Method                        | Output Format | Description                        |
| ----------------------------- | ------------- | ---------------------------------- |
| `export_to_markdown()`        | Markdown      | Human-readable text with structure |
| `export_to_json()`            | JSON          | Complete structured document data  |
| `export_to_html()`            | HTML          | Web-ready HTML output              |
| `export_to_document_tokens()` | DocTags       | Structured token sequence          |

Example with JSON export:

```
```

**Sources:** [docling/cli/main.py191-275](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L191-L275) [docling/datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L215)

## VLM Pipeline Usage

Docling supports vision-language models for end-to-end document processing. The `VlmPipeline` processes pages using models like GraniteDocling or SmolDocling:

```
```

### VLM with MLX Acceleration (macOS)

On Apple Silicon, use MLX for faster inference:

```
```

**Sources:** [docs/examples/minimal\_vlm\_pipeline.py1-71](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py#L1-L71) [docs/usage/vision\_models.md11-38](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L11-L38)

## Pipeline Selection Diagram

```
```

**Sources:** [docling/document\_converter.py132-182](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L132-L182) [docling/document\_converter.py351-378](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L351-L378) [docling/datamodel/pipeline\_options.py273-368](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L273-L368)

## CLI Usage

Docling provides a command-line interface for quick conversions without writing code:

### Basic Conversion

```
```

### VLM Pipeline via CLI

```
```

### Common CLI Options

```
```

### CLI Command Structure

```
```

**Sources:** [docling/cli/main.py298-816](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L298-L816) [docs/usage/index.md26-39](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L26-L39) [README.md84-98](https://github.com/docling-project/docling/blob/f7244a43/README.md#L84-L98)

## Processing Multiple Documents

Convert multiple documents in batch:

```
```

**Sources:** [docling/document\_converter.py247-283](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L247-L283)

## Table Extraction

Docling automatically extracts tables. Access them from the `DoclingDocument`:

```
```

**Sources:** [docling\_core.types.doc](https://github.com/docling-project/docling/blob/f7244a43/docling_core.types.doc#LNaN-LNaN) [docling/datamodel/document.py24-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L24-L32)

## Configuration Options Summary

Key configuration classes for customizing conversion:

| Class                   | Purpose                       | Used For                            |
| ----------------------- | ----------------------------- | ----------------------------------- |
| `PdfPipelineOptions`    | Configure PDF processing      | OCR, table extraction, enrichment   |
| `VlmPipelineOptions`    | Configure VLM models          | Model selection, prompts, inference |
| `AsrPipelineOptions`    | Configure audio transcription | Whisper model selection             |
| `OcrOptions`            | Configure OCR engines         | Engine type, languages, parameters  |
| `TableStructureOptions` | Configure table extraction    | Accuracy vs speed tradeoffs         |
| `AcceleratorOptions`    | Configure hardware            | Device (CPU/CUDA/MPS), threads      |

Example with custom options:

```
```

**Sources:** [docling/datamodel/pipeline\_options.py273-384](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L273-L384) [docling/cli/main.py619-697](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L619-L697)

## Error Handling

Control error behavior during conversion:

```
```

**Sources:** [docling/document\_converter.py227-245](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L227-L245) [docling/datamodel/base\_models.py45-51](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L45-L51)

## Next Steps

- For installation details and optional dependencies, see [Installation](docling-project/docling/1.1-installation.md)
- For format-specific guidance, see [Supported Formats](https://docling-project.github.io/docling/usage/supported_formats/)
- For detailed configuration, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md)
- For advanced pipeline usage, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md)
- For integration examples, see [Framework Integrations](docling-project/docling/8.3-framework-integrations.md)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Quick Start](#quick-start.md)
- [Prerequisites](#prerequisites.md)
- [Basic Document Conversion](#basic-document-conversion.md)
- [Conversion Flow Diagram](#conversion-flow-diagram.md)
- [Output Formats](#output-formats.md)
- [VLM Pipeline Usage](#vlm-pipeline-usage.md)
- [VLM with MLX Acceleration (macOS)](#vlm-with-mlx-acceleration-macos.md)
- [Pipeline Selection Diagram](#pipeline-selection-diagram.md)
- [CLI Usage](#cli-usage.md)
- [Basic Conversion](#basic-conversion.md)
- [VLM Pipeline via CLI](#vlm-pipeline-via-cli.md)
- [Common CLI Options](#common-cli-options.md)
- [CLI Command Structure](#cli-command-structure.md)
- [Processing Multiple Documents](#processing-multiple-documents.md)
- [Table Extraction](#table-extraction.md)
- [Configuration Options Summary](#configuration-options-summary.md)
- [Error Handling](#error-handling.md)
- [Next Steps](#next-steps.md)
