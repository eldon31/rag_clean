Shards and Replica Sets | qdrant/qdrant | DeepWiki

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

# Shards and Replica Sets

Relevant source files

- [lib/collection/src/collection/collection\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs)
- [lib/collection/src/collection/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs)
- [lib/collection/src/collection/shard\_transfer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs)
- [lib/collection/src/collection/sharding\_keys.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs)
- [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)
- [lib/collection/src/shards/replica\_set/update.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs)
- [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs)

## Purpose and Scope

This document describes the `ShardReplicaSet` abstraction, which coordinates replicas of a single shard across multiple peers in a Qdrant cluster. It covers replica state management, write ordering guarantees, local vs remote shard coordination, and consistency mechanisms.

For information about the internal implementation of local shards (segments, WAL, optimization), see [Local Shard Architecture](qdrant/qdrant/2.4-local-shard-architecture.md). For information about collection-level shard distribution and routing, see [Collections and Table of Content](qdrant/qdrant/2.2-collections-and-table-of-content.md). For information about shard transfer operations and resharding, see [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md).

---

## Core Abstraction

### ShardReplicaSet Structure

The `ShardReplicaSet` is the primary abstraction for managing a set of replicas for a single shard. It handles both local replicas (hosted on the current peer) and remote replicas (proxies to other peers), ensuring consistency across all replicas.

```
```

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs84-119](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L84-L119)

The `ShardReplicaSet` struct contains:

| Field                    | Type                               | Purpose                                                 |
| ------------------------ | ---------------------------------- | ------------------------------------------------------- |
| `local`                  | `RwLock<Option<Shard>>`            | Local shard variant (Local, Dummy, QueueProxy, or None) |
| `remotes`                | `RwLock<Vec<RemoteShard>>`         | Remote shard proxies to other peers                     |
| `replica_state`          | `Arc<SaveOnDisk<ReplicaSetState>>` | Persisted replica state for all peers                   |
| `locally_disabled_peers` | `Registry`                         | Peers marked as failed locally, pending consensus       |
| `shard_id`               | `ShardId`                          | Unique identifier for this shard                        |
| `shard_key`              | `Option<ShardKey>`                 | Optional shard key for custom sharding                  |
| `write_ordering_lock`    | `Mutex<()>`                        | Serialization lock for strong/medium ordering           |
| `clock_set`              | `Mutex<ClockSet>`                  | Local clock for tagging operations                      |
| `write_rate_limiter`     | `Option<RateLimiter>`              | Optional rate limiting for strict mode                  |

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs90-119](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L90-L119)

### Local vs Remote Shards

The replica set distinguishes between local and remote shards:

```
```

**Local Shard Variants:**

- **`Shard::Local(LocalShard)`**: Fully functional local shard with segments, WAL, and indices
- **`Shard::Dummy(DummyShard)`**: Placeholder when in recovery mode or after load failure
- **`Shard::QueueProxy`**: Temporary proxy during snapshot creation, queues updates

**Remote Shards:**

- **`RemoteShard`**: Proxy that forwards operations to other peers via internal gRPC

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs91-92](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L91-L92) [lib/collection/src/shards/replica\_set/mod.rs400-413](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L400-L413)

---

## Replica State Management

### Replica States

Each replica in a `ShardReplicaSet` has a state that determines how it participates in read and write operations:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs48-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L48-L82)

| State                 | Description                               | Accepts Updates    | Serves Reads |
| --------------------- | ----------------------------------------- | ------------------ | ------------ |
| `Active`              | Fully operational replica                 | Yes                | Yes          |
| `Dead`                | Failed or unavailable replica             | No                 | No           |
| `Initializing`        | Newly created, not yet activated          | Yes                | No           |
| `Listener`            | Read-only replica on listener node        | Yes (async)        | Yes          |
| `Partial`             | Receiving shard transfer (stream records) | Yes                | No           |
| `Recovery`            | Receiving snapshot/WAL delta transfer     | No (unless forced) | No           |
| `PartialSnapshot`     | Creating snapshot for transfer            | No (unless forced) | No           |
| `Resharding`          | Participating in scale-up resharding      | Yes                | Yes          |
| `ReshardingScaleDown` | Participating in scale-down resharding    | Yes                | Yes          |

**Sources:** [lib/collection/src/shards/replica\_set/update.rs58-103](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L58-L103) [lib/collection/src/shards/replica\_set/update.rs570-586](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L570-L586)

### ReplicaSetState Persistence

The `ReplicaSetState` is persisted to disk in `replica_state.json` and contains:

```
```

This state is loaded on startup and updated through consensus operations.

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs125](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L125-L125) [lib/collection/src/shards/replica\_set/mod.rs169-182](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L169-L182)

### Locally Disabled Peers

When a replica fails an operation, it is immediately marked as "locally disabled" to prevent further requests until consensus confirms the state change:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs94-98](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L94-L98) [lib/collection/src/shards/replica\_set/mod.rs872-896](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L872-L896)

