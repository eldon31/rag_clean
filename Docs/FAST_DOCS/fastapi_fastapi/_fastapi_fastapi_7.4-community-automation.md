Community Automation | fastapi/fastapi | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[fastapi/fastapi](https://github.com/fastapi/fastapi "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 5 September 2025 ([3e2dbf](https://github.com/fastapi/fastapi/commits/3e2dbf91))

- [FastAPI Overview](fastapi/fastapi/1-fastapi-overview.md)
- [Core Architecture](fastapi/fastapi/2-core-architecture.md)
- [Application and Routing System](fastapi/fastapi/2.1-application-and-routing-system.md)
- [Dependency Injection](fastapi/fastapi/2.2-dependency-injection.md)
- [Parameter Validation and Handling](fastapi/fastapi/2.3-parameter-validation-and-handling.md)
- [Response Handling](fastapi/fastapi/2.4-response-handling.md)
- [Security Components](fastapi/fastapi/2.5-security-components.md)
- [Settings Management](fastapi/fastapi/2.6-settings-management.md)
- [Error Handling](fastapi/fastapi/2.7-error-handling.md)
- [API Documentation System](fastapi/fastapi/3-api-documentation-system.md)
- [OpenAPI Schema Generation](fastapi/fastapi/3.1-openapi-schema-generation.md)
- [Customizing API Documentation UI](fastapi/fastapi/3.2-customizing-api-documentation-ui.md)
- [Advanced Features](fastapi/fastapi/4-advanced-features.md)
- [Asynchronous Support](fastapi/fastapi/4.1-asynchronous-support.md)
- [Database Integration](fastapi/fastapi/4.2-database-integration.md)
- [Background Tasks](fastapi/fastapi/4.3-background-tasks.md)
- [Deployment and Production Considerations](fastapi/fastapi/4.4-deployment-and-production-considerations.md)
- [Testing Infrastructure](fastapi/fastapi/5-testing-infrastructure.md)
- [Test Framework and Tools](fastapi/fastapi/5.1-test-framework-and-tools.md)
- [Code Quality and Pre-commit](fastapi/fastapi/5.2-code-quality-and-pre-commit.md)
- [Project Infrastructure](fastapi/fastapi/6-project-infrastructure.md)
- [Documentation System](fastapi/fastapi/6.1-documentation-system.md)
- [CI/CD Pipeline](fastapi/fastapi/6.2-cicd-pipeline.md)
- [Development Workflow](fastapi/fastapi/6.3-development-workflow.md)
- [Community Ecosystem](fastapi/fastapi/7-community-ecosystem.md)
- [Contributors and Experts Management](fastapi/fastapi/7.1-contributors-and-experts-management.md)
- [Translation Management](fastapi/fastapi/7.2-translation-management.md)
- [External Resources and Sponsorship](fastapi/fastapi/7.3-external-resources-and-sponsorship.md)
- [Community Automation](fastapi/fastapi/7.4-community-automation.md)

Menu

# Community Automation

Relevant source files

- [.github/workflows/build-docs.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml)
- [.github/workflows/contributors.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/contributors.yml)
- [.github/workflows/deploy-docs.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/deploy-docs.yml)
- [.github/workflows/issue-manager.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/issue-manager.yml)
- [.github/workflows/label-approved.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/label-approved.yml)
- [.github/workflows/latest-changes.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/latest-changes.yml)
- [.github/workflows/notify-translations.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/notify-translations.yml)
- [.github/workflows/people.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/people.yml)
- [.github/workflows/publish.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/publish.yml)
- [.github/workflows/smokeshow.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/smokeshow.yml)
- [.github/workflows/sponsors.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/sponsors.yml)
- [.github/workflows/test-redistribute.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test-redistribute.yml)
- [.github/workflows/test.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml)
- [.github/workflows/topic-repos.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/topic-repos.yml)
- [scripts/deploy\_docs\_status.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py)
- [scripts/notify\_translations.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py)
- [scripts/sponsors.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/sponsors.py)

This document covers the automated systems that manage community interactions and notifications within the FastAPI project. These systems handle notifications for documentation deployments, translation reviews, and other community-driven activities through GitHub integrations.

For information about contributor tracking and expert identification, see [Contributors and Experts Management](fastapi/fastapi/7.1-contributors-and-experts-management.md). For details about the translation workflow itself, see [Translation Management](fastapi/fastapi/7.2-translation-management.md).

## Overview

The FastAPI project uses two primary automation scripts to manage community notifications:

| System                                 | Purpose                                            | Trigger                            |
| -------------------------------------- | -------------------------------------------------- | ---------------------------------- |
| Documentation Deployment Notifications | Notify PRs about documentation preview deployments | GitHub Actions workflow completion |
| Translation Community Notifications    | Notify language communities about translation PRs  | PR label changes                   |

## Documentation Deployment Notifications

The `deploy_docs_status` system automatically updates pull requests with documentation preview links and deployment status information when documentation changes are detected.

### Core Functionality

The system operates through the `Settings` class which configures GitHub repository access and deployment parameters:

```
```

### Status Management

The system creates different commit statuses based on deployment state:

- **Pending**: When deployment is in progress [scripts/deploy\_docs\_status.py50-57](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L50-L57)
- **Success (No Changes)**: When no documentation files were modified [scripts/deploy\_docs\_status.py40-48](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L40-L48)
- **Success (Deployed)**: When documentation is successfully deployed [scripts/deploy\_docs\_status.py58-63](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L58-L63)

### Link Generation Process

The system processes documentation files to generate preview links using regex matching:

1. Identifies files matching pattern `docs/([^/]+)/docs/(.*)` [scripts/deploy\_docs\_status.py71-74](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L71-L74)
2. Converts file paths to URL paths by handling `index.md` and `.md` extensions [scripts/deploy\_docs\_status.py76-84](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L76-L84)
3. Generates `LinkData` objects containing preview, previous, and English reference links [scripts/deploy\_docs\_status.py85-91](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L85-L91)

**Sources:** [scripts/deploy\_docs\_status.py1-126](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L1-L126)

## Translation Community Notifications

The `notify_translations` system manages notifications to language-specific discussion threads when translation pull requests are opened, reviewed, or completed.

### System Architecture

```
```

### Label-Based Workflow

The system uses specific GitHub labels to trigger notifications:

| Label             | Purpose                         | Action                        |
| ----------------- | ------------------------------- | ----------------------------- |
| `awaiting-review` | PR needs translation review     | Create notification comment   |
| `lang-all`        | Marks PR as translation-related | Required for processing       |
| `lang-{code}`     | Identifies target language      | Maps to discussion thread     |
| `approved-1`      | Translation is approved         | Update notification to "done" |

### GraphQL Queries and Mutations

The system uses four main GraphQL operations:

1. **Discussion Discovery**: `all_discussions_query` finds translation discussions [scripts/notify\_translations.py21-41](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L21-L41)
2. **Comment Retrieval**: `translation_discussion_query` gets existing comments [scripts/notify\_translations.py43-60](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L43-L60)
3. **Comment Creation**: `add_comment_mutation` creates new notifications [scripts/notify\_translations.py62-72](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L62-L72)
4. **Comment Updates**: `update_comment_mutation` marks translations as complete [scripts/notify\_translations.py74-84](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L74-L84)

### Message Templates

The system uses two message templates:

- **New Translation**: `new_translation_message` announces new PRs requiring review [scripts/notify\_translations.py361](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L361-L361)
- **Completed Translation**: `done_translation_message` marks translations as finished [scripts/notify\_translations.py362](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L362-L362)

### Race Condition Prevention

To avoid multiple simultaneous notifications, the system includes a randomized delay:

```
```

This prevents race conditions when multiple labels are applied simultaneously [scripts/notify\_translations.py329-334](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L329-L334)

**Sources:** [scripts/notify\_translations.py1-433](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L1-L433)

## Integration with GitHub Actions

Both automation systems integrate with GitHub Actions workflows through environment variables and event data:

### Common Configuration Pattern

Both scripts use `BaseSettings` from Pydantic for configuration management:

- `github_repository`: Target repository identifier
- `github_token`: Authentication token for API access
- Event-specific parameters (commit SHA, PR number, etc.)

### Event Processing

The `notify_translations` system processes GitHub webhook events:

1. Reads event data from `github_event_path` [scripts/notify\_translations.py315-320](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L315-L320)
2. Extracts PR number from event or settings [scripts/notify\_translations.py322-326](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L322-L326)
3. Processes PR labels to determine language scope [scripts/notify\_translations.py336-347](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L336-L347)

### Error Handling and Logging

Both systems implement comprehensive error handling:

- HTTP response validation [scripts/notify\_translations.py224-229](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L224-L229)
- GraphQL error checking [scripts/notify\_translations.py231-236](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L231-L236)
- Missing resource handling [scripts/deploy\_docs\_status.py34-36](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L34-L36)

**Sources:** [scripts/deploy\_docs\_status.py9-16](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py#L9-L16) [scripts/notify\_translations.py178-188](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L178-L188)

## Community Discussion Integration

The translation notification system specifically targets the "Questions: Translations" discussion category using the category ID `DIC_kwDOCZduT84CT5P9` [scripts/notify\_translations.py19](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L19-L19) This integration enables:

- Automatic discovery of language-specific discussion threads
- Targeted notifications to relevant community members
- Persistent comment tracking to avoid duplicate notifications
- Status updates when translations are completed

The system maintains a mapping between language codes and discussion threads, allowing precise targeting of notifications to the appropriate community groups [scripts/notify\_translations.py350-358](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L350-L358)

**Sources:** [scripts/notify\_translations.py18-20](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L18-L20) [scripts/notify\_translations.py349-373](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L349-L373)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Community Automation](#community-automation.md)
- [Overview](#overview.md)
- [Documentation Deployment Notifications](#documentation-deployment-notifications.md)
- [Core Functionality](#core-functionality.md)
- [Status Management](#status-management.md)
- [Link Generation Process](#link-generation-process.md)
- [Translation Community Notifications](#translation-community-notifications.md)
- [System Architecture](#system-architecture.md)
- [Label-Based Workflow](#label-based-workflow.md)
- [GraphQL Queries and Mutations](#graphql-queries-and-mutations.md)
- [Message Templates](#message-templates.md)
- [Race Condition Prevention](#race-condition-prevention.md)
- [Integration with GitHub Actions](#integration-with-github-actions.md)
- [Common Configuration Pattern](#common-configuration-pattern.md)
- [Event Processing](#event-processing.md)
- [Error Handling and Logging](#error-handling-and-logging.md)
- [Community Discussion Integration](#community-discussion-integration.md)
