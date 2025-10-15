Configuration System | qdrant/mcp-server-qdrant | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 20 April 2025 ([a3ab0b](https://github.com/qdrant/mcp-server-qdrant/commits/a3ab0b96))

- [Overview](qdrant/mcp-server-qdrant/1-overview.md)
- [Architecture](qdrant/mcp-server-qdrant/2-architecture.md)
- [Core Components](qdrant/mcp-server-qdrant/2.1-core-components.md)
- [Embedding System](qdrant/mcp-server-qdrant/2.2-embedding-system.md)
- [Configuration System](qdrant/mcp-server-qdrant/2.3-configuration-system.md)
- [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md)
- [Configuration Options](qdrant/mcp-server-qdrant/3.1-configuration-options.md)
- [Client Integration](qdrant/mcp-server-qdrant/3.2-client-integration.md)
- [API Reference](qdrant/mcp-server-qdrant/4-api-reference.md)
- [qdrant-store Tool](qdrant/mcp-server-qdrant/4.1-qdrant-store-tool.md)
- [qdrant-find Tool](qdrant/mcp-server-qdrant/4.2-qdrant-find-tool.md)
- [QdrantConnector Reference](qdrant/mcp-server-qdrant/5-qdrantconnector-reference.md)
- [Embedding Providers](qdrant/mcp-server-qdrant/6-embedding-providers.md)
- [Development Guide](qdrant/mcp-server-qdrant/7-development-guide.md)

Menu

# Configuration System

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/settings.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py)
- [tests/test\_settings.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_settings.py)

The mcp-server-qdrant configuration system provides a flexible way to customize the server's behavior through environment variables. This page describes how configuration works in the codebase, including the settings classes, environment variables, and how they interact with the rest of the system.

For installation options and deployment guidelines, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md), and for detailed configuration options, see [Configuration Options](qdrant/mcp-server-qdrant/3.1-configuration-options.md).

## Configuration Overview

The configuration system in mcp-server-qdrant is built on top of Pydantic's settings management, which automatically loads values from environment variables. The system uses three main settings classes to organize configuration by functional area:

1. `QdrantSettings` - Configuration for the Qdrant vector database connection
2. `EmbeddingProviderSettings` - Configuration for the embedding model
3. `ToolSettings` - Configuration for the tool descriptions and behaviors

### Configuration Flow

```
```

Sources: [src/mcp\_server\_qdrant/settings.py1-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L1-L64) [README.md39-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L57)

## Settings Classes

The configuration system is based on three Pydantic settings classes that map environment variables to typed Python attributes:

### Class Structure

```
```

Sources: [src/mcp\_server\_qdrant/settings.py19-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L64)

### QdrantSettings

The `QdrantSettings` class manages all configuration related to the Qdrant vector database connection:

```
```

Sources: [src/mcp\_server\_qdrant/settings.py49-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L49-L64)

### EmbeddingProviderSettings

The `EmbeddingProviderSettings` class manages configuration for the embedding model used to convert text to vector embeddings:

```
```

Sources: [src/mcp\_server\_qdrant/settings.py34-47](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L34-L47)

### ToolSettings

The `ToolSettings` class manages configuration for the MCP tool descriptions that determine how the tools are presented to LLM clients:

```
```

Sources: [src/mcp\_server\_qdrant/settings.py19-31](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L31)

## Environment Variables

The configuration system uses environment variables to configure all aspects of the server. The following table lists all supported environment variables:

| Environment Variable     | Description                                       | Default Value                            |
| ------------------------ | ------------------------------------------------- | ---------------------------------------- |
| `QDRANT_URL`             | URL of the Qdrant server                          | None                                     |
| `QDRANT_API_KEY`         | API key for the Qdrant server                     | None                                     |
| `COLLECTION_NAME`        | Name of the default collection to use             | None                                     |
| `QDRANT_LOCAL_PATH`      | Path to the local Qdrant database                 | None                                     |
| `QDRANT_SEARCH_LIMIT`    | Maximum number of results to return from searches | 10                                       |
| `QDRANT_READ_ONLY`       | Whether to operate in read-only mode              | False                                    |
| `EMBEDDING_PROVIDER`     | Embedding provider to use                         | `fastembed`                              |
| `EMBEDDING_MODEL`        | Name of the embedding model to use                | `sentence-transformers/all-MiniLM-L6-v2` |
| `TOOL_STORE_DESCRIPTION` | Custom description for the store tool             | See default in settings.py               |
| `TOOL_FIND_DESCRIPTION`  | Custom description for the find tool              | See default in settings.py               |

