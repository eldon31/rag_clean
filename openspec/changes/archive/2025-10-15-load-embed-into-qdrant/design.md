# Design: Qdrant Embedding Loader & Verification Pipeline

## Context

Kaggle pipelines produce fresh embeddings (currently `output/embed/qdrant_ecosystem_embeddings.jsonl`) that must be ingested into a running Qdrant instance powering our RAG APIs and MCP servers. Today ingestion is manual; the repo only contains generation scripts. We need a robust, repeatable workflow that:

1. Discovers the embedding artifact (JSONL + summary) and validates basic integrity.
2. Connects to Qdrant using environment-configured credentials.
3. Creates or updates the target collection with consistent vector schema and payload indexes.
4. Streams points into Qdrant with progress logging, batching, retries, and optional truncation.
5. Verifies ingestion via point counts and sample similarity queries.
6. Fits naturally into CLI/automation (Poetry script, Make target, or MCP tool).

**Stakeholders:** Platform team (maintains RAG infra), Data team (generates embeddings), QA/Integration engineers.

**Related assets:**
- `output/embed/qdrant_ecosystem_embeddings.jsonl` (Kaggle output)
- `src/storage/qdrant_store.py` (existing Qdrant integration layer)
- Docker `docker-compose.yml` (contains Qdrant service)

## Requirements

- ✅ Read embeddings from local filesystem (default `output/embed/qdrant_ecosystem_embeddings.jsonl`).
- ✅ Support configurable collection name & vector dimension (default 768, matches nomic-embed-code).
- ✅ Verify Qdrant health before upload; fail fast otherwise.
- ✅ Create collection with payload schema (string fields for `subdirectory`, `source_file`, etc.) and appropriate HNSW config.
- ✅ Batch insert (configurable, default 256) with exponential backoff on transient errors.
- ✅ Option to truncate existing collection before upload (guarded by explicit flag).
- ✅ Post-upload validation: compare point count, run sample query, dump summary.
- ✅ Provide CLI logging with progress and metrics (records/sec, total duration).
- ✅ Exit codes conform to CI expectations (non-zero on any failure).

## Non-Goals

- ❌ Real-time incremental sync (batch-only).
- ❌ Multi-collection orchestration in one run (single collection per invocation, but can be called multiple times).
- ❌ Handling of heterogeneous vector dimensions in one file (validation will reject mismatches).
- ❌ Uploading raw documents or chunking (inputs are pre-chunked embeddings).

## Architecture & Components

### 1. Configuration Layer

Augment existing config module (`src/config/providers.py` or new `config/qdrant_upload.py`) with:

```python
@dataclass
class QdrantUploadConfig:
    url: str = "http://localhost:6333"
    api_key: Optional[str] = None
    collection_name: str = "qdrant_ecosystem"
    vector_dim: int = 768
    payload_schema: Dict[str, ValueSchema] = {
        "subdirectory": str,
        "source_file": str,
        "source_path": str,
        "chunk_index": int,
    }
    embeddings_path: Path = Path("output/embed/qdrant_ecosystem_embeddings.jsonl")
    batch_size: int = 256
    truncate_before_upload: bool = False
    dry_run: bool = False
```

Configuration will load from environment variables (e.g., `QDRANT_URL`, `QDRANT_API_KEY`) with CLI overrides.

### 2. CLI Entrypoint

Create `scripts/upload_qdrant_embeddings.py` with a `main()` function using `argparse`. Responsibilities:

1. Load config (env vars → CLI args → defaults).
2. Instantiate `QdrantClient` from `qdrant-client` library.
3. Call helper functions in this order:
   - `assert_health(client)` → GET `/healthz` or `/readyz`.
   - `ensure_collection(client, config)` → create/update collection with proper vector size and payload indexes.
   - `stream_embeddings_to_qdrant(client, config)` → core upload loop.
   - `validate_ingestion(client, config, summary)` → confirm point count & run sample query.
4. Print summary metrics and exit.

### 3. Collection Management

- Use `client.get_collection(collection_name)` and inspect `vectors.size`. If mismatched, prompt user (or fail depending on `--force`).
- Payload index creation using `client.create_payload_index` for fields frequently filtered in UI/search.
- Provide `--truncate` flag to delete all points prior to upload. Implement via `client.delete(collection_name, points_selector=AllSelector())` with confirmation prompt unless `--yes` or `--force` supplied.

### 4. Embedding Streamer

- Read JSONL in streaming fashion using buffered IO.
- Each line should contain `id`, `embedding`, `metadata`, `text`.
- Validate presence and types; log & skip malformed lines with warning counter.
- Batch upserts via `client.upsert(collection_name, points=Batch(ids, vectors, payloads))`.
- Track metrics: total_points, skipped, duration.
- Implement simple retry with exponential backoff (e.g., 3 attempts, base delay 0.5s) for transient network errors.
- Respect `--dry-run` to simulate without hitting Qdrant (for testing).

### 5. Post-Upload Validation

- Fetch collection info (`client.count`) to ensure expected count.
- Load summary JSON (`qdrant_ecosystem_embedding_summary.json`) if present; compare total chunks.
- Run sample similarity search using vector from first record (or random) to ensure searchable pipeline.
- Output results to console and optionally write `upload_report.json` with metrics.

### 6. Testing Strategy

- Add integration test under `tests/integration/test_qdrant_upload.py`:
  - Spin up docker-compose Qdrant service (reuse existing fixture or provide instructions to run `docker compose up qdrant -d`).
  - Use trimmed fixture JSONL (10-20 points) to simulate upload.
  - Assert count matches and search returns results.

### 7. Observability & Logging

- Use `logging` module with INFO level by default, DEBUG via `--verbose`.
- Include progress bar (tqdm) if available; fallback to periodic log updates.
- Emit final metrics summary: `{total, inserted, skipped, failed, elapsed_seconds, avg_qps}`.

## Alternatives Considered

1. **Using existing `src/storage/qdrant_store.py` directly**: It is tightly coupled with runtime services; easier to create dedicated script so ingestion can run standalone without full app context.
2. **Implementing ingestion in Go/Rust**: Overkill; Python `qdrant-client` is already in use.
3. **Uploading via HTTP curl**: Lack of validation/error handling; Python client provides typed operations and easier schema checks.

## Dependencies

- Ensure `qdrant-client>=1.9.0` is listed in `pyproject.toml` or `requirements-mcp.txt`.
- Optional: `tqdm` for progress bars (already present? verify).

## Rollout Plan

1. Implement CLI + config support.
2. Test locally against dockerized Qdrant using small fixture.
3. Document usage in README.
4. Run uploader against full dataset in staging; verify counts & query results.
5. Promote to production/stable usage.
