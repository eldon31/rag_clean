# Operational Safeguards

Default behavior enables both rerank and sparse stages through the runtime
configuration loader. CLI runs will log the resolved toggle sources; use the
controls below when staging rollbacks or smoke tests.

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

| Layer | Package | Version/PIN | Status | Notes |
| --- | --- | --- | --- | --- |
| GPU orchestration | torch, accelerate | 2.3.x / 0.30.x | present | Align with Kaggle CUDA 12.1 runtime. |
| Dense embeddings | sentence-transformers | 2.7.x | present | Powers the existing dense ensemble. |
| Sparse inference | splade, pyserini (or chosen stack) | latest compatible | pending | Required for Story 2.1; document cache path. |
| Rerank | transformers, cross-encoder weights | 4.41.x | present | Ensure adaptive batching keeps usage <12 GB. |
| Export & storage | qdrant-client, faiss-cpu, numpy, pandas | 1.8.x / 1.7.x / 1.26.x / 2.2.x | present | Produces manifests and JSONL artifacts. |
| API / orchestration | fastapi, pydantic, typer, rich | 0.111.x / 2.7.x / 0.12.x / 13.x | present | CLI, validation, and operator ergonomics. |
| Telemetry | opentelemetry-sdk, prometheus-client | 1.25.x / 0.20.x | pending | Captures rerank/sparse spans and metrics. |
| Tooling | ruff, pytest, pytest-asyncio, mypy | pinned in pyproject | present | Supports regression harness and quality gates. |

