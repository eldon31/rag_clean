Raft Consensus Protocol | qdrant/qdrant | DeepWiki

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

# Raft Consensus Protocol

Relevant source files

- [config/config.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml)
- [lib/collection/src/common/snapshots\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/common/snapshots_manager.rs)
- [lib/collection/src/operations/shared\_storage\_config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs)
- [lib/storage/src/content\_manager/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs)
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

This document describes the implementation of the Raft consensus protocol in Qdrant's distributed deployment mode. The Raft implementation coordinates metadata operations across cluster peers, ensuring that collection configurations, shard assignments, and peer membership changes are consistently applied across all nodes.

For information about data-level replication and shard transfers, see [Shard Transfers and Resharding](qdrant/qdrant/7.2-shard-transfers-and-resharding.md). For general distributed system concepts, see [Distributed System Features](qdrant/qdrant/7-distributed-system-features.md).

---

## Purpose and Scope

The Raft consensus protocol in Qdrant serves a specific role: **coordinating metadata operations** across the cluster. This includes:

- Collection creation, deletion, and configuration changes
- Shard assignment and replica placement
- Peer membership (adding/removing nodes)
- Shard transfer coordination
- Cluster metadata key-value storage

**What Raft does NOT handle:**

- Individual point operations (upserts, deletes) - these use optimistic replication with logical clocks
- Search queries - these are routed directly to appropriate shards
- Shard-level data replication - handled by `ShardReplicaSet` with write consistency factors

The consensus layer operates independently from data operations, allowing high throughput for vector operations while maintaining strong consistency for cluster topology changes.

Sources: [src/consensus.rs1-150](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L1-L150) [lib/storage/src/content\_manager/consensus\_ops.rs20-207](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L20-L207)

---

## Architecture Overview

```
```

**Key Components:**

| Component           | Type             | Purpose                                          |
| ------------------- | ---------------- | ------------------------------------------------ |
| `Consensus`         | Thread Runner    | Main consensus loop processing Raft protocol     |
| `RawNode`           | Raft Library     | `raft` crate's Raft node implementation          |
| `ConsensusStateRef` | State Manager    | `Arc<ConsensusManager>` managing consensus state |
| `Persistent`        | WAL Storage      | Persistent Raft log and hard state               |
| `OperationSender`   | Proposal Channel | High-level API for proposing operations          |
| `RaftService`       | gRPC Service     | Receives Raft messages from peers                |
| `RaftMessageBroker` | Message Sender   | Sends Raft messages to peers                     |

Sources: [src/consensus.rs34-58](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L34-L58) [src/main.rs329-447](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L329-L447) [lib/storage/src/content\_manager/consensus\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_manager.rs)

---

## Consensus Thread Lifecycle

The consensus thread is spawned during service initialization and runs independently from the main application logic:

```
```

**Thread Initialization Steps:**

1. **Load Persistent State** [src/main.rs273-278](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L273-L278) - `Persistent::load_or_init()` loads existing Raft state or initializes new state with optional peer\_id
2. **Create Consensus Instance** [src/consensus.rs174-283](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L174-L283) - `Consensus::new()` sets up Raft config, channels, and determines if initialization or recovery is needed
3. **Bootstrap or Recover** [src/consensus.rs286-463](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L286-L463) - New deployments bootstrap from a peer or self-initialize; existing deployments recover by notifying peers of address changes
4. **Apply Uncommitted Entries** [src/consensus.rs249-251](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L249-L251) - Before starting the loop, apply any committed but unapplied entries from previous shutdown
5. **Start Main Loop** [src/consensus.rs465-546](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L465-L546) - Enter infinite loop processing Raft protocol

Sources: [src/consensus.rs60-170](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L60-L170) [src/main.rs273-447](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L273-L447)

---

## Operation Types and Flow

All operations that require cluster-wide consensus are modeled as `ConsensusOperations`:

```
```

**Operation Processing Flow:**

```
```

**Helper Methods for Common Operations:**

The `ConsensusOperations` enum provides factory methods for common patterns:

