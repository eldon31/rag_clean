Core Operations | qdrant/qdrant-client | DeepWiki

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

# Core Operations

Relevant source files

- [qdrant\_client/async\_qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/async_qdrant_client.py)
- [qdrant\_client/qdrant\_client.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py)

This document covers the fundamental operations for working with vectors, collections, and points in Qdrant through the Python client library. Core operations provide the primary interface for data manipulation, retrieval, and management in both local and remote Qdrant instances.

For advanced search capabilities including hybrid search and FastEmbed integration, see [Advanced Features](qdrant/qdrant-client/4-advanced-features.md). For information about the underlying client architecture and backend implementations, see [Client Architecture](qdrant/qdrant-client/2-client-architecture.md).

## Operation Categories

The qdrant-client provides three main categories of core operations:

| Category                  | Purpose                                                          | Key Operations                                             |
| ------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| **Search Operations**     | Vector similarity search, recommendations, and data discovery    | `query_points`, `query_batch_points`, `scroll`, `count`    |
| **Collection Management** | Create, configure, and manage vector collections                 | `create_collection`, `delete_collection`, `get_collection` |
| **Point Operations**      | CRUD operations for individual points and their vectors/payloads | `upsert`, `retrieve`, `delete`, `update_vectors`           |

## Universal Query Interface

The `query_points` method serves as the universal endpoint for all search operations, replacing older specialized methods like `search`, `recommend`, and `discover`:

```
```

**Sources:** [qdrant\_client/qdrant\_client.py437-610](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L437-L610) [qdrant\_client/qdrant\_client.py393-435](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L393-L435)

## Search Operations Flow

Search operations follow a consistent pattern from query resolution through result processing:

```
```

**Sources:** [qdrant\_client/qdrant\_client.py554-610](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L554-L610) [qdrant\_client/qdrant\_client.py421-435](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L421-L435)

## Point Lifecycle Operations

Point operations manage the complete lifecycle of vector points from creation to deletion:

```
```

**Sources:** [qdrant\_client/qdrant\_client.py1565-1641](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L1565-L1641) [qdrant\_client/qdrant\_client.py1642-1695](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L1642-L1695) [qdrant\_client/qdrant\_client.py1747-1803](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L1747-L1803)

## Collection Management Operations

Collection management provides comprehensive control over vector storage configuration:

```
```

**Sources:** [qdrant\_client/qdrant\_client.py2233-2320](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L2233-L2320) [qdrant\_client/qdrant\_client.py2164-2212](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L2164-L2212) [qdrant\_client/qdrant\_client.py2084-2130](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L2084-L2130)

## Consistency and Ordering Controls

All operations support configurable consistency and ordering guarantees:

| Parameter     | Type              | Values                                   | Purpose                           |
| ------------- | ----------------- | ---------------------------------------- | --------------------------------- |
| `consistency` | `ReadConsistency` | `int`, `'majority'`, `'quorum'`, `'all'` | Controls replica read consistency |
| `ordering`    | `WriteOrdering`   | `'weak'`, `'medium'`, `'strong'`         | Controls write operation ordering |
| `wait`        | `bool`            | `True`, `False`                          | Wait for operation completion     |
| `timeout`     | `int`             | seconds                                  | Override global timeout           |

## Error Handling and Retries

Operations include built-in error handling and retry mechanisms:

```
```

**Sources:** [qdrant\_client/qdrant\_client.py262](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L262-L262) [qdrant\_client/qdrant\_client.py369](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L369-L369) [qdrant\_client/qdrant\_client.py552](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L552-L552)

## Batch Operations Optimization

Batch operations provide optimized performance for bulk data processing:

```
```

**Sources:** [qdrant\_client/qdrant\_client.py2466-2529](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L2466-L2529) [qdrant\_client/qdrant\_client.py2531-2602](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L2531-L2602) [qdrant\_client/qdrant\_client.py2044-2082](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/qdrant_client.py#L2044-L2082)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Core Operations](#core-operations.md)
- [Operation Categories](#operation-categories.md)
- [Universal Query Interface](#universal-query-interface.md)
- [Search Operations Flow](#search-operations-flow.md)
- [Point Lifecycle Operations](#point-lifecycle-operations.md)
- [Collection Management Operations](#collection-management-operations.md)
- [Consistency and Ordering Controls](#consistency-and-ordering-controls.md)
- [Error Handling and Retries](#error-handling-and-retries.md)
- [Batch Operations Optimization](#batch-operations-optimization.md)
