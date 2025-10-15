# qdrant-optimization Specification

## Purpose
Optimize Qdrant performance through quantization, HNSW parameter tuning, connection pooling, and batch processing to achieve 75% memory reduction and <100ms p95 search latency while maintaining >0.95 recall.

## ADDED Requirements

### Requirement: Scalar Quantization for Memory Optimization

The system SHALL implement int8 scalar quantization for high-dimensional vectors to reduce memory usage by ~4x.

#### Scenario: Enable quantization for code embeddings (3584-dim)
- **GIVEN** qdrant_ecosystem collection with 1,344 documents × 3584-dim float32 vectors (≈19MB)
- **WHEN** scalar quantization is enabled with type=ScalarType.INT8, quantile=0.99
- **THEN** memory usage reduces to ≈5MB (4x reduction)
- **AND** original vectors are preserved in on-disk storage
- **AND** quantized vectors are used for initial search pass
- **AND** top-k candidates are re-scored with original vectors

#### Scenario: Maintain recall with quantization
- **GIVEN** collection with quantization enabled
- **WHEN** search is performed with limit=10, query_vector of 3584 dimensions
- **THEN** recall@10 is ≥0.95 compared to non-quantized search
- **AND** search latency is <100ms at p95
- **AND** quantization does not affect exact match scenarios

#### Scenario: Quantization configuration validation
- **GIVEN** user sets quantization type=ScalarType.INT4 (too aggressive for 3584-dim)
- **WHEN** config validation runs
- **THEN** warning is logged: "INT4 quantization may reduce recall for high-dim vectors, INT8 recommended"
- **AND** system allows override via always_ram=True
- **AND** documentation links are provided

### Requirement: HNSW Index Optimization

The system SHALL optimize HNSW parameters for code embeddings to balance indexing speed, search speed, and recall.

#### Scenario: Configure HNSW for code search workload
- **GIVEN** code embeddings collection with 1,000+ documents
- **WHEN** HNSW config is set to m=16, ef_construct=100, ef_search=64
- **THEN** indexing time is <1s per 100 documents
- **AND** search latency is <50ms at p50, <100ms at p95
- **AND** recall@10 is ≥0.98

#### Scenario: Auto-tune HNSW for collection size
- **GIVEN** collection grows from 1K to 10K documents
- **WHEN** auto-tuning is enabled with target_recall=0.95, target_latency_ms=100
- **THEN** system increases ef_construct to 200 for better graph quality
- **AND** ef_search is adjusted to maintain latency targets
- **AND** m remains at 16 (cannot change after collection creation)

#### Scenario: HNSW parameter validation
- **GIVEN** user sets m=64, ef_construct=50
- **WHEN** validation runs
- **THEN** ValidationError is raised: "ef_construct must be >= 2*m (got 50, need ≥128)"
- **AND** recommended values are suggested based on collection size

### Requirement: Connection Pooling with QdrantRegistry

The system SHALL implement connection pooling to reuse Qdrant clients and prevent connection exhaustion.

#### Scenario: Reuse connection for same collection
- **GIVEN** multiple operations on qdrant_ecosystem collection
- **WHEN** `QdrantRegistry.get_client(collection_config)` is called 3 times
- **THEN** same client instance is returned for all 3 calls
- **AND** connection count remains 1
- **AND** client is keyed by (url, api_key, collection_name) tuple

#### Scenario: Separate connections for different collections
- **GIVEN** operations on agent_kit and qdrant_ecosystem collections
- **WHEN** registry retrieves clients for both
- **THEN** two separate client instances are created
- **AND** each client is cached independently
- **AND** connection pool limit (default 10) is not exceeded

#### Scenario: Connection pool cleanup
- **GIVEN** 5 idle connections older than 300 seconds
- **WHEN** `QdrantRegistry.cleanup_idle_connections(max_age_seconds=300)` is called
- **THEN** idle connections are closed and removed from pool
- **AND** active connections are preserved
- **AND** memory is freed