| Method                 | Purpose                   | Citation                                                                                                                                                               |
| ---------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `abort_transfer()`     | Abort a shard transfer    | [lib/storage/src/content\_manager/consensus\_ops.rs70-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L70-L82)     |
| `finish_transfer()`    | Complete a shard transfer | [lib/storage/src/content\_manager/consensus\_ops.rs84-89](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L84-L89)     |
| `set_replica_state()`  | Change replica state      | [lib/storage/src/content\_manager/consensus\_ops.rs105-122](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L105-L122) |
| `initialize_replica()` | Mark replica as Active    | [lib/storage/src/content\_manager/consensus\_ops.rs151-163](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L151-L163) |
| `start_transfer()`     | Begin shard transfer      | [lib/storage/src/content\_manager/consensus\_ops.rs165-170](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L165-L170) |

Sources: [lib/storage/src/content\_manager/consensus\_ops.rs38-207](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L38-L207) [src/consensus.rs627-696](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L627-L696)

---

## Bootstrapping and Peer Management

### First Peer (Origin Peer)

The first peer in a cluster starts without a bootstrap URI and self-initializes:

```
```

The origin peer goes through special handling in `try_add_origin()` [src/consensus.rs720-777](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L720-L777):

- Only executes if peer count is 1 and commit index ≤ 1
- Waits until the peer self-elects as Leader
- Proposes itself as a voter (AddNode conf change)

### Adding a New Peer

When a new peer joins the cluster:

```
```

**Learner Promotion Logic** [src/consensus.rs784-832](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L784-L832):

- Only the leader promotes learners
- Promotion only happens when there are no uncommitted changes (commit == last\_log\_entry)
- A learner is promoted when its `matched` index equals the current `commit` index
- Learners are promoted one at a time to ensure safety

**Recovery After Restart** [src/consensus.rs358-418](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L358-L418): If a peer restarts with a different URI, it notifies other peers:

- Tries to contact any known peer via `add_peer_to_known` with new URI
- Uses exponential backoff with up to 3 retries
- Other peers update their `peer_address_by_id` mapping

Sources: [src/consensus.rs286-323](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L286-L323) [src/consensus.rs420-463](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L420-L463) [src/tonic/api/raft\_api.rs64-149](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L64-L149)

---

## Message Processing and Raft Loop

The consensus thread runs a continuous loop processing two types of messages:

### Message Types

```
```

### Main Loop Structure

The consensus loop in `start()` [src/consensus.rs465-546](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L465-L546) operates as follows:

```
```

**Key Loop Features:**

1. **Batching**: Processes up to 128 messages per iteration for efficiency [src/consensus.rs559](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L559-L559)
2. **Tick Capping**: If Raft messages were received, caps reported ticks to prevent spurious elections [src/consensus.rs488-513](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L488-L513)
3. **Early Break on Conf-Change**: Only one conf-change can be pending at a time [src/consensus.rs587-611](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L587-L611)
4. **Idle Detection**: After 3 idle cycles with activity, syncs local state changes [src/consensus.rs541-544](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L541-L544)

Sources: [src/consensus.rs465-546](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L465-L546) [src/consensus.rs548-625](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L548-L625)

---

## Processing Ready State

When the Raft node has updates to process, the `on_ready()` method handles the work:

```
```

**Ready State Components** [src/consensus.rs834-979](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L834-L979):

| Component           | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| `snapshot`          | Full state snapshot to apply (for lagging peers) |
| `hs` (HardState)    | Persistent Raft state: term, vote, commit        |
| `entries`           | Log entries to persist                           |
| `committed_entries` | Entries to apply to state machine                |
| `messages`          | Raft messages to send to peers                   |
| `conf_state`        | Updated cluster configuration                    |

**Entry Application** [lib/storage/src/content\_manager/consensus/state.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus/state.rs):

- Decodes each entry's data as `ConsensusOperations` (CBOR format)
- Routes `CollectionMeta` operations to `TableOfContent`
- Updates `peer_address_by_id` for peer management operations
- Updates `cluster_metadata` for metadata operations
- Tracks `last_applied_entry` to avoid re-application

Sources: [src/consensus.rs834-979](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L834-L979) [src/consensus.rs981-1133](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L981-L1133)

---

## Sending Messages to Peers

The `RaftMessageBroker` handles sending Raft protocol messages to other peers:

```
```

**Message Sending Process** [src/consensus.rs1135-1308](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L1135-L1308):

