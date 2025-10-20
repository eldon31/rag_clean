Configuration and Deployment | qdrant/qdrant | DeepWiki

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

# Configuration and Deployment

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
- [config/config.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml)
- [config/deb.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml)
- [lib/collection/src/common/snapshots\_manager.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/common/snapshots_manager.rs)
- [lib/collection/src/operations/shared\_storage\_config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs)
- [lib/storage/src/content\_manager/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/content_manager/mod.rs)
- [lib/storage/src/types.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs)
- [src/actix/api/cluster\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/cluster_api.rs)
- [src/actix/api/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/api/mod.rs)
- [src/actix/certificate\_helpers.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/certificate_helpers.rs)
- [src/actix/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs)
- [src/common/helpers.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs)
- [src/common/http\_client.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/common/http_client.rs)
- [src/consensus.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs)
- [src/main.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs)
- [src/settings.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs)
- [src/tonic/api/raft\_api.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/api/raft_api.rs)
- [src/tonic/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs)
- [tests/integration-tests.sh](https://github.com/qdrant/qdrant/blob/48203e41/tests/integration-tests.sh)
- [tools/sync-web-ui.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/sync-web-ui.sh)

This document covers the configuration system and deployment options for Qdrant. It explains how configuration is loaded, structured, and applied at runtime, as well as the various deployment modes and container build processes.

For detailed information about specific aspects:

- Configuration file structure and environment variables: see [Configuration System](qdrant/qdrant/10.1-configuration-system.md)
- Docker images and containerization: see [Docker Deployment](qdrant/qdrant/10.2-docker-deployment.md)
- Build process and CI/CD workflows: see [Building and CI/CD](qdrant/qdrant/10.3-building-and-cicd.md)

For information about distributed cluster setup and consensus, see [Raft Consensus Protocol](qdrant/qdrant/7.1-raft-consensus-protocol.md) and [Distributed System Features](qdrant/qdrant/7-distributed-system-features.md).

---

## Configuration Overview

Qdrant uses a hierarchical YAML-based configuration system with support for environment variable overrides. Configuration is loaded at startup via the `Settings` structure and controls all aspects of the service including storage, API endpoints, cluster behavior, and TLS settings.

### Configuration Loading Flow

```
```

**Sources:** [src/settings.rs230-285](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L230-L285) [src/main.rs140-152](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L140-L152)

### Core Configuration Structures

The configuration system is organized into several major components, each represented by a Rust struct:

| Configuration Component | Struct              | Purpose                                   |
| ----------------------- | ------------------- | ----------------------------------------- |
| Root Configuration      | `Settings`          | Top-level settings container              |
| Storage Settings        | `StorageConfig`     | Data storage paths, WAL, optimizers, HNSW |
| Service Settings        | `ServiceConfig`     | HTTP/gRPC ports, TLS, API keys, CORS      |
| Cluster Settings        | `ClusterConfig`     | Distributed mode, peer ID, consensus      |
| P2P Settings            | `P2pConfig`         | Internal port, connection pool, TLS       |
| Consensus Settings      | `ConsensusConfig`   | Raft tick period, WAL compaction          |
| TLS Settings            | `TlsConfig`         | Certificate paths, TTL                    |
| Performance Settings    | `PerformanceConfig` | Thread counts, rate limits                |

**Sources:** [src/settings.rs197-227](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L197-L227) [lib/storage/src/types.rs62-114](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L62-L114)

### Configuration-to-Code Mapping

```
```

**Sources:** [src/settings.rs22-60](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L22-L60) [src/main.rs365-374](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L365-L374) [src/actix/mod.rs55-61](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L61) [src/tonic/mod.rs147-153](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L153)

---

## Deployment Modes

Qdrant supports two primary deployment modes: **standalone** and **distributed**. The mode is determined by the `cluster.enabled` configuration setting.

### Standalone Mode

In standalone mode, Qdrant runs as a single node without distributed consensus. All operations are handled locally.

```
```

**Configuration:**

- `cluster.enabled: false` (default)
- No consensus or peer communication
- Simpler deployment, lower latency

**Sources:** [src/main.rs392-393](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L392-L393) [config/config.yaml301-303](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L301-L303)

### Distributed Mode

In distributed mode, Qdrant runs as part of a cluster with Raft consensus for metadata operations. Data is sharded and replicated across peers.

```
```

**Configuration:**

- `cluster.enabled: true`
- `cluster.peer_id`: Unique peer identifier
- `cluster.p2p.port`: Internal communication port (default 6335)
- `--uri` and `--bootstrap` CLI arguments for cluster formation

**Sources:** [src/main.rs395-406](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L395-L406) [src/consensus.rs63-94](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L63-L94) [config/config.yaml301-327](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L301-L327)

### Cluster Initialization

The cluster initialization process differs for the first peer versus subsequent peers:

```
```

**Sources:** [src/consensus.rs286-322](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L286-L322) [src/consensus.rs426-462](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L426-L462) [src/main.rs261-278](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L261-L278)

---

## Runtime Initialization

The application startup sequence initializes multiple runtime components and threads:

```
```

**Sources:** [src/main.rs307-374](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L307-L374) [src/main.rs431-447](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L431-L447) [src/main.rs549-594](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L549-L594)

### Thread Configuration

Qdrant creates dedicated thread pools for different workloads:

| Runtime          | Builder Function                   | Thread Naming   | Purpose                                     |
| ---------------- | ---------------------------------- | --------------- | ------------------------------------------- |
| Search Runtime   | `create_search_runtime()`          | `search-{id}`   | Vector search operations                    |
| Update Runtime   | `create_update_runtime()`          | `update-{id}`   | Background optimizations                    |
| General Runtime  | `create_general_purpose_runtime()` | `general-{id}`  | General async tasks                         |
| Consensus Thread | `Consensus::run()`                 | `consensus`     | Raft state machine (high priority on Linux) |
| REST Server      | `actix::init()`                    | `web`           | REST API handling                           |
| gRPC Server      | `tonic::init()`                    | `grpc`          | gRPC API handling                           |
| Internal gRPC    | `tonic::init_internal()`           | `grpc_internal` | Peer-to-peer communication                  |

**Sources:** [src/common/helpers.rs20-63](https://github.com/qdrant/qdrant/blob/48203e41/src/common/helpers.rs#L20-L63) [src/main.rs309-322](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L309-L322) [src/consensus.rs96-115](https://github.com/qdrant/qdrant/blob/48203e41/src/consensus.rs#L96-L115)

---

## API Server Configuration

Both REST and gRPC servers support TLS, authentication, and various protocol-specific options.

### REST API (Actix-web)

The REST API is implemented using Actix-web and supports:

- CORS (configurable via `service.enable_cors`)
- TLS with certificate rotation (`service.enable_tls`, `tls.cert_ttl`)
- API key authentication (`service.api_key`, `service.read_only_api_key`)
- JWT RBAC (`service.jwt_rbac`)
- Request size limits (`service.max_request_size_mb`)
- Worker threads (`service.max_workers`)

**TLS Configuration with Certificate Rotation:**

```
```

**Sources:** [src/actix/mod.rs55-205](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/mod.rs#L55-L205) [src/actix/certificate\_helpers.rs19-75](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/certificate_helpers.rs#L19-L75) [config/config.yaml234-275](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L234-L275)

### gRPC API (Tonic)

The gRPC API is implemented using Tonic and supports:

- Compression (Gzip encoding for all services)
- TLS (`service.enable_tls`)
- API key authentication (shared with REST)
- Unlimited message sizes (`max_decoding_message_size(usize::MAX)`)
- Service reflection for development

**Services Exposed:**

| Service                 | Proto Definition    | Description                |
| ----------------------- | ------------------- | -------------------------- |
| `qdrant.Qdrant`         | `QdrantServer`      | Health check endpoint      |
| `qdrant.Collections`    | `CollectionsServer` | Collection management      |
| `qdrant.Points`         | `PointsServer`      | Point operations           |
| `qdrant.Snapshots`      | `SnapshotsServer`   | Snapshot management        |
| `grpc.health.v1.Health` | `HealthServer`      | Standard gRPC health check |

**Internal gRPC Services (distributed mode only):**

| Service                      | Proto Definition            | Purpose                 |
| ---------------------------- | --------------------------- | ----------------------- |
| `qdrant.Raft`                | `RaftServer`                | Raft message passing    |
| `qdrant.QdrantInternal`      | `QdrantInternalServer`      | Consensus state queries |
| `qdrant.CollectionsInternal` | `CollectionsInternalServer` | Internal collection ops |
| `qdrant.PointsInternal`      | `PointsInternalServer`      | Internal point ops      |
| `qdrant.ShardSnapshots`      | `ShardSnapshotsServer`      | Shard snapshot transfer |

**Sources:** [src/tonic/mod.rs147-253](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L147-L253) [src/tonic/mod.rs256-360](https://github.com/qdrant/qdrant/blob/48203e41/src/tonic/mod.rs#L256-L360)

---

## Environment Variables

All configuration options can be overridden using environment variables with the `QDRANT__` prefix and double underscores for nested fields.

### Common Environment Variable Patterns

```
```

**Sources:** [src/settings.rs278-280](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L278-L280) [.github/workflows/integration-tests.yml198-203](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L198-L203)

### CLI Arguments

Key command-line arguments for deployment:

| Argument                  | Environment Variable | Purpose                            |
| ------------------------- | -------------------- | ---------------------------------- |
| `--config-path PATH`      | N/A                  | Path to custom config file         |
| `--uri URI`               | `QDRANT_URI`         | This peer's URI for cluster        |
| `--bootstrap URI`         | `QDRANT_BOOTSTRAP`   | Bootstrap from existing peer       |
| `--snapshot PATH:NAME`    | N/A                  | Recover from collection snapshot   |
| `--storage-snapshot PATH` | N/A                  | Recover from full storage snapshot |
| `--disable-telemetry`     | N/A                  | Disable usage telemetry            |
| `--reinit`                | N/A                  | Reinitialize consensus state       |

**Sources:** [src/main.rs72-138](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L72-L138) [src/main.rs261-305](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L261-L305)

---

## Docker Deployment

Qdrant provides multi-architecture Docker images with support for CPU and GPU variants. The Docker build process uses multi-stage builds for optimization.

### Image Variants

| Image Tag Pattern                   | Architecture | Features                         |
| ----------------------------------- | ------------ | -------------------------------- |
| `qdrant/qdrant:latest`              | amd64, arm64 | Standard CPU build               |
| `qdrant/qdrant:latest-unprivileged` | amd64, arm64 | Runs as non-root user (UID 1000) |
| `qdrant/qdrant:latest-gpu-nvidia`   | amd64        | NVIDIA GPU support               |
| `qdrant/qdrant:latest-gpu-amd`      | amd64        | AMD GPU support                  |

### Multi-Stage Build Process

```
```

**Sources:** [Dockerfile10-230](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L10-L230)

### Build Arguments

The Docker build supports various build arguments:

| Build Arg       | Default   | Purpose                                      |
| --------------- | --------- | -------------------------------------------- |
| `GPU`           | (none)    | Set to `nvidia` or `amd` for GPU support     |
| `PROFILE`       | `release` | Cargo build profile (`release`, `dev`, `ci`) |
| `FEATURES`      | (none)    | Additional Cargo features to enable          |
| `RUSTFLAGS`     | (none)    | Custom Rust compiler flags                   |
| `LINKER`        | `mold`    | Linker to use (`mold`, `lld`, or empty)      |
| `USER_ID`       | `0`       | User ID for unprivileged images              |
| `PACKAGES`      | (none)    | Additional apt packages to install           |
| `SOURCES`       | (none)    | Include source files for debugging           |
| `GIT_COMMIT_ID` | (none)    | Embed git commit hash in binary              |

**Sources:** [Dockerfile76-109](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L76-L109) [.github/workflows/docker-image.yml48-56](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L48-L56)

### Container Ports

The container exposes two ports by default:

```
```

In distributed mode, port 6335 is used internally for peer-to-peer communication (not exposed by default).

**Sources:** [Dockerfile220-221](https://github.com/qdrant/qdrant/blob/48203e41/Dockerfile#L220-L221)

### Volume Mounts

Recommended volume mounts for persistent data:

```
```

**Sources:** [config/config.yaml17-22](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L17-L22)

---

## Build System and CI/CD

Qdrant uses GitHub Actions for continuous integration and release automation.

### Key CI Workflows

```
```

**Sources:** [.github/workflows/rust.yml12-50](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust.yml#L12-L50) [.github/workflows/integration-tests.yml14-84](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L14-L84) [.github/workflows/rust-lint.yml13-45](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-lint.yml#L13-L45)

### Release Process

The release workflow is triggered on git tags:

```
```

**Sources:** [.github/workflows/docker-image.yml10-148](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/docker-image.yml#L10-L148) [.github/workflows/release-artifacts.yml9-177](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/release-artifacts.yml#L9-L177)

### Cargo Features

The codebase supports various Cargo features for conditional compilation:

| Feature                  | Purpose                                   | Used In              |
| ------------------------ | ----------------------------------------- | -------------------- |
| `service_debug`          | Enable deadlock detection and debugging   | Integration tests    |
| `data-consistency-check` | Enable additional consistency checks      | Integration tests    |
| `stacktrace`             | Enable stacktrace collector for debugging | Runtime flag         |
| `gpu`                    | Enable GPU support (NVIDIA/AMD)           | GPU builds           |
| `deb`                    | Include Debian package paths              | Debian package build |

**Sources:** [.github/workflows/integration-tests.yml40](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L40-L40) [.github/workflows/rust-gpu.yml35](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/rust-gpu.yml#L35-L35) [src/main.rs59-64](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L59-L64)

---

## Storage Paths and Directories

Qdrant uses several directories for different purposes:

```
```

**Default Paths:**

- Storage: `./storage` (configurable via `storage.storage_path`)
- Snapshots: `./snapshots` (configurable via `storage.snapshots_path`)
- Temp: `./storage/snapshots_temp/` (configurable via `storage.temp_path`)
- Static: `./static` (configurable via `service.static_content_dir`)

**Debian Package Paths:**

- Storage: `/var/lib/qdrant/storage`
- Snapshots: `/var/lib/qdrant/snapshots`
- Static: `/var/lib/qdrant/static`
- Config: `/etc/qdrant/config.yaml`

**Sources:** [config/config.yaml17-35](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L17-L35) [config/deb.yaml1-9](https://github.com/qdrant/qdrant/blob/48203e41/config/deb.yaml#L1-L9) [lib/storage/src/types.rs139-141](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L139-L141)

---

## Performance Tuning

Key configuration parameters for performance tuning:

### Thread Pool Configuration

```
```

**Sources:** [config/config.yaml64-78](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L64-L78) [lib/storage/src/types.rs28-55](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L28-L55)

### Memory Management

```
```

**Sources:** [config/config.yaml37-43](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L37-L43) [config/config.yaml172-174](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L172-L174) [lib/storage/src/types.rs89-90](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L89-L90)

### Shard Transfer Limits

```
```

**Sources:** [config/config.yaml80-90](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L80-L90) [lib/collection/src/operations/shared\_storage\_config.rs16](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs#L16-L16)

---

## Security Configuration

### TLS Setup

TLS can be enabled for both external APIs and internal cluster communication:

```
```

**Certificate Rotation:**

- Supported for REST API only (not gRPC or internal communication)
- Certificates are reloaded from disk when TTL expires
- If reload fails, old certificate is retained with error logged

**Sources:** [config/config.yaml259-354](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L259-L354) [src/actix/certificate\_helpers.rs33-68](https://github.com/qdrant/qdrant/blob/48203e41/src/actix/certificate_helpers.rs#L33-L68)

### Authentication

```
```

**JWT RBAC Notes:**

- Uses `api_key` as JWT secret (minimum 32 bytes recommended)
- Enables fine-grained access control
- Generates tokens via API with custom permissions

**Sources:** [config/config.yaml266-291](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L266-L291) [src/settings.rs298-325](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L298-L325)

---

## Snapshot Storage Configuration

Qdrant supports local and S3-compatible snapshot storage:

### Local Snapshot Storage

```
```

### S3 Snapshot Storage

```
```

**Environment Variable Override:**

```
```

**Sources:** [lib/collection/src/common/snapshots\_manager.rs18-39](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/common/snapshots_manager.rs#L18-L39) [.github/workflows/integration-tests.yml198-203](https://github.com/qdrant/qdrant/blob/48203e41/.github/workflows/integration-tests.yml#L198-L203)

---

This page provides an overview of Qdrant's configuration and deployment capabilities. For detailed information about specific aspects, refer to the sub-pages: [Configuration System](qdrant/qdrant/10.1-configuration-system.md), [Docker Deployment](qdrant/qdrant/10.2-docker-deployment.md), and [Building and CI/CD](qdrant/qdrant/10.3-building-and-cicd.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Configuration and Deployment](#configuration-and-deployment.md)
- [Configuration Overview](#configuration-overview.md)
- [Configuration Loading Flow](#configuration-loading-flow.md)
- [Core Configuration Structures](#core-configuration-structures.md)
- [Configuration-to-Code Mapping](#configuration-to-code-mapping.md)
- [Deployment Modes](#deployment-modes.md)
- [Standalone Mode](#standalone-mode.md)
- [Distributed Mode](#distributed-mode.md)
- [Cluster Initialization](#cluster-initialization.md)
- [Runtime Initialization](#runtime-initialization.md)
- [Thread Configuration](#thread-configuration.md)
- [API Server Configuration](#api-server-configuration.md)
- [REST API (Actix-web)](#rest-api-actix-web.md)
- [gRPC API (Tonic)](#grpc-api-tonic.md)
- [Environment Variables](#environment-variables.md)
- [Common Environment Variable Patterns](#common-environment-variable-patterns.md)
- [CLI Arguments](#cli-arguments.md)
- [Docker Deployment](#docker-deployment.md)
- [Image Variants](#image-variants.md)
- [Multi-Stage Build Process](#multi-stage-build-process.md)
- [Build Arguments](#build-arguments.md)
- [Container Ports](#container-ports.md)
- [Volume Mounts](#volume-mounts.md)
- [Build System and CI/CD](#build-system-and-cicd.md)
- [Key CI Workflows](#key-ci-workflows.md)
- [Release Process](#release-process.md)
- [Cargo Features](#cargo-features.md)
- [Storage Paths and Directories](#storage-paths-and-directories.md)
- [Performance Tuning](#performance-tuning.md)
- [Thread Pool Configuration](#thread-pool-configuration.md)
- [Memory Management](#memory-management.md)
- [Shard Transfer Limits](#shard-transfer-limits.md)
- [Security Configuration](#security-configuration.md)
- [TLS Setup](#tls-setup.md)
- [Authentication](#authentication.md)
- [Snapshot Storage Configuration](#snapshot-storage-configuration.md)
- [Local Snapshot Storage](#local-snapshot-storage.md)
- [S3 Snapshot Storage](#s3-snapshot-storage.md)
