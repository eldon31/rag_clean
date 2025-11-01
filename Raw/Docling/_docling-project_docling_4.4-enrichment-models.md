Enrichment Models | docling-project/docling | DeepWiki

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

# Enrichment Models

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

Enrichment Models operate on assembled document items after the initial extraction and layout analysis phases. They enhance document elements with additional information such as LaTeX formulas, code snippets with language detection, picture classifications, and image captions. Unlike page-level models (see [Layout and Table Structure Models](docling-project/docling/4.2-layout-and-table-structure-models.md)), enrichment models process individual document items (text blocks, code blocks, pictures) along with their cropped images.

This page documents the three main types of enrichment models:

- **CodeFormulaModel**: Extracts LaTeX formulas and code with language detection
- **DocumentPictureClassifier**: Classifies pictures into 16 semantic categories
- **PictureDescriptionVlmModel**: Generates natural language descriptions of images

For VLM-based document processing that operates at the page level, see [Vision Language Models](docling-project/docling/4.3-vision-language-models.md). For the pipeline execution flow that includes enrichment, see [Base Pipeline Architecture](docling-project/docling/5.6-base-pipeline-architecture.md).

---

## Enrichment Architecture

### Processing Flow

Enrichment models are invoked during the `_enrich_document` phase of the pipeline, after document assembly is complete. They process items in batches, receiving both the document item and its cropped image.

**Diagram: Enrichment Processing Flow**

```
```

Sources: [docling/pipeline/base\_pipeline.py177-206](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L177-L206) [docling/pipeline/standard\_pdf\_pipeline.py77-90](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L77-L90)

---

### Base Class Interface

All enrichment models inherit from `BaseItemAndImageEnrichmentModel`, which defines the standard interface for item-level processing.

**Diagram: Enrichment Model Class Hierarchy**

```
```

Sources: [docling/models/base\_model.py67-113](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L67-L113) [docling/models/code\_formula\_model.py45-66](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L45-L66) [docling/models/document\_picture\_classifier.py36-60](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L36-L60) [docling/models/picture\_description\_vlm\_model.py24-46](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L24-L46)

---

### Item and Image Element Structure

Enrichment models receive `ItemAndImageEnrichmentElement` objects that bundle the document item with its cropped image and bounding box information.

| Field        | Type                        | Description                                         |
| ------------ | --------------------------- | --------------------------------------------------- |
| `item`       | `NodeItem`                  | The document item (CodeItem, TextItem, PictureItem) |
| `image`      | `Image.Image \| np.ndarray` | Cropped image of the item                           |
| `page_image` | `Image.Image`               | Full page image (for context)                       |
| `bbox`       | `BoundingBox`               | Item's bounding box on the page                     |
| `page_no`    | `int`                       | Page number containing the item                     |

Sources: [docling/datamodel/base\_models.py285-294](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L285-L294)

---

## Code and Formula Enrichment

### CodeFormulaModel

The `CodeFormulaModel` processes code blocks and formula elements to extract structured representations. It uses a vision-language model fine-tuned for converting images of code and formulas into their text representations.

**Model Details:**

| Attribute        | Value                         | Purpose                      |
| ---------------- | ----------------------------- | ---------------------------- |
| Repository       | `ds4sd/CodeFormulaV2`         | Hugging Face model ID        |
| Model Type       | `AutoModelForImageTextToText` | Florence-based architecture  |
| Batch Size       | `5`                           | Elements processed per batch |
| Image Scale      | `1.67` (120 DPI)              | Resolution for image input   |
| Expansion Factor | `0.18`                        | Bounding box expansion (18%) |

Sources: [docling/models/code\_formula\_model.py68-72](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L68-L72)

---

### Processing Logic

**Diagram: CodeFormulaModel Processing Pipeline**

```
```

Sources: [docling/models/code\_formula\_model.py277-337](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L277-L337)

---

### Code Language Detection

The model outputs code with a language prefix in the format `<_language_>`. The `_extract_code_language` method extracts this information:

**Pattern:** `^<_([^_>]+)_>\s*(.*)`

**Example Output:**

- Input: `<_python_>def main():\n print("Hello")`
- Extracted Language: `python`
- Remainder: `def main():\n print("Hello")`

The language string is then converted to a `CodeLanguageLabel` enum member. If the language is unrecognized or missing, it defaults to `CodeLanguageLabel.UNKNOWN`.

Sources: [docling/models/code\_formula\_model.py156-206](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L156-L206)

---

### Formula Extraction

For formula elements (identified by `DocItemLabel.FORMULA`), the model extracts LaTeX representations:

**Example:**

- Input: Image of mathematical formula
- Output: `E = mc^2`

