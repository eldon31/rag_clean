Payload Filtering | qdrant/qdrant-client | DeepWiki

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

# Payload Filtering

Relevant source files

- [qdrant\_client/local/geo.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py)
- [qdrant\_client/local/payload\_filters.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py)
- [qdrant\_client/local/payload\_value\_extractor.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py)
- [tests/fixtures/filters.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/fixtures/filters.py)
- [tests/fixtures/payload.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/fixtures/payload.py)

Payload filtering is a core functionality in the Qdrant client that enables filtering vector search results based on metadata attached to vectors. This document explains how payload filtering works in the client implementation, the available filter types, and how they are processed.

For information about search operations that use these filters, see [Search Operations](qdrant/qdrant-client/3.1-search-operations.md). For details about expression evaluation involving filters, see [Expression Evaluation](qdrant/qdrant-client/4.3-hybrid-search.md).

## 1. Filter Structure Overview

Payload filters in Qdrant follow a boolean query structure similar to Elasticsearch's Query DSL. They combine conditions with boolean operators to create complex filtering expressions.

```
```

Sources: [qdrant\_client/local/payload\_filters.py275-312](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L275-L312)

### Filter Boolean Logic

A filter combines conditions using boolean logic:

| Operator     | Description                              | Implementation              |
| ------------ | ---------------------------------------- | --------------------------- |
| `must`       | All conditions must match (AND)          | `check_must` function       |
| `must_not`   | All conditions must NOT match (NOT)      | `check_must_not` function   |
| `should`     | At least one condition should match (OR) | `check_should` function     |
| `min_should` | At least N conditions should match       | `check_min_should` function |

Sources: [qdrant\_client/local/payload\_filters.py229-272](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L229-L272)

## 2. Condition Types

Conditions are the building blocks of filters. Qdrant supports various condition types to filter points based on their payload, ID, or vector existence.

### Field Conditions

Field conditions operate on specific payload fields identified by a key path. They can use various matchers:

```
```

Sources: [qdrant\_client/local/payload\_filters.py150-159](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L150-L159)

### Special Condition Types

In addition to field conditions, Qdrant supports special condition types:

| Condition Type       | Description                                  | Implementation                 |
| -------------------- | -------------------------------------------- | ------------------------------ |
| `IsEmptyCondition`   | Checks if a field is empty or doesn't exist  | `check_condition` function     |
| `IsNullCondition`    | Checks if a field is explicitly null         | `check_condition` function     |
| `HasIdCondition`     | Checks if a point ID is in the provided list | `check_condition` function     |
| `HasVectorCondition` | Checks if a point has a named vector         | `check_condition` function     |
| `NestedCondition`    | Applies a filter to nested objects           | `check_nested_filter` function |

Sources: [qdrant\_client/local/payload\_filters.py166-226](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L166-L226)

## 3. Field Matchers Implementation

### Match Condition Types

Match conditions check for equality or inclusion:

```
```

The implementation checks these conditions in the `check_match` function, which handles different types of matching operations:

| Match Type    | Implementation                       | Line Reference |
| ------------- | ------------------------------------ | -------------- |
| `MatchValue`  | Exact equality comparison            | Line 152       |
| `MatchText`   | Substring search using `in` operator | Line 154       |
| `MatchAny`    | Value membership in array            | Line 156       |
| `MatchExcept` | Value exclusion from array           | Line 158       |

Sources: [qdrant\_client/local/payload\_filters.py150-159](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L150-L159)

### Range Conditions

Range conditions filter numeric or datetime values:

```
```

The `check_range` and `check_datetime_range` functions validate whether values fall within specified ranges:

| Function                | Purpose                   | Implementation Details                     |
| ----------------------- | ------------------------- | ------------------------------------------ |
| `check_range`           | Numeric range validation  | Checks `lt`, `lte`, `gt`, `gte` conditions |
| `check_datetime_range`  | Datetime range validation | Parses datetime strings, handles timezones |
| `check_range_interface` | Dispatcher function       | Routes to appropriate range checker        |

