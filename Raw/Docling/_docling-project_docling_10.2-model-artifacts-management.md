Model Artifacts Management | docling-project/docling | DeepWiki

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

# Model Artifacts Management

Relevant source files

- [docling/cli/models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py)
- [docling/models/auto\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py)
- [docling/models/base\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py)
- [docling/models/code\_formula\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py)
- [docling/models/document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py)
- [docling/models/easyocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py)
- [docling/models/layout\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py)
- [docling/models/page\_assemble\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py)
- [docling/models/page\_preprocessing\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py)
- [docling/models/picture\_description\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py)
- [docling/models/plugins/defaults.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py)
- [docling/models/rapid\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py)
- [docling/models/table\_structure\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py)
- [docling/pipeline/standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py)
- [docling/utils/model\_downloader.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py)
- [tests/test\_document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py)
- [tests/test\_options.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py)

This page documents how Docling manages AI/ML model artifacts, including downloading models from remote sources, configuring local storage paths, and operating in offline mode. Model artifacts include weights, tokenizers, configuration files, and other resources required by various AI models used throughout the pipeline.

For information about model integration and usage within pipelines, see [AI/ML Models](docling-project/docling/4-aiml-models.md). For deployment considerations, see [Docker Deployment](docling-project/docling/10.1-docker-deployment.md).

## Overview

Docling uses multiple AI models that require downloading large binary artifacts before first use. The system provides:

- **Automatic downloading**: Models are downloaded on first use if not found locally
- **Centralized cache**: All models stored in a configurable cache directory
- **Offline mode**: Pre-download models for air-gapped environments
- **CLI tools**: `docling-tools` command for managing model downloads
- **HuggingFace integration**: Primary model source with fallback to ModelScope

The default cache location is `~/.cache/docling/models/`, but this can be customized via configuration or environment variables.

Sources: \[docling/datamodel/settings.py], [docling/utils/model\_downloader.py1-159](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L1-L159) [docling/cli/models.py1-197](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L1-L197)

## Model Download Architecture

```
```

**Diagram: Model Download Flow**

The download system has three entry points: CLI-based pre-download, automatic download on first model use, and explicit programmatic calls. Downloads are routed through either the centralized `download_models()` function or model-specific downloaders. HuggingFace serves as the primary source with ModelScope fallback, while OCR models use specialized sources (ModelScope for RapidOCR, GitHub for EasyOCR).

