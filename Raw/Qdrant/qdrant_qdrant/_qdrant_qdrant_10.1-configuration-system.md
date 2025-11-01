Configuration System | qdrant/qdrant | DeepWiki

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

# Configuration System

Relevant source files

- [config/config.yaml](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml)
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

The Configuration System in Qdrant is responsible for loading, validating, and providing runtime access to all service settings. It supports a hierarchical configuration loading mechanism that merges settings from multiple sources including embedded defaults, YAML files, and environment variables. This system is initialized early during application startup and provides configuration data to all components throughout the service lifecycle.

For API-level configuration endpoints, see [Cluster API](qdrant/qdrant/9.1-rest-api-endpoints.md). For deployment-specific configuration, see [Docker Deployment](qdrant/qdrant/10.2-docker-deployment.md).

## Configuration Loading Flow

The configuration system employs a layered loading strategy where each subsequent source can override values from previous sources. This design allows for flexible deployment scenarios while maintaining sensible defaults.

```
```

Sources: [src/settings.rs230-286](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L230-L286) [src/main.rs152](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L152-L152)

The configuration loading process is implemented in the `Settings::new()` method, which uses the `config` crate to build a layered configuration hierarchy. Each layer can override values from the previous layer, with environment variables having the highest priority.

## Configuration Structure Hierarchy

The `Settings` struct serves as the root configuration object and contains multiple nested configuration sections, each responsible for a specific domain of the application.

```
```

Sources: [src/settings.rs196-227](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L196-L227) [lib/storage/src/types.rs62-114](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L62-L114) [src/settings.rs22-60](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L22-L60) [src/settings.rs68-88](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L68-L88) [src/settings.rs111-127](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L111-L127)

## Configuration Sections

### Service Configuration

The `ServiceConfig` struct defines API service settings including network binding, protocol enablement, and authentication.

| Field                             | Type             | Purpose                            | Default         |
| --------------------------------- | ---------------- | ---------------------------------- | --------------- |
| `host`                            | `String`         | Bind address for HTTP/gRPC servers | `0.0.0.0`       |
| `http_port`                       | `u16`            | REST API port                      | `6333`          |
| `grpc_port`                       | `Option<u16>`    | gRPC API port (None disables gRPC) | `6334`          |
| `max_request_size_mb`             | `usize`          | Maximum POST request size          | `32`            |
| `max_workers`                     | `Option<usize>`  | Number of actix workers            | Auto-calculated |
| `enable_cors`                     | `bool`           | Enable CORS headers                | `true`          |
| `enable_tls`                      | `bool`           | Enable TLS for external APIs       | `false`         |
| `verify_https_client_certificate` | `bool`           | Verify HTTPS client certs          | `false`         |
| `api_key`                         | `Option<String>` | API key for authentication         | None            |
| `read_only_api_key`               | `Option<String>` | Read-only API key                  | None            |
| `jwt_rbac`                        | `Option<bool>`   | Enable JWT-based RBAC              | `false`         |

Sources: [src/settings.rs22-60](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L22-L60)

### Storage Configuration

The `StorageConfig` struct controls all storage-related behavior including paths, performance tuning, and optimization strategies.

| Field                   | Type                          | Purpose                          |
| ----------------------- | ----------------------------- | -------------------------------- |
| `storage_path`          | `String`                      | Root path for all data           |
| `snapshots_path`        | `String`                      | Path for snapshots               |
| `on_disk_payload`       | `bool`                        | Store payloads on disk vs memory |
| `performance`           | `PerformanceConfig`           | Performance tuning parameters    |
| `optimizers`            | `OptimizersConfig`            | Segment optimization settings    |
| `wal`                   | `WalConfig`                   | Write-ahead log configuration    |
| `hnsw_index`            | `HnswConfig`                  | Default HNSW index parameters    |
| `node_type`             | `NodeType`                    | Normal or Listener node          |
| `recovery_mode`         | `Option<String>`              | Recovery mode message            |
| `shard_transfer_method` | `Option<ShardTransferMethod>` | Default shard transfer method    |
| `max_collections`       | `Option<usize>`               | Maximum number of collections    |

Sources: [lib/storage/src/types.rs62-114](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L62-L114)

### Cluster Configuration

