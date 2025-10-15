Query Request Flow | qdrant/qdrant | DeepWiki

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

# Query Request Flow

Relevant source files

- [docs/grpc/docs.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/grpc/docs.md)
- [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json)
- [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)
- [lib/api/src/grpc/proto/collections.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto)
- [lib/api/src/grpc/proto/points.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto)
- [lib/api/src/grpc/qdrant.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs)
- [lib/collection/src/collection\_manager/collection\_updater.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs)
- [lib/collection/src/config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs)
- [lib/collection/src/operations/config\_diff.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs)
- [lib/collection/src/operations/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs)
- [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs)
- [lib/collection/src/optimizers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/optimizers_builder.rs)
- [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)
- [lib/collection/src/shards/local\_shard/scroll.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs)
- [lib/collection/src/shards/local\_shard/snapshot.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs)
- [lib/collection/src/shards/local\_shard/snapshot\_tests.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot_tests.rs)
- [lib/collection/src/update\_handler.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs)
- [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)
- [lib/storage/src/content\_manager/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/collection_meta_ops.rs)
- [lib/storage/src/content\_manager/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs)

## Purpose and Scope

This document describes how query and search requests are processed in Qdrant, tracing the execution path from initial API request through collection routing, shard selection, and segment-level search operations. It covers the complete flow of search queries, including request validation, shard selection, read consistency enforcement, and result merging.

For information about specific filtering and scoring mechanisms, see [Filtering and Scoring](qdrant/qdrant/5.2-filtering-and-scoring.md). For details on data updates and write operations, see [Update Processing Pipeline](qdrant/qdrant/6.1-update-processing-pipeline.md).

## Query Request Flow Overview

Query requests in Qdrant flow through multiple layers, with each layer performing specific responsibilities: request validation, shard routing, replica selection, segment search coordination, and result aggregation.

```
```

**Sources:**

