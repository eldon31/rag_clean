Snapshots and Recovery | qdrant/qdrant | DeepWiki

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

# Snapshots and Recovery

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

This page describes Qdrant's snapshot and recovery system, which provides data backup, restoration, and cluster synchronization capabilities. The system supports both full collection snapshots and individual shard snapshots, with various recovery strategies for distributed deployments.

For information about collection management and optimization processes, see [Update Processing and Optimization](qdrant/qdrant/5.1-query-request-flow.md). For consensus mechanisms that coordinate snapshot operations in distributed mode, see [Consensus Mechanism](qdrant/qdrant/6-data-updates-and-consistency.md).

## Snapshot Creation Architecture

Snapshots in Qdrant are created at the `LocalShard` level, with the core implementation in the `snapshot.rs` module. The process involves temporarily proxying segments to allow writes to continue during snapshot creation.

Snapshot Creation Flow: LocalShard::create\_snapshot to segment archiving

```
```

Sources: [lib/collection/src/shards/local\_shard/snapshot.rs1-352](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L1-L352) [lib/collection/src/shards/local\_shard/mod.rs84-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L84-L124)

## Segment Proxying Mechanism

The key innovation in Qdrant's snapshot system is the segment proxying mechanism, which allows writes to continue during snapshot creation. This is implemented in `proxy_all_segments_and_apply`.

Segment Proxying: Temporary redirection of writes during snapshot

```
```

The `proxy_all_segments_and_apply` function performs the following steps:

1. **Acquire upgradable read lock** on `SegmentHolder` to prevent external modifications
2. **Create temporary segment** to receive all writes during snapshot
3. **Wrap all segments in ProxySegment** - each proxy redirects writes to the temporary segment while allowing reads from the wrapped segment
4. **Apply operation** (e.g., `take_snapshot`) to each wrapped segment sequentially
5. **Unproxy segments incrementally** - as each segment finishes, restore it to reduce proxy overhead
6. **Final atomic unproxy** - restore remaining segments and promote temporary segment if it has data

This mechanism ensures:

- **No write blocking**: Updates continue via temporary segment during long-running snapshot operations
- **Consistent point-in-time view**: All wrapped segments represent the same moment
- **Minimal proxy duration**: Segments are unproxied as soon as their snapshot completes
- **Atomic state transitions**: All segment changes use proper locking

Sources: [lib/collection/src/shards/local\_shard/snapshot.rs268-352](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L268-L352) [lib/collection/src/shards/local\_shard/mod.rs108-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L108-L124)

## Snapshot Creation Process

The `LocalShard::create_snapshot` method orchestrates the complete snapshot creation process, with special handling for the WAL and coordination with the update system.

LocalShard Snapshot Creation: WAL handling and segment archiving

```
```

### WAL Handling Strategies

The snapshot system supports two WAL handling modes:

| Mode          | Function               | Behavior                            | Use Case                           |
| ------------- | ---------------------- | ----------------------------------- | ---------------------------------- |
| **Save WAL**  | `snapshot_wal()`       | Archives complete WAL contents      | Full backup with operation history |
| **Empty WAL** | `snapshot_empty_wal()` | Generates empty WAL at `last_index` | Compact snapshots without history  |

When `save_wal=false`, the system uses the `UpdateSignal::Plunger` mechanism to ensure all pending updates are flushed to segments before snapshotting. This ensures the snapshot is complete without needing the WAL.

The empty WAL generation creates a minimal WAL structure that maintains compatibility:

- Uses same `segment_capacity` as original WAL
- Positioned at the `last_index` of original WAL
- Allows normal WAL operations after recovery

Sources: [lib/collection/src/shards/local\_shard/snapshot.rs62-121](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L62-L121) [lib/collection/src/shards/local\_shard/snapshot.rs128-161](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L128-L161) [lib/collection/src/shards/local\_shard/snapshot.rs168-197](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L168-L197)

## Update Lock Coordination

The `update_operation_lock` in `LocalShard` is critical for coordinating snapshots with concurrent update operations. This `Arc<tokio::sync::RwLock<()>>` prevents data races during critical sections.

Update Lock Usage During Snapshot Operations

```
```

The lock serves two critical purposes:

1. **During snapshots**: Prevents updates during segment proxy/unproxy operations to maintain consistency
2. **During scroll operations**: Prevents updates that could corrupt scroll cursors, critical for re-sharding and shard transfer

Lock acquisition pattern:

- **Write lock**: Held during all update operations and segment state changes
- **Read lock**: Held during scroll operations and while segments are in proxied state
- **Blocking operations**: Uses `blocking_write()` in sync contexts, `write().await` in async

The lock is passed to `proxy_all_segments_and_apply` which acquires it via `update_lock.blocking_write()` when unproxying segments, ensuring no updates can modify segment state during transitions.

Sources: [lib/collection/src/shards/local\_shard/mod.rs108-124](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L108-L124) [lib/collection/src/shards/local\_shard/snapshot.rs218-352](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L218-L352) [lib/collection/src/shards/local\_shard/scroll.rs156-213](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/scroll.rs#L156-L213) [lib/collection/src/collection\_manager/collection\_updater.rs42-77](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection_manager/collection_updater.rs#L42-L77)

## Snapshot Recovery Process

Recovery restores a snapshot by unpacking segment data and reinitializing the shard. The `LocalShard::restore_snapshot` method handles segment-level recovery.

LocalShard Recovery: Segment restoration from snapshot archive

```
```

### Recovery Implementation Details

The recovery process follows these steps:

1. **Read snapshot directory**: `LocalShard::restore_snapshot` reads the `segments/` directory from the snapshot path
2. **Filter entries**: Hidden files (starting with `.`) are skipped to avoid temporary or system files
3. **Per-segment recovery**: Each segment directory calls `Segment::restore_snapshot_in_place` to unpack its data
4. **In-place restoration**: Segments restore themselves directly into their final location (no temporary moves)
5. **Error propagation**: Any segment restoration failure aborts the entire recovery

Key characteristics:

- **No WAL replay**: Recovery assumes snapshot contains complete data; WAL (if present) provides operation history but isn't replayed
- **Atomic per-segment**: Each segment restores atomically, but overall recovery is not atomic across all segments
- **Path-based**: Recovery expects a specific directory structure with `segments/` and `wal/` subdirectories

### Directory Structure After Recovery

```
shard_path/
├── segments/
│   ├── <segment_id_1>/
│   │   ├── segment.json
│   │   ├── vector_storage/
│   │   └── payload_index/
│   ├── <segment_id_2>/
│   └── ...
├── wal/
│   └── (WAL files)
├── newest_clocks.json
└── oldest_clocks.json
```

Sources: [lib/collection/src/shards/local\_shard/snapshot.rs33-59](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/snapshot.rs#L33-L59) [lib/collection/src/shards/local\_shard/mod.rs76-83](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs#L76-L83)

## Consensus and State Management

In distributed deployments, snapshot operations coordinate with the Raft consensus system to maintain cluster consistency:

```
```

The system handles complex scenarios like:

- **Split-brain prevention**: Consensus ensures only valid state transitions
- **Replication factor maintenance**: Automatic replica management during recovery
- **Synchronization conflicts**: Priority-based resolution when multiple replicas exist
- **Partial snapshot locks**: Prevents concurrent partial snapshot operations

Sources: [lib/storage/src/content\_manager/snapshots/recover.rs213-346](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/snapshots/recover.rs#L213-L346) [lib/collection/src/shards/replica\_set/snapshots.rs34-109](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/snapshots.rs#L34-L109) [src/common/snapshots.rs318-337](https://github.com/qdrant/qdrant/blob/48203e41/src/common/snapshots.rs#L318-L337)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Snapshots and Recovery](#snapshots-and-recovery.md)
- [Snapshot Creation Architecture](#snapshot-creation-architecture.md)
- [Segment Proxying Mechanism](#segment-proxying-mechanism.md)
- [Snapshot Creation Process](#snapshot-creation-process.md)
- [WAL Handling Strategies](#wal-handling-strategies.md)
- [Update Lock Coordination](#update-lock-coordination.md)
- [Snapshot Recovery Process](#snapshot-recovery-process.md)
- [Recovery Implementation Details](#recovery-implementation-details.md)
- [Directory Structure After Recovery](#directory-structure-after-recovery.md)
- [Consensus and State Management](#consensus-and-state-management.md)
