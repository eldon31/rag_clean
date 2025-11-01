API-Based VLM Models | docling-project/docling | DeepWiki

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

# API-Based VLM Models

Relevant source files

- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/datamodel/pipeline\_options\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py)
- [docling/datamodel/vlm\_model\_specs.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/api\_vlm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py)
- [docling/models/base\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_model.py)
- [docling/models/utils/hf\_model\_download.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/utils/hf_model_download.py)
- [docling/models/vlm\_models\_inline/hf\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py)
- [docling/models/vlm\_models\_inline/mlx\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/mlx_model.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/models/vlm\_models\_inline/vllm\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/vllm_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)

## Purpose and Scope

This page documents the API-based Vision Language Model (VLM) integration in Docling, which enables document processing using external VLM services via OpenAI-compatible HTTP APIs. API-based models connect to remote inference servers (e.g., Ollama, vLLM server, OpenAI) rather than loading models locally.

For locally-executed VLM models using Transformers, MLX, or vLLM frameworks, see [Inline VLM Models](docling-project/docling/4.3.1-inline-vlm-models.md). For the broader VLM system architecture and pipeline integration, see [Vision Language Models](docling-project/docling/4.3-vision-language-models.md).

API-based models are configured through `ApiVlmOptions` and executed by the `ApiVlmModel` class, which provides threaded request handling, streaming support, and early-abort capabilities through custom stopping criteria.

**Sources:** [docling/models/api\_vlm\_model.py1-102](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L1-L102) [docling/datamodel/pipeline\_options\_vlm\_model.py96-112](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L96-L112)

---

## System Architecture

```
```

**Diagram: API-Based VLM Model Architecture**

The architecture separates configuration (`ApiVlmOptions`), execution (`ApiVlmModel`), and HTTP communication (`api_image_request` functions). The `ThreadPoolExecutor` enables concurrent processing of page batches, while the streaming path supports early termination via `GenerationStopper` instances.

**Sources:** [docling/models/api\_vlm\_model.py19-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L19-L101) [docling/pipeline/vlm\_pipeline.py66-73](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L66-L73)

---

## Configuration: ApiVlmOptions

The `ApiVlmOptions` class defines all parameters for connecting to and configuring an external VLM API:

| Field                      | Type                           | Default                                      | Description                                      |
| -------------------------- | ------------------------------ | -------------------------------------------- | ------------------------------------------------ |
| `kind`                     | `Literal["api_model_options"]` | `"api_model_options"`                        | Discriminator for option type                    |
| `url`                      | `AnyUrl`                       | `http://localhost:11434/v1/chat/completions` | API endpoint URL (OpenAI-compatible)             |
| `headers`                  | `Dict[str, str]`               | `{}`                                         | HTTP headers (e.g., authorization)               |
| `params`                   | `Dict[str, Any]`               | `{}`                                         | Model-specific parameters (e.g., `model` name)   |
| `timeout`                  | `float`                        | `60`                                         | Request timeout in seconds                       |
| `concurrency`              | `int`                          | `1`                                          | Number of concurrent page requests               |
| `response_format`          | `ResponseFormat`               | —                                            | Expected response format (DOCTAGS/Markdown/HTML) |
| `prompt`                   | `str`                          | —                                            | User prompt template                             |
| `scale`                    | `float`                        | `2.0`                                        | Image scaling factor                             |
| `max_size`                 | `Optional[int]`                | `None`                                       | Maximum image dimension                          |
| `temperature`              | `float`                        | `0.0`                                        | Generation temperature                           |
| `stop_strings`             | `List[str]`                    | `[]`                                         | Stop string tokens                               |
| `custom_stopping_criteria` | `List[GenerationStopper]`      | `[]`                                         | Early-abort logic instances                      |

**Key Configuration Patterns:**

```
```

The `url` must point to an OpenAI-compatible `/v1/chat/completions` endpoint. The `params` dict is merged with runtime temperature settings and passed as the request body. The `concurrency` parameter controls the `ThreadPoolExecutor` worker count.

**Sources:** [docling/datamodel/pipeline\_options\_vlm\_model.py96-112](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L96-L112) [docling/datamodel/vlm\_model\_specs.py171-179](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L171-L179)

---

## Request Flow Sequence

```
```

**Diagram: API VLM Request Flow**

The `ApiVlmModel.__call__` method uses `ThreadPoolExecutor.map` to process pages concurrently. Each worker thread executes `_vlm_request`, which retrieves the page image, formats the prompt, and makes an HTTP request. If custom stopping criteria are configured, the streaming path (`api_image_request_streaming`) is used to enable early termination.

**Sources:** [docling/models/api\_vlm\_model.py43-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L43-L101)

