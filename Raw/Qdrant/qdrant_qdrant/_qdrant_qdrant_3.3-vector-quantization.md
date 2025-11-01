Vector Quantization | qdrant/qdrant | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant](https://github.com/qdrant/qdrant "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 4 October 2025 ([48203e](https://github.com/qdrant/qdrant/commits/48203e41))

- [Introduction to Qdrant](qdrant/qdrant/1-introduction-to-qdrant.md)
- [Key Concepts and Terminology](qdrant/qdrant/1.1-key-concepts-and-terminology.md)
- [System Architecture](qdrant/qdrant/2-system-architecture.md)
- [Application Initialization and Runtime](qdrant/qdrant/2.1-application-initialization-and-runtime.md)
- [Collections and Table of Content](qdrant/qdrant/2.2-collections-and-table-of-content.md)
- [Shards and Replica Sets](qdrant/qdrant/2.3-shards-and-replica-sets.md)
- [Local Shard Architecture](qdrant/qdrant/2.4-local-shard-architecture.md)
- [Segment Lifecycle and Construction](qdrant/qdrant/2.5-segment-lifecycle-and-construction.md)
- [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md)
- [Vector Storage Formats](qdrant/qdrant/3.1-vector-storage-formats.md)
- [HNSW Index Implementation](qdrant/qdrant/3.2-hnsw-index-implementation.md)
- [Vector Quantization](qdrant/qdrant/3.3-vector-quantization.md)
- [Sparse Vector Indexing](qdrant/qdrant/3.4-sparse-vector-indexing.md)
- [Payload Indexing and Filtering](qdrant/qdrant/4-payload-indexing-and-filtering.md)
- [Field Index Types](qdrant/qdrant/4.1-field-index-types.md)
- [Index Selection and Storage Backends](qdrant/qdrant/4.2-index-selection-and-storage-backends.md)
- [Search and Query Processing](qdrant/qdrant/5-search-and-query-processing.md)
- [Query Request Flow](qdrant/qdrant/5.1-query-request-flow.md)
- [Filtering and Scoring](qdrant/qdrant/5.2-filtering-and-scoring.md)
- [Data Updates and Consistency](qdrant/qdrant/6-data-updates-and-consistency.md)
- [Update Processing Pipeline](qdrant/qdrant/6.1-update-processing-pipeline.md)
- [Write Consistency and Replication](qdrant/qdrant/6.2-write-consistency-and-replication.md)
- [Distributed System Features](qdrant/qdrant/7-distributed-system-features.md)
- [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md)
- [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md)
- [Snapshots and Recovery](qdrant/qdrant/8-snapshots-and-recovery.md)
- [API Reference](qdrant/qdrant/9-api-reference.md)
- [REST API Endpoints](qdrant/qdrant/9.1-rest-api-endpoints.md)
- [gRPC API Services](qdrant/qdrant/9.2-grpc-api-services.md)
- [Data Types and Conversions](qdrant/qdrant/9.3-data-types-and-conversions.md)
- [Configuration and Deployment](qdrant/qdrant/10-configuration-and-deployment.md)
- [Configuration System](qdrant/qdrant/10.1-configuration-system.md)
- [Docker Deployment](qdrant/qdrant/10.2-docker-deployment.md)
- [Building and CI/CD](qdrant/qdrant/10.3-building-and-cicd.md)
- [Development Guide](qdrant/qdrant/11-development-guide.md)

Menu

# Vector Quantization

Relevant source files

- [Cargo.lock](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.lock)
- [Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml)
- [docs/redoc/default\_version.js](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/default_version.js)
- [docs/redoc/index.html](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/index.html)
- [docs/redoc/v0.10.3/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.3/openapi.json)
- [docs/redoc/v0.10.4/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.4/openapi.json)
- [docs/redoc/v0.10.5/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.5/openapi.json)
- [docs/redoc/v1.10.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.10.x/openapi.json)
- [docs/redoc/v1.11.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.11.x/openapi.json)
- [docs/redoc/v1.13.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.13.x/openapi.json)
- [docs/redoc/v1.15.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.15.x/openapi.json)
- [lib/api/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/Cargo.toml)
- [lib/collection/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml)
- [lib/common/common/src/defaults.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs)
- [lib/common/dataset/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/dataset/Cargo.toml)
- [lib/common/io/src/file\_operations.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/io/src/file_operations.rs)
- [lib/common/issues/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/issues/Cargo.toml)
- [lib/segment/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml)
- [lib/segment/benches/hnsw\_build\_asymptotic.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_build_asymptotic.rs)
- [lib/segment/benches/hnsw\_build\_graph.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_build_graph.rs)
- [lib/segment/benches/hnsw\_search\_graph.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_search_graph.rs)
- [lib/segment/src/index/hnsw\_index/graph\_layers.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs)
- [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/header.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/header.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/serializer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/serializer.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/view.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs)
- [lib/segment/src/index/hnsw\_index/hnsw.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs)
- [lib/segment/src/index/hnsw\_index/tests/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/tests/mod.rs)
- [lib/segment/src/index/hnsw\_index/tests/test\_compact\_graph\_layer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/tests/test_compact_graph_layer.rs)
- [lib/sparse/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/Cargo.toml)
- [lib/storage/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml)
- [tools/missed\_cherry\_picks.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/missed_cherry_picks.sh)

Vector quantization in Qdrant provides memory optimization techniques that reduce the storage footprint of high-dimensional vectors while maintaining search accuracy. This system supports multiple quantization methods including scalar quantization, product quantization, and binary quantization, with both in-memory and memory-mapped storage options.

For information about vector indexing structures, see [HNSW Index Implementation](qdrant/qdrant/3.1-vector-storage-formats.md). For payload data indexing, see [Payload Indexing and Filtering](qdrant/qdrant/3.2-hnsw-index-implementation.md).

## Quantization Types and Storage Architecture

Qdrant implements three primary quantization methods through the `QuantizedVectorStorage` enum, each with distinct memory and accuracy trade-offs:

| Quantization Type     | Configuration               | Encoding            | Use Case                                   |
| --------------------- | --------------------------- | ------------------- | ------------------------------------------ |
| `ScalarQuantization`  | `ScalarQuantizationConfig`  | `EncodedVectorsU8`  | Uniform quantization to 8-bit integers     |
| `ProductQuantization` | `ProductQuantizationConfig` | `EncodedVectorsPQ`  | Subspace quantization with codebooks       |
| `BinaryQuantization`  | `BinaryQuantizationConfig`  | `EncodedVectorsBin` | Bit-level encoding for maximum compression |

```
```

**QuantizedVectorStorage Architecture with Configuration Details**

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs83-96](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L83-L96) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs59-81](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L59-L81) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs22-27](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L22-L27)

