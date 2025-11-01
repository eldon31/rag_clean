# Infrastructure and Deployment

### Runtime Outputs and Storage Order

- Embedding runs must finish by persisting artifacts in this sequence: (1) dense embeddings and metadata bundles, (2) sparse vectors merged into JSONL/FAISS outputs, and (3) rerank manifests that log candidate ordering, latency, and GPU usage. The export runtime writes `processing_summary.json` (v4.1) and per-collection JSONL/FAISS files once all stages complete so downstream tools always see dense, sparse, and rerank payloads together.
- Each manifest exposes a `compatibility` block (`{"current": "v4.1", "legacy":
["v4.0"]}`) and nests stage-specific payloads under `rerank_run.payload` and
  `sparse_run.payload`. Operators can rely on the `warnings` array to spot
  missing payloads without blocking exports and trace individual runs via the
  propagated `run_id` fields.
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

### Staging Validation Ownership

**Developer Responsibility:** All staging validation tasks—including Prometheus authentication verification, TLS enforcement checks, and firewall rule testing—are owned by the project developer. This is a solo developer project; references to "operations teams" in validation documentation reflect standard enterprise patterns but map to developer-owned execution in this context.

If a persistent staging environment is provisioned beyond Kaggle in the future, follow the validation plan in `docs/qa/assessments/1.4-security-controls-20251025.md`. No external team coordination is required.

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
