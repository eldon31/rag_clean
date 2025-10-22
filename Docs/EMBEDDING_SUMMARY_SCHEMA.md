# Embedding Run Summary Schema

The batch embedding runner writes a summary JSON payload (default name `embedding_summary.json`) for every collection. Each `CollectionRunResult` entry describes the status of a processed collection and the telemetry that accompanies it. Starting with the V5 modular refactor, summary generation is handled by `processor/ultimate_embedder/core.py` with telemetry helpers in `processor/ultimate_embedder/telemetry.py`; the legacy `processor/kaggle_ultimate_embedder_v4.py` module remains as a compatibility shim that re-exports the new package and emits a deprecation warning.

## Base Fields

Every summary entry contains:

- `collection` – Collection name taken from the directory name.
- `status` – `completed`, `skipped_*`, or `failed`. Consumers should treat any non-`completed` value as a soft failure.
- `chunks` – Total chunks processed when a run completes.
- `performance` – Raw embedder output with timing, batch sizing, and telemetry. See the rotation telemetry section below for notable sub-fields.
- `exports` – Map of export artifact names to file paths.
- `target_qdrant_collection` – Target collection name when the Qdrant export module is active.
- `v5_metadata` – V5-specific metadata (chunker version, matryoshka dimension, chunk file counts).
- `archive` – Path to the generated `.zip` bundle when `--zip-output` is enabled.
- `mitigation_events` / `cache_events` – Lists of mitigation and cache telemetry emitted by the embedder. Only present when events exist.
- `gpu_snapshot_summary` – Aggregated GPU utilisation telemetry when GPU monitoring is active.
- `rotation_events` – Sequential ensemble rotation telemetry (optional; see below).
- `error` / `skip_reason` – Present only when a failure or skip occurs.

## Rotation Telemetry Payload

Sequential ensemble runs emit a rotation timeline under `performance.ensemble_rotation`. Each event contains the following keys:

| Field | Description |
| --- | --- |
| `batch_index` | Zero-based batch ordinal captured at run time. |
| `model` | Model key resolved from `KAGGLE_OPTIMIZED_MODELS`. |
| `device` | Device string (for example `cuda:0` or `cpu`). |
| `chunk_count` | Number of chunks encoded during the pass. |
| `duration_seconds` | Wall-clock time spent encoding the batch. |
| `status` | `completed`, `failed`, or `retried`. |
| `chunk_samples` | Up to five representative chunk IDs, trimmed to prevent payload bloat. |
| `timestamp` | Epoch timestamp added server-side when the event is recorded. |

### Payload Limits

To keep Kaggle logs manageable, rotation telemetry is capped inside the embedder:

- `performance.ensemble_rotation_limit` – Maximum number of events retained per run. Default is `500`; override with `EMBEDDER_ROTATION_LIMIT=<int>`.
- `performance.ensemble_rotation_overflow` – Count of events dropped once the limit is reached. The embedder always prefers retaining non-`completed` statuses so that failures are not discarded.

When overflow occurs, `scripts/embed_collections_v5.py` surfaces a warning similar to:

```
… truncated 42 rotation event(s) beyond limit 500
```

This makes it easy to detect when additional instrumentation is required.

### Consumer Guidance

- Treat the telemetry arrays as best-effort diagnostics. Runs succeed even when the rotation payload is truncated.
- Use the overflow counter to decide whether to re-run with a higher limit (via `EMBEDDER_ROTATION_LIMIT`) when deeper auditing is required.
- The `chunk_samples` array is intentionally trimmed to five entries to prevent noisy Kaggle stdout logs. Do not rely on it for exhaustive coverage.

## Backward Compatibility

Existing fields remain unchanged. Consumers that ignore the new rotation metadata continue to operate as before. The new fields are optional and only appear when sequential ensemble mode is active.
