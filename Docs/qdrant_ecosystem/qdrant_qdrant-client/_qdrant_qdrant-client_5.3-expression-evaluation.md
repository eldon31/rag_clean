Expression Evaluation | qdrant/qdrant-client | DeepWiki

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

- [qdrant\_client/embed/\_inspection\_cache.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/embed/_inspection_cache.py)
- [qdrant\_client/hybrid/formula.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py)
- [tests/fixtures/expressions.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/fixtures/expressions.py)

## Purpose and Scope

This document covers the expression evaluation system used in Qdrant's hybrid search and formula queries. The system provides a comprehensive framework for evaluating complex mathematical, geographical, and conditional expressions that can reference point scores, payload values, and external variables. This evaluation system is primarily used in hybrid search scenarios where custom scoring formulas need to be applied to search results.

For information about payload filtering conditions, see [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md). For details about the type inspection system that detects inference objects, see [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md).

## System Architecture

The expression evaluation system is built around a recursive evaluation engine that processes a tree of expression objects. Each expression type has specific evaluation logic that can reference point data, scores from multiple search stages, and external defaults.

```
```

Sources: [qdrant\_client/hybrid/formula.py19-26](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L19-L26) [qdrant\_client/hybrid/formula.py266-298](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L266-L298) [qdrant\_client/hybrid/formula.py245-263](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L245-L263)

## Core Expression Types

### Mathematical Expressions

The system supports a comprehensive set of mathematical operations that can be combined recursively to create complex formulas.

```
```

Sources: [qdrant\_client/hybrid/formula.py38-49](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L38-L49) [qdrant\_client/hybrid/formula.py51-55](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L51-L55) [qdrant\_client/hybrid/formula.py68-89](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L68-L89) [qdrant\_client/hybrid/formula.py101-116](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L101-L116) [qdrant\_client/hybrid/formula.py118-150](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L118-L150)

### Variable Resolution System

Variables in expressions can reference two types of data: payload fields and search scores from different stages.

| Variable Type   | Pattern                     | Example                     | Resolution                    |
| --------------- | --------------------------- | --------------------------- | ----------------------------- |
| Payload Field   | `"field.name"`              | `"price"`, `"nested.value"` | Extracted from point payload  |
| Score Reference | `"$score"` or `"$score[n]"` | `"$score"`, `"$score[1]"`   | Retrieved from search results |

```
```

Sources: [qdrant\_client/hybrid/formula.py301-331](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L301-L331) [qdrant\_client/hybrid/formula.py266-298](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L266-L298) [qdrant\_client/hybrid/formula.py245-263](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L245-L263)

## Decay Functions

Decay functions provide sophisticated scoring mechanisms that decrease based on distance from a target value. Three types are supported:

### Linear Decay

```
score = max(0, -λ * |x - target| + 1)
where λ = (1 - midpoint) / scale
```

### Exponential Decay

```
score = exp(λ * |x - target|)
where λ = ln(midpoint) / scale
```

### Gaussian Decay

```
score = exp(λ * (x - target)²)
where λ = ln(midpoint) / scale²
```

```
```

Sources: [qdrant\_client/hybrid/formula.py186-211](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L186-L211) [qdrant\_client/hybrid/formula.py216-242](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L216-L242) [qdrant\_client/hybrid/formula.py13-16](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L13-L16)

## Geographical and Datetime Expressions

### Geographical Distance Calculation

The `GeoDistance` expression calculates the distance between two geographical points using the haversine formula.

```
```

Sources: [qdrant\_client/hybrid/formula.py152-166](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L152-L166) [qdrant\_client/local/geo.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/geo.py)

### Datetime Expressions

Two types of datetime expressions are supported:

| Type                    | Purpose                  | Example                                |
| ----------------------- | ------------------------ | -------------------------------------- |
| `DatetimeExpression`    | Literal datetime values  | `{"datetime": "2023-01-01T00:00:00Z"}` |
| `DatetimeKeyExpression` | Payload field references | `{"datetime_key": "created_at"}`       |

Sources: [qdrant\_client/hybrid/formula.py168-184](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L168-L184) [qdrant\_client/local/datetime\_utils.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/local/datetime_utils.py)

## Error Handling and Validation

The expression evaluation system includes comprehensive error handling for mathematical edge cases and invalid inputs.

### Mathematical Error Handling

```
```

Sources: [qdrant\_client/hybrid/formula.py80-89](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L80-L89) [qdrant\_client/hybrid/formula.py96-99](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L96-L99) [qdrant\_client/hybrid/formula.py133-139](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L133-L139) [qdrant\_client/hybrid/formula.py334-335](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L334-L335)

### Validation Functions

The system includes several validation functions to ensure data integrity:

- `is_number()`: Validates that a value is a numeric type (excluding boolean)
- `raise_non_finite_error()`: Provides consistent error reporting for mathematical errors
- Domain validation for decay parameters (midpoint and scale ranges)

Sources: [qdrant\_client/hybrid/formula.py338-339](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L338-L339) [qdrant\_client/hybrid/formula.py235-240](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L235-L240)

## Testing Infrastructure

The expression evaluation system includes comprehensive test fixtures for generating random expressions and validating functionality.

```
```

Sources: [tests/fixtures/expressions.py8-111](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/fixtures/expressions.py#L8-L111) [qdrant\_client/hybrid/formula.py342-370](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L342-L370)

## Integration with Search System

The expression evaluation system is integrated with Qdrant's hybrid search capabilities, allowing complex scoring formulas to be applied to search results across multiple stages.

```
```

Sources: [qdrant\_client/hybrid/formula.py19-26](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/hybrid/formula.py#L19-L26) [qdrant\_client/conversions/common\_types.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/qdrant_client/conversions/common_types.py)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Expression Evaluation](#expression-evaluation.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [System Architecture](#system-architecture.md)
- [Core Expression Types](#core-expression-types.md)
- [Mathematical Expressions](#mathematical-expressions.md)
- [Variable Resolution System](#variable-resolution-system.md)
- [Decay Functions](#decay-functions.md)
- [Linear Decay](#linear-decay.md)
- [Exponential Decay](#exponential-decay.md)
- [Gaussian Decay](#gaussian-decay.md)
- [Geographical and Datetime Expressions](#geographical-and-datetime-expressions.md)
- [Geographical Distance Calculation](#geographical-distance-calculation.md)
- [Datetime Expressions](#datetime-expressions.md)
- [Error Handling and Validation](#error-handling-and-validation.md)
- [Mathematical Error Handling](#mathematical-error-handling.md)
- [Validation Functions](#validation-functions.md)
- [Testing Infrastructure](#testing-infrastructure.md)
- [Integration with Search System](#integration-with-search-system.md)
