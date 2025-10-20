HNSW Index Implementation | qdrant/qdrant | DeepWiki

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

# HNSW Index Implementation

Relevant source files

- [lib/common/io/src/file\_operations.rs](https://github.com/qdrant/qdrant/blob/48203e41/lib/common/io/src/file_operations.rs)
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

This document describes the implementation of the Hierarchical Navigable Small World (HNSW) algorithm in Qdrant. HNSW is a graph-based approximate nearest neighbor search index that provides fast vector similarity search with tunable accuracy/speed tradeoffs.

For information about other vector index types (Plain, Sparse), see [Vector Storage and Indexing](qdrant/qdrant/3-vector-storage-and-indexing.md). For details on quantization techniques used with HNSW, see [Vector Quantization](qdrant/qdrant/3.3-vector-quantization.md). For search/query processing that uses HNSW, see [Query Request Flow](qdrant/qdrant/5.1-query-request-flow.md).

## Core Architecture

The HNSW implementation consists of four primary components that work together to provide efficient graph-based search:

```
```

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs83-93](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L83-L93) [lib/segment/src/index/hnsw\_index/graph\_layers.rs44-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L44-L50) [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs32-48](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L32-L48) [lib/segment/src/index/hnsw\_index/graph\_links.rs56-61](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs#L56-L61)

### HNSWIndex

The `HNSWIndex` struct is the top-level index interface that implements the `VectorIndex` trait. It maintains references to all necessary components and coordinates between graph operations and vector/payload storage.

**Key Fields**:

- `graph: GraphLayers` - The immutable hierarchical graph structure
- `vector_storage: Arc<AtomicRefCell<VectorStorageEnum>>` - Raw vector data
- `quantized_vectors: Arc<AtomicRefCell<Option<QuantizedVectors>>>` - Compressed vectors for search
- `id_tracker: Arc<AtomicRefCell<IdTrackerSS>>` - Maps external IDs to internal offsets
- `payload_index: Arc<AtomicRefCell<StructPayloadIndex>>` - For filtered search
- `config: HnswGraphConfig` - Configuration parameters (m, ef\_construct, etc.)

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs83-93](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L83-L93)

### GraphLayers

`GraphLayers` is the immutable graph structure used during search operations. It provides efficient read-only access to the multi-level graph connectivity.

**Key Fields**:

- `hnsw_m: HnswM` - M parameters (m for level > 0, m0 for level 0)
- `links: GraphLinks` - Actual link storage (neighbors for each node)
- `entry_points: EntryPoints` - Multiple entry points for different filters
- `visited_pool: VisitedPool` - Pool of reusable visited lists for search

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers.rs44-50](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L44-L50)

### GraphLayersBuilder

`GraphLayersBuilder` is the mutable builder used during index construction. It allows concurrent point insertion and converts to the immutable `GraphLayers` when complete.

**Key Fields**:

- `links_layers: Vec<LockedLayersContainer>` - Per-point, per-level link containers with locks
- `ready_list: RwLock<BitVec>` - Tracks which points have been indexed
- `entry_points: Mutex<EntryPoints>` - Maintains entry points during construction
- `hnsw_m: HnswM` - M parameters for graph construction
- `ef_construct: usize` - Size of candidate list during construction

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs32-48](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L32-L48)

### GraphLinks

`GraphLinks` is a self-referential struct that manages the storage and access to graph connectivity data. It supports multiple storage formats for space/speed tradeoffs.

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_links.rs199-207](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs#L199-L207) [lib/segment/src/index/hnsw\_index/graph\_links.rs224-331](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs#L224-L331)

## Hierarchical Graph Structure

HNSW uses a multi-level graph where each level is a subset of the level below it. Points are assigned to levels using a geometric distribution, creating a hierarchical structure that enables efficient search.

### Level Assignment

The level for each point is determined using a geometric distribution during insertion:

```
```

**Formula**: `level_factor = 1.0 / ln(max(m, 2))`

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs357-366](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L357-L366) [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs286-290](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L286-L290)

