Field Index Types | qdrant/qdrant | DeepWiki

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

# Field Index Types

Relevant source files

- [lib/segment/src/index/field\_index/field\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs)
- [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs)
- [lib/segment/src/index/field\_index/index\_selector.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs)
- [lib/segment/src/index/plain\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs)
- [lib/segment/src/index/struct\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs)
- [lib/segment/src/index/vector\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/vector_index_base.rs)

## Purpose and Scope

This page documents the specific field index types available in Qdrant for indexing payload data. Each index type is optimized for different data types and query patterns, providing efficient filtering and cardinality estimation during search operations.

For information about storage backends (RocksDB, Mmap, Gridstore) and how indices are selected and migrated between storage types, see [Index Selection and Storage Backends](qdrant/qdrant/4.2-index-selection-and-storage-backends.md). For the overall payload indexing architecture and how these indices are managed, see [Payload Indexing and Filtering](qdrant/qdrant/4-payload-indexing-and-filtering.md).

## Field Index Variants

All field index types are represented by the `FieldIndex` enum, which provides a unified interface for different specialized index implementations. Each variant wraps a specific index structure optimized for particular data types and query patterns.

**FieldIndex Enum Structure**

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs131-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L131-L143)

## Numeric Indices

Numeric indices support range queries and ordering operations on numeric data types. They use interval trees and histograms internally to enable efficient range filtering and cardinality estimation.

### Index Types

| Index Variant   | Underlying Type                                     | Payload Type      | Use Case                |
| --------------- | --------------------------------------------------- | ----------------- | ----------------------- |
| `IntIndex`      | `NumericIndex<IntPayloadType, IntPayloadType>`      | 64-bit integers   | Integer range queries   |
| `DatetimeIndex` | `NumericIndex<IntPayloadType, DateTimePayloadType>` | RFC 3339 datetime | Date/time range queries |
| `FloatIndex`    | `NumericIndex<FloatPayloadType, FloatPayloadType>`  | 64-bit floats     | Float range queries     |
| `UuidIndex`     | `NumericIndex<UuidIntType, UuidPayloadType>`        | UUIDs             | UUID ordering           |

### Supported Queries

Numeric indices handle the following field condition types:

- **Range queries**: `gte`, `lte`, `gt`, `lt` conditions
- **Exact match**: Equality comparisons
- **Ordering**: Support for `order_by` operations via `StreamRange` iteration

### Internal Structure

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs132-141](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L132-L141) [lib/segment/src/index/field\_index/numeric\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/numeric_index.rs)

## Map Indices

Map indices provide exact-match lookups using hash-based data structures. They are optimized for equality comparisons and faceted search operations.

### Index Types

| Index Variant  | Underlying Type            | Key Type | Use Case               |
| -------------- | -------------------------- | -------- | ---------------------- |
| `KeywordIndex` | `MapIndex<str>`            | String   | Exact keyword matching |
| `IntMapIndex`  | `MapIndex<IntPayloadType>` | Integer  | Integer equality       |
| `UuidMapIndex` | `MapIndex<UuidIntType>`    | UUID     | UUID equality          |

### Supported Queries

Map indices handle:

- **Match conditions**: Exact value matching via `Match::Value`
- **Match Any conditions**: Matching against multiple values via `Match::Any`
- **Match Except conditions**: Negation via `Match::Except`
- **Facet operations**: Efficient facet counting for search results

### Internal Structure

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs134-142](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L134-L142) [lib/segment/src/index/field\_index/map\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/map_index)

### Integer Field Dual Indexing

Integer fields can be indexed with both `IntIndex` (for range queries) and `IntMapIndex` (for exact match), controlled by the `range` and `lookup` parameters in the payload schema:

```
```

Sources: [lib/segment/src/index/field\_index/index\_selector.rs161-182](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L161-L182)

## Geo Index

The `GeoIndex` (`GeoMapIndex`) enables spatial queries on geographic coordinates.

### Supported Queries

- **Geo Radius**: Find points within a radius of a coordinate
- **Geo Bounding Box**: Find points within a rectangular area
- **Geo Polygon**: Find points within a polygon (via radius decomposition)

