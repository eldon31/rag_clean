Building and CI/CD | qdrant/qdrant | DeepWiki

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

# Building and CI/CD

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

## Purpose and Scope

This document describes Qdrant's build system, continuous integration pipelines, and release artifact generation. It covers the Docker multi-stage build process, GitHub Actions workflows for testing and deployment, testing infrastructure using nextest and pytest, and the release process for Docker images and binary artifacts.

For information about:

- Runtime configuration options, see [Configuration System](qdrant/qdrant/10.1-configuration-system.md)
- Deploying with Docker, see [Docker Deployment](qdrant/qdrant/10.2-docker-deployment.md)
- Contributing and local development workflows, see [Development Guide](qdrant/qdrant/11-development-guide.md)

---

## Docker Multi-Stage Build Architecture

Qdrant uses a sophisticated multi-stage Docker build with cross-compilation support, layer caching optimization via `cargo-chef`, and conditional base images for CPU and GPU variants.

```
```

**Docker Build Stages**

Sources: [Dockerfile1-230](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L1-L230)

### Stage 1: Dependency Planning

The `planner` stage uses `cargo-chef` to extract the dependency graph without source code, enabling Docker layer caching of dependencies separately from application code.

```
```

**Key mechanism**: [Dockerfile22-25](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L22-L25) copies all source files and runs `cargo chef prepare` to generate a recipe that captures dependencies without code.

Sources: [Dockerfile22-25](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L22-L25)

### Stage 2: Builder

The `builder` stage performs cross-compilation with multiple optimizations:

**Dependencies and Tooling**

| Component           | Purpose                     | Installation                                                                                                         |
| ------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `clang`, `lld`      | C/C++ compiler and linker   | `apt-get install` [Dockerfile42-44](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L42-L44)               |
| `protobuf-compiler` | Protocol buffer compilation | `apt-get install` [Dockerfile42-44](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L42-L44)               |
| `mold` v2.36.0      | Fast linker (default)       | Downloaded from GitHub releases [Dockerfile52-66](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L52-L66) |
| `xx` tools          | Cross-compilation helpers   | Copied from `tonistiigi/xx` [Dockerfile31](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L31-L31)        |
| `cargo-chef`        | Dependency caching          | Pre-installed in base image [Dockerfile19](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L19-L19)        |

**Build Arguments**

| Argument        | Default   | Purpose                                                                                                                        |
| --------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `PROFILE`       | `release` | Cargo profile (`release`, `dev`, `ci`) [Dockerfile77](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L77-L77)       |
| `FEATURES`      | (none)    | Comma-separated crate features [Dockerfile80](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L80-L80)               |
| `RUSTFLAGS`     | (none)    | Additional Rust compiler flags [Dockerfile83](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L83-L83)               |
| `LINKER`        | `mold`    | Linker selection (`mold`, `lld`, or default) [Dockerfile86](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L86-L86) |
| `GPU`           | (none)    | GPU support (`nvidia` or `amd`) [Dockerfile89](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L89-L89)              |
| `GIT_COMMIT_ID` | (none)    | Git commit SHA embedded in binary [Dockerfile108](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L108-L108)         |

**Cross-Compilation Setup**

The builder uses `xx-cargo` wrapper with a workaround for `PKG_CONFIG` path resolution:

```
```

This configuration:

- Sets correct `PKG_CONFIG` for cross-compilation [Dockerfile101-104](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L101-L104)
- Adds mold to PATH if selected
- Configures linker via `RUSTFLAGS`
- Always includes `stacktrace` feature
- Conditionally adds `gpu` feature

**Web UI Integration**

The build downloads the latest Qdrant Web UI from GitHub releases:

```
```

