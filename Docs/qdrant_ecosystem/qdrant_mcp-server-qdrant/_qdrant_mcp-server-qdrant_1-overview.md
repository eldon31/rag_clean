qdrant/mcp-server-qdrant | DeepWiki

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

# Overview

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [pyproject.toml](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml)
- [src/mcp\_server\_qdrant/server.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py)

This document provides an introduction to the mcp-server-qdrant repository, which implements a semantic memory layer on top of the Qdrant vector database using the Model Context Protocol (MCP). For detailed information about the architecture, see [Architecture](qdrant/mcp-server-qdrant/2-architecture.md), and for installation instructions, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md).

## What is mcp-server-qdrant?

mcp-server-qdrant is an official Model Context Protocol server that enables LLM applications to store and retrieve information in a Qdrant vector database using semantic search. It converts text into vector embeddings and performs similarity searches to find the most relevant information based on meaning rather than just keywords.

The server acts as a bridge between LLM applications and the Qdrant vector database, allowing AI systems to maintain persistent memory that can be queried semantically.

Sources: [README.md1-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L1-L17)

## System Components

The mcp-server-qdrant system consists of three main components:

1. **QdrantMCPServer**: The core server that implements the Model Context Protocol interface, exposing tools for storing and finding information.
2. **QdrantConnector**: Handles the connection to the Qdrant database and manages vector operations.
3. **EmbeddingProvider**: Generates vector embeddings from text, with FastEmbedProvider as the current implementation.

These components are configured through three settings classes: ToolSettings, QdrantSettings, and EmbeddingProviderSettings.

Sources: [src/mcp\_server\_qdrant/server.py1-12](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L12) [README.md19-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L19-L38)

## Core Architecture

Below is a diagram showing the high-level architecture of the mcp-server-qdrant system:

```
```

Sources: [README.md14-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L14-L38) [src/mcp\_server\_qdrant/server.py1-12](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L12)

## Key Information Flows

The system handles two primary operations: storing information and finding information. Here's how these processes work:

```
```

Sources: [README.md19-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L19-L38)

## Exposed Tools

The mcp-server-qdrant exposes two primary tools to clients:

| Tool Name      | Purpose                                         | Parameters                                                                                                                           | Return Value                              |
| -------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| `qdrant-store` | Store information in the Qdrant database        | `information` (string): Content to store `metadata` (JSON): Optional metadata `collection_name` (string): Optional target collection | Confirmation message                      |
| `qdrant-find`  | Retrieve relevant information from the database | `query` (string): Search query `collection_name` (string): Optional target collection                                                | Relevant information as separate messages |

Sources: [README.md21-37](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L21-L37)

## Configuration System

The system is configured through environment variables that map to three settings classes:

```
```

Sources: [src/mcp\_server\_qdrant/server.py1-12](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/server.py#L1-L12) [README.md39-57](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L57)

## Deployment Methods

mcp-server-qdrant can be deployed using several methods:

1. **Using uvx**: Direct execution with the `uvx` command
2. **Using Docker**: Running as a containerized application
3. **Smithery Installation**: Automated installation for Claude Desktop
4. **Manual Configuration**: Custom setup for various clients

The server supports two transport protocols:

- `stdio` (default): For local MCP clients
- `sse`: Server-Sent Events for remote clients

Sources: [README.md59-150](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L59-L150)

## Integration Options

The server can be integrated with various MCP-compatible clients:

1. **Claude Desktop**: For AI-assisted chat and work
2. **Cursor/Windsurf**: For code search and development
3. **VS Code**: For coding with AI assistance
4. **Claude Code**: For code generation and search capabilities

Each integration can be customized by modifying the tool descriptions to suit specific use cases.

Sources: [README.md154-350](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L154-L350)

## Technical Requirements

- Python 3.10 or later

- Dependencies:

  - mcp\[cli] ≥ 1.3.0
  - fastembed ≥ 0.6.0
  - qdrant-client ≥ 1.12.0
  - pydantic ≥ 2.10.6

Sources: [pyproject.toml1-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L1-L38)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Overview](#overview.md)
- [What is mcp-server-qdrant?](#what-is-mcp-server-qdrant.md)
- [System Components](#system-components.md)
- [Core Architecture](#core-architecture.md)
- [Key Information Flows](#key-information-flows.md)
- [Exposed Tools](#exposed-tools.md)
- [Configuration System](#configuration-system.md)
- [Deployment Methods](#deployment-methods.md)
- [Integration Options](#integration-options.md)
- [Technical Requirements](#technical-requirements.md)
