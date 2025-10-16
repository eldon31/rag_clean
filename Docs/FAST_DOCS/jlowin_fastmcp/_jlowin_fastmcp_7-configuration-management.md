Configuration Management | jlowin/fastmcp | DeepWiki

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

# Configuration Management

Relevant source files

- [.github/workflows/run-tests.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml)
- [pyproject.toml](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml)
- [tests/test\_mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py)
- [uv.lock](https://github.com/jlowin/fastmcp/blob/66221ed3/uv.lock)

This document covers FastMCP's configuration management system, which enables declarative server definitions, multi-server orchestration, and standardized MCP client configurations. The system provides both programmatic and file-based configuration approaches for defining MCP servers, their connections, authentication, and behavioral transformations.

For information about HTTP server deployment configuration, see [HTTP Server and Deployment](jlowin/fastmcp/4-http-server-and-deployment.md). For CLI-based configuration commands, see [Command Line Interface](jlowin/fastmcp/5-command-line-interface.md). For project build and dependency configuration, see [Installation and Setup](jlowin/fastmcp/1.1-installation-and-setup.md).

## Configuration System Architecture

The configuration management system centers around the `MCPConfig` class hierarchy, which provides both standard and canonical configuration formats for defining MCP servers and their properties.

```
```

Sources: [tests/test\_mcp\_config.py25-33](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L25-L33) [src/fastmcp/mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/mcp_config.py)

## Server Configuration Types

FastMCP supports three primary server configuration types, each designed for different deployment scenarios and capability requirements.

### StdioMCPServer Configuration

`StdioMCPServer` configurations define local subprocess-based MCP servers that communicate via standard input/output streams.

```
```

Example configuration structure:

```
```

Sources: [tests/test\_mcp\_config.py50-63](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L50-L63) [tests/test\_mcp\_config.py177-202](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L177-L202)

### RemoteMCPServer Configuration

`RemoteMCPServer` configurations define HTTP-based remote MCP servers with automatic transport inference and authentication support.

```
```

The system automatically infers `SSETransport` for URLs containing `/sse/` paths, while defaulting to `StreamableHttpTransport` for other HTTP endpoints.

Sources: [tests/test\_mcp\_config.py134-175](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L134-L175) [tests/test\_mcp\_config.py412-467](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L412-L467)

### TransformingStdioMCPServer Configuration

`TransformingStdioMCPServer` extends stdio servers with tool and resource transformation capabilities, enabling name remapping, argument transformation, and selective inclusion/exclusion.

```
```

Sources: [tests/test\_mcp\_config.py534-588](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L534-L588) [tests/test\_mcp\_config.py639-698](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L639-L698)

## Configuration File Formats

FastMCP supports multiple configuration input formats with automatic normalization and validation.

### Dictionary-based Configuration

The system accepts both nested `mcpServers` format and root-level server definitions:

```
```

The parser automatically detects and normalizes root-level server definitions to the standard nested format.

Sources: [tests/test\_mcp\_config.py86-99](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L86-L99) [tests/test\_mcp\_config.py66-84](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L66-L84)

### Configuration Discrimination

The system uses discriminated unions to automatically select appropriate server types based on configuration content:

```
```

Sources: [tests/test\_mcp\_config.py101-132](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L101-L132)

## Transport Configuration and Generation

The configuration system generates appropriate transport instances based on server definitions, with automatic inference and override capabilities.

### Transport Generation Pipeline

```
```

Sources: [tests/test\_mcp\_config.py142-175](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L142-L175) [src/fastmcp/client/transports.py](https://github.com/jlowin/fastmcp/blob/66221ed3/src/fastmcp/client/transports.py)

## Authentication Configuration

FastMCP provides flexible authentication configuration supporting bearer tokens and OAuth flows for remote servers.

### Authentication Types

```
```

Authentication is automatically applied to both `StreamableHttpTransport` and `SSETransport` instances based on the remote server configuration.

Sources: [tests/test\_mcp\_config.py425-467](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L425-L467)

## Multi-Server Orchestration

The `MCPConfigTransport` enables simultaneous connection to multiple MCP servers with unified tool/resource/prompt namespacing.

### Multi-Server Architecture

```
```

Each server's tools, resources, and prompts are prefixed with the server name (e.g., `server_name_tool_name`) to avoid conflicts while maintaining clear attribution.

Sources: [tests/test\_mcp\_config.py204-244](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L204-L244) [tests/test\_mcp\_config.py469-532](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L469-L532) [tests/test\_mcp\_config.py700-740](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py#L700-L740)

## Environment and Project Configuration

FastMCP integrates with standard Python project configuration through `pyproject.toml` and supports environment-based configuration management.

### Project Configuration Structure

```
```

The configuration system supports environment variable-based test configuration through `FASTMCP_TEST_MODE`, `FASTMCP_LOG_LEVEL`, and other `FASTMCP_*` prefixed variables.

Sources: [pyproject.toml1-147](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L1-L147) [.github/workflows/run-tests.yml78-81](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml#L78-L81)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Configuration Management](#configuration-management.md)
- [Configuration System Architecture](#configuration-system-architecture.md)
- [Server Configuration Types](#server-configuration-types.md)
- [StdioMCPServer Configuration](#stdiomcpserver-configuration.md)
- [RemoteMCPServer Configuration](#remotemcpserver-configuration.md)
- [TransformingStdioMCPServer Configuration](#transformingstdiomcpserver-configuration.md)
- [Configuration File Formats](#configuration-file-formats.md)
- [Dictionary-based Configuration](#dictionary-based-configuration.md)
- [Configuration Discrimination](#configuration-discrimination.md)
- [Transport Configuration and Generation](#transport-configuration-and-generation.md)
- [Transport Generation Pipeline](#transport-generation-pipeline.md)
- [Authentication Configuration](#authentication-configuration.md)
- [Authentication Types](#authentication-types.md)
- [Multi-Server Orchestration](#multi-server-orchestration.md)
- [Multi-Server Architecture](#multi-server-architecture.md)
- [Environment and Project Configuration](#environment-and-project-configuration.md)
- [Project Configuration Structure](#project-configuration-structure.md)
