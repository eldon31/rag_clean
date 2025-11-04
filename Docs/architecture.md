# RAG_CLEAN Brownfield Enhancement Architecture

## Introduction

This document outlines the architectural approach for enhancing `RAG_CLEAN` with a fully staffed CrossEncoder reranking stage inside the modular Ultimate Embedder. The goal is to merge dense embeddings, learned sparse vectors, and CrossEncoder reranking into a coordinated pipeline that respects the 12 GB-per-GPU ceiling while preserving the mature export and telemetry surfaces already in place.

**Relationship to existing architecture:** This plan extends the exclusive-ensemble embedder (GPU leasing, telemetry-backed batch runner, sparse helper scaffolding) by activating the dormant rerank and live sparse execution paths. Whenever new orchestration collides with the current flow, this document explains how to reconcile conflicts so consistency and backward compatibility are maintained.

## Existing Project Analysis

### Current Project State

- **Primary Purpose:** Universal file-to-knowledge converter that chunks heterogeneous documents and builds vector plus knowledge-graph search surfaces for downstream RAG workloads.
- **Current Tech Stack:** Python 3.11, FastAPI service, Docling extraction, Sentence Transformers ensemble (Jina/BGE/Qwen), PyTorch for GPU orchestration, Pydantic v2 data models, Qdrant/FAISS exporters, Kaggle dual-T4 deployment scripts.
- **Architecture Style:** Modular pipelines orchestrated through the Ultimate Embedder facade: adaptive batching, GPU leasing, telemetry hooks, and export runtime producing JSONL + FAISS bundles.
- **Deployment Method:** Split deployment—embedding generation on Kaggle T4×2 notebooks exporting artifacts to local vector stores; local tooling managed via Poetry/Docker (per `project.md`).

### Available Documentation

- `openspec/project.md` – end-to-end charter, constraints, environment details.
- `openspec/changes/refactor-ultimate-embedder-ensemble/task-24-feature-request.md` – CrossEncoder rerank story requirements.
- `openspec/changes/refactor-ultimate-embedder-ensemble/sparse-helpers-keep-list.md` – sparse helper API contracts to retain.
- `processor/ultimate_embedder/*.py` – authoritative source for embedder orchestration (core, batch_runner, model_manager, gpu_lease, telemetry, rerank_pipeline, sparse_pipeline).
- `scripts/embed_collections_v6.py` – CLI entry currently wiring exclusive ensemble mode.

### Identified Constraints

- Kaggle exclusive ensemble flow must respect a hard **12 GB VRAM cap per GPU**; GPU leasing, hydration, and adaptive batching need to enforce that cap explicitly.
- CrossEncoder `RerankPipeline` is scaffolded but not wired; full activation (model lifecycle, CLI entry, telemetry, export) is mandatory per Task 2.4.
- Sparse helper components listed in `sparse-helpers-keep-list.md` must stay intact and be integrated so live sparse inference replaces metadata-only fallbacks without regressions.
- CLI/runtime exports and telemetry currently assume rerank/sparse are optional; upgrades must add new signals without breaking existing consumers.

## Enhancement Scope and Integration Strategy

### Enhancement Overview

**Enhancement Type:** CrossEncoder Rerank and Sparse Inference Integration

**Scope:** Activate the full CrossEncoder reranking pipeline and convert sparse vector generation from metadata echoing to live inference, ensuring GPU leasing, telemetry, CLI workflow, and export schemas treat dense, sparse, and rerank stages as first-class citizens.

**Integration Impact:** High – touches model loading, batch runner sequencing, GPU leasing lifecycle, export runtime, telemetry schema, CLI interface, and optional service entry points.

### Integration Approach

- **Code Integration Strategy:**
  - Extend `UltimateKaggleEmbedderV4`/`ModelManager` to hydrate CrossEncoder and sparse models via existing registries, staging to CPU by default.
  - Enhance `BatchRunner` to schedule rerank passes (post dense/sparse fusion) and live sparse inference, reusing GPU leasing helpers to stay under 12 GB.
  - Wire `RerankPipeline` into CLI (`embed_collections_v6.py`) and any service adapters so rerank execution is driven by `RerankingConfig` toggles.
