Architecture | qdrant/mcp-server-qdrant | DeepWiki

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

# Architecture

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/mcp\_server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py)
- [src/mcp\_server\_qdrant/qdrant.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py)
- [src/mcp\_server\_qdrant/server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py)

This document provides a high-level overview of the mcp-server-qdrant architecture, explaining the main components and their interactions. It covers the core structural elements, data flows, and integration points that make up the system. For installation and configuration details, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md).

## System Overview

The mcp-server-qdrant is a Model Context Protocol (MCP) server that provides a semantic memory layer on top of the Qdrant vector database. It allows LLM applications to store and retrieve information using vector embeddings for semantic similarity search rather than simple keyword matching.

### High-Level Architecture Diagram

```
```

Sources: [src/mcp\_server\_qdrant/server.py1-13](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L13) [src/mcp\_server\_qdrant/mcp\_server.py1-170](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L1-L170) [README.md1-50](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L1-L50)

## Core Components

The architecture consists of four main components that work together to provide the semantic memory functionality:

### QdrantMCPServer

The `QdrantMCPServer` class is the central component that initializes the server and registers the MCP tools. It inherits from `FastMCP` and serves as the entry point for client requests. The server:

1. Sets up the embedding provider and Qdrant connector
2. Registers the `qdrant-store` and `qdrant-find` tools
3. Handles formatting of entries for display to clients

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py18-50](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L18-L50) [src/mcp\_server\_qdrant/server.py1-13](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L13)

### QdrantConnector

The `QdrantConnector` handles all interactions with the Qdrant vector database. It provides methods to:

1. Connect to either a remote Qdrant instance or a local database file
2. Store entries with their vector embeddings
3. Search for semantically similar entries using vector similarity
4. Manage collections in the Qdrant database

```
```

Sources: [src/mcp\_server\_qdrant/qdrant.py24-149](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L24-L149)

### Embedding System

The embedding system converts text to vector embeddings that can be stored and searched in the Qdrant database. It uses an abstraction called `EmbeddingProvider` with implementations for different embedding technologies. The current implementation supports FastEmbed for generating embeddings.

For detailed information about embedding providers, see [Embedding Providers](qdrant/mcp-server-qdrant/6-embedding-providers.md).

### MCP Tools

The server provides two main tools to clients:

1. **qdrant-store**: Allows storing information with optional metadata in a specified collection
2. **qdrant-find**: Enables semantic search for information based on a query

The behavior of these tools adapts based on the server configuration. For example, if a default collection name is configured, the tools don't require a collection name parameter.

Sources: [src/mcp\_server\_qdrant/mcp\_server.py58-169](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L58-L169) [README.md21-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L21-L38)

## Data Flow

The mcp-server-qdrant handles two primary operations: storing information and finding relevant information. Here's how data flows through the system for these operations:

### Store Operation Flow

```
```

### Find Operation Flow

```
```

Sources: [src/mcp\_server\_qdrant/mcp\_server.py63-138](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/mcp_server.py#L63-L138) [src/mcp\_server\_qdrant/qdrant.py59-126](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L59-L126)

## Configuration Architecture

The system uses a layered configuration approach based on environment variables. There are three main settings classes:

1. **QdrantSettings**: Configures the connection to the Qdrant database
2. **EmbeddingProviderSettings**: Configures the embedding provider
3. **ToolSettings**: Configures the behavior and descriptions of the MCP tools

```
```

For detailed information about configuration options, see [Configuration System](qdrant/mcp-server-qdrant/2.3-configuration-system.md).

Sources: [src/mcp\_server\_qdrant/server.py1-13](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L13) [README.md39-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L57)

## Deployment Architecture

The mcp-server-qdrant can be deployed in several ways:

1. Using `uvx` for direct execution
2. Using Docker containers
3. Via Smithery installation

The server supports multiple transport protocols:

- **stdio**: Standard input/output transport for local clients
- **sse**: Server-Sent Events transport for remote clients

```
```

For detailed deployment instructions, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md).

Sources: [README.md59-149](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L59-L149)

## Security Considerations

The architecture supports secure connections to Qdrant through:

1. API key authentication for remote Qdrant instances
2. Local file-based storage for sensitive environments

When using the SSE transport protocol, the server listens on port 8000 by default and should be secured appropriately if exposed to external networks.

Sources: [README.md39-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L57) [src/mcp\_server\_qdrant/qdrant.py35-49](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/qdrant.py#L35-L49)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Architecture](#architecture.md)
- [System Overview](#system-overview.md)
- [High-Level Architecture Diagram](#high-level-architecture-diagram.md)
- [Core Components](#core-components.md)
- [QdrantMCPServer](#qdrantmcpserver.md)
- [QdrantConnector](#qdrantconnector.md)
- [Embedding System](#embedding-system.md)
- [MCP Tools](#mcp-tools.md)
- [Data Flow](#data-flow.md)
- [Store Operation Flow](#store-operation-flow.md)
- [Find Operation Flow](#find-operation-flow.md)
- [Configuration Architecture](#configuration-architecture.md)
- [Deployment Architecture](#deployment-architecture.md)
- [Security Considerations](#security-considerations.md)