1. **Batch Messages**: Groups messages by destination peer ID
2. **Spawn Async Tasks**: Uses tokio runtime to send messages concurrently
3. **Get gRPC Channel**: Retrieves connection from `TransportChannelPool`
4. **Encode and Send**: Encodes Raft message as protobuf and sends via `RaftClient::send()`
5. **Error Tracking**: Records failures in `message_send_failures` for monitoring

**Message Batching Strategy**:

- Messages are batched per peer to reduce task overhead
- Each batch is sent in a single async task
- Failures are logged but don't block the consensus loop

**Special Handling for Snapshots** [src/consensus.rs1225-1261](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L1225-L1261):

- Snapshot messages trigger `ConsensusOperations::RequestSnapshot` to be sent to self
- This ensures snapshots are created in the consensus thread context
- After creation, `report_snapshot()` notifies Raft of success/failure

Sources: [src/consensus.rs1135-1308](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L1135-L1308)

---

## WAL and State Persistence

### Persistent Storage Structure

The `Persistent` struct manages Raft's durable state:

```
```

**State Files**:

| File              | Content                             | Purpose                               |
| ----------------- | ----------------------------------- | ------------------------------------- |
| `meta.json`       | `{this_peer_id, is_new_deployment}` | Peer identity and cluster init status |
| `hard_state.json` | `{term, vote, commit}`              | Raft's persistent hard state          |
| `conf_state.json` | `{voters, learners, ...}`           | Current cluster configuration         |
| `raft_log_*.dat`  | CBOR-encoded log entries            | Write-ahead log of operations         |
| `snapshot_*.dat`  | Consensus state snapshot            | Full state for recovering peers       |

**WAL Compaction** [src/consensus.rs253-258](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L253-L258):

- Compacts WAL when it exceeds `compact_wal_entries` applied operations (default: 128)
- Creates a snapshot of current state
- Truncates old log entries before the snapshot
- Allows faster bootstrap for new peers (transfer snapshot instead of replaying full log)

Sources: [lib/storage/src/content\_manager/consensus/persistent.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus/persistent.rs) [config/config.yaml314-326](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L314-L326)

---

## Configuration

The consensus configuration is specified in `ConsensusConfig`:

```
```

**Configuration Parameters**:

| Parameter                | Default | Description                                                                         |
| ------------------------ | ------- | ----------------------------------------------------------------------------------- |
| `tick_period_ms`         | 100     | How often Raft ticks (in ms). Lower = faster election/heartbeat, higher CPU/network |
| `bootstrap_timeout_sec`  | 15      | Timeout for initial peer bootstrap requests                                         |
| `max_message_queue_size` | 100     | Backpressure limit for consensus operation channel                                  |
| `message_timeout_ticks`  | 10      | (Unused in current implementation)                                                  |
| `compact_wal_entries`    | 128     | Compact WAL after this many applied entries                                         |

**Derived Timeouts**:

- **Election Timeout**: `tick_period_ms * max_election_tick` (typically \~2 seconds with default config)
- **Heartbeat Interval**: `tick_period_ms * heartbeat_tick` (typically \~1 second)
- **Leader Established**: `tick_period_ms * max_election_tick` (\~2 seconds)

**Important Tuning Notes** [config/config.yaml314-326](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L314-L326):

> "Setting this parameter to lower value will allow consensus to detect disconnected nodes earlier, but too frequent tick period may create significant network and CPU overhead. We encourage you NOT to change this parameter unless you know what you are doing."

Sources: [src/settings.rs111-139](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L111-L139) [config/config.yaml314-326](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L314-L326) [src/consensus.rs203-209](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L203-L209)

---

## Internal gRPC API

The `RaftService` provides the gRPC API for inter-peer Raft communication:

```
```

**RPC Methods**:

| Method                    | Request                 | Response   | Purpose                                   |
| ------------------------- | ----------------------- | ---------- | ----------------------------------------- |
| `send`                    | `RaftMessage` (encoded) | `()`       | Receive Raft protocol messages from peers |
| `who_is`                  | `PeerId`                | `UriStr`   | Resolve peer ID to URI                    |
| `add_peer_to_known`       | `{id, uri?, port?}`     | `AllPeers` | Bootstrap a new peer into cluster         |
| `add_peer_as_participant` | `PeerId`                | `()`       | Deprecated, no-op for compatibility       |

