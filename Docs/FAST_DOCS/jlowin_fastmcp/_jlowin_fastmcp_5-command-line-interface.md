Command Line Interface | jlowin/fastmcp | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[jlowin/fastmcp](https://github.com/jlowin/fastmcp "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 30 September 2025 ([66221e](https://github.com/jlowin/fastmcp/commits/66221ed3))

- [FastMCP Overview](jlowin/fastmcp/1-fastmcp-overview.md)
- [Installation and Setup](jlowin/fastmcp/1.1-installation-and-setup.md)
- [FastMCP Server Core](jlowin/fastmcp/2-fastmcp-server-core.md)
- [Component System Architecture](jlowin/fastmcp/2.1-component-system-architecture.md)
- [Context System and Dependencies](jlowin/fastmcp/2.2-context-system-and-dependencies.md)
- [Server Composition and Proxying](jlowin/fastmcp/2.3-server-composition-and-proxying.md)
- [FastMCP Client System](jlowin/fastmcp/3-fastmcp-client-system.md)
- [Transport Mechanisms](jlowin/fastmcp/3.1-transport-mechanisms.md)
- [Client Authentication](jlowin/fastmcp/3.2-client-authentication.md)
- [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md)
- [Authentication and Security](jlowin/fastmcp/4.1-authentication-and-security.md)
- [Middleware System](jlowin/fastmcp/4.2-middleware-system.md)
- [Command Line Interface](jlowin/fastmcp/5-command-line-interface.md)
- [OpenAPI Integration](jlowin/fastmcp/6-openapi-integration.md)
- [Configuration Management](jlowin/fastmcp/7-configuration-management.md)
- [Testing and Development Framework](jlowin/fastmcp/8-testing-and-development-framework.md)
- [Project Infrastructure](jlowin/fastmcp/9-project-infrastructure.md)
- [Documentation and Updates](jlowin/fastmcp/10-documentation-and-updates.md)

Menu

# Command Line Interface

Relevant source files

- [docs/patterns/cli.mdx](https://github.com/jlowin/fastmcp/blob/66221ed3/docs/patterns/cli.mdx)
- [src/fastmcp/cli/claude.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/claude.py)
- [src/fastmcp/cli/cli.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py)
- [src/fastmcp/cli/install/claude\_code.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_code.py)
- [src/fastmcp/cli/install/claude\_desktop.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_desktop.py)
- [src/fastmcp/cli/install/cursor.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/cursor.py)
- [src/fastmcp/cli/install/mcp\_json.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/mcp_json.py)
- [src/fastmcp/cli/run.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py)
- [tests/cli/test\_cli.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/cli/test_cli.py)
- [tests/cli/test\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/cli/test_config.py)
- [tests/cli/test\_cursor.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/cli/test_cursor.py)
- [tests/cli/test\_run\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/cli/test_run_config.py)
- [tests/utilities/test\_cli.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/utilities/test_cli.py)

The FastMCP CLI provides a comprehensive command-line interface for running, developing, installing, and inspecting MCP servers. Built with `cyclopts`, it serves as the primary entry point for all FastMCP operations from development to production deployment.

For information about the underlying server architecture that the CLI manages, see [FastMCP Server Core](jlowin/fastmcp/2-fastmcp-server-core.md). For details about client-server communication patterns, see [FastMCP Client System](jlowin/fastmcp/3-fastmcp-client-system.md).

## CLI Application Architecture

The FastMCP CLI is implemented as a `cyclopts.App` with modular command structure supporting both direct execution and subprocess delegation through `uv`.

### Main CLI Application Structure

```
```

**Sources:** [src/fastmcp/cli/cli.py36-40](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L36-L40) [src/fastmcp/cli/cli.py781-782](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L781-L782) [src/fastmcp/cli/cli.py871-874](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L871-L874)

### Configuration and Environment Management

```
```

**Sources:** [src/fastmcp/utilities/cli.py23](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/cli.py#L23-L23) [src/fastmcp/cli/cli.py465-469](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L465-L469) [src/fastmcp/cli/cli.py497-517](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L497-L517)

## Core CLI Commands

### Version Command

The `version()` command provides comprehensive version and platform information for debugging and support purposes.

| Option | Flag     | Description                                             |
| ------ | -------- | ------------------------------------------------------- |
| Copy   | `--copy` | Copy version information to clipboard using `pyperclip` |

Information displayed:

- `fastmcp.__version__` - FastMCP version
- `importlib.metadata.version("mcp")` - MCP protocol version
- `platform.python_version()` - Python version
- `platform.platform()` - Platform details
- `Path(fastmcp.__file__).resolve().parents[1]` - FastMCP root path

**Sources:** [src/fastmcp/cli/cli.py92-127](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L92-L127)

### Run Command

The `run()` command executes MCP servers with flexible server specification parsing and multiple execution modes.

#### Server Specification Resolution

```
```

**Sources:** [src/fastmcp/cli/run.py79-198](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L79-L198) [src/fastmcp/cli/run.py25-29](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L25-L29) [src/fastmcp/cli/run.py31-49](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L31-L49) [src/fastmcp/cli/run.py51-60](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L51-L60)

#### Transport Configuration

| Transport                  | Default Host | Default Port | Default Path |
| -------------------------- | ------------ | ------------ | ------------ |
| `stdio`                    | N/A          | N/A          | N/A          |
| `http` / `streamable-http` | `127.0.0.1`  | `8000`       | `/mcp/`      |
| `sse`                      | `127.0.0.1`  | `8000`       | `/sse/`      |

The run command supports both direct execution and `uv run` subprocess execution based on environment configuration.

**Sources:** [src/fastmcp/cli/cli.py313-333](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L313-L333) [src/fastmcp/cli/cli.py465-517](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L465-L517)

### Dev Command

The `dev()` command launches the MCP Inspector with automatic environment setup and dependency management.

#### Development Workflow

```
```

The `dev` command always runs via `uv run` subprocess and includes deprecation warnings for servers using the legacy `dependencies` parameter.

**Sources:** [src/fastmcp/cli/cli.py129-307](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L129-L307) [src/fastmcp/cli/cli.py43-56](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L43-L56) [src/fastmcp/cli/cli.py234-251](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L234-L251)

### Inspect Command

The `inspect()` command analyzes FastMCP servers and generates detailed reports in multiple formats.

| Option | Flag              | Description                        |
| ------ | ----------------- | ---------------------------------- |
| Format | `--format` / `-f` | Output format: `fastmcp` or `mcp`  |
| Output | `--output` / `-o` | Save to file (requires `--format`) |

#### Inspection Process

```
```

**Sources:** [src/fastmcp/cli/cli.py543-777](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L543-L777) [src/fastmcp/utilities/inspect.py26-28](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/inspect.py#L26-L28)

## Install Commands

The FastMCP CLI provides installation commands for multiple MCP clients through a dedicated install subcommand structure.

### Install Command Architecture

```
```

**Sources:** [src/fastmcp/cli/cli.py874](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L874-L874) [src/fastmcp/cli/install/claude\_code.py153-244](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_code.py#L153-L244) [src/fastmcp/cli/install/claude\_desktop.py125-214](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_desktop.py#L125-L214) [src/fastmcp/cli/install/cursor.py234-331](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/cursor.py#L234-L331) [src/fastmcp/cli/install/mcp\_json.py98-196](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/mcp_json.py#L98-L196)

### Client-Specific Installation

#### Claude Desktop Integration

```
```

**Sources:** [src/fastmcp/cli/install/claude\_desktop.py20-36](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_desktop.py#L20-L36) [src/fastmcp/cli/install/claude\_desktop.py38-123](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_desktop.py#L38-L123)

#### Cursor Integration

```
```

**Sources:** [src/fastmcp/cli/install/cursor.py21-43](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/cursor.py#L21-L43) [src/fastmcp/cli/install/cursor.py45-66](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/cursor.py#L45-L66)

### Project Preparation

The `project prepare` command creates persistent environments for repeated server execution.

#### Project Prepare Flow

```
```

**Sources:** [src/fastmcp/cli/cli.py784-867](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L784-L867) [src/fastmcp/utilities/mcp\_server\_config/\_\_init\_\_.py31](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/mcp_server_config/__init__.py#L31-L31) [src/fastmcp/utilities/mcp\_server\_config/\_\_init\_\_.py55-57](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/mcp_server_config/__init__.py#L55-L57)

## Configuration System Integration

### Configuration Loading and Merging

The CLI integrates with the FastMCP configuration system to provide seamless operation across different deployment scenarios.

```
```

**Sources:** [src/fastmcp/utilities/cli.py23](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/utilities/cli.py#L23-L23) [src/fastmcp/cli/cli.py424-439](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L424-L439) [src/fastmcp/cli/cli.py467-469](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L467-L469)

## Error Handling and Platform Support

### Cross-Platform Command Detection

The CLI handles platform-specific differences for external tool detection and subprocess execution.

```
```

**Sources:** [src/fastmcp/cli/cli.py43-56](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L43-L56) [src/fastmcp/cli/install/claude\_code.py20-66](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/claude_code.py#L20-L66) [src/fastmcp/cli/install/cursor.py45-66](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/install/cursor.py#L45-L66)

## Command Execution Patterns

### UV Integration

The CLI leverages `uv` for modern Python dependency management and isolated execution environments:

```
```

**Sources:** [src/fastmcp/cli/cli.py60-100](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L60-L100) [src/fastmcp/cli/cli.py389-413](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L389-L413) [src/fastmcp/cli/run.py174-250](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L174-L250)

### Cross-Platform Considerations

The CLI handles platform-specific differences, particularly for Windows systems:

| Platform  | NPX Detection                   | Shell Usage   | Path Handling               |
| --------- | ------------------------------- | ------------- | --------------------------- |
| Windows   | Try `npx.cmd`, `npx.exe`, `npx` | `shell=True`  | Drive letter colon handling |
| Unix-like | Use `npx` directly              | `shell=False` | Standard path parsing       |

**Sources:** [src/fastmcp/cli/cli.py35-49](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L35-L49) [src/fastmcp/cli/cli.py257-262](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L257-L262)

## Error Handling and Validation

The CLI implements comprehensive error handling with structured logging:

- **File validation**: Checks for file existence and type during path parsing
- **Module import errors**: Graceful handling of import failures with descriptive messages
- **Server validation**: Ensures imported objects are valid FastMCP instances
- **Subprocess errors**: Captures and reports subprocess execution failures
- **Configuration validation**: Validates MCP config files using Pydantic models

Exit codes follow standard conventions:

- `0`: Success
- `1`: General errors (file not found, import failures, validation errors)

**Sources:** [src/fastmcp/cli/run.py52-57](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L52-L57) [src/fastmcp/cli/run.py94-100](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L94-L100) [src/fastmcp/cli/run.py118-124](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/run.py#L118-L124) [src/fastmcp/cli/cli.py265-282](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/cli/cli.py#L265-L282)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Command Line Interface](#command-line-interface.md)
- [CLI Application Architecture](#cli-application-architecture.md)
- [Main CLI Application Structure](#main-cli-application-structure.md)
- [Configuration and Environment Management](#configuration-and-environment-management.md)
- [Core CLI Commands](#core-cli-commands.md)
- [Version Command](#version-command.md)
- [Run Command](#run-command.md)
- [Server Specification Resolution](#server-specification-resolution.md)
- [Transport Configuration](#transport-configuration.md)
- [Dev Command](#dev-command.md)
- [Development Workflow](#development-workflow.md)
- [Inspect Command](#inspect-command.md)
- [Inspection Process](#inspection-process.md)
- [Install Commands](#install-commands.md)
- [Install Command Architecture](#install-command-architecture.md)
- [Client-Specific Installation](#client-specific-installation.md)
- [Claude Desktop Integration](#claude-desktop-integration.md)
- [Cursor Integration](#cursor-integration.md)
- [Project Preparation](#project-preparation.md)
- [Project Prepare Flow](#project-prepare-flow.md)
- [Configuration System Integration](#configuration-system-integration.md)
- [Configuration Loading and Merging](#configuration-loading-and-merging.md)
- [Error Handling and Platform Support](#error-handling-and-platform-support.md)
- [Cross-Platform Command Detection](#cross-platform-command-detection.md)
- [Command Execution Patterns](#command-execution-patterns.md)
- [UV Integration](#uv-integration.md)
- [Cross-Platform Considerations](#cross-platform-considerations.md)
- [Error Handling and Validation](#error-handling-and-validation.md)
