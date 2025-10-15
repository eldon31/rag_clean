Docker Deployment | qdrant/qdrant | DeepWiki

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

# Docker Deployment

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
- [config/deb.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml)
- [tests/integration-tests.sh](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh)
- [tools/sync-web-ui.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/sync-web-ui.sh)

This page describes the Docker build system, image variants, build configuration, and deployment workflows for Qdrant. It covers the multi-stage Dockerfile architecture, build arguments, image variants (CPU/GPU), cross-compilation support, and CI/CD integration.

For information about configuration options that can be set via environment variables, see [Configuration System](qdrant/qdrant/10.1-configuration-system.md). For details on the CI/CD workflows and build artifacts, see [Building and CI/CD](qdrant/qdrant/10.3-building-and-cicd.md).

---

## Multi-Stage Build Architecture

The Dockerfile implements a multi-stage build process optimized for Docker layer caching and cross-platform compilation. The build consists of three primary stages and conditional GPU-specific base images.

```
```

**Sources:** [Dockerfile1-231](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L1-L231)

### Planner Stage

The planner stage uses `cargo-chef` to analyze dependencies and generate a recipe file. This enables Docker to cache dependency builds separately from application code.

```
```

**Sources:** [Dockerfile22-25](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L22-L25)

### Builder Stage

The builder stage performs the actual compilation with support for cross-compilation, custom linkers, and multiple build profiles. It consists of several distinct phases:

1. **Dependency Installation** - System packages and Rust components
2. **Mold Linker Setup** - Fast linker for reduced build times
3. **Cross-compilation Setup** - Platform-specific toolchains via `xx`
4. **Web UI Download** - Static assets from qdrant-web-ui repository
5. **Dependency Compilation** - Using cargo-chef recipe
6. **Application Compilation** - Final Qdrant binary
7. **SBOM Generation** - Software Bill of Materials

```
```

**Sources:** [Dockerfile28-122](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L28-L122)

---

## Build Arguments and Configuration

The Dockerfile accepts multiple build arguments that control compilation behavior, features, and target architecture.

| Argument         | Default       | Purpose                    | Usage                                 |
| ---------------- | ------------- | -------------------------- | ------------------------------------- |
| `BUILDPLATFORM`  | `linux/amd64` | Host platform for build    | Set by Docker buildx                  |
| `TARGETPLATFORM` | `linux/amd64` | Target platform for binary | Set by Docker buildx                  |
| `PROFILE`        | `release`     | Cargo build profile        | `release`, `dev`, or `ci`             |
| `FEATURES`       | (none)        | Cargo feature flags        | Comma-separated list                  |
| `RUSTFLAGS`      | (none)        | Custom Rust compiler flags | E.g., `--cfg tokio_unstable`          |
| `LINKER`         | `mold`        | Linker to use              | `mold`, `lld`, or empty               |
| `GPU`            | (none)        | GPU support variant        | `nvidia` or `amd`                     |
| `GIT_COMMIT_ID`  | (none)        | Git commit hash            | Embedded in binary                    |
| `USER_ID`        | `0`           | Runtime user ID            | `0` for root, `1000` for unprivileged |
| `PACKAGES`       | (none)        | Additional apt packages    | E.g., `gdb lldb`                      |
| `SOURCES`        | (none)        | Include source code        | Any non-empty value                   |

### Build Profile Selection

The `PROFILE` argument determines the optimization level and debug information:

```
```

**Sources:** [Dockerfile76-77](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L76-L77)

### Feature Flag Configuration

Features are enabled via the `FEATURES` argument and combined with mandatory features:

```
```

The build always includes the `stacktrace` feature for better error diagnostics.

**Sources:** [Dockerfile79-104](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L79-L104) [Dockerfile113-118](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L113-L118)

### Linker Configuration

The build supports multiple linkers for optimization:

```
```

The linker is set via `RUSTFLAGS` during compilation:

```
RUSTFLAGS="${LINKER:+-C link-arg=-fuse-ld=}$LINKER $RUSTFLAGS"
```

**Sources:** [Dockerfile85-86](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L85-L86) [Dockerfile101-104](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L101-L104) [Dockerfile113-116](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L113-L116)

---

## Image Variants

Qdrant provides multiple Docker image variants to support different hardware and security requirements.

```
```

### CPU Variant (Default)

The default image uses `debian:13-slim` as the base, minimizing image size while providing necessary runtime libraries.

**Base Image:** `debian:13-slim`

