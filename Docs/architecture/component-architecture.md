# Component Architecture

### New Components

#### `CrossEncoderBatchExecutor`
- **Responsibility:** Manage CrossEncoder batching under GPU leasing, including dynamic batch sizing, telemetry capture, and fallback on OOM/timeouts.
- **Integration:** Instantiated by `BatchRunner` post dense/sparse fusion; delegates to existing `RerankPipeline` but wraps with leasing and telemetry logic.
- **Interfaces:**
  - Consumes candidate list + query text.
  - Produces reranked candidate list + `CrossEncoderRerankRun` payload.

#### `SparseVectorGenerator`
- **Responsibility:** Execute live sparse inference using loaded SPLADE-style models, handling CPU/GPU routing and fallback to metadata.
- **Integration:** Invoked by `BatchRunner` before export; interacts with `SparseInferenceRun` to persist results.
- **Interfaces:**
  - Input: chunk texts/metadata.
  - Output: sparse vectors stored in `embedder.sparse_vectors` and export artifacts.

### Updated Components

- **`UltimateKaggleEmbedderV4`:**
  - Loads CrossEncoder and sparse models through `ModelManager` when configs enabled.
  - Tracks model dtypes/device placement for audit; records rerank/sparse run references for export.
- **`BatchRunner`:**
  - Adds sparse inference stage (CPU-first, GPU optional) before export.
  - Adds rerank stage after dense/sparse fusion using `CrossEncoderBatchExecutor`.
  - Captures telemetry spans per stage with GPU peak metrics.
- **`ModelManager`:**
  - Ensures CrossEncoder and sparse models share HF cache directory.
  - Stages models to CPU by default; hydrates to GPU via leasing when needed.
- **`ExportRuntime`:**
  - Writes optional `rerank_run`/`sparse_run` sections into JSON manifests.
  - Emits rerank scores alongside dense/sparse similarities in JSONL.
- **`embed_collections_v6.py`:**
  - Adds CLI flags (`--enable-rerank`, `--enable-sparse`, `--sparse-models`).
  - Displays per-stage latency, batch sizes, GPU peak usage, and rerank coverage in logs.

### Component Interaction Diagram

```mermaid
graph TD
    A[CLI Entry
    embed_collections_v6.py] --> B[UltimateKaggleEmbedderV4]
    B --> C[ModelManager
    (load dense, sparse, rerank)]
    B --> D[BatchRunner]
    D --> D1[Dense Ensemble Pass]
    D --> D2[SparseVectorGenerator]
    D --> D3[Result Fusion]
    D --> D4[CrossEncoderBatchExecutor]
    D --> E[ExportRuntime]
    D2 -->|vectors| E
    D4 -->|scores + telemetry| E
    E --> F[Artifacts
    (JSONL, manifest, metrics)]
    D --> G[Telemetry / OpenTelemetry spans]
```