### Internal Structure

The geo index uses an R-tree structure for efficient spatial partitioning and query execution. Points are indexed by their lat/lon coordinates and can be queried with geographic predicates.

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs137](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L137-L137) [lib/segment/src/index/field\_index/geo\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/geo_index)

## Full-Text Index

The `FullTextIndex` supports tokenized text search with configurable tokenization and text analysis.

### Variants

```
```

Sources: [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs37-41](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs#L37-L41)

### Supported Queries

| Query Type   | Parsed As                | Behavior                                 |
| ------------ | ------------------------ | ---------------------------------------- |
| Text Match   | `ParsedQuery::AllTokens` | All query tokens must appear in document |
| Phrase Match | `ParsedQuery::Phrase`    | Query tokens must appear in exact order  |
| Any Match    | `ParsedQuery::AnyTokens` | At least one query token must appear     |

### Text Processing Pipeline

```
```

### Tokenization

The full-text index uses a `Tokenizer` that can be configured with:

- **Lowercase normalization**: Convert tokens to lowercase
- **Stemming**: Reduce words to root form
- **Stop words**: Filter common words
- **Custom tokenizers**: Language-specific processing

Sources: [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs171-353](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs#L171-L353)

### Phrase Query Example

Phrase queries preserve token order using a `Document` structure that maintains positional information:

```
```

Sources: [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs284-353](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs#L284-L353)

## Boolean Index

The `BoolIndex` provides efficient filtering for boolean (true/false) fields.

### Variants

```
```

Sources: [lib/segment/src/index/field\_index/bool\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/bool_index)

### Implementation

Boolean indices use bitmap structures to efficiently store which points have `true` vs `false` values. This allows for:

- Constant-time lookup for boolean conditions
- Efficient cardinality estimation
- Minimal memory footprint

## Null Index

The `NullIndex` (`MutableNullIndex`) tracks which points have null or missing values for a field. It complements every other index type.

### Purpose

The null index enables:

- **IsNull condition**: Find points where field is null
- **IsEmpty condition**: Find points where field has no values
- **Completeness checking**: Verify data quality

### Automatic Creation

The null index is automatically added alongside every other index type:

```
```

Sources: [lib/segment/src/index/struct\_payload\_index.rs196-209](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L196-L209)

### Structure

The null index maintains a bitmap tracking which points have null values for the indexed field. It is always mutable and stored on disk using mmap.

Sources: [lib/segment/src/index/field\_index/null\_index](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/null_index)

## Common Index Interfaces

All field index types implement common traits that enable polymorphic usage within the `StructPayloadIndex`.

### PayloadFieldIndex Trait

The `PayloadFieldIndex` trait defines core operations all indices must support:

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs39-76](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L39-L76)

### ValueIndexer Trait

The `ValueIndexer` trait defines how indices are built and maintained:

| Method                   | Purpose                               |
| ------------------------ | ------------------------------------- |
| `add_many(id, values)`   | Add multiple values for a point       |
| `add_point(id, payload)` | Extract and index values from payload |
| `remove_point(id)`       | Remove point from index               |
| `get_value(value)`       | Extract indexable value from JSON     |
| `get_values(value)`      | Extract values, handling arrays       |

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs78-127](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L78-L127)

### FieldIndex Delegation

The `FieldIndex` enum delegates method calls to the appropriate wrapped index implementation:

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs200-254](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L200-L254)

## Schema to Index Type Mapping

The `IndexSelector` determines which index types to create based on payload schema configuration.

### Mapping Logic

```
```

Sources: [lib/segment/src/index/field\_index/index\_selector.rs150-205](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L150-L205)

### Integer Field Configuration

Integer fields support dual indexing controlled by schema parameters:

| Parameter | Default | Creates       | Purpose                        |
| --------- | ------- | ------------- | ------------------------------ |
| `range`   | `true`  | `IntIndex`    | Range queries (gte, lte, etc.) |
| `lookup`  | `true`  | `IntMapIndex` | Exact match queries            |

Both indices can exist simultaneously, with each handling different query types optimally.

