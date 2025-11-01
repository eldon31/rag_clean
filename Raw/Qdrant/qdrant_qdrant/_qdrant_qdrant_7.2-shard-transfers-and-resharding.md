Shard Transfers and Resharding | qdrant/qdrant | DeepWiki

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

# Shard Transfers and Resharding

Relevant source files

- [lib/collection/src/collection/collection\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs)
- [lib/collection/src/collection/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs)
- [lib/collection/src/collection/shard\_transfer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs)
- [lib/collection/src/collection/sharding\_keys.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs)
- [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)
- [lib/collection/src/shards/replica\_set/update.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs)
- [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs)

This page describes the mechanisms for transferring shard data between peers in a distributed Qdrant cluster, and the resharding process that reorganizes data distribution across shards. For information about the basic shard and replica architecture, see [Shards and Replica Sets](qdrant/qdrant/2.3-shards-and-replica-sets.md). For details on consensus coordination, see [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md).

Shard transfers enable:

- **Replica recovery**: Restoring dead or failed replicas from active ones
- **Cluster rebalancing**: Moving shards to new peers when scaling the cluster
- **Resharding**: Redistributing data when changing the number of shards

## Shard Transfer Concepts

A shard transfer moves data from one peer (source) to another peer (destination). Transfers are coordinated through Raft consensus and executed asynchronously with progress tracking.

### Transfer Descriptor

The `ShardTransfer` struct identifies and configures a transfer:

```
```

**Sources:** [lib/collection/src/collection/shard\_transfer.rs17-19](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L17-L19)

### Transfer Methods

Four transfer methods are supported, each using different replica states:

| Method                    | Replica State                         | Use Case          | Description                               |
| ------------------------- | ------------------------------------- | ----------------- | ----------------------------------------- |
| `StreamRecords`           | `Partial`                             | Default transfer  | Streams individual points                 |
| `Snapshot`                | `Recovery`                            | Large transfers   | Transfers snapshot files                  |
| `WalDelta`                | `Recovery`                            | Recent divergence | Transfers WAL operations since divergence |
| `ReshardingStreamRecords` | `Resharding` or `ReshardingScaleDown` | Resharding only   | Streams points during resharding          |

The method is selected based on cluster version compatibility and configuration. If all peers are version 1.8.0+, `WalDelta` is preferred; otherwise `StreamRecords` is used.

**Sources:** [lib/collection/src/collection/shard\_transfer.rs82-103](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L82-L103)

## Replica State Machine

Replica states govern which operations are allowed on a shard replica. The state transitions form the core of the transfer lifecycle:

```
```

**Key States:**

- **Initializing**: Newly created replica, not yet operational
- **Active**: Fully operational, serves reads and writes
- **Listener**: Read-only mode for listener nodes
- **Partial**: Receiving data via StreamRecords, accepts writes but incomplete data
- **Recovery**: Receiving snapshot/WAL, rejects normal writes (force flag required)
- **PartialSnapshot**: Temporarily set during snapshot transfer
- **Resharding/ReshardingScaleDown**: During resharding operations
- **Dead**: Failed replica, excluded from operations

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs48-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L48-L82) [lib/collection/src/shards/replica\_set/update.rs58-103](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L58-L103)

## Shard Transfer Lifecycle

### Initiation Phase

```
```

The transfer begins when a `ShardTransferOperations::Start` operation is committed through consensus:

1. **Validation**: Check that source peer exists and has the shard, destination peer exists, and no conflicting transfers exist
2. **State Registration**: Add transfer to `ShardHolder.shard_transfers`
3. **Replica Initialization**: Create or update destination replica with appropriate state (Partial/Recovery/Resharding)
4. **Task Spawning**: If sender is local, spawn background transfer task

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs390-480](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L390-L480) [lib/collection/src/collection/shard\_transfer.rs36-141](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L36-L141)

### Execution Phase

Transfer tasks run asynchronously in the background, managed by `TransferTasksPool`:

```
```

Each transfer method operates differently:

