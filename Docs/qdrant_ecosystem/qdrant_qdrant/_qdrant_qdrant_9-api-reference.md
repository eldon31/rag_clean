API Reference | qdrant/qdrant | DeepWiki

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

# API Reference

Relevant source files

- [Cargo.lock](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.lock)
- [Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml)
- [docs/grpc/docs.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/grpc/docs.md)
- [docs/redoc/default\_version.js](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/default_version.js)
- [docs/redoc/index.html](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/index.html)
- [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json)
- [docs/redoc/v0.10.3/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.3/openapi.json)
- [docs/redoc/v0.10.4/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.4/openapi.json)
- [docs/redoc/v0.10.5/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.5/openapi.json)
- [docs/redoc/v1.10.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.10.x/openapi.json)
- [docs/redoc/v1.11.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.11.x/openapi.json)
- [docs/redoc/v1.13.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.13.x/openapi.json)
- [docs/redoc/v1.15.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.15.x/openapi.json)
- [lib/api/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/Cargo.toml)
- [lib/api/src/grpc/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/conversions.rs)
- [lib/api/src/grpc/proto/collections.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections.proto)
- [lib/api/src/grpc/proto/points.proto](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto)
- [lib/api/src/grpc/qdrant.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs)
- [lib/collection/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml)
- [lib/collection/src/config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/config.rs)
- [lib/collection/src/operations/config\_diff.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/config_diff.rs)
- [lib/collection/src/operations/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/conversions.rs)
- [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs)
- [lib/collection/src/optimizers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/optimizers_builder.rs)
- [lib/common/common/src/defaults.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs)
- [lib/common/dataset/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/dataset/Cargo.toml)
- [lib/common/issues/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/issues/Cargo.toml)
- [lib/segment/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml)
- [lib/segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs)
- [lib/sparse/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/Cargo.toml)
- [lib/storage/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml)
- [lib/storage/src/content\_manager/collection\_meta\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/collection_meta_ops.rs)
- [lib/storage/src/content\_manager/conversions.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs)
- [tools/missed\_cherry\_picks.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/missed_cherry_picks.sh)

This document provides a comprehensive overview of Qdrant's API interfaces, covering both REST and gRPC protocols. It describes the architectural structure, service organization, and common patterns used across all API endpoints. For detailed endpoint documentation, see [REST API](qdrant/qdrant/7.1-raft-consensus-protocol.md) for HTTP interface specifics and [gRPC API](qdrant/qdrant/7.2-shard-transfers-and-resharding.md) for gRPC service details.

## API Architecture Overview

Qdrant exposes multiple API interfaces to support different client needs and deployment scenarios. The system provides both external-facing APIs for client applications and internal APIs for distributed cluster communication.

```
```