Sources: [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158) [docling/cli/models.py54-127](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L127) [docling/models/rapid\_ocr\_model.py202-224](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L202-L224) [docling/models/easyocr\_model.py93-127](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py#L93-L127)

## Artifacts Path Resolution

```
```

**Diagram: Artifacts Path Resolution Strategy**

When initializing models, Docling follows a structured resolution process. If `artifacts_path` is provided explicitly, it checks for the new folder structure with `model_repo_folder` subdirectories (e.g., `ds4sd--docling-models/`). If not found, it falls back to the deprecated flat structure while emitting a deprecation warning. If no `artifacts_path` is provided, models are automatically downloaded to the default cache directory from `settings.cache_dir`.

Sources: [docling/models/table\_structure\_model.py33-68](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L33-L68) [docling/models/layout\_model.py49-81](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L49-L81) [docling/models/code\_formula\_model.py73-106](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L73-L106)

## Model Download CLI

The `docling-tools` command provides utilities for pre-downloading models:

### Basic Download Command

```
```

### Available Models

| Model              | Identifier           | Purpose                                     | Default |
| ------------------ | -------------------- | ------------------------------------------- | ------- |
| Layout Model       | `layout`             | Document layout analysis (Heron)            | ✓       |
| TableFormer        | `tableformer`        | Table structure recognition                 | ✓       |
| Code/Formula       | `code_formula`       | LaTeX extraction from images                | ✓       |
| Picture Classifier | `picture_classifier` | Figure classification                       | ✓       |
| RapidOCR           | `rapidocr`           | OCR engine (ONNX/Torch)                     | ✓       |
| EasyOCR            | `easyocr`            | OCR engine (deep learning)                  | ✓       |
| SmolVLM            | `smolvlm`            | Vision-language model (picture description) | -       |
| GraniteDocling     | `granitedocling`     | VLM for document parsing (Transformers)     | -       |
| GraniteDocling MLX | `granitedocling_mlx` | VLM for document parsing (Apple MLX)        | -       |
| SmolDocling        | `smoldocling`        | Compact VLM (Transformers)                  | -       |
| SmolDocling MLX    | `smoldocling_mlx`    | Compact VLM (Apple MLX)                     | -       |
| Granite Vision     | `granite_vision`     | IBM Granite Vision model                    | -       |

### Download Arbitrary HuggingFace Repositories

```
```

Sources: [docling/cli/models.py54-191](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L191) [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158)

## Programmatic Model Downloads

### Central Download Function

The `download_models()` function in `docling.utils.model_downloader` provides programmatic access:

```
```

### Model-Specific Download Methods

Each model class provides a static `download_models()` method:

```
```

Sources: [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158) [docling/models/table\_structure\_model.py91-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L91-L101) [docling/models/layout\_model.py89-102](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L89-L102) [docling/models/rapid\_ocr\_model.py202-224](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L202-L224)

## Model Initialization with Artifacts

```
```

**Diagram: Model Initialization Flow**

All model classes follow a consistent initialization pattern. If the model is disabled, initialization completes immediately with passthrough behavior. For enabled models, the system first checks if `artifacts_path` was provided. If not, models are automatically downloaded to the cache. The path resolution logic handles both the new (with `model_repo_folder`) and deprecated (flat) directory structures. Finally, the appropriate predictor or model instance is loaded using the resolved path.

Sources: [docling/models/table\_structure\_model.py33-89](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L33-L89) [docling/models/layout\_model.py49-87](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L49-L87) [docling/models/code\_formula\_model.py73-115](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L73-L115) [docling/models/rapid\_ocr\_model.py82-200](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L82-L200)

## Offline Mode Configuration

For air-gapped or offline environments, pre-download all required models:

### Pre-Download All Models

```
```

### Configure Pipeline for Offline Use

```
```

### CLI with Offline Artifacts

```
```

Sources: [docling/cli/models.py128-135](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L128-L135) [tests/test\_options.py121-165](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L121-L165)

## HuggingFace Model Download Implementation

```
```

**Diagram: HuggingFace Model Download Process**

The `download_hf_model()` function provides a thin wrapper around HuggingFace Hub's `snapshot_download()`. It standardizes local directory handling by converting repository IDs to folder names (replacing `/` with `--`) and provides ModelScope fallback for regions where HuggingFace is unavailable. The function returns the path to the downloaded repository folder.

Sources: \[docling/models/utils/hf\_model\_download.py]

## Model Repository Folder Structure

Each model type uses a standardized folder structure with a `_model_repo_folder` class attribute:

```
~/.cache/docling/models/
├── ds4sd--docling-models/          # Layout and TableFormer models
│   ├── model_artifacts/
│   │   ├── layout/
│   │   │   └── heron/              # Layout model files
│   │   └── tableformer/
│   │       ├── accurate/           # TableFormer accurate mode
│   │       └── fast/               # TableFormer fast mode
│   └── ...
├── ds4sd--CodeFormulaV2/           # Code/Formula extraction model
│   ├── config.json
│   ├── preprocessor_config.json
│   └── ...
├── ds4sd--DocumentFigureClassifier/  # Picture classifier
│   └── ...
├── RapidOcr/                       # RapidOCR models
│   ├── onnx/
│   │   └── PP-OCRv4/
│   │       ├── det/
│   │       ├── cls/
│   │       └── rec/
│   └── torch/
│       └── PP-OCRv4/
│           └── ...
├── EasyOcr/                        # EasyOCR models
│   ├── craft.pth
│   ├── english_g2.pth
│   └── latin_g2.pth
└── IBM--granite-docling-v1/        # VLM models
    └── ...
```

### Model Repository Folder Mapping

| Model Class                 | `_model_repo_folder`              | HuggingFace Repo                 |
| --------------------------- | --------------------------------- | -------------------------------- |
| `LayoutModel`               | `ds4sd--docling-models`           | `ds4sd/docling-models`           |
| `TableStructureModel`       | `ds4sd--docling-models`           | `ds4sd/docling-models`           |
| `CodeFormulaModel`          | `ds4sd--CodeFormulaV2`            | `ds4sd/CodeFormulaV2`            |
| `DocumentPictureClassifier` | `ds4sd--DocumentFigureClassifier` | `ds4sd/DocumentFigureClassifier` |
| `RapidOcrModel`             | `RapidOcr`                        | ModelScope: `RapidAI/RapidOCR`   |
| `EasyOcrModel`              | `EasyOcr`                         | GitHub: `JaidedAI/EasyOCR`       |

Sources: [docling/models/table\_structure\_model.py29-31](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L29-L31) [docling/models/layout\_model.py28](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L28-L28) [docling/models/code\_formula\_model.py68](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L68-L68) [docling/models/document\_picture\_classifier.py62](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L62-L62) [docling/models/rapid\_ocr\_model.py37](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L37-L37) [docling/models/easyocr\_model.py29](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py#L29-L29)

## Troubleshooting Model Loading

### Common Issues and Solutions

#### Issue: Models Not Found After Download

**Symptom**: Models download successfully but initialization fails with "model not found" errors.

**Cause**: Mismatch between artifacts path structure (flat vs. nested with `model_repo_folder`).

**Solution**:

```
```

#### Issue: Deprecation Warnings

**Symptom**: `DeprecationWarning: The usage of artifacts_path containing directly model_path is deprecated`

**Cause**: Using old flat directory structure without `model_repo_folder` subdirectories.

**Solution**: Reorganize cache to new structure or re-download models using `docling-tools models download`.

#### Issue: Download Failures in China

**Symptom**: Timeouts or connection errors when downloading from HuggingFace.

**Solution**: The system automatically falls back to ModelScope. Ensure ModelScope access is available or use VPN.

#### Issue: Insufficient Disk Space

**Symptom**: Partial downloads or corrupted model files.

**Solution**: Ensure sufficient disk space before downloading. Full model set requires approximately:

- Layout models: \~1.2 GB
- TableFormer: \~500 MB per mode (fast/accurate)
- Code/Formula: \~2.5 GB
- VLM models: 3-8 GB each
- OCR models: \~150-300 MB each

#### Issue: Permission Errors

**Symptom**: `PermissionError` when writing to cache directory.

**Solution**:

```
```

Sources: [docling/models/table\_structure\_model.py55-63](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L55-L63) [docling/models/layout\_model.py73-81](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L73-L81)

## Environment Variables

The following environment variables affect model artifacts management:

| Variable            | Purpose                        | Default            | Example                |
| ------------------- | ------------------------------ | ------------------ | ---------------------- |
| `DOCLING_CACHE_DIR` | Base cache directory           | `~/.cache/docling` | `/data/docling-cache`  |
| `HF_HOME`           | HuggingFace cache (if used)    | Not set            | `~/.cache/huggingface` |
| `HF_HUB_OFFLINE`    | Force HuggingFace offline mode | Not set            | `1`                    |

### Setting Environment Variables

```
```

Sources: \[docling/datamodel/settings.py]

## Model Version Management

Models are versioned through HuggingFace repository revisions:

```
```

### Current Model Versions

| Model              | Repository                       | Revision | Location in Code                                                                                                                             |
| ------------------ | -------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Layout (Heron)     | `ds4sd/docling-models`           | `v2.3.0` | [layout\_model.py96-98](https://github.com/docling-project/docling/blob/f7244a43/layout_model.py#L96-L98)                                    |
| TableFormer        | `ds4sd/docling-models`           | `v2.3.0` | [table\_structure\_model.py95-100](https://github.com/docling-project/docling/blob/f7244a43/table_structure_model.py#L95-L100)               |
| Code/Formula       | `ds4sd/CodeFormulaV2`            | `main`   | [code\_formula\_model.py123-128](https://github.com/docling-project/docling/blob/f7244a43/code_formula_model.py#L123-L128)                   |
| Picture Classifier | `ds4sd/DocumentFigureClassifier` | `v1.0.1` | [document\_picture\_classifier.py110-115](https://github.com/docling-project/docling/blob/f7244a43/document_picture_classifier.py#L110-L115) |

Sources: [docling/models/table\_structure\_model.py91-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L91-L101) [docling/models/layout\_model.py89-102](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L89-L102) [docling/models/code\_formula\_model.py118-129](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L118-L129) [docling/models/document\_picture\_classifier.py106-116](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L106-L116)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Model Artifacts Management](#model-artifacts-management.md)
- [Overview](#overview.md)
- [Model Download Architecture](#model-download-architecture.md)
- [Artifacts Path Resolution](#artifacts-path-resolution.md)
- [Model Download CLI](#model-download-cli.md)
- [Basic Download Command](#basic-download-command.md)
- [Available Models](#available-models.md)
- [Download Arbitrary HuggingFace Repositories](#download-arbitrary-huggingface-repositories.md)
- [Programmatic Model Downloads](#programmatic-model-downloads.md)
- [Central Download Function](#central-download-function.md)
- [Model-Specific Download Methods](#model-specific-download-methods.md)
- [Model Initialization with Artifacts](#model-initialization-with-artifacts.md)
- [Offline Mode Configuration](#offline-mode-configuration.md)
- [Pre-Download All Models](#pre-download-all-models.md)
- [Configure Pipeline for Offline Use](#configure-pipeline-for-offline-use.md)
- [CLI with Offline Artifacts](#cli-with-offline-artifacts.md)
- [HuggingFace Model Download Implementation](#huggingface-model-download-implementation.md)
- [Model Repository Folder Structure](#model-repository-folder-structure.md)
- [Model Repository Folder Mapping](#model-repository-folder-mapping.md)
- [Troubleshooting Model Loading](#troubleshooting-model-loading.md)
- [Common Issues and Solutions](#common-issues-and-solutions.md)
- [Issue: Models Not Found After Download](#issue-models-not-found-after-download.md)
- [Issue: Deprecation Warnings](#issue-deprecation-warnings.md)
- [Issue: Download Failures in China](#issue-download-failures-in-china.md)
- [Issue: Insufficient Disk Space](#issue-insufficient-disk-space.md)
- [Issue: Permission Errors](#issue-permission-errors.md)
- [Environment Variables](#environment-variables.md)
- [Setting Environment Variables](#setting-environment-variables.md)
- [Model Version Management](#model-version-management.md)
- [Current Model Versions](#current-model-versions.md)
