Vector Storage Formats | qdrant/qdrant | DeepWiki

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

# Vector Storage Formats

Relevant source files

- [lib/segment/src/entry/entry\_point.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/entry/entry_point.rs)
- [lib/segment/src/fixtures/index\_fixtures.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/fixtures/index_fixtures.rs)
- [lib/segment/src/segment\_constructor/segment\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs)
- [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs)
- [lib/segment/src/vector\_storage/vector\_storage\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs)

## Purpose and Scope

This document describes the different vector storage formats available in Qdrant for storing dense, sparse, and multi-dense vectors. It covers the `VectorStorageEnum` variants, their underlying storage backends, supported data types, and the mechanisms for creating and selecting appropriate storage formats.

For information about vector indexing structures built on top of these storage formats, see [HNSW Index Implementation](qdrant/qdrant/3.2-hnsw-index-implementation.md) and [Sparse Vector Indexing](qdrant/qdrant/3.4-sparse-vector-indexing.md). For details on how vectors are quantized to reduce memory usage, see [Vector Quantization](qdrant/qdrant/3.3-vector-quantization.md).

## Vector Storage Architecture

Vector storage in Qdrant is abstracted through the `VectorStorage` trait and implemented via the `VectorStorageEnum`, which provides multiple storage backends optimized for different use cases. Each segment maintains a collection of vector storages (one per vector name) that handle the persistence and retrieval of raw vector data.

**Storage Classification**

```
```

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs217-349](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L217-L349)

## Dense Vector Storage Formats

Dense vector storage handles fixed-dimension vectors where all elements are present. Each storage format is available in three data type variants: `Float32` (default), `Uint8`, and `Float16`.

### Storage Type Comparison

| Storage Type            | Appendable | On-Disk | Memory Usage | Use Case                     |
| ----------------------- | ---------- | ------- | ------------ | ---------------------------- |
| `DenseSimple` (RocksDB) | Yes        | No      | Low          | Legacy, being migrated away  |
| `DenseVolatile`         | Yes        | No      | High         | Testing only                 |
| `DenseMemmap`           | No         | Yes     | Low          | Optimized read-only segments |
| `DenseAppendableMemmap` | Yes        | Yes     | Low          | Mutable segments (default)   |
| `DenseAppendableInRam`  | Yes        | No      | Medium       | Fast access with persistence |

### DenseSimple (RocksDB-based)

RocksDB-based storage that persists vectors in a key-value database. This format is being actively migrated to memory-mapped formats for better performance.

```
```

**Key Implementation:**

- Created via `open_simple_dense_vector_storage()` when `VectorStorageType::Memory` is configured
- Uses a dedicated RocksDB column family named with `DB_VECTOR_CF` prefix
- Supports migration to mmap format via `migrate_rocksdb_dense_vector_storage_to_mmap()`

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs116-142](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L116-L142) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs1047-1126](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L1047-L1126)

### DenseMemmap (Immutable Memory-Mapped)

Immutable memory-mapped storage that provides low memory usage for read-only segments. Vectors are stored in a single contiguous file mapped into memory.

**File Structure:**

- Vector data stored as raw bytes in a single memory-mapped file
- No fragmentation, optimal for sequential reads
- Supports `populate()` to prefetch data into page cache

**Creation Path:**

```
```

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs144-172](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L144-L172)

### DenseAppendableMemmap (Chunked Memory-Mapped)

Chunked memory-mapped storage that supports both reads and writes. Vectors are stored across multiple memory-mapped chunks, allowing the storage to grow dynamically.

**Architecture:**

- Uses `ChunkedMmapVectors<T>` backend for storing vectors in chunks
- Supports dynamic growth by adding new chunks
- Default storage type for mutable segments

**Chunk Management:**

```
```

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs175-203](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L175-L203)

### DenseAppendableInRam (In-Memory Persisted)

In-memory storage that maintains vectors in RAM while persisting to disk. Provides fast access with durability guarantees.

**Characteristics:**

- Uses `InRamPersistedVectors<T>` backend
- All vectors kept in memory for fast access
- Periodic flush to disk for persistence
- Lower memory pressure than `ChunkedMmapVectors` as data stays in RAM

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs204-221](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L204-L221)

## Sparse Vector Storage Formats

Sparse vectors store only non-zero indices and values, making them efficient for high-dimensional sparse data like TF-IDF or BM25 vectors.

### Sparse Storage Types

| Storage Type     | Backend   | On-Disk | Use Case             |
| ---------------- | --------- | ------- | -------------------- |
| `SparseSimple`   | RocksDB   | No      | Legacy format        |
| `SparseVolatile` | In-Memory | No      | Testing              |
| `SparseMmap`     | Mmap      | Yes     | Production (default) |

### SparseMmap Storage

Memory-mapped sparse vector storage using the `MmapSparseVectorStorage` implementation.

**Data Layout:**

- Indices stored separately from values for compression
- Variable-length encoding for sparse vectors
- Optimized for space efficiency