The locally disabled registry uses exponential backoff to avoid spamming consensus with failure notifications:

**Sources:** [lib/collection/src/shards/replica\_set/locally\_disabled\_peers.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/locally_disabled_peers.rs) (implied from usage)

---

## Write Coordination and Consistency

### WriteOrdering Levels

The replica set supports three levels of write ordering, each providing different consistency guarantees:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs168-190](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L168-L190)

The `write_ordering_lock` ensures that Strong and Medium ordering requests are serialized:

**Sources:** [lib/collection/src/shards/replica\_set/update.rs137-142](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L137-L142)

### Clock-Based Consistency

Each update operation is tagged with a logical clock to establish causality:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs111-166](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L111-L166) [lib/collection/src/shards/replica\_set/update.rs256-397](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L256-L397)

**Clock Tag Structure:**

```
```

If a replica echoes a newer tick, the local clock advances to maintain consistency:

**Sources:** [lib/collection/src/shards/replica\_set/update.rs368-396](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L368-L396)

### Update Flow with Retry Logic

Operations may be rejected if the clock is outdated. The replica set retries with a new clock:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs17-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L17-L20) [lib/collection/src/shards/replica\_set/update.rs195-251](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L195-L251)

### Write Consistency Factor

The replica set requires a minimum number of successful replicas based on `write_consistency_factor`:

```
```

If insufficient replicas succeed, the operation fails. Failed replicas are marked as locally disabled:

**Sources:** [lib/collection/src/shards/replica\_set/update.rs355-365](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L355-L365) [lib/collection/src/shards/replica\_set/update.rs432-510](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L432-L510)

### Handling Failed Replicas

When replicas fail during an update:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/update.rs409-511](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L409-L511) [lib/collection/src/shards/replica\_set/update.rs597-662](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L597-L662)

**Special Cases:**

- **Listener replicas**: Failures are ignored
- **Partial/Recovery replicas**: Pre-condition failures and missing point errors are ignored (transfer in progress)
- **Resharding replicas**: Always deactivated on failure if not enough successes
- **Initializing replicas**: Always trigger deactivation wait

**Sources:** [lib/collection/src/shards/replica\_set/update.rs610-646](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L610-L646)

---

## Read Operations

### Shard Selection for Queries

Read operations prefer local shards for performance:

```
```

**Sources:** [lib/collection/src/shards/replica\_set/execute\_read\_operation.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/execute_read_operation.rs) (implied from replica\_set structure)

The methods `peer_is_active()` and `is_locally_disabled()` determine which replicas can serve reads:

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs1007-1018](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L1007-L1018)

---

## Shard Transfer Integration

### Transfer Lifecycle in Replica Set

Shard transfers change replica states throughout their lifecycle:

```
```

**Sources:** [lib/collection/src/collection/shard\_transfer.rs36-141](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L36-L141) [lib/collection/src/collection/shard\_transfer.rs195-300](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L195-L300)

### Transfer Method and Initial State

Different transfer methods set different initial states:

| Transfer Method           | Initial Replica State                 | Accepts Updates During Transfer |
| ------------------------- | ------------------------------------- | ------------------------------- |
| `StreamRecords`           | `Partial`                             | Yes                             |
| `Snapshot`                | `Recovery`                            | No (unless forced)              |
| `WalDelta`                | `Recovery`                            | No (unless forced)              |
| `ReshardingStreamRecords` | `Resharding` or `ReshardingScaleDown` | Yes                             |

**Sources:** [lib/collection/src/collection/shard\_transfer.rs82-103](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L82-L103)

### Transfer Abortion

When a transfer is aborted:

```
```

**Sources:** [lib/collection/src/collection/shard\_transfer.rs303-361](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L303-L361)

---

## Key Methods and Operations

### Building a Replica Set

```
ShardReplicaSet::build(
    shard_id,
    shard_key,
    collection_id,
    this_peer_id,
    local: bool,
    remotes: HashSet<PeerId>,
    on_peer_failure: Callback,
    abort_shard_transfer: Callback,
    ...
) -> CollectionResult<ShardReplicaSet>
```

Creates a new replica set with initial state. If `local=true`, builds a `LocalShard`.

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs127-230](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L127-L230)

### Loading a Replica Set

```
ShardReplicaSet::load(
    shard_id,
    shard_key,
    collection_id,
    shard_path,
    is_dirty_shard: bool,
    ...
) -> ShardReplicaSet
```

Loads an existing replica set from disk. Handles recovery mode and dirty shards by creating dummy shards.

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs232-382](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L232-L382)

### State Management

| Method                                     | Purpose                                                      |
| ------------------------------------------ | ------------------------------------------------------------ |
| `set_replica_state(peer_id, state)`        | Updates replica state and persists to disk                   |
| `peer_state(peer_id)`                      | Gets current state of a peer                                 |
| `peers()`                                  | Returns all peers and their states                           |
| `active_remote_shards()`                   | Returns active remote peer IDs (excludes local and disabled) |
| `is_last_source_of_truth_replica(peer_id)` | Checks if replica is the only active source                  |

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs415-469](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L415-L469) [lib/collection/src/shards/replica\_set/mod.rs695-711](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L695-L711)