Sources: [README.md39-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L57) [src/mcp\_server\_qdrant/settings.py8-16](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L8-L16) [src/mcp\_server\_qdrant/settings.py19-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L64)

## Configuration Loading and Usage

The configuration system automatically loads values from environment variables when the settings classes are instantiated. This process happens at server startup.

```
```

Sources: [tests/test\_settings.py14-107](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_settings.py#L14-L107)

## Configuration Validation

The settings classes leverage Pydantic's validation system to ensure that values are of the correct type and format. When an invalid configuration is provided, the server will fail to start with a detailed error message indicating which value was invalid and why.

Key validation features:

1. Type checking - ensures values are of the correct type (string, integer, boolean, etc.)
2. Enum validation - ensures that values like `provider_type` are one of the allowed options
3. Default values - provides sensible defaults for optional settings

Sources: [src/mcp\_server\_qdrant/settings.py19-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L64) [tests/test\_settings.py14-107](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_settings.py#L14-L107)

## Configuration Best Practices

### Minimal Configuration

At minimum, you need to configure the Qdrant connection:

```
```

Sources: [README.md65-70](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L65-L70) [README.md133-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L133-L147)

### Custom Tool Descriptions

To customize how the tools appear to LLM applications, you can set custom tool descriptions:

```
```

This can help guide the LLM on how best to use the tools for specific use cases, such as code retrieval or knowledge management.

Sources: [README.md164-177](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L164-L177) [tests/test\_settings.py76-107](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_settings.py#L76-L107)

### Deployment-Specific Configuration

Different deployment methods may have different ways of providing environment variables:

1. **Direct environment variables** - Used with `uvx` and direct execution
2. **Docker environment variables** - Passed to Docker containers using `-e` flags
3. **Configuration files** - Used with Claude Desktop and VS Code

Each method serves the same purpose - providing values to the settings classes through environment variables.

Sources: [README.md61-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L61-L147) [README.md266-305](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L266-L305)

## Integration with System Components

The settings classes are used to initialize and configure the core system components:

```
```

Sources: [README.md19-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L19-L37)

## Summary

The configuration system in mcp-server-qdrant provides a flexible, type-safe way to customize the server's behavior through environment variables. The three main settings classes - `QdrantSettings`, `EmbeddingProviderSettings`, and `ToolSettings` - organize configuration by functional area and automatically load values from environment variables using Pydantic's settings system.

This approach makes it easy to configure the server for different environments and use cases without modifying code, whether running locally with `uvx`, in a Docker container, or integrated with tools like Claude Desktop or VS Code.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Configuration System](#configuration-system.md)
- [Configuration Overview](#configuration-overview.md)
- [Configuration Flow](#configuration-flow.md)
- [Settings Classes](#settings-classes.md)
- [Class Structure](#class-structure.md)
- [QdrantSettings](#qdrantsettings.md)
- [EmbeddingProviderSettings](#embeddingprovidersettings.md)
- [ToolSettings](#toolsettings.md)
- [Environment Variables](#environment-variables.md)
- [Configuration Loading and Usage](#configuration-loading-and-usage.md)
- [Configuration Validation](#configuration-validation.md)
- [Configuration Best Practices](#configuration-best-practices.md)
- [Minimal Configuration](#minimal-configuration.md)
- [Custom Tool Descriptions](#custom-tool-descriptions.md)
- [Deployment-Specific Configuration](#deployment-specific-configuration.md)
- [Integration with System Components](#integration-with-system-components.md)
- [Summary](#summary.md)
