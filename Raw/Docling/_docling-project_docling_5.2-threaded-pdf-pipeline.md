Threaded PDF Pipeline | docling-project/docling | DeepWiki

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

# Threaded PDF Pipeline

Relevant source files

- [docling/datamodel/extraction.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/extraction.py)
- [docling/document\_extractor.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_extractor.py)
- [docling/models/base\_ocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/base_ocr_model.py)
- [docling/models/code\_formula\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/code_formula_model.py)
- [docling/models/document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/document_picture_classifier.py)
- [docling/models/easyocr\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/easyocr_model.py)
- [docling/models/layout\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/layout_model.py)
- [docling/models/page\_assemble\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_assemble_model.py)
- [docling/models/page\_preprocessing\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/page_preprocessing_model.py)
- [docling/models/table\_structure\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/table_structure_model.py)
- [docling/models/vlm\_models\_inline/nuextract\_transformers\_model.py](https://github.com/docling-project/docling/blob/f7244a43/docling/models/vlm_models_inline/nuextract_transformers_model.py)
- [docling/pipeline/asr\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/asr_pipeline.py)
- [docling/pipeline/base\_extraction\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_extraction_pipeline.py)
- [docling/pipeline/base\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py)
- [docling/pipeline/extraction\_vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/extraction_vlm_pipeline.py)
- [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py)
- [docling/pipeline/standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py)
- [docling/pipeline/threaded\_standard\_pdf\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py)
- [docling/pipeline/vlm\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/vlm_pipeline.py)
- [tests/test\_document\_picture\_classifier.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_document_picture_classifier.py)
- [tests/test\_options.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py)

## Purpose and Scope

The **Threaded PDF Pipeline** is a high-performance, multi-threaded implementation of PDF document processing that parallelizes work across multiple pipeline stages. It processes pages through five sequential stages (preprocessing, OCR, layout analysis, table structure detection, and assembly) using bounded queues and dedicated worker threads for each stage, enabling concurrent processing of multiple pages at different stages simultaneously.

This pipeline extends the standard sequential PDF processing flow with thread-based parallelism while maintaining strict isolation between concurrent document conversions. For the sequential single-threaded version, see [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md). For VLM-based PDF processing, see [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md).

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py1-16](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L1-L16)

## Architecture Overview

The `ThreadedStandardPdfPipeline` class extends `ConvertPipeline` and implements a stage-based architecture where each stage runs in its own worker thread. Pages flow through the pipeline wrapped in `ThreadedItem` envelopes, traveling through `ThreadedQueue` instances that provide backpressure and flow control.

```
```

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296-310](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L310) [docling/pipeline/base\_pipeline.py135-163](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L135-L163)

## Core Components

### ThreadedQueue

The `ThreadedQueue` class implements a bounded queue with explicit close semantics. It provides blocking `put()` and `get_batch()` operations with timeout support, and propagates closure downstream to enable deterministic shutdown.

| Method                     | Description                 | Blocking Behavior                            |
| -------------------------- | --------------------------- | -------------------------------------------- |
| `put(item, timeout)`       | Enqueue single item         | Blocks until space available or queue closed |
| `get_batch(size, timeout)` | Retrieve up to `size` items | Blocks until ≥1 item or queue closed         |
| `close()`                  | Mark queue as closed        | Wakes all waiting threads                    |
| `closed` (property)        | Check if queue is closed    | Non-blocking                                 |

```
```

**Key implementation details:**

- **Bounded capacity:** Uses `deque` with `_max` size constraint
- **Condition variables:** `_not_full` and `_not_empty` coordinate producer/consumer threads
- **Timeout support:** Both operations accept optional timeout for bounded waiting
- **Close propagation:** Once closed, all operations immediately return/fail

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py96-163](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L96-L163)

### ThreadedPipelineStage

Each `ThreadedPipelineStage` wraps a model (e.g., `LayoutModel`, `TableStructureModel`) and runs it in a dedicated worker thread. The stage pulls batches from its `input_queue`, processes them through the model, and emits results to downstream `output_queue`(s).