### M Parameters

The graph uses two M parameters that control connectivity:

- **m**: Maximum links per node on levels 1 and above
- **m0**: Maximum links per node on level 0 (typically `m0 = 2 * m`)

| Parameter      | Level 0            | Level > 0         |
| -------------- | ------------------ | ----------------- |
| Maximum links  | m0 (typ. 2\*m)     | m                 |
| Link selection | Heuristic pruning  | Heuristic pruning |
| Purpose        | Dense connectivity | Sparse navigation |

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers.rs359-361](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L359-L361) [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs68-70](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L68-L70)

### Entry Points

The index maintains multiple entry points to support filtered searches. Entry points are stored per filter predicate and updated during construction.

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers.rs387-409](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L387-L409)

## Index Construction Process

### Build Pipeline

Title: **HNSW Index Build Pipeline**

```
```

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs199-665](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L199-L665)

### Point Insertion Algorithm

The `link_new_point()` method in `GraphLayersBuilder` inserts a new point into the graph:

**Algorithm Steps**:

1. **Find Entry Point**: Get an entry point that satisfies filters

2. **Navigate to Target Level**: Use greedy search from entry point down to the point's assigned level

3. **For Each Level (top-down)**:

   - Find nearest neighbors using beam search with `ef_construct` candidates
   - Select M best neighbors using heuristic
   - Create bidirectional links
   - Use selected neighbors as entry for next level

```
```

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs387-440](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L387-L440) [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs466-506](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L466-L506)

### Heuristic Link Selection

When `use_heuristic` is enabled (default: `true`), the algorithm selects neighbors that are "not closer to each other than to the new point." This prevents clustering and maintains graph connectivity.

**Heuristic Logic** (`link_with_heuristic`):

1. Sort candidates by distance to new point

2. For each candidate in order:

   - If less than M neighbors selected, add it
   - Only add if it's not closer to existing selected neighbors than to new point

3. Create bidirectional links with selected neighbors

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers\_builder.rs508-545](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers_builder.rs#L508-L545) [lib/segment/src/index/hnsw\_index/hnsw.rs70](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L70-L70)

### Payload-Specific Graphs

After building the main graph, HNSW constructs additional connectivity for payload-filtered searches. This ensures good search quality even with filters.

**Process**:

1. For each indexed payload field, identify blocks (groups of points with same value)
2. For blocks smaller than `max_block_size`, check connectivity in main graph
3. If connectivity is insufficient, build additional `GraphLayersBuilder` for that block
4. Merge additional links into main graph using `merge_from_other()`

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs453-607](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L453-L607)

### Old Index Reuse

During rebuilds, HNSW can reuse structure from an old index to speed up construction:

**Reuse Strategy**:

1. Check if old index has compatible configuration
2. Create mapping between old and new point IDs
3. Use `GraphLayersHealer` to migrate links from old index
4. Only insert truly new points (not in old index)

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs261-275](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L261-L275) [lib/segment/src/index/hnsw\_index/hnsw.rs390-417](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L390-L417)

## Search Algorithm

The HNSW search consists of two phases: a greedy search from the entry point to level 0, followed by a beam search on level 0.

### Two-Phase Search

Title: **HNSW Two-Phase Search Algorithm**

```
```

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers.rs411-439](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L411-L439)

### Search Entry (Phase 1)

The `search_entry` method performs greedy search from the entry point down to level 0:

```
```

**Key Characteristic**: Beam size = 1 (follows only the single best neighbor at each step)

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers.rs122-151](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L122-L151) [lib/segment/src/index/hnsw\_index/graph\_layers.rs153-190](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L153-L190)

### Search on Level (Phase 2)

The `search_on_level` method performs beam search with configurable `ef` parameter:

**Algorithm**:

1. Initialize `SearchContext` with `ef` capacity

2. Add entry point to candidates and nearest

