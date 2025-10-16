System Architecture | qdrant/qdrant | DeepWiki

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

# System Architecture

Relevant source files

- [Cargo.lock](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.lock)
- [Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml)
- [config/config.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml)
- [docs/redoc/default\_version.js](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/default_version.js)
- [docs/redoc/index.html](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/index.html)
- [docs/redoc/v0.10.3/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.3/openapi.json)
- [docs/redoc/v0.10.4/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.4/openapi.json)
- [docs/redoc/v0.10.5/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.5/openapi.json)
- [docs/redoc/v1.10.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.10.x/openapi.json)
- [docs/redoc/v1.11.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.11.x/openapi.json)
- [docs/redoc/v1.13.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.13.x/openapi.json)
- [docs/redoc/v1.15.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.15.x/openapi.json)
- [lib/api/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/Cargo.toml)
- [lib/collection/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml)
- [lib/collection/src/common/snapshots\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/common/snapshots_manager.rs)
- [lib/collection/src/operations/shared\_storage\_config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs)
- [lib/common/common/src/defaults.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs)
- [lib/common/dataset/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/dataset/Cargo.toml)
- [lib/common/issues/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/issues/Cargo.toml)
- [lib/segment/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml)
- [lib/sparse/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/Cargo.toml)
- [lib/storage/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml)
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
- [tools/missed\_cherry\_picks.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/missed_cherry_picks.sh)

## Purpose and Scope

This document provides a comprehensive overview of Qdrant's system architecture, describing the layered design from the API layer down to persistent storage. It covers both standalone and distributed deployment modes, the core abstractions at each layer, and how components interact to serve search and update operations.

For specific details on:

- Application startup and runtime initialization, see [Application Initialization and Runtime](qdrant/qdrant/2.1-application-initialization-and-runtime.md)
- Collection management and the table of content system, see [Collections and Table of Content](qdrant/qdrant/2.2-collections-and-table-of-content.md)
- Shard distribution and replica coordination, see [Shards and Replica Sets](qdrant/qdrant/2.3-shards-and-replica-sets.md)
- Internal structure of local shards, see [Local Shard Architecture](qdrant/qdrant/2.4-local-shard-architecture.md)
- Segment construction and optimization, see [Segment Lifecycle and Construction](qdrant/qdrant/2.5-segment-lifecycle-and-construction.md)
- Vector indexing strategies, see [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md)
- Consensus and distributed features, see [Distributed System Features](qdrant/qdrant/7-distributed-system-features.md)

---

## Architectural Overview

Qdrant employs a **layered architecture** with clear separation of concerns. The system is organized into six primary layers, each responsible for specific aspects of data management and query processing.

### System Layers

```
```

**Sources:** [src/main.rs1-700](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L1-L700) [lib/storage/src/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/dispatcher.rs) [lib/storage/src/content\_manager/toc/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/mod.rs) [lib/collection/src/collection.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection.rs) [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs)

### Layer Responsibilities

| Layer                     | Primary Components                                 | Responsibilities                                                         |
| ------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------ |
| **API Layer**             | `actix::init`, `tonic::init`                       | HTTP/REST and gRPC endpoints, request validation, authentication         |
| **Service Orchestration** | `Dispatcher`, `ConsensusManager`, `TableOfContent` | Request routing, consensus coordination, collection lifecycle management |
| **Collection Layer**      | `Collection`, `ShardHolder`                        | Logical data containers, shard key routing, collection-level operations  |
| **Shard Layer**           | `ShardReplicaSet`, `LocalShard`, `RemoteShard`     | Data partitioning, replication, replica coordination, update ordering    |
| **Segment Layer**         | `Segment`, `SegmentHolder`, `UpdateHandler`        | Data unit management, indexing, background optimization                  |
| **Storage/Index Layer**   | Vector/Payload indices and storage                 | Physical data storage, index structures, persistence                     |

**Sources:** [src/actix/mod.rs55-205](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L205) [src/tonic/mod.rs147-240](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L240) [lib/storage/src/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/dispatcher.rs)

---

## Deployment Modes

Qdrant supports two deployment modes configured via the `cluster.enabled` setting in [config/config.yaml301-303](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L301-L303)

### Standalone Mode

