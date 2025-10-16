MCP CLI Commands | modelcontextprotocol/python-sdk | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 27 September 2025 ([146d7e](https://github.com/modelcontextprotocol/python-sdk/commits/146d7efb))

- [Overview](modelcontextprotocol/python-sdk/1-overview.md)
- [Installation & Dependencies](modelcontextprotocol/python-sdk/1.1-installation-and-dependencies.md)
- [Key Concepts](modelcontextprotocol/python-sdk/1.2-key-concepts.md)
- [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md)
- [FastMCP Server Architecture](modelcontextprotocol/python-sdk/2.1-fastmcp-server-architecture.md)
- [Tool Management](modelcontextprotocol/python-sdk/2.2-tool-management.md)
- [Resource & Prompt Management](modelcontextprotocol/python-sdk/2.3-resource-and-prompt-management.md)
- [Function Introspection & Structured Output](modelcontextprotocol/python-sdk/2.4-function-introspection-and-structured-output.md)
- [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md)
- [ClientSession Core](modelcontextprotocol/python-sdk/3.1-clientsession-core.md)
- [Client Transports](modelcontextprotocol/python-sdk/3.2-client-transports.md)
- [Client Authentication](modelcontextprotocol/python-sdk/3.3-client-authentication.md)
- [Protocol & Message System](modelcontextprotocol/python-sdk/4-protocol-and-message-system.md)
- [Protocol Types & JSON-RPC](modelcontextprotocol/python-sdk/4.1-protocol-types-and-json-rpc.md)
- [Session Management](modelcontextprotocol/python-sdk/4.2-session-management.md)
- [Context & Progress Reporting](modelcontextprotocol/python-sdk/4.3-context-and-progress-reporting.md)
- [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md)
- [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md)
- [Server-Sent Events (SSE) Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md)
- [STDIO Transport](modelcontextprotocol/python-sdk/5.3-stdio-transport.md)
- [Transport Security](modelcontextprotocol/python-sdk/5.4-transport-security.md)
- [Low-Level Server Implementation](modelcontextprotocol/python-sdk/6-low-level-server-implementation.md)
- [Low-Level Server Architecture](modelcontextprotocol/python-sdk/6.1-low-level-server-architecture.md)
- [ServerSession Implementation](modelcontextprotocol/python-sdk/6.2-serversession-implementation.md)
- [Authentication & Security](modelcontextprotocol/python-sdk/7-authentication-and-security.md)
- [OAuth 2.0 System](modelcontextprotocol/python-sdk/7.1-oauth-2.0-system.md)
- [Development Tools & CLI](modelcontextprotocol/python-sdk/8-development-tools-and-cli.md)
- [MCP CLI Commands](modelcontextprotocol/python-sdk/8.1-mcp-cli-commands.md)
- [Development Environment](modelcontextprotocol/python-sdk/8.2-development-environment.md)
- [Claude Desktop Integration](modelcontextprotocol/python-sdk/8.3-claude-desktop-integration.md)
- [Examples & Tutorials](modelcontextprotocol/python-sdk/9-examples-and-tutorials.md)
- [Server Examples](modelcontextprotocol/python-sdk/9.1-server-examples.md)
- [Client Examples](modelcontextprotocol/python-sdk/9.2-client-examples.md)

Menu

# MCP CLI Commands

Relevant source files

- [examples/fastmcp/unicode\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/fastmcp/unicode_example.py)
- [src/mcp/cli/claude.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py)
- [src/mcp/cli/cli.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py)
- [tests/client/test\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_config.py)
- [tests/issues/test\_100\_tool\_listing.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_100_tool_listing.py)

This document covers the MCP CLI commands that provide development tools for building, testing, and deploying MCP servers. The CLI facilitates server development with dependency management, debugging tools, and integration with Claude Desktop.

For information about the underlying FastMCP server framework that these commands operate on, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For details about Claude Desktop integration configuration, see [Claude Desktop Integration](modelcontextprotocol/python-sdk/8.3-claude-desktop-integration.md).

## Purpose and Scope

The MCP CLI provides three primary commands for MCP server development and deployment:

- `mcp dev` - Development server with MCP Inspector integration
- `mcp run` - Direct server execution
- `mcp install` - Claude Desktop application integration
- `mcp version` - Version information

All commands support automatic dependency management through `uv` and handle both standalone Python files and package-based servers.

## CLI Architecture Overview

```
```

Sources: [src/mcp/cli/cli.py34-39](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L34-L39) [src/mcp/cli/cli.py42-86](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L42-L86) [src/mcp/cli/claude.py44-148](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L44-L148)

## Development Command (mcp dev)

The `mcp dev` command launches the MCP Inspector for interactive server testing and debugging.

### Command Syntax

```
```

### Implementation Flow

```
```

Sources: [src/mcp/cli/cli.py222-303](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L222-L303) [src/mcp/cli/cli.py65-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L65-L85) [src/mcp/cli/cli.py268-283](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L268-L283)

### Key Features

| Feature              | Implementation                                                                                                             | Purpose                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Dependency Detection | [src/mcp/cli/cli.py262-264](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L262-L264) | Automatically includes server.dependencies |
| NPX Integration      | [src/mcp/cli/cli.py268-283](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L268-L283) | Launches MCP Inspector for debugging       |
| Cross-Platform       | [src/mcp/cli/cli.py42-53](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L42-L53)     | Handles Windows/Unix npx differences       |
| Editable Install     | [src/mcp/cli/cli.py228-238](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L228-L238) | Supports --with-editable for development   |

Sources: [src/mcp/cli/cli.py222-303](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L222-L303)

## Run Command (mcp run)

The `mcp run` command executes MCP servers directly without dependency management.

### Command Syntax

```
```

### Server Import Process

```
```

Sources: [src/mcp/cli/cli.py88-208](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L88-L208) [src/mcp/cli/cli.py305-360](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L305-L360)

### Transport Support

The run command supports optional transport specification:

- `stdio` - Standard input/output transport
- `sse` - Server-Sent Events transport
- Default: Server's configured transport

Sources: [src/mcp/cli/cli.py311-318](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L311-L318) [src/mcp/cli/cli.py346-350](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L346-L350)

## Install Command (mcp install)

The `mcp install` command configures MCP servers in Claude Desktop's configuration.

### Command Syntax

```
```

### Claude Configuration Process

```
```

Sources: [src/mcp/cli/claude.py17-31](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L17-L31) [src/mcp/cli/claude.py44-148](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L44-L148) [src/mcp/cli/cli.py362-489](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L362-L489)

### Environment Variable Handling

The install command supports flexible environment variable configuration:

| Method       | Implementation             | Behavior                                                                                                                     |
| ------------ | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Command Line | `--env-var KEY=VALUE`      | [src/mcp/cli/cli.py474-476](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L474-L476)   |
| .env File    | `--env-file path.env`      | [src/mcp/cli/cli.py462-471](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L462-L471)   |
| Preservation | Existing vars preserved    | [src/mcp/cli/claude.py92-99](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L92-L99) |
| Merging      | New vars override existing | [src/mcp/cli/claude.py96-97](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L96-L97) |

Sources: [src/mcp/cli/cli.py394-413](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L394-L413) [src/mcp/cli/cli.py457-477](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L457-L477)

## Version Command (mcp version)

Simple command that displays the installed MCP package version using `importlib.metadata`.

```
```

Sources: [src/mcp/cli/cli.py211-219](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L211-L219)

## Dependency Management Integration

All CLI commands integrate with `uv` for dependency management:

### UV Command Construction

```
```

Sources: [src/mcp/cli/cli.py65-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L65-L85) [src/mcp/cli/claude.py101-125](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L101-L125)

### UV Path Resolution

The CLI automatically locates the `uv` executable using platform-appropriate methods:

- Uses `shutil.which("uv")` to find full path
- Falls back to `"uv"` string if not found in PATH
- Provides clear error messages for missing uv installation

Sources: [src/mcp/cli/claude.py33-41](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L33-L41)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [MCP CLI Commands](#mcp-cli-commands.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [CLI Architecture Overview](#cli-architecture-overview.md)
- [Development Command (mcp dev)](#development-command-mcp-dev.md)
- [Command Syntax](#command-syntax.md)
- [Implementation Flow](#implementation-flow.md)
- [Key Features](#key-features.md)
- [Run Command (mcp run)](#run-command-mcp-run.md)
- [Command Syntax](#command-syntax-1.md)
- [Server Import Process](#server-import-process.md)
- [Transport Support](#transport-support.md)
- [Install Command (mcp install)](#install-command-mcp-install.md)
- [Command Syntax](#command-syntax-2.md)
- [Claude Configuration Process](#claude-configuration-process.md)
- [Environment Variable Handling](#environment-variable-handling.md)
- [Version Command (mcp version)](#version-command-mcp-version.md)
- [Dependency Management Integration](#dependency-management-integration.md)
- [UV Command Construction](#uv-command-construction.md)
- [UV Path Resolution](#uv-path-resolution.md)
