Network Types | pydantic/pydantic | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[pydantic/pydantic](https://github.com/pydantic/pydantic "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 11 October 2025 ([76ef0b](https://github.com/pydantic/pydantic/commits/76ef0b08))

- [Overview](pydantic/pydantic/1-overview.md)
- [Core Model System](pydantic/pydantic/2-core-model-system.md)
- [BaseModel](pydantic/pydantic/2.1-basemodel.md)
- [Field System](pydantic/pydantic/2.2-field-system.md)
- [Model Configuration](pydantic/pydantic/2.3-model-configuration.md)
- [Type System](pydantic/pydantic/3-type-system.md)
- [Constrained Types](pydantic/pydantic/3.1-constrained-types.md)
- [Network Types](pydantic/pydantic/3.2-network-types.md)
- [TypeAdapter](pydantic/pydantic/3.3-typeadapter.md)
- [Generics and Forward References](pydantic/pydantic/3.4-generics-and-forward-references.md)
- [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md)
- [Validators](pydantic/pydantic/4.1-validators.md)
- [Serializers](pydantic/pydantic/4.2-serializers.md)
- [JSON Conversion](pydantic/pydantic/4.3-json-conversion.md)
- [Schema Generation](pydantic/pydantic/5-schema-generation.md)
- [Core Schema Generation](pydantic/pydantic/5.1-core-schema-generation.md)
- [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md)
- [Advanced Features](pydantic/pydantic/6-advanced-features.md)
- [Dataclass Support](pydantic/pydantic/6.1-dataclass-support.md)
- [Function Validation](pydantic/pydantic/6.2-function-validation.md)
- [RootModel and Computed Fields](pydantic/pydantic/6.3-rootmodel-and-computed-fields.md)
- [Plugin System](pydantic/pydantic/6.4-plugin-system.md)
- [Development and Deployment](pydantic/pydantic/7-development-and-deployment.md)
- [Testing Framework](pydantic/pydantic/7.1-testing-framework.md)
- [CI/CD Pipeline](pydantic/pydantic/7.2-cicd-pipeline.md)
- [Documentation System](pydantic/pydantic/7.3-documentation-system.md)
- [Versioning and Dependencies](pydantic/pydantic/7.4-versioning-and-dependencies.md)
- [Migration and Compatibility](pydantic/pydantic/8-migration-and-compatibility.md)
- [V1 to V2 Migration](pydantic/pydantic/8.1-v1-to-v2-migration.md)
- [Backported Modules](pydantic/pydantic/8.2-backported-modules.md)

Menu

# Network Types

Relevant source files

- [pydantic/\_\_init\_\_.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py)
- [pydantic/errors.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/errors.py)
- [pydantic/networks.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py)
- [pydantic/types.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/types.py)
- [pydantic/validators.py](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/validators.py)
- [tests/test\_networks.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py)
- [tests/test\_types.py](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_types.py)

This page documents the network-related types in Pydantic, which provide specialized validation and handling for network data formats such as URLs, email addresses, IP addresses, and database connection strings. These types help ensure that network-related data is properly validated and structured for use in your applications.

## Core Network Types Overview

Pydantic offers several categories of network types that handle different types of network-related data:

```
```

Sources: [pydantic/networks.py1-67](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L1-L67)(showing exported types), [pydantic/\_\_init\_\_.py120-144](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/__init__.py#L120-L144)

## URL Types Architecture

URL types in Pydantic are built on a hierarchical architecture with two base classes: `_BaseUrl` for single-host URLs and `_BaseMultiHostUrl` for URLs that can contain multiple hosts (commonly used in database connection strings).

```
```

Sources: [pydantic/networks.py70-532](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L70-L532)

## Common URL Types

Pydantic provides several specialized URL types for different protocols:

| Type              | Description                            | Constraints                                   |
| ----------------- | -------------------------------------- | --------------------------------------------- |
| `AnyUrl`          | Base type for all URLs                 | Any scheme allowed, TLD and host not required |
| `HttpUrl`         | HTTP/HTTPS URLs                        | Only http/https schemes, max length 2083      |
| `AnyHttpUrl`      | HTTP/HTTPS URLs with fewer constraints | Only http/https schemes                       |
| `FileUrl`         | File URLs                              | Only file scheme                              |
| `FtpUrl`          | FTP URLs                               | Only ftp scheme                               |
| `WebsocketUrl`    | WebSocket URLs                         | Only ws/wss schemes, max length 2083          |
| `AnyWebsocketUrl` | WebSocket URLs with fewer constraints  | Only ws/wss schemes                           |

Sources: [pydantic/networks.py534-688](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L534-L688)

### URL Components and Properties

All URL types provide access to standard URL components:

```
```

Sources: [pydantic/networks.py124-226](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L124-L226) [pydantic/networks.py351-426](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L351-L426)

### Usage Example

```
```

Sources: [tests/test\_networks.py115-119](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L115-L119) [tests/test\_networks.py173-194](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L173-L194)

## Database Connection Strings (DSNs)

Pydantic provides specialized types for validating and handling database connection strings (Data Source Names or DSNs), which are URLs that specify how to connect to a database.

### Supported DSN Types

| Type            | Description                 | Allowed Schemes                                  |
| --------------- | --------------------------- | ------------------------------------------------ |
| `PostgresDsn`   | PostgreSQL connections      | postgres, postgresql, postgresql+asyncpg, etc.   |
| `CockroachDsn`  | CockroachDB connections     | cockroachdb, cockroachdb+psycopg2, etc.          |
| `MySQLDsn`      | MySQL connections           | mysql, mysql+mysqlconnector, mysql+pymysql, etc. |
| `MariaDBDsn`    | MariaDB connections         | mariadb, mariadb+mariadbconnector, etc.          |
| `ClickHouseDsn` | ClickHouse connections      | clickhouse, clickhouse+http, etc.                |
| `SnowflakeDsn`  | Snowflake connections       | snowflake                                        |
| `MongoDsn`      | MongoDB connections         | mongodb                                          |
| `RedisDsn`      | Redis connections           | redis, rediss                                    |
| `AmqpDsn`       | AMQP (RabbitMQ) connections | amqp, amqps                                      |
| `KafkaDsn`      | Kafka connections           | kafka                                            |
| `NatsDsn`       | NATS connections            | nats, tls, ws                                    |

Sources: [pydantic/networks.py690-826](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L690-L826)

### DSN Example

```
```

Sources: [tests/test\_networks.py482-494](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L482-L494) [tests/test\_networks.py700-731](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L700-L731)

### Multi-Host Support

Some DSN types support connecting to multiple hosts, which is useful for database clusters:

```
```

Sources: [pydantic/networks.py389-406](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L389-L406) [tests/test\_networks.py628-647](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L628-L647)

## Email Validation Types

Pydantic provides specialized types for validating email addresses. These types depend on the optional `email_validator` package.

```
```

Sources: [pydantic/networks.py31-39](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L31-L39)

### Email Types Example

```
```

Note: If the `email_validator` package is not installed, an error will be raised when these types are used.

## IP Address Types

Pydantic provides types for validating IP addresses, network interfaces, and networks.

```
```

These types leverage Python's standard `ipaddress` module and provide proper validation during model instantiation.

### IP Address Types Categories

| Type              | Description                           | Example                |
| ----------------- | ------------------------------------- | ---------------------- |
| `IPvAnyAddress`   | Either IPv4 or IPv6 address           | "192.168.1.1" or "::1" |
| `IPvAnyInterface` | IP interface with network information | "192.168.1.1/24"       |
| `IPvAnyNetwork`   | IP network                            | "192.168.0.0/24"       |

Sources: [pydantic/networks.py52-54](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L52-L54)

## Customization with UrlConstraints

The `UrlConstraints` class allows you to customize URL validation with specific constraints.

```
```

### UrlConstraints Parameters

| Parameter         | Description                   | Default |
| ----------------- | ----------------------------- | ------- |
| `max_length`      | Maximum URL length            | `None`  |
| `allowed_schemes` | List of allowed schemes       | `None`  |
| `host_required`   | Whether host is required      | `None`  |
| `default_host`    | Default host if none provided | `None`  |
| `default_port`    | Default port if none provided | `None`  |
| `default_path`    | Default path if none provided | `None`  |

Sources: [pydantic/networks.py70-120](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L70-L120) [tests/test\_networks.py823-841](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L823-L841)

## Implementation Details

### URL Validation Process

URL validation and processing in Pydantic follows these steps:

1. Parse the URL string into components
2. Validate the scheme against allowed schemes
3. Apply length constraints
4. Convert international domain names to punycode
5. Apply default values for missing components
6. Construct a validated URL object with accessible properties

### International Domain Name Support

Pydantic's URL types support internationalized domain names (IDNs) by automatically converting them to punycode:

```
```

Sources: [tests/test\_networks.py330-337](https://github.com/pydantic/pydantic/blob/76ef0b08/tests/test_networks.py#L330-L337)

### Database DSN Customization

Each DSN type comes with pre-configured constraints for its respective database system:

- Allowed schemes specific to the database
- Default ports (e.g., 5432 for PostgreSQL, 6379 for Redis)
- Default hosts (often "localhost")
- Default paths where applicable (e.g., "/0" for Redis databases)

This makes it easier to handle database connection strings with minimal configuration.

Sources: [pydantic/networks.py690-826](https://github.com/pydantic/pydantic/blob/76ef0b08/pydantic/networks.py#L690-L826)

## Best Practices

1. **Choose the most specific type**: Use the most specific URL type for your use case (e.g., `HttpUrl` rather than `AnyUrl` for HTTP endpoints).

2. **Handle connection credentials securely**: For DSNs with credentials, consider using environment variables or secure storage.

3. **Default fallbacks**: Use `UrlConstraints` to provide sensible defaults for missing URL components.

4. **Validation at boundaries**: Validate network inputs at application boundaries to ensure they are properly formed.

5. **Consider the optional dependencies**: Install `email_validator` package when using email validation types.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Network Types](#network-types.md)
- [Core Network Types Overview](#core-network-types-overview.md)
- [URL Types Architecture](#url-types-architecture.md)
- [Common URL Types](#common-url-types.md)
- [URL Components and Properties](#url-components-and-properties.md)
- [Usage Example](#usage-example.md)
- [Database Connection Strings (DSNs)](#database-connection-strings-dsns.md)
- [Supported DSN Types](#supported-dsn-types.md)
- [DSN Example](#dsn-example.md)
- [Multi-Host Support](#multi-host-support.md)
- [Email Validation Types](#email-validation-types.md)
- [Email Types Example](#email-types-example.md)
- [IP Address Types](#ip-address-types.md)
- [IP Address Types Categories](#ip-address-types-categories.md)
- [Customization with UrlConstraints](#customization-with-urlconstraints.md)
- [UrlConstraints Parameters](#urlconstraints-parameters.md)
- [Implementation Details](#implementation-details.md)
- [URL Validation Process](#url-validation-process.md)
- [International Domain Name Support](#international-domain-name-support.md)
- [Database DSN Customization](#database-dsn-customization.md)
- [Best Practices](#best-practices.md)
