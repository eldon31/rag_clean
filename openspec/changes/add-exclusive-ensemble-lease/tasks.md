## 1. Planning
- [x] 1.1 Review existing sequential ensemble implementation, telemetry coverage, and aggregation/storage flows.
- [x] 1.2 Confirm operator expectations for CLI/config defaults, documentation touchpoints, and acceptable storage strategies for per-model embeddings.

## 2. Implementation
- [x] 2.1 Add GPU lease helper coordinating device acquisition, release, cache eviction, VRAM sampling, and telemetry hooks.
- [x] 2.2 Update `processor/ultimate_embedder/config.py` and CLI plumbing to surface the exclusive ensemble flag and progress annotations.
- [x] 2.3 Teach `model_manager.py` to stage ensemble models on CPU when exclusive mode is active and to hydrate within a lease, including DataParallel unwrap/rewrap and optional warm-cache controls.
- [x] 2.4 Refactor `batch_runner.py` to iterate batches by model, reset adaptive controllers per pass, reindex progress as `(model_pass, batch_idx)`, and propagate model identifiers to progress reporters.
- [x] 2.5 Adjust `core.py` (and companion/reranker integrations) to respect lease ownership, manage per-pass storage/aggregation (RAM or disk), and ensure telemetry records lease lifecycle and VRAM metrics.
- [x] 2.6 Update embedding summaries, run summary serialization, and relevant docs to describe exclusive ensemble behaviour, VRAM reporting, and operator guidance.

## 3. Testing & Validation
- [x] 3.1 Add unit tests covering the lease helper (mocked torch), batch hint recalculation, telemetry payloads, and progress indexing (CPU-compatible).
- [x] 3.2 Extend integration tests verifying model-first execution order and config propagation (CPU mode, no GPU assertions).
- [x] 3.3 Run local regression smokes for default/CPU paths to ensure non-exclusive modes remain unaffected.
- [x] 3.4 Execute `openspec validate add-exclusive-ensemble-lease --strict` and ensure all checks pass.
