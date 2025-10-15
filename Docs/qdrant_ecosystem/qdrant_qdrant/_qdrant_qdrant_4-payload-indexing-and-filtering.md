Payload Indexing and Filtering | qdrant/qdrant | DeepWiki

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

# Payload Indexing and Filtering

Relevant source files

- [lib/segment/src/index/field\_index/field\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs)
- [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs)
- [lib/segment/src/index/field\_index/index\_selector.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs)
- [lib/segment/src/index/plain\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs)
- [lib/segment/src/index/struct\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs)
- [lib/segment/src/index/vector\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/vector_index_base.rs)

## Purpose and Scope

This document explains Qdrant's payload indexing and filtering system, which enables efficient filtering of vector search results based on structured metadata (JSON payloads) attached to points. Payload indices accelerate filter evaluation by building specialized data structures for different field types, allowing queries to skip vector similarity computation for points that don't match filter criteria.

For information about vector indexing (HNSW, quantization), see [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md). For the complete search flow including filter application during vector search, see [Search and Query Processing](qdrant/qdrant/5-search-and-query-processing.md).

## Core Components and Architecture

Qdrant implements two payload index strategies at the segment level:

- **`StructPayloadIndex`**: Full-featured implementation that builds and maintains field-specific indices for accelerated filtering
- **`PlainPayloadIndex`**: Minimal implementation that performs full scans without indices, used for small segments where index overhead outweighs benefits

Both implement the `PayloadIndex` trait, which defines the interface for filter evaluation, cardinality estimation, and index management.

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs78-98](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L78-L98) [lib/segment/src/index/plain\_payload\_index.rs27-32](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs#L27-L32)

### StructPayloadIndex Implementation

The `StructPayloadIndex` struct maintains multiple field-specific indices organized by field path. Key components:

| Component         | Type                                     | Purpose                                     |
| ----------------- | ---------------------------------------- | ------------------------------------------- |
| `payload`         | `Arc<AtomicRefCell<PayloadStorageEnum>>` | Stores raw JSON payloads                    |
| `id_tracker`      | `Arc<AtomicRefCell<IdTrackerSS>>`        | Tracks point existence and internal IDs     |
| `vector_storages` | `HashMap<VectorNameBuf, Arc<...>>`       | For `has_vector` condition evaluation       |
| `field_indexes`   | `IndexesMap`                             | Maps field paths to index implementations   |
| `config`          | `PayloadConfig`                          | Persisted index configuration               |
| `storage_type`    | `StorageType`                            | Determines backend (RocksDB/Mmap/Gridstore) |

The `field_indexes` map uses `JsonPath` as keys, allowing nested field indexing. Each field can have multiple indices (e.g., integer fields may have both range and lookup indices).

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs79-98](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L79-L98)

## Field Index Types

Each field type requires specialized data structures for efficient filtering. Qdrant provides nine index types, wrapped in the `FieldIndex` enum.

```
```

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs131-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L131-L143)

### Numeric Indices

Numeric indices (`NumericIndex<T, P>`) support range queries using a mutable interval tree structure. They handle:

- **Integer fields**: Range queries, comparisons (`<`, `>`, `<=`, `>=`, `=`)
- **Float fields**: Same operations with floating-point values
- **Datetime fields**: Stored as integer timestamps, enabling range-based temporal queries

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs132-140](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L132-L140)

### Map Indices (Hash-Based)

Map indices (`MapIndex<K>`) provide O(1) exact-match lookups using hash maps:

- **KeywordIndex**: String exact matching for tags, categories
- **IntMapIndex**: Integer exact matching with faceting support
- **UuidMapIndex**: UUID exact matching

These indices also support the facet API for aggregation queries.

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs134-141](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L134-L141)

### Full-Text Index

The `FullTextIndex` implements tokenized text search with configurable tokenization:

```
```

Text queries are parsed into three types:

- **AllTokens**: Match documents containing all query tokens (AND logic)
- **Phrase**: Match documents with tokens in exact order
- **AnyTokens**: Match documents containing any query token (OR logic)

**Sources:** [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs37-322](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs#L37-L322)

### Geo, Bool, and Null Indices

- **GeoIndex**: Spatial index supporting radius and bounding box queries
- **BoolIndex**: Bitmap-based index for true/false values
- **NullIndex**: Tracks which points have null/missing values for a field

The `NullIndex` complements every other index type, enabling efficient "field exists" queries.

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs137-142](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L137-L142) [lib/segment/src/index/struct\_payload\_index.rs202-209](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L202-L209)

