Sparse Vector Indexing | qdrant/qdrant | DeepWiki

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

# Sparse Vector Indexing

Relevant source files

- [Cargo.lock](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.lock)
- [Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/Cargo.toml)
- [docs/redoc/default\_version.js](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/default_version.js)
- [docs/redoc/index.html](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/index.html)
- [docs/redoc/v0.10.3/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.3/openapi.json)
- [docs/redoc/v0.10.4/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.4/openapi.json)
- [docs/redoc/v0.10.5/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v0.10.5/openapi.json)
- [docs/redoc/v1.10.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.10.x/openapi.json)
- [docs/redoc/v1.11.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.11.x/openapi.json)
- [docs/redoc/v1.13.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.13.x/openapi.json)
- [docs/redoc/v1.15.x/openapi.json](https://github.com/qdrant/qdrant/blob/48203e41/docs/redoc/v1.15.x/openapi.json)
- [lib/api/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/api/Cargo.toml)
- [lib/collection/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/collection/Cargo.toml)
- [lib/common/common/src/defaults.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/common/src/defaults.rs)
- [lib/common/dataset/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/dataset/Cargo.toml)
- [lib/common/io/src/file\_operations.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/io/src/file_operations.rs)
- [lib/common/issues/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/issues/Cargo.toml)
- [lib/segment/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/Cargo.toml)
- [lib/segment/benches/hnsw\_build\_asymptotic.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_build_asymptotic.rs)
- [lib/segment/benches/hnsw\_build\_graph.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_build_graph.rs)
- [lib/segment/benches/hnsw\_search\_graph.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_search_graph.rs)
- [lib/segment/src/index/hnsw\_index/graph\_layers.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs)
- [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/header.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/header.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/serializer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/serializer.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/view.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs)
- [lib/segment/src/index/hnsw\_index/hnsw.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs)
- [lib/segment/src/index/hnsw\_index/tests/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/tests/mod.rs)
- [lib/segment/src/index/hnsw\_index/tests/test\_compact\_graph\_layer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/tests/test_compact_graph_layer.rs)
- [lib/sparse/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/Cargo.toml)
- [lib/storage/Cargo.toml](https://github.com/qdrant/qdrant/blob/48203e41/lib/storage/Cargo.toml)
- [tools/missed\_cherry\_picks.sh](https://github.com/qdrant/qdrant/blob/48203e41/tools/missed_cherry_picks.sh)

This document covers Qdrant's sparse vector indexing system, which provides efficient storage and search capabilities for sparse vectors using inverted index data structures. For dense vector indexing, see [HNSW Index Implementation](qdrant/qdrant/3.1-vector-storage-formats.md). For payload-based filtering, see [Payload Indexing and Filtering](qdrant/qdrant/3.2-hnsw-index-implementation.md).

The sparse vector indexing system enables keyword-style search and hybrid search scenarios by maintaining inverted indexes that map dimension IDs to posting lists containing document IDs and weights.

## Architecture Overview

The sparse vector indexing system is built around the `SparseVectorIndex` class which provides a unified interface for different types of inverted indexes. The system supports both mutable and immutable indexes, with options for RAM-based and memory-mapped storage.

### Core Architecture

```
```

Sources: [lib/segment/src/index/sparse\_index/sparse\_vector\_index.rs45-55](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/sparse_vector_index.rs#L45-L55) [lib/sparse/src/index/search\_context.rs26-37](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/search_context.rs#L26-L37) [lib/segment/src/index/sparse\_index/sparse\_index\_config.rs13-25](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/sparse_index_config.rs#L13-L25)

## Index Types and Storage

The system supports multiple index implementations optimized for different use cases, from mutable RAM indexes for real-time updates to compressed memory-mapped indexes for large-scale read-only scenarios.

### Index Type Hierarchy

```
```

Sources: [lib/segment/src/index/sparse\_index/sparse\_index\_config.rs17-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/sparse_index_config.rs#L17-L43) [lib/sparse/src/index/inverted\_index/mod.rs24-86](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/inverted_index/mod.rs#L24-L86) [lib/sparse/src/index/inverted\_index/inverted\_index\_ram.rs23-33](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/inverted_index/inverted_index_ram.rs#L23-L33)

### Weight Type Support

The compressed index implementations support multiple weight types for memory optimization:

| Weight Type   | Description                 | Use Case                                      |
| ------------- | --------------------------- | --------------------------------------------- |
| `f32`         | Full precision float        | High accuracy requirements                    |
| `half::f16`   | Half precision float        | Memory savings with good precision            |
| `u8`          | 8-bit unsigned integer      | Extreme compression (testing only)            |
| `QuantizedU8` | Quantized 8-bit with params | Optimal compression with calibrated precision |

Sources: [lib/sparse/src/common/types.rs11-161](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/common/types.rs#L11-L161)

## Search Process

The search system uses a `SearchContext` to coordinate queries across multiple posting lists, with sophisticated pruning mechanisms to optimize performance.

### Search Flow

```
```

Sources: [lib/sparse/src/index/search\_context.rs39-94](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/search_context.rs#L39-L94) [lib/sparse/src/index/search\_context.rs269-355](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/search_context.rs#L269-L355) [lib/segment/src/index/sparse\_index/sparse\_vector\_index.rs440-482](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/sparse_vector_index.rs#L440-L482)

### Pruning Mechanism

The search system implements sophisticated pruning to skip posting list elements that cannot contribute to top-k results:

```
```

Sources: [lib/sparse/src/index/search\_context.rs360-421](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/search_context.rs#L360-L421)

## Data Structures

### Posting Lists

Posting lists are the core data structure storing (record\_id, weight) pairs for each dimension, sorted by record\_id for efficient traversal and binary search.

#### Posting List Structure

```
```

Sources: [lib/sparse/src/index/posting\_list.rs11-15](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/posting_list.rs#L11-L15) [lib/sparse/src/index/posting\_list\_common.rs23-31](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/posting_list_common.rs#L23-L31) [lib/sparse/src/index/compressed\_posting\_list.rs21-37](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/compressed_posting_list.rs#L21-L37)

### Indices Tracking

The `IndicesTracker` manages dimension ID remapping to ensure contiguous posting list arrays:

| Component              | Purpose                                                 |
| ---------------------- | ------------------------------------------------------- |
| `original_to_remapped` | Maps original dimension IDs to contiguous array indices |
| `remapped_to_original` | Reverse mapping for reconstruction                      |
| `remap_vector()`       | Converts sparse vectors to use remapped indices         |

Sources: [lib/segment/src/index/sparse\_index/indices\_tracker.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/indices_tracker.rs)

## Configuration and Optimization

### Sparse Index Configuration

The `SparseIndexConfig` controls index behavior and performance characteristics:

```
```

### Performance Thresholds

| Threshold             | Default | Purpose                                      |
| --------------------- | ------- | -------------------------------------------- |
| `full_scan_threshold` | 20,000  | Switch to plain search for small result sets |
| `ADVANCE_BATCH_SIZE`  | 10,000  | Batch size for posting list processing       |
| `CHUNK_SIZE`          | 128     | Elements per compressed chunk                |

Sources: [lib/segment/src/index/sparse\_index/sparse\_index\_config.rs45-62](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/sparse_index_config.rs#L45-L62) [lib/sparse/src/index/search\_context.rs24](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/search_context.rs#L24-L24) [lib/sparse/src/index/compressed\_posting\_list.rs19](https://github.com/qdrant/qdrant/blob/48203e41/lib/sparse/src/index/compressed_posting_list.rs#L19-L19)

### Index Selection Strategy

The system automatically selects between indexed search and plain search based on query cardinality:

```
```

Sources: [lib/segment/src/index/sparse\_index/sparse\_vector\_index.rs452-481](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sparse_index/sparse_vector_index.rs#L452-L481)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Sparse Vector Indexing](#sparse-vector-indexing.md)
- [Architecture Overview](#architecture-overview.md)
- [Core Architecture](#core-architecture.md)
- [Index Types and Storage](#index-types-and-storage.md)
- [Index Type Hierarchy](#index-type-hierarchy.md)
- [Weight Type Support](#weight-type-support.md)
- [Search Process](#search-process.md)
- [Search Flow](#search-flow.md)
- [Pruning Mechanism](#pruning-mechanism.md)
- [Data Structures](#data-structures.md)
- [Posting Lists](#posting-lists.md)
- [Posting List Structure](#posting-list-structure.md)
- [Indices Tracking](#indices-tracking.md)
- [Configuration and Optimization](#configuration-and-optimization.md)
- [Sparse Index Configuration](#sparse-index-configuration.md)
- [Performance Thresholds](#performance-thresholds.md)
- [Index Selection Strategy](#index-selection-strategy.md)
