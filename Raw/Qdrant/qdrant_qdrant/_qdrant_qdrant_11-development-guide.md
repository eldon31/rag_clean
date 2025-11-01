Development Guide | qdrant/qdrant | DeepWiki

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

# Development Guide

Relevant source files

- [.config/nextest.toml](https://github.com/qdrant/qdrant/blob/48203e41/.config/nextest.toml)
- [.github/ISSUE\_TEMPLATE/flaky\_test.md](https://github.com/qdrant/qdrant/blob/48203e41/.github/ISSUE_TEMPLATE/flaky_test.md)
- [.github/workflows/coverage.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml)
- [.github/workflows/docker-image.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml)
- [.github/workflows/integration-tests.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml)
- [.github/workflows/release-artifacts.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml)
- [.github/workflows/rust-gpu.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-gpu.yml)
- [.github/workflows/rust-lint.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-lint.yml)
- [.github/workflows/rust.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml)
- [.github/workflows/storage-compat.yml](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/storage-compat.yml)
- [Dockerfile](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile)
- [README.md](https://github.com/qdrant/qdrant/blob/48203e41/README.md)
- [config/deb.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml)
- [docs/CODE\_OF\_CONDUCT.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/CODE_OF_CONDUCT.md)
- [docs/CONTRIBUTING.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/CONTRIBUTING.md)
- [docs/DEVELOPMENT.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md)
- [docs/QUICK\_START.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/QUICK_START.md)
- [docs/imgs/ci-coverage-report.png](https://github.com/qdrant/qdrant/blob/48203e41/docs/imgs/ci-coverage-report.png)
- [docs/imgs/local-coverage-report.png](https://github.com/qdrant/qdrant/blob/48203e41/docs/imgs/local-coverage-report.png)
- [docs/roadmap/README.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/README.md)
- [docs/roadmap/roadmap-2022.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2022.md)
- [docs/roadmap/roadmap-2023.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2023.md)
- [docs/roadmap/roadmap-2024.md](https://github.com/qdrant/qdrant/blob/48203e41/docs/roadmap/roadmap-2024.md)
- [tests/integration-tests.sh](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh)
- [tools/sync-web-ui.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/sync-web-ui.sh)

This guide provides practical information for developers contributing to Qdrant, including environment setup, development workflow, API changes, performance profiling, and testing procedures. For deployment and configuration details, see [Configuration and Deployment](qdrant/qdrant/10-configuration-and-deployment.md). For general contribution guidelines, see [docs/CONTRIBUTING.md1-50](https://github.com/qdrant/qdrant/blob/48203e41/docs/CONTRIBUTING.md#L1-L50)

---

## Development Environment Setup

### Prerequisites and Dependencies

Qdrant requires the following tools and dependencies for local development:

| Component          | Purpose                  | Installation                    |
| ------------------ | ------------------------ | ------------------------------- |
| **Rust toolchain** | Core compilation         | `rustup` with stable channel    |
| **rustfmt**        | Code formatting          | `rustup component add rustfmt`  |
| **clippy**         | Linting                  | `rustup component add clippy`   |
| **protoc**         | gRPC code generation     | Platform-specific (see below)   |
| **clang**          | C++ interop and linking  | `apt-get install clang` (Linux) |
| **Poetry**         | Python test dependencies | `pip install poetry`            |

**Protobuf Compiler Installation:**

On Linux/macOS, install protoc manually:

```
```

Sources: [docs/DEVELOPMENT.md62-78](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L62-L78)

### Building Qdrant

**Basic Build:**

```
```

**Development Build with Features:**

```
```

The build system uses `cargo-chef` for Docker layer caching (see [Dockerfile22-25](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L22-L25)) and supports cross-compilation via `xx` tooling ([Dockerfile10](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L10-L10) [Dockerfile28-31](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L28-L31)).

Sources: [docs/DEVELOPMENT.md80-85](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L80-L85) [Dockerfile28-118](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L28-L118)

### Development Environment Flow

```
```

Sources: [docs/DEVELOPMENT.md45-97](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L45-L97) [Dockerfile1-230](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L1-L230)

### Nix Development Shell

For Nix users, a complete development environment is available:

```
```

This provides Rust toolchain, Python dependencies, and all tools needed for development and testing.

Sources: [docs/DEVELOPMENT.md98-100](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L98-L100)

---

## API Changes Workflow

### REST API Changes

Qdrant uses OpenAPI 3.0 specifications with schema generation from Rust types. API changes must maintain consistency between code, specs, and tests.

```
```

**Detailed Steps:**

1. **Implement Rust endpoints and models** in `src/actix/` and `lib/api/`

2. **Update OpenAPI YTT templates** in `openapi/*ytt.yaml` files

3. **Add schema definitions** to `src/schema_generator.rs` for new types

4. **Generate specs:** `./tools/generate_openapi_models.sh`

5. **Update integration tests** in `tests/openapi/` directory

6. **Run tests:** `poetry -C tests run pytest tests/openapi`

7. **Validate specs:**

   - Serve docs: `cd docs/redoc && python -m http.server`
   - View at `http://localhost:8000/?v=master`
   - Validate YAML in [Swagger Editor](https://editor.swagger.io/)

The CI enforces consistency via `./tests/openapi_consistency_check.sh` which fails if generated specs don't match committed specs.

Sources: [docs/DEVELOPMENT.md260-278](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L260-L278) [.github/workflows/integration-tests.yml150-153](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L150-L153)

### gRPC API Changes

Qdrant uses Tonic for gRPC with protocol buffer definitions in `lib/api/src/grpc/proto/*.proto`.

```
```

**Protocol Buffer Guidelines:**

- Use `oneof` for enum-like payloads to enable type-safe variants
- Request/response types are auto-generated as Rust structs
- Service trait is implemented in Rust code
- Default gRPC port: `6334` ([tests/integration-tests.sh11](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L11-L11))

**Testing:**

```
```

Sources: [docs/DEVELOPMENT.md280-293](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L280-L293) [tests/integration-tests.sh69-75](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L69-L75)

### System Integration Considerations

When making API changes, also update:

1. **Metrics allow lists** in `src/common/metrics.rs` for new endpoints
2. **JWT integration tests** in `tests/auth_tests` for authenticated endpoints

Sources: [docs/DEVELOPMENT.md296-300](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L296-L300)

---

## Testing Infrastructure

### Test Hierarchy

```
```

Sources: [.github/workflows/rust.yml42-45](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L42-L45) [tests/integration-tests.sh63-75](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L63-L75) [.github/workflows/integration-tests.yml45-84](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L45-L84)

### Running Tests Locally

**Unit Tests:**

```
```

Configuration for nextest is in [.config/nextest.toml1-13](https://github.com/qdrant/qdrant/blob/48203e41/.config/nextest.toml#L1-L13) with retry logic and failure output settings.

**Integration Tests:**

```
```

**Consensus Tests:**

```
```

**E2E Tests:**

```
```

Sources: [tests/integration-tests.sh1-76](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L1-L76) [.github/workflows/integration-tests.yml14-83](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L14-L83) [.github/workflows/integration-tests.yml211-265](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L211-L265)

### CI/CD Pipeline

```
```

**Key CI Features:**

- **Automatic flaky test detection:** JUnit XML parsing creates GitHub issues for flaky tests ([.github/workflows/rust.yml55-112](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L55-L112))
- **Multi-platform testing:** Ubuntu, Windows, macOS ([.github/workflows/rust.yml17](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L17-L17))
- **Coverage reporting:** Daily runs upload to Codecov ([.github/workflows/coverage.yml84-111](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml#L84-L111))
- **Storage compatibility:** Tests migration between versions ([.github/workflows/storage-compat.yml1-34](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/storage-compat.yml#L1-L34))
- **GPU testing:** Separate workflow with Vulkan setup ([.github/workflows/rust-gpu.yml1-44](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-gpu.yml#L1-L44))

Sources: [.github/workflows/rust.yml1-149](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L1-L149) [.github/workflows/integration-tests.yml1-274](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L1-L274) [.github/workflows/coverage.yml1-112](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml#L1-L112)

---

## Performance Profiling and Benchmarking

### Criterion Benchmarks

Qdrant uses Criterion.rs for micro-benchmarks. Benchmarks are located in sub-crates under `benches/` directories.

**Running Benchmarks:**

```
```

Criterion automatically detects performance regressions by comparing against previous runs.

Sources: [docs/DEVELOPMENT.md102-133](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L102-L133)

### FlameGraph Profiling

Generate flame graphs for visual performance analysis:

```
```

This creates:

- FlameGraph SVG showing time spent in each function
- Profiling records for call-graph generation

**Generating Call Graphs:**

```
```

Sources: [docs/DEVELOPMENT.md136-154](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L136-L154)

### Tango.rs Comparative Benchmarks

For precise performance comparisons between code revisions:

**1. Run baseline in solo mode:**

```
```

**2. Save baseline binary:**

```
```

**3. Make code changes, then compare:**

```
```

Tango.rs runs both versions simultaneously to eliminate environmental variance.

Sources: [docs/DEVELOPMENT.md178-207](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L178-L207)

### Coverage Reporting

**Local Coverage Generation:**

```
```

**CI Coverage:**

- Daily runs on `dev` branch ([.github/workflows/coverage.yml5-6](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml#L5-L6))
- Separate unit and integration coverage
- Merged reports uploaded to [Codecov](https://app.codecov.io/gh/qdrant/qdrant/)

Sources: [docs/DEVELOPMENT.md156-176](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L156-L176) [.github/workflows/coverage.yml1-112](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml#L1-L112)

### Real-Time Profiling with Tracy

Qdrant supports optional Tracy profiler integration:

**Enable Tracy:**

```
```

**Enable tokio-console:**

```
```

**Important:**

- `tracing` is an optional dependency
- Use `#[cfg_attr(feature = "tracing", tracing::instrument)]` for optional tracing
- Never enable `log` or `log-always` features with tracing-log backend

Sources: [docs/DEVELOPMENT.md209-258](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L209-L258)

---

## Docker Development

### Multi-Stage Build Process

```
```

**Build Arguments:**

| Argument   | Purpose                          | Default    |
| ---------- | -------------------------------- | ---------- |
| `PROFILE`  | Cargo profile (release, dev, ci) | `release`  |
| `FEATURES` | Enable additional features       | `""`       |
| `GPU`      | GPU support (nvidia, amd)        | `""`       |
| `LINKER`   | Linker choice (mold, lld)        | `mold`     |
| `USER_ID`  | Non-root user ID                 | `0` (root) |
| `PACKAGES` | Extra apt packages (e.g., gdb)   | `""`       |
| `SOURCES`  | Include source in image          | `""`       |

**Building Custom Images:**

```
```

Sources: [Dockerfile1-230](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L1-L230) [docs/DEVELOPMENT.md7-40](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L7-L40)

### Development Workflow with Docker

**Run with custom configuration:**

```
```

**Key mount points:**

- `/qdrant/storage` - Persistent vector data (required)
- `/qdrant/snapshots` - Backup storage
- `/qdrant/config/production.yaml` - Config overrides
- `/qdrant/static` - Web UI assets

Sources: [docs/QUICK\_START.md26-40](https://github.com/qdrant/qdrant/blob/48203e41/docs/QUICK_START.md#L26-L40) [Dockerfile196-211](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L196-L211)

---

## Web UI Synchronization

The Qdrant web UI is maintained in a separate repository and synced using a utility script:

```
```

This script:

1. Downloads latest `dist-qdrant.zip` from [qdrant-web-ui releases](<https://github.com/qdrant/qdrant/blob/48203e41/qdrant-web-ui releases>)
2. Extracts to `./static/` directory
3. Copies OpenAPI spec from `./docs/redoc/master/openapi.json` to `./static/openapi.json`

The script is automatically invoked during Docker builds ([Dockerfile92-94](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L92-L94)).

Sources: [tools/sync-web-ui.sh1-27](https://github.com/qdrant/qdrant/blob/48203e41/tools/sync-web-ui.sh#L1-L27) [docs/DEVELOPMENT.md92-96](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L92-L96)

---

## Integration Test Details

### Test Execution Flow

```
```

**Environment Variables:**

- `QDRANT__SERVICE__GRPC_PORT=6334` - gRPC port ([tests/integration-tests.sh11](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L11-L11))
- `QDRANT__CLUSTER__ENABLED=true` - Enable distributed mode ([tests/integration-tests.sh22](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L22-L22))
- `COVERAGE=1` - Use coverage-instrumented binary ([tests/integration-tests.sh14](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L14-L14))
- `LLVM_PROFILE_FILE` - Coverage output path ([tests/integration-tests.sh12](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L12-L12))

**Graceful Shutdown:**

For coverage collection, use `kill -2` (SIGINT) instead of `kill -9` to allow graceful shutdown and coverage data flush ([tests/integration-tests.sh39](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L39-L39)).

Sources: [tests/integration-tests.sh1-76](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L1-L76)

### Consensus Test Scenarios

The consensus tests validate distributed Qdrant behavior:

```
```

These tests verify:

- Raft consensus protocol correctness
- Shard replication and failover
- Cluster scaling operations
- Snapshot and recovery in distributed mode

Sources: [.github/workflows/integration-tests.yml45-84](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L45-L84) [.github/workflows/integration-tests.yml86-118](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L86-L118)

---

## Release Process

### Build Artifacts

The release workflow ([.github/workflows/release-artifacts.yml1-178](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml#L1-L178)) produces:

| Artifact             | Platforms                               | Build Target                        |
| -------------------- | --------------------------------------- | ----------------------------------- |
| **Linux binaries**   | x86\_64-gnu, x86\_64-musl, aarch64-musl | `taiki-e/upload-rust-binary-action` |
| **macOS binaries**   | x86\_64-darwin, aarch64-darwin          | Native compilation                  |
| **Windows binaries** | x86\_64-windows                         | Native compilation                  |
| **Debian package**   | x86\_64-musl                            | `cargo deb`                         |
| **AppImage**         | x86\_64                                 | `linuxdeploy` with bundled deps     |

**Debian Package:**

```
```

**AppImage:**

```
```

Sources: [.github/workflows/release-artifacts.yml1-178](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml#L1-L178)

### Docker Image Release

Docker images are built on self-hosted runners for tag pushes:

**Image Variants:**

| Tag Pattern                         | Description              | Platforms                |
| ----------------------------------- | ------------------------ | ------------------------ |
| `qdrant/qdrant:v1.x.y`              | Release version          | linux/amd64, linux/arm64 |
| `qdrant/qdrant:latest`              | Latest release           | linux/amd64, linux/arm64 |
| `qdrant/qdrant:v1.x.y-unprivileged` | Non-root user (UID 1000) | linux/amd64, linux/arm64 |
| `qdrant/qdrant:v1.x.y-gpu-nvidia`   | NVIDIA GPU support       | linux/amd64              |
| `qdrant/qdrant:v1.x.y-gpu-amd`      | AMD GPU support          | linux/amd64              |

**Build and Push:**

```
```

Sources: [.github/workflows/docker-image.yml1-148](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L1-L148)

---

## Summary

This development guide covers the essential workflows for contributing to Qdrant:

1. **Environment Setup**: Install Rust toolchain, protoc, and dependencies
2. **Building**: Use `cargo build` with appropriate features and profiles
3. **API Changes**: Update OpenAPI specs and proto files, regenerate schemas
4. **Testing**: Run unit, integration, consensus, and E2E tests locally and in CI
5. **Profiling**: Use Criterion, FlameGraph, Tango.rs, and Tracy for performance analysis
6. **Docker**: Build custom images with multi-stage builds and build arguments
7. **Release**: Automated builds for multiple platforms and package formats

For more detailed information on specific topics:

- Configuration: See [Configuration System](qdrant/qdrant/10.1-configuration-system.md)
- Docker deployment: See [Docker Deployment](qdrant/qdrant/10.2-docker-deployment.md)
- API specifications: See [REST API Endpoints](qdrant/qdrant/9.1-rest-api-endpoints.md) and [gRPC API Services](qdrant/qdrant/9.2-grpc-api-services.md)

Sources: [docs/DEVELOPMENT.md1-301](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L1-L301) [docs/CONTRIBUTING.md1-50](https://github.com/qdrant/qdrant/blob/48203e41/docs/CONTRIBUTING.md#L1-L50)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development Guide](#development-guide.md)
- [Development Environment Setup](#development-environment-setup.md)
- [Prerequisites and Dependencies](#prerequisites-and-dependencies.md)
- [Building Qdrant](#building-qdrant.md)
- [Development Environment Flow](#development-environment-flow.md)
- [Nix Development Shell](#nix-development-shell.md)
- [API Changes Workflow](#api-changes-workflow.md)
- [REST API Changes](#rest-api-changes.md)
- [gRPC API Changes](#grpc-api-changes.md)
- [System Integration Considerations](#system-integration-considerations.md)
- [Testing Infrastructure](#testing-infrastructure.md)
- [Test Hierarchy](#test-hierarchy.md)
- [Running Tests Locally](#running-tests-locally.md)
- [CI/CD Pipeline](#cicd-pipeline.md)
- [Performance Profiling and Benchmarking](#performance-profiling-and-benchmarking.md)
- [Criterion Benchmarks](#criterion-benchmarks.md)
- [FlameGraph Profiling](#flamegraph-profiling.md)
- [Tango.rs Comparative Benchmarks](#tangors-comparative-benchmarks.md)
- [Coverage Reporting](#coverage-reporting.md)
- [Real-Time Profiling with Tracy](#real-time-profiling-with-tracy.md)
- [Docker Development](#docker-development.md)
- [Multi-Stage Build Process](#multi-stage-build-process.md)
- [Development Workflow with Docker](#development-workflow-with-docker.md)
- [Web UI Synchronization](#web-ui-synchronization.md)
- [Integration Test Details](#integration-test-details.md)
- [Test Execution Flow](#test-execution-flow.md)
- [Consensus Test Scenarios](#consensus-test-scenarios.md)
- [Release Process](#release-process.md)
- [Build Artifacts](#build-artifacts.md)
- [Docker Image Release](#docker-image-release.md)
- [Summary](#summary.md)