3. While candidates exist:

   - Pop best candidate from priority queue

   - If its score is worse than `ef`-th best, stop

   - For each unvisited neighbor:

     - Score the neighbor
     - Add to candidates and nearest if good enough

4. Return top results

**SearchContext Fields**:

- `candidates: FixedLengthPriorityQueue` - Candidates to explore (max-heap by score)
- `nearest: FixedLengthPriorityQueue` - Best results found (min-heap by score)

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_layers.rs99-120](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L99-L120) [lib/segment/src/index/hnsw\_index/graph\_layers.rs63-97](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L63-L97)

### Search with Quantized Vectors

When quantized vectors are available, HNSW can optionally use them during search for faster distance calculations:

**Two-Stage Scoring**:

1. **Coarse Search**: Use quantized vectors stored in graph links for fast filtering
2. **Refinement**: Rescore top candidates with original vectors for accuracy

This is enabled via the `CompressedWithVectors` graph format, where each link embeds the quantized vector of the neighbor.

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs969-1035](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L969-L1035) [lib/segment/src/index/hnsw\_index/graph\_layers.rs441-474](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_layers.rs#L441-L474)

## Graph Links Storage Formats

HNSW supports three storage formats for graph links, offering different tradeoffs between memory usage, disk size, and search speed.

### Format Comparison

| Format                | Memory Usage | Disk Size | Search Speed | Quantization Support |
| --------------------- | ------------ | --------- | ------------ | -------------------- |
| Plain                 | High         | High      | Fast         | No                   |
| Compressed            | Medium       | Low       | Fast         | No                   |
| CompressedWithVectors | Medium-High  | Medium    | Fastest\*    | Yes                  |

\*When using quantized search with embedded vectors

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_links.rs56-61](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs#L56-L61)

### Plain Format

The `Plain` format stores links as uncompressed arrays of `u32` neighbor IDs.

**File Structure**:

```
[HeaderPlain]
[level_offsets: u64[]]
[reindex: u32[]]
[neighbors: u32[]]
[padding: u8[]]
[offsets: u64[]]
```

**HeaderPlain Fields**:

- `point_count`: Number of points in the graph
- `levels_count`: Number of levels in the graph
- `total_neighbors_count`: Total number of neighbor entries
- `total_offset_count`: Number of offset entries
- `offsets_padding_bytes`: Padding before offsets array (0 or 4 bytes)

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_links/header.rs9-20](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/header.rs#L9-L20) [lib/segment/src/index/hnsw\_index/graph\_links/view.rs121-135](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs#L121-L135)

### Compressed Format

The `Compressed` format uses bit-packing to reduce storage:

**Compression Techniques**:

1. **Sorted Prefix**: First M links are sorted and stored with delta encoding
2. **Unsorted Suffix**: Remaining links use variable-bit encoding
3. **Offset Compression**: Offsets are compressed using bitpacking

**File Structure**:

```
[HeaderCompressed]
[level_offsets: u64[]]
[reindex: u32[]]
[neighbors: u8[]] (compressed)
[offsets: u8[]] (compressed)
```

**HeaderCompressed Additional Fields**:

- `version`: Magic number `0xFFFF_FFFF_FFFF_FF01`
- `m`, `m0`: M parameters needed for decompression
- `offsets_parameters`: Bitpacking parameters for offset decompression

**Compression Ratio**: Typically 2-4x smaller than Plain format

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_links/header.rs22-35](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/header.rs#L22-L35) [lib/segment/src/index/hnsw\_index/graph\_links/view.rs137-166](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs#L137-L166)

### CompressedWithVectors Format

The `CompressedWithVectors` format embeds quantized vectors alongside links for faster search:

**File Structure**:

```
[HeaderCompressedWithVectors]
[level_offsets: u64[]]
[reindex: u32[]]
[padding for alignment]
[neighbors_and_vectors: u8[]]
[offsets: u8[]] (compressed)
```

**Per-Point Data Layout** (for level 0):

```
[base_vector: u8[base_size]]
[neighbors_count: varint]
[compressed_links: u8[]]
[padding for link_vector alignment]
[link_vectors: u8[neighbors_count * link_size]]
[padding for next base_vector alignment]
```

**Per-Point Data Layout** (for level > 0):

```
[neighbors_count: varint]
[compressed_links: u8[]]
[padding for link_vector alignment]
[link_vectors: u8[neighbors_count * link_size]]
```

**HeaderCompressedWithVectors Additional Fields**:

- `version`: Magic number `0xFFFF_FFFF_FFFF_FF02`
- `base_vector_layout`: Layout of base vectors (size, alignment)
- `link_vector_layout`: Layout of link vectors (size, alignment)

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_links/header.rs37-52](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/header.rs#L37-L52) [lib/segment/src/index/hnsw\_index/graph\_links/view.rs168-213](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs#L168-L213) [lib/segment/src/index/hnsw\_index/graph\_links/view.rs259-340](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/view.rs#L259-L340)

### Reindexing for Level Sorting

All formats use a "reindex" array to optimize level-based access:

Title: **Graph Links Reindexing Strategy**

```
```

**Purpose**: Points at higher levels appear first in the flattened links array, enabling efficient level-based iteration without seeking.

**Sources**: [lib/segment/src/index/hnsw\_index/graph\_links/serializer.rs51-88](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links/serializer.rs#L51-L88)

## Configuration Parameters

### HnswGraphConfig

The `HnswGraphConfig` struct stores persistent HNSW configuration:

| Parameter              | Type            | Description                        | Typical Value                |
| ---------------------- | --------------- | ---------------------------------- | ---------------------------- |
| `m`                    | `usize`         | Max links per node (level > 0)     | 16                           |
| `m0`                   | `usize`         | Max links per node (level 0)       | 32 (2\*m)                    |
| `ef_construct`         | `usize`         | Candidate list size during build   | 100                          |
| `full_scan_threshold`  | `usize`         | Point count to switch to full scan | Calculated from KB threshold |
| `max_indexing_threads` | `usize`         | Max threads for parallel build     | CPU count                    |
| `payload_m`            | `Option<usize>` | M for payload-specific graphs      | m or custom                  |

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs140-165](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L140-L165) [lib/segment/src/index/hnsw\_index/hnsw.rs252-260](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L252-L260)

### HnswConfig (User-Facing)

The `HnswConfig` type is the user-facing configuration in segment config:

| Parameter              | Type            | Description                         |
| ---------------------- | --------------- | ----------------------------------- |
| `m`                    | `usize`         | Connectivity parameter              |
| `ef_construct`         | `usize`         | Construction quality                |
| `full_scan_threshold`  | `usize`         | Full scan threshold in KB           |
| `max_indexing_threads` | `usize`         | Build parallelism                   |
| `on_disk`              | `Option<bool>`  | Load graph into RAM or keep on disk |
| `payload_m`            | `Option<usize>` | M for filtered graphs               |
| `copy_vectors`         | `Option<bool>`  | Use CompressedWithVectors format    |

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs120-127](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L120-L127)

