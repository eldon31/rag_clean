Hybrid Search | qdrant/qdrant-client | DeepWiki

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

# Expression Evaluation

Relevant source files

- [qdrant\_client/hybrid/\_\_init\_\_.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/__init__.py)
- [qdrant\_client/hybrid/fusion.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/fusion.py)
- [qdrant\_client/hybrid/test\_reranking.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/test_reranking.py)

## Purpose and Scope

This document details the expression evaluation system in the Qdrant client library. This system provides a powerful way to perform mathematical operations, create custom scoring functions, filter data, and transform values within queries. For information about batch operations, see [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md), and for local inference capabilities, see [Local Inference](qdrant/qdrant-client/4.4-local-inference.md).

## Overview

The expression evaluation system allows users to create complex mathematical and logical expressions that can be used in various operations, particularly for custom relevance scoring in hybrid search. Expressions support access to vector similarity scores, payload fields, filtering conditions, and a wide range of mathematical operations.

```
```

Sources: [qdrant\_client/hybrid/formula.py19-214](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L19-L214) [qdrant\_client/embed/\_inspection\_cache.py1-244](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/_inspection_cache.py#L1-L244)

## Expression Types

The Qdrant client supports a rich set of expression types that can be combined to create complex scoring and filtering logic.

### Basic Expression Types

| Expression Type  | Description               | Example                                                                 |
| ---------------- | ------------------------- | ----------------------------------------------------------------------- |
| Constant         | Numeric literals          | `0.5`, `42`                                                             |
| Variable         | Payload field or score    | `price`, `$score`                                                       |
| Filter Condition | Boolean condition         | `FieldCondition(key="category", match=MatchValue(value="electronics"))` |
| Mathematical     | Mathematical operations   | `MultExpression`, `SumExpression`, `DivExpression`                      |
| Geo              | Geo-distance calculations | `GeoDistance`                                                           |
| Datetime         | Date/time operations      | `DatetimeExpression`, `DatetimeKeyExpression`                           |
| Decay            | Decay functions           | `LinDecayExpression`, `ExpDecayExpression`, `GaussDecayExpression`      |

### Mathematical Operations

```
```

Sources: [qdrant\_client/hybrid/formula.py35-150](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L35-L150) [qdrant\_client/embed/\_inspection\_cache.py245-310](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/_inspection_cache.py#L245-L310)

### Decay Functions

Decay functions are used to transform distances (numeric, geographic, temporal) into relevance scores that decrease with distance from a target value.

```
```

Sources: [qdrant\_client/hybrid/formula.py186-211](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L186-L211) [qdrant\_client/embed/\_inspection\_cache.py360-444](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/_inspection_cache.py#L360-L444)

## Expression Evaluation Process

The expression evaluation system recursively processes expressions to produce a final numeric value.

```
```

Sources: [qdrant\_client/hybrid/formula.py19-214](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L19-L214) [qdrant\_client/hybrid/formula.py266-298](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L266-L298)

## Using Variables in Expressions

### Payload Fields

Any field from a point's payload can be referenced by its path:

- Simple field: `"price"`
- Nested field: `"product.details.price"`
- Array element: `"features[0]"`
- Array elements: `"features[]"`

### Score Variables

Score variables provide access to vector similarity scores:

- `$score` or `$score[0]`: First vector similarity score
- `$score[1]`: Second vector similarity score (in multi-vector queries)
- `$score[n]`: Nth vector similarity score

```
```

Sources: [qdrant\_client/hybrid/formula.py245-298](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L245-L298) [qdrant\_client/local/payload\_value\_extractor.py1-92](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_value_extractor.py#L1-L92)

## Filter Expressions

Expressions can include filter conditions that evaluate to 1.0 (true) or 0.0 (false). These conditions support the same rich filtering capabilities as Qdrant's regular filters.

```
```

Sources: [qdrant\_client/local/payload\_filters.py165-313](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/payload_filters.py#L165-L313) [qdrant\_client/embed/\_inspection\_cache.py573-735](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/_inspection_cache.py#L573-L735)

## Practical Examples

### Example 1: Combining Vector Search with Price Factor

```
```

### Example 2: Distance-Based Decay Function

```
```

## Expression Evaluation Implementation

The core expression evaluation logic resides in the `evaluate_expression` function. This function recursively processes expressions based on their type, handling constants, variables, conditions, and operations.

### Key Components

- **Expression Parser**: Converts expression objects into calculations
- **Variable Resolver**: Retrieves values from payloads or scores
- **Condition Evaluator**: Processes filter conditions
- **Mathematical Evaluator**: Performs mathematical operations
- **Error Handling**: Handles edge cases like division by zero

Sources: [qdrant\_client/hybrid/formula.py19-214](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L19-L214) [qdrant\_client/hybrid/formula.py216-242](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L216-L242)

## Expression Safety and Limitations

The expression evaluation system includes several safety measures:

1. **Non-finite Value Detection**: Functions like `div`, `sqrt`, `pow`, `exp`, `log10`, and `ln` check for non-finite results and raise appropriate errors.

2. **Division by Zero Handling**: The `DivExpression` allows specifying a `by_zero_default` value to handle division by zero gracefully.

3. **Decay Function Validation**: Decay functions validate parameters like `midpoint` (must be between 0 and 1) and `scale` (must be positive).

```
```

Sources: [qdrant\_client/hybrid/formula.py83-89](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L83-L89) [qdrant\_client/hybrid/formula.py235-240](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L235-L240)

## Integration with Search and Query Operations

The expression evaluation system integrates with Qdrant's search functionality through:

1. **Formula Queries**: Apply a scoring formula to search results
2. **Fusion Queries**: Combine multiple search strategies with custom weights

These operations leverage the expression evaluation system to compute final relevance scores for returned points.

Sources: [qdrant\_client/hybrid/formula.py19-33](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L19-L33)

## Conclusion

Qdrant's expression evaluation system provides a powerful and flexible way to customize search relevance, perform calculations, and create complex scoring functions. By combining vector similarity with other factors like numerical properties, text matches, and geo-distance, users can create highly tailored search experiences that balance multiple relevance signals.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Expression Evaluation](#expression-evaluation.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Expression Types](#expression-types.md)
- [Basic Expression Types](#basic-expression-types.md)
- [Mathematical Operations](#mathematical-operations.md)
- [Decay Functions](#decay-functions.md)
- [Expression Evaluation Process](#expression-evaluation-process.md)
- [Using Variables in Expressions](#using-variables-in-expressions.md)
- [Payload Fields](#payload-fields.md)
- [Score Variables](#score-variables.md)
- [Filter Expressions](#filter-expressions.md)
- [Practical Examples](#practical-examples.md)
- [Example 1: Combining Vector Search with Price Factor](#example-1-combining-vector-search-with-price-factor.md)
- [Example 2: Distance-Based Decay Function](#example-2-distance-based-decay-function.md)
- [Expression Evaluation Implementation](#expression-evaluation-implementation.md)
- [Key Components](#key-components.md)
- [Expression Safety and Limitations](#expression-safety-and-limitations.md)
- [Integration with Search and Query Operations](#integration-with-search-and-query-operations.md)
- [Conclusion](#conclusion.md)
