Installation & Deployment | qdrant/mcp-server-qdrant | DeepWiki

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

# Installation & Deployment

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [pyproject.toml](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml)
- [src/mcp\_server\_qdrant/main.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/main.py)
- [uv.lock](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/uv.lock)

This page provides comprehensive instructions for installing and deploying the mcp-server-qdrant system. The document covers various installation methods, configuration options, and client integration approaches. For detailed configuration settings, see [Configuration Options](qdrant/mcp-server-qdrant/3.1-configuration-options.md).

## Installation Methods

The mcp-server-qdrant can be installed and run using several methods. Choose the approach that best fits your environment and needs.

### Using uvx (Recommended)

The simplest way to run mcp-server-qdrant is using `uvx`, which allows direct execution without a separate installation step:

```
```

This method requires the `uvx` tool from the `uv` Python package manager to be installed on your system.

### Using Docker

The repository includes a Dockerfile for containerized deployment:

```
```

Docker deployment is ideal for production environments or when you need isolation from the host system.

### Installing via Smithery

For automatic installation with Claude Desktop integration, you can use Smithery:

```
```

This installs and configures the MCP server for immediate use with Claude Desktop.

### Manual Installation

You can install the package directly using pip:

```
```

Then run it using the installed entry point:

```
```

Sources: [README.md59-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L59-L147) [pyproject.toml1-32](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/pyproject.toml#L1-L32)

## Transport Protocols

The server supports multiple transport protocols for communication with clients:

```
```

To specify a transport protocol, use the `--transport` flag:

```
```

- `stdio` (default): Standard input/output transport, suitable for local MCP clients
- `sse`: Server-Sent Events transport, ideal for remote clients (listening on port 8000)

Sources: [README.md72-86](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L72-L86) [src/mcp\_server\_qdrant/main.py1-25](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/main.py#L1-L25)

## Deployment Architecture

The following diagram illustrates the overall deployment architecture of mcp-server-qdrant:

```
```

The deployment consists of:

1. The MCP server that implements the Model Context Protocol
2. A connection to a Qdrant vector database (either local or hosted)
3. An embedding provider for converting text to vectors
4. Client applications that communicate with the server using the MCP protocol

Sources: [README.md14-38](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L14-L38)

## Configuration Flow

The configuration system uses environment variables to set up the server components:

```
```

This shows how environment variables are mapped to settings classes that configure different components of the system.

Sources: [README.md39-58](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L39-L58)

## Client Integration Examples

### Claude Desktop Integration

Add the following to your `claude_desktop_config.json`:

```
```

For local Qdrant:

```
```

Sources: [README.md102-152](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L102-L152)

### VS Code Integration

VS Code offers both one-click installation and manual setup options.

For manual installation, add the following to your VS Code User Settings (JSON):

```
```

Alternatively, create a `.vscode/mcp.json` file in your workspace with similar configuration.

Sources: [README.md257-386](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L257-L386)

### Cursor/Windsurf Integration

For Cursor and Windsurf, configure the MCP server with SSE transport:

```
```

Then in Cursor/Windsurf, configure the MCP server using the URL:

```
http://localhost:8000/sse
```

Sources: [README.md158-212](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L158-L212)

### Claude Code Integration

Add the MCP server to Claude Code:

```
```

Sources: [README.md213-247](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L213-L247)

## Development Mode

For development and testing purposes, use the MCP dev command:

```
```

This starts the server and opens the MCP inspector in your browser for testing the API.

Sources: [README.md248-256](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L248-L256)

## Client Integration Matrix

The following table summarizes the integration options for different clients:

| Client          | Transport | Integration Method  | Configuration Location                             |
| --------------- | --------- | ------------------- | -------------------------------------------------- |
| Claude Desktop  | stdio     | Smithery or Manual  | claude\_desktop\_config.json                       |
| VS Code         | stdio     | One-click or Manual | User Settings or .vscode/mcp.json                  |
| Cursor/Windsurf | sse       | Manual              | Cursor settings (URL: <http://localhost:8000/sse>) |
| Claude Code     | stdio     | Command-line        | claude configuration                               |

This matrix helps you determine the appropriate deployment approach based on your client application.

Sources: [README.md102-247](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L102-L247)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Installation & Deployment](#installation-deployment.md)
- [Installation Methods](#installation-methods.md)
- [Using uvx (Recommended)](#using-uvx-recommended.md)
- [Using Docker](#using-docker.md)
- [Installing via Smithery](#installing-via-smithery.md)
- [Manual Installation](#manual-installation.md)
- [Transport Protocols](#transport-protocols.md)
- [Deployment Architecture](#deployment-architecture.md)
- [Configuration Flow](#configuration-flow.md)
- [Client Integration Examples](#client-integration-examples.md)
- [Claude Desktop Integration](#claude-desktop-integration.md)
- [VS Code Integration](#vs-code-integration.md)
- [Cursor/Windsurf Integration](#cursorwindsurf-integration.md)
- [Claude Code Integration](#claude-code-integration.md)
- [Development Mode](#development-mode.md)
- [Client Integration Matrix](#client-integration-matrix.md)
