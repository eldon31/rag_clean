Data Types and Conversions | qdrant/qdrant | DeepWiki

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

# Data Types and Conversions

Relevant source files

- [docs/grpc/docs.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/grpc/docs.md)
- [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json)
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

This document describes the data type system used throughout Qdrant's API layer and the conversion mechanisms between different representations. It covers:

- The three-layer type architecture (REST JSON, gRPC Protobuf, Internal Rust)
- Core data types for points, vectors, payloads, filters, and configuration
- Conversion and validation logic between type representations
- Type patterns used for API flexibility (optional fields, diff types, enumerations)

For information about the actual API endpoints and RPC methods, see [REST API Endpoints](qdrant/qdrant/9.1-rest-api-endpoints.md) and [gRPC API Services](qdrant/qdrant/9.2-grpc-api-services.md).

## Type System Architecture

Qdrant maintains three distinct type representations that are converted between as requests flow through the system:

```
```

**Type Flow Architecture**

The system uses different type representations at each layer to optimize for their specific use cases:

- **REST JSON**: Human-readable, flexible field naming, optional fields via `Option<T>`
- **gRPC Protobuf**: Efficient binary encoding, strict schema, backward compatibility
- **Internal Rust**: Type-safe, optimized for processing, domain-specific validation

Sources: [lib/api/src/grpc/conversions.rs1-64](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L1-L64) [lib/collection/src/operations/conversions.rs1-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L1-L60)

## Core Data Types

### Point Identifiers

Points can be identified by either numeric IDs or UUIDs, represented by `ExtendedPointId`:

```
```

**Point ID Type Hierarchy**

| Type Layer | Representation                         | Source                                                                                                                                 |
| ---------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| REST       | Untagged union: `u64` or `String` UUID | OpenAPI schema                                                                                                                         |
| gRPC       | `PointId { oneof point_id_options }`   | [lib/api/src/grpc/proto/points.proto38-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L38-L43) |
| Internal   | `ExtendedPointId` enum                 | [lib/segment/src/types.rs155-162](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L155-L162)                   |

The internal `ExtendedPointId` provides methods for type checking and display:

Sources: [lib/segment/src/types.rs155-220](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L155-L220) [lib/api/src/grpc/proto/points.proto38-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L38-L43)

### Vector Types

Qdrant supports multiple vector representations with different storage and indexing characteristics:

```
```

**Vector Type Conversion Flow**

Key vector type definitions:

| Type                   | Purpose                         | Definition                                |
| ---------------------- | ------------------------------- | ----------------------------------------- |
| `DenseVector`          | Standard dense vectors          | `Vec<f32>`                                |
| `SparseVector`         | Sparse vectors with indices     | `{ values: Vec<f32>, indices: Vec<u32> }` |
| `MultiDenseVector`     | Multiple vectors per point      | `Vec<DenseVector>`                        |
| `VectorStructInternal` | Internal unified representation | Enum over all vector types                |

Sources: [lib/api/src/grpc/proto/points.proto68-117](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L68-L117) [lib/segment/src/types.rs39](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L39-L39) [lib/api/src/grpc/conversions.rs16-17](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L16-L17)

### Vector Configuration

Vector configuration defines how vectors are stored and indexed:

```
```

**Vector Configuration Schema**

