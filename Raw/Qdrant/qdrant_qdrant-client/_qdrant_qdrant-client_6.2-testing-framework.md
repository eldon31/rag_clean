Testing Framework | qdrant/qdrant-client | DeepWiki

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

# Testing Framework

Relevant source files

- [tests/congruence\_tests/test\_search.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_search.py)
- [tests/congruence\_tests/test\_sparse\_search.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_sparse_search.py)
- [tests/congruence\_tests/test\_updates.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_updates.py)
- [tests/test\_in\_memory.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_in_memory.py)
- [tests/test\_local\_persistence.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_local_persistence.py)
- [tests/test\_qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py)

This page documents the testing methodology and organization of the test suite for the qdrant-client library. It provides an overview of how tests are structured, configured, and executed to ensure the library's functionality and compatibility.

## Purpose and Scope

The qdrant-client testing framework is designed to verify the correctness, reliability, and compatibility of the client library across different environments, configurations, and usage patterns. It includes unit tests, integration tests, and specialized test suites to provide comprehensive coverage of the codebase.

## Testing Architecture

The testing architecture of qdrant-client is organized around three main test categories that verify different aspects of client functionality and ensure consistency across implementations.

### Test Framework Structure

```
```

Sources: [tests/test\_qdrant\_client.py1-1161](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L1-L1161) [tests/congruence\_tests/test\_common.py58-63](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_common.py#L58-L63) [tests/test\_local\_persistence.py1-153](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_local_persistence.py#L1-L153) [tests/test\_in\_memory.py1-123](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_in_memory.py#L1-L123)

## Test Dependencies and Configuration

The testing framework relies on several Python testing libraries as specified in the project's configuration.

| Dependency     | Version | Purpose                   |
| -------------- | ------- | ------------------------- |
| pytest         | ^7.1    | Main testing framework    |
| coverage       | ^6.3.3  | Test coverage measurement |
| pytest-asyncio | ^0.21.0 | Testing asynchronous code |
| pytest-timeout | ^2.1.0  | Testing timeout scenarios |
| pytest-mock    | ^3.14.0 | Test mocking capabilities |
| autoflake      | ^2.2.1  | Code quality checks       |
| ruff           | 0.4.3   | Linting and formatting    |

The project defines custom pytest markers to categorize tests:

```
[tool.pytest.ini_options]
markers = [
    "fastembed: marks tests that require the fastembed package (deselect with '-m \"not fastembed\"')",
    "no_fastembed: marks tests that do not require the fastembed package (deselect with '-m \"not no_fastembed\"')"
]
```

These markers allow selective test execution based on the availability of optional dependencies.

Sources: [pyproject.toml37-44](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L37-L44) [pyproject.toml70-74](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L70-L74)

## Test Organization

### Unit Tests

Unit tests focus on testing individual components of the client library in isolation. The main test file `tests/test_qdrant_client.py` contains numerous test cases that verify:

1. Client initialization with different parameters
2. Collection creation and management
3. Point operations (upsert, delete, search)
4. Filtering and payload operations
5. Protocol handling (REST vs gRPC)

Example test parameterization from the codebase:

```
```

This approach ensures features are tested across both REST and gRPC protocols, as well as with different parallelism settings.

Sources: [tests/test\_qdrant\_client.py93-206](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L93-L206) [tests/test\_qdrant\_client.py208-275](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L208-L275)

### Integration Tests

Integration tests in `test_qdrant_client.py` verify end-to-end functionality with parameterized testing across different client configurations. Key test functions include:

| Test Function                    | Parameters                                  | Purpose                                |
| -------------------------------- | ------------------------------------------- | -------------------------------------- |
| `test_qdrant_client_integration` | `prefer_grpc`, `numpy_upload`, `local_mode` | Full client functionality testing      |
| `test_records_upload`            | `prefer_grpc`, `parallel`                   | Record upload with different protocols |
| `test_point_upload`              | `prefer_grpc`, `parallel`                   | Point upload operations                |
| `test_multiple_vectors`          | `prefer_grpc`                               | Multi-vector collection handling       |
| `test_upload_collection`         | `prefer_grpc`, `parallel`                   | Collection upload operations           |

Integration Test Execution Flow:

```
```

Sources: [tests/integration-tests.sh13-47](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L13-L47) [tests/test\_qdrant\_client.py243-378](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L243-L378) [tests/test\_qdrant\_client.py488-1102](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L488-L1102)

### Congruence Tests

Congruence tests verify behavioral consistency between `QdrantLocal` and `QdrantRemote` implementations. The `test_common.py` module provides client initialization fixtures:

```
```

Congruence Test Categories:

```
```

The integration test script conditionally skips congruence tests for backward compatibility testing:

```
```

Sources: [tests/congruence\_tests/test\_common.py58-84](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_common.py#L58-L84) [tests/congruence\_tests/test\_updates.py23-84](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_updates.py#L23-L84) [tests/congruence\_tests/test\_search.py148-179](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_search.py#L148-L179) [tests/integration-tests.sh41-45](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L41-L45)

## CI/CD Integration

The GitHub Actions workflow executes a comprehensive test matrix across multiple Python versions with specialized test categories.

### CI Workflow Steps

```
```

### Test Matrix Configuration

| Step                    | Python Versions | Purpose                           |
| ----------------------- | --------------- | --------------------------------- |
| Poetry Installation     | 3.9-3.13        | Install all dependencies          |
| Async Client Generation | 3.10 only       | Test code generation              |
| Cache Consistency       | 3.10 only       | Test inspection cache             |
| Coverage Testing        | 3.9-3.13        | Measure test coverage             |
| Integration Tests       | 3.9-3.13        | Full functionality testing        |
| Backward Compatibility  | 3.9-3.13        | Test against Qdrant v1.13.6       |
| No-FastEmbed Tests      | 3.9-3.13        | Test optional dependency handling |

### Environment Variables

- `QDRANT_VERSION`: Controls Qdrant server version for testing
- `IGNORE_CONGRUENCE_TESTS`: Skips congruence tests when set to "true"

Sources: [.github/workflows/integration-tests.yml14-76](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L14-L76)

## Test Execution

### Local Development Testing

The test suite supports various execution modes for local development:

```
```

### Integration Testing Process

The `integration-tests.sh` script orchestrates Docker-based testing:

Integration Test Flow:

```
```

Environment Variables:

- `QDRANT_VERSION`: Specifies Qdrant server version (default: v1.14.0)
- `IGNORE_CONGRUENCE_TESTS`: Skip congruence tests when set to "true"

Sources: [tests/integration-tests.sh13-47](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/integration-tests.sh#L13-L47)

## Specialized Test Categories

### Protocol Testing

Protocol testing ensures consistent behavior across REST and gRPC implementations using parameterized tests:

```
```

Key parameterized test functions:

- `test_records_upload(prefer_grpc, parallel)`
- `test_point_upload(prefer_grpc, parallel)`
- `test_multiple_vectors(prefer_grpc)`
- `test_qdrant_client_integration(prefer_grpc, numpy_upload, local_mode)`

Sources: [tests/test\_qdrant\_client.py243-244](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L243-L244) [tests/test\_qdrant\_client.py312-313](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L312-L313) [tests/test\_qdrant\_client.py488-491](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_qdrant_client.py#L488-L491)

### Local Mode Testing

Local mode tests verify in-process and persistence functionality:

| Test File                   | Test Functions                                                                                            | Purpose                                        |
| --------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `test_local_persistence.py` | `test_local_dense_persistence()`, `test_local_sparse_persistence()`                                       | Verify data persistence across client restarts |
| `test_in_memory.py`         | `test_dense_in_memory_key_filter_returns_results()`, `test_sparse_in_memory_key_filter_returns_results()` | Verify in-memory operation correctness         |

### FastEmbed Integration

FastEmbed integration testing uses pytest markers to handle optional dependencies:

```
```

The CI workflow validates graceful degradation when fastembed is unavailable:

```
```

Sources: [.github/workflows/integration-tests.yml72-76](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/.github/workflows/integration-tests.yml#L72-L76) [pyproject.toml70-74](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/pyproject.toml#L70-L74) [tests/test\_local\_persistence.py92-153](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_local_persistence.py#L92-L153) [tests/test\_in\_memory.py11-123](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/test_in_memory.py#L11-L123)

## Conclusion

The qdrant-client testing framework provides comprehensive test coverage across different client configurations, protocols, and environments. The combination of unit tests, integration tests, and specialized test suites ensures that the client behaves correctly and consistently in various scenarios.

The test architecture supports both local development testing and automated CI testing, with special consideration for backward compatibility and optional dependency testing. This ensures that the client remains reliable as both the client and server evolve over time.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Testing Framework](#testing-framework.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Testing Architecture](#testing-architecture.md)
- [Test Framework Structure](#test-framework-structure.md)
- [Test Dependencies and Configuration](#test-dependencies-and-configuration.md)
- [Test Organization](#test-organization.md)
- [Unit Tests](#unit-tests.md)
- [Integration Tests](#integration-tests.md)
- [Congruence Tests](#congruence-tests.md)
- [CI/CD Integration](#cicd-integration.md)
- [CI Workflow Steps](#ci-workflow-steps.md)
- [Test Matrix Configuration](#test-matrix-configuration.md)
- [Environment Variables](#environment-variables.md)
- [Test Execution](#test-execution.md)
- [Local Development Testing](#local-development-testing.md)
- [Integration Testing Process](#integration-testing-process.md)
- [Specialized Test Categories](#specialized-test-categories.md)
- [Protocol Testing](#protocol-testing.md)
- [Local Mode Testing](#local-mode-testing.md)
- [FastEmbed Integration](#fastembed-integration.md)
- [Conclusion](#conclusion.md)
