qdrant-store Tool | qdrant/mcp-server-qdrant | DeepWiki

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

# qdrant-store Tool

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/mcp\_server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py)

## Purpose and Scope

The `qdrant-store` tool enables applications to store text information and optional metadata in the Qdrant vector database with semantic meaning preserved through vector embeddings. This tool is one of the two primary tools provided by the mcp-server-qdrant, with the other being the `qdrant-find` tool (see [qdrant-find Tool](qdrant/mcp-server-qdrant/4.2-qdrant-find-tool.md) for more details on retrieving stored information).

The tool's primary purpose is to create persistent memory for LLM applications by storing information that can later be retrieved based on semantic similarity rather than exact keyword matching.

Sources: [README.md22-30](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L22-L30) [src/mcp\_server\_qdrant/mcp\_server.py63-88](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L88)

## Parameters and Usage

The `qdrant-store` tool accepts the following parameters:

| Parameter         | Type   | Required    | Description                                             |
| ----------------- | ------ | ----------- | ------------------------------------------------------- |
| `information`     | string | Yes         | The text content to store in the vector database        |
| `metadata`        | JSON   | No          | Optional structured data to store alongside the content |
| `collection_name` | string | Conditional | Required only if no default collection is configured    |

### Parameter Details

- **information**: The text content that will be converted to a vector embedding and stored in Qdrant. This is the primary data that will be returned in search results.
- **metadata**: Optional JSON object containing additional structured data you want to associate with the text content. This can include tags, timestamps, source references, or any other organizational data.
- **collection\_name**: The name of the Qdrant collection in which to store the information. This parameter is conditionally required - if you've configured the server with a default collection name, this parameter will not be available.

Sources: [README.md22-30](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L22-L30) [src/mcp\_server\_qdrant/mcp\_server.py63-88](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L88)

## Implementation Flow

The following diagram illustrates how the `qdrant-store` tool processes and stores information:

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py63-88](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L88) [README.md22-30](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L22-L30)

## Internal Architecture

The following class diagram shows how the `qdrant-store` tool is implemented within the system architecture:

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py20-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L20-L169)

## Configuration Options

The behavior of the `qdrant-store` tool can be customized using several environment variables:

| Environment Variable     | Description                          | Default                                  | Effect on qdrant-store                              |
| ------------------------ | ------------------------------------ | ---------------------------------------- | --------------------------------------------------- |
| `QDRANT_URL`             | URL of the Qdrant server             | None                                     | Defines where information is stored                 |
| `QDRANT_API_KEY`         | API key for the Qdrant server        | None                                     | Authentication for storage operations               |
| `COLLECTION_NAME`        | Default collection name              | None                                     | When set, the `collection_name` parameter is hidden |
| `QDRANT_LOCAL_PATH`      | Path to local Qdrant database        | None                                     | Alternative to `QDRANT_URL` for local storage       |
| `QDRANT_READ_ONLY`       | Set server to read-only mode         | False                                    | When `true`, disables the `qdrant-store` tool       |
| `EMBEDDING_MODEL`        | Model used for generating embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Affects how text is converted to vectors            |
| `TOOL_STORE_DESCRIPTION` | Custom description for the tool      | Default in settings.py                   | Modifies how the tool appears to users              |

### Important Configuration Details

1. If `QDRANT_READ_ONLY` is set to `true`, the `qdrant-store` tool will not be available.
2. If `COLLECTION_NAME` is provided, the `collection_name` parameter will not be available to users, and all storage operations will use the default collection.
3. You cannot provide both `QDRANT_URL` and `QDRANT_LOCAL_PATH` simultaneously.

Sources: [README.md39-54](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L54) [src/mcp\_server\_qdrant/mcp\_server.py155-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L155-L169)

## Tool Registration Logic

The following flowchart illustrates how the `qdrant-store` tool is registered in the server based on configuration:

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py155-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L155-L169)

## Usage Examples

### Basic Usage

When storing simple text without metadata:

```
qdrant-store(
  information: "The Python language was created by Guido van Rossum and first released in 1991."
)
```

Response: `"Remembered: The Python language was created by Guido van Rossum and first released in 1991."`

### With Metadata

