API Reference | qdrant/mcp-server-qdrant | DeepWiki

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

# API Reference

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/mcp\_server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py)

This document provides a comprehensive overview of the Model Context Protocol (MCP) API for the mcp-server-qdrant system. It documents the available tools, their parameters, and how they interact with the Qdrant vector database. For detailed information about individual tools, see [qdrant-store Tool](qdrant/mcp-server-qdrant/4.1-qdrant-store-tool.md) and [qdrant-find Tool](qdrant/mcp-server-qdrant/4.2-qdrant-find-tool.md).

## Available Tools

The mcp-server-qdrant exposes two primary MCP tools:

| Tool Name      | Purpose                                         | Key Parameters                                          |
| -------------- | ----------------------------------------------- | ------------------------------------------------------- |
| `qdrant-store` | Store information in the Qdrant vector database | `information`, `metadata`, `collection_name` (optional) |
| `qdrant-find`  | Retrieve relevant information from the database | `query`, `collection_name` (optional)                   |

Sources: [README.md22-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L22-L38)

## API Architecture

### Tool Integration in MCP Server

```
```

The diagram shows how client applications interact with the MCP tools provided by QdrantMCPServer. Each tool calls specific methods in the QdrantConnector, which handles the interaction with the Qdrant database and the EmbeddingProvider.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py18-20](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L18-L20) [src/mcp\_server\_qdrant/mcp\_server.py58-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L58-L169)

### Tool Registration Flow

```
```

This diagram illustrates the tool registration logic in the `setup_tools()` method, showing how different tools are registered based on configuration settings.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py142-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L142-L169)

## Data Flow

### qdrant-store Data Flow

```
```

This diagram shows the data flow when using the `qdrant-store` tool, from client request to storage in the Qdrant database.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py63-89](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L89) [src/mcp\_server\_qdrant/mcp\_server.py90-99](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L90-L99)

### qdrant-find Data Flow

```
```

This diagram illustrates the data flow when using the `qdrant-find` tool, from search query to retrieving and formatting results.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py100-132](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L100-L132) [src/mcp\_server\_qdrant/mcp\_server.py133-139](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L133-L139) [src/mcp\_server\_qdrant/mcp\_server.py51-56](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L51-L56)

## Tool Parameters

### qdrant-store Parameters

| Parameter         | Type   | Required    | Description                                              |
| ----------------- | ------ | ----------- | -------------------------------------------------------- |
| `information`     | string | Yes         | The content to be stored in the database                 |
| `metadata`        | JSON   | No          | Additional structured data to associate with the content |
| `collection_name` | string | Conditional | Required if no default collection is configured          |

The tool returns a confirmation message indicating that the information was successfully stored.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py63-71](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L71) [README.md23-30](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L23-L30)

### qdrant-find Parameters

| Parameter         | Type   | Required    | Description                                        |
| ----------------- | ------ | ----------- | -------------------------------------------------- |
| `query`           | string | Yes         | The search query used to find relevant information |
| `collection_name` | string | Conditional | Required if no default collection is configured    |

The tool returns a list of entries that match the query, formatted according to the `format_entry` method.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py100-105](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L100-L105) [README.md31-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L31-L37)

## Response Format

When using the `qdrant-find` tool, results are returned as a list of formatted entries. Each entry is formatted as:

```
<entry><content>The stored information</content><metadata>{"any": "metadata", "as": "JSON"}</metadata></entry>
```

The first message always contains the text: `Results for the query '{query}'`. If no results are found, the response will be: `No information found for the query '{query}'`.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py51-56](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L51-L56) [src/mcp\_server\_qdrant/mcp\_server.py124-131](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L124-L131)

## Example Usage

### Basic Usage Examples

**Storing Information:**

```
qdrant-store(
  information="The capital of France is Paris.",
  metadata={"category": "geography", "confidence": "high"}
)
```

**Finding Information:**

```
qdrant-find(query="What is the capital of France?")
```

### Common Use Cases

1. **Knowledge Base Creation and Retrieval:**

   - Store facts, knowledge, or documentation
   - Retrieve relevant information based on semantic search

2. **Code Snippet Management:**

   - Store code snippets with descriptions
   - Retrieve snippets based on functionality needs

3. **Conversation Memory:**

   - Store important parts of conversations
   - Retrieve context from previous exchanges

Sources: [README.md14-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L14-L17) [README.md166-197](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L166-L197)

## Configuration Impact on API

The API behavior is affected by several environment variables:

| Environment Variable     | Effect on API                                                      |
| ------------------------ | ------------------------------------------------------------------ |
| `COLLECTION_NAME`        | When set, makes `collection_name` parameter optional in both tools |
| `QDRANT_READ_ONLY`       | When set to `true`, disables the `qdrant-store` tool               |
| `QDRANT_SEARCH_LIMIT`    | Controls the maximum number of results returned by `qdrant-find`   |
| `TOOL_STORE_DESCRIPTION` | Customizes the description of the `qdrant-store` tool              |
| `TOOL_FIND_DESCRIPTION`  | Customizes the description of the `qdrant-find` tool               |

For a complete list of configuration options, see [Configuration Options](qdrant/mcp-server-qdrant/3.1-configuration-options.md).

Sources: [README.md39-53](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L53) [src/mcp\_server\_qdrant/mcp\_server.py142-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L142-L169)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [API Reference](#api-reference.md)
- [Available Tools](#available-tools.md)
- [API Architecture](#api-architecture.md)
- [Tool Integration in MCP Server](#tool-integration-in-mcp-server.md)
- [Tool Registration Flow](#tool-registration-flow.md)
- [Data Flow](#data-flow.md)
- [qdrant-store Data Flow](#qdrant-store-data-flow.md)
- [qdrant-find Data Flow](#qdrant-find-data-flow.md)
- [Tool Parameters](#tool-parameters.md)
- [qdrant-store Parameters](#qdrant-store-parameters.md)
- [qdrant-find Parameters](#qdrant-find-parameters.md)
- [Response Format](#response-format.md)
- [Example Usage](#example-usage.md)
- [Basic Usage Examples](#basic-usage-examples.md)
- [Common Use Cases](#common-use-cases.md)
- [Configuration Impact on API](#configuration-impact-on-api.md)
