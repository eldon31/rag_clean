- [x] 1.1 Capture current telemetry/export snapshots from `UltimateKaggleEmbedderV4.generate_embeddings_kaggle_optimized` using dry-run fixtures.
- [x] 1.2 Record `core.py` public surface (methods, attributes) for regression tracking.
- [x] 1.3 Prototype executable-line counting script for `core.py`, record baseline output, and store it with engineering notes.

## 2. Module Extraction
- [x] 2.1 Introduce `chunk_loader.py` with chunk ingestion + metadata enrichment helpers migrated from `core.py`.
- [x] 2.2 Move sparse vector and modal hint logic into `sparse_pipeline.py` and reranking helpers into `rerank_pipeline.py`.
- [x] 2.3 Create `model_manager.py` encapsulating primary/ensemble/companion model lifecycle, cache, and device placement.
- [x] 2.4 Implement `batch_runner.py` with adaptive batching loop integrating `AdaptiveBatchController` + telemetry hooks.
- [x] 2.5 Extract performance monitoring into `monitoring.py` and migrate export coordination into the new `export_runtime.py`, leaving `export.py` as a compatibility shim.

## 3. Facade Refactor
- [x] 3.1 Refactor `UltimateKaggleEmbedderV4` to delegate responsibilities to new services while preserving public API.
- [x] 3.2 Update dependency injection defaults and wire telemetry to new modules.
- [x] 3.3 Ensure legacy shim `processor/kaggle_ultimate_embedder_v4.py` re-exports the facade without breaking imports.

## 4. Test & Tooling Updates
- [x] 4.1 Add targeted unit tests for each new module (chunk loader, model manager, batch runner, sparse/rerank pipelines, monitoring/export).
- [x] 4.2 Refresh integration tests and fixtures referencing moved helpers; add regression assertions for telemetry/export parity.
- [x] 4.3 Run full `pytest` suite + linting; update CI documentation if new commands added. *(Commands: `C:/Python313/python.exe -m pytest`, `C:/Python313/python.exe -m ruff check processor/ultimate_embedder`.)*
- [x] 4.4 Integrate the executable-line checker into CI/tooling so builds fail when `core.py` exceeds 800 executable lines. *(New guard: `tests/test_core_line_limit.py`; baseline enforced via `openspec/.../core_executable_line_baseline.json`. Commands: `C:/Python313/python.exe -m pytest`, `C:/Python313/python.exe -m ruff check tests/test_core_line_limit.py`.)*

## 5. Documentation & Spec Alignment
- [x] 5.1 Update developer docs (e.g., `Docs/`, `EMBEDDING_LOGGING_ENHANCEMENTS.md`) to explain the modular layout.
- [x] 5.2 Finalise spec delta validation with `npx openspec validate refactor-ultimate-embedder-core --strict` and attach evidence.