- **StreamRecords**: Scrolls through source shard, batches points, and updates destination
- **Snapshot**: Creates snapshot file, transfers to destination, destination recovers from snapshot
- **WalDelta**: Identifies WAL operations since cutoff point, replays on destination

The task updates `TransferTaskProgress` which can be queried for status. On completion or failure, callbacks propose consensus operations to finalize the transfer.

**Sources:** [lib/collection/src/collection/shard\_transfer.rs143-190](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L143-L190)

### Completion Phase

```
```

When transfer completes successfully:

1. **Stop Task**: Remove from `TransferTasksPool`

2. **Promote Destination**:

   - Regular transfer: `Partial`/`Recovery` → `Active`
   - Resharding transfer: Keep `Resharding`/`ReshardingScaleDown` state

3. **Handle Source**:

   - **Sync transfer**: Keep source replica (un-proxify if proxied)
   - **Non-sync transfer**: Remove source replica entirely

4. **Unregister Transfer**: Remove from `shard_transfers` state

**Sources:** [lib/collection/src/collection/shard\_transfer.rs195-300](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L195-L300)

### Abort/Failure Handling

```
```

Transfer abort handling depends on transfer type:

- **Regular sync transfer**: Mark destination as `Dead` (triggers recovery)
- **Regular non-sync transfer**: Remove destination replica entirely
- **Resharding transfer**: No state change (resharding abort handles cleanup)
- **Source handling**: If source was proxied, revert proxy to normal `LocalShard`

**Sources:** [lib/collection/src/collection/shard\_transfer.rs303-361](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L303-L361)

## Automatic Transfer Initiation

The system automatically initiates transfers to recover `Dead` replicas during `sync_local_state`:

```
```

Conditions for automatic recovery:

- Replica state is `Dead`
- At least one `Active` or `ReshardingScaleDown` remote replica exists
- No conflicting transfers exist
- Transfer limits not exceeded (incoming/outgoing per peer)
- Target peer passes health check

Transfer method is selected based on cluster version and configuration.

**Sources:** [lib/collection/src/collection/mod.rs686-776](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L686-L776)

## Resharding Operations

Resharding reorganizes data distribution by changing the number of shards in a collection. It is a multi-step process coordinated through consensus.

### Resharding State

```
```

### Resharding Lifecycle

```
```

**Resharding Steps:**

1. **Start**:

   - Create new target shards (scale-up) or identify source shard (scale-down)
   - Mark relevant replicas as `Resharding` or `ReshardingScaleDown`
   - Start transfers using `ReshardingStreamRecords` method

2. **MigratingPoints**: Transfer tasks execute in background, moving data

3. **CommitRead**: Switch read operations to new hash ring while writes still use old ring

4. **CommitWrite**: Switch write operations to new hash ring

5. **Finish**:

   - Promote resharding replicas to `Active`
   - Remove old shards (scale-down) or update routing
   - Clean up resharding state

6. **Abort**: Roll back any changes, remove temporary shards

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs306-376](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L306-L376) [lib/collection/src/collection/resharding.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/resharding.rs) (referenced but not in provided files)

### Scale-Up vs Scale-Down

**Scale-Up** (increase shard count):

- Creates new empty shards with `Resharding` state
- Transfers subset of data from existing shards to new shards
- New shards become `Active` when resharding finishes
- Original shards remain `Active` throughout

**Scale-Down** (decrease shard count):

- Marks shard-to-be-removed as `ReshardingScaleDown`
- Transfers all data from that shard to remaining shards
- Removes the scaled-down shard when resharding finishes
- Other shards remain `Active`, accepting transferred data

**Sources:** [lib/collection/src/collection/shard\_transfer.rs89-102](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L89-L102) [lib/collection/src/collection/shard\_transfer.rs241-257](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L241-L257)

## Transfer Task Management

### TransferTasksPool

The `TransferTasksPool` manages active transfer tasks:

```
```

Task pool operations:

- `add_task()`: Register new transfer task with progress tracker
- `stop_task()`: Cancel running task and return result
- `get_task_status()`: Query current task progress

