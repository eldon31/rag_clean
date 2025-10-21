## Implementation
1. Scaffold `processor/ultimate_embedder/` package with `__init__.py` and placeholder modules (`config.py`, `controllers.py`, `core.py`, `export.py`, `telemetry.py`) and rehome existing dataclasses/utilities from `processor/kaggle_ultimate_embedder_v4.py` without behaviour changes.
2. Move `AdaptiveBatchController`, GPU snapshot helpers, and telemetry recording logic into `controllers.py` / `telemetry.py`; update imports in the legacy file and ensure compatibility shims are in place.
3. Reconstruct `UltimateKaggleEmbedderV4` inside `core.py` using the newly extracted components; reduce the legacy file to thin wrapper exports while keeping runtime behaviour identical.
4. Update `scripts/embed_collections_v5.py`, fixtures (`tests/conftest.py`), and targeted tests (`tests/test_ensemble_rotation.py`, `tests/test_batch_source_logging.py`, `tests/test_summary_serialization.py`) to import from the new package; maintain backwards compatibility for external callers.
5. Expand unit test coverage for newly isolated modules (e.g., the batch controller and the telemetry helpers extracted into `telemetry.py`) and add an integration test covering `generate_embeddings_kaggle_optimized` via fake models.
6. Refresh documentation (`Docs/EMBEDDING_SUMMARY_SCHEMA.md`, deployment guides) and OpenSpec specifications to reflect the modular architecture and deprecation timeline for the legacy monolith file.

## Validation
1. Run `pytest tests/test_ensemble_rotation.py tests/test_batch_source_logging.py tests/test_summary_serialization.py` to confirm regression coverage remains green.
2. Execute any new module-level unit tests and integration tests introduced in Implementation Task 5.
3. Perform a CPU dry-run of `scripts/embed_collections_v5.py` against `Chunked/Docling/_docling-project_docling_1-overview_chunks.json` to confirm telemetry, batch logging, and exports remain consistent.
