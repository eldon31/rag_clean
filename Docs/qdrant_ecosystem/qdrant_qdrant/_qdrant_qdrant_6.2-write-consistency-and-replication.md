Write Consistency and Replication | qdrant/qdrant | DeepWiki

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

# Write Consistency and Replication

Relevant source files

- [lib/collection/src/collection/collection\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs)
- [lib/collection/src/collection/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs)
- [lib/collection/src/collection/shard\_transfer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs)
- [lib/collection/src/collection/sharding\_keys.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs)
- [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)
- [lib/collection/src/shards/replica\_set/update.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs)
- [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs)

This document explains how Qdrant ensures consistency across replicas when processing write operations. It covers write ordering guarantees, leader-based coordination, logical clock mechanisms, and failure handling strategies that enable Qdrant to maintain data consistency across distributed shard replicas.

For information about the update processing pipeline and WAL persistence, see [Update Processing Pipeline](qdrant/qdrant/6.1-update-processing-pipeline.md). For distributed consensus and metadata operations, see [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md).

---

## Purpose and Scope

When a collection has multiple replicas of a shard distributed across peers, write operations must be coordinated to maintain consistency. This page describes:

- **Write ordering levels** (`Weak`, `Medium`, `Strong`) and their consistency guarantees
- **Leader-based replication** for coordinating updates across replicas
- **Logical clock mechanisms** (`ClockTag`, `ClockSet`) for detecting and resolving conflicts
- **Write consistency factor** configuration and enforcement
- **Failure detection** and automatic replica deactivation
- **Rate limiting** for write operations in strict mode

The core implementation resides in `ShardReplicaSet::update_with_consistency` and `ShardReplicaSet::update_impl`, which orchestrate parallel replica updates while enforcing consistency guarantees.

---

## Write Ordering Levels

Qdrant supports three write ordering levels that trade off between performance and consistency guarantees. These are defined in the `WriteOrdering` enum.

| Ordering | Leader Selection             | Consistency Guarantee                  | Use Case                                           |
| -------- | ---------------------------- | -------------------------------------- | -------------------------------------------------- |
| `Weak`   | Local peer                   | Best-effort, eventual consistency      | High throughput, tolerates temporary inconsistency |
| `Medium` | Highest alive replica peer   | Consistent with highest alive peer     | Balanced consistency and availability              |
| `Strong` | Highest replica peer (by ID) | Strict consistency across all replicas | Maximum consistency, lower throughput              |

### WriteOrdering and Leader Selection

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs168-190](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L168-L190)
- [lib/collection/src/shards/replica\_set/update.rs111-166](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L111-L166)

### Implementation Details

The leader peer for an update is determined by the `leader_peer_for_update` method:

**Weak Ordering:**

- Always uses the local peer (`this_peer_id()`)
- No serialization lock acquired
- Each peer processes updates independently
- Provides highest throughput but weakest consistency

**Medium Ordering:**

- Selects the highest peer ID among **alive** replicas (Active or Resharding states)
- Serialization lock (`write_ordering_lock`) acquired on the leader
- Filters out locally disabled peers
- Balances consistency with availability

**Strong Ordering:**

- Selects the highest peer ID among **all** replicas, regardless of state
- Serialization lock acquired on the leader
- Provides strongest consistency guarantees
- May block if the highest peer is unavailable

The `write_ordering_lock` is a `Mutex<()>` that serializes updates on the leader peer, ensuring operations are applied in a consistent order.

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs168-190](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L168-L190)
- [lib/collection/src/shards/replica\_set/mod.rs114](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L114-L114)
- [lib/collection/src/shards/replica\_set/update.rs136-142](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L136-L142)

---

## Replica Coordination and Leader Selection

### Leader-Based Update Flow

When `Medium` or `Strong` ordering is specified, updates flow through a designated leader peer to ensure consistent ordering:

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs111-166](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L111-L166)
- [lib/collection/src/shards/replica\_set/update.rs669-686](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L669-L686)

### Forwarding to Leader

If the local peer is not the designated leader, the update is forwarded via internal gRPC:

1. `RemoteShard::forward_update` sends the operation to the leader peer
2. If forwarding fails with a transient error, the leader is marked as locally disabled
3. A service error is returned to the client to retry

This ensures that even if a client connects to a non-leader peer, the update will be properly coordinated through the leader.

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs148-165](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L148-L165)

---

## Clock-Based Consistency

Qdrant uses logical clocks to detect and resolve conflicting updates across replicas. Each replica maintains a `ClockSet` that tracks logical timestamps.

### ClockTag Structure