### Replica Management

| Method                                      | Purpose                                 |
| ------------------------------------------- | --------------------------------------- |
| `add_remote(peer_id, state)`                | Adds a new remote replica               |
| `remove_remote(peer_id)`                    | Removes a remote replica                |
| `set_local(shard, state)`                   | Sets or replaces local shard            |
| `remove_local()`                            | Removes local shard and clears data     |
| `ensure_replica_with_state(peer_id, state)` | Ensures replica exists with given state |

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs598-693](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L598-L693)

### Waiting for States

```
wait_for_local_state(state, timeout) -> CollectionResult<()>
wait_for_state(peer_id, state, timeout) -> Future<CollectionResult<()>>
```

These methods block until a replica reaches the desired state or timeout occurs. Used during transfer operations.

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs474-559](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L474-L559)

---

## Integration with Collection

The `Collection` uses `ShardHolder` to manage multiple `ShardReplicaSet` instances:

```
```

**Sources:** [lib/collection/src/collection/mod.rs62-94](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L62-L94)

### Applying State from Consensus

When consensus updates the cluster state:

```
collection.set_shard_replica_state(
    shard_id,
    peer_id,
    new_state,
    from_state: Option<ReplicaState>
) -> CollectionResult<()>
```

This method:

1. Validates peer exists and `from_state` matches current state
2. Prevents deactivating last active replica
3. Updates replica state via `ensure_replica_with_state()`
4. Aborts transfers if replica becomes `Dead`
5. Triggers collection initialization check

**Sources:** [lib/collection/src/collection/mod.rs386-512](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L386-L512)

### Syncing Local State to Consensus

```
collection.sync_local_state(...) -> CollectionResult<()>
```

Periodically called to:

1. Check for locally disabled replicas and report to consensus
2. Verify transfer task states match consensus
3. Auto-recover `Dead` replicas by requesting transfers
4. Convert replicas to/from `Listener` state based on node type

**Sources:** [lib/collection/src/collection/mod.rs595-777](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L595-L777)

---

## Summary

The `ShardReplicaSet` is the core abstraction for managing replica consistency in Qdrant:

- **Coordinates local and remote shards** across multiple peers
- **Manages replica states** through a persisted state machine
- **Provides write ordering guarantees** (Weak, Medium, Strong) via leader selection and serialization
- **Uses logical clocks** to establish causality and detect outdated operations
- **Handles replica failures** with locally disabled peers and consensus notification
- **Integrates with shard transfers** to support data migration and recovery
- **Prefers local shards** for read operations to minimize latency
- **Enforces write consistency factor** to ensure sufficient replica agreement

All state changes are coordinated through the consensus layer (Raft), ensuring cluster-wide consistency while allowing optimistic local operations for performance.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Shards and Replica Sets](#shards-and-replica-sets.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Core Abstraction](#core-abstraction.md)
- [ShardReplicaSet Structure](#shardreplicaset-structure.md)
- [Local vs Remote Shards](#local-vs-remote-shards.md)
- [Replica State Management](#replica-state-management.md)
- [Replica States](#replica-states.md)
- [ReplicaSetState Persistence](#replicasetstate-persistence.md)
- [Locally Disabled Peers](#locally-disabled-peers.md)
- [Write Coordination and Consistency](#write-coordination-and-consistency.md)
- [WriteOrdering Levels](#writeordering-levels.md)
- [Clock-Based Consistency](#clock-based-consistency.md)
- [Update Flow with Retry Logic](#update-flow-with-retry-logic.md)
- [Write Consistency Factor](#write-consistency-factor.md)
- [Handling Failed Replicas](#handling-failed-replicas.md)
- [Read Operations](#read-operations.md)
- [Shard Selection for Queries](#shard-selection-for-queries.md)
- [Shard Transfer Integration](#shard-transfer-integration.md)
- [Transfer Lifecycle in Replica Set](#transfer-lifecycle-in-replica-set.md)
- [Transfer Method and Initial State](#transfer-method-and-initial-state.md)
- [Transfer Abortion](#transfer-abortion.md)
- [Key Methods and Operations](#key-methods-and-operations.md)
- [Building a Replica Set](#building-a-replica-set.md)
- [Loading a Replica Set](#loading-a-replica-set.md)
- [State Management](#state-management.md)
- [Replica Management](#replica-management.md)
- [Waiting for States](#waiting-for-states.md)
- [Integration with Collection](#integration-with-collection.md)
- [Applying State from Consensus](#applying-state-from-consensus.md)
- [Syncing Local State to Consensus](#syncing-local-state-to-consensus.md)
- [Summary](#summary.md)