**Installed Packages:**

- `ca-certificates` - SSL/TLS certificates
- `tzdata` - Timezone data
- `libunwind8` - Stack unwinding support

**Image Name Pattern:** `qdrant/qdrant:{version}`

**Sources:** [Dockerfile126-128](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L126-L128)

### GPU NVIDIA Variant

For NVIDIA GPU acceleration, the image uses `nvidia/opengl:1.2-glvnd-devel-ubuntu22.04` as the base.

**Base Image:** `nvidia/opengl:1.2-glvnd-devel-ubuntu22.04`

**Environment Variables:**

- `NVIDIA_DRIVER_CAPABILITIES=compute,graphics,utility` - Enables compute and graphics capabilities
- `DEBIAN_FRONTEND=noninteractive` - Non-interactive apt-get

**Additional Files:**

- `/etc/vulkan/icd.d/nvidia_icd.json` - Vulkan ICD loader configuration

**Installed GPU Packages:**

- `libvulkan1`, `libvulkan-dev` - Vulkan runtime and development files
- `vulkan-tools` - Vulkan utilities

**Image Name Pattern:** `qdrant/qdrant:{version}-gpu-nvidia`

**Sources:** [Dockerfile130-140](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L130-L140) [Dockerfile152-161](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L152-L161)

### GPU AMD Variant

For AMD GPU acceleration, the image uses `rocm/dev-ubuntu-22.04` as the base.

**Base Image:** `rocm/dev-ubuntu-22.04`

**Environment Variables:**

- `DEBIAN_FRONTEND=noninteractive` - Non-interactive apt-get

**Installed GPU Packages:**

- Same Vulkan packages as NVIDIA variant

**Image Name Pattern:** `qdrant/qdrant:{version}-gpu-amd`

**Sources:** [Dockerfile142-148](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L142-L148) [Dockerfile152-161](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L152-L161)

### Unprivileged Variant

Security-hardened variant that runs as a non-root user with UID 1000.

**Build Configuration:**

```
```

**Runtime User:** `qdrant:qdrant` (UID/GID 1000)

**Pre-created Directories:**

- `/qdrant/storage` - Data storage directory
- `/qdrant/snapshots` - Snapshot directory

**Image Name Pattern:** `qdrant/qdrant:{version}-unprivileged`

**Sources:** [Dockerfile198-215](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L198-L215) [.github/workflows/docker-image.yml64-79](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L64-L79)

---

## Cross-Platform Compilation

The Docker build system supports multi-platform builds using Docker Buildx and the `xx` cross-compilation toolkit.

```
```

### Platform-Specific Toolchain Setup

The build uses `xx-apt-get` to install platform-specific development dependencies:

```
```

This installs cross-compilation toolchains for the target platform specified by `TARGETPLATFORM`.

**Sources:** [Dockerfile71-74](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L71-L74)

### Cross-Compilation Wrapper

The `xx-cargo` wrapper automatically configures Cargo for cross-compilation:

```
```

The `PKG_CONFIG` workaround addresses a bug in `xx-cargo` for crates using `pkg-config`.

**Sources:** [Dockerfile96-104](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L96-L104) [Dockerfile109-118](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L109-L118)

### Mold Linker Platform Support

The Mold linker is installed with platform-specific binaries:

```
```

**Supported Platforms:**

- `x86_64-linux` (amd64)
- `aarch64-linux` (arm64)

**Sources:** [Dockerfile52-66](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L52-L66)

---

## Layer Caching Strategy

The build implements cargo-chef for efficient Docker layer caching, significantly reducing rebuild times when only application code changes.

```
```

### Recipe Generation

The planner analyzes `Cargo.toml` and `Cargo.lock` files to generate a dependency recipe:

```
```

**Sources:** [Dockerfile22-25](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L22-L25)

### Dependency Cooking

The builder uses the recipe to compile dependencies before copying application code:

```
```

This layer is cached and only invalidated when dependencies change.

**Sources:** [Dockerfile96-104](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L96-L104)

### Application Build

After dependencies are built, application code is copied and compiled:

```
```

Only this layer needs rebuilding when application code changes.

**Sources:** [Dockerfile106-118](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L106-L118)

---

## Web UI Integration

The Docker build includes the Qdrant web UI by downloading the latest release from the qdrant-web-ui repository.

```
```

### Download Process

The `sync-web-ui.sh` script fetches the latest web UI bundle:

```
```

