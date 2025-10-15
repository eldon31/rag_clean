# embedding-alignment Specification

## Purpose
Ensure consistent, accurate embedding generation aligned with Qdrant best practices and nomic-embed-text-v1.5 model specifications. Fix dimension mismatches, optimize chunking for code embeddings, and implement proper matryoshka representation learning dimensions.

## Problem Statement

The codebase has **critical misalignments** that affect vector search accuracy and performance:

1. **Dimension Mismatch Crisis**: 
   - `kaggle_embed_qdrant_ecosystem.py` says 768-dim
   - `src/ingestion/embedder.py` says 3584-dim
   - Actual qdrant_ecosystem collection: **3584-dim** (verified)
   - **nomic-embed-text-v1.5 actual output: 768-dim** (verified)
   - This means search queries will use 768-dim while collection expects 3584-dim → **complete search failure**

2. **Model Confusion**:
   - `nomic-ai/nomic-embed-code` (7B params, not usable on CPU, no matryoshka)
   - `nomic-ai/nomic-embed-text-v1.5` (137M params, matryoshka, CPU-friendly, **actual model being used**)
   - Codebase references are inconsistent

3. **Chunking Not Optimized for Code**:
   - Current chunker uses 2048 char chunks, but not optimized for code token limits
   - No consideration of matryoshka dimensions (64, 128, 256, 512, 768 for nomic-embed-text-v1.5)
   - Missing code-specific context preservation

## ADDED Requirements

### Requirement: Correct Nomic Model Identification

The system SHALL use `nomic-ai/nomic-embed-text-v1.5` with matryoshka representation learning dimensions (768, 512, 256, 128, 64).

#### Scenario: Configure correct embedding model
- **GIVEN** system is initializing embedding configuration
- **WHEN** EmbedderConfig is created
- **THEN** model_name is "nomic-ai/nomic-embed-text-v1.5" (not nomic-embed-code)
- **AND** default dimension is 768 (full matryoshka dimension)
- **AND** model supports matryoshka dimensions: [64, 128, 256, 512, 768]
- **AND** documentation clearly states: "nomic-embed-code (7B) is NOT used - CPU incompatible, no matryoshka"

#### Scenario: Detect dimension mismatch at startup
- **GIVEN** qdrant_ecosystem collection has 3584-dim vectors
- **WHEN** embedder initializes with nomic-embed-text-v1.5 (768-dim)
- **THEN** system logs CRITICAL warning: "Dimension mismatch detected! Collection expects 3584-dim, model outputs 768-dim. Search will fail. Recommendation: Re-embed collection with nomic-embed-text-v1.5 or use different model."
- **AND** system raises ConfigurationError preventing startup

#### Scenario: Validate embedding dimension at runtime
- **GIVEN** embedder generates vector for text "def factorial(n): return 1 if n == 0 else n * factorial(n-1)"
- **WHEN** embedding is generated
- **THEN** vector dimension is exactly 768 (for nomic-embed-text-v1.5 full dimension)
- **AND** vector norm is approximately 1.0 (normalized)
- **AND** dimension matches collection configuration

### Requirement: Matryoshka Dimension Support

The system SHALL support matryoshka representation learning with dimension selection (768, 512, 256, 128, 64) for nomic-embed-text-v1.5.

#### Scenario: Use optimal dimension for code search
- **GIVEN** user wants to optimize for speed vs accuracy tradeoff
- **WHEN** QdrantCollectionConfig is created with matryoshka_dim=512
- **THEN** embeddings are truncated to first 512 dimensions
- **AND** collection is configured with vector_size=512
- **AND** search speed improves by ~33% vs 768-dim
- **AND** recall@10 remains ≥0.95 (matryoshka design preserves quality)