### Search Parameters

Search behavior is controlled by `SearchParams`:

| Parameter      | Type                               | Description                  | Default     |
| -------------- | ---------------------------------- | ---------------------------- | ----------- |
| `hnsw_ef`      | `Option<usize>`                    | Beam size for level 0 search | `config.ef` |
| `quantization` | `Option<QuantizationSearchParams>` | Quantization settings        | None        |
| `exact`        | `Option<bool>`                     | Force exact search           | `false`     |

**ef Parameter**: Higher values improve accuracy but increase search time. Typical range: 32-512.

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs942-954](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L942-L954)

## On-Disk vs In-Memory

HNSW supports both in-memory and memory-mapped (on-disk) operation:

**In-Memory Mode** (`on_disk = false`):

- Graph loaded into RAM as `GraphLinksEnum::Ram(Vec<u8>)`
- Fastest search performance
- High memory usage

**On-Disk Mode** (`on_disk = true`):

- Graph memory-mapped as `GraphLinksEnum::Mmap(Arc<Mmap>)`
- Relies on OS page cache
- Lower memory footprint
- Slight performance penalty on cold reads

**Default**: Determined by storage configuration, typically `false` for small collections and `true` for large ones.

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs169](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L169-L169) [lib/segment/src/index/hnsw\_index/graph\_links.rs209-222](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs#L209-L222) [lib/segment/src/index/hnsw\_index/graph\_links.rs225-235](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/graph_links.rs#L225-L235)

## GPU Acceleration

When compiled with the `gpu` feature and a GPU is available, HNSW can offload graph construction to GPU:

**GPU Build Process**:

1. Transfer vectors to GPU memory via `GpuVectorStorage`
2. Execute parallel graph construction on GPU using `build_hnsw_on_gpu`
3. If GPU build fails, fall back to CPU implementation
4. GPU-built graphs are identical to CPU-built graphs

**GPU Support**: Only for the main graph; payload-specific graphs always use CPU.

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs279-383](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L279-L383) [lib/segment/src/index/hnsw\_index/hnsw.rs780-902](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L780-L902) [lib/segment/src/index/hnsw\_index/hnsw.rs904-939](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L904-L939)

