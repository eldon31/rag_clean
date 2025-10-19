Remote Mode | qdrant/qdrant-client | DeepWiki

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

# Remote Mode

Relevant source files

- [qdrant\_client/async\_qdrant\_remote.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py)
- [qdrant\_client/conversions/common\_types.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/common_types.py)
- [qdrant\_client/qdrant\_remote.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py)

## Purpose and Scope

Remote Mode provides the network-based client implementation for communicating with external Qdrant services. This document covers the `QdrantRemote` and `AsyncQdrantRemote` classes that handle HTTP/REST and gRPC protocol communication, connection management, authentication, and protocol conversion.

For information about the local in-process implementation, see [Local Mode](qdrant/qdrant-client/2.2-local-mode.md). For details about protocol handling and conversion between gRPC and REST, see [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md).

## Architecture Overview

The remote client architecture centers around two main classes that implement network communication with Qdrant services through dual protocol support.

```
```

**Sources:** [qdrant\_client/qdrant\_remote.py46-208](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L46-L208) [qdrant\_client/async\_qdrant\_remote.py55-196](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py#L55-L196)

## Initialization and Configuration

The `QdrantRemote` class provides comprehensive initialization with support for various connection parameters and authentication methods.

### Connection Parameters

| Parameter     | Type             | Default       | Description                        |
| ------------- | ---------------- | ------------- | ---------------------------------- |
| `url`         | `Optional[str]`  | `None`        | Full URL including scheme and port |
| `host`        | `Optional[str]`  | `"localhost"` | Hostname or IP address             |
| `port`        | `Optional[int]`  | `6333`        | HTTP port number                   |
| `grpc_port`   | `int`            | `6334`        | gRPC port number                   |
| `prefer_grpc` | `bool`           | `False`       | Protocol preference flag           |
| `https`       | `Optional[bool]` | `None`        | HTTPS enforcement                  |
| `timeout`     | `Optional[int]`  | `None`        | Request timeout in seconds         |

### Authentication Options

| Parameter             | Type                    | Description                |
| --------------------- | ----------------------- | -------------------------- |
| `api_key`             | `Optional[str]`         | API key for authentication |
| `auth_token_provider` | `Optional[Callable]`    | Dynamic token provider     |
| `grpc_options`        | `Optional[dict]`        | gRPC channel options       |
| `grpc_compression`    | `Optional[Compression]` | gRPC compression method    |

```
```

**Sources:** [qdrant\_client/qdrant\_remote.py49-235](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L49-L235) [qdrant\_client/async\_qdrant\_remote.py58-195](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py#L58-L195)

## Protocol Selection

The remote client implements a dual-protocol system with runtime selection based on the `prefer_grpc` flag and method-specific logic.

### Protocol Selection Logic

```
```

### Protocol-Specific Implementations

Each operation method contains branching logic to handle both protocols:

```
```

**Sources:** [qdrant\_client/qdrant\_remote.py368-541](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L368-L541) [qdrant\_client/qdrant\_remote.py453-508](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L453-L508)

## Connection Management

The remote client implements lazy initialization for gRPC connections and proper resource cleanup.

### gRPC Connection Initialization

```
```

### Connection Properties

The client exposes both HTTP and gRPC clients through properties:

- `rest` / `http`: Returns `SyncApis[ApiClient]` for HTTP operations
- `grpc_points`: Returns `grpc.PointsStub` for point operations
- `grpc_collections`: Returns `grpc.CollectionsStub` for collection operations
- `grpc_snapshots`: Returns `grpc.SnapshotsStub` for snapshot operations
- `grpc_root`: Returns `grpc.QdrantStub` for root operations

**Sources:** [qdrant\_client/qdrant\_remote.py273-304](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L273-L304) [qdrant\_client/qdrant\_remote.py306-366](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L306-L366)

## Authentication

The remote client supports multiple authentication mechanisms with security warnings for insecure connections.

### Authentication Methods

```
```

### Security Implementation

The client enforces security best practices:

- Issues warnings when API keys are used over HTTP
- Supports dynamic token providers for OAuth-style authentication
- Configures appropriate headers for both REST and gRPC protocols
- Validates HTTPS usage with authentication

**Sources:** [qdrant\_client/qdrant\_remote.py133-190](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L133-L190) [qdrant\_client/async\_qdrant\_remote.py121-164](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py#L121-L164)

## Operations Implementation

The remote client implements comprehensive CRUD and search operations with consistent dual-protocol support.

### Core Operations

```
```

### Operation Pattern

Each operation follows a consistent pattern:

1. **Input Validation**: Check parameter types and convert as needed
2. **Protocol Branching**: Use `prefer_grpc` to select implementation path
3. **Model Conversion**: Convert between REST and gRPC models
4. **API Call**: Execute the appropriate client method
5. **Response Processing**: Convert response to common format
6. **Error Handling**: Handle protocol-specific errors

**Sources:** [qdrant\_client/qdrant\_remote.py368-1132](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L368-L1132) [qdrant\_client/async\_qdrant\_remote.py326-1000](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py#L326-L1000)

## Protocol Conversion

The remote client extensively uses conversion utilities to maintain compatibility between REST and gRPC protocols.

### Conversion Flow

```
```

### Common Conversions

The client performs bidirectional conversions for:

- **Filters**: `models.Filter` ↔ `grpc.Filter`
- **Search Parameters**: `models.SearchParams` ↔ `grpc.SearchParams`
- **Points**: `models.ScoredPoint` ↔ `grpc.ScoredPoint`
- **Vectors**: `models.NamedVector` ↔ `grpc.NamedVector`
- **Payloads**: `models.WithPayloadInterface` ↔ `grpc.WithPayloadSelector`

**Sources:** [qdrant\_client/qdrant\_remote.py34-47](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L34-L47) [qdrant\_client/conversions/common\_types.py48-164](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/common_types.py#L48-L164)

## Error Handling and Cleanup

The remote client implements comprehensive error handling and resource cleanup mechanisms.

### Resource Cleanup

```
```

### Connection State Management

The client maintains connection state through:

- `closed` property for state inspection
- Runtime checks before operations
- Graceful error handling for interrupted connections
- Warning system for connection issues

### Version Compatibility

The client includes automatic version compatibility checking:

- Retrieves server version on initialization
- Compares client and server versions
- Issues warnings for incompatible versions
- Allows bypassing checks with `check_compatibility=False`

**Sources:** [qdrant\_client/qdrant\_remote.py209-261](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L209-L261) [qdrant\_client/async\_qdrant\_remote.py197-221](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py#L197-L221)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Remote Mode](#remote-mode.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Architecture Overview](#architecture-overview.md)
- [Initialization and Configuration](#initialization-and-configuration.md)
- [Connection Parameters](#connection-parameters.md)
- [Authentication Options](#authentication-options.md)
- [Protocol Selection](#protocol-selection.md)
- [Protocol Selection Logic](#protocol-selection-logic.md)
- [Protocol-Specific Implementations](#protocol-specific-implementations.md)
- [Connection Management](#connection-management.md)
- [gRPC Connection Initialization](#grpc-connection-initialization.md)
- [Connection Properties](#connection-properties.md)
- [Authentication](#authentication.md)
- [Authentication Methods](#authentication-methods.md)
- [Security Implementation](#security-implementation.md)
- [Operations Implementation](#operations-implementation.md)
- [Core Operations](#core-operations.md)
- [Operation Pattern](#operation-pattern.md)
- [Protocol Conversion](#protocol-conversion.md)
- [Conversion Flow](#conversion-flow.md)
- [Common Conversions](#common-conversions.md)
- [Error Handling and Cleanup](#error-handling-and-cleanup.md)
- [Resource Cleanup](#resource-cleanup.md)
- [Connection State Management](#connection-state-management.md)
- [Version Compatibility](#version-compatibility.md)