- **Database Integration:**
  - Continue exporting artifacts as JSON/JSONL bundles; append optional rerank/sparse sections without altering persistent tables.
- **API Integration:**
  - Expose rerank/sparse toggles in CLI now; later surface via FastAPI endpoints with Pydantic request/response models.
- **UI Integration:**
  - Update CLI/log output to report rerank model, batch size, latency, GPU peak usage, and sparse model activation. Telemetry dashboards consume new signals; no separate GUI changes required.

### Compatibility Requirements

- **Existing API Compatibility:** Rerank and sparse stages run by default, with opt-out switches preserving dense-only parity when explicitly requested.
- **Database Schema Compatibility:** Export schema remains additive—legacy parsers bypass unknown keys.
- **UI/UX Consistency:** CLI progress and summaries follow current exclusive-mode style, appending rerank/sparse metrics without reordering existing lines.
- **Performance Impact:** Respect 12 GB ceiling by dynamically sizing rerank batches, limiting candidate counts under latency pressure, and keeping sparse inference CPU-first with GPU-cached hot shards only.

## Tech Stack

### Existing Technology Stack

| --- | --- | --- | --- | --- |
| Core Runtime | Python | 3.11 | Maintain | Runtime for embedder, CLI, telemetry integrations. |
| Web/API | FastAPI | Pinned in project | Maintain | Future API exposure of rerank/sparse toggles; no immediate change. |
| Embedding Ensemble | Sentence Transformers | 3.x | Extend | Continue dense models; add CrossEncoder + sparse encoders via same cache dirs. |
| GPU Framework | PyTorch | 2.x | Extend | Enforce leasing + adaptive batching within 12 GB cap across dense, sparse, rerank stages. |
| CLI Orchestration | `embed_collections_v6.py` | V6 | Extend | Add flags for rerank/sparse, enhanced progress telemetry. |
| Export Runtime | Qdrant/FAISS JSONL writers | V4 schema | Extend | Append optional rerank/sparse blocks while keeping legacy keys intact. |
| Sparse Helpers | Custom SPLADE-style pipeline | V5 | Extend | Transition from metadata-only to live sparse inference, honoring keep-list. |

### New Technology Additions

None—enhancements reuse existing dependencies while activating previously scaffolded modules (CrossEncoder reranker, sparse encoders, telemetry hooks).

## Data Models and Schema Changes

### New Data Models

#### `CrossEncoderRerankRun`

- **Purpose:** Capture telemetry/export payload for a CrossEncoder batch rerank pass.
- **Integration:** Stored alongside dense export manifests (JSON). Enables CLI summaries, QA audits, telemetry dashboards.

| Field           | Type        | Description                                         |
| --------------- | ----------- | --------------------------------------------------- |
| `run_id`        | UUID        | Correlates with embedding/export batch.             |
| `query`         | string      | User query (truncated/anonymized per policy).       |
| `candidate_ids` | list[str]   | Document IDs scored in this rerank pass.            |
| `batch_size`    | int         | Dynamic batch size selected under 12 GB constraint. |
| `scores`        | list[float] | CrossEncoder similarity scores per candidate.       |
| `latency_ms`    | float       | End-to-end rerank latency.                          |
| `gpu_peak_gb`   | float       | Peak GPU memory recorded for audit/alerts.          |

_Relations_: linked to existing embedding run metadata; future child records (e.g., per-candidate diagnostics) can reference `run_id` if needed.

#### `SparseInferenceRun`

- **Purpose:** Document live sparse vector generation replacing metadata echo path.
- **Integration:** Complements existing sparse JSONL exports; indicates whether live inference or fallback was used.

| Field                     | Type       | Description                                                                 |
| ------------------------- | ---------- | --------------------------------------------------------------------------- |
| `run_id`                  | UUID       | Shares ID with parent embedding batch.                                      |
| `sparse_model`            | string     | Identifier from `SPARSE_MODELS` registry (e.g., `qdrant-bm25`).             |
| `query_sparse_vector`     | dict       | Non-zero indices/values representing query sparse vector.                   |
| `document_sparse_vectors` | list[dict] | Sparse vectors per processed chunk (indices/values).                        |
| `latency_ms`              | float      | Processing time for sparse inference stage.                                 |
| `fallback_used`           | bool       | Indicates metadata-derived sparse vectors (true) vs live inference (false). |

