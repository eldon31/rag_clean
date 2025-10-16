Development Environment | modelcontextprotocol/python-sdk | DeepWiki

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

# Development Environment

Relevant source files

- [.github/workflows/publish-docs-manually.yml](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.github/workflows/publish-docs-manually.yml)
- [.github/workflows/publish-pypi.yml](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.github/workflows/publish-pypi.yml)
- [.github/workflows/shared.yml](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.github/workflows/shared.yml)
- [.pre-commit-config.yaml](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.pre-commit-config.yaml)
- [CLAUDE.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md)
- [CODE\_OF\_CONDUCT.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CONTRIBUTING.md)
- [SECURITY.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/SECURITY.md)
- [examples/clients/simple-chatbot/README.MD](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/README.MD)
- [examples/servers/simple-streamablehttp-stateless/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp-stateless/README.md)
- [examples/servers/simple-streamablehttp/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp/README.md)

This document covers the development setup, code quality standards, pre-commit hooks, and contribution workflow for the MCP Python SDK. It provides the complete toolchain configuration and processes for maintaining code quality using uv and modern Python development tools.

For information about CLI commands and project management workflows, see [MCP CLI Commands](modelcontextprotocol/python-sdk/8.1-mcp-cli-commands.md). For Claude Desktop integration setup, see [Claude Desktop Integration](modelcontextprotocol/python-sdk/8.3-claude-desktop-integration.md).

## Development Setup Requirements

The MCP Python SDK uses a modern Python development stack with strict tooling requirements to ensure code quality and consistency.

### Core Requirements

| Requirement | Version | Purpose                        |
| ----------- | ------- | ------------------------------ |
| Python      | 3.10+   | Runtime environment            |
| uv          | Latest  | Package and project management |
| pre-commit  | Latest  | Git hook automation            |

### Installation Process

The development environment setup follows a specific sequence to ensure all tools are properly configured:

```
```

**Development Environment Setup Flow**