## Vector Storage Integration

The quantization system integrates with Qdrant's vector storage layer through the `VectorStorage` trait and `VectorStorageEnum`. The `QuantizedVectors` struct wraps `QuantizedVectorStorage` and implements the `RawScorer` interface. The system supports three vector element types with corresponding storage variants:

| Element Type            | Rust Type | Storage Variants                                          | Use Case                   |
| ----------------------- | --------- | --------------------------------------------------------- | -------------------------- |
| `VectorElementType`     | `f32`     | `DenseSimple`, `DenseMemmap`, `DenseVolatile`             | Standard precision vectors |
| `VectorElementTypeHalf` | `f16`     | `DenseSimpleHalf`, `DenseMemmapHalf`, `DenseVolatileHalf` | Memory-optimized vectors   |
| `VectorElementTypeByte` | `u8`      | `DenseSimpleByte`, `DenseMemmapByte`, `DenseVolatileByte` | Compact integer vectors    |

```
```

**QuantizedVectors Integration Architecture**

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs124-130](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L124-L130) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs45-49](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L45-L49) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs161-175](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L161-L175) [lib/segment/src/data\_types/vectors.rs212-216](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/data_types/vectors.rs#L212-L216) [lib/segment/src/vector\_storage/vector\_storage\_base.rs189-321](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L189-L321)

## Creation and Loading Process

Quantized vectors are created from existing `VectorStorageEnum` instances through a dispatch-based process that handles both single vectors and multi-vectors:

| Component                       | Purpose                                             | File Location                                                                                                 |
| ------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `QuantizedVectors::create()`    | Main entry point dispatching on VectorStorageEnum   | [quantized\_vectors.rs286-390](https://github.com/qdrant/qdrant/blob/48203e41/quantized_vectors.rs#L286-L390) |
| `create_impl()`                 | Implementation for DenseVectorStorage types         | [quantized\_vectors.rs392-467](https://github.com/qdrant/qdrant/blob/48203e41/quantized_vectors.rs#L392-L467) |
| `create_multi_impl()`           | Implementation for MultiVectorStorage types         | [quantized\_vectors.rs469-559](https://github.com/qdrant/qdrant/blob/48203e41/quantized_vectors.rs#L469-L559) |
| `construct_vector_parameters()` | Builds vector\_parameters from distance, dim, count | [quantized\_vectors.rs721-730](https://github.com/qdrant/qdrant/blob/48203e41/quantized_vectors.rs#L721-L730) |

```
```

**QuantizedVectors::create() Flow with Preprocessing Details**

The `quantization_preprocess()` method performs vector preprocessing based on the quantization type and distance metric, handling different vector element types (`f32`, `f16`, `u8`) and applying distance-specific transformations before encoding.

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs286-390](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L286-L390) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs40-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L40-L43) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs392-467](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L392-L467) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs406-412](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L406-L412) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs721-730](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L721-L730)

