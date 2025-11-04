# MCP Qdrant Server Architecture

## Overview

This document outlines the architecture for a Model Context Protocol (MCP) server that integrates with Qdrant to provide embedding search and management capabilities. The server is designed to work with the existing embedding export system and supports multi-vector channels, Matryoshka embeddings, and sparse vectors.

## Architecture Goals

- **Type Safety**: Leverage Python type hints for automatic schema generation
- **Performance**: Async operations and efficient vector search
- **Flexibility**: Support for multiple transport modes (stdio, HTTP)
- **Integration**: Seamless integration with existing embedding export pipeline
- **Scalability**: Handle large embedding datasets with proper resource management

## Core Components

### 1. Server Foundation

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import qdrant_client

# Server initialization
mcp = FastMCP(
    "Qdrant Embedding Server",
    version="1.0.0",
    stateless_http=True,  # For scalability
    json_response=True    # Modern client support
)
```

### 2. Configuration Management

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class QdrantServerConfig:
    """Server configuration with environment variable support"""
    qdrant_host: str = Field(default="localhost", description="Qdrant server host")
    qdrant_port: int = Field(default=6333, description="Qdrant server port")
    qdrant_api_key: Optional[str] = Field(default=None, description="Qdrant API key")
    working_dir: Path = Field(default=Path("./embeddings"), description="Embedding storage directory")
    default_collection: str = Field(default="embeddings", description="Default collection name")
    enable_sparse_vectors: bool = Field(default=True, description="Enable sparse vector support")
    matryoshka_levels: List[int] = Field(default_factory=lambda: [1024, 512, 256, 128])
    
    @classmethod
    def from_env(cls) -> "QdrantServerConfig":
        """Load configuration from environment variables"""
        return cls(
            qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
            qdrant_port=int(os.getenv("QDRANT_PORT", "6333")),
            qdrant_api_key=os.getenv("QDRANT_API_KEY"),
            working_dir=Path(os.getenv("EMBEDDING_WORKING_DIR", "./embeddings")),
            default_collection=os.getenv("DEFAULT_COLLECTION", "embeddings"),
            enable_sparse_vectors=os.getenv("ENABLE_SPARSE", "true").lower() == "true"
        )
```

### 3. Data Models

```python
from typing import Literal
from datetime import datetime

class EmbeddingVector(BaseModel):
    """Single embedding vector with metadata"""
    id: str = Field(description="Unique identifier")
    vector: List[float] = Field(description="Dense embedding vector")
    text: Optional[str] = Field(default=None, description="Original text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Associated metadata")
    created_at: datetime = Field(default_factory=datetime.now)

class MultiVectorEmbedding(BaseModel):
    """Multi-vector embedding with Matryoshka levels"""
    id: str = Field(description="Unique identifier")
    channels: Dict[str, List[float]] = Field(description="Vector channels by dimension")
    text: Optional[str] = Field(default=None, description="Original text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Associated metadata")
    
class SparseVector(BaseModel):
    """Sparse vector representation"""
    indices: List[int] = Field(description="Non-zero dimension indices")
    values: List[float] = Field(description="Non-zero dimension values")

class HybridEmbedding(BaseModel):
    """Combined dense and sparse embedding"""
    id: str = Field(description="Unique identifier")
    dense_vector: List[float] = Field(description="Dense embedding vector")
    sparse_vector: Optional[SparseVector] = Field(default=None, description="Sparse vector")
    text: Optional[str] = Field(default=None, description="Original text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Associated metadata")

class SearchResult(BaseModel):
    """Search result with score and metadata"""
    id: str = Field(description="Result identifier")
    score: float = Field(description="Similarity score")
    text: Optional[str] = Field(default=None, description="Text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Associated metadata")
    vector_channel: Optional[str] = Field(default=None, description="Best matching channel")

class SearchQuery(BaseModel):
    """Search query parameters"""
    query_vector: List[float] = Field(description="Query embedding vector")
    collection: str = Field(description="Target collection")
    limit: int = Field(default=10, ge=1, le=1000, description="Number of results")
    score_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Minimum score threshold")
    filter: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filter")
    channel: Optional[str] = Field(default=None, description="Specific vector channel")
```

