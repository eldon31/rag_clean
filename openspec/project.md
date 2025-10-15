# Project Context

## Purpose
**Universal File-to-Knowledge Converter** - Transform any file (PDF, DOCX, TXT, MD, HTML, MP3) into LLM-ready knowledge with automatic embeddings and semantic search capabilities.

**Core Goals:**
- Multi-format document ingestion with zero manual preprocessing
- Production-ready vector search using Qdrant with optimized embeddings
- MCP (Model Context Protocol) server integration for AI assistant workflows
- Batch processing with parallel execution and progress tracking
- Zero-cost optimizations prioritized over expensive LLM calls

## Tech Stack

### Core Framework
- **Python 3.11+** - Primary language
- **Pydantic v2** - Data validation and settings management
- **Pydantic-AI 0.7.4+** - LLM integration framework
- **FastAPI 0.115.13+** - RESTful API framework
- **MCP 0.9.0+** - Model Context Protocol server

### Document Processing
- **Docling 2.55.0+** - Multi-format document conversion (PDF, DOCX, HTML)
- **Docling HybridChunker** - Intelligent token-aware chunking
- **Transformers 4.30.0+** - HuggingFace tokenizers for accurate token counting

### Vector Database & Search
- **Qdrant 1.7.0+** - Production vector database (HNSW indexes, quantization)
- **nomic-embed-code** - 768-dim embeddings optimized for code and technical docs
- **sentence-transformers 2.2.0+** - Embedding model framework
- **PyTorch 2.0.0+** - Deep learning backend
- **ONNX Runtime 1.16.0+** - 2-4x faster CPU inference (optional optimization)

### LLM Providers
- **OpenAI API 1.0.0+** - GPT models
- **Anthropic API 0.8.0+** - Claude models

### Infrastructure
- **Docker & Docker Compose** - Container orchestration
- **Uvicorn** - ASGI server with standard extras
- **python-multipart** - File upload handling
- **SSE-starlette** - Server-sent events for streaming

### Development Tools
- **pytest 8.0.0+** - Testing framework with async support
- **ruff** - Fast Python linter and formatter
- **mypy** - Static type checking
- **rich** - Terminal formatting and progress bars
- **click** - CLI framework

## Project Conventions

