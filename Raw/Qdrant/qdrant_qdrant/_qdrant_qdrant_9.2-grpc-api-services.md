gRPC API Services | qdrant/qdrant | DeepWiki

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

# gRPC API

Relevant source files

- [config/config.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml)
- [docs/grpc/docs.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/grpc/docs.md)
- [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json)
- [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)
- [lib/api/src/grpc/proto/collections.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto)
- [lib/api/src/grpc/proto/points.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto)
- [lib/api/src/grpc/qdrant.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs)
- [lib/collection/src/common/snapshots\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/common/snapshots_manager.rs)
- [lib/collection/src/config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs)
- [lib/collection/src/operations/config\_diff.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs)
- [lib/collection/src/operations/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs)
- [lib/collection/src/operations/shared\_storage\_config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs)
- [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs)
- [lib/collection/src/optimizers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/optimizers_builder.rs)
- [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)
- [lib/storage/src/content\_manager/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/collection_meta_ops.rs)
- [lib/storage/src/content\_manager/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs)
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

This document describes Qdrant's gRPC API implementation, which provides high-performance remote procedure call (RPC) interfaces for both external client communication and internal cluster coordination. The gRPC API serves as an alternative to the REST API for client operations and enables efficient peer-to-peer communication in distributed deployments.

For information about the REST API interface, see [REST API](qdrant/qdrant/7.1-raft-consensus-protocol.md). For details about distributed consensus mechanisms, see [Consensus Mechanism](qdrant/qdrant/6-data-updates-and-consistency.md).

## API Architecture Overview

Qdrant's gRPC implementation uses the Tonic framework and operates on two distinct communication channels with different purposes and security models.

```
```

Sources: [src/tonic/mod.rs147-360](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L360) [src/main.rs580-600](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L580-L600)

## Server Initialization and Configuration

The gRPC servers are initialized during application startup with separate configurations for external and internal communication.

### External gRPC Server Setup

The external gRPC server handles client requests and includes middleware for authentication, telemetry, and compression.

```
```

Sources: [src/tonic/mod.rs147-253](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L253) [src/tonic/mod.rs192-210](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L192-L210)

### Internal gRPC Server Setup

The internal server facilitates peer-to-peer communication within the cluster, including consensus operations and shard management.

```
```

Sources: [src/tonic/mod.rs256-360](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L256-L360) [src/tonic/mod.rs289-297](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L289-L297)

## Core gRPC Services

### Points Service

The `PointsService` handles vector and payload operations for external clients, implementing the complete points management interface.

| Method           | Purpose                      | Input Type           | Output Type               |
| ---------------- | ---------------------------- | -------------------- | ------------------------- |
| `upsert`         | Insert or update points      | `UpsertPoints`       | `PointsOperationResponse` |
| `delete`         | Delete points by selector    | `DeletePoints`       | `PointsOperationResponse` |
| `search`         | Vector similarity search     | `SearchPoints`       | `SearchResponse`          |
| `scroll`         | Paginated point retrieval    | `ScrollPoints`       | `ScrollResponse`          |
| `get`            | Retrieve specific points     | `GetPoints`          | `GetResponse`             |
| `count`          | Count points matching filter | `CountPoints`        | `CountResponse`           |
| `query`          | Universal query interface    | `QueryPoints`        | `QueryResponse`           |
| `update_vectors` | Update point vectors         | `UpdatePointVectors` | `PointsOperationResponse` |
| `set_payload`    | Set point payload fields     | `SetPayloadPoints`   | `PointsOperationResponse` |