_Relations_: ties into export runtime merging sparse vectors with chunk metadata; telemetry uses `run_id` for correlations.

### Schema Integration Strategy

- **New Tables:** None—continue storing run metadata as JSON/JSONL artifacts; avoid relational migrations.
- **Modified Artifacts:**
  - Export manifest (`processing_summary.json`) versioned to `v4.1`, adding optional `rerank_run` and `sparse_run` sections.
  - CLI summary picks up new sections when present; older runs remain valid.
- **Indexes:** Not required; correlations handled through existing filename conventions and UUIDs.
- **Migration Strategy:**
  - Introduce schema version check in CLI/export runtime.
  - When enhancements disabled, new sections omitted to maintain backward compatibility.
  - Tests verify both legacy (`v4.0`) and enhanced (`v4.1`) manifests parse cleanly.

### Backward Compatibility

- All new fields are additive/optional; legacy tooling ignoring unknown keys continues to function.
- CLI emits soft warnings if rerank/sparse toggles enabled but corresponding sections missing, guiding operators without breaking flows.
- Export runtime retains metadata-derived sparse vectors as fallback until live inference confirmed stable.

## Component Architecture

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

## Source Tree

### Existing Project Structure (Relevant Extract)

```text
processor/
  ultimate_embedder/
    batch_runner.py
    core.py
    gpu_lease.py
    model_manager.py
    rerank_pipeline.py
    sparse_pipeline.py
    telemetry.py
scripts/
  embed_collections_v6.py
docs/
  architecture.md
  ...
```

### New File Organization (Additions Only)

```text
processor/
  ultimate_embedder/
    cross_encoder_executor.py      # New module wrapping rerank batching
    sparse_generator.py            # New module for live sparse inference
docs/
  telemetry/
    rerank_sparse_signals.md       # Optional runbook documenting new metrics
```

> Note: Module naming subject to implementation preference; can alternatively live inside existing files if scope small. Primary requirement is keeping responsibilities isolated and testable.

## Operational Safeguards

### Brownfield Rollback and Contingency Plan

1. **Toggle-first rollback:** Disable the new stages without redeploying by setting `EMBEDDER_ENABLE_RERANK=false` and/or `EMBEDDER_ENABLE_SPARSE=false` (CLI equivalents: `--disable-rerank`, `--disable-sparse`). Confirm the override in the `embed_collections_v6.py` run header.
2. **Dense-only smoke test:** Re-run the latest corpus with toggles off and validate `processing_summary.json` shows `rerank_run=null` and `sparse_run=null` while dense exports hash-match the previous baseline.
3. **Repository rollback:** If toggles fail to stabilize the run, revert the orchestration package to the last known-good tag (e.g. `git checkout tags/embedder-v4.0 && poetry install`) and redeploy. Preserve failed artifacts for diffing before the next attempt.
4. **Telemetry cleanup:** Purge rerank/sparse dashboards, alerts, or temporary log streams created during the failed deployment so legacy monitoring stays noise-free.
5. **Re-enable criteria:** Only re-enable rerank/sparse once dense parity tests pass, GPU leasing logs are clean, and downstream consumers ingest the legacy schema without errors.

### Local Development Environment Setup

- **Prerequisites:** Python 3.11, Node.js ≥18, Poetry 1.7+, Git, and CUDA 12.1 drivers when exercising GPU flows locally.
- **Bootstrap:**
  1. `git clone https://github.com/eldon31/rag_clean.git && cd rag_clean`
  2. `poetry env use 3.11` (or `py -3.11 -m venv .venv && .\.venv\Scripts\Activate.ps1`)
  3. `poetry install` (installs PyTorch, Sentence Transformers, Docling, FastAPI, Qdrant client, FAISS CPU, OpenTelemetry SDK)
  4. `npm install` (pulls the tree-sitter grammars defined in `package.json`)
  5. Copy `.env.example` to `.env`, then supply Kaggle/OpenAI/Anthropic credentials plus default values for `EMBEDDER_ENABLE_RERANK`/`EMBEDDER_ENABLE_SPARSE`.
  6. `poetry run python scripts/embed_collections_v6.py --help` to confirm CLI wiring.
