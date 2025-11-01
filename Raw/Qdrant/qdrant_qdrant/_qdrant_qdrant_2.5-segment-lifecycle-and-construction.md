Segment Lifecycle and Construction | qdrant/qdrant | DeepWiki

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

# Segment Lifecycle and Construction

Relevant source files

- [lib/segment/src/entry/entry\_point.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/entry/entry_point.rs)
- [lib/segment/src/fixtures/index\_fixtures.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/fixtures/index_fixtures.rs)
- [lib/segment/src/segment\_constructor/segment\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs)
- [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs)
- [lib/segment/src/vector\_storage/vector\_storage\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/vector_storage/vector_storage_base.rs)

This page explains the structure, lifecycle, and construction of Segments, which are the fundamental data units in Qdrant that store vectors, payloads, and indices. This document covers segment types, component composition, creation/loading processes, and the SegmentBuilder optimization workflow.

For information about how LocalShard manages segments and triggers optimization, see [Local Shard Architecture](qdrant/qdrant/2.4-local-shard-architecture.md). For details on specific index implementations, see [HNSW Index Implementation](qdrant/qdrant/3.2-hnsw-index-implementation.md) and [Field Index Types](qdrant/qdrant/4.1-field-index-types.md).

## Segment Overview

A Segment is a self-contained unit that stores:

- Vector data (dense, sparse, or multi-dense vectors)
- Payload data (JSON payloads associated with points)
- Vector indices (HNSW, Plain, or Sparse indices)
- Payload indices (field-specific indices for filtering)
- ID mappings (external point IDs to internal offsets)
- Version information for each point

Each segment operates independently with its own storage files and can be of two types: **Plain** (unindexed) or **Indexed** (with vector indices built).

**Sources:** [lib/segment/src/entry/entry\_point.rs26-357](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/entry/entry_point.rs#L26-L357)

## Segment Types

```
```

The segment type is determined by the configuration:

- **Plain**: `segment_config.is_any_vector_indexed()` returns false
- **Indexed**: `segment_config.is_any_vector_indexed()` returns true

The appendable flag determines whether the segment can accept new writes:

- **Appendable segments** use `MutableIdTracker` and accept insertions
- **Immutable segments** use `ImmutableIdTracker` for better memory efficiency

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs603-607](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L603-L607) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs454-457](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L454-L457)

## Segment Component Composition

A Segment is composed of multiple storage and indexing components:

```
```

Each component is wrapped in `Arc<AtomicRefCell<T>>` to allow shared, interior-mutable access across threads while maintaining Rust's borrowing rules.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs609-627](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L609-L627) [lib/segment/src/segment\_constructor/segment\_builder.rs467-627](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L467-L627)

## Component Initialization Paths

The segment construction process involves creating and initializing each component based on the segment configuration:

```
```

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs436-627](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L436-L627) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs99-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L99-L223)

## Segment Creation and Loading

### Creating a New Segment

The `build_segment()` function creates a new segment from scratch:

| Function             | Purpose                   | Key Parameters                          |
| -------------------- | ------------------------- | --------------------------------------- |
| `build_segment()`    | Create new empty segment  | `segments_path`, `config`, `ready` flag |
| `new_segment_path()` | Generate unique UUID path | Returns `PathBuf` with UUID             |
| `create_segment()`   | Internal constructor      | Sets up all components                  |

**Creation flow:**

1. Generate unique path: `segments_path.join(UUID)`
2. Create directory
3. Initialize all components via `create_segment()`
4. Save segment state to `segment_state.json`
5. Save version file (if `ready=true`) to mark segment as loadable

The `ready` flag controls whether the segment is immediately loadable. If false, the version file is not saved, and the segment will be skipped on restart.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs782-808](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L782-L808) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs766-768](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L766-L768)

### Loading an Existing Segment

The `load_segment()` function restores a segment from disk:

```
```

The loader handles version migrations automatically, converting old segment formats to the current version. It also supports migrating from RocksDB-based storage to newer memory-mapped storage formats when feature flags are enabled.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs687-764](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L687-L764) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs810-901](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L810-L901)

## Segment Construction via SegmentBuilder

The `SegmentBuilder` is used to create optimized segments by merging multiple existing segments. This is the core of the optimization process.

### SegmentBuilder Structure

```
```

**Sources:** [lib/segment/src/segment\_constructor/segment\_builder.rs58-74](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L58-L74)

### SegmentBuilder Workflow

The complete optimization workflow:

```
```

**Key optimizations:**

1. **Defragmentation**: Points with similar payload values are placed near each other in internal ID space to improve cache locality during filtered searches
2. **Index reuse**: Old indices from source segments are passed to `build_vector_index()` to speed up HNSW construction by providing good starting points
3. **Cache eviction**: After building, all caches are cleared to avoid polluting RAM with data that should stay on disk
4. **Atomic completion**: The segment is only marked as valid (version file saved) after all components are built successfully

