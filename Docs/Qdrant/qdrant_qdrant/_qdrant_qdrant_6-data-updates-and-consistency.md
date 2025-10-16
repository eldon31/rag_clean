Data Updates and Consistency | qdrant/qdrant | DeepWiki

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

# Data Updates and Consistency

Relevant source files

- [lib/collection/src/collection/collection\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs)
- [lib/collection/src/collection/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs)
- [lib/collection/src/collection/shard\_transfer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs)
- [lib/collection/src/collection/sharding\_keys.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs)
- [lib/collection/src/collection\_manager/collection\_updater.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs)
- [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)
- [lib/collection/src/shards/local\_shard/scroll.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs)
- [lib/collection/src/shards/local\_shard/snapshot.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs)
- [lib/collection/src/shards/local\_shard/snapshot\_tests.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot_tests.rs)
- [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)
- [lib/collection/src/shards/replica\_set/update.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs)
- [lib/collection/src/update\_handler.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs)
- [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs)

This page describes how Qdrant handles data updates and maintains consistency across replicas. It covers the write path architecture, durability guarantees through Write-Ahead Logs, logical clock-based consistency mechanisms, and the interaction between update handlers, segments, and replicas.

For detailed information about the update processing pipeline (WAL persistence, segment updates, optimization triggers), see [Update Processing Pipeline](qdrant/qdrant/6.1-update-processing-pipeline.md). For write consistency levels, replica coordination, and failure handling mechanisms, see [Write Consistency and Replication](qdrant/qdrant/6.2-write-consistency-and-replication.md).

For information about the search and query flow, see [Search and Query Processing](qdrant/qdrant/5-search-and-query-processing.md).

---

## Write Path Overview

When a client submits an update operation (upsert, delete, set payload, etc.), it flows through multiple layers of the system before being persisted to disk. The system provides configurable consistency guarantees and handles replica coordination, failure detection, and automatic recovery.

### High-Level Write Flow

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs24-251](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L24-L251) [lib/collection/src/shards/local\_shard/mod.rs84-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L84-L124)

---

## Write-Ahead Log (WAL)

The Write-Ahead Log ensures durability and enables crash recovery. All update operations are written to the WAL before being applied to in-memory segments, guaranteeing that no acknowledged writes are lost.

### WAL Architecture

The `RecoverableWal` wrapper extends the basic WAL with clock tracking for consistency:

```
```

**Key Components:**

| Component       | Type                                          | Purpose                                 |
| --------------- | --------------------------------------------- | --------------------------------------- |
| `wal`           | `Arc<Mutex<SerdeWal<OperationWithClockTag>>>` | Underlying WAL implementation           |
| `newest_clocks` | `Arc<Mutex<ClockMap>>`                        | Highest clock values seen for each peer |
| `oldest_clocks` | `Arc<Mutex<ClockMap>>`                        | Cutoff clocks for recovery              |

**Sources:** [lib/collection/src/wal\_delta.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/wal_delta.rs) (referenced), [lib/collection/src/shards/local\_shard/mod.rs95](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L95-L95)

### WAL Recovery

On shard startup, the WAL is replayed to restore the state:

```
```

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs618-736](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L618-L736)

---

## Logical Clocks and Consistency

Qdrant uses logical clocks (Lamport-style) to establish a partial ordering of operations across replicas. This enables detection of stale operations and ensures convergence without requiring synchronized physical clocks.

### Clock Tag Structure

Every update operation is tagged with a `ClockTag`:

| Field        | Type     | Description                                    |
| ------------ | -------- | ---------------------------------------------- |
| `peer_id`    | `PeerId` | ID of the peer that created this clock tick    |
| `clock_id`   | `u32`    | Identifies the specific clock instance         |
| `clock_tick` | `u64`    | Monotonically increasing counter               |
| `force`      | `bool`   | If true, bypass clock rejection (for recovery) |

**Sources:** [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs) (referenced in update.rs)

### ClockSet and Clock Assignment

The `ShardReplicaSet` maintains a `ClockSet` that assigns clock tags to new operations:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs195-251](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L195-L251) [lib/collection/src/shards/replica\_set/clock\_set.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/clock_set.rs) (referenced)

### Clock-Based Rejection

Replicas track the highest clock tick seen from each peer in their `ClockMap`. Operations with older ticks are rejected to prevent applying stale updates:

