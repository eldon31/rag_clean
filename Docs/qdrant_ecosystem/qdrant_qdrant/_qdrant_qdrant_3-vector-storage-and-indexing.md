Vector Storage and Indexing | qdrant/qdrant | DeepWiki

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

# Vector Storage and Indexing

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
- [lib/common/issues/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/issues/Cargo.toml)
- [lib/segment/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml)
- [lib/segment/src/entry/entry\_point.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/entry/entry_point.rs)
- [lib/segment/src/fixtures/index\_fixtures.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/fixtures/index_fixtures.rs)
- [lib/segment/src/segment\_constructor/segment\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs)
- [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs)
- [lib/segment/src/vector\_storage/vector\_storage\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs)
- [lib/sparse/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/Cargo.toml)
- [lib/storage/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml)
- [tools/missed\_cherry\_picks.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/missed_cherry_picks.sh)

## Purpose and Scope

This page provides an overview of vector storage strategies and indexing approaches in Qdrant. It covers the core abstractions for storing vector data, the different storage backends available, and how indexing structures are layered on top of storage. This page focuses on the architectural design and available options.

For implementation details of specific index types, see:

- **HNSW Index**: [3.2](qdrant/qdrant/3.2-hnsw-index-implementation.md)
- **Vector Quantization**: [3.3](qdrant/qdrant/3.3-vector-quantization.md)
- **Sparse Vector Indexing**: [3.4](qdrant/qdrant/3.4-sparse-vector-indexing.md)

For storage format details, see [3.1](qdrant/qdrant/3.1-vector-storage-formats.md).

For how segments use these components, see [2.5](qdrant/qdrant/2.5-segment-lifecycle-and-construction.md).

---

## Vector Storage and Indexing Architecture

Qdrant separates **vector storage** from **vector indexing** as distinct concerns. Storage handles persisting and retrieving raw vector data, while indexing provides fast similarity search capabilities over that data.

### Core Abstractions Diagram

```
```

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs60-150](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L60-L150) [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs) [lib/segment/src/index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/mod.rs)

### Key Traits

**`VectorStorage` Trait**

The fundamental trait for vector storage, defined in [lib/segment/src/vector\_storage/vector\_storage\_base.rs63-150](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L63-L150) Key methods:

| Method                   | Purpose                         |
| ------------------------ | ------------------------------- |
| `get_vector<P>()`        | Retrieve a vector by offset     |
| `insert_vector()`        | Store a new vector              |
| `delete_vector()`        | Mark vector as deleted          |
| `update_from()`          | Batch update from iterator      |
| `total_vector_count()`   | Total vectors including deleted |
| `deleted_vector_count()` | Count of deleted vectors        |
| `is_on_disk()`           | Whether storage is disk-backed  |

**`VectorIndex` Trait**

Provides similarity search over vectors. Different implementations offer trade-offs between speed and accuracy.

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs60-150](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L60-L150) [lib/segment/src/index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/mod.rs)

---

## Vector Storage Backends

Qdrant supports multiple storage backends, each optimized for different use cases. The choice is controlled by `VectorStorageType` configuration.

### Storage Backend Types

```
```

**Sources:** [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs99-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L99-L223)

### Storage Backend Selection

The function `open_vector_storage()` in [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs99-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L99-L223) selects the appropriate storage implementation based on configuration:

| Storage Type       | Implementation                              | Use Case                              | RocksDB Required |
| ------------------ | ------------------------------------------- | ------------------------------------- | ---------------- |
| `Memory`           | `SimpleDenseVectorStorage`                  | Fast in-memory access, small datasets | Yes              |
| `Mmap`             | `MemmapDenseVectorStorage`                  | Large datasets, minimal RAM usage     | No               |
| `ChunkedMmap`      | `AppendableMmapDenseVectorStorage`          | Appendable segments, growing data     | No               |
| `InRamChunkedMmap` | `AppendableMmapDenseVectorStorage` (in-RAM) | Fast access + crash recovery          | No               |

