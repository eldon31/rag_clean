QdrantConnector Reference | qdrant/mcp-server-qdrant | DeepWiki

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

# QdrantConnector Reference

Relevant source files

- [src/mcp\_server\_qdrant/qdrant.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py)
- [tests/test\_qdrant\_integration.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py)

## Purpose and Scope

This technical reference document provides detailed information about the `QdrantConnector` class, which serves as the interface between the MCP Server and the Qdrant vector database. The connector handles vector storage, retrieval, and collection management. For information about embedding generation, see [Embedding Providers](qdrant/mcp-server-qdrant/6-embedding-providers.md).

Sources: [src/mcp\_server\_qdrant/qdrant.py24-149](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L24-L149)

## Class Overview

```
```

The `QdrantConnector` class is responsible for:

- Managing connections to the Qdrant database
- Creating and managing collections
- Storing entries with their vector embeddings
- Performing semantic similarity searches

Sources: [src/mcp\_server\_qdrant/qdrant.py24-49](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L24-L49)

## Initialization Parameters

The `QdrantConnector` constructor accepts the following parameters:

| Parameter            | Type                | Description                                     | Required |
| -------------------- | ------------------- | ----------------------------------------------- | -------- |
| `qdrant_url`         | `Optional[str]`     | URL of the Qdrant server (remote or `:memory:`) | No       |
| `qdrant_api_key`     | `Optional[str]`     | API key for the Qdrant server                   | No       |
| `collection_name`    | `Optional[str]`     | Default collection name                         | No       |
| `embedding_provider` | `EmbeddingProvider` | Provider for generating embeddings              | Yes      |
| `qdrant_local_path`  | `Optional[str]`     | Path for local Qdrant storage                   | No       |

Sources: [src/mcp\_server\_qdrant/qdrant.py35-49](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L35-L49)

## Entry Model

The `Entry` class represents a single item stored in the Qdrant collection:

```
```

| Field      | Type                 | Description                                            |
| ---------- | -------------------- | ------------------------------------------------------ |
| `content`  | `str`                | The text content to be embedded and stored             |
| `metadata` | `Optional[Metadata]` | Additional data associated with the content (optional) |

Sources: [src/mcp\_server\_qdrant/qdrant.py15-21](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L15-L21)

## Core Operations

### Store Operation

The `store` method adds an entry to a Qdrant collection.

```
```

**Method Signature**:

```
```

**Parameters**:

- `entry`: The `Entry` object containing content and optional metadata
- `collection_name`: Optional name of the collection (uses default if not specified)

**Implementation Details**:

1. Determines the collection name to use
2. Ensures the collection exists (creates it if needed)
3. Generates embeddings for the entry content
4. Creates a point with unique ID, embedding vectors, and payload
5. Stores the point in the Qdrant collection

Sources: [src/mcp\_server\_qdrant/qdrant.py59-87](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L59-L87)

### Search Operation

The `search` method performs semantic similarity search in a Qdrant collection.

```
```

**Method Signature**:

```
```

**Parameters**:

- `query`: The text query to search for
- `collection_name`: Optional name of the collection (uses default if not specified)
- `limit`: Maximum number of results to return (default: 10)

**Returns**:

- List of `Entry` objects containing the matched content and metadata

**Implementation Details**:

1. Determines the collection name to use
2. Checks if the collection exists (returns empty list if not)
3. Generates embeddings for the query
4. Performs vector similarity search in the Qdrant collection
5. Converts the results to `Entry` objects

Sources: [src/mcp\_server\_qdrant/qdrant.py89-126](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L89-L126)

## Collection Management

### Get Collection Names

Retrieves all collection names from the Qdrant server.

**Method Signature**:

```
```

**Returns**:

- List of collection names as strings

Sources: [src/mcp\_server\_qdrant/qdrant.py51-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L51-L57)

### Ensure Collection Exists

Internal method to create a collection if it doesn't exist.

**Method Signature**:

```
```

**Implementation Details**:

1. Checks if the collection exists