Sources: [src/tonic/api/points\_api.rs61-681](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_api.rs#L61-L681) [src/tonic/api/points\_api.rs34-59](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_api.rs#L34-L59)

### Points Internal Service

The `PointsInternalService` provides the same operations optimized for peer-to-peer communication within the cluster.

```
```

Sources: [src/tonic/api/points\_internal\_api.rs42-55](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_internal_api.rs#L42-L55) [src/tonic/api/points\_internal\_api.rs332-385](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_internal_api.rs#L332-L385)

### Raft Service

The `RaftService` implements consensus communication between cluster peers using the Raft protocol.

| Method              | Purpose                          | Input Type              | Output Type |
| ------------------- | -------------------------------- | ----------------------- | ----------- |
| `send`              | Send Raft messages between peers | `RaftMessageBytes`      | `()`        |
| `who_is`            | Resolve peer ID to URI           | `PeerId`                | `UriStr`    |
| `add_peer_to_known` | Add new peer to cluster          | `AddPeerToKnownMessage` | `AllPeers`  |

```
```

Sources: [src/tonic/api/raft\_api.rs16-34](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L16-L34) [src/tonic/api/raft\_api.rs37-149](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L37-L149)

## Request Processing Architecture

### External Request Processing

External gRPC requests follow a standardized processing pipeline with authentication, validation, and telemetry collection.

```
```

Sources: [src/tonic/api/points\_api.rs63-85](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_api.rs#L63-L85) [src/tonic/api/update\_common.rs40-82](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/update_common.rs#L40-L82)

### Internal Request Processing

Internal requests bypass authentication but include shard targeting and clock synchronization for distributed consistency.

```
```

Sources: [src/tonic/api/points\_internal\_api.rs56-81](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_internal_api.rs#L56-L81) [src/common/update.rs54-70](https://github.com/qdrant/qdrant/blob/48203e41/src/common/update.rs#L54-L70)

## Protocol Buffer Integration

The gRPC API relies on Protocol Buffer definitions that specify message formats and service contracts.

### Key Protocol Definitions

| Service          | Proto File                      | Purpose                       |
| ---------------- | ------------------------------- | ----------------------------- |
| `Points`         | `points.proto`                  | Vector and payload operations |
| `PointsInternal` | `points_internal_service.proto` | Internal peer operations      |
| `Collections`    | `collections.proto`             | Collection management         |
| `Raft`           | `raft_service.proto`            | Consensus communication       |

### Internal Message Types

The internal API uses specialized message types optimized for cluster communication:

```
```

Sources: [lib/api/src/grpc/proto/points\_internal\_service.proto137-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points_internal_service.proto#L137-L143) [lib/api/src/grpc/proto/points\_internal\_service.proto40-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points_internal_service.proto#L40-L50)

## Authentication and Security

### TLS Configuration

Both external and internal gRPC servers support TLS encryption with separate configuration options.

```
```

Sources: [src/tonic/mod.rs180-190](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L180-L190) [src/tonic/mod.rs299-305](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L299-L305)

### Authentication Middleware

The external gRPC server includes optional API key authentication through the `AuthLayer` middleware.

Sources: [src/tonic/mod.rs198-209](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L198-L209) [src/tonic/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/auth.rs)

## Performance and Monitoring

### Hardware Usage Tracking

The gRPC API includes comprehensive hardware usage monitoring for performance analysis and resource accounting.

```
```

Sources: [src/tonic/api/points\_api.rs47-58](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_api.rs#L47-L58) [src/tonic/api/points\_internal\_api.rs436-447](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_internal_api.rs#L436-L447)

### Telemetry Collection

The gRPC server integrates with Qdrant's telemetry system to collect operational metrics and performance data.

Sources: [src/tonic/mod.rs195-197](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L195-L197) [src/tonic/tonic\_telemetry.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/tonic_telemetry.rs)

## Error Handling and Status Codes

The gRPC API uses Tonic's `Status` type to return standardized error responses with appropriate gRPC status codes.

### Common Error Patterns

| Error Type            | gRPC Status           | Usage                                       |
| --------------------- | --------------------- | ------------------------------------------- |
| `invalid_argument`    | `INVALID_ARGUMENT`    | Malformed requests, missing required fields |
| `internal`            | `INTERNAL`            | System errors, consensus failures           |
| `failed_precondition` | `FAILED_PRECONDITION` | State validation failures                   |
| `not_found`           | `NOT_FOUND`           | Missing collections or points               |

Sources: [src/tonic/api/raft\_api.rs42-43](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs#L42-L43) [src/tonic/api/points\_internal\_api.rs568-569](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_internal_api.rs#L568-L569)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [gRPC API](#grpc-api.md)
- [API Architecture Overview](#api-architecture-overview.md)
- [Server Initialization and Configuration](#server-initialization-and-configuration.md)
- [External gRPC Server Setup](#external-grpc-server-setup.md)
- [Internal gRPC Server Setup](#internal-grpc-server-setup.md)
- [Core gRPC Services](#core-grpc-services.md)
- [Points Service](#points-service.md)
- [Points Internal Service](#points-internal-service.md)
- [Raft Service](#raft-service.md)
- [Request Processing Architecture](#request-processing-architecture.md)
- [External Request Processing](#external-request-processing.md)
- [Internal Request Processing](#internal-request-processing.md)
- [Protocol Buffer Integration](#protocol-buffer-integration.md)
- [Key Protocol Definitions](#key-protocol-definitions.md)
- [Internal Message Types](#internal-message-types.md)
- [Authentication and Security](#authentication-and-security.md)
- [TLS Configuration](#tls-configuration.md)
- [Authentication Middleware](#authentication-middleware.md)
- [Performance and Monitoring](#performance-and-monitoring.md)
- [Hardware Usage Tracking](#hardware-usage-tracking.md)
- [Telemetry Collection](#telemetry-collection.md)
- [Error Handling and Status Codes](#error-handling-and-status-codes.md)
- [Common Error Patterns](#common-error-patterns.md)
