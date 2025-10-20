Client Architecture | qdrant/qdrant-client | DeepWiki

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

# Client Architecture

Relevant source files

- [qdrant\_client/async\_qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_client.py)
- [qdrant\_client/qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py)

This document explains the overall architecture of the qdrant-client Python library, covering the unified client interface and dual backend implementation strategy. The architecture provides a consistent API surface while supporting both local in-process vector storage and remote network-based communication with Qdrant services.

For information about specific search operations and query processing, see [Search Operations](qdrant/qdrant-client/3.1-search-operations.md). For details about FastEmbed integration and embedding workflows, see [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md).

## Unified Client Interface

The client architecture centers around two main entry points that provide identical APIs for synchronous and asynchronous operations:

```
```

The `QdrantClient` class serves as the primary synchronous interface, while `AsyncQdrantClient` provides the asynchronous equivalent. Both classes inherit from `QdrantFastembedMixin` to enable automatic embedding generation capabilities.

**Sources:** [qdrant\_client/qdrant\_client.py27-78](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L27-L78) [qdrant\_client/async\_qdrant\_client.py26-77](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_client.py#L26-L77)

## Backend Selection Logic

The client architecture implements a parameter-based backend selection system that determines whether to use local or remote implementations:

```
```

The selection logic follows these rules:

| Parameter                                 | Backend | Description                   |
| ----------------------------------------- | ------- | ----------------------------- |
| `location=":memory:"`                     | Local   | In-memory vector database     |
| `path="/some/path"`                       | Local   | Persistent file-based storage |
| `url`, `host`, or `location` (non-memory) | Remote  | Network-based communication   |

**Sources:** [qdrant\_client/qdrant\_client.py121-153](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L121-L153) [qdrant\_client/async\_qdrant\_client.py111-140](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_client.py#L111-L140)

## Local Backend Implementation

The local backend provides in-process vector storage and search capabilities through the `QdrantLocal` class:

```
```

The local implementation enables:

- **In-memory mode**: Volatile storage for development and testing
- **Persistent mode**: File-based storage for production deployments
- **Full vector operations**: Search, CRUD operations, and filtering without network overhead
- **Thread safety controls**: Configurable via `force_disable_check_same_thread`

**Sources:** [qdrant\_client/qdrant\_client.py126-135](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L126-L135) [qdrant\_client/local/qdrant\_local.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py)

## Remote Backend Implementation

The remote backend handles network communication with external Qdrant services through the `QdrantRemote` class:

```
```

The remote implementation provides:

- **Dual protocol support**: HTTP/REST (port 6333) and gRPC (port 6334)
- **Protocol preference**: Configurable via `prefer_grpc` parameter
- **Authentication**: API key support and token provider callbacks
- **Connection management**: Timeout configuration and connection pooling
- **Cloud integration**: Direct support for Qdrant Cloud services

**Sources:** [qdrant\_client/qdrant\_client.py139-153](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L139-L153) [qdrant\_client/qdrant\_remote.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py)

## Protocol Abstraction Layer

The client architecture implements a protocol abstraction that allows transparent switching between HTTP/REST and gRPC communication:

```
```

Key features of the protocol abstraction:

- **Automatic conversion**: Seamless translation between gRPC and REST data structures
- **Unified types**: Common type system in `conversions.common_types`
- **Protocol transparency**: Client methods accept both gRPC and REST structures
- **Performance optimization**: Protocol selection based on operation type and preferences

The client exposes low-level protocol access through properties:

- `grpc_points` and `grpc_collections`: Direct gRPC stub access
- `http`/`rest`: Direct REST API client access

**Sources:** [qdrant\_client/qdrant\_client.py174-225](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L174-L225) [qdrant\_client/conversions/common\_types.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/common_types.py)

## Embedding Integration Architecture

The client architecture integrates embedding capabilities through the `QdrantFastembedMixin` class:

```
```

The embedding integration enables:

- **Automatic detection**: Type inspection for inference objects
- **Batch processing**: Configurable batch sizes for embedding generation
- **Dual inference modes**: Local FastEmbed models or cloud-based inference
- **Seamless integration**: Transparent embedding in query and upsert operations

**Sources:** [qdrant\_client/qdrant\_client.py112-116](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L112-L116) [qdrant\_client/qdrant\_fastembed.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_fastembed.py) [qdrant\_client/embed/type\_inspector.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/type_inspector.py)

## Configuration and Initialization

The client architecture provides comprehensive configuration through initialization parameters:

| Parameter Category          | Parameters                                      | Purpose                        |
| --------------------------- | ----------------------------------------------- | ------------------------------ |
| **Backend Selection**       | `location`, `url`, `host`, `path`               | Choose local vs remote backend |
| **Network Configuration**   | `port`, `grpc_port`, `https`, `timeout`         | Network connection settings    |
| **Authentication**          | `api_key`, `auth_token_provider`                | Security credentials           |
| **Protocol Settings**       | `prefer_grpc`, `prefix`                         | Protocol preferences           |
| **Embedding Configuration** | `cloud_inference`, `local_inference_batch_size` | Embedding behavior             |
| **Local Settings**          | `force_disable_check_same_thread`               | Local backend options          |

The initialization process validates parameter combinations and configures the appropriate backend with proper error handling for invalid configurations.

**Sources:** [qdrant\_client/qdrant\_client.py80-161](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L80-L161) [qdrant\_client/async\_qdrant\_client.py79-146](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_client.py#L79-L146)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Architecture](#client-architecture.md)
- [Unified Client Interface](#unified-client-interface.md)
- [Backend Selection Logic](#backend-selection-logic.md)
- [Local Backend Implementation](#local-backend-implementation.md)
- [Remote Backend Implementation](#remote-backend-implementation.md)
- [Protocol Abstraction Layer](#protocol-abstraction-layer.md)
- [Embedding Integration Architecture](#embedding-integration-architecture.md)
- [Configuration and Initialization](#configuration-and-initialization.md)