- **Developer services:** `poetry run pytest`, `poetry run ruff check .`, and `poetry run uvicorn openspec.api:app --reload` once FastAPI surfaces are in play.

### Core Dependency Matrix

| Layer               | Package                                 | Version/PIN                     | Status  | Notes                                          |
| ------------------- | --------------------------------------- | ------------------------------- | ------- | ---------------------------------------------- |
| GPU orchestration   | torch, accelerate                       | 2.3.x / 0.30.x                  | present | Align with Kaggle CUDA 12.1 runtime.           |
| Dense embeddings    | sentence-transformers                   | 2.7.x                           | present | Powers the existing dense ensemble.            |
| Sparse inference    | splade, pyserini (or chosen stack)      | latest compatible               | pending | Required for Story 2.1; document cache path.   |
| Rerank              | transformers, cross-encoder weights     | 4.41.x                          | present | Ensure adaptive batching keeps usage <12 GB.   |
| Export & storage    | qdrant-client, faiss-cpu, numpy, pandas | 1.8.x / 1.7.x / 1.26.x / 2.2.x  | present | Produces manifests and JSONL artifacts.        |
| API / orchestration | fastapi, pydantic, typer, rich          | 0.111.x / 2.7.x / 0.12.x / 13.x | present | CLI, validation, and operator ergonomics.      |
| Telemetry           | opentelemetry-sdk, prometheus-client    | 1.25.x / 0.20.x                 | pending | Captures rerank/sparse spans and metrics.      |
| Tooling             | ruff, pytest, pytest-asyncio, mypy      | pinned in pyproject             | present | Supports regression harness and quality gates. |

## Infrastructure and Deployment

### Runtime Outputs and Storage Order

- Embedding runs must finish by persisting artifacts in this sequence: (1) dense embeddings and metadata bundles, (2) sparse vectors merged into JSONL/FAISS outputs, and (3) rerank manifests that log candidate ordering, latency, and GPU usage. The export runtime writes `processing_summary.json` (v4.1) and per-collection JSONL/FAISS files once all stages complete so downstream tools always see dense, sparse, and rerank payloads together.
- Hash comparisons against the previous dense-only baseline should continue to run after each job to confirm additive compatibility.

### Execution Environment

- No external API surface is required; all orchestration executes inside a Kaggle notebook session.
- Standard run flow: open a fresh Kaggle notebook with T4 GPU, `git clone https://github.com/eldon31/rag_clean.git`, run `poetry install`, and download Hugging Face model weights into `/kaggle/working/hf_cache` (or set `HF_HOME`).
- Cached models include dense ensemble members, the selected sparse encoders, and the CrossEncoder reranker; the notebook primes them before the embedder run to avoid mid-execution downloads.

### Kaggle Notebook Workflow

- Prerequisite: launch a Kaggle Notebook with GPU (T4) and internet access enabled.
- Setup commands to run at the top of the notebook:
  - `!git clone https://github.com/eldon31/rag_clean.git && cd rag_clean`
  - `!pip install poetry`
  - `!poetry env use 3.11`
  - `!poetry install`
  - `!poetry run pip install -r scripts/requirements_kaggle.txt` _(optional helper if you maintain a Kaggle-specific dependency list)_
  - `!pip install --upgrade pip setuptools wheel --no-cache-dir`
  - `!pip install numpy --no-cache-dir`
  - `!pip install scipy --no-cache-dir`
  - `!pip install scikit-learn --no-cache-dir`
  - `!pip install pandas --no-cache-dir`
  - `!pip install tqdm --no-cache-dir`
  - `!pip install tiktoken --no-cache-dir`
  - `!pip install rich --no-cache-dir`
  - `!pip install pydantic --no-cache-dir`
  - `!pip install fastapi --no-cache-dir`
  - `!pip install "uvicorn[standard]" --no-cache-dir`
  - `!pip install torch --no-cache-dir`
  - `!pip install torchvision --no-cache-dir`
  - `!pip install torchaudio --no-cache-dir`
  - `!pip install accelerate --no-cache-dir`
  - `!pip install transformers --no-cache-dir`
  - `!pip install sentence-transformers --no-cache-dir`
  - `!pip install huggingface-hub --no-cache-dir`
  - `!pip install qdrant-client --no-cache-dir`
  - `!pip install docling --no-cache-dir`
  - `!pip install optimum --no-cache-dir`
  - `!pip install onnxruntime --no-cache-dir`
  - `!pip install onnxruntime-tools --no-cache-dir`
  - `!pip install "faiss-gpu-cu12[fix-cuda]" --no-cache-dir`
  - `!pip install "faiss-gpu-cu11[fix-cuda]" --no-cache-dir`
  - `!pip install faiss-cpu --no-cache-dir`
  - `!pip install splade-cpu --no-cache-dir`
  - `!poetry run python scripts/embed_collections_v6.py --help`
