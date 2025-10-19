Embedding System | qdrant/mcp-server-qdrant | DeepWiki

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

# Embedding System

Relevant source files

- [src/mcp\_server\_qdrant/embeddings/\_\_init\_\_.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/__init__.py)
- [src/mcp\_server\_qdrant/embeddings/base.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py)
- [src/mcp\_server\_qdrant/embeddings/factory.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py)
- [src/mcp\_server\_qdrant/embeddings/fastembed.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py)
- [src/mcp\_server\_qdrant/embeddings/types.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/types.py)

The Embedding System is a core component of the mcp-server-qdrant architecture responsible for converting text data (both documents and queries) into vector representations that enable semantic search capabilities in the Qdrant vector database. This page documents the design, implementation, and usage of the embedding system.

For information about the overall architecture, see [Architecture](qdrant/mcp-server-qdrant/2-architecture.md), and for details about configuring the embedding system, see [Configuration System](qdrant/mcp-server-qdrant/2.3-configuration-system.md).

## System Overview

The Embedding System serves as the bridge between natural language text and the vector space where semantic similarity operations can be performed.

```
```

The Embedding System transforms raw text into numerical vector representations that capture semantic meaning, enabling similarity-based search rather than simple keyword matching.

Sources: [src/mcp\_server\_qdrant/embeddings/factory.py6-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py#L6-L17) [src/mcp\_server\_qdrant/embeddings/base.py5-26](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py#L5-L26) [src/mcp\_server\_qdrant/embeddings/fastembed.py10-51](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L10-L51)

## EmbeddingProvider Interface

At the core of the embedding system is the abstract `EmbeddingProvider` interface:

```
```

This interface defines four critical methods that all embedding providers must implement:

| Method            | Purpose                                                 | Return Type         |
| ----------------- | ------------------------------------------------------- | ------------------- |
| `embed_documents` | Converts multiple text documents into vector embeddings | `List[List[float]]` |
| `embed_query`     | Converts a single query string into a vector embedding  | `List[float]`       |
| `get_vector_name` | Returns an identifier for the vector type               | `str`               |
| `get_vector_size` | Returns the dimensionality of the vectors               | `int`               |

Both embedding methods are asynchronous, allowing the server to handle multiple concurrent requests efficiently.

Sources: [src/mcp\_server\_qdrant/embeddings/base.py5-26](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/base.py#L5-L26)

## FastEmbed Implementation

The current implementation uses the FastEmbed library through the `FastEmbedProvider` class:

```
```

The `FastEmbedProvider` class:

1. Is initialized with a model name and creates an internal `TextEmbedding` instance
2. Implements `embed_documents` by running FastEmbed's `passage_embed` method
3. Implements `embed_query` by running FastEmbed's `query_embed` method
4. Provides a vector name in the format `fast-{model_name}`
5. Retrieves the vector dimensionality from the model's metadata

Since FastEmbed's API is synchronous but the `EmbeddingProvider` interface is asynchronous, the implementation uses `asyncio.get_event_loop().run_in_executor()` to run the embedding operations in thread pools, preventing blocking of the main event loop.

Sources: [src/mcp\_server\_qdrant/embeddings/fastembed.py10-51](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L10-L51)

## Provider Factory

The embedding system uses a factory pattern to create embedding providers based on configuration settings:

```
```

The `create_embedding_provider` factory function:

1. Takes an `EmbeddingProviderSettings` instance as input
2. Checks the `provider_type` field to determine which implementation to create
3. Creates and returns the appropriate `EmbeddingProvider` implementation
4. Raises a `ValueError` for unsupported provider types

Currently, only the `FASTEMBED` provider type is supported, defined in the `EmbeddingProviderType` enum.

Sources: [src/mcp\_server\_qdrant/embeddings/factory.py6-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py#L6-L17) [src/mcp\_server\_qdrant/embeddings/types.py1-5](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/types.py#L1-L5)

## Embedding Workflow

The following sequence diagram illustrates how the embedding system is used in the two main operations of the mcp-server-qdrant:

```
```

1. **Store Operation**: When storing information, the text is first embedded into a vector before being stored in Qdrant
2. **Find Operation**: When searching for information, the query text is embedded to perform semantic similarity search

Sources: [src/mcp\_server\_qdrant/embeddings/fastembed.py20-36](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L20-L36)

## Technical Implementation Details

### Asynchronous Operation

The embedding interface is designed to be asynchronous, but the FastEmbed library provides synchronous methods. To bridge this gap, the `FastEmbedProvider` implementation runs the synchronous FastEmbed operations in thread pools:

```
```

This approach allows the server to handle multiple requests efficiently without being blocked by embedding operations.

Sources: [src/mcp\_server\_qdrant/embeddings/fastembed.py20-27](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L20-L27)

### Vector Characteristics

Each embedding model produces vectors with specific characteristics that need to be communicated to the Qdrant database:

| Method              | Purpose                                          | Example (for FastEmbed)                 |
| ------------------- | ------------------------------------------------ | --------------------------------------- |
| `get_vector_name()` | Provides a unique identifier for the vector type | `"fast-baai-bge-small-en"`              |
| `get_vector_size()` | Provides the dimensionality of the vectors       | Typically 384 or 768 depending on model |

The `FastEmbedProvider` implementation:

- Generates vector names in the format `fast-{model_name}`
- Retrieves the vector dimensionality from the model's metadata via `model_description.dim`

Sources: [src/mcp\_server\_qdrant/embeddings/fastembed.py38-51](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/fastembed.py#L38-L51)

## Extending the Embedding System

To add support for new embedding models or libraries:

1. Add a new value to the `EmbeddingProviderType` enum in `types.py`
2. Create a new implementation of the `EmbeddingProvider` interface
3. Update the `create_embedding_provider` factory function to handle the new provider type

This modular design allows the system to evolve with minimal changes to existing code.

Sources: [src/mcp\_server\_qdrant/embeddings/types.py1-5](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/types.py#L1-L5) [src/mcp\_server\_qdrant/embeddings/factory.py6-17](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/embeddings/factory.py#L6-L17)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Embedding System](#embedding-system.md)
- [System Overview](#system-overview.md)
- [EmbeddingProvider Interface](#embeddingprovider-interface.md)
- [FastEmbed Implementation](#fastembed-implementation.md)
- [Provider Factory](#provider-factory.md)
- [Embedding Workflow](#embedding-workflow.md)
- [Technical Implementation Details](#technical-implementation-details.md)
- [Asynchronous Operation](#asynchronous-operation.md)
- [Vector Characteristics](#vector-characteristics.md)
- [Extending the Embedding System](#extending-the-embedding-system.md)
