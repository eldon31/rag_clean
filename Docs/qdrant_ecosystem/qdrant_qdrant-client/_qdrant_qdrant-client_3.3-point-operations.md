Point Operations | qdrant/qdrant-client | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant-client](https://github.com/qdrant/qdrant-client "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 9 July 2025 ([ac6f6c](https://github.com/qdrant/qdrant-client/commits/ac6f6cd2))

- [Overview](qdrant/qdrant-client/1-overview.md)
- [Client Architecture](qdrant/qdrant-client/2-client-architecture.md)
- [Client Interface](qdrant/qdrant-client/2.1-client-interface.md)
- [Local Mode](qdrant/qdrant-client/2.2-local-mode.md)
- [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md)
- [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md)
- [Core Operations](qdrant/qdrant-client/3-core-operations.md)
- [Search Operations](qdrant/qdrant-client/3.1-search-operations.md)
- [Collection Management](qdrant/qdrant-client/3.2-collection-management.md)
- [Point Operations](qdrant/qdrant-client/3.3-point-operations.md)
- [Advanced Features](qdrant/qdrant-client/4-advanced-features.md)
- [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md)
- [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md)
- [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md)
- [Local Inference](qdrant/qdrant-client/4.4-local-inference.md)
- [Implementation Details](qdrant/qdrant-client/5-implementation-details.md)
- [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md)
- [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md)
- [Expression Evaluation](qdrant/qdrant-client/5.3-expression-evaluation.md)
- [Development & Testing](qdrant/qdrant-client/6-development-and-testing.md)
- [Project Setup](qdrant/qdrant-client/6.1-project-setup.md)
- [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md)
- [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md)

Menu

# Point Operations

Relevant source files

- [qdrant\_client/grpc/points\_pb2.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/points_pb2.py)
- [qdrant\_client/http/api/collections\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py)
- [qdrant\_client/http/api/points\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py)
- [qdrant\_client/http/api/service\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/service_api.py)
- [qdrant\_client/http/api/snapshots\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/snapshots_api.py)
- [qdrant\_client/proto/points.proto](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto)

This document covers the fundamental CRUD (Create, Read, Update, Delete) operations for points in the Qdrant client library. Point operations include inserting, retrieving, updating, and deleting vector points along with their associated payload data. These operations work across both local and remote Qdrant instances through HTTP and gRPC protocols.

For information about search and query operations on points, see [Search Operations](qdrant/qdrant-client/3.1-search-operations.md). For collection-level management, see [Collection Management](qdrant/qdrant-client/3.2-collection-management.md).

## Overview

Point operations in Qdrant are the core data manipulation functions that allow users to manage vector points and their associated metadata. Each point consists of:

- **Point ID**: A unique identifier (numeric or UUID)
- **Vector Data**: Dense, sparse, or multi-dense vectors
- **Payload**: Key-value metadata associated with the point

The system supports both individual and batch operations, with configurable consistency guarantees and write ordering options.

```
```

Sources: [qdrant\_client/http/api/points\_api.py51-521](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L51-L521) [qdrant\_client/grpc/points\_pb2.py1-50](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/points_pb2.py#L1-L50) [qdrant\_client/proto/points.proto1-50](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L1-L50)

## Core Point Operations

### Upsert Points

The `upsert_points` operation inserts new points or updates existing ones. If a point with the given ID already exists, it will be completely replaced.

**HTTP Implementation:**

- Method: `PUT /collections/{collection_name}/points`
- Function: `upsert_points(collection_name, point_insert_operations, wait, ordering)`

**gRPC Implementation:**

- Message: `UpsertPoints`
- Fields: `collection_name`, `points`, `wait`, `ordering`, `shard_key_selector`

```
```

Sources: [qdrant\_client/http/api/points\_api.py488-520](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L488-L520) [qdrant\_client/proto/points.proto132-138](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L132-L138)

### Delete Points

The `delete_points` operation removes points from the collection based on a points selector.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/delete`
- Function: `delete_points(collection_name, points_selector, wait, ordering)`

**gRPC Implementation:**

- Message: `DeletePoints`
- Fields: `collection_name`, `points`, `wait`, `ordering`, `shard_key_selector`

**Points Selection Methods:**

- By ID list: Specify exact point IDs to delete
- By filter: Delete points matching payload conditions
- By point selector: Combined ID and filter criteria

Sources: [qdrant\_client/http/api/points\_api.py188-220](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L188-L220) [qdrant\_client/proto/points.proto140-146](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L140-L146)

### Get Points

The `get_points` operations retrieve point data by ID. Two variants are available:

1. **Get Single Point**: `get_point(collection_name, id)`
2. **Get Multiple Points**: `get_points(collection_name, point_request)`

**HTTP Implementation:**

- Single: `GET /collections/{collection_name}/points/{id}`
- Multiple: `POST /collections/{collection_name}/points`

**gRPC Implementation:**

- Message: `GetPoints`
- Fields: `collection_name`, `ids`, `with_payload`, `with_vectors`, `read_consistency`

**Response Control:**

- `with_payload`: Control which payload fields to include/exclude
- `with_vectors`: Control which vector types to include
- `read_consistency`: Specify consistency guarantees

Sources: [qdrant\_client/http/api/points\_api.py290-350](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L290-L350) [qdrant\_client/proto/points.proto148-157](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L148-L157)

## Vector Operations

### Update Point Vectors

The `update_vectors` operation updates specific named vectors for points while keeping other vectors intact.

**HTTP Implementation:**

- Method: `PUT /collections/{collection_name}/points/vectors`
- Function: `update_vectors(collection_name, update_vectors, wait, ordering)`

**gRPC Implementation:**

- Message: `UpdatePointVectors`
- Fields: `collection_name`, `points`, `wait`, `ordering`, `shard_key_selector`

### Delete Point Vectors

The `delete_vectors` operation removes specific named vectors from points without deleting the points themselves.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/vectors/delete`
- Function: `delete_vectors(collection_name, delete_vectors, wait, ordering)`

**gRPC Implementation:**

- Message: `DeletePointVectors`
- Fields: `collection_name`, `points_selector`, `vectors`, `wait`, `ordering`

Sources: [qdrant\_client/http/api/points\_api.py454-486](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L454-L486) [qdrant\_client/proto/points.proto159-179](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L159-L179)

## Payload Operations

### Set Payload

The `set_payload` operation adds or updates payload fields for selected points.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/payload`
- Function: `set_payload(collection_name, set_payload, wait, ordering)`

**gRPC Implementation:**

- Message: `SetPayloadPoints`
- Fields: `collection_name`, `payload`, `points_selector`, `wait`, `ordering`

### Delete Payload

The `delete_payload` operation removes specific payload keys from selected points.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/payload/delete`
- Function: `delete_payload(collection_name, delete_payload, wait, ordering)`

**gRPC Implementation:**

- Message: `DeletePayloadPoints`
- Fields: `collection_name`, `keys`, `points_selector`, `wait`, `ordering`

### Clear Payload

The `clear_payload` operation removes all payload data from selected points.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/payload/clear`
- Function: `clear_payload(collection_name, points_selector, wait, ordering)`

**gRPC Implementation:**

- Message: `ClearPayloadPoints`
- Fields: `collection_name`, `points`, `wait`, `ordering`

```
```

Sources: [qdrant\_client/http/api/points\_api.py420-452](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L420-L452) [qdrant\_client/proto/points.proto181-208](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L181-L208)

## Batch Operations

### Batch Update

The `batch_update` operation allows multiple point operations to be executed in a single request for improved performance.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/batch`
- Function: `batch_update(collection_name, update_operations, wait, ordering)`

**gRPC Implementation:**

- Message: `UpdateBatchPoints`
- Fields: `collection_name`, `operations`, `wait`, `ordering`

**Supported Batch Operations:**

- `upsert`: Insert or update points
- `delete_points`: Delete points by selector
- `set_payload`: Set payload fields
- `overwrite_payload`: Replace entire payload
- `delete_payload`: Delete payload keys
- `clear_payload`: Clear all payload
- `update_vectors`: Update vector data
- `delete_vectors`: Delete specific vectors

```
```

Sources: [qdrant\_client/http/api/points\_api.py55-87](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L55-L87) [qdrant\_client/proto/points.proto848-865](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L848-L865)

## Point Retrieval Operations

### Scroll Points

The `scroll_points` operation provides paginated access to points in a collection with optional filtering.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/scroll`
- Function: `scroll_points(collection_name, scroll_request, consistency, timeout)`

**gRPC Implementation:**

- Message: `ScrollPoints`
- Fields: `collection_name`, `filter`, `offset`, `limit`, `with_payload`, `with_vectors`, `order_by`

**Pagination Control:**

- `offset`: Starting point ID for pagination
- `limit`: Maximum number of points to return
- `order_by`: Sort by payload field with direction

### Count Points

The `count_points` operation returns the number of points matching a filter condition.

**HTTP Implementation:**

- Method: `POST /collections/{collection_name}/points/count`
- Function: `count_points(collection_name, count_request, timeout)`

**gRPC Implementation:**

- Message: `CountPoints`
- Fields: `collection_name`, `filter`, `exact`, `read_consistency`

**Count Options:**

- `exact`: Whether to return exact count (slower) or approximate count (faster)
- `filter`: Optional filter condition to count only matching points

Sources: [qdrant\_client/http/api/points\_api.py386-418](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py#L386-L418) [qdrant\_client/proto/points.proto404-543](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L404-L543)

## Consistency and Ordering

### Write Ordering

Point operations support different write ordering guarantees:

| Ordering Type | Description                         | Performance | Consistency         |
| ------------- | ----------------------------------- | ----------- | ------------------- |
| `Weak`        | Operations may be reordered         | Fastest     | Eventual            |
| `Medium`      | Operations through dynamic leader   | Medium      | Short inconsistency |
| `Strong`      | Operations through permanent leader | Slowest     | Strong              |

### Read Consistency

Point retrieval operations support different read consistency levels:

| Consistency Type | Description                        | Latency      | Reliability   |
| ---------------- | ---------------------------------- | ------------ | ------------- |
| `All`            | Read from all nodes                | Highest      | Most reliable |
| `Majority`       | Read from majority of nodes        | Medium       | Balanced      |
| `Quorum`         | Read from half + 1 nodes           | Lowest       | Faster        |
| `factor`         | Read from specific number of nodes | Configurable | Configurable  |

Sources: [qdrant\_client/proto/points.proto11-32](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points.proto#L11-L32)

## Error Handling and Responses

All point operations return structured responses containing:

- **Result**: Operation-specific data (points, count, etc.)
- **Status**: Success/failure indication
- **Time**: Execution time in seconds
- **Usage**: Hardware resource usage statistics (optional)

**Common Response Types:**

- `UpdateResult`: For modification operations (upsert, delete, update)
- `RetrievedPoint[]`: For retrieval operations (get, scroll)
- `CountResult`: For count operations
- `BatchResult`: For batch operations

```
```

Sources: [qdrant\_client/grpc/points\_pb2.py1000-1100](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/points_pb2.py#L1000-L1100)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Point Operations](#point-operations.md)
- [Overview](#overview.md)
- [Core Point Operations](#core-point-operations.md)
- [Upsert Points](#upsert-points.md)
- [Delete Points](#delete-points.md)
- [Get Points](#get-points.md)
- [Vector Operations](#vector-operations.md)
- [Update Point Vectors](#update-point-vectors.md)
- [Delete Point Vectors](#delete-point-vectors.md)
- [Payload Operations](#payload-operations.md)
- [Set Payload](#set-payload.md)
- [Delete Payload](#delete-payload.md)
- [Clear Payload](#clear-payload.md)
- [Batch Operations](#batch-operations.md)
- [Batch Update](#batch-update.md)
- [Point Retrieval Operations](#point-retrieval-operations.md)
- [Scroll Points](#scroll-points.md)
- [Count Points](#count-points.md)
- [Consistency and Ordering](#consistency-and-ordering.md)
- [Write Ordering](#write-ordering.md)
- [Read Consistency](#read-consistency.md)
- [Error Handling and Responses](#error-handling-and-responses.md)