The `ClusterConfig` struct enables and configures distributed deployment mode using Raft consensus.

| Field                   | Type              | Purpose                      | Default       |
| ----------------------- | ----------------- | ---------------------------- | ------------- |
| `enabled`               | `bool`            | Enable distributed mode      | `false`       |
| `peer_id`               | `Option<PeerId>`  | This peer's ID (1 to 2^53-1) | Auto-assigned |
| `grpc_timeout_ms`       | `u64`             | P2P gRPC timeout             | `5000`        |
| `connection_timeout_ms` | `u64`             | Connection timeout           | `5000`        |
| `p2p`                   | `P2pConfig`       | P2P network configuration    | -             |
| `consensus`             | `ConsensusConfig` | Raft consensus parameters    | -             |

The `ConsensusConfig` sub-section controls Raft behavior:

| Field                    | Type    | Purpose                    | Default |
| ------------------------ | ------- | -------------------------- | ------- |
| `tick_period_ms`         | `u64`   | Raft tick interval         | `100`   |
| `compact_wal_entries`    | `u64`   | WAL compaction threshold   | `128`   |
| `max_message_queue_size` | `usize` | Message queue backpressure | `100`   |
| `bootstrap_timeout_sec`  | `u64`   | Bootstrap timeout          | `15`    |

Sources: [src/settings.rs68-139](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L68-L139)

### TLS Configuration

The `TlsConfig` struct defines certificate paths for TLS encryption in both external APIs and internal P2P communication.

| Field      | Type             | Purpose                           |
| ---------- | ---------------- | --------------------------------- |
| `cert`     | `String`         | Path to server certificate PEM    |
| `key`      | `String`         | Path to private key PEM           |
| `ca_cert`  | `Option<String>` | Path to CA certificate PEM        |
| `cert_ttl` | `Option<u64>`    | Certificate reload TTL in seconds |

Sources: [src/settings.rs141-149](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L141-L149)

## Environment Variable Overrides

Environment variables provide the highest-priority configuration source and use a double-underscore (`__`) separator to represent nested configuration paths.

```
```

Sources: [src/settings.rs280](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L280-L280)

Common environment variable patterns:

| Environment Variable            | Configuration Path     | Example Value             |
| ------------------------------- | ---------------------- | ------------------------- |
| `QDRANT__LOG_LEVEL`             | `log_level`            | `INFO`, `DEBUG`           |
| `QDRANT__SERVICE__HOST`         | `service.host`         | `0.0.0.0`                 |
| `QDRANT__SERVICE__HTTP_PORT`    | `service.http_port`    | `6333`                    |
| `QDRANT__SERVICE__GRPC_PORT`    | `service.grpc_port`    | `6334`                    |
| `QDRANT__SERVICE__API_KEY`      | `service.api_key`      | `secret_key`              |
| `QDRANT__CLUSTER__ENABLED`      | `cluster.enabled`      | `true`                    |
| `QDRANT__CLUSTER__P2P__PORT`    | `cluster.p2p.port`     | `6335`                    |
| `QDRANT__STORAGE__STORAGE_PATH` | `storage.storage_path` | `/var/lib/qdrant/storage` |

The environment variable system is case-insensitive and automatically converts between snake\_case in YAML and the double-underscore notation.

Sources: [src/settings.rs280](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L280-L280)

## Configuration Validation

The configuration system performs validation using the `validator` crate after all sources are merged and deserialized. Validation errors are logged as warnings but do not prevent service startup.

```
```

Sources: [src/settings.rs298-325](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L298-L325) [src/settings.rs22-23](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L22-L23) [src/settings.rs68-88](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L68-L88) [lib/storage/src/types.rs62-76](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L62-L76)

The `Settings::validate_and_warn()` method performs additional custom validation:

1. **JWT RBAC Validation** (lines 306-317): Warns if JWT RBAC is enabled without an API key, or if the API key is shorter than the recommended 32 bytes for HMAC-SHA256.

2. **Load Error Reporting** (line 320): Reports any errors that occurred during configuration file loading (e.g., missing files).

3. **Validator Crate Validation** (lines 322-324): Runs struct-level validation rules defined via `#[validate]` attributes.

Sources: [src/settings.rs298-325](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L298-L325)

## Configuration Usage at Runtime

