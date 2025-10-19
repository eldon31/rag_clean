# Project Context

## Purpose
This project is a Universal File-to-Knowledge Converter that transforms any file (PDF, DOCX, TXT, MD, HTML, MP3) into LLM-ready knowledge with automatic embeddings and knowledge graph generation. The system enables semantic search across documentation collections using vector databases and graph traversals, optimized for processing technical documentation from libraries and frameworks.

### Key Goals
- **Multi-Format Processing**: Handle diverse document types with specialized extractors (Docling for PDFs, audio transcription for MP3)
- **High-Performance Embeddings**: Generate 768D CodeRankEmbed vectors optimized for code and technical documentation
- **Hybrid Search**: Combine vector similarity search with knowledge graph traversals using RRF (Reciprocal Rank Fusion)
- **Scalable Architecture**: Docker-first deployment supporting batch processing and real-time streaming responses
- **GPU Acceleration**: Kaggle T4 x2 optimized processing at 310-516 chunks/second

## Tech Stack

### Core Technologies
- **Python 3.11+**: Primary development language with async/await patterns
- **FastAPI**: REST API framework with automatic OpenAPI documentation
- **Pydantic V2**: Data validation and serialization with strict typing
- **Docling**: Advanced document processing (PDF, DOCX extraction)
- **Sentence Transformers**: Embedding generation with CodeRankEmbed model

### Vector Databases & Search
- **Chroma**: Primary vector database with HNSW indexing
- **Qdrant**: Alternative vector database with advanced filtering
- **FAISS**: CPU-based similarity search with IVF indexes

### Knowledge Graph
- **Neo4j**: Graph database for entity-relationship modeling
- **Graphiti**: Knowledge graph extraction from text
- **LangChain**: Graph traversal and hybrid search orchestration

### Infrastructure & Deployment
- **Docker**: Containerized services (Chroma, Neo4j, API, Worker)
- **Docker Compose**: Multi-service orchestration
- **Kaggle GPUs**: T4 x2 acceleration for embedding generation
- **Poetry**: Dependency management with lockfile versioning

### External APIs
- **OpenAI API**: LLM-powered entity extraction and question answering
- **Anthropic API**: Alternative LLM provider for knowledge processing

## Project Conventions

### Code Style
- **PEP 8**: Python style guide with 88-character line limits
- **Type Hints**: Full type annotation using `typing` module
- **Docstrings**: Google-style docstrings for all public functions
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes
- **Imports**: Absolute imports with explicit module paths
- **Formatting**: Ruff linter with black-compatible formatting

### Architecture Patterns
- **Pydantic-First**: All data models use Pydantic validation
- **Repository Pattern**: Data access layer abstraction
- **Dependency Injection**: Explicit service dependencies
- **Async/Await**: Non-blocking I/O for all database operations
- **Streaming Responses**: Server-sent events for long-running tasks
- **MCP Integration**: Model Context Protocol for tool extensibility

### Testing Strategy
- **TDD**: Test-driven development with pytest
- **Test Coverage**: 85%+ target with coverage.py
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end service testing
- **Contract Tests**: MCP server interface validation
- **Performance Tests**: Benchmark embedding generation speeds

### Git Workflow
- **Main Branch**: Protected with required reviews
- **Feature Branches**: `feature/` prefix with descriptive names
- **PR Template**: Standardized pull request format
- **Conventional Commits**: Semantic versioning with commit types
- **Release Tags**: Automated versioning with semantic-release

## Domain Context

### RAG (Retrieval-Augmented Generation)
- **Document Chunking**: Intelligent text segmentation using recursive character/text splitters
- **Embedding Models**: Specialized models for code/technical content (CodeRankEmbed, text-embedding-ada-002)
- **Vector Search**: Approximate nearest neighbor search with HNSW/IVF algorithms
- **Hybrid Search**: Combining semantic similarity with keyword-based BM25 scoring
- **Reranking**: Cross-encoder models for improved result precision

### Knowledge Graph Construction
- **Entity Extraction**: Named entity recognition from technical documentation
- **Relationship Mining**: Dependency analysis between code components and concepts
- **Graph Traversal**: Path finding algorithms for multi-hop reasoning
- **Knowledge Fusion**: Merging vector similarity with graph-based recommendations

### MLOps for Embeddings
- **Batch Processing**: GPU-accelerated embedding generation at scale
- **Model Optimization**: Quantization and distillation for production deployment
- **Performance Monitoring**: Latency, throughput, and accuracy metrics
- **Data Pipeline**: ETL processes for continuous knowledge updates

## Important Constraints

### Technical Constraints
- **GPU Memory**: Maximum 15.83GB per T4 GPU (2 GPUs available on Kaggle)
- **API Rate Limits**: OpenAI/Anthropic API quotas and rate limiting
- **Vector Dimensions**: 768D embeddings for CodeRankEmbed model
- **Database Performance**: Sub-2-second query response times required
- **Container Resources**: 2GB memory limit per Docker container

### Business Constraints
- **Open Source**: MIT license with no commercial restrictions
- **Cost Optimization**: Minimize API calls through efficient batching
- **Scalability**: Support 10+ concurrent users with <500ms cached responses
- **Accuracy**: 95%+ retrieval precision for technical documentation queries

### Regulatory Constraints
- **Data Privacy**: No personal data processing or storage
- **API Compliance**: Adherence to OpenAI/Anthropic usage policies
- **Content Safety**: Technical documentation focus excludes sensitive topics

## External Dependencies

### Primary APIs
- **OpenAI API**: GPT-4 for entity extraction, question answering, and graph construction
- **Anthropic API**: Claude for alternative LLM processing and safety validation
- **Context7 MCP**: Real-time documentation retrieval for libraries and frameworks
- **Memory MCP**: Knowledge graph persistence and querying

### Vector Databases
- **Chroma**: Local vector storage with HNSW indexing
- **Qdrant**: Cloud-native vector database with advanced filtering
- **Neo4j**: Graph database for knowledge representation

### Cloud Infrastructure
- **Kaggle**: GPU acceleration for embedding generation (T4 x2 instances)
- **Docker Hub**: Container registry for service images
- **GitHub**: Source control and continuous integration
