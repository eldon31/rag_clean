Translation Management | fastapi/fastapi | DeepWiki

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

# Translation Management

Relevant source files

- [.github/workflows/translate.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/translate.yml)
- [docs/es/llm-prompt.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/es/llm-prompt.md)
- [docs\_src/configure\_swagger\_ui/tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/configure_swagger_ui/tutorial002.py)
- [requirements-translations.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-translations.txt)
- [scripts/deploy\_docs\_status.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/deploy_docs_status.py)
- [scripts/notify\_translations.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py)
- [scripts/translate.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py)
- [tests/test\_enforce\_once\_required\_parameter.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_enforce_once_required_parameter.py)
- [tests/test\_generic\_parameterless\_depends.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_generic_parameterless_depends.py)
- [tests/test\_repeated\_dependency\_schema.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_repeated_dependency_schema.py)
- [tests/test\_tutorial/test\_configure\_swagger\_ui/test\_tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_configure_swagger_ui/test_tutorial001.py)
- [tests/test\_tutorial/test\_configure\_swagger\_ui/test\_tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_configure_swagger_ui/test_tutorial002.py)
- [tests/test\_tutorial/test\_configure\_swagger\_ui/test\_tutorial003.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_configure_swagger_ui/test_tutorial003.py)

This document covers FastAPI's AI-powered translation workflow, which automatically translates documentation into multiple languages and coordinates community review through GitHub Discussions and automated workflows.

For information about the broader documentation system architecture, see [Documentation System](fastapi/fastapi/6.1-documentation-system.md). For community management aspects, see [Contributors and Experts Management](fastapi/fastapi/7.1-contributors-and-experts-management.md).

## Overview

FastAPI maintains documentation in 11+ languages through an automated translation system that combines AI-powered translation with community review processes. The system uses OpenAI's GPT-4o model to translate English documentation, manages file synchronization across languages, and coordinates review workflows through GitHub Discussions.

## Core Translation Engine

### AI Translation Agent

The translation system centers around the `Agent` class from pydantic-ai, configured with OpenAI's GPT-4o model. The `translate_page()` function in [scripts/translate.py97-158](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L97-L158) handles individual page translation with sophisticated prompt engineering.

```
```

**Translation Pipeline Architecture**

The system uses a multi-layered prompting approach. The `general_prompt` variable [scripts/translate.py26-66](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L26-L66) provides base translation instructions, while language-specific prompts from `docs/{lang}/llm-prompt.md` files add terminology guidelines and style preferences.

Sources: [scripts/translate.py122-157](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L122-L157) [scripts/translate.py26-66](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L26-L66)

### File Organization and Path Mapping

The translation system maintains a structured file organization where English documentation in `docs/en/docs/` maps to translated versions in `docs/{lang}/docs/`. Two key functions handle this mapping:

| Function               | Purpose                   | Input                                  | Output                                 |
| ---------------------- | ------------------------- | -------------------------------------- | -------------------------------------- |
| `generate_lang_path()` | English → Translated path | `docs/en/docs/tutorial/first-steps.md` | `docs/es/docs/tutorial/first-steps.md` |
| `generate_en_path()`   | Translated → English path | `docs/es/docs/tutorial/first-steps.md` | `docs/en/docs/tutorial/first-steps.md` |

The `non_translated_sections` tuple [scripts/translate.py14-23](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L14-L23) excludes specific content types like API reference, release notes, and management documentation from automatic translation.

Sources: [scripts/translate.py76-94](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L76-L94) [scripts/translate.py14-23](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L14-L23)

### Translation Commands and Workflows

The CLI interface provides multiple translation commands through the `typer` app:

```
```

**Translation Command Architecture**

The `list_outdated()` function [scripts/translate.py276-295](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L276-L295) uses Git commit timestamps to identify translations that need updates when English source files have been modified more recently than their translated counterparts.

Sources: [scripts/translate.py192-324](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L192-L324) [scripts/translate.py276-295](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L276-L295)

## GitHub Actions Integration

### Automated Translation Workflow

The GitHub Actions workflow `.github/workflows/translate.yml` provides a manual dispatch interface for running translation operations with different commands and target languages.

```
```

**GitHub Actions Translation Workflow**

