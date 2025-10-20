qdrant-find Tool | qdrant/mcp-server-qdrant | DeepWiki

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

# qdrant-find Tool

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/mcp\_server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py)

## Purpose and Overview

The `qdrant-find` tool is a core component of the mcp-server-qdrant system that enables semantic search capabilities within a Qdrant vector database. This tool allows LLM applications to retrieve information previously stored in the database based on the semantic meaning of a query, rather than exact keyword matching.

This page documents the `qdrant-find` tool specifically. For information about storing information in the Qdrant database, see the [qdrant-store Tool](qdrant/mcp-server-qdrant/4.1-qdrant-store-tool.md) page.

Sources: [README.md31-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L31-L37)

## How It Works

The `qdrant-find` tool operates by converting natural language queries into vector embeddings, then using these embeddings to perform similarity searches against stored information in the Qdrant vector database.

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py100-138](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L100-L138)

### Technical Implementation

The `qdrant-find` tool is implemented in the `QdrantMCPServer` class through either the `find` or `find_with_default_collection` functions, depending on whether a default collection name is configured.

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py100-131](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L100-L131) [README.md31-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L31-L37)

## Parameters

The `qdrant-find` tool accepts the following parameters:

| Parameter         | Type   | Required    | Description                                                                               |
| ----------------- | ------ | ----------- | ----------------------------------------------------------------------------------------- |
| `query`           | string | Yes         | The natural language query to search for                                                  |
| `collection_name` | string | Conditional | Name of the collection to search in. Required only if no default collection is configured |

Sources: [src/mcp\_server\_qdrant/mcp\_server.py101-104](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L101-L104) [README.md33-36](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L33-L36)

## Return Value

The tool returns a list of strings containing:

1. A header message indicating the query that was used
2. Zero or more formatted entries that match the query
3. If no entries are found, a message indicating no information was found

Each entry is formatted by the `format_entry` method, which by default returns a string in the following format:

```
<entry><content>The content of the entry</content><metadata>{"metadata_field": "value"}</metadata></entry>
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py51-56](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L51-L56) [src/mcp\_server\_qdrant/mcp\_server.py119-131](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L119-L131)

## Configuration

The `qdrant-find` tool can be configured using several environment variables:

| Environment Variable    | Description                                | Default                                  |
| ----------------------- | ------------------------------------------ | ---------------------------------------- |
| `QDRANT_URL`            | URL of the Qdrant server                   | None                                     |
| `QDRANT_API_KEY`        | API key for the Qdrant server              | None                                     |
| `COLLECTION_NAME`       | Default collection name to use             | None                                     |
| `QDRANT_SEARCH_LIMIT`   | Maximum number of search results to return | (Not specified in provided files)        |
| `TOOL_FIND_DESCRIPTION` | Custom description for the find tool       | (Default in settings.py)                 |
| `EMBEDDING_PROVIDER`    | Embedding provider to use                  | `fastembed`                              |
| `EMBEDDING_MODEL`       | Name of the embedding model to use         | `sentence-transformers/all-MiniLM-L6-v2` |

Sources: [README.md43-52](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L43-L52)

## Usage Examples

### Basic Usage with Default Collection

When a default collection is configured:

```
qdrant-find("How to implement a binary search algorithm?")
```

### Specifying a Collection

When no default collection is configured, or to override the default:

```
qdrant-find("How to implement a binary search algorithm?", "code-examples")
```

### Integration in Cursor/Windsurf

The `qdrant-find` tool can be customized for specific use cases, such as code search in Cursor/Windsurf, by modifying the tool description:

```
```

Sources: [README.md166-178](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L166-L178)

## Implementation Details

The search operation is performed through several key steps:

1. The query string is converted to a vector embedding using the configured embedding provider
2. The QdrantConnector's search method is called with the query, collection name, and limit
3. The Qdrant database performs a similarity search on the vector embeddings
4. Matching entries are returned to the server
5. The server formats each entry using the format\_entry method
6. A list of formatted strings is returned to the client

Sources: [src/mcp\_server\_qdrant/mcp\_server.py100-138](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L100-L138)

## Related Components

The `qdrant-find` tool relies on two key components:

1. **EmbeddingProvider**: Responsible for converting text queries into vector embeddings
2. **QdrantConnector**: Handles communication with the Qdrant database, including vector similarity searches

For more information about the embedding system, see the [Embedding System](qdrant/mcp-server-qdrant/2.2-embedding-system.md) page. For more details about the QdrantConnector, see the [QdrantConnector Reference](qdrant/mcp-server-qdrant/5-qdrantconnector-reference.md) page.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py37-45](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L37-L45) [README.md19-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L19-L37)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [qdrant-find Tool](#qdrant-find-tool.md)
- [Purpose and Overview](#purpose-and-overview.md)
- [How It Works](#how-it-works.md)
- [Technical Implementation](#technical-implementation.md)
- [Parameters](#parameters.md)
- [Return Value](#return-value.md)
- [Configuration](#configuration.md)
- [Usage Examples](#usage-examples.md)
- [Basic Usage with Default Collection](#basic-usage-with-default-collection.md)
- [Specifying a Collection](#specifying-a-collection.md)
- [Integration in Cursor/Windsurf](#integration-in-cursorwindsurf.md)
- [Implementation Details](#implementation-details.md)
- [Related Components](#related-components.md)
