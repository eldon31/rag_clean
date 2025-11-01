# Data Models and Schema Changes

### New Data Models

#### `CrossEncoderRerankRun`

- **Purpose:** Capture telemetry/export payload for a CrossEncoder batch rerank pass.
- **Integration:** Stored alongside dense export manifests (JSON). Enables CLI summaries, QA audits, telemetry dashboards.

| Field           | Type        | Description                                         |
| --------------- | ----------- | --------------------------------------------------- |
| `run_id`        | UUID        | Correlates with embedding/export batch.             |
| `query`         | string      | User query (truncated/anonymized per policy).       |
| `candidate_ids` | list[str]   | Document IDs scored in this rerank pass.            |
| `batch_size`    | int         | Dynamic batch size selected under 12 GB constraint. |
| `scores`        | list[float] | CrossEncoder similarity scores per candidate.       |
| `latency_ms`    | float       | End-to-end rerank latency.                          |
| `gpu_peak_gb`   | float       | Peak GPU memory recorded for audit/alerts.          |

_Relations_: linked to existing embedding run metadata; future child records (e.g., per-candidate diagnostics) can reference `run_id` if needed.

#### `SparseInferenceRun`

- **Purpose:** Document live sparse vector generation replacing metadata echo path.
- **Integration:** Complements existing sparse JSONL exports; indicates whether live inference or fallback was used.

| Field                     | Type       | Description                                                                 |
| ------------------------- | ---------- | --------------------------------------------------------------------------- |
| `run_id`                  | UUID       | Shares ID with parent embedding batch.                                      |
| `sparse_model`            | string     | Identifier from `SPARSE_MODELS` registry (e.g., `qdrant-bm25`).             |
| `query_sparse_vector`     | dict       | Non-zero indices/values representing query sparse vector.                   |
| `document_sparse_vectors` | list[dict] | Sparse vectors per processed chunk (indices/values).                        |
| `latency_ms`              | float      | Processing time for sparse inference stage.                                 |
| `fallback_used`           | bool       | Indicates metadata-derived sparse vectors (true) vs live inference (false). |

_Relations_: ties into export runtime merging sparse vectors with chunk metadata; telemetry uses `run_id` for correlations.

### Schema Integration Strategy

- **New Tables:** None—continue storing run metadata as JSON/JSONL artifacts; avoid relational migrations.
- **Modified Artifacts:**
  - Export manifest (`processing_summary.json`) versioned to `v4.1`, adding optional `rerank_run` and `sparse_run` sections.
  - CLI summary picks up new sections when present; older runs remain valid.
  - Manifests now include an optional `warnings` array surfaced when rerank/sparse stages are enabled but payloads are missing or when execution failures occur. These warnings preserve run continuity while flagging operators to investigate telemetry/logs.
- **Indexes:** Not required; correlations handled through existing filename conventions and UUIDs.
- **Migration Strategy:**
  - Introduce schema version check in CLI/export runtime.
  - When enhancements disabled, new sections omitted to maintain backward compatibility.
  - Tests verify both legacy (`v4.0`) and enhanced (`v4.1`) manifests parse cleanly.

### Processing Summary v4.1 Additions

- Manifest `schema_version` is fixed at `v4.1` and publishes optional `rerank_run`
  and `sparse_run` sections with nested `payload` objects. The payload mirrors
  the serialized `CrossEncoderRerankRun` and `SparseInferenceRun` fields (e.g.,
  `run_id`, latency, candidate lists, sparse vector coverage) without altering
  existing top-level keys.
- A new `compatibility` block advertises the active schema via
  `{"current": "v4.1", "legacy": ["v4.0"]}` so downstream tooling can branch
  on supported versions.
- `normalize_processing_summary` helper produces defensive copies of manifests,
  ensuring v4.0 payloads receive default `telemetry`, `compatibility`, and
  `warnings` structures before validation scripts compare artifacts.

### Backward Compatibility

- All new fields are additive/optional; legacy tooling ignoring unknown keys continues to function.
- CLI emits soft warnings if rerank/sparse toggles enabled but corresponding sections missing, guiding operators without breaking flows.
- Compatibility metadata keeps v4.0 consumers functional while signalling
  availability of enriched payloads, and normalization ensures QA scripts can
  reason over mixed-version evidence bundles.
- Export runtime retains metadata-derived sparse vectors as fallback until live inference confirmed stable.
