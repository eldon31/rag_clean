Search and Query Processing | qdrant/qdrant | DeepWiki

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

# Search and Query Processing

Relevant source files

- [lib/collection/benches/batch\_query\_bench.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/benches/batch_query_bench.rs)
- [lib/collection/benches/batch\_search\_bench.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/benches/batch_search_bench.rs)
- [lib/collection/src/collection\_manager/collection\_updater.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs)
- [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)
- [lib/collection/src/shards/local\_shard/scroll.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs)
- [lib/collection/src/shards/local\_shard/snapshot.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs)
- [lib/collection/src/shards/local\_shard/snapshot\_tests.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot_tests.rs)
- [lib/collection/src/tests/snapshot\_test.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/tests/snapshot_test.rs)
- [lib/collection/src/update\_handler.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs)

This document covers the query processing pipeline in Qdrant, from API request parsing through query execution and result aggregation. It explains how different query types are processed, planned, and executed across shards to return search results.

For information about vector indexing strategies, see [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md). For details about scoring and ranking mechanisms, see [Scoring and Ranking](qdrant/qdrant/4.2-index-selection-and-storage-backends.md). For query types and API interfaces, see [Query Types and Options](qdrant/qdrant/4.1-field-index-types.md).

## Query Processing Overview

Qdrant supports multiple types of vector search operations that are processed through a unified query pipeline. The system transforms user requests into optimized execution plans that can be efficiently executed across distributed shards.

```
```

Sources: [lib/collection/src/operations/types.rs587-623](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L587-L623) [lib/collection/src/operations/universal\_query/collection\_query.rs28-55](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/collection_query.rs#L28-L55) [lib/collection/src/operations/universal\_query/shard\_query.rs33-46](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/shard_query.rs#L33-L46)

## Core Query Types

The system processes several fundamental query types through a unified interface:

| Query Type          | Purpose                                            | Core Implementation          |
| ------------------- | -------------------------------------------------- | ---------------------------- |
| **Search**          | Vector similarity search                           | `CoreSearchRequest`          |
| **Recommend**       | Recommendation based on positive/negative examples | `RecommendRequestInternal`   |
| **Discover**        | Discovery with context pairs                       | `DiscoverRequestInternal`    |
| **Universal Query** | Flexible query with prefetch and fusion            | `CollectionQueryRequest`     |
| **Scroll**          | Paginated retrieval                                | `QueryScrollRequestInternal` |

```
```

Sources: [lib/collection/src/operations/types.rs603-622](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs#L603-L622) [lib/collection/src/operations/query\_enum.rs1-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/query_enum.rs#L1-L50) [lib/collection/src/operations/universal\_query/collection\_query.rs29-44](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/collection_query.rs#L29-L44)

## Search Parameters and Configuration

Search behavior is controlled through `SearchParams` which configures indexing, quantization, and execution parameters:

```
```

Sources: [lib/segment/src/types.rs482-503](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L482-L503) [lib/segment/src/types.rs448-471](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L448-L471)

## Query Planning and Optimization

The query planning system transforms high-level queries into optimized execution plans through the `PlannedQuery` structure:

```
```

Sources: [lib/collection/src/operations/universal\_query/planned\_query.rs17-32](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/planned_query.rs#L17-L32) [lib/collection/src/operations/universal\_query/planned\_query.rs69-95](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/planned_query.rs#L69-L95)

## Shard-Level Query Execution

Query execution occurs at the shard level through the `LocalShard::do_planned_query` method, which coordinates concurrent execution of searches and scrolls:

```
```

Sources: [lib/collection/src/shards/local\_shard/query.rs57-104](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/query.rs#L57-L104) [lib/collection/src/shards/local\_shard/query.rs146-180](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/query.rs#L146-L180)

## Result Processing and Scoring

Search results flow through multiple processing stages to apply scoring, filtering, and formatting:

```
```

Sources: [lib/collection/src/shards/local\_shard/query.rs106-145](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/query.rs#L106-L145) [lib/segment/src/types.rs325-342](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L325-L342)

## Request Flow Implementation

The complete request processing flow involves multiple layers of conversion and optimization:

```
```

Sources: [docs/redoc/master/openapi.json2-100](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L2-L100) [lib/collection/src/collection/query.rs1-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/query.rs#L1-L50) [lib/collection/src/shards/local\_shard/query.rs1-30](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/query.rs#L1-L30)

## Universal Query System

The universal query system provides a flexible interface for complex search operations with prefetch capabilities:

| Component    | Purpose                         | Implementation       |
| ------------ | ------------------------------- | -------------------- |
| **Prefetch** | Pre-gather candidate sets       | `CollectionPrefetch` |
| **Query**    | Main query operation            | `Query` enum         |
| **Fusion**   | Combine multiple result sets    | `FusionInternal`     |
| **Rescore**  | Re-rank with different criteria | `ScoringQuery`       |

```
```

Sources: [lib/collection/src/operations/universal\_query/collection\_query.rs85-120](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/collection_query.rs#L85-L120) [lib/collection/src/operations/universal\_query/shard\_query.rs33-70](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/shard_query.rs#L33-L70)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Search and Query Processing](#search-and-query-processing.md)
- [Query Processing Overview](#query-processing-overview.md)
- [Core Query Types](#core-query-types.md)
- [Search Parameters and Configuration](#search-parameters-and-configuration.md)
- [Query Planning and Optimization](#query-planning-and-optimization.md)
- [Shard-Level Query Execution](#shard-level-query-execution.md)
- [Result Processing and Scoring](#result-processing-and-scoring.md)
- [Request Flow Implementation](#request-flow-implementation.md)
- [Universal Query System](#universal-query-system.md)
