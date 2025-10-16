Claude Desktop Integration | modelcontextprotocol/python-sdk | DeepWiki

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

# Claude Desktop Integration

Relevant source files

- [examples/fastmcp/unicode\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/fastmcp/unicode_example.py)
- [src/mcp/cli/claude.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py)
- [src/mcp/cli/cli.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py)
- [tests/client/test\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_config.py)
- [tests/issues/test\_100\_tool\_listing.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_100_tool_listing.py)

This document covers the integration of MCP servers with the Claude Desktop application. The integration allows MCP servers built with the Python SDK to be automatically discovered and used by Claude Desktop through configuration file management and standardized execution commands.

For information about building MCP servers, see [FastMCP Server Framework](modelcontextprotocol/python-sdk/2-fastmcp-server-framework.md). For CLI development tools, see [MCP CLI Commands](modelcontextprotocol/python-sdk/8.1-mcp-cli-commands.md).

## Integration Architecture

The Claude Desktop integration operates through a configuration-based approach where MCP servers are registered in Claude Desktop's configuration file and executed via standardized `uv run` commands.

```
```

**Claude Desktop Integration Architecture**

Sources: [src/mcp/cli/claude.py44-148](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L44-L148) [src/mcp/cli/cli.py362-488](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L362-L488)

## Installation Process

The installation process uses the `mcp install` command to register MCP servers with Claude Desktop. The process involves server discovery, dependency resolution, and configuration file updates.

```
```

**MCP Server Installation Flow**

The installation process handles several key aspects:

| Component             | Function                 | Purpose                                            |
| --------------------- | ------------------------ | -------------------------------------------------- |
| File parsing          | `_parse_file_path()`     | Extracts file path and optional server object name |
| Server import         | `_import_server()`       | Loads server to extract metadata and dependencies  |
| Config update         | `update_claude_config()` | Updates Claude's configuration file                |
| Dependency resolution | Server.dependencies      | Automatically includes required packages           |

Sources: [src/mcp/cli/cli.py420-488](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L420-L488) [src/mcp/cli/cli.py88-117](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L88-L117) [src/mcp/cli/cli.py119-208](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L119-L208)

## Configuration File Structure

Claude Desktop uses a JSON configuration file to store MCP server definitions. The configuration file follows a specific structure that defines execution commands, environment variables, and server metadata.

```
```

**Configuration File Structure**

The generated configuration follows this pattern:

```
```

Sources: [src/mcp/cli/claude.py87-135](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L87-L135) [src/mcp/cli/claude.py101-125](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L101-L125)

## Platform-Specific Configuration Paths

The system automatically detects Claude Desktop's configuration directory based on the operating system platform using standardized application data locations.

```
```

**Platform-Specific Configuration Paths**

| Platform | Configuration Path                              | Environment Variable |
| -------- | ----------------------------------------------- | -------------------- |
| Windows  | `%USERPROFILE%\AppData\Roaming\Claude`          | -                    |
| macOS    | `~/Library/Application Support/Claude`          | -                    |
| Linux    | `$XDG_CONFIG_HOME/Claude` or `~/.config/Claude` | `XDG_CONFIG_HOME`    |

Sources: [src/mcp/cli/claude.py17-30](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L17-L30)

## Environment Variables and Dependencies

The configuration system supports environment variables and automatic dependency management for MCP servers. Environment variables are preserved across updates and can be loaded from files or command line arguments.

```
```

**Environment and Dependency Management**

The system handles environment variables with the following precedence:

1. New command-line variables override existing ones
2. Existing variables are preserved if not explicitly updated
3. Variables from `.env` files are loaded using the `python-dotenv` library

Dependency management includes:

- Automatic inclusion of `mcp[cli]` package
- Server-specific dependencies from `server.dependencies` attribute
- Additional packages specified via `--with` flags
- Editable package installations via `--with-editable`

Sources: [src/mcp/cli/claude.py92-99](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L92-L99) [src/mcp/cli/cli.py452-456](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L452-L456) [src/mcp/cli/cli.py104-115](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L104-L115) [src/mcp/cli/cli.py458-476](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/cli.py#L458-L476)

## UV Command Generation

The integration generates standardized `uv run` commands that Claude Desktop executes to launch MCP servers. The command structure ensures proper dependency isolation and package management.

```
```

**UV Command Generation Process**

The system generates commands following this pattern:

```
```

Key aspects of command generation:

- Uses absolute path to `uv` executable for reliability
- Converts relative file paths to absolute paths
- Preserves server object specifications (e.g., `server.py:app`)
- Deduplicates packages while preserving order
- Handles Windows drive letter syntax correctly

Sources: [src/mcp/cli/claude.py33-41](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L33-L41) [src/mcp/cli/claude.py101-125](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L101-L125) [src/mcp/cli/claude.py116-122](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/cli/claude.py#L116-L122)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Claude Desktop Integration](#claude-desktop-integration.md)
- [Integration Architecture](#integration-architecture.md)
- [Installation Process](#installation-process.md)
- [Configuration File Structure](#configuration-file-structure.md)
- [Platform-Specific Configuration Paths](#platform-specific-configuration-paths.md)
- [Environment Variables and Dependencies](#environment-variables-and-dependencies.md)
- [UV Command Generation](#uv-command-generation.md)
