# Project Context

## Purpose
Universal File-to-Knowledge Converter: transforms any file (PDF, DOCX, TXT, MD, HTML, MP3) into LLM-ready knowledge with automatic embeddings and knowledge graph generation. Enables semantic and hybrid search across technical documentation collections.

## Tech Stack
- Python 3.11+
- FastAPI (REST API)
- Pydantic V2 (data validation)
- Docling (document extraction)
- Sentence Transformers (embeddings)
- Chroma, Qdrant, FAISS (vector DBs)
- Neo4j (knowledge graph)
- Docker, Docker Compose
- Kaggle T4 x2 GPUs (embedding acceleration)
- Poetry (dependency management)
- OpenAI & Anthropic APIs (LLM-powered extraction)
- Tree-sitter (code parsing)

## Project Conventions

### Code Style
- PEP 8, 88-char lines
- Full type hints
- Google-style docstrings
- snake_case for functions/variables, PascalCase for classes
- Absolute imports
- Ruff linter, black formatting

### Architecture Patterns
- Pydantic-first models
- Repository/data-access pattern
- Dependency injection
- Async/await for DB ops
- Streaming responses for long tasks
- MCP (Model Context Protocol) integration

### Testing Strategy
- TDD with pytest
- 85%+ coverage target
- Unit, integration, contract, and performance tests

### Git Workflow
- Protected main branch
- Feature branches: `feature/` prefix
- PR template required
- Conventional commits
- Semantic-release for versioning

## Domain Context
- RAG (Retrieval-Augmented Generation): chunking, embeddings, vector/hybrid search, reranking
- Knowledge graph construction: entity extraction, relationship mining, graph traversal, fusion
- MLOps for embeddings: batch GPU processing, quantization, monitoring, ETL

## Important Constraints
- GPU: 15.83GB per T4 (Kaggle)
- API rate limits (OpenAI/Anthropic)
- 768D embeddings (CodeRankEmbed)
- Query response <2s
- 2GB/container RAM
- MIT license, open source
- No personal data; technical docs only
- Adhere to API usage policies

## External Dependencies
- OpenAI API (GPT-4)
- Anthropic API (Claude)
- Context7 MCP, Memory MCP
- Chroma, Qdrant, Neo4j
- Kaggle (GPU), Docker Hub, GitHub
