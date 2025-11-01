Installation | docling-project/docling | DeepWiki

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

# Installation

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

## Purpose and Scope

This page provides comprehensive instructions for installing Docling, including system requirements, dependency management, and model artifact setup. It covers base installation, optional feature packages, platform-specific considerations, and offline deployment scenarios.

For information about using Docling after installation, see [Quick Start](docling-project/docling/1.2-quick-start.md). For advanced configuration options, see [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md).

---

## System Requirements

### Python Version

Docling requires **Python 3.9 or higher, but less than 4.0**. The package supports Python 3.9 through 3.13.

```
requires-python = '>=3.9,<4.0'
```

### Platform Support

Docling is tested and supported on:

| Platform    | Architecture                             | Notes                                        |
| ----------- | ---------------------------------------- | -------------------------------------------- |
| **macOS**   | x86\_64, arm64                           | Full support including native OCR (`ocrmac`) |
| **Linux**   | x86\_64, aarch64, armv7l, ppc64le, s390x | vLLM backend only on x86\_64                 |
| **Windows** | x86\_64, i686                            | Full support                                 |

Sources: [pyproject.toml19-32](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L19-L32) [pyproject.toml94-100](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L94-L100)

---

## Base Installation

### Standard Installation

Install Docling using pip or uv:

```
```

or with uv:

```
```

This installs the core package with the following key dependencies:

| Dependency                   | Purpose                                  |
| ---------------------------- | ---------------------------------------- |
| `docling-core`               | Unified document data model and chunking |
| `docling-parse`              | Text extraction from PDFs                |
| `docling-ibm-models`         | AI model implementations                 |
| `pypdfium2`                  | PDF rendering backend                    |
| `rapidocr`                   | Default OCR engine (Python <3.14)        |
| `python-docx`, `python-pptx` | Office document parsing                  |
| `beautifulsoup4`, `lxml`     | HTML/XML parsing                         |
| `openpyxl`                   | Excel file support                       |
| `pillow`                     | Image processing                         |
| `transformers`, `accelerate` | ML model inference                       |

### Installation Architecture

```
```

Sources: [pyproject.toml45-76](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L45-L76) [pyproject.toml91-110](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L91-L110)

---

## Optional Extras

Docling provides several optional feature packages installed via extras syntax:

```
```

### OCR Engines

#### EasyOCR

Deep learning-based OCR engine:

```
```

Installs: `easyocr>=1.7,<2.0`

#### Tesseract OCR

Python binding for Tesseract OCR:

```
```

Installs: `tesserocr>=2.7.1,<3.0.0`

**Note**: Requires Tesseract system libraries. On RHEL/CentOS, also install OSD data:

```
```

#### macOS Native OCR

Native Vision framework OCR (macOS only):

```
```

Installs: `ocrmac>=1.0.0,<2.0.0` (only on Darwin systems)

#### RapidOCR with ONNX Runtime

Optimized OCR with ONNX backend:

```
```

Installs: `rapidocr>=3.3,<4.0.0` + `onnxruntime>=1.7.0,<2.0.0`

**Note**: `rapidocr` is included in base installation for Python <3.14, but without `onnxruntime`. This extra adds ONNX acceleration.

### Vision Language Models (VLM)

For end-to-end document understanding with VLMs:

```
```

Includes:

- `transformers>=4.46.0,<5.0.0` - HuggingFace Transformers backend
- `accelerate>=1.2.1,<2.0.0` - Model acceleration
- `mlx-vlm>=0.3.0,<1.0.0` - Apple Silicon acceleration (macOS arm64, Python ≥3.10)
- `vllm>=0.10.0,<1.0.0` - Optimized inference (Linux x86\_64, Python ≥3.10)
- `qwen-vl-utils>=0.0.11` - Qwen VL utilities

**Platform Requirements**:

- `mlx-vlm`: macOS (arm64) and Python ≥3.10
- `vllm`: Linux (x86\_64) and Python ≥3.10

### Audio Transcription (ASR)

For processing audio files:

```
```

Installs: `openai-whisper>=20250625`

### Optional Extras Summary Table

| Extra       | Purpose                | Platform Constraints                                             | Key Dependencies                          |
| ----------- | ---------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| `easyocr`   | Deep learning OCR      | All                                                              | `easyocr>=1.7`                            |
| `tesserocr` | Tesseract binding      | All (requires system libs)                                       | `tesserocr>=2.7.1`                        |
| `ocrmac`    | Native macOS OCR       | macOS only                                                       | `ocrmac>=1.0.0`                           |
| `rapidocr`  | ONNX-accelerated OCR   | All                                                              | `rapidocr>=3.3`, `onnxruntime>=1.7.0`     |
| `vlm`       | Vision language models | mlx: macOS arm64, Python ≥3.10 vllm: Linux x86\_64, Python ≥3.10 | `transformers>=4.46.0`, `mlx-vlm`, `vllm` |
| `asr`       | Audio transcription    | All                                                              | `openai-whisper>=20250625`                |

Sources: [pyproject.toml91-110](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L91-L110)

---

## Model Artifacts

