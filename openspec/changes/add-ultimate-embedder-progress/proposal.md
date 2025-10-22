## Why
The current embedding pipeline does not expose deterministic progress metadata for batch execution, making it difficult for operators to understand which documents are being processed during the "Generating embeddings" phase. This limits observability and delays troubleshooting when runs stall or misbehave.

## What Changes
- Add batch progress context (index, total, primary source label) to `_call_encode` invocations so tqdm displays `Batches(<source>)` progress updates.
- Emit structured batch-progress telemetry entries that align with existing mitigation and rotation logs.
- Surface progress labels in run summaries and CLI output for `scripts/embed_collections_v5.py`.

## Impact
- Affected specs: embedding-pipeline
- Affected code: `processor/ultimate_embedder/{core.py,batch_runner.py,telemetry.py,monitoring.py}`, `scripts/embed_collections_v5.py`, documentation under `Docs/`

## Risks & Mitigations
- **SentenceTransformer compatibility:** Passing extra kwargs could break third-party wrappers. *Mitigate* by feature-detecting `encode` signatures, falling back when unsupported, and covering both GPU/CPU paths in tests.
- **Telemetry payload growth:** Additional progress events may exceed existing rotation limits. *Mitigate* by truncating labels and enforcing payload caps inside `TelemetryTracker.record_batch_progress`.
- **Sequential ensemble regressions:** Multi-model runs touch multiple encode paths. *Mitigate* with focused integration tests (`tests/test_ensemble_rotation.py`) and incremental validation after each refactor step.
