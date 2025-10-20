## 1. Implementation
- [x] 1.1 Instrument `UltimateKaggleEmbedderV4` with a rotation telemetry tracker that captures batch index, chunk slice, model key, device, timing, and status for every sequential pass without altering existing mitigation/OOM hooks.
- [x] 1.2 Update `generate_embeddings_kaggle_optimized` to pass an explicit `slice(batch_index, batch_end)` into `generate_ensemble_embeddings`, collect emitted telemetry per batch, and fail fast if any configured model skips a batch.
- [x] 1.3 Refactor the sequential execution loop in `generate_ensemble_embeddings` to enforce deterministic participation, handle retries, and surface structured failure metadata while keeping aggregation logic unchanged.
- [x] 1.4 Extend `CollectionRunResult` and `scripts/embed_collections_v5.py` logging to stream rotation telemetry to stdout and embed it in the run summary payload alongside mitigation events.
- [x] 1.5 Document the updated summary schema (rotation timeline field) and gate telemetry payload size to avoid excessive Kaggle logging noise.

## 2. Validation
- [x] 2.1 Add unit tests covering sequential ensemble rotation with three models, asserting telemetry order, batch coverage from index 0, and failure handling when a pass is forced to error.
- [ ] 2.2 Write summary serialization coverage that asserts `rotation_events`, `ensemble_rotation_limit`, and overflow metadata persist in the run summary payload.
- [ ] 2.3 Run an end-to-end dry run (CPU acceptable) with three ensemble models, capturing the enhanced batch-source logs and verifying summary telemetry reflects every model on every processed batch.