- **Operation tick > newest tick**: Operation is applied, `newest_clocks` is updated
- **Operation tick <= newest tick**: Operation is rejected with `UpdateStatus::ClockRejected`
- **Operation has `force=true`**: Clock check is bypassed (used during recovery)

When an operation is rejected, the replica set retries with a new clock tick up to `UPDATE_MAX_CLOCK_REJECTED_RETRIES` (3) times.

**Sources:** [lib/collection/src/shards/replica\_set/update.rs16-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L16-L20) [lib/collection/src/shards/replica\_set/update.rs212-244](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L212-L244)

---

## Update Handler Architecture

The `UpdateHandler` manages three types of background workers that process updates, optimize segments, and periodically flush data to disk.

### Worker Types

```
```

**Sources:** [lib/collection/src/update\_handler.rs92-144](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L92-L144) [lib/collection/src/update\_handler.rs193-252](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L193-L252)

### Update Signal Types

| Signal                         | Purpose                                               |
| ------------------------------ | ----------------------------------------------------- |
| `Operation(OperationData)`     | Contains the update operation to apply                |
| `Stop`                         | Gracefully stops all workers                          |
| `Nop`                          | Trigger signal to wake optimizers                     |
| `Plunger(oneshot::Sender<()>)` | Ensures previous updates are applied before notifying |

**Sources:** [lib/collection/src/update\_handler.rs66-78](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L66-L78)

---

## Update Processing Pipeline

When an update operation arrives at a `LocalShard`, it goes through a multi-stage pipeline:

### Pipeline Stages

```
```

**Sources:** [lib/collection/src/shards/shard\_trait.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/shard_trait.rs) (referenced), [lib/collection/src/shards/local\_shard/shard\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/shard_ops.rs) (referenced)

### CollectionUpdater

The `CollectionUpdater` applies operations to segments:

```
```

**Sources:** [lib/collection/src/collection\_manager/collection\_updater.rs42-78](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs#L42-L78)

---

## Write Consistency Models

Qdrant provides three write ordering levels that control consistency vs. availability tradeoffs.

### WriteOrdering Levels

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs168-175](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L168-L175)

### Leader Selection

The leader for an update is determined by the `WriteOrdering`:

| Ordering | Leader Selection                                     | Lock Required               |
| -------- | ---------------------------------------------------- | --------------------------- |
| `Weak`   | Always local peer                                    | No                          |
| `Medium` | Highest peer ID that is alive (Active or Resharding) | Yes (`write_ordering_lock`) |
| `Strong` | Highest peer ID (even if dead)                       | Yes (`write_ordering_lock`) |

If the local peer is not the leader, the update is forwarded to the designated leader via internal gRPC.

**Sources:** [lib/collection/src/shards/replica\_set/update.rs136-165](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L136-L165)

### Write Consistency Factor

After applying an update to replicas, the `ShardReplicaSet` checks if enough replicas succeeded:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs355-542](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L355-L542)

### Replica Failure Handling

When a replica fails to apply an update:

1. **Transient errors** (network issues, timeouts): Replica is marked as locally disabled
2. **Non-transient errors** (validation failures): Only deactivated if there are full-completed updates
3. **Locally disabled replicas**: Not considered for read or write operations
4. **Consensus notification**: After timeout (30s default), failures are reported to consensus
5. **Automatic recovery**: Failed replicas eventually recover via shard transfer

**Sources:** [lib/collection/src/shards/replica\_set/update.rs409-542](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L409-L542) [lib/collection/src/shards/replica\_set/mod.rs94-98](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L94-L98)

---

## Key Data Structures

### LocalShard

The `LocalShard` is the core data-holding component on each peer:

| Field                   | Type                            | Purpose                                     |
| ----------------------- | ------------------------------- | ------------------------------------------- |
| `segments`              | `LockedSegmentHolder`           | Holds all segment data                      |
| `wal`                   | `RecoverableWal`                | Write-ahead log for durability              |
| `update_handler`        | `Arc<Mutex<UpdateHandler>>`     | Manages update processing workers           |
| `update_sender`         | `ArcSwap<Sender<UpdateSignal>>` | Channel to send updates to workers          |
| `update_tracker`        | `UpdateTracker`                 | Tracks ongoing updates                      |
| `update_operation_lock` | `Arc<RwLock<()>>`               | Prevents updates during critical operations |
| `optimizers`            | `Arc<Vec<Arc<Optimizer>>>`      | Segment optimization strategies             |

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs84-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L84-L124)