- Model weights are pulled on-demand via Hugging Face within the Kaggle runtime; if you want to reuse downloads across sessions, persist `/kaggle/working/hf_cache` as a Kaggle Dataset and attach it to new notebooks.
- Primary scripts:

  - `poetry run python scripts/chunk_docs_v5.py` for CPU-based chunking/preprocessing.
  - `poetry run python scripts/embed_collections_v6.py --collections <name>` to execute dense+sparse+rerank pipelines on GPU.
  - Use `--disable-rerank`/`--disable-sparse` flags for rollback verification.
  - This workflow assumes Kaggle credentials and Hugging Face access are already provisioned; model downloads occur on demand in-session, and no alternative mirrors or secret-management steps are maintained by design.

  ## Delivery Dependencies

  ### Functional Dependency Roadmap

  1. **Epic 1 – Default-On Controls:** Configure CLI flags, env vars, and telemetry defaults so rerank/sparse can be toggled and observed. Dense-only parity tests run after each story to confirm legacy behaviour remains intact.
  2. **Epic 2 – Sparse Integration:** Requires Epic 1’s toggles to expose enable/disable controls and telemetry slots. Sparse vectors must populate exports before any rerank work proceeds.
  3. **Epic 3 – CrossEncoder Rerank:** Depends on Epics 1 and 2 for fused candidate sets, telemetry plumbing, and opt-out handling. Rerank executor is blocked until sparse vectors attach to each chunk.
  4. **Epic 4 – Exports, Regression, Documentation:** Consumes telemetry, exports, and toggles established in Epics 1–3. Documentation updates and schema versioning occur only after live sparse/rerank data exists.

  Dense-only validation runs between each epic to ensure existing functionality remains stable throughout the rollout.

  ### Technical Dependency Notes

  - Model registries, configs, and HF cache paths are initialized during `UltimateKaggleEmbedderV4` setup before `BatchRunner` stages execute. Data models (`CrossEncoderRerankRun`, `SparseInferenceRun`) and manifest v4.1 schema updates are defined prior to any write operations so downstream consumers never see partial structures.
  - Libraries such as PyTorch, Sentence Transformers, SPLADE/pyserini, and Transformers are imported and version-checked at CLI boot. Telemetry export schemas register before spans emit, guaranteeing instrumentation is ready when stages run.

  ### Cross-Epic Dependency Matrix

  | Sequence | Dependent Epic                              | Prerequisites | Rationale                                                          |
  | -------- | ------------------------------------------- | ------------- | ------------------------------------------------------------------ |
  | 1        | Epic 1 – Default Rerank & Sparse Activation | None          | Establish toggles, configs, telemetry slots.                       |
  | 2        | Epic 2 – Sparse Generator & Fusion          | Epic 1        | Needs enable/disable controls and baseline telemetry.              |
  | 3        | Epic 3 – CrossEncoder Rerank                | Epics 1 & 2   | Requires fused dense+sparse outputs and telemetry streams.         |
  | 4        | Epic 4 – Export Schema & Regression         | Epics 1–3     | Depends on actual sparse/rerank data to version exports and tests. |

  Incremental value is delivered at each step: Epic 1 unlocks observability, Epic 2 adds live sparse retrieval, Epic 3 improves ranking quality, and Epic 4 hardens exports/tests. Dense-only regression checks run after every epic to preserve system integrity.

  ## MVP Scope Alignment

  ### Goal Traceability

  | PRD Goal / Requirement                                                     | Architecture Coverage                                                                                                    |
  | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
  | Default-on rerank and sparse without regressing dense path (FR1, FR4, FR8) | Functional dependency roadmap and Operational Safeguards describe toggles, dense-only parity checks, and staged rollout. |
  | Live sparse inference with fallbacks (FR2)                                 | SparseVectorGenerator component, Delivery Dependencies (Epic 2), and manifest v4.1 schema integration.                   |
  | CrossEncoder rerank stage after fusion (FR3)                               | CrossEncoderBatchExecutor design, BatchRunner sequencing, and telemetry instrumentation.                                 |
  | Export/telemetry updates with additive schema (FR5, FR6, NFR1, NFR3)       | Runtime Outputs, Schema Integration Strategy, Observability section.                                                     |
  | 12 GB GPU ceiling with adaptive batching (FR7, NFR2, NFR4)                 | Technical notes on model hydration, adaptive batching, and GPU monitoring in Observability.                              |
  | Telemetry coverage for dense, sparse, rerank stages (FR6)                  | Operational Safeguards, Observability metrics, and Delivery Dependencies (Epic 3).                                       |
  | Documentation/test hardening (Epic 4, NFR5)                                | Delivery Dependencies (Epic 4), Testing and Validation section.                                                          |

  ### Operator Journey Overview

  1. **Pre-run preparation (human):** Launch Kaggle notebook with GPU, pull repo, install deps, configure `.env`, and verify toggles.
  2. **Document ingestion (automation):** `poetry run python scripts/chunk_docs_v5.py` performs CPU-only chunking, logging progress to console.
  3. **Embedding execution (automation):** `poetry run python scripts/embed_collections_v6.py --collections <name>` loads dense, sparse, and rerank models, executes stages in order, and streams status logs plus telemetry metrics.
  4. **Completion review (human):** Operator checks `processing_summary.json`, dense/sparse JSONL/FAISS outputs, and telemetry dashboards. If errors occur, rerun with dense-only toggles and inspect logs.
  5. **Artifact export (human):** Copy outputs from Kaggle workspace to local vector store or downstream pipelines.

  Edge cases include GPU OOM (handled by adaptive batching) and stage failure (operator debugs, optionally re-runs dense-only). Telemetry provides latency and GPU usage signals to guide troubleshooting.

  ### Operator Reference Note

  All operator-facing guidance lives in this architecture document. No separate user manual is maintained; operators should follow the Kaggle workflow and Operational Safeguards sections when running or debugging jobs.

  ### Knowledge Transfer

  - The brownfield context, constraints, and historical decisions remain in `openspec/project.md` and `docs/prd.md`.
  - Rollback procedures, deployment notes, and telemetry guidance live in this architecture document and the optional `docs/telemetry/rerank_sparse_signals.md` runbook.
  - Code reviews, regression findings, and future lessons learned should be appended to `openspec/changes/` entries to keep a chronological trail for future maintainers.

  ## Post-MVP Outlook

  - The MVP focuses on activating default-on dense+sparse+rering execution on Kaggle. Post-MVP enhancements under consideration:
    - Enriching CLI UX (status dashboards, structured logging output).
    - Exposing a FastAPI surface for orchestration once the notebook flow proves stable.
    - Automating Hugging Face cache seeding between sessions (packaged Kaggle dataset or startup script).
  - No ongoing analytics program is planned; manual log/telemetry reviews after each run are sufficient for this personal workflow.