Every update operation is tagged with a `ClockTag` containing:

```
```

The `ClockSet` maintains a mapping of clocks and increments ticks for each new operation:

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs290-292](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L290-L292)
- [lib/collection/src/shards/replica\_set/mod.rs116](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L116-L116)

### Clock Rejection and Retry

When an update is rejected due to an old clock (another replica has seen a newer tick), the operation is retried with a fresh clock:

1. **Initial attempt:** Update sent with `clock_tick = N`
2. **Replica A:** Accepts and stores `tick = N`
3. **Replica B:** Already saw `tick = N+1` from a concurrent update
4. **Replica B:** Returns `UpdateStatus::ClockRejected`
5. **Leader:** Detects rejection, advances clock to `max(N, echo_ticks)`, retries
6. **Retry:** Update sent with `clock_tick = N+2`
7. **All replicas:** Accept the update

The maximum number of retries is defined by `UPDATE_MAX_CLOCK_REJECTED_RETRIES = 3`.

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs16-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L16-L20)
- [lib/collection/src/shards/replica\_set/update.rs212-250](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L212-L250)
- [lib/collection/src/shards/replica\_set/update.rs368-396](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L368-L396)

### Clock Advancement

After each update, the leader examines the echoed clock ticks from all replicas and advances its local clock to the maximum observed:

```
```

This ensures that the local clock stays synchronized with the distributed state.

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs368-396](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L368-L396)

---

## Write Consistency Factor

The write consistency factor determines how many replicas must successfully apply an update before the operation is considered successful.

### Configuration

The `write_consistency_factor` is configured in collection parameters and defaults to 1:

```
```

### Success Criteria

An update succeeds if:

1. At least `write_consistency_factor` replicas successfully apply the update
2. At least one **Active** or **Resharding** replica applies the update
3. The consistency factor is capped at the total number of replicas

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs355-365](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L355-L365)
- [lib/collection/src/shards/replica\_set/update.rs432-511](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L432-L511)
- [lib/collection/src/shards/replica\_set/update.rs513-522](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L513-L522)

### Handling Partial Failures

When some replicas fail but enough succeed to meet the consistency factor:

1. **Failed replicas** are marked as locally disabled
2. If `wait=true`, the operation waits for consensus to deactivate the failed replicas (30s timeout)
3. If deactivation times out, a consistency error is returned to the user
4. Failed replicas will automatically recover via shard transfer

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs446-495](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L446-L495)

---

## Failure Handling and Recovery

### Locally Disabled Peers

When a replica fails to apply an update, it is marked as **locally disabled** to prevent future updates from being sent to it:

```
```

The `locally_disabled_peers` registry tracks:

- Which peers are disabled
- When they were disabled
- The replica state they were in when disabled

**Sources:**

- [lib/collection/src/shards/replica\_set/mod.rs98](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L98-L98)
- [lib/collection/src/shards/replica\_set/update.rs597-662](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L597-L662)

### Failure Detection Flow

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs597-662](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L597-L662)
- [lib/collection/src/shards/replica\_set/mod.rs872-896](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L872-L896)

### Replica State Transitions

Replicas progress through various states during their lifecycle:

| State          | Description                  | Accepts Updates? | Accepts Queries? |
| -------------- | ---------------------------- | ---------------- | ---------------- |
| `Initializing` | Initial state after creation | Yes              | No               |
| `Active`       | Fully operational            | Yes              | Yes              |
| `Partial`      | Receiving shard transfer     | Yes              | No               |
| `Recovery`     | Recovering from snapshot     | Force only       | No               |
| `Listener`     | Read-only replica            | Yes (no wait)    | Yes              |
| `Resharding`   | Participating in resharding  | Yes              | Yes              |
| `Dead`         | Failed replica               | No               | No               |

The `is_peer_updatable` method determines whether updates should be sent to a replica:

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs567-586](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L567-L586)
- [lib/collection/src/shards/replica\_set/update.rs24-106](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L24-L106)

### Consensus Synchronization

The `sync_local_state` method periodically reports locally disabled peers to consensus:

1. `locally_disabled_peers.notify_elapsed()` returns peers ready to be reported
2. `notify_peer_failure_cb` is called for each failed peer
3. Consensus proposes a `SetShardReplicaState` operation to mark the peer as `Dead`
4. Related shard transfers are aborted

**Sources:**

- [lib/collection/src/shards/replica\_set/mod.rs872-896](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L872-L896)
- [lib/collection/src/collection/mod.rs595-646](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L595-L646)

---

## Rate Limiting