**Sources:** [tools/sync-web-ui.sh1-27](https://github.com/qdrant/qdrant/blob/48203e41/tools/sync-web-ui.sh#L1-L27)

### Build Integration

The Dockerfile invokes the sync script during the builder stage:

```
```

**Sources:** [Dockerfile92-94](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L92-L94)

### Runtime Deployment

Static files are copied to the final image:

```
```

The web UI is served at the root path `/` on the HTTP API port (6333).

**Sources:** [Dockerfile211](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L211-L211)

---

## Runtime Configuration

The final Docker image exposes standard ports, sets environment variables, and defines the entrypoint for container execution.

### Exposed Ports

| Port | Protocol  | Purpose                           |
| ---- | --------- | --------------------------------- |
| 6333 | HTTP/gRPC | REST API and gRPC API             |
| 6334 | gRPC      | Internal gRPC (P2P communication) |

**Sources:** [Dockerfile220-221](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L220-L221)

### Environment Variables

| Variable   | Default      | Purpose            |
| ---------- | ------------ | ------------------ |
| `TZ`       | `Etc/UTC`    | Container timezone |
| `RUN_MODE` | `production` | Runtime mode       |

Additional configuration can be set via `QDRANT__*` environment variables (see [Configuration System](qdrant/qdrant/10.1-configuration-system.md)).

**Sources:** [Dockerfile217-218](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L217-L218)

### File System Layout

```
/qdrant/
├── qdrant              # Binary executable
├── qdrant.spdx.json    # Software Bill of Materials
├── config/             # Configuration files
├── static/             # Web UI static files
├── entrypoint.sh       # Container entrypoint
├── storage/            # Data directory (volume mount)
└── snapshots/          # Snapshot directory (volume mount)
```

**Sources:** [Dockerfile196-213](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L196-L213)

### Entrypoint Script

The container executes via `entrypoint.sh`:

```
```

This script is located at [tools/entrypoint.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/entrypoint.sh) and handles initialization before starting the Qdrant process.

**Sources:** [Dockerfile210](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L210-L210) [Dockerfile230](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L230-L230)

### User Configuration

The image supports two user modes:

**Root Mode (USER\_ID=0, default):**

- Runs as root user
- No pre-created directories
- Maximum flexibility for volume mounting

**Unprivileged Mode (USER\_ID=1000):**

- Runs as `qdrant:qdrant` user (UID/GID 1000)
- Pre-created `storage` and `snapshots` directories
- Enhanced security posture

**Sources:** [Dockerfile198-215](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L198-L215)

---

## CI/CD Integration

Qdrant's Docker images are built and deployed through GitHub Actions workflows that handle multi-platform builds, tagging strategies, and image signing.

```
```

### Multi-Platform Build Configuration

The CPU build targets multiple platforms using Docker Buildx:

```
```

GPU builds are limited to `linux/amd64` due to GPU driver compatibility.

**Sources:** [.github/workflows/docker-image.yml38-62](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L38-L62) [.github/workflows/docker-image.yml108-148](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L108-L148)

### Tag Generation Strategy

For a release tag like `v1.2.3`, the workflow generates multiple tags:

| Tag Pattern   | Example                | Purpose       |
| ------------- | ---------------------- | ------------- |
| Full version  | `qdrant/qdrant:v1.2.3` | Exact release |
| Minor version | `qdrant/qdrant:1.2`    | Latest patch  |
| Major version | `qdrant/qdrant:1`      | Latest minor  |
| Latest        | `qdrant/qdrant:latest` | Latest stable |

**Version Extraction:**

```
```

**Sources:** [.github/workflows/docker-image.yml26-37](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L26-L37) [.github/workflows/docker-image.yml95-106](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L95-L106)

### Image Registries

Images are pushed to two registries:

1. **Docker Hub:** `qdrant/qdrant:{tag}`
2. **GitHub Packages:** `docker.pkg.github.com/qdrant/qdrant/qdrant:{tag}`

**Sources:** [.github/workflows/docker-image.yml44-59](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L44-L59) [.github/workflows/docker-image.yml113-128](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L113-L128)

### Image Signing with Cosign

All published images are signed using Sigstore Cosign with keyless OIDC signing:

```
```

This enables verification of image authenticity without managing signing keys.

**Sources:** [.github/workflows/docker-image.yml61-62](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L61-L62) [.github/workflows/docker-image.yml130-131](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L130-L131)

### SBOM Generation

Software Bill of Materials (SBOM) is generated during build:

```
```

The SBOM is included in the final image at `/qdrant/qdrant.spdx.json` and also embedded in the image metadata:

```
```

**Sources:** [Dockerfile120-121](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L120-L121) [Dockerfile208](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L208-L208) [.github/workflows/docker-image.yml56](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L56-L56)

### Testing Integration

Docker builds are tested in CI through multiple workflows:

**Consensus Testing:**

```
```

**E2E Testing:**

```
```

**Sources:** [.github/workflows/integration-tests.yml101-117](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L101-L117) [.github/workflows/integration-tests.yml238-265](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L238-L265)

### Cache Strategy

GitHub Actions cache is used to speed up builds:

```
```

This creates separate cache scopes per branch while allowing fallback to base branch cache.

**Sources:** [.github/workflows/integration-tests.yml108-111](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L108-L111)

---

## Development and Debugging Support

The Docker build supports optional features for debugging and development workflows.

### Source Code Inclusion

Source files can be included in the image for debugging:

```
```

This copies the following directories:

- `/qdrant/src` - Application source
- `/qdrant/lib` - Library source
- `/usr/local/cargo/registry/src` - Crate sources
- `/usr/local/cargo/git/checkouts` - Git dependencies

The conditional copy uses parameter expansion to work around Dockerfile limitations:

```
```

**Sources:** [Dockerfile172-194](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L172-L194)

### Debug Tools Installation

Additional debugging packages can be installed:

```
```

These packages are installed in the final image alongside base dependencies.

**Sources:** [Dockerfile163-170](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L163-L170)

### Build Profile for CI

The `ci` build profile balances build time and binary size for CI environments:

```
```

This profile is defined in `.cargo/config.toml` and used by integration tests.

**Sources:** [.github/workflows/integration-tests.yml114](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L114-L114) [.github/workflows/integration-tests.yml259](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L259-L259)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Docker Deployment](#docker-deployment.md)
- [Multi-Stage Build Architecture](#multi-stage-build-architecture.md)
- [Planner Stage](#planner-stage.md)
- [Builder Stage](#builder-stage.md)
- [Build Arguments and Configuration](#build-arguments-and-configuration.md)
- [Build Profile Selection](#build-profile-selection.md)
- [Feature Flag Configuration](#feature-flag-configuration.md)
- [Linker Configuration](#linker-configuration.md)
- [Image Variants](#image-variants.md)
- [CPU Variant (Default)](#cpu-variant-default.md)
- [GPU NVIDIA Variant](#gpu-nvidia-variant.md)
- [GPU AMD Variant](#gpu-amd-variant.md)
- [Unprivileged Variant](#unprivileged-variant.md)
- [Cross-Platform Compilation](#cross-platform-compilation.md)
- [Platform-Specific Toolchain Setup](#platform-specific-toolchain-setup.md)
- [Cross-Compilation Wrapper](#cross-compilation-wrapper.md)
- [Mold Linker Platform Support](#mold-linker-platform-support.md)
- [Layer Caching Strategy](#layer-caching-strategy.md)
- [Recipe Generation](#recipe-generation.md)
- [Dependency Cooking](#dependency-cooking.md)
- [Application Build](#application-build.md)
- [Web UI Integration](#web-ui-integration.md)
- [Download Process](#download-process.md)
- [Build Integration](#build-integration.md)
- [Runtime Deployment](#runtime-deployment.md)
- [Runtime Configuration](#runtime-configuration.md)
- [Exposed Ports](#exposed-ports.md)
- [Environment Variables](#environment-variables.md)
- [File System Layout](#file-system-layout.md)
- [Entrypoint Script](#entrypoint-script.md)
- [User Configuration](#user-configuration.md)
- [CI/CD Integration](#cicd-integration.md)
- [Multi-Platform Build Configuration](#multi-platform-build-configuration.md)
- [Tag Generation Strategy](#tag-generation-strategy.md)
- [Image Registries](#image-registries.md)
- [Image Signing with Cosign](#image-signing-with-cosign.md)
- [SBOM Generation](#sbom-generation.md)
- [Testing Integration](#testing-integration.md)
- [Cache Strategy](#cache-strategy.md)
- [Development and Debugging Support](#development-and-debugging-support.md)
- [Source Code Inclusion](#source-code-inclusion.md)
- [Debug Tools Installation](#debug-tools-installation.md)
- [Build Profile for CI](#build-profile-for-ci.md)