Sources: [qdrant\_client/local/payload\_filters.py99-147](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L99-L147)

### Geo Conditions

Qdrant provides several geo-spatial filtering capabilities implemented in the `check_geo_radius`, `check_geo_bounding_box`, and `check_geo_polygon` functions:

```
```

The implementation uses mathematical algorithms implemented in separate functions:

| Geo Function             | Algorithm                  | Implementation                                           |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| `check_geo_radius`       | Haversine formula          | Calls `geo_distance` from geo module                     |
| `check_geo_bounding_box` | Coordinate bounds checking | Direct coordinate comparison with anti-meridian handling |
| `check_geo_polygon`      | Ray-casting algorithm      | Calls `boolean_point_in_polygon` from geo module         |

Sources: [qdrant\_client/local/payload\_filters.py46-96](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L46-L96) [qdrant\_client/local/geo.py7-91](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py#L7-L91)

### Values Count Condition

The values count condition filters based on the number of values in a field:

```
```

The `check_values_count` function determines whether a field has the required number of values, using the helper function `get_value_counts` to calculate actual counts:

```
```

Sources: [qdrant\_client/local/payload\_filters.py13-43](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L13-L43)

## 4. Nested Filtering

Qdrant supports filtering on nested objects and arrays using dot notation and array indexing:

```
```

The `NestedCondition` is particularly powerful as it allows applying a complete filter to each element of an array:

```
```

The `check_nested_filter` function handles nested filtering by applying the filter to each element in the specified array. It uses the `value_by_key` function from the payload value extractor module to navigate nested structures:

```
```

The `value_by_key` function supports JSON path notation with array indexing and wildcard access patterns.

Sources: [qdrant\_client/local/payload\_filters.py162-163](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L162-L163) [qdrant\_client/local/payload\_value\_extractor.py11-81](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py#L11-L81)

## 5. Filter Processing Flow

When a search request includes a filter, the filtering process follows these steps:

Filter Processing Flow Diagram

```
```

The key function in this process is `calculate_payload_mask`, which applies the filter to all payloads and returns a boolean mask that indicates which points match the filter.

Sources: [qdrant\_client/local/payload\_filters.py315-333](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L315-L333)

## 6. Performance Considerations

Payload filtering takes place after vector similarity search in the Qdrant client implementation. This means that:

1. The filter is applied to the top-k results from the vector search
2. If you need to filter first, consider using `prefiltration=True` in your search request
3. Complex filters on large result sets can impact performance

For optimal performance:

- Use simple conditions when possible
- Avoid deeply nested filters
- Consider indexing frequently filtered fields (server-side)
- For local mode, filters operate in-memory without indexing

Sources: [qdrant\_client/local/payload\_filters.py315-333](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L315-L333)

## 7. Integration with Formula Expressions

Payload filters can also be used within formula expressions to adjust scores based on payload values:

```
```

The `check_condition` function is reused in the formula expression evaluation to determine if conditions are met.

Sources: [qdrant\_client/hybrid/formula.py33-36](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L33-L36)

This integration allows for powerful hybrid search capabilities where both vector similarity and metadata influence the final ranking.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Payload Filtering](#payload-filtering.md)
- [1. Filter Structure Overview](#1-filter-structure-overview.md)
- [Filter Boolean Logic](#filter-boolean-logic.md)
- [2. Condition Types](#2-condition-types.md)
- [Field Conditions](#field-conditions.md)
- [Special Condition Types](#special-condition-types.md)
- [3. Field Matchers Implementation](#3-field-matchers-implementation.md)
- [Match Condition Types](#match-condition-types.md)
- [Range Conditions](#range-conditions.md)
- [Geo Conditions](#geo-conditions.md)
- [Values Count Condition](#values-count-condition.md)
- [4. Nested Filtering](#4-nested-filtering.md)
- [5. Filter Processing Flow](#5-filter-processing-flow.md)
- [6. Performance Considerations](#6-performance-considerations.md)
- [7. Integration with Formula Expressions](#7-integration-with-formula-expressions.md)
