## ADDED Requirements

### Requirement: Vector Dimension Configuration
The system SHALL support configurable vector dimensions for embedding storage, with 768-dim as the default for CodeRankEmbed model.

#### Scenario: Configure 768-dim vectors
- **WHEN** `QdrantUploadConfig` is initialized
- **THEN** `vector_dim` SHALL default to `768`
- **AND** dimension SHALL be validated against embedding file dimensions

#### Scenario: Reject mismatched dimensions
- **WHEN** embeddings with dimension 3584 are uploaded to a 768-dim collection
- **THEN** the system SHALL raise a validation error
- **AND** log the dimension mismatch with expected vs actual values

### Requirement: Qdrant Collection Management
The system SHALL provide utilities to create, delete, and verify Qdrant collections with optimized configuration for code embeddings.

#### Scenario: Create collection with HNSW indexing
- **WHEN** a new collection is created via `ensure_collection()`
- **THEN** collection SHALL use HNSW index with `m=16`, `ef_construct=100`
- **AND** vectors SHALL use COSINE distance metric
- **AND** optimizers SHALL be configured for 10K indexing threshold

#### Scenario: Delete collection with safety check
- **WHEN** deleting a collection via dimension-based cleanup
- **THEN** system SHALL verify collection dimension matches target (e.g., 3584)
- **AND** system SHALL skip deletion if dimension doesn't match
- **AND** system SHALL log skipped collections

#### Scenario: Verify collection exists
- **WHEN** checking if a collection exists
- **THEN** system SHALL query Qdrant API for collection list
- **AND** return True if collection name matches
- **AND** return False otherwise without raising errors

### Requirement: Binary Quantization Support
The system SHALL enable binary quantization for 768-dim vectors to optimize query performance with minimal accuracy trade-off.

#### Scenario: Enable binary quantization on 768-dim collection
- **WHEN** a collection is created with 768-dim vectors
- **THEN** system SHALL attempt to enable binary quantization
- **AND** quantization SHALL be configured with `always_ram=True`
- **AND** system SHALL log success when enabled

#### Scenario: Fallback to scalar quantization
- **WHEN** binary quantization fails for a collection
- **THEN** system SHALL automatically attempt scalar quantization (INT8)
- **AND** quantization SHALL use `quantile=0.99`, `always_ram=True`
- **AND** system SHALL log the fallback action

#### Scenario: No quantization fallback
- **WHEN** both binary and scalar quantization fail
- **THEN** system SHALL log an error
- **AND** collection SHALL remain functional without quantization
- **AND** system SHALL NOT raise an exception

### Requirement: Embedding Upload with Validation
The system SHALL upload embeddings from JSONL files to Qdrant collections with pre/post validation and batch retry logic.

#### Scenario: Upload embeddings in batches
- **WHEN** uploading embeddings via `stream_embeddings_to_qdrant()`
- **THEN** embeddings SHALL be processed in configurable batch sizes (default: 256)
- **AND** each batch SHALL be upserted with `wait=True`
- **AND** upload progress SHALL be logged

#### Scenario: Validate embedding schema
- **WHEN** loading embeddings from JSONL
- **THEN** each record SHALL be validated for required fields: `id`, `embedding`, `text`
- **AND** records missing required fields SHALL be skipped with a warning
- **AND** embedding dimension SHALL match collection configuration

#### Scenario: Handle batch upload failures
- **WHEN** a batch upload fails
- **THEN** system SHALL retry up to `max_retries` times (default: 3)
- **AND** retry delay SHALL use exponential backoff
- **AND** failed batches SHALL be logged with error details

#### Scenario: Verify point count after upload
- **WHEN** upload completes
- **THEN** system SHALL query collection for point count
- **AND** compare stored count with uploaded count
- **AND** log warning if counts don't match

### Requirement: Deterministic ID Conversion
The system SHALL convert hex-based embedding IDs to valid UUIDs using deterministic hashing to ensure idempotency.

