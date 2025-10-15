qdrant/qdrant | DeepWiki

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

# Introduction to Qdrant

Relevant source files

- [Cargo.lock](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.lock)
- [Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml)
- [README.md](https://github.com/qdrant/qdrant/blob/48203e41/README.md)
- [docs/CODE\_OF\_CONDUCT.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/CODE_OF_CONDUCT.md)
- [docs/CONTRIBUTING.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/CONTRIBUTING.md)
- [docs/DEVELOPMENT.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md)
- [docs/QUICK\_START.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/QUICK_START.md)
- [docs/imgs/ci-coverage-report.png](https://github.com/qdrant/qdrant/blob/48203e41/docs/imgs/ci-coverage-report.png)
- [docs/imgs/local-coverage-report.png](https://github.com/qdrant/qdrant/blob/48203e41/docs/imgs/local-coverage-report.png)
- [docs/redoc/default\_version.js](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/default_version.js)
- [docs/redoc/index.html](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/index.html)
- [docs/redoc/v0.10.3/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.3/openapi.json)
- [docs/redoc/v0.10.4/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.4/openapi.json)
- [docs/redoc/v0.10.5/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.5/openapi.json)
- [docs/redoc/v1.10.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.10.x/openapi.json)
- [docs/redoc/v1.11.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.11.x/openapi.json)
- [docs/redoc/v1.13.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.13.x/openapi.json)
- [docs/redoc/v1.15.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.15.x/openapi.json)
- [docs/roadmap/README.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/README.md)
- [docs/roadmap/roadmap-2022.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2022.md)
- [docs/roadmap/roadmap-2023.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2023.md)
- [docs/roadmap/roadmap-2024.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2024.md)
- [lib/api/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/Cargo.toml)
- [lib/collection/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml)
- [lib/common/common/src/defaults.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs)
- [lib/common/dataset/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/dataset/Cargo.toml)
- [lib/common/issues/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/issues/Cargo.toml)
- [lib/segment/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml)
- [lib/sparse/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/Cargo.toml)
- [lib/storage/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml)
- [tools/missed\_cherry\_picks.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/missed_cherry_picks.sh)

## Purpose and Scope

This document provides a high-level overview of Qdrant, a vector similarity search engine and vector database written in Rust. It covers the fundamental concepts, system architecture, and deployment modes. This introduction is intended to orient developers and operators to Qdrant's core functionality and how its major components fit together.

For detailed information about specific subsystems, see:

- System architecture layers: [System Architecture](qdrant/qdrant/2-system-architecture.md)
- Vector storage and indexing strategies: [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md)
- Distributed deployment and clustering: [Distributed System Features](qdrant/qdrant/7-distributed-system-features.md)
- API endpoints and interfaces: [API Reference](qdrant/qdrant/9-api-reference.md)

**Sources:** [README.md1-237](https://github.com/qdrant/qdrant/blob/48203e41/README.md#L1-L237) [Cargo.toml1-400](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L1-L400)

---

## What is Qdrant?

Qdrant (read: *quadrant*) is a production-ready vector similarity search engine that provides:

- **Vector storage and search**: Store high-dimensional vectors and perform similarity searches with various distance metrics (Dot product, Cosine, Euclidean)
- **Payload filtering**: Attach JSON payloads to vectors and filter search results based on payload values
- **Horizontal scaling**: Distributed deployment with sharding and replication for billion-scale datasets
- **Multiple APIs**: REST API (port 6333) and gRPC interface for production workloads
- **Persistence**: All data persisted to disk with write-ahead logging (WAL)

The system is designed for neural network and semantic-based matching applications, including semantic search, recommendation engines, and similarity-based retrieval systems.

**Sources:** [README.md22-28](https://github.com/qdrant/qdrant/blob/48203e41/README.md#L22-L28) [lib/common/common/src/defaults.rs9-13](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs#L9-L13)

---

## Core Concepts

### Points

A **point** is the fundamental data unit in Qdrant. Each point consists of:

| Component     | Description                                  |
| ------------- | -------------------------------------------- |
| **ID**        | Unique identifier (integer or UUID)          |
| **Vector(s)** | One or more dense or sparse vectors          |
| **Payload**   | Optional JSON object with arbitrary metadata |

Points are the entities that users create, update, search, and retrieve.

### Vectors

Vectors are numerical representations of data (embeddings). Qdrant supports:

- **Dense vectors**: Fixed-size arrays of floating-point numbers
- **Sparse vectors**: Vectors with mostly zero values, stored efficiently as index-value pairs
- **Multi-vectors**: Multiple vectors per point for different embedding models
- **Named vectors**: Collections can store multiple vector types per point

**Sources:** [README.md23-24](https://github.com/qdrant/qdrant/blob/48203e41/README.md#L23-L24) [QUICK\_START.md120-135](https://github.com/qdrant/qdrant/blob/48203e41/QUICK_START.md#L120-L135)

### Collections

A **collection** is a named container that groups points with a shared vector configuration. Collections define:

- Vector dimensions and distance metrics
- Indexing parameters (HNSW configuration)
- Optimization settings
- Sharding and replication strategy (in distributed mode)

```
```

**Diagram: Collection Structure**

**Sources:** [QUICK\_START.md44-116](https://github.com/qdrant/qdrant/blob/48203e41/QUICK_START.md#L44-L116) [lib/collection/Cargo.toml1-112](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml#L1-L112)

### Segments

Within each collection, data is organized into **segments** - immutable data units containing:

- Vector storage (dense/sparse vectors)
- Payload storage (JSON data)
- Vector indices (HNSW, Plain, or Sparse indices)
- Payload indices (for filtering)
- ID tracker (mapping external to internal IDs)

Segments are the basic unit of storage and optimization in Qdrant.

**Sources:** Diagram 1 in high-level architecture diagrams

---

## System Architecture Overview

Qdrant employs a layered architecture with clear separation of concerns:

```
```

**Diagram: Layered Architecture from API to Storage**

The key architectural layers are:

1. **API Layer**: HTTP/REST (Actix-web) and gRPC (Tonic) endpoints handle client requests
2. **Service Orchestration**: Request routing and consensus coordination
3. **Collection Management**: Logical data containers with sharding strategy
4. **Shard Distribution**: Local shards (hosted on current node) and remote shards (proxies to other peers)
5. **Segment Management**: Immutable data units with indices and storage
6. **Persistence**: Disk-backed storage with memory-mapped files and WAL

**Sources:** Diagram 1 from high-level architecture, [Cargo.toml78-86](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L78-L86) [lib/segment/Cargo.toml1-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml#L1-L223) [lib/collection/Cargo.toml1-112](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml#L1-L112)

---

## Deployment Modes

### Standalone Mode

In standalone mode, Qdrant runs as a single process:

```
```

**Diagram: Standalone Deployment**

- All data stored locally
- No consensus coordination overhead
- Suitable for development, testing, and single-machine production deployments

### Distributed Mode

In distributed mode, multiple Qdrant peers form a cluster using Raft consensus:

```
```

**Diagram: Distributed Cluster with 3 Peers**

- **Raft consensus**: Metadata operations (collection creation, shard transfers) use Raft for strong consistency
- **Sharding**: Collections divided into shards distributed across peers
- **Replication**: Each shard can have multiple replicas on different peers
- **Internal gRPC**: Peers communicate via internal gRPC port for replication and forwarding

**Sources:** Diagram 4 from high-level architecture, [Cargo.toml103-114](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L103-L114) [lib/storage/Cargo.toml43-49](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml#L43-L49)

---

## API Interfaces

### REST API

The REST API is built with **Actix-web** and provides:

- Collection management (`/collections/*`)
- Point operations (`/collections/{name}/points/*`)
- Search and query endpoints
- Cluster management (`/cluster/*`)
- Snapshots and telemetry

Example endpoint structure:

| Endpoint                            | Method | Purpose           |
| ----------------------------------- | ------ | ----------------- |
| `/collections/{name}`               | PUT    | Create collection |
| `/collections/{name}/points`        | PUT    | Upsert points     |
| `/collections/{name}/points/search` | POST   | Search vectors    |
| `/collections/{name}/points/scroll` | POST   | Iterate points    |

**Sources:** [Cargo.toml78-80](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L78-L80) [docs/redoc/index.html1-103](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/index.html#L1-L103)

### gRPC API

The gRPC interface uses **Tonic** and provides:

- All REST API functionality with protocol buffer definitions
- Better performance for production workloads
- Streaming support for batch operations
- Protocol definitions in `lib/api/src/grpc/proto/*.proto`

The gRPC service runs on the same port as REST (6333) with automatic protocol detection.

**Sources:** [Cargo.toml81-84](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml#L81-L84) [lib/api/Cargo.toml17-47](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/Cargo.toml#L17-L47)

---

## Key Features Mapping to Code

```
```

**Diagram: Feature to Code Component Mapping**

**Sources:** Diagram 2 and Diagram 3 from high-level architecture

---

## Version and Compatibility

Current version: **1.15.5**

Qdrant maintains backward compatibility for at least one minor version, allowing rolling upgrades without downtime in distributed deployments. Storage formats are compatible between consecutive versions with automatic migration support.

**Sources:** [lib/common/common/src/defaults.rs9-13](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs#L9-L13) [docs/redoc/default\_version.js1-2](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/default_version.js#L1-L2)

---

## Next Steps

For deeper understanding of specific subsystems:

- **Architecture details**: See [System Architecture](qdrant/qdrant/2-system-architecture.md) for the complete layer breakdown
- **Vector indexing**: See [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md) for HNSW, quantization, and sparse vectors
- **Search processing**: See [Search and Query Processing](qdrant/qdrant/5-search-and-query-processing.md) for the complete query flow
- **Distributed features**: See [Distributed System Features](qdrant/qdrant/7-distributed-system-features.md) for Raft consensus and shard management
- **Configuration**: See [Configuration and Deployment](qdrant/qdrant/10-configuration-and-deployment.md) for setup and deployment options

**Sources:** Table of contents JSON structure

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Introduction to Qdrant](#introduction-to-qdrant.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [What is Qdrant?](#what-is-qdrant.md)
- [Core Concepts](#core-concepts.md)
- [Points](#points.md)
- [Vectors](#vectors.md)
- [Collections](#collections.md)
- [Segments](#segments.md)
- [System Architecture Overview](#system-architecture-overview.md)
- [Deployment Modes](#deployment-modes.md)
- [Standalone Mode](#standalone-mode.md)
- [Distributed Mode](#distributed-mode.md)
- [API Interfaces](#api-interfaces.md)
- [REST API](#rest-api.md)
- [gRPC API](#grpc-api.md)
- [Key Features Mapping to Code](#key-features-mapping-to-code.md)
- [Version and Compatibility](#version-and-compatibility.md)
- [Next Steps](#next-steps.md)