### Deployment and Run Procedure

- This is a personal workflow with no automated CI/CD. Deployment equals preparing a Kaggle session: pull latest `main`, install dependencies, restore cached models, and execute `poetry run python scripts/embed_collections_v6.py` with desired toggles.
- After successful runs, copy the generated artifacts from Kaggle storage to the local vector-store host. If a regression occurs, revert to a previous git tag and rerun within the same session (per rollback plan above).

### GPU and CPU Usage Modes

- Chunkers and document preprocessing run in CPU mode (`poetry run python scripts/chunk_docs_v5.py`) to conserve limited Kaggle GPU hours and simplify text processing reproducibility.
- The Ultimate Embedder stages leverage the provisioned T4 GPU(s). Ensure `CUDA_VISIBLE_DEVICES` reflects available GPUs before invoking `embed_collections_v6.py`; adaptive batch sizing keeps VRAM below 12 GB per device.
- Tests that validate sparse/rerank integration should execute once in CPU fallback mode for parity and once on GPU hardware to confirm leasing telemetry.

- **GPU Environment:** Maintain Kaggle dual-T4 support; enhancements default to single-GPU execution but honor leasing logic for multi-GPU scenarios.
- **Environment Variables:**
  - `EMBEDDER_ENABLE_RERANK` / `EMBEDDER_ENABLE_SPARSE` allow explicit disablement when the default-on behavior must be overridden.
  - `EMBEDDER_RERANK_BATCH_CAP` to override auto batch sizing when needed.