The extracted LaTeX is stored in the `TextItem.text` field, replacing any placeholder text from layout analysis.

Sources: [docling/models/code\_formula\_model.py208-245](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L208-L245)

---

## Picture Classification

### DocumentPictureClassifier

The `DocumentPictureClassifier` categorizes picture elements into semantic classes such as charts, diagrams, photographs, and maps.

**Model Details:**

| Attribute         | Value                            |
| ----------------- | -------------------------------- |
| Repository        | `ds4sd/DocumentFigureClassifier` |
| Revision          | `v1.0.1`                         |
| Image Scale       | `2` (144 DPI)                    |
| Number of Classes | `16`                             |
| Output Type       | `PictureClassificationData`      |

Sources: [docling/models/document\_picture\_classifier.py62-105](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L62-L105)

---

### Classification Classes

The classifier predicts probabilities for 16 figure types. Results are sorted by confidence in descending order.

**Common Classification Classes:**

- `bar_chart`
- `line_chart`
- `pie_chart`
- `scatter_plot`
- `map`
- `photograph`
- `diagram`
- `flowchart`
- `table` (visual table representation)
- `equation`
- `schematic`
- `illustration`

Sources: [tests/test\_document\_picture\_classifier.py54-79](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py#L54-L79)

---

### Output Structure

**Diagram: PictureClassificationData Structure**

```
```

**Example:**

```
```

Sources: [docling/models/document\_picture\_classifier.py136-185](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L136-L185) [tests/test\_document\_picture\_classifier.py47-64](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py#L47-L64)

---

## Picture Description

### PictureDescriptionVlmModel

The `PictureDescriptionVlmModel` generates natural language descriptions of images using vision-language models. It supports multiple VLM backends and custom prompts.

**Supported Models:**

| Model Name     | Repository                             | Use Case                |
| -------------- | -------------------------------------- | ----------------------- |
| SmolVLM        | `HuggingFaceTB/SmolVLM2-1.7B-Instruct` | Lightweight description |
| Granite Vision | `ibm-granite/granite-vision-3.1-2b`    | IBM Granite family      |
| Custom VLM     | User-specified                         | Any compatible VLM      |

Sources: [docling/datamodel/pipeline\_options.py416-438](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L416-L438) [docling/models/picture\_description\_vlm\_model.py24-81](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L24-L81)

---

### Description Generation

**Diagram: Picture Description Pipeline**

```
```

Sources: [docling/models/picture\_description\_vlm\_model.py82-116](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L82-L116)

---

### Custom Prompts

The `PictureDescriptionVlmOptions` allows customization of the description prompt:

**Default Configuration:**

```
```

**Message Format:**

```
```

Sources: [docling/models/picture\_description\_vlm\_model.py86-103](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_vlm_model.py#L86-L103) [docling/datamodel/pipeline\_options.py416-438](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L416-L438)

---

### API-Based Picture Description

The `PictureDescriptionApiModel` provides an alternative that uses OpenAI-compatible APIs instead of local model inference.

**Configuration:**

```
```

Sources: [docling/models/picture\_description\_api\_model.py1-100](https://github.com/docling-project/docling/blob/f7244a43/docling/models/picture_description_api_model.py#L1-L100) [docling/datamodel/pipeline\_options.py441-466](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L441-L466)

---

## Configuration

### Pipeline Options

Enrichment models are configured through `PdfPipelineOptions`:

**Configuration Table:**

| Option                        | Type    | Default | Description                   |
| ----------------------------- | ------- | ------- | ----------------------------- |
| `do_code_enrichment`          | `bool`  | `False` | Enable code extraction        |
| `do_formula_enrichment`       | `bool`  | `False` | Enable formula extraction     |
| `do_picture_classification`   | `bool`  | `False` | Enable picture classification |
| `do_picture_description`      | `bool`  | `False` | Enable picture description    |
| `picture_description_options` | Options | `None`  | VLM or API configuration      |

**Example Configuration:**

```
```

Sources: [docling/pipeline/standard\_pdf\_pipeline.py77-98](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L77-L98) [docling/datamodel/pipeline\_options.py184-204](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L184-L204)

---

### Model Downloading

Enrichment models are downloaded from Hugging Face using the `download_models` utility:

**CLI Command:**

```
```

**Programmatic Download:**

```
```

**Downloaded Artifacts:**

| Model                     | Folder                                  | Size     |
| ------------------------- | --------------------------------------- | -------- |
| CodeFormulaModel          | `ds4sd--CodeFormulaV2`                  | \~6 GB   |
| DocumentPictureClassifier | `ds4sd--DocumentFigureClassifier`       | \~500 MB |
| SmolVLM                   | `HuggingFaceTB--SmolVLM2-1.7B-Instruct` | \~3.5 GB |

Sources: [docling/utils/model\_downloader.py30-158](https://github.com/docling-project/docling/blob/f7244a43/docling/utils/model_downloader.py#L30-L158) [docling/cli/models.py30-50](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/models.py#L30-L50)

---

## Integration with Pipeline

### Enrichment Pipe Construction

The `StandardPdfPipeline` constructs the enrichment pipeline by prepending the `CodeFormulaModel` to inherited enrichment models:

**File:** [docling/pipeline/standard\_pdf\_pipeline.py77-90](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L77-L90)

```
```

Sources: [docling/pipeline/standard\_pdf\_pipeline.py77-90](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L77-L90)

---

### Execution Flow in ConvertPipeline

The `ConvertPipeline` base class implements the `_enrich_document` method that orchestrates enrichment processing:

**Diagram: Enrichment Execution in ConvertPipeline**

```
```

Sources: [docling/pipeline/base\_pipeline.py177-206](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L177-L206)

---

### Image Scaling and Cropping

Enrichment models specify their required image resolution through `images_scale` and bounding box expansion through `expansion_factor`:

**Scaling Calculation:**

```
```

**Scaling Values by Model:**

| Model                      | `images_scale` | `expansion_factor` | Effective DPI |
| -------------------------- | -------------- | ------------------ | ------------- |
| CodeFormulaModel           | 1.67           | 0.18               | 120 DPI       |
| DocumentPictureClassifier  | 2.0            | 0.0                | 144 DPI       |
| PictureDescriptionVlmModel | 1.0            | 0.0                | 72 DPI        |

Sources: [docling/models/code\_formula\_model.py70-71](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py#L70-L71) [docling/models/document\_picture\_classifier.py63](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py#L63-L63) [docling/pipeline/base\_pipeline.py177-206](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L177-L206)

---

### Backend Retention for Enrichment

When enrichment models are enabled, the pipeline retains the document backend after assembly to support image cropping:

**File:** [docling/pipeline/standard\_pdf\_pipeline.py92-98](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L92-L98)

```
```

This ensures that page images remain accessible during the enrichment phase, allowing models to crop item-specific regions from the full page images.

Sources: [docling/pipeline/standard\_pdf\_pipeline.py92-98](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L92-L98)

---

## Plugin System for Enrichment

Enrichment models are discoverable through the plugin system using Python entry points. The `docling_defaults` entry point provides default enrichment implementations:

**File:** [docling/models/plugins/defaults.py21-30](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py#L21-L30)

```
```

This allows third-party packages to register additional enrichment models by defining their own entry points.

Sources: [docling/models/plugins/defaults.py21-30](https://github.com/docling-project/docling/blob/f7244a43/docling/models/plugins/defaults.py#L21-L30) [docling/models/factories.py1-50](https://github.com/docling-project/docling/blob/f7244a43/docling/models/factories.py#L1-L50)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Enrichment Models](#enrichment-models.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Enrichment Architecture](#enrichment-architecture.md)
- [Processing Flow](#processing-flow.md)
- [Base Class Interface](#base-class-interface.md)
- [Item and Image Element Structure](#item-and-image-element-structure.md)
- [Code and Formula Enrichment](#code-and-formula-enrichment.md)
- [CodeFormulaModel](#codeformulamodel.md)
- [Processing Logic](#processing-logic.md)
- [Code Language Detection](#code-language-detection.md)
- [Formula Extraction](#formula-extraction.md)
- [Picture Classification](#picture-classification.md)
- [DocumentPictureClassifier](#documentpictureclassifier.md)
- [Classification Classes](#classification-classes.md)
- [Output Structure](#output-structure.md)
- [Picture Description](#picture-description.md)
- [PictureDescriptionVlmModel](#picturedescriptionvlmmodel.md)
- [Description Generation](#description-generation.md)
- [Custom Prompts](#custom-prompts.md)
- [API-Based Picture Description](#api-based-picture-description.md)
- [Configuration](#configuration.md)
- [Pipeline Options](#pipeline-options.md)
- [Model Downloading](#model-downloading.md)
- [Integration with Pipeline](#integration-with-pipeline.md)
- [Enrichment Pipe Construction](#enrichment-pipe-construction.md)
- [Execution Flow in ConvertPipeline](#execution-flow-in-convertpipeline.md)
- [Image Scaling and Cropping](#image-scaling-and-cropping.md)
- [Backend Retention for Enrichment](#backend-retention-for-enrichment.md)
- [Plugin System for Enrichment](#plugin-system-for-enrichment.md)