#### Scenario: Convert hex ID to UUID
- **WHEN** an embedding has a hex ID (e.g., "7b54a84c32a7a66d")
- **THEN** system SHALL pad hex to 32 characters with trailing zeros
- **AND** format as UUID: "7b54a84c-32a7-a66d-0000-000000000000"
- **AND** store original ID in payload as `original_id`

#### Scenario: Idempotent UUID generation
- **WHEN** the same hex ID is converted multiple times
- **THEN** system SHALL produce the same UUID each time
- **AND** re-uploading SHALL update existing points (not duplicate)

### Requirement: Migration Safety and Dry-Run Mode
The system SHALL provide dry-run and backup capabilities for safe migration from 3584-dim to 768-dim vectors.

#### Scenario: Dry-run validates without changes
- **WHEN** migration is run with `--dry-run` flag
- **THEN** system SHALL validate all embedding files exist
- **AND** system SHALL check schema and dimensions
- **AND** system SHALL NOT create collections or upload data
- **AND** system SHALL log what would be changed

#### Scenario: Backup collections before deletion
- **WHEN** deleting old collections with `--backup` flag
- **THEN** system SHALL export collection data to JSON
- **AND** backup SHALL include all points with vectors and payloads
- **AND** backup file SHALL be timestamped and stored in `output/collection_backups/`

#### Scenario: Force overwrite existing collections
- **WHEN** migration is run with `--force` flag on existing 768-dim collection
- **THEN** system SHALL delete existing collection
- **AND** create new collection with same name
- **AND** upload embeddings
- **AND** log warning about data loss

### Requirement: Collection Health Verification
The system SHALL provide automated verification to ensure collections are properly configured and functional after migration.

#### Scenario: Verify collection dimension
- **WHEN** running verification script
- **THEN** system SHALL check each collection's vector dimension
- **AND** verify dimension equals expected value (768)
- **AND** log error if dimension mismatches

#### Scenario: Verify point count
- **WHEN** running verification script
- **THEN** system SHALL check each collection's point count
- **AND** compare with expected count (e.g., 9,654)
- **AND** log warning if count is below expected

#### Scenario: Verify quantization enabled
- **WHEN** running verification script
- **THEN** system SHALL check collection quantization config
- **AND** verify binary or scalar quantization is enabled
- **AND** log status for each collection

#### Scenario: Test sample search
- **WHEN** running verification script
- **THEN** system SHALL execute a sample search on each collection
- **AND** verify search returns results within 500ms
- **AND** log error if search fails or times out

## ADDED Metadata

### Collection Naming Convention
- Collection names SHALL match embedding source (e.g., `qdrant_ecosystem`, `docling`, `sentence_transformers`)
- Collection names SHALL be lowercase with underscores (snake_case)
- Collection names SHALL NOT include version numbers or dimension indicators

### Embedding File Format
Embedding JSONL files SHALL follow this schema:
```json
{
  "id": "hex_string_16_chars",
  "embedding": [float × 768],
  "text": "chunk text content",
  "metadata": {
    "subdirectory": "path/to/section",
    "source_file": "original_filename.md",
    "source_path": "full/path/to/file",
    "heading_path": "Section > Subsection",
    "has_complete_code_blocks": true,
    "token_count_valid": true
  }
}
```

### Quantization Configuration
- **Binary Quantization**: For 768-dim vectors, provides 40x speedup, 1-2% accuracy trade-off
- **Scalar Quantization**: INT8 fallback, provides 4x speedup, <1% accuracy trade-off
- **Configuration**: `always_ram=True` to keep quantized vectors in memory for speed

### Performance Targets
- **Query Latency**: <500ms per query (target: 200-400ms)
- **Upload Throughput**: >100 points/second
- **Memory Usage**: <4GB per collection with quantization
- **Accuracy**: >98% recall@10 vs non-quantized
