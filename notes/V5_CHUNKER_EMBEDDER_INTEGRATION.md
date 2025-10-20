# V5 Chunker-Embedder Integration Guide
**Ensuring Chunker Compatibility with Jina Code 1.5B Model Parameters**

**Date**: 2025-10-20  
**Purpose**: Define how chunker references embedding model parameters to prevent token limit issues

---

## Problem Statement

**Issue**: Chunker must respect the target embedding model's token limits to avoid:
- Truncated embeddings (context loss)
- Model errors (exceeds max_tokens)
- Inconsistent chunk sizes across the pipeline

**Solution**: Chunker reads model configuration and adjusts chunk sizes accordingly.

---

## Model Parameters Reference

### Jina Code 1.5B Configuration

```python
# From processor/kaggle_ultimate_embedder_v4.py line 127-135
"jina-code-embeddings-1.5b": ModelConfig(
    name="jina-code-embeddings-1.5b",
    hf_model_id="jinaai/jina-code-embeddings-1.5b",
    vector_dim=1536,           # Output dimension
    max_tokens=32768,          # CRITICAL: Maximum input tokens
    query_prefix="Encode this code snippet for semantic retrieval: ",
    recommended_batch_size=16,
    memory_efficient=True
)
```

**Key Parameters for Chunking**:
- `max_tokens=32768` - Maximum context window (extremely large)
- `vector_dim=1536` - Output embedding size
- Token estimation: ~4 characters per token (average)

---

## Chunker Integration Strategy

### Approach 1: Model-Aware Chunking (Recommended)

**Implementation**: Chunker queries embedder for model config before chunking

```python
# In enhanced_ultimate_chunker_v5.py

class EnhancedUltimateChunkerV5:
    """V5 Chunker with model-aware token limits."""
    
    def __init__(
        self,
        target_model: str = "jina-code-embeddings-1.5b",
        chunk_size_tokens: Optional[int] = None,  # Auto-detect from model
        chunk_overlap_tokens: Optional[int] = None,  # Auto-detect
        safety_margin: float = 0.8,  # Use 80% of max_tokens
        **kwargs
    ):
        """
        Initialize chunker with target embedding model awareness.
        
        Args:
            target_model: Name of target embedding model
            chunk_size_tokens: Override chunk size (if None, auto-detect)
            chunk_overlap_tokens: Override overlap (if None, auto-detect)
            safety_margin: Safety factor (0.8 = use 80% of max_tokens)
        """
        
        # Import model config from embedder
        from processor.kaggle_ultimate_embedder_v4 import KAGGLE_OPTIMIZED_MODELS
        
        if target_model not in KAGGLE_OPTIMIZED_MODELS:
            raise ValueError(f"Unknown target model: {target_model}")
        
        self.target_model = target_model
        self.model_config = KAGGLE_OPTIMIZED_MODELS[target_model]
        
        # Calculate optimal chunk size from model's max_tokens
        max_tokens = self.model_config.max_tokens
        
        if chunk_size_tokens is None:
            # Use safety margin to avoid edge cases
            self.chunk_size_tokens = int(max_tokens * safety_margin)
        else:
            # Validate user-provided chunk size
            if chunk_size_tokens > max_tokens:
                raise ValueError(
                    f"chunk_size_tokens ({chunk_size_tokens}) exceeds "
                    f"model max_tokens ({max_tokens})"
                )
            self.chunk_size_tokens = chunk_size_tokens
        
        if chunk_overlap_tokens is None:
            # Default overlap: 10% of chunk size
            self.chunk_overlap_tokens = int(self.chunk_size_tokens * 0.1)
        else:
            self.chunk_overlap_tokens = chunk_overlap_tokens
        
        # Convert tokens to characters (rough estimation)
        # Jina models use ~4 chars per token average
        self.chunk_size_chars = self.chunk_size_tokens * 4
        self.chunk_overlap_chars = self.chunk_overlap_tokens * 4
        
        # Store model info in metadata
        self.model_metadata = {
            "target_model": target_model,
            "model_hf_id": self.model_config.hf_model_id,
            "model_max_tokens": max_tokens,
            "chunk_size_tokens": self.chunk_size_tokens,
            "chunk_overlap_tokens": self.chunk_overlap_tokens,
            "safety_margin": safety_margin,
            "embedding_dimension": self.model_config.vector_dim
        }
        
        print(f"✓ Chunker initialized for {target_model}")
        print(f"  Model max tokens: {max_tokens:,}")
        print(f"  Chunk size: {self.chunk_size_tokens:,} tokens "
              f"(~{self.chunk_size_chars:,} chars)")
        print(f"  Chunk overlap: {self.chunk_overlap_tokens:,} tokens "
              f"(~{self.chunk_overlap_chars:,} chars)")
```

### Usage Example

```python
# Chunker automatically configures for Jina Code 1.5B
chunker = EnhancedUltimateChunkerV5(
    target_model="jina-code-embeddings-1.5b",  # 32768 tokens max
    safety_margin=0.8  # Use 26,214 tokens per chunk (80% of max)
)

# Alternatively, use different model
chunker = EnhancedUltimateChunkerV5(
    target_model="bge-m3",  # 8192 tokens max
    safety_margin=0.9  # Use 7,372 tokens per chunk
)
```