**Sources:** [lib/segment/src/segment\_constructor/segment\_builder.rs287-459](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L287-L459) [lib/segment/src/segment\_constructor/segment\_builder.rs461-691](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L461-L691)

### Defragmentation Strategy

The defragmentation process improves query performance by sorting points:

```
```

The ordering value is a heuristic that groups similar payloads together. For example, if defragmenting on a `user_id` field, all points with the same `user_id` will have similar ordering values and end up adjacent in the segment.

**Sources:** [lib/segment/src/segment\_constructor/segment\_builder.rs311-329](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L311-L329) [lib/segment/src/segment\_constructor/segment\_builder.rs201-276](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_builder.rs#L201-L276)

## Segment Lifecycle States

```
```

**Lifecycle summary:**

1. **Building**: Segment directory created, components being initialized. If process crashes, segment is skipped on restart (no version file).

2. **Ready**: Version file saved, segment is complete and will be loaded on restart.

3. **Loading**: On restart, `load_segment()` reads the segment from disk.

4. **Migrating**: If the stored version differs from the application version, migration routines convert the data.

5. **Loaded**: Segment is in memory and active, serving queries and updates.

6. **Optimizing**: SegmentBuilder merges this segment with others to create a new optimized segment.

7. **Deleted**: Segment directory renamed to `*.deleted` extension, will be skipped on load and eventually cleaned up.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs782-808](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L782-L808) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs687-736](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L687-L736)

## Storage Backend Selection

Vector and payload storage backends are selected based on configuration:

| Storage Type                          | Implementation                | Use Case                       | On-Disk |
| ------------------------------------- | ----------------------------- | ------------------------------ | ------- |
| `VectorStorageType::Memory`           | RocksDB-based (legacy)        | Small datasets, fast access    | No      |
| `VectorStorageType::Mmap`             | Memory-mapped files           | Large datasets, read-optimized | Yes     |
| `VectorStorageType::ChunkedMmap`      | Chunked mmap, appendable      | Large datasets, write-capable  | Yes     |
| `VectorStorageType::InRamChunkedMmap` | Chunked mmap, in-memory cache | High performance               | No      |
| `PayloadStorageType::InMemory`        | RocksDB-based (legacy)        | Small payloads                 | No      |
| `PayloadStorageType::OnDisk`          | RocksDB-based (legacy)        | Large payloads                 | Yes     |
| `PayloadStorageType::Mmap`            | Memory-mapped gridstore       | Modern default                 | Yes     |
| `PayloadStorageType::InRamMmap`       | Mmap with in-memory cache     | High performance               | No      |

Qdrant is actively migrating away from RocksDB storage to memory-mapped formats for better performance. The migration is triggered by feature flags and happens automatically during segment loading.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs99-223](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L99-L223) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs225-248](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L225-L248)

## File Structure

A typical segment directory contains:

```
<uuid>/
├── segment_state.json          # Segment configuration and metadata
├── version                      # Version file (marks segment as ready)
├── id_tracker/                  # ID mapping files
│   ├── mappings.dat            # External → Internal ID
│   └── versions.dat            # Point versions
├── payload_index/               # Payload field indices
│   ├── <field_name>.index
│   └── ...
├── payload_storage/             # Payload data
│   ├── gridstore/
│   └── ...
├── vector_storage/              # Default vector storage
│   ├── vectors.dat
│   ├── deleted.dat
│   └── ...
├── vector_storage-<name>/       # Named vector storage
├── vector_index/                # Default vector index (HNSW)
│   ├── graph.dat
│   └── ...
└── vector_index-<name>/         # Named vector indices
```

Each component is responsible for managing its own files within the segment directory.

**Sources:** [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs72-97](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L72-L97) [lib/segment/src/segment\_constructor/segment\_constructor\_base.rs267-269](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/segment_constructor/segment_constructor_base.rs#L267-L269)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Segment Lifecycle and Construction](#segment-lifecycle-and-construction.md)
- [Segment Overview](#segment-overview.md)
- [Segment Types](#segment-types.md)
- [Segment Component Composition](#segment-component-composition.md)
- [Component Initialization Paths](#component-initialization-paths.md)
- [Segment Creation and Loading](#segment-creation-and-loading.md)
- [Creating a New Segment](#creating-a-new-segment.md)
- [Loading an Existing Segment](#loading-an-existing-segment.md)
- [Segment Construction via SegmentBuilder](#segment-construction-via-segmentbuilder.md)
- [SegmentBuilder Structure](#segmentbuilder-structure.md)
- [SegmentBuilder Workflow](#segmentbuilder-workflow.md)
- [Defragmentation Strategy](#defragmentation-strategy.md)
- [Segment Lifecycle States](#segment-lifecycle-states.md)
- [Storage Backend Selection](#storage-backend-selection.md)
- [File Structure](#file-structure.md)
