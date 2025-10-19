## Why
The project currently has multiple Qdrant MCP server implementations scattered across different files, but lacks a unified, containerized MCP server that can be easily deployed as a Docker service. This creates operational complexity and inconsistency in how vector search capabilities are exposed via the Model Context Protocol.

## What Changes
- Create a new `qdrant-mcp-server` capability that provides containerized MCP server functionality
- Implement a FastMCP-based server using FastAPI for HTTP transport
- Add Docker containerization with proper health checks and configuration
- Integrate with existing Qdrant vector database for semantic search operations
- Provide standardized MCP tools for vector operations (search, upload, collection management)

## Impact
- Affected specs: Creates new `qdrant-mcp-server` capability
- Affected code: New files in `mcp_server/` directory with Docker integration
- **BREAKING**: None - this is a new capability that doesn't modify existing functionality