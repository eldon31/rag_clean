Inline VLM Models | docling-project/docling | DeepWiki

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

# Inline VLM Models

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

This page documents the inline Vision Language Model (VLM) implementations in Docling. Inline VLM models run locally on the host machine, in contrast to API-based VLM models that connect to remote services. Three inference frameworks are supported: Hugging Face Transformers, MLX (for Apple Silicon acceleration), and vLLM (for optimized GPU inference).

For information about API-based VLM models that connect to remote services like Ollama or vLLM servers, see [API-Based VLM Models](docling-project/docling/4.3.2-api-based-vlm-models.md). For general VLM integration concepts and configuration options, see [Vision Language Models](docling-project/docling/4.3-vision-language-models.md).

## Architecture Overview

The inline VLM model system provides three specialized implementations sharing a common interface:

```
```

**Sources:** [docling/models/base\_model.py46-127](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L46-L127) [docling/models/vlm\_models\_inline/hf\_transformers\_model.py36-376](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L36-L376) [docling/models/vlm\_models\_inline/mlx\_model.py33-318](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L33-L318) [docling/models/vlm\_models\_inline/vllm\_model.py25-301](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L25-L301)

## Configuration via InlineVlmOptions

All inline VLM models are configured through `InlineVlmOptions`, which specifies the model repository, inference framework, and generation parameters:

| Parameter                   | Type                                               | Description                                                                                                |
| --------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `repo_id`                   | `str`                                              | Hugging Face repository identifier (e.g., `"ibm-granite/granite-docling-258M"`)                            |
| `inference_framework`       | `InferenceFramework`                               | One of `TRANSFORMERS`, `MLX`, or `VLLM`                                                                    |
| `transformers_model_type`   | `TransformersModelType`                            | Auto-loading class: `AUTOMODEL`, `AUTOMODEL_VISION2SEQ`, `AUTOMODEL_CAUSALLM`, `AUTOMODEL_IMAGETEXTTOTEXT` |
| `transformers_prompt_style` | `TransformersPromptStyle`                          | Prompt formatting: `CHAT`, `RAW`, or `NONE`                                                                |
| `response_format`           | `ResponseFormat`                                   | Expected output format: `DOCTAGS`, `MARKDOWN`, `HTML`, `OTSL`, or `PLAINTEXT`                              |
| `torch_dtype`               | `Optional[str]`                                    | PyTorch dtype (e.g., `"bfloat16"`)                                                                         |
| `max_new_tokens`            | `int`                                              | Maximum tokens to generate (default: `4096`)                                                               |
| `temperature`               | `float`                                            | Sampling temperature (default: `0.0` for greedy)                                                           |
| `scale`                     | `float`                                            | Image scaling factor (default: `2.0`)                                                                      |
| `max_size`                  | `Optional[int]`                                    | Maximum image dimension                                                                                    |
| `use_kv_cache`              | `bool`                                             | Enable key-value caching (default: `True`)                                                                 |
| `stop_strings`              | `List[str]`                                        | Strings that trigger generation stop                                                                       |
| `custom_stopping_criteria`  | `List[Union[StoppingCriteria, GenerationStopper]]` | Custom stopping logic                                                                                      |
| `extra_generation_config`   | `Dict[str, Any]`                                   | Additional framework-specific generation parameters                                                        |
| `extra_processor_kwargs`    | `Dict[str, Any]`                                   | Additional processor parameters                                                                            |
| `quantized`                 | `bool`                                             | Enable quantization (default: `False`)                                                                     |
| `load_in_8bit`              | `bool`                                             | Use 8-bit quantization (default: `True`)                                                                   |
| `trust_remote_code`         | `bool`                                             | Allow remote code execution (default: `False`)                                                             |
| `revision`                  | `str`                                              | Model revision/branch (default: `"main"`)                                                                  |

**Sources:** [docling/datamodel/pipeline\_options\_vlm\_model.py54-89](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L54-L89)

## Hugging Face Transformers Implementation

### Model Loading and Initialization

`HuggingFaceTransformersVlmModel` loads models using Transformers' auto-loading classes:

