Filtering and Scoring | qdrant/qdrant | DeepWiki

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

# Filtering and Scoring

Relevant source files

- [lib/common/io/src/file\_operations.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/io/src/file_operations.rs)
- [lib/segment/benches/hnsw\_build\_asymptotic.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_build_asymptotic.rs)
- [lib/segment/benches/hnsw\_build\_graph.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_build_graph.rs)
- [lib/segment/benches/hnsw\_search\_graph.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/benches/hnsw_search_graph.rs)
- [lib/segment/src/index/field\_index/field\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs)
- [lib/segment/src/index/field\_index/full\_text\_index/text\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/full_text_index/text_index.rs)
- [lib/segment/src/index/field\_index/index\_selector.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/index_selector.rs)
- [lib/segment/src/index/hnsw\_index/graph\_layers.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs)
- [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/header.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/header.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/serializer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/serializer.rs)
- [lib/segment/src/index/hnsw\_index/graph\_links/view.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs)
- [lib/segment/src/index/hnsw\_index/hnsw.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs)
- [lib/segment/src/index/hnsw\_index/tests/mod.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/tests/mod.rs)
- [lib/segment/src/index/hnsw\_index/tests/test\_compact\_graph\_layer.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/tests/test_compact_graph_layer.rs)
- [lib/segment/src/index/plain\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs)
- [lib/segment/src/index/struct\_payload\_index.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs)
- [lib/segment/src/index/vector\_index\_base.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/vector_index_base.rs)

**Purpose**: This page explains how Qdrant evaluates filters and scores vectors during search operations. It covers cardinality estimation, filter evaluation strategies, the integration of filtering with vector scoring, and how search strategies are selected based on estimated filter selectivity.

**Scope**: This document focuses on the filtering and scoring mechanisms during query execution. For the overall query flow through Collection, ReplicaSet, and Segment layers, see [5.1 Query Request Flow](qdrant/qdrant/5.1-query-request-flow.md). For details on specific payload index implementations, see [4.1 Field Index Types](qdrant/qdrant/4.1-field-index-types.md).

## Overview

During vector search, Qdrant must efficiently combine two operations:

1. **Filtering**: Selecting only points that satisfy payload conditions
2. **Scoring**: Computing vector similarity between query and candidates

The system uses cardinality estimation to predict how many points will match a filter, then selects an appropriate search strategy. The `FilteredScorer` component integrates both filtering and scoring into a single interface used by the vector index.

```
```

**Diagram: Filter Evaluation and Search Strategy Selection**

Sources: [lib/segment/src/index/hnsw\_index/hnsw.rs941-1165](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L941-L1165) [lib/segment/src/index/struct\_payload\_index.rs507-571](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L507-L571)

---

## Cardinality Estimation

Cardinality estimation predicts how many points will match a filter without actually evaluating it on all points. This estimate guides the selection of an efficient search strategy.

### CardinalityEstimation Structure

The `CardinalityEstimation` struct contains:

- **`min`**: Minimum possible matching points
- **`exp`**: Expected (most likely) matching points
- **`max`**: Maximum possible matching points
- **`primary_clauses`**: Conditions that can be evaluated directly using indices

```
```

**Diagram: CardinalityEstimation Structure**

