# qdrant-mcp-ecosystem Specification

## Purpose
Extend the existing MCP server to expose the `qdrant_ecosystem` collection (Qdrant documentation embeddings) with semantic search, storage, and statistics tools for AI assistants.

## ADDED Requirements

### Requirement: Ecosystem Collection Search Tool

The MCP server SHALL expose a `qdrant_search_ecosystem` tool that performs semantic similarity search on the Qdrant documentation collection.

#### Scenario: Basic semantic search on Qdrant docs
- **GIVEN** the `qdrant_ecosystem` collection contains 1,344 embedded documents
- **WHEN** AI assistant calls `qdrant_search_ecosystem` with query "How to optimize HNSW indexing?"
- **THEN** the tool returns top 5 semantically similar chunks
- **AND** each result includes score, text content, subdirectory, and source_file metadata
- **AND** results are ordered by descending similarity score

#### Scenario: Filtered search by subdirectory
- **GIVEN** user wants results only from `qdrant_client_docs` subdirectory
- **WHEN** tool is called with `query="batch upload"` and `filter={"subdirectory": "qdrant_client_docs"}`
- **THEN** results are limited to chunks from that subdirectory
- **AND** other subdirectories (qdrant_documentation, qdrant_examples, etc.) are excluded

#### Scenario: Score threshold filtering
- **GIVEN** user sets `score_threshold=0.8` for high-confidence results
- **WHEN** semantic search executes
- **THEN** only results with similarity score ≥ 0.8 are returned
- **AND** lower-scoring results are excluded even if limit not reached

#### Scenario: Empty results handling
- **GIVEN** query has no semantically similar matches above threshold
- **WHEN** search executes
- **THEN** tool returns empty results list
- **AND** response includes message: "No results found matching criteria"

### Requirement: Ecosystem Collection Storage Tool

The MCP server SHALL expose a `qdrant_store_ecosystem` tool that embeds and stores new documentation chunks in the collection.

#### Scenario: Store new documentation chunk
- **GIVEN** user provides text "New Qdrant feature: quantization for 4x memory savings"
- **WHEN** `qdrant_store_ecosystem` is called with text and metadata `{"subdirectory": "qdrant_documentation", "source_file": "optimization.md"}`
- **THEN** text is embedded using nomic-embed-code model (3584-dim)
- **AND** vector + metadata are stored in `qdrant_ecosystem` collection
- **AND** tool returns point ID and confirmation message

#### Scenario: Automatic original_id preservation
- **GIVEN** stored chunk has string ID "qdrant_ecosystem:new_docs:optimization.md:chunk:0"
- **WHEN** storage operation completes
- **THEN** ID is converted to UUID via MD5 hash for Qdrant compatibility
- **AND** original string ID is preserved in payload as `original_id` field

### Requirement: Collection Statistics Tool

The MCP server SHALL expose a `qdrant_get_stats` tool that returns metrics for all registered collections.

#### Scenario: Retrieve stats for all collections
- **GIVEN** MCP server manages 3 collections (agent_kit, inngest_overall, qdrant_ecosystem)
- **WHEN** `qdrant_get_stats` is called without arguments
- **THEN** tool returns statistics for all three collections
- **AND** each collection stat includes: name, vector_count, indexed_vectors_count, points_count, segments_count

#### Scenario: Single collection stats
- **GIVEN** user requests stats only for `qdrant_ecosystem`
- **WHEN** `qdrant_get_stats` is called with `collection_name="qdrant_ecosystem"`
- **THEN** only qdrant_ecosystem stats are returned
- **AND** response includes: 1,344 total points, vector dimension 3584, distance metric COSINE

### Requirement: MCP Server Initialization

The MCP server SHALL initialize the `qdrant_ecosystem` collection connection lazily on first use.

#### Scenario: Lazy collection initialization
- **GIVEN** MCP server starts without pre-loading collections
- **WHEN** first tool call targets `qdrant_ecosystem` collection
- **THEN** QdrantStore instance is created with config (host=localhost, port=6333, collection_name=qdrant_ecosystem, vector_size=3584)
- **AND** connection is cached in registry for subsequent requests
- **AND** initialization latency is logged

#### Scenario: Connection reuse across requests
- **GIVEN** `qdrant_ecosystem` collection is already initialized
- **WHEN** multiple tool calls target the same collection within session
- **THEN** existing QdrantStore instance is reused
- **AND** no redundant connections are created
- **AND** performance overhead is minimized

### Requirement: Error Handling and Validation

The MCP server SHALL provide clear error messages for invalid requests and connection failures.

#### Scenario: Qdrant connection failure
- **GIVEN** Qdrant server is not running on localhost:6333
- **WHEN** MCP tool attempts to search qdrant_ecosystem
- **THEN** tool returns error: "Failed to connect to Qdrant at localhost:6333. Ensure Qdrant is running: docker compose up -d"
- **AND** error is logged with stack trace
- **AND** MCP client receives structured error response

#### Scenario: Empty query validation
- **GIVEN** user calls `qdrant_search_ecosystem` with empty query string
- **WHEN** validation runs
- **THEN** tool returns error: "Query cannot be empty"
- **AND** no embedding or search is performed

#### Scenario: Invalid limit parameter
- **GIVEN** user sets `limit=0` or `limit>100`
- **WHEN** parameter validation runs
- **THEN** tool returns error: "Limit must be between 1 and 100"
- **AND** sensible default (5) is not applied to invalid input

## MODIFIED Requirements

### Requirement: MCP Tool Registration (from existing server)

The MCP server tool list SHALL include ecosystem collection tools alongside existing agent_kit and inngest_overall tools.

#### Scenario: List all available tools
- **GIVEN** MCP server is initialized
- **WHEN** client calls `list_tools()`
- **THEN** response includes 9 tools total:
  - `qdrant_search_agent_kit`
  - `qdrant_search_inngest`
  - `qdrant_search_ecosystem` (NEW)
  - `qdrant_store_agent_kit`
  - `qdrant_store_inngest`
  - `qdrant_store_ecosystem` (NEW)
  - `qdrant_get_stats` (MODIFIED to include ecosystem)

#### Scenario: Tool descriptions are clear and actionable
- **GIVEN** user browses available MCP tools
- **WHEN** `qdrant_search_ecosystem` description is displayed
- **THEN** description reads: "Search the qdrant_ecosystem collection (Qdrant documentation) using semantic similarity with nomic-embed-code"
- **AND** inputSchema clearly defines query (required), limit (optional, default: 5), score_threshold (optional, default: 0.7)

