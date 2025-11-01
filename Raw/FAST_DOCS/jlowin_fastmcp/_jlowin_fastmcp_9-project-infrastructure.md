Project Infrastructure | jlowin/fastmcp | DeepWiki

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

# Project Infrastructure

Relevant source files

- [.github/workflows/auto-close-duplicates.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/auto-close-duplicates.yml)
- [.github/workflows/marvin-dedupe-issues.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin-dedupe-issues.yml)
- [.github/workflows/marvin-label-triage.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin-label-triage.yml)
- [.github/workflows/marvin.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin.yml)
- [.github/workflows/publish.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/publish.yml)
- [.github/workflows/update-config-schema.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-config-schema.yml)
- [.github/workflows/update-sdk-docs.yml](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-sdk-docs.yml)
- [scripts/auto\_close\_duplicates.py](https://github.com/jlowin/fastmcp/blob/66221ed3/scripts/auto_close_duplicates.py)

This document covers the automated infrastructure and workflows that maintain the FastMCP project, including AI-driven automation, documentation generation, issue management, and CI/CD pipelines. The infrastructure is primarily built around GitHub Actions workflows and integrates with external AI services for intelligent project maintenance.

For information about testing infrastructure and development workflows, see [Testing and Development Framework](jlowin/fastmcp/8-testing-and-development-framework.md).

## AI-Driven Automation System

The core of FastMCP's infrastructure is the Marvin Context Protocol system, which provides AI-powered assistance for project maintenance, issue triage, and development tasks.

### Marvin Context Protocol Workflow

```
```

The main Marvin workflow is defined in [.github/workflows/marvin.yml1-72](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin.yml#L1-L72) and triggers on various GitHub events when the `/marvin` phrase is detected. The workflow uses the `anthropics/claude-code-action@beta` action with extensive tool permissions for code analysis and repository interaction.

**Sources:** [.github/workflows/marvin.yml1-72](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin.yml#L1-L72)

### Issue Triage Automation

```
```

The triage system is implemented in [.github/workflows/marvin-label-triage.yml1-158](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin-label-triage.yml#L1-L158) and uses sophisticated rules to categorize issues and PRs automatically. The system enforces mutually exclusive core categories and applies area labels only when thematically central.

**Sources:** [.github/workflows/marvin-label-triage.yml1-158](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin-label-triage.yml#L1-L158)

## Documentation Automation

### SDK Documentation Pipeline

```
```

The SDK documentation workflow [.github/workflows/update-sdk-docs.yml1-75](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-sdk-docs.yml#L1-L75) automatically generates API reference documentation from source code docstrings and type annotations using the `just api-ref-all` command.

**Sources:** [.github/workflows/update-sdk-docs.yml1-75](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-sdk-docs.yml#L1-L75)

### Configuration Schema Updates

The schema update workflow [.github/workflows/update-config-schema.yml1-92](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-config-schema.yml#L1-L92) maintains the `fastmcp.json` configuration schema by generating it from the `MCPServerConfig` class definition:

```
```

**Sources:** [.github/workflows/update-config-schema.yml1-92](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-config-schema.yml#L1-L92)

## Issue Management Automation

### Duplicate Detection System

```
```

The duplicate detection system [.github/workflows/marvin-dedupe-issues.yml1-81](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin-dedupe-issues.yml#L1-L81) uses a multi-agent approach with the Task tool to coordinate parallel searches and intelligent filtering.

**Sources:** [.github/workflows/marvin-dedupe-issues.yml1-81](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/marvin-dedupe-issues.yml#L1-L81)

### Auto-Close Implementation

The auto-close mechanism is implemented in [scripts/auto\_close\_duplicates.py1-332](https://github.com/jlowin/fastmcp/blob/66221ed3/scripts/auto_close_duplicates.py#L1-L332) with the following key components:

| Component         | Class          | Purpose                      |
| ----------------- | -------------- | ---------------------------- |
| Issue Management  | `Issue`        | Represents GitHub issue data |
| Comment Handling  | `Comment`      | Manages issue comments       |
| Reaction Tracking | `Reaction`     | Tracks user reactions        |
| API Client        | `GitHubClient` | GitHub API interaction       |

The script implements sophisticated logic in `should_close_as_duplicate()` [scripts/auto\_close\_duplicates.py216-254](https://github.com/jlowin/fastmcp/blob/66221ed3/scripts/auto_close_duplicates.py#L216-L254) to check for preventing conditions before auto-closing issues.

**Sources:** [scripts/auto\_close\_duplicates.py1-332](https://github.com/jlowin/fastmcp/blob/66221ed3/scripts/auto_close_duplicates.py#L1-L332) [.github/workflows/auto-close-duplicates.yml1-29](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/auto-close-duplicates.yml#L1-L29)

## CI/CD Pipeline

### Publishing Workflow

```
```

The publishing workflow [.github/workflows/publish.yml1-27](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/publish.yml#L1-L27) uses PyPI's trusted publishing feature for secure package deployment without managing API tokens.

**Sources:** [.github/workflows/publish.yml1-27](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/publish.yml#L1-L27)

## Infrastructure Components

### GitHub App Integration

The Marvin Context Protocol system relies on a GitHub App for authentication:

- **App ID**: Stored as `MARVIN_APP_ID` secret
- **Private Key**: Stored as `MARVIN_APP_PRIVATE_KEY` secret
- **Token Generation**: Uses `actions/create-github-app-token@v2`
- **Permissions**: Comprehensive access to contents, issues, pull-requests, discussions, and actions

### External Service Dependencies

| Service                | Purpose                                 | Authentication            |
| ---------------------- | --------------------------------------- | ------------------------- |
| Anthropic Claude       | AI-powered code analysis and automation | `ANTHROPIC_API_KEY`       |
| GitHub Docker Registry | MCP server containers                   | App token                 |
| PyPI                   | Package publishing                      | Trusted publishing (OIDC) |

### Automation Bot Identity

All automated actions use the bot identity:

- **Name**: `marvin-context-protocol[bot]`
- **Email**: `225465937+marvin-context-protocol[bot]@users.noreply.github.com`
- **User ID**: `225465937`

This ensures consistent attribution for automated contributions and proper GitHub integration.

**Sources:** [.github/workflows/update-sdk-docs.yml68-69](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-sdk-docs.yml#L68-L69) [.github/workflows/update-config-schema.yml85-86](https://github.com/jlowin/fastmcp/blob/66221ed3/.github/workflows/update-config-schema.yml#L85-L86)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Project Infrastructure](#project-infrastructure.md)
- [AI-Driven Automation System](#ai-driven-automation-system.md)
- [Marvin Context Protocol Workflow](#marvin-context-protocol-workflow.md)
- [Issue Triage Automation](#issue-triage-automation.md)
- [Documentation Automation](#documentation-automation.md)
- [SDK Documentation Pipeline](#sdk-documentation-pipeline.md)
- [Configuration Schema Updates](#configuration-schema-updates.md)
- [Issue Management Automation](#issue-management-automation.md)
- [Duplicate Detection System](#duplicate-detection-system.md)
- [Auto-Close Implementation](#auto-close-implementation.md)
- [CI/CD Pipeline](#cicd-pipeline.md)
- [Publishing Workflow](#publishing-workflow.md)
- [Infrastructure Components](#infrastructure-components.md)
- [GitHub App Integration](#github-app-integration.md)
- [External Service Dependencies](#external-service-dependencies.md)
- [Automation Bot Identity](#automation-bot-identity.md)
