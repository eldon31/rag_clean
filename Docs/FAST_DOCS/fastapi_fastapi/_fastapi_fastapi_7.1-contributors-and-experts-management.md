Contributors and Experts Management | fastapi/fastapi | DeepWiki

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

# Contributors and Experts Management

Relevant source files

- [docs/az/docs/learn/index.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/az/docs/learn/index.md)
- [docs/en/data/contributors.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/contributors.yml)
- [docs/en/data/github\_sponsors.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/github_sponsors.yml)
- [docs/en/data/people.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/people.yml)
- [docs/en/data/skip\_users.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/skip_users.yml)
- [docs/en/data/translation\_reviewers.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/translation_reviewers.yml)
- [docs/en/data/translators.yml](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/translators.yml)
- [docs/en/docs/fastapi-people.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/fastapi-people.md)
- [requirements-docs-tests.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-docs-tests.txt)
- [requirements-github-actions.txt](https://github.com/fastapi/fastapi/blob/3e2dbf91/requirements-github-actions.txt)
- [scripts/contributors.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py)
- [scripts/people.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py)
- [tests/test\_tutorial/test\_custom\_request\_and\_route/test\_tutorial002.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_request_and_route/test_tutorial002.py)

This document covers FastAPI's automated system for recognizing and managing community contributors and experts. The system tracks GitHub Discussions participation, Pull Request contributions, translations, and sponsorship to create community recognition pages.

For information about the translation workflow automation, see [Translation Management](fastapi/fastapi/7.2-translation-management.md). For external sponsorship and community resources, see [External Resources and Sponsorship](fastapi/fastapi/7.3-external-resources-and-sponsorship.md).

## Purpose and Architecture

The Contributors and Experts Management system automatically identifies and recognizes community members across multiple contribution categories:

- **FastAPI Experts**: Users who help answer questions in GitHub Discussions
- **Contributors**: Users who create merged Pull Requests
- **Translators**: Contributors who submit translation Pull Requests
- **Translation Reviewers**: Users who review and approve translations
- **Sponsors**: Financial supporters through GitHub Sponsors

The system operates through automated data collection scripts that query GitHub APIs, process contribution data, and generate YAML files consumed by documentation pages.

## Data Collection Architecture

```
```

**Data Collection and Documentation Flow**

Sources: [scripts/people.py1-316](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L1-L316) [scripts/contributors.py1-316](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py#L1-L316) [docs/en/data/people.yml1-715](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/people.yml#L1-L715) [docs/en/docs/fastapi-people.md1-306](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/fastapi-people.md#L1-L306)

## FastAPI Experts Detection System

The experts detection system analyzes GitHub Discussions to identify users who consistently help answer questions in the FastAPI community.

### Discussion Data Model

```
```

**GitHub Discussions Data Structure**

The system uses specific Pydantic models to parse GitHub GraphQL responses:

| Model                      | Purpose                      | Key Fields                                   |
| -------------------------- | ---------------------------- | -------------------------------------------- |
| `DiscussionsNode`          | Individual discussion thread | `number`, `author`, `createdAt`, `comments`  |
| `DiscussionsCommentsNode`  | Comment within discussion    | `createdAt`, `author`, `replies`             |
| `Author`                   | User information             | `login`, `avatarUrl`, `url`                  |
| `DiscussionExpertsResults` | Aggregated results           | `commenters`, time-based counters, `authors` |

Sources: [scripts/people.py64-177](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L64-L177)

### Expert Identification Algorithm

```
```

**Expert Detection Algorithm Flow**

The algorithm tracks participation over multiple time windows:

- **Last Month**: 30 days ago to now
- **3 Months**: 90 days ago to now
- **6 Months**: 180 days ago to now
- **1 Year**: 365 days ago to now
- **All Time**: Complete history

Key logic in `get_discussions_experts()`:

1. Excludes discussion authors from being counted as helpers for their own discussions
2. Tracks the most recent comment time per user per discussion
3. Increments counters based on time window inclusion
4. Uses `Counter[str]` for efficient counting and ranking

Sources: [scripts/people.py195-255](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L195-L255) [scripts/people.py258-280](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L258-L280)

## Contributors and Translations System

The contributors system analyzes Pull Requests to categorize different types of contributions and identify translation workflow participants.

### Pull Request Analysis Pipeline

```
```

**Pull Request Processing Pipeline**

The system distinguishes contributions by analyzing PR metadata:

| Contribution Type        | Detection Logic                    | Counter                 |
| ------------------------ | ---------------------------------- | ----------------------- |
| **Regular Contributor**  | Merged PR without `lang-all` label | `contributors`          |
| **Translator**           | Merged PR with `lang-all` label    | `translators`           |
| **Translation Reviewer** | Review on PR with `lang-all` label | `translation_reviewers` |

Sources: [scripts/contributors.py175-204](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py#L175-L204)

### Data Output Structure

The processed data generates multiple YAML files with consistent structure:

```
```

**Standardized User Data Structure**

All user data follows the pattern established by the `get_users_to_write()` function, ensuring consistency across different contribution types.

Sources: [scripts/contributors.py207-224](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py#L207-L224) [scripts/people.py282-301](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L282-L301)

## Automated Updates and Git Integration

Both collection scripts include automated Git workflow integration for updating community data.

### Update Workflow

| Step                   | Function             | Purpose                    |
| ---------------------- | -------------------- | -------------------------- |
| **Data Collection**    | `main()`             | Execute GitHub API queries |
| **Content Comparison** | `update_content()`   | Check if data changed      |
| **Git Configuration**  | `subprocess.run()`   | Set up GitHub Actions user |
| **Branch Creation**    | `git checkout -b`    | Create update branch       |
| **Pull Request**       | `repo.create_pull()` | Submit changes for review  |

The system only creates PRs when data has actually changed, using YAML content comparison:

```
```

Sources: [scripts/people.py304-314](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L304-L314) [scripts/contributors.py226-235](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py#L226-L235) [scripts/contributors.py284-311](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py#L284-L311)

## Configuration and Security

### Settings Management

Both scripts use Pydantic Settings for configuration:

| Setting             | Purpose                   | Default    |
| ------------------- | ------------------------- | ---------- |
| `github_token`      | GitHub API authentication | Required   |
| `github_repository` | Target repository         | Required   |
| `httpx_timeout`     | API request timeout       | 30 seconds |
| `sleep_interval`    | Rate limiting delay       | 5 seconds  |

The `sleep_interval` in `people.py` handles GitHub's secondary rate limits for GraphQL queries.

### User Filtering

The system excludes certain automated users via `skip_users.yml`:

- `tiangolo` (project creator, counted separately)
- `codecov`, `github-actions`, `pre-commit-ci`, `dependabot` (bots)

Sources: [scripts/people.py118-123](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/people.py#L118-L123) [scripts/contributors.py115-119](https://github.com/fastapi/fastapi/blob/3e2dbf91/scripts/contributors.py#L115-L119) [docs/en/data/skip\_users.yml1-6](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/data/skip_users.yml#L1-L6)

## Documentation Integration

The community data integrates into documentation through template rendering in `fastapi-people.md`:

### Template Variables

| Variable                    | Source                      | Usage                         |
| --------------------------- | --------------------------- | ----------------------------- |
| `people.experts`            | `people.yml`                | All-time FastAPI experts list |
| `people.last_month_experts` | `people.yml`                | Recent experts                |
| `contributors`              | `contributors.yml`          | Top contributors              |
| `translators`               | `translators.yml`           | Top translators               |
| `translation_reviewers`     | `translation_reviewers.yml` | Top reviewers                 |
| `github_sponsors`           | `github_sponsors.yml`       | Sponsor information           |

The documentation uses Jinja2-style templating to render user lists with avatars, usernames, and contribution counts.

Sources: [docs/en/docs/fastapi-people.md17-293](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/fastapi-people.md#L17-L293)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Contributors and Experts Management](#contributors-and-experts-management.md)
- [Purpose and Architecture](#purpose-and-architecture.md)
- [Data Collection Architecture](#data-collection-architecture.md)
- [FastAPI Experts Detection System](#fastapi-experts-detection-system.md)
- [Discussion Data Model](#discussion-data-model.md)
- [Expert Identification Algorithm](#expert-identification-algorithm.md)
- [Contributors and Translations System](#contributors-and-translations-system.md)
- [Pull Request Analysis Pipeline](#pull-request-analysis-pipeline.md)
- [Data Output Structure](#data-output-structure.md)
- [Automated Updates and Git Integration](#automated-updates-and-git-integration.md)
- [Update Workflow](#update-workflow.md)
- [Configuration and Security](#configuration-and-security.md)
- [Settings Management](#settings-management.md)
- [User Filtering](#user-filtering.md)
- [Documentation Integration](#documentation-integration.md)
- [Template Variables](#template-variables.md)