In strict mode, Qdrant can enforce write rate limits to prevent resource exhaustion.

### Write Rate Limiter

The `write_rate_limiter` is configured per replica set:

```
```

The rate limiter is initialized from collection configuration:

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/mod.rs117](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L117-L117)
- [lib/collection/src/shards/replica\_set/mod.rs196-204](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L196-L204)

### Rate Limit Enforcement

Before applying an update, the rate limiter checks if the operation is allowed:

```
```

The cost is estimated based on the number of points affected by the operation. If the rate limit is exceeded, a `CollectionError::RateLimitError` is returned.

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs540-565](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L540-L565)
- [lib/collection/src/shards/replica\_set/mod.rs843-868](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L843-L868)

### Exemptions

Internal operations and resharding operations are exempt from rate limiting:

- Operations with `hw_measurement_acc.is_disposable()` are not rate limited
- Resharding operations automatically use disposable hardware measurement

**Sources:**

- [lib/collection/src/shards/replica\_set/mod.rs856-859](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L856-L859)
- [lib/collection/src/shards/replica\_set/update.rs128-132](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L128-L132)

---

## Complete Update Flow

### End-to-End Write Path with Consistency

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs111-166](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L111-L166)
- [lib/collection/src/shards/replica\_set/update.rs195-251](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L195-L251)
- [lib/collection/src/shards/replica\_set/update.rs253-538](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L253-L538)

### Failure Recovery Example

```
```

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs432-495](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L432-L495)
- [lib/collection/src/shards/replica\_set/mod.rs872-896](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L872-L896)
- [lib/collection/src/collection/mod.rs595-646](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L595-L646)

---

## Key Takeaways

1. **Three ordering levels:** Weak (eventual), Medium (leader-based, alive peers), Strong (leader-based, all peers)

2. **Logical clocks:** Every operation receives a `ClockTag` with monotonically increasing ticks to detect conflicts

3. **Write consistency factor:** Configurable number of replicas that must successfully apply an update

4. **Automatic failure recovery:** Failed replicas are marked locally disabled, reported to consensus, and automatically recovered via shard transfer

5. **Rate limiting:** Optional per-minute write rate limits in strict mode, with cost based on affected points

6. **Parallel execution:** Updates are sent to all replicas in parallel (with optional concurrency limit), reducing latency

7. **Retry mechanism:** Clock-rejected operations are retried up to 3 times with fresh clocks

The combination of these mechanisms enables Qdrant to provide tunable consistency guarantees while maintaining high availability and performance across distributed replicas.

**Sources:**

- [lib/collection/src/shards/replica\_set/update.rs1-686](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs#L1-L686)
- [lib/collection/src/shards/replica\_set/mod.rs1-1690](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L1-L1690)
- [lib/collection/src/collection/mod.rs595-646](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L595-L646)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Write Consistency and Replication](#write-consistency-and-replication.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Write Ordering Levels](#write-ordering-levels.md)
- [WriteOrdering and Leader Selection](#writeordering-and-leader-selection.md)
- [Implementation Details](#implementation-details.md)
- [Replica Coordination and Leader Selection](#replica-coordination-and-leader-selection.md)
- [Leader-Based Update Flow](#leader-based-update-flow.md)
- [Forwarding to Leader](#forwarding-to-leader.md)
- [Clock-Based Consistency](#clock-based-consistency.md)
- [ClockTag Structure](#clocktag-structure.md)
- [Clock Rejection and Retry](#clock-rejection-and-retry.md)
- [Clock Advancement](#clock-advancement.md)
- [Write Consistency Factor](#write-consistency-factor.md)
- [Configuration](#configuration.md)
- [Success Criteria](#success-criteria.md)
- [Handling Partial Failures](#handling-partial-failures.md)
- [Failure Handling and Recovery](#failure-handling-and-recovery.md)
- [Locally Disabled Peers](#locally-disabled-peers.md)
- [Failure Detection Flow](#failure-detection-flow.md)
- [Replica State Transitions](#replica-state-transitions.md)
- [Consensus Synchronization](#consensus-synchronization.md)
- [Rate Limiting](#rate-limiting.md)
- [Write Rate Limiter](#write-rate-limiter.md)
- [Rate Limit Enforcement](#rate-limit-enforcement.md)
- [Exemptions](#exemptions.md)
- [Complete Update Flow](#complete-update-flow.md)
- [End-to-End Write Path with Consistency](#end-to-end-write-path-with-consistency.md)
- [Failure Recovery Example](#failure-recovery-example.md)
- [Key Takeaways](#key-takeaways.md)
