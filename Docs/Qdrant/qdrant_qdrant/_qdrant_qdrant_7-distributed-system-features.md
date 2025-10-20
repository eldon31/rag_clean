Distributed System Features | qdrant/qdrant | DeepWiki

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

# Distributed System Features

Relevant source files

- [config/config.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml)
- [lib/collection/src/collection/collection\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs)
- [lib/collection/src/collection/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs)
- [lib/collection/src/collection/shard\_transfer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs)
- [lib/collection/src/collection/sharding\_keys.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs)
- [lib/collection/src/common/snapshots\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/common/snapshots_manager.rs)
- [lib/collection/src/operations/shared\_storage\_config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs)
- [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)
- [lib/collection/src/shards/replica\_set/update.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs)
- [lib/storage/src/content\_manager/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs)
- [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs)
- [lib/storage/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs)
- [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)
- [src/actix/api/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/mod.rs)
- [src/actix/certificate\_helpers.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/certificate_helpers.rs)
- [src/actix/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs)
- [src/common/helpers.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs)
- [src/common/http\_client.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/http_client.rs)
- [src/consensus.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs)
- [src/main.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs)
- [src/settings.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs)
- [src/tonic/api/raft\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs)
- [src/tonic/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs)

This document describes the distributed deployment capabilities of Qdrant. It covers cluster architecture, data distribution through sharding and replication, write consistency models, and peer management. For detailed information about the Raft consensus protocol implementation, see [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md). For shard transfer mechanisms and resharding operations, see [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md).

## Overview

Qdrant supports distributed deployment mode where multiple nodes (peers) form a cluster. In this mode:

- **Metadata** (collection configurations, shard placement, peer membership) is coordinated through Raft consensus
- **Data operations** (point updates, searches) use optimistic replication with logical clocks
- **Collections** are split into shards distributed across peers
- **Shards** are replicated for fault tolerance
- **Peers** communicate via internal gRPC on a separate P2P port

The distributed mode is enabled via the `cluster.enabled` configuration and requires coordination through the Raft consensus protocol running in a dedicated thread on each peer.

**Sources:** [src/main.rs280-306](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L280-L306) [config/config.yaml301-327](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L301-L327) [src/settings.rs68-88](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L68-L88)

## Cluster Architecture

### Peer Components

```
```

**Peer Architecture**

Each peer in the cluster runs:

1. **Main thread** - Initializes services and spawns worker threads
2. **Consensus thread** - Runs Raft protocol, processes metadata operations
3. **REST/gRPC APIs** - Handle client requests
4. **Internal gRPC server** - Handles peer-to-peer communication on the P2P port
5. **Dispatcher** - Routes requests to consensus or directly to TableOfContent
6. **TableOfContent** - Manages collections and shards

**Sources:** [src/main.rs388-502](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L388-L502) [src/consensus.rs44-58](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L44-L58) [src/tonic/mod.rs255-279](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L255-L279)

### Cluster Configuration

The cluster is configured through the `cluster` section in `config.yaml`:

| Configuration                      | Type  | Default | Description                          |
| ---------------------------------- | ----- | ------- | ------------------------------------ |
| `enabled`                          | bool  | `false` | Enable distributed mode              |
| `peer_id`                          | u64   | auto    | Unique peer identifier (1 to 2^53-1) |
| `p2p.port`                         | u16   | `6335`  | Port for internal P2P communication  |
| `p2p.enable_tls`                   | bool  | `false` | Use TLS for peer communication       |
| `p2p.connection_pool_size`         | usize | 1       | Number of connections per peer       |
| `grpc_timeout_ms`                  | u64   | 5000    | Timeout for internal gRPC calls      |
| `connection_timeout_ms`            | u64   | 5000    | Timeout for establishing connections |
| `consensus.tick_period_ms`         | u64   | 100     | Raft tick interval                   |
| `consensus.max_message_queue_size` | usize | 100     | Backpressure limit for consensus     |
| `consensus.bootstrap_timeout_sec`  | u64   | 15      | Timeout for joining cluster          |
| `consensus.compact_wal_entries`    | u64   | 128     | Compact WAL after this many entries  |

**Sources:** [config/config.yaml301-327](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L301-L327) [src/settings.rs68-139](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L68-L139)

### Peer Initialization

```
```

**Peer Initialization Flow**

The initialization process differs based on deployment type:

1. **First peer** (`--uri` provided, no `--bootstrap`):

   - Generates unique peer\_id
   - Self-elects as Raft leader
   - Adds itself as first voter in consensus