**Note:** As of the current codebase, Qdrant is deprecating RocksDB storage. The `Memory` storage type requires the `rocksdb` feature flag, which is optional.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs99-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L99-L223) [lib/segment/Cargo.toml18](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml#L18-L18)

---

## VectorStorageEnum Variants

The `VectorStorageEnum` in [lib/segment/src/vector\_storage/vector\_storage\_base.rs216-349](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L216-L349) is a large enum that combines storage backend type, vector type (dense/sparse/multi), and element data type (Float32/Float16/Uint8).

### Dense Vector Storage Variants

```
```

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs216-349](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L216-L349)

### Sparse and Multi-Dense Variants

| Vector Type     | Variants                                               | Notes                      |
| --------------- | ------------------------------------------------------ | -------------------------- |
| **Sparse**      | `SparseSimple`, `SparseVolatile`, `SparseMmap`         | Inverted index structure   |
| **Multi-Dense** | `MultiDenseSimple`, `MultiDenseAppendableMemmap`, etc. | Multiple vectors per point |

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs281-348](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L281-L348)

---

## Vector Index Types

Qdrant provides three main index types, each with different performance characteristics.

### Index Type Comparison

```
```

**Sources:** [lib/segment/src/index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/mod.rs) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs291-318](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L291-L318)

### PlainVectorIndex

- **Algorithm:** Brute-force linear scan
- **Accuracy:** 100% (exact search)
- **Speed:** O(n) per query
- **Use case:** Small collections (<10K vectors), perfect recall required
- **Implementation:** [lib/segment/src/index/plain\_vector\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_vector_index.rs)

### HNSWIndex

- **Algorithm:** Hierarchical Navigable Small World graph
- **Accuracy:** Approximate (tunable via `ef` parameter)
- **Speed:** O(log n) expected
- **Use case:** Large collections, fast search with acceptable recall
- **Implementation:** See [3.2](qdrant/qdrant/3.2-hnsw-index-implementation.md) for details

### SparseVectorIndex

- **Algorithm:** Inverted index (like text search)
- **Data structure:** Maps dimension→points with non-zero values
- **Use case:** High-dimensional sparse vectors (e.g., TF-IDF, BM25)
- **Implementation:** See [3.4](qdrant/qdrant/3.4-sparse-vector-indexing.md) for details

**Sources:** [lib/segment/src/index/plain\_vector\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_vector_index.rs) [lib/segment/src/index/hnsw\_index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/mod.rs) [lib/segment/src/index/sparse\_index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/mod.rs)

### Index Selection in Code

The function `open_vector_index()` in [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs291-318](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L291-L318) selects the index type:

```
match &vector_config.index {
    Indexes::Plain {} => VectorIndexEnum::Plain(PlainVectorIndex::new(...)),
    Indexes::Hnsw(hnsw_config) => VectorIndexEnum::Hnsw(HNSWIndex::open(...)),
}
```

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs291-318](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L291-L318)

---

## Vector Data Types

Qdrant supports three classes of vectors, each with specialized storage and indexing.

### Dense Vectors

Standard fixed-dimensional vectors. Most common use case (e.g., embeddings from neural networks).

- **Storage trait:** `DenseVectorStorage<T>` in [lib/segment/src/vector\_storage/vector\_storage\_base.rs152-183](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L152-L183)
- **Element types:** `VectorElementType` (f32), `VectorElementTypeByte` (u8), `VectorElementTypeHalf` (f16)
- **Access methods:** `get_dense<P>()`, `get_dense_batch()`

### Sparse Vectors

High-dimensional vectors with mostly zero values, stored as (index, value) pairs.

- **Storage trait:** `SparseVectorStorage` in [lib/segment/src/vector\_storage/vector\_storage\_base.rs185-191](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L185-L191)
- **Format:** `SparseVector` from sparse crate
- **Access methods:** `get_sparse<P>()`, `get_sparse_opt<P>()`

### Multi-Dense Vectors

Multiple dense vectors per point (e.g., ColBERT embeddings).