The pool allows Collection to track all active transfers and their progress, essential for reporting cluster state and handling failures.

**Sources:** [lib/collection/src/collection/shard\_transfer.rs154-189](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L154-L189) [lib/collection/src/shards/transfer/transfer\_tasks\_pool.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/transfer/transfer_tasks_pool.rs) (referenced)

## Consensus Integration

Shard transfers integrate tightly with Raft consensus:

### Consensus Operations

```
```

Each operation is proposed through consensus and applied on all peers when committed. This ensures all peers agree on:

- Which transfers are active
- Current state of each replica
- When transfers complete or fail

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs390-603](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L390-L603)

### Transfer Validation

Before starting a transfer, the system validates:

1. **Peer existence**: Source and destination peers are in the cluster
2. **Shard existence**: Source shard exists with active replicas
3. **No conflicts**: No other transfer affects the same replica
4. **State consistency**: Source is not in recovery/partial state

Validation prevents inconsistent states and transfer conflicts.

**Sources:** [lib/collection/src/shards/transfer/helpers.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/transfer/helpers.rs) (referenced), [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs423-430](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L423-L430)

## Shard Key Operations

Custom shard keys allow user-defined partitioning. Creating and dropping shard keys involves transfer-like operations:

### Creating Shard Key

```
```

New shards start in `Initializing` state (on version 1.14.2+) or `Active` state (older versions). The `Initializing` state ensures shards are properly set up before accepting traffic.

**Sources:** [lib/collection/src/collection/sharding\_keys.rs59-144](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs#L59-L144) [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs623-641](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L623-L641)

### Dropping Shard Key

Dropping a shard key:

1. Aborts any active resharding on that shard key
2. Invalidates shard cleaning tasks
3. Removes all shards associated with the key
4. Cancels related transfers (on version 1.9.0+)

**Sources:** [lib/collection/src/collection/sharding\_keys.rs146-191](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs#L146-L191)

## State Persistence

Transfer and resharding state is persisted to survive restarts:

- **ShardHolder state**: Stored in `shard_transfers` and `resharding_state` within `ShardHolder`
- **ReplicaSet state**: Each replica set persists its `replica_state.json` including peer states
- **Transfer progress**: Lost on restart; transfers restart from beginning

On recovery, the system:

1. Loads persisted replica states
2. Checks for in-progress transfers in consensus state
3. Re-initiates transfers as needed based on replica states (`Partial`/`Recovery`)

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs125](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L125-L125) [lib/collection/src/shards/replica\_set/mod.rs232-382](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L232-L382)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Shard Transfers and Resharding](#shard-transfers-and-resharding.md)
- [Shard Transfer Concepts](#shard-transfer-concepts.md)
- [Transfer Descriptor](#transfer-descriptor.md)
- [Transfer Methods](#transfer-methods.md)
- [Replica State Machine](#replica-state-machine.md)
- [Shard Transfer Lifecycle](#shard-transfer-lifecycle.md)
- [Initiation Phase](#initiation-phase.md)
- [Execution Phase](#execution-phase.md)
- [Completion Phase](#completion-phase.md)
- [Abort/Failure Handling](#abortfailure-handling.md)
- [Automatic Transfer Initiation](#automatic-transfer-initiation.md)
- [Resharding Operations](#resharding-operations.md)
- [Resharding State](#resharding-state.md)
- [Resharding Lifecycle](#resharding-lifecycle.md)
- [Scale-Up vs Scale-Down](#scale-up-vs-scale-down.md)
- [Transfer Task Management](#transfer-task-management.md)
- [TransferTasksPool](#transfertaskspool.md)
- [Consensus Integration](#consensus-integration.md)
- [Consensus Operations](#consensus-operations.md)
- [Transfer Validation](#transfer-validation.md)
- [Shard Key Operations](#shard-key-operations.md)
- [Creating Shard Key](#creating-shard-key.md)
- [Dropping Shard Key](#dropping-shard-key.md)
- [State Persistence](#state-persistence.md)
