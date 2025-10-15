docling-project/docling | DeepWiki

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

# Overview

Relevant source files

- [.github/SECURITY.md](https://github.com/docling-project/docling/blob/f7244a43/.github/SECURITY.md)
- [CHANGELOG.md](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md)
- [CITATION.cff](https://github.com/docling-project/docling/blob/f7244a43/CITATION.cff)
- [README.md](https://github.com/docling-project/docling/blob/f7244a43/README.md)
- [docs/examples/minimal\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py)
- [docs/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md)
- [docs/usage/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md)
- [docs/usage/mcp.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md)
- [docs/usage/vision\_models.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md)
- [mkdocs.yml](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml)
- [pyproject.toml](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml)
- [uv.lock](https://github.com/docling-project/docling/blob/f7244a43/uv.lock)

## Purpose and Scope

This document provides a high-level technical overview of Docling, a document parsing and conversion system. It explains the system's purpose, core architecture, key components, and processing flow. This overview serves as an entry point for understanding how Docling transforms diverse document formats into structured, unified representations.

For installation instructions, see [Installation](docling-project/docling/1.1-installation.md). For quick start examples, see [Quick Start](docling-project/docling/1.2-quick-start.md). For detailed architecture concepts, see [Core Architecture](docling-project/docling/2-core-architecture.md).

## System Purpose

Docling is an SDK and CLI for parsing documents in multiple formats (PDF, DOCX, PPTX, XLSX, HTML, images, audio, and more) into a unified `DoclingDocument` representation. The system is designed to power downstream workflows such as generative AI applications, RAG systems, and document analysis pipelines.

Key capabilities:

- **Format-agnostic parsing**: Handles 15+ document formats through specialized backends
- **Advanced PDF understanding**: Page layout detection, reading order, table structure, formula extraction, OCR integration
- **Unified output**: All formats convert to `DoclingDocument`, which exports to Markdown, HTML, JSON, or DocTags
- **AI model integration**: OCR engines, layout models, table structure models, vision-language models, and enrichment models
- **Local execution**: Supports air-gapped environments and sensitive data processing
- **Framework integrations**: Native support for LangChain, LlamaIndex, Haystack, and other AI frameworks

Sources: [pyproject.toml1-80](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L80) [README.md28-43](https://github.com/docling-project/docling/blob/f7244a43/README.md#L28-L43) [docs/index.md20-34](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md#L20-L34)

## Core Architecture

Docling implements a layered architecture with clear separation between user interfaces, orchestration logic, processing pipelines, and model integration.

### System Architecture Diagram

```
```

Sources: Diagram 1 from high-level overview, [pyproject.toml84-89](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L84-L89)

### Component Overview

| Layer               | Key Classes                                                            | Purpose                                                 |
| ------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- |
| **User Interfaces** | `CLI (docling)`, `DocumentConverter`, `DocumentExtractor`              | Entry points for document processing                    |
| **Orchestration**   | `DocumentConverter`, `FormatOption` mapping                            | Routes documents to appropriate pipelines and backends  |
| **Pipelines**       | `BasePipeline`, `StandardPdfPipeline`, `VlmPipeline`, `SimplePipeline` | Implements format-specific processing strategies        |
| **Backends**        | `DoclingParseV4Backend`, `MsWordBackend`, `HTMLBackend`, etc.          | Provides format-specific document readers               |
| **Models**          | `LayoutModel`, `TableStructureModel`, `OcrAutoModel`, VLM models       | AI/ML models for document understanding                 |
| **Output**          | `DoclingDocument`                                                      | Unified representation that exports to multiple formats |

Sources: [pyproject.toml84-90](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L84-L90) Diagram 1 from high-level overview

## Key Components

### User Interfaces

**CLI (`docling` command)**

- Entry point: [pyproject.toml88](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L88-L88)
- Implementation: `docling.cli.main:app`
- Provides command-line interface for document conversion with extensive options

**Python SDK**

- `DocumentConverter`: Main class for document conversion
- `DocumentExtractor`: Schema-based structured extraction (beta)
- Used programmatically in Python applications

**MCP Server**

- Model Context Protocol server for AI agent integration
- Enables Docling capabilities in agentic AI systems
- See [MCP Server](docling-project/docling/6.2-model-management-cli.md) for details

Sources: [pyproject.toml84-89](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L84-L89) [README.md84-97](https://github.com/docling-project/docling/blob/f7244a43/README.md#L84-L97) [docs/usage/mcp.md1-31](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md#L1-L31)

### Core Orchestration Layer

**DocumentConverter**

- Central orchestration class that routes documents through the system
- Maintains `format_to_options` dictionary mapping `InputFormat` to `FormatOption` instances
- Implements pipeline caching via `_initialized_pipelines` dictionary
- Key methods: `convert()`, `convert_all()`, `_get_pipeline()`

**FormatOption Classes**

- `PdfFormatOption`, `WordFormatOption`, `HtmlFormatOption`, etc.
- Each pairs an `InputFormat` with a `pipeline_cls` (pipeline class) and `backend_cls` (backend class)
- Contains format-specific `PipelineOptions`

**Format Detection**

- Function `_guess_format()` uses MIME types, file extensions, and content analysis
- Routes to correct backend for processing

Sources: Diagram 2 from high-level overview, Diagram 6 from high-level overview

### Processing Pipelines

All pipelines inherit from `BasePipeline` which defines a three-phase execution model:

```
```

**Pipeline Execution Phases**:

1. `_build_document`: Extract raw structure from backend
2. `_assemble_document`: Construct hierarchical document representation
3. `_enrich_document`: Apply enrichment models (code detection, picture classification, etc.)

**Key Pipeline Implementations**:

- `StandardPdfPipeline`: Sequential 5-stage processing (preprocess → OCR → layout → table → assemble)
- `ThreadedStandardPdfPipeline`: Default for PDFs, uses multi-threading with bounded queues
- `VlmPipeline`: End-to-end processing with vision-language models
- `SimplePipeline`: Direct conversion for DOCX, HTML, Markdown
- `AsrPipeline`: Audio transcription using Whisper models
- `ExtractionVlmPipeline`: Schema-based data extraction (beta)

Sources: Diagram 4 from high-level overview, [README.md38-46](https://github.com/docling-project/docling/blob/f7244a43/README.md#L38-L46)

### Document Backends

Backends provide format-specific document readers implementing the `AbstractDocumentBackend` interface.

**PDF Backends**:

- `DoclingParseV4Backend`: Current default, uses `docling-parse` library for character-level text extraction
- `DoclingParseV2Backend`: Legacy sanitized format
- `PyPdfiumBackend`: Pure `pypdfium2` implementation

**Office Format Backends**:

- `MsWordBackend`: Uses `python-docx` library
- `MsExcelBackend`: Uses `openpyxl` library
- `MsPowerpointBackend`: Uses `python-pptx` library

**Web and Markup Backends**:

- `HTMLBackend`: Uses `BeautifulSoup` parser
- `MarkdownBackend`: Uses `marko` parser
- `AsciiDocBackend`: AsciiDoc support

**Specialized Backends**:

- `JATSBackend`: Scientific articles in JATS XML format
- `METSBackend`: Google Books METS archives
- `USPTOBackend`: Patent documents
- `ImageBackend`: Image files (PNG, JPEG, TIFF, WEBP, etc.)
- `AudioBackend`: Audio files (WAV, MP3)
- `WebVTTBackend`: Subtitle files

Sources: Diagram 3 from high-level overview, [pyproject.toml45-76](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L45-L76)

### AI/ML Model Layer

The model layer uses a plugin system for discovery and registration.

**OCR Models**:

- `OcrAutoModel`: Automatic selection with fallback logic
- `RapidOcrModel`: ONNX/Torch backends (default on most platforms)
- `EasyOcrModel`: Deep learning OCR
- `TesseractOcrModel`: Tesseract binding
- `OcrMacModel`: macOS native OCR

**Layout and Table Models**:

- `LayoutModel`: Heron model (default), DocLayoutModel (legacy)
- `TableStructureModel`: TableFormer with FAST/ACCURATE modes
- `PagePreprocessingModel`: Image generation and cell extraction
- `PageAssembleModel`: Hierarchy construction

**Vision-Language Models**:

- `HuggingFaceTransformersVlmModel`: AutoModel + Transformers framework
- `HuggingFaceMlxModel`: Apple Silicon acceleration
- `VllmVlmModel`: Optimized inference (Linux x86\_64 only)
- `ApiVlmModel`: OpenAI-compatible API clients
- Models: GraniteDocling, SmolDocling, Qwen2.5-VL, Pixtral, Gemma3, Phi-4

**Enrichment Models**:

- `CodeFormulaModel`: LaTeX extraction from images
- `DocumentPictureClassifier`: Figure classification
- `PictureDescriptionVlmModel`: Image caption generation
- `PictureDescriptionApiModel`: External API-based captions

Sources: Diagram 5 from high-level overview, [pyproject.toml49-110](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L49-L110) [docs/usage/vision\_models.md1-124](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L1-L124)

## Processing Flow

### Document Conversion Flow

```
```

**Key Flow Points**:

1. **Format Detection**: `_guess_format()` analyzes MIME type, file extension, and content to determine `InputFormat`
2. **Pipeline Selection**: `FormatOption` mapping routes to appropriate pipeline class and backend class
3. **Pipeline Caching**: Pipelines cached by `(pipeline_class, options_hash)` to avoid redundant model loading
4. **Three-Phase Processing**: `_build_document()` → `_assemble_document()` → `_enrich_document()`
5. **Model Integration**: Models invoked throughout pipeline stages
6. **Unified Output**: All pipelines produce `DoclingDocument` instance

Sources: Diagram 2 from high-level overview

### Pipeline Caching Strategy

The `DocumentConverter` maintains an `_initialized_pipelines` cache keyed by `(pipeline_class, options_hash)`. This ensures:

- Models loaded once per configuration
- Pipelines reused across documents with identical settings
- Significant performance improvement for batch processing

Sources: Diagram 6 from high-level overview

## Technology Stack

### Core Dependencies

| Dependency           | Purpose                           |
| -------------------- | --------------------------------- |
| `docling-core`       | Core data models and utilities    |
| `docling-parse`      | PDF text extraction library       |
| `docling-ibm-models` | Layout and table structure models |
| `pypdfium2`          | PDF rendering                     |
| `pydantic`           | Data validation and settings      |
| `huggingface_hub`    | Model downloading                 |

### Optional Dependencies

| Extra       | Dependencies                                       | Purpose                           |
| ----------- | -------------------------------------------------- | --------------------------------- |
| `easyocr`   | `easyocr`                                          | Deep learning OCR engine          |
| `tesserocr` | `tesserocr`                                        | Tesseract OCR binding             |
| `ocrmac`    | `ocrmac`                                           | macOS native OCR                  |
| `vlm`       | `transformers`, `mlx-vlm`, `vllm`, `qwen-vl-utils` | Vision-language model support     |
| `rapidocr`  | `rapidocr`, `onnxruntime`                          | RapidOCR engine with ONNX backend |
| `asr`       | `openai-whisper`                                   | Audio transcription               |

### Platform Support

- **Operating Systems**: macOS, Linux (x86\_64, aarch64, arm64), Windows
- **Python Versions**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Accelerators**: CPU, CUDA, MPS (Apple Silicon), AUTO detection

Sources: [pyproject.toml44-111](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L44-L111) [uv.lock1-15](https://github.com/docling-project/docling/blob/f7244a43/uv.lock#L1-L15)

## Entry Points

### CLI Entry Points

```
docling          # Main CLI: docling.cli.main:app
docling-tools    # Model management: docling.cli.tools:app
```

### Plugin System

Entry point `docling_defaults` registered at [pyproject.toml84-85](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L84-L85) enables plugin discovery:

- `docling.models.plugins.defaults` provides default OCR engines and picture description models
- Third-party plugins can extend Docling without modifying core

### Python API Entry Points

```
```

Sources: [pyproject.toml84-90](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L84-L90) [docs/usage/index.md1-46](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md#L1-L46) [docs/examples/minimal\_vlm\_pipeline.py1-71](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py#L1-L71)

## Configuration and Environment

### Configuration Hierarchy

1. **CLI Arguments**: Parsed into option objects
2. **Environment Variables**: `DOCLING_DEVICE`, `OMP_NUM_THREADS`, `DOCLING_NUM_THREADS`
3. **Pipeline Options**: `PdfPipelineOptions`, `VlmPipelineOptions`, `AsrPipelineOptions`
4. **Model-Specific Options**: `OcrOptions`, `LayoutOptions`, `TableStructureOptions`
5. **Accelerator Options**: Device placement and thread configuration

### Key Configuration Classes

- `AcceleratorOptions`: Hardware acceleration settings
- `PdfPipelineOptions`: PDF processing configuration
- `VlmPipelineOptions`: Vision-language model settings
- `InlineVlmOptions` / `ApiVlmOptions`: Local vs. remote VLM configuration
- `OcrOptions`: OCR engine selection and language settings
- `TableStructureOptions`: Table model precision modes (FAST/ACCURATE)

Sources: Diagram 6 from high-level overview

## Output Formats

`DoclingDocument` supports multiple export formats:

| Format   | Method                 | Use Case                                    |
| -------- | ---------------------- | ------------------------------------------- |
| Markdown | `export_to_markdown()` | Human-readable, LLM-friendly                |
| HTML     | `export_to_html()`     | Web display, rich formatting                |
| JSON     | `export_to_json()`     | Lossless serialization, programmatic access |
| DocTags  | `export_to_doctags()`  | Structured markup format                    |

All exports preserve document structure, provenance, and metadata. The `DoclingDocument` data model is defined in `docling-core` package.

Sources: [README.md35](https://github.com/docling-project/docling/blob/f7244a43/README.md#L35-L35) Diagram 1 from high-level overview

## Development and Distribution

### Package Distribution

- **PyPI**: `pip install docling` - [pyproject.toml2](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L2-L2)
- **Version**: 2.55.1 (auto-updated via semantic release)
- **License**: MIT - [pyproject.toml5](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L5-L5)

### Development Tools

- **Package Manager**: `uv` - [pyproject.toml155-157](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L155-L157)
- **Code Formatting**: `ruff` - [pyproject.toml162-238](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L162-L238)
- **Type Checking**: `mypy` - [pyproject.toml239-266](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L239-L266)
- **Testing**: `pytest` with coverage
- **CI/CD**: GitHub Actions, semantic release

### Versioning

Semantic versioning with automated releases based on conventional commits:

- `feat:` triggers minor version bump
- `fix:`, `perf:` trigger patch version bump
- Version stored in [pyproject.toml3](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L3-L3)

Sources: [pyproject.toml1-280](https://github.com/docling-project/docling/blob/f7244a43/pyproject.toml#L1-L280) [CHANGELOG.md1-430](https://github.com/docling-project/docling/blob/f7244a43/CHANGELOG.md#L1-L430)

## Security and Compliance

Docling participates in the OpenSSF Best Practices Badge Program and implements:

- HTTPS for network communication
- TLS certificate verification
- Cryptographically signed releases on PyPI, Quay.io, and GHCR.io
- Private vulnerability reporting via email: [deepsearch-core@zurich.ibm.com](mailto:deepsearch-core@zurich.ibm.com.md)
- Issue tracking on GitHub

Security-conscious features:

- Local execution support for air-gapped environments
- No telemetry or data transmission by default
- Configurable model artifact storage

Sources: [.github/SECURITY.md1-43](https://github.com/docling-project/docling/blob/f7244a43/.github/SECURITY.md#L1-L43)

## Project Governance

- **Hosted by**: LF AI & Data Foundation
- **Started by**: IBM Research Zurich (AI for knowledge team)
- **Code Repository**: <https://github.com/docling-project/docling>
- **Documentation**: <https://docling-project.github.io/docling/>
- **License**: MIT
- **Citation**: arXiv:2408.09869 (Docling Technical Report)

Sources: [README.md149-156](https://github.com/docling-project/docling/blob/f7244a43/README.md#L149-L156) [CITATION.cff1-16](https://github.com/docling-project/docling/blob/f7244a43/CITATION.cff#L1-L16) [docs/index.md59-65](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md#L59-L65)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Overview](#overview.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Purpose](#system-purpose.md)
- [Core Architecture](#core-architecture.md)
- [System Architecture Diagram](#system-architecture-diagram.md)
- [Component Overview](#component-overview.md)
- [Key Components](#key-components.md)
- [User Interfaces](#user-interfaces.md)
- [Core Orchestration Layer](#core-orchestration-layer.md)
- [Processing Pipelines](#processing-pipelines.md)
- [Document Backends](#document-backends.md)
- [AI/ML Model Layer](#aiml-model-layer.md)
- [Processing Flow](#processing-flow.md)
- [Document Conversion Flow](#document-conversion-flow.md)
- [Pipeline Caching Strategy](#pipeline-caching-strategy.md)
- [Technology Stack](#technology-stack.md)
- [Core Dependencies](#core-dependencies.md)
- [Optional Dependencies](#optional-dependencies.md)
- [Platform Support](#platform-support.md)
- [Entry Points](#entry-points.md)
- [CLI Entry Points](#cli-entry-points.md)
- [Plugin System](#plugin-system.md)
- [Python API Entry Points](#python-api-entry-points.md)
- [Configuration and Environment](#configuration-and-environment.md)
- [Configuration Hierarchy](#configuration-hierarchy.md)
- [Key Configuration Classes](#key-configuration-classes.md)
- [Output Formats](#output-formats.md)
- [Development and Distribution](#development-and-distribution.md)
- [Package Distribution](#package-distribution.md)
- [Development Tools](#development-tools.md)
- [Versioning](#versioning.md)
- [Security and Compliance](#security-and-compliance.md)
- [Project Governance](#project-governance.md)
