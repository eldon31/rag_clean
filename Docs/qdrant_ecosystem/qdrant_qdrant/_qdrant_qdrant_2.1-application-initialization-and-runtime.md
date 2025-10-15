Application Initialization and Runtime | qdrant/qdrant | DeepWiki

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

# Application Initialization and Runtime

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

This document describes how Qdrant initializes and runs as a service, covering the entry point, configuration loading, runtime creation, storage initialization, API server setup, and thread management. For information about the collections and data management layer, see [Collections and Table of Content](qdrant/qdrant/2.2-collections-and-table-of-content.md). For distributed consensus mechanics, see [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md).

## Entry Point and Command-Line Arguments

The application starts in the `main()` function at [src/main.rs140-645](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L140-L645) The entry point handles:

- Command-line argument parsing using the `Args` struct
- Settings initialization from configuration files
- Global feature flags setup
- Logging infrastructure configuration
- Panic hook registration
- Core initialization sequence

### Command-Line Arguments

The `Args` struct [src/main.rs72-138](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L72-L138) defines the CLI interface:

```
Args
├── bootstrap: Option<Uri>        // Bootstrap peer for joining cluster
├── uri: Option<Uri>              // This peer's advertised URI
├── force_snapshot: bool          // Force collection recreation from snapshots
├── snapshot: Option<Vec<String>> // Individual collection snapshots
├── storage_snapshot: Option<String> // Full storage snapshot
├── config_path: Option<String>   // Alternative config file path
├── disable_telemetry: bool       // Disable telemetry reporting
├── stacktrace: bool              // Run stacktrace collector
└── reinit: bool                  // Reinitialize consensus state
```

**Sources:** [src/main.rs72-138](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L72-L138)

### Initialization Sequence Overview

```
```

**Sources:** [src/main.rs140-645](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L140-L645)

## Configuration Loading

Configuration is loaded through a hierarchical system managed by the `Settings` struct. The loading order (from lowest to highest precedence) is:

```
```

The `Settings::new()` function [src/settings.rs230-286](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L230-L286) implements this hierarchy using the `config` crate. Configuration sources are merged, with later sources overriding earlier ones.

**Key Configuration Sections:**

| Section   | Description                                   | Struct          |
| --------- | --------------------------------------------- | --------------- |
| `storage` | Storage paths, optimizers, WAL, HNSW settings | `StorageConfig` |
| `service` | HTTP/gRPC ports, TLS, API keys, CORS          | `ServiceConfig` |
| `cluster` | Distributed mode, P2P settings, consensus     | `ClusterConfig` |
| `tls`     | Certificate paths, CA cert, TTL               | `TlsConfig`     |
| `logger`  | Logging configuration                         | `LoggerConfig`  |

**Sources:** [src/settings.rs197-327](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L197-L327) [config/config.yaml1-355](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L1-L355)

## Runtime Creation

Qdrant uses three separate Tokio runtimes to isolate different workload types:

### Runtime Architecture

```
```

**Sources:** [src/main.rs309-322](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L309-L322) [src/common/helpers.rs20-63](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L20-L63)

### Runtime Creation Details

The three runtimes are created at [src/main.rs309-322](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L309-L322):

1. **Search Runtime** [src/common/helpers.rs20-32](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L20-L32)

   - Thread count: `common::defaults::search_thread_count(max_search_threads)`
   - Used for all search and query operations
   - Each thread can handle blocking operations

2. **Update Runtime** [src/common/helpers.rs34-50](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L34-L50)

   - Thread count: Configurable via `max_optimization_runtime_threads`
   - Used for segment optimization and index building
   - Background workers run here

3. **General Purpose Runtime** [src/common/helpers.rs52-63](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L52-L63)

   - Thread count: `max(num_cpus, 2)`
   - Used for API request handling, consensus, and general async operations
   - Handle to this runtime is stored for use throughout the application

**Sources:** [src/main.rs309-322](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L309-L322) [src/common/helpers.rs20-63](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L20-L63)

## Storage Initialization: TableOfContent

The `TableOfContent` (ToC) is the central collection manager. It's initialized at [src/main.rs365-383](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L365-L383):

```
```

The ToC is then wrapped in an `Arc` for shared ownership across threads [src/main.rs385](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L385-L385)

**Sources:** [src/main.rs365-386](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L365-L386)

## Distributed vs Standalone Mode

The application can run in two modes, controlled by `settings.cluster.enabled`:

```
```

**Sources:** [src/main.rs280-502](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L280-L502)

### Standalone Mode

