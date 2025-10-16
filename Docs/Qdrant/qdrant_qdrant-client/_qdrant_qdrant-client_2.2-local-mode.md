Local Mode | qdrant/qdrant-client | DeepWiki

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

# Local Mode

Relevant source files

- [qdrant\_client/local/async\_qdrant\_local.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/async_qdrant_local.py)
- [qdrant\_client/local/local\_collection.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py)
- [qdrant\_client/local/qdrant\_local.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py)
- [tests/congruence\_tests/test\_common.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_common.py)
- [tests/congruence\_tests/test\_query.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_query.py)

Local Mode provides an in-process implementation of Qdrant functionality through the `QdrantLocal` and `AsyncQdrantLocal` classes. This mode operates entirely within your application process using the `LocalCollection` class for vector storage and search operations. Data can be stored in-memory or persisted to disk using SQLite-based storage.

Local Mode is designed for development, testing, and small-scale applications where deploying a separate Qdrant server is unnecessary. For production deployments with larger datasets, see [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md).

## Architecture Overview

**Local Mode Class Hierarchy**

```
```

Sources: [qdrant\_client/local/qdrant\_local.py38-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L38-L67) [qdrant\_client/local/async\_qdrant\_local.py38-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/async_qdrant_local.py#L38-L67) [qdrant\_client/local/local\_collection.py93-148](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L93-L148)

## Initialization

Local Mode initialization creates either `QdrantLocal` or `AsyncQdrantLocal` instances based on the provided location parameter:

**QdrantLocal Constructor**

```
```

**Storage Modes:**

- **In-memory**: `location=":memory:"` - Data exists only during application lifetime
- **Persistent**: `location="path/to/directory"` - Data persisted to disk with SQLite storage

**Initialization Process:**

1. Set `persistent = location != ":memory:"`
2. Initialize empty collections dictionary: `self.collections: dict[str, LocalCollection] = {}`
3. If persistent, load metadata from `meta.json` and create `LocalCollection` instances
4. Acquire file lock to prevent concurrent access
5. Load existing vector data into memory

Sources: [qdrant\_client/local/qdrant\_local.py51-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L51-L67) [qdrant\_client/local/qdrant\_local.py94-141](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L94-L141)

## Storage Architecture

**QdrantLocal Data Structures**

```
```

**LocalCollection Vector Storage:**

- `vectors: dict[str, NumpyArray]` - Dense vectors indexed by name
- `sparse_vectors: dict[str, list[SparseVector]]` - Sparse vectors with indices/values
- `multivectors: dict[str, list[NumpyArray]]` - Multi-vector collections
- `payload: list[models.Payload]` - Point payloads indexed by internal ID
- `ids: dict[ExtendedPointId, int]` - External ID to internal index mapping
- `deleted: NumpyArray` - Boolean array tracking deleted points

Sources: [qdrant\_client/local/qdrant\_local.py51-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L51-L67) [qdrant\_client/local/local\_collection.py100-148](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L100-L148)

## Vector Storage Implementation

**LocalCollection Vector Type Resolution**

```
```

**Vector Storage Details:**

- **Dense vectors**: `np.zeros((0, params.size), dtype=np.float32)` initialized per vector name
- **Sparse vectors**: `list[SparseVector]` with `indices` and `values` arrays
- **Multivectors**: `list[NumpyArray]` where each point can have multiple vectors
- **Deleted tracking**: `deleted_per_vector: dict[str, NumpyArray]` tracks deletions per vector type

**Vector Name Resolution:**

- `DEFAULT_VECTOR_NAME = ""` used for anonymous vectors
- `_all_vectors_keys` combines all vector type names for unified access

Sources: [qdrant\_client/local/local\_collection.py112-140](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L112-L140) [qdrant\_client/local/local\_collection.py150-169](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L150-L169) [qdrant\_client/local/local\_collection.py81](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L81-L81)

## Storage Persistence

**File-based Persistence Architecture**

```
```

**Persistence Components:**

- **meta.json**: Contains collection configurations and aliases
- **Collection directories**: `{location}/collection/{collection_name}/`
- **File locking**: Uses `portalocker` with `EXCLUSIVE|NON_BLOCKING` flags
- **CollectionPersistence**: Handles SQLite-based storage per collection

**Lock File Management:**

```
```

Sources: [qdrant\_client/local/qdrant\_local.py94-141](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L94-L141) [qdrant\_client/local/local\_collection.py143-148](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L143-L148) [qdrant\_client/local/local\_collection.py204-280](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L204-L280)

**Data Loading Process:**

1. `_load()` reads `meta.json` and creates collections
2. `load_vectors()` populates in-memory data structures from disk
3. Vector data organized by type: dense, sparse, and multivectors
4. Payload and ID mappings loaded into list and dictionary structures

## Performance Considerations

**Size Thresholds:**

- `LARGE_DATA_THRESHOLD = 20_000` points triggers performance warnings
- `LocalCollection.LARGE_DATA_THRESHOLD = 20_000` used for collection-level warnings

**Warning Implementation:**

```
```

**Performance Characteristics:**

- All data stored in memory for fast access
- No indexing structures (HNSW, etc.) - uses brute force search
- Suitable for development, testing, and small datasets
- Payload filtering uses `calculate_payload_mask()` for each query

Sources: [qdrant\_client/local/qdrant\_local.py49](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L49-L49) [qdrant\_client/local/qdrant\_local.py114-123](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L114-L123) [qdrant\_client/local/local\_collection.py98](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L98-L98)

## Search and Retrieval

**LocalCollection Search Implementation**

```
```

**Search Method Signature:**

```
```

**Query Processing Flow:**

1. `_resolve_query_vector_name()` determines vector type and name
2. Distance calculation based on vector type (dense/sparse/multi)
3. `_payload_and_non_deleted_mask()` applies filters
4. Results sorted by score and limited
5. `ScoredPoint` objects constructed with payload and vectors

Sources: [qdrant\_client/local/local\_collection.py533-701](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L533-L701) [qdrant\_client/local/local\_collection.py282-332](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L282-L332) [qdrant\_client/local/local\_collection.py499-523](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/local_collection.py#L499-L523)

## Feature Parity with Remote Mode

**Implemented Operations in QdrantLocal:**

| Operation Category    | Methods                                                                                                        | Implementation Status |
| --------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------- |
| Collection Management | `create_collection()`, `delete_collection()`, `get_collection()`, `collection_exists()`, `update_collection()` | ✅ Full                |
| Point Operations      | `upsert()`, `delete()`, `retrieve()`, `update_vectors()`, `delete_vectors()`                                   | ✅ Full                |
| Search Operations     | `search()`, `search_batch()`, `search_groups()`, `search_matrix_*()`                                           | ✅ Full                |
| Advanced Search       | `query_points()`, `query_batch_points()`, `query_points_groups()`                                              | ✅ Full                |
| Recommendation        | `recommend()`, `recommend_batch()`, `recommend_groups()`                                                       | ✅ Full                |
| Discovery             | `discover()`, `discover_batch()`                                                                               | ✅ Full                |
| Payload Operations    | `set_payload()`, `overwrite_payload()`, `delete_payload()`, `clear_payload()`                                  | ✅ Full                |
| Aliases               | `update_collection_aliases()`, `get_aliases()`, `get_collection_aliases()`                                     | ✅ Full                |
| Pagination            | `scroll()`, `count()`, `facet()`                                                                               | ✅ Full                |
| Batch Operations      | `batch_update_points()`                                                                                        | ✅ Full                |

**Unsupported Operations:**

- Payload indexes: `create_payload_index()`, `delete_payload_index()` (warnings only)
- Snapshots: All snapshot operations raise `NotImplementedError`
- Sharding: `create_shard_key()`, `delete_shard_key()` raise `NotImplementedError`
- Locks: `lock_storage()`, `unlock_storage()` raise `NotImplementedError`

**Congruence Testing:** Tests in `test_query.py` verify identical behavior between local and remote modes using `compare_client_results()` function.

Sources: [qdrant\_client/local/qdrant\_local.py773-1165](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L773-L1165) [tests/congruence\_tests/test\_query.py804-826](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/congruence_tests/test_query.py#L804-L826)

## Concurrency and Threading

**File Locking Mechanism:**

```
```

**SQLite Thread Safety:**

- Default: SQLite connections use `check_same_thread=True`
- Override: `force_disable_check_same_thread=True` parameter
- Passed to: `CollectionPersistence(location, force_disable_check_same_thread)`

**Concurrency Limitations:**

- **Process-level**: File locking prevents multiple processes from accessing same directory
- **Thread-level**: Single SQLite connection per collection, optional thread check bypass
- **Recommended**: Use Qdrant server for multi-user/multi-process scenarios

**Error Handling:**

```
```

Sources: [qdrant\_client/local/qdrant\_local.py126-141](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L126-L141) [qdrant\_client/local/qdrant\_local.py51-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L51-L67)

## Async Implementation

**AsyncQdrantLocal Class:**

```
```

**Async vs Sync Implementation:**

- **Shared**: Both use the same `LocalCollection` class for actual operations
- **Difference**: Async methods have `async def` signatures and `await` keywords
- **Persistence**: Same file locking and SQLite mechanisms
- **Performance**: No actual async I/O benefits since operations are in-memory

**Method Signatures:**

```
```

**Usage Pattern:**

```
```

Sources: [qdrant\_client/local/async\_qdrant\_local.py38-67](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/async_qdrant_local.py#L38-L67) [qdrant\_client/local/async\_qdrant\_local.py179-207](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/async_qdrant_local.py#L179-L207)

## When to Use Local Mode vs Remote Mode

| Scenario                          | Recommended Mode |
| --------------------------------- | ---------------- |
| Development & testing             | Local Mode       |
| Small applications (<20K vectors) | Local Mode       |
| Embedded applications             | Local Mode       |
| Production systems                | Remote Mode      |
| Large datasets                    | Remote Mode      |
| Multi-user access                 | Remote Mode      |
| High query throughput             | Remote Mode      |

Sources: [qdrant\_client/local/qdrant\_local.py38-47](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/qdrant_local.py#L38-L47)

## Conclusion

Local Mode provides a convenient way to use Qdrant's vector search capabilities without deploying a separate server. It's ideal for development, testing, and small-scale applications. The API is designed to be compatible with Remote Mode, allowing for easy migration when scaling up.

For larger datasets, higher throughput requirements, or multi-user scenarios, it's recommended to switch to a full Qdrant server deployment as described in [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Local Mode](#local-mode.md)
- [Architecture Overview](#architecture-overview.md)
- [Initialization](#initialization.md)
- [Storage Architecture](#storage-architecture.md)
- [Vector Storage Implementation](#vector-storage-implementation.md)
- [Storage Persistence](#storage-persistence.md)
- [Performance Considerations](#performance-considerations.md)
- [Search and Retrieval](#search-and-retrieval.md)
- [Feature Parity with Remote Mode](#feature-parity-with-remote-mode.md)
- [Concurrency and Threading](#concurrency-and-threading.md)
- [Async Implementation](#async-implementation.md)
- [When to Use Local Mode vs Remote Mode](#when-to-use-local-mode-vs-remote-mode.md)
- [Conclusion](#conclusion.md)
