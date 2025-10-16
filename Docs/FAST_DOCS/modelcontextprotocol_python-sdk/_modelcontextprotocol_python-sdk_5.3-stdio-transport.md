STDIO Transport | modelcontextprotocol/python-sdk | DeepWiki

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

# STDIO Transport

Relevant source files

- [examples/servers/simple-prompt/mcp\_simple\_prompt/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-prompt/mcp_simple_prompt/server.py)
- [examples/servers/simple-resource/mcp\_simple\_resource/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-resource/mcp_simple_resource/server.py)
- [examples/servers/simple-tool/mcp\_simple\_tool/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/examples/servers/simple-tool/mcp_simple_tool/server.py)
- [src/mcp/client/stdio/\_\_init\_\_.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py)
- [tests/client/test\_stdio.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_stdio.py)
- [tests/issues/test\_1027\_win\_unreachable\_cleanup.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/issues/test_1027_win_unreachable_cleanup.py)
- [tests/shared/test\_win32\_utils.py](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/shared/test_win32_utils.py)

The STDIO Transport enables MCP clients to communicate with servers by spawning processes and using standard input/output streams for message exchange. This transport is particularly useful for local development, CLI tools, and scenarios where servers are distributed as standalone executables. For HTTP-based transports, see [StreamableHTTP Transport](modelcontextprotocol/python-sdk/5.1-streamablehttp-transport.md) and [SSE Transport](modelcontextprotocol/python-sdk/5.2-server-sent-events-\(sse\)-transport.md).

## Configuration

The STDIO transport is configured using the `StdioServerParameters` class, which defines how the server process should be spawned and managed.

### StdioServerParameters

The configuration model provides comprehensive control over process execution:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py72-103](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L72-L103)

The `env` parameter controls environment variable inheritance. When `None`, the system uses `get_default_environment()` which provides a secure subset of environment variables filtered for safety.

### Default Environment Security

The transport implements security measures for environment variable inheritance:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py51-69](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L51-L69) [src/mcp/client/stdio/\_\_init\_\_.py27-45](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L27-L45)

## Connection Management

### stdio\_client Context Manager

The `stdio_client` function provides the primary interface for establishing STDIO connections. It returns read and write streams for JSON-RPC message exchange:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py105-216](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L105-L216)

### Message Processing

The transport handles JSON-RPC message serialization automatically:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py139-179](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L139-L179)

## Process Management

### Cross-Platform Process Creation

The transport provides platform-specific process creation to ensure reliable child process management:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py234-258](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L234-L258) [src/mcp/client/stdio/\_\_init\_\_.py218-232](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L218-L232)

### Process Tree Termination

The transport implements comprehensive child process cleanup using platform-specific mechanisms:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py261-277](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L261-L277)

## Shutdown and Cleanup

### MCP-Compliant Shutdown Sequence

The transport implements the MCP specification's stdio shutdown sequence for graceful server termination:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py190-215](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L190-L215)

### Timeout Configuration

The transport uses configurable timeouts for process termination:

- **`PROCESS_TERMINATION_TIMEOUT`**: 2.0 seconds for graceful exit after stdin closure
- Escalation to SIGTERM if graceful exit fails
- Final SIGKILL if SIGTERM is ignored

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py47-48](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L47-L48)

## Platform Considerations

### Windows-Specific Handling

Windows requires special handling for executable resolution and process management:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py228-232](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L228-L232) [src/mcp/client/stdio/\_\_init\_\_.py16-22](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L16-L22)

### Unix Process Groups

Unix systems use process groups for reliable child process management:

- **Session Creation**: `start_new_session=True` creates new process group
- **Atomic Termination**: `os.killpg()` terminates entire process group
- **Signal Escalation**: SIGTERM → SIGKILL escalation for unresponsive processes

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py250-256](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L250-L256)

## Error Handling and Edge Cases

### Connection Failures

The transport handles various failure scenarios:

```
```

**Sources:** [src/mcp/client/stdio/\_\_init\_\_.py131-137](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L131-L137) [src/mcp/client/stdio/\_\_init\_\_.py154-161](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L154-L161)

### Child Process Cleanup

The transport includes comprehensive tests for child process scenarios:

- **Basic Parent-Child**: Single child process termination
- **Nested Trees**: Multi-level process hierarchies (parent → child → grandchild)
- **Race Conditions**: Parent exits during cleanup sequence
- **Signal Handling**: Processes that ignore specific signals

**Sources:** [tests/client/test\_stdio.py226-521](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_stdio.py#L226-L521)

## Integration Examples

### Basic Usage

```
```

### Custom Environment

```
```

**Sources:** [tests/client/test\_stdio.py37-81](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/tests/client/test_stdio.py#L37-L81) [src/mcp/client/stdio/\_\_init\_\_.py127-128](https://github.com/modelcontextprotocol/python-sdk/blob/146d7efb/src/mcp/client/stdio/__init__.py#L127-L128)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [STDIO Transport](#stdio-transport.md)
- [Configuration](#configuration.md)
- [StdioServerParameters](#stdioserverparameters.md)
- [Default Environment Security](#default-environment-security.md)
- [Connection Management](#connection-management.md)
- [stdio\_client Context Manager](#stdio_client-context-manager.md)
- [Message Processing](#message-processing.md)
- [Process Management](#process-management.md)
- [Cross-Platform Process Creation](#cross-platform-process-creation.md)
- [Process Tree Termination](#process-tree-termination.md)
- [Shutdown and Cleanup](#shutdown-and-cleanup.md)
- [MCP-Compliant Shutdown Sequence](#mcp-compliant-shutdown-sequence.md)
- [Timeout Configuration](#timeout-configuration.md)
- [Platform Considerations](#platform-considerations.md)
- [Windows-Specific Handling](#windows-specific-handling.md)
- [Unix Process Groups](#unix-process-groups.md)
- [Error Handling and Edge Cases](#error-handling-and-edge-cases.md)
- [Connection Failures](#connection-failures.md)
- [Child Process Cleanup](#child-process-cleanup.md)
- [Integration Examples](#integration-examples.md)
- [Basic Usage](#basic-usage.md)
- [Custom Environment](#custom-environment.md)