```
```

The model class is selected based on `transformers_model_type`:

- `AUTOMODEL` → `AutoModel`
- `AUTOMODEL_CAUSALLM` → `AutoModelForCausalLM`
- `AUTOMODEL_VISION2SEQ` → `AutoModelForVision2Seq`
- `AUTOMODEL_IMAGETEXTTOTEXT` → `AutoModelForImageTextToText`

The processor's tokenizer padding is configured with `padding_side = "left"` for batch processing.

**Sources:** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py36-138](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L36-L138)

### Batch Inference Pipeline

The Transformers implementation processes images in batches:

```
```

**Key Implementation Details:**

1. **Image Normalization** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py209-224](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L209-L224): Converts numpy arrays to PIL RGB images
2. **Prompt Handling** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py229-236](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L229-L236): Accepts single prompt string or list of prompts (one per image)
3. **Processor Integration** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py240-256](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L240-L256): Handles both text and image preprocessing with automatic padding
4. **Stopping Criteria** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py260-296](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L260-L296): Supports `StopStringCriteria` and custom `GenerationStopper` instances
5. **Token Trimming** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py343-344](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L343-L344): Removes input tokens from output sequences using attention mask

**Sources:** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py139-376](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L139-L376)

### Stopping Criteria Handling

The Transformers implementation supports two types of stopping criteria:

```
```

The implementation distinguishes between:

- **String-based stopping** via `StopStringCriteria` [docling/models/vlm\_models\_inline/hf\_transformers\_model.py264-269](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L264-L269)
- **GenerationStopper classes/instances** wrapped in `HFStoppingCriteriaWrapper` [docling/models/vlm\_models\_inline/hf\_transformers\_model.py276-283](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L276-L283)
- **Native StoppingCriteria classes** instantiated with tokenizer [docling/models/vlm\_models\_inline/hf\_transformers\_model.py284-287](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L284-L287)
- **StoppingCriteria instances** used directly [docling/models/vlm\_models\_inline/hf\_transformers\_model.py294-296](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L294-L296)

**Sources:** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py260-302](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L260-L302)

## MLX Implementation (Apple Silicon)

### Architecture and Thread Safety

`HuggingFaceMlxModel` uses the MLX framework for Apple Silicon acceleration with important thread safety considerations:

```
```

**Critical Constraint:** MLX models are **not thread-safe**. All MLX inference operations are serialized using a global lock [docling/models/vlm\_models\_inline/mlx\_model.py28-30](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L28-L30):

```
```

This means only one MLX model instance can perform inference at a time across the entire process.

**Sources:** [docling/models/vlm\_models\_inline/mlx\_model.py28-90](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L28-L90)

### Streaming Generation and Token Collection

Unlike the Transformers implementation, MLX uses streaming generation:

```
```

**Key Characteristics:**

