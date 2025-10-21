# Modular Ultimate Embedder Design

## Overview
The current `processor/kaggle_ultimate_embedder_v4.py` file combines configuration registries, adaptive batching logic, telemetry collectors, export utilities, and the Kaggle-specific orchestration class inside a single 4K+ line module. The refactor introduces a dedicated package (`processor/ultimate_embedder/`) that separates responsibilities while preserving the existing public API. The legacy module will persist as a thin compatibility layer re-exporting classes/functions from the new package until downstream consumers migrate.

## Proposed Package Layout
```
processor/ultimate_embedder/
  __init__.py             # Public exports and compatibility helpers
  config.py               # ModelConfig, KaggleGPUConfig, export configs, registries
  controllers.py          # AdaptiveBatchController, GPU snapshot utilities
  telemetry.py            # Rotation event tracking, mitigation logging helpers
  core.py                 # UltimateKaggleEmbedderV4 orchestrator and embedding pipeline
  export.py               # Export utilities (JSONL, FAISS, sparse sidecars)
```
Optional future modules (`preprocessing.py`, `companions.py`) can be introduced as additional refactors occur.

## Module Responsibilities
- **config.py**
  - Houses dataclasses defining model, GPU, export, ensemble, reranking, and preprocessing configurations.
  - Maintains registry dictionaries (e.g., `KAGGLE_OPTIMIZED_MODELS`) and related helpers.
  - Provides factory functions for resolving HuggingFace cache paths.
- **controllers.py**
  - Contains `AdaptiveBatchController`, GPU memory snapshot dataclasses, and logic for adaptive batch adjustments.
  - Offers deterministic APIs consumed by the core orchestrator; no direct Kaggle dependencies beyond telemetry callbacks.
- **telemetry.py**
  - Implements rotation event tracking, mitigation logging, and batch source summarisation.
  - Exposes structured payload builders used by both the embedder core and summary exporters.
- **core.py**
  - Defines `UltimateKaggleEmbedderV4` with composition: imports configs/controllers/telemetry to orchestrate batch encoding, sequential ensemble passes, and summary production.
  - Provides helper functions formerly embedded in the class (e.g., model loading, encode wrappers, sparse feature toggles) as private utilities within the module.
- **export.py**
  - Contains export logic for numpy arrays, JSONL outputs, FAISS indices, and summary metadata.
  - Accepts dependency injection from `core.py` to avoid circular imports.

## Dependency Direction
- `core.py` is the only module that coordinates runtime state; it imports helpers from `config.py`, `controllers.py`, `telemetry.py`, and `export.py`.
- Supporting modules remain stateless and MUST NOT import back into `core.py` (or each other) beyond type hints, preventing circular dependencies.
- Export helpers receive data structures from `core.py` but do not retain global state, keeping the dependency graph acyclic.

## Compatibility Strategy
- `processor/kaggle_ultimate_embedder_v4.py` remains present, importing public symbols from `processor.ultimate_embedder.core` (and other modules as needed) then re-exporting them. Deprecated warnings can be added after behaviour stabilises.
- Scripts/tests that rely on the old path continue working immediately after refactor, enabling gradual migration.

## Data & Control Flow
1. `UltimateKaggleEmbedderV4` initialises by loading config dataclasses from `config.py` and constructing controllers/telemetry objects.
2. During embedding runs, batch orchestration delegates to `AdaptiveBatchController` and telemetry helpers for rotation events.
3. After each batch, export helpers commit intermediate results through `export.py` functions.
4. Batch runner scripts consume identical APIs; only import locations change.

## Open Questions / Follow-up
- Determine whether export utilities should be further split between dense and sparse outputs.
- Evaluate whether Matryoshka and companion model utilities warrant separate modules; defer until initial extraction succeeds.
- Decide on deprecation timeline for the old module path based on downstream readiness.
