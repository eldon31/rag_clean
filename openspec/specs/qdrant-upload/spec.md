# qdrant-upload Specification

## Purpose
TBD - created by archiving change load-embed-into-qdrant. Update Purpose after archive.
## Requirements
### Requirement: CLI Configuration and Environment Integration

The system SHALL provide a command-line interface that accepts configuration from environment variables, CLI arguments, and sensible defaults.

#### Scenario: Load configuration from environment variables
- **GIVEN** environment variables `QDRANT_URL=http://192.168.1.10:6333` and `QDRANT_API_KEY=secret123` are set
- **WHEN** the CLI runs without `--url` or `--api-key` arguments
- **THEN** the uploader connects to `http://192.168.1.10:6333` with API key `secret123`
- **AND** other settings use defaults (collection=qdrant_ecosystem, batch_size=256)

#### Scenario: Override environment with CLI arguments
- **GIVEN** environment has `QDRANT_URL=http://localhost:6333`
- **WHEN** CLI runs with `--url http://staging.qdrant:6333 --collection test_upload`
- **THEN** the uploader connects to staging server
- **AND** targets collection `test_upload` instead of default
- **AND** CLI arguments take precedence over environment variables

#### Scenario: Validate embeddings file existence before connection
- **GIVEN** CLI is invoked with `--embeddings /nonexistent/file.jsonl`
- **WHEN** configuration validation runs
- **THEN** the CLI exits with code 1
- **AND** error message states: "Embeddings file not found: /nonexistent/file.jsonl"
- **AND** no connection to Qdrant is attempted

### Requirement: Qdrant Health Check and Collection Management

The system SHALL verify Qdrant connectivity and ensure the target collection exists with correct schema before uploading.

#### Scenario: Detect Qdrant connection failure early
- **GIVEN** Qdrant server is not running at configured URL
- **WHEN** health check executes via `client.get_collections()`
- **THEN** CLI exits with code 2
- **AND** error message states: "✗ Qdrant health check failed: [connection error details]"
- **AND** no upload attempts are made

#### Scenario: Create new collection with proper schema
- **GIVEN** Qdrant is running but collection `qdrant_ecosystem` does not exist
- **WHEN** `ensure_collection()` runs
- **THEN** collection is created with vector size 768
- **AND** distance metric is COSINE
- **AND** HNSW config has m=16, ef_construct=100
- **AND** payload indexes are created for: subdirectory, source_file, source_path
- **AND** CLI logs: "✓ Collection 'qdrant_ecosystem' ready"

#### Scenario: Detect vector dimension mismatch
- **GIVEN** collection `qdrant_ecosystem` exists with vector size 512
- **WHEN** uploader attempts to insert 768-dim embeddings without `--force`
- **THEN** CLI exits with code 3
- **AND** error message states: "✗ Vector dimension mismatch: collection has 512, embeddings have 768. Use --force to recreate collection."
- **AND** no data is uploaded

#### Scenario: Recreate collection on dimension mismatch with force flag
- **GIVEN** collection exists with vector size 512
- **WHEN** CLI runs with `--force` flag
- **THEN** existing collection is deleted
- **AND** new collection is created with vector size 768
- **AND** upload proceeds
- **AND** CLI logs: "⚠ Recreated collection due to dimension mismatch (512 → 768)"

### Requirement: Batched Streaming Upload with Validation

The system SHALL read JSONL embeddings line-by-line, validate each record, batch them, and upsert to Qdrant with progress tracking.

#### Scenario: Parse and validate JSONL records
- **GIVEN** JSONL file contains line: `{"id": "chunk_1", "embedding": [0.1, 0.2, ...], "metadata": {...}, "text": "content"}`
- **WHEN** record is read
- **THEN** JSON is parsed successfully
- **AND** required fields (id, embedding, metadata, text) are present
- **AND** embedding dimension equals 768
- **AND** record is added to batch

#### Scenario: Skip malformed records with warning
- **GIVEN** JSONL contains line: `{"id": "chunk_2", "embedding": [0.1]}`  (wrong dimension)
- **WHEN** validation runs
- **THEN** record is skipped
- **AND** warning is logged: "⚠ Skipping malformed record at line 42: embedding dimension mismatch (1 != 768)"
- **AND** `stats.skipped` counter increments
- **AND** processing continues with next line

#### Scenario: Upsert batches when batch size reached
- **GIVEN** batch size is configured as 256
- **WHEN** 256 valid records have been accumulated
- **THEN** `client.upsert()` is called with batch of 256 points
- **AND** batch contains ids, vectors, and payloads
- **AND** progress is logged: "Uploaded 256/10000 records (2.56%)"
- **AND** batch buffer is cleared for next batch

#### Scenario: Upsert final partial batch
- **GIVEN** 10,250 total records with batch size 256
- **WHEN** file reading completes after 40 full batches
- **THEN** remaining 10 records are upserted as final batch
- **AND** `stats.inserted` totals 10,250
- **AND** no records are lost

### Requirement: Retry Logic for Transient Errors

The system SHALL retry failed upsert operations with exponential backoff to handle transient network issues.

#### Scenario: Retry on temporary network error
- **GIVEN** batch upsert fails with connection timeout
- **WHEN** first retry occurs
- **THEN** system waits 0.5 seconds
- **AND** retries upsert
- **AND** logs: "Retry 1/3 for batch starting at record 512"