Sources: [lib/segment/src/index/field\_index/index\_selector.rs161-182](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L161-L182)

## Index Type Detection and Storage

When loading an existing index, the system checks the persisted `FullPayloadIndexType` which contains:

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs481-533](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L481-L533)

### Type Consistency Checking

The system validates that loaded index types match the current payload schema:

```
```

Sources: [lib/segment/src/index/field\_index/index\_selector.rs61-148](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs#L61-L148)

## Index Builder Pattern

All field index types support a builder pattern for construction during segment optimization:

### FieldIndexBuilder Enum

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs565-603](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L565-L603)

### Builder Lifecycle

```
```

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs537-728](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L537-L728) [lib/segment/src/index/struct\_payload\_index.rs447-481](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L447-L481)

## Summary Table

| Index Type      | Underlying Structure | Query Types            | Typical Use Case        |
| --------------- | -------------------- | ---------------------- | ----------------------- |
| `IntIndex`      | `NumericIndex`       | Range, equality        | Integer ranges          |
| `DatetimeIndex` | `NumericIndex`       | Range, equality        | Date/time ranges        |
| `FloatIndex`    | `NumericIndex`       | Range, equality        | Float ranges            |
| `UuidIndex`     | `NumericIndex`       | Ordering               | UUID ranges             |
| `IntMapIndex`   | `MapIndex`           | Exact match, match any | Integer facets          |
| `KeywordIndex`  | `MapIndex`           | Exact match, match any | String keywords, facets |
| `UuidMapIndex`  | `MapIndex`           | Exact match, match any | UUID equality           |
| `GeoIndex`      | `GeoMapIndex`        | Radius, bbox, polygon  | Geographic search       |
| `FullTextIndex` | `InvertedIndex`      | Text, phrase, any      | Full-text search        |
| `BoolIndex`     | Bitmap               | Boolean equality       | True/false filters      |
| `NullIndex`     | Bitmap               | Is null, is empty      | Null value tracking     |

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs131-143](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L131-L143)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Field Index Types](#field-index-types.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Field Index Variants](#field-index-variants.md)
- [Numeric Indices](#numeric-indices.md)
- [Index Types](#index-types.md)
- [Supported Queries](#supported-queries.md)
- [Internal Structure](#internal-structure.md)
- [Map Indices](#map-indices.md)
- [Index Types](#index-types-1.md)
- [Supported Queries](#supported-queries-1.md)
- [Internal Structure](#internal-structure-1.md)
- [Integer Field Dual Indexing](#integer-field-dual-indexing.md)
- [Geo Index](#geo-index.md)
- [Supported Queries](#supported-queries-2.md)
- [Internal Structure](#internal-structure-2.md)
- [Full-Text Index](#full-text-index.md)
- [Variants](#variants.md)
- [Supported Queries](#supported-queries-3.md)
- [Text Processing Pipeline](#text-processing-pipeline.md)
- [Tokenization](#tokenization.md)
- [Phrase Query Example](#phrase-query-example.md)
- [Boolean Index](#boolean-index.md)
- [Variants](#variants-1.md)
- [Implementation](#implementation.md)
- [Null Index](#null-index.md)
- [Purpose](#purpose.md)
- [Automatic Creation](#automatic-creation.md)
- [Structure](#structure.md)
- [Common Index Interfaces](#common-index-interfaces.md)
- [PayloadFieldIndex Trait](#payloadfieldindex-trait.md)
- [ValueIndexer Trait](#valueindexer-trait.md)
- [FieldIndex Delegation](#fieldindex-delegation.md)
- [Schema to Index Type Mapping](#schema-to-index-type-mapping.md)
- [Mapping Logic](#mapping-logic.md)
- [Integer Field Configuration](#integer-field-configuration.md)
- [Index Type Detection and Storage](#index-type-detection-and-storage.md)
- [Type Consistency Checking](#type-consistency-checking.md)
- [Index Builder Pattern](#index-builder-pattern.md)
- [FieldIndexBuilder Enum](#fieldindexbuilder-enum.md)
- [Builder Lifecycle](#builder-lifecycle.md)
- [Summary Table](#summary-table.md)
