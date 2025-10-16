Client Integration | qdrant/mcp-server-qdrant | DeepWiki

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

# Client Integration

Relevant source files

- [README.md](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md)
- [src/mcp\_server\_qdrant/main.py](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/main.py)

This page describes how to integrate the Qdrant MCP server with various LLM applications and development environments. It covers configuration methods for different client tools, transport protocol options, and specific integration patterns for each supported client application.

For details on server installation and deployment methods, see [Installation & Deployment](qdrant/mcp-server-qdrant/3-installation-and-deployment.md).

## Supported Clients and Integration Methods

The Qdrant MCP server can be integrated with various client applications that support the Model Context Protocol. Each client offers different integration methods:

### Client Integration Overview

```
```

Sources: [README.md105-149](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L105-L149) [README.md156-212](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L156-L212) [README.md213-257](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L213-L257) [README.md258-431](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L258-L431)

## Transport Protocols

The MCP server supports different transport protocols for communication with clients:

### Transport Protocol Selection

```
```

Sources: [README.md72-87](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L72-L87) [src/mcp\_server\_qdrant/main.py11-18](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/src/mcp_server_qdrant/main.py#L11-L18)

| Protocol        | Description           | Use Case       | Configuration       |
| --------------- | --------------------- | -------------- | ------------------- |
| stdio (default) | Standard input/output | Local clients  | `--transport stdio` |
| sse             | Server-Sent Events    | Remote clients | `--transport sse`   |

## Claude Desktop Integration

Claude Desktop can be integrated with the Qdrant MCP server in two ways:

### Smithery Installation (Recommended)

Smithery provides a streamlined installation process:

```
```

Sources: [README.md105-111](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L105-L111)

### Manual Configuration

To manually configure Claude Desktop:

1. Locate your `claude_desktop_config.json` file
2. Add the Qdrant server configuration to the "mcpServers" section:

```
```

For local Qdrant mode:

```
```

Sources: [README.md114-147](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L114-L147)

## Cursor/Windsurf Integration

Cursor and Windsurf can be configured to use the MCP server as a code search tool.

### Setup Process

1. Start the MCP server with customized tool descriptions for code search:

```
```

2. In Cursor/Windsurf, configure the MCP server in settings by pointing to the running server using the URL:

```
http://localhost:8000/sse
```

Sources: [README.md160-187](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L160-L187)

### Usage in Cursor/Windsurf

With this configuration, the Qdrant MCP server acts as a specialized code search tool that can:

- Store code snippets with natural language descriptions
- Retrieve relevant code examples based on semantic search
- Provide a persistent memory for code patterns and solutions

For best results, create [Cursor rules](https://docs.cursor.com/context/rules-for-ai) to ensure the MCP tools are always used when generating new code snippets.

Sources: [README.md189-212](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L189-L212)

## VS Code Integration

VS Code provides multiple methods for integrating with the Qdrant MCP server.

### One-Click Installation

VS Code and VS Code Insiders offer one-click installation options:

- VS Code with UVX
- VS Code Insiders with UVX
- VS Code with Docker
- VS Code Insiders with Docker

These installation methods are available as buttons in the VS Code documentation.

Sources: [README.md260-263](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L260-L263)

### Manual Installation

To manually configure VS Code:

1. Add the configuration to User Settings (JSON) by pressing `Ctrl + Shift + P` and typing `Preferences: Open User Settings (JSON)`:

```
```

Alternatively, create a `.vscode/mcp.json` file in your workspace with similar configuration.

Sources: [README.md265-385](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L265-L385)

## Claude Code Integration

Claude Code can be enhanced with the Qdrant MCP server for semantic search capabilities.

### Setup Process

1. Add the MCP server to Claude Code:

```
```

2. Verify the server was added:

```
```

Sources: [README.md217-237](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L217-L237)

## Common Integration Patterns

The integration of the Qdrant MCP server with various clients follows common patterns, particularly for code storage and retrieval.

### Code Repository Integration Pattern

```
```

Sources: [README.md168-183](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L168-L183) [README.md193-206](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L193-L206)

When configured as a code repository, this pattern enables:

| Parameter       | Usage                                                 |
| --------------- | ----------------------------------------------------- |
| `information`   | Natural language description of code functionality    |
| `metadata.code` | Actual code snippet to be stored                      |
| `query`         | Natural language description of desired functionality |

## Development and Testing

For development and testing purposes, you can run the MCP server in development mode with the MCP inspector:

```
```

This starts the server and opens the MCP inspector in your browser at <http://localhost:5173>, which provides an interface for testing and debugging tool interactions.

Sources: [README.md249-256](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L249-L256) [README.md444-450](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L444-L450)

## Troubleshooting

### Common Issues

- If the MCP server doesn't appear to be used in Cursor, check that you have configured proper [Cursor rules](https://docs.cursor.com/context/rules-for-ai)
- For VS Code integration issues, verify that the MCP extension is properly installed and configured
- When using SSE transport, ensure port 8000 is accessible to the client
- For Claude Desktop integration, check that the configuration JSON is correctly formatted and in the right location

Sources: [README.md208-212](https://github.com/qdrant/mcp-server-qdrant/blob/a3ab0b96/README.md#L208-L212)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Integration](#client-integration.md)
- [Supported Clients and Integration Methods](#supported-clients-and-integration-methods.md)
- [Client Integration Overview](#client-integration-overview.md)
- [Transport Protocols](#transport-protocols.md)
- [Transport Protocol Selection](#transport-protocol-selection.md)
- [Claude Desktop Integration](#claude-desktop-integration.md)
- [Smithery Installation (Recommended)](#smithery-installation-recommended.md)
- [Manual Configuration](#manual-configuration.md)
- [Cursor/Windsurf Integration](#cursorwindsurf-integration.md)
- [Setup Process](#setup-process.md)
- [Usage in Cursor/Windsurf](#usage-in-cursorwindsurf.md)
- [VS Code Integration](#vs-code-integration.md)
- [One-Click Installation](#one-click-installation.md)
- [Manual Installation](#manual-installation.md)
- [Claude Code Integration](#claude-code-integration.md)
- [Setup Process](#setup-process-1.md)
- [Common Integration Patterns](#common-integration-patterns.md)
- [Code Repository Integration Pattern](#code-repository-integration-pattern.md)
- [Development and Testing](#development-and-testing.md)
- [Troubleshooting](#troubleshooting.md)
- [Common Issues](#common-issues.md)
