Batch Operations | qdrant/qdrant-client | DeepWiki

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

# Batch Operations

Relevant source files

- [qdrant\_client/parallel\_processor.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py)
- [qdrant\_client/uploader/grpc\_uploader.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py)
- [qdrant\_client/uploader/rest\_uploader.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py)
- [qdrant\_client/uploader/uploader.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/uploader.py)

This document covers the batch upload system for efficient data ingestion in the qdrant-client library. The batch operations system provides parallel processing capabilities for uploading large volumes of vectors, payloads, and point data to Qdrant collections using both REST and gRPC protocols.

For information about individual point operations, see [Point Operations](qdrant/qdrant-client/3.3-point-operations.md). For FastEmbed integration with batch operations, see [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md).

## System Architecture

The batch operations system consists of three main components: the base uploader infrastructure, protocol-specific uploaders, and a parallel processing framework.

```
```

Sources: [qdrant\_client/uploader/uploader.py26-27](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/uploader.py#L26-L27) [qdrant\_client/uploader/rest\_uploader.py68](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L68-L68) [qdrant\_client/uploader/grpc\_uploader.py76](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py#L76-L76) [qdrant\_client/parallel\_processor.py87](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L87-L87)

## Base Uploader Infrastructure

The `BaseUploader` class serves as the foundation for all batch uploaders, providing common functionality for data iteration and batch processing.

### Data Iteration Methods

The base uploader provides two primary methods for organizing data into batches:

| Method                      | Purpose                                   | Input Types                                   |
| --------------------------- | ----------------------------------------- | --------------------------------------------- |
| `iterate_records_batches()` | Process `Record` or `PointStruct` objects | `Iterable[Union[Record, types.PointStruct]]`  |
| `iterate_batches()`         | Process raw vectors, payloads, and IDs    | `vectors`, `payload`, `ids` with `batch_size` |

```
```

Sources: [qdrant\_client/uploader/uploader.py28-43](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/uploader.py#L28-L43) [qdrant\_client/uploader/uploader.py45-73](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/uploader.py#L45-L73) [qdrant\_client/uploader/uploader.py13-23](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/uploader.py#L13-L23)

### Vector Batch Processing

The system handles different vector formats through specialized methods:

- **NumPy arrays**: Processed via `_vector_batches_from_numpy()` using array slicing
- **Named vectors**: Handled by `_vector_batches_from_numpy_named_vectors()` for multi-vector points
- **Iterables**: Processed directly through `iter_batch()`

Sources: [qdrant\_client/uploader/uploader.py64-94](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/uploader.py#L64-L94)

## REST Batch Uploader

The `RestBatchUploader` implements batch uploading using Qdrant's REST API through the `SyncApis` client.

### Upload Process

```
```

Sources: [qdrant\_client/uploader/rest\_uploader.py68-105](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L68-L105) [qdrant\_client/uploader/rest\_uploader.py15-65](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L15-L65)

### Key Features

- **Automatic ID generation**: Uses `uuid4()` when IDs are not provided
- **Rate limiting**: Handles `ResourceExhaustedResponse` with exponential backoff
- **Vector conversion**: Converts NumPy arrays to lists via `vector.tolist()`
- **Shard key support**: Supports `ShardKeySelector` for distributed collections

Sources: [qdrant\_client/uploader/rest\_uploader.py25-26](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L25-L26) [qdrant\_client/uploader/rest\_uploader.py46-52](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L46-L52) [qdrant\_client/uploader/rest\_uploader.py31](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L31-L31)

## gRPC Batch Uploader

The `GrpcBatchUploader` provides batch uploading using Qdrant's gRPC API with protocol buffer serialization.

### Upload Process

```
```

Sources: [qdrant\_client/uploader/grpc\_uploader.py116-131](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py#L116-L131) [qdrant\_client/uploader/grpc\_uploader.py16-73](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py#L16-L73)

### Protocol Conversion

The gRPC uploader performs extensive data conversion using the `RestToGrpc` conversion layer:

- **Point IDs**: Converts to `PointId` protobuf objects
- **Vectors**: Transforms via `convert_vector_struct()`
- **Payloads**: Serializes using `payload_to_grpc()`
- **Shard selectors**: Converts using `convert_shard_key_selector()`

Sources: [qdrant\_client/uploader/grpc\_uploader.py32-37](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py#L32-L37) [qdrant\_client/uploader/grpc\_uploader.py47-49](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py#L47-L49)

## Parallel Processing System

The `ParallelWorkerPool` coordinates multiple worker processes for concurrent batch upload operations.

### Worker Pool Architecture

```
```

Sources: [qdrant\_client/parallel\_processor.py87-103](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L87-L103) [qdrant\_client/parallel\_processor.py33-85](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L33-L85) [qdrant\_client/parallel\_processor.py129-183](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L129-L183)

### Processing Modes

The parallel processor supports three processing modes:

| Mode         | Method               | Ordering               | Use Case                   |
| ------------ | -------------------- | ---------------------- | -------------------------- |
| Unordered    | `unordered_map()`    | No ordering guarantees | Maximum throughput         |
| Semi-ordered | `semi_ordered_map()` | Index-based ordering   | Debugging and tracking     |
| Ordered      | `ordered_map()`      | Strict input order     | Order-sensitive operations |

### Error Handling and Recovery

The system includes comprehensive error handling:

- **Worker health monitoring**: Detects terminated processes via `check_worker_health()`
- **Emergency shutdown**: Terminates all processes on critical errors
- **Timeout management**: 10-minute timeout per batch processing
- **Signal-based communication**: Uses `QueueSignals` enum for process coordination

Sources: [qdrant\_client/parallel\_processor.py197-207](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L197-L207) [qdrant\_client/parallel\_processor.py209-225](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L209-L225) [qdrant\_client/parallel\_processor.py18-21](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/parallel_processor.py#L18-L21)

## Configuration and Usage

Both uploaders support similar configuration parameters:

| Parameter            | REST Uploader | gRPC Uploader | Purpose                        |
| -------------------- | ------------- | ------------- | ------------------------------ |
| `collection_name`    | ✓             | ✓             | Target collection              |
| `max_retries`        | ✓             | ✓             | Retry attempts                 |
| `wait`               | ✓             | ✓             | Wait for operation completion  |
| `shard_key_selector` | ✓             | ✓             | Distributed collection routing |
| `timeout`            | -             | ✓             | gRPC call timeout              |

### Factory Methods

Both uploaders provide `start()` class methods for initialization:

- **REST**: `RestBatchUploader.start(uri="http://localhost:6333")`
- **gRPC**: `GrpcBatchUploader.start(host="localhost", port=6334)`

Sources: [qdrant\_client/uploader/rest\_uploader.py84-94](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/rest_uploader.py#L84-L94) [qdrant\_client/uploader/grpc\_uploader.py96-114](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/uploader/grpc_uploader.py#L96-L114)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Batch Operations](#batch-operations.md)
- [System Architecture](#system-architecture.md)
- [Base Uploader Infrastructure](#base-uploader-infrastructure.md)
- [Data Iteration Methods](#data-iteration-methods.md)
- [Vector Batch Processing](#vector-batch-processing.md)
- [REST Batch Uploader](#rest-batch-uploader.md)
- [Upload Process](#upload-process.md)
- [Key Features](#key-features.md)
- [gRPC Batch Uploader](#grpc-batch-uploader.md)
- [Upload Process](#upload-process-1.md)
- [Protocol Conversion](#protocol-conversion.md)
- [Parallel Processing System](#parallel-processing-system.md)
- [Worker Pool Architecture](#worker-pool-architecture.md)
- [Processing Modes](#processing-modes.md)
- [Error Handling and Recovery](#error-handling-and-recovery.md)
- [Configuration and Usage](#configuration-and-usage.md)
- [Factory Methods](#factory-methods.md)
