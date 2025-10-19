## ADDED Requirements

### Requirement: MCP Server Container
The system SHALL provide a containerized MCP server that exposes vector database operations via the Model Context Protocol over HTTP transport using FastAPI.

#### Scenario: Server startup
- **WHEN** the Docker container starts
- **THEN** the MCP server SHALL initialize with FastMCP
- **AND** SHALL connect to the configured Qdrant instance
- **AND** SHALL expose tools at the configured HTTP endpoint

### Requirement: Semantic Search Tool
The MCP server SHALL provide a `semantic_search` tool that performs vector similarity search across Qdrant collections using nomic-ai/CodeRankEmbed.

#### Scenario: Successful search
- **WHEN** a client calls the semantic_search tool with query and collection parameters
- **THEN** the server SHALL embed the query using nomic-ai/CodeRankEmbed (768D)
- **AND** SHALL perform vector search in Qdrant with configurable score threshold
- **AND** SHALL return formatted results with scores, content, and metadata

### Requirement: Vector Upload Tool
The MCP server SHALL provide a `upload_vectors` tool that ingests vector data into Qdrant collections.

#### Scenario: Batch upload
- **WHEN** a client provides vectors and metadata
- **THEN** the server SHALL validate the input format
- **AND** SHALL upload vectors to the specified collection
- **AND** SHALL return success confirmation with upload statistics

### Requirement: Collection Management Tool
The MCP server SHALL provide a `manage_collections` tool for creating, listing, and deleting vector collections.

#### Scenario: List collections
- **WHEN** a client requests collection information
- **THEN** the server SHALL query Qdrant for available collections
- **AND** SHALL return collection names, sizes, and metadata

### Requirement: Health Check Endpoint
The MCP server SHALL provide a health check endpoint for container orchestration monitoring.

#### Scenario: Health verification
- **WHEN** an orchestrator checks the /health endpoint
- **THEN** the server SHALL verify Qdrant connectivity
- **AND** SHALL return HTTP 200 if healthy or 503 if unhealthy

### Requirement: Configuration Management
The MCP server SHALL support environment-based configuration for Qdrant connection and server settings.

#### Scenario: Environment configuration
- **WHEN** the server starts
- **THEN** it SHALL read QDRANT_URL and QDRANT_API_KEY from environment
- **AND** SHALL use default values for optional settings
- **AND** SHALL log configuration on startup