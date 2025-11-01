Context & Progress Reporting | modelcontextprotocol/python-sdk | DeepWiki

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

# Context & Progress Reporting

Relevant source files

- [.gitattribute](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.gitattribute)
- [.gitignore](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.gitignore)
- [src/mcp/server/auth/handlers/authorize.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/auth/handlers/authorize.py)
- [src/mcp/server/fastmcp/prompts/manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/prompts/manager.py)
- [src/mcp/server/fastmcp/resources/resource\_manager.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/resources/resource_manager.py)
- [src/mcp/server/fastmcp/utilities/context\_injection.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/fastmcp/utilities/context_injection.py)
- [src/mcp/server/models.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/models.py)
- [src/mcp/server/session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/server/session.py)
- [tests/server/test\_session.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/server/test_session.py)

This document covers the MCP SDK's context and progress reporting systems, which enable request-scoped data access and bidirectional progress communication between clients and servers. These systems provide the foundation for tracking long-running operations and maintaining request state throughout the MCP protocol lifecycle.

For information about session management and message correlation, see [Session Management](modelcontextprotocol/python-sdk/4.2-session-management.md). For details about protocol message types, see [Protocol Types & JSON-RPC](modelcontextprotocol/python-sdk/4.1-protocol-types-and-json-rpc.md).

## Request Context System

The request context system provides a structured way to access request-scoped information including session references, metadata, and lifecycle context. The `RequestContext` class serves as the primary interface for accessing this information within request handlers.

### RequestContext Architecture

```
```

The `RequestContext` provides access to:

- **request\_id**: Unique identifier for the current request
- **session**: Reference to the active session for sending notifications
- **meta**: Request metadata including progress tokens
- **lifespan\_context**: Application lifecycle context

Sources: [tests/shared/test\_progress\_notifications.py276-281](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L276-L281)

## Progress Notification System

Progress notifications enable both clients and servers to report the status of long-running operations. The system uses progress tokens to correlate notifications with specific requests and supports both absolute and incremental progress reporting.

### Progress Notification Types

| Component              | Description                                | Usage                            |
| ---------------------- | ------------------------------------------ | -------------------------------- |
| `ProgressNotification` | Protocol message type for progress updates | Sent over transport              |
| `progressToken`        | String or int identifier                   | Correlates progress with request |
| `progress`             | Float value                                | Current progress amount          |
| `total`                | Optional float                             | Total expected progress          |
| `message`              | Optional string                            | Human-readable status            |

### Bidirectional Progress Flow

```
```

Both clients and servers can send progress notifications using the `send_progress_notification()` method available on their respective session classes. Progress tokens passed in request metadata enable correlation between requests and their associated progress updates.

Sources: [tests/shared/test\_progress\_notifications.py98-119](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L98-L119) [tests/shared/test\_progress\_notifications.py168-187](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L168-L187)

## Progress Context Manager

The SDK provides a convenient context manager for sending progress notifications that automatically handles progress token extraction and incremental progress tracking.

### Progress Manager Usage

```
```

The progress context manager:

- Extracts progress tokens from request context automatically
- Maintains running total of incremental progress updates
- Provides simple `progress(amount, message)` interface
- Handles session communication transparently

Sources: [tests/shared/test\_progress\_notifications.py287-292](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L287-L292)

## Session Integration

Progress reporting is deeply integrated with the session layer, where both `ClientSession` and `ServerSession` provide `send_progress_notification()` methods for sending progress updates.

### Session Progress Methods

```
```

### Progress Handler Registration

Servers register progress notification handlers using decorators:

```
```

Clients handle progress notifications through message handlers that receive `ProgressNotification` messages and extract the relevant progress information.

Sources: [tests/shared/test\_progress\_notifications.py57-71](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L57-L71) [tests/shared/test\_progress\_notifications.py128-144](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L128-L144)

## Request Metadata Integration

Progress tokens are typically passed as part of request metadata using the `_meta` field in request parameters. This enables correlation between tool calls, resource reads, or other operations and their associated progress updates.

### Metadata Structure

```
```

The metadata integration enables:

- Automatic progress token propagation from requests to handlers
- Correlation of progress updates with specific operations
- Support for multiple concurrent operations with distinct progress tokens

Sources: [tests/shared/test\_progress\_notifications.py89-96](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L89-L96) [tests/shared/test\_progress\_notifications.py275-281](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_progress_notifications.py#L275-L281)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Context & Progress Reporting](#context-progress-reporting.md)
- [Request Context System](#request-context-system.md)
- [RequestContext Architecture](#requestcontext-architecture.md)
- [Progress Notification System](#progress-notification-system.md)
- [Progress Notification Types](#progress-notification-types.md)
- [Bidirectional Progress Flow](#bidirectional-progress-flow.md)
- [Progress Context Manager](#progress-context-manager.md)
- [Progress Manager Usage](#progress-manager-usage.md)
- [Session Integration](#session-integration.md)
- [Session Progress Methods](#session-progress-methods.md)
- [Progress Handler Registration](#progress-handler-registration.md)
- [Request Metadata Integration](#request-metadata-integration.md)
- [Metadata Structure](#metadata-structure.md)
