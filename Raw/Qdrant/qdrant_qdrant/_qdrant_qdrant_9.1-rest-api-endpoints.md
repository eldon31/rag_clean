REST API Endpoints | qdrant/qdrant | DeepWiki

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

# REST API Endpoints

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

## Purpose and Scope

This document describes the REST API endpoints provided by Qdrant's HTTP server. The REST API is the primary interface for client applications to interact with Qdrant collections, points, and cluster operations. It provides JSON-based HTTP endpoints for all vector database operations including collection management, point CRUD operations, search, recommendations, and cluster administration.

For information about the gRPC API interface, see [gRPC API Services](qdrant/qdrant/9.2-grpc-api-services.md). For details on internal data type conversions between API formats, see [Data Types and Conversions](qdrant/qdrant/9.3-data-types-and-conversions.md).

## REST API Server Architecture

The REST API is implemented using the Actix-web framework and runs on the HTTP port specified in the service configuration (default: 6333). The server is initialized in [src/actix/mod.rs55-116](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L116) and configured with various middleware layers.

### Request Flow Architecture

```
```

**Diagram: REST API Request Processing Flow**

The request enters through the Actix-web server and passes through multiple middleware layers before being routed to the appropriate API module, which then interacts with the core storage layer.

Sources: [src/actix/mod.rs55-180](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L180) [src/actix/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/auth.rs) [src/actix/actix\_telemetry.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/actix_telemetry.rs)

### API Module to Route Mapping

```
```

**Diagram: API Modules to Route Mapping**

Each API module configures a specific set of related endpoints. The configuration functions are called during server initialization to register routes.

Sources: [src/actix/mod.rs99-158](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L99-L158) [src/actix/api/service\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/service_api.rs) [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs) [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)

## API Endpoint Categories

The REST API endpoints are organized into the following functional categories:

| Category        | Base Path                                     | Purpose                                      | Source Module                                                                                                        |
| --------------- | --------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Service**     | `/`                                           | Server information, health checks, telemetry | [src/actix/api/service\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/service_api.rs)         |
| **Collections** | `/collections`                                | Collection lifecycle management              | [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs) |
| **Points**      | `/collections/{name}/points`                  | Point CRUD operations                        | [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)           |
| **Search**      | `/collections/{name}/points/search`           | Vector similarity search                     | [src/actix/api/search\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/search_api.rs)           |
| **Recommend**   | `/collections/{name}/points/recommend`        | Recommendation queries                       | [src/actix/api/recommend\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/recommend_api.rs)     |
| **Query**       | `/collections/{name}/points/query`            | Universal query API                          | [src/actix/api/query\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/query_api.rs)             |
| **Discovery**   | `/collections/{name}/points/discover`         | Context-based discovery                      | [src/actix/api/discovery\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/discovery_api.rs)     |
| **Scroll**      | `/collections/{name}/points/scroll`           | Paginated point retrieval                    | [src/actix/api/retrieve\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/retrieve_api.rs)       |
| **Facet**       | `/collections/{name}/facet`                   | Faceted search                               | [lib/api/src/facet\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/facet_api.rs)                 |
| **Cluster**     | `/cluster`                                    | Distributed cluster management               | [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)         |
| **Snapshots**   | `/snapshots`, `/collections/{name}/snapshots` | Snapshot operations                          | [src/actix/api/snapshot\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/snapshot_api.rs)       |
| **Shards**      | `/collections/{name}/shards`                  | Shard key management                         | [src/actix/api/shards\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/shards_api.rs)           |

Sources: [docs/redoc/master/openapi.json2-194](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L2-L194)

## Common Request/Response Format

### Standard Response Envelope

All successful REST API responses follow a consistent envelope structure:

```
```

- `result`: The actual response data (varies by endpoint)
- `status`: Operation status, typically `"ok"` for success
- `time`: Time spent processing the request in seconds

Some responses may include an optional `usage` field when hardware reporting is enabled:

```
```

Sources: [docs/redoc/master/openapi.json60-95](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L60-L95) [lib/api/src/rest/models.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/rest/models.rs)

### Error Response Format

