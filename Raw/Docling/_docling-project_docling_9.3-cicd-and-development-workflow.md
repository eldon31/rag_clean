CI/CD and Development Workflow | docling-project/docling | DeepWiki

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

# CI/CD and Development Workflow

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

This document covers the continuous integration and continuous deployment (CI/CD) pipeline and development workflow for the Docling project. It details the automated testing, quality assurance, security scanning, version management, documentation generation, and package distribution processes that ensure code quality and reliable releases.

For information about the testing framework and test data organization, see [Testing Framework](docling-project/docling/9.1-testing-framework.md) and [Ground Truth Data](docling-project/docling/9.2-ground-truth-data.md).

## CI/CD Pipeline Overview

The Docling project employs a comprehensive CI/CD pipeline built on GitHub Actions that ensures code quality, runs extensive tests across multiple Python versions, and automates documentation and package distribution.

```
```

**Sources:** [.github/workflows/checks.yml1-118](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L1-L118) [README.md13-26](https://github.com/docling-project/docling/blob/f7244a43/README.md#L13-L26)

## GitHub Actions Workflow Configuration

The main CI/CD workflow is defined in `checks.yml` and includes three primary jobs: `run-checks`, `build-package`, and `test-package`.

### Workflow Jobs Architecture

```
```

### Environment Configuration

The workflow configures several environment variables and caching strategies:

| Configuration             | Purpose                             | Implementation         |
| ------------------------- | ----------------------------------- | ---------------------- |
| `HF_HUB_DOWNLOAD_TIMEOUT` | Hugging Face model download timeout | Set to 60 seconds      |
| `HF_HUB_ETAG_TIMEOUT`     | Hugging Face ETag timeout           | Set to 60 seconds      |
| `UV_FROZEN`               | Lock dependency versions            | Set to "1"             |
| `TESSDATA_PREFIX`         | Tesseract data path                 | Dynamically determined |

**Sources:** [.github/workflows/checks.yml12-29](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L12-L29)

### Multi-Version Testing Matrix

The pipeline tests against five Python versions to ensure broad compatibility:

```
```

**Sources:** [.github/workflows/checks.yml20-22](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L20-L22) [.github/workflows/checks.yml50-71](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L50-L71)

## Development Tools and Quality Assurance

### Pre-commit Hook Integration

The project uses `pre-commit` for automated code quality enforcement. The workflow includes pre-commit cache optimization and runs all configured hooks:

```
```

**Sources:** [.github/workflows/checks.yml40-49](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L40-L49) [README.md18-20](https://github.com/docling-project/docling/blob/f7244a43/README.md#L18-L20)

### Testing and Coverage

The testing pipeline uses `pytest` with coverage reporting and uploads results to Codecov:

| Component          | Purpose                      | Configuration                       |
| ------------------ | ---------------------------- | ----------------------------------- |
| `pytest`           | Unit and integration testing | `-v --cov=docling --cov-report=xml` |
| `codecov`          | Coverage reporting           | Uploads to codecov.io               |
| Example validation | Real-world usage testing     | Runs all example scripts            |

**Sources:** [.github/workflows/checks.yml50-58](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L50-L58)

### Example Script Validation

The CI pipeline validates example scripts to ensure documentation accuracy, with selective execution based on script characteristics. Some examples are skipped in CI due to external dependencies or resource requirements.

**Sources:** [.github/workflows/checks.yml59-71](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L59-L71)

## Documentation Generation Pipeline

### MkDocs Configuration

The documentation system uses MkDocs with Material theme and extensive plugin integration:

```
```

### Theme and Extension Configuration

The documentation uses Material theme with comprehensive feature enablement:

| Feature Category | Enabled Features                                                  |
| ---------------- | ----------------------------------------------------------------- |
| Content          | `content.tabs.link`, `content.code.annotate`, `content.code.copy` |
| Navigation       | `navigation.footer`, `navigation.tabs`, `navigation.indexes`      |
| Search           | `search.suggest`                                                  |
| TOC              | `toc.follow`                                                      |

**Sources:** [mkdocs.yml36-54](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L36-L54)

### Plugin Configuration

Key plugins and their purposes:

| Plugin           | Configuration                        | Purpose                      |
| ---------------- | ------------------------------------ | ---------------------------- |
| `mkdocs-jupyter` | Default settings                     | Jupyter notebook integration |
| `mkdocstrings`   | Python handler with Pydantic support | API documentation generation |
| `mkdocs-click`   | Default settings                     | CLI documentation            |

**Sources:** [mkdocs.yml176-187](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml#L176-L187)

## Package Building and Distribution

### Build Process

The package building uses `uv build` with validation steps:

```
```

### Package Validation

The built package undergoes validation to ensure proper installation and functionality:

| Validation Step     | Purpose                   | Command                     |
| ------------------- | ------------------------- | --------------------------- |
| Wheel content check | Verify package contents   | `unzip -l dist/*.whl`       |
| Installation test   | Validate pip installation | `uv pip install dist/*.whl` |
| CLI functionality   | Ensure CLI works          | `docling --help`            |

**Sources:** [.github/workflows/checks.yml72-118](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L72-L118)

## Development Workflow

### Developer Environment Setup

The development workflow relies on `uv` for dependency management and environment setup:

```
```

### Quality Assurance Integration

The project integrates multiple quality assurance tools as evidenced by the badges and configuration:

| Tool        | Purpose                     | Integration         |
| ----------- | --------------------------- | ------------------- |
| Ruff        | Code linting and formatting | Pre-commit and CI   |
| Pydantic v2 | Data validation             | Runtime and testing |
| Pre-commit  | Git hook automation         | Local and CI        |
| UV          | Fast dependency management  | All environments    |
| Codecov     | Coverage reporting          | CI pipeline         |

**Sources:** [README.md17-21](https://github.com/docling-project/docling/blob/f7244a43/README.md#L17-L21) [.github/workflows/checks.yml35-49](https://github.com/docling-project/docling/blob/f7244a43/.github/workflows/checks.yml#L35-L49)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [CI/CD and Development Workflow](#cicd-and-development-workflow.md)
- [CI/CD Pipeline Overview](#cicd-pipeline-overview.md)
- [GitHub Actions Workflow Configuration](#github-actions-workflow-configuration.md)
- [Workflow Jobs Architecture](#workflow-jobs-architecture.md)
- [Environment Configuration](#environment-configuration.md)
- [Multi-Version Testing Matrix](#multi-version-testing-matrix.md)
- [Development Tools and Quality Assurance](#development-tools-and-quality-assurance.md)
- [Pre-commit Hook Integration](#pre-commit-hook-integration.md)
- [Testing and Coverage](#testing-and-coverage.md)
- [Example Script Validation](#example-script-validation.md)
- [Documentation Generation Pipeline](#documentation-generation-pipeline.md)
- [MkDocs Configuration](#mkdocs-configuration.md)
- [Theme and Extension Configuration](#theme-and-extension-configuration.md)
- [Plugin Configuration](#plugin-configuration.md)
- [Package Building and Distribution](#package-building-and-distribution.md)
- [Build Process](#build-process.md)
- [Package Validation](#package-validation.md)
- [Development Workflow](#development-workflow.md)
- [Developer Environment Setup](#developer-environment-setup.md)
- [Quality Assurance Integration](#quality-assurance-integration.md)
