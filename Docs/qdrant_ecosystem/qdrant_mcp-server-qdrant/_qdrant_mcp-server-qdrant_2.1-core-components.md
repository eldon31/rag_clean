Core Components | qdrant/mcp-server-qdrant | DeepWiki

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

# Core Components

Relevant source files

- [src/mcp\_server\_qdrant/mcp\_server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py)
- [src/mcp\_server\_qdrant/qdrant.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py)
- [src/mcp\_server\_qdrant/server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py)

This document details the main software components that form the foundation of the MCP Server Qdrant system. It covers the key classes and their interactions that enable vector search functionality through the Model Context Protocol (MCP). For details about the embedding system that powers vector generation, see [Embedding System](qdrant/mcp-server-qdrant/2.2-embedding-system.md).

## Overview of Core Components

The MCP Server Qdrant system consists of three primary components that work together to provide vector-based semantic search capabilities:

1. **QdrantMCPServer** - The main server class that handles MCP protocol requests and exposes tools to clients
2. **QdrantConnector** - Manages the connection to Qdrant and handles vector storage and retrieval operations
3. **Entry** - A data model representing a single entry in the Qdrant collection

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py20-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L20-L169) [src/mcp\_server\_qdrant/qdrant.py15-21](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L15-L21) [src/mcp\_server\_qdrant/qdrant.py24-148](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L24-L148)

## QdrantMCPServer

The `QdrantMCPServer` class serves as the primary entry point for the system, extending the `FastMCP` base class to provide an MCP-compatible interface for Qdrant operations. It configures and initializes the other core components and registers the MCP tools that will be exposed to clients.

### Key Responsibilities

- Initializing the embedding provider and Qdrant connector components
- Registering MCP tools (qdrant-store and qdrant-find) based on configuration
- Formatting entries for client presentation
- Handling client requests for storing and finding information

### Main Methods

| Method         | Purpose                                                              |
| -------------- | -------------------------------------------------------------------- |
| `__init__`     | Initializes the server with settings and creates required components |
| `setup_tools`  | Registers the MCP tools based on configuration                       |
| `format_entry` | Formats an Entry object for client presentation                      |

Sources: [src/mcp\_server\_qdrant/mcp\_server.py20-49](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L20-L49) [src/mcp\_server\_qdrant/mcp\_server.py58-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L58-L169)

## QdrantConnector

The `QdrantConnector` class encapsulates all interactions with the Qdrant vector database. It handles the connection setup and provides methods for storing and retrieving vectors.

### Key Responsibilities

- Managing the connection to the Qdrant server
- Creating collections when needed
- Converting text entries to vector embeddings (via the embedding provider)
- Storing and retrieving vectors and their associated metadata

### Main Methods

| Method                      | Purpose                                                |
| --------------------------- | ------------------------------------------------------ |
| `store`                     | Embeds and stores an entry in the specified collection |
| `search`                    | Finds semantically similar entries based on a query    |
| `_ensure_collection_exists` | Creates a collection if it doesn't exist               |
| `get_collection_names`      | Retrieves all collection names from the server         |

Sources: [src/mcp\_server\_qdrant/qdrant.py24-148](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L24-L148)

## Entry Model

The `Entry` class is a Pydantic model that represents a single entry in the Qdrant collection. It encapsulates both the content text and optional metadata.

### Structure

| Field      | Type                       | Description                                           |
| ---------- | -------------------------- | ----------------------------------------------------- |
| `content`  | str                        | The text content to be stored and retrieved           |
| `metadata` | Optional\[Dict\[str, Any]] | Optional key-value metadata associated with the entry |

Sources: [src/mcp\_server\_qdrant/qdrant.py15-21](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L15-L21)

## Request Flow

The following diagram illustrates how these components interact during the two primary operations: storing and finding information.

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py63-138](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L138) [src/mcp\_server\_qdrant/qdrant.py59-126](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L59-L126)

## Component Initialization

The system initialization starts with the server creation in `server.py`, which sets up all the core components with their respective settings:

```
```

Sources: [src/mcp\_server\_qdrant/server.py1-12](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L12) [src/mcp\_server\_qdrant/mcp\_server.py25-49](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L25-L49)

## Server Configuration

The server is configured via three main settings classes passed to the `QdrantMCPServer` constructor:

1. **ToolSettings** - Controls tool descriptions and behavior
2. **QdrantSettings** - Configures the Qdrant connection and collection parameters
3. **EmbeddingProviderSettings** - Specifies which embedding provider and model to use

These settings determine how the components are initialized and how they interact. For more details on configuration options, see [Configuration System](qdrant/mcp-server-qdrant/2.3-configuration-system.md).

Sources: [src/mcp\_server\_qdrant/server.py1-12](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L12) [src/mcp\_server\_qdrant/mcp\_server.py25-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L25-L37)

## Tool Registration

The `QdrantMCPServer` registers two primary tools for client use:

1. **qdrant-store** - Allows clients to store information with metadata in Qdrant
2. **qdrant-find** - Enables semantic search to retrieve relevant information

The exact tool registration depends on configuration settings, particularly:

- Whether a default collection name is provided
- Whether the server is in read-only mode

Sources: [src/mcp\_server\_qdrant/mcp\_server.py58-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L58-L169)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Core Components](#core-components.md)
- [Overview of Core Components](#overview-of-core-components.md)
- [QdrantMCPServer](#qdrantmcpserver.md)
- [Key Responsibilities](#key-responsibilities.md)
- [Main Methods](#main-methods.md)
- [QdrantConnector](#qdrantconnector.md)
- [Key Responsibilities](#key-responsibilities-1.md)
- [Main Methods](#main-methods-1.md)
- [Entry Model](#entry-model.md)
- [Structure](#structure.md)
- [Request Flow](#request-flow.md)
- [Component Initialization](#component-initialization.md)
- [Server Configuration](#server-configuration.md)
- [Tool Registration](#tool-registration.md)
