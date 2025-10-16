Development Tools & CLI | modelcontextprotocol/python-sdk | DeepWiki

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

# Development Tools & CLI

Relevant source files

- [examples/fastmcp/unicode\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/fastmcp/unicode_example.py)
- [src/mcp/cli/claude.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py)
- [src/mcp/cli/cli.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py)
- [tests/client/test\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_config.py)
- [tests/issues/test\_100\_tool\_listing.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_100_tool_listing.py)

The MCP Python SDK includes a comprehensive command-line interface (CLI) that streamlines the development workflow for MCP servers. The CLI provides commands for running servers, integrating with development tools, and deploying to client applications like Claude Desktop.

For information about the underlying server frameworks, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For details about transport implementations, see [Transport Layer](modelcontextprotocol/python-sdk/5-transport-layer.md).

## CLI Architecture

The MCP CLI is built using the `typer` library and provides a unified interface for server development and deployment operations. The system consists of two main modules: the core CLI implementation and Claude Desktop integration utilities.

### CLI Command Structure

```
```

**Sources:** [src/mcp/cli/cli.py34-39](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L34-L39) [src/mcp/cli/cli.py211-488](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L211-L488) [src/mcp/cli/claude.py44-148](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L44-L148)

### Server Import and Resolution

The CLI includes sophisticated server discovery and import mechanisms that handle various server specification formats and automatically resolve FastMCP server instances.

```
```

**Sources:** [src/mcp/cli/cli.py88-116](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L88-L116) [src/mcp/cli/cli.py119-208](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L119-L208) [src/mcp/cli/cli.py143-159](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L143-L159)

## CLI Commands

### Version Command

The `version` command displays the currently installed MCP package version using Python's metadata system.

```
```

**Sources:** [src/mcp/cli/cli.py212-219](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L212-L219)

### Development Command

The `dev` command runs an MCP server with the MCP Inspector for interactive development and testing. It automatically manages dependencies using `uv` and launches the Node.js-based inspector tool.

```
```

**Sources:** [src/mcp/cli/cli.py222-303](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L222-L303) [src/mcp/cli/cli.py42-53](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L42-L53) [src/mcp/cli/cli.py65-85](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L65-L85)

### Run Command

The `run` command executes an MCP server directly without additional tooling. It supports transport specification and runs the server using the FastMCP framework.

Key features:

- Direct server execution without dependency management
- Transport protocol selection (`stdio` or `sse`)
- Server object import and validation

**Sources:** [src/mcp/cli/cli.py305-359](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L305-L359)

### Install Command

The `install` command configures MCP servers for use with Claude Desktop by updating the application's configuration file. It handles dependency specification, environment variable management, and cross-platform config file locations.

```
```

**Sources:** [src/mcp/cli/cli.py362-488](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L362-L488) [src/mcp/cli/cli.py456-476](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L456-L476) [src/mcp/cli/claude.py44-148](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L44-L148)

## Claude Desktop Integration

The Claude integration module provides platform-aware configuration management for installing MCP servers into the Claude Desktop application.

### Configuration Path Detection

The system detects Claude Desktop configuration directories across different platforms:

| Platform | Configuration Path                              |
| -------- | ----------------------------------------------- |
| Windows  | `%APPDATA%\Claude`                              |
| macOS    | `~/Library/Application Support/Claude`          |
| Linux    | `$XDG_CONFIG_HOME/Claude` or `~/.config/Claude` |

**Sources:** [src/mcp/cli/claude.py17-30](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L17-L30)

### Config File Management

The `update_claude_config()` function manages the `claude_desktop_config.json` file, handling:

- Server entry creation and updates
- Environment variable preservation and merging
- Absolute path resolution for server files
- UV command generation with dependency specifications

```
```

**Sources:** [src/mcp/cli/claude.py44-148](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L44-L148) [src/mcp/cli/claude.py101-125](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L101-L125) [src/mcp/cli/claude.py33-41](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L33-L41)

## Development Workflow Integration

The CLI system integrates with the broader MCP development ecosystem through several key mechanisms:

### Dependency Management with UV

All CLI commands use `uv` for Python dependency management, ensuring reproducible environments and fast package installation. The system automatically includes the `mcp[cli]` package and any server-specific dependencies.

### FastMCP Server Integration

The CLI specifically targets FastMCP servers and includes validation to ensure compatibility. It automatically extracts server metadata including:

- Server name for Claude Desktop registration
- Dependency requirements for installation
- Transport capabilities for runtime configuration

### Inspector Integration

The `dev` command integrates with the Node.js-based MCP Inspector tool, providing a web interface for interactive server testing and debugging.

**Sources:** [src/mcp/cli/cli.py260-284](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L260-L284) [src/mcp/cli/cli.py152-159](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L152-L159) [src/mcp/cli/cli.py442-455](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L442-L455)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development Tools & CLI](#development-tools-cli.md)
- [CLI Architecture](#cli-architecture.md)
- [CLI Command Structure](#cli-command-structure.md)
- [Server Import and Resolution](#server-import-and-resolution.md)
- [CLI Commands](#cli-commands.md)
- [Version Command](#version-command.md)
- [Development Command](#development-command.md)
- [Run Command](#run-command.md)
- [Install Command](#install-command.md)
- [Claude Desktop Integration](#claude-desktop-integration.md)
- [Configuration Path Detection](#configuration-path-detection.md)
- [Config File Management](#config-file-management.md)
- [Development Workflow Integration](#development-workflow-integration.md)
- [Dependency Management with UV](#dependency-management-with-uv.md)
- [FastMCP Server Integration](#fastmcp-server-integration.md)
- [Inspector Integration](#inspector-integration.md)