Storing information with optional metadata:

```
qdrant-store(
  information: "Python uses indentation for scope such as loops and functions",
  metadata: {
    "language": "Python",
    "category": "syntax",
    "importance": "high"
  }
)
```

Response: `"Remembered: Python uses indentation for scope such as loops and functions"`

### With Custom Collection

When no default collection is configured:

```
qdrant-store(
  information: "FastAPI is a modern Python web framework for building APIs",
  metadata: {"framework": "FastAPI", "purpose": "API development"},
  collection_name: "python_frameworks"
)
```

Response: `"Remembered: FastAPI is a modern Python web framework for building APIs in collection python_frameworks"`

Sources: [README.md22-30](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L22-L30) [src/mcp\_server\_qdrant/mcp\_server.py63-88](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L88)

## Use Case: Code Snippet Storage

The `qdrant-store` tool can be configured for specialized use cases, such as storing code snippets for later retrieval. The following diagram shows how to structure this use case:

```
```

This approach allows for natural language querying of code snippets, where:

1. The description is used to generate the vector embedding for semantic search
2. The actual code and additional metadata are stored in the payload
3. When retrieved with `qdrant-find`, both the description and code are available

Sources: [README.md160-199](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L160-L199)

## Best Practices

1. **Meaningful Information**: Provide clear, descriptive information that captures the semantic meaning you want to retrieve later.

2. **Structured Metadata**: Use consistent metadata schemas to enable more advanced filtering when retrieving information.

3. **Collection Organization**: Use separate collections for different types of information or contexts (e.g., code snippets, documentation, project notes).

4. **Information Size**: Keep individual entries reasonably sized - very large text blocks may not embed as effectively.

5. **Contextual Information**: Include relevant context in the information field to improve retrieval accuracy.

Sources: [README.md160-199](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L160-L199) [src/mcp\_server\_qdrant/mcp\_server.py63-88](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L88)

## Common Issues and Troubleshooting

| Issue                         | Possible Cause                   | Solution                                                                          |
| ----------------------------- | -------------------------------- | --------------------------------------------------------------------------------- |
| Tool not available            | Server in read-only mode         | Check `QDRANT_READ_ONLY` setting                                                  |
| Collection parameter missing  | Default collection configured    | This is expected behavior; use the default collection                             |
| Collection parameter required | No default collection configured | Provide `collection_name` parameter or set `COLLECTION_NAME` environment variable |
| Connection errors             | Incorrect Qdrant URL or API key  | Verify `QDRANT_URL` and `QDRANT_API_KEY` settings                                 |
| Permission errors             | Missing write permissions        | Check Qdrant permissions for your API key                                         |

Sources: [README.md39-54](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L54) [src/mcp\_server\_qdrant/mcp\_server.py155-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L155-L169)

## Related Components

The `qdrant-store` tool works closely with:

1. The `qdrant-find` tool (see [qdrant-find Tool](qdrant/mcp-server-qdrant/4.2-qdrant-find-tool.md)) for retrieving stored information
2. The embedding system (see [Embedding System](qdrant/mcp-server-qdrant/2.2-embedding-system.md)) for converting text to vector embeddings
3. The QdrantConnector (see [QdrantConnector Reference](qdrant/mcp-server-qdrant/5-qdrantconnector-reference.md)) for interaction with the Qdrant database

Sources: [README.md19-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L19-L37)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [qdrant-store Tool](#qdrant-store-tool.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Parameters and Usage](#parameters-and-usage.md)
- [Parameter Details](#parameter-details.md)
- [Implementation Flow](#implementation-flow.md)
- [Internal Architecture](#internal-architecture.md)
- [Configuration Options](#configuration-options.md)
- [Important Configuration Details](#important-configuration-details.md)
- [Tool Registration Logic](#tool-registration-logic.md)
- [Usage Examples](#usage-examples.md)
- [Basic Usage](#basic-usage.md)
- [With Metadata](#with-metadata.md)
- [With Custom Collection](#with-custom-collection.md)
- [Use Case: Code Snippet Storage](#use-case-code-snippet-storage.md)
- [Best Practices](#best-practices.md)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting.md)
- [Related Components](#related-components.md)
