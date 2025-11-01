Settings Management | fastapi/fastapi | DeepWiki

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

# Settings Management

Relevant source files

- [docs/en/docs/advanced/additional-responses.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/additional-responses.md)
- [docs/en/docs/advanced/behind-a-proxy.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/behind-a-proxy.md)
- [docs/en/docs/advanced/custom-response.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/custom-response.md)
- [docs/en/docs/advanced/path-operation-advanced-configuration.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/path-operation-advanced-configuration.md)
- [docs/en/docs/advanced/response-directly.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/response-directly.md)
- [docs/en/docs/advanced/settings.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md)
- [docs/en/docs/deployment/https.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/deployment/https.md)
- [docs/en/docs/release-notes.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/release-notes.md)
- [docs\_src/additional\_responses/tutorial001.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/additional_responses/tutorial001.py)
- [docs\_src/behind\_a\_proxy/tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/behind_a_proxy/tutorial001_01.py)
- [docs\_src/custom\_response/tutorial001b.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial001b.py)
- [docs\_src/custom\_response/tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial009c.py)
- [docs\_src/custom\_response/tutorial010.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs_src/custom_response/tutorial010.py)
- [fastapi/\_\_init\_\_.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/fastapi/__init__.py)
- [tests/test\_tutorial/test\_behind\_a\_proxy/test\_tutorial001\_01.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_behind_a_proxy/test_tutorial001_01.py)
- [tests/test\_tutorial/test\_custom\_response/test\_tutorial009c.py](https://github.com/fastapi/fastapi/blob/3e2dbf91/tests/test_tutorial/test_custom_response/test_tutorial009c.py)

FastAPI's settings management system provides type-safe configuration handling through Pydantic's `BaseSettings` class. The system automatically reads environment variables, validates configuration values, and integrates with FastAPI's dependency injection system for clean application architecture.

This system centers around the `BaseSettings` class from `pydantic-settings`, dependency injection using `Depends()`, and performance optimization through `@lru_cache` decorators.

## BaseSettings Architecture

The settings system is built around `BaseSettings` from `pydantic-settings`, which provides automatic environment variable reading and type validation. Configuration flows from environment variables through `BaseSettings` subclasses to application components via dependency injection.

**BaseSettings Implementation Flow**

```
```

Sources: [docs/en/docs/advanced/settings.md55-90](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L55-L90) [docs/en/docs/advanced/settings.md141-172](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L141-L172)

## BaseSettings Class Implementation

The `BaseSettings` class from `pydantic-settings` provides the core functionality for configuration management. It automatically reads environment variables, performs type conversion, and validates configuration values.

### Settings Class Definition

Settings classes inherit from `BaseSettings` and declare configuration as typed class attributes:

```
```

**Settings Class Structure**

```
```

Sources: [docs/en/docs/advanced/settings.md55-90](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L55-L90) [docs/en/docs/advanced/settings.md218-249](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L218-L249)

### Environment Variable Mapping

`BaseSettings` automatically maps environment variables to class attributes using case-insensitive matching. The system performs type conversion based on the declared type annotations.

| Class Attribute         | Environment Variable | Type Conversion  | Example               |
| ----------------------- | -------------------- | ---------------- | --------------------- |
| `app_name: str`         | `APP_NAME`           | String           | `"FastAPI App"`       |
| `debug: bool`           | `DEBUG`              | Boolean parsing  | `"true"` → `True`     |
| `items_per_user: int`   | `ITEMS_PER_USER`     | Integer parsing  | `"50"` → `50`         |
| `admin_email: EmailStr` | `ADMIN_EMAIL`        | Email validation | `"admin@example.com"` |
| `database_url: str`     | `DATABASE_URL`       | String           | `"postgresql://..."`  |

The mapping follows Python naming conventions (snake\_case) for attributes while accepting standard environment variable naming (UPPER\_CASE).

Sources: [docs/en/docs/advanced/settings.md87-89](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L87-L89)

## Settings Integration Patterns

### Module-Level Settings

The simplest pattern creates a settings instance at module level that can be imported across the application:

```
```

This pattern works for simple applications but creates global state that complicates testing.

Sources: [docs/en/docs/advanced/settings.md124-139](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L124-L139)

### Dependency Injection Pattern

The recommended pattern uses FastAPI's dependency system with `Depends()` to inject settings into path operations. This enables testing through dependency overrides and performance optimization through caching.

**Settings Dependency Implementation**

```
```

This pattern provides clean separation of concerns and supports dependency overrides for testing.

Sources: [docs/en/docs/advanced/settings.md141-182](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L141-L182) [docs/en/docs/advanced/settings.md250-275](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L250-L275)

## Configuration Sources

### Environment Variables

`BaseSettings` automatically reads environment variables as the primary configuration source. All environment variables are initially strings and are converted to declared types through Pydantic's type conversion system.

### .env File Integration

The system supports `.env` files through `python-dotenv` integration, configured via `SettingsConfigDict`:

```
```

**Configuration Source Resolution**

```
```

Configuration follows a strict precedence: environment variables override `.env` file values, which override class defaults.

Sources: [docs/en/docs/advanced/settings.md183-249](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L183-L249)

## Performance Optimization with @lru\_cache

### LRU Cache Implementation

The `@lru_cache` decorator from `functools` prevents repeated `Settings()` instantiation and file system access, providing significant performance benefits for frequently accessed configuration.

```
```

**@lru\_cache Optimization Flow**

```
```

The `@lru_cache` decorator ensures `Settings()` is only called once, eliminating repeated file I/O and object instantiation overhead.

Sources: [docs/en/docs/advanced/settings.md250-339](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L250-L339)

## Testing Patterns

### Dependency Overrides for Testing

The dependency injection pattern enables clean testing through `app.dependency_overrides`, allowing test-specific configuration without modifying global state.

```
```

**Testing Override Pattern**

```
```

This pattern ensures test isolation and enables testing with different configuration scenarios.

Sources: [docs/en/docs/advanced/settings.md173-182](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L173-L182)

## Security Considerations

Settings management often involves sensitive configuration like database credentials, API keys, and secret tokens. The system supports secure practices through:

- Environment variable isolation from code
- `.env` file exclusion from version control
- Type validation preventing configuration errors
- Dependency injection enabling secure testing practices

For specific security implementations, see [Security Components](fastapi/fastapi/2.5-security-components.md) which covers OAuth2, JWT tokens, and authentication configuration patterns.

Sources: [docs/en/docs/advanced/settings.md1-7](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/advanced/settings.md#L1-L7)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Settings Management](#settings-management.md)
- [BaseSettings Architecture](#basesettings-architecture.md)
- [BaseSettings Class Implementation](#basesettings-class-implementation.md)
- [Settings Class Definition](#settings-class-definition.md)
- [Environment Variable Mapping](#environment-variable-mapping.md)
- [Settings Integration Patterns](#settings-integration-patterns.md)
- [Module-Level Settings](#module-level-settings.md)
- [Dependency Injection Pattern](#dependency-injection-pattern.md)
- [Configuration Sources](#configuration-sources.md)
- [Environment Variables](#environment-variables.md)
- [.env File Integration](#env-file-integration.md)
- [Performance Optimization with @lru\_cache](#performance-optimization-with-lru_cache.md)
- [LRU Cache Implementation](#lru-cache-implementation.md)
- [Testing Patterns](#testing-patterns.md)
- [Dependency Overrides for Testing](#dependency-overrides-for-testing.md)
- [Security Considerations](#security-considerations.md)
