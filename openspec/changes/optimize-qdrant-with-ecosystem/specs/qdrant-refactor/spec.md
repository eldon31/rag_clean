# qdrant-refactor Specification

## Purpose
Consolidate fragmented Qdrant code into unified abstractions to eliminate duplication, improve maintainability, and standardize patterns across the project.

## ADDED Requirements

### Requirement: QdrantRegistry Singleton

The system SHALL provide a singleton `QdrantRegistry` class for managing all Qdrant client connections.

#### Scenario: Get or create client from registry
- **GIVEN** no existing connection for qdrant_ecosystem collection
- **WHEN** `QdrantRegistry.get_or_create_client(config)` is called
- **THEN** new QdrantClient is created with config.connection settings
- **AND** client is cached in registry keyed by (url, api_key, collection_name)
- **AND** subsequent calls return the same client instance

#### Scenario: Registry prevents duplicate connections
- **GIVEN** existing client for url="http://localhost:6333", collection="agent_kit"
- **WHEN** second request for same (url, collection) is made
- **THEN** existing client is returned
- **AND** connection count remains 1
- **AND** no new network connection is established

#### Scenario: Close all connections on shutdown
- **GIVEN** registry has 3 active clients
- **WHEN** `QdrantRegistry.close_all()` is called
- **THEN** all 3 clients are closed gracefully
- **AND** registry cache is cleared
- **AND** memory is freed

### Requirement: QdrantBatchUploader Utility

The system SHALL provide a unified `QdrantBatchUploader` class to consolidate all upload logic.

#### Scenario: Upload embeddings with automatic batching
- **GIVEN** 10,000 embeddings as list of dicts with {id, vector, payload}
- **WHEN** `QdrantBatchUploader.upload(client, collection_name, embeddings, batch_size=256)` is called
- **THEN** embeddings are divided into batches of 256
- **AND** each batch is uploaded using client.upsert()
- **AND** progress is logged every 10 batches: "Uploaded 2560/10000 points (25.6%)"
- **AND** upload completes successfully

#### Scenario: Handle duplicate point_id errors
- **GIVEN** batch contains point with duplicate id from previous upload
- **WHEN** upsert is attempted
- **THEN** error is caught and logged: "Duplicate point_id detected: abc-123"
- **AND** batch is retried with duplicate removed
- **AND** upload continues for remaining points

#### Scenario: Stream from file for large datasets
- **GIVEN** embeddings file with 100K records (too large for memory)
- **WHEN** `QdrantBatchUploader.upload_from_file(client, collection_name, file_path, batch_size=512)` is called
- **THEN** file is streamed in chunks
- **AND** batches are uploaded incrementally
- **AND** memory usage stays below 1GB regardless of file size

### Requirement: Unified ID Conversion

The system SHALL standardize all ID handling through `QdrantIDConverter` to ensure consistency.

#### Scenario: Convert string UUIDs to Qdrant format
- **GIVEN** point_id as string "550e8400-e29b-41d4-a716-446655440000"
- **WHEN** `QdrantIDConverter.to_qdrant_id(point_id)` is called
- **THEN** UUID object is returned
- **AND** Qdrant accepts ID without errors

#### Scenario: Convert integer IDs
- **GIVEN** point_id as integer 12345
- **WHEN** `QdrantIDConverter.to_qdrant_id(point_id)` is called
- **THEN** integer is returned as-is
- **AND** Qdrant accepts ID without errors

#### Scenario: Handle malformed IDs gracefully
- **GIVEN** point_id as invalid string "not-a-uuid"
- **WHEN** conversion is attempted
- **THEN** ValueError is raised: "Invalid point_id format: 'not-a-uuid'. Expected UUID string or integer."
- **AND** original value is included in error for debugging

### Requirement: Consolidated Upload Utilities

The system SHALL replace scattered upload code in scripts/ and src/storage/ with unified utilities.

#### Scenario: Replace upload_utils.py with QdrantBatchUploader
- **GIVEN** existing `src/storage/upload_utils.py` with custom upload logic
- **WHEN** refactoring is complete
- **THEN** all upload logic is moved to `QdrantBatchUploader` class
- **AND** upload_utils.py contains only backward-compatible wrappers
- **AND** deprecation warnings guide users to new API

#### Scenario: Migrate scripts/process_qdrant_ecosystem.py
- **GIVEN** script with inline upload code (100+ lines)
- **WHEN** refactored to use QdrantBatchUploader
- **THEN** script reduces to <20 lines of config + uploader calls
- **AND** functionality is identical
- **AND** performance improves by 20% due to optimized batching

