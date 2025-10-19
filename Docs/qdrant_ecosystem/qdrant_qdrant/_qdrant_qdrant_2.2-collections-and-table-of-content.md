Collections and Table of Content | qdrant/qdrant | DeepWiki

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

# Collections and Table of Content

Relevant source files

- [lib/collection/benches/batch\_query\_bench.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/benches/batch_query_bench.rs)
- [lib/collection/benches/batch\_search\_bench.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/benches/batch_search_bench.rs)
- [lib/collection/src/collection/collection\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs)
- [lib/collection/src/collection/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs)
- [lib/collection/src/collection/shard\_transfer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/shard_transfer.rs)
- [lib/collection/src/collection/sharding\_keys.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/sharding_keys.rs)
- [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)
- [lib/collection/src/shards/replica\_set/update.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/update.rs)
- [lib/collection/src/tests/snapshot\_test.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/tests/snapshot_test.rs)
- [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs)

## Purpose and Scope

This page describes the **TableOfContent** component and **Collection** abstraction, which together form the collection management layer in Qdrant. The TableOfContent (TOC) is the central registry that manages all collections in the system, while each Collection is a logical container for vector data, managing its configuration, shards, and operations.

This page covers:

- TableOfContent structure and responsibilities
- Collection abstraction and lifecycle
- Collection meta-operations (create, update, delete, aliases)
- Configuration management and persistence

For shard-level architecture and replica coordination, see [2.3](qdrant/qdrant/2.3-shards-and-replica-sets.md). For consensus-based operations in distributed mode, see [7.1](qdrant/qdrant/7.1-raft-consensus-protocol.md). For API endpoints that trigger these operations, see [9](qdrant/qdrant/9-api-reference.md).

## TableOfContent Component

The **TableOfContent** is the top-level management component that maintains a registry of all collections in the Qdrant instance. It acts as the entry point for all collection-level operations and orchestrates collection lifecycle management.

### Core Responsibilities

| Responsibility           | Description                                                                       |
| ------------------------ | --------------------------------------------------------------------------------- |
| Collection Registry      | Maintains in-memory map of collection name → `Collection` instance                |
| Meta-Operation Handling  | Processes `CollectionMetaOperations` for creating, updating, deleting collections |
| Alias Management         | Manages collection aliases for logical naming                                     |
| Persistence Coordination | Ensures collection configurations are saved to disk                               |
| Consensus Integration    | In distributed mode, applies operations from Raft consensus                       |

### TableOfContent in System Architecture

```
```

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs1-262](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L1-L262)

### Collection Meta-Operations

The TOC processes `CollectionMetaOperations`, which are the only operations that modify collection structure and configuration. These operations flow through consensus in distributed mode.

```
```

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs38-123](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L38-L123)

## Collection Abstraction

The **Collection** struct represents a single named collection and encapsulates all collection-level state, configuration, and operations. It manages shards, handles updates and queries, and maintains collection metadata.

### Collection Structure

```
```

**Sources:** [lib/collection/src/collection/mod.rs62-94](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L62-L94)

### Key Collection Fields

| Field                    | Type                                    | Purpose                                      |
| ------------------------ | --------------------------------------- | -------------------------------------------- |
| `id`                     | `CollectionId`                          | Unique collection name                       |
| `shards_holder`          | `Arc<LockedShardHolder>`                | Manages all shards and their replica sets    |
| `collection_config`      | `Arc<RwLock<CollectionConfigInternal>>` | Collection parameters and configuration      |
| `payload_index_schema`   | `Arc<SaveOnDisk<PayloadIndexSchema>>`   | Schema for payload field indices             |
| `transfer_tasks`         | `Mutex<TransferTasksPool>`              | Active shard transfer tasks                  |
| `is_initialized`         | `Arc<IsReady>`                          | Flag set when all shards are first activated |
| `updates_lock`           | `Arc<RwLock<()>>`                       | Prevents updates during migration operations |
| `collection_stats_cache` | `CollectionSizeStatsCache`              | Cached collection size statistics            |

**Sources:** [lib/collection/src/collection/mod.rs62-94](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L62-L94)

## Collection Lifecycle

Collections have a well-defined lifecycle managed by the TableOfContent component.

### Collection Creation Flow

```
```

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs39-69](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L39-L69) [lib/collection/src/collection/mod.rs103-200](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L103-L200)

### Collection Loading Flow

On startup, collections are loaded from disk:

```
```

**Sources:** [lib/collection/src/collection/mod.rs203-316](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L203-L316) [lib/collection/src/shards/replica\_set/mod.rs238-382](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L238-L382)

### Version Compatibility

Collections enforce version compatibility to ensure safe upgrades:

```
```

**Sources:** [lib/collection/src/collection/mod.rs318-339](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L318-L339)