Error responses use the `ErrorResponse` schema:

```
```

HTTP status codes follow standard conventions:

- `200 OK`: Successful operation
- `4XX`: Client errors (invalid request, not found, etc.)
- `5XX`: Server errors

Sources: [docs/redoc/master/openapi.json42-48](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L42-L48)

### Common Query Parameters

Many endpoints support common query parameters:

| Parameter     | Type           | Description                                   | Used By                      |
| ------------- | -------------- | --------------------------------------------- | ---------------------------- |
| `timeout`     | integer        | Operation timeout in seconds                  | Collections, Points, Cluster |
| `wait`        | boolean        | Wait for operation to complete                | Collections, Points          |
| `ordering`    | string         | Write ordering guarantee (weak/medium/strong) | Points updates               |
| `shard_key`   | string/array   | Target specific shard(s)                      | Points operations            |
| `consistency` | integer/string | Read consistency level                        | Points queries               |

Sources: [docs/redoc/master/openapi.json30-37](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L30-L37) [lib/collection/src/operations/point\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/point_ops.rs)

## Service Endpoints

### Version Information

**GET /** - Returns Qdrant instance version information

```
GET /
```

Response:

```
```

Sources: [src/actix/mod.rs50-53](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L50-L53) [docs/redoc/master/openapi.json195-218](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L195-L218)

### Health Checks

Kubernetes-compatible health check endpoints:

| Endpoint       | Purpose              |
| -------------- | -------------------- |
| `GET /healthz` | General health check |
| `GET /livez`   | Liveness probe       |
| `GET /readyz`  | Readiness probe      |

All return `200 OK` with text response `"healthz check passed"` when healthy.

Sources: [docs/redoc/master/openapi.json492-569](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L492-L569) [src/actix/api/service\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/service_api.rs)

### Telemetry

**GET /telemetry** - Collect telemetry data about the instance

Query Parameters:

- `anonymize` (boolean): Anonymize sensitive information
- `details_level` (integer): Level of detail (0=minimal, higher=more detail)

Returns comprehensive telemetry including app info, system info, collections info, cluster info, and statistics.

Sources: [docs/redoc/master/openapi.json220-307](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L220-L307) [src/actix/api/service\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/service_api.rs)

### Metrics

**GET /metrics** - Prometheus-compatible metrics endpoint

Query Parameters:

- `anonymize` (boolean): Anonymize result

Returns metrics in Prometheus text format.

Sources: [docs/redoc/master/openapi.json309-344](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L309-L344) [src/actix/api/service\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/service_api.rs)

### Issues Reporting

**GET /issues** - Get performance issues and configuration suggestions

**DELETE /issues** - Clear all reported issues

Sources: [docs/redoc/master/openapi.json570-616](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L570-L616) [src/actix/api/issues\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/issues_api.rs)

## Collections Endpoints

### List Collections

**GET /collections** - Get list of all collections

Response includes collection names:

```
```

Sources: [docs/redoc/master/openapi.json849-915](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L849-L915)

### Get Collection Info

**GET /collections/{collection\_name}** - Get detailed collection information

Returns comprehensive collection metadata including:

- Configuration (vectors, HNSW, optimization settings)
- Status (green/yellow/grey/red)
- Statistics (point count, segment count, indexed vectors)
- Payload schema

Sources: [docs/redoc/master/openapi.json917-993](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L917-L993)

### Create Collection

**PUT /collections/{collection\_name}** - Create a new collection

Request body specifies collection configuration including vector parameters, HNSW settings, quantization, and optimization settings.

Query Parameters:

- `timeout` (integer): Operation timeout in seconds

Sources: [docs/redoc/master/openapi.json995-1088](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L995-L1088) [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs)

### Update Collection

**PATCH /collections/{collection\_name}** - Update collection parameters

Supports partial updates of:

- Optimizers configuration
- HNSW configuration
- Vector parameters
- Quantization settings

Sources: [docs/redoc/master/openapi.json1090-1183](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L1090-L1183)

### Delete Collection

**DELETE /collections/{collection\_name}** - Delete a collection and all data

Query Parameters:

- `timeout` (integer): Operation timeout in seconds

Sources: [docs/redoc/master/openapi.json1185-1272](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L1185-L1272)

### Collection Aliases

Collections support aliasing for flexible naming:

| Endpoint               | Method | Purpose                           |
| ---------------------- | ------ | --------------------------------- |
| `/collections/aliases` | POST   | Create, rename, or delete aliases |

Sources: [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json) [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs)

## Points Endpoints

### Upsert Points

**PUT /collections/{collection\_name}/points** - Insert or update points

Request body contains points with ID, vector(s), and optional payload:

```
```

Query Parameters:

- `wait` (boolean): Wait for operation to complete
- `ordering` (string): Write ordering guarantee

Sources: [lib/collection/src/operations/point\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/point_ops.rs) [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)

### Get Points

**POST /collections/{collection\_name}/points** - Retrieve points by IDs

Request:

```
```

Sources: [src/actix/api/retrieve\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/retrieve_api.rs)

### Scroll Points

**POST /collections/{collection\_name}/points/scroll** - Paginated point retrieval

Supports:

- Filtering by payload conditions
- Ordering by payload fields
- Cursor-based pagination

Sources: [src/actix/api/retrieve\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/retrieve_api.rs) [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json)

### Delete Points

**POST /collections/{collection\_name}/points/delete** - Delete points

Can delete by:

- Point IDs list
- Filter conditions

Sources: [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)

### Update Vectors

**PUT /collections/{collection\_name}/points/vectors** - Update only vectors

**DELETE /collections/{collection\_name}/points/vectors** - Delete specific named vectors

Sources: [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)

### Set/Delete/Clear Payload

| Endpoint                                    | Method | Purpose               |
| ------------------------------------------- | ------ | --------------------- |
| `/collections/{name}/points/payload`        | POST   | Set payload fields    |
| `/collections/{name}/points/payload`        | PUT    | Overwrite payload     |
| `/collections/{name}/points/payload/delete` | POST   | Delete payload fields |
| `/collections/{name}/points/payload/clear`  | POST   | Clear all payload     |

Sources: [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)

### Batch Operations

**POST /collections/{collection\_name}/points/batch** - Execute multiple operations in a batch

Supports batching of upsert, delete, and payload operations for efficiency.

Sources: [src/actix/api/update\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/update_api.rs)

## Search Endpoints

### Vector Search

**POST /collections/{collection\_name}/points/search** - Vector similarity search

Request:

```
```

Search parameters:

- `hnsw_ef`: Size of beam in HNSW search (accuracy vs speed)
- `exact`: Force exact search (no approximation)
- `quantization`: Quantization search parameters
- `indexed_only`: Search only indexed segments

Sources: [src/actix/api/search\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/search_api.rs) [lib/segment/src/types.rs471-546](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/types.rs#L471-L546)

### Batch Search

**POST /collections/{collection\_name}/points/search/batch** - Execute multiple searches

Returns results for all searches in a single request.

Sources: [src/actix/api/search\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/search_api.rs)

### Search Groups

**POST /collections/{collection\_name}/points/search/groups** - Group search results

Supports grouping results by payload field values.

Sources: [src/actix/api/search\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/search_api.rs)

### Search Matrix

Matrix search endpoints for computing pairwise similarities:

| Endpoint                                                | Purpose               |
| ------------------------------------------------------- | --------------------- |
| `POST /collections/{name}/points/search/matrix/pairs`   | Find similar pairs    |
| `POST /collections/{name}/points/search/matrix/offsets` | Compute offset matrix |

Sources: [src/actix/api/search\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/search_api.rs)

## Recommendation Endpoints

### Recommend Points

**POST /collections/{collection\_name}/points/recommend** - Get recommendations

Request:

```
```

Recommendation strategies:

- `average_vector`: Average positive examples, subtract negatives
- `best_score`: Use best scoring positive example

Sources: [src/actix/api/recommend\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/recommend_api.rs) [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs)

### Recommend Batch

**POST /collections/{collection\_name}/points/recommend/batch** - Batch recommendations

Sources: [src/actix/api/recommend\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/recommend_api.rs)

### Recommend Groups

**POST /collections/{collection\_name}/points/recommend/groups** - Group recommendations

Sources: [src/actix/api/recommend\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/recommend_api.rs)

## Query API

### Universal Query

**POST /collections/{collection\_name}/points/query** - Universal query interface

Unified endpoint supporting:

- Nearest neighbor search
- Recommendations
- Discovery (context-based search)
- Fusion (combining multiple queries)
- Prefetch (multi-stage queries)

Request example:

```
```

Query types:

- `nearest`: Vector similarity
- `recommend`: Recommendation query
- `discover`: Context discovery
- `context`: Context pairs
- `fusion`: RRF/DBF fusion
- `order_by`: Order by payload field

Sources: [src/actix/api/query\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/query_api.rs) [lib/collection/src/operations/universal\_query/](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/universal_query/)

### Query Batch

**POST /collections/{collection\_name}/points/query/batch** - Batch universal queries

Sources: [src/actix/api/query\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/query_api.rs)

### Query Groups

**POST /collections/{collection\_name}/points/query/groups** - Universal query with grouping

Sources: [src/actix/api/query\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/query_api.rs)

## Discovery Endpoints

### Discover Points

**POST /collections/{collection\_name}/points/discover** - Context-based discovery

Request:

```
```

Finds points similar to target while considering context pairs.

Sources: [src/actix/api/discovery\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/discovery_api.rs) [lib/collection/src/operations/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/types.rs)

### Discover Batch

**POST /collections/{collection\_name}/points/discover/batch** - Batch discovery

Sources: [src/actix/api/discovery\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/discovery_api.rs)

## Facet Endpoints

### Facet Search

**POST /collections/{collection\_name}/facet** - Get faceted search results

Returns aggregated counts/values for specified payload fields.

Sources: [lib/api/src/facet\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/src/facet_api.rs)

## Count Endpoint

### Count Points

**POST /collections/{collection\_name}/points/count** - Count points matching filter

Request:

```
```

Returns point count, optionally with exact counting.

Sources: [src/actix/api/count\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/count_api.rs)

## Cluster Management Endpoints

### Cluster Status

**GET /cluster** - Get cluster status and composition

Returns information about:

- Peer IDs and states
- Raft consensus status
- Cluster membership

Sources: [docs/redoc/master/openapi.json618-683](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L618-L683) [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)

### Recover Cluster

**POST /cluster/recover** - Attempt to recover current peer Raft state

Used for disaster recovery scenarios.

Sources: [docs/redoc/master/openapi.json686-751](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L686-L751) [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)

### Remove Peer

**DELETE /cluster/peer/{peer\_id}** - Remove peer from cluster

Query Parameters:

- `force` (boolean): Force removal even if peer has shards
- `timeout` (integer): Operation timeout

Sources: [docs/redoc/master/openapi.json753-847](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L753-L847) [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)

### Collection Cluster Info

**GET /collections/{collection\_name}/cluster** - Get collection's cluster distribution

Returns:

- Shard distribution across peers
- Replica states
- Active shard transfers
- Resharding operations (if enabled)

Sources: [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)

### Cluster Setup Operations

**POST /collections/{collection\_name}/cluster** - Update collection cluster setup

Supports operations:

- Move shard between peers
- Replicate shard to peer
- Abort shard transfer
- Drop replica
- Restart transfer

Sources: [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs) [lib/collection/src/operations/cluster\_ops.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/cluster_ops.rs)

## Shard Key Endpoints

### Create Shard Key

**PUT /collections/{collection\_name}/shards** - Create custom shard key

Used for custom sharding strategies.

Sources: [docs/redoc/master/openapi.json3-97](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L3-L97) [src/actix/api/shards\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/shards_api.rs)

### Delete Shard Key

**POST /collections/{collection\_name}/shards/delete** - Delete shard key

Sources: [docs/redoc/master/openapi.json99-193](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L99-L193) [src/actix/api/shards\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/shards_api.rs)

## Snapshot Endpoints

### Collection Snapshots

| Endpoint                                          | Method | Purpose                          |
| ------------------------------------------------- | ------ | -------------------------------- |
| `GET /collections/{name}/snapshots`               | GET    | List collection snapshots        |
| `POST /collections/{name}/snapshots`              | POST   | Create collection snapshot       |
| `DELETE /collections/{name}/snapshots/{snapshot}` | DELETE | Delete collection snapshot       |
| `GET /collections/{name}/snapshots/{snapshot}`    | GET    | Download snapshot                |
| `PUT /collections/{name}/snapshots/upload`        | PUT    | Upload and recover from snapshot |
| `POST /collections/{name}/snapshots/recover`      | POST   | Recover from uploaded snapshot   |

Sources: [src/actix/api/snapshot\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/snapshot_api.rs)

### Full Storage Snapshots

| Endpoint                       | Method | Purpose                      |
| ------------------------------ | ------ | ---------------------------- |
| `GET /snapshots`               | GET    | List full storage snapshots  |
| `POST /snapshots`              | POST   | Create full storage snapshot |
| `DELETE /snapshots/{snapshot}` | DELETE | Delete storage snapshot      |
| `GET /snapshots/{snapshot}`    | GET    | Download snapshot            |

Sources: [src/actix/api/snapshot\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/snapshot_api.rs)

### Shard Snapshots

Collection shard-level snapshot operations for distributed recovery:

| Endpoint                                                            | Method | Purpose                     |
| ------------------------------------------------------------------- | ------ | --------------------------- |
| `POST /collections/{name}/shards/{shard_id}/snapshots`              | POST   | Create shard snapshot       |
| `GET /collections/{name}/shards/{shard_id}/snapshots`               | GET    | List shard snapshots        |
| `DELETE /collections/{name}/shards/{shard_id}/snapshots/{snapshot}` | DELETE | Delete shard snapshot       |
| `GET /collections/{name}/shards/{shard_id}/snapshots/{snapshot}`    | GET    | Download shard snapshot     |
| `PUT /collections/{name}/shards/{shard_id}/snapshots/upload`        | PUT    | Upload shard snapshot       |
| `POST /collections/{name}/shards/{shard_id}/snapshots/recover`      | POST   | Recover shard from snapshot |

Sources: [src/actix/api/snapshot\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/snapshot_api.rs)

## Payload Index Endpoints

### Create Field Index

**PUT /collections/{collection\_name}/index** - Create payload field index

Request:

```
```

Supported index types:

- `keyword`: Exact match indexing
- `integer`: Integer range indexing
- `float`: Float range indexing
- `geo`: Geospatial indexing
- `text`: Full-text search indexing
- `bool`: Boolean indexing
- `datetime`: Datetime range indexing
- `uuid`: UUID indexing

Sources: [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs) [segment/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/segment/src/types.rs)

### Delete Field Index

**DELETE /collections/{collection\_name}/index/{field\_name}** - Delete payload field index

Sources: [src/actix/api/collections\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/collections_api.rs)

## Authentication

The REST API supports multiple authentication methods:

### API Key Authentication

Provide API key in request header:

```
api-key: your-api-key-here
```

Two types of API keys:

- Full access key (read + write)
- Read-only key (read operations only)

Configured via `service.api_key` and `service.read_only_api_key` settings.

Sources: [src/actix/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/auth.rs) [src/settings.rs36-37](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L36-L37)

### JWT RBAC Authentication

When JWT RBAC is enabled (`service.jwt_rbac: true`), authentication uses JWT tokens in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

JWT tokens encode access permissions for fine-grained access control.

Sources: [src/actix/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/auth.rs) [src/common/auth.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/auth.rs)

### Whitelisted Endpoints

Some endpoints are accessible without authentication:

- `GET /`
- `GET /healthz`
- `GET /livez`
- `GET /readyz`
- Web UI paths (if enabled)

Sources: [src/actix/mod.rs89-97](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L89-L97)

## OpenAPI Specification

The complete OpenAPI specification is available at the `/openapi` endpoint and is also stored in [docs/redoc/master/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json) This specification can be used to:

- Generate client libraries in various languages
- Browse the API documentation interactively (via Swagger UI/Redoc)
- Validate requests and responses
- Generate mock servers for testing

The OpenAPI spec is automatically generated from the code annotations and schemas defined in the API implementation modules.

Sources: [docs/redoc/master/openapi.json1-519829](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/master/openapi.json#L1-L519829) [src/actix/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [REST API Endpoints](#rest-api-endpoints.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [REST API Server Architecture](#rest-api-server-architecture.md)
- [Request Flow Architecture](#request-flow-architecture.md)
- [API Module to Route Mapping](#api-module-to-route-mapping.md)
- [API Endpoint Categories](#api-endpoint-categories.md)
- [Common Request/Response Format](#common-requestresponse-format.md)
- [Standard Response Envelope](#standard-response-envelope.md)
- [Error Response Format](#error-response-format.md)
- [Common Query Parameters](#common-query-parameters.md)
- [Service Endpoints](#service-endpoints.md)
- [Version Information](#version-information.md)
- [Health Checks](#health-checks.md)
- [Telemetry](#telemetry.md)
- [Metrics](#metrics.md)
- [Issues Reporting](#issues-reporting.md)
- [Collections Endpoints](#collections-endpoints.md)
- [List Collections](#list-collections.md)
- [Get Collection Info](#get-collection-info.md)
- [Create Collection](#create-collection.md)
- [Update Collection](#update-collection.md)
- [Delete Collection](#delete-collection.md)
- [Collection Aliases](#collection-aliases.md)
- [Points Endpoints](#points-endpoints.md)
- [Upsert Points](#upsert-points.md)
- [Get Points](#get-points.md)
- [Scroll Points](#scroll-points.md)
- [Delete Points](#delete-points.md)
- [Update Vectors](#update-vectors.md)
- [Set/Delete/Clear Payload](#setdeleteclear-payload.md)
- [Batch Operations](#batch-operations.md)
- [Search Endpoints](#search-endpoints.md)
- [Vector Search](#vector-search.md)
- [Batch Search](#batch-search.md)
- [Search Groups](#search-groups.md)
- [Search Matrix](#search-matrix.md)
- [Recommendation Endpoints](#recommendation-endpoints.md)
- [Recommend Points](#recommend-points.md)
- [Recommend Batch](#recommend-batch.md)
- [Recommend Groups](#recommend-groups.md)
- [Query API](#query-api.md)
- [Universal Query](#universal-query.md)
- [Query Batch](#query-batch.md)
- [Query Groups](#query-groups.md)
- [Discovery Endpoints](#discovery-endpoints.md)
- [Discover Points](#discover-points.md)
- [Discover Batch](#discover-batch.md)
- [Facet Endpoints](#facet-endpoints.md)
- [Facet Search](#facet-search.md)
- [Count Endpoint](#count-endpoint.md)
- [Count Points](#count-points.md)
- [Cluster Management Endpoints](#cluster-management-endpoints.md)
- [Cluster Status](#cluster-status.md)
- [Recover Cluster](#recover-cluster.md)
- [Remove Peer](#remove-peer.md)
- [Collection Cluster Info](#collection-cluster-info.md)
- [Cluster Setup Operations](#cluster-setup-operations.md)
- [Shard Key Endpoints](#shard-key-endpoints.md)
- [Create Shard Key](#create-shard-key.md)
- [Delete Shard Key](#delete-shard-key.md)
- [Snapshot Endpoints](#snapshot-endpoints.md)
- [Collection Snapshots](#collection-snapshots.md)
- [Full Storage Snapshots](#full-storage-snapshots.md)
- [Shard Snapshots](#shard-snapshots.md)
- [Payload Index Endpoints](#payload-index-endpoints.md)
- [Create Field Index](#create-field-index.md)
- [Delete Field Index](#delete-field-index.md)
- [Authentication](#authentication.md)
- [API Key Authentication](#api-key-authentication.md)
- [JWT RBAC Authentication](#jwt-rbac-authentication.md)
- [Whitelisted Endpoints](#whitelisted-endpoints.md)
- [OpenAPI Specification](#openapi-specification.md)