## Storage Backends and Index Selection

Qdrant supports three storage backends for payload indices, selected via the `IndexSelector` abstraction.

### Storage Backend Types

| Backend              | Use Case           | Appendable | Description                                   |
| -------------------- | ------------------ | ---------- | --------------------------------------------- |
| **RocksDB** (legacy) | Historical         | Yes/No     | Embedded key-value store, being migrated away |
| **Gridstore**        | Mutable segments   | Yes        | Custom blob storage for in-memory indices     |
| **Mmap**             | Immutable segments | No         | Memory-mapped files, supports on-disk mode    |

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs46-75](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L46-L75) [lib/segment/src/index/field\_index/index\_selector.rs31-58](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L31-L58)

### Index Selection Strategy

The `IndexSelector` enum encapsulates storage backend selection logic:

```
```

Selection is based on:

1. **Segment mutability**: Appendable segments prefer Gridstore/RocksDB
2. **Configuration flags**: `skip_rocksdb` forces non-RocksDB backends
3. **Field schema**: `is_on_disk` flag influences Mmap usage
4. **Migration state**: Active migration from RocksDB to Gridstore

**Sources:** [lib/segment/src/index/field\_index/index\_selector.rs31-148](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L31-L148)

### RocksDB Migration

Qdrant is actively migrating away from RocksDB indices. When the `migrate_rocksdb_payload_indices` feature flag is enabled:

1. Existing RocksDB indices are detected during load ([line 251-256](<https://github.com/qdrant/qdrant/blob/48203e41/line 251-256>))
2. All RocksDB indices are cleaned up ([line 274-280](<https://github.com/qdrant/qdrant/blob/48203e41/line 274-280>))
3. Storage type is changed to Gridstore ([line 261-270](<https://github.com/qdrant/qdrant/blob/48203e41/line 261-270>))
4. Indices are rebuilt using the new backend ([line 284-294](<https://github.com/qdrant/qdrant/blob/48203e41/line 284-294>))

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs248-281](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L248-L281)

## Filter Evaluation and Cardinality Estimation

Filter evaluation in Qdrant follows a two-phase approach: **cardinality estimation** followed by **point iteration**.

### Cardinality Estimation

Before executing a filter, `StructPayloadIndex` estimates how many points match using `estimate_cardinality()`:

```
```

The `CardinalityEstimation` struct contains:

- **primary\_clauses**: Conditions that can use index iterators directly
- **min/exp/max**: Cardinality bounds for query planning

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs507-942](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L507-L942)

### Primary Clauses and Filter Optimization

Primary clauses are filter conditions that can be evaluated entirely by index iteration, avoiding payload access:

| Clause Type                   | When Used           | Example                               |
| ----------------------------- | ------------------- | ------------------------------------- |
| `PrimaryCondition::Condition` | Field has index     | `age > 25` with indexed integer field |
| `PrimaryCondition::Ids`       | Has ID filter       | `id in [1, 2, 3]`                     |
| `PrimaryCondition::HasVector` | Vector exists check | `has_vector("image")`                 |

The optimizer selects primary clauses during estimation ([line 635-639](<https://github.com/qdrant/qdrant/blob/48203e41/line 635-639>)), enabling efficient iteration strategies.

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs614-680](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L614-L680)

### Filter Execution Strategies

`iter_filtered_points()` implements three strategies based on primary clauses:

```
```

**Strategy A (Full Scan)**: No primary clauses available. Iterate all points, apply full filter.

**Strategy B (Primary Only)**: All conditions are primary. Iterate index results, deduplicate with visited pool.

**Strategy C (Primary + Filter)**: Some conditions primary. Iterate index results, deduplicate, then apply remaining filter conditions.

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs614-680](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L614-L680)

### StructFilterContext

The `StructFilterContext` wraps an optimized filter for efficient point-by-point checking:

```
```

This context is used during vector search to check individual points against filter conditions.

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs490-505](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L490-L505)

## Index Building and Lifecycle

### Index Creation Flow

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs447-883](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L447-L883)

### Builder Pattern

Each index type implements `FieldIndexBuilderTrait`:

```
```

The builder pattern enables:

- **Batch construction**: All points added before finalization
- **Backend-specific initialization**: Different setup for RocksDB vs Mmap
- **Immutable result**: `finalize()` consumes builder, returns immutable index

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs537-563](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L537-L563)

### Index Updates and Maintenance

For mutable segments, indices support incremental updates:

```
```

The `add_point()` method internally calls `remove_point()` first to handle value changes correctly.

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs274-331](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L274-L331)

### Index Persistence

Index configuration is persisted in `PayloadConfig`:

```
```

Each indexed field stores:

- **schema**: Field type and indexing parameters
- **types**: Exact index implementation types (for reload)

This allows loading indices with the correct backend on segment reopening.

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs141-172](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L141-L172)

## Index Cleanup and Memory Management

### Cleanup Operations

Indices can be explicitly cleaned up via:

```
```

Each `FieldIndex` variant implements cleanup to remove:

- RocksDB column families
- Mmap files
- Gridstore blobs

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs885-900](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L885-L900)