In standalone mode, Qdrant runs as a single node without distributed consensus. The `Dispatcher` routes requests directly to `TableOfContent` without going through the consensus layer.

```
```

**Sources:** [src/main.rs494-502](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L494-L502) [lib/storage/src/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/dispatcher.rs)

### Distributed Mode

In distributed mode (when `cluster.enabled = true`), the system uses Raft consensus for metadata coordination. The `Dispatcher` routes metadata operations through `ConsensusManager`, while data operations go directly to shards with optimistic replication.

```
```

**Sources:** [src/main.rs395-493](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L395-L493) [src/consensus.rs45-283](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L45-L283) [lib/storage/src/content\_manager/consensus\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_manager.rs)

---

## API Layer

The API layer provides REST and gRPC interfaces for client communication. Both protocols expose equivalent functionality.

### REST API (Actix-web)

The REST API runs on port 6333 (configurable via `service.http_port`) and uses the Actix-web framework.

**Key components:**

- **Entry point:** `actix::init` in [src/actix/mod.rs55-205](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L205)

- **HTTP server configuration:** [src/actix/mod.rs99-200](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L99-L200)

- **Endpoint modules:**

  - Collections API: [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs)
  - Search API: [src/actix/api/search\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/search_api.rs)
  - Update API: [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)
  - Cluster API: [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)
  - Snapshots API: [src/actix/api/snapshot\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/snapshot_api.rs)

**Sources:** [src/actix/mod.rs1-264](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L1-L264) [config/config.yaml234-246](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L234-L246)

### gRPC API (Tonic)

The gRPC API runs on port 6334 (configurable via `service.grpc_port`) and uses the Tonic framework. It provides:

- **Public gRPC services:** `QdrantServer`, `CollectionsServer`, `PointsServer`, `SnapshotsServer`
- **Internal gRPC services:** `QdrantInternalServer`, `RaftServer` (for peer-to-peer communication)

**Key components:**

- **Entry point:** `tonic::init` in [src/tonic/mod.rs147-240](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L240)
- **Service implementations:** [src/tonic/api/](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/)
- **Internal P2P port:** Configured via `cluster.p2p.port` [config/config.yaml306-308](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L306-L308)

**Sources:** [src/tonic/mod.rs1-290](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L1-L290) [config/config.yaml248-251](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L248-L251)

### Authentication and Authorization

Both API layers support:

- **API key authentication:** Via `service.api_key` and `service.read_only_api_key` [config/config.yaml266-285](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L266-L285)
- **JWT RBAC:** Via `service.jwt_rbac` for fine-grained access control
- **TLS encryption:** Via `service.enable_tls` and `cluster.p2p.enable_tls` [config/config.yaml259-312](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L259-L312)

**Sources:** [src/actix/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/auth.rs) [src/tonic/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/auth.rs) [src/settings.rs22-66](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L22-L66)

---

## Service Orchestration Layer

This layer coordinates request routing, consensus, and collection management.

### Dispatcher

The `Dispatcher` is the central request router that determines whether operations should:

1. Go directly to `TableOfContent` (standalone mode or data operations)
2. Pass through `ConsensusManager` (distributed mode metadata operations)

**Code entity:** `storage::dispatcher::Dispatcher` in [lib/storage/src/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/dispatcher.rs)

```
```

**Sources:** [lib/storage/src/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/dispatcher.rs) [src/main.rs391-407](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L391-L407)

### ConsensusManager

The `ConsensusManager` wraps the Raft state machine and manages consensus operations for cluster metadata.

**Key responsibilities:**

- Proposing operations to Raft consensus
- Applying committed operations to `TableOfContent`
- Managing peer membership and addresses
- Handling snapshot requests and transfers

**Code entity:** `storage::content_manager::consensus_manager::ConsensusManager` in [lib/storage/src/content\_manager/consensus\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_manager.rs)

