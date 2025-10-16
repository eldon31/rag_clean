Key Concepts and Terminology | qdrant/qdrant | DeepWiki

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

# Key Concepts and Terminology

Relevant source files

- [README.md](https://github.com/qdrant/qdrant/blob/48203e41/README.md)
- [docs/CODE\_OF\_CONDUCT.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/CODE_OF_CONDUCT.md)
- [docs/CONTRIBUTING.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/CONTRIBUTING.md)
- [docs/DEVELOPMENT.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md)
- [docs/QUICK\_START.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/QUICK_START.md)
- [docs/grpc/docs.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/grpc/docs.md)
- [docs/imgs/ci-coverage-report.png](https://github.com/qdrant/qdrant/blob/48203e41/docs/imgs/ci-coverage-report.png)
- [docs/imgs/local-coverage-report.png](https://github.com/qdrant/qdrant/blob/48203e41/docs/imgs/local-coverage-report.png)
- [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json)
- [docs/roadmap/README.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/README.md)
- [docs/roadmap/roadmap-2022.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2022.md)
- [docs/roadmap/roadmap-2023.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2023.md)
- [docs/roadmap/roadmap-2024.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2024.md)
- [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)
- [lib/api/src/grpc/proto/collections.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto)
- [lib/api/src/grpc/proto/points.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto)
- [lib/api/src/grpc/qdrant.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs)
- [lib/collection/src/config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs)
- [lib/collection/src/operations/config\_diff.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs)
- [lib/collection/src/operations/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs)
- [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs)
- [lib/collection/src/optimizers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/optimizers_builder.rs)
- [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)
- [lib/storage/src/content\_manager/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/collection_meta_ops.rs)
- [lib/storage/src/content\_manager/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs)

## Purpose and Scope

This page defines the fundamental concepts and terminology used throughout Qdrant's architecture and codebase. Understanding these concepts is essential for working with or extending Qdrant. For details on how these components are organized into a complete system, see [System Architecture](qdrant/qdrant/2-system-architecture.md). For information on specific operational aspects like search processing or data updates, see [Search and Query Processing](qdrant/qdrant/5-search-and-query-processing.md) and [Data Updates and Consistency](qdrant/qdrant/6-data-updates-and-consistency.md).

---

## Points

A **point** is the fundamental data unit in Qdrant. Each point consists of:

- **ID**: A unique identifier (numeric or UUID)
- **Vector(s)**: One or more vector embeddings
- **Payload**: Optional JSON metadata
- **Version**: A sequential number tracking modifications

### Point Structure in Code

```
```

**Internal Representation**:

- `PointStruct`: API representation for point insertion [lib/api/src/grpc/qdrant.rs213-218](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L213-L218)
- `RecordInternal`: Internal representation with all fields [lib/collection/src/operations/types.rs131-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L131-L143)
- `ScoredPoint`: Search result with score [lib/segment/src/types.rs350-366](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L350-L366)

### Point IDs

Qdrant supports two types of point identifiers:

| Type    | Rust Type | Example                                | Use Case                               |
| ------- | --------- | -------------------------------------- | -------------------------------------- |
| Numeric | `u64`     | `42`                                   | Sequential IDs, simple indexing        |
| UUID    | `Uuid`    | `550e8400-e29b-41d4-a716-446655440000` | Distributed systems, global uniqueness |

The `ExtendedPointId` enum represents both types:

[lib/segment/src/types.rs155-162](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L155-L162)

**Compact Representation**: Internally, Qdrant uses `CompactExtendedPointId` (17 bytes) instead of `ExtendedPointId` (24 bytes) for memory efficiency [lib/segment/src/types.rs248-254](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L248-L254)

**Sources**: [lib/segment/src/types.rs146-272](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L146-L272) [lib/api/src/grpc/proto/points.proto38-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L38-L43)

---

## Vectors

Vectors are numerical representations of data used for similarity search. Qdrant supports multiple vector types per point.

### Vector Types

```
```

### Dense Vectors

Standard float vectors commonly used for semantic embeddings:

- **Type**: `Vec<f32>` (default) or `Vec<u8>`, `Vec<f16>` [lib/api/src/grpc/proto/collections.proto8-13](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto#L8-L13)
- **Storage**: Optimized for SIMD operations
- **Example**: 768-dimensional BERT embedding

### Sparse Vectors

High-dimensional vectors with mostly zero values:

- **Type**: Indices (`Vec<u32>`) + Values (`Vec<f32>`) [lib/api/src/grpc/proto/points.proto97-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L97-L100)
- **Storage**: Only non-zero elements stored
- **Use case**: Text search with learned sparse representations, BM25-style retrieval

### Multi-Dense Vectors

Multiple dense vectors per point:

- **Type**: `Vec<DenseVector>` [lib/api/src/grpc/proto/points.proto102-104](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L102-L104)
- **Comparator**: `MaxSim` - maximum similarity across all vectors [lib/api/src/grpc/proto/collections.proto67-73](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto#L67-L73)
- **Use case**: Multiple aspects/views of the same entity

### Named Vectors

Collections can store multiple different vector types under different names:

- **Type**: `HashMap<VectorNameBuf, VectorInternal>` [lib/segment/src/data\_types/vectors.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/data_types/vectors.rs)
- **Default name**: `""` (empty string) stored as `DEFAULT_VECTOR_NAME` [lib/segment/src/data\_types/vectors.rs16](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/data_types/vectors.rs#L16-L16)
- **Use case**: Multi-modal search (e.g., text + image embeddings)

**Sources**: [lib/segment/src/types.rs62-66](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L62-L66) [lib/segment/src/data\_types/vectors.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/data_types/vectors.rs) [lib/api/src/grpc/proto/points.proto68-117](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L68-L117)

---

## Payloads

Payloads are arbitrary JSON metadata attached to points. They enable filtering and enrichment of search results.

### Payload Structure

```
```

### Payload Types

| Type     | Rust Type         | Indexed As                    | Example                  |
| -------- | ----------------- | ----------------------------- | ------------------------ |
| Keyword  | `String`          | `PayloadSchemaType::Keyword`  | `"category"`             |
| Integer  | `i64`             | `PayloadSchemaType::Integer`  | `42`                     |
| Float    | `f64`             | `PayloadSchemaType::Float`    | `3.14`                   |
| Boolean  | `bool`            | `PayloadSchemaType::Bool`     | `true`                   |
| Datetime | `DateTimeWrapper` | `PayloadSchemaType::Datetime` | `"2024-01-15T12:00:00Z"` |
| UUID     | `Uuid`            | `PayloadSchemaType::Uuid`     | `"550e8400-..."`         |
| Geo      | `GeoPoint`        | `PayloadSchemaType::Geo`      | `{lat: 51.5, lon: -0.1}` |
| Text     | `String`          | `PayloadSchemaType::Text`     | `"Full text content"`    |

### Payload Keys and Paths

Payload keys use JSON path notation:

- **Type**: `JsonPath` (alias for `PayloadKeyType`) [lib/segment/src/types.rs48](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L48-L48)
- **Nested access**: `"user.address.city"`
- **Array access**: `"items[0].name"`

### DateTime Representation

DateTime values are stored as microsecond timestamps:

- **External format**: RFC 3339 string (`"2024-01-15T12:00:00Z"`)
- **Internal format**: `i64` microseconds since Unix epoch
- **Type**: `DateTimeWrapper` wrapping `chrono::DateTime<Utc>` [lib/segment/src/types.rs68-81](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L68-L81)

**Sources**: [lib/segment/src/types.rs48-138](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L48-L138) [lib/api/src/grpc/qdrant.rs13-17](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L13-L17)

---

## Collections

A **collection** is a named logical container for points with a defined schema. Collections are the primary organizational unit in Qdrant.

### Collection Components Hierarchy

```
```

### Collection Configuration

The `CollectionConfig` defines the collection's behavior:

**Core Parameters** (`CollectionParams`):

- **Vectors**: Vector configurations (size, distance metric, quantization)
- **Shard number**: Number of shards (default: 1 standalone, N nodes distributed)
- **Replication factor**: Number of replicas per shard [lib/collection/src/config.rs104-106](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L104-L106)
- **Write consistency factor**: Minimum replicas for successful writes [lib/collection/src/config.rs108-113](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L108-L113)
- **On-disk payload**: Whether payloads are stored in memory or on disk [lib/collection/src/config.rs121-128](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L121-L128)

**Index Configuration**:

- **HNSW config**: Graph construction parameters [lib/collection/src/operations/types.rs175](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L175-L175)
- **Quantization config**: Vector compression settings [lib/collection/src/operations/types.rs179](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L179-L179)
- **Optimizer config**: Segment optimization thresholds [lib/collection/src/operations/types.rs176](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L176-L176)

### Collection Status

Collections report their operational state:

| Status | Code                       | Meaning                  |
| ------ | -------------------------- | ------------------------ |
| Green  | `CollectionStatus::Green`  | All segments ready       |
| Yellow | `CollectionStatus::Yellow` | Optimization in progress |
| Grey   | `CollectionStatus::Grey`   | Optimization pending     |
| Red    | `CollectionStatus::Red`    | Operations failed        |

**Sources**: [lib/collection/src/operations/types.rs66-79](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L66-L79) [lib/collection/src/config.rs86-133](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L86-L133)

---

## Shards and Partitioning

Shards enable horizontal scaling by partitioning data across nodes. Each collection is divided into shards, which are distributed across the cluster.

### Shard Distribution Model

```
```

### Sharding Methods

**Auto Sharding** (`ShardingMethod::Auto`):

- Points distributed uniformly using hash function
- Default method [lib/collection/src/config.rs76-84](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L76-L84)

**Custom Sharding** (`ShardingMethod::Custom`):

- Points routed by shard key (keyword or numeric)
- Enables tenant isolation, geographic partitioning [lib/collection/src/config.rs99-102](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L99-L102)
- Shard key types: `ShardKey::Keyword(String)` or `ShardKey::Number(u64)` [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)

### Shard Replicas

Each shard can have multiple replicas for fault tolerance:

**Replica Types**:

- **LocalShard**: Hosted on current peer, contains actual data [lib/collection/src/shards/local\_shard](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard)
- **RemoteShard**: Proxy to replica on another peer [lib/collection/src/shards/remote\_shard](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/remote_shard)
- **ProxyShard**: Temporary proxy during snapshot recovery [lib/collection/src/shards/proxy\_shard](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/proxy_shard)

**Replica States**:

| State        | Code                         | Description                    |
| ------------ | ---------------------------- | ------------------------------ |
| Active       | `ReplicaState::Active`       | Serving read/write requests    |
| Dead         | `ReplicaState::Dead`         | Failed, not serving requests   |
| Partial      | `ReplicaState::Partial`      | Being transferred/recovered    |
| Initializing | `ReplicaState::Initializing` | Being created                  |
| Listener     | `ReplicaState::Listener`     | Receiving updates, not serving |

### ShardReplicaSet

The `ShardReplicaSet` coordinates operations across replicas:

- Selects which replica handles read requests (prefer local)
- Distributes write operations to all active replicas
- Manages replica state transitions
- Enforces consistency guarantees via `WriteOrdering` [lib/collection/src/shards/replica\_set](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set)

**Sources**: [lib/collection/src/config.rs76-102](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L76-L102) [lib/collection/src/shards/shard.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/shard.rs) [lib/collection/src/shards/replica\_set](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set)

---

## Segments

A **segment** is the fundamental storage and indexing unit within a shard. Segments are immutable once optimized and are managed by background optimization processes.

### Segment Architecture

```
```

### Segment Types

**Plain Segments** (`SegmentType::Plain`):

- Unindexed, supports all operations (insert, update, delete)
- Uses brute-force search (exact results)
- Typically small, recent data [lib/segment/src/types.rs397-404](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L397-L404)

**Indexed Segments** (`SegmentType::Indexed`):

- Contains HNSW graph index for fast approximate search
- Read-only (new writes trigger re-optimization)
- Typically larger, optimized segments [lib/segment/src/types.rs397-404](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L397-L404)

### Segment Components

**IdTracker**: Maps external point IDs to internal sequential IDs [lib/segment/src/id\_tracker](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/id_tracker)

- External: `ExtendedPointId` (u64 or UUID)
- Internal: `PointOffsetType` (u32, dense sequential)
- Tracks deletions via bitset

**VectorData**: One instance per named vector [lib/segment/src/vector\_data](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_data)

- `VectorStorage`: Raw vector data (dense/sparse/multi)
- `VectorIndex`: Search index (HNSW/Plain/Sparse)
- `QuantizedVectors`: Optional compressed vectors

**PayloadStorage**: JSON document store [lib/segment/src/payload\_storage](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/payload_storage)

- Types: `SimplePayloadStorage` (in-memory), `OnDiskPayloadStorage` (RocksDB/Gridstore), `MmapPayloadStorage`
- Stores arbitrary JSON per point

**PayloadIndex**: Indexes for filtered search [lib/segment/src/index/field\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index)

- One index per payload field
- Types: Numeric, Keyword, FullText, Geo, Bool, Datetime, UUID

### Segment Optimization

The `UpdateHandler` manages background optimization:

1. **Vacuum Optimizer**: Removes deleted points
2. **Merge Optimizer**: Merges small segments
3. **Indexing Optimizer**: Builds HNSW indexes for large segments
4. **Config Mismatch Optimizer**: Rebuilds segments when config changes

Optimization triggered when:

- Deleted points exceed threshold (`deleted_threshold`)
- Segment size exceeds indexing threshold (`indexing_threshold`)
- Too many segments exist (`default_segment_number`)

**Sources**: [lib/segment/src/types.rs394-461](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L394-L461) [lib/collection/src/shards/local\_shard](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard) [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs)

---

## Distance Metrics

Distance metrics determine how vector similarity is calculated. Qdrant supports four primary distance functions.

### Distance Types

```
```

### Distance Implementation

[lib/segment/src/types.rs290-341](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L290-L341)

| Metric      | Enum                  | Order             | Use Case                            |
| ----------- | --------------------- | ----------------- | ----------------------------------- |
| Cosine      | `Distance::Cosine`    | Larger is better  | Text embeddings, normalized vectors |
| Euclidean   | `Distance::Euclid`    | Smaller is better | Image embeddings, absolute distance |
| Dot Product | `Distance::Dot`       | Larger is better  | Non-normalized embeddings           |
| Manhattan   | `Distance::Manhattan` | Smaller is better | High-dimensional sparse vectors     |

**Score Post-Processing**:

- `Distance::postprocess_score()`: Converts raw distance to similarity score
- Cosine/Dot: Higher scores = more similar
- Euclid/Manhattan: Lower scores = more similar (inverted for ranking)

**Vector Preprocessing**:

- `Distance::preprocess_vector()`: Normalizes vectors if needed
- Cosine: Normalizes to unit length
- Others: No preprocessing

**Sources**: [lib/segment/src/types.rs275-341](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L275-L341) [lib/segment/src/spaces/metric.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/spaces/metric.rs)

---

## Indexes

Indexes accelerate search operations. Qdrant uses different index types for vectors and payloads.

### Vector Indexes

**HNSW (Hierarchical Navigable Small World)**:

- Graph-based approximate nearest neighbor index

- Type: `Indexes::Hnsw(HnswConfig)` [lib/segment/src/types.rs559-566](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L559-L566)

- Fast search with configurable accuracy/speed tradeoff

- Parameters:

  - `m`: Edges per node (higher = more accurate, more memory)
  - `ef_construct`: Neighbors during construction (higher = better quality)
  - `full_scan_threshold`: Switch to brute-force for small result sets

**Plain Index**:

- Brute-force search, exact results
- Type: `Indexes::Plain {}` [lib/segment/src/types.rs559-566](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L559-L566)
- Used for small segments or when 100% precision required

**Sparse Vector Index**:

- Inverted index for sparse vectors
- Optimized for high-dimensional sparse data
- Supports BM25-like scoring

### Payload Indexes

Payload indexes enable efficient filtering during search:

| Index Type | Payload Type   | Operations                  | Structure                        |
| ---------- | -------------- | --------------------------- | -------------------------------- |
| Keyword    | String         | `=`, `≠`, `in`              | HashMap                          |
| Numeric    | Integer, Float | `<`, `>`, `≤`, `≥`, `range` | Range tree                       |
| FullText   | Text           | `match`, `contains`         | Inverted index with tokenization |
| Geo        | GeoPoint       | `radius`, `bbox`            | R-tree                           |
| Bool       | Boolean        | `=`, `≠`                    | Bitmap                           |
| Datetime   | DateTime       | `<`, `>`, `range`           | Range tree (as i64 microseconds) |
| UUID       | UUID           | `=`, `≠`, `in`              | HashMap (as u128)                |

**Index Selection**:

- `FieldIndex`: Per-field index abstraction [lib/segment/src/index/field\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index)
- `StructPayloadIndex`: Manages all payload indexes for a segment
- Auto-created based on schema or explicit configuration

### Quantization

Vector quantization compresses vectors to reduce memory usage:

**Scalar Quantization** (`ScalarQuantization`):

- Converts f32 → u8 (4x compression)
- Quantile-based range selection [lib/segment/src/types.rs693-717](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L693-L717)

**Product Quantization** (`ProductQuantization`):

- Divides vector into subvectors, quantizes each
- 4x-64x compression ratio [lib/segment/src/types.rs719-743](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L719-L743)

**Binary Quantization** (`BinaryQuantization`):

- Converts to 1-bit or 2-bit representation
- 32x compression [lib/segment/src/types.rs775-789](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L775-L789)
- Supports asymmetric query encoding for accuracy

Quantization is transparent to search - original vectors used for rescoring top-K candidates.

**Sources**: [lib/segment/src/types.rs555-829](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L555-L829) [lib/segment/src/index/hnsw\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index) [lib/segment/src/index/field\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index)

---

## Summary Table: Key Type Mappings

| Concept     | Rust Type              | File Location                                                                                                                                | Description                  |
| ----------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Point ID    | `ExtendedPointId`      | [lib/segment/src/types.rs155-162](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L155-L162)                         | u64 or UUID identifier       |
| Point       | `PointStruct`          | [lib/api/src/grpc/qdrant.rs213](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L213-L213)                         | API representation           |
| Record      | `RecordInternal`       | [lib/collection/src/operations/types.rs131](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L131-L131) | Internal point with all data |
| Vector      | `VectorStructInternal` | [lib/segment/src/data\_types/vectors.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/data_types/vectors.rs)               | All vector types             |
| Payload     | `Payload`              | [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)                                          | JSON metadata map            |
| Collection  | `Collection`           | [lib/collection/src/collection](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection)                                | Logical container            |
| Shard       | `ShardId`              | [lib/collection/src/shards/shard.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/shard.rs)                      | u32 partition identifier     |
| Replica Set | `ShardReplicaSet`      | [lib/collection/src/shards/replica\_set](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set)               | Replica coordinator          |
| Segment     | `Segment`              | [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs)                                      | Storage/index unit           |
| Distance    | `Distance`             | [lib/segment/src/types.rs290](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L290-L290)                             | Similarity metric enum       |
| Index       | `Indexes`              | [lib/segment/src/types.rs559](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L559-L559)                             | Vector index config          |

**Sources**: [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs) [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs) [lib/segment/src/data\_types/vectors.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/data_types/vectors.rs)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Key Concepts and Terminology](#key-concepts-and-terminology.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Points](#points.md)
- [Point Structure in Code](#point-structure-in-code.md)
- [Point IDs](#point-ids.md)
- [Vectors](#vectors.md)
- [Vector Types](#vector-types.md)
- [Dense Vectors](#dense-vectors.md)
- [Sparse Vectors](#sparse-vectors.md)
- [Multi-Dense Vectors](#multi-dense-vectors.md)
- [Named Vectors](#named-vectors.md)
- [Payloads](#payloads.md)
- [Payload Structure](#payload-structure.md)
- [Payload Types](#payload-types.md)
- [Payload Keys and Paths](#payload-keys-and-paths.md)
- [DateTime Representation](#datetime-representation.md)
- [Collections](#collections.md)
- [Collection Components Hierarchy](#collection-components-hierarchy.md)
- [Collection Configuration](#collection-configuration.md)
- [Collection Status](#collection-status.md)
- [Shards and Partitioning](#shards-and-partitioning.md)
- [Shard Distribution Model](#shard-distribution-model.md)
- [Sharding Methods](#sharding-methods.md)
- [Shard Replicas](#shard-replicas.md)
- [ShardReplicaSet](#shardreplicaset.md)
- [Segments](#segments.md)
- [Segment Architecture](#segment-architecture.md)
- [Segment Types](#segment-types.md)
- [Segment Components](#segment-components.md)
- [Segment Optimization](#segment-optimization.md)
- [Distance Metrics](#distance-metrics.md)
- [Distance Types](#distance-types.md)
- [Distance Implementation](#distance-implementation.md)
- [Indexes](#indexes.md)
- [Vector Indexes](#vector-indexes.md)
- [Payload Indexes](#payload-indexes.md)
- [Quantization](#quantization.md)
- [Summary Table: Key Type Mappings](#summary-table-key-type-mappings.md)