Docling uses pre-trained AI models for document understanding. Models can be downloaded automatically (online mode) or pre-downloaded for offline deployment.

### Automatic Download (Online Mode)

By default, models are downloaded automatically on first use from HuggingFace or ModelScope. They are cached in:

```
~/.cache/docling/models/
```

or the directory specified by the `DOCLING_CACHE_DIR` environment variable.

### Pre-downloading Models (Offline Mode)

The `docling-tools` CLI provides commands for pre-downloading models.

#### Download Default Models

Download the standard set of models (layout, tableformer, code\_formula, picture\_classifier, rapidocr):

```
```

#### Download Specific Models

```
```

#### Download All Available Models

```
```

#### Available Model Options

| Model                | Description                                  | Default |
| -------------------- | -------------------------------------------- | ------- |
| `layout`             | Heron layout analysis model                  | ✓       |
| `tableformer`        | Table structure recognition                  | ✓       |
| `code_formula`       | Code and formula detection                   | ✓       |
| `picture_classifier` | Image classification                         | ✓       |
| `rapidocr`           | RapidOCR models (both torch and onnxruntime) | ✓       |
| `easyocr`            | EasyOCR models                               | ✗       |
| `smolvlm`            | SmolVLM vision model                         | ✗       |
| `granitedocling`     | GraniteDocling VLM (Transformers)            | ✗       |
| `granitedocling_mlx` | GraniteDocling VLM (MLX, macOS)              | ✗       |
| `smoldocling`        | SmolDocling VLM (Transformers)               | ✗       |
| `smoldocling_mlx`    | SmolDocling VLM (MLX, macOS)                 | ✗       |
| `granite_vision`     | Granite Vision picture description           | ✗       |

#### Download Arbitrary HuggingFace Models

For custom models or repositories:

```
```

### Using Pre-downloaded Models

After downloading, configure Docling to use local artifacts:

**CLI**:

```
```

**Python**:

```
```

### Model Download Architecture

```
```

Sources: [docling/cli/models.py54-136](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L136) [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158)

---

## OCR Engine Selection

Docling's `OcrAutoModel` automatically selects the best available OCR engine based on platform and installed packages.

### Selection Priority

The auto-selection follows this priority order:

```
```

**Priority Order**:

1. **OcrMacModel** (macOS only) - Uses native Vision framework
2. **RapidOcrModel with onnxruntime** - Fast ONNX-accelerated inference
3. **EasyOcrModel** - Deep learning-based OCR
4. **RapidOcrModel with torch** - PyTorch-based inference

If no engine is found, a warning is logged: "No OCR engine found. Please review the install details."