**Bootstrap Peer Sequence** [src/tonic/api/raft\_api.rs64-149](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L64-L149):

1. New peer calls `add_peer_to_known` on bootstrap peer
2. Bootstrap peer proposes `ConsensusOperations::AddPeer` with `AddLearnerNode`
3. Operation replicates and commits via Raft
4. Bootstrap peer returns `AllPeers` with all current peer addresses plus `first_peer_id`
5. New peer stores peer addresses and sets initial conf state with `first_voter_id`

Sources: [src/tonic/api/raft\_api.rs1-150](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L1-L150) [src/tonic/mod.rs256-360](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L256-L360)

---

## Cluster Metadata Storage

Qdrant supports arbitrary key-value metadata storage in consensus:

```
```

**API Endpoints**:

| Endpoint                       | Method | Description                |
| ------------------------------ | ------ | -------------------------- |
| `/cluster/metadata/keys`       | GET    | List all metadata keys     |
| `/cluster/metadata/keys/{key}` | GET    | Get value for specific key |
| `/cluster/metadata/keys/{key}` | PUT    | Set value (JSON) for key   |
| `/cluster/metadata/keys/{key}` | DELETE | Remove key (sets to null)  |

**Use Cases**:

- Storing cluster-wide configuration
- Coordination flags between nodes
- Custom metadata for tooling/monitoring

Sources: [src/actix/api/cluster\_api.rs98-178](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs#L98-L178) [lib/storage/src/content\_manager/consensus\_ops.rs50-53](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_ops.rs#L50-L53)

---

## High Priority Thread

The consensus thread attempts to run with high priority on Linux systems:

```
```

This is a best-effort optimization - it will likely fail without elevated permissions but gracefully continues. The reasoning is that consensus timing is critical for cluster stability:

- Election timeouts depend on timely message processing
- Heartbeat delays can trigger unnecessary leader elections
- Higher priority reduces latency variance

Sources: [src/consensus.rs99-106](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L99-L106) [src/consensus.rs121-128](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L121-L128)

---

## Monitoring and Health

### Cluster Status API

The `/cluster` endpoint returns consensus health information:

```
```

**Key Metrics**:

- `term`: Current Raft term (increases with elections)
- `commit`: Index of last committed operation
- `pending_operations`: Uncommitted entries count
- `role`: Follower, Candidate, Leader, or PreCandidate
- `consensus_thread_status`: Working, Stopped, or StoppedWithErr

### Health Tracking

The `ConsensusManager` tracks consensus health:

- `record_consensus_working()`: Called on each `on_ready()` cycle
- `on_consensus_thread_err()`: Called if consensus thread panics
- `on_consensus_stopped()`: Called on clean shutdown

Sources: [lib/storage/src/types.rs148-246](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L148-L246) [src/actix/api/cluster\_api.rs32-41](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs#L32-L41)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Raft Consensus Protocol](#raft-consensus-protocol.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Architecture Overview](#architecture-overview.md)
- [Consensus Thread Lifecycle](#consensus-thread-lifecycle.md)
- [Operation Types and Flow](#operation-types-and-flow.md)
- [Bootstrapping and Peer Management](#bootstrapping-and-peer-management.md)
- [First Peer (Origin Peer)](#first-peer-origin-peer.md)
- [Adding a New Peer](#adding-a-new-peer.md)
- [Message Processing and Raft Loop](#message-processing-and-raft-loop.md)
- [Message Types](#message-types.md)
- [Main Loop Structure](#main-loop-structure.md)
- [Processing Ready State](#processing-ready-state.md)
- [Sending Messages to Peers](#sending-messages-to-peers.md)
- [WAL and State Persistence](#wal-and-state-persistence.md)
- [Persistent Storage Structure](#persistent-storage-structure.md)
- [Configuration](#configuration.md)
- [Internal gRPC API](#internal-grpc-api.md)
- [Cluster Metadata Storage](#cluster-metadata-storage.md)
- [High Priority Thread](#high-priority-thread.md)
- [Monitoring and Health](#monitoring-and-health.md)
- [Cluster Status API](#cluster-status-api.md)
- [Health Tracking](#health-tracking.md)