#### Scenario: Recommend matryoshka dimension based on collection size
- **GIVEN** collection has <10K documents
- **WHEN** auto-optimization is enabled
- **THEN** system recommends matryoshka_dim=256 (2x faster, minimal recall loss)
- **AND** for >10K documents, recommends matryoshka_dim=512 (balanced)
- **AND** for >100K documents, recommends matryoshka_dim=768 (full quality)

#### Scenario: Validate matryoshka dimension
- **GIVEN** user sets matryoshka_dim=400 (not supported)
- **WHEN** validation runs
- **THEN** ValidationError is raised: "matryoshka_dim must be one of [64, 128, 256, 512, 768] for nomic-embed-text-v1.5"
- **AND** suggestion is provided: "Use 512 for balanced performance/quality"

### Requirement: Code-Optimized Chunking

The system SHALL optimize chunking strategy for code embeddings with proper token limits and context preservation.

#### Scenario: Chunk code with function-level granularity
- **GIVEN** Python file with 10 functions averaging 50 lines each
- **WHEN** DoclingHybridChunker processes the file with code_mode=True
- **THEN** each function becomes a separate chunk (preserves function boundaries)
- **AND** chunk metadata includes: function_name, signature, docstring
- **AND** heading context preserves: module > class > function hierarchy
- **AND** chunks stay within 512 token limit (optimal for nomic-embed-text-v1.5)

#### Scenario: Optimize chunk size for embedding model token limit
- **GIVEN** nomic-embed-text-v1.5 has 8192 token limit (but optimal is <512 for accuracy)
- **WHEN** ChunkingConfig is created for code
- **THEN** max_tokens is set to 512 (not 2048)
- **AND** chunk_overlap is set to 50 tokens (10%)
- **AND** tokenizer is nomic-ai/nomic-embed-text-v1.5 tokenizer (not generic)
- **AND** validation ensures chunks don't exceed 512 tokens

#### Scenario: Preserve code context in chunks
- **GIVEN** long function with 100+ lines
- **WHEN** chunking splits it into multiple chunks
- **THEN** each chunk includes:
  - Function signature as prefix
  - Docstring (if present)
  - Relevant class/module context
  - Line number range in metadata
- **AND** overlapping chunks share context (50 token overlap)

### Requirement: Embedding Normalization and Distance Metrics

The system SHALL apply proper normalization and distance metrics aligned with nomic-embed-text-v1.5 training.

#### Scenario: Normalize embeddings for cosine similarity
- **GIVEN** nomic-embed-text-v1.5 is trained with cosine similarity
- **WHEN** embeddings are generated
- **THEN** vectors are L2-normalized (unit length)
- **AND** vector norm is 1.0 ± 0.001
- **AND** Qdrant collection uses Cosine distance metric

#### Scenario: Detect incorrect distance metric
- **GIVEN** collection is configured with Euclidean distance
- **WHEN** validation runs
- **THEN** warning is logged: "nomic-embed-text-v1.5 is trained for Cosine similarity, but collection uses Euclidean. Recommendation: Use Cosine for optimal accuracy."
- **AND** migration script is suggested

#### Scenario: Apply task-specific prompts (nomic convention)
- **GIVEN** embedding query text "find API documentation for authentication"
- **WHEN** query embedding is generated
- **THEN** prefix is prepended: "search_query: find API documentation for authentication"
- **AND** for documents, prefix is: "search_document: " + content
- **AND** this follows nomic-ai recommended practice for asymmetric search

### Requirement: Re-embedding Strategy for Dimension Mismatch

The system SHALL provide migration tools to re-embed existing collections when dimension mismatch is detected.

#### Scenario: Detect and warn about re-embedding requirement
- **GIVEN** qdrant_ecosystem collection has 3584-dim vectors
- **WHEN** system attempts to use nomic-embed-text-v1.5 (768-dim)
- **THEN** clear error message is displayed:
  ```
  ERROR: Dimension mismatch detected!
  
  Collection: qdrant_ecosystem
  Expected: 3584 dimensions
  Current model (nomic-embed-text-v1.5): 768 dimensions
  
  Options:
  1. Re-embed collection: python scripts/re_embed_collection.py --collection qdrant_ecosystem --model nomic-embed-text-v1.5 --dimension 768
  2. Use different model that produces 3584-dim vectors
  3. Create new collection with correct dimension
  
  Recommendation: Re-embed with nomic-embed-text-v1.5 (768-dim) using matryoshka for flexibility.
  ```