### ShardReplicaSet

The `ShardReplicaSet` coordinates replicas of a single shard:

| Field                    | Type                               | Purpose                                      |
| ------------------------ | ---------------------------------- | -------------------------------------------- |
| `local`                  | `RwLock<Option<Shard>>`            | Local shard instance if present              |
| `remotes`                | `RwLock<Vec<RemoteShard>>`         | Remote shard proxies                         |
| `replica_state`          | `Arc<SaveOnDisk<ReplicaSetState>>` | Persisted replica states                     |
| `locally_disabled_peers` | `RwLock<Registry>`                 | Peers marked as failed locally               |
| `write_ordering_lock`    | `Mutex<()>`                        | Serializes writes for Medium/Strong ordering |
| `clock_set`              | `Mutex<ClockSet>`                  | Assigns logical clocks                       |

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs90-119](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L90-L119)

### UpdateHandler

Manages background workers for updates, optimization, and flushing:

| Field                  | Type                                         | Purpose                         |
| ---------------------- | -------------------------------------------- | ------------------------------- |
| `segments`             | `LockedSegmentHolder`                        | Reference to segments           |
| `wal`                  | `LockedWal`                                  | Reference to WAL                |
| `optimizers`           | `Arc<Vec<Arc<Optimizer>>>`                   | List of optimization strategies |
| `update_worker`        | `Option<JoinHandle<()>>`                     | Update processing worker        |
| `optimizer_worker`     | `Option<JoinHandle<()>>`                     | Optimization worker             |
| `flush_worker`         | `Option<JoinHandle<()>>`                     | Periodic flush worker           |
| `optimization_handles` | `Arc<Mutex<Vec<StoppableTaskHandle<bool>>>>` | Active optimization tasks       |

**Sources:** [lib/collection/src/update\_handler.rs92-144](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/update_handler.rs#L92-L144)

---

## Update Operation Lock

The `update_operation_lock` is a `RwLock` that prevents data races between updates and certain read operations:

**Write lock held during:**

- Update operations (point upsert/delete, vector updates, payload operations)

**Read lock held during:**

- Scroll operations (ensuring consistent iteration)
- Snapshot creation (preventing segment changes)

This lock ensures that scroll operations see a consistent view of the data and that snapshots capture a coherent state.

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs108-123](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L108-L123) [lib/collection/src/shards/local\_shard/scroll.rs156-157](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs#L156-L157) [lib/collection/src/shards/local\_shard/snapshot.rs93-106](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L93-L106)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Data Updates and Consistency](#data-updates-and-consistency.md)
- [Write Path Overview](#write-path-overview.md)
- [High-Level Write Flow](#high-level-write-flow.md)
- [Write-Ahead Log (WAL)](#write-ahead-log-wal.md)
- [WAL Architecture](#wal-architecture.md)
- [WAL Recovery](#wal-recovery.md)
- [Logical Clocks and Consistency](#logical-clocks-and-consistency.md)
- [Clock Tag Structure](#clock-tag-structure.md)
- [ClockSet and Clock Assignment](#clockset-and-clock-assignment.md)
- [Clock-Based Rejection](#clock-based-rejection.md)
- [Update Handler Architecture](#update-handler-architecture.md)
- [Worker Types](#worker-types.md)
- [Update Signal Types](#update-signal-types.md)
- [Update Processing Pipeline](#update-processing-pipeline.md)
- [Pipeline Stages](#pipeline-stages.md)
- [CollectionUpdater](#collectionupdater.md)
- [Write Consistency Models](#write-consistency-models.md)
- [WriteOrdering Levels](#writeordering-levels.md)
- [Leader Selection](#leader-selection.md)
- [Write Consistency Factor](#write-consistency-factor.md)
- [Replica Failure Handling](#replica-failure-handling.md)
- [Key Data Structures](#key-data-structures.md)
- [LocalShard](#localshard.md)
- [ShardReplicaSet](#shardreplicaset.md)
- [UpdateHandler](#updatehandler.md)
- [Update Operation Lock](#update-operation-lock.md)
