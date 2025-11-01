Installation and Setup | jlowin/fastmcp | DeepWiki

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

# Installation and Setup

Relevant source files

- [.github/workflows/run-tests.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml)
- [pyproject.toml](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml)
- [tests/test\_mcp\_config.py](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/test_mcp_config.py)
- [uv.lock](https://github.com/jlowin/fastmcp/blob/66221ed3/uv.lock)

This document covers the installation procedures, dependency management, and initial configuration for the FastMCP framework. It provides step-by-step instructions for setting up a development or production environment.

For information about running FastMCP servers and CLI commands, see [Command Line Interface](jlowin/fastmcp/5-command-line-interface.md). For details about server configuration and settings, see [Configuration Management](jlowin/fastmcp/8-testing-and-development-framework.md).

## System Requirements

FastMCP requires Python 3.10 or higher and uses UV as the primary package manager for dependency resolution and virtual environment management.

### Python Version Support

| Python Version | Support Status  |
| -------------- | --------------- |
| 3.10           | ✅ Supported     |
| 3.11           | ✅ Supported     |
| 3.12           | ✅ Supported     |
| < 3.10         | ❌ Not supported |

**Sources:** [pyproject.toml20](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L20-L20) [pyproject.toml37-39](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L37-L39)

## Installation Methods

### UV Package Manager Installation

The recommended installation method uses UV for optimal dependency resolution and environment isolation:

```
```

### Development Installation

For development work, install with development dependencies:

```
```

**Sources:** [.github/workflows/run-tests.yml46-48](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml#L46-L48) [pyproject.toml47-71](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L47-L71)

## Dependency Architecture

The following diagram shows the core dependency structure and how packages map to FastMCP functionality:

```
```

**Sources:** [pyproject.toml6-18](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L6-L18) [pyproject.toml43-46](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L43-L46) [pyproject.toml47-71](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L47-L71)

## Project Configuration Files

FastMCP uses several configuration files for different aspects of the development and runtime environment:

### Build and Dependency Configuration

```
```

**Sources:** [pyproject.toml1-143](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L1-L143) [uv.lock1-8](https://github.com/jlowin/fastmcp/blob/66221ed3/uv.lock#L1-L8) [.pre-commit-config.yaml1-42](https://github.com/jlowin/fastmcp/blob/66221ed3/.pre-commit-config.yaml#L1-L42)

### CLI Script Configuration

The `fastmcp` command-line interface is configured as an entry point script:

| Configuration | Value                             | Purpose                             |
| ------------- | --------------------------------- | ----------------------------------- |
| Script name   | `fastmcp`                         | CLI command name                    |
| Entry point   | `fastmcp.cli:app`                 | Module and function path            |
| Dependencies  | `cyclopts>=3.0.0`, `rich>=13.9.4` | CLI framework and output formatting |

**Sources:** [pyproject.toml73-74](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L73-L74) [pyproject.toml12-13](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L12-L13)

## Environment Setup

### Environment Variables

FastMCP supports several environment variables for configuration:

| Variable                         | Purpose                      | Default |
| -------------------------------- | ---------------------------- | ------- |
| `FASTMCP_TEST_MODE`              | Enable test mode             | `0`     |
| `FASTMCP_LOG_LEVEL`              | Set logging level            | `INFO`  |
| `FASTMCP_ENABLE_RICH_TRACEBACKS` | Enable rich error formatting | `1`     |

### Testing Environment

The testing environment is configured with specific settings:

```
```

**Sources:** [pyproject.toml98-119](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L98-L119) [.github/workflows/run-tests.yml25-82](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml#L25-L82) [.github/workflows/run-static.yml26-55](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-static.yml#L26-L55)

## Authentication Setup

For development and testing with authentication providers, additional environment variables are required:

### GitHub OAuth Configuration

| Variable                                 | Purpose             | Required For        |
| ---------------------------------------- | ------------------- | ------------------- |
| `FASTMCP_GITHUB_TOKEN`                   | GitHub API access   | GitHub integrations |
| `FASTMCP_TEST_AUTH_GITHUB_CLIENT_ID`     | OAuth client ID     | GitHub auth testing |
| `FASTMCP_TEST_AUTH_GITHUB_CLIENT_SECRET` | OAuth client secret | GitHub auth testing |

**Sources:** [tests/integration\_tests/auth/test\_github\_provider\_integration.py25-28](https://github.com/jlowin/fastmcp/blob/66221ed3/tests/integration_tests/auth/test_github_provider_integration.py#L25-L28) [.github/workflows/run-tests.yml79-81](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml#L79-L81)

## Installation Verification

After installation, verify the setup using these commands:

### Basic Verification

```
```

### Development Environment Verification

```
```

**Sources:** [.github/workflows/run-tests.yml50-54](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-tests.yml#L50-L54) [.github/workflows/run-static.yml44-54](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-static.yml#L44-L54) [.pre-commit-config.yaml27-34](https://github.com/jlowin/fastmcp/blob/66221ed3/.pre-commit-config.yaml#L27-L34)

## Troubleshooting Common Issues

### Dependency Resolution Issues

If UV fails to resolve dependencies, ensure the lockfile is up to date:

```
```

### Python Version Compatibility

Verify Python version compatibility if installation fails:

```
```

**Sources:** [.github/workflows/run-static.yml44-50](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/run-static.yml#L44-L50) [pyproject.toml20](https://github.com/jlowin/fastmcp/blob/66221ed3/pyproject.toml#L20-L20)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Installation and Setup](#installation-and-setup.md)
- [System Requirements](#system-requirements.md)
- [Python Version Support](#python-version-support.md)
- [Installation Methods](#installation-methods.md)
- [UV Package Manager Installation](#uv-package-manager-installation.md)
- [Development Installation](#development-installation.md)
- [Dependency Architecture](#dependency-architecture.md)
- [Project Configuration Files](#project-configuration-files.md)
- [Build and Dependency Configuration](#build-and-dependency-configuration.md)
- [CLI Script Configuration](#cli-script-configuration.md)
- [Environment Setup](#environment-setup.md)
- [Environment Variables](#environment-variables.md)
- [Testing Environment](#testing-environment.md)
- [Authentication Setup](#authentication-setup.md)
- [GitHub OAuth Configuration](#github-oauth-configuration.md)
- [Installation Verification](#installation-verification.md)
- [Basic Verification](#basic-verification.md)
- [Development Environment Verification](#development-environment-verification.md)
- [Troubleshooting Common Issues](#troubleshooting-common-issues.md)
- [Dependency Resolution Issues](#dependency-resolution-issues.md)
- [Python Version Compatibility](#python-version-compatibility.md)