---

## ApiVlmModel Implementation

### Class Structure

The `ApiVlmModel` class implements `BasePageModel` and orchestrates API-based inference:

```
```

**Initialization Validation:**

The constructor enforces the `enable_remote_services` flag to prevent accidental external connections:

```
```

This safety check requires explicit opt-in at the pipeline level before API requests are allowed.

**Sources:** [docling/models/api\_vlm\_model.py20-41](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L20-L41)

### Request Execution Pattern

The `_vlm_request` helper function processes a single page:

1. **Validation:** Check `page._backend.is_valid()`
2. **Image Extraction:** Call `page.get_image(scale, max_size)` and convert to RGB
3. **Prompt Construction:** Use `vlm_options.build_prompt(page.parsed_page)`
4. **Stopping Criteria Processing:** Instantiate any `GenerationStopper` classes
5. **API Call:** Route to streaming or non-streaming based on `custom_stopping_criteria`
6. **Response Decoding:** Apply `vlm_options.decode_response()`
7. **Result Attachment:** Set `page.predictions.vlm_response`

**Concurrency Control:**

```
```

The executor processes up to `concurrency` pages in parallel, with each thread making independent HTTP requests. This is essential for throughput when processing large documents.

**Sources:** [docling/models/api\_vlm\_model.py43-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L43-L101)

---

## Streaming and Early Abort

### Streaming Request Flow

When `custom_stopping_criteria` is non-empty, the model uses the streaming API path:

```
```

### GenerationStopper Interface

The `GenerationStopper` protocol enables custom early-abort logic:

```
```

Streaming requests check `should_stop()` after each token chunk arrives. This allows stopping generation when:

- A specific pattern is detected (e.g., closing XML tag)
- A confidence threshold is crossed
- A maximum content length is reached

**Sources:** [docling/models/api\_vlm\_model.py63-97](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L63-L97)

---

## Pipeline Integration

### VlmPipeline Instantiation

The `VlmPipeline` detects `ApiVlmOptions` and instantiates `ApiVlmModel`:

```
```

This is the sole model in the `build_pipe` list, as API-based inference is end-to-end (no separate OCR, layout, or table models).

