Vision Language Models | docling-project/docling | DeepWiki

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

# Vision Language Models

Relevant source files

- [README.md](https://github.com/docling-project/docling/blob/f7244a43/README.md)
- [docling/datamodel/pipeline\_options\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py)
- [docling/datamodel/vlm\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py)
- [docling/models/api\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py)
- [docling/models/base\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py)
- [docling/models/utils/hf\_model\_download.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/utils/hf_model_download.py)
- [docling/models/vlm\_models\_inline/hf\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py)
- [docling/models/vlm\_models\_inline/mlx\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py)
- [docling/models/vlm\_models\_inline/vllm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py)
- [docs/examples/minimal\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py)
- [docs/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/index.md)
- [docs/usage/index.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/index.md)
- [docs/usage/mcp.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/mcp.md)
- [docs/usage/vision\_models.md](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md)
- [mkdocs.yml](https://github.com/docling-project/docling/blob/f7244a43/mkdocs.yml)

Vision Language Models (VLMs) in Docling enable end-to-end document understanding by processing document page images directly through multimodal AI models. Unlike the traditional pipeline approach that uses specialized models for layout, tables, and OCR, VLMs can perform document analysis in a single inference pass, generating structured output formats like DOCTAGS, Markdown, or HTML.

This page provides an overview of VLM integration in Docling, covering available model variants, response formats, and configuration options. For detailed implementation of inline VLM models (Transformers, MLX, vLLM), see [Inline VLM Models](docling-project/docling/4.3.1-inline-vlm-models.md). For API-based VLM integration, see [API-Based VLM Models](docling-project/docling/4.3.2-api-based-vlm-models.md). For pipeline-level VLM usage, see [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md).

Sources: [docling/models/base\_model.py46-66](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L46-L66) [docling/datamodel/pipeline\_options\_vlm\_model.py13-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L13-L32) [docs/usage/vision\_models.md1-10](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L1-L10)

## VLM Integration Architecture

Docling provides a unified interface for VLM integration supporting both local model execution and external API services. The architecture separates model deployment strategy from the VLM capabilities exposed to pipelines.

**Diagram: VLM Integration Architecture**

```
```

The architecture provides two key abstractions:

- **`BaseVlmPageModel`**: Defines the interface for page-level VLM processing, requiring implementations to provide `__call__(conv_res, page_batch)` and `process_images(image_batch, prompt)` methods
- **`BaseVlmOptions`**: Provides configuration for VLM behavior including prompts, scaling, temperature, and response format handling

Sources: [docling/models/base\_model.py46-127](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L46-L127) [docling/datamodel/pipeline\_options\_vlm\_model.py13-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L13-L32) [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)

## Available VLM Model Variants

Docling provides pre-configured specifications for popular VLM models, optimized for document understanding tasks. These are defined in `vlm_model_specs` and can be used directly or customized.

**Diagram: VLM Model Variants and Frameworks**

```
```

### GraniteDocling Models

GraniteDocling is a specialized 258M parameter model trained for document understanding that outputs structured DOCTAGS format. It represents the recommended choice for document conversion in Docling.

| Variant                          | Repo ID                                | Framework    | Devices   | Notes                          |
| -------------------------------- | -------------------------------------- | ------------ | --------- | ------------------------------ |
| **GRANITEDOCLING\_TRANSFORMERS** | `ibm-granite/granite-docling-258M`     | Transformers | CPU, CUDA | Default for non-Apple hardware |
| **GRANITEDOCLING\_MLX**          | `ibm-granite/granite-docling-258M-mlx` | MLX          | MPS       | Optimized for Apple Silicon    |
| **GRANITEDOCLING\_VLLM**         | `ibm-granite/granite-docling-258M`     | vLLM         | CUDA      | High-throughput inference      |

Configuration example:

```
```

Sources: [docling/datamodel/vlm\_model\_specs.py21-56](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L21-L56) [docs/usage/vision\_models.md40-87](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L40-L87)

### SmolDocling Models

SmolDocling is another 256M parameter model designed for document understanding with DOCTAGS output. It provides an alternative to GraniteDocling with similar capabilities.

| Variant                       | Repo ID                                   | Framework    | Devices   |
| ----------------------------- | ----------------------------------------- | ------------ | --------- |
| **SMOLDOCLING\_TRANSFORMERS** | `ds4sd/SmolDocling-256M-preview`          | Transformers | CPU, CUDA |
| **SMOLDOCLING\_MLX**          | `ds4sd/SmolDocling-256M-preview-mlx-bf16` | MLX          | MPS       |
| **SMOLDOCLING\_VLLM**         | `ds4sd/SmolDocling-256M-preview`          | vLLM         | CUDA      |

Sources: [docling/datamodel/vlm\_model\_specs.py58-97](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L58-L97)

### General-Purpose VLM Models

Docling supports general-purpose VLMs that output Markdown or HTML, suitable for document conversion when DOCTAGS-trained models are not required.

| Model                  | Primary Output | Notable Features                                |
| ---------------------- | -------------- | ----------------------------------------------- |
| **Granite Vision 3.2** | Markdown       | IBM's 2B vision model, multi-framework support  |
| **Pixtral 12B**        | Markdown       | Mistral's 12B multimodal model                  |
| **Qwen2.5-VL**         | Markdown       | 3B parameter model with strong OCR capabilities |
| **Phi-4**              | Markdown       | Microsoft's 14B multimodal model                |
| **GOT-OCR 2.0**        | Markdown       | Specialized OCR model with format preservation  |

Example configuration for Granite Vision:

```
```

Sources: [docling/datamodel/vlm\_model\_specs.py143-245](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L143-L245) [docs/usage/vision\_models.md46-58](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L46-L58)

### Custom Model Configuration

Beyond pre-configured models, custom VLMs can be integrated by specifying `InlineVlmOptions` directly:

```
```

Sources: [docs/usage/vision\_models.md88-113](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L88-L113) [docling/datamodel/pipeline\_options\_vlm\_model.py54-89](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L54-L89)

## Response Formats

VLM models support multiple output formats optimized for different document understanding tasks. The response format determines how the VLM structures its output and how Docling processes it into a `DoclingDocument`.

**Diagram: Response Format Processing**

```
```

### DOCTAGS Format

DOCTAGS is an XML-based structured format designed specifically for document understanding. It provides the most accurate representation of document structure and is the recommended format for document conversion.

Example DOCTAGS output:

```
```

Models trained for DOCTAGS output include:

- GraniteDocling (all variants)
- SmolDocling (all variants)

Configuration:

```
```

Sources: [docling/datamodel/pipeline\_options\_vlm\_model.py27-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L27-L32) [docling/datamodel/vlm\_model\_specs.py22-37](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L22-L37)

### Markdown Format

Markdown format outputs standard Markdown syntax, suitable for general-purpose document representation. This format is widely compatible with downstream tools and libraries.

Example Markdown output:

```
```

Models outputting Markdown include:

- Granite Vision
- Pixtral
- Qwen2.5-VL
- GOT-OCR 2.0

Configuration:

```
```

Sources: [docling/datamodel/vlm\_model\_specs.py144-157](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L144-L157) [docs/usage/vision\_models.md4-9](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L4-L9)

### HTML Format

HTML format outputs HTML markup, preserving semantic document structure through HTML tags. This format is useful for web-based applications and rich document viewers.

Configuration:

```
```

Sources: [docling/datamodel/pipeline\_options\_vlm\_model.py27-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L27-L32)

### Custom Response Processing

The `decode_response()` method in `BaseVlmOptions` allows custom post-processing of VLM outputs. This enables integration with models that return structured responses requiring transformation.

Example implementation:

```
```

This pattern is used internally for specialized models like OlmOcr that return JSON-structured responses.

Sources: [docling/datamodel/pipeline\_options\_vlm\_model.py20-24](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L20-L24)

## VLM Configuration Options

VLM behavior is controlled through configuration classes that specify model selection, inference parameters, and processing options.

**Diagram: VLM Configuration Hierarchy**

```
```

### Core Configuration Parameters

| Parameter            | Type             | Default        | Description                                |
| -------------------- | ---------------- | -------------- | ------------------------------------------ |
| **prompt**           | `str`            | Model-specific | Prompt text sent to VLM                    |
| **scale**            | `float`          | `2.0`          | Image scaling factor for higher resolution |
| **max\_size**        | `Optional[int]`  | `None`         | Maximum image dimension (pixels)           |
| **temperature**      | `float`          | `0.0`          | Sampling temperature (0.0 = deterministic) |
| **response\_format** | `ResponseFormat` | Required       | Expected output format                     |

### Inline Model Parameters

| Parameter                | Type                      | Purpose                                      |
| ------------------------ | ------------------------- | -------------------------------------------- |
| **repo\_id**             | `str`                     | HuggingFace model repository identifier      |
| **revision**             | `str`                     | Model version/branch (default: "main")       |
| **inference\_framework** | `InferenceFramework`      | Framework selection: MLX, TRANSFORMERS, VLLM |
| **max\_new\_tokens**     | `int`                     | Maximum tokens to generate (default: 4096)   |
| **stop\_strings**        | `List[str]`               | Strings that trigger generation stop         |
| **supported\_devices**   | `List[AcceleratorDevice]` | Compatible hardware devices                  |

### API Model Parameters

| Parameter       | Type             | Purpose                             |
| --------------- | ---------------- | ----------------------------------- |
| **url**         | `AnyUrl`         | API endpoint URL                    |
| **headers**     | `Dict[str, str]` | HTTP headers (e.g., authentication) |
| **timeout**     | `float`          | Request timeout in seconds          |
| **concurrency** | `int`            | Number of parallel API requests     |

Sources: [docling/datamodel/pipeline\_options\_vlm\_model.py13-112](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L13-L112)

### Generation Control

VLM generation behavior can be fine-tuned through stopping criteria and generation configuration:

**Stop Strings**: Simple string-based stopping

```
```

**Custom Stopping Criteria**: Programmatic stopping logic

```
```

**Extra Generation Config**: Framework-specific parameters

```
```

Sources: [docling/datamodel/pipeline\_options\_vlm\_model.py78-82](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L78-L82) [docling/models/utils/generation\_utils.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/utils/generation_utils.py)

## Prompt Construction and Formatting

VLM prompts are constructed through the `build_prompt()` method, which can be customized to include page-specific context or structured instructions.

**Diagram: Prompt Processing Flow**

```
```

### Prompt Styles

| Style    | Usage                            | Example                         |
| -------- | -------------------------------- | ------------------------------- |
| **CHAT** | Uses model's chat template       | \`<                             |
| **RAW**  | Direct prompt without formatting | `Convert this page to docling.` |
| **NONE** | No text prompt (image-only)      | `""`                            |

### Dynamic Prompt Construction

The `build_prompt()` method can access page metadata for context-aware prompts:

```
```

Sources: [docling/models/base\_model.py85-126](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L85-L126) [docling/datamodel/pipeline\_options\_vlm\_model.py20-24](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L20-L24)

## Response Formats and Processing

VLM models support multiple output formats optimized for different document understanding tasks and downstream processing requirements.

### Response Format Types

```
```

### Custom Response Processing

VLM options support custom response processing through the `decode_response()` method, enabling specialized handling for specific model outputs:

```
```

This pattern allows integration with models that return structured responses requiring post-processing before integration into the document representation.

Sources: [docling/datamodel/pipeline\_options\_vlm\_model.py18-22](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L18-L22) [docs/examples/vlm\_pipeline\_api\_model.py78-85](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/vlm_pipeline_api_model.py#L78-L85)

## VLM Integration Examples

The codebase includes comprehensive examples demonstrating VLM integration patterns for different deployment scenarios and model types.

### Multi-Model Comparison Framework

The `compare_vlm_models.py` example provides a systematic approach for evaluating different VLM models and frameworks:

```
```

This framework enables systematic evaluation of model performance, output quality, and resource utilization across different VLM implementations.

Sources: [docs/examples/compare\_vlm\_models.py33-101](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/compare_vlm_models.py#L33-L101) [docs/examples/compare\_vlm\_models.py146-198](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/compare_vlm_models.py#L146-L198)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Vision Language Models](#vision-language-models.md)
- [VLM Integration Architecture](#vlm-integration-architecture.md)
- [Available VLM Model Variants](#available-vlm-model-variants.md)
- [GraniteDocling Models](#granitedocling-models.md)
- [SmolDocling Models](#smoldocling-models.md)
- [General-Purpose VLM Models](#general-purpose-vlm-models.md)
- [Custom Model Configuration](#custom-model-configuration.md)
- [Response Formats](#response-formats.md)
- [DOCTAGS Format](#doctags-format.md)
- [Markdown Format](#markdown-format.md)
- [HTML Format](#html-format.md)
- [Custom Response Processing](#custom-response-processing.md)
- [VLM Configuration Options](#vlm-configuration-options.md)
- [Core Configuration Parameters](#core-configuration-parameters.md)
- [Inline Model Parameters](#inline-model-parameters.md)
- [API Model Parameters](#api-model-parameters.md)
- [Generation Control](#generation-control.md)
- [Prompt Construction and Formatting](#prompt-construction-and-formatting.md)
- [Prompt Styles](#prompt-styles.md)
- [Dynamic Prompt Construction](#dynamic-prompt-construction.md)
- [Response Formats and Processing](#response-formats-and-processing.md)
- [Response Format Types](#response-format-types.md)
- [Custom Response Processing](#custom-response-processing-1.md)
- [VLM Integration Examples](#vlm-integration-examples.md)
- [Multi-Model Comparison Framework](#multi-model-comparison-framework.md)
