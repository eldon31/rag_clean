Embedding Providers | qdrant/mcp-server-qdrant | DeepWiki

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

# Embedding Providers

Relevant source files

- [src/mcp\_server\_qdrant/embeddings/base.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py)
- [src/mcp\_server\_qdrant/embeddings/factory.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py)
- [src/mcp\_server\_qdrant/embeddings/fastembed.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py)
- [tests/test\_fastembed\_integration.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py)

## Purpose and Scope

This document details the embedding system within the mcp-server-qdrant repository, which is responsible for converting text into vector representations (embeddings) for semantic search operations. It covers the embedding provider interface, available implementations, configuration options, and extension points. For information about the overall system architecture, see [Architecture](qdrant/mcp-server-qdrant/2-architecture.md).

## Overview

Embedding providers are fundamental components in the mcp-server-qdrant system that transform natural language text into high-dimensional vector representations. These vectors capture semantic meaning, enabling similarity-based search operations in the Qdrant vector database.

```
```

Sources: [src/mcp\_server\_qdrant/embeddings/base.py1-27](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py#L1-L27) [src/mcp\_server\_qdrant/embeddings/fastembed.py1-52](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L1-L52)

## Architecture

The embedding system follows a simple yet extensible architecture based on the Provider pattern. It consists of an abstract interface that all concrete embedding providers must implement, with a factory method to instantiate the appropriate provider based on configuration.

```
```

Sources: [src/mcp\_server\_qdrant/embeddings/base.py1-27](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py#L1-L27) [src/mcp\_server\_qdrant/embeddings/fastembed.py1-52](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L1-L52) [src/mcp\_server\_qdrant/embeddings/factory.py1-18](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py#L1-L18)

## EmbeddingProvider Interface

The `EmbeddingProvider` abstract base class defines the contract that all embedding providers must implement:

| Method                                  | Description                                                | Return Type         |
| --------------------------------------- | ---------------------------------------------------------- | ------------------- |
| `embed_documents(documents: List[str])` | Converts multiple text documents into vector embeddings    | `List[List[float]]` |
| `embed_query(query: str)`               | Converts a single query text into a vector embedding       | `List[float]`       |
| `get_vector_name()`                     | Returns the name identifier for the vector field in Qdrant | `str`               |
| `get_vector_size()`                     | Returns the dimensionality of the embedding vectors        | `int`               |

Sources: [src/mcp\_server\_qdrant/embeddings/base.py5-26](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py#L5-L26)

## Current Implementation: FastEmbedProvider

The system currently includes one implementation based on the FastEmbed library, which wraps various sentence transformer models.

### Implementation Details

The `FastEmbedProvider` uses the FastEmbed library to generate embeddings:

```
```

Sources: [src/mcp\_server\_qdrant/embeddings/fastembed.py10-52](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L10-L52)

### Key Features

1. **Async Operation**: Although FastEmbed operates synchronously, the provider wraps operations in `run_in_executor` to maintain the async interface.

2. **Vector Naming Convention**: The provider generates standardized vector names based on the model used (e.g., `fast-minilm-l6-v2`).

3. **Automatic Dimension Detection**: Retrieves the correct vector dimension from the model description.

Sources: [src/mcp\_server\_qdrant/embeddings/fastembed.py20-51](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L20-L51) [tests/test\_fastembed\_integration.py56-64](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py#L56-L64)

## Configuring Embedding Providers

The embedding provider is configured through environment variables:

| Environment Variable | Description                                                        | Default                                  |
| -------------------- | ------------------------------------------------------------------ | ---------------------------------------- |
| EMBEDDING\_PROVIDER  | The type of embedding provider to use (currently only "fastembed") | "fastembed"                              |
| EMBEDDING\_MODEL     | The model name to use for embedding generation                     | "sentence-transformers/all-MiniLM-L6-v2" |

Example configuration:

```
EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

The configuration flow works as follows:

```
```

Sources: [src/mcp\_server\_qdrant/embeddings/factory.py6-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py#L6-L17)

## Available Models

The FastEmbedProvider supports several models from the FastEmbed library:

| Model Name                                      | Dimensions | Use Case                                        |
| ----------------------------------------------- | ---------- | ----------------------------------------------- |
| sentence-transformers/all-MiniLM-L6-v2          | 384        | General purpose, balanced performance (default) |
| sentence-transformers/all-mpnet-base-v2         | 768        | Higher quality, larger model                    |
| sentence-transformers/multi-qa-MiniLM-L6-cos-v1 | 384        | Optimized for question-answering                |
| intfloat/e5-small                               | 384        | Efficient general-purpose model                 |
| intfloat/e5-base                                | 768        | Higher quality general-purpose model            |

Sources: [tests/test\_fastembed\_integration.py12-15](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py#L12-L15) [src/mcp\_server\_qdrant/embeddings/fastembed.py16-18](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L16-L18)

## Integration Testing

The embedding system includes integration tests that verify:

1. Proper initialization with a model
2. Consistent embedding generation for documents
3. Consistent embedding generation for queries
4. Vector dimensionality and stability
5. Proper vector naming convention

These tests ensure the embedding providers function correctly when integrated with actual models.

Sources: [tests/test\_fastembed\_integration.py8-63](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/tests/test_fastembed_integration.py#L8-L63)

## Extending with Custom Providers

To implement a custom embedding provider:

1. Create a new class that inherits from `EmbeddingProvider`
2. Implement all required methods
3. Update the `create_embedding_provider` factory function to support your new provider type
4. Add a new value to the `EmbeddingProviderType` enum

```
```

Sources: [src/mcp\_server\_qdrant/embeddings/factory.py6-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py#L6-L17) [src/mcp\_server\_qdrant/embeddings/base.py5-26](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py#L5-L26)

## System Integration

The embedding provider is used by the following system components:

1. **QdrantMCPServer**: Uses the provider to embed queries and documents for the MCP tools
2. **QdrantConnector**: Uses the provider to configure vector properties in Qdrant collections

This integration enables seamless translation between natural language and vector space for both storing and retrieving information.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Embedding Providers](#embedding-providers.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Overview](#overview.md)
- [Architecture](#architecture.md)
- [EmbeddingProvider Interface](#embeddingprovider-interface.md)
- [Current Implementation: FastEmbedProvider](#current-implementation-fastembedprovider.md)
- [Implementation Details](#implementation-details.md)
- [Key Features](#key-features.md)
- [Configuring Embedding Providers](#configuring-embedding-providers.md)
- [Available Models](#available-models.md)
- [Integration Testing](#integration-testing.md)
- [Extending with Custom Providers](#extending-with-custom-providers.md)
- [System Integration](#system-integration.md)