2. If not, creates a new collection with vector configuration:

   - Vector size from the embedding provider
   - Vector name from the embedding provider
   - COSINE distance metric

Sources: [src/mcp\_server\_qdrant/qdrant.py128-148](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L128-L148)

## Integration with System Architecture

The `QdrantConnector` is positioned between the QdrantMCPServer and the Qdrant vector database:

```
```

Sources: [src/mcp\_server\_qdrant/qdrant.py24-149](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L24-L149)

## Usage Examples

### Basic Store and Search

```
```

Sources: [tests/test\_qdrant\_integration.py32-48](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L32-L48)

### Working with Multiple Collections

```
```

Sources: [tests/test\_qdrant\_integration.py192-225](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L192-L225)

### Handling Metadata

```
```

Sources: [tests/test\_qdrant\_integration.py113-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L113-L147)

## Qdrant Connection Options

The `QdrantConnector` supports multiple ways to connect to Qdrant:

| Connection Type            | Configuration                                                          |
| -------------------------- | ---------------------------------------------------------------------- |
| Remote Qdrant Server       | Set `qdrant_url` to server URL and optionally provide `qdrant_api_key` |
| Local Qdrant Instance      | Set `qdrant_local_path` to a directory path                            |
| In-Memory Qdrant (testing) | Set `qdrant_url` to `:memory:`                                         |

Sources: [src/mcp\_server\_qdrant/qdrant.py47-49](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L47-L49) [tests/test\_qdrant\_integration.py16-29](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L16-L29)

## Technical Implementation Details

### Point Storage Structure

When storing entries, `QdrantConnector` creates points with this structure:

| Field     | Description                                             |
| --------- | ------------------------------------------------------- |
| `id`      | Unique UUID generated for each point                    |
| `vector`  | Dictionary mapping vector name to embedding array       |
| `payload` | Contains "document" (the content) and "metadata" fields |

Sources: [src/mcp\_server\_qdrant/qdrant.py76-87](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L76-L87)

### Collection Creation Parameters

When creating a new collection, these parameters are used:

| Parameter       | Value                            |
| --------------- | -------------------------------- |
| Vector size     | Obtained from embedding provider |
| Vector name     | Obtained from embedding provider |
| Distance metric | COSINE (similarity measure)      |

Sources: [src/mcp\_server\_qdrant/qdrant.py140-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L140-L147)

## Best Practices

1. **Default Collection**: Set a default collection name during initialization to avoid passing it with every operation.
2. **Error Handling**: The connector handles non-existent collections gracefully by returning empty results.
3. **Metadata Usage**: Use metadata for storing additional information that doesn't need to be embedded.
4. **Collection Design**: Create separate collections for logically distinct data sets.

Sources: [src/mcp\_server\_qdrant/qdrant.py59-126](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L59-L126) [tests/test\_qdrant\_integration.py192-239](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_qdrant_integration.py#L192-L239)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [QdrantConnector Reference](#qdrantconnector-reference.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Class Overview](#class-overview.md)
- [Initialization Parameters](#initialization-parameters.md)
- [Entry Model](#entry-model.md)
- [Core Operations](#core-operations.md)
- [Store Operation](#store-operation.md)
- [Search Operation](#search-operation.md)
- [Collection Management](#collection-management.md)
- [Get Collection Names](#get-collection-names.md)
- [Ensure Collection Exists](#ensure-collection-exists.md)
- [Integration with System Architecture](#integration-with-system-architecture.md)
- [Usage Examples](#usage-examples.md)
- [Basic Store and Search](#basic-store-and-search.md)
- [Working with Multiple Collections](#working-with-multiple-collections.md)
- [Handling Metadata](#handling-metadata.md)
- [Qdrant Connection Options](#qdrant-connection-options.md)
- [Technical Implementation Details](#technical-implementation-details.md)
- [Point Storage Structure](#point-storage-structure.md)
- [Collection Creation Parameters](#collection-creation-parameters.md)
- [Best Practices](#best-practices.md)
