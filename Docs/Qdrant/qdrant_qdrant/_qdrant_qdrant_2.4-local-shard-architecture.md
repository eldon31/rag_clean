Local Shard Architecture | qdrant/qdrant | DeepWiki

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

# Local Shard Architecture

Relevant source files

- [lib/collection/src/collection\_manager/collection\_updater.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs)
- [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)
- [lib/collection/src/shards/local\_shard/scroll.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs)
- [lib/collection/src/shards/local\_shard/snapshot.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs)
- [lib/collection/src/shards/local\_shard/snapshot\_tests.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot_tests.rs)
- [lib/collection/src/update\_handler.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs)

## Purpose and Scope

This document describes the internal architecture of `LocalShard`, which is the fundamental data storage and processing unit in Qdrant. A `LocalShard` encapsulates all components necessary for storing and indexing vector data on a single node, including segments, WAL (Write-Ahead Log), background optimization workers, and update coordination mechanisms.

For information about how multiple shards are coordinated across replicas, see [Shards and Replica Sets](qdrant/qdrant/2.3-shards-and-replica-sets.md). For details about segment internals and construction, see [Segment Lifecycle and Construction](qdrant/qdrant/2.5-segment-lifecycle-and-construction.md). For distributed operations like shard transfers, see [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md).

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs84-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L84-L124)

---

## Core Components Overview

A `LocalShard` is composed of several interacting subsystems:

| Component               | Type                                         | Purpose                                                        |
| ----------------------- | -------------------------------------------- | -------------------------------------------------------------- |
| `segments`              | `LockedSegmentHolder`                        | Container managing all segments in the shard                   |
| `wal`                   | `RecoverableWal`                             | Write-ahead log for durability and recovery                    |
| `update_handler`        | `Arc<Mutex<UpdateHandler>>`                  | Coordinates background workers for optimization and flushing   |
| `update_sender`         | `ArcSwap<Sender<UpdateSignal>>`              | Channel for sending update signals to workers                  |
| `update_tracker`        | `UpdateTracker`                              | Tracks ongoing update operations                               |
| `optimizers`            | `Arc<Vec<Arc<Optimizer>>>`                   | Collection of segment optimization strategies                  |
| `payload_index_schema`  | `Arc<SaveOnDisk<PayloadIndexSchema>>`        | Schema for payload field indices                               |
| `collection_config`     | `Arc<TokioRwLock<CollectionConfigInternal>>` | Collection configuration                                       |
| `update_operation_lock` | `Arc<tokio::sync::RwLock<()>>`               | Prevents updates during critical operations (scroll, snapshot) |

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs89-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L89-L124)

---

## LocalShard Internal Architecture

```
```

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs89-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L89-L124) [lib/collection/src/update\_handler.rs92-144](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L92-L144)

---

## Initialization and Loading

### Building a New LocalShard

When creating a new `LocalShard` from scratch, the `build()` method performs the following steps:

```
```

The number of initial segments is determined by `optimizer_config.get_number_segments()`. Each segment is built in parallel using dedicated threads to speed up initialization.

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs503-606](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L503-L606)

### Loading an Existing LocalShard

Recovery from disk follows a different path:

```
```

Key aspects:

- Segments are loaded in parallel (up to `MAX_CONCURRENT_SEGMENT_LOADS = 10`)
- Consistency checks and repairs are performed on each segment
- Deduplication removes any duplicate point IDs across segments
- WAL operations are replayed sequentially to restore the latest state
- A final flush ensures on-disk consistency

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs270-456](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L270-L456) [lib/collection/src/shards/local\_shard/mod.rs618-736](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L618-L736)

---

## UpdateHandler and Background Workers

The `UpdateHandler` manages three concurrent background workers that handle different aspects of shard maintenance:

### Worker Architecture

```
```

**Sources:** [lib/collection/src/update\_handler.rs92-144](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L92-L144) [lib/collection/src/update\_handler.rs193-252](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L193-L252)

### Update Worker

The **update worker** runs on a blocking thread and processes incoming update operations:

1. Receives `UpdateSignal` messages from the update queue
2. Acquires the `update_operation_lock` (write lock) to prevent conflicts with scrolls/snapshots
3. Writes operations to the WAL for durability
4. Applies operations to segments via `CollectionUpdater::update()`
5. Signals the optimizer worker after each operation
6. Handles recovery by re-applying failed operations

**Signal Types:**

- `UpdateSignal::Operation(OperationData)` - Apply a collection update operation
- `UpdateSignal::Stop` - Gracefully stop the worker
- `UpdateSignal::Nop` - Trigger optimizers without performing an operation
- `UpdateSignal::Plunger(oneshot::Sender)` - Wait for all previous updates to complete

**Sources:** [lib/collection/src/update\_handler.rs67-78](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L67-L78) [lib/collection/src/update\_handler.rs218-228](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L218-L228)

### Optimizer Worker