**Stage configuration:**

| Parameter        | Purpose                       | Typical Value                                         |
| ---------------- | ----------------------------- | ----------------------------------------------------- |
| `name`           | Stage identifier for logging  | "preprocess", "ocr", "layout", "table", "assemble"    |
| `model`          | The actual processing model   | `LayoutModel`, `TableStructureModel`, etc.            |
| `batch_size`     | Max items to process together | 1 for preprocessing/assembly, configurable for others |
| `batch_timeout`  | Max wait time for batch fill  | `ThreadedPdfPipelineOptions.batch_timeout_seconds`    |
| `queue_max_size` | Bounded queue capacity        | `ThreadedPdfPipelineOptions.queue_max_size`           |

```
```

**Error handling:** If a model raises an exception, the stage marks all items in that run as failed (`is_failed=True`, `error` set) but continues processing other runs.

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py165-280](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L165-L280)

### ThreadedItem Envelope

Pages travel through the pipeline wrapped in `ThreadedItem` dataclasses, which carry metadata for routing and error tracking:

```
```

**Key design decision:** The `run_id` is a monotonic counter (from `itertools.count`) rather than using `id(conv_res)`, preventing clashes after garbage collection in long-running pipelines.

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py59-69](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L59-L69)

### RunContext

Each call to `execute()` creates a fresh `RunContext` containing the complete stage graph, queues, and wiring for that specific document conversion. This ensures **per-run isolation** — concurrent conversions never share mutable state.

```
```

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py282-289](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L282-L289)

## Pipeline Stage Graph

The pipeline instantiates five stages in a linear topology, with each stage's output feeding the next stage's input:

```
```

**Wiring details (from `_create_run_ctx()`):**

1. **Preprocess stage:** `batch_size=1`, runs `PagePreprocessingModel` (image generation, cell extraction)
2. **OCR stage:** `batch_size=ocr_batch_size` (configurable), runs `BaseOcrModel` implementations
3. **Layout stage:** `batch_size=layout_batch_size`, runs `LayoutModel` (Heron)
4. **Table stage:** `batch_size=table_batch_size`, runs `TableStructureModel` (TableFormer)
5. **Assemble stage:** `batch_size=1`, runs `PageAssembleModel` (constructs page elements)

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py379-426](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L379-L426)

## Model Initialization

Models are instantiated **once per pipeline instance** in `_init_models()`, not per document conversion. This amortizes model loading costs across multiple documents:

```
```

**Model sharing:** Worker threads read model parameters but never mutate them, enabling safe concurrent access. The models themselves handle any internal thread-safety (e.g., PyTorch models).

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py311-362](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L311-L362)

## Execution Flow

The `_build_document()` method implements an **interleaved feed-and-drain pattern** to maximize throughput while respecting bounded queue capacity:

```
```

**Key invariants:**

1. **Non-blocking feed:** `put(timeout=0.0)` ensures the main thread doesn't block waiting for space
2. **Short drain timeout:** `get_batch(timeout=0.05)` allows rapid switching between feed and drain
3. **Close propagation:** Closing the first queue triggers cascade through all downstream queues
4. **Failure safety:** If output queue closes early, missing pages are marked as failed

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py429-507](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L429-L507)

## Thread Safety and Isolation

### Per-Run Isolation

Each `execute()` call creates a fresh set of queues and worker threads, ensuring zero shared mutable state between concurrent document conversions:

```
```

**Isolation guarantees:**

- **Separate queues:** Each execution has its own `ThreadedQueue` instances
- **Separate threads:** Worker threads are created and joined per execution
- **Run ID filtering:** Stages ignore items from other runs (defensive check)
- **No shared state:** Only models are shared, accessed read-only

### Deterministic Run IDs

The `run_id` is generated from a monotonic counter (`itertools.count`) initialized at pipeline creation:

```
```

This prevents ID clashes that could occur if using `id(conv_res)` after garbage collection in long-running processes.

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py302](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L302-L302) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py431](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L431-L431)