- **Storage trait:** `MultiVectorStorage<T>` in [lib/segment/src/vector\_storage/vector\_storage\_base.rs193-214](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L193-L214)
- **Configuration:** `MultiVectorConfig` specifies comparator (max\_sim, etc.)
- **Access methods:** `get_multi<P>()`, `get_batch_multi()`

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs152-214](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L152-L214) [lib/sparse/src/common/sparse\_vector.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/common/sparse_vector.rs)

---

## Storage Element Data Types

Vectors can be stored with different precision levels, trading accuracy for memory and performance.

### VectorStorageDatatype Options

```
```

**Sources:** [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)

### Type Selection

Configured via `VectorDataConfig.datatype`. The element type determines which variant of storage enum is used (e.g., `DenseSimple` vs `DenseSimpleByte` vs `DenseSimpleHalf`).

**Tradeoffs:**

| Type    | Memory | Accuracy | Speed    | Use Case                            |
| ------- | ------ | -------- | -------- | ----------------------------------- |
| Float32 | 4B/dim | Highest  | Baseline | Default, best quality               |
| Float16 | 2B/dim | Good     | Similar  | Large datasets, 2x compression      |
| Uint8   | 1B/dim | Lower    | Faster   | Extreme compression, with rescoring |

**Sources:** [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs) [lib/segment/src/vector\_storage/vector\_storage\_base.rs216-349](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L216-L349)

---

## Quantization Layer

Quantization is an optional compression layer that reduces memory usage while maintaining search quality through rescoring.

### Quantization Architecture

```
```

**Key concept:** Quantized vectors are stored separately from original vectors. Search happens on compressed data first (fast), then top candidates are rescored with original vectors (accurate).

**Sources:** [lib/segment/src/vector\_storage/quantized/quantized\_vectors.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/quantized/quantized_vectors.rs) [lib/quantization/](https://github.com/qdrant/qdrant/blob/48203e41/lib/quantization/)

For detailed quantization implementation, see [3.3](qdrant/qdrant/3.3-vector-quantization.md).

---

## Segment Vector Data Organization

Each `Segment` contains a `HashMap<VectorNameBuf, VectorData>` to support named vectors (multi-vector collections).

### VectorData Structure in Segment

```
```

**Sources:** [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs514-576](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L514-L576)

### Storage Path Convention

Each vector name gets dedicated directories:

- Storage: `<segment>/vector_storage` or `<segment>/vector_storage-<name>`
- Index: `<segment>/vector_index` or `<segment>/vector_index-<name>`

Helper functions in [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs80-97](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L80-L97):

- `get_vector_storage_path(segment_path, vector_name)`
- `get_vector_index_path(segment_path, vector_name)`

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs80-97](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L80-L97)

---

## Creating and Opening Vector Storage

### Sparse Vector Storage Creation

For sparse vectors, the function `create_sparse_vector_storage()` in [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs410-434](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L410-L434) handles initialization:

```
match storage_type {
    SparseVectorStorageType::OnDisk => {
        // RocksDB-backed (requires feature flag)
        open_simple_sparse_vector_storage(db, column, stopped)
    }
    SparseVectorStorageType::Mmap => {
        // Memory-mapped
        MmapSparseVectorStorage::open_or_create(path)
    }
}
```

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs410-434](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L410-L434)

### Dense Vector Index Creation

The function `open_vector_index()` creates the index, while `build_vector_index()` in [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs320-351](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L320-L351) performs initial construction with optimization.

For HNSW indices, old indices from merged segments can be reused to speed up construction:

```
```

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs291-351](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L291-L351)

---

## Access Patterns

The `VectorStorage` trait uses a type parameter `P: AccessPattern` to optimize reads.

### AccessPattern Types

```
```

This allows storage implementations to optimize based on access pattern (e.g., prefetching for sequential reads).

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs42-58](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L42-L58) [lib/segment/src/vector\_storage/vector\_storage\_base.rs89-92](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs#L89-L92)

---

## Storage and Index Coordination

### Segment Building Example

When constructing a new segment (e.g., during optimization), `SegmentBuilder` in [lib/segment/src/segment\_constructor/segment\_builder.rs58-74](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L58-L74) coordinates storage and index creation:

1. Create ID tracker

2. Create payload storage

3. For each vector name:

   - Create vector storage (via `open_vector_storage()`)
   - Populate with data from source segments
   - Create quantized vectors (if configured)
   - Build vector index (with `build_vector_index()`)

**Sources:** [lib/segment/src/segment\_constructor/segment\_builder.rs58-167](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L58-L167) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs436-576](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L436-L576)

