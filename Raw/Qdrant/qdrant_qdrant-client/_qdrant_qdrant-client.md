qdrant/qdrant-client | DeepWiki

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

# Overview

Relevant source files

- [.github/workflows/integration-tests.yml](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml)
- [README.md](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md)
- [poetry.lock](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/poetry.lock)
- [pyproject.toml](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml)
- [qdrant\_client/\_\_init\_\_.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/__init__.py)
- [tests/benches/test\_grpc\_upload.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/benches/test_grpc_upload.py)
- [tests/benches/test\_rest\_upload.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/benches/test_rest_upload.py)
- [tests/integration-tests.sh](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh)

This document provides a comprehensive overview of the qdrant-client Python library, a client SDK for interacting with the Qdrant vector database. The qdrant-client provides both local in-process capabilities and remote network-based communication with Qdrant servers, supporting multiple protocols and embedding integrations.

For detailed information about specific subsystems, see [Client Architecture](qdrant/qdrant-client/2-client-architecture.md), [Core Operations](qdrant/qdrant-client/3-core-operations.md), [Advanced Features](qdrant/qdrant-client/4-advanced-features.md), and [Implementation Details](qdrant/qdrant-client/5-implementation-details.md).

## Purpose and Scope

The qdrant-client is a Python library that serves as the primary interface for interacting with Qdrant, a vector similarity search engine. The library provides:

- **Unified API**: Single interface for both local and remote Qdrant instances
- **Protocol Support**: HTTP/REST and gRPC communication protocols
- **Embedding Integration**: Built-in FastEmbed support for automatic text/image embedding
- **Async Support**: Full async/await compatibility alongside synchronous operations
- **Local Development**: In-memory and file-based storage for development and testing

**Sources:** [pyproject.toml1-79](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L1-L79) [README.md1-301](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L1-L301)

## Core Architecture

The qdrant-client implements a layered architecture with unified client interfaces that abstract over different backend implementations and communication protocols.

### Primary Client Interface

```
```

**Sources:** [qdrant\_client/\_\_init\_\_.py1-3](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/__init__.py#L1-L3) [README.md54-62](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L54-L62) [README.md133-139](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L133-L139)

### Protocol and Communication Layer

```
```

**Sources:** [tests/integration-tests.sh17-19](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L17-L19) [README.md237-245](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L237-L245) [pyproject.toml18](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L18-L18) [pyproject.toml26-27](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L26-L27)

## Installation and Dependencies

The library is distributed as a Python package with configurable optional dependencies:

| Component     | Installation                               | Purpose                              |
| ------------- | ------------------------------------------ | ------------------------------------ |
| Core          | `pip install qdrant-client`                | Basic HTTP/gRPC client functionality |
| FastEmbed     | `pip install qdrant-client[fastembed]`     | CPU-based embedding generation       |
| FastEmbed GPU | `pip install qdrant-client[fastembed-gpu]` | GPU-accelerated embeddings           |

### Key Dependencies

- **Core Runtime**: `httpx`, `grpcio`, `protobuf`, `pydantic`, `numpy`
- **Local Storage**: `portalocker` for file-based persistence
- **Optional Embeddings**: `fastembed` or `fastembed-gpu` for model inference
- **Development**: `pytest`, `poetry`, `ruff`, `mypy` for testing and code quality

**Sources:** [pyproject.toml16-36](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L16-L36) [pyproject.toml60-62](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L60-L62) [README.md31-35](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L31-L35) [README.md72-74](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L72-L74)

## Usage Patterns

### Local Mode Operations

```
```

**Sources:** [README.md56-62](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L56-L62) [README.md64-68](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L64-L68)

### Remote Mode Operations

```
```

**Sources:** [README.md133-139](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L133-L139) [README.md150-163](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L150-L163) [README.md241-245](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L241-L245)

## Testing and Quality Assurance

The library implements comprehensive testing across multiple dimensions:

### Test Matrix

| Test Type           | Coverage                 | Purpose                              |
| ------------------- | ------------------------ | ------------------------------------ |
| Integration Tests   | Full API surface         | End-to-end functionality with Docker |
| Congruence Tests    | Local vs Remote          | Behavioral consistency validation    |
| Unit Tests          | Individual components    | Component-level correctness          |
| Async Tests         | Async client methods     | Async/await compatibility            |
| Compatibility Tests | Multiple Python versions | Cross-version support                |

### CI/CD Pipeline

The continuous integration system validates across:

- **Python Versions**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Qdrant Versions**: Latest and backward compatibility (v1.13.6)
- **Optional Dependencies**: With and without FastEmbed
- **Protocol Testing**: Both HTTP and gRPC implementations

**Sources:** [.github/workflows/integration-tests.yml14-24](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L14-L24) [tests/integration-tests.sh14-45](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L14-L45) [pyproject.toml71-75](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L71-L75)

## FastEmbed Integration

The library provides optional integration with FastEmbed for automatic embedding generation:

```
```

**Sources:** [README.md76-79](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L76-L79) [README.md86-112](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L86-L112) [README.md114-128](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L114-L128)

This overview establishes the foundation for understanding the qdrant-client's architecture and capabilities. Detailed implementation specifics are covered in subsequent sections of this documentation.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Overview](#overview.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Core Architecture](#core-architecture.md)
- [Primary Client Interface](#primary-client-interface.md)
- [Protocol and Communication Layer](#protocol-and-communication-layer.md)
- [Installation and Dependencies](#installation-and-dependencies.md)
- [Key Dependencies](#key-dependencies.md)
- [Usage Patterns](#usage-patterns.md)
- [Local Mode Operations](#local-mode-operations.md)
- [Remote Mode Operations](#remote-mode-operations.md)
- [Testing and Quality Assurance](#testing-and-quality-assurance.md)
- [Test Matrix](#test-matrix.md)
- [CI/CD Pipeline](#cicd-pipeline.md)
- [FastEmbed Integration](#fastembed-integration.md)
