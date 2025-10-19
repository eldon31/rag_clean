Generics and Forward References | pydantic/pydantic | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[pydantic/pydantic](https://github.com/pydantic/pydantic "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 11 October 2025 ([76ef0b](https://github.com/pydantic/pydantic/commits/76ef0b08))

- [Overview](pydantic/pydantic/1-overview.md)
- [Core Model System](pydantic/pydantic/2-core-model-system.md)
- [BaseModel](pydantic/pydantic/2.1-basemodel.md)
- [Field System](pydantic/pydantic/2.2-field-system.md)
- [Model Configuration](pydantic/pydantic/2.3-model-configuration.md)
- [Type System](pydantic/pydantic/3-type-system.md)
- [Constrained Types](pydantic/pydantic/3.1-constrained-types.md)
- [Network Types](pydantic/pydantic/3.2-network-types.md)
- [TypeAdapter](pydantic/pydantic/3.3-typeadapter.md)
- [Generics and Forward References](pydantic/pydantic/3.4-generics-and-forward-references.md)
- [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md)
- [Validators](pydantic/pydantic/4.1-validators.md)
- [Serializers](pydantic/pydantic/4.2-serializers.md)
- [JSON Conversion](pydantic/pydantic/4.3-json-conversion.md)
- [Schema Generation](pydantic/pydantic/5-schema-generation.md)
- [Core Schema Generation](pydantic/pydantic/5.1-core-schema-generation.md)
- [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md)
- [Advanced Features](pydantic/pydantic/6-advanced-features.md)
- [Dataclass Support](pydantic/pydantic/6.1-dataclass-support.md)
- [Function Validation](pydantic/pydantic/6.2-function-validation.md)
- [RootModel and Computed Fields](pydantic/pydantic/6.3-rootmodel-and-computed-fields.md)
- [Plugin System](pydantic/pydantic/6.4-plugin-system.md)
- [Development and Deployment](pydantic/pydantic/7-development-and-deployment.md)
- [Testing Framework](pydantic/pydantic/7.1-testing-framework.md)
- [CI/CD Pipeline](pydantic/pydantic/7.2-cicd-pipeline.md)
- [Documentation System](pydantic/pydantic/7.3-documentation-system.md)
- [Versioning and Dependencies](pydantic/pydantic/7.4-versioning-and-dependencies.md)
- [Migration and Compatibility](pydantic/pydantic/8-migration-and-compatibility.md)
- [V1 to V2 Migration](pydantic/pydantic/8.1-v1-to-v2-migration.md)
- [Backported Modules](pydantic/pydantic/8.2-backported-modules.md)

Menu

# Generics and Forward References

Relevant source files

- [pydantic/\_internal/\_dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_dataclasses.py)
- [pydantic/\_internal/\_fields.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_fields.py)
- [pydantic/\_internal/\_generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_generics.py)
- [pydantic/\_internal/\_typing\_extra.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_typing_extra.py)
- [pydantic/dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/dataclasses.py)
- [pydantic/generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/generics.py)
- [tests/test\_dataclasses.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_dataclasses.py)
- [tests/test\_forward\_ref.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_forward_ref.py)
- [tests/test\_generics.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_generics.py)
- [tests/test\_typing.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_typing.py)

This page documents Pydantic's implementation of generic models and forward references, which are advanced typing features that enhance model reusability and enable self-referential data structures. These features are essential parts of Pydantic's type system, complementing the fundamental types covered in [Constrained Types](pydantic/pydantic/3.1-constrained-types.md) and [Network Types](pydantic/pydantic/3.2-network-types.md).

## Generic Models

Generic models in Pydantic allow you to create model templates that can be parameterized with different types, similar to how generic classes work in languages like Java or C#. This enables type-safe reuse of model structures across different data types.

### Basic Usage

To create a generic model, inherit from both `BaseModel` and `Generic[T]` (where `T` is a type variable):

```
```

When you parameterize a generic model with a specific type (e.g., `Container[int]`), Pydantic creates a specialized model class with validation specifically for that type.

```
```

Sources:

- `tests/test_generics.py:83-92`
- `tests/test_generics.py:580-648`

### Implementation Mechanics

When you parameterize a generic model like `Container[int]`, several key processes occur:

1. **Type Substitution**: All occurrences of the type variable `T` in the model are replaced with the concrete type `int`
2. **Class Creation**: A new subclass of the original model is created with the concrete types
3. **Caching**: The created class is cached to ensure the same parameterization returns the same class

```
```

Sources:

- `pydantic/_internal/_generics.py:106-150`
- `pydantic/_internal/_generics.py:246-340`
- `pydantic/_internal/_generics.py:439-547`

### Type Substitution in Depth

The `replace_types` function recursively traverses type annotations and substitutes type variables with concrete types:

```
```

This handles complex nested types like `List[Dict[str, T]]` → `List[Dict[str, int]]` when substituting `T` with `int`.

Sources:

- `pydantic/_internal/_generics.py:178-195`
- `pydantic/_internal/_generics.py:246-340`

### Caching System

Pydantic employs a sophisticated caching mechanism to ensure that:

1. The same parameterization of a generic model returns the same class
2. Memory usage is optimized by using weak references
3. The system can handle recursive generic types

```
```

The caching system uses a two-stage lookup to optimize performance:

1. An "early" cache key for quick lookups
2. A "late" cache key that handles more complex equivalence relationships

Sources:

- `pydantic/_internal/_generics.py:42-57`
- `pydantic/_internal/_generics.py:97-97`
- `pydantic/_internal/_generics.py:439-547`
- `tests/test_generics.py:352-456`

## Forward References

Forward references allow referencing types that haven't been fully defined yet, which is essential for recursive models and handling circular dependencies.

### Basic Usage

In Python, forward references are typically written as string literals:

```
```

This creates a recursive data structure where a `Person` can have a list of `Person` objects as friends.

```
```

Sources:

- `tests/test_forward_ref.py:128-166`
- `tests/test_forward_ref.py:261-289`

### Forward Reference Resolution

When Pydantic encounters a string annotation, it:

1. Records the original string annotation
2. Marks the field as incomplete (`_complete = False`)
3. Attempts to resolve the reference when needed

The resolution process happens:

- **Automatically** during validation if a model has unresolved references
- **Explicitly** when calling `Model.model_rebuild()`

```
```

Sources:

- `pydantic/_internal/_fields.py:78-282`
- `pydantic/_internal/_fields.py:300-337`
- `tests/test_forward_ref.py:42-75`

### Type Evaluation

Pydantic evaluates string annotations by:

1. Using the `eval_type` function to convert the string to a type object
2. Searching for the referenced type in appropriate namespaces
3. Handling failure gracefully if a type can't be resolved immediately

```
```

Sources:

- `pydantic/_internal/_typing_extra.py:290-457`
- `pydantic/_internal/_typing_extra.py:209-271`

### Recursive Models and Circular Dependencies

Pydantic efficiently handles recursive models (like trees or graphs) and circular dependencies between models by:

1. Detecting recursion during schema generation
2. Using special schema references to avoid infinite recursion
3. Auto-rebuilding models as necessary to resolve circular dependencies

```
```

Sources:

- `tests/test_forward_ref.py:111-166`
- `tests/test_forward_ref.py:205-260`
- `tests/test_forward_ref.py:261-411`
- `tests/test_forward_ref.py:697-714`

## Combining Generics and Forward References

### Generic Models with Forward References

Combining generics and forward references enables powerful type patterns:

```
```

When this forward reference is resolved, the type variable `T` is correctly substituted with the concrete type.

```
```

Sources:

- `tests/test_generics.py:664-794`
- `pydantic/_internal/_fields.py:327-328`
- `pydantic/_internal/_generics.py:396-437`

### Handling Recursive Generic Types

For recursive generic types, Pydantic implements special handling to prevent infinite recursion:

```
```

This allows for properly handling complex structures like trees where nodes can contain other nodes of the same type.

Sources:

- `pydantic/_internal/_generics.py:396-437`
- `tests/test_generics.py:458-486`

## Advanced Usage Patterns

### Bounded Type Variables

You can restrict the allowed types by using bounded type variables:

```
```

This ensures that only types compatible with the bound can be used as parameters.

Sources:

- `tests/test_generics.py:881-912`

### Default Type Arguments

Generic models can have default type arguments using Python 3.12+ syntax:

```
```

This allows users to only specify some type arguments while others default to predefined types.

Sources:

- `tests/test_generics.py:297-349`

### Partial Specialization

You can partially specialize a generic model with multiple type variables:

```
```

Partial specialization allows for creating intermediate template models.

Sources:

- `tests/test_generics.py:797-878`

## Implementation Details

### Generic Model Creation Internals

When a generic model is parameterized, the `create_generic_submodel` function creates a new subclass:

```
```

The created model contains metadata about its generic origin, arguments, and parameters to support further operations.

Sources:

- `pydantic/_internal/_generics.py:100-150`
- `pydantic/_internal/_generics.py:343-393`

### Forward Reference Handling Internals

The handling of forward references is primarily implemented in the `_fields.py` and `_typing_extra.py` modules:

```
```

The resolution process uses Python's introspection capabilities to find the right namespace context for evaluating the string annotations.

Sources:

- `pydantic/_internal/_fields.py:78-167`
- `pydantic/_internal/_fields.py:300-337`
- `pydantic/_internal/_typing_extra.py:290-464`

## Conclusion

Generics and forward references are powerful features in Pydantic that enable complex type patterns while maintaining type safety. They allow for:

1. Creating reusable model templates with generics
2. Building recursive data structures with forward references
3. Combining both to create sophisticated type systems

Understanding these features is essential for advanced Pydantic usage, especially when building models with complex relationships or when creating reusable model libraries.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Generics and Forward References](#generics-and-forward-references.md)
- [Generic Models](#generic-models.md)
- [Basic Usage](#basic-usage.md)
- [Implementation Mechanics](#implementation-mechanics.md)
- [Type Substitution in Depth](#type-substitution-in-depth.md)
- [Caching System](#caching-system.md)
- [Forward References](#forward-references.md)
- [Basic Usage](#basic-usage-1.md)
- [Forward Reference Resolution](#forward-reference-resolution.md)
- [Type Evaluation](#type-evaluation.md)
- [Recursive Models and Circular Dependencies](#recursive-models-and-circular-dependencies.md)
- [Combining Generics and Forward References](#combining-generics-and-forward-references.md)
- [Generic Models with Forward References](#generic-models-with-forward-references.md)
- [Handling Recursive Generic Types](#handling-recursive-generic-types.md)
- [Advanced Usage Patterns](#advanced-usage-patterns.md)
- [Bounded Type Variables](#bounded-type-variables.md)
- [Default Type Arguments](#default-type-arguments.md)
- [Partial Specialization](#partial-specialization.md)
- [Implementation Details](#implementation-details.md)
- [Generic Model Creation Internals](#generic-model-creation-internals.md)
- [Forward Reference Handling Internals](#forward-reference-handling-internals.md)
- [Conclusion](#conclusion.md)