**Sources:** [docling/pipeline/vlm\_pipeline.py66-73](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py#L66-L73)

### Page Processing

The pipeline's `initialize_page` method loads page backends, then `_apply_on_pages` iterates the `build_pipe`:

```
```

For `ApiVlmModel`, the `__call__` method internally uses the thread pool, so the outer iteration is straightforward. The model modifies `page.predictions.vlm_response` in-place and yields the updated pages.

**Sources:** [docling/pipeline/base\_pipeline.py189-195](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L189-L195)

---

## Predefined API Configurations

The `docling/datamodel/vlm_model_specs.py` module provides ready-to-use configurations:

### GRANITE\_VISION\_OLLAMA

```
```

This configuration targets a local Ollama server running the Granite Vision model. The `scale=1.0` uses original image resolution, and `timeout=120` allows longer processing for complex pages.

**Usage Pattern:**

```
```

**Sources:** [docling/datamodel/vlm\_model\_specs.py171-179](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/vlm_model_specs.py#L171-L179)

---

## API Request Format

### OpenAI Chat Completions Schema

The API client sends requests to the `/v1/chat/completions` endpoint using the OpenAI-compatible schema:

```
```

The image is base64-encoded and included as a data URL. Additional parameters from `ApiVlmOptions.params` are merged into the request body.

### Response Parsing

**Non-Streaming Response:**

```
```

The `api_image_request` function extracts `choices[0].message.content`.

**Streaming Response:**

Server-Sent Events (SSE) format:

```
data: {"choices": [{"delta": {"content": "# "}}]}

data: {"choices": [{"delta": {"content": "Document"}}]}

data: [DONE]
```

The `api_image_request_streaming` function accumulates chunks until a stopper triggers or the stream completes.

**Sources:** [docling/models/api\_vlm\_model.py76-97](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L76-L97)

---

## Error Handling and Timeout

### Request-Level Timeouts

Each API request respects the `timeout` parameter:

```
```

If the server doesn't respond within `timeout` seconds, the request raises a timeout exception, which is caught by the pipeline's error handling.

### Backend Validation

Before making API requests, the model validates the page backend:

```
```

Invalid pages (e.g., corrupted PDFs) are returned unchanged, preventing unnecessary API calls.

### Remote Services Flag

The `enable_remote_services` flag provides a safety gate:

```
```

This prevents accidental API calls in environments where external connections are forbidden or should be audited.

**Sources:** [docling/models/api\_vlm\_model.py28-49](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L28-L49)

---

## Comparison with Inline VLM Models

| Aspect                | API-Based Models                        | Inline Models                                                            |
| --------------------- | --------------------------------------- | ------------------------------------------------------------------------ |
| **Execution**         | Remote HTTP API                         | Local model loading (Transformers/MLX/vLLM)                              |
| **Configuration**     | `ApiVlmOptions`                         | `InlineVlmOptions`                                                       |
| **Model Class**       | `ApiVlmModel`                           | `HuggingFaceTransformersVlmModel`, `HuggingFaceMlxModel`, `VllmVlmModel` |
| **Dependencies**      | HTTP client only                        | `transformers`, `torch`, `mlx`, `vllm`                                   |
| **Concurrency**       | `ThreadPoolExecutor` (I/O bound)        | Model batching (compute bound)                                           |
| **Device**            | N/A (server-side)                       | CPU/CUDA/MPS                                                             |
| **Artifacts**         | None (server manages)                   | Downloaded to `artifacts_path`                                           |
| **Stopping Criteria** | `GenerationStopper` (streaming only)    | `StoppingCriteria` + `GenerationStopper`                                 |
| **Use Case**          | Distributed inference, limited hardware | Local control, offline operation                                         |

**Sources:** [docling/models/api\_vlm\_model.py19-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L19-L101) [docling/models/vlm\_models\_inline/hf\_transformers\_model.py36-376](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/hf_transformers_model.py#L36-L376)

---

## Example: Custom Stopping Criteria

### Implementing a GenerationStopper

```
```

### Configuration with Stopper

```
```

When configured, the streaming API path is automatically selected, and generation terminates as soon as `</doctag>` appears in the output, saving tokens and reducing latency.

**Sources:** [docling/models/api\_vlm\_model.py63-74](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L63-L74) [docling/datamodel/pipeline\_options\_vlm\_model.py110-112](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options_vlm_model.py#L110-L112)

---

## Performance Considerations

### Concurrency Tuning

The `concurrency` parameter controls parallel requests:

- **Low concurrency (1-2):** Sequential processing, minimal server load
- **Medium concurrency (4-8):** Balanced throughput for typical documents
- **High concurrency (16+):** Maximum speed for large batches, requires server capacity

Optimal settings depend on:

1. Server capacity (GPU count, batch size)
2. Network latency and bandwidth
3. Document complexity (larger images = longer inference)

### Timeout Configuration

Appropriate timeout values vary by model and document type:

- **Simple text extraction:** 30-60 seconds
- **Complex documents (tables, figures):** 120-300 seconds
- **Large images (high resolution):** 300+ seconds

Insufficient timeouts cause false failures; excessive timeouts delay error detection.

**Sources:** [docling/models/api\_vlm\_model.py36-101](https://github.com/docling-project/docling/blob/f7244a43/docling/models/api_vlm_model.py#L36-L101)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [API-Based VLM Models](#api-based-vlm-models.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Architecture](#system-architecture.md)
- [Configuration: ApiVlmOptions](#configuration-apivlmoptions.md)
- [Request Flow Sequence](#request-flow-sequence.md)
- [ApiVlmModel Implementation](#apivlmmodel-implementation.md)
- [Class Structure](#class-structure.md)
- [Request Execution Pattern](#request-execution-pattern.md)
- [Streaming and Early Abort](#streaming-and-early-abort.md)
- [Streaming Request Flow](#streaming-request-flow.md)
- [GenerationStopper Interface](#generationstopper-interface.md)
- [Pipeline Integration](#pipeline-integration.md)
- [VlmPipeline Instantiation](#vlmpipeline-instantiation.md)
- [Page Processing](#page-processing.md)
- [Predefined API Configurations](#predefined-api-configurations.md)
- [GRANITE\_VISION\_OLLAMA](#granite_vision_ollama.md)
- [API Request Format](#api-request-format.md)
- [OpenAI Chat Completions Schema](#openai-chat-completions-schema.md)
- [Response Parsing](#response-parsing.md)
- [Error Handling and Timeout](#error-handling-and-timeout.md)
- [Request-Level Timeouts](#request-level-timeouts.md)
- [Backend Validation](#backend-validation.md)
- [Remote Services Flag](#remote-services-flag.md)
- [Comparison with Inline VLM Models](#comparison-with-inline-vlm-models.md)
- [Example: Custom Stopping Criteria](#example-custom-stopping-criteria.md)
- [Implementing a GenerationStopper](#implementing-a-generationstopper.md)
- [Configuration with Stopper](#configuration-with-stopper.md)
- [Performance Considerations](#performance-considerations.md)
- [Concurrency Tuning](#concurrency-tuning.md)
- [Timeout Configuration](#timeout-configuration.md)
