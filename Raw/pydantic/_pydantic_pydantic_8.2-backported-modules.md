Backported Modules | pydantic/pydantic | DeepWiki

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

# Backported Modules

Relevant source files

- [pydantic/decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py)
- [pydantic/env\_settings.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py)
- [pydantic/schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py)
- [pydantic/typing.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py)
- [pydantic/utils.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py)
- [tests/test\_utils.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py)

## Purpose and Scope

This document covers the V1 compatibility layer provided by Pydantic V2 through backported modules. These modules (`pydantic.schema`, `pydantic.utils`, `pydantic.typing`, `pydantic.env_settings`, and `pydantic.decorator`) serve as migration shims that redirect imports from their V1 locations to appropriate V2 equivalents while issuing deprecation warnings.

For information about broader migration strategies and API changes between V1 and V2, see [V1 to V2 Migration](pydantic/pydantic/8.1-v1-to-v2-migration.md).

---

## Overview

Pydantic V2 reorganized its internal structure significantly compared to V1. To ease the transition for users with existing codebases, several commonly-imported V1 modules were preserved as "backported modules" that use the `getattr_migration` mechanism to provide backwards compatibility.

**Sources:** [pydantic/schema.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L5) [pydantic/utils.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L5) [pydantic/typing.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py#L1-L5)

---

## Migration Architecture

The backported modules use a dynamic attribute resolution mechanism to intercept imports and redirect them to their new V2 locations.

### Import Resolution Flow

```
```

**How it Works:**

1. User imports from a V1 module location (e.g., `from pydantic.schema import schema_of`)
2. Python invokes `__getattr__` on the module
3. `getattr_migration` function intercepts the attribute lookup
4. A deprecation warning is issued
5. The attribute is resolved from its new V2 location and returned

**Sources:** [pydantic/schema.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L5) [pydantic/utils.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L5)

---

## Backported Module List

All backported modules follow the same pattern: they import `getattr_migration` and assign it as their module-level `__getattr__` function.

### Module Mapping

| V1 Module               | Status     | Common Use Cases in V1                            |
| ----------------------- | ---------- | ------------------------------------------------- |
| `pydantic.schema`       | Backported | Schema generation utilities                       |
| `pydantic.utils`        | Backported | General utility functions                         |
| `pydantic.typing`       | Backported | Type annotation utilities                         |
| `pydantic.env_settings` | Backported | Environment-based settings (now separate library) |
| `pydantic.decorator`    | Backported | Decorator utilities for validation                |

**Sources:** [pydantic/schema.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L1) [pydantic/utils.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L1) [pydantic/typing.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py#L1-L1) [pydantic/env\_settings.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py#L1-L1) [pydantic/decorator.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py#L1-L1)

---

## Implementation Pattern

Each backported module uses an identical implementation pattern:

```
```

### Code Structure

All five backported modules follow this template:

```
```

**Key Components:**

- **Module docstring**: Identifies the module as a V1 backport
- **`getattr_migration` import**: Brings in the migration function from `pydantic._migration`
- **`__getattr__` assignment**: Python's special module-level attribute that is called when an attribute is not found through normal lookup

**Sources:** [pydantic/schema.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L5) [pydantic/utils.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L5) [pydantic/typing.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py#L1-L5) [pydantic/env\_settings.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py#L1-L5) [pydantic/decorator.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py#L1-L5)

---

## Specific Backported Modules

### pydantic.schema

The `schema` module in V1 contained utilities for generating JSON schemas from Pydantic models. In V2, this functionality has been reorganized.

**File Location:** [pydantic/schema.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py)

**V1 Usage Example:**

```
```

**Sources:** [pydantic/schema.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L5)

---

### pydantic.utils

The `utils` module in V1 contained various utility functions. In V2, these utilities have been moved to internal modules or replaced with new implementations.

**File Location:** [pydantic/utils.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py)

**V1 Usage Example:**

```
```

**Note:** Test utilities like `import_string` are now located in `pydantic._internal._validators`.

**Sources:** [pydantic/utils.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L5) [tests/test\_utils.py35-47](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L35-L47)

---

### pydantic.typing

The `typing` module in V1 contained type-related utilities. In V2, typing utilities have been reorganized into `pydantic._internal._typing_extra`.

**File Location:** [pydantic/typing.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py)

**V1 Usage Example:**

```
```

**Sources:** [pydantic/typing.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py#L1-L5)

---

### pydantic.env\_settings

The `env_settings` module provided the `BaseSettings` class for environment-based configuration in V1. In V2, this functionality has been moved to a separate package: `pydantic-settings`.

**File Location:** [pydantic/env\_settings.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py)

**Migration Path:**

```
```

**Sources:** [pydantic/env\_settings.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py#L1-L5)

---

### pydantic.decorator

The `decorator` module in V1 contained decorator utilities. In V2, the `@validate_call` decorator and related functionality are available directly from the main `pydantic` module.

**File Location:** [pydantic/decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py)

**V1 Usage Example:**

```
```

**Sources:** [pydantic/decorator.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py#L1-L5)

---

## getattr\_migration Mechanism

The `getattr_migration` function is the core of the backport system. It creates a custom `__getattr__` handler for a module that:

1. **Intercepts attribute access** when an attribute is not found in the module
2. **Issues deprecation warnings** to inform users that the import location is deprecated
3. **Resolves the new location** of the requested attribute in V2's structure
4. **Returns the attribute** from its new location

### Attribute Resolution Process

```
```

**Sources:** [pydantic/schema.py3-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L3-L5) [pydantic/utils.py3-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L3-L5)

---

## Usage Behavior

### Import Compatibility

When code attempts to import from a backported module location:

```
```

**Runtime Behavior:**

1. Python loads the backport module (e.g., `pydantic/utils.py`)
2. `some_utility` is not in the module's `__dict__`
3. Python calls `__getattr__('some_utility')`
4. `getattr_migration` is invoked
5. A `DeprecationWarning` is issued
6. The function resolves the new location
7. The attribute from the new location is returned

**Sources:** [pydantic/utils.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L5)

---

### Deprecation Warnings

The backport system issues deprecation warnings to encourage migration to V2 patterns. These warnings:

- Identify the deprecated import path
- Suggest the new V2 import location
- Provide context for migration

This approach allows existing code to continue working while guiding users toward V2 best practices.

**Sources:** [pydantic/schema.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L1) [pydantic/utils.py1](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L1)

---

## Migration Recommendations

### Short-term Strategy

For immediate V2 compatibility:

1. **Accept the warnings**: The backported modules allow code to run without immediate changes
2. **Plan migration**: Use deprecation warnings as a guide for what needs updating
3. **Prioritize changes**: Focus on frequently-used imports first

### Long-term Strategy

For sustainable V2 code:

1. **Remove backport dependencies**: Update imports to use V2 locations
2. **Install separate packages**: For `env_settings`, migrate to `pydantic-settings`
3. **Update to V2 APIs**: Use new V2 methods and patterns (see [V1 to V2 Migration](pydantic/pydantic/8.1-v1-to-v2-migration.md))
4. **Test thoroughly**: Ensure behavior matches expectations after migration

**Sources:** [pydantic/env\_settings.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py#L1-L5)

---

## Testing Considerations

The test suite validates utility functions that were historically part of these backported modules:

### Utility Function Tests

The test file `tests/test_utils.py` covers various utilities that were part of the V1 `utils` module:

- **`import_string`**: Dynamic module/attribute importing ([tests/test\_utils.py35-46](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L35-L46))
- **`display_as_type`**: Type representation formatting ([tests/test\_utils.py60-102](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L60-L102))
- **`lenient_issubclass`**: Safe subclass checking ([tests/test\_utils.py105-120](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L105-L120))
- **`unique_list`**: Deduplication utilities ([tests/test\_utils.py123-133](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L123-L133))
- **`ValueItems`**: Include/exclude logic for nested data ([tests/test\_utils.py136-246](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L136-L246))
- **Alias generators**: `to_camel`, `to_pascal`, `to_snake` ([tests/test\_utils.py445-523](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L445-L523))

These utilities demonstrate the types of functions that were available through `pydantic.utils` in V1 and are now accessible through internal modules in V2.

**Sources:** [tests/test\_utils.py1-528](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_utils.py#L1-L528)

---

## Summary

The backported modules provide a compatibility layer that:

- **Enables gradual migration** from Pydantic V1 to V2
- **Maintains backwards compatibility** for existing import paths
- **Issues clear warnings** to guide users toward V2 patterns
- **Uses a consistent mechanism** across all five modules (`schema`, `utils`, `typing`, `env_settings`, `decorator`)

All backported modules rely on the `getattr_migration` function to intercept attribute access and redirect to new V2 locations, making the transition smoother for users with large existing codebases.

**Sources:** [pydantic/schema.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/schema.py#L1-L5) [pydantic/utils.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/utils.py#L1-L5) [pydantic/typing.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/typing.py#L1-L5) [pydantic/env\_settings.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/env_settings.py#L1-L5) [pydantic/decorator.py1-5](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/decorator.py#L1-L5)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Backported Modules](#backported-modules.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Migration Architecture](#migration-architecture.md)
- [Import Resolution Flow](#import-resolution-flow.md)
- [Backported Module List](#backported-module-list.md)
- [Module Mapping](#module-mapping.md)
- [Implementation Pattern](#implementation-pattern.md)
- [Code Structure](#code-structure.md)
- [Specific Backported Modules](#specific-backported-modules.md)
- [pydantic.schema](#pydanticschema.md)
- [pydantic.utils](#pydanticutils.md)
- [pydantic.typing](#pydantictyping.md)
- [pydantic.env\_settings](#pydanticenv_settings.md)
- [pydantic.decorator](#pydanticdecorator.md)
- [getattr\_migration Mechanism](#getattr_migration-mechanism.md)
- [Attribute Resolution Process](#attribute-resolution-process.md)
- [Usage Behavior](#usage-behavior.md)
- [Import Compatibility](#import-compatibility.md)
- [Deprecation Warnings](#deprecation-warnings.md)
- [Migration Recommendations](#migration-recommendations.md)
- [Short-term Strategy](#short-term-strategy.md)
- [Long-term Strategy](#long-term-strategy.md)
- [Testing Considerations](#testing-considerations.md)
- [Utility Function Tests](#utility-function-tests.md)
- [Summary](#summary.md)
