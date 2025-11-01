- [x] 1.1 Review the ensemble flow in `batch_runner.generate_ensemble_embeddings`, tracking the parallel branch, legacy sequential pass logic, and the exclusive lease path documented in `REFACTORING_ANALYSIS_MONOLITHIC_VS_MODULAR.md`.
	- [x] 1.1.a Trace the decision tree in `generate_ensemble_embeddings` (primary-only vs sequential vs parallel) with line references.
	- [x] 1.1.b Follow `BatchRunner.run()` → `run_exclusive_ensemble()` to document how exclusive mode overrides legacy toggles.
	- [x] 1.1.c Identify all call sites (core facade, CLI scripts, tests) that still invoke `generate_ensemble_embeddings` directly and note their expectations.
	- [x] 1.1.d Capture the findings in a short note or summary, clarifying which path we plan to keep and which will be removed.
- [x] 1.2 Inventory configuration flags on `EnsembleConfig` (including `parallel_encoding`, `weighting_strategy`, `aggregation_method`, `memory_efficient`, `preferred_devices`, `warm_cache_after_release`, `sequential_passes`, `exclusive_mode`) plus reranker helpers and sparse runtime entry points to confirm actual call sites.
	- [x] 1.2.a Enumerate every `EnsembleConfig` field and note whether it remains after the refactor (`ensemble_models`, `model_weights`, `exclusive_mode`).
	- [x] 1.2.b Map each removable flag to its current usage (if any) across `processor/ultimate_embedder` and `scripts/`.
	- [x] 1.2.c Identify tests or fixtures that instantiate `EnsembleConfig` with the deprecated fields so they can be updated.
	- [x] 1.2.d Record findings in `findings.md`, including any reranker helpers or sparse runtime toggles discovered during the audit.
- [x] 1.3 Confirm whether `core.main()` remains required for CLI execution and validate that `controllers.GPUMemorySnapshot.used_bytes` is intentionally internal.
	- [x] 1.3.a Double-check external consumers (shim, package exports, scripts) before removing `core.main()`.
	- [x] 1.3.b Draft the refactor plan for deleting `core.main()` and updating exports, pending implement approval.

## 2. Implementation
- [x] 2.1 Remove the unused `EnsembleConfig` attributes (`parallel_encoding`, `weighting_strategy`, `aggregation_method`, `memory_efficient`, `preferred_devices`, `warm_cache_after_release`, `sequential_passes`) and adjust validation/tests so `exclusive_mode` is the sole control flag.
	- Updated config/model manager/core/batch runner to rely on `exclusive_mode`, pruned CLI/test references, and ran `pytest tests/test_exclusive_ensemble_integration.py tests/test_gpu_lease.py` (12 passed).
- [x] 2.2 Delete the parallel ensemble branch and the legacy sequential pass logic in `batch_runner.generate_ensemble_embeddings()`, ensuring the exclusive GPU leasing flow is the only execution path.
- [ ] 2.3 Excise dormant helpers while explicitly retaining the sparse hooks and telemetry utilities we still depend on.
	- **Keep**: `SPARSE_MODELS`, `enable_sparse`, `ModelManager.initialize_sparse_models`, `GPULease.summarize`, `GPULease.get_vram_delta_gb`, `ThroughputMonitor.log_error`, `_normalize_collection_name`, `_get_model_primary_dtype` (for ensemble dtype inspection).
	- [x] 2.3.a Remove `progress.BatchProgressContext.to_dict` (no remaining callers post-telemetry rewrite).
		- Deleted the unused serializer, cleaned up typing imports, and validated progress timeline tests (`test_batch_progress.py`).
	- [x] 2.3.b Document current usage of `_get_model_primary_dtype` and ensure tests cover the dtype enforcement behaviour we rely on during ensemble setup.
		- Added `model_dtypes` registry and `_record_model_dtype` wiring in `core.py`/`model_manager.py`, updated exclusive ensemble stubs, and introduced `test_model_dtype_registry.py` alongside expanded integration assertions to verify dtype tracking surfaces for primary and ensemble models.
	- [x] 2.3.c Remove `core._save_intermediate_results` (abandoned Kaggle intermediate-save helper).
		- Excised the dead Kaggle-only saver and confirmed no callers remain across batch runner flows.
	- [x] 2.3.d Remove `core._generate_upload_script` (duplicate passthrough to `export_runtime`).
		- Dropped the redundant facade wrapper; all export script generation now routes through `ExportRuntime` directly.
- [ ] 2.4 Simplify or revive reranker helpers to support an end-to-end CrossEncoder stage, and verify the CLI entry surface (`core.main()`) still matches the supported execution flow.
	- [ ] 2.4.a Audit existing reranker hooks (helpers, exports, CLI usage) and document required changes for a live CrossEncoder rerank pass.
	- [ ] 2.4.b Reintroduce or adapt the helper functions needed to configure CrossEncoder devices (`set_cross_encoder_device`, `unload_reranker`, `get_device`) within the modular pipeline, ensuring they align with `RerankPipeline` and telemetry expectations.
	- [ ] 2.4.c Confirm `core.main()` either reflects the revived rerank flow or remove/update it if it no longer represents the supported execution path.
- [x] 2.5 Promote `KAGGLE_OPTIMIZED_MODELS` as the canonical dense registry, refactoring CLI entry points, batch runners, and tests to resolve model keys solely against it.

## 3. Validation
- [ ] 3.1 Update or add tests to exercise the exclusive ensemble flow and confirm no parallel/sequential branches remain callable.
- [ ] 3.2 Add regression tests that fail if removed helpers or config fields resurface (attribute access, telemetry payload shape, invocation attempts on deleted sparse/runtime helpers).
- [ ] 3.3 Run the existing embedding pipeline integration tests or smoke tests to verify end-to-end behavior after refactor.
- [ ] 3.4 Update documentation or CLI usage notes reflecting the exclusive-only ensemble control surface.
