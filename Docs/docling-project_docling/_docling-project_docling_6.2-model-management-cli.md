Model Management CLI | docling-project/docling | DeepWiki

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

# Model Management CLI

Relevant source files

- [.github/SECURITY.md](https://github.com/docling-project/docling/blob/f7244a43/.github/SECURITY.md)
- [CHANGELOG.md](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md)
- [CITATION.cff](https://github.com/docling-project/docling/blob/f7244a43/CITATION.cff)
- [docling/cli/models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py)
- [docling/models/auto\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py)
- [docling/models/picture\_description\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py)
- [docling/models/plugins/defaults.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py)
- [docling/models/rapid\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py)
- [docling/utils/model\_downloader.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py)
- [pyproject.toml](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml)
- [uv.lock](https://github.com/docling-project/docling/blob/f7244a43/uv.lock)

This document covers the `docling-tools` command-line interface, which provides model management capabilities for Docling's AI/ML pipeline. The `docling-tools` CLI handles downloading, caching, and managing model artifacts required by Docling's document processing backends.

For information about document conversion using the main CLI, see [Document Conversion CLI](docling-project/docling/6.1-document-conversion-cli.md).

## Overview

The `docling-tools` CLI is the dedicated model management interface for Docling, providing utilities to download and manage AI model artifacts used throughout the document processing pipeline. It serves as the primary tool for setting up and maintaining the machine learning models that power Docling's advanced document understanding capabilities.

**CLI Architecture**

```
```

**Sources:** [pyproject.toml86-88](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L86-L88) [Dockerfile19](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L19-L19)

## Model Download Command

The primary function of `docling-tools` is the `models download` command, which handles downloading and caching model artifacts required by Docling's processing pipelines.

**Model Download Workflow**

```
```

**Sources:** [Dockerfile19](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L19-L19) [CHANGELOG.md76](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md#L76-L76)

## HuggingFace Model Integration

The `docling-tools` CLI provides specialized functionality for downloading arbitrary HuggingFace models, particularly for VLM (Vision Language Model) backends used in advanced document understanding pipelines.

**HuggingFace Download Architecture**

```
```

**Sources:** [CHANGELOG.md76](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md#L76-L76) [pyproject.toml53](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L53-L53)

## Artifact Path Management

The CLI provides flexible configuration for model artifact storage locations through environment variables and command-line options, enabling deployment-specific model management strategies.

| Configuration Method     | Description                   | Priority |
| ------------------------ | ----------------------------- | -------- |
| `DOCLING_ARTIFACTS_PATH` | Environment variable override | Highest  |
| `--artifacts-path`       | CLI argument (if available)   | Medium   |
| Default cache            | `~/.cache/docling/models`     | Lowest   |

**Environment Integration**

```
```

**Sources:** [Dockerfile14-15](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L14-L15) [Dockerfile28-29](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L28-L29)

## Model Type Management

The `docling-tools` CLI manages different categories of AI models used throughout Docling's processing pipeline, each with specific download and caching strategies.

**Model Category Breakdown**

```
```

**Sources:** [pyproject.toml49](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L49-L49) [pyproject.toml55](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L55-L55) [pyproject.toml93-99](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L93-L99)

## Pipeline Integration

The model management CLI integrates tightly with Docling's document processing pipelines, ensuring that required models are available before pipeline initialization.

**Model-to-Pipeline Mapping**

```
```

**Sources:** [pyproject.toml107-109](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L107-L109) [docling/backend/docling\_parse\_v4\_backend.py1-250](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/docling_parse_v4_backend.py#L1-L250)

## Container Deployment Integration

The `docling-tools` CLI is designed to work seamlessly in containerized environments, with pre-download capabilities for building container images with embedded model artifacts.

**Container Model Management**

```
```

**Sources:** [Dockerfile19](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L19-L19) [Dockerfile28-29](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L28-L29)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Model Management CLI](#model-management-cli.md)
- [Overview](#overview.md)
- [Model Download Command](#model-download-command.md)
- [HuggingFace Model Integration](#huggingface-model-integration.md)
- [Artifact Path Management](#artifact-path-management.md)
- [Model Type Management](#model-type-management.md)
- [Pipeline Integration](#pipeline-integration.md)
- [Container Deployment Integration](#container-deployment-integration.md)
