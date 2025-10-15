Configuration Options | qdrant/mcp-server-qdrant | DeepWiki

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

# Configuration Options

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/settings.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py)

This page details all configuration options available for the mcp-server-qdrant. The server's behavior can be customized entirely through environment variables that map to internal settings classes. This page documents all supported environment variables, their purposes, default values, and usage patterns.

For information about installation and deployment methods, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md), and for details about client integration, see [Client Integration](qdrant/mcp-server-qdrant/3.2-client-integration.md).

## Configuration System Overview

The mcp-server-qdrant configuration is organized into three logical groups, each managed by a dedicated settings class:

1. **Qdrant Connection Settings**: Configure how the server connects to Qdrant vector database
2. **Embedding Provider Settings**: Configure which embedding model to use
3. **Tool Settings**: Customize the descriptions of the MCP tools

## Core Settings Classes

The configuration system is implemented through three Pydantic settings classes that map environment variables to typed Python objects:

```
```

**Figure: Settings Class Hierarchy**

Sources: [src/mcp\_server\_qdrant/settings.py19-63](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L63)

## Environment Variables Reference

The following table lists all environment variables that can be used to configure the server:

| Environment Variable     | Description                       | Default Value                            | Settings Class            | Required |
| ------------------------ | --------------------------------- | ---------------------------------------- | ------------------------- | -------- |
| `QDRANT_URL`             | URL of the Qdrant server          | None                                     | QdrantSettings            | Yes\*    |
| `QDRANT_API_KEY`         | API key for the Qdrant server     | None                                     | QdrantSettings            | No       |
| `COLLECTION_NAME`        | Name of the default collection    | None                                     | QdrantSettings            | Yes      |
| `QDRANT_LOCAL_PATH`      | Path to local Qdrant database     | None                                     | QdrantSettings            | Yes\*    |
| `QDRANT_SEARCH_LIMIT`    | Maximum number of search results  | 10                                       | QdrantSettings            | No       |
| `QDRANT_READ_ONLY`       | Run in read-only mode             | False                                    | QdrantSettings            | No       |
| `EMBEDDING_PROVIDER`     | Embedding provider to use         | "fastembed"                              | EmbeddingProviderSettings | No       |
| `EMBEDDING_MODEL`        | Name of the embedding model       | "sentence-transformers/all-MiniLM-L6-v2" | EmbeddingProviderSettings | No       |
| `TOOL_STORE_DESCRIPTION` | Custom description for store tool | See below                                | ToolSettings              | No       |
| `TOOL_FIND_DESCRIPTION`  | Custom description for find tool  | See below                                | ToolSettings              | No       |

\* Either `QDRANT_URL` or `QDRANT_LOCAL_PATH` must be provided, but not both.

Sources: [src/mcp\_server\_qdrant/settings.py19-63](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L63) [README.md39-54](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L54)

### Default Tool Descriptions

The default tool descriptions are defined in [src/mcp\_server\_qdrant/settings.py8-16](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L8-L16):

For `TOOL_STORE_DESCRIPTION`:

```
Keep the memory for later use, when you are asked to remember something.
```

For `TOOL_FIND_DESCRIPTION`:

```
Look up memories in Qdrant. Use this tool when you need to:
 - Find memories by their content
 - Access memories for further analysis
 - Get some personal information about the user
```

Sources: [src/mcp\_server\_qdrant/settings.py8-16](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L8-L16)

## Configuration Flow

The following diagram illustrates how environment variables flow through the system to configure its behavior:

```
```

**Figure: Configuration Flow Through System Components**

Sources: [src/mcp\_server\_qdrant/settings.py19-63](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/settings.py#L19-L63) [README.md39-54](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L54)

## Configuration Examples

### Basic Qdrant Cloud Configuration

```
```

### Local Qdrant Configuration

```
```

### In-Memory Configuration (for Testing)

```
```

### Custom Embedding Model Configuration

```
```

Sources: [README.md62-70](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L62-L70) [README.md112-152](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L112-L152)

## Configuration Use Cases

### Customizing Tool Descriptions for Code Search

Customizing the tool descriptions can adapt the server for specific use cases, such as code search:

```
```

Sources: [README.md166-178](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L166-L178)

## Integration with Deployment Methods

The following diagram shows how configuration options integrate with different deployment methods:

```
```

**Figure: Configuration Integration with Deployment Methods**

Sources: [README.md59-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L59-L147) [README.md156-187](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L156-L187)

## Configuration Method Evolution

> \[!IMPORTANT] Command-line arguments are not supported anymore! Please use environment variables for all configuration.

All configuration must be done through environment variables. The system previously supported command-line arguments, but this approach has been deprecated in favor of environment variables for consistency across deployment methods.

Sources: [README.md56-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L56-L57)

## Important Constraints

1. You cannot provide both `QDRANT_URL` and `QDRANT_LOCAL_PATH` at the same time.
2. If no `COLLECTION_NAME` is provided, the server will require it as a parameter to the tools.
3. For production use with Qdrant Cloud, both `QDRANT_URL` and `QDRANT_API_KEY` should be provided.

Sources: [README.md54](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L54-L54)

## Client-Specific Configuration

### Claude Desktop Configuration

Add the following to your `claude_desktop_config.json` file:

```
```

Sources: [README.md118-130](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L118-L130)

### VS Code Configuration

Add the following to your VS Code settings or `.vscode/mcp.json` file:

```
```

Sources: [README.md356-386](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L356-L386)

## Development Configuration

When developing or testing the server, you can use the MCP inspector:

```
```

This runs the server with an in-memory Qdrant database and opens the MCP inspector in your browser for interactive testing.

Sources: [README.md444-447](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L444-L447)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Configuration Options](#configuration-options.md)
- [Configuration System Overview](#configuration-system-overview.md)
- [Core Settings Classes](#core-settings-classes.md)
- [Environment Variables Reference](#environment-variables-reference.md)
- [Default Tool Descriptions](#default-tool-descriptions.md)
- [Configuration Flow](#configuration-flow.md)
- [Configuration Examples](#configuration-examples.md)
- [Basic Qdrant Cloud Configuration](#basic-qdrant-cloud-configuration.md)
- [Local Qdrant Configuration](#local-qdrant-configuration.md)
- [In-Memory Configuration (for Testing)](#in-memory-configuration-for-testing.md)
- [Custom Embedding Model Configuration](#custom-embedding-model-configuration.md)
- [Configuration Use Cases](#configuration-use-cases.md)
- [Customizing Tool Descriptions for Code Search](#customizing-tool-descriptions-for-code-search.md)
- [Integration with Deployment Methods](#integration-with-deployment-methods.md)
- [Configuration Method Evolution](#configuration-method-evolution.md)
- [Important Constraints](#important-constraints.md)
- [Client-Specific Configuration](#client-specific-configuration.md)
- [Claude Desktop Configuration](#claude-desktop-configuration.md)
- [VS Code Configuration](#vs-code-configuration.md)
- [Development Configuration](#development-configuration.md)