- **Monitoring:**
  - Extend existing telemetry exporter (OpenTelemetry or custom) with rerank/sparse spans and metrics.
  - Alert when rerank latency exceeds thresholds or GPU peak approaches 12 GB cap consistently.

## Coding Standards

- Follow existing 88-character line limit, Ruff linting, and type hints (Pydantic models typed explicitly).
- Document new modules with high-level docstrings summarizing orchestration responsibilities.
- Add succinct inline comments only where orchestration or leasing logic would otherwise be opaque (per repo coding standards).

## Security Considerations

- Ensure queries logged in telemetry are truncated/anonymized per existing privacy rules.
- When writing rerank/sparse artifacts, avoid storing full query text if privacy compliance requires redaction.
- Validate CLI inputs (Pydantic or argparse) to prevent invalid model selections causing unsafe downloads.

## Observability

- Instrument dense, sparse, fusion, rerank, and export stages with OpenTelemetry spans (`rag.dense`, `rag.sparse`, `rag.rerank`, `rag.export`).
- Record per-stage latency, batch size, candidate counts, GPU peak usage, and fallback flags.
- Export Prometheus metrics:
  - `rag_rerank_latency_seconds` (histogram)
  - `rag_sparse_latency_seconds`
  - `rag_gpu_peak_bytes{stage="rerank"}`
  - `rag_candidate_count{stage="fusion"}`
- CLI summarizes metrics post-run; optional runbook (`docs/telemetry/rerank_sparse_signals.md`) details interpretation.

## Risks and Mitigations

| Risk                               | Impact                            | Mitigation                                                                                      |
| ---------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------- |
| GPU OOM during rerank batches      | Pipeline aborts mid-run           | Dynamic batch sizing, leasing cleanup, retry with reduced candidate count.                      |
| Sparse inference latency increases | Total run time extends beyond SLO | Keep sparse models CPU-first; cache hot indices on GPU; allow fallback to metadata.             |
| Export parsers break on new schema | Downstream tooling fails          | Maintain additive schema, version manifests, update documentation/tests, provide feature flags. |
| Telemetry volume spikes            | Monitoring costs/log noise        | Sample or aggregate spans; expose config to adjust logging level.                               |

## Testing and Validation

- **Unit Tests:**
  - Cover `CrossEncoderBatchExecutor` batch sizing, leasing behavior, and telemetry emission.
  - Validate `SparseVectorGenerator` handles live inference and fallback paths.
- **Integration Tests:**
  - Run end-to-end embedder on small corpus with rerank/sparse enabled; verify export manifest, JSONL outputs, telemetry entries.
  - Stress test dynamic batch sizing by simulating low-memory conditions.
- **Performance Tests:**
  - Benchmark rerank latency with varying candidate counts/batch sizes to confirm adherence to 12 GB cap.
  - Measure sparse inference throughput vs metadata fallback to ensure acceptable overhead.

## Next Steps

1. Implement CrossEncoder and sparse executor modules, integrate with `BatchRunner`, and wire CLI flags.
2. Update export runtime and telemetry instrumentation, including schema versioning and docs.
3. Add regression tests and performance benchmarks ensuring rerank/sparse paths stay within resource limits.
4. Roll out in staged environment (e.g., local GPU, then Kaggle) with telemetry monitoring before broad adoption.
