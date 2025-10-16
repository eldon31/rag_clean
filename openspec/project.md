# Project Context

## Purpose
**Universal File-to-Knowledge Converter** - Transform any file (PDF, DOCX, TXT, MD, HTML, MP3) into LLM-ready knowledge with automatic embeddings and vector search capabilities.

### Goals
- **Multi-format document processing**: Support PDF, DOCX, TXT, MD, HTML, and MP3 (audio transcription)
- **Production-ready RAG**: Semantic search using Qdrant vector database with optimized embeddings
- **Intelligent chunking**: Preserve document structure and code context using Docling's HybridChunker
- **MCP integration**: Expose functionality as Model Context Protocol servers for LLM agents
- **Zero-cost optimizations**: Maximize accuracy without API costs (achieved 4% improvement in Tier 1)

## Tech Stack

### Core Technologies
- **Python 3.11+**: Primary language
- **Pydantic v2**: Data validation and settings management (strict compliance required)
- **Pydantic AI**: LLM integration framework

### Document Processing
- **Docling v2.55+**: Multi-format document conversion (PDF, DOCX, HTML, etc.)
- **transformers**: Tokenization for Docling HybridChunker
- **Docling HybridChunker**: Token-aware, structure-preserving chunking

### Vector Database & Embeddings
- **Qdrant**: Production vector database with quantization support
- **nomic-ai/CodeRankEmbed**: 768-dim embeddings (migrated from CodeRankEmbed)
- **sentence-transformers**: Embedding and reranking models
- **ONNX Runtime + Optimum**: 2-4x faster CPU inference (optional)

### API & Services
- **FastAPI**: REST API framework
- **MCP (Model Context Protocol)**: Server implementations for LLM agents
- **uvicorn**: ASGI server
- **Docker Compose**: Service orchestration (Qdrant)

### Development Tools
- **pytest**: Testing framework with async support
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **black**: Code formatting

## Project Conventions

### Code Style
- **Pydantic Models**: Use `BaseModel` instead of dataclasses for all configuration and data structures
- **Type Hints**: Mandatory for all function signatures and class attributes
- **Docstrings**: Google-style docstrings required for all public functions/classes
- **Imports**: Absolute imports from `src.*` modules; group into stdlib, third-party, local
- **Naming**:
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: `_leading_underscore`

### Architecture Patterns

#### Modular Structure
```
src/
├── agent/          # LLM agent integration
├── api/            # FastAPI endpoints
├── config/         # Pydantic configuration models
├── ingestion/      # Document processing & chunking
├── retrieval/      # Vector search & reranking
├── storage/        # Qdrant client abstraction
├── models/         # Shared data models
└── monitoring/     # Logging & metrics
```

#### Key Patterns
- **Configuration**: Environment-based using Pydantic Settings (`from_env()` class methods)
- **Dependency Injection**: Prefer explicit configuration passing over globals
- **Error Handling**: Use custom exceptions from `src/exceptions.py`
- **Async-First**: Use `async/await` for I/O operations (Qdrant, embeddings, API endpoints)
- **Metadata Enrichment**: All chunks include structured metadata (heading paths, code block detection, token counts)

#### Design Decisions
- **Docling HybridChunker**: Battle-tested, token-precise, preserves document structure (no custom chunking)
- **Qdrant Only**: Removed Chroma/ChromaDB; Qdrant is production-ready with quantization
- **No Knowledge Graphs**: Removed Neo4j/Graphiti; focus on vector search + metadata filtering
- **Zero-Cost First**: Optimize with metadata, structure, tokenization before adding API costs

### Testing Strategy
- **Test Framework**: pytest with async support (`pytest-asyncio`)
- **Coverage**: Use `pytest-cov` for coverage reporting
- **Test Structure**:
  - Unit tests: `tests/unit/`
  - Integration tests: `tests/integration/`
  - Verification scripts: `scripts/verify_*.py`
- **Mocking**: Use `pytest-mock` for external dependencies
- **Validation Scripts**: Standalone verification for major features (e.g., `verify_tier1_chunker.py`)
- **Example Tests**: See `test_mcp_search.py`, `mcp_server/test_qdrant_server.py`

### Git Workflow
- **Branch**: `main` (default branch)
- **Commits**: Descriptive messages following conventional commits format preferred
- **Repository**: `eldonrey0531/rad_clean`
- **Documentation**: Keep migration guides, implementation summaries, and quick references up-to-date

## Domain Context

### RAG (Retrieval-Augmented Generation)
This project builds RAG infrastructure for LLM applications:
- **Chunking**: Break documents into semantically meaningful pieces with context
- **Embeddings**: Convert chunks to dense vectors for similarity search
- **Retrieval**: Find relevant chunks based on semantic similarity
- **Metadata Filtering**: Use document structure (headings, code blocks) to improve precision

### Embedding Model Migration
- **Old**: `nomic-ai/CodeRankEmbed` (768-dim)
- **New**: `nomic-ai/CodeRankEmbed` (768-dim)
- **Benefit**: 75x faster queries (30s → 400ms), 4.7x smaller vectors, 4x memory reduction
- **Status**: Embeddings generated, migration scripts ready

### MCP (Model Context Protocol)
Expose vector search as MCP servers so LLM agents can query documentation:
- `mcp_server/qdrant_code_server.py`: Main MCP implementation
- Collections: `docling`, `qdrant_ecosystem`, `sentence_transformers`

### Tier 1 Optimizations (Completed)
Zero-cost metadata enrichment for 4% accuracy improvement:
1. **Code Block Detection**: Identify incomplete code fences
2. **Heading Path Extraction**: Hierarchical context (e.g., "Installation > Quick Start")
3. **Token Count Validation**: Ensure chunks fit embedding model limits (2048 tokens)

## Important Constraints

### Technical Constraints
- **Python 3.11+**: Minimum version requirement
- **Pydantic v2**: All models must use Pydantic BaseModel (not dataclasses)
- **Token Limits**: CodeRankEmbed/CodeRankEmbed max 2048 tokens per chunk
- **Memory**: Optimize for CPU inference (ONNX Runtime) not GPU
- **Windows Environment**: Default shell is PowerShell v5.1

### Business Constraints
- **Zero-Cost Preference**: Avoid LLM API calls for chunking/processing where possible
- **Production-Ready**: Prioritize Qdrant quantization, ONNX optimization over experimental features
- **Code-Focused**: Optimized for technical documentation and code repositories

### Regulatory Constraints
- None currently (open-source project)

## External Dependencies

### Vector Database
- **Qdrant**: `http://localhost:6333` (Docker container)
  - API: REST + gRPC (port 6334)
  - Storage: Persistent volume (`qdrant_storage`)
  - Authentication: Optional API key via `QDRANT_API_KEY`

### Embedding Models
- **nomic-ai/CodeRankEmbed**: Primary embedding model (768-dim)
- **sentence-transformers**: Reranking and alternative embeddings
- **Hugging Face Transformers**: Tokenizers for chunking

### LLM Providers (Optional)
- **OpenAI**: API key via `OPENAI_API_KEY`
- **Anthropic**: API key via `ANTHROPIC_API_KEY`

### Document Processing
- **Docling**: Multi-format document conversion (requires model artifacts)
- **VLM Models**: Optional vision-language models for advanced PDF processing

### Infrastructure
- **Docker & Docker Compose**: Required for Qdrant deployment
- **ONNX Runtime**: Optional for faster CPU inference
