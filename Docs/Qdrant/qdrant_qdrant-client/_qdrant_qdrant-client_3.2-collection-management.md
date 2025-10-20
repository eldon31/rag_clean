Collection Management | qdrant/qdrant-client | DeepWiki

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

# Collection Management

Relevant source files

- [qdrant\_client/grpc/collections\_pb2.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/collections_pb2.py)
- [qdrant\_client/grpc/points\_service\_pb2.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/points_service_pb2.py)
- [qdrant\_client/grpc/points\_service\_pb2\_grpc.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/points_service_pb2_grpc.py)
- [qdrant\_client/http/api/collections\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py)
- [qdrant\_client/http/api/points\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/points_api.py)
- [qdrant\_client/http/api/service\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/service_api.py)
- [qdrant\_client/http/api/snapshots\_api.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/snapshots_api.py)
- [qdrant\_client/proto/collections.proto](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto)
- [qdrant\_client/proto/points\_service.proto](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/points_service.proto)

Collection Management encompasses the creation, configuration, modification, and deletion of vector collections in Qdrant. This system provides a unified interface for managing collections across both local and remote Qdrant instances using HTTP REST and gRPC protocols. For information about point operations within collections, see [Point Operations](qdrant/qdrant-client/3.3-point-operations.md). For search operations across collections, see [Search Operations](qdrant/qdrant-client/3.1-search-operations.md).

## Collection Lifecycle Operations

The collection management system provides five core operations that form the complete lifecycle of a Qdrant collection:

```
```

**Sources:** [qdrant\_client/http/api/collections\_api.py51-346](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py#L51-L346) [qdrant\_client/proto/collections.proto366-401](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L366-L401)

### Core Collection Operations

| Operation           | HTTP Method                      | gRPC Message               | Purpose                                            |
| ------------------- | -------------------------------- | -------------------------- | -------------------------------------------------- |
| `create_collection` | PUT `/collections/{name}`        | `CreateCollection`         | Create new collection with specified configuration |
| `collection_exists` | GET `/collections/{name}/exists` | `CollectionExistsRequest`  | Check if collection exists                         |
| `get_collection`    | GET `/collections/{name}`        | `GetCollectionInfoRequest` | Retrieve detailed collection information           |
| `get_collections`   | GET `/collections`               | `ListCollectionsRequest`   | List all existing collections                      |
| `update_collection` | PATCH `/collections/{name}`      | `UpdateCollection`         | Modify collection parameters                       |
| `delete_collection` | DELETE `/collections/{name}`     | `DeleteCollection`         | Remove collection and all data                     |

**Sources:** [qdrant\_client/http/api/collections\_api.py75-195](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py#L75-L195) [qdrant\_client/proto/collections.proto73-401](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L73-L401)

## Collection Configuration Structure

Collections in Qdrant are configured through a hierarchical structure that defines vector storage, indexing, optimization, and operational parameters:

```
```

**Sources:** [qdrant\_client/proto/collections.proto428-435](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L428-L435) [qdrant\_client/proto/collections.proto36-70](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L36-L70) [qdrant\_client/proto/collections.proto488-498](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L488-L498)

### Vector Configuration Types

The `VectorsConfig` message supports two distinct configuration modes for vector storage:

```
```

**Sources:** [qdrant\_client/proto/collections.proto12-20](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L12-L20) [qdrant\_client/proto/collections.proto36-41](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L36-L41) [qdrant\_client/proto/collections.proto28-30](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L28-L30)

## Protocol Implementation Architecture

The collection management system implements a dual-protocol architecture supporting both HTTP REST and gRPC communication:

```
```

**Sources:** [qdrant\_client/http/api/collections\_api.py51-52](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py#L51-L52) [qdrant\_client/grpc/collections\_pb2.py1-189](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/grpc/collections_pb2.py#L1-L189) [qdrant\_client/proto/collections.proto1-724](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L1-L724)

### HTTP API Implementation

The HTTP collections API provides both synchronous and asynchronous implementations with consistent method signatures:

```
```

**Sources:** [qdrant\_client/http/api/collections\_api.py51-53](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py#L51-L53) [qdrant\_client/http/api/collections\_api.py75-104](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py#L75-L104) [qdrant\_client/http/api/collections\_api.py18-44](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api/collections_api.py#L18-L44)

### Collection Creation Parameters

The `CreateCollection` message defines the comprehensive set of parameters available when creating a new collection:

| Parameter                  | Type                   | Purpose                                   |
| -------------------------- | ---------------------- | ----------------------------------------- |
| `collection_name`          | `string`               | Unique identifier for the collection      |
| `vectors_config`           | `VectorsConfig`        | Vector storage and indexing configuration |
| `hnsw_config`              | `HnswConfigDiff`       | HNSW index parameters                     |
| `optimizers_config`        | `OptimizersConfigDiff` | Background optimization settings          |
| `wal_config`               | `WalConfigDiff`        | Write-ahead log configuration             |
| `shard_number`             | `uint32`               | Number of shards for distribution         |
| `replication_factor`       | `uint32`               | Number of replicas per shard              |
| `write_consistency_factor` | `uint32`               | Write consistency requirements            |
| `on_disk_payload`          | `bool`                 | Store payload on disk vs memory           |
| `quantization_config`      | `QuantizationConfig`   | Vector quantization settings              |
| `sharding_method`          | `ShardingMethod`       | Auto or custom sharding                   |
| `sparse_vectors_config`    | `SparseVectorConfig`   | Sparse vector configuration               |
| `strict_mode_config`       | `StrictModeConfig`     | Operational constraints                   |

**Sources:** [qdrant\_client/proto/collections.proto366-384](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L366-L384)

### Collection Update Operations

Collection updates are performed through the `UpdateCollection` message, which allows modification of specific configuration aspects without recreating the collection:

```
```

**Sources:** [qdrant\_client/proto/collections.proto386-396](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L386-L396) [qdrant\_client/proto/collections.proto421-426](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/proto/collections.proto#L421-L426)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Collection Management](#collection-management.md)
- [Collection Lifecycle Operations](#collection-lifecycle-operations.md)
- [Core Collection Operations](#core-collection-operations.md)
- [Collection Configuration Structure](#collection-configuration-structure.md)
- [Vector Configuration Types](#vector-configuration-types.md)
- [Protocol Implementation Architecture](#protocol-implementation-architecture.md)
- [HTTP API Implementation](#http-api-implementation.md)
- [Collection Creation Parameters](#collection-creation-parameters.md)
- [Collection Update Operations](#collection-update-operations.md)
