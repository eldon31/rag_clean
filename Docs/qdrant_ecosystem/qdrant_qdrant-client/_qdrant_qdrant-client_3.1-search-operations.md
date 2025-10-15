Search Operations | qdrant/qdrant-client | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant-client](https://github.com/qdrant/qdrant-client "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 9 July 2025 ([ac6f6c](https://github.com/qdrant/qdrant-client/commits/ac6f6cd2))

- [Overview](qdrant/qdrant-client/1-overview.md)
- [Client Architecture](qdrant/qdrant-client/2-client-architecture.md)
- [Client Interface](qdrant/qdrant-client/2.1-client-interface.md)
- [Local Mode](qdrant/qdrant-client/2.2-local-mode.md)
- [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md)
- [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md)
- [Core Operations](qdrant/qdrant-client/3-core-operations.md)
- [Search Operations](qdrant/qdrant-client/3.1-search-operations.md)
- [Collection Management](qdrant/qdrant-client/3.2-collection-management.md)
- [Point Operations](qdrant/qdrant-client/3.3-point-operations.md)
- [Advanced Features](qdrant/qdrant-client/4-advanced-features.md)
- [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md)
- [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md)
- [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md)
- [Local Inference](qdrant/qdrant-client/4.4-local-inference.md)
- [Implementation Details](qdrant/qdrant-client/5-implementation-details.md)
- [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md)
- [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md)
- [Expression Evaluation](qdrant/qdrant-client/5.3-expression-evaluation.md)
- [Development & Testing](qdrant/qdrant-client/6-development-and-testing.md)
- [Project Setup](qdrant/qdrant-client/6.1-project-setup.md)
- [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md)
- [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md)

Menu

# Search Operations

Relevant source files

- [qdrant\_client/async\_qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_client.py)
- [qdrant\_client/async\_qdrant\_remote.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_remote.py)
- [qdrant\_client/conversions/common\_types.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/common_types.py)
- [qdrant\_client/local/async\_qdrant\_local.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/async_qdrant_local.py)
- [qdrant\_client/local/local\_collection.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py)
- [qdrant\_client/local/qdrant\_local.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py)
- [qdrant\_client/qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py)
- [qdrant\_client/qdrant\_remote.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py)
- [tests/congruence\_tests/test\_common.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_common.py)
- [tests/congruence\_tests/test\_query.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_query.py)

Search operations are the core functionality of the qdrant-client library, enabling vector similarity search, recommendations, discovery, and hybrid queries across both local and remote Qdrant instances. This document covers the search architecture, query types, and execution flows for all search operations in the client.

For collection management operations, see [Collection Management](qdrant/qdrant-client/3.2-collection-management.md). For embedding integration during search, see [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md). For hybrid search algorithms, see [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md).

## Search Architecture Overview

The search system follows a unified architecture where all search operations flow through a consistent interface regardless of the backend implementation.

```
```

Sources: [qdrant\_client/qdrant\_client.py437-610](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L437-L610) [qdrant\_client/qdrant\_remote.py543-682](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L543-L682) [qdrant\_client/local/qdrant\_local.py174-224](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L174-L224)

## Search Methods

### Universal Query Interface

The `query_points()` method serves as the universal endpoint for all search operations, supporting vector search, recommendations, discovery, context search, and hybrid queries.

```
```

Sources: [qdrant\_client/qdrant\_client.py437-610](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L437-L610) [qdrant\_client/qdrant\_client.py554-592](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L554-L592)

### Legacy Search Methods

The `search()` and `search_batch()` methods are deprecated but maintained for backward compatibility. They internally convert to `query_points()` calls.

| Method            | Status     | Replacement             | Purpose                         |
| ----------------- | ---------- | ----------------------- | ------------------------------- |
| `search()`        | Deprecated | `query_points()`        | Single vector similarity search |
| `search_batch()`  | Deprecated | `query_batch_points()`  | Batch vector searches           |
| `search_groups()` | Deprecated | `query_points_groups()` | Grouped search results          |

Sources: [qdrant\_client/qdrant\_client.py277-391](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L277-L391) [qdrant\_client/qdrant\_client.py236-275](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L236-L275)

## Query Types and Resolution

### Dense Vector Queries

Dense vector queries use numerical vectors for similarity search with various distance metrics.

```
```

Sources: [qdrant\_client/local/local\_collection.py533-701](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L533-L701) [qdrant\_client/local/local\_collection.py282-332](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L282-L332)

### Sparse Vector Queries

Sparse vectors use index-value pairs for high-dimensional sparse data with optional IDF rescoring.

```
```

Sources: [qdrant\_client/local/local\_collection.py639-646](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L639-L646) [qdrant\_client/local/local\_collection.py190-202](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L190-L202)

### Advanced Query Types

#### Recommendation Queries

Recommendation queries use positive and negative examples to find similar vectors.

```
```

Sources: [qdrant\_client/local/local\_collection.py591-622](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L591-L622) [qdrant\_client/local/qdrant\_local.py353-361](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L353-L361)

#### Discovery and Context Queries

Discovery queries find vectors that distinguish between target and context, while context queries use positive-negative pairs.

```
```

Sources: [qdrant\_client/local/local\_collection.py623-638](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L623-L638) [qdrant\_client/local/qdrant\_local.py363-385](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L363-L385)

## Search Execution Pipeline

### Local Collection Search

The `LocalCollection` class implements the complete search pipeline for local execution.

```
```

Sources: [qdrant\_client/local/local\_collection.py533-701](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L533-L701) [qdrant\_client/local/local\_collection.py499-523](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L499-L523)

### Remote Search Execution

Remote searches are handled by `QdrantRemote` with automatic protocol conversion between REST and gRPC.

```
```

Sources: [qdrant\_client/qdrant\_remote.py543-682](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L543-L682) [qdrant\_client/qdrant\_remote.py573-629](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L573-L629)

## Hybrid Search and Prefetch

### Prefetch Pipeline

Prefetch operations enable multi-stage search with rescoring and fusion algorithms.

```
```

Sources: [qdrant\_client/local/local\_collection.py703-755](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L703-L755) [qdrant\_client/local/local\_collection.py792-842](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L792-L842)

### Fusion Query Processing

```
```

Sources: [qdrant\_client/local/local\_collection.py804-842](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L804-L842) [qdrant\_client/hybrid/fusion.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/fusion.py)

## Performance Considerations

### Vector Type Performance

| Vector Type | Storage              | Search Performance              | Memory Usage              |
| ----------- | -------------------- | ------------------------------- | ------------------------- |
| Dense       | `np.ndarray`         | Fast with vectorized operations | High for large dimensions |
| Sparse      | `list[SparseVector]` | Efficient for high sparsity     | Low for sparse data       |
| Multi       | `list[np.ndarray]`   | Variable by comparator          | Highest memory usage      |

### Search Optimizations

The local collection implements several optimizations for search performance:

- **Early termination** with score thresholds
- **Vectorized distance calculations** using NumPy operations
- **Payload filtering masks** to avoid unnecessary computations
- **Result ordering** based on distance metrics
- **IDF rescoring** for sparse vectors when configured

Sources: [qdrant\_client/local/local\_collection.py649-701](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L649-L701) [qdrant\_client/local/local\_collection.py175-202](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L175-L202)

### Batch Processing

Batch operations reduce network overhead for multiple queries:

```
```

Sources: [qdrant\_client/qdrant\_client.py393-435](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L393-L435) [qdrant\_client/qdrant\_remote.py684-750](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_remote.py#L684-L750)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Search Operations](#search-operations.md)
- [Search Architecture Overview](#search-architecture-overview.md)
- [Search Methods](#search-methods.md)
- [Universal Query Interface](#universal-query-interface.md)
- [Legacy Search Methods](#legacy-search-methods.md)
- [Query Types and Resolution](#query-types-and-resolution.md)
- [Dense Vector Queries](#dense-vector-queries.md)
- [Sparse Vector Queries](#sparse-vector-queries.md)
- [Advanced Query Types](#advanced-query-types.md)
- [Recommendation Queries](#recommendation-queries.md)
- [Discovery and Context Queries](#discovery-and-context-queries.md)
- [Search Execution Pipeline](#search-execution-pipeline.md)
- [Local Collection Search](#local-collection-search.md)
- [Remote Search Execution](#remote-search-execution.md)
- [Hybrid Search and Prefetch](#hybrid-search-and-prefetch.md)
- [Prefetch Pipeline](#prefetch-pipeline.md)
- [Fusion Query Processing](#fusion-query-processing.md)
- [Performance Considerations](#performance-considerations.md)
- [Vector Type Performance](#vector-type-performance.md)
- [Search Optimizations](#search-optimizations.md)
- [Batch Processing](#batch-processing.md)