---

## Metadata Enrichment

### Model-Aware Metadata

Each chunk's metadata should include model compatibility info:

```python
def _enrich_chunk_metadata(
    self,
    chunk: Dict,
    docling_doc: Optional[DoclingDocument]
) -> Dict:
    """Add V5 metadata with model compatibility info."""
    
    metadata = chunk.get("metadata", {})
    
    # Add model-specific metadata
    metadata.update({
        # Model compatibility
        "target_model": self.target_model,
        "target_model_max_tokens": self.model_config.max_tokens,
        "embedding_dimension": self.model_config.vector_dim,
        
        # Token counts (for validation)
        "chunk_size_tokens": self.chunk_size_tokens,
        "estimated_tokens": self._estimate_tokens(chunk["text"]),
        
        # Safety checks
        "within_token_limit": True,  # Validate before embedding
        "chunker_version": "v5",
        "model_aware_chunking": True
    })
    
    # Validate token count doesn't exceed model max
    estimated_tokens = metadata["estimated_tokens"]
    if estimated_tokens > self.model_config.max_tokens:
        metadata["within_token_limit"] = False
        metadata["token_overflow"] = estimated_tokens - self.model_config.max_tokens
        
        # Log warning
        print(f"⚠️  Chunk exceeds model token limit: "
              f"{estimated_tokens} > {self.model_config.max_tokens}")
    
    return metadata

def _estimate_tokens(self, text: str) -> int:
    """Estimate token count (4 chars per token average for Jina models)."""
    return len(text) // 4
```

---

## Chunk Size Validation

### Pre-Embedding Validation

Before generating embeddings, validate all chunks:

```python
# In UltimateKaggleEmbedderV4

def validate_chunks_for_model(
    self,
    chunks: List[Dict]
) -> Dict[str, Any]:
    """
    Validate chunks are compatible with target embedding model.
    
    Returns:
        {
            "valid_chunks": int,
            "invalid_chunks": int,
            "max_tokens_exceeded": List[int],  # Chunk indices
            "validation_passed": bool
        }
    """
    
    max_tokens = self.model_config.max_tokens
    invalid_chunks = []
    
    for i, chunk in enumerate(chunks):
        metadata = chunk.get("metadata", {})
        estimated_tokens = metadata.get("estimated_tokens", 0)
        
        if estimated_tokens > max_tokens:
            invalid_chunks.append(i)
    
    validation = {
        "valid_chunks": len(chunks) - len(invalid_chunks),
        "invalid_chunks": len(invalid_chunks),
        "max_tokens_exceeded": invalid_chunks,
        "validation_passed": len(invalid_chunks) == 0,
        "model_max_tokens": max_tokens
    }
    
    if not validation["validation_passed"]:
        print(f"⚠️  Validation failed: {len(invalid_chunks)} chunks exceed "
              f"{max_tokens} token limit")
        print(f"   Chunk indices: {invalid_chunks[:10]}...")  # Show first 10
    else:
        print(f"✓ Validation passed: All {len(chunks)} chunks within token limit")
    
    return validation
```

---

## Complete Pipeline Integration

### End-to-End Flow with Model Awareness

```python
# Step 1: Initialize chunker with target model
from processor.enhanced_ultimate_chunker_v5 import EnhancedUltimateChunkerV5

chunker = EnhancedUltimateChunkerV5(
    target_model="jina-code-embeddings-1.5b",  # CRITICAL: Match embedder model
    use_docling=True,
    use_tree_sitter=True,
    use_semchunk=True,
    safety_margin=0.8  # 26,214 tokens per chunk
)

# Step 2: Chunk documents
chunks = chunker.chunk_documents(
    file_paths=["docs/api.md", "docs/tutorial.md"],
    output_dir="Chunked/v5_output"
)

print(f"Generated {len(chunks)} chunks")
print(f"Chunk size: {chunker.chunk_size_tokens:,} tokens")

# Step 3: Initialize embedder with SAME model
from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",  # MUST match chunker target_model
    companion_dense_models=["bge-m3", "nomic-coderank", "qdrant-minilm-onnx"]
)

# Step 4: Load chunks and validate
embedder.load_chunks_from_processing("Chunked/v5_output")

# Validate chunks before embedding
validation = embedder.validate_chunks_for_model(embedder.chunks_metadata)

if not validation["validation_passed"]:
    raise ValueError(
        f"Chunks validation failed: {validation['invalid_chunks']} chunks "
        f"exceed {validation['model_max_tokens']} token limit. "
        f"Re-chunk with smaller chunk_size_tokens."
    )

# Step 5: Generate embeddings (safe - all chunks validated)
results = embedder.generate_embeddings_kaggle_optimized()

# Step 6: Export for Qdrant
exported = embedder.export_for_local_qdrant()
```

---

## Configuration Examples

### Example 1: Jina Code 1.5B (Large Context)

