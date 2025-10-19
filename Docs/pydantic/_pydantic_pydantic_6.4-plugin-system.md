Plugin System | pydantic/pydantic | DeepWiki

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

# Plugin System

Relevant source files

- [pydantic/\_internal/\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py)
- [pydantic/functional\_serializers.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_serializers.py)
- [pydantic/functional\_validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/functional_validators.py)
- [pydantic/plugin/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py)
- [pydantic/plugin/\_schema\_validator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py)
- [pydantic/root\_model.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/root_model.py)
- [pydantic/type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py)
- [pydantic/validate\_call\_decorator.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validate_call_decorator.py)
- [tests/test\_plugins.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py)
- [tests/test\_type\_adapter.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_type_adapter.py)
- [tests/test\_validate\_call.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_validate_call.py)

This document describes Pydantic's plugin system, which allows external code to hook into the validation lifecycle through event handlers. Plugins can observe validation inputs, outputs, errors, and exceptions for all validation methods (`validate_python`, `validate_json`, `validate_strings`).

For information about custom validators and serializers at the field or model level, see [Validators](pydantic/pydantic/4.1-validators.md) and [Serializers](pydantic/pydantic/4.2-serializers.md). For type-level customization hooks, see [Core Schema Generation](pydantic/pydantic/5.1-core-schema-generation.md).

## Overview

The plugin system provides a way to instrument Pydantic's validation process without modifying models or types. Plugins implement the `PydanticPluginProtocol` and receive callbacks at key points during validation:

- **on\_enter**: Before validation begins
- **on\_success**: After successful validation
- **on\_error**: When validation fails
- **on\_exception**: When an unexpected exception occurs

Plugins are invoked automatically whenever a `SchemaValidator` is created for BaseModels, TypeAdapters, dataclasses, `validate_call`, or `create_model`.

**Sources:** [pydantic/plugin/\_\_init\_\_.py1-194](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L1-L194)

## Plugin Protocol

### PydanticPluginProtocol

```
```

Plugins must implement a single method that returns event handlers for each of the three validation modes:

| Parameter          | Type                 | Description                                                                                |
| ------------------ | -------------------- | ------------------------------------------------------------------------------------------ |
| `schema`           | `CoreSchema`         | The pydantic-core schema for validation                                                    |
| `schema_type`      | `Any`                | The original Python type (e.g., model class)                                               |
| `schema_type_path` | `SchemaTypePath`     | Module and name where the type was defined                                                 |
| `schema_kind`      | `SchemaKind`         | One of: `'BaseModel'`, `'TypeAdapter'`, `'dataclass'`, `'create_model'`, `'validate_call'` |
| `config`           | `CoreConfig \| None` | Core configuration for the validator                                                       |
| `plugin_settings`  | `dict[str, object]`  | Settings passed via `plugin_settings` in model config                                      |

**Sources:** [pydantic/plugin/\_\_init\_\_.py40-73](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L40-L73)

### SchemaTypePath and SchemaKind

```
```

The `SchemaTypePath` identifies where a schema was created, useful for filtering which schemas a plugin should observe. The `SchemaKind` indicates what API created the schema.

**Sources:** [pydantic/plugin/\_\_init\_\_.py30-37](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L30-L37)

## Event Handler Protocols

### Handler Lifecycle

```
```

Each handler protocol defines four callback methods. All methods have default no-op implementations, so plugins only need to implement the callbacks they care about.

**Sources:** [pydantic/plugin/\_schema\_validator.py96-126](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L96-L126)

### ValidatePythonHandlerProtocol

Handles events for `validate_python()` calls:

```
```

The `self_instance` parameter is populated when validation occurs during model `__init__`, allowing plugins to observe the model instance being initialized.

**Sources:** [pydantic/plugin/\_\_init\_\_.py110-138](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L110-L138)

### ValidateJsonHandlerProtocol

Handles events for `validate_json()` calls with JSON string/bytes input:

```
```

**Sources:** [pydantic/plugin/\_\_init\_\_.py140-166](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L140-L166)

### ValidateStringsHandlerProtocol

Handles events for `validate_strings()` calls:

```
```