#### Scenario: Re-embed collection with new model
- **GIVEN** qdrant_ecosystem has 1,344 points with 3584-dim vectors
- **WHEN** re-embedding script runs with nomic-embed-text-v1.5, matryoshka_dim=768
- **THEN** original collection is backed up to qdrant_ecosystem_backup_3584dim
- **AND** new collection qdrant_ecosystem is created with 768-dim vectors
- **AND** all points are re-embedded using nomic-embed-text-v1.5
- **AND** metadata is preserved (subdirectory, source_file, source_path)
- **AND** indexed_fields are recreated
- **AND** progress is logged: "Re-embedded 500/1344 points (37.2%)"

#### Scenario: Verify re-embedding quality
- **GIVEN** collection has been re-embedded
- **WHEN** quality check runs with 100 test queries
- **THEN** recall@10 is ≥0.95 compared to original embeddings
- **AND** search latency is <100ms at p95
- **AND** memory usage is reduced (768-dim vs 3584-dim = ~4.6x smaller)

## MODIFIED Requirements

### Requirement: EmbeddingGenerator Configuration (from src/ingestion/embedder.py)

The `EmbeddingGenerator` class SHALL correctly configure nomic-embed-text-v1.5 with accurate dimensions and matryoshka support.

#### Scenario: Fix model_configs dictionary
- **GIVEN** EmbeddingGenerator initialization
- **WHEN** model_configs is defined
- **THEN** configuration for nomic models is:
  ```python
  "nomic-ai/nomic-embed-text-v1.5": {
      "dimensions": 768,  # Full matryoshka dimension
      "matryoshka_dims": [64, 128, 256, 512, 768],
      "max_tokens": 8192,  # Model limit (but use 512 for optimal accuracy)
      "optimal_tokens": 512,
      "distance_metric": "Cosine",
      "requires_normalization": True,
      "task_prefixes": {
          "search_query": "search_query: ",
          "search_document": "search_document: "
      }
  }
  ```
- **AND** deprecated reference to "nomic-ai/nomic-embed-code" logs warning: "nomic-embed-code (7B) is not supported, use nomic-embed-text-v1.5"

### Requirement: ChunkingConfig for Code (from src/ingestion/chunker.py)

The `ChunkingConfig` class SHALL optimize chunking for code embeddings with proper token limits.

#### Scenario: Create code-optimized chunking config
- **GIVEN** user is processing code files
- **WHEN** ChunkingConfig.for_code_embeddings() factory method is called
- **THEN** config is created with:
  - chunk_size: 1024 chars (≈512 tokens for code)
  - chunk_overlap: 100 chars (≈50 tokens)
  - max_chunk_size: 2048 chars (≈1024 tokens, hard limit)
  - max_tokens: 512 (optimal for nomic-embed-text-v1.5)
  - use_semantic_splitting: True (respect function boundaries)
  - preserve_structure: True (keep class/function hierarchy)
  - tokenizer: "nomic-ai/nomic-embed-text-v1.5"

#### Scenario: Validate chunk token count
- **GIVEN** chunk with 600 tokens
- **WHEN** validation runs
- **THEN** warning is logged: "Chunk exceeds optimal token limit (600 > 512), may affect embedding quality"
- **AND** chunk is split into 2 chunks with 50 token overlap
- **AND** both chunks reference original chunk_id in metadata

### Requirement: QdrantCollectionConfig Vector Dimension (from specs/qdrant-unified-config)

The `QdrantCollectionConfig.for_code_embeddings()` factory SHALL use correct 768-dim default for nomic-embed-text-v1.5.