1. **No Batching** [docling/models/vlm\_models\_inline/mlx\_model.py186-188](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L186-L188): Images are processed sequentially within the global lock
2. **Token-Level Collection** [doclog/models/vlm\_models\_inline/mlx\_model.py232-254](https://github.com/docling-project/docling/blob/f7244a43/doclog/models/vlm_models_inline/mlx_model.py#L232-L254): Each token includes text, token ID, and log probability
3. **Early Stopping** [docling/models/vlm\_models\_inline/mlx\_model.py258-302](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L258-L302): Stop strings and `GenerationStopper` instances are checked during streaming
4. **Lookback Window** [docling/models/vlm\_models\_inline/mlx\_model.py279-287](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L279-L287): Custom stoppers can specify how many recent characters to examine

**Sources:** [docling/models/vlm\_models\_inline/mlx\_model.py149-318](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L149-L318)

### Stopping Criteria Validation

MLX enforces strict stopping criteria types [docling/models/vlm\_models\_inline/mlx\_model.py75-89](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L75-L89):

| Allowed                       | Not Allowed                  |
| ----------------------------- | ---------------------------- |
| `GenerationStopper` instances | `StoppingCriteria` instances |
| `GenerationStopper` classes   | `StoppingCriteria` classes   |
| Stop strings                  | -                            |

If Hugging Face `StoppingCriteria` is detected, a `ValueError` is raised with a clear message explaining that only `GenerationStopper` is supported for MLX.

**Sources:** [docling/models/vlm\_models\_inline/mlx\_model.py75-89](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py#L75-L89)

## vLLM Implementation

### Configuration and Initialization

`VllmVlmModel` provides GPU-optimized inference with strict separation of load-time and runtime parameters:

```
```

**Parameter Allowlists:**

The implementation maintains two explicit allowlists [docling/models/vlm\_models\_inline/vllm\_model.py32-80](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L32-L80):

1. **`_VLLM_ENGINE_KEYS`** - Parameters passed to `LLM.__init__()` (load time)
2. **`_VLLM_SAMPLING_KEYS`** - Parameters passed to `SamplingParams` (runtime)

Any keys in `extra_generation_config` not in either allowlist trigger a warning and are ignored.

**Sources:** [docling/models/vlm\_models\_inline/vllm\_model.py82-174](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L82-L174)

### Batch Inference with Multi-Modal Data

vLLM processes images as multi-modal data in batch mode:

```
```

**Key Features:**

1. **True Batching** [docling/models/vlm\_models\_inline/vllm\_model.py233-300](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L233-L300): vLLM processes all images in a single `generate()` call
2. **Multi-Modal Data Format** [docling/models/vlm\_models\_inline/vllm\_model.py277-280](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L277-L280): Images are passed via `multi_modal_data` dictionary with `"image"` key
3. **Memory Limit** [docling/models/vlm\_models\_inline/vllm\_model.py140](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L140-L140): `limit_mm_per_prompt={"image": 1}` restricts one image per prompt
4. **GPU Memory Management** [docling/models/vlm\_models\_inline/vllm\_model.py146-151](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L146-L151): Defaults to 30% GPU memory utilization to share with other models

**Sources:** [docling/models/vlm\_models\_inline/vllm\_model.py175-301](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L175-L301)

## Prompt Formatting

All inline VLM models share the `formulate_prompt()` method from `BaseVlmPageModel`:

```
```

**Prompt Style Options:**

| Style          | Behavior                               | Use Case                                            |
| -------------- | -------------------------------------- | --------------------------------------------------- |
| `RAW`          | Returns user prompt unchanged          | Models that handle formatting internally            |
| `NONE`         | Returns empty string                   | Models that don't need text prompts (e.g., GOT-OCR) |
| `CHAT`         | Applies processor's chat template      | Standard instruction-following models               |
| Custom (Phi-4) | Special formatting for specific models | Model-specific requirements                         |

**Sources:** [docling/models/base\_model.py85-126](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py#L85-L126)

## Model Download and Caching

All inline VLM implementations inherit from `HuggingFaceModelDownloadMixin`:

```
```

The `repo_cache_folder` property converts slashes in `repo_id` to dashes (e.g., `"ibm-granite/granite-docling-258M"` → `"ibm-granite--granite-docling-258M"`).

**Sources:** [docling/models/utils/hf\_model\_download.py8-45](https://github.com/docling-project/docling/blob/f7244a43/docling/models/utils/hf_model_download.py#L8-L45) [docling/datamodel/pipeline\_options\_vlm\_model.py86-88](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L86-L88)

## Available Model Specifications

Docling provides pre-configured model specifications in `vlm_model_specs`:

### DocTags Output Models

| Model Spec                    | Repository                                | Framework    | Devices   | Response Format |
| ----------------------------- | ----------------------------------------- | ------------ | --------- | --------------- |
| `GRANITEDOCLING_TRANSFORMERS` | `ibm-granite/granite-docling-258M`        | Transformers | CPU, CUDA | DOCTAGS         |
| `GRANITEDOCLING_VLLM`         | `ibm-granite/granite-docling-258M`        | vLLM         | CUDA      | DOCTAGS         |
| `GRANITEDOCLING_MLX`          | `ibm-granite/granite-docling-258M-mlx`    | MLX          | MPS       | DOCTAGS         |
| `SMOLDOCLING_TRANSFORMERS`    | `ds4sd/SmolDocling-256M-preview`          | Transformers | CPU, CUDA | DOCTAGS         |
| `SMOLDOCLING_VLLM`            | `ds4sd/SmolDocling-256M-preview`          | vLLM         | CUDA      | DOCTAGS         |
| `SMOLDOCLING_MLX`             | `ds4sd/SmolDocling-256M-preview-mlx-bf16` | MLX          | MPS       | DOCTAGS         |

### Markdown Output Models

| Model Spec                    | Repository                                  | Framework    | Devices        | Response Format |
| ----------------------------- | ------------------------------------------- | ------------ | -------------- | --------------- |
| `GRANITE_VISION_TRANSFORMERS` | `ibm-granite/granite-vision-3.2-2b`         | Transformers | CPU, CUDA, MPS | MARKDOWN        |
| `GRANITE_VISION_VLLM`         | `ibm-granite/granite-vision-3.2-2b`         | vLLM         | CUDA           | MARKDOWN        |
| `PIXTRAL_12B_TRANSFORMERS`    | `mistral-community/pixtral-12b`             | Transformers | CPU, CUDA      | MARKDOWN        |
| `PIXTRAL_12B_MLX`             | `mlx-community/pixtral-12b-bf16`            | MLX          | MPS            | MARKDOWN        |
| `PHI4_TRANSFORMERS`           | `microsoft/Phi-4-multimodal-instruct`       | Transformers | CPU, CUDA      | MARKDOWN        |
| `QWEN25_VL_3B_MLX`            | `mlx-community/Qwen2.5-VL-3B-Instruct-bf16` | MLX          | MPS            | MARKDOWN        |
| `GOT2_TRANSFORMERS`           | `stepfun-ai/GOT-OCR-2.0-hf`                 | Transformers | CPU, CUDA      | MARKDOWN        |
| `GEMMA3_12B_MLX`              | `mlx-community/gemma-3-12b-it-bf16`         | MLX          | MPS            | MARKDOWN        |
| `GEMMA3_27B_MLX`              | `mlx-community/gemma-3-27b-it-bf16`         | MLX          | MPS            | MARKDOWN        |
| `DOLPHIN_TRANSFORMERS`        | `ByteDance/Dolphin`                         | Transformers | CPU, CUDA, MPS | MARKDOWN        |

### Plaintext Output Models

| Model Spec                | Repository                            | Framework    | Devices   | Response Format |
| ------------------------- | ------------------------------------- | ------------ | --------- | --------------- |
| `SMOLVLM256_TRANSFORMERS` | `HuggingFaceTB/SmolVLM-256M-Instruct` | Transformers | CPU, CUDA | PLAINTEXT       |
| `SMOLVLM256_MLX`          | `moot20/SmolVLM-256M-Instruct-MLX`    | MLX          | MPS       | PLAINTEXT       |
| `SMOLVLM256_VLLM`         | `HuggingFaceTB/SmolVLM-256M-Instruct` | vLLM         | CUDA      | PLAINTEXT       |

### Extraction Models

| Model Spec                   | Repository                | Framework    | Devices        | Response Format |
| ---------------------------- | ------------------------- | ------------ | -------------- | --------------- |
| `NU_EXTRACT_2B_TRANSFORMERS` | `numind/NuExtract-2.0-2B` | Transformers | CPU, CUDA, MPS | PLAINTEXT       |

**Special Configuration Notes:**

1. **GOT-OCR-2.0** uses `TransformersPromptStyle.NONE` and includes `extra_processor_kwargs={"format": True}`
2. **Phi-4** requires `transformers<4.52.0` and uses `extra_generation_config={"num_logits_to_keep": 0}`
3. **Dolphin** uses `TransformersPromptStyle.RAW` with a custom prompt format
4. **GraniteDocling VLLM** uses `revision="untied"` for compatibility with vLLM ≤0.10.2

**Sources:** [docling/datamodel/vlm\_model\_specs.py1-303](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L1-L303)

## Usage Examples

### Basic Usage with Default Model

```
```

### Selecting a Specific Model

```
```

### Custom Model Configuration

```
```

### Direct Image Processing

All inline VLM models support direct image processing via the `process_images()` method:

```
```

**Sources:** [docs/examples/minimal\_vlm\_pipeline.py1-71](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal_vlm_pipeline.py#L1-L71) [docs/usage/vision\_models.md1-124](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L1-L124)

## Performance Considerations

### Framework Comparison

| Framework        | Batching             | Thread Safety          | Best For                            |
| ---------------- | -------------------- | ---------------------- | ----------------------------------- |
| **Transformers** | ✅ Full batch support | ✅ Thread-safe          | General purpose, CPU/CUDA/MPS       |
| **MLX**          | ❌ Sequential only    | ❌ Global lock required | Apple Silicon (fastest on M-series) |
| **vLLM**         | ✅ Optimized batching | ✅ Thread-safe          | High-throughput GPU inference       |

### Memory Management

1. **Transformers**: Uses PyTorch's default memory management; consider `torch_dtype="bfloat16"` for memory savings
2. **MLX**: Automatically manages unified memory on Apple Silicon
3. **vLLM**: Set `gpu_memory_utilization` (default 0.3) to reserve GPU memory for other models

### Acceleration Options

- **Flash Attention 2**: Automatically enabled on CUDA devices when `accelerator_options.cuda_use_flash_attention2=True`
- **Quantization**: Enable with `quantized=True` and `load_in_8bit=True` (Transformers and vLLM only)
- **KV Cache**: Enabled by default with `use_kv_cache=True`; disable only if memory is constrained

**Sources:** [docling/models/vlm\_models\_inline/hf\_transformers\_model.py123-128](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L123-L128) [docling/models/vlm\_models\_inline/vllm\_model.py146-155](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py#L146-L155) [docs/usage/vision\_models.md46-58](https://github.com/docling-project/docling/blob/f7244a43/docs/usage/vision_models.md#L46-L58)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Inline VLM Models](#inline-vlm-models.md)
- [Architecture Overview](#architecture-overview.md)
- [Configuration via InlineVlmOptions](#configuration-via-inlinevlmoptions.md)
- [Hugging Face Transformers Implementation](#hugging-face-transformers-implementation.md)
- [Model Loading and Initialization](#model-loading-and-initialization.md)
- [Batch Inference Pipeline](#batch-inference-pipeline.md)
- [Stopping Criteria Handling](#stopping-criteria-handling.md)
- [MLX Implementation (Apple Silicon)](#mlx-implementation-apple-silicon.md)
- [Architecture and Thread Safety](#architecture-and-thread-safety.md)
- [Streaming Generation and Token Collection](#streaming-generation-and-token-collection.md)
- [Stopping Criteria Validation](#stopping-criteria-validation.md)
- [vLLM Implementation](#vllm-implementation.md)
- [Configuration and Initialization](#configuration-and-initialization.md)
- [Batch Inference with Multi-Modal Data](#batch-inference-with-multi-modal-data.md)
- [Prompt Formatting](#prompt-formatting.md)
- [Model Download and Caching](#model-download-and-caching.md)
- [Available Model Specifications](#available-model-specifications.md)
- [DocTags Output Models](#doctags-output-models.md)
- [Markdown Output Models](#markdown-output-models.md)
- [Plaintext Output Models](#plaintext-output-models.md)
- [Extraction Models](#extraction-models.md)
- [Usage Examples](#usage-examples.md)
- [Basic Usage with Default Model](#basic-usage-with-default-model.md)
- [Selecting a Specific Model](#selecting-a-specific-model.md)
- [Custom Model Configuration](#custom-model-configuration.md)
- [Direct Image Processing](#direct-image-processing.md)
- [Performance Considerations](#performance-considerations.md)
- [Framework Comparison](#framework-comparison.md)
- [Memory Management](#memory-management.md)
- [Acceleration Options](#acceleration-options.md)
