AI/ML Models | docling-project/docling | DeepWiki

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

# AI/ML Models

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

## Purpose and Scope

This document provides an overview of the AI/ML model layer in Docling, covering the architecture, plugin system, model downloading, and common interfaces that all models implement. The model layer provides specialized AI capabilities for document understanding tasks such as OCR, layout analysis, table structure recognition, and enrichment.

For detailed information about specific model types, see:

- OCR engines and text extraction: [OCR Models](docling-project/docling/4.1-ocr-models.md)
- Layout analysis and table structure: [Layout and Table Structure Models](docling-project/docling/4.2-layout-and-table-structure-models.md)
- Vision-language models: [Vision Language Models](docling-project/docling/4.3-vision-language-models.md)
- Content enrichment models: [Enrichment Models](docling-project/docling/4.4-enrichment-models.md)

For information about how models are integrated into document processing workflows, see [Processing Pipelines](docling-project/docling/5-processing-pipelines.md).

---

## Model Architecture Overview

The Docling model layer is organized around a hierarchy of base classes that define common interfaces for different model types. Models are categorized into two primary groups based on their processing scope:

**Diagram: Model Class Hierarchy**

```
```

Sources: [docling/models/base\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py) [docling/models/base\_ocr\_model.py24-228](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L24-L228) [docling/models/layout\_model.py28-238](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L28-L238) [docling/models/table\_structure\_model.py29-305](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L29-L305)

### Page-Level Models

Page-level models inherit from `BasePageModel` and process entire pages through a batch iterator pattern. They implement:

```
```

Models in this category include:

- **OCR Models**: Extract text from images ([RapidOcrModel](https://github.com/docling-project/docling/blob/f7244a43/RapidOcrModel) [EasyOcrModel](https://github.com/docling-project/docling/blob/f7244a43/EasyOcrModel) [TesseractOcrModel](https://github.com/docling-project/docling/blob/f7244a43/TesseractOcrModel) [OcrMacModel](https://github.com/docling-project/docling/blob/f7244a43/OcrMacModel))
- **LayoutModel**: Analyzes page layout and identifies document elements
- **TableStructureModel**: Recognizes table structure and extracts cells
- **PagePreprocessingModel**: Generates page images and extracts text cells
- **PageAssembleModel**: Assembles page elements into structured output

### Item-Level Enrichment Models

Item-level models inherit from `BaseItemAndImageEnrichmentModel` and process individual document items after page assembly. They implement:

```
```

Models in this category include:

- **CodeFormulaModel**: Converts code and formula images to LaTeX/text
- **DocumentPictureClassifier**: Classifies figure types
- **PictureDescriptionVlmModel**: Generates text descriptions of images

Sources: [docling/models/code\_formula\_model.py45-338](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L45-L338) [docling/models/document\_picture\_classifier.py36-186](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L36-L186) [docling/models/picture\_description\_vlm\_model.py24-117](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L24-L117)

---

## Plugin System and Model Discovery

Docling uses a plugin-based architecture for model discovery, allowing external packages to register additional model implementations without modifying core code.

**Diagram: Plugin Discovery Mechanism**

```
```

Sources: [docling/models/plugins/defaults.py1-31](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py#L1-L31) [docling/models/factories.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/factories.py)

### Plugin Registration

The default plugin entry point is registered in the package setup configuration:

```
[docling_defaults]
docling.models.plugins.defaults = 
```

The plugin system provides two primary extension points:

1. **OCR Engines** - Registered via `ocr_engines()` function returning a dictionary with key `"ocr_engines"`
2. **Picture Description** - Registered via `picture_description()` function returning a dictionary with key `"picture_description"`

Default implementations are registered in [docling/models/plugins/defaults.py1-31](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py#L1-L31):

```
```

### Factory Pattern

Factories use the plugin system to discover and instantiate models based on options classes. The `get_ocr_factory()` function creates an `OcrModelFactory` that:

1. Discovers registered OCR models via entry points
2. Matches options classes to implementation classes via `get_options_type()`
3. Instantiates the appropriate model based on user-provided options

The `allow_external_plugins` flag controls whether external plugins are loaded, providing security for production deployments.

Sources: [docling/models/factories.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/factories.py) [docling/pipeline/standard\_pdf\_pipeline.py115-124](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L115-L124)

---

## Model Downloading and Artifact Management

Models require artifact files (weights, configurations) that are downloaded from HuggingFace or ModelScope repositories. Docling provides both programmatic and CLI interfaces for model management.

**Diagram: Model Download and Loading Flow**

```
```

Sources: [docling/utils/model\_downloader.py30-159](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L159) [docling/models/utils/hf\_model\_download.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/utils/hf_model_download.py) [docling/cli/models.py54-127](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L127)

### Model Download Interface

Each model class implements a static `download_models()` method:

```
```

This method handles downloading from the appropriate source:

- **HuggingFace** (default): Uses `huggingface_hub.snapshot_download()`
- **ModelScope** (alternative): Uses `modelscope` library for downloads in China

### Model Repository Structure

Models are organized by repository folders:

| Model                     | Repository Folder                 | HuggingFace Repo ID              |
| ------------------------- | --------------------------------- | -------------------------------- |
| LayoutModel               | `ds4sd--docling-models`           | `ds4sd/docling-models`           |
| TableStructureModel       | `ds4sd--docling-models`           | `ds4sd/docling-models`           |
| CodeFormulaModel          | `ds4sd--CodeFormulaV2`            | `ds4sd/CodeFormulaV2`            |
| DocumentPictureClassifier | `ds4sd--DocumentFigureClassifier` | `ds4sd/DocumentFigureClassifier` |
| RapidOcrModel             | `RapidOcr`                        | Custom downloads from ModelScope |
| EasyOcrModel              | `EasyOcr`                         | Custom downloads from GitHub     |

Sources: [docling/models/layout\_model.py90-102](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L90-L102) [docling/models/table\_structure\_model.py91-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L91-L101) [docling/models/code\_formula\_model.py118-129](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L118-L129)

### CLI Model Management

The `docling-tools` CLI provides model downloading capabilities:

```
```

Available models defined in [docling/cli/models.py30-43](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L30-L43):

```
```

Default models (downloaded when no specific models are requested): `layout`, `tableformer`, `code_formula`, `picture_classifier`, `rapidocr`

Sources: [docling/cli/models.py54-136](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L54-L136)

### Artifact Path Resolution

Models support two artifact path patterns for backward compatibility:

1. **Modern structure** (recommended): `artifacts_path / model_repo_folder / model_path`
2. **Legacy structure** (deprecated): `artifacts_path / model_path`

Example from [docling/models/layout\_model.py64-81](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L64-L81):

```
```

---

## Common Model Interfaces

All models implement specific interfaces based on their processing type, with common patterns for initialization, configuration, and execution.

**Diagram: Model Interface Contracts**

```
```

Sources: [docling/models/base\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py) [docling/models/base\_ocr\_model.py24-228](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L24-L228)

### Initialization Pattern

All models follow a consistent initialization pattern:

1. **enabled**: Boolean flag controlling whether the model is active
2. **artifacts\_path**: Optional path to model artifacts (triggers download if None)
3. **options**: Model-specific configuration object
4. **accelerator\_options**: Hardware acceleration settings (device, threads)

Example from [docling/models/layout\_model.py49-87](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L49-L87):

```
```

### Page-Level Processing

Page-level models process batches of pages, yielding results iteratively:

```
```

Key characteristics:

- **Streaming**: Pages are processed and yielded one at a time
- **Profiling**: Wrapped in `TimeRecorder` for performance tracking
- **Disabled passthrough**: If `enabled=False`, pages pass through unmodified

Sources: [docling/models/layout\_model.py148-238](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py#L148-L238) [docling/models/table\_structure\_model.py170-305](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py#L170-L305)

### Item-Level Enrichment

Item-level models filter and process document items:

```
```

Key characteristics:

- **Filtering**: `is_processable()` determines which items to process
- **Batch processing**: Items are collected and processed in batches
- **In-place enrichment**: Items are modified and yielded

Sources: [docling/models/code\_formula\_model.py131-338](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L131-L338) [docling/models/document\_picture\_classifier.py118-186](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L118-L186)

---

## Model Configuration and Options

Models are configured through specialized options classes that follow the Pydantic `BaseModel` pattern. Options control model behavior, resource paths, and inference parameters.

**Diagram: Options Class Hierarchy**

```
```

Sources: [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py) [docling/models/code\_formula\_model.py26-43](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L26-L43)

### OCR Options

OCR options control text extraction behavior:

**Common OCR Options** (base class):

- `bitmap_area_threshold` (float, default 0.05): Minimum page coverage to trigger OCR
- `force_full_page_ocr` (bool, default False): Always OCR entire page

**RapidOcrOptions** ([docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)):

- `backend`: Engine type ("onnxruntime", "torch", "openvino", "paddle")
- `use_det`: Enable text detection (default True)
- `use_cls`: Enable text direction classification (default True)
- `use_rec`: Enable text recognition (default True)
- `text_score`: Confidence threshold for text detection
- Model paths: `det_model_path`, `cls_model_path`, `rec_model_path`, `rec_keys_path`

**EasyOcrOptions**:

- `lang`: List of language codes (default \["en"])
- `recog_network`: Recognition network to use
- `use_gpu`: Enable GPU acceleration (deprecated, use `accelerator_options.device`)
- `confidence_threshold`: Minimum confidence for OCR results

### Layout and Table Options

**LayoutOptions**:

- `model_spec`: `LayoutModelConfig` specifying the model variant (default: Heron/DOCLING\_LAYOUT\_V2)

**TableStructureOptions**:

- `mode`: `TableFormerMode.FAST` or `TableFormerMode.ACCURATE` (default FAST)
- `do_cell_matching`: Enable cell matching between table cells and text cells (default True)

Example from [tests/test\_options.py25-33](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L25-L33):

```
```

Sources: [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)

### Enrichment Model Options

**CodeFormulaModelOptions** ([docling/models/code\_formula\_model.py26-43](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L26-L43)):

- `do_code_enrichment`: Enable code block enrichment (default True)
- `do_formula_enrichment`: Enable formula enrichment (default True)

**PictureDescriptionVlmOptions** ([docling/models/picture\_description\_vlm\_model.py31-46](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L31-L46)):

- `repo_id`: HuggingFace repository ID
- `prompt`: Text prompt for image description
- `generation_config`: Dictionary of generation parameters

### Accelerator Options

All models receive `AcceleratorOptions` controlling hardware acceleration:

```
```

**Device Options**:

- `AUTO`: Automatically select best available device
- `CPU`: Force CPU execution
- `CUDA`: Use NVIDIA GPU
- `MPS`: Use Apple Metal Performance Shaders
- `DML`: Use DirectML (Windows)

Environment variable overrides:

- `DOCLING_DEVICE` or `DEVICE`: Override device selection
- `DOCLING_NUM_THREADS` or `OMP_NUM_THREADS`: Override thread count

Sources: [docling/datamodel/accelerator\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/accelerator_options.py) [tests/test\_options.py43-96](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L43-L96)

---

## Model Integration in Pipelines

Models are integrated into pipelines through two primary mechanisms: build pipelines (page-level) and enrichment pipelines (item-level).

**Diagram: Model Integration Points**

```
```

Sources: [docling/pipeline/standard\_pdf\_pipeline.py34-99](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L34-L99)

### Build Pipeline Construction

The build pipeline is constructed in `StandardPdfPipeline.__init__()` [docling/pipeline/standard\_pdf\_pipeline.py51-75](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L51-L75):

```
```

Models in the build pipeline:

1. Process pages sequentially in order
2. Each model receives output from previous model
3. Operate on `Page` objects with backend access
4. Execute during `_build_document()` phase

### Enrichment Pipeline Construction

The enrichment pipeline is constructed by the `ConvertPipeline` base class and extended in `StandardPdfPipeline` [docling/pipeline/standard\_pdf\_pipeline.py77-90](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L77-L90):

```
```

Models in the enrichment pipeline:

1. Process document items after page assembly
2. Filter items via `is_processable()`
3. Operate on `DoclingDocument` and `NodeItem` objects
4. Execute during `_enrich_document()` phase

Sources: [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py) [docling/pipeline/standard\_pdf\_pipeline.py34-99](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L34-L99)

### Model Execution Order

The complete model execution sequence in `StandardPdfPipeline`:

1. **Page Initialization**: Backend loads page ([line 126-132](<https://github.com/docling-project/docling/blob/f7244a43/line 126-132>))

2. **Build Phase**: Sequential application of build\_pipe models

   - PagePreprocessingModel generates images
   - OCR model extracts text from bitmaps
   - LayoutModel identifies document structure
   - TableStructureModel recognizes tables
   - PageAssembleModel creates structured elements

3. **Assembly Phase**: Pages combined into document ([line 134-234](<https://github.com/docling-project/docling/blob/f7244a43/line 134-234>))

4. **Enrichment Phase**: Enrichment models process document items

   - CodeFormulaModel converts code/formula images
   - PictureClassifier classifies figures
   - PictureDescription generates captions

Each model respects its `enabled` flag, passing data through unmodified when disabled.

---

This page provides an overview of the model architecture and common patterns. For details on specific model implementations, see the child pages for OCR, Layout/Table, VLM, and Enrichment models.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [AI/ML Models](#aiml-models.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Model Architecture Overview](#model-architecture-overview.md)
- [Page-Level Models](#page-level-models.md)
- [Item-Level Enrichment Models](#item-level-enrichment-models.md)
- [Plugin System and Model Discovery](#plugin-system-and-model-discovery.md)
- [Plugin Registration](#plugin-registration.md)
- [Factory Pattern](#factory-pattern.md)
- [Model Downloading and Artifact Management](#model-downloading-and-artifact-management.md)
- [Model Download Interface](#model-download-interface.md)
- [Model Repository Structure](#model-repository-structure.md)
- [CLI Model Management](#cli-model-management.md)
- [Artifact Path Resolution](#artifact-path-resolution.md)
- [Common Model Interfaces](#common-model-interfaces.md)
- [Initialization Pattern](#initialization-pattern.md)
- [Page-Level Processing](#page-level-processing.md)
- [Item-Level Enrichment](#item-level-enrichment.md)
- [Model Configuration and Options](#model-configuration-and-options.md)
- [OCR Options](#ocr-options.md)
- [Layout and Table Options](#layout-and-table-options.md)
- [Enrichment Model Options](#enrichment-model-options.md)
- [Accelerator Options](#accelerator-options.md)
- [Model Integration in Pipelines](#model-integration-in-pipelines.md)
- [Build Pipeline Construction](#build-pipeline-construction.md)
- [Enrichment Pipeline Construction](#enrichment-pipeline-construction.md)
- [Model Execution Order](#model-execution-order.md)