## Configuration Options

The pipeline is configured via `ThreadedPdfPipelineOptions`, which extends `PdfPipelineOptions` with threading-specific parameters:

```
```

### Key Configuration Parameters

| Parameter               | Description                               | Default | Impact                                          |
| ----------------------- | ----------------------------------------- | ------- | ----------------------------------------------- |
| `ocr_batch_size`        | Max pages processed together in OCR stage | 8       | Higher = better GPU utilization, more memory    |
| `layout_batch_size`     | Max pages for layout model batching       | 8       | Higher = better throughput for layout inference |
| `table_batch_size`      | Max pages for table structure batching    | 4       | Lower = less memory per batch                   |
| `queue_max_size`        | Bounded capacity per queue                | 10      | Higher = more buffering, more memory            |
| `batch_timeout_seconds` | Max wait for batch to fill                | 0.1s    | Lower = faster empty queue detection            |

### Inherited Options

From `PdfPipelineOptions`:

- `do_ocr`, `ocr_options` — OCR configuration (see [OCR Models](docling-project/docling/4.1-ocr-models.md))
- `do_table_structure`, `table_structure_options` — Table detection (see [Layout and Table Structure Models](docling-project/docling/4.2-layout-and-table-structure-models.md))
- `layout_options` — Layout model selection
- `images_scale` — Image resolution scaling
- `generate_page_images`, `generate_picture_images` — Image generation flags
- `do_code_enrichment`, `do_formula_enrichment` — Enrichment flags (see [Enrichment Models](docling-project/docling/4.4-enrichment-models.md))
- `accelerator_options` — Device and threading config

**Sources:** [docling/datamodel/pipeline\_options.py171-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py#L171-L215) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py299-301](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L299-L301)

## Result Integration

After all pages complete processing, `_integrate_results()` merges the successful and failed pages back into `conv_res`:

```
```

**Status determination:**

- `SUCCESS` — All pages processed successfully
- `PARTIAL_SUCCESS` — Some pages failed (0 < success < total)
- `FAILURE` — All pages failed or no pages processed

**Cleanup operations:**

1. Clear image caches if not needed: `p._image_cache = {}`
2. Unload page backends if not needed: `p._backend.unload()`
3. Delete parsed pages if not configured: `del p.parsed_page`

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py509-534](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L509-L534)

## Document Assembly and Enrichment

After `_build_document()` completes, the pipeline invokes inherited methods:

### \_assemble\_document()

Aggregates page-level elements into a document-level structure and applies reading order:

1. Collect all `p.assembled.body`, `p.assembled.headers`, `p.assembled.elements` from pages
2. Create `conv_res.assembled` with aggregated lists
3. Invoke `ReadingOrderModel` to construct hierarchical `DoclingDocument`
4. Generate page/picture/table images if configured
5. Compute document-level confidence scores (mean layout/OCR/table scores)

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py536-628](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L536-L628)

### \_enrich\_document()

Inherited from `ConvertPipeline`, runs enrichment models on assembled document items:

- **CodeFormulaModel** — LaTeX extraction from code/formula images (if enabled)
- **DocumentPictureClassifier** — Figure classification (if enabled)
- **PictureDescriptionModel** — Image captioning (if enabled)

Enrichment operates on `conv_res.document` after assembly is complete, iterating over document items in batches.

**Sources:** [docling/pipeline/base\_pipeline.py93-115](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/base_pipeline.py#L93-L115) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py339-362](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L339-L362)

## Performance Characteristics

### Advantages Over Sequential Pipeline

1. **Parallelism:** Multiple pages can be at different stages simultaneously
2. **GPU utilization:** Batching in layout/table stages maximizes GPU efficiency
3. **Pipeline balancing:** Slow stages don't block fast stages (up to queue capacity)
4. **Minimal overhead:** Bounded queues prevent unbounded memory growth

### Throughput Analysis

For a document with `N` pages and 5 stages:

- **Sequential pipeline:** Processes `N` pages serially through all stages
- **Threaded pipeline:** Can process up to `min(N, queue_capacity * num_stages)` pages concurrently

**Example:** With `queue_max_size=10` and 5 stages, up to 50 pages can be "in flight" simultaneously across the pipeline.

### Memory Footprint

Memory usage scales with:

1. **Queue capacity:** `queue_max_size * num_stages * size_per_page`
2. **Batch sizes:** Larger batches require more GPU memory
3. **Image caching:** `images_scale` parameter affects per-page image size

**Trade-off:** Higher `queue_max_size` improves throughput but increases memory consumption.

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py96-163](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L96-L163) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py379-426](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L379-L426)

