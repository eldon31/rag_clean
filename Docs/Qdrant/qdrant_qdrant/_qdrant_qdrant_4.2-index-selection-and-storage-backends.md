Index Selection and Storage Backends | qdrant/qdrant | DeepWiki

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

# Index Selection and Storage Backends

Relevant source files

- [lib/segment/src/index/field\_index/field\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs)
- [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs)
- [lib/segment/src/index/field\_index/index\_selector.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs)
- [lib/segment/src/index/plain\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs)
- [lib/segment/src/index/struct\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs)
- [lib/segment/src/index/vector\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/vector_index_base.rs)

## Purpose and Scope

This document describes how Qdrant selects appropriate storage backends for payload indices and manages the lifecycle of these indices across different storage types. It covers the `IndexSelector` abstraction, storage backend determination logic, and the migration path from legacy RocksDB indices to newer storage implementations.

For information about the specific types of payload indices (numeric, keyword, full-text, etc.), see [Field Index Types](qdrant/qdrant/4.1-field-index-types.md). For details on how indices are used during query processing, see [Filtering and Scoring](qdrant/qdrant/5.2-filtering-and-scoring.md).

---

## Storage Backend Overview

Qdrant supports three storage backends for payload indices, each optimized for different use cases:

| Backend       | Mutability              | Storage Location                     | Best For                                      |
| ------------- | ----------------------- | ------------------------------------ | --------------------------------------------- |
| **RocksDB**   | Appendable or Immutable | Disk with in-memory cache            | Legacy segments, being phased out             |
| **Mmap**      | Immutable               | Memory-mapped files                  | Non-appendable segments, low memory footprint |
| **Gridstore** | Appendable              | Gridstore files with in-memory index | New appendable segments, active development   |

The choice of backend is determined by the segment's mutability requirements and configuration flags. The system is actively migrating away from RocksDB towards Gridstore for appendable segments and Mmap for non-appendable segments.

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs46-75](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L46-L75) [lib/segment/src/index/field\_index/index\_selector.rs30-58](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L30-L58)

---

## StorageType Enum and Selection Logic

### StorageType Variants

The `StorageType` enum in `StructPayloadIndex` determines which backend to use:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs46-75](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L46-L75) [lib/segment/src/index/struct\_payload\_index.rs335-373](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L335-L373)

### Storage Selection in StructPayloadIndex::open

The storage backend is selected when opening a `StructPayloadIndex`:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs300-445](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L300-L445)

---

## IndexSelector Abstraction

The `IndexSelector` enum provides a unified interface for creating different index types across different storage backends. It acts as a factory that produces the appropriate index or builder based on the storage type.

### IndexSelector Variants

```
```

**Sources:** [lib/segment/src/index/field\_index/index\_selector.rs30-58](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L30-L58)

### Selector Method in StructPayloadIndex

The `selector()` method maps `StorageType` to `IndexSelector`:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs682-715](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L682-L715)

---

## Index Creation and Loading Flow

### Creating New Indices

When creating a new index, the flow goes through `build_field_indexes()` which uses the selector to get builders:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs447-481](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L447-L481) [lib/segment/src/index/field\_index/index\_selector.rs207-298](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L207-L298)

### Loading Existing Indices

Loading persisted indices uses `new_index_with_type()` to reconstruct the exact index type:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs174-298](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L174-L298) [lib/segment/src/index/field\_index/index\_selector.rs61-148](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L61-L148)

---

## Backend-Specific Index Implementation

Each index type supports multiple backends through variant enums and builders. Here's how this works for numeric indices as an example:

### FieldIndexBuilder Variants

```
```

### IndexSelector Backend Routing

The `IndexSelector` methods route to the appropriate builder based on the selector variant:

```
```

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs566-603](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L566-L603) [lib/segment/src/index/field\_index/index\_selector.rs381-411](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L381-L411)

### Full-Text Index Example

The `FullTextIndex` enum demonstrates backend support:

```
```

**Sources:** [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs37-93](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs#L37-L93)

---

## Storage Migration: RocksDB to Gridstore

Qdrant is actively migrating from RocksDB to Gridstore/Mmap backends. The migration happens automatically during index loading.

### Migration Trigger and Process

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs248-281](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L248-L281)

### Migration Logic Details

The migration is controlled by feature flags and happens in `load_from_db()`:

1. **Detection**: Check if any loaded indices use RocksDB via `index.is_rocksdb()`
2. **Flag Check**: Verify `migrate_rocksdb_payload_indices` feature flag is enabled
3. **Storage Type Update**: Convert `RocksDbAppendable` → `GridstoreAppendable` or `RocksDbNonAppendable` → `GridstoreNonAppendable`
4. **Config Update**: Set `skip_rocksdb = true` in the persisted config
5. **Cleanup**: Delete old RocksDB-backed indices
6. **Rebuild**: Trigger full index rebuild with new storage backend
7. **Persist**: Save new index types to config

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs248-281](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L248-L281)