Sources: [docs/redoc/master/openapi.json1-50](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L1-L50) [lib/api/src/grpc/proto/points.proto1-30](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points.proto#L1-L30) [lib/api/src/grpc/proto/qdrant\_internal\_service.proto1-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/qdrant_internal_service.proto#L1-L20) [src/tonic/api/points\_api.rs34-45](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_api.rs#L34-L45)

## Service Organization

The API is organized into distinct services, each handling specific aspects of vector database operations. Each service is implemented in both REST and gRPC protocols with consistent functionality.

```
```

Sources: [lib/api/src/grpc/proto/collections\_service.proto1-30](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/collections_service.proto#L1-L30) [lib/api/src/grpc/proto/points\_service.proto1-30](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points_service.proto#L1-L30) [lib/api/src/grpc/proto/snapshots\_service.proto1-30](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/snapshots_service.proto#L1-L30) [docs/grpc/docs.md116-125](https://github.com/qdrant/qdrant/blob/48203e41/docs/grpc/docs.md#L116-L125)

## Request Processing Flow

All API requests follow a consistent processing pattern through the system's layered architecture, with different paths for read and write operations.

```
```

Sources: [src/tonic/api/points\_api.rs61-85](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_api.rs#L61-L85) [src/actix/api/update\_api.rs31-65](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs#L31-L65) [storage/dispatcher.rs](https://github.com/qdrant/qdrant/blob/48203e41/storage/dispatcher.rs) [src/common/strict\_mode.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/strict_mode.rs) [storage/content\_manager/toc/](https://github.com/qdrant/qdrant/blob/48203e41/storage/content_manager/toc/)

## API Response Structure

All API responses follow a consistent structure with metadata about request processing, hardware usage, and timing information.

### Standard Response Format

| Field    | Type   | Description                           |
| -------- | ------ | ------------------------------------- |
| `result` | Object | The actual response data              |
| `status` | String | Operation status ("ok" or error)      |
| `time`   | Number | Processing time in seconds            |
| `usage`  | Object | Optional hardware and inference usage |

### Hardware Usage Reporting

The system tracks detailed hardware usage for operations when enabled:

```
```

Sources: [lib/api/src/grpc/qdrant.rs180-290](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L180-L290) [lib/api/src/grpc/ops.rs5-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/ops.rs#L5-L50) [docs/redoc/master/openapi.json276-307](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L276-L307)

## Authentication and Authorization

The API supports multiple authentication mechanisms and role-based access control for securing operations.

### Access Control Implementation

| Component        | Purpose                           | Location                                                                              |
| ---------------- | --------------------------------- | ------------------------------------------------------------------------------------- |
| `ActixAccess`    | REST API authentication extractor | [src/actix/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/auth.rs) |
| `rbac::Access`   | Role-based access control         | [storage/rbac/](https://github.com/qdrant/qdrant/blob/48203e41/storage/rbac/)         |
| `extract_access` | gRPC authentication extractor     | [src/tonic/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/auth.rs) |

### API Key Authentication

The system supports API key-based authentication through HTTP headers:

- **Header**: `api-key`
- **Validation**: Keys are validated against configured access rules
- **Scope**: Different keys can have different permissions (read-only, read-write, admin)

Sources: [src/actix/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/auth.rs) [src/tonic/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/auth.rs) [storage/rbac/](https://github.com/qdrant/qdrant/blob/48203e41/storage/rbac/)

## Error Handling

The API provides consistent error handling across both REST and gRPC interfaces with detailed error information.

### Error Response Structure

```
```

### Status Code Mapping

| Internal Error      | REST HTTP Code            | gRPC Code           |
| ------------------- | ------------------------- | ------------------- |
| `BadInput`          | 400 Bad Request           | `InvalidArgument`   |
| `NotFound`          | 404 Not Found             | `NotFound`          |
| `ServiceError`      | 500 Internal Server Error | `Internal`          |
| `Timeout`           | 408 Request Timeout       | `DeadlineExceeded`  |
| `RateLimitExceeded` | 429 Too Many Requests     | `ResourceExhausted` |
| `Forbidden`         | 403 Forbidden             | `PermissionDenied`  |

Sources: [lib/storage/src/content\_manager/conversions.rs21-61](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/conversions.rs#L21-L61) [docs/redoc/master/openapi.json40-60](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L40-L60)

## Request Validation

All API requests undergo validation using the `validator` crate with custom validation rules specific to vector database operations.

### Validation Patterns

| Field Type        | Validation Rules               | Example                                    |
| ----------------- | ------------------------------ | ------------------------------------------ |
| Collection Names  | Length 1-255, valid characters | `validate_collection_name_legacy`          |
| Vector Dimensions | Range 1-65536                  | `#[validate(range(min = 1, max = 65536))]` |
| Search Limits     | Minimum 1                      | `#[validate(range(min = 1))]`              |
| HNSW Parameters   | `ef_construct >= 4`            | `#[validate(range(min = 4))]`              |
| Quantization      | `quantile` 0.5-1.0             | `#[validate(range(min = 0.5, max = 1.0))]` |

### Validation Implementation

The validation occurs at multiple levels:

1. **Protocol Level**: Protobuf/JSON schema validation
2. **Field Level**: Individual field constraints using `#[validate()]` annotations
3. **Business Logic**: Custom validation functions for complex rules
4. **Strict Mode**: Additional constraints when strict mode is enabled

Sources: [lib/api/src/grpc/qdrant.rs2-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/qdrant.rs#L2-L50) [lib/segment/src/types.rs448-503](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L448-L503) [common/validation.rs](https://github.com/qdrant/qdrant/blob/48203e41/common/validation.rs) [src/common/strict\_mode.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/strict_mode.rs)

## Internal vs External APIs

The system distinguishes between external client-facing APIs and internal peer-to-peer communication APIs for distributed operations.

### External APIs

- **Purpose**: Client application integration
- **Authentication**: API key or token-based
- **Rate Limiting**: Configurable per-client limits
- **Protocols**: REST HTTP/JSON and gRPC

### Internal APIs

- **Purpose**: Cluster node communication
- **Authentication**: Full access assumed (`FULL_ACCESS`)
- **Services**: `PointsInternal`, `QdrantInternal`
- **Usage**: Shard operations, consensus, replication

| Service       | Port    | Purpose            | Access Level  |
| ------------- | ------- | ------------------ | ------------- |
| REST API      | 6333    | Client operations  | Authenticated |
| gRPC API      | 6334    | Client operations  | Authenticated |
| Internal gRPC | Various | Peer communication | Internal      |
| Health Checks | Same    | Kubernetes probes  | Public        |

Sources: [src/tonic/api/points\_internal\_api.rs40-55](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/points_internal_api.rs#L40-L55) [lib/api/src/grpc/proto/points\_internal\_service.proto1-30](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/points_internal_service.proto#L1-L30) [lib/api/src/grpc/proto/qdrant\_internal\_service.proto1-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/grpc/proto/qdrant_internal_service.proto#L1-L20)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [API Reference](#api-reference.md)
- [API Architecture Overview](#api-architecture-overview.md)
- [Service Organization](#service-organization.md)
- [Request Processing Flow](#request-processing-flow.md)
- [API Response Structure](#api-response-structure.md)
- [Standard Response Format](#standard-response-format.md)
- [Hardware Usage Reporting](#hardware-usage-reporting.md)
- [Authentication and Authorization](#authentication-and-authorization.md)
- [Access Control Implementation](#access-control-implementation.md)
- [API Key Authentication](#api-key-authentication.md)
- [Error Handling](#error-handling.md)
- [Error Response Structure](#error-response-structure.md)
- [Status Code Mapping](#status-code-mapping.md)
- [Request Validation](#request-validation.md)
- [Validation Patterns](#validation-patterns.md)
- [Validation Implementation](#validation-implementation.md)
- [Internal vs External APIs](#internal-vs-external-apis.md)
- [External APIs](#external-apis.md)
- [Internal APIs](#internal-apis.md)