Sources: [lib/segment/src/index/field\_index/mod.rs36-43](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/mod.rs#L36-L43) [lib/segment/src/index/struct\_payload\_index.rs542-550](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L542-L550)

### Estimation Process

The estimation process flows from top-level filters down to individual field conditions:

| Level | Component            | Function                     | Purpose                                                      |
| ----- | -------------------- | ---------------------------- | ------------------------------------------------------------ |
| 1     | `StructPayloadIndex` | `estimate_cardinality()`     | Entry point, calls `estimate_filter()`                       |
| 2     | Query Estimator      | `estimate_filter()`          | Recursively processes filter clauses (must/should/must\_not) |
| 3     | `StructPayloadIndex` | `condition_cardinality()`    | Handles individual conditions                                |
| 4     | `StructPayloadIndex` | `estimate_field_condition()` | Queries specific field index                                 |
| 5     | `FieldIndex`         | `estimate_cardinality()`     | Returns actual cardinality from index                        |

```
```

**Diagram: Cardinality Estimation Flow**

Sources: [lib/segment/src/index/struct\_payload\_index.rs507-571](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L507-L571) [lib/segment/src/index/query\_estimator.rs1-150](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/query_estimator.rs#L1-L150)

### Primary vs Secondary Conditions

**Primary Conditions** can be evaluated directly from an index, returning an iterator over matching point IDs:

- Field conditions with indexed fields
- `HasId` conditions (resolved to point offsets)
- `HasVector` conditions (using vector storage availability)

**Secondary Conditions** require checking the actual payload value:

- Field conditions on non-indexed fields
- Complex nested conditions
- Conditions where index doesn't support the operation

Primary conditions enable significant optimization: if all conditions are primary, post-filtering can be skipped entirely.

```
```

**Diagram: Primary vs Secondary Condition Handling**

Sources: [lib/segment/src/index/struct\_payload\_index.rs614-680](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L614-L680) [lib/segment/src/index/field\_index/mod.rs23-35](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/mod.rs#L23-L35)

---

## Filter Evaluation Strategies

Qdrant uses different strategies to evaluate filters depending on the estimated cardinality and available indices.

### Index-Based Filtering

When primary conditions exist and field indices are available, Qdrant uses `query_field()` to retrieve matching point IDs directly from the index:

```
```

**Diagram: Field Index Filter Methods**

Each field index type implements filtering appropriate to its data type:

| Index Type      | Filter Operations                                     | Implementation                         |
| --------------- | ----------------------------------------------------- | -------------------------------------- |
| `NumericIndex`  | Range queries (`lt`, `gt`, `gte`, `lte`), exact match | Iterates over sorted histogram buckets |
| `MapIndex`      | Exact match, `any_of`                                 | Hash map lookup                        |
| `FullTextIndex` | Text match, phrase match                              | Inverted index query                   |
| `GeoIndex`      | Radius, bounding box                                  | Geo-spatial index                      |
| `BoolIndex`     | True/false                                            | Bitmap                                 |
| `NullIndex`     | Is null, is not null                                  | Bitmap                                 |

Sources: [lib/segment/src/index/field\_index/field\_index\_base.rs248-254](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/field_index/field_index_base.rs#L248-L254) [lib/segment/src/index/struct\_payload\_index.rs121-139](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L121-L139)

### Full Scan Filtering

When no indices are available or conditions are secondary, Qdrant falls back to full scan with `FilterContext`:

```
```

**Diagram: Full Scan Filter Evaluation**

Two implementations of `FilterContext`:

1. **`StructFilterContext`** ([lib/segment/src/index/struct\_filter\_context.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_filter_context.rs)): Uses optimized filter representation
2. **`PlainFilterContext`** ([lib/segment/src/index/plain\_payload\_index.rs265-274](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/plain_payload_index.rs#L265-L274)): Simple condition checking

Sources: [lib/segment/src/index/struct\_payload\_index.rs490-505](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L490-L505) [lib/segment/src/payload\_storage/mod.rs44-46](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/payload_storage/mod.rs#L44-L46)

### Hybrid Strategy with Visited List

When some conditions are primary and others are secondary, Qdrant uses a hybrid approach with a visited list to ensure uniqueness:

```
```

**Diagram: Hybrid Filtering with Visited List**

The visited list ensures that points returned by multiple primary condition iterators are only checked once.

Sources: [lib/segment/src/index/struct\_payload\_index.rs614-680](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/struct_payload_index.rs#L614-L680)

---

## Scoring Integration

### FilteredScorer

The `FilteredScorer` combines filtering and vector scoring into a single component used by the HNSW index during search:

```
```

**Diagram: FilteredScorer Structure**

The scorer provides:

1. **Vector scoring** via `RawScorer` (delegates to vector storage)
2. **Filter checking** via `ScorerFilters`
3. **Deleted point filtering** via bitslice
4. **Batch scoring** with integrated filtering

Sources: [lib/segment/src/index/hnsw\_index/point\_scorer.rs1-350](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/point_scorer.rs#L1-L350)

### Scoring in HNSW Search

During HNSW graph traversal, `FilteredScorer` is called at each step:

```
```

**Diagram: FilteredScorer Interaction During HNSW Search**

Points that don't pass the filter receive a score of `f32::MIN`, effectively excluding them from results.

Sources: [lib/segment/src/index/hnsw\_index/point\_scorer.rs150-250](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/point_scorer.rs#L150-L250) [lib/segment/src/index/hnsw\_index/graph\_layers.rs63-97](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L63-L97)

---

## Search Strategy Selection

The HNSW index selects a search strategy based on cardinality estimation and configuration:

### Strategy Decision Tree

```
```

**Diagram: HNSW Search Strategy Selection**

Sources: [lib/segment/src/index/hnsw\_index/hnsw.rs941-1165](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L941-L1165)

### Strategy Implementations

#### 1. Exact Unfiltered Search

Brute force scoring of all available vectors (used when `params.exact = true` and no filter):

```
for each point in vector_storage:
    score = scorer.score_point(point)
    add to top-k heap
```

**Telemetry**: Tracked in `exact_unfiltered` aggregator

#### 2. Exact Filtered Search

Brute force scoring of filtered points (used when cardinality is small):

```
filtered_points = payload_index.iter_filtered_points(filter)
for each point in filtered_points:
    score = scorer.score_point(point)
    add to top-k heap
```

**Telemetry**: Tracked in `exact_filtered` aggregator

**Threshold**: `available_vector_count < full_scan_threshold`

#### 3. Unfiltered HNSW Search

Standard HNSW graph traversal without filters:

```
entry_point = get highest level point
level_entry = search_entry(entry_point, top_level, 0)
results = search_on_level(level_entry, 0, ef)
```

**Telemetry**: Tracked in `unfiltered_hnsw` aggregator

#### 4. Filtered HNSW - Small Cardinality

Sample estimation to decide between graph-based or plain filtering:

```
sample_size = min(cardinality.exp, SAMPLE_SIZE)
sample_points = random sample from filtered points
sample_matched = count points in HNSW graph

if sample_matched / sample_size < SAMPLE_OPTIMISTIC_THRESHOLD:
    use exact_filtered_search()
else:
    use filtered_hnsw_search()
```

**Telemetry**: Tracked in `small_cardinality` aggregator

**Constants**:

- `SAMPLE_SIZE = 20`
- `SAMPLE_OPTIMISTIC_THRESHOLD = 0.2`

#### 5. Filtered HNSW - Large Cardinality

HNSW traversal with filter checks at each step:

```
entry_point = get filtered entry point
level_entry = search_entry(entry_point, top_level, 0, filter)
results = search_on_level(level_entry, 0, ef, filter)
```

**Telemetry**: Tracked in `large_cardinality` aggregator

Sources: [lib/segment/src/index/hnsw\_index/hnsw.rs1000-1165](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L1000-L1165) [lib/segment/src/index/sample\_estimation.rs1-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/sample_estimation.rs#L1-L50)

### Full Scan Threshold

The `full_scan_threshold` determines when to switch from graph-based to brute-force search:

| Configuration      | Calculation                             |
| ------------------ | --------------------------------------- |
| HNSW Config        | `full_scan_threshold` (in KB)           |
| Runtime Conversion | `threshold_kb * 1024 / avg_vector_size` |
| Default            | `10000` (10KB)                          |

This threshold is computed during index construction and stored in `HnswGraphConfig`.

Sources: [lib/segment/src/index/hnsw\_index/hnsw.rs140-165](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L140-L165) [lib/segment/src/index/hnsw\_index/config.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/config.rs#L1-L100)

---

## Telemetry and Performance Tracking

Search strategies are tracked separately for performance analysis:

```
```

**Diagram: Search Strategy Telemetry Tracking**

Each search path uses `ScopeDurationMeasurer` to automatically track its execution time, enabling analysis of which strategies are most commonly used and their performance characteristics.

Sources: [lib/segment/src/index/hnsw\_index/hnsw.rs96-118](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L96-L118) [lib/segment/src/common/operation\_time\_statistics.rs1-100](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/common/operation_time_statistics.rs#L1-L100)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Filtering and Scoring](#filtering-and-scoring.md)
- [Overview](#overview.md)
- [Cardinality Estimation](#cardinality-estimation.md)
- [CardinalityEstimation Structure](#cardinalityestimation-structure.md)
- [Estimation Process](#estimation-process.md)
- [Primary vs Secondary Conditions](#primary-vs-secondary-conditions.md)
- [Filter Evaluation Strategies](#filter-evaluation-strategies.md)
- [Index-Based Filtering](#index-based-filtering.md)
- [Full Scan Filtering](#full-scan-filtering.md)
- [Hybrid Strategy with Visited List](#hybrid-strategy-with-visited-list.md)
- [Scoring Integration](#scoring-integration.md)
- [FilteredScorer](#filteredscorer.md)
- [Scoring in HNSW Search](#scoring-in-hnsw-search.md)
- [Search Strategy Selection](#search-strategy-selection.md)
- [Strategy Decision Tree](#strategy-decision-tree.md)
- [Strategy Implementations](#strategy-implementations.md)
- [1. Exact Unfiltered Search](#1-exact-unfiltered-search.md)
- [2. Exact Filtered Search](#2-exact-filtered-search.md)
- [3. Unfiltered HNSW Search](#3-unfiltered-hnsw-search.md)
- [4. Filtered HNSW - Small Cardinality](#4-filtered-hnsw---small-cardinality.md)
- [5. Filtered HNSW - Large Cardinality](#5-filtered-hnsw---large-cardinality.md)
- [Full Scan Threshold](#full-scan-threshold.md)
- [Telemetry and Performance Tracking](#telemetry-and-performance-tracking.md)