## Telemetry

HNSW tracks search performance across different strategies:

**Telemetry Categories**:

- `unfiltered_plain`: Brute-force search without filters
- `filtered_plain`: Brute-force search with filters
- `unfiltered_hnsw`: HNSW search without filters
- `small_cardinality`: HNSW search with restrictive filters
- `large_cardinality`: HNSW search with permissive filters
- `exact_filtered`: Exact filtered search
- `exact_unfiltered`: Exact unfiltered search

Each category maintains an `OperationDurationsAggregator` to track timing statistics.

**Sources**: [lib/segment/src/index/hnsw\_index/hnsw.rs95-118](https://github.com/qdrant/qdrant/blob/48203e41/lib/segment/src/index/hnsw_index/hnsw.rs#L95-L118)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [HNSW Index Implementation](#hnsw-index-implementation.md)
- [Core Architecture](#core-architecture.md)
- [HNSWIndex](#hnswindex.md)
- [GraphLayers](#graphlayers.md)
- [GraphLayersBuilder](#graphlayersbuilder.md)
- [GraphLinks](#graphlinks.md)
- [Hierarchical Graph Structure](#hierarchical-graph-structure.md)
- [Level Assignment](#level-assignment.md)
- [M Parameters](#m-parameters.md)
- [Entry Points](#entry-points.md)
- [Index Construction Process](#index-construction-process.md)
- [Build Pipeline](#build-pipeline.md)
- [Point Insertion Algorithm](#point-insertion-algorithm.md)
- [Heuristic Link Selection](#heuristic-link-selection.md)
- [Payload-Specific Graphs](#payload-specific-graphs.md)
- [Old Index Reuse](#old-index-reuse.md)
- [Search Algorithm](#search-algorithm.md)
- [Two-Phase Search](#two-phase-search.md)
- [Search Entry (Phase 1)](#search-entry-phase-1.md)
- [Search on Level (Phase 2)](#search-on-level-phase-2.md)
- [Search with Quantized Vectors](#search-with-quantized-vectors.md)
- [Graph Links Storage Formats](#graph-links-storage-formats.md)
- [Format Comparison](#format-comparison.md)
- [Plain Format](#plain-format.md)
- [Compressed Format](#compressed-format.md)
- [CompressedWithVectors Format](#compressedwithvectors-format.md)
- [Reindexing for Level Sorting](#reindexing-for-level-sorting.md)
- [Configuration Parameters](#configuration-parameters.md)
- [HnswGraphConfig](#hnswgraphconfig.md)
- [HnswConfig (User-Facing)](#hnswconfig-user-facing.md)
- [Search Parameters](#search-parameters.md)
- [On-Disk vs In-Memory](#on-disk-vs-in-memory.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Telemetry](#telemetry.md)
