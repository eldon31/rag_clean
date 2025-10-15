# Tasks: Qdrant Embedding Upload Implementation

## Phase 1: Configuration & Setup

### 1.1 Create Configuration Module
- [ ] Create `src/config/qdrant_upload.py`
- [ ] Implement `QdrantUploadConfig` dataclass with all fields from spec
- [ ] Add `from_env()` classmethod for environment variable loading
- [ ] Add `__post_init__()` for path normalization and summary path derivation
- [ ] Write unit tests for config parsing (`tests/unit/test_qdrant_upload_config.py`)

**Acceptance:** Config loads from env vars, CLI args override, paths auto-normalize.

---

## Phase 2: Core Upload Functions

### 2.1 Helper Utilities Module
- [ ] Create `src/storage/upload_utils.py`
- [ ] Implement `assert_health(client: QdrantClient) -> None`
  - [ ] Try `client.get_collections()`
  - [ ] Raise `ConnectionError` on failure
- [ ] Implement `ensure_collection(client, config, force) -> None`
  - [ ] Check collection existence
  - [ ] Validate vector dimension
  - [ ] Create collection if missing
  - [ ] Set HNSW config: `m=16, ef_construct=100`
  - [ ] Create payload indexes for `indexed_fields`
- [ ] Implement `truncate_collection(client, name, force) -> int`
  - [ ] Get current count
  - [ ] Prompt confirmation (if not force)
  - [ ] Delete all points
  - [ ] Return count

**Acceptance:** Functions handle edge cases (missing collection, dimension mismatch, empty collection).

### 2.2 Upload Statistics Tracking
- [ ] Add `UploadStats` dataclass to `upload_utils.py`
- [ ] Implement `elapsed` and `qps` properties
- [ ] Add `__str__()` for pretty printing

**Acceptance:** Stats correctly calculate QPS and elapsed time.

### 2.3 Streaming Upload Function
- [ ] Implement `stream_embeddings_to_qdrant(client, config) -> UploadStats`
- [ ] JSONL reading with line-by-line parsing
- [ ] Validate each record:
  - [ ] Required fields: `id`, `embedding`, `metadata`, `text`
  - [ ] Vector dimension matches `config.vector_dim`
  - [ ] Log warnings for malformed records
- [ ] Batch accumulation (list of ids/vectors/payloads)
- [ ] Upsert with retry logic:
  - [ ] Max 3 attempts
  - [ ] Exponential backoff: 0.5s, 1s, 2s
  - [ ] Log retry attempts
- [ ] Progress logging every 1000 records or 5 seconds
- [ ] Handle final partial batch
- [ ] Return `UploadStats`

**Acceptance:** Successfully uploads 10k+ record file with batching, handles retries, skips malformed lines.

---

## Phase 3: Validation

### 3.1 Validation Module
- [ ] Add `ValidationResult` dataclass to `upload_utils.py`
- [ ] Implement `validate_ingestion(client, config, stats) -> ValidationResult`
- [ ] Get collection count via `client.count()`
- [ ] Load summary JSON (if exists):
  - [ ] Parse `total_chunks` field
  - [ ] Compare with collection count
- [ ] Run sample search:
  - [ ] Scroll to get first point
  - [ ] Search with its vector
  - [ ] Confirm results returned
- [ ] Populate `ValidationResult` with:
  - [ ] `collection_count`
  - [ ] `expected_count`
  - [ ] `count_match` (boolean)
  - [ ] `sample_search_success` (boolean)
  - [ ] `errors` (list of discrepancies)

**Acceptance:** Validation detects count mismatches and search failures.

---

## Phase 4: CLI Implementation

### 4.1 Argument Parsing
- [ ] Create `scripts/upload_qdrant_embeddings.py`
- [ ] Add `argparse` setup with all arguments from spec:
  - [ ] `--embeddings` (Path)
  - [ ] `--collection` (str)
  - [ ] `--url` (str)
  - [ ] `--api-key` (str, optional)
  - [ ] `--batch-size` (int)
  - [ ] `--truncate` (flag)
  - [ ] `--force` (flag)
  - [ ] `--dry-run` (flag)
  - [ ] `--verbose` (flag)
- [ ] Add `--help` descriptions

**Acceptance:** `python scripts/upload_qdrant_embeddings.py --help` shows all options.

### 4.2 Main CLI Flow
- [ ] Implement `main()` function following spec flow:
  1. [ ] Parse arguments
  2. [ ] Setup logging (INFO/DEBUG based on --verbose)
  3. [ ] Load config from env
  4. [ ] Override config with CLI args
  5. [ ] Validate embeddings file exists (exit 1 if not)
  6. [ ] Create `QdrantClient`
  7. [ ] Health check (exit 2 on failure)
  8. [ ] Ensure collection (exit 3 on schema error)
  9. [ ] Optional truncation
  10. [ ] Skip upload if dry-run
  11. [ ] Stream upload (exit 4 on failure)
  12. [ ] Validate ingestion (exit 5 on validation failure)
  13. [ ] Success exit 0
- [ ] Add `if __name__ == "__main__": main()`

**Acceptance:** CLI runs end-to-end, handles errors gracefully with correct exit codes.

