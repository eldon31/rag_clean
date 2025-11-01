Docker Deployment | docling-project/docling | DeepWiki

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

# Docker Deployment

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

This document covers containerized deployment of Docling using Docker, including Dockerfile configuration, environment setup, model management, and production deployment considerations. For information about model artifacts management and caching strategies, see [Model Artifacts Management](docling-project/docling/10.2-model-artifacts-management.md). For general development and testing setup, see [Development and Testing](docling-project/docling/9-development-and-testing.md).

## Container Architecture Overview

Docling's Docker deployment provides a self-contained environment that includes the Python SDK, AI models, and all necessary system dependencies. The containerization approach enables consistent deployment across different environments while managing the complexity of AI model dependencies.

```
```

**Container Architecture**: The Docker image packages Docling with pre-downloaded AI models and optimized environment settings for container deployment.

Sources: [Dockerfile1-30](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L1-L30)

## Dockerfile Configuration Analysis

The Docling Dockerfile implements a multi-stage approach that optimizes for both functionality and container size:

### Base Image and System Dependencies

The container uses `python:3.11-slim-bookworm` as the base image and installs essential system libraries required for AI processing:

[Dockerfile1-8](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L1-L8) establishes the foundation with:

- OpenGL support (`libgl1`) for image processing
- GLib libraries (`libglib2.0-0`) for low-level operations
- Git, curl, wget for model downloading and updates
- Process utilities (`procps`) for container management

### PyTorch CPU-Only Installation

The installation specifically targets CPU-only PyTorch deployment to minimize container size:

[Dockerfile12](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L12-L12) installs Docling with CPU-optimized dependencies using the PyTorch CPU wheel index. This approach reduces the container size significantly compared to GPU-enabled installations.

### Environment Optimization

Critical environment variables are configured for container environments:

| Variable          | Value   | Purpose                    |
| ----------------- | ------- | -------------------------- |
| `HF_HOME`         | `/tmp/` | HuggingFace cache location |
| `TORCH_HOME`      | `/tmp/` | PyTorch model cache        |
| `OMP_NUM_THREADS` | `4`     | Thread budget control      |

[Dockerfile14-22](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L14-L22) sets these variables to optimize memory usage and prevent thread congestion in containerized environments.

Sources: [Dockerfile1-22](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L1-L22)

## Model Pre-loading Strategy

The Dockerfile implements a model pre-loading strategy to optimize container startup time:

```
```

**Model Pre-loading Flow**: Models are downloaded during container build and can be accessed at runtime through environment variable configuration.

[Dockerfile19](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L19-L19) executes `docling-tools models download` during the build process, ensuring all required AI models are available immediately when the container starts.

The runtime configuration [Dockerfile28-29](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L28-L29) shows how to use pre-loaded models by setting `DOCLING_ARTIFACTS_PATH=/root/.cache/docling/models`.

Sources: [Dockerfile19](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L19-L19) [Dockerfile28-29](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L28-L29)

## Runtime Configuration and Usage

### Basic Container Execution

The container includes a minimal example for immediate testing:

[Dockerfile17](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L17-L17) copies `docs/examples/minimal.py` to `/root/minimal.py`, providing a ready-to-run example that demonstrates basic document conversion functionality.

### Environment Variable Configuration

For production deployment, several environment variables control container behavior:

```
```

### Volume Mounting for Production

Production deployments typically require volume mounting for input/output operations:

```
```

Sources: [Dockerfile17](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L17-L17) [Dockerfile28-29](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L28-L29)

## Performance Considerations

### Thread Management

[Dockerfile22](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L22-L22) sets `OMP_NUM_THREADS=4` to prevent thread congestion in container environments. This setting should be adjusted based on:

- Available CPU cores in the container
- Concurrent container instances
- Memory constraints
- Expected document processing load

### Memory Optimization

The container configuration optimizes memory usage through:

- **Temporary cache locations**: Using `/tmp/` for model caches reduces persistent storage requirements
- **CPU-only PyTorch**: Eliminates GPU memory overhead
- **Slim base image**: Minimizes container footprint

### Model Loading Optimization

The pre-loading strategy eliminates cold start delays but requires consideration of:

- Container image size increase due to embedded models
- Alternative approaches using persistent volumes for model caching
- Trade-offs between startup time and image size

Sources: [Dockerfile14-16](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L14-L16) [Dockerfile22](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L22-L22)

## Production Deployment Patterns

### Stateless Container Design

The Dockerfile implements a stateless container pattern where:

- Models are either pre-loaded or mounted from external volumes
- Processing state is not persisted within the container
- Input/output operations use mounted volumes or network endpoints

### Scaling Considerations

For horizontal scaling, consider:

- Shared model cache volumes across container instances
- Load balancing for document processing requests
- Resource allocation based on document types and processing complexity

### Security Configuration

Container security best practices include:

- Running with non-root user (not implemented in current Dockerfile)
- Limiting container capabilities
- Securing model artifact access
- Network isolation for processing workloads

Sources: [Dockerfile1-30](https://github.com/docling-project/docling/blob/f7244a43/Dockerfile#L1-L30)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Docker Deployment](#docker-deployment.md)
- [Container Architecture Overview](#container-architecture-overview.md)
- [Dockerfile Configuration Analysis](#dockerfile-configuration-analysis.md)
- [Base Image and System Dependencies](#base-image-and-system-dependencies.md)
- [PyTorch CPU-Only Installation](#pytorch-cpu-only-installation.md)
- [Environment Optimization](#environment-optimization.md)
- [Model Pre-loading Strategy](#model-pre-loading-strategy.md)
- [Runtime Configuration and Usage](#runtime-configuration-and-usage.md)
- [Basic Container Execution](#basic-container-execution.md)
- [Environment Variable Configuration](#environment-variable-configuration.md)
- [Volume Mounting for Production](#volume-mounting-for-production.md)
- [Performance Considerations](#performance-considerations.md)
- [Thread Management](#thread-management.md)
- [Memory Optimization](#memory-optimization.md)
- [Model Loading Optimization](#model-loading-optimization.md)
- [Production Deployment Patterns](#production-deployment-patterns.md)
- [Stateless Container Design](#stateless-container-design.md)
- [Scaling Considerations](#scaling-considerations.md)
- [Security Configuration](#security-configuration.md)
