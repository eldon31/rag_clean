Update Processing Pipeline | qdrant/qdrant | DeepWiki

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

# Update Processing and Optimization

Relevant source files

- [lib/collection/src/collection\_manager/collection\_updater.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs)
- [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)
- [lib/collection/src/shards/local\_shard/scroll.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs)
- [lib/collection/src/shards/local\_shard/snapshot.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs)
- [lib/collection/src/shards/local\_shard/snapshot\_tests.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot_tests.rs)
- [lib/collection/src/update\_handler.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs)

This page covers Qdrant's update processing pipeline and segment optimization system. Update processing handles the ingestion and application of point operations (inserts, updates, deletes) to collection segments, while optimization manages background maintenance tasks that rebuild and consolidate segments for better performance.

For information about collection lifecycle management and configuration, see [Collection Management](qdrant/qdrant/5-search-and-query-processing.md). For details about snapshot creation and recovery mechanisms, see [Snapshots and Recovery](qdrant/qdrant/5.2-filtering-and-scoring.md).

## Overview

Qdrant's update processing and optimization system operates through three main worker processes managed by the `UpdateHandler`:

- **Update Worker**: Processes incoming point operations and applies them to segments
- **Optimizer Worker**: Monitors segment conditions and launches optimization tasks
- **Flush Worker**: Periodically flushes segment data to disk and manages WAL cleanup

The system uses a copy-on-write approach during optimization, allowing reads and writes to continue while segments are being rebuilt in the background.

## Update Handler Architecture

The `UpdateHandler` serves as the central coordinator for all update and optimization operations within a collection shard.

```
```

Sources: [lib/collection/src/update\_handler.rs87-129](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L87-L129) [lib/collection/src/update\_handler.rs172-205](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L172-L205)

## Update Processing Pipeline

### Update Worker

The update worker processes incoming operations sequentially, ensuring consistency and proper ordering.

```
```

The update worker handles several operation types:

| Signal Type | Purpose                    | Action                                  |
| ----------- | -------------------------- | --------------------------------------- |
| `Operation` | Point update/insert/delete | Apply to segments, trigger optimization |
| `Stop`      | Shutdown signal            | Graceful worker termination             |
| `Nop`       | Trigger optimization       | Signal optimizer without operation      |
| `Plunger`   | Synchronization            | Ensure previous updates are applied     |

Sources: [lib/collection/src/update\_handler.rs691-761](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L691-L761) [lib/collection/src/update\_handler.rs63-74](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L63-L74)

### Write-Ahead Log Integration

Updates are written to the WAL before being applied to segments, ensuring durability:

```
```

Sources: [lib/collection/src/update\_handler.rs706-714](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L706-L714) [lib/collection/src/update\_handler.rs831-834](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L831-L834)

## Optimization System

### Optimizer Types

Qdrant implements four main optimizers, each addressing specific segment maintenance needs:

#### Indexing Optimizer

Creates indexes for segments that exceed size thresholds but lack proper indexing:

```
```

Sources: [lib/collection/src/collection\_manager/optimizers/indexing\_optimizer.rs94-184](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/indexing_optimizer.rs#L94-L184)

#### Merge Optimizer

Consolidates small segments to maintain optimal segment count:

```
```

Sources: [lib/collection/src/collection\_manager/optimizers/merge\_optimizer.rs96-151](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/merge_optimizer.rs#L96-L151)

#### Vacuum Optimizer

Removes soft-deleted points and rebuilds fragmented indexes:

```
```

Sources: [lib/collection/src/collection\_manager/optimizers/vacuum\_optimizer.rs67-88](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/vacuum_optimizer.rs#L67-L88)

#### Config Mismatch Optimizer

Rebuilds segments when collection configuration changes require different segment parameters:

Sources: [lib/collection/src/collection\_manager/optimizers/config\_mismatch\_optimizer.rs104-215](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/config_mismatch_optimizer.rs#L104-L215)

### Optimization Process

The optimization process uses proxy segments to maintain availability during rebuilding:

```
```

Sources: [lib/collection/src/collection\_manager/optimizers/segment\_optimizer.rs576-685](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/segment_optimizer.rs#L576-L685)

## Segment Builder

The `SegmentBuilder` constructs optimized segments by combining data from multiple source segments:

```
```

Key building steps include:

1. **Data Copying**: Transfer vectors and payloads from source segments
2. **Index Building**: Create HNSW or other indexes based on configuration
3. **Quantization**: Apply vector compression if configured
4. **Defragmentation**: Reorganize data for better locality

Sources: [lib/segment/src/segment\_constructor/segment\_builder.rs459-685](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L459-L685)

## Resource Management

### CPU and IO Budgeting

Optimization tasks use resource permits to control concurrent operations:

```
```

Sources: [lib/collection/src/update\_handler.rs270-326](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L270-L326) [lib/collection/src/update\_handler.rs521-526](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L521-L526)

### Optimization Limits

The system enforces several limits to prevent resource exhaustion:

| Parameter                   | Purpose                               | Configuration    |
| --------------------------- | ------------------------------------- | ---------------- |
| `max_optimization_threads`  | Concurrent optimizations per shard    | Optimizer config |
| `optimizer_resource_budget` | CPU/IO permits available              | Global budget    |
| `max_segment_size_kb`       | Maximum segment size before splitting | Threshold config |

Sources: [lib/collection/src/update\_handler.rs121-123](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L121-L123) [lib/collection/src/collection\_manager/optimizers/segment\_optimizer.rs37-42](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/segment_optimizer.rs#L37-L42)

## Flush Operations

The flush worker manages periodic data persistence and WAL cleanup:

```
```

The flush interval is configurable through `flush_interval_sec`, with a default of 5 seconds in development mode.

Sources: [lib/collection/src/update\_handler.rs769-835](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L769-L835) [config/development.yaml28](https://github.com/qdrant/qdrant/blob/48203e41/config/development.yaml#L28-L28)

## Error Handling and Recovery

### Failed Operation Recovery

The system maintains tracking of failed operations and attempts recovery:

```
```

Sources: [lib/collection/src/update\_handler.rs247-265](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L247-L265)

### Optimization Cancellation

Optimizations can be cancelled gracefully, restoring original segments:

Sources: [lib/collection/src/update\_handler.rs381-396](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L381-L396) [lib/collection/src/collection\_manager/optimizers/segment\_optimizer.rs341-396](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/optimizers/segment_optimizer.rs#L341-L396)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Update Processing and Optimization](#update-processing-and-optimization.md)
- [Overview](#overview.md)
- [Update Handler Architecture](#update-handler-architecture.md)
- [Update Processing Pipeline](#update-processing-pipeline.md)
- [Update Worker](#update-worker.md)
- [Write-Ahead Log Integration](#write-ahead-log-integration.md)
- [Optimization System](#optimization-system.md)
- [Optimizer Types](#optimizer-types.md)
- [Indexing Optimizer](#indexing-optimizer.md)
- [Merge Optimizer](#merge-optimizer.md)
- [Vacuum Optimizer](#vacuum-optimizer.md)
- [Config Mismatch Optimizer](#config-mismatch-optimizer.md)
- [Optimization Process](#optimization-process.md)
- [Segment Builder](#segment-builder.md)
- [Resource Management](#resource-management.md)
- [CPU and IO Budgeting](#cpu-and-io-budgeting.md)
- [Optimization Limits](#optimization-limits.md)
- [Flush Operations](#flush-operations.md)
- [Error Handling and Recovery](#error-handling-and-recovery.md)
- [Failed Operation Recovery](#failed-operation-recovery.md)
- [Optimization Cancellation](#optimization-cancellation.md)