### Requirement: Batch Upload Optimization

The system SHALL optimize batch upload throughput to achieve >250 queries per second (qps) for large collections.

#### Scenario: Batch upload with optimal batch size
- **GIVEN** 10,000 embeddings to upload with 3584-dim vectors
- **WHEN** `QdrantBatchUploader` uploads with batch_size=256, parallel_workers=4
- **THEN** upload completes in <40 seconds (≥250 qps)
- **AND** no duplicate point_id errors occur
- **AND** memory usage stays below 2GB during upload

#### Scenario: Auto-adjust batch size on memory pressure
- **GIVEN** upload with batch_size=512 causes OOM warnings
- **WHEN** memory threshold (80% of available) is exceeded
- **THEN** batch_size is reduced to 256
- **AND** upload continues without interruption
- **AND** warning is logged with adjustment details

#### Scenario: Retry failed batches with exponential backoff
- **GIVEN** network error during batch upload (connection timeout)
- **WHEN** error is detected
- **THEN** batch is retried with exponential backoff (1s, 2s, 4s, 8s, max 5 retries)
- **AND** successful retries continue upload
- **AND** permanent failures are logged with batch details

### Requirement: Search Performance Monitoring

The system SHALL expose performance metrics for monitoring and optimization feedback.

#### Scenario: Track search latency percentiles
- **GIVEN** 1,000 search queries executed
- **WHEN** metrics are aggregated
- **THEN** p50, p95, p99 latencies are calculated
- **AND** results are logged: "Search latency - p50: 35ms, p95: 82ms, p99: 145ms"
- **AND** violations of SLA (<100ms p95) trigger alerts

#### Scenario: Monitor quantization recall impact
- **GIVEN** quantization enabled on collection
- **WHEN** 100 test queries are executed with known ground truth
- **THEN** recall@10 is calculated as (correct_in_top10 / total_queries)
- **AND** result is logged: "Quantization recall@10: 0.967"
- **AND** degradation below 0.95 triggers recommendation to disable quantization

#### Scenario: Track memory usage per collection
- **GIVEN** 3 collections: qdrant_ecosystem, agent_kit, inngest_overall
- **WHEN** `QdrantRegistry.get_collection_stats()` is called
- **THEN** memory usage breakdown is returned: {"qdrant_ecosystem": 5.2MB, "agent_kit": 12.4MB, ...}
- **AND** quantization savings are calculated: {"qdrant_ecosystem": "4x reduction"}

## MODIFIED Requirements

### Requirement: QdrantStore Search Method (from src/storage/qdrant_store.py)

The `QdrantStore.search()` method SHALL support quantization-aware search and performance tracking.

#### Scenario: Search with quantization rescoring
- **GIVEN** collection with quantization enabled
- **WHEN** `store.search(query_vector, limit=10, rescore=True)` is called
- **THEN** initial search uses quantized vectors
- **AND** top-k * oversample_ratio (default 3x) candidates are retrieved
- **AND** candidates are re-scored with original vectors
- **AND** final top-k results are returned

#### Scenario: Track search performance metrics
- **GIVEN** search operation completes
- **WHEN** metrics are recorded
- **THEN** latency is logged with collection name and limit
- **AND** quantization usage is recorded (quantized: true/false)
- **AND** metrics are exportable to monitoring systems (Prometheus format)

### Requirement: Collection Creation (from src/storage/qdrant_store.py)

Collection creation SHALL apply optimized HNSW and quantization settings from config.

#### Scenario: Create collection with optimizations
- **GIVEN** QdrantCollectionConfig with quantization=True, hnsw_m=16, hnsw_ef_construct=100
- **WHEN** `store.create_collection()` is called
- **THEN** collection is created with HNSW config (m=16, ef_construct=100)
- **AND** scalar quantization is configured (type=INT8, quantile=0.99)
- **AND** indexed fields from config are created
- **AND** success is logged with optimization summary