Sources: [lib/api/src/grpc/proto/collections.proto8-73](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto#L8-L73) [lib/api/src/grpc/qdrant.rs102-240](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L102-L240) [lib/collection/src/operations/types.rs32-37](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L32-L37)

### Payload Types

Payloads are arbitrary JSON-like data attached to points:

```
```

**Payload Type System**

The internal `Payload` type wraps `serde_json::Map<String, Value>` for flexibility. Payload fields can be indexed with type-specific parameters:

Sources: [lib/api/src/grpc/qdrant.rs1-101](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L1-L101) [lib/segment/src/types.rs48-66](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L48-L66) [lib/api/src/grpc/conversions.rs149-283](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L149-L283)

### Filter Conditions

Filters enable complex querying with various condition types:

```
```

**Filter Condition Hierarchy**

Sources: [lib/api/src/grpc/proto/points.proto163-176](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L163-L176) [lib/api/src/grpc/qdrant.rs40-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L40-L60)

## Conversion Mechanisms

### REST to Internal Conversions

REST JSON types are converted using `serde` deserialization with custom traits:

```
```

**REST Conversion Pipeline**

Example conversion for collection creation:

Sources: [lib/storage/src/content\_manager/conversions.rs65-122](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs#L65-L122)

### gRPC to Internal Conversions

gRPC uses protobuf-generated types with explicit conversion implementations:

```
```

**gRPC Conversion Pipeline**

Key conversion implementations:

| From                 | To                         | Trait     | Location                                                                                                                                    |
| -------------------- | -------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `grpc::PointId`      | `ExtendedPointId`          | `TryFrom` | [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)                           |
| `grpc::Filter`       | `segment::types::Filter`   | `TryFrom` | [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)                           |
| `grpc::VectorParams` | `VectorParams`             | `TryFrom` | [lib/collection/src/operations/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs) |
| `grpc::ShardKey`     | `segment::types::ShardKey` | Custom    | [lib/api/src/grpc/conversions.rs65-91](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L65-L91)              |

Sources: [lib/api/src/grpc/conversions.rs1-64](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L1-L64) [lib/collection/src/operations/conversions.rs1-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L1-L60)

### Bidirectional Conversions

Some types require bidirectional conversion for request/response handling:

```
```

**Bidirectional Conversion Pattern**

Common bidirectional conversions:

- `PointStruct` ↔ `RecordInternal` - [lib/collection/src/operations/conversions.rs116-152](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L116-L152)
- `ScoredPoint` ↔ response types - [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)
- `CollectionInfo` ↔ response types - [lib/collection/src/operations/types.rs189-273](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L189-L273)

Sources: [lib/collection/src/operations/conversions.rs116-152](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L116-L152) [lib/api/src/grpc/conversions.rs1-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L1-L50)

## Configuration Diff Types

To support partial updates, configuration uses "diff" types with all optional fields:

```
```

**Configuration Update Pattern**

Diff types use the `DiffConfig` trait to apply partial updates:

| Full Type            | Diff Type                | Purpose                          |
| -------------------- | ------------------------ | -------------------------------- |
| `HnswConfig`         | `HnswConfigDiff`         | HNSW index configuration updates |
| `OptimizersConfig`   | `OptimizersConfigDiff`   | Optimizer parameter updates      |
| `WalConfig`          | `WalConfigDiff`          | WAL configuration updates        |
| `CollectionParams`   | `CollectionParamsDiff`   | Collection parameter updates     |
| `QuantizationConfig` | `QuantizationConfigDiff` | Quantization updates             |

The `DiffConfig` trait provides update logic:

Sources: [lib/collection/src/operations/config\_diff.rs23-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs#L23-L43) [lib/collection/src/operations/config\_diff.rs45-99](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs#L45-L99) [lib/collection/src/operations/config\_diff.rs101-112](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs#L101-L112)

## Type Validation

Validation occurs at multiple stages using the `validator` crate:

```
```

**Validation Pipeline**

Example validation attributes in use:

```
```

Validation is performed in conversions using the `Validate` trait:

Sources: [lib/api/src/grpc/qdrant.rs102-131](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L102-L131) [lib/collection/src/operations/config\_diff.rs45-99](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs#L45-L99) [lib/collection/src/config.rs86-133](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L86-L133)

## Special Type Patterns

### Datetime Handling

Datetimes are stored as microsecond timestamps (i64) with flexible parsing:

```
```

**Datetime Type Conversion**

Sources: [lib/segment/src/types.rs68-138](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L68-L138)

### Shard Key Selectors

Shard keys support both keyword and numeric types:

```
```

**Shard Key Conversion**

Sources: [lib/api/src/grpc/conversions.rs65-106](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L65-L106) [lib/api/src/grpc/proto/points.proto123-125](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L123-L125)

### Enumeration Mappings

Enumerations are mapped between protobuf integers and Rust enums:

| Concept           | gRPC Proto                                                   | Internal Rust                                                                                                                                  |
| ----------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Distance          | `enum Distance { Cosine=1, Euclid=2, Dot=3, Manhattan=4 }`   | [lib/segment/src/types.rs291-310](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L291-L310)                           |
| Collection Status | `enum CollectionStatus { Green=1, Yellow=2, Red=3, Grey=4 }` | [lib/collection/src/operations/types.rs67-107](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L67-L107) |
| Write Ordering    | `enum WriteOrderingType { Weak=0, Medium=1, Strong=2 }`      | [lib/collection/src/operations/point\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/point_ops.rs)       |
| Quantization Type | `enum QuantizationType { Int8=1 }`                           | [lib/segment/src/types.rs688-691](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L688-L691)                           |

Conversion uses `TryFrom` with error handling for invalid enum values:

Sources: [lib/collection/src/operations/conversions.rs81-114](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L81-L114) [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)

### Update Result Types

Update operations return status and optional metadata:

```
```

**Update Result Conversion**

The `UpdateResult` type supports asynchronous operation tracking:

Sources: [lib/collection/src/operations/types.rs399-423](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L399-L423) [lib/api/src/grpc/qdrant.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs)

## Type Safety and Error Handling

Type conversions handle errors through the `Result` type with specific error variants:

| Error Type         | Usage                  | Example                            |
| ------------------ | ---------------------- | ---------------------------------- |
| `tonic::Status`    | gRPC conversion errors | Invalid enum value, malformed UUID |
| `OperationError`   | Segment-level errors   | Invalid vector dimension           |
| `StorageError`     | Storage-level errors   | Collection not found               |
| `ValidationErrors` | Validation failures    | Out of range value                 |

Error conversion chain:

```
```

**Error Conversion Flow**

Sources: [lib/storage/src/content\_manager/conversions.rs22-63](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs#L22-L63) [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Data Types and Conversions](#data-types-and-conversions.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Type System Architecture](#type-system-architecture.md)
- [Core Data Types](#core-data-types.md)
- [Point Identifiers](#point-identifiers.md)
- [Vector Types](#vector-types.md)
- [Vector Configuration](#vector-configuration.md)
- [Payload Types](#payload-types.md)
- [Filter Conditions](#filter-conditions.md)
- [Conversion Mechanisms](#conversion-mechanisms.md)
- [REST to Internal Conversions](#rest-to-internal-conversions.md)
- [gRPC to Internal Conversions](#grpc-to-internal-conversions.md)
- [Bidirectional Conversions](#bidirectional-conversions.md)
- [Configuration Diff Types](#configuration-diff-types.md)
- [Type Validation](#type-validation.md)
- [Special Type Patterns](#special-type-patterns.md)
- [Datetime Handling](#datetime-handling.md)
- [Shard Key Selectors](#shard-key-selectors.md)
- [Enumeration Mappings](#enumeration-mappings.md)
- [Update Result Types](#update-result-types.md)
- [Type Safety and Error Handling](#type-safety-and-error-handling.md)