The **optimizer worker** runs as an async task and manages segment optimization:

1. Receives `OptimizerSignal` messages
2. Checks optimizer conditions to identify non-optimal segments
3. Launches optimization tasks up to `max_optimization_threads` limit
4. Manages CPU/IO resource budgets for optimization tasks
5. Cleans up finished optimization handles every `OPTIMIZER_CLEANUP_INTERVAL` (5 seconds)
6. Ensures at least one appendable segment with capacity exists

Each optimization task:

- Acquires a resource permit (IO threads for HNSW indexing)
- Runs the optimizer on specified segments
- Reports status via `Tracker` in `optimizers_log`
- Releases the resource permit on completion
- Triggers another optimizer check via callback

**Sources:** [lib/collection/src/update\_handler.rs620-753](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L620-L753) [lib/collection/src/update\_handler.rs324-484](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L324-L484)

### Flush Worker

The **flush worker** runs on a blocking thread and periodically persists data:

1. Wakes up every `flush_interval_sec` seconds
2. Flushes all segments to disk
3. Saves `LocalShardClocks` (newest/oldest clock maps)
4. Truncates the WAL up to the minimum flushed operation number
5. Respects `wal_keep_from` to prevent truncating operations still needed by other components

**Sources:** [lib/collection/src/update\_handler.rs238-249](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L238-L249)

### Worker Coordination

```
```

**Sources:** [lib/collection/src/update\_handler.rs193-252](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L193-L252)

---

## WAL and Clock Management

### RecoverableWal Structure

The `RecoverableWal` wrapper extends the base `SerdeWal` with logical clock tracking:

```
```

**Clock Management:**

- `newest_clocks` tracks the highest clock tag received from each peer
- `oldest_clocks` tracks the cutoff clock below which operations are guaranteed to be applied
- Clock tags enable optimistic replication without consensus (see [Write Consistency and Replication](qdrant/qdrant/6.2-write-consistency-and-replication.md))
- Clock files are persisted alongside segments during flushes

**Sources:** [lib/collection/src/wal\_delta.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/wal_delta.rs) (referenced in mod.rs:95,249), [lib/collection/src/shards/local\_shard/mod.rs76-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L76-L82)

### WAL Recovery Process

During `load_from_wal()`, operations are replayed to restore state:

```
```

Key behaviors:

- Operations are read from the first un-truncated WAL index
- Clock tags are advanced for each operation
- Transient errors (disk full, etc.) are tracked in `failed_operation` set for retry
- Service errors (corrupted data) abort recovery
- Other errors (NotFound) are logged but don't stop recovery
- Final flush ensures on-disk consistency even if only past operations were re-applied

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs618-736](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L618-L736)

---

## Segment Operations and Locking

### Update Operation Lock

The `update_operation_lock` is a critical synchronization primitive:

```
```

**Purpose:**

1. **Scroll consistency** - Prevents updates from modifying segments during scroll operations, ensuring consistent pagination for resharding and shard transfers
2. **Snapshot integrity** - Prevents updates during segment proxy/unproxy operations
3. **Read isolation** - Multiple reads can proceed concurrently (read locks are shared)

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs108-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L108-L124) [lib/collection/src/shards/local\_shard/scroll.rs156-213](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs#L156-L213) [lib/collection/src/collection\_manager/collection\_updater.rs42-78](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs#L42-L78)

---

## Snapshot Creation with Segment Proxying

Snapshot creation uses a sophisticated proxying mechanism to allow writes during the long-running snapshot process:

### Proxy Mechanism

```
```

**Key Steps:**

1. **Plunger signal** (if WAL not saved): Ensures all updates are flushed to segments before snapshotting
2. **Proxy creation**: All segments wrapped in `ProxySegment` that redirects writes to temporary segment
3. **Incremental unproxying**: Each segment unproxied immediately after snapshot to minimize temp segment growth
4. **Atomic finalization**: Last proxy and temp segment promoted together to maintain consistency
5. **Temp segment handling**: Added to collection if non-empty, otherwise deleted

**Sources:** [lib/collection/src/shards/local\_shard/snapshot.rs62-121](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L62-L121) [lib/collection/src/shards/local\_shard/snapshot.rs268-352](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L268-L352)

### Proxy Segment Structure

```
```

**Sources:** [lib/collection/src/shards/local\_shard/snapshot.rs268-352](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L268-L352)

---

## Disk Usage Monitoring

The `DiskUsageWatcher` component monitors shard disk usage and prevents excessive WAL growth:

```
```

The watcher uses a default threshold of `2 * wal_capacity_mb` to detect when the shard is using excessive disk space, which typically indicates the WAL has grown too large and needs truncation.

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs198-206](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L198-L206)

---

## LocalShard Lifecycle Operations

### Graceful Shutdown

```
```

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs824-835](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L824-L835) [lib/collection/src/update\_handler.rs254-290](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L254-L290)

### Optimizer Configuration Update

