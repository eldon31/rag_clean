# Feature Planning Process

## 1. Feature Requirements
- **Problem Statement:** `processor/kaggle_ultimate_embedder_v4.py` has grown into a 4K+ line monolith that mixes configuration models, adaptive batching, telemetry, export logic, and Kaggle-specific orchestration. Refactoring into modular units is required to improve robustness, reuse, and testability for chunked collection workflows.
- **Target Users:** Internal operators running chunked embedding jobs (local or Kaggle) who need reliable, debuggable pipelines.
- **Success Criteria:**
  - Introduce a modular package that separates configuration/dataclasses, controllers (adaptive batching, telemetry), core embedder orchestration, and export routines.
  - Preserve existing behaviour and public entry points (`UltimateKaggleEmbedderV4`, `generate_embeddings_kaggle_optimized`) while enabling unit-level testing of new modules.
  - Deliver a task plan that can be executed incrementally with regression coverage.

## 2. Architectural Considerations
- **Current Components:**
  - `processor/kaggle_ultimate_embedder_v4.py` defines dataclasses (`ModelConfig`, `KaggleGPUConfig`, etc.), helper classes (`AdaptiveBatchController`, `AdvancedTextCache`), and the main `UltimateKaggleEmbedderV4` class alongside export helpers.
  - Dependent scripts: `scripts/embed_collections_v5.py`, tests under `tests/test_ensemble_rotation.py`, `tests/test_batch_source_logging.py`, `tests/test_summary_serialization.py`, plus fixtures in `tests/conftest.py`.
- **New Components Needed:**
  - `processor/ultimate_embedder/config.py` for dataclasses and registries.
  - `processor/ultimate_embedder/controllers.py` for adaptive batching, telemetry, GPU snapshot utilities.
  - `processor/ultimate_embedder/core.py` (or `engine.py`) for the primary embedder orchestration class.
  - `processor/ultimate_embedder/export.py` for export routines.
  - `processor/ultimate_embedder/__init__.py` to re-export public API and maintain compatibility.
- **API Considerations:**
  - Maintain existing imports (`from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4`) via shim module or deprecation path.
  - Ensure new modules expose the same public constructor signatures and methods so dependent scripts/tests remain unchanged.
  - Consider optional environment hooks (Kaggle-specific path detection) when relocating constants.

## 3. Implementation Strategy
- **Task Breakdown:**
  1. Introduce new package scaffolding with config, controllers, telemetry, and export modules; migrate dataclasses and helper classes.
  2. Refactor `UltimateKaggleEmbedderV4` into smaller mixins or composition units within `core.py`, wiring dependencies from imported modules.
  3. Update the legacy file to import from the new package and issue compatibility exports (minimise churn for consumers).
  4. Adjust scripts/tests to import from the new namespace where appropriate and ensure fixtures align with refactored structure.
  5. Expand unit tests for newly isolated modules (e.g., AdaptiveBatchController, telemetry writers) to safeguard behaviour during migration.
  6. Update documentation (schema references, deployment guides) to reflect new layout.
- **Dependencies:**
  - Task 2 depends on Task 1 (modules must exist before class refactor).
  - Script/test updates (Task 4) depend on Tasks 1-3 completing.
  - Additional unit tests (Task 5) rely on the modularised code existing.
- **Complexity & Effort:**
  - High: requires careful dependency untangling and thorough regression coverage due to central role of embedder.
  - Aim for incremental commits per module extraction to reduce risk.
- **Implementation Sequence:**
  1. Scaffold package + move low-risk dataclasses/utilities.
  2. Migrate controller/telemetry helpers.
  3. Rebuild embedder core with imports.
  4. Update compatibility layer and consumers.
  5. Enhance tests/docs.
- **Files Affected (initial estimate):**
  - New: `processor/ultimate_embedder/{__init__.py,config.py,controllers.py,core.py,export.py,telemetry.py}` (exact breakdown to confirm in design doc).
  - Modified: `processor/kaggle_ultimate_embedder_v4.py`, `scripts/embed_collections_v5.py`, tests under `tests/` noted above, documentation referencing file path.

## 4. Testing Strategy
- **Unit Tests:**
  - Add dedicated tests for `AdaptiveBatchController`, GPU snapshot helpers, and telemetry recorders in their new modules.
  - Ensure config dataclasses maintain defaults via builder tests.
  - Validate compatibility layer by instantiating `UltimateKaggleEmbedderV4` through the legacy import path using fixtures.
- **Integration Tests:**
  - Re-run existing pytest suites (`tests/test_ensemble_rotation.py`, `tests/test_batch_source_logging.py`, `tests/test_summary_serialization.py`).
  - Add an integration test covering `generate_embeddings_kaggle_optimized` path using fake models to confirm module wiring.
- **Validation of Requirements:**
  - Confirm new package exports align with API expectations (no import regressions).
  - Verify summary serialization and telemetry outputs are unchanged via snapshot/assertion tests.
- **Existing Tests to Update:**
  - Update fixtures in `tests/conftest.py` if module paths change.
  - Adjust any direct references to helper classes now residing in different modules.

## 5. Risks and Mitigations
- **Technical Risks:**
  - Regression risk from moving code across files -> Mitigate with incremental migrations, extensive unit coverage, and temporary compatibility layer.
  - Circular dependencies when splitting modules -> Mitigate by defining clear module boundaries (config -> controllers -> core) documented in design.
  - Performance regressions due to refactor -> Mitigate by running performance smoke tests or verifying key metrics (batch throughput) after refactor.
- **Product/User Risks:**
  - Operators might experience downtime if imports break -> Provide shim module and update documentation before removal.
  - Kaggle notebooks referencing old paths might fail -> Communicate path updates and keep deprecated paths for at least one release.
- **Mitigation Approaches:**
  - Staged rollout with feature flag or environment switch to revert to legacy module if critical issues appear.
  - Add automated import tests to ensure both old and new entry points resolve successfully.

## 6. Acceptance Criteria
- **Functional:**
  - `UltimateKaggleEmbedderV4` instantiation works via both old and new module paths with identical behaviour verified by regression tests.
  - Telemetry, batch logging, and export outputs match pre-refactor expectations.
- **Performance & Quality:**
  - No measurable degradation (>5% slowdown) when replaying the CPU smoke workload (`scripts/embed_collections_v5.py` against `Chunked/Docling/_docling-project_docling_1-overview_chunks.json`) compared to the current main-branch baseline.
  - All unit/integration tests green; linting passes.
- **Review Scope:**
  - Changes across new `processor/ultimate_embedder` package, legacy shim, scripts, and updated tests must pass code review.
  - Documentation updates (`Docs/`, `openspec/specs/embedding-pipeline/`) reviewed for accuracy.
