# Feature Planning Process

## 1. Feature Requirements
- **Problem Statement:** `processor/ultimate_embedder/core.py` remains a 3.6K-line monolith that couples chunk loading, model lifecycle, adaptive batching, sparse/ensemble orchestration, monitoring, and export logic. The size and entanglement hinder testability, slow onboarding, and increase regression risk whenever we adjust Kaggle execution.
- **Target Users:** Internal operators and contributors who maintain the embedding runtime, run Kaggle batches, and extend hybrid retrieval capabilities.
- **Success Criteria:**
  - Introduce focused runtime services (chunk ingestion, model management, batch execution, sparse/rerank pipelines, export coordination) under `processor/ultimate_embedder/` with clean interfaces consumed by the existing facade.
  - Reduce `core.py` to a façade/controller under 800 lines while preserving public APIs (`UltimateKaggleEmbedderV4`, `generate_embeddings_kaggle_optimized`) and enforce the limit via an automated executable-line check in CI/tooling.
  - Deliver executable tasks (see `tasks.md`) fully checked off with passing regression and new unit coverage.

## 2. Architectural Considerations
- **Current Components:**
  - `core.py` implements every stage of the pipeline, from filesystem crawling through GPU telemetry, embedding loops, sparse vectors, reranking, search helpers, and exporters.
  - Supporting modules (`config.py`, `controllers.py`, `telemetry.py`) exist but are under-utilised; `export.py` is effectively empty.
  - Downstream consumers include `scripts/embed_collections_v5.py`, processor tests, and future MCP integrations.
- **Components to Introduce:**
  - `chunk_loader.py`: load and normalise chunk files, metadata enrichment, modal hint inference.
  - `model_manager.py`: resolve primary/ensemble/companion model lifecycles, cache management, device placement.
  - `batch_runner.py`: own adaptive batching loop, GPU snapshot sampling, telemetry hooks, aggregation outputs.
  - `sparse_pipeline.py` and `rerank_pipeline.py`: encapsulate sparse vector generation and CrossEncoder reranking.
  - `export_runtime.py`: coordinate export writers, run summary emission, and telemetry hand-off (with `export.py` acting as a thin compatibility shim).
  - `monitoring.py`: consolidate performance monitors and background threads currently buried in `core.py`.
- **API Considerations:**
  - Keep `UltimateKaggleEmbedderV4` constructor signature stable; surface new services via dependency injection defaults for advanced use cases.
  - Ensure legacy shim `processor/kaggle_ultimate_embedder_v4.py` remains functional.
  - No external API changes expected, but module import paths for internals will update; document in developer notes.

## 3. Implementation Strategy
- **Task Breakdown:**
  1. Capture current behaviour: baseline telemetry payloads, export structures, and Kaggle batch metrics.
  2. Extract reusable utilities from `core.py` into new modules (loader, sparse/rerank helpers) without altering orchestration.
  3. Introduce `ModelManager` and `BatchRunner` abstractions; refactor the facade to delegate responsibilities.
  4. Rehome monitoring/export logic into dedicated modules and wire them into the facade.
  5. Update tests/docs to reflect module layout; expand unit coverage for each new component.
  6. Run full pytest suite plus targeted performance smoke to validate parity.
- **Dependencies:** later refactors rely on extracted utilities existing; testing/documentation updates depend on refactored facade.
- **Complexity & Effort:** High—touches critical runtime path; plan phased commits per service to reduce risk.
- **Implementation Sequence:** loader → sparse/rerank → model manager → batch runner → monitoring/export (`export_runtime.py`) → line-check integration → facade cleanup → compatibility + tests → docs.
- **Files Impacted:** new modules under `processor/ultimate_embedder/`, trimmed `core.py`, legacy shim, scripts, tests, docs, OpenSpec specs.

## 4. Testing Strategy
- **Unit Tests:**
  - Add suites for `ChunkLoader`, `ModelManager`, `BatchRunner`, sparse/rerank helpers, and monitoring utilities.
  - Verify adaptive batching and mitigation events via isolated tests using torch stubs.
  - Ensure export/runtime modules emit structured summaries identical to current expectations.
- **Integration Tests:**
  - Re-run existing embedder pipeline tests; add scenario invoking the facade end-to-end with fake models to assert telemetry and export outputs.
  - Exercise Kaggle-like configuration in dry-run mode to confirm device assignments.
- **Validation:** compare JSON summaries and telemetry logs before/after refactor; update fixtures if canonical structure changes.
- **Test Updates Needed:** adjust fixtures referencing methods moved out of `core.py`, extend regression snapshots for new module boundaries.

## 5. Risks and Mitigations
- **Service Boundary Drift:** keep modules focused, document dependencies in `design.md`, and enforce through unit tests.
- **Performance Regression:** maintain streaming behaviour, run smoke performance tests, and monitor GPU telemetry consistency.
- **Compatibility Issues:** retain shim exports, add import regression tests, and provide migration notes.
- **Complexity Creep:** favour simple classes/functions per module; postpone advanced abstractions unless justified by use cases.

## 6. Acceptance Criteria
- `core.py` reduced below 800 lines with responsibilities delegated to new modules.
- All tasks in `tasks.md` checked off with associated tests passing (`pytest` green, lint clean).
- Telemetry, export artefacts, and summary JSONs match baseline expectations within tolerance.
- Documentation updated (developer notes + relevant docs) describing new module layout.
- Spec delta under `specs/embedding-pipeline/` validated; `npx openspec validate refactor-ultimate-embedder-core --strict` passes.