Sources: [CONTRIBUTING.md7-22](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CONTRIBUTING.md#L7-L22) [CLAUDE.md7-12](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L7-L12)

## Package Management with uv

The project exclusively uses `uv` for all package management operations. Traditional `pip` usage is explicitly forbidden to ensure consistent dependency resolution and lock file management.

### uv Command Patterns

```
```

**uv Package Management Commands**

| Operation          | Command                                          | Purpose                                |
| ------------------ | ------------------------------------------------ | -------------------------------------- |
| Add dependency     | `uv add package`                                 | Install production dependency          |
| Add dev dependency | `uv add --dev package`                           | Install development dependency         |
| Upgrade package    | `uv add --dev package --upgrade-package package` | Update specific package                |
| Run tool           | `uv run tool`                                    | Execute tool with project dependencies |
| Sync dependencies  | `uv sync --frozen --all-extras --dev`            | Install all dependencies from lock     |
| Check lock file    | `uv lock --check`                                | Verify lock file is current            |

Sources: [CLAUDE.md7-12](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L7-L12) [.pre-commit-config.yaml48-52](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.pre-commit-config.yaml#L48-L52)

## Code Quality Standards

The project enforces strict code quality standards through automated tooling and explicit requirements for all contributions.

### Code Quality Tools Integration

```
```

**Code Quality Tool Chain**

### Quality Requirements

| Requirement    | Tool    | Configuration            |
| -------------- | ------- | ------------------------ |
| Line length    | ruff    | 120 characters maximum   |
| Type hints     | pyright | Required for all code    |
| Docstrings     | manual  | Required for public APIs |
| Import sorting | ruff    | I001 rule enforcement    |
| Function size  | manual  | Small, focused functions |

### Tool Execution Commands

| Tool            | Format Command                  | Check Command                        |
| --------------- | ------------------------------- | ------------------------------------ |
| ruff            | `uv run --frozen ruff format .` | `uv run --frozen ruff check .`       |
| ruff (with fix) | N/A                             | `uv run --frozen ruff check . --fix` |
| pyright         | N/A                             | `uv run --frozen pyright`            |

Sources: [CLAUDE.md14-20](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L14-L20) [CLAUDE.md60-78](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L60-L78) [.pre-commit-config.yaml26-46](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.pre-commit-config.yaml#L26-L46)

## Pre-commit Hooks System

The project uses an automated pre-commit hook system that runs multiple quality checks on every commit to ensure code standards are maintained.

### Pre-commit Hook Configuration

```
```

**Pre-commit Hook Execution Flow**

### Hook Configuration Details

The pre-commit configuration in [.pre-commit-config.yaml1-59](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.pre-commit-config.yaml#L1-L59) defines the complete hook pipeline:

| Hook            | Type     | Purpose                       | Files                           |
| --------------- | -------- | ----------------------------- | ------------------------------- |
| prettier        | External | Format YAML/JSON5             | `types_or: [yaml, json5]`       |
| markdownlint    | External | Lint Markdown files           | `types: [markdown]`             |
| ruff-format     | Local    | Python code formatting        | `types: [python]`               |
| ruff            | Local    | Python linting with auto-fix  | `types: [python]`               |
| pyright         | Local    | Python type checking          | `types: [python]`               |
| uv-lock-check   | Local    | Verify uv.lock currency       | `^(pyproject\.toml\|uv\.lock)$` |
| readme-snippets | Local    | Validate README code snippets | README and example files        |

### Pre-commit Execution

| Operation           | Command                                                             | Purpose                       |
| ------------------- | ------------------------------------------------------------------- | ----------------------------- |
| Install hooks       | `uv tool install pre-commit --with pre-commit-uv --force-reinstall` | Set up pre-commit system      |
| Run on all files    | `pre-commit run --all-files`                                        | Manual execution of all hooks |
| Automatic execution | Triggered on `git commit`                                           | Automatic quality gate        |

Sources: [.pre-commit-config.yaml1-59](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.pre-commit-config.yaml#L1-L59) [CONTRIBUTING.md17-22](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CONTRIBUTING.md#L17-L22) [CLAUDE.md80-87](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L80-L87)

## Testing Framework

The project uses pytest with anyio for async testing, with specific configuration requirements to ensure consistent test execution.

### Testing Configuration

```
```

**Testing Framework Architecture**

### Testing Requirements

| Requirement   | Implementation        | Notes                                   |
| ------------- | --------------------- | --------------------------------------- |
| Test runner   | pytest                | Framework: `uv run --frozen pytest`     |
| Async testing | anyio                 | NOT asyncio for async tests             |
| Coverage      | Edge cases and errors | Required for all code paths             |
| New features  | Tests required        | Must include tests with feature         |
| Bug fixes     | Regression tests      | Must include test preventing regression |

### Test Execution Commands

| Command                                                    | Purpose                    | Environment Variable                |
| ---------------------------------------------------------- | -------------------------- | ----------------------------------- |
| `uv run --frozen pytest`                                   | Standard test execution    | None                                |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD="" uv run --frozen pytest` | Plugin conflict resolution | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=""` |

Sources: [CLAUDE.md21-27](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L21-L27) [CLAUDE.md111-114](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L111-L114) [CONTRIBUTING.md34-38](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CONTRIBUTING.md#L34-L38)

## Development Workflow

The development workflow integrates all quality tools into a structured process that ensures code quality and proper contribution management.

### Complete Development Workflow

```
```

**Complete Development Workflow Process**

### Error Resolution Priority

The development guidelines specify a specific order for resolving CI failures:

| Priority | Issue Type  | Common Solutions                                   |
| -------- | ----------- | -------------------------------------------------- |
| 1        | Formatting  | `uv run ruff format .`                             |
| 2        | Type errors | Add None checks, type narrowing, verify signatures |
| 3        | Linting     | `uv run ruff check . --fix`                        |

### Git Commit Standards

| Scenario                    | Command                                         | Purpose               |
| --------------------------- | ----------------------------------------------- | --------------------- |
| Bug fixes from user reports | `git commit --trailer "Reported-by:<name>"`     | Credit user reporting |
| GitHub issue fixes          | `git commit --trailer "Github-Issue:#<number>"` | Link to issue         |
| General commits             | Standard commit message                         | No special trailers   |

**Prohibited:** Any mention of co-authored-by or development tools in commit messages.

Sources: [CONTRIBUTING.md25-66](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CONTRIBUTING.md#L25-L66) [CLAUDE.md28-44](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L28-L44) [CLAUDE.md89-123](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L89-L123)

## Exception Handling Standards

The project enforces specific exception handling patterns to ensure proper error reporting and debugging capabilities.

### Exception Handling Rules

| Rule                | Implementation                                | Example                                |
| ------------------- | --------------------------------------------- | -------------------------------------- |
| Logging             | Use `logger.exception()` not `logger.error()` | `logger.exception("Failed")`           |
| Message format      | Don't include exception in message            | NOT `logger.exception(f"Failed: {e}")` |
| Specific exceptions | Catch specific types where possible           | `except (OSError, PermissionError):`   |
| General exceptions  | Only for top-level handlers                   | `except Exception:` (limited use)      |

### Exception Categories

| Operation Type     | Recommended Exceptions            | Purpose                          |
| ------------------ | --------------------------------- | -------------------------------- |
| File operations    | `(OSError, PermissionError)`      | Handle file system errors        |
| JSON operations    | `json.JSONDecodeError`            | Handle JSON parsing errors       |
| Network operations | `(ConnectionError, TimeoutError)` | Handle network failures          |
| Top-level handlers | `Exception`                       | Prevent crashes in critical code |

Sources: [CLAUDE.md124-135](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md#L124-L135)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Development Environment](#development-environment.md)
- [Development Setup Requirements](#development-setup-requirements.md)
- [Core Requirements](#core-requirements.md)
- [Installation Process](#installation-process.md)
- [Package Management with uv](#package-management-with-uv.md)
- [uv Command Patterns](#uv-command-patterns.md)
- [Code Quality Standards](#code-quality-standards.md)
- [Code Quality Tools Integration](#code-quality-tools-integration.md)
- [Quality Requirements](#quality-requirements.md)
- [Tool Execution Commands](#tool-execution-commands.md)
- [Pre-commit Hooks System](#pre-commit-hooks-system.md)
- [Pre-commit Hook Configuration](#pre-commit-hook-configuration.md)
- [Hook Configuration Details](#hook-configuration-details.md)
- [Pre-commit Execution](#pre-commit-execution.md)
- [Testing Framework](#testing-framework.md)
- [Testing Configuration](#testing-configuration.md)
- [Testing Requirements](#testing-requirements.md)
- [Test Execution Commands](#test-execution-commands.md)
- [Development Workflow](#development-workflow.md)
- [Complete Development Workflow](#complete-development-workflow.md)
- [Error Resolution Priority](#error-resolution-priority.md)
- [Git Commit Standards](#git-commit-standards.md)
- [Exception Handling Standards](#exception-handling-standards.md)
- [Exception Handling Rules](#exception-handling-rules.md)
- [Exception Categories](#exception-categories.md)
