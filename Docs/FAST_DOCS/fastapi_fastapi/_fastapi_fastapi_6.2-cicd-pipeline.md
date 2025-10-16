CI/CD Pipeline | fastapi/fastapi | DeepWiki

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

# CI/CD Pipeline

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
- [.gitignore](https://github.com/fastapi/fastapi/blob/3e2dbf91/.gitignore)
- [scripts/sponsors.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/sponsors.py)

This document covers the comprehensive Continuous Integration/Continuous Deployment (CI/CD) infrastructure for the FastAPI repository, including automated testing, documentation building, package publishing, and community management workflows.

The CI/CD system is implemented entirely using GitHub Actions and consists of multiple interconnected workflows that handle code quality assurance, documentation generation, release automation, and community engagement. For information about the development workflow and local tooling, see [Development Workflow](fastapi/fastapi/6.3-development-workflow.md). For details about the documentation build system itself, see [Documentation System](fastapi/fastapi/6.1-documentation-system.md).

## Pipeline Architecture Overview

The FastAPI CI/CD pipeline consists of four main categories of automation: core development workflows, documentation pipelines, release management, and community automation.

```
```

Sources: [.github/workflows/test.yml1-156](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml#L1-L156) [.github/workflows/build-docs.yml1-138](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml#L1-L138) [.github/workflows/deploy-docs.yml1-78](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/deploy-docs.yml#L1-L78) [.github/workflows/publish.yml1-43](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/publish.yml#L1-L43)

## Core Testing and Quality Assurance

The testing pipeline ensures code quality through comprehensive linting, multi-version testing, and coverage reporting.

### Test Workflow

The `test.yml` workflow implements a multi-dimensional test matrix covering Python versions 3.8-3.13 and both Pydantic v1 and v2 compatibility.

```
```

The test workflow uses specific environment variables and configurations:

- `UV_SYSTEM_PYTHON: 1` for system Python usage
- `COVERAGE_FILE` with unique naming per test matrix combination
- Conditional Pydantic version installation based on matrix parameters

Sources: [.github/workflows/test.yml46-101](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml#L46-L101) [.github/workflows/test.yml102-140](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml#L102-L140)

### Coverage Reporting

The coverage system integrates with Smokeshow for visual coverage reporting:

```
```

Sources: [.github/workflows/test.yml89-139](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml#L89-L139) [.github/workflows/smokeshow.yml14-61](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/smokeshow.yml#L14-L61)

## Documentation Build and Deployment Pipeline

The documentation system implements a sophisticated multi-language build and deployment process.

### Documentation Build Workflow

The `build-docs.yml` workflow handles path-based change detection and multi-language documentation building:

```
```

The workflow uses conditional MkDocs Material Insiders installation based on secret availability and supports caching for performance optimization.

Sources: [.github/workflows/build-docs.yml14-138](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml#L14-L138) [.github/workflows/build-docs.yml71-76](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml#L71-L76) [.github/workflows/build-docs.yml112-124](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml#L112-L124)

### Documentation Deployment

The `deploy-docs.yml` workflow handles automatic deployment to Cloudflare Pages:

```
```

Sources: [.github/workflows/deploy-docs.yml19-78](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/deploy-docs.yml#L19-L78) [.github/workflows/deploy-docs.yml58-69](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/deploy-docs.yml#L58-L69)

## Release and Publishing Pipeline

The publishing system handles automated package distribution to PyPI for both `fastapi` and `fastapi-slim` variants.

### Package Publishing

```
```

The publishing workflow uses trusted publishing with OpenID Connect tokens and supports building multiple package variants through the `TIANGOLO_BUILD_PACKAGE` environment variable.

Sources: [.github/workflows/publish.yml8-43](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/publish.yml#L8-L43) [.github/workflows/publish.yml34-38](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/publish.yml#L34-L38)

### Distribution Testing

The `test-redistribute.yml` workflow validates package distributions:

| Test Phase                | Description                | Commands                                 |
| ------------------------- | -------------------------- | ---------------------------------------- |
| Source Distribution Build | Build sdist package        | `python -m build --sdist`                |
| Source Distribution Test  | Test from extracted source | `bash scripts/test.sh` in dist directory |
| Wheel Build               | Build wheel from sdist     | `pip wheel --no-deps fastapi*.tar.gz`    |

Sources: [.github/workflows/test-redistribute.yml13-58](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test-redistribute.yml#L13-L58)

## Community Automation Workflows

The FastAPI repository includes extensive automation for community management, contributor recognition, and content updates.

### Contributor and Sponsor Management

```
```

Sources: [.github/workflows/people.yml3-55](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/people.yml#L3-L55) [.github/workflows/contributors.yml3-54](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/contributors.yml#L3-L54) [.github/workflows/sponsors.yml3-53](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/sponsors.yml#L3-L53) [.github/workflows/topic-repos.yml3-41](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/topic-repos.yml#L3-L41)

### Sponsor Data Processing

The `sponsors.py` script demonstrates the sophisticated data processing pipeline:

```
```

Sources: [scripts/sponsors.py17-45](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/sponsors.py#L17-L45) [scripts/sponsors.py119-144](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/sponsors.py#L119-L144) [scripts/sponsors.py192-217](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/sponsors.py#L192-L217)

### Issue and PR Management

The repository includes automated issue and PR management workflows:

| Workflow                  | Purpose                   | Trigger                    | Key Features                              |
| ------------------------- | ------------------------- | -------------------------- | ----------------------------------------- |
| `issue-manager.yml`       | Auto-close stale issues   | Schedule, labels, comments | Configurable delay, custom messages       |
| `label-approved.yml`      | Label approved PRs        | Daily schedule             | Approval tracking, awaiting-review label  |
| `latest-changes.yml`      | Update changelog          | PR merge, manual           | Automatic release notes generation        |
| `notify-translations.yml` | Translation notifications | PR labels, close           | Discussion creation for translation teams |

Sources: [.github/workflows/issue-manager.yml22-48](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/issue-manager.yml#L22-L48) [.github/workflows/label-approved.yml14-50](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/label-approved.yml#L14-L50) [.github/workflows/latest-changes.yml19-45](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/latest-changes.yml#L19-L45) [.github/workflows/notify-translations.yml21-60](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/notify-translations.yml#L21-L60)

## Pipeline Configuration and Dependencies

The CI/CD system relies on standardized tooling and configuration across all workflows:

### Common Dependencies

| Tool           | Version  | Purpose             | Configuration             |
| -------------- | -------- | ------------------- | ------------------------- |
| `uv`           | 0.4.15   | Package management  | `astral-sh/setup-uv@v6`   |
| Python         | 3.8-3.13 | Runtime environment | `actions/setup-python@v5` |
| GitHub Actions | Latest   | Workflow execution  | Various action versions   |

### Environment Variables and Secrets

```
```

Sources: [.github/workflows/test.yml15-16](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml#L15-L16) [.github/workflows/build-docs.yml11-12](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml#L11-L12) [.github/workflows/publish.yml34-35](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/publish.yml#L34-L35)

### Branch Protection and Status Checks

The pipeline implements comprehensive status checking through "all-green" jobs that aggregate multiple workflow results:

- `docs-all-green` in `build-docs.yml` - Aggregates documentation build status
- `check` in `test.yml` - Aggregates test and coverage results
- `test-redistribute-alls-green` in `test-redistribute.yml` - Aggregates distribution test results

These jobs use the `re-actors/alls-green@release/v1` action to provide unified status reporting for branch protection rules.

Sources: [.github/workflows/build-docs.yml127-137](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/build-docs.yml#L127-L137) [.github/workflows/test.yml142-155](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test.yml#L142-L155) [.github/workflows/test-redistribute.yml60-69](https://github.com/fastapi/fastapi/blob/3e2dbf91/.github/workflows/test-redistribute.yml#L60-L69)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [CI/CD Pipeline](#cicd-pipeline.md)
- [Pipeline Architecture Overview](#pipeline-architecture-overview.md)
- [Core Testing and Quality Assurance](#core-testing-and-quality-assurance.md)
- [Test Workflow](#test-workflow.md)
- [Coverage Reporting](#coverage-reporting.md)
- [Documentation Build and Deployment Pipeline](#documentation-build-and-deployment-pipeline.md)
- [Documentation Build Workflow](#documentation-build-workflow.md)
- [Documentation Deployment](#documentation-deployment.md)
- [Release and Publishing Pipeline](#release-and-publishing-pipeline.md)
- [Package Publishing](#package-publishing.md)
- [Distribution Testing](#distribution-testing.md)
- [Community Automation Workflows](#community-automation-workflows.md)
- [Contributor and Sponsor Management](#contributor-and-sponsor-management.md)
- [Sponsor Data Processing](#sponsor-data-processing.md)
- [Issue and PR Management](#issue-and-pr-management.md)
- [Pipeline Configuration and Dependencies](#pipeline-configuration-and-dependencies.md)
- [Common Dependencies](#common-dependencies.md)
- [Environment Variables and Secrets](#environment-variables-and-secrets.md)
- [Branch Protection and Status Checks](#branch-protection-and-status-checks.md)
