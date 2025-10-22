## Context
`UltimateKaggleEmbedderV4` currently mixes chunk ingestion, model resolution, adaptive batching, sparse/rerank pipelines, performance monitoring, and export orchestration within a single 3.6K-line class. This violates our maintainability guardrails and complicates targeted testing (e.g., sparse pipeline, GPU mitigation logic) while increasing the blast radius of each change. Prior modularisation introduced `config.py`, `controllers.py`, and `telemetry.py`, but `core.py` still hosts the bulk of the behaviour.

## Goals / Non-Goals
- **Goals:**
  - Factor the embedder runtime into cohesive services consumed by the existing facade.
  - Provide seams for unit testing GPU mitigation, sparse/rerank logic, and export behaviours without setting up full runs.
  - Maintain functional parity and public APIs for downstream scripts and Kaggle notebooks.
- **Non-Goals:**
  - Changing model registries, GPU heuristics, or export formats.
  - Replacing torch/sentence-transformers dependencies.
  - Removing the legacy shim module (deprecation handled separately).

## Decisions
- **Service Layout:**
  - `chunk_loader.py` exports `ChunkLoader` to ingest chunk directories, normalise metadata, and infer modal hints. `core.py` will request preprocessed chunks via this service.
  - `model_manager.py` exposes `ModelManager` handling primary, ensemble, and companion models, including cache refresh, device assignment, and data-parallel wrapping.
  - `batch_runner.py` defines `BatchRunner` coordinating the adaptive batching loop, leveraging `AdaptiveBatchController` and `TelemetryTracker` to emit events while delegating embedding execution back to injected callbacks.
  - `sparse_pipeline.py` / `rerank_pipeline.py` wrap existing sparse vector construction and CrossEncoder reranking logic, now stateless functions or lightweight classes.
  - `export_runtime.py` manages run summary assembly, export artifacts, and mitigation aggregation fed by telemetry snapshots; `export.py` will re-export the public API for backwards compatibility only.
  - `monitoring.py` centralises performance monitor threads/timers currently scattered in `core.py` to avoid duplicate logic.
- **Maintainability Enforcement:** introduce a lightweight executable-line checker (AST/token-based) integrated into CI to ensure `core.py` remains below the 800-line ceiling after refactor.
- **Facade Role:** `UltimateKaggleEmbedderV4` becomes an orchestrator that wires services together; it keeps lifecycle methods (`load_chunks_from_processing`, `generate_embeddings_kaggle_optimized`, export helpers) but defers implementation details to injected services.
- **Dependency Injection:** Services default to concrete implementations but may be replaced during testing. Constructor will accept optional overrides (e.g., `model_manager=None`) to support mocks.
- **State Management:** Shared state (chunk texts, metadata, telemetry) will live in a small data container passed among services to avoid circular references.

## Alternatives Considered
1. **Gradual internal functions without new modules:** rejected because it keeps the monolithic file and hinders reuse/testability.
2. **Full rewrite into pipeline framework (e.g., Prefect):** overkill for current scope, introduces external dependency and exceeds requirement.
3. **Mixins inside `core.py`:** reduces some duplication but keeps file massive and still complicates testing; lacks clear module boundaries.

## Risks / Trade-offs
- **Cross-module coupling:** services may depend on shared state; mitigate by defining a `RuntimeContext` dataclass passed explicitly.
- **Performance overhead:** additional abstractions might add Python indirection; mitigate by keeping services thin and measuring baseline throughput.
- **Torch availability in unit tests:** new modules must guard optional imports (mirroring existing pattern) to keep tests runnable without GPU.

## Migration Plan
1. Introduce services with code copied from `core.py` while keeping existing behaviour; add targeted unit tests for each service.
2. Refactor facade methods to call services; maintain temporary adapters ensuring method signatures do not change.
3. Remove duplicated logic from `core.py` once service integration passes tests.
4. Add `export_runtime.py`, move export orchestration there, and keep `export.py` as a shim.
5. Update legacy shim and documentation.
6. Implement the executable-line checker, wire it into CI/tooling, and document enforcement steps.
7. Execute regression tests and performance smoke; compare telemetry/export snapshots to baseline captured in Task 1.

## Open Questions
- Do we need a persistent cache service shared across runs (vs. existing in-memory cache)? (Out of scope unless required during implementation.)
- Should sparse/rerank services expose async interfaces to prepare future concurrency improvements? (Likely not for this refactor; revisit after modularisation.)
