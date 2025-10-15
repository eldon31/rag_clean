# qdrant-unified-config Specification

## Purpose
Create unified configuration abstractions for all Qdrant operations to eliminate code duplication, ensure consistency, and enable easy extension of Qdrant usage across the project.

## ADDED Requirements

### Requirement: Base Configuration Classes

The system SHALL provide hierarchical configuration classes that compose connection, vector, index, and optimization settings.

#### Scenario: Create base Qdrant configuration
- **GIVEN** user needs to configure Qdrant connection
- **WHEN** `QdrantBaseConfig` is instantiated with url="http://localhost:6333", vector_size=3584, distance="Cosine"
- **THEN** configuration object validates all parameters
- **AND** provides typed access to connection, vector, index, and optimization sub-configs
- **AND** applies sensible defaults (timeout=60, hnsw_m=16, enable_quantization=True)

#### Scenario: Override specific settings
- **GIVEN** base config has default batch_size=256
- **WHEN** user creates config with batch_size=512
- **THEN** custom value overrides default
- **AND** other defaults remain unchanged
- **AND** validation ensures batch_size is positive integer

#### Scenario: Environment variable support
- **GIVEN** environment has `QDRANT_URL=http://prod.qdrant:6333` and `QDRANT_API_KEY=secret123`
- **WHEN** `QdrantBaseConfig.from_env()` is called
- **THEN** config loads values from environment variables
- **AND** falls back to defaults for unset variables
- **AND** type conversion is applied (strings to ints where needed)

### Requirement: Collection-Specific Configuration

The system SHALL provide `QdrantCollectionConfig` that extends base config with collection-specific settings.

#### Scenario: Configure collection with indexed fields
- **GIVEN** user wants to create `qdrant_ecosystem` collection
- **WHEN** `QdrantCollectionConfig` is created with collection_name="qdrant_ecosystem", indexed_fields=["subdirectory", "source_file", "source_path"]
- **THEN** config includes base settings plus collection-specific overrides
- **AND** indexed_fields are validated as list of strings
- **AND** collection_name is validated as non-empty string

#### Scenario: Detect vector dimension from data
- **GIVEN** embeddings file has mixed dimensions (some 768, some 3584)
- **WHEN** config auto-detection runs on first batch
- **THEN** system detects majority dimension (3584)
- **AND** config is updated with detected value
- **AND** warning is logged for mismatched records

### Requirement: Configuration Factory Pattern

The system SHALL provide factory methods for creating collection configs for common scenarios.

#### Scenario: Create config for code embeddings
- **GIVEN** user is working with nomic-embed-code embeddings
- **WHEN** `QdrantCollectionConfig.for_code_embeddings(collection_name="my_code")` is called
- **THEN** factory returns config with vector_size=3584, distance="Cosine"
- **AND** enables quantization for memory efficiency
- **AND** sets HNSW parameters optimized for code search (m=16, ef_construct=100)

#### Scenario: Create config for document embeddings
- **GIVEN** user is working with text-embedding-ada-002
- **WHEN** `QdrantCollectionConfig.for_document_embeddings(collection_name="my_docs")` is called
- **THEN** factory returns config with vector_size=1536, distance="Cosine"
- **AND** sets HNSW parameters optimized for document retrieval (m=32, ef_construct=200)

### Requirement: Configuration Validation

The system SHALL validate all configuration parameters and provide clear error messages for invalid values.

#### Scenario: Invalid vector dimension
- **GIVEN** user sets vector_size=0
- **WHEN** config validation runs
- **THEN** Pydantic ValidationError is raised
- **AND** error message states: "vector_size must be a positive integer"

#### Scenario: Invalid distance metric
- **GIVEN** user sets distance="Manhattan" (unsupported)
- **WHEN** config validation runs
- **THEN** ValidationError is raised with allowed values: "Cosine", "Euclidean", "Dot"

#### Scenario: Invalid HNSW parameters
- **GIVEN** user sets hnsw_m=0 or hnsw_ef_construct<hnsw_m
- **WHEN** custom validator runs
- **THEN** ValidationError is raised
- **AND** error explains: "hnsw_ef_construct must be >= hnsw_m and hnsw_m must be > 0"

### Requirement: Configuration Serialization

The system SHALL support JSON serialization/deserialization of configurations for persistence and debugging.

#### Scenario: Serialize config to JSON
- **GIVEN** QdrantCollectionConfig instance with all settings
- **WHEN** `config.model_dump_json()` is called
- **THEN** JSON string is returned with all configuration fields
- **AND** nested objects (connection, vector, index) are properly serialized
- **AND** Pydantic enums are converted to string values

#### Scenario: Deserialize config from JSON
- **GIVEN** JSON string from previous serialization
- **WHEN** `QdrantCollectionConfig.model_validate_json(json_str)` is called
- **THEN** config object is reconstructed with identical values
- **AND** validation is performed during deserialization
- **AND** TypeError is raised if JSON structure is invalid

## MODIFIED Requirements

### Requirement: QdrantStore Initialization (from existing src/storage/qdrant_store.py)

The `QdrantStore` class SHALL accept `QdrantCollectionConfig` instead of old `QdrantStoreConfig`.

#### Scenario: Create QdrantStore with new config
- **GIVEN** unified `QdrantCollectionConfig` instance
- **WHEN** `QdrantStore(config)` is instantiated
- **THEN** store extracts connection settings from config.connection
- **AND** extracts vector settings from config.vector
- **AND** extracts index settings from config.index
- **AND** applies quantization from config.optimization
- **AND** backward compatibility is maintained via deprecation wrapper

#### Scenario: Deprecation warning for old config
- **GIVEN** user passes old `QdrantStoreConfig` instance
- **WHEN** QdrantStore initialization runs
- **THEN** deprecation warning is logged: "QdrantStoreConfig is deprecated, use QdrantCollectionConfig"
- **AND** automatic migration to new config occurs
- **AND** functionality remains identical

### Requirement: Upload Utilities Configuration (from src/storage/upload_utils.py)

Upload utilities SHALL use `QdrantCollectionConfig` for all operations.

#### Scenario: Upload with unified config
- **GIVEN** upload script uses `QdrantCollectionConfig.from_env()`
- **WHEN** `stream_embeddings_to_qdrant(client, config)` is called
- **THEN** batch_size is read from config.optimization.batch_size
- **AND** indexed_fields are read from config.indexed_fields
- **AND** vector_dim is read from config.vector.size
- **AND** no hardcoded values are used