**Sources:** [pydantic/plugin/\_\_init\_\_.py171-193](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/__init__.py#L171-L193)

## PluggableSchemaValidator

### Architecture

```
```

The `PluggableSchemaValidator` wraps a standard `SchemaValidator` and intercepts its validation methods. When plugins are registered, `create_schema_validator()` returns a `PluggableSchemaValidator` instead of a plain `SchemaValidator`.

**Sources:** [pydantic/plugin/\_schema\_validator.py22-52](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L22-L52) [pydantic/plugin/\_schema\_validator.py54-94](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L54-L94)

### Wrapper Construction

The `build_wrapper()` function creates wrapper methods that invoke event handlers:

| Step                 | Action                                                                   |
| -------------------- | ------------------------------------------------------------------------ |
| 1. Filter handlers   | Only include handlers with custom (non-protocol) implementations         |
| 2. Extract callbacks | Collect all `on_enter`, `on_success`, `on_error`, `on_exception` methods |
| 3. Wrap function     | Create wrapper that calls handlers at appropriate points                 |

```
```

The `filter_handlers()` function checks if a method is implemented by the plugin (not inherited from the protocol) by checking if `handler.__module__ == 'pydantic.plugin'`.

**Sources:** [pydantic/plugin/\_schema\_validator.py96-141](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L96-L141)

## Plugin Registration

### Integration Points

```
```

All schema validation entry points use `create_schema_validator()` to construct validators:

| Entry Point            | Schema Kind       | Location                                   |
| ---------------------- | ----------------- | ------------------------------------------ |
| BaseModel              | `'BaseModel'`     | Model metaclass during class creation      |
| TypeAdapter            | `'TypeAdapter'`   | `TypeAdapter._init_core_attrs()`           |
| @dataclasses.dataclass | `'dataclass'`     | Dataclass wrapper initialization           |
| @validate\_call        | `'validate_call'` | `ValidateCallWrapper._create_validators()` |
| create\_model()        | `'create_model'`  | Dynamic model creation                     |

**Sources:** [pydantic/type\_adapter.py321-330](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/type_adapter.py#L321-L330) [pydantic/\_internal/\_validate\_call.py91-104](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/_internal/_validate_call.py#L91-L104)

### Plugin Settings

Models can pass settings to plugins via the `plugin_settings` configuration:

```
```

These settings are passed to `PydanticPluginProtocol.new_schema_validator()` as the `plugin_settings` parameter, allowing plugins to customize behavior per schema.

**Sources:** [tests/test\_plugins.py68-76](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L68-L76)

## Usage Examples

### Basic Logging Plugin

```
```

**Sources:** [tests/test\_plugins.py126-165](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L126-L165)

### Stateful Plugin with Cleanup

Plugins can maintain state across validation calls:

```
```

All three lifecycle methods (`on_success`, `on_error`, `on_exception`) are called to ensure proper cleanup regardless of validation outcome.

**Sources:** [tests/test\_plugins.py217-272](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L217-L272)

### Multi-Method Plugin

Plugins can handle all three validation methods:

```
```

Each handler receives method-specific parameters in `on_enter()`. For example, `ValidateJsonHandlerProtocol.on_enter()` receives `input: str | bytes | bytearray` while `ValidatePythonHandlerProtocol.on_enter()` receives `input: Any`.

**Sources:** [tests/test\_plugins.py274-336](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L274-L336)

### Filtering by Schema Kind

Plugins can choose which schemas to observe based on `schema_kind`:

```
```

**Sources:** [tests/test\_plugins.py338-355](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L338-L355)

### Filtering by Module Path

Plugins can filter based on where types are defined:

```
```

**Sources:** [tests/test\_plugins.py357-408](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_plugins.py#L357-L408)

## Implementation Details

### Handler Method Filtering

The `filter_handlers()` function prevents calling protocol default methods:

```
```

This allows plugins to only implement the callbacks they need without performance overhead from no-op protocol defaults.

**Sources:** [pydantic/plugin/\_schema\_validator.py128-141](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L128-L141)

### Attribute Proxying

`PluggableSchemaValidator` proxies all other attributes to the wrapped `SchemaValidator`:

```
```

This ensures that `PluggableSchemaValidator` behaves identically to `SchemaValidator` for attributes like `title`, `get_default_value()`, etc.

**Sources:** [pydantic/plugin/\_schema\_validator.py92-93](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L92-L93)

### Performance Considerations

When no plugins are installed, `create_schema_validator()` returns a plain `SchemaValidator` with zero overhead. The plugin system only activates when plugins are registered via the plugin loader.

**Sources:** [pydantic/plugin/\_schema\_validator.py22-51](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/plugin/_schema_validator.py#L22-L51)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Plugin System](#plugin-system.md)
- [Overview](#overview.md)
- [Plugin Protocol](#plugin-protocol.md)
- [PydanticPluginProtocol](#pydanticpluginprotocol.md)
- [SchemaTypePath and SchemaKind](#schematypepath-and-schemakind.md)
- [Event Handler Protocols](#event-handler-protocols.md)
- [Handler Lifecycle](#handler-lifecycle.md)
- [ValidatePythonHandlerProtocol](#validatepythonhandlerprotocol.md)
- [ValidateJsonHandlerProtocol](#validatejsonhandlerprotocol.md)
- [ValidateStringsHandlerProtocol](#validatestringshandlerprotocol.md)
- [PluggableSchemaValidator](#pluggableschemavalidator.md)
- [Architecture](#architecture.md)
- [Wrapper Construction](#wrapper-construction.md)
- [Plugin Registration](#plugin-registration.md)
- [Integration Points](#integration-points.md)
- [Plugin Settings](#plugin-settings.md)
- [Usage Examples](#usage-examples.md)
- [Basic Logging Plugin](#basic-logging-plugin.md)
- [Stateful Plugin with Cleanup](#stateful-plugin-with-cleanup.md)
- [Multi-Method Plugin](#multi-method-plugin.md)
- [Filtering by Schema Kind](#filtering-by-schema-kind.md)
- [Filtering by Module Path](#filtering-by-module-path.md)
- [Implementation Details](#implementation-details.md)
- [Handler Method Filtering](#handler-method-filtering.md)
- [Attribute Proxying](#attribute-proxying.md)
- [Performance Considerations](#performance-considerations.md)