### 4. Lifespan Management

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@dataclass
class ServerContext:
    """Shared server context with Qdrant client"""
    config: QdrantServerConfig
    qdrant_client: qdrant_client.QdrantClient
    collections: Dict[str, Any] = field(default_factory=dict)

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncGenerator[ServerContext, None]:
    """Manage server lifecycle and resources"""
    config = QdrantServerConfig.from_env()
    
    # Initialize Qdrant client
    client = qdrant_client.QdrantClient(
        host=config.qdrant_host,
        port=config.qdrant_port,
        api_key=config.qdrant_api_key
    )
    
    # Test connection
    try:
        client.get_collections()
        logger.info("Connected to Qdrant at %s:%d", config.qdrant_host, config.qdrant_port)
    except Exception as e:
        logger.error("Failed to connect to Qdrant: %s", e)
        raise
    
    context = ServerContext(config=config, qdrant_client=client)
    
    try:
        yield context
    finally:
        # Cleanup resources
        client.close()
        logger.info("Qdrant client closed")

# Initialize server with lifespan
mcp = FastMCP(
    "Qdrant Embedding Server",
    lifespan=server_lifespan
)
```

### 5. Tool Definitions

```python
@mcp.tool()
async def search_embeddings(
    query: SearchQuery,
    ctx: Context
) -> List[SearchResult]:
    """Search for similar embeddings in Qdrant"""
    server_ctx = ctx.request_context.lifespan_context
    client = server_ctx.qdrant_client
    
    await ctx.info(f"Searching collection '{query.collection}' with limit {query.limit}")
    
    try:
        # Perform search
        results = client.search(
            collection_name=query.collection,
            query_vector=query.query_vector,
            limit=query.limit,
            score_threshold=query.score_threshold,
            query_filter=query.filter
        )
        
        # Convert to structured results
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                id=result.id,
                score=result.score,
                text=result.payload.get("text"),
                metadata=result.payload.get("metadata", {}),
                vector_channel=query.channel
            ))
        
        await ctx.info(f"Found {len(search_results)} results")
        return search_results
        
    except Exception as e:
        await ctx.error(f"Search failed: {str(e)}")
        raise

@mcp.tool()
async def search_multi_vector(
    query_id: str,
    query_text: str,
    collection: str,
    channels: List[str] = None,
    limit: int = 10,
    ctx: Context = None
) -> Dict[str, List[SearchResult]]:
    """Search across multiple vector channels (Matryoshka levels)"""
    server_ctx = ctx.request_context.lifespan_context
    client = server_ctx.qdrant_client
    
    if channels is None:
        channels = ["1024", "512", "256", "128"]  # Default Matryoshka levels
    
    await ctx.info(f"Multi-vector search across channels: {channels}")
    
    results_by_channel = {}
    
    for channel in channels:
        try:
            # Search specific channel
            channel_results = client.search(
                collection_name=f"{collection}_{channel}",
                query_vector=await generate_embedding(query_text, channel),
                limit=limit
            )
            
            results_by_channel[channel] = [
                SearchResult(
                    id=result.id,
                    score=result.score,
                    text=result.payload.get("text"),
                    metadata=result.payload.get("metadata", {}),
                    vector_channel=channel
                )
                for result in channel_results
            ]
            
        except Exception as e:
            await ctx.warning(f"Channel {channel} search failed: {str(e)}")
            results_by_channel[channel] = []
    
    return results_by_channel

