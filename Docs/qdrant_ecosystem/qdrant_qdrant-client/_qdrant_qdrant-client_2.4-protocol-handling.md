Protocol Handling | qdrant/qdrant-client | DeepWiki

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

# Protocol Handling

Relevant source files

- [qdrant\_client/common/client\_exceptions.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/common/client_exceptions.py)
- [qdrant\_client/connection.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py)
- [qdrant\_client/conversions/conversion.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py)
- [qdrant\_client/http/api\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py)
- [qdrant\_client/http/models/models.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/models/models.py)
- [tests/conversions/fixtures.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/conversions/fixtures.py)
- [tests/conversions/test\_validate\_conversions.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/conversions/test_validate_conversions.py)
- [tools/generate\_grpc\_client.sh](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tools/generate_grpc_client.sh)
- [tools/generate\_rest\_client.sh](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tools/generate_rest_client.sh)

This document covers the protocol handling mechanisms in the qdrant-client library, specifically focusing on the conversion layer between gRPC and REST protocols, connection management, and protocol selection logic. The system enables seamless communication with Qdrant services through both HTTP/REST and gRPC interfaces while maintaining a unified client API.

For information about the client interface that utilizes these protocols, see [Client Interface](qdrant/qdrant-client/2.1-client-interface.md). For details about remote mode implementation, see [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md).

## Architecture Overview

The protocol handling system consists of three main components: bidirectional conversion between gRPC and REST formats, connection management for both protocols, and error handling across transport layers.

### Protocol Conversion Flow

```
```

Sources: [qdrant\_client/conversions/conversion.py1-2069](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L1-L2069) [qdrant\_client/connection.py1-308](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L1-L308) [qdrant\_client/http/api\_client.py1-264](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py#L1-L264)

## gRPC to REST Conversion System

The `GrpcToRest` class provides comprehensive conversion from gRPC protocol buffer messages to REST API Pydantic models. This system handles complex nested structures, enums, and specialized data types.

### Core Conversion Methods

```
```

The conversion system handles complex type mapping including:

| gRPC Type          | REST Type           | Conversion Method        |
| ------------------ | ------------------- | ------------------------ |
| `grpc.Condition`   | `rest.Condition`    | `convert_condition()`    |
| `grpc.Filter`      | `rest.Filter`       | `convert_filter()`       |
| `grpc.ScoredPoint` | `rest.ScoredPoint`  | `convert_scored_point()` |
| `grpc.Value`       | Python native types | `value_to_json()`        |

Sources: [qdrant\_client/conversions/conversion.py140-163](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L140-L163) [qdrant\_client/conversions/conversion.py165-182](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L165-L182) [qdrant\_client/conversions/conversion.py560-578](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L560-L578)

### Payload Conversion

The payload conversion system transforms between gRPC's structured `Value` types and Python native types:

```
```

Sources: [qdrant\_client/conversions/conversion.py58-88](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L58-L88) [qdrant\_client/conversions/conversion.py90-96](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L90-L96)

## REST to gRPC Conversion System

The `RestToGrpc` class performs the inverse conversion, transforming REST API requests into gRPC protocol buffer messages. This system ensures proper field mapping and type validation.

### Payload to gRPC Conversion

```
```

Sources: [qdrant\_client/conversions/conversion.py36-56](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L36-L56) [qdrant\_client/conversions/conversion.py90-92](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/conversion.py#L90-L92)

## Connection Management

The connection management system handles both gRPC and HTTP connections with support for authentication, interceptors, and error handling.

### gRPC Connection System

```
```

Sources: [qdrant\_client/connection.py254-276](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L254-L276) [qdrant\_client/connection.py278-307](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L278-L307) [qdrant\_client/connection.py131-182](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L131-L182)

### HTTP Connection System

```
```

Sources: [qdrant\_client/http/api\_client.py67-153](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py#L67-L153) [qdrant\_client/http/api\_client.py154-241](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py#L154-L241) [qdrant\_client/http/api\_client.py243-251](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py#L243-L251)

## Error Handling

The protocol handling system includes comprehensive error handling for both gRPC and HTTP protocols, with special attention to rate limiting and resource exhaustion.

### gRPC Error Handling

```
```

Sources: [qdrant\_client/connection.py135-148](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L135-L148) [qdrant\_client/connection.py189-207](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L189-L207)

### HTTP Error Handling

```
```

Sources: [qdrant\_client/http/api\_client.py114-130](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py#L114-L130) [qdrant\_client/http/api\_client.py203-219](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/http/api_client.py#L203-L219) [qdrant\_client/common/client\_exceptions.py5-17](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/common/client_exceptions.py#L5-L17)

## Protocol Selection Logic

The protocol selection mechanism allows clients to choose between gRPC and HTTP protocols based on configuration and preferences. This is typically handled at the client initialization level, with the conversion system providing the necessary bridge between protocols.

### Default Channel Options

The connection system provides default gRPC channel options for optimal performance:

| Option                            | Value | Purpose                        |
| --------------------------------- | ----- | ------------------------------ |
| `grpc.max_send_message_length`    | -1    | Unlimited send message size    |
| `grpc.max_receive_message_length` | -1    | Unlimited receive message size |

Sources: [qdrant\_client/connection.py239-252](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/connection.py#L239-L252)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Protocol Handling](#protocol-handling.md)
- [Architecture Overview](#architecture-overview.md)
- [Protocol Conversion Flow](#protocol-conversion-flow.md)
- [gRPC to REST Conversion System](#grpc-to-rest-conversion-system.md)
- [Core Conversion Methods](#core-conversion-methods.md)
- [Payload Conversion](#payload-conversion.md)
- [REST to gRPC Conversion System](#rest-to-grpc-conversion-system.md)
- [Payload to gRPC Conversion](#payload-to-grpc-conversion.md)
- [Connection Management](#connection-management.md)
- [gRPC Connection System](#grpc-connection-system.md)
- [HTTP Connection System](#http-connection-system.md)
- [Error Handling](#error-handling.md)
- [gRPC Error Handling](#grpc-error-handling.md)
- [HTTP Error Handling](#http-error-handling.md)
- [Protocol Selection Logic](#protocol-selection-logic.md)
- [Default Channel Options](#default-channel-options.md)