### RocksDB Cleanup

After migration, if no indices use RocksDB anymore, the database is destroyed:

```
```

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs407-442](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L407-L442)

---

## File Layout and Directory Structure

Each index type uses a consistent directory naming scheme based on the field name and index type:

### Directory Naming Conventions

| Index Type    | Directory Pattern | Example               |
| ------------- | ----------------- | --------------------- |
| Map Index     | `{field}-map`     | `country-map`         |
| Numeric Index | `{field}-numeric` | `price-numeric`       |
| Text Index    | `{field}-text`    | `description-text`    |
| Boolean Index | `{field}-bool`    | `is_active-bool`      |
| Null Index    | `{field}-null`    | `optional_field-null` |

**Sources:** [lib/segment/src/index/field\_index/index\_selector.rs590-608](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L590-L608)

### FullPayloadIndexType Persistence

The exact backend and mutability of each index is persisted in `PayloadConfig`:

```
```

**Sources:** [lib/segment/src/index/field\_index/field\_index\_base.rs481-533](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L481-L533) [lib/segment/src/index/payload\_config.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/payload_config.rs) (implied)

---

## Configuration and Feature Flags

### PayloadConfig Fields

The `PayloadConfig` persisted at `{segment_path}/payload_index/config.json` contains:

- **`indices`**: Map of field name → `PayloadFieldSchemaWithIndexType`
  - Includes the field schema and exact index types (with storage backend)
- **`skip_rocksdb`**: Optional flag to prevent RocksDB usage

### Feature Flags Controlling Backend Selection

| Flag                                 | Purpose                                  | Default                    |
| ------------------------------------ | ---------------------------------------- | -------------------------- |
| `payload_index_skip_mutable_rocksdb` | Skip RocksDB for appendable segments     | Determined by build config |
| `payload_index_skip_rocksdb`         | Skip RocksDB for non-appendable segments | Determined by build config |
| `migrate_rocksdb_payload_indices`    | Enable automatic migration               | Determined by build config |

**Sources:** [lib/segment/src/index/struct\_payload\_index.rs313-331](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L313-L331)

---

## Summary

The index selection and storage backend system in Qdrant provides:

1. **Flexible Backend Selection**: Automatic choice between RocksDB, Mmap, and Gridstore based on segment mutability and configuration
2. **Abstraction Layer**: `IndexSelector` pattern allows uniform index creation across backends
3. **Type Persistence**: Full index type information (including backend) is saved in `PayloadConfig`
4. **Migration Path**: Automatic migration from legacy RocksDB to modern backends
5. **Per-Field Control**: Different fields can use different backends based on their storage requirements

The migration from RocksDB to Gridstore/Mmap is a key ongoing optimization, reducing storage overhead and improving performance for both mutable and immutable segments.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Index Selection and Storage Backends](#index-selection-and-storage-backends.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Storage Backend Overview](#storage-backend-overview.md)
- [StorageType Enum and Selection Logic](#storagetype-enum-and-selection-logic.md)
- [StorageType Variants](#storagetype-variants.md)
- [Storage Selection in StructPayloadIndex::open](#storage-selection-in-structpayloadindexopen.md)
- [IndexSelector Abstraction](#indexselector-abstraction.md)
- [IndexSelector Variants](#indexselector-variants.md)
- [Selector Method in StructPayloadIndex](#selector-method-in-structpayloadindex.md)
- [Index Creation and Loading Flow](#index-creation-and-loading-flow.md)
- [Creating New Indices](#creating-new-indices.md)
- [Loading Existing Indices](#loading-existing-indices.md)
- [Backend-Specific Index Implementation](#backend-specific-index-implementation.md)
- [FieldIndexBuilder Variants](#fieldindexbuilder-variants.md)
- [IndexSelector Backend Routing](#indexselector-backend-routing.md)
- [Full-Text Index Example](#full-text-index-example.md)
- [Storage Migration: RocksDB to Gridstore](#storage-migration-rocksdb-to-gridstore.md)
- [Migration Trigger and Process](#migration-trigger-and-process.md)
- [Migration Logic Details](#migration-logic-details.md)
- [RocksDB Cleanup](#rocksdb-cleanup.md)
- [File Layout and Directory Structure](#file-layout-and-directory-structure.md)
- [Directory Naming Conventions](#directory-naming-conventions.md)
- [FullPayloadIndexType Persistence](#fullpayloadindextype-persistence.md)
- [Configuration and Feature Flags](#configuration-and-feature-flags.md)
- [PayloadConfig Fields](#payloadconfig-fields.md)
- [Feature Flags Controlling Backend Selection](#feature-flags-controlling-backend-selection.md)
- [Summary](#summary.md)