Sources: [Dockerfile91-94](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L91-L94) [tools/sync-web-ui.sh1-27](https://github.com/qdrant/qdrant/blob/48203e41/tools/sync-web-ui.sh#L1-L27)

### Stage 3: Base Image Selection

Qdrant supports three base image variants selected via the `GPU` build argument:

```
```

**GPU-Specific Configuration**

For NVIDIA GPUs [Dockerfile130-139](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L130-L139):

- Adds `/etc/vulkan/icd.d/nvidia_icd.json` for Vulkan loader
- Sets `NVIDIA_DRIVER_CAPABILITIES=compute,graphics,utility`
- Requires `--gpus all` flag at runtime

For AMD GPUs [Dockerfile142-147](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L142-L147):

- Uses ROCm development image with GPU drivers pre-installed

Both GPU variants install Vulkan runtime dependencies [Dockerfile155-161](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L155-L161):

```
```

Sources: [Dockerfile123-161](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L123-L161)

### Stage 4: Final Runtime Image

The final stage assembles the minimal runtime environment:

**Optional Features via Build Args**

| Build Arg  | Effect                                                                                                                                 |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `PACKAGES` | Additional apt packages (e.g., `gdb`, `lldb`) [Dockerfile165-167](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L165-L167) |
| `SOURCES`  | Copy source code for debugging [Dockerfile174-194](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L174-L194)                |
| `USER_ID`  | Run as non-root user (default: `0`) [Dockerfile198-205](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L198-L205)           |

**Conditional Source Copy**

When `SOURCES` is set, the build includes debugging symbols:

```
```

This hack uses parameter expansion with wildcard to make `COPY` conditional. If `SOURCES` is unset, `${DIR:-/null?}` matches nothing and `COPY` silently skips.

Sources: [Dockerfile176-194](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L176-L194)

**File Layout**

```
/qdrant/
├── qdrant                # Binary executable
├── qdrant.spdx.json      # SBOM (Software Bill of Materials)
├── config/               # Default configurations
├── static/               # Web UI assets
├── entrypoint.sh         # Startup script
├── storage/              # Data directory (volume mount)
└── snapshots/            # Snapshot directory (volume mount)
```

Sources: [Dockerfile196-230](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L196-L230)

---

## GitHub Actions Workflows

Qdrant uses multiple GitHub Actions workflows for continuous integration and deployment. All workflows use Swatinem/rust-cache for dependency caching.

```
```

Sources: [.github/workflows/](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/)

### rust.yml - Core Test Suite

The primary test workflow runs on every push and pull request, executing tests across three operating systems.

**Matrix Strategy**

```
```

**Test Execution with Nextest**

Qdrant uses `cargo-nextest` instead of `cargo test` for faster test execution and better output:

```
```

The `ci` profile is configured in [.config/nextest.toml1-12](https://github.com/qdrant/qdrant/blob/48203e41/.config/nextest.toml#L1-L12):

- Retries failing tests with exponential backoff (1 retry, 2s initial delay)
- Does not fail-fast (runs all tests even after failures)
- Outputs failure details immediately and at end
- Generates JUnit XML report

**Flaky Test Detection**

A separate `process-results` job parses the JUnit XML output to detect flaky tests (tests that fail but pass on retry):

```
```

The workflow uses `yq`/`xq` to extract flaky test information and creates issues from [.github/ISSUE\_TEMPLATE/flaky\_test.md1-26](https://github.com/qdrant/qdrant/blob/48203e41/.github/ISSUE_TEMPLATE/flaky_test.md#L1-L26) template.

Sources: [.github/workflows/rust.yml1-149](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L1-L149)

### integration-tests.yml - Integration Testing

This workflow runs multiple test suites validating API behavior, distributed consensus, and end-to-end scenarios.

**Job 1: integration-tests**

Runs OpenAPI integration tests with Python pytest:

```
```

The integration test script [tests/integration-tests.sh1-76](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L1-L76):

1. Starts Qdrant in background (standalone or distributed mode)
2. Waits for server readiness via `/collections` endpoint
3. Runs pytest on `tests/openapi`
4. Runs shell-based tests: `basic_api_test.sh`, `basic_sparse_test.sh`, `basic_grpc_test.sh`

**Job 2: integration-tests-consensus**

Tests distributed Qdrant with Raft consensus:

```
```

Consensus tests validate:

- Leader election
- Shard transfers
- Replica synchronization
- Failure recovery

**Job 3: test-consensus-compose**

Validates multi-node deployment using Docker Compose:

```
```

**Job 4: test-consistency**

Ensures generated API schemas match source code:

```
```

These scripts verify that committed OpenAPI and gRPC definitions are up-to-date with code changes.

**Job 5: test-shard-snapshot-api-s3-minio**

Tests snapshot functionality with local S3 (MinIO) and filesystem storage:

```
```

**Job 6: e2e-tests**

End-to-end tests with Docker containers and pytest-xdist parallel execution:

```
```

Sources: [.github/workflows/integration-tests.yml1-274](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L1-L274)

### rust-lint.yml - Code Quality

Enforces code formatting and linting standards:

```
```

The workflow uses three clippy invocations with increasing scope to catch issues in:

1. Library code
2. Tests and benchmarks (`--all-targets`)
3. Optional feature combinations (`--all-features`)

Sources: [.github/workflows/rust-lint.yml1-46](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-lint.yml#L1-L46)

### coverage.yml - Code Coverage

Runs daily (cron schedule) to generate coverage reports for both unit and integration tests.

**Coverage Collection Strategy**

```
```

The workflow uses `cargo-llvm-cov` to instrument code and generate coverage data. Integration tests run with `LLVM_PROFILE_FILE` environment variable set [tests/integration-tests.sh12](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L12-L12)

**Branch Override Logic**

Coverage reports can be triggered manually or by cron. The workflow adjusts the target branch:

```
```

For scheduled runs, coverage targets the `dev` branch; for manual triggers, it uses the current branch.

Sources: [.github/workflows/coverage.yml1-112](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml#L1-L112)

### docker-image.yml - Container Image Publishing

Triggered on Git tag push, this workflow builds and publishes multi-platform Docker images with multiple variants.

**Self-Hosted Runner Strategy**

This workflow runs on `[self-hosted, linux, x64]` runners rather than GitHub-hosted to handle:

- Multi-platform builds requiring QEMU
- Large Docker layer caches
- Extended build times for cross-compilation

**Job 1: build (CPU + Unprivileged)**

Builds standard and unprivileged variants for CPU-only workloads:

```
```

The unprivileged variant uses `--build-arg USER_ID=1000` to run as non-root user.

**Job 2: build-gpu (NVIDIA + AMD)**

Builds GPU-accelerated images for NVIDIA and AMD platforms:

```
```

GPU images are amd64-only due to lack of ARM GPU support in base images.

**Image Tags**

For version tag `v1.2.3`, the workflow publishes:

| Variant      | Tags                                                                              |
| ------------ | --------------------------------------------------------------------------------- |
| CPU          | `1.2.3`, `latest`, `1.2`, `1`                                                     |
| Unprivileged | `1.2.3-unprivileged`, `latest-unprivileged`, `1.2-unprivileged`, `1-unprivileged` |
| GPU NVIDIA   | `1.2.3-gpu-nvidia`, `gpu-nvidia-latest`, `1.2-gpu-nvidia`, `1-gpu-nvidia`         |
| GPU AMD      | `1.2.3-gpu-amd`, `gpu-amd-latest`, `1.2-gpu-amd`, `1-gpu-amd`                     |

**SBOM and Signing**

All images include Software Bill of Materials (SBOM) via `--sbom=true` flag and are signed with Cosign using OIDC keyless signing for supply chain security.

Sources: [.github/workflows/docker-image.yml1-148](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L1-L148)

### release-artifacts.yml - Binary Releases

Triggered on GitHub release publication, this workflow builds and uploads binary artifacts for multiple platforms.

**Build Matrix**

```
```

**Linux Build Process**

Uses `taiki-e/setup-cross-toolchain-action` for musl cross-compilation:

```
```

**Debian Package Generation**

The `x86_64-unknown-linux-musl` target additionally generates a `.deb` package:

```
```

The Debian package uses configuration from [config/deb.yaml1-10](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml#L1-L10) to set:

- Storage path: `/var/lib/qdrant/storage`
- Snapshots path: `/var/lib/qdrant/snapshots`
- Static content: `/var/lib/qdrant/static`

**AppImage Creation**

The `build-app-image` job creates a portable Linux executable:

```
```

The resulting `qdrant-x86_64.AppImage` is a self-contained executable that includes the web UI and all dependencies.

Sources: [.github/workflows/release-artifacts.yml1-178](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml#L1-L178)

### storage-compat.yml - Version Compatibility

Tests storage format compatibility between Qdrant versions to ensure seamless upgrades.

```
```

This workflow validates that collections created with older Qdrant versions can be read by newer versions, preventing data migration issues.

Sources: [.github/workflows/storage-compat.yml1-34](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/storage-compat.yml#L1-L34)

### rust-gpu.yml - GPU Functionality

Manually triggered workflow to test GPU-enabled features (requires GPU hardware on runners):

```
```

Tests validate:

- Vulkan initialization
- GPU vector operations
- Quantization on GPU
- HNSW graph operations with GPU acceleration

Sources: [.github/workflows/rust-gpu.yml1-105](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-gpu.yml#L1-L105)

---

## Testing Infrastructure

Qdrant employs a multi-layered testing strategy combining Rust unit tests, integration tests via pytest, and end-to-end scenarios.

### Nextest Configuration

The [.config/nextest.toml1-12](https://github.com/qdrant/qdrant/blob/48203e41/.config/nextest.toml#L1-L12) file defines the `ci` profile used in GitHub Actions:

```
```

**Key behaviors**:

- Retries flaky tests once with 2-second initial delay
- Continues running all tests after failures
- Outputs failures immediately and again at end for scrollback
- Generates JUnit XML for GitHub Actions integration

### Integration Test Script

The [tests/integration-tests.sh1-76](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L1-L76) orchestrates multiple test suites:

```
```

**Test Organization**

| Test Suite              | Purpose                | Technology                      |
| ----------------------- | ---------------------- | ------------------------------- |
| `tests/openapi`         | REST API functionality | pytest                          |
| `tests/consensus_tests` | Distributed consensus  | pytest with multi-node clusters |
| `tests/e2e_tests`       | End-to-end scenarios   | pytest + Docker                 |
| `basic_api_test.sh`     | Core API smoke tests   | bash + curl                     |
| `basic_grpc_test.sh`    | gRPC API validation    | bash + grpcurl                  |
| `shard-snapshot-api.sh` | Snapshot functionality | bash + curl                     |

Sources: [tests/integration-tests.sh1-76](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh#L1-L76) [.github/workflows/integration-tests.yml1-274](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L1-L274)

### Coverage Reporting

Coverage collection uses `cargo-llvm-cov` to instrument binaries and `lcov` to merge results:

```
```

Coverage reports are available at [Codecov dashboard](https://app.codecov.io/gh/qdrant/qdrant) showing per-file and per-function coverage.

Sources: [.github/workflows/coverage.yml1-112](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/coverage.yml#L1-L112) [docs/DEVELOPMENT.md156-177](https://github.com/qdrant/qdrant/blob/48203e41/docs/DEVELOPMENT.md#L156-L177)

---

## Release Process

Qdrant releases are triggered by pushing Git tags matching version patterns (e.g., `v1.2.3`).

### Release Artifact Matrix

```
```

### Docker Image Build Details

**Platform Support**

| Image Variant | Platforms                | Base Image                                |
| ------------- | ------------------------ | ----------------------------------------- |
| CPU           | linux/amd64, linux/arm64 | debian:13-slim                            |
| GPU NVIDIA    | linux/amd64              | nvidia/opengl:1.2-glvnd-devel-ubuntu22.04 |
| GPU AMD       | linux/amd64              | rocm/dev-ubuntu-22.04                     |
| Unprivileged  | linux/amd64, linux/arm64 | debian:13-slim (USER\_ID=1000)            |

**Build Command Template**

```
```

**SBOM and Provenance**

All Docker images include:

- SBOM (Software Bill of Materials) via `--sbom=true` [.github/workflows/docker-image.yml56](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L56-L56)
- Cosign signature for supply chain verification [.github/workflows/docker-image.yml62](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L62-L62)

### Binary Release Details

**Linux Targets**

| Target                       | Linking         | Use Case                           |
| ---------------------------- | --------------- | ---------------------------------- |
| `x86_64-unknown-linux-gnu`   | Dynamic (glibc) | Standard Linux systems             |
| `x86_64-unknown-linux-musl`  | Static          | Portable, Alpine Linux, containers |
| `aarch64-unknown-linux-musl` | Static          | ARM64 servers (e.g., AWS Graviton) |

**macOS Targets**

| Target                 | Architecture             |
| ---------------------- | ------------------------ |
| `x86_64-apple-darwin`  | Intel Macs               |
| `aarch64-apple-darwin` | Apple Silicon (M1/M2/M3) |

**Windows Target**

| Target                   | Toolchain            |
| ------------------------ | -------------------- |
| `x86_64-pc-windows-msvc` | MSVC (Visual Studio) |

### Debian Package Structure

Generated from `x86_64-unknown-linux-musl` build using `cargo-deb`:

```
Package: qdrant
Architecture: amd64
Depends: libc6
Description: Qdrant - High-performance vector similarity search engine

/usr/bin/qdrant
/var/lib/qdrant/storage/
/var/lib/qdrant/snapshots/
/var/lib/qdrant/static/
/etc/qdrant/config/
```

Configuration from [config/deb.yaml1-10](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml#L1-L10) sets default paths for system installation.

Sources: [.github/workflows/release-artifacts.yml50-64](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml#L50-L64) [config/deb.yaml1-10](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml#L1-L10)

### AppImage Bundle

The AppImage bundles:

- Qdrant binary
- Web UI static files
- Desktop integration metadata
- Custom AppRun launcher script

This creates a single executable file that works on any Linux distribution without installation.

Sources: [.github/workflows/release-artifacts.yml117-177](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml#L117-L177)

---

## Build Optimization Techniques

### Cargo-Chef Layer Caching

Traditional Docker builds invalidate all layers when source code changes. Cargo-chef separates dependency compilation from source compilation:

```
```

**Cache layers**:

1. `recipe.json` changes only when dependencies change
2. `cargo chef cook` layer cached until dependencies change
3. Source code changes only invalidate final build step

This typically reduces Docker build time from \~30min to \~5min for code-only changes.

Sources: [Dockerfile22-25](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L22-L25) [Dockerfile96-104](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L96-L104)

### Linker Selection

Qdrant supports three linkers via `LINKER` build arg:

| Linker    | Speed                          | Default |
| --------- | ------------------------------ | ------- |
| `mold`    | Fastest (2-3x faster than lld) | ✓       |
| `lld`     | Fast                           |         |
| (default) | Slower                         |         |

The mold linker is downloaded during build [Dockerfile52-66](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L52-L66) and added to PATH [Dockerfile102](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L102-L102)

### Rust Cache in GitHub Actions

All workflows use `Swatinem/rust-cache@v2` to cache:

- `~/.cargo/registry` - crate registry index and downloads
- `~/.cargo/git` - git dependencies
- `target/` - compiled artifacts

**Cache key configuration**:

```
```

The `shared-key` parameter allows multiple jobs to share the same cache, reducing redundant compilations.

Sources: [.github/workflows/rust.yml23](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L23-L23) [.github/workflows/integration-tests.yml26-28](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L26-L28)

---

## Continuous Integration Summary

**Workflow Trigger Matrix**

| Workflow              | Trigger         | Duration    | Purpose               |
| --------------------- | --------------- | ----------- | --------------------- |
| rust.yml              | Every push/PR   | \~10-15 min | Unit tests on 3 OS    |
| rust-lint.yml         | Every push/PR   | \~3-5 min   | Code quality checks   |
| integration-tests.yml | Every push/PR   | \~20-30 min | API + consensus tests |
| storage-compat.yml    | Every push/PR   | \~5-10 min  | Version migration     |
| coverage.yml          | Daily cron      | \~30-40 min | Coverage reporting    |
| rust-gpu.yml          | Manual          | \~15-20 min | GPU functionality     |
| docker-image.yml      | Tag push        | \~60-90 min | Multi-platform images |
| release-artifacts.yml | Release publish | \~45-60 min | Binary artifacts      |

**Test Execution Flow**

```
```

Sources: All workflow files in [.github/workflows/](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Building and CI/CD](#building-and-cicd.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Docker Multi-Stage Build Architecture](#docker-multi-stage-build-architecture.md)
- [Stage 1: Dependency Planning](#stage-1-dependency-planning.md)
- [Stage 2: Builder](#stage-2-builder.md)
- [Stage 3: Base Image Selection](#stage-3-base-image-selection.md)
- [Stage 4: Final Runtime Image](#stage-4-final-runtime-image.md)
- [GitHub Actions Workflows](#github-actions-workflows.md)
- [rust.yml - Core Test Suite](#rustyml---core-test-suite.md)
- [integration-tests.yml - Integration Testing](#integration-testsyml---integration-testing.md)
- [rust-lint.yml - Code Quality](#rust-lintyml---code-quality.md)
- [coverage.yml - Code Coverage](#coverageyml---code-coverage.md)
- [docker-image.yml - Container Image Publishing](#docker-imageyml---container-image-publishing.md)
- [release-artifacts.yml - Binary Releases](#release-artifactsyml---binary-releases.md)
- [storage-compat.yml - Version Compatibility](#storage-compatyml---version-compatibility.md)
- [rust-gpu.yml - GPU Functionality](#rust-gpuyml---gpu-functionality.md)
- [Testing Infrastructure](#testing-infrastructure.md)
- [Nextest Configuration](#nextest-configuration.md)
- [Integration Test Script](#integration-test-script.md)
- [Coverage Reporting](#coverage-reporting.md)
- [Release Process](#release-process.md)
- [Release Artifact Matrix](#release-artifact-matrix.md)
- [Docker Image Build Details](#docker-image-build-details.md)
- [Binary Release Details](#binary-release-details.md)
- [Debian Package Structure](#debian-package-structure.md)
- [AppImage Bundle](#appimage-bundle.md)
- [Build Optimization Techniques](#build-optimization-techniques.md)
- [Cargo-Chef Layer Caching](#cargo-chef-layer-caching.md)
- [Linker Selection](#linker-selection.md)
- [Rust Cache in GitHub Actions](#rust-cache-in-github-actions.md)
- [Continuous Integration Summary](#continuous-integration-summary.md)