@mcp.tool()
async def create_collection(
    collection_name: str,
    vector_size: int,
    distance: str = "Cosine",
    enable_multivector: bool = False,
    matryoshka_levels: List[int] = None,
    enable_sparse: bool = False,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new Qdrant collection with proper configuration"""
    server_ctx = ctx.request_context.lifespan_context
    client = server_ctx.qdrant_client
    
    await ctx.info(f"Creating collection '{collection_name}' with vector size {vector_size}")
    
    try:
        # Create main collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "size": vector_size,
                "distance": distance,
                "hnsw_config": {
                    "m": 16,
                    "ef_construct": 200,
                    "full_scan_threshold": 10000
                },
                "quantization_config": {
                    "scalar": {
                        "type": "int8",
                        "quantile": 0.99
                    }
                }
            }
        )
        
        collections_created = [collection_name]
        
        # Create multivector channels if enabled
        if enable_multivector and matryoshka_levels:
            for level in matryoshka_levels:
                channel_name = f"{collection_name}_{level}"
                client.create_collection(
                    collection_name=channel_name,
                    vectors_config={
                        "size": level,
                        "distance": distance,
                        "hnsw_config": {
                            "m": 16,
                            "ef_construct": 200
                        }
                    }
                )
                collections_created.append(channel_name)
                await ctx.info(f"Created multivector channel: {channel_name}")
        
        # Create sparse collection if enabled
        if enable_sparse:
            sparse_name = f"{collection_name}_sparse"
            client.create_collection(
                collection_name=sparse_name,
                vectors_config={},
                sparse_vectors_config={
                    "sparse": {
                        "index": {
                            "on_disk": True
                        }
                    }
                }
            )
            collections_created.append(sparse_name)
            await ctx.info(f"Created sparse collection: {sparse_name}")
        
        return {
            "status": "success",
            "collections_created": collections_created,
            "vector_size": vector_size,
            "distance": distance
        }
        
    except Exception as e:
        await ctx.error(f"Collection creation failed: {str(e)}")
        raise

@mcp.tool()
async def upload_embeddings(
    embeddings: List[EmbeddingVector],
    collection: str,
    batch_size: int = 100,
    ctx: Context = None
) -> Dict[str, Any]:
    """Upload embeddings to Qdrant in batches"""
    server_ctx = ctx.request_context.lifespan_context
    client = server_ctx.qdrant_client
    
    await ctx.info(f"Uploading {len(embeddings)} embeddings to '{collection}'")
    
    uploaded_count = 0
    batch_count = 0
    
    try:
        # Process in batches
        for i in range(0, len(embeddings), batch_size):
            batch = embeddings[i:i + batch_size]
            batch_count += 1
            
            # Prepare points
            points = []
            for embedding in batch:
                point = {
                    "id": embedding.id,
                    "vector": embedding.vector,
                    "payload": {
                        "text": embedding.text,
                        "metadata": embedding.metadata,
                        "created_at": embedding.created_at.isoformat()
                    }
                }
                points.append(point)
            
            # Upload batch
            client.upsert(
                collection_name=collection,
                points=points
            )
            
            uploaded_count += len(batch)
            await ctx.report_progress(uploaded_count, len(embeddings), f"Batch {batch_count} uploaded")
            
            # Small delay to avoid overwhelming Qdrant
            await asyncio.sleep(0.1)
        
        await ctx.info(f"Successfully uploaded {uploaded_count} embeddings")
        
        return {
            "status": "success",
            "uploaded_count": uploaded_count,
            "batch_count": batch_count,
            "collection": collection
        }
        
    except Exception as e:
        await ctx.error(f"Upload failed at batch {batch_count}: {str(e)}")
        raise
```

### 6. Resource Definitions

```python
@mcp.resource("collections://{collection_name}")
def get_collection_info(collection_name: str) -> Dict[str, Any]:
    """Get information about a specific collection"""
    # Implementation to retrieve collection details
    pass

@mcp.resource("embeddings://{collection_name}/{embedding_id}")
def get_embedding(collection_name: str, embedding_id: str) -> EmbeddingVector:
    """Retrieve a specific embedding by ID"""
    # Implementation to retrieve embedding
    pass

@mcp.resource("export://{collection_name}/status")
def get_export_status(collection_name: str) -> Dict[str, Any]:
    """Get export status for a collection"""
    # Implementation to check export status
    pass
```

### 7. Prompt Definitions

```python
@mcp.prompt(title="Embedding Search Assistant")
def create_search_prompt(query: str, context: str = None) -> List[base.Message]:
    """Create a prompt for embedding search assistance"""
    messages = [
        base.UserMessage("You are an embedding search assistant."),
        base.UserMessage(f"Search query: {query}")
    ]
    
    if context:
        messages.append(base.UserMessage(f"Context: {context}"))
    
    messages.extend([
        base.UserMessage("Please help me find relevant embeddings using the available search tools."),
        base.AssistantMessage("I'll help you search for relevant embeddings. Let me use the search tools to find the most relevant results.")
    ])
    
    return messages

@mcp.prompt(title="Collection Setup Assistant")
def create_collection_setup_prompt(collection_name: str, vector_size: int) -> List[base.Message]:
    """Create a prompt for collection setup guidance"""
    return [
        base.UserMessage("You are a Qdrant collection setup assistant."),
        base.UserMessage(f"Collection: {collection_name}"),
        base.UserMessage(f"Vector size: {vector_size}"),
        base.UserMessage("Please guide me through setting up this collection with appropriate configurations for embeddings, multi-vector channels, and sparse vectors if needed."),
        base.AssistantMessage("I'll help you set up the Qdrant collection with the proper configuration. Let me create the collection with the recommended settings.")
    ]
```

## Transport Configuration

### STDIO Mode (Local Development)
```python
if __name__ == "__main__":
    mcp.run()  # Default stdio transport
```

### HTTP Mode (Production)
```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

### ASGI Mounting (Integration)
```python
from starlette.applications import Starlette
from starlette.routing import Mount

# Create ASGI app for mounting
qdrant_app = mcp.streamable_http_app()

# Mount in larger application
app = Starlette(routes=[
    Mount("/qdrant", qdrant_app),
    # Other routes...
])
```

## Integration with Existing Export System

### 1. Configuration Compatibility
The MCP server uses the same configuration patterns as the existing export system:
- Working directory configuration
- Collection naming conventions
- Vector dimension handling
- Matryoshka level support

### 2. File Format Support
- Load exported NumPy arrays (`.npy` files)
- Process metadata JSON files
- Handle text exports
- Support multivector JSON configurations

### 3. Collection Creation
- Use same HNSW parameters as upload scripts
- Apply INT8 quantization configuration
- Create multi-vector channels automatically
- Support sparse vector collections

## Error Handling and Observability

### Logging Strategy
```python
@mcp.tool()
async def robust_search(query: SearchQuery, ctx: Context) -> List[SearchResult]:
    """Search with comprehensive error handling"""
    try:
        await ctx.debug(f"Starting search with query: {query.dict()}")
        
        # Validate inputs
        if not query.query_vector:
            raise ValueError("Query vector cannot be empty")
        
        if len(query.query_vector) < 10:  # Minimum reasonable dimension
            await ctx.warning(f"Query vector dimension {len(query.query_vector)} seems low")
        
        # Perform search
        results = await perform_search(query)
        
        await ctx.info(f"Search completed with {len(results)} results")
        return results
        
    except qdrant_client.exceptions.QdrantException as e:
        await ctx.error(f"Qdrant error: {str(e)}")
        raise ValueError(f"Search service error: {str(e)}")
        
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise ValueError(f"Search failed: {str(e)}")
```

### Metrics Collection
```python
# Add to lifespan context
@dataclass
class ServerMetrics:
    search_count: int = 0
    upload_count: int = 0
    error_count: int = 0
    average_search_latency: float = 0.0
    
    def record_search(self, latency: float):
        self.search_count += 1
        self.average_search_latency = (
            (self.average_search_latency * (self.search_count - 1) + latency) / 
            self.search_count
        )
```

## Testing Strategy

### Unit Tests
```python
import pytest
from mcp.server.fastmcp import Context
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_search_embeddings():
    """Test embedding search functionality"""
    # Mock context and client
    ctx = Mock(spec=Context)
    ctx.request_context.lifespan_context = Mock()
    ctx.request_context.lifespan_context.qdrant_client = Mock()
    
    # Test search
    query = SearchQuery(
        query_vector=[0.1, 0.2, 0.3],
        collection="test_collection",
        limit=5
    )
    
    results = await search_embeddings(query, ctx)
    assert len(results) <= 5
    assert all(isinstance(r, SearchResult) for r in results)
```

### Integration Tests
```bash
# Test with MCP Inspector
uv run mcp dev mcp_qdrant_server.py

# Test HTTP transport
uv run mcp dev mcp_qdrant_server.py --transport streamable-http --port 8000
```

## Deployment Options

### 1. Local Development
```bash
# Install dependencies
uv add "mcp[cli]" qdrant-client pydantic

# Run locally
uv run python mcp_qdrant_server.py
```

### 2. Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy server
COPY mcp_qdrant_server.py .

# Expose port for HTTP mode
EXPOSE 8000

# Run server
CMD ["python", "mcp_qdrant_server.py"]
```

### 3. Production with Docker Compose
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  mcp-qdrant-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
      - EMBEDDING_WORKING_DIR=/app/embeddings
    volumes:
      - ./embeddings:/app/embeddings
    depends_on:
      - qdrant

volumes:
  qdrant_data:
```

## Security Considerations

### 1. API Key Management
```python
# Use environment variables for sensitive data
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY environment variable required")
```

### 2. Input Validation
```python
@mcp.tool()
async def validate_embedding(embedding: List[float], ctx: Context) -> bool:
    """Validate embedding vector"""
    if not embedding:
        raise ValueError("Embedding cannot be empty")
    
    if len(embedding) < 10 or len(embedding) > 4096:
        raise ValueError("Embedding dimension must be between 10 and 4096")
    
    if not all(isinstance(x, (int, float)) for x in embedding):
        raise ValueError("All embedding values must be numeric")
    
    return True
```

### 3. Rate Limiting
```python
from asyncio import Semaphore

# Add to server context
@dataclass
class RateLimiter:
    search_semaphore: Semaphore = field(default_factory=lambda: Semaphore(10))
    upload_semaphore: Semaphore = field(default_factory=lambda: Semaphore(5))
```

## Performance Optimization

### 1. Batch Operations
- Use batch uploads for large datasets
- Implement batch search for multiple queries
- Configure optimal batch sizes based on vector dimensions

### 2. Connection Pooling
- Reuse Qdrant client connections
- Implement connection health checks
- Handle connection failures gracefully

### 3. Caching Strategy
- Cache collection metadata
- Cache frequently accessed embeddings
- Implement cache invalidation for updates

## Monitoring and Observability

### 1. Structured Logging
```python
import structlog

logger = structlog.get_logger()

@mcp.tool()
async def monitored_search(query: SearchQuery, ctx: Context) -> List[SearchResult]:
    """Search with structured logging"""
    logger.info(
        "search_started",
        collection=query.collection,
        limit=query.limit,
        vector_dim=len(query.query_vector)
    )
    
    try:
        results = await perform_search(query)
        
        logger.info(
            "search_completed",
            collection=query.collection,
            result_count=len(results),
            top_score=results[0].score if results else 0.0
        )
        
        return results
        
    except Exception as e:
        logger.error(
            "search_failed",
            collection=query.collection,
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

### 2. Metrics Export
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

search_counter = Counter('qdrant_search_total', 'Total search operations')
search_duration = Histogram('qdrant_search_duration_seconds', 'Search duration')
collection_gauge = Gauge('qdrant_collections_total', 'Total collections')
```

This architecture provides a robust, scalable, and type-safe MCP server for Qdrant integration that seamlessly works with the existing embedding export pipeline while providing comprehensive search and management capabilities.