### Requirement: Standardized Error Handling

The system SHALL implement consistent error handling patterns across all Qdrant operations.

#### Scenario: Network timeout during search
- **GIVEN** Qdrant server is unresponsive
- **WHEN** `store.search()` is called with timeout=5s
- **THEN** custom QdrantTimeoutError is raised after 5s
- **AND** error includes collection name, query details, and server URL
- **AND** caller can catch specific exception type

#### Scenario: Collection does not exist
- **GIVEN** search on non-existent collection "missing_collection"
- **WHEN** search is attempted
- **THEN** QdrantCollectionNotFoundError is raised
- **AND** error message suggests: "Collection 'missing_collection' not found. Available collections: ['agent_kit', 'qdrant_ecosystem', 'inngest_overall']"
- **AND** helpful documentation link is included

#### Scenario: Invalid vector dimension
- **GIVEN** collection expects 3584-dim vectors
- **WHEN** search with 768-dim vector is attempted
- **THEN** QdrantVectorDimensionError is raised
- **AND** error states: "Expected vector dimension 3584, got 768 for collection 'qdrant_ecosystem'"

## MODIFIED Requirements

### Requirement: QdrantStore Constructor (from src/storage/qdrant_store.py)

The `QdrantStore` class SHALL use QdrantRegistry for client management instead of creating direct clients.

#### Scenario: Create QdrantStore with registry
- **GIVEN** QdrantCollectionConfig for qdrant_ecosystem
- **WHEN** `QdrantStore(config)` is instantiated
- **THEN** store retrieves client from `QdrantRegistry.get_or_create_client(config)`
- **AND** client is reused across multiple QdrantStore instances
- **AND** no duplicate connections are created

#### Scenario: Backward compatibility with direct client
- **GIVEN** existing code creates QdrantStore with client=QdrantClient(...)
- **WHEN** store is instantiated with explicit client parameter
- **THEN** store uses provided client without registry
- **AND** deprecation warning is logged: "Passing client directly is deprecated, use config-based initialization"

### Requirement: Upload Scripts (scripts/process_qdrant_ecosystem.py, src/storage/upload_utils.py)

All upload scripts SHALL migrate to QdrantBatchUploader and QdrantCollectionConfig.

#### Scenario: Refactor process_qdrant_ecosystem.py
- **GIVEN** script with 200+ lines of custom upload logic
- **WHEN** refactored to use new abstractions
- **THEN** script structure is:
  1. Load config: `config = QdrantCollectionConfig.from_env()`
  2. Load embeddings: `embeddings = load_embeddings_from_directory(path)`
  3. Upload: `QdrantBatchUploader.upload_from_iterable(client, config, embeddings)`
- **AND** total script length is <50 lines
- **AND** upload performance is ≥250 qps

#### Scenario: Deprecate upload_utils.py functions
- **GIVEN** existing `stream_embeddings_to_qdrant()` function
- **WHEN** called
- **THEN** function logs deprecation warning: "stream_embeddings_to_qdrant is deprecated, use QdrantBatchUploader.upload_from_file"
- **AND** internally delegates to QdrantBatchUploader
- **AND** maintains identical API for 2 minor versions

### Requirement: Collection Manager (src/storage/collection_manager.py)

The `CollectionManager` class SHALL use unified config and registry patterns.

#### Scenario: Create collection via manager
- **GIVEN** CollectionManager initialized with QdrantRegistry
- **WHEN** `manager.create_collection(config)` is called
- **THEN** manager retrieves client from registry
- **AND** creates collection with config.vector, config.index, config.optimization settings
- **AND** applies indexed_fields from config
- **AND** logs success with collection stats

#### Scenario: List all collections
- **GIVEN** registry has clients for 3 collections
- **WHEN** `manager.list_collections()` is called
- **THEN** all collection names are returned: ["agent_kit", "qdrant_ecosystem", "inngest_overall"]
- **AND** stats are fetched for each: {name, vectors_count, indexed_fields_count, memory_usage}

## REMOVED Requirements

### Requirement: Direct QdrantClient Instantiation in Scripts

Scripts SHALL NOT create QdrantClient instances directly, instead using QdrantRegistry.

#### Scenario: Remove direct client creation
- **GIVEN** script with `client = QdrantClient(host="localhost", port=6333)`
- **WHEN** refactoring is applied
- **THEN** client creation is replaced with `client = QdrantRegistry.get_or_create_client(config)`
- **AND** connection pooling is automatically enabled
- **AND** no functionality is lost