### Code Style
- **Type Hints:** All functions must have type annotations (enforced by mypy)
- **Pydantic Models:** Use Pydantic BaseModel for all data structures (no dataclasses)
- **Field Validation:** Use `Field()` with descriptions for all model fields
- **Naming:**
  - Classes: `PascalCase` (e.g., `DocumentChunk`, `ChunkingConfig`)
  - Functions/variables: `snake_case` (e.g., `chunk_document`, `token_count`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_CHUNK_SIZE`)
  - Private members: prefix with `_` (e.g., `_validate_config`)
- **Docstrings:** Use triple-quoted strings with clear descriptions
- **Line Length:** 120 characters max (ruff default)
- **Imports:** Group by standard library, third-party, local (sorted alphabetically within groups)

### Architecture Patterns

#### Modular Structure
```
src/
├── api/          # FastAPI routes and middleware
├── cli/          # Click-based command-line interface
├── config/       # Pydantic settings and provider configs
├── ingestion/    # Document processing pipeline (chunker, embedder, processor)
├── models/       # Pydantic domain models (chunk, document, collection, etc.)
├── retrieval/    # Vector and hybrid search implementations
├── storage/      # Qdrant client wrapper and collection management
├── monitoring/   # Logging, metrics, profiling
└── worker/       # Background job processing
```

#### Key Design Principles
1. **Dependency Injection:** Pass dependencies explicitly (no globals)
2. **Configuration as Code:** Pydantic Settings for all config (12-factor app)
3. **Fail Fast:** Validate inputs early with Pydantic validators
4. **Immutability Preferred:** Use frozen Pydantic models where possible
5. **Single Responsibility:** Each module has one clear purpose
6. **Zero-Cost First:** Optimize with heuristics before calling LLM APIs
7. **Battle-Tested Libraries:** Prefer Docling HybridChunker over custom chunking logic

#### Data Flow Pattern
```
Document → Docling Converter → HybridChunker → Embedder → Qdrant Storage → Vector Search
```

### Testing Strategy

#### Test Organization
- **Unit Tests:** `tests/unit/` - Pure function tests with mocks
- **Integration Tests:** `tests/integration/` - Component interaction tests
- **End-to-End Tests:** `tests/e2e/` - Full pipeline tests with real data

#### Testing Requirements
- **Coverage Target:** 80%+ for core modules (ingestion, retrieval, storage)
- **Async Support:** Use `pytest-asyncio` for async code
- **Fixtures:** Create reusable fixtures in `conftest.py`
- **Mocking:** Use `pytest-mock` for external dependencies (Qdrant, LLM APIs)
- **Test Naming:** `test_<function>_<scenario>` (e.g., `test_chunk_document_with_code_blocks`)

#### Run Tests
```bash
pytest                     # Run all tests
pytest -v --cov=src        # With coverage report
pytest tests/unit          # Specific test directory
pytest -k "chunk"          # Tests matching pattern
```

### Git Workflow

#### Branch Strategy
- `main` - Production-ready code (protected)
- `feature/*` - New features (e.g., `feature/add-reranking`)
- `fix/*` - Bug fixes (e.g., `fix/chunker-token-overflow`)
- `refactor/*` - Code improvements (e.g., `refactor/pydantic-models`)

#### Commit Conventions (Conventional Commits)
```
<type>(<scope>): <subject>

feat(chunker): add tier 1 optimizations for code block detection
fix(embedder): handle token overflow in nomic-embed-code
refactor(models): migrate from dataclass to Pydantic BaseModel
docs(readme): update quick start guide with Docker commands
test(ingestion): add integration tests for batch processor
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`

#### Pull Request Requirements
- PR must include tests for new functionality
- All CI checks must pass (pytest, ruff, mypy)
- Code review required before merge
- Squash commits on merge to main

## Domain Context

### RAG (Retrieval-Augmented Generation)
This project focuses on the **retrieval** pipeline for RAG systems:
- **Ingestion:** Convert documents → chunks → embeddings → vector store
- **Retrieval:** Query → semantic search → top-K chunks → context for LLM
- **No Generation:** This system provides context; external LLMs handle generation

### Vector Search Concepts
- **Embeddings:** Dense vectors (768-dim) representing semantic meaning
- **HNSW Index:** Approximate nearest neighbor search (fast, scalable)
- **Semantic Similarity:** Cosine similarity between query and chunk embeddings
- **Top-K Retrieval:** Return K most similar chunks to query

### Document Chunking Strategy
- **HybridChunker:** Combines token-aware + structure-aware chunking
- **Token Limits:** nomic-embed-code supports max 2048 tokens per chunk
- **Overlap:** 100 chars overlap between chunks for context continuity
- **Heading Preservation:** Chunks include hierarchical heading paths for context

### MCP Server Architecture
MCP (Model Context Protocol) servers expose tools to AI assistants (Claude, ChatGPT):
- **Tools:** `search_collection`, `get_collection_stats`, `list_collections`
- **Resources:** Pre-indexed documentation (Qdrant, FastAPI, Pydantic, etc.)
- **Prompts:** Reusable search templates for common queries

## Important Constraints

### Performance Requirements
- **Embedding Speed:** Use ONNX Runtime for 2-4x CPU inference speedup
- **GPU Support:** Auto device mapping for multi-GPU environments (Kaggle, Colab)
- **Batch Processing:** Process 8 chunks per batch for embedding efficiency
- **Memory Limits:** nomic-embed-code is 26GB model (use FP16 + device_map="auto")

### Cost Optimization
- **Zero LLM Calls for Chunking:** Use HybridChunker (deterministic, free)
- **No Reranking by Default:** Qdrant HNSW is fast enough for most queries
- **Local Embeddings:** sentence-transformers runs locally (no API costs)

### Data Quality
- **Minimum Chunk Size:** 100 characters (avoid noise)
- **Maximum Chunk Size:** 4096 characters (respect token limits)
- **Token Count Validation:** Use actual tokenizer (not character estimates)
- **Code Block Detection:** Validate complete code fences (```) in chunks

### Security
- **API Key Authentication:** All API endpoints require `X-API-Key` header
- **No Arbitrary Code Execution:** Validate all inputs with Pydantic
- **Rate Limiting:** Implement in production deployments
- **Docker Isolation:** Run services in containers

## External Dependencies

### Required Services
- **Qdrant Vector Database** - `localhost:6333` (HTTP), `localhost:6334` (gRPC)
  - Docker: `qdrant/qdrant:latest`
  - Persistent storage: `qdrant_storage` volume
  - Required for: Vector search, collection management

### Optional Services
- **Neo4j Graph Database** - Knowledge graph (future enhancement)
- **Redis** - Caching layer (future enhancement)

### External APIs
- **OpenAI API** - GPT models (optional, for agent workflows)
- **Anthropic API** - Claude models (optional, for agent workflows)
- **HuggingFace Hub** - Download pretrained models (nomic-embed-code, tokenizers)

### Python Package Ecosystem
- **Docling** - Document processing (critical dependency, no alternatives)
- **Qdrant Client** - Vector database SDK (production-ready, actively maintained)
- **sentence-transformers** - Embedding models (HuggingFace ecosystem)
- **FastMCP** - MCP server framework (active development, breaking changes possible)

### Development Infrastructure
- **Docker Desktop** - Container runtime (Windows, macOS)
- **WSL2** - Linux subsystem for Windows development
- **Kaggle Notebooks** - GPU environments for batch processing (2x Tesla T4)
- **GitHub Actions** - CI/CD (future enhancement)

---

## Quick Reference

### Start Development Environment
```bash
# Start Qdrant
docker-compose up -d

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest -v
```

### Common Commands
```bash
# CLI tool
ufk --help

# Run MCP server
python mcp_server/qdrant_fastmcp_server.py

# Start API server
uvicorn src.api.main:app --reload

# Code quality
ruff check src/
mypy src/
```