### 4.3 Logging & Progress
- [ ] Configure `logging` module with timestamp format
- [ ] Add checkmark/cross symbols for status (✓/✗)
- [ ] Optional: Add `tqdm` progress bar in `stream_embeddings_to_qdrant`
- [ ] Log final summary:
  - [ ] Total records
  - [ ] Inserted/skipped/failed
  - [ ] Elapsed time
  - [ ] QPS

**Acceptance:** Logs are readable and provide clear progress indicators.

---

## Phase 5: Testing

### 5.1 Unit Tests
- [ ] Create `tests/unit/test_upload_utils.py`
- [ ] Test `UploadStats` calculations
- [ ] Test retry backoff logic (mock client)
- [ ] Test record validation (malformed JSON, missing fields, wrong dimension)

**Acceptance:** All unit tests pass.

### 5.2 Integration Test Fixture
- [ ] Create `tests/integration/fixtures/sample_embeddings.jsonl`
- [ ] Generate 20 synthetic records:
  - [ ] IDs: `test_chunk_0` to `test_chunk_19`
  - [ ] Embeddings: Random 768-dim vectors (normalized)
  - [ ] Metadata: Sample subdirectory/source_file/chunk_index
  - [ ] Text: Lorem ipsum snippets

**Acceptance:** Fixture file is valid JSONL with 20 records.

### 5.3 Integration Test
- [ ] Create `tests/integration/test_qdrant_upload.py`
- [ ] Add pytest fixture to start/stop Qdrant docker container (or assume running)
- [ ] Test: `test_full_upload_flow`
  - [ ] Upload 20-record fixture
  - [ ] Assert `stats.inserted == 20`
  - [ ] Assert collection count == 20
  - [ ] Run sample search
  - [ ] Cleanup collection
- [ ] Test: `test_truncate_flow`
  - [ ] Upload fixture
  - [ ] Upload again with `--truncate`
  - [ ] Assert count still 20 (not 40)
- [ ] Test: `test_dimension_mismatch`
  - [ ] Create collection with wrong dimension
  - [ ] Attempt upload without force
  - [ ] Assert raises error

**Acceptance:** All integration tests pass with dockerized Qdrant.

---

## Phase 6: Documentation & Polish

### 6.1 README Updates
- [ ] Add "Uploading Embeddings to Qdrant" section
- [ ] Include example commands
- [ ] Document environment variables
- [ ] Add troubleshooting tips (connection errors, dimension mismatch)

**Acceptance:** README clearly explains upload workflow.

### 6.2 Poetry Script Entry
- [ ] Add to `pyproject.toml`:
  ```toml
  [tool.poetry.scripts]
  upload-embeddings = "scripts.upload_qdrant_embeddings:main"
  ```
- [ ] Test: `poetry run upload-embeddings --help`

**Acceptance:** Can invoke via `poetry run upload-embeddings`.

### 6.3 Error Handling Polish
- [ ] Review all error messages for clarity
- [ ] Add suggestions to error messages (e.g., "Check QDRANT_URL environment variable")
- [ ] Ensure stack traces only shown in verbose mode

**Acceptance:** Error messages are user-friendly and actionable.

---

## Phase 7: Real-World Validation

### 7.1 Local Test with Kaggle Output
- [ ] Ensure `docker-compose.yml` Qdrant service is running
- [ ] Run upload with actual `output/embed/qdrant_ecosystem_embeddings.jsonl`
- [ ] Verify counts match summary JSON
- [ ] Run sample queries via Qdrant dashboard (http://localhost:6333/dashboard)
- [ ] Check payload fields are indexed

**Acceptance:** Real dataset uploads successfully; queries return results.

### 7.2 Performance Benchmarking
- [ ] Upload 10k records, measure time & QPS
- [ ] Upload 100k records (if available), check memory usage
- [ ] Test batch size variations (128, 256, 512)
- [ ] Document optimal batch size in README

**Acceptance:** Upload handles large datasets efficiently (>500 qps for 768-dim vectors).

---

## Phase 8: Final Review & Merge

### 8.1 Code Review Checklist
- [ ] All functions have docstrings
- [ ] Type hints present
- [ ] No hardcoded credentials
- [ ] Logging follows consistent format
- [ ] Tests cover happy path & error cases
- [ ] No TODOs or commented-out code

**Acceptance:** Code passes review standards.

### 8.2 OpenSpec Finalization
- [ ] Update `openspec/changes/load-embed-into-qdrant/proposal.md` status to "IMPLEMENTED"
- [ ] Add implementation notes (what worked, what changed from design)
- [ ] Archive change in `openspec/changes/archive/` if using archive pattern

**Acceptance:** OpenSpec change documented as complete.

### 8.3 Git Commit & Push
- [ ] Commit all files with message:
  ```
  feat: Add Qdrant embedding upload CLI
  
  - Implements scripts/upload_qdrant_embeddings.py
  - Adds config/upload_utils.py with validation
  - Includes integration tests with fixtures
  - Updates README with usage examples
  
  Closes #<issue-number>
  ```
- [ ] Push to remote
- [ ] Create PR if using PR workflow

**Acceptance:** Changes merged to main branch.

---

## Summary Checklist

- [ ] Configuration module complete
- [ ] Core upload functions implemented
- [ ] Validation logic working
- [ ] CLI fully functional
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Real-world validation successful
- [ ] Code reviewed & merged

**Estimated Effort:** 6-8 hours (assuming existing Qdrant setup)
