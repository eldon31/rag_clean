Deployment | docling-project/docling | DeepWiki

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

# Deployment

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

This document covers deploying Docling in production environments, focusing on Docker containerization, model artifact management, and performance optimization. Key topics include the `docling-tools` CLI for model management, offline deployment strategies, and environment configuration for scalable document processing systems.

For configuration details, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md). For model specifications, see [AI/ML Models](docling-project/docling/4-aiml-models.md).

## Docker Deployment

Docling supports containerized deployment through Docker, with pre-built images available on Quay.io and GHCR.io. The deployment strategy involves managing AI model artifacts, configuring environment variables, and optimizing resource usage for production workloads.

### Container Architecture

```
```

**Container Build Strategy**: The container starts with a minimal Python base image, installs Docling with required dependencies, configures cache directories via environment variables, and pre-downloads models using `docling-tools`. At runtime, models are loaded on-demand based on the configured pipelines.

Sources: [pyproject.toml1-90](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L90) [docling/cli/models.py54-127](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L127) [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158)

### Environment Configuration

Docling uses several environment variables for deployment configuration:

| Variable              | Purpose                 | Code Reference                   | Production Value     |
| --------------------- | ----------------------- | -------------------------------- | -------------------- |
| `DOCLING_CACHE_DIR`   | Base cache directory    | `settings.cache_dir`             | Persistent volume    |
| `HF_HOME`             | HuggingFace model cache | Used by `transformers`           | Persistent volume    |
| `TORCH_HOME`          | PyTorch model cache     | Used by `torch`                  | Persistent volume    |
| `OMP_NUM_THREADS`     | OpenMP thread limit     | `AcceleratorOptions`             | CPU cores / 2        |
| `DOCLING_NUM_THREADS` | Docling thread budget   | `AcceleratorOptions.num_threads` | CPU cores            |
| `DOCLING_DEVICE`      | Compute device          | `AcceleratorOptions.device`      | `cpu`, `cuda`, `mps` |

The `settings` object in `docling.datamodel.settings` provides centralized configuration management with environment variable overrides.

Sources: [pyproject.toml44-76](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L44-L76) [docling/datamodel/settings.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/settings.py)

## Model Artifacts Management

Docling requires several AI models for document processing. The `docling-tools` CLI provides model download and management capabilities for production deployments.

### Model Download CLI

The `docling-tools download` command pre-downloads models for offline use:

```
```

**CLI Usage**: The `docling-tools download` command supports selective model downloading via the `models` argument or `--all` flag. The `--force` flag enables re-downloading, and `--quiet` suppresses progress output for CI/CD environments.

Sources: [docling/cli/models.py54-136](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L136) [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158)

### Model Storage Architecture

```
```

**Model Storage Conventions**: Each model type defines a `_model_repo_folder` class attribute (e.g., `RapidOcrModel._model_repo_folder = "RapidOcr"`) used for organizing downloaded files. HuggingFace models use a `repo_cache_folder` property that sanitizes repo IDs by replacing `/` with `--`.

Sources: [docling/utils/model\_downloader.py1-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L1-L158) [docling/models/rapid\_ocr\_model.py37-224](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L37-L224) [docling/models/picture\_description\_vlm\_model.py49-53](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L49-L53)

### Offline Mode

For air-gapped or offline deployments, models must be pre-downloaded:

```
```

At runtime, configure Docling to use the offline model cache:

```
```

The `artifacts_path` parameter is passed to model constructors and overrides automatic model downloading. Each model's `__init__` method checks if `artifacts_path` is provided before attempting downloads.

Sources: [docling/cli/models.py54-127](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L127) [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158) [docling/models/rapid\_ocr\_model.py82-150](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L82-L150)

### RapidOCR Model Management

RapidOCR requires additional consideration for offline deployment as it downloads models from ModelScope:

```
```

**RapidOCR Architecture**: RapidOCR supports two backends (`onnxruntime` and `torch`), each requiring separate model files. The `RapidOcrModel._default_models` dictionary maps backend types to model URLs and paths. The `download_models()` static method handles offline preparation.

Sources: [docling/models/rapid\_ocr\_model.py36-224](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L36-L224)

## Performance Considerations

### Threading Configuration

Docling uses multiple threading mechanisms that must be coordinated in production:

| Threading Layer    | Configuration         | Purpose                          |
| ------------------ | --------------------- | -------------------------------- |
| OpenMP             | `OMP_NUM_THREADS`     | Controls NumPy/SciPy parallelism |
| Docling            | `DOCLING_NUM_THREADS` | Controls internal threading      |
| AcceleratorOptions | `num_threads`         | Passed to ONNX models            |

The `AcceleratorOptions` class in pipeline options provides thread budget configuration:

```
```

For CPU-bound workloads, set `OMP_NUM_THREADS` and `num_threads` to half the available cores to prevent oversubscription.

Sources: [docling/models/rapid\_ocr\_model.py82-200](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L82-L200)

### Memory Management

Model loading can consume significant memory. Docling provides several strategies for memory optimization:

1. **Pipeline Caching**: `DocumentConverter` caches pipeline instances by configuration hash to avoid redundant model loading
2. **Lazy Loading**: Models are only loaded when needed for specific document formats
3. **Shared Models**: Multiple `DocumentConverter` instances can share underlying model instances

```
```

The threading lock in model initialization (`_model_init_lock` in [docling/models/picture\_description\_vlm\_model.py21](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L21-L21)) prevents race conditions during parallel initialization.

Sources: [docling/models/picture\_description\_vlm\_model.py20-78](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L20-L78)

### Device Selection

The `AcceleratorDevice` enum supports multiple compute backends:

```
```

The `decide_device()` function in `accelerator_utils` resolves device strings to actual hardware availability.

Sources: [docling/models/rapid\_ocr\_model.py109](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L109-L109) [docling/models/picture\_description\_vlm\_model.py54](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L54-L54)

## Performance Considerations

### CPU Optimization

The Dockerfile configures PyTorch for CPU-only operation to reduce image size and memory requirements:

```
```

This configuration is suitable for CPU-based inference but may require modification for GPU-accelerated deployments.

Sources: [Dockerfile10-12](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L10-L12)

### Memory Management

Environment variables are configured to use temporary storage for framework caches, reducing persistent storage requirements:

```
```

In production, these should be mapped to persistent volumes to avoid model re-downloads on container restarts.

Sources: [Dockerfile14-15](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L14-L15)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Deployment](#deployment.md)
- [Docker Deployment](#docker-deployment.md)
- [Container Architecture](#container-architecture.md)
- [Environment Configuration](#environment-configuration.md)
- [Model Artifacts Management](#model-artifacts-management.md)
- [Model Download CLI](#model-download-cli.md)
- [Model Storage Architecture](#model-storage-architecture.md)
- [Offline Mode](#offline-mode.md)
- [RapidOCR Model Management](#rapidocr-model-management.md)
- [Performance Considerations](#performance-considerations.md)
- [Threading Configuration](#threading-configuration.md)
- [Memory Management](#memory-management.md)
- [Device Selection](#device-selection.md)
- [Performance Considerations](#performance-considerations-1.md)
- [CPU Optimization](#cpu-optimization.md)
- [Memory Management](#memory-management-1.md)