### Immutability and Appendability

Segments come in two flavors affecting storage choice:

| Segment Type   | Storage                 | Typical Index | Use Case                         |
| -------------- | ----------------------- | ------------- | -------------------------------- |
| **Appendable** | `ChunkedMmap`, `Memory` | `Plain`       | Active segments receiving writes |
| **Immutable**  | `Mmap`                  | `HNSW`        | Optimized read-only segments     |

The transition happens during segment optimization (see [2.4](qdrant/qdrant/2.4-local-shard-architecture.md)).

**Sources:** [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs) [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs)

---

## Summary

Qdrant's vector storage and indexing system provides:

1. **Separation of Concerns:** Storage (persistence) and indexing (search) are independent layers
2. **Multiple Storage Backends:** RocksDB (deprecated), Mmap, ChunkedMmap, InRamChunkedMmap
3. **Multiple Index Types:** Plain (exact), HNSW (approximate), Sparse (inverted)
4. **Vector Type Support:** Dense, Sparse, Multi-dense vectors
5. **Data Type Flexibility:** Float32, Float16, Uint8 storage
6. **Optional Quantization:** Compression layer for memory reduction
7. **Per-Vector-Name Organization:** Named vectors with independent storage/index

The architecture allows flexible configuration for different scale and performance requirements while maintaining clean abstractions between components.

**Sources:** [lib/segment/src/vector\_storage/vector\_storage\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs) [lib/segment/src/index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/mod.rs) [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Vector Storage and Indexing](#vector-storage-and-indexing.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Vector Storage and Indexing Architecture](#vector-storage-and-indexing-architecture.md)
- [Core Abstractions Diagram](#core-abstractions-diagram.md)
- [Key Traits](#key-traits.md)
- [Vector Storage Backends](#vector-storage-backends.md)
- [Storage Backend Types](#storage-backend-types.md)
- [Storage Backend Selection](#storage-backend-selection.md)
- [VectorStorageEnum Variants](#vectorstorageenum-variants.md)
- [Dense Vector Storage Variants](#dense-vector-storage-variants.md)
- [Sparse and Multi-Dense Variants](#sparse-and-multi-dense-variants.md)
- [Vector Index Types](#vector-index-types.md)
- [Index Type Comparison](#index-type-comparison.md)
- [PlainVectorIndex](#plainvectorindex.md)
- [HNSWIndex](#hnswindex.md)
- [SparseVectorIndex](#sparsevectorindex.md)
- [Index Selection in Code](#index-selection-in-code.md)
- [Vector Data Types](#vector-data-types.md)
- [Dense Vectors](#dense-vectors.md)
- [Sparse Vectors](#sparse-vectors.md)
- [Multi-Dense Vectors](#multi-dense-vectors.md)
- [Storage Element Data Types](#storage-element-data-types.md)
- [VectorStorageDatatype Options](#vectorstoragedatatype-options.md)
- [Type Selection](#type-selection.md)
- [Quantization Layer](#quantization-layer.md)
- [Quantization Architecture](#quantization-architecture.md)
- [Segment Vector Data Organization](#segment-vector-data-organization.md)
- [VectorData Structure in Segment](#vectordata-structure-in-segment.md)
- [Storage Path Convention](#storage-path-convention.md)
- [Creating and Opening Vector Storage](#creating-and-opening-vector-storage.md)
- [Sparse Vector Storage Creation](#sparse-vector-storage-creation.md)
- [Dense Vector Index Creation](#dense-vector-index-creation.md)
- [Access Patterns](#access-patterns.md)
- [AccessPattern Types](#accesspattern-types.md)
- [Storage and Index Coordination](#storage-and-index-coordination.md)
- [Segment Building Example](#segment-building-example.md)
- [Immutability and Appendability](#immutability-and-appendability.md)
- [Summary](#summary.md)
