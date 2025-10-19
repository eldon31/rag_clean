# Enterprise FastMCP API Server v2.0

Production-ready FastMCP server with advanced REST API integration for Qdrant vector operations. Enhanced with server composition, OpenAPI integration, and enterprise-grade optimizations.

## 🚀 Features

### Core Architecture
- **FastMCP Framework**: Server composition with mounting patterns
- **OpenAPI Integration**: Automatic API documentation and client generation
- **Advanced Middleware**: Authentication, rate limiting, monitoring, and error handling
- **Proxy Capabilities**: Multi-tenant deployments with load balancing
- **Multi-level Caching**: Embeddings, queries, and results with aiocache
- **Connection Pooling**: Optimized HTTP and Qdrant gRPC connections

### Enterprise Features
- **Kubernetes Native**: HPA support with ConfigMaps and Secrets
- **Monitoring Stack**: Prometheus/Grafana integration with custom metrics
- **HTTP+SSE Transport**: Real-time streaming capabilities
- **Dual Interfaces**: Both MCP tools and REST API endpoints
- **Production Observability**: Distributed tracing and performance monitoring

### Collections Supported
- `sentence_transformers_768`: 457 vectors (embedding expertise)
- `docling_768`: 1,089 vectors (document processing mastery)
- `qdrant_ecosystem_768`: 8,108 vectors (vector DB optimization)

## 📋 Requirements

```bash
pip install -r requirements-fastmcp-api.txt
```

Key dependencies:
- fastapi>=0.100.0
- fastmcp>=0.9.0
- qdrant-client>=1.7.0
- sentence-transformers>=2.2.0
- uvicorn>=0.23.0
- prometheus-client>=0.17.0 (optional)
- psutil>=5.9.0

## ⚙️ Configuration

Environment variables:

```bash
# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-api-key-here

# Embedding Configuration
EMBEDDING_MODEL=nomic-ai/CodeRankEmbed
EMBEDDING_DEVICE=auto  # auto, cpu, cuda

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Performance Tuning
MAX_CONNECTIONS=100
CONNECTION_POOL_SIZE=50
EMBEDDING_BATCH_SIZE=32

# Enterprise Features
ENABLE_METRICS=true
METRICS_PORT=9090
ENABLE_AUTH=false
ENABLE_OPENAPI_ENHANCEMENT=true
```

## 🏃‍♂️ Quick Start

### Development Mode
```bash
# Start the server
python -m uvicorn mcp_server.qdrant_fastmcp_api_server:app --reload --host 0.0.0.0 --port 8000

# Or use the convenience script
./start_server.sh
```

### Production Deployment
```bash
# Using Docker
docker build -f Dockerfile.fastmcp-api -t fastmcp-api .
docker run -p 8000:8000 -e QDRANT_URL=http://host.docker.internal:6333 fastmcp-api

# Using Docker Compose
docker-compose -f docker-compose.fastmcp-api.yml up

# Kubernetes deployment
kubectl apply -f k8s-deployment.yaml
```

## 📚 API Documentation

### REST API Endpoints

#### Health & Monitoring
- `GET /health` - Comprehensive health check
- `GET /metrics` - Prometheus metrics
- `GET /server/stats` - Detailed server statistics

#### Collections Management
- `GET /collections` - List available collections
- `GET /collections/stats` - Detailed collection statistics
- `POST /collections/{name}/optimize` - Collection optimization recommendations

#### Search Operations
- `POST /search` - Basic semantic search
- `POST /search/ultimate` - Advanced search with auto-classification

#### Optimization Tools
- `POST /optimize/chunking` - Content chunking strategy recommendations
- `GET /performance/analysis` - Collection performance analysis

### MCP Tools

#### Search Tools
- `semantic_search_enterprise` - Enterprise semantic search
- `semantic_search_ultimate` - Ultimate search with auto-classification
- `search_ultimate_knowledge` - Legacy knowledge base search

#### Analytics Tools
- `get_server_stats` - Server performance statistics
- `get_collection_stats` - Collection statistics
- `analyze_collection_performance` - Performance analysis
- `optimize_collection_performance` - Collection optimization

#### Optimization Tools
- `optimize_chunking_strategy` - Chunking strategy recommendations

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python mcp_server/test_qdrant_fastmcp_api_server.py

# Run specific test
python -m pytest mcp_server/test_qdrant_fastmcp_api_server.py::TestFastMCPAPIServer::test_health_endpoint -v
```

## 📊 Monitoring

### Prometheus Metrics
The server exposes Prometheus metrics at `/metrics`:

```
# HELP qdrant_fastmcp_requests_total Total number of requests
# TYPE qdrant_fastmcp_requests_total counter
qdrant_fastmcp_requests_total 150

# HELP qdrant_fastmcp_request_duration_seconds Request duration in seconds
# TYPE qdrant_fastmcp_request_duration_seconds histogram

# HELP qdrant_fastmcp_active_connections Current active connections
# TYPE qdrant_fastmcp_active_connections gauge
```

### Health Checks
```bash
# Basic health check
curl http://localhost:8000/health

# Detailed server stats
curl http://localhost:8000/server/stats

# Collection performance
curl http://localhost:8000/performance/analysis
```

## 🔧 Advanced Configuration

### Custom Middleware
The server includes advanced middleware for production deployments:

- **RequestLoggingMiddleware**: Performance logging and request tracking
- **ErrorHandlingMiddleware**: Circuit breaker pattern and error recovery
- **MetricsMiddleware**: Prometheus metrics collection
- **RateLimitingMiddleware**: Request rate limiting (when available)

### Caching Strategy
Multi-level caching for optimal performance:

1. **Embedding Cache**: LRU cache for query embeddings
2. **Query Cache**: Results cache with TTL
3. **Connection Pooling**: HTTP and Qdrant connection reuse

### GPU Support
Automatic GPU detection and utilization:

```python
# Configuration options
EMBEDDING_DEVICE=auto  # Auto-detect GPU
EMBEDDING_DEVICE=cuda  # Force GPU
EMBEDDING_DEVICE=cpu   # Force CPU
```

## 🚀 Performance Targets

- **Latency**: <10ms cached, <100ms new queries
- **Throughput**: 2000+ QPS with horizontal scaling
- **Availability**: 99.9% uptime with circuit breakers
- **Memory**: <512MB per instance with intelligent caching

## 🐳 Docker Deployment

```yaml
# docker-compose.fastmcp-api.yml
version: '3.8'
services:
  fastmcp-api:
    build:
      context: .
      dockerfile: Dockerfile.fastmcp-api
    ports:
      - "8000:8000"
    environment:
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - qdrant
```

## 📝 Development

### Project Structure
```
mcp_server/
├── qdrant_fastmcp_api_server.py    # Main server application
├── test_qdrant_fastmcp_api_server.py # Test suite
├── ultimate_qdrant_mcp_v2_fixed.py   # Legacy MCP server
└── ...

requirements/
├── requirements-fastmcp-api.txt     # Server dependencies
└── requirements-mcp.txt            # MCP-specific deps

docs/
├── AGENTS.md                        # Agent specifications
├── QUICK_START_CORRECTED_V4.md      # Quick start guide
└── ...
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Support

For issues and questions:
- Check the [troubleshooting guide](docs/TROUBLESHOOTING.md)
- Review [API documentation](http://localhost:8000/docs) when running
- Open an issue on GitHub

---

**Built with ❤️ by AI Assistant - Enhanced with FastMCP Architecture Patterns**