**Creation:**

```
```

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs410-434](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L410-L434)

## Multi-Dense Vector Storage Formats

Multi-dense vectors allow storing multiple vectors per point, useful for multi-representation embeddings (e.g., ColBERT).

### Storage Architecture

Multi-dense storage maintains two parallel structures:

1. **Vector data** - All sub-vectors stored contiguously or chunked
2. **Offset data** - Mapping from point to vector ranges

```
```

**Key Components:**

- `MultiVectorConfig` defines configuration (comparator type)
- Each point can have variable number of sub-vectors
- Sub-vectors stored sequentially, indexed by offset structure

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs145-153](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L145-L153) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs176-182](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L176-L182)

## Vector Data Types

Each storage format supports three primitive data types for vector elements:

### Supported Data Types

| Type      | Rust Type                     | Size    | Use Case                          |
| --------- | ----------------------------- | ------- | --------------------------------- |
| `Float32` | `VectorElementType` (f32)     | 4 bytes | Default, full precision           |
| `Float16` | `VectorElementTypeHalf` (f16) | 2 bytes | Memory savings, reduced precision |
| `Uint8`   | `VectorElementTypeByte` (u8)  | 1 byte  | Quantized storage                 |

**Type Selection:**

- Configured via `VectorDataConfig.datatype` field
- Different types cannot be mixed in same storage
- Type influences storage size and precision

```
```

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs106-107](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L106-L107) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs155-200](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L155-L200)

## Storage Backend Selection

The `open_vector_storage()` function selects the appropriate storage implementation based on configuration.

### Selection Logic

```
```

**Configuration Mapping:**

- `VectorStorageType::Memory` → RocksDB-based storage (being deprecated)
- `VectorStorageType::Mmap` → Immutable memory-mapped storage
- `VectorStorageType::ChunkedMmap` → Appendable chunked memory-mapped (default for mutable)
- `VectorStorageType::InRamChunkedMmap` → In-RAM with disk persistence

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs99-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L99-L223)

## Storage Operations

### Vector Insertion

All storage types implement the `insert_vector()` method from the `VectorStorage` trait:

```
```

**Process:**

1. Convert input vector to storage data type (Float32/Float16/Uint8)
2. Write vector data to appropriate backend (RocksDB/Mmap/Memory)
3. Update internal tracking (deleted flags, count, etc.)

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs94-99](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L94-L99)

### Batch Updates

The `update_from()` method handles bulk insertion from iterators, used during segment optimization:

**Update Flow:**

1. Iterate over source vectors
2. Insert each vector at next available offset
3. Mark deleted vectors appropriately
4. Return range of inserted offsets

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs107-111](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L107-L111)

### Vector Retrieval

Vectors are retrieved using access pattern hints for optimization:

```
```

**Access Patterns:**

- `Sequential` - Enables prefetching for sequential reads
- `Random` - No prefetching, single vector access

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs42-58](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L42-L58) [lib/segment/src/vector\_storage/vector\_storage\_base.rs89-92](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L89-L92)

## Storage Migration

Qdrant actively migrates from RocksDB-based storage to memory-mapped formats for better performance.

### Dense Vector Migration

```
```

**Migration Process:**

1. Create new mmap-based storage in segment path
2. Copy all vectors from RocksDB to new storage
3. Preserve deletion flags during migration
4. Flush new storage to ensure persistence
5. Update segment configuration to reflect new storage type
6. Destroy old RocksDB column family

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs1047-1126](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L1047-L1126)

### Multi-Dense Vector Migration

Similar process for multi-dense vectors:

**Key Differences:**

- Preserves `MultiVectorConfig` during migration
- Migrates both vector data and offset structures
- Uses `migrate_rocksdb_multi_dense_vector_storage_to_mmap()`

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs1135-1195](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L1135-L1195)

### Feature Flag Control

Migration is controlled by feature flags:

- `migrate_rocksdb_vector_storage` - Enables vector storage migration
- `migrate_rocksdb_id_tracker` - Enables ID tracker migration
- `migrate_rocksdb_payload_storage` - Enables payload storage migration

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs753-756](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L753-L756)

## Performance Characteristics

### Memory Usage

| Storage Type     | RAM Usage | Disk Usage | Trade-off                     |
| ---------------- | --------- | ---------- | ----------------------------- |
| RocksDB (Simple) | Low       | Medium     | Legacy, slower reads          |
| Mmap (Immutable) | Minimal   | High       | OS page cache, read-only      |
| ChunkedMmap      | Minimal   | High       | OS page cache, appendable     |
| InRamChunkedMmap | High      | High       | Fast access, full data in RAM |

### Cache Control

Storage types support cache management:

- `populate()` - Prefetch mmap data into page cache
- `clear_cache()` - Advise OS to drop cached pages

**Usage Pattern:**

