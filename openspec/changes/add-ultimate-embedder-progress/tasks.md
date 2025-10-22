## 1. Implementation
- [x] 1.1 Introduce a `BatchProgressContext` in `processor/ultimate_embedder/core.py::_call_encode`, include signature fallback detection for incompatible `encode` implementations, and update internal call sites to provide batch index, total batches, and label.
- [x] 1.2 Update `processor/ultimate_embedder/batch_runner.py` to calculate batch totals once per run, derive labels via `_get_batch_progress_label`, and pass context into `_call_encode` for standard and sequential ensemble paths; confirm sequential device rotations honour the new context.
- [x] 1.3 Extend `processor/ultimate_embedder/telemetry.py::TelemetryTracker` with `record_batch_progress`, enforce payload limits (e.g., label truncation, event caps), and invoke it wherever batch progress events are produced.
- [x] 1.4 Ensure `processor/ultimate_embedder/monitoring.py` and `processor/ultimate_embedder/export_runtime.py` persist batch progress data into run summaries while keeping schemas backwards-compatible via optional fields.
- [x] 1.5 Modify `scripts/embed_collections_v5.py` CLI workflow to render the new progress information alongside existing step logs and verify CLI output in both quiet and verbose modes.

## 2. Validation
- [x] 2.1 Add unit coverage for progress label derivation and tqdm kwargs in `tests/test_batch_source_logging.py` and new `tests/test_batch_progress.py`, covering CPU and CUDA feature flags.
- [x] 2.2 Extend integration tests (`tests/test_ensemble_rotation.py`) to assert sequential ensemble runs emit progress telemetry for every batch and that fallback logic avoids duplicate tqdm kwargs.
- [x] 2.3 Update documentation (`Docs/EMBEDDING_SUMMARY_SCHEMA.md`, `Docs/V5_TUTORIAL.md`) and confirm link checks succeed.
- [x] 2.4 Perform incremental validation after each implementation task (targeted pytest modules, CLI smoke run) to surface regressions early.
- [x] 2.5 Run a manual smoke test on a CPU-only workstation using the locally cached Hugging Face model `models--nomic-ai--CodeRankEmbed`, processing **exactly one chunk file** (e.g., a single JSON from `Chunked/`) to confirm progress bars and telemetry behave without GPU acceleration.