```python
# Maximum context window: 32,768 tokens
chunker = EnhancedUltimateChunkerV5(
    target_model="jina-code-embeddings-1.5b",
    safety_margin=0.8  # 26,214 tokens per chunk
)

# Result:
# - Chunk size: ~26,214 tokens (~104,856 characters)
# - Can handle entire large files in single chunks
# - Ideal for: API documentation, long tutorials, codebases
```

### Example 2: BGE-M3 (Medium Context)

```python
# Maximum context window: 8,192 tokens
chunker = EnhancedUltimateChunkerV5(
    target_model="bge-m3",
    safety_margin=0.9  # 7,372 tokens per chunk
)

# Result:
# - Chunk size: ~7,372 tokens (~29,488 characters)
# - Standard chunking for most documents
# - Ideal for: General documentation, articles
```

### Example 3: All MiniLM (Small Context)

```python
# Maximum context window: 256 tokens
chunker = EnhancedUltimateChunkerV5(
    target_model="all-miniLM-l6",
    safety_margin=0.9  # 230 tokens per chunk
)

# Result:
# - Chunk size: ~230 tokens (~920 characters)
# - Fine-grained chunking
# - Ideal for: Sentence-level retrieval, Q&A
```

---

## Safety Mechanisms

### 1. Token Limit Validation

```python
# Automatic validation before embedding
if chunk_tokens > model_max_tokens:
    raise TokenLimitExceeded(
        f"Chunk {chunk_id} has {chunk_tokens} tokens, "
        f"exceeds model limit of {model_max_tokens}"
    )
```

### 2. Automatic Chunk Splitting

```python
# If chunk exceeds limit, automatically split
if chunk_tokens > model_max_tokens:
    sub_chunks = chunker.split_oversized_chunk(
        chunk,
        max_tokens=model_max_tokens
    )
    chunks.extend(sub_chunks)
```

### 3. Model Mismatch Detection

```python
# Detect if chunker and embedder use different models
if chunker.target_model != embedder.model_name:
    print(f"⚠️  WARNING: Model mismatch detected!")
    print(f"   Chunker: {chunker.target_model} "
          f"(max {chunker.model_config.max_tokens} tokens)")
    print(f"   Embedder: {embedder.model_name} "
          f"(max {embedder.model_config.max_tokens} tokens)")
    
    # Check if compatible
    if embedder.model_config.max_tokens < chunker.chunk_size_tokens:
        raise ValueError(
            "Embedder model cannot handle chunks from this chunker. "
            "Re-chunk with smaller chunk_size_tokens or use larger embedder model."
        )
```

---

## Recommended Configurations

### Production Setup (Jina Code 1.5B)

```python
# Chunker configuration
chunker = EnhancedUltimateChunkerV5(
    target_model="jina-code-embeddings-1.5b",
    chunk_size_tokens=24000,  # Explicit (below 32768 max)
    chunk_overlap_tokens=2400,  # 10% overlap
    safety_margin=0.8,
    use_docling=True,
    use_tree_sitter=True,
    use_semchunk=True
)

# Embedder configuration (matching model)
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",  # MUST match
    companion_dense_models=["bge-m3", "nomic-coderank"],
    gpu_config=KaggleGPUConfig(
        base_batch_size=16,  # Jina recommended batch size
        dynamic_batching=True
    )
)
```

### Fast Inference Setup (Qdrant ONNX)

```python
# Chunker for smaller context model
chunker = EnhancedUltimateChunkerV5(
    target_model="qdrant-minilm-onnx",  # 256 tokens max
    chunk_size_tokens=230,
    chunk_overlap_tokens=25,
    safety_margin=0.9
)

# Fast ONNX embedder
embedder = UltimateKaggleEmbedderV4(
    model_name="qdrant-minilm-onnx",  # MUST match
    gpu_config=KaggleGPUConfig(
        backend="onnx",  # ONNX optimization
        base_batch_size=128  # Large batch for small model
    )
)
```

---

## Summary

### Critical Integration Points

1. **Chunker MUST reference target embedding model's `max_tokens`**
   - Location: `KAGGLE_OPTIMIZED_MODELS` in `kaggle_ultimate_embedder_v4.py`
   - Parameter: `model_config.max_tokens`

2. **Chunk size MUST be < model's max_tokens**
   - Use safety margin (0.8-0.9) to avoid edge cases
   - Validate before embedding

3. **Metadata MUST include model compatibility info**
   - `target_model`, `target_model_max_tokens`, `estimated_tokens`
   - Enables validation and debugging

4. **Chunker and embedder MUST use same model name**
   - Prevents token limit mismatches
   - Ensures pipeline consistency

### Files to Update

1. **processor/enhanced_ultimate_chunker_v5.py** (NEW)
   - Add model-aware initialization
   - Reference `KAGGLE_OPTIMIZED_MODELS` from embedder
   - Validate chunk sizes against model limits

2. **processor/kaggle_ultimate_embedder_v4.py** (ENHANCE)
   - Add `validate_chunks_for_model()` method
   - Add pre-embedding validation
   - Add model mismatch detection

**Ready for implementation in Code mode**.