In standalone mode [src/main.rs494-502](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L494-L502):

- No consensus manager is created
- `Dispatcher` routes requests directly to `TableOfContent`
- Only external REST and gRPC APIs are started
- Single-node operation, no replication

### Distributed Mode

In distributed mode [src/main.rs395-493](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L395-L493):

1. **Consensus State Initialization** [src/main.rs396-403](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L396-L403)

   - Creates `ConsensusManager` with persistent state
   - Wraps in `ConsensusStateRef` for shared access

2. **Dispatcher Configuration** [src/main.rs405-409](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L405-L409)

   - Dispatcher is configured with consensus state
   - Routes metadata operations through Raft consensus

3. **Consensus Thread** [src/main.rs432-447](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L432-L447)

   - Spawned via `Consensus::run()`
   - Runs Raft protocol in dedicated thread
   - Processes proposals from `propose_receiver` channel

4. **Internal gRPC Server** [src/main.rs152-168](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L152-L168) in [src/consensus.rs96-170](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L96-L170)

   - Started via `init_internal()` in separate thread
   - Handles inter-peer Raft messages
   - P2P communication on configured port

**Sources:** [src/main.rs395-493](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L395-L493) [src/consensus.rs63-170](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L63-L170)

## Dispatcher and Request Routing

The `Dispatcher` acts as the routing layer between API servers and storage:

```
```

**Creation:**

- Standalone: `Dispatcher::new(toc)` [src/main.rs393](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L393-L393)
- Distributed: `dispatcher.with_consensus(consensus_state, resharding_enabled)` [src/main.rs405-406](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L405-L406)

**Sources:** [src/main.rs393-411](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L393-L411)

## API Server Initialization

### Thread Topology

The application spawns multiple threads for different services:

```
```

**Sources:** [src/main.rs389-641](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L389-L641)

### REST API Server (Actix-web)

Started at [src/main.rs549-568](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L549-L568):

```
```

The `actix::init()` function [src/actix/mod.rs55-205](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L205):

- Binds to `settings.service.host:http_port`
- Configures middleware (compression, CORS, authentication, logging)
- Registers all API endpoints
- Optionally enables TLS with certificate rotation
- Worker count: `max_web_workers(&settings)`

**Key Features:**

- **Authentication:** API key middleware via `Auth` layer
- **Compression:** Automatic gzip compression
- **Validation:** Request validation using `actix-web-validator`
- **TLS:** Optional with certificate TTL rotation [src/actix/certificate\_helpers.rs1-207](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/certificate_helpers.rs#L1-L207)

**Sources:** [src/main.rs549-568](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L549-L568) [src/actix/mod.rs55-205](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L205)

### Public gRPC API Server (Tonic)

Started at [src/main.rs574-592](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L574-L592) if `settings.service.grpc_port` is set:

```
```

The `tonic::init()` function [src/tonic/mod.rs147-253](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L253):

- Binds to `settings.service.host:grpc_port`
- Registers services: `Qdrant`, `Collections`, `Points`, `Snapshots`, `Health`
- Configures middleware (logging, telemetry, authentication)
- Enables gRPC reflection
- Optional TLS configuration

**Services Registered:**

- `QdrantServer` - Health checks and version info
- `CollectionsServer` - Collection management
- `PointsServer` - Point operations
- `SnapshotsServer` - Snapshot operations
- `HealthServer` - Standard gRPC health protocol

**Sources:** [src/main.rs574-592](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L574-L592) [src/tonic/mod.rs147-253](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L253)

### Internal gRPC Server (Distributed Mode Only)

Started within the consensus thread at [src/consensus.rs152-168](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L152-L168):

```
```

The `init_internal()` function [src/tonic/mod.rs256-360](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L256-L360):

- Binds to `settings.service.host:p2p.port`
- Handles Raft messages between peers
- Provides internal APIs for shard transfers and consensus
- Mandatory TLS configuration in production clusters

**Internal Services:**

- `RaftServer` - Raft message handling [src/tonic/api/raft\_api.rs16-150](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L16-L150)
- `QdrantInternalServer` - Consensus commit tracking
- `PointsInternalServer` - Internal point operations
- `CollectionsInternalServer` - Internal collection operations
- `ShardSnapshotsServer` - Shard snapshot transfers

**Sources:** [src/consensus.rs152-168](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L152-L168) [src/tonic/mod.rs256-360](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L256-L360)

## Consensus Thread Lifecycle

In distributed mode, the consensus thread is critical for cluster coordination:

### Consensus Thread Setup

```
```

**Sources:** [src/consensus.rs63-170](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L63-L170) [src/main.rs329-447](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L329-L447)

### Consensus Initialization Flow

The `Consensus::run()` function [src/consensus.rs63-170](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L63-L170) performs:

1. **TLS Configuration** [src/consensus.rs76](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L76-L76)

   - Loads TLS client config if `cluster.p2p.enable_tls` is enabled

2. **Consensus Object Creation** [src/consensus.rs82-93](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L82-L93)

   - Calls `Consensus::new()` with state, bootstrap peer, URI, config
   - Creates bounded tokio channel for backpressure

3. **Bootstrap or Recovery** [src/consensus.rs213-244](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L213-L244)

   - New deployment: Bootstrap from peer or initialize as first peer
   - Existing deployment: Recover state and potentially update URI

4. **Thread Spawning** [src/consensus.rs96-115](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L96-L115)

   - Main consensus thread runs `consensus.start()`
   - Sets high thread priority on Linux for better latency
   - Error handling reports to `ConsensusStateRef`

5. **Proposal Forwarder** [src/consensus.rs117-139](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L117-L139)

   - Separate thread forwards proposals from `std::sync::mpsc` to tokio channel
   - Bridges sync and async worlds

6. **Internal gRPC Server** [src/consensus.rs152-168](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L152-L168)

   - Spawns thread for internal peer communication
   - Receives Raft messages via gRPC and forwards to consensus

**Sources:** [src/consensus.rs63-244](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L63-L244)

## Resource Budgets

Before initialization, CPU and I/O budgets are computed for optimization tasks:

```
```

These budgets control how many CPU cores and parallel I/O operations can be used for segment optimization and index building [src/main.rs325-327](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L325-L327)

**Sources:** [src/main.rs325-327](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L325-L327)

## Telemetry and Monitoring

Telemetry collection is initialized for both standalone and distributed modes:

```
```

If reporting is enabled, a background task is spawned to periodically report metrics [src/main.rs513-519](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L513-L519)

**Sources:** [src/main.rs413-519](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L413-L519)

## Lifecycle Management

The main thread waits for all spawned threads to complete:

```
```

This blocks until a shutdown signal is received by one of the servers [src/main.rs635-641](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L635-L641)

**Shutdown Handling:**

- REST API: Controlled by Actix runtime
- gRPC API: Uses `wait_stop_signal()` [src/tonic/mod.rs130-145](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L130-L145)
- Signals: SIGTERM and SIGINT are handled gracefully

**Sources:** [src/main.rs635-645](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L635-L645) [src/tonic/mod.rs130-145](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L130-L145)

## Summary: Complete Initialization Flow

```
```

**Sources:** [src/main.rs140-645](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L140-L645)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Application Initialization and Runtime](#application-initialization-and-runtime.md)
- [Entry Point and Command-Line Arguments](#entry-point-and-command-line-arguments.md)
- [Command-Line Arguments](#command-line-arguments.md)
- [Initialization Sequence Overview](#initialization-sequence-overview.md)
- [Configuration Loading](#configuration-loading.md)
- [Runtime Creation](#runtime-creation.md)
- [Runtime Architecture](#runtime-architecture.md)
- [Runtime Creation Details](#runtime-creation-details.md)
- [Storage Initialization: TableOfContent](#storage-initialization-tableofcontent.md)
- [Distributed vs Standalone Mode](#distributed-vs-standalone-mode.md)
- [Standalone Mode](#standalone-mode.md)
- [Distributed Mode](#distributed-mode.md)
- [Dispatcher and Request Routing](#dispatcher-and-request-routing.md)
- [API Server Initialization](#api-server-initialization.md)
- [Thread Topology](#thread-topology.md)
- [REST API Server (Actix-web)](#rest-api-server-actix-web.md)
- [Public gRPC API Server (Tonic)](#public-grpc-api-server-tonic.md)
- [Internal gRPC Server (Distributed Mode Only)](#internal-grpc-server-distributed-mode-only.md)
- [Consensus Thread Lifecycle](#consensus-thread-lifecycle.md)
- [Consensus Thread Setup](#consensus-thread-setup.md)
- [Consensus Initialization Flow](#consensus-initialization-flow.md)
- [Resource Budgets](#resource-budgets.md)
- [Telemetry and Monitoring](#telemetry-and-monitoring.md)
- [Lifecycle Management](#lifecycle-management.md)
- [Summary: Complete Initialization Flow](#summary-complete-initialization-flow.md)
