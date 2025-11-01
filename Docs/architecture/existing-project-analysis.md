# Existing Project Analysis

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
