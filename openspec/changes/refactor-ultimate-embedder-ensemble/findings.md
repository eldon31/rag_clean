# Task 1.1 Findings

## 1.1.a Decision Tree in `BatchRunner.generate_ensemble_embeddings`
- **Primary-only path** (`batch_runner.py:108-148`): triggered when `enable_ensemble` is false or `ensemble_config` is absent. Calls `_get_primary_model()` and `_call_encode()` once, logs progress, and returns early.
- **Parallel branch** (`batch_runner.py:170-226`): executes when `sequential_passes` is falsy. Iterates `ordered_models`, loads each on the current device, encodes without staging, and aggregates with weighting. No GPU leasing; prone to VRAM spikes.
- **Legacy sequential branch** (`batch_runner.py:228-498`): runs when `sequential_passes` is truthy. Moves models to preferred devices, retries on OOM, optionally falls back to CPU, records rotation telemetry. Still uses manual device juggling instead of the lease abstraction.

## 1.1.b Exclusive Path in `BatchRunner.run()`
- `BatchRunner.run()` (`batch_runner.py:522-579`) fabricates an ensemble config if missing, forces `exclusive_mode=True`, and delegates to `run_exclusive_ensemble()`.
- `run_exclusive_ensemble()` (`batch_runner.py:581-810`) is the only path called by `generate_embeddings_kaggle_optimized()`. It acquires GPU leases per model, stages prior models to CPU, and runs batches inside the lease context. Sequential toggles are ignored here.

## 1.1.c Current Call Sites
- The facade method `UltimateKaggleEmbedderV4.generate_ensemble_embeddings()` (`core.py:937-965`) simply delegates to the batch runner.
- CLI and pipeline calls (`generate_embeddings_kaggle_optimized()` in `core.py:1332-1346`, scripts like `scripts/embed_collections_v6.py`, and tests under `tests/`) invoke `BatchRunner.run()`, not `generate_ensemble_embeddings()` directly.
- Tests and scripts still construct `EnsembleConfig(sequential_passes=True)` to avoid the parallel branch when calling older APIs; these will need updating when the field is removed.

## 1.1.d Summary
- We will preserve the exclusive lease path (`BatchRunner.run_exclusive_ensemble`) and the primary-only fallback.
- The parallel branch and manual sequential branch in `generate_ensemble_embeddings()` are slated for removal once call sites are updated.
- Downstream code already relies on `run()`/`run_exclusive_ensemble()` for real runs, so deleting the legacy branches should be low risk after config cleanup.

## 1.2 Ensemble Configuration & Related Surfaces
- **Fields to retain**: `ensemble_models`, `model_weights`, `exclusive_mode` (the only knobs needed for exclusive ensemble execution).
- **Fields flagged for removal**:
	- `parallel_encoding`: declared in `config.py` but never read elsewhere.
	- `weighting_strategy` / `aggregation_method`: only referenced in the demo `core.main()` stub; no runtime logic branches on them.
	- `memory_efficient`: unused for ensembles (dense `ModelConfig` retains its own flag).
	- `sequential_passes`: toggles the legacy sequential branch; used in tests (`tests/conftest.py`, `tests/test_exclusive_ensemble_integration.py`) and `scripts/embed_collections_v6.py` defaults.
	- `preferred_devices`: read in `core.py` (`__init__`, `_select_sequential_device`) solely to support the legacy sequential logic.
	- `warm_cache_after_release`: checked in `model_manager.py:493` when staging models between passes.
- **Exclusive mode**: Actively used throughout (`model_manager.py`, `batch_runner.py`, environment overrides) and becomes the sole ensemble control.
- **Reranker helpers**: No standalone helpers like `set_cross_encoder_device` exist in the current package; `rerank_pipeline.py` exposes only the `RerankPipeline` class, so deletions will focus on stale exports if found.
- **Sparse runtime toggles**: `core.py` still honours `enable_sparse` and calls `_initialize_sparse_models()` (delegating to `ModelManager.initialize_sparse_models()`). `config.py` exports `SPARSE_MODELS`, and `model_manager.py` maintains sparse loaders—prime targets for removal in later tasks.
- **Test/fixture touch points**: `EnsembleConfig(sequential_passes=True)` appears in `tests/conftest.py` and `tests/test_exclusive_ensemble_integration.py`; CLI presets in `scripts/embed_collections_v6.py` also set `sequential_passes`. These will need updating once the fields are removed.

## 1.3 CLI Entry & GPU Snapshot Checks
- `core.main()`: defined in `processor/ultimate_embedder/core.py:1408-1506`, exported via `processor.ultimate_embedder.__init__` and the `kaggle_ultimate_embedder_v4` shim. No in-repo code imports or invokes it; the CLI (`scripts/embed_collections_v6.py`) and tests rely on `generate_embeddings_kaggle_optimized()` instead. Removing `core.main()` will therefore require only updating the shim and public exports.
- `GPUMemorySnapshot.used_bytes`: remains an internal property inside `controllers.py`; no external call sites reference it. It safely continues to serve as a convenience for utilization metrics without exposing public API.
- External consumer audit (1.3.a): repo-wide searches for `from processor.ultimate_embedder import main`, `ultimate_embedder.core import main`, and direct `main()` calls returned no matches beyond the package exports. The only surfaces to adjust are `processor/ultimate_embedder/__init__.py` and `processor/kaggle_ultimate_embedder_v4.py`.
- Refactor plan (1.3.b): when approved, delete `core.main()` and its import/export entries, prune any demo-only configuration that references removed fields, and ensure documentation points users to the CLI script or direct `UltimateKaggleEmbedderV4` usage instead of the old demo entry point.