When optimizer configuration changes (e.g., flush interval, max optimization threads), the `UpdateHandler` must be restarted:

```
```

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs767-795](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L767-L795)

---

## Data Consistency and Recovery

### Failed Operation Tracking

The `SegmentHolder` maintains a `failed_operation` set containing operation numbers that failed with transient errors:

```
```

**Transient vs Non-Transient Errors:**

- **Transient:** Disk full, temporary I/O errors - will be retried
- **Non-Transient:** Point not found, invalid operation - logged but not retried

**Sources:** [lib/collection/src/collection\_manager/collection\_updater.rs17-40](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs#L17-L40) [lib/collection/src/update\_handler.rs293-319](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L293-L319)

### Data Consistency Check

When the `data-consistency-check` feature is enabled, the shard performs deep consistency validation after WAL recovery:

```
```

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs732-735](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L732-L735) [lib/collection/src/shards/local\_shard/mod.rs741-765](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L741-L765)

---

## Shard Status and Health Monitoring

The `LocalShard` reports its health status based on various conditions:

### Status Determination Logic

```
```

**Status Meanings:**

- **Red:** Failed operations or optimizer errors - shard is unhealthy
- **Yellow:** Proxy segments present (snapshotting/optimizing) or pending optimizations
- **Grey:** Suboptimal state but optimizers never triggered (prevents crash loop on startup)
- **Green:** All operations successful and no pending optimizations

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs879-936](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L879-L936)

---

## File System Layout

The `LocalShard` uses a well-defined directory structure:

```
<shard_path>/
├── wal/                      # Write-ahead log directory
│   ├── 00000000000000000000  # WAL segment files
│   └── 00000000000000000001
├── segments/                 # Segment storage directory
│   ├── <segment_id_1>/       # Individual segment directories
│   ├── <segment_id_2>/
│   └── ...
├── newest_clocks.json        # Highest clock tags from each peer
└── oldest_clocks.json        # Cutoff clocks (guaranteed applied)
```

**Path Construction:**

- `wal_path()` → `shard_path/wal`
- `segments_path()` → `shard_path/segments`

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs76-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L76-L82) [lib/collection/src/shards/local\_shard/mod.rs462-468](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L462-L468)

---

## Summary

The `LocalShard` is a sophisticated data management component that coordinates:

1. **Durable storage** via WAL and segment persistence
2. **Background optimization** through concurrent worker threads
3. **Update consistency** using locks and logical clocks
4. **Snapshot creation** with minimal write disruption via segment proxying
5. **Health monitoring** and automatic recovery from transient failures

Key design principles:

- **Separation of concerns:** Update, optimization, and flush workers operate independently
- **Non-blocking operations:** Segment proxying enables long operations without blocking writes
- **Robust recovery:** WAL replay and failed operation tracking ensure data integrity
- **Resource management:** Budget-based optimization prevents resource exhaustion

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs) [lib/collection/src/update\_handler.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Local Shard Architecture](#local-shard-architecture.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Core Components Overview](#core-components-overview.md)
- [LocalShard Internal Architecture](#localshard-internal-architecture.md)
- [Initialization and Loading](#initialization-and-loading.md)
- [Building a New LocalShard](#building-a-new-localshard.md)
- [Loading an Existing LocalShard](#loading-an-existing-localshard.md)
- [UpdateHandler and Background Workers](#updatehandler-and-background-workers.md)
- [Worker Architecture](#worker-architecture.md)
- [Update Worker](#update-worker.md)
- [Optimizer Worker](#optimizer-worker.md)
- [Flush Worker](#flush-worker.md)
- [Worker Coordination](#worker-coordination.md)
- [WAL and Clock Management](#wal-and-clock-management.md)
- [RecoverableWal Structure](#recoverablewal-structure.md)
- [WAL Recovery Process](#wal-recovery-process.md)
- [Segment Operations and Locking](#segment-operations-and-locking.md)
- [Update Operation Lock](#update-operation-lock.md)
- [Snapshot Creation with Segment Proxying](#snapshot-creation-with-segment-proxying.md)
- [Proxy Mechanism](#proxy-mechanism.md)
- [Proxy Segment Structure](#proxy-segment-structure.md)
- [Disk Usage Monitoring](#disk-usage-monitoring.md)
- [LocalShard Lifecycle Operations](#localshard-lifecycle-operations.md)
- [Graceful Shutdown](#graceful-shutdown.md)
- [Optimizer Configuration Update](#optimizer-configuration-update.md)
- [Data Consistency and Recovery](#data-consistency-and-recovery.md)
- [Failed Operation Tracking](#failed-operation-tracking.md)
- [Data Consistency Check](#data-consistency-check.md)
- [Shard Status and Health Monitoring](#shard-status-and-health-monitoring.md)
- [Status Determination Logic](#status-determination-logic.md)
- [File System Layout](#file-system-layout.md)
- [Summary](#summary.md)