#### Scenario: Fix factory method for code embeddings
- **GIVEN** user calls QdrantCollectionConfig.for_code_embeddings(collection_name="my_code")
- **WHEN** factory creates config
- **THEN** vector_size is set to 768 (not 3584)
- **AND** distance is "Cosine"
- **AND** model_name is "nomic-ai/nomic-embed-text-v1.5"
- **AND** matryoshka_dim is 768 (default to full dimension)
- **AND** hnsw_m is 16, hnsw_ef_construct is 100 (optimized for code search)
- **AND** quantization is enabled (int8, quantile=0.99)

## REMOVED Requirements

### Requirement: nomic-embed-code Model Support (INCORRECT)

The system SHALL NOT support `nomic-ai/nomic-embed-code` (7B parameter model) as it is incompatible with CPU inference and lacks matryoshka dimensions.

#### Scenario: Reject nomic-embed-code configuration
- **GIVEN** user attempts to configure model_name="nomic-ai/nomic-embed-code"
- **WHEN** validation runs
- **THEN** ValidationError is raised: "nomic-embed-code (7B params) is not supported. Use nomic-embed-text-v1.5 (137M params) which supports CPU inference and matryoshka dimensions (64-768)."
- **AND** migration guide is provided

## Testing & Validation

### Test 1: Dimension Consistency Check
```python
from src.config.jina_provider import SentenceTransformerEmbedder, EmbedderConfig
from qdrant_client import QdrantClient

# Initialize embedder
embedder = SentenceTransformerEmbedder(
    EmbedderConfig(model_name="nomic-ai/nomic-embed-text-v1.5")
)

# Generate embedding
vec = await embedder.embed_texts(["test code snippet"])
assert len(vec[0]) == 768, f"Expected 768-dim, got {len(vec[0])}"

# Check collection
client = QdrantClient(host="localhost", port=6333)
info = client.get_collection("qdrant_ecosystem")
assert info.config.params.vectors.size == 768, "Collection must be 768-dim for nomic-embed-text-v1.5"
```

### Test 2: Matryoshka Dimension Truncation
```python
# Full 768-dim embedding
vec_768 = await embedder.embed_texts(["test"], matryoshka_dim=768)

# Truncated to 256-dim
vec_256 = vec_768[0][:256]

# Search with 256-dim (collection must support)
results = store.search(query_embedding=vec_256, limit=10)
assert len(results) > 0, "Matryoshka search should work"
```

### Test 3: Code Chunking Validation
```python
from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig

config = ChunkingConfig.for_code_embeddings()
chunker = DoclingHybridChunker(config)

code = '''
def factorial(n):
    """Calculate factorial of n"""
    return 1 if n == 0 else n * factorial(n-1)

def fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

chunks = chunker.chunk_text(code, metadata={"file": "math.py"})

# Verify each function is a separate chunk
assert len(chunks) == 2, "Should have 2 chunks (one per function)"
assert all(chunk.token_count <= 512 for chunk in chunks), "Chunks must be ≤512 tokens"
assert "factorial" in chunks[0].content
assert "fibonacci" in chunks[1].content
```

## Migration Impact

**CRITICAL**: This spec identifies a **breaking issue** that will cause search failures:

1. **Immediate Action Required**: Verify qdrant_ecosystem collection dimension
   - If 3584-dim: Must re-embed with nomic-embed-text-v1.5 (768-dim) or find model that produces 3584-dim
   - If 768-dim: Update all references from 3584 to 768

2. **Re-embedding Downtime**: Re-embedding 1,344 documents will take ~5-10 minutes

3. **Model Clarification**: Update all documentation to clearly state:
   - ✅ **USE**: `nomic-ai/nomic-embed-text-v1.5` (768-dim, matryoshka, CPU-friendly)
   - ❌ **DON'T USE**: `nomic-ai/nomic-embed-code` (7B params, 3584-dim, GPU-only)