2. **Joining peer** (`--bootstrap` and `--uri` provided):

   - Contacts bootstrap peer via `add_peer_to_known` RPC
   - Receives list of all peers and their addresses
   - Joins cluster as learner
   - Receives log entries from leader
   - Gets promoted to voter once caught up

3. **Recovering peer** (has existing state):

   - Loads persisted peer\_id and Raft state
   - Notifies peers if URI has changed
   - Rejoins with existing role

**Sources:** [src/main.rs260-306](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L260-L306) [src/consensus.rs172-283](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L172-L283) [src/consensus.rs286-323](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L286-L323) [src/consensus.rs420-463](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L420-L463)

## Data Distribution

### Sharding and Replication

```
```

**Sharding and Replication Model**

Data is distributed across the cluster using:

- **Shards** - Collection data is partitioned into multiple shards (controlled by `shard_number`)
- **Replicas** - Each shard has multiple replicas on different peers (`replication_factor`)
- **ShardReplicaSet** - Coordinates all replicas of a shard
- **Local vs Remote** - Each peer has local shards (with data) and remote shards (proxies to other peers)

The `ShardHolder` on each peer manages the `ShardReplicaSet` instances, which in turn manage `LocalShard` and `RemoteShard` instances.

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs84-119](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L84-L119) [lib/collection/src/collection/mod.rs61-94](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L61-L94)

### Replica States

```
```

**Replica State Transitions**

Each replica has a state managed through consensus:

| State                 | Description                                 | Accepts Updates    | Serves Queries |
| --------------------- | ------------------------------------------- | ------------------ | -------------- |
| `Initializing`        | Newly created, not yet activated            | Yes                | No             |
| `Active`              | Fully operational                           | Yes                | Yes            |
| `Partial`             | Receiving streaming updates during transfer | Yes                | No             |
| `Recovery`            | Recovering from snapshot/WAL                | No (unless forced) | No             |
| `PartialSnapshot`     | Creating snapshot                           | No (unless forced) | Yes            |
| `Listener`            | Receives updates but doesn't serve queries  | Yes (async)        | No             |
| `Resharding`          | Target shard during scale-up                | Yes                | No             |
| `ReshardingScaleDown` | Source shard during scale-down              | Yes                | Yes            |
| `Dead`                | Failed or deactivated                       | No                 | No             |