The workflow supports command options including `translate-page`, `translate-lang`, `update-outdated`, `add-missing`, `update-and-add`, and `remove-all-removable` [.github/workflows/translate.yml10-19](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/translate.yml#L10-L19)

Sources: [.github/workflows/translate.yml1-78](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/translate.yml#L1-L78)

### Pull Request Creation

The `make_pr()` function [scripts/translate.py328-367](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L328-L367) handles automated PR creation with Git configuration, branch management, and GitHub API integration through the `PyGithub` library.

Sources: [scripts/translate.py328-367](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L328-L367)

## Community Coordination System

### GitHub Discussions Integration

The notification system in `scripts/notify_translations.py` coordinates translation reviews through GitHub Discussions using GraphQL queries to track translation PRs and notify community reviewers.

```
```

**GitHub Discussions Coordination Architecture**

The system uses specific labels for translation workflow management: `awaiting-review`, `lang-all`, and `approved-1` [scripts/notify\_translations.py13-15](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L13-L15) The `questions_translations_category_id` constant [scripts/notify\_translations.py19](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L19-L19) identifies the GitHub Discussions category for translation coordination.

Sources: [scripts/notify\_translations.py13-15](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L13-L15) [scripts/notify\_translations.py21-84](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L21-L84) [scripts/notify\_translations.py349-373](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L349-L373)

### Review Workflow States

The notification system tracks three primary states for translation PRs:

| State                | Trigger                      | Action              | Message Type               |
| -------------------- | ---------------------------- | ------------------- | -------------------------- |
| **Awaiting Review**  | `awaiting-review` label      | Create notification | `new_translation_message`  |
| **Approved/Closed**  | `approved-1` label or closed | Update to done      | `done_translation_message` |
| **Already Notified** | Existing comment             | Skip action         | No change                  |

Sources: [scripts/notify\_translations.py360-427](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L360-L427)

## Language Configuration

### Language-Specific Prompts

Each supported language has a dedicated prompt file at `docs/{lang}/llm-prompt.md` that provides translation guidelines, terminology preferences, and style instructions. The Spanish prompt file [docs/es/llm-prompt.md1-99](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/es/llm-prompt.md#L1-L99) exemplifies this approach with specific translation rules for technical terms.

### Language Registry

The `get_langs()` function [scripts/translate.py72-73](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L72-L73) loads language configurations from `docs/language_names.yml`, providing the mapping between language codes and display names used throughout the translation system.

Sources: [scripts/translate.py72-73](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L72-L73) [docs/es/llm-prompt.md1-99](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/es/llm-prompt.md#L1-L99)

## Quality Control and Diff Minimization

### Incremental Translation Updates

The translation system implements sophisticated diff minimization to preserve existing translations when updating content. When `old_translation` exists [scripts/translate.py128-144](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L128-L144) the system instructs the AI to minimize changes by preserving correct lines and only updating content that reflects changes in the English source.

### Technical Term Preservation

The `general_prompt` includes specific instructions for handling code snippets, technical terms, and markdown formatting [scripts/translate.py27-37](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L27-L37) Code fragments surrounded by backticks remain untranslated, and console/terminal examples preserve their original English content.

Sources: [scripts/translate.py128-144](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L128-L144) [scripts/translate.py27-37](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L27-L37)

## Integration Points

The translation management system integrates with several other FastAPI infrastructure components:

- **Documentation Build System**: Translated files feed into the MkDocs build pipeline covered in [Documentation System](fastapi/fastapi/6.1-documentation-system.md)
- **CI/CD Pipeline**: Translation workflows integrate with the broader automation system described in [CI/CD Pipeline](fastapi/fastapi/6.2-cicd-pipeline.md)
- **Community Management**: Translation coordination connects with contributor recognition systems detailed in [Contributors and Experts Management](fastapi/fastapi/7.1-contributors-and-experts-management.md)

Sources: [scripts/translate.py1-371](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/translate.py#L1-L371) [.github/workflows/translate.yml1-78](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/translate.yml#L1-L78) [scripts/notify\_translations.py1-433](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/notify_translations.py#L1-L433)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Translation Management](#translation-management.md)
- [Overview](#overview.md)
- [Core Translation Engine](#core-translation-engine.md)
- [AI Translation Agent](#ai-translation-agent.md)
- [File Organization and Path Mapping](#file-organization-and-path-mapping.md)
- [Translation Commands and Workflows](#translation-commands-and-workflows.md)
- [GitHub Actions Integration](#github-actions-integration.md)
- [Automated Translation Workflow](#automated-translation-workflow.md)
- [Pull Request Creation](#pull-request-creation.md)
- [Community Coordination System](#community-coordination-system.md)
- [GitHub Discussions Integration](#github-discussions-integration.md)
- [Review Workflow States](#review-workflow-states.md)
- [Language Configuration](#language-configuration.md)
- [Language-Specific Prompts](#language-specific-prompts.md)
- [Language Registry](#language-registry.md)
- [Quality Control and Diff Minimization](#quality-control-and-diff-minimization.md)
- [Incremental Translation Updates](#incremental-translation-updates.md)
- [Technical Term Preservation](#technical-term-preservation.md)
- [Integration Points](#integration-points.md)