### Cache Management

For memory-mapped indices, Qdrant provides cache control operations:

- **`populate()`**: Eagerly load all mmap pages into RAM
- **`clear_cache()`**: Drop OS page cache for mmap files

These operations are exposed on both `FieldIndex` and `StructPayloadIndex`:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs779-806](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L779-L806) [lib/segment/src/index/field\_index/field\_index\_base.rs448-479](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L448-L479)

## Integration with Search Pipeline

During vector search, payload filtering occurs in two places:

1. **Pre-filtering**: `estimate_cardinality()` + `iter_filtered_points()` narrows candidates before vector computation
2. **Post-filtering**: `filter_context().check(id)` verifies individual points during result collection

The search flow (from Diagram 3) shows this integration:

```
```

**Sources:** Referenced in high-level Diagram 3 from system architecture

## PlainPayloadIndex for Small Segments

For segments below the indexing threshold, `PlainPayloadIndex` provides a simpler implementation:

| Feature                | StructPayloadIndex   | PlainPayloadIndex         |
| ---------------------- | -------------------- | ------------------------- |
| Index structures       | Yes, multiple types  | No indices                |
| Filter evaluation      | Index-accelerated    | Full scan                 |
| Cardinality estimation | Accurate via indices | Returns midpoint estimate |
| Memory overhead        | Per-field index data | Minimal                   |
| Update cost            | Index maintenance    | Negligible                |

`PlainPayloadIndex` always returns pessimistic cardinality estimates and relies on the `ConditionCheckerSS` for brute-force filtering.

**Sources:** [lib/segment/src/index/plain\_payload\_index.rs23-160](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs#L23-L160)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Payload Indexing and Filtering](#payload-indexing-and-filtering.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Core Components and Architecture](#core-components-and-architecture.md)
- [StructPayloadIndex Implementation](#structpayloadindex-implementation.md)
- [Field Index Types](#field-index-types.md)
- [Numeric Indices](#numeric-indices.md)
- [Map Indices (Hash-Based)](#map-indices-hash-based.md)
- [Full-Text Index](#full-text-index.md)
- [Geo, Bool, and Null Indices](#geo-bool-and-null-indices.md)
- [Storage Backends and Index Selection](#storage-backends-and-index-selection.md)
- [Storage Backend Types](#storage-backend-types.md)
- [Index Selection Strategy](#index-selection-strategy.md)
- [RocksDB Migration](#rocksdb-migration.md)
- [Filter Evaluation and Cardinality Estimation](#filter-evaluation-and-cardinality-estimation.md)
- [Cardinality Estimation](#cardinality-estimation.md)
- [Primary Clauses and Filter Optimization](#primary-clauses-and-filter-optimization.md)
- [Filter Execution Strategies](#filter-execution-strategies.md)
- [StructFilterContext](#structfiltercontext.md)
- [Index Building and Lifecycle](#index-building-and-lifecycle.md)
- [Index Creation Flow](#index-creation-flow.md)
- [Builder Pattern](#builder-pattern.md)
- [Index Updates and Maintenance](#index-updates-and-maintenance.md)
- [Index Persistence](#index-persistence.md)
- [Index Cleanup and Memory Management](#index-cleanup-and-memory-management.md)
- [Cleanup Operations](#cleanup-operations.md)
- [Cache Management](#cache-management.md)
- [Integration with Search Pipeline](#integration-with-search-pipeline.md)
- [PlainPayloadIndex for Small Segments](#plainpayloadindex-for-small-segments.md)
