Installation & Dependencies | modelcontextprotocol/python-sdk | DeepWiki

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

# Installation & Dependencies

Relevant source files

- [pyproject.toml](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml)
- [uv.lock](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/uv.lock)

This document covers the installation process for the MCP Python SDK and explains its dependency management system. It provides guidance on system requirements, installation methods, and the role of each dependency category in the SDK's functionality.

For information about core MCP concepts after installation, see [Key Concepts](modelcontextprotocol/python-sdk/1.2-key-concepts.md). For development environment setup including CLI tools, see [Development Environment](modelcontextprotocol/python-sdk/8.2-development-environment.md).

## System Requirements

The MCP Python SDK has specific system requirements that must be met before installation.

### Python Version Requirements

```
```

The SDK requires Python 3.10 or higher, with official support through Python 3.13. Platform-specific dependencies include `pywin32>=310` for Windows systems to support process management and inter-process communication.

**Sources:** [pyproject.toml6](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L6-L6) [pyproject.toml19-22](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L19-L22) [pyproject.toml35](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L35-L35)

### Package Manager Requirements

The project uses `uv` as its primary dependency manager with a minimum required version of 0.7.2. This is enforced through the build configuration to ensure consistent dependency resolution and workspace management.

**Sources:** [pyproject.toml46-48](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L46-L48)

## Installation Methods

### Standard Installation

The MCP SDK can be installed from PyPI using standard Python package managers:

```
```

### Optional Feature Installation

The SDK provides optional feature sets that can be installed as needed:

```
```

### Development Installation

For development work, install from source with development dependencies:

```
```

**Sources:** [pyproject.toml38-41](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L38-L41) [pyproject.toml43-44](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L43-L44)

## Core Dependencies Architecture

The following diagram shows how core dependencies support different functional areas of the MCP SDK:

```
```

**Sources:** [pyproject.toml24-36](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L24-L36)

### Core Dependency Functions

| Dependency          | Version         | Purpose                                                   |
| ------------------- | --------------- | --------------------------------------------------------- |
| `anyio`             | >=4.5           | Async I/O abstraction for cross-platform async operations |
| `httpx`             | >=0.27.1        | HTTP client for transport layer communication             |
| `httpx-sse`         | >=0.4           | Server-Sent Events support for real-time communication    |
| `pydantic`          | >=2.11.0,<3.0.0 | Data validation and serialization                         |
| `starlette`         | >=0.27          | ASGI web framework for server implementations             |
| `python-multipart`  | >=0.0.9         | Multipart form data parsing for HTTP transport            |
| `sse-starlette`     | >=1.6.1         | SSE server implementation for Starlette                   |
| `pydantic-settings` | >=2.5.2         | Configuration management with Pydantic                    |
| `uvicorn`           | >=0.31.1        | ASGI server (excluded on emscripten platform)             |
| `jsonschema`        | >=4.20.0        | JSON schema validation and generation                     |

## Optional Dependencies

### Feature-Specific Optional Dependencies

```
```

**Sources:** [pyproject.toml38-41](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L38-L41)

### CLI Script Configuration

The SDK provides a CLI entry point through the `mcp` command, which requires the `cli` optional dependency group to be installed. The CLI script configuration automatically includes the required dependencies when the CLI feature is requested.

**Sources:** [pyproject.toml43-44](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L43-L44)

## Development Dependencies

### Development Dependency Groups

```
```

The development environment automatically includes both `dev` and `docs` dependency groups through the default groups configuration.

**Sources:** [pyproject.toml46-47](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L46-L47) [pyproject.toml50-68](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L50-L68)

## Build System & Versioning

### Build Configuration

The SDK uses a modern Python build system with dynamic versioning:

| Component        | Tool                    | Purpose                              |
| ---------------- | ----------------------- | ------------------------------------ |
| Build Backend    | `hatchling`             | Modern Python packaging build system |
| Version Source   | `uv-dynamic-versioning` | Git-based dynamic version generation |
| Version Style    | `pep440`                | PEP 440 compliant version numbering  |
| Package Location | `src/mcp`               | Source package directory             |

The build system automatically generates versions from Git tags using PEP 440 formatting with bump support for development versions.

**Sources:** [pyproject.toml70-80](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L70-L80) [pyproject.toml87-88](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L87-L88)

## Dependency Management with uv

### Workspace Configuration

```
```

The uv workspace configuration enables unified dependency management across the main SDK package and all example projects. This ensures consistent dependency versions and simplifies development workflows.

**Sources:** [pyproject.toml136-140](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L136-L140) [pyproject.toml46-47](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L46-L47)

### Version Constraints

The uv configuration enforces minimum version requirements and provides automatic dependency resolution across the entire workspace. The required uv version (>=0.7.2) ensures access to modern workspace features and dependency group management.

**Sources:** [pyproject.toml46-48](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/pyproject.toml#L46-L48)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Installation & Dependencies](#installation-dependencies.md)
- [System Requirements](#system-requirements.md)
- [Python Version Requirements](#python-version-requirements.md)
- [Package Manager Requirements](#package-manager-requirements.md)
- [Installation Methods](#installation-methods.md)
- [Standard Installation](#standard-installation.md)
- [Optional Feature Installation](#optional-feature-installation.md)
- [Development Installation](#development-installation.md)
- [Core Dependencies Architecture](#core-dependencies-architecture.md)
- [Core Dependency Functions](#core-dependency-functions.md)
- [Optional Dependencies](#optional-dependencies.md)
- [Feature-Specific Optional Dependencies](#feature-specific-optional-dependencies.md)
- [CLI Script Configuration](#cli-script-configuration.md)
- [Development Dependencies](#development-dependencies.md)
- [Development Dependency Groups](#development-dependency-groups.md)
- [Build System & Versioning](#build-system-versioning.md)
- [Build Configuration](#build-configuration.md)
- [Dependency Management with uv](#dependency-management-with-uv.md)
- [Workspace Configuration](#workspace-configuration.md)
- [Version Constraints](#version-constraints.md)
