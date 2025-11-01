Database Integration | fastapi/fastapi | DeepWiki

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

# Database Integration

Relevant source files

- [docs/en/docs/tutorial/background-tasks.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/background-tasks.md)
- [docs/en/docs/tutorial/extra-data-types.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/extra-data-types.md)
- [docs/en/docs/tutorial/handling-errors.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md)
- [docs/en/docs/tutorial/security/first-steps.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/first-steps.md)
- [docs/en/docs/tutorial/security/oauth2-jwt.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/oauth2-jwt.md)
- [docs/en/docs/tutorial/security/simple-oauth2.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/security/simple-oauth2.md)
- [docs/en/docs/tutorial/sql-databases.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md)
- [docs/ja/docs/tutorial/security/oauth2-jwt.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/ja/docs/tutorial/security/oauth2-jwt.md)
- [docs/pt/docs/tutorial/cookie-param-models.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/pt/docs/tutorial/cookie-param-models.md)
- [docs/zh/docs/tutorial/sql-databases.md](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/zh/docs/tutorial/sql-databases.md)

This document covers FastAPI's database integration capabilities, focusing primarily on SQLModel as the recommended approach for SQL database integration. It includes session management, model patterns, CRUD operations, and security considerations for database-backed applications.

For background task integration with databases, see [Background Tasks](fastapi/fastapi/4.3-background-tasks.md). For general error handling patterns including database errors, see [Error Handling](fastapi/fastapi/2.7-error-handling.md).

## Overview

FastAPI provides flexible database integration through SQLModel, which combines SQLAlchemy's database capabilities with Pydantic's validation features. The integration supports both simple single-model approaches and sophisticated multi-model patterns for production applications.

## Database Integration Architecture

```
```

**Database Integration Flow in FastAPI**

This architecture shows how FastAPI integrates with databases through SQLModel, which serves as an abstraction layer over SQLAlchemy while providing Pydantic validation capabilities.

Sources: [docs/en/docs/tutorial/sql-databases.md1-358](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L1-L358)

## SQLModel Foundation

SQLModel serves as the primary database integration tool, combining SQLAlchemy's ORM capabilities with Pydantic's data validation. The framework distinguishes between table models and data models.

### Model Types

```
```

**SQLModel Model Hierarchy**

Table models represent actual database tables with `table=True`, while data models handle API serialization and validation without direct database mapping.

Sources: [docs/en/docs/tutorial/sql-databases.md182-187](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L182-L187)

## Engine and Session Management

### Engine Configuration

The database engine manages connections to the database. FastAPI applications typically create a single engine instance shared across the application.

```
```

**Engine and Session Creation Flow**

The engine configuration includes thread safety settings for SQLite and connection pooling for production databases.

Sources: [docs/en/docs/tutorial/sql-databases.md74-84](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L74-L84)

### Session Dependency Pattern

FastAPI uses dependency injection to provide database sessions to path operations:

```
```

**Session Dependency Lifecycle**

Each request receives its own session instance through the dependency injection system, ensuring proper transaction isolation.

Sources: [docs/en/docs/tutorial/sql-databases.md92-100](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L92-L100)

## Model Patterns

### Single Model Approach

The simplest pattern uses one model class for both database representation and API serialization:

- Direct model usage in path operations
- Simple CRUD operations
- Minimal security separation

Sources: [docs/en/docs/tutorial/sql-databases.md48-167](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L48-L167)

### Multiple Model Approach

Production applications typically use separate models for different purposes:

```
```

**Multi-Model Pattern Structure**

This pattern provides security by controlling which fields are exposed in different contexts while avoiding code duplication through inheritance.

Sources: [docs/en/docs/tutorial/sql-databases.md180-283](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L180-L283)

## CRUD Operations

### Create Operations

Create operations receive data models and convert them to table models:

```
```

**Create Operation Flow**

The create flow demonstrates the conversion from input data model to table model and back to response data model.

Sources: [docs/en/docs/tutorial/sql-databases.md281-291](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L281-L291)

### Read Operations

Read operations use SQLModel's `select()` function with session execution:

- List operations with pagination support
- Single item retrieval by ID
- Automatic conversion to response models

Sources: [docs/en/docs/tutorial/sql-databases.md130-140](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L130-L140) [docs/en/docs/tutorial/sql-databases.md303-316](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L303-L316)

### Update Operations

Update operations use partial data models with `exclude_unset=True`:

```
```

**Update Operation Pattern**

The update pattern ensures only explicitly provided fields are modified, avoiding accidental overwrites of unspecified fields.

Sources: [docs/en/docs/tutorial/sql-databases.md315-326](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L315-L326)

### Delete Operations

Delete operations retrieve the entity, verify existence, and remove it from the session:

Sources: [docs/en/docs/tutorial/sql-databases.md325-334](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L325-L334)

## Security Considerations

### Field Exposure Control

The multiple model pattern provides security by controlling field visibility:

- `secret_name` fields excluded from public responses
- `id` fields prevented from client input during creation
- Response models ensure consistent data contracts

Sources: [docs/en/docs/tutorial/sql-databases.md168-180](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L168-L180)

### Database Initialization

Table creation typically occurs during application startup rather than on-demand:

```
```

**Database Initialization Patterns**

Development uses automatic table creation while production relies on migration scripts for controlled schema changes.

Sources: [docs/en/docs/tutorial/sql-databases.md102-116](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L102-L116)

## Error Handling Integration

Database operations integrate with FastAPI's error handling through `HTTPException`:

- 404 errors for missing entities
- Validation errors for invalid data
- Database constraint violations

For comprehensive error handling patterns, see [Error Handling](fastapi/fastapi/2.7-error-handling.md).

Sources: [docs/en/docs/tutorial/handling-errors.md22-43](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/handling-errors.md#L22-L43)

## Production Considerations

### Database Selection

SQLModel supports multiple database backends through SQLAlchemy:

- SQLite for development and simple deployments
- PostgreSQL for production applications
- MySQL, Oracle, SQL Server for enterprise environments

Sources: [docs/en/docs/tutorial/sql-databases.md15-26](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L15-L26)

### Migration Management

Production deployments require proper migration handling:

- Alembic integration for schema changes
- Version control for database schemas
- Automated deployment pipelines

Sources: [docs/en/docs/tutorial/sql-databases.md110-116](https://github.com/fastapi/fastapi/blob/3e2dbf91/docs/en/docs/tutorial/sql-databases.md#L110-L116)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Database Integration](#database-integration.md)
- [Overview](#overview.md)
- [Database Integration Architecture](#database-integration-architecture.md)
- [SQLModel Foundation](#sqlmodel-foundation.md)
- [Model Types](#model-types.md)
- [Engine and Session Management](#engine-and-session-management.md)
- [Engine Configuration](#engine-configuration.md)
- [Session Dependency Pattern](#session-dependency-pattern.md)
- [Model Patterns](#model-patterns.md)
- [Single Model Approach](#single-model-approach.md)
- [Multiple Model Approach](#multiple-model-approach.md)
- [CRUD Operations](#crud-operations.md)
- [Create Operations](#create-operations.md)
- [Read Operations](#read-operations.md)
- [Update Operations](#update-operations.md)
- [Delete Operations](#delete-operations.md)
- [Security Considerations](#security-considerations.md)
- [Field Exposure Control](#field-exposure-control.md)
- [Database Initialization](#database-initialization.md)
- [Error Handling Integration](#error-handling-integration.md)
- [Production Considerations](#production-considerations.md)
- [Database Selection](#database-selection.md)
- [Migration Management](#migration-management.md)