## Usage Example

```
```

**Note:** The threaded pipeline is **not** the default; you must explicitly specify `pipeline_cls=ThreadedStandardPdfPipeline` in the format options.

**Sources:** [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296-298](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L298) [tests/test\_options.py25-41](https://github.com/docling-project/docling/blob/f7244a43/tests/test_options.py#L25-L41)

## Comparison with Standard Pipeline

| Aspect                | StandardPdfPipeline         | ThreadedStandardPdfPipeline       |
| --------------------- | --------------------------- | --------------------------------- |
| **Execution model**   | Sequential (page-by-page)   | Concurrent (stage-parallel)       |
| **Thread usage**      | Single-threaded             | 5 worker threads per execution    |
| **Batching strategy** | Per-stage generator chains  | Bounded queues with timeouts      |
| **Isolation**         | Implicit (single execution) | Explicit (per-run queues/threads) |
| **Memory profile**    | Lower (one page at a time)  | Higher (multiple pages in-flight) |
| **Throughput**        | Lower (no parallelism)      | Higher (stage pipelining)         |
| **Complexity**        | Simpler (linear flow)       | More complex (threading, queues)  |
| **Default choice**    | Yes (for most PDFs)         | No (opt-in for performance)       |

**When to use threaded pipeline:**

- Large documents (100+ pages) where throughput matters
- GPU-accelerated environments where batching is beneficial
- Production deployments with sufficient memory headroom

**When to use standard pipeline:**

- Small documents (<20 pages)
- Memory-constrained environments
- Simpler debugging/profiling requirements
- Default use cases

**Sources:** [docling/pipeline/standard\_pdf\_pipeline.py34-243](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/standard_pdf_pipeline.py#L34-L243) [docling/pipeline/threaded\_standard\_pdf\_pipeline.py296-648](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/threaded_standard_pdf_pipeline.py#L296-L648)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Threaded PDF Pipeline](#threaded-pdf-pipeline.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Components](#core-components.md)
- [ThreadedQueue](#threadedqueue.md)
- [ThreadedPipelineStage](#threadedpipelinestage.md)
- [ThreadedItem Envelope](#threadeditem-envelope.md)
- [RunContext](#runcontext.md)
- [Pipeline Stage Graph](#pipeline-stage-graph.md)
- [Model Initialization](#model-initialization.md)
- [Execution Flow](#execution-flow.md)
- [Thread Safety and Isolation](#thread-safety-and-isolation.md)
- [Per-Run Isolation](#per-run-isolation.md)
- [Deterministic Run IDs](#deterministic-run-ids.md)
- [Configuration Options](#configuration-options.md)
- [Key Configuration Parameters](#key-configuration-parameters.md)
- [Inherited Options](#inherited-options.md)
- [Result Integration](#result-integration.md)
- [Document Assembly and Enrichment](#document-assembly-and-enrichment.md)
- [\_assemble\_document()](#_assemble_document.md)
- [\_enrich\_document()](#_enrich_document.md)
- [Performance Characteristics](#performance-characteristics.md)
- [Advantages Over Sequential Pipeline](#advantages-over-sequential-pipeline.md)
- [Throughput Analysis](#throughput-analysis.md)
- [Memory Footprint](#memory-footprint.md)
- [Usage Example](#usage-example.md)
- [Comparison with Standard Pipeline](#comparison-with-standard-pipeline.md)