## Storage File Structure

Quantized vectors persist to disk using a standardized file structure with constants defined in `quantized_vectors.rs`:

| File                     | Purpose                                   | Constant                 | Required For                   |
| ------------------------ | ----------------------------------------- | ------------------------ | ------------------------------ |
| `quantized.config.json`  | QuantizedVectorsConfig serialization      | `QUANTIZED_CONFIG_PATH`  | All quantized vectors          |
| `quantized.data`         | EncodedVectors binary data                | `QUANTIZED_DATA_PATH`    | All quantized vectors          |
| `quantized.meta.json`    | EncodedVectors metadata                   | `QUANTIZED_META_PATH`    | All quantized vectors          |
| `quantized.offsets.data` | MultivectorOffset array for multi-vectors | `QUANTIZED_OFFSETS_PATH` | Multi-vector quantization only |

```
```

**Quantized Vector File Management**

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs40-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L40-L43) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs263-276](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L263-L276) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs565-640](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L565-L640)

## Query Processing and Scoring

The quantization system provides optimized query processing through the `raw_scorer()` and `raw_internal_scorer()` methods that create specialized scorers operating on quantized data:

```
```

**QuantizedVectors RawScorer Interface**

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs161-175](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L161-L175) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs177-228](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L177-L228) [lib/segment/src/vector\_storage/raw\_scorer.rs31-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/raw_scorer.rs#L31-L43)

## Memory Management Strategies

Quantization supports both in-memory and memory-mapped storage determined by the `is_ram()` function and `VectorStorage::is_on_disk()` method:

| Storage Variant                | Condition                     | Backend Implementation               |
| ------------------------------ | ----------------------------- | ------------------------------------ |
| ScalarRam, PQRam, BinaryRam    | `is_ram() == true`            | `ChunkedVectors<T>`                  |
| ScalarMmap, PQMmap, BinaryMmap | `is_ram() == false`           | `QuantizedMmapStorage`               |
| Multi variants                 | Same logic as single variants | Includes `MultivectorOffsetsStorage` |

The `is_ram()` function determines storage type based on quantization configuration and source vector storage:

```
```

Each quantization configuration includes an `always_ram` field that explicitly controls storage type, overriding the default behavior based on the source vector storage's `is_on_disk()` property.

```
```

**Quantization Storage Selection Logic**

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs732-734](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L732-L734) [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs580-622](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L580-L622) [lib/segment/src/vector\_storage/vector\_storage\_base.rs48](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L48-L48)

## Multi-Vector Quantization

For multi-vector configurations, quantization includes additional offset tracking to maintain vector boundaries:

```
```

**Multi-Vector Quantization Structure**

Sources: [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs434-452](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs#L434-L452) [lib/segment/src/vector\_storage/quantized/quantized\_multivector\_storage.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_multivector_storage.rs)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Vector Quantization](#vector-quantization.md)
- [Quantization Types and Storage Architecture](#quantization-types-and-storage-architecture.md)
- [Vector Storage Integration](#vector-storage-integration.md)
- [Creation and Loading Process](#creation-and-loading-process.md)
- [Storage File Structure](#storage-file-structure.md)
- [Query Processing and Scoring](#query-processing-and-scoring.md)
- [Memory Management Strategies](#memory-management-strategies.md)
- [Multi-Vector Quantization](#multi-vector-quantization.md)