Once loaded and validated, the `Settings` instance is used to initialize and configure various system components during the startup sequence.

```
```

Sources: [src/main.rs152-594](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L152-L594)

Key initialization steps using configuration:

1. **Feature Flags** (line 155): Global feature flags are initialized from `settings.feature_flags`
2. **GPU Configuration** (lines 184-208): GPU devices manager initialized if `settings.gpu.indexing` is enabled
3. **Storage Path Creation** (line 220): Creates `settings.storage.storage_path` directory
4. **Runtime Creation** (lines 309-322): Search, update, and general-purpose runtimes created based on `settings.storage.performance`
5. **Resource Budgets** (lines 325-327): CPU and IO budgets calculated from `settings.storage.performance.optimizer_cpu_budget`
6. **TableOfContent** (lines 365-374): Initialized with storage config, runtimes, and channel service
7. **Consensus State** (lines 273-278): Persistent consensus state loaded using cluster configuration
8. **API Servers** (lines 557-594): HTTP and gRPC servers initialized with service configuration

Sources: [src/main.rs152-594](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L152-L594)

## Configuration File Format

The default configuration is embedded as a YAML string in the binary and can be overridden by external files. The embedded default is located at [config/config.yaml1-355](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L1-L355)

Key sections in the default configuration:

```
```

Sources: [config/config.yaml1-355](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L1-L355)

## Configuration Error Handling

The configuration system tracks loading errors in the `Settings::load_errors` field and reports them after logging is initialized. This deferred error reporting ensures that configuration problems are properly logged even though they occur before the logger is configured.

```
```

Sources: [src/settings.rs230-286](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L230-L286) [src/settings.rs218-225](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L218-L225) [src/settings.rs298-325](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L298-L325)

The `LogMsg` enum defines two error severity levels:

- `LogMsg::Warn`: Used for optional configuration files that don't exist (e.g., `config/config`, `config/local`)
- `LogMsg::Error`: Used for explicitly specified configuration files that don't exist (e.g., via `--config-path`)

Sources: [src/settings.rs340-353](https://github.com/qdrant/qdrant/blob/48203e41/src/settings.rs#L340-L353)

## Special Configuration Modes

### Recovery Mode

When `storage.recovery_mode` is set to a string value, Qdrant starts in a restricted mode where only collection metadata operations are available. This mode is used for disaster recovery scenarios.

- All data operations return the recovery mode error message
- Only collection deletion is permitted
- Documented at: `https://qdrant.tech/documentation/guides/administration/#recovery-mode`

Sources: [src/main.rs210-215](https://github.com/qdrant/qdrant/blob/48203e41/src/main.rs#L210-L215) [lib/storage/src/types.rs97-101](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/src/types.rs#L97-L101)

### Node Types

The `storage.node_type` configuration determines the node's role in the cluster:

- `Normal`: Receives updates and answers all queries (default)
- `Listener`: Receives all updates but does not answer search/read queries (useful for dedicated backup nodes)

The node type affects the default update queue size:

- Normal nodes: 100 entries
- Listener nodes: 10,000 entries

Sources: [config/config.yaml57-62](https://github.com/qdrant/qdrant/blob/48203e41/config/config.yaml#L57-L62) [lib/collection/src/operations/shared\_storage\_config.rs79-82](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/src/operations/shared_storage_config.rs#L79-L82)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Configuration System](#configuration-system.md)
- [Configuration Loading Flow](#configuration-loading-flow.md)
- [Configuration Structure Hierarchy](#configuration-structure-hierarchy.md)
- [Configuration Sections](#configuration-sections.md)
- [Service Configuration](#service-configuration.md)
- [Storage Configuration](#storage-configuration.md)
- [Cluster Configuration](#cluster-configuration.md)
- [TLS Configuration](#tls-configuration.md)
- [Environment Variable Overrides](#environment-variable-overrides.md)
- [Configuration Validation](#configuration-validation.md)
- [Configuration Usage at Runtime](#configuration-usage-at-runtime.md)
- [Configuration File Format](#configuration-file-format.md)
- [Configuration Error Handling](#configuration-error-handling.md)
- [Special Configuration Modes](#special-configuration-modes.md)
- [Recovery Mode](#recovery-mode.md)
- [Node Types](#node-types.md)