Sources: [docling/models/auto\_ocr\_model.py41-121](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py#L41-L121)

---

## RapidOCR Model Configuration

RapidOCR requires model files to be downloaded. The system automatically manages this through `RapidOcrModel.download_models()`.

### Default Models

RapidOCR uses PP-OCRv4 models from ModelScope:

| Component      | Purpose               | ONNX Path                                                     | Torch Path                                              |
| -------------- | --------------------- | ------------------------------------------------------------- | ------------------------------------------------------- |
| Detection      | Text region detection | `onnx/PP-OCRv4/det/ch_PP-OCRv4_det_infer.onnx`                | `torch/PP-OCRv4/det/ch_PP-OCRv4_det_infer.pth`          |
| Classification | Text orientation      | `onnx/PP-OCRv4/cls/ch_ppocr_mobile_v2.0_cls_infer.onnx`       | `torch/PP-OCRv4/cls/ch_ptocr_mobile_v2.0_cls_infer.pth` |
| Recognition    | Character recognition | `onnx/PP-OCRv4/rec/ch_PP-OCRv4_rec_infer.onnx`                | `torch/PP-OCRv4/rec/ch_PP-OCRv4_rec_infer.pth`          |
| Keys           | Character dictionary  | `paddle/PP-OCRv4/rec/ch_PP-OCRv4_rec_infer/ppocr_keys_v1.txt` | Same                                                    |

### Model Download Process

When `docling-tools download rapidocr` is executed:

1. Both `onnxruntime` and `torch` backend models are downloaded
2. Models are fetched from ModelScope CDN
3. Files are stored in `{cache_dir}/models/RapidOcr/`
4. Model paths follow the structure defined in `_default_models` dictionary

Sources: [docling/models/rapid\_ocr\_model.py38-80](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L38-L80) [docling/models/rapid\_ocr\_model.py202-224](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L202-L224)

---

## Platform-Specific Setup

### macOS

**Native OCR**:

- Install `ocrmac` extra for native Vision framework OCR
- Automatically selected by `OcrAutoModel` on macOS
- Best performance on Apple Silicon with MLX models

**MLX Acceleration**:

- For VLM models on Apple Silicon (arm64), install `vlm` extra
- Enables `mlx-vlm>=0.3.0` (Python ≥3.10 required)
- Provides hardware acceleration for M1/M2/M3 chips

**Example**:

```
```

### Linux

**CUDA Support**:

- Core dependencies support CUDA acceleration
- VLM extra includes `vllm` for optimized inference (x86\_64 only, Python ≥3.10)
- Use `--device=cuda` or `DOCLING_DEVICE=cuda` for GPU acceleration

**System Dependencies for Tesseract**:

```
```

**Example**:

```
```

### Windows

Windows is fully supported for core functionality and most OCR engines.

**Limitations**:

- `vllm` backend not available (Linux x86\_64 only)
- `mlx-vlm` not available (macOS only)

**Example**:

```
```

Sources: [pyproject.toml55](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L55-L55) [pyproject.toml94-99](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L94-L99)

---

## Verification

### Verify Installation

Check that Docling is installed correctly:

```
```

### Verify OCR Engine

Test OCR engine selection:

```
```

Expected log output:

```
INFO: Auto OCR model selected rapidocr with onnxruntime.
```

or

```
INFO: Auto OCR model selected ocrmac.
```

### Verify Model Downloads

Check that models are cached:

```
```

Expected directories:

- `Heron/` - Layout model
- `TableFormer/` - Table structure model
- `RapidOcr/` - OCR models
- Other model directories based on usage

### Verify VLM Installation

If VLM extra is installed:

```
```

Sources: [docling/models/auto\_ocr\_model.py42-120](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py#L42-L120) [docling/cli/models.py54-136](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L136)

---

## Troubleshooting

### Common Issues

**Issue**: `No OCR engine found` warning

**Solution**: Install at least one OCR engine:

```
```

**Issue**: `ImportError: transformers >=4.46 is not installed`

**Solution**: Install VLM extra:

```
```

**Issue**: RapidOCR returns empty results

**Solution**: Ensure models are downloaded:

```
```

**Issue**: Tesseract OSD errors on RHEL

**Solution**: Install OSD data package:

```
```

### Dependency Conflicts

If you encounter dependency conflicts, consider using `uv` for better dependency resolution:

```
```

Sources: [docling/models/rapid\_ocr\_model.py100-106](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L100-L106) [docling/models/picture\_description\_vlm\_model.py56-62](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L56-L62)

---

## Environment Variables

The following environment variables affect installation and runtime behavior:

| Variable              | Purpose                               | Default                    |
| --------------------- | ------------------------------------- | -------------------------- |
| `DOCLING_CACHE_DIR`   | Model cache directory                 | `~/.cache/docling`         |
| `DOCLING_DEVICE`      | Compute device (cpu, cuda, mps, auto) | `auto`                     |
| `OMP_NUM_THREADS`     | OpenMP thread count                   | System default             |
| `DOCLING_NUM_THREADS` | Docling-specific thread count         | Value of `OMP_NUM_THREADS` |

Example:

```
```

Sources: [pyproject.toml1-110](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L110)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Installation](#installation.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Requirements](#system-requirements.md)
- [Python Version](#python-version.md)
- [Platform Support](#platform-support.md)
- [Base Installation](#base-installation.md)
- [Standard Installation](#standard-installation.md)
- [Installation Architecture](#installation-architecture.md)
- [Optional Extras](#optional-extras.md)
- [OCR Engines](#ocr-engines.md)
- [EasyOCR](#easyocr.md)
- [Tesseract OCR](#tesseract-ocr.md)
- [macOS Native OCR](#macos-native-ocr.md)
- [RapidOCR with ONNX Runtime](#rapidocr-with-onnx-runtime.md)
- [Vision Language Models (VLM)](#vision-language-models-vlm.md)
- [Audio Transcription (ASR)](#audio-transcription-asr.md)
- [Optional Extras Summary Table](#optional-extras-summary-table.md)
- [Model Artifacts](#model-artifacts.md)
- [Automatic Download (Online Mode)](#automatic-download-online-mode.md)
- [Pre-downloading Models (Offline Mode)](#pre-downloading-models-offline-mode.md)
- [Download Default Models](#download-default-models.md)
- [Download Specific Models](#download-specific-models.md)
- [Download All Available Models](#download-all-available-models.md)
- [Available Model Options](#available-model-options.md)
- [Download Arbitrary HuggingFace Models](#download-arbitrary-huggingface-models.md)
- [Using Pre-downloaded Models](#using-pre-downloaded-models.md)
- [Model Download Architecture](#model-download-architecture.md)
- [OCR Engine Selection](#ocr-engine-selection.md)
- [Selection Priority](#selection-priority.md)
- [RapidOCR Model Configuration](#rapidocr-model-configuration.md)
- [Default Models](#default-models.md)
- [Model Download Process](#model-download-process.md)
- [Platform-Specific Setup](#platform-specific-setup.md)
- [macOS](#macos.md)
- [Linux](#linux.md)
- [Windows](#windows.md)
- [Verification](#verification.md)
- [Verify Installation](#verify-installation.md)
- [Verify OCR Engine](#verify-ocr-engine.md)
- [Verify Model Downloads](#verify-model-downloads.md)
- [Verify VLM Installation](#verify-vlm-installation.md)
- [Troubleshooting](#troubleshooting.md)
- [Common Issues](#common-issues.md)
- [Dependency Conflicts](#dependency-conflicts.md)
- [Environment Variables](#environment-variables.md)
