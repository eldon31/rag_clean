# Proposal: Load Kaggle-Generated Embeddings into Qdrant

## Why

We now have Kaggle-generated embeddings stored in `output/embed/qdrant_ecosystem_embeddings.jsonl` with a matching summary file. To make these embeddings queryable we must load them into the running Qdrant instance used by the RAG pipeline. Today there is no automated process to:

1. Verify that the Qdrant service is healthy and the target collection exists (or create it with the correct vector schema).
2. Stream the JSONL embeddings into Qdrant with batching, payload hydration, and id preservation.
3. Validate ingestion by checking point counts and running a sample query.
4. Provide a CLI entry point so devs and CI can re-run the upload whenever new embeddings are produced.

Without this work the new embeddings will remain unused on disk and the search stack will continue to serve stale vectors.

## What Changes

- **NEW CLI COMMAND**: `python -m scripts.upload_qdrant_embeddings` (or `poetry run upload-qdrant-embeddings`) that:
  - Loads configuration (Qdrant URL, API key, collection name, vector dimension) from env/config.
  - Performs a `/healthz` check before uploading.
  - Creates or updates the collection with the expected 768-dim vector schema and payload indexes.
  - Streams the JSONL points in configurable batch sizes with graceful resume support.
  - Validates point count against the input file and optionally executes a probe query.
- **CONFIG SUPPORT**: Add Qdrant upload settings to existing config module (host, port, TLS, API key, collection name, chunk path).
- **DOCUMENTATION**: Update README / operations guide with steps for running the uploader locally and in CI, including prerequisites (running Qdrant container, environment variables).
- **TESTING**: Add integration-style test that spins up the local Qdrant service (via docker-compose) and ensures upload + search is successful against a small fixture.

## Impact

### Affected Specs
- **NEW**: `qdrant-upload` specification describing uploader behavior, validation rules, and observability expectations.

### Affected Code
- `scripts/upload_qdrant_embeddings.py` (new)
- `src/config/providers.py` or similar (new config entries)
- `poetry` / requirements adjustments if `qdrant-client` is missing
- README / operations docs for upload instructions
- Optional: integration test harness under `tests/integration/`

### Benefits
- Embeddings generated on Kaggle become queryable in production/local Qdrant deployments.
- Automated health checks and ingestion validation reduce risk of partial uploads.
- Repeatable CLI enables ops pipelines and regression testing.
- Provides a foundation for future incremental updates or delta uploads.

### Risks & Mitigations
- **Large JSONL size**: Mitigate with streaming reads and small batch upserts.
- **Collection mismatch**: Explicitly enforce 768-dim schema and metadata field presence.
- **Network/auth failures**: Fail fast with descriptive errors and retry logic on transient errors.
- **Duplicate uploads**: Support optional `--truncate` flag or idempotent upserts using deterministic ids from JSONL.

## Success Criteria
- Qdrant collection `qdrant_ecosystem` exists with 768-dim vectors and payload indexes for `subdirectory`, `source_file`, etc.
- Point count in Qdrant matches JSONL record count exactly (validated post-upload).
- Sample search for a known query returns expected metadata payload confirming accessibility.
- CLI exits successfully and provides metrics summary (points inserted, duration, QPS).
- Documentation enables a fresh developer to ingest embeddings with <5 manual steps.
