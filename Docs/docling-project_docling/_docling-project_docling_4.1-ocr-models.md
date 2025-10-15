OCR Models | docling-project/docling | DeepWiki

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

# OCR Models

Relevant source files

- [docling/cli/models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py)
- [docling/models/auto\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py)
- [docling/models/picture\_description\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py)
- [docling/models/plugins/defaults.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py)
- [docling/models/rapid\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py)
- [docling/models/tesseract\_ocr\_cli\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_cli_model.py)
- [docling/models/tesseract\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_model.py)
- [docling/utils/model\_downloader.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py)
- [tests/data\_scanned/sample\_with\_rotation\_mismatch.pdf](https://github.com/docling-project/docling/blob/f7244a43/tests/data_scanned/sample_with_rotation_mismatch.pdf)
- [tests/test\_backend\_docling\_parse.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse.py)
- [tests/test\_backend\_docling\_parse\_v2.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_docling_parse_v2.py)
- [tests/test\_backend\_pdfium.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_pdfium.py)
- [tests/test\_e2e\_ocr\_conversion.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_e2e_ocr_conversion.py)

This document covers the Optical Character Recognition (OCR) models and engines available in Docling's document processing pipeline. OCR models are responsible for extracting text from image regions in documents, particularly scanned PDFs and bitmap areas where programmatic text extraction is not possible.

For information about layout analysis and document structure recognition, see [Layout and Table Structure Models](docling-project/docling/4.2-layout-and-table-structure-models.md). For details about vision-language models that can understand document content, see [Vision Language Models](docling-project/docling/4.3-vision-language-models.md).

## OCR Architecture Overview

Docling provides a flexible OCR framework that supports multiple OCR engines through a common interface. The system automatically detects areas requiring OCR processing and applies the configured engine to extract text.

### OCR Model Class Hierarchy

```
```

**Sources:** [docling/models/base\_ocr\_model.py24-228](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L24-L228) [docling/models/tesseract\_ocr\_model.py29-255](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_model.py#L29-L255) [docling/models/tesseract\_ocr\_cli\_model.py35-328](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_cli_model.py#L35-L328) [docling/models/easyocr\_model.py28-201](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py#L28-L201)

## Base OCR Model Framework

The `BaseOcrModel` class provides the foundation for all OCR implementations in Docling. It defines the common interface and shared functionality used by all OCR engines.

### Core Functionality

| Method                 | Purpose                                              | Implementation                                     |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------- |
| `get_ocr_rects()`      | Identifies bitmap regions requiring OCR              | Uses bitmap detection and morphological operations |
| `post_process_cells()` | Integrates OCR results with existing text            | Handles cell filtering and re-indexing             |
| `_filter_ocr_cells()`  | Removes OCR cells overlapping with programmatic text | Uses R-tree spatial indexing for efficiency        |
| `_combine_cells()`     | Merges OCR and programmatic text cells               | Handles full-page OCR vs. selective OCR modes      |

### OCR Region Detection

The base class implements intelligent OCR region detection in `get_ocr_rects()`:

1. **Bitmap Analysis**: Identifies image regions in the document using `page._backend.get_bitmap_rects()`
2. **Morphological Processing**: Uses binary dilation to merge nearby bitmap regions
3. **Coverage Calculation**: Determines if full-page OCR is needed based on bitmap coverage
4. **Threshold-based Decision**: Compares coverage against `bitmap_area_threshold` and `force_full_page_ocr` settings

**Sources:** [docling/models/base\_ocr\_model.py40-113](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L40-L113) [docling/models/base\_ocr\_model.py140-172](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L140-L172)

## Supported OCR Engines

Docling supports multiple OCR engines through a plugin-based architecture. Each engine has specific strengths and implementation characteristics.

### OcrAutoModel (Automatic Engine Selection)

The `OcrAutoModel` implements intelligent fallback logic to automatically select the best available OCR engine on the current system.

#### Selection Priority

The auto-selection follows this priority order:

1. **OcrMac** (Darwin/macOS only) - Native macOS OCR API via `ocrmac` library
2. **RapidOcrModel** with ONNX backend - If `onnxruntime` is installed
3. **EasyOcrModel** - If `easyocr` is installed
4. **RapidOcrModel** with Torch backend - If `torch` is installed

#### Implementation

The selection logic is implemented in `OcrAutoModel.__init__()`:

```
```

**Sources:** [docling/models/auto\_ocr\_model.py25-133](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py#L25-L133)

### RapidOcrModel

The `RapidOcrModel` provides a lightweight OCR solution with multiple backend options (ONNX and PyTorch).

#### Architecture

RapidOCR uses a three-stage pipeline:

- **Detection**: Locates text regions in images
- **Classification**: Determines text orientation
- **Recognition**: Extracts text from detected regions

#### Backend Support

| Backend       | Library        | Use Case                         |
| ------------- | -------------- | -------------------------------- |
| `onnxruntime` | ONNX Runtime   | Default, CPU-optimized inference |
| `torch`       | PyTorch        | GPU acceleration support         |
| `openvino`    | Intel OpenVINO | Intel hardware optimization      |
| `paddle`      | PaddlePaddle   | PaddleOCR native backend         |

#### Model Artifacts

RapidOCR uses PP-OCRv4 models downloaded from ModelScope:

```
```

#### Configuration Options

RapidOcrOptions provides extensive control over the OCR pipeline:

| Option            | Type             | Default         | Description                       |
| ----------------- | ---------------- | --------------- | --------------------------------- |
| `backend`         | `str`            | `"onnxruntime"` | Backend engine to use             |
| `use_det`         | `bool`           | `True`          | Enable text detection             |
| `use_cls`         | `bool`           | `True`          | Enable orientation classification |
| `use_rec`         | `bool`           | `True`          | Enable text recognition           |
| `text_score`      | `float`          | `0.5`           | Minimum confidence threshold      |
| `det_model_path`  | `Optional[str]`  | `None`          | Custom detection model path       |
| `cls_model_path`  | `Optional[str]`  | `None`          | Custom classification model path  |
| `rec_model_path`  | `Optional[str]`  | `None`          | Custom recognition model path     |
| `rec_keys_path`   | `Optional[str]`  | `None`          | Custom character dictionary path  |
| `rapidocr_params` | `Optional[dict]` | `None`          | Advanced RapidOCR parameters      |

#### Processing Flow

The implementation in `RapidOcrModel.__call__()` processes each OCR rectangle:

1. Extract image region with 3x scaling (216 DPI)
2. Convert to numpy array
3. Call `self.reader(im, use_det=..., use_cls=..., use_rec=...)`
4. Parse results as `(boxes, texts, scores)` tuples
5. Transform coordinates back to page coordinate system
6. Create `TextCell` objects with bounding rectangles

**Sources:** [docling/models/rapid\_ocr\_model.py36-306](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L36-L306)

### TesseractOcrModel

The `TesseractOcrModel` provides direct integration with Tesseract via the `tesserocr` Python binding.

#### Key Features

- **Direct API Access**: Uses `tesserocr.PyTessBaseAPI` for optimal performance
- **Automatic Language Detection**: Script detection with automatic language switching via `lang=["auto"]`
- **Orientation Detection**: OSD (Orientation and Script Detection) via separate `osd_reader`
- **Multi-script Support**: Maintains separate `script_readers` dictionary for detected scripts
- **PSM Configuration**: Configurable Page Segmentation Mode via `psm` option

#### Language Detection Implementation

When `lang=["auto"]` is configured:

1. **OSD Detection**: `osd_reader.DetectOrientationScript()` identifies script and orientation
2. **Script Mapping**: `map_tesseract_script()` converts Tesseract script names to language codes
3. **Language Validation**: Checks if detected language exists in `_tesserocr_languages`
4. **Reader Creation**: Creates script-specific `PyTessBaseAPI` instance and caches in `script_readers`
5. **Dynamic Switching**: Uses appropriate reader for each OCR rectangle

#### Configuration Options

| Option | Type            | Default   | Description                                |
| ------ | --------------- | --------- | ------------------------------------------ |
| `lang` | `List[str]`     | `["eng"]` | Language codes or `["auto"]` for detection |
| `path` | `Optional[str]` | `None`    | Custom tessdata directory path             |
| `psm`  | `Optional[int]` | `None`    | Page Segmentation Mode (0-13)              |

**Sources:** [docling/models/tesseract\_ocr\_model.py29-265](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_model.py#L29-L265)

### TesseractOcrCliModel

The `TesseractOcrCliModel` provides CLI-based Tesseract integration as an alternative when `tesserocr` binding is unavailable.

#### Implementation Characteristics

- **Subprocess Execution**: Uses `subprocess.run()` to invoke tesseract CLI
- **TSV Output**: Parses Tesseract's tab-separated value output format
- **Temporary Files**: Creates temporary PNG files for each OCR rectangle
- **OSD via CLI**: Runs `tesseract --psm 0 -l osd` for orientation detection
- **Language Enumeration**: Uses `tesseract --list-langs` to discover installed languages

#### Key Methods

| Method                        | Purpose                                                 |
| ----------------------------- | ------------------------------------------------------- |
| `_get_name_and_version()`     | Executes `tesseract --version` to validate installation |
| `_set_languages_and_prefix()` | Discovers installed languages and script prefix         |
| `_perform_osd()`              | Runs OSD mode for orientation/script detection          |
| `_parse_language()`           | Maps detected script to language code                   |
| `_run_tesseract()`            | Executes main OCR with language and PSM settings        |

#### Configuration Options

| Option          | Type            | Default       | Description                  |
| --------------- | --------------- | ------------- | ---------------------------- |
| `tesseract_cmd` | `str`           | `"tesseract"` | Path to tesseract executable |
| `lang`          | `List[str]`     | `["eng"]`     | Language codes or `["auto"]` |
| `path`          | `Optional[str]` | `None`        | Custom tessdata directory    |
| `psm`           | `Optional[int]` | `None`        | Page Segmentation Mode       |

**Sources:** [docling/models/tesseract\_ocr\_cli\_model.py35-332](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_cli_model.py#L35-L332)

### EasyOcrModel

The `EasyOcrModel` integrates the EasyOCR library, providing deep learning-based OCR.

#### Key Features

- **GPU Acceleration**: Supports CUDA and MPS via `accelerator_options`
- **Neural Networks**: Uses deep learning models for text recognition
- **Multi-language**: Built-in support for 80+ languages
- **Model Management**: Automatic model downloading via `download_models()` static method

#### Configuration Options

| Option                    | Type             | Default      | Description                                |
| ------------------------- | ---------------- | ------------ | ------------------------------------------ |
| `lang`                    | `List[str]`      | `["en"]`     | EasyOCR language codes                     |
| `use_gpu`                 | `Optional[bool]` | `None`       | GPU usage (auto-detected from accelerator) |
| `confidence_threshold`    | `float`          | `0.5`        | Minimum confidence for results             |
| `recog_network`           | `str`            | `"standard"` | Recognition network architecture           |
| `model_storage_directory` | `Optional[str]`  | `None`       | Custom model cache directory               |

**Sources:** [docling/models/easyocr\_model.py28-201](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py#L28-L201)

### OcrMacModel

The `OcrMacModel` provides macOS-specific OCR using native system APIs via the `ocrmac` library.

#### Platform Requirements

- **Platform**: macOS (Darwin) only
- **Library**: `ocrmac` Python package
- **System**: Uses macOS Vision framework

**Sources:** [docling/models/auto\_ocr\_model.py43-58](https://github.com/docling-project/docling/blob/f7244a43/docling/models/auto_ocr_model.py#L43-L58)

## OCR Processing Pipeline

The OCR processing flow integrates with Docling's document processing pipeline through the `BaseOcrModel` framework.

### End-to-End OCR Flow

```
```

### Coordinate Transformation

OCR engines return coordinates in the scaled image space. The `tesseract_box_to_bounding_rectangle()` utility transforms these to page coordinates:

1. **Apply Rotation**: If document has rotation from OSD, apply inverse rotation
2. **Scale Factor**: Divide by scale factor (typically 3)
3. **Offset Translation**: Add OCR rectangle origin offset
4. **Coordinate Origin**: Convert from TOPLEFT to BOTTOMLEFT if needed

**Sources:** [docling/models/base\_ocr\_model.py40-228](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L40-L228) [docling/models/tesseract\_ocr\_model.py125-260](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_model.py#L125-L260) [docling/models/tesseract\_ocr\_cli\_model.py208-319](https://github.com/docling-project/docling/blob/f7244a43/docling/models/tesseract_ocr_cli_model.py#L208-L319) [docling/models/rapid\_ocr\_model.py226-301](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L226-L301) [docling/utils/ocr\_utils.py](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/ocr_utils.py)

### OCR Cell Post-Processing

The `post_process_cells()` method handles integration of OCR results:

```
```

**Sources:** [docling/models/base\_ocr\_model.py140-228](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L140-L228)

## Configuration and Options

OCR behavior is controlled through `PdfPipelineOptions.ocr_options`, with engine selection via the options factory pattern.

### OCR Options Factory

The options class determines which OCR engine is instantiated:

```
```

### Common Options (All Engines)

| Option                  | Type        | Default   | Description                                            |
| ----------------------- | ----------- | --------- | ------------------------------------------------------ |
| `bitmap_area_threshold` | `float`     | `0.05`    | Minimum bitmap coverage (0.0-1.0) to trigger OCR       |
| `force_full_page_ocr`   | `bool`      | `False`   | Force OCR on entire page regardless of bitmap coverage |
| `lang`                  | `List[str]` | `["eng"]` | Language codes for OCR engine                          |

### Usage Examples

```
```

### Integration with Accelerator Options

OCR engines respect global `AcceleratorOptions` for device and threading:

| AcceleratorOption | Effect on OCR                                |
| ----------------- | -------------------------------------------- |
| `device = CUDA`   | Enables GPU for EasyOCR and RapidOCR (torch) |
| `device = CPU`    | Forces CPU execution                         |
| `device = AUTO`   | Uses DirectML on Windows for RapidOCR ONNX   |
| `num_threads = N` | Sets `intra_op_num_threads` for RapidOCR     |

**Sources:** [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py) [docling/models/rapid\_ocr\_model.py82-200](https://github.com/docling-project/docling/blob/f7244a43/docling/models/rapid_ocr_model.py#L82-L200) [docling/models/easyocr\_model.py57-73](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py#L57-L73) [tests/test\_e2e\_ocr\_conversion.py39-56](https://github.com/docling-project/docling/blob/f7244a43/tests/test_e2e_ocr_conversion.py#L39-L56)

## Performance and Capabilities

### Engine Comparison

| Feature                | TesseractOCR   | TesseractCLI   | EasyOCR        | RapidOCR       | OCR Mac    |
| ---------------------- | -------------- | -------------- | -------------- | -------------- | ---------- |
| **Performance**        | High           | Medium         | Medium         | High           | High       |
| **GPU Support**        | No             | No             | Yes            | No             | No         |
| **Language Detection** | Yes            | Yes            | No             | Limited        | Yes        |
| **Rotation Handling**  | Yes            | Yes            | No             | No             | Yes        |
| **Installation**       | Complex        | Simple         | Simple         | Simple         | Built-in   |
| **Platform Support**   | Cross-platform | Cross-platform | Cross-platform | Cross-platform | macOS only |

### Processing Characteristics

- **Image Scaling**: All engines scale input images to 216 DPI (3x multiplier) for optimal OCR accuracy
- **Confidence Scoring**: Each engine provides confidence scores for extracted text
- **Spatial Indexing**: Uses R-tree indexing for efficient cell overlap detection
- **Memory Management**: Implements proper cleanup for large image processing

### Quality Assessment

The system includes text quality rating in `PagePreprocessingModel.rate_text_quality()` to assess OCR results:

- Detects problematic patterns (glyph codes, fragmented text)
- Applies penalties for low-quality OCR output
- Integrates with overall document confidence scoring

**Sources:** [docling/models/base\_ocr\_model.py173-217](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py#L173-L217) [docling/models/page\_preprocessing\_model.py120-146](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py#L120-L146) [tests/test\_e2e\_ocr\_conversion.py59-101](https://github.com/docling-project/docling/blob/f7244a43/tests/test_e2e_ocr_conversion.py#L59-L101)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [OCR Models](#ocr-models.md)
- [OCR Architecture Overview](#ocr-architecture-overview.md)
- [OCR Model Class Hierarchy](#ocr-model-class-hierarchy.md)
- [Base OCR Model Framework](#base-ocr-model-framework.md)
- [Core Functionality](#core-functionality.md)
- [OCR Region Detection](#ocr-region-detection.md)
- [Supported OCR Engines](#supported-ocr-engines.md)
- [OcrAutoModel (Automatic Engine Selection)](#ocrautomodel-automatic-engine-selection.md)
- [Selection Priority](#selection-priority.md)
- [Implementation](#implementation.md)
- [RapidOcrModel](#rapidocrmodel.md)
- [Architecture](#architecture.md)
- [Backend Support](#backend-support.md)
- [Model Artifacts](#model-artifacts.md)
- [Configuration Options](#configuration-options.md)
- [Processing Flow](#processing-flow.md)
- [TesseractOcrModel](#tesseractocrmodel.md)
- [Key Features](#key-features.md)
- [Language Detection Implementation](#language-detection-implementation.md)
- [Configuration Options](#configuration-options-1.md)
- [TesseractOcrCliModel](#tesseractocrclimodel.md)
- [Implementation Characteristics](#implementation-characteristics.md)
- [Key Methods](#key-methods.md)
- [Configuration Options](#configuration-options-2.md)
- [EasyOcrModel](#easyocrmodel.md)
- [Key Features](#key-features-1.md)
- [Configuration Options](#configuration-options-3.md)
- [OcrMacModel](#ocrmacmodel.md)
- [Platform Requirements](#platform-requirements.md)
- [OCR Processing Pipeline](#ocr-processing-pipeline.md)
- [End-to-End OCR Flow](#end-to-end-ocr-flow.md)
- [Coordinate Transformation](#coordinate-transformation.md)
- [OCR Cell Post-Processing](#ocr-cell-post-processing.md)
- [Configuration and Options](#configuration-and-options.md)
- [OCR Options Factory](#ocr-options-factory.md)
- [Common Options (All Engines)](#common-options-all-engines.md)
- [Usage Examples](#usage-examples.md)
- [Integration with Accelerator Options](#integration-with-accelerator-options.md)
- [Performance and Capabilities](#performance-and-capabilities.md)
- [Engine Comparison](#engine-comparison.md)
- [Processing Characteristics](#processing-characteristics.md)
- [Quality Assessment](#quality-assessment.md)