#### Scenario: Exponential backoff on repeated failures
- **GIVEN** first retry fails
- **WHEN** second retry occurs
- **THEN** system waits 1.0 second (0.5 * 2^1)
- **AND** retries upsert again
- **AND** if second retry fails, waits 2.0 seconds for third attempt

#### Scenario: Fail after max retries exhausted
- **GIVEN** batch fails 3 times
- **WHEN** all retries are exhausted
- **THEN** CLI exits with code 4
- **AND** error message includes batch details and last error
- **AND** `stats.failed` counter reflects failed batch size

### Requirement: Collection Truncation with Safety Guards

The system SHALL optionally delete all points from collection before upload, with explicit confirmation required.

#### Scenario: Prompt confirmation for truncation
- **GIVEN** CLI runs with `--truncate` flag
- **WHEN** truncation step executes and collection has 5,000 points
- **THEN** CLI prompts: "Delete 5000 points from qdrant_ecosystem? [y/N] "
- **AND** waits for user input
- **AND** only proceeds if user types 'y' or 'yes'

#### Scenario: Skip confirmation with force flag
- **GIVEN** CLI runs with `--truncate --force`
- **WHEN** truncation step executes
- **THEN** all points are deleted immediately
- **AND** no confirmation prompt is shown
- **AND** CLI logs: "✓ Truncated 5000 points"

#### Scenario: Abort truncation on negative response
- **GIVEN** truncation prompt is shown
- **WHEN** user types 'n' or presses Enter
- **THEN** truncation is cancelled
- **AND** CLI exits with code 0
- **AND** message states: "Truncation cancelled by user"

### Requirement: Post-Upload Validation and Reporting

The system SHALL verify uploaded data matches expected counts and is searchable after upload completes.

#### Scenario: Validate point count matches inserted records
- **GIVEN** 10,000 records were successfully inserted
- **WHEN** validation runs
- **THEN** `client.count(collection_name)` returns 10,000
- **AND** validation passes with: "✓ Validation passed"
- **AND** report shows: "Collection count: 10000, Expected: 10000"

#### Scenario: Detect count mismatch
- **GIVEN** 10,000 records inserted but collection only has 9,995
- **WHEN** validation runs
- **THEN** validation fails
- **AND** CLI exits with code 5
- **AND** error lists: "Count mismatch: expected 10000, got 9995 (5 points missing)"

#### Scenario: Verify searchability with sample query
- **GIVEN** upload completed successfully
- **WHEN** validation retrieves first point and searches with its vector
- **THEN** search returns at least 1 result
- **AND** validation confirms: "✓ Sample search successful"
- **AND** if search fails, error states: "Sample search failed: collection may not be properly indexed"

#### Scenario: Cross-check with summary JSON
- **GIVEN** `qdrant_ecosystem_embedding_summary.json` exists with `total_chunks: 10500`
- **WHEN** validation loads summary
- **THEN** expected count is set to 10,500
- **AND** validation compares collection count (10,500) against summary
- **AND** if mismatch exists, reports: "Summary file expects 10500, but collection has 10000"

### Requirement: Dry Run Mode and Progress Logging

The system SHALL support simulation mode and provide clear progress indicators during upload.

#### Scenario: Simulate upload without modifying Qdrant
- **GIVEN** CLI runs with `--dry-run` flag
- **WHEN** processing executes
- **THEN** JSONL is read and validated
- **AND** batches are prepared but NOT sent to Qdrant
- **AND** CLI logs: "DRY RUN: Skipping upload"
- **AND** validation stats show what would have been uploaded
- **AND** CLI exits with code 0

#### Scenario: Log progress at regular intervals
- **GIVEN** upload is processing 50,000 records
- **WHEN** every 1,000 records or 5 seconds elapses
- **THEN** progress is logged: "Uploaded 5000/50000 records (10.0%) - 347 qps"
- **AND** includes elapsed time and throughput

#### Scenario: Display final summary metrics
- **GIVEN** upload completes
- **WHEN** final statistics are printed
- **THEN** summary includes:
  - Total records processed
  - Inserted count
  - Skipped count (malformed records)
  - Failed count
  - Elapsed time in seconds
  - Average queries per second (QPS)
- **AND** formatted as: "✓ Upload complete: 10000 points in 28.5s (351 qps)"

### Requirement: Error Handling and Exit Codes

The system SHALL use specific exit codes for different failure modes to support CI/CD integration.

#### Scenario: Exit code 0 for successful upload
- **GIVEN** upload and validation complete without errors
- **WHEN** CLI exits
- **THEN** exit code is 0
- **AND** final message is: "✅ All done!"

#### Scenario: Exit code 1 for configuration errors
- **GIVEN** embeddings file does not exist
- **WHEN** CLI exits
- **THEN** exit code is 1
- **AND** indicates invalid configuration or missing file

#### Scenario: Exit code 2 for connection errors
- **GIVEN** Qdrant is unreachable
- **WHEN** health check fails
- **THEN** exit code is 2
- **AND** indicates network/connection problem

#### Scenario: Exit code 3 for schema errors
- **GIVEN** vector dimension mismatch without force
- **WHEN** collection validation fails
- **THEN** exit code is 3
- **AND** indicates schema incompatibility

#### Scenario: Exit code 4 for upload errors
- **GIVEN** batch upsert fails after all retries
- **WHEN** upload fails
- **THEN** exit code is 4
- **AND** indicates data upload failure

#### Scenario: Exit code 5 for validation errors
- **GIVEN** post-upload count mismatch detected
- **WHEN** validation fails
- **THEN** exit code is 5
- **AND** indicates data integrity issue