State transitions are coordinated through the `SetShardReplicaState` consensus operation.

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs47-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L47-L82) [lib/collection/src/shards/replica\_set/update.rs46-106](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L46-L106) [lib/storage/src/content\_manager/mod.rs20-207](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs#L20-L207)

## Write Consistency

### Write Ordering Levels

```
```

**Write Ordering Modes**

Qdrant provides three write ordering levels that trade off between throughput and consistency:

1. **Weak** (`WriteOrdering::Weak`):

   - No leader selection - operations processed on any peer
   - No serialization lock
   - Highest throughput
   - Eventual consistency via logical clocks
   - Use case: High-volume ingestion where exact ordering doesn't matter

2. **Medium** (`WriteOrdering::Medium`):

   - Leader is highest *alive* peer\_id
   - Operations serialized through `write_ordering_lock` on leader
   - Consistency guarantees per shard
   - Leader forwards if not local
   - Use case: Standard operations requiring ordering

3. **Strong** (`WriteOrdering::Strong`):

   - Leader is highest peer\_id (even if temporarily unavailable)
   - Operations serialized through `write_ordering_lock` on leader
   - Strongest consistency guarantees
   - May have higher latency if leader is slow
   - Use case: Critical operations requiring strict ordering

**Sources:** [lib/collection/src/shards/replica\_set/update.rs108-166](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L108-L166) [lib/collection/src/shards/replica\_set/update.rs169-190](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L169-L190)

### Clock-Based Consistency

```
```

**Logical Clock Mechanism**

Each shard replica maintains a `LocalShardClocks` structure with per-peer logical clocks. Every update is tagged with:

- **peer\_id** - Originating peer
- **clock\_id** - Clock identifier
- **tick** - Monotonically increasing counter

When a replica receives an update:

1. Checks if the clock tick is newer than its local clock for that peer
2. If older, rejects the update (returns `None`)
3. If newer, applies update and advances local clock

If updates are rejected, the ReplicaSet retries up to 3 times with incremented ticks. This ensures:

- Eventual consistency across replicas
- Updates from same peer are applied in order
- Concurrent updates from different peers can be reordered

**Sources:** [lib/collection/src/shards/replica\_set/update.rs16-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L16-L20) [lib/collection/src/shards/replica\_set/update.rs195-251](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L195-L251) [lib/collection/src/shards/replica\_set/update.rs253-363](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L253-L363)

### Write Consistency Factor

The `write_consistency_factor` determines how many replicas must successfully apply an update:

```
```

If a replica fails to apply an update, it is marked as "locally disabled" and reported to consensus for automatic recovery through shard transfers.

**Sources:** [lib/collection/src/shards/replica\_set/update.rs355-428](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L355-L428)

## Consensus Overview

Metadata operations are coordinated through Raft consensus, including:

- **Collection operations** - Create, update, delete collections
- **Shard management** - Create/drop shards, replica state changes
- **Peer management** - Add/remove peers from cluster
- **Shard transfers** - Start, finish, abort transfers
- **Resharding** - Start, finish, abort resharding operations

### Consensus Operations

| Operation Type  | Examples                                                   | Flow                                        |
| --------------- | ---------------------------------------------------------- | ------------------------------------------- |
| Collection Meta | `CreateCollection`, `UpdateCollection`, `DeleteCollection` | Proposed → Replicated → Committed → Applied |
| Replica State   | `SetShardReplicaState`                                     | State transitions managed by consensus      |
| Peer Lifecycle  | `AddPeer`, `RemovePeer`                                    | Raft membership changes                     |
| Data Transfer   | `TransferShard` (Start/Finish/Abort)                       | Coordination of shard movement              |
| Resharding      | `Resharding` (Start/Finish/Abort)                          | Coordination of shard splitting/merging     |

### Consensus Architecture

The consensus system uses:

- **RawNode** from the `raft` crate for Raft state machine
- **Persistent** for durable storage of Raft state and peer addresses
- **ConsensusManager** for operation proposals and state queries
- **Message channels** for communication between API layer and consensus thread

Detailed implementation is covered in [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md).

**Sources:** [src/consensus.rs1-58](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L1-L58) [lib/storage/src/content\_manager/mod.rs20-207](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs#L20-L207) [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs25-123](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L25-L123)

## Peer Management

### Adding a Peer

```
```

**Peer Addition Process**

1. New peer starts with `--bootstrap` URI and optionally `--uri`
2. Contacts bootstrap peer via `add_peer_to_known` gRPC
3. Bootstrap peer proposes `AddPeer` to consensus
4. All peers update their peer address mappings
5. New peer receives list of all peers
6. New peer joins as Raft learner (non-voting)
7. Leader replicates log entries to new peer
8. Once caught up, leader proposes promotion to voter
9. New peer becomes voting member

**Sources:** [src/consensus.rs420-463](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L420-L463) [src/tonic/api/raft\_api.rs63-105](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L63-L105) [src/consensus.rs627-696](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L627-L696)

### Removing a Peer

```
```

**Peer Removal Process**

1. Client issues `DELETE /cluster/peer/{id}` request
2. API checks if peer has any shards
3. If `force=false` and peer has shards, request is rejected
4. If allowed, `RemovePeer` is proposed to consensus
5. Consensus replicates and commits the operation
6. All peers remove the peer from their address mappings
7. Collections remove the peer from replica sets
8. Removed peer becomes isolated (no longer receives updates)

Note: Before removing a peer, it's recommended to transfer all shards off the peer first using shard transfer operations.

**Sources:** [src/actix/api/cluster\_api.rs58-96](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs#L58-L96)

### Health Checking

```
```

**Health Checking System**

The `HealthChecker` task runs in the background and:

1. **Peer health checks**:

   - Periodically pings each peer via `health_check` gRPC
   - Tracks consecutive failures in `message_send_failures`
   - Updates `ClusterInfo` with failure counts and timestamps

2. **Replica health monitoring**:

   - Checks for replicas in `Dead` state
   - Identifies failed transfers
   - Can trigger automatic recovery

3. **Leader readiness**:

   - Waits for Raft leader to be established
   - Only performs checks once cluster is stable

The health information is exposed via the `/cluster` API endpoint.

**Sources:** [src/main.rs424-430](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L424-L430) [lib/storage/src/types.rs200-246](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L200-L246)

## Shard Operations Overview

### Shard Transfer Lifecycle

Shard transfers move a shard replica from one peer to another. The high-level flow:

1. **Initiation** - `TransferShard::Start` proposed to consensus
2. **State change** - Target replica set to `Partial` or `Recovery` state
3. **Data transfer** - Source streams data to target (method-specific)
4. **Activation** - Target replica promoted to `Active`
5. **Completion** - `TransferShard::Finish` committed to consensus

Transfer methods:

- `StreamRecords` - Incremental streaming of point updates
- `Snapshot` - Transfer via snapshot file
- `WalDelta` - Transfer WAL + catch-up
- `ReshardingStreamRecords` - Special mode for resharding

Detailed mechanisms are covered in [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md).

**Sources:** [lib/collection/src/collection/shard\_transfer.rs36-141](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs#L36-L141) [lib/collection/src/shards/transfer/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/transfer/mod.rs)

### Resharding Operations

Resharding changes the number of shards in a collection:

- **Scale Up** - Split shards to increase parallelism
- **Scale Down** - Merge shards to reduce overhead

Resharding is managed through consensus operations:

- `Resharding::Start` - Initiate resharding with new shard distribution
- `Resharding::Finish` - Complete resharding, commit new hash ring
- `Resharding::Abort` - Cancel ongoing resharding

The resharding process creates temporary target shards, migrates data, then atomically switches the routing (hash ring).

Detailed resharding mechanisms are covered in [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md).

**Sources:** [lib/collection/src/collection/resharding.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/resharding.rs) [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs83-89](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L83-L89)

## Cluster API

### REST Endpoints

| Endpoint                       | Method | Purpose                          |
| ------------------------------ | ------ | -------------------------------- |
| `/cluster`                     | GET    | Get cluster status and Raft info |
| `/cluster/recover`             | POST   | Request consensus snapshot       |
| `/cluster/peer/{id}`           | DELETE | Remove peer from cluster         |
| `/cluster/metadata/keys`       | GET    | List cluster metadata keys       |
| `/cluster/metadata/keys/{key}` | GET    | Get cluster metadata value       |
| `/cluster/metadata/keys/{key}` | PUT    | Set cluster metadata value       |
| `/cluster/metadata/keys/{key}` | DELETE | Delete cluster metadata          |

### Cluster Status Response

```
```

**Sources:** [src/actix/api/cluster\_api.rs1-197](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs#L1-L197) [lib/storage/src/types.rs147-246](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L147-L246)

### Internal gRPC Services

The internal gRPC server on the P2P port provides:

| Service               | RPC                          | Purpose                          |
| --------------------- | ---------------------------- | -------------------------------- |
| `Raft`                | `send()`                     | Receive Raft messages from peers |
| `Raft`                | `who_is()`                   | Query peer address by ID         |
| `Raft`                | `add_peer_to_known()`        | Bootstrap new peer into cluster  |
| `QdrantInternal`      | `get_consensus_commit()`     | Get current Raft commit index    |
| `QdrantInternal`      | `wait_on_consensus_commit()` | Wait for specific commit         |
| `CollectionsInternal` | Collection operations        | Internal collection management   |
| `PointsInternal`      | Point operations             | Internal point operations        |

**Sources:** [src/tonic/mod.rs255-305](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L255-L305) [src/tonic/api/raft\_api.rs1-105](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L1-L105)

## Configuration Examples

### Single Node to Cluster Migration

```
```

```
```

```
```

```
```

```
```

### TLS Configuration for P2P

```
```

**Sources:** [config/config.yaml301-355](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L301-L355) [src/main.rs74-88](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L74-L88)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Distributed System Features](#distributed-system-features.md)
- [Overview](#overview.md)
- [Cluster Architecture](#cluster-architecture.md)
- [Peer Components](#peer-components.md)
- [Cluster Configuration](#cluster-configuration.md)
- [Peer Initialization](#peer-initialization.md)
- [Data Distribution](#data-distribution.md)
- [Sharding and Replication](#sharding-and-replication.md)
- [Replica States](#replica-states.md)
- [Write Consistency](#write-consistency.md)
- [Write Ordering Levels](#write-ordering-levels.md)
- [Clock-Based Consistency](#clock-based-consistency.md)
- [Write Consistency Factor](#write-consistency-factor.md)
- [Consensus Overview](#consensus-overview.md)
- [Consensus Operations](#consensus-operations.md)
- [Consensus Architecture](#consensus-architecture.md)
- [Peer Management](#peer-management.md)
- [Adding a Peer](#adding-a-peer.md)
- [Removing a Peer](#removing-a-peer.md)
- [Health Checking](#health-checking.md)
- [Shard Operations Overview](#shard-operations-overview.md)
- [Shard Transfer Lifecycle](#shard-transfer-lifecycle.md)
- [Resharding Operations](#resharding-operations.md)
- [Cluster API](#cluster-api.md)
- [REST Endpoints](#rest-endpoints.md)
- [Cluster Status Response](#cluster-status-response.md)
- [Internal gRPC Services](#internal-grpc-services.md)
- [Configuration Examples](#configuration-examples.md)
- [Single Node to Cluster Migration](#single-node-to-cluster-migration.md)
- [TLS Configuration for P2P](#tls-configuration-for-p2p.md)
