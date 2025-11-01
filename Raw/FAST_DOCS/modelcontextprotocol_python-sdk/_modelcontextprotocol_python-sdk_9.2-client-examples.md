Client Examples | modelcontextprotocol/python-sdk | DeepWiki

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

# Client Examples

Relevant source files

- [.pre-commit-config.yaml](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/.pre-commit-config.yaml)
- [CLAUDE.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CLAUDE.md)
- [CODE\_OF\_CONDUCT.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/CONTRIBUTING.md)
- [SECURITY.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/SECURITY.md)
- [examples/clients/simple-auth-client/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-auth-client/README.md)
- [examples/clients/simple-auth-client/mcp\_simple\_auth\_client/main.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-auth-client/mcp_simple_auth_client/main.py)
- [examples/clients/simple-chatbot/README.MD](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/README.MD)
- [examples/servers/simple-auth/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-auth/README.md)
- [examples/servers/simple-auth/mcp\_simple\_auth/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-auth/mcp_simple_auth/server.py)
- [examples/servers/simple-streamablehttp-stateless/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp-stateless/README.md)
- [examples/servers/simple-streamablehttp/README.md](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-streamablehttp/README.md)

This document provides practical examples of MCP client implementations, focusing on real-world usage patterns and architectures. The primary example is the simple-chatbot client that demonstrates comprehensive integration with MCP servers, LLM providers, and user interaction patterns.

For server-side examples, see [Server Examples](modelcontextprotocol/python-sdk/9.1-server-examples.md). For core client framework documentation, see [Client Framework](modelcontextprotocol/python-sdk/3-client-framework.md).

## Simple Chatbot Example Overview

The simple-chatbot example demonstrates a complete MCP client implementation that connects to multiple MCP servers, discovers their tools, and integrates with an LLM provider to create an interactive chatbot experience.

```
```

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py1-409](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L1-L409)

## Client Architecture Components

The simple-chatbot demonstrates four main architectural components that work together to provide a complete MCP client experience.

### Configuration Management

The `Configuration` class handles environment setup and server configuration loading:

```
```

The configuration system supports:

- Environment variable management via `python-dotenv`
- JSON-based server configuration loading
- API key validation and access

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py18-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L18-L61)

### Server Connection Management

The `Server` class manages individual MCP server connections with proper lifecycle management:

```
```

Key features include:

- `AsyncExitStack` for proper resource cleanup
- Retry logic with configurable attempts and delays
- Error handling and recovery mechanisms

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py63-169](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L63-L169)

## Connection and Session Management

The client demonstrates proper MCP session establishment and management patterns:

```
```

The session management includes:

- Process spawning with `shutil.which()` for command resolution
- Stream-based communication setup
- Capability negotiation through `session.initialize()`
- Proper error handling and cleanup on failure

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py74-94](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L74-L94)

## Tool Discovery and Execution

The client implements comprehensive tool management with LLM integration:

### Tool Discovery Pattern

```
```

The discovery process extracts tool metadata and formats it for LLM consumption:

- Tool name and description
- JSON schema for input parameters
- Required vs optional parameter identification
- Human-readable formatting for LLM prompts

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py96-115](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L96-L115) [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py171-213](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L171-L213)

### Tool Execution with Retry Logic

```
```

The execution system provides:

- Configurable retry attempts (default: 2)
- Exponential backoff with configurable delay
- Comprehensive error logging
- Progress reporting for long-running tools

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py117-158](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L117-L158)

## LLM Integration Patterns

The client demonstrates how to integrate MCP tools with LLM providers through structured prompting and tool calling protocols.

### LLM Communication Flow

```
```

### Tool Call Protocol

The client implements a JSON-based tool calling protocol:

```
```

The system message instructs the LLM on tool usage patterns and response formatting, ensuring consistent tool invocation and natural language result processing.

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py283-321](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L283-L321) [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py341-361](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L341-L361)

## Usage Examples

### Basic Client Setup

The simple-chatbot can be configured through a JSON configuration file:

```
```

### Environment Configuration

Required environment variables:

- `LLM_API_KEY`: API key for the LLM provider (Groq in this example)

The client uses `python-dotenv` for environment management, supporting `.env` files for development.

Sources: [examples/clients/simple-chatbot/mcp\_simple\_chatbot/main.py397-404](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py#L397-L404)

### Test Integration Patterns

The codebase includes several test patterns that demonstrate client usage:

#### Resource Testing with Client Sessions

```
```

This pattern is used extensively in tests for validating server behavior from a client perspective.

Sources: [tests/issues/test\_152\_resource\_mime\_type.py36-61](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_152_resource_mime_type.py#L36-L61) [tests/issues/test\_141\_resource\_templates.py81-114](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_141_resource_templates.py#L81-L114)

The examples demonstrate comprehensive MCP client implementation patterns, from basic connection management to advanced tool integration with LLM providers, providing a solid foundation for building sophisticated MCP client applications.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Client Examples](#client-examples.md)
- [Simple Chatbot Example Overview](#simple-chatbot-example-overview.md)
- [Client Architecture Components](#client-architecture-components.md)
- [Configuration Management](#configuration-management.md)
- [Server Connection Management](#server-connection-management.md)
- [Connection and Session Management](#connection-and-session-management.md)
- [Tool Discovery and Execution](#tool-discovery-and-execution.md)
- [Tool Discovery Pattern](#tool-discovery-pattern.md)
- [Tool Execution with Retry Logic](#tool-execution-with-retry-logic.md)
- [LLM Integration Patterns](#llm-integration-patterns.md)
- [LLM Communication Flow](#llm-communication-flow.md)
- [Tool Call Protocol](#tool-call-protocol.md)
- [Usage Examples](#usage-examples.md)
- [Basic Client Setup](#basic-client-setup.md)
- [Environment Configuration](#environment-configuration.md)
- [Test Integration Patterns](#test-integration-patterns.md)
- [Resource Testing with Client Sessions](#resource-testing-with-client-sessions.md)