**Metadata operations** managed by consensus (defined in [lib/storage/src/content\_manager/mod.rs20-146](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs#L20-L146)):

- `CollectionMetaOperations` - collection creation, deletion, updates
- `AddPeer`, `RemovePeer` - peer membership changes
- `UpdatePeerMetadata` - peer metadata updates
- `RequestSnapshot`, `ReportSnapshot` - snapshot coordination

**Sources:** [lib/storage/src/content\_manager/consensus\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/consensus_manager.rs) [lib/storage/src/content\_manager/mod.rs20-146](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs#L20-L146) [src/consensus.rs44-627](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L44-L627)

### TableOfContent

The `TableOfContent` (TOC) manages all collections in the system. It acts as the collection registry and provides methods for collection lifecycle management.

**Code entity:** `storage::content_manager::toc::TableOfContent` in [lib/storage/src/content\_manager/toc/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/mod.rs)

**Key responsibilities:**

- Collection creation, deletion, and updates
- Collection metadata persistence
- Collection access control
- Coordinating collection operations across the cluster

**Initialization** in [src/main.rs365-377](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L365-L377):

```
let toc = TableOfContent::new(
    &settings.storage,
    search_runtime,
    update_runtime,
    general_runtime,
    optimizer_resource_budget,
    channel_service.clone(),
    persistent_consensus_state.this_peer_id(),
    propose_operation_sender.clone(),
);
```

**Sources:** [lib/storage/src/content\_manager/toc/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/toc/mod.rs) [src/main.rs365-383](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L365-L383)

---

## Collection and Shard Layer

### Collection

A `Collection` is the primary logical container for vector data. Each collection has:

- A unique name
- Configuration (vector dimensions, distance metric, etc.)
- One or more shards for data partitioning
- Optional shard keys for custom partitioning

**Code entity:** `collection::Collection` in [lib/collection/src/collection.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection.rs)

**Key components:**

- `ShardHolder` - manages shard distribution
- `CollectionConfig` - collection configuration
- `CollectionParams` - collection parameters

**Sources:** [lib/collection/src/collection.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection.rs) [lib/collection/src/config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs)

### ShardHolder

The `ShardHolder` maps data to shards and manages shard distribution. It supports two partitioning strategies:

1. **Hash-based partitioning** - automatic distribution using `HashRing`
2. **Shard key-based partitioning** - custom partitioning using user-defined shard keys

**Code entity:** `collection::shards::shard_holder::ShardHolder` in [lib/collection/src/shards/shard\_holder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/shard_holder.rs)

```
```

**Sources:** [lib/collection/src/shards/shard\_holder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/shard_holder.rs) [lib/collection/src/shards/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/mod.rs)

### ShardReplicaSet

A `ShardReplicaSet` coordinates multiple replicas of a single shard across peers. It handles:

- Replica state management (Active, Dead, Listener, Initializing, etc.)
- Update ordering and clock synchronization
- Write consistency enforcement
- Replica failover

**Code entity:** `collection::shards::replica_set::ShardReplicaSet` in [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs)

**Replica types:**

- `LocalShard` - replica hosted on current peer
- `RemoteShard` - proxy to replica on another peer
- `QueueProxyShard` - proxy for updates during shard transfers

**Sources:** [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs) [lib/collection/src/shards/replica\_set/replica\_state.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/replica_state.rs)

---

## Shard and Segment Layer

### LocalShard

A `LocalShard` is the core data-holding component on each peer. It contains:

- `SegmentHolder` - manages multiple segments
- `RecoverableWal` - write-ahead log for durability
- `UpdateHandler` - background optimization workers
- `LocalShardClocks` - logical clocks for update ordering

**Code entity:** `collection::shards::local_shard::LocalShard` in [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)

```
```

**Update flow:**

1. Write to WAL [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)
2. Apply to segments via `SegmentHolder`
3. Trigger optimization check via `UpdateHandler`

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs) [lib/collection/src/shards/update\_tracker.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/update_tracker.rs)

### Segment

A `Segment` is the fundamental unit of data storage and indexing. Each segment contains:

- `IdTracker` - maps external IDs to internal IDs
- `VectorData` - one or more named vector storages and indices
- `PayloadStorage` - JSON payload data
- `StructPayloadIndex` - field indices for filtering

**Code entity:** `segment::segment::Segment` in [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs)

**Segment types:**

- **Plain segments** - unindexed, for small datasets or during construction
- **Indexed segments** - with HNSW or other vector indices

**Sources:** [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs) [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)

### SegmentHolder

The `SegmentHolder` manages all segments within a shard and coordinates segment-level operations.

**Code entity:** `collection::shards::segment_holder::SegmentHolder` in [lib/collection/src/shards/local\_shard/segment\_holder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/segment_holder.rs)

**Key operations:**

- Read operations across all segments
- Append-only segments for new data
- Locked segments during optimization
- Segment replacement during optimization

**Sources:** [lib/collection/src/shards/local\_shard/segment\_holder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/segment_holder.rs)

---

## Storage and Index Layer

### Vector Storage

Vector data is stored in specialized storage backends optimized for different access patterns:

| Storage Type              | Use Case                   | Code Entity                                            |
| ------------------------- | -------------------------- | ------------------------------------------------------ |
| `DenseSimpleStorage`      | In-memory, fast access     | `segment::vector_storage::simple_dense_vector_storage` |
| `DenseMmapStorage`        | Memory-mapped, low memory  | `segment::vector_storage::mmap_dense_vector_storage`   |
| `SparseVectorStorage`     | Sparse vectors             | `sparse::index::sparse_vector_index`                   |
| `MultiDenseVectorStorage` | Multiple vectors per point | `segment::vector_storage::multi_dense`                 |

**Configuration:** [config/config.yaml192-197](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L192-L197)

**Sources:** [lib/segment/src/vector\_storage/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/mod.rs) [lib/sparse/src/index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/mod.rs)

### Vector Indices

Vector similarity search is accelerated using various index types:

| Index Type    | Algorithm              | Best For                         |
| ------------- | ---------------------- | -------------------------------- |
| `HnswIndex`   | Hierarchical NSW graph | General purpose, fast searches   |
| `PlainIndex`  | Brute force            | Small datasets, perfect accuracy |
| `SparseIndex` | Inverted index         | Sparse vectors, keyword search   |

**Configuration:** [config/config.yaml151-174](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L151-L174)

**Sources:** [lib/segment/src/index/hnsw\_index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/mod.rs) [lib/segment/src/index/plain\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs) [lib/sparse/src/index/inverted\_index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/inverted_index/mod.rs)

### Payload Storage and Indices

Payload data (JSON documents) is stored and indexed for filtering:

**Payload storage backends:**

- `SimplePayloadStorage` - in-memory
- `OnDiskPayloadStorage` - RocksDB or Gridstore
- `MmapPayloadStorage` - memory-mapped

**Payload index types:**

- `NumericIndex` - range queries on numbers
- `KeywordIndex` - exact match on strings
- `FullTextIndex` - tokenized text search
- `GeoIndex` - geospatial queries
- `BoolIndex` - boolean values
- `NullIndex` - existence checks

**Sources:** [lib/segment/src/payload\_storage/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/payload_storage/mod.rs) [lib/segment/src/index/field\_index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/mod.rs)

### Write-Ahead Log

The WAL ensures durability by persisting operations before applying them to segments.

**Code entity:** `wal::RecoverableWal` from external crate [Cargo.toml70](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L70-L70) and [Cargo.toml275](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L275-L275)

**Configuration:** [config/config.yaml49-56](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L49-L56)

**Sources:** [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs) [config/config.yaml49-56](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L49-L56)

---

## Runtime Architecture

Qdrant uses multiple Tokio runtimes for workload isolation:

### Runtime Separation

```
```

**Runtime creation** in [src/main.rs309-322](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L309-L322):

```
let search_runtime = create_search_runtime(settings.storage.performance.max_search_threads)
let update_runtime = create_update_runtime(settings.storage.performance.max_optimization_runtime_threads)
let general_runtime = create_general_purpose_runtime()
```

**Runtime functions:**

- `create_search_runtime` - [src/common/helpers.rs20-32](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L20-L32)
- `create_update_runtime` - [src/common/helpers.rs34-50](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L34-L50)
- `create_general_purpose_runtime` - [src/common/helpers.rs52-63](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L52-L63)

**Sources:** [src/main.rs309-322](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L309-L322) [src/common/helpers.rs20-63](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L20-L63) [config/config.yaml64-96](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L64-L96)

### Resource Budgets

Qdrant uses CPU and IO budgets to control resource usage during optimization:

**CPU Budget:** Configured via `optimizer_cpu_budget` [config/config.yaml68-72](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L68-L72)

- If `0`: auto-select, reserve CPUs based on system size
- If negative: subtract this number from available CPUs
- If positive: use this exact number of CPUs

**IO Budget:** Configured via `optimizer_io_budget` [lib/storage/src/types.rs43-48](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L43-L48)

- Controls parallel IO operations during optimization
- Defaults to one IO operation per CPU

**Budget initialization** in [src/main.rs325-327](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L325-L327):

```
let cpu_budget = get_cpu_budget(settings.storage.performance.optimizer_cpu_budget);
let io_budget = get_io_budget(settings.storage.performance.optimizer_io_budget, cpu_budget);
let optimizer_resource_budget = ResourceBudget::new(cpu_budget, io_budget);
```

**Sources:** [src/main.rs325-327](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L325-L327) [lib/common/common/src/cpu.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/cpu.rs) [lib/common/common/src/budget.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/budget.rs)

---

## Data Flow Overview

### Write Path

```
```

**Sources:** [lib/storage/src/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/dispatcher.rs) [lib/collection/src/collection.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection.rs) [lib/collection/src/shards/replica\_set/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/replica_set/mod.rs) [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs)

### Search Path

```
```

**Sources:** [lib/collection/src/collection.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/collection.rs) [lib/collection/src/shards/local\_shard/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/shards/local_shard/mod.rs) [lib/segment/src/segment.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment.rs) [lib/segment/src/index/hnsw\_index/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/mod.rs)

---

## Configuration

The system is configured via YAML files with environment variable overrides. The configuration hierarchy is:

1. Compile-time defaults [src/settings.rs20](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L20-L20)
2. `config/config.yaml` [config/config.yaml1-355](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L1-L355)
3. Environment-specific config (e.g., `config/development.yaml`)
4. Local config `config/local.yaml` (not tracked in git)
5. Custom config via `--config-path` CLI argument
6. Environment variables prefixed with `QDRANT__`

**Configuration loading** in [src/settings.rs230-285](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L230-L285)

**Key configuration sections:**

- `storage` - storage paths, performance, optimizers
- `service` - HTTP/gRPC ports, TLS, API keys
- `cluster` - distributed mode, consensus, P2P
- `log_level` - logging configuration

**Sources:** [src/settings.rs196-326](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L196-L326) [config/config.yaml1-355](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L1-L355)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [System Architecture](#system-architecture.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Architectural Overview](#architectural-overview.md)
- [System Layers](#system-layers.md)
- [Layer Responsibilities](#layer-responsibilities.md)
- [Deployment Modes](#deployment-modes.md)
- [Standalone Mode](#standalone-mode.md)
- [Distributed Mode](#distributed-mode.md)
- [API Layer](#api-layer.md)
- [REST API (Actix-web)](#rest-api-actix-web.md)
- [gRPC API (Tonic)](#grpc-api-tonic.md)
- [Authentication and Authorization](#authentication-and-authorization.md)
- [Service Orchestration Layer](#service-orchestration-layer.md)
- [Dispatcher](#dispatcher.md)
- [ConsensusManager](#consensusmanager.md)
- [TableOfContent](#tableofcontent.md)
- [Collection and Shard Layer](#collection-and-shard-layer.md)
- [Collection](#collection.md)
- [ShardHolder](#shardholder.md)
- [ShardReplicaSet](#shardreplicaset.md)
- [Shard and Segment Layer](#shard-and-segment-layer.md)
- [LocalShard](#localshard.md)
- [Segment](#segment.md)
- [SegmentHolder](#segmentholder.md)
- [Storage and Index Layer](#storage-and-index-layer.md)
- [Vector Storage](#vector-storage.md)
- [Vector Indices](#vector-indices.md)
- [Payload Storage and Indices](#payload-storage-and-indices.md)
- [Write-Ahead Log](#write-ahead-log.md)
- [Runtime Architecture](#runtime-architecture.md)
- [Runtime Separation](#runtime-separation.md)
- [Resource Budgets](#resource-budgets.md)
- [Data Flow Overview](#data-flow-overview.md)
- [Write Path](#write-path.md)
- [Search Path](#search-path.md)
- [Configuration](#configuration.md)
