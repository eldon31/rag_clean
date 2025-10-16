Implementation Details | qdrant/qdrant-client | DeepWiki

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

# Implementation Details

Relevant source files

- [qdrant\_client/local/geo.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py)
- [qdrant\_client/local/payload\_filters.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py)
- [qdrant\_client/local/payload\_value\_extractor.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py)
- [tests/fixtures/filters.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/fixtures/filters.py)
- [tests/fixtures/payload.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/fixtures/payload.py)

This document covers the internal implementation details of the qdrant-client library's core systems, including payload filtering, value extraction, and geographic operations. These components provide the foundation for local vector database operations and query processing.

For information about the overall client architecture, see [Client Architecture](qdrant/qdrant-client/2-client-architecture.md). For details about search operations that use these systems, see [Search Operations](qdrant/qdrant-client/3.1-search-operations.md). For payload filtering usage patterns, see [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md).

## Payload Filtering Architecture

The payload filtering system provides comprehensive condition evaluation for both local and remote operations. The system supports boolean logic, range queries, text matching, geographic constraints, and nested object filtering.

### Core Filter Components

```
```

The filtering system processes `models.Filter` objects through a hierarchical evaluation structure. The main entry point `check_filter()` coordinates boolean logic operators (`must`, `must_not`, `should`, `min_should`) which delegate to specific condition evaluators.

**Sources:** [qdrant\_client/local/payload\_filters.py275-312](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L275-L312)

### Condition Evaluation Flow

```
```

The `check_condition()` function dispatches to specialized handlers based on condition type. Each handler implements the specific logic for its condition category.

**Sources:** [qdrant\_client/local/payload\_filters.py166-226](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L166-L226)

## Value Extraction System

The value extraction system provides flexible access to nested payload data using JSON path expressions. It supports array indexing, wildcard operations, and deep object traversal.

### JSON Path Processing

```
```

The `value_by_key()` function supports complex path expressions for accessing nested data structures. The `flat` parameter controls whether list values are flattened or preserved as arrays.

**Sources:** [qdrant\_client/local/payload\_value\_extractor.py11-81](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py#L11-L81)

### Value Extraction Process

```
```

The extraction process recursively traverses the payload structure, handling different data types and accumulating results based on the flattening mode.

**Sources:** [qdrant\_client/local/payload\_value\_extractor.py32-80](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py#L32-L80)

## Geographic Operations

The geographic operations system provides distance calculations and spatial containment checks for location-based filtering.

### Distance Calculation

```
```

The `geo_distance()` function implements the Haversine formula for calculating great-circle distances between two points on Earth's surface.

**Sources:** [qdrant\_client/local/geo.py7-29](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py#L7-L29)

### Polygon Containment

```
```

The polygon containment system uses ray casting to determine if a point lies within a polygon, supporting both exterior boundaries and interior holes.

**Sources:** [qdrant\_client/local/geo.py45-91](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py#L45-L91)

## Integration Architecture

The implementation systems work together to provide comprehensive filtering and data access capabilities for the local vector database.

### System Integration

```
```

The integration architecture shows how filtering, value extraction, and geographic operations combine to process queries efficiently. The `calculate_payload_mask()` function coordinates all systems to produce boolean masks for result filtering.

**Sources:** [qdrant\_client/local/payload\_filters.py315-333](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L315-L333)

### Performance Considerations

| Component                  | Optimization                  | Implementation                             |
| -------------------------- | ----------------------------- | ------------------------------------------ |
| `calculate_payload_mask()` | Vectorized boolean operations | Uses NumPy arrays for mask generation      |
| `value_by_key()`           | Path parsing caching          | JSON path items parsed once per key        |
| `geo_distance()`           | Mathematical optimization     | Direct Haversine implementation            |
| `check_condition()`        | Early termination             | Short-circuit evaluation for boolean logic |

The implementation prioritizes performance through vectorized operations, caching strategies, and efficient algorithms for common operations.

**Sources:** [qdrant\_client/local/payload\_filters.py320-333](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L320-L333) [qdrant\_client/local/payload\_value\_extractor.py11-28](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py#L11-L28) [qdrant\_client/local/geo.py7-29](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py#L7-L29)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Implementation Details](#implementation-details.md)
- [Payload Filtering Architecture](#payload-filtering-architecture.md)
- [Core Filter Components](#core-filter-components.md)
- [Condition Evaluation Flow](#condition-evaluation-flow.md)
- [Value Extraction System](#value-extraction-system.md)
- [JSON Path Processing](#json-path-processing.md)
- [Value Extraction Process](#value-extraction-process.md)
- [Geographic Operations](#geographic-operations.md)
- [Distance Calculation](#distance-calculation.md)
- [Polygon Containment](#polygon-containment.md)
- [Integration Architecture](#integration-architecture.md)
- [System Integration](#system-integration.md)
- [Performance Considerations](#performance-considerations.md)