```
```

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs562-607](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L562-L607) [lib/segment/src/vector\_storage/vector\_storage\_base.rs609-654](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L609-L654)

## VectorStorageEnum Implementation

The `VectorStorageEnum` serves as a unified interface to all storage implementations:

### Enum Variants by Category

**Dense Variants (per datatype):**

- `DenseSimple`, `DenseSimpleByte`, `DenseSimpleHalf`
- `DenseVolatile`, `DenseVolatileByte`, `DenseVolatileHalf`
- `DenseMemmap`, `DenseMemmapByte`, `DenseMemmapHalf`
- `DenseAppendableMemmap`, `DenseAppendableMemmapByte`, `DenseAppendableMemmapHalf`
- `DenseAppendableInRam`, `DenseAppendableInRamByte`, `DenseAppendableInRamHalf`

**Sparse Variants:**

- `SparseSimple`, `SparseVolatile`, `SparseMmap`

**Multi-Dense Variants (per datatype):**

- `MultiDenseSimple`, `MultiDenseSimpleByte`, `MultiDenseSimpleHalf`
- `MultiDenseVolatile`, `MultiDenseVolatileByte`, `MultiDenseVolatileHalf`
- `MultiDenseAppendableMemmap`, `MultiDenseAppendableMemmapByte`, `MultiDenseAppendableMemmapHalf`
- `MultiDenseAppendableInRam`, `MultiDenseAppendableInRamByte`, `MultiDenseAppendableInRamHalf`

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs217-349](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L217-L349)

### Trait Implementations

All storage enum variants delegate to their inner implementation:

```
```

**Key Methods:**

- `distance()` - Returns configured distance metric
- `datatype()` - Returns vector element data type
- `is_on_disk()` - Whether data is memory-mapped vs RAM
- `total_vector_count()` - Total vectors including deleted
- `available_vector_count()` - Non-deleted vector count
- `deleted_vector_count()` - Count of deleted vectors
- `deleted_vector_bitslice()` - Bitslice of deletion flags

Sources: [lib/segment/src/vector\_storage/vector\_storage\_base.rs754-1031](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L754-L1031)

## Integration with Segments

Vector storage is created and managed as part of segment construction:

### Segment Creation Flow

```
```

**Key Steps:**

1. Create payload storage based on config

2. For each vector name in configuration:

   - Determine vector storage path
   - Open/create appropriate vector storage
   - Create vector index on top of storage

3. Assemble all components into `Segment`

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs436-627](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L436-L627)

### Storage Paths

Vector storage files are organized by vector name:

- Path pattern: `{segment_path}/vector_storage[-{vector_name}]`
- For default vector: `vector_storage`
- For named vectors: `vector_storage-{name}`

Sources: [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs88-93](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L88-L93)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Vector Storage Formats](#vector-storage-formats.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Vector Storage Architecture](#vector-storage-architecture.md)
- [Dense Vector Storage Formats](#dense-vector-storage-formats.md)
- [Storage Type Comparison](#storage-type-comparison.md)
- [DenseSimple (RocksDB-based)](#densesimple-rocksdb-based.md)
- [DenseMemmap (Immutable Memory-Mapped)](#densememmap-immutable-memory-mapped.md)
- [DenseAppendableMemmap (Chunked Memory-Mapped)](#denseappendablememmap-chunked-memory-mapped.md)
- [DenseAppendableInRam (In-Memory Persisted)](#denseappendableinram-in-memory-persisted.md)
- [Sparse Vector Storage Formats](#sparse-vector-storage-formats.md)
- [Sparse Storage Types](#sparse-storage-types.md)
- [SparseMmap Storage](#sparsemmap-storage.md)
- [Multi-Dense Vector Storage Formats](#multi-dense-vector-storage-formats.md)
- [Storage Architecture](#storage-architecture.md)
- [Vector Data Types](#vector-data-types.md)
- [Supported Data Types](#supported-data-types.md)
- [Storage Backend Selection](#storage-backend-selection.md)
- [Selection Logic](#selection-logic.md)
- [Storage Operations](#storage-operations.md)
- [Vector Insertion](#vector-insertion.md)
- [Batch Updates](#batch-updates.md)
- [Vector Retrieval](#vector-retrieval.md)
- [Storage Migration](#storage-migration.md)
- [Dense Vector Migration](#dense-vector-migration.md)
- [Multi-Dense Vector Migration](#multi-dense-vector-migration.md)
- [Feature Flag Control](#feature-flag-control.md)
- [Performance Characteristics](#performance-characteristics.md)
- [Memory Usage](#memory-usage.md)
- [Cache Control](#cache-control.md)
- [VectorStorageEnum Implementation](#vectorstorageenum-implementation.md)
- [Enum Variants by Category](#enum-variants-by-category.md)
- [Trait Implementations](#trait-implementations.md)
- [Integration with Segments](#integration-with-segments.md)
- [Segment Creation Flow](#segment-creation-flow.md)
- [Storage Paths](#storage-paths.md)
