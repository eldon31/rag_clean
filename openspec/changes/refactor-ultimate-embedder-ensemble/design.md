## Context
The modular Ultimate Embedder retains compatibility scaffolding from the monolithic refactor: duplicate ensemble execution paths, dormant sparse vector runtime hooks, and partially implemented configuration flags. Production workflows rely on the exclusive GPU leasing flow, yet alternate branches still exist and complicate reasoning. We need a clean architecture that exposes a single ensemble coordination surface and a single dense model registry while dropping unused helpers.

Key constraints:
- Kaggle GPU memory limits (T4 x2) require one-model-at-a-time leasing for stability.
- The compatibility shim must continue to import from `processor.ultimate_embedder` without exposing retired APIs.
- Downstream scripts (`scripts/embed_collections_v5.py`) must still support CLI execution, but only through the exclusive path.

## Goals / Non-Goals
- Goals: Simplify ensemble orchestration around `exclusive_mode`; remove unused config fields, sparse runtime, and dead helpers; consolidate model registry usage; update specs/tests for the new contract.
- Non-Goals: Rework chunking/export formats, introduce new ensemble strategies, or redesign telemetry payload structure beyond removing references to deleted helpers.

## Decisions
- Decision: Make `exclusive_mode` the sole control flag for ensemble execution. All sequential/parallel toggles will be removed, and the batch runner will always lease GPUs to the active model.
- Decision: Delete sparse runtime initialisation paths and enforce metadata-driven sparse vector generation as the only supported approach.
- Decision: Treat `KAGGLE_OPTIMIZED_MODELS` as the single source of truth for dense encoders. Any duplicated registries or overrides will be removed in favour of this dictionary.
- Decision: Remove helper methods that only served the deprecated code paths (progress `to_dict`, GPU lease summary metrics, throughput error logging, core export/upload helpers). Telemetry will no longer reference them.

## Risks / Trade-offs
- Removing sparse runtime hooks may affect any hidden consumers; mitigate by confirming no active callers and documenting the removal as breaking.
- Exclusive-only pipeline could surface latent issues if parallel mode masked bugs; mitigate with targeted integration tests on multi-model ensembles.
- Simplifying reranker helpers may limit future expansion; mitigate by documenting TODOs if new wiring is planned soon.

## Migration Plan
1. Update specs to capture the exclusive-only ensemble contract and canonical registry requirement.
2. Remove code paths and helpers, adjusting tests accordingly.
3. Run integration tests/smoke suites and document CLI changes.
4. Communicate breaking removal of sparse runtime and deprecated helpers in release notes.

## Open Questions
- Do we need to expose a future extensibility point for alternative ensemble strategies, or is exclusive leasing sufficient for the foreseeable roadmap?