### Collection Deletion Flow

```
```

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs189-262](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L189-L262)

## Collection Configuration

Each collection is configured via `CollectionConfigInternal`, which contains all parameters that define the collection's behavior.

### Configuration Components

```
```

**Sources:** [lib/collection/src/collection/mod.rs65](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L65-L65) [lib/collection/benches/batch\_search\_bench.rs66-90](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/benches/batch_search_bench.rs#L66-L90)

### Configuration Updates

Collections support dynamic configuration updates via `UpdateCollectionOperation`:

```
```

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs125-187](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L125-L187) [lib/collection/src/collection/collection\_ops.rs31-204](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs#L31-L204)

## Collection State and Operations

### Collection State Structure

The `Collection::state()` method returns a complete snapshot of the collection's current state:

```
```

**Sources:** [lib/collection/src/collection/mod.rs544-564](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L544-L564)

### Collection Info Retrieval

The `Collection::info()` method aggregates information from all shards:

```
```

**Sources:** [lib/collection/src/collection/collection\_ops.rs301-340](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs#L301-L340)

### Cluster Information

For distributed deployments, `Collection::cluster_info()` provides per-peer shard distribution:

| Info Type               | Contents                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `local_shards`          | Shards with local replicas on this peer (shard\_id, points\_count, state, shard\_key) |
| `remote_shards`         | Remote shard replicas on other peers (shard\_id, peer\_id, state, shard\_key)         |
| `shard_transfers`       | Active shard transfer operations                                                      |
| `resharding_operations` | Active resharding operations                                                          |

**Sources:** [lib/collection/src/collection/collection\_ops.rs342-409](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/collection_ops.rs#L342-L409)

## Alias Management

The TableOfContent manages collection aliases, providing logical names for collections:

```
```

The alias operations are atomic - all aliases in a `ChangeAliasesOperation` are applied together while holding both collection and alias write locks, preventing partial updates and race conditions.

**Sources:** [lib/storage/src/content\_manager/toc/collection\_meta\_ops.rs264-304](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/collection_meta_ops.rs#L264-L304)

## Collection Persistence

Collections persist their state across multiple files and directories:

```
storage_path/
└── collections/
    └── {collection_name}/
        ├── collection_config.json      # CollectionConfigInternal
        ├── .collection_version          # Version marker
        ├── payload_index_schema.json   # PayloadIndexSchema
        ├── shard_key_mapping.json      # ShardKeyMapping (if custom sharding)
        └── shards/
            ├── {shard_id}/
            │   ├── replica_state.json   # ReplicaSetState
            │   ├── shard_config.json    # ShardConfig
            │   ├── segments/            # Segment data (see 2.5)
            │   └── wal/                 # Write-Ahead Log
            └── ...
```

Each component saves independently using `SaveOnDisk` wrapper, which provides atomic updates via rename operations.

**Sources:** [lib/collection/src/collection/mod.rs103-200](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L103-L200) [lib/collection/src/shards/replica\_set/mod.rs128-230](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs#L128-L230)

## Collection Initialization States

Collections track initialization via the `is_initialized` flag, which is set when all shards reach an active state for the first time:

```
```

This flag ensures that the collection is fully operational before serving production traffic. It accounts for:

- Initial shard creation in distributed mode
- Shard transfers completing
- Recovery from failures

**Sources:** [lib/collection/src/collection/mod.rs486-509](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection/mod.rs#L486-L509)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Collections and Table of Content](#collections-and-table-of-content.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [TableOfContent Component](#tableofcontent-component.md)
- [Core Responsibilities](#core-responsibilities.md)
- [TableOfContent in System Architecture](#tableofcontent-in-system-architecture.md)
- [Collection Meta-Operations](#collection-meta-operations.md)
- [Collection Abstraction](#collection-abstraction.md)
- [Collection Structure](#collection-structure.md)
- [Key Collection Fields](#key-collection-fields.md)
- [Collection Lifecycle](#collection-lifecycle.md)
- [Collection Creation Flow](#collection-creation-flow.md)
- [Collection Loading Flow](#collection-loading-flow.md)
- [Version Compatibility](#version-compatibility.md)
- [Collection Deletion Flow](#collection-deletion-flow.md)
- [Collection Configuration](#collection-configuration.md)
- [Configuration Components](#configuration-components.md)
- [Configuration Updates](#configuration-updates.md)
- [Collection State and Operations](#collection-state-and-operations.md)
- [Collection State Structure](#collection-state-structure.md)
- [Collection Info Retrieval](#collection-info-retrieval.md)
- [Cluster Information](#cluster-information.md)
- [Alias Management](#alias-management.md)
- [Collection Persistence](#collection-persistence.md)
- [Collection Initialization States](#collection-initialization-states.md)