- [lib/collection/src/shards/local\_shard/search.rs1-400](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/search.rs#L1-L400)
- Diagram 3 from high-level architecture

## Request Types and Entry Points

Qdrant supports multiple query types that enter through REST and gRPC APIs. All requests are converted to internal representations for processing.

### Core Request Types

| Request Type       | Purpose                                         | Internal Type              |
| ------------------ | ----------------------------------------------- | -------------------------- |
| `SearchRequest`    | Vector similarity search                        | `CoreSearchRequest`        |
| `QueryRequest`     | Universal query API (search, scroll, recommend) | `ShardQueryRequest`        |
| `ScrollRequest`    | Paginated retrieval                             | `ScrollRequestInternal`    |
| `RecommendRequest` | Recommendation by examples                      | `RecommendRequestInternal` |

```
```

**Key Fields in CoreSearchRequest:**

- `query: QueryEnum` - The query vector or strategy
- `filter: Option<Filter>` - Payload filtering conditions
- `params: Option<SearchParams>` - HNSW parameters, quantization settings
- `limit: usize` - Maximum results to return
- `offset: usize` - Pagination offset
- `with_payload: WithPayloadInterface` - Payload fields to include
- `with_vector: WithVector` - Whether to return vectors

**Sources:**

- [lib/collection/src/operations/types.rs554-575](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L554-L575)
- [lib/api/src/grpc/qdrant.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L1-L100)
- [lib/collection/src/operations/conversions.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L1-L100)

## Collection-Level Request Routing

The `Collection` layer receives requests and routes them to the appropriate shards based on shard keys (if using custom sharding) or distributes across all shards (if using auto sharding).

```
```

**Sharding Method Determination:**

- **Auto Sharding**: Request is sent to all `ShardReplicaSet` instances, and results are merged

- **Custom Sharding**: `shard_key` field in request determines which shards to query

  - Shard keys can be keywords or numbers
  - Multiple shard keys can be specified via `ShardKeySelector`

**Sources:**

- [lib/collection/src/config.rs76-84](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs#L76-L84)
- [lib/api/src/grpc/conversions.rs92-105](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs#L92-L105)
- [lib/collection/src/operations/types.rs554-595](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L554-L595)

## ReplicaSet Selection and Read Consistency

The `ShardReplicaSet` selects which replica to query based on read consistency requirements and replica health status.

### Replica Selection Algorithm

```
```

**Read Consistency Levels:**

| Level                | Behavior                                          | Use Case                                     |
| -------------------- | ------------------------------------------------- | -------------------------------------------- |
| `None` / `Factor(1)` | Query single local replica (preferred)            | Low latency, eventual consistency acceptable |
| `Majority`           | Query majority of replicas, return common results | Balance of consistency and performance       |
| `Quorum`             | Query n/2 + 1 replicas                            | Stronger consistency guarantees              |
| `All`                | Query all replicas, return results present in all | Strongest consistency, highest latency       |
| `Factor(n)`          | Query n replicas                                  | Custom consistency level                     |

**Replica State Filtering:**

Only replicas in `Active` state are queried. Replicas in other states (`Dead`, `Partial`, `Initializing`, `Listener`) are excluded from search operations.

**Sources:**

- [lib/collection/src/operations/point\_ops.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/point_ops.rs#L1-L100)
- [lib/collection/src/shards/replica\_set.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set.rs#L1-L100)
- [lib/collection/src/operations/conversions.rs91-114](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs#L91-L114)

## LocalShard Search Execution

The `LocalShard` coordinates search across all segments, acquiring locks to ensure read consistency with concurrent updates.

### Search Coordination Flow

```
```

**Key Components:**

- **`update_operation_lock`**: A `tokio::sync::RwLock` that prevents updates during critical read operations

  - Read lock held during search to ensure consistency
  - Write lock held during updates
  - Critical for scroll operations and shard transfers

- **`SegmentHolder`**: Manages all segments in the shard

  - Segments are searched in parallel
  - Each segment returns partial results
  - Results are merged based on scores

**Batch Processing:**

The `core_search_batch()` method processes multiple search requests concurrently:

- Requests in batch share the same read lock acquisition
- Segment searches for different requests run in parallel
- Results for each request are returned as separate vectors

**Sources:**

- [lib/collection/src/shards/local\_shard/search.rs1-200](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/search.rs#L1-L200)
- [lib/collection/src/shards/local\_shard/mod.rs108-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L108-L124)
- [lib/collection/src/collection\_manager/segments\_searcher.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/segments_searcher.rs#L1-L100)

## Segment-Level Search Operations

Each segment performs the actual vector search, combining payload filtering with vector similarity computation.

### Segment Search Process

```
```

**Filter Application:**

Payload filters are applied before vector search to narrow the search space:

1. **Filter parsing**: `Filter` conditions converted to queries for payload indices
2. **Index lookup**: `FieldIndex` instances (numeric, keyword, geo, etc.) return matching point IDs
3. **Cardinality estimation**: Estimated number of matching points determines search strategy
4. **Threshold check**: If estimated points < `full_scan_threshold`, use brute force; otherwise use HNSW

**HNSW Search Strategy:**

When using HNSW index:

- **Entry point selection**: Find entry node in HNSW graph
- **Greedy search**: Navigate down layers to level 0
- **Beam search**: Explore level 0 with configurable `ef` parameter
- **Filtered search**: Only visit points matching payload filter

**Quantization-Aware Search:**

If quantization is enabled (scalar, product, or binary):

1. Search using quantized vectors for speed
2. Retrieve top candidates (with oversampling if configured)
3. Rescore candidates using original vectors for accuracy
4. Return refined results

**Sources:**

- [lib/segment/src/types.rs471-546](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L471-L546)
- [lib/collection/src/operations/types.rs25-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L25-L60)
- Diagram 3 from high-level architecture

## Result Merging and Response Construction

Results from multiple segments (and potentially multiple shards) are merged to produce the final response.

### Multi-Level Result Merging

```
```

**Merging Algorithm:**

1. **Segment-level merge** (in `LocalShard`):

   - Collect results from all segments
   - Sort by score (considering distance metric)
   - Take top `limit + offset` results
   - Handle pagination by skipping `offset` items

2. **Shard-level merge** (in `Collection`):

   - For auto-sharding: merge results from all shards
   - For custom sharding: only results from queried shards
   - Re-sort combined results
   - Apply final limit

**Score Ordering:**

The ordering depends on the distance metric:

- **Cosine, Dot**: Larger scores are better (`Order::LargeBetter`)
- **Euclid, Manhattan**: Smaller scores are better (`Order::SmallBetter`)

**Response Construction:**

Final `ScoredPoint` objects contain:

- `id`: Point ID (numeric or UUID)
- `score`: Distance/similarity score
- `payload`: Requested payload fields (if `with_payload` specified)
- `vector`: Point vector(s) (if `with_vector` specified)
- `shard_key`: Shard key for custom sharding
- `order_value`: For order\_by queries

**Sources:**

- [lib/segment/src/types.rs349-366](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L349-L366)
- [lib/segment/src/types.rs327-341](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L327-L341)
- [lib/collection/src/operations/types.rs131-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L131-L143)

## Search Parameters and Optimization

Search behavior is controlled by `SearchParams` which configure HNSW search, quantization, and exactness requirements.

### SearchParams Structure

| **Field**      | **Type**                           | **Purpose**                                     |
| -------------- | ---------------------------------- | ----------------------------------------------- |
| `hnsw_ef`      | `Option<usize>`                    | HNSW beam size (higher = more accurate, slower) |
| `exact`        | `bool`                             | Force exact search (bypass HNSW)                |
| `quantization` | `Option<QuantizationSearchParams>` | Quantization settings                           |
| `indexed_only` | `bool`                             | Only search indexed segments                    |

**Quantization Search Parameters:**

- `ignore`: Skip quantized vectors entirely
- `rescore`: Force rescoring with original vectors
- `oversampling`: Factor for retrieving extra candidates before rescoring
  - Example: `oversampling = 2.4` with `limit = 100` retrieves 240 candidates, then rescores to get top 100

**HNSW Parameters:**

The `hnsw_ef` parameter controls search accuracy vs. speed tradeoff:

- Default: Uses collection's `ef_construct` value
- Higher values: More neighbors explored, better recall, slower search
- Lower values: Fewer neighbors explored, lower recall, faster search

**Sources:**

- [lib/segment/src/types.rs471-546](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L471-L546)
- [lib/collection/src/operations/types.rs25-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L25-L60)

## Query Timeout and Cancellation

Queries can specify timeout values to prevent long-running searches from blocking resources.

### Timeout Handling

```
```

**Timeout Mechanisms:**

1. **API-level timeout**: Specified in request, applied at collection level
2. **Segment-level timeout**: Propagated to individual segment searches
3. **Cancellation**: Operations check for timeout between segments and during HNSW traversal

**Error Response:**

When timeout occurs:

- Error type: `CollectionError::timeout()`
- HTTP status: 408 Request Timeout
- gRPC status: `DEADLINE_EXCEEDED`

**Sources:**

- [lib/collection/src/operations/types.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L1-L100)
- [lib/collection/src/shards/local\_shard/scroll.rs40-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs#L40-L60)

## Read Lock Acquisition for Consistency

The `update_operation_lock` ensures that queries have a consistent view of data during execution, preventing race conditions with concurrent updates.

### Locking Strategy

**Lock Type**: `Arc<tokio::sync::RwLock<()>>`

**Read Lock Held By:**

- Search operations
- Scroll operations
- Point retrieval operations
- Snapshot creation (partial)

**Write Lock Held By:**

- Update operations (upsert, delete)
- Segment optimization
- Snapshot proxy wrapping/unwrapping

**Lock Acquisition Timing:**

```
```

**Consistency Guarantees:**

- **Snapshot isolation**: Queries see a consistent snapshot of data
- **No torn reads**: Point data (vector + payload) are read atomically
- **Scroll consistency**: Paginated scrolls see same data version across pages

**Sources:**

- [lib/collection/src/shards/local\_shard/mod.rs108-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L108-L124)
- [lib/collection/src/update\_handler.rs135-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L135-L143)
- [lib/collection/src/collection\_manager/collection\_updater.rs40-60](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs#L40-L60)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Query Request Flow](#query-request-flow.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Query Request Flow Overview](#query-request-flow-overview.md)
- [Request Types and Entry Points](#request-types-and-entry-points.md)
- [Core Request Types](#core-request-types.md)
- [Collection-Level Request Routing](#collection-level-request-routing.md)
- [ReplicaSet Selection and Read Consistency](#replicaset-selection-and-read-consistency.md)
- [Replica Selection Algorithm](#replica-selection-algorithm.md)
- [LocalShard Search Execution](#localshard-search-execution.md)
- [Search Coordination Flow](#search-coordination-flow.md)
- [Segment-Level Search Operations](#segment-level-search-operations.md)
- [Segment Search Process](#segment-search-process.md)
- [Result Merging and Response Construction](#result-merging-and-response-construction.md)
- [Multi-Level Result Merging](#multi-level-result-merging.md)
- [Search Parameters and Optimization](#search-parameters-and-optimization.md)
- [SearchParams Structure](#searchparams-structure.md)
- [Query Timeout and Cancellation](#query-timeout-and-cancellation.md)
- [Timeout Handling](#timeout-handling.md)
- [Read Lock Acquisition for Consistency](#read-lock-acquisition-for-consistency.md)
- [Locking Strategy](#locking-strategy.md)
