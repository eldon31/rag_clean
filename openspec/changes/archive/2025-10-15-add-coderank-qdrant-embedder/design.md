# Design: CodeRank Qdrant Ecosystem Embedding Pipeline

## Context

The `output/qdrant_ecosystem` directory contains pre-chunked JSON files from 6 subdirectories representing different Qdrant-related documentation sources. We need a Kaggle-optimized embedding script that:

1. Processes all 6 subdirectories under a single `qdrant_ecosystem` collection
2. Uses advanced CodeRank models for better embedding quality
3. Respects Kaggle GPU memory limits (15GB per Tesla T4)
4. Enables subdirectory filtering via metadata for hybrid search

**Stakeholders**: Kaggle users, RAG system developers, Qdrant integration teams

**Constraints**:
- Kaggle 2x Tesla T4 GPUs with 15GB VRAM each
- CodeRank models may be newer/experimental (need fallback)
- Large dataset (~50K chunks estimated across 6 subdirs)
- Must maintain compatibility with existing Qdrant upload scripts

## Goals / Non-Goals

### Goals
✅ Single script that processes all 6 subdirectories in `output/qdrant_ecosystem`
✅ Multi-model support: CodeRankEmbed (code), CodeRankLLM (docs), nomic-embed-code (fallback)
✅ Data parallelism across 2 GPUs with VRAM-aware batching
✅ Subdirectory metadata for filtered search (`metadata.source_subdir`)
✅ Drop-in replacement for `kaggle_embed_docling.py` pattern
✅ JSONL output format compatible with existing upload scripts

### Non-Goals
❌ Real-time embedding (offline batch processing only)
❌ Multi-collection support (single `qdrant_ecosystem` collection)
❌ Reranking or hybrid search (focus on embedding generation)
❌ Auto-upload to Qdrant (separate upload script exists)

## Decisions

### Decision 1: Unified Collection with Subdirectory Metadata

**Why**: Cleaner than creating 6 separate collections (qdrant_client_docs, qdrant_documentation, etc.)

**Implementation**:
```python
metadata = {
    "collection": "qdrant_ecosystem",          # All chunks share this
    "source_subdir": "qdrant_client_docs",     # Filter by subdirectory
    "source": "qdrant_client_docs/_qdrant_qdrant-client_1-overview.md",
    # ... other metadata from JSON
}

chunk_id = f"qdrant_ecosystem:{subdir}:{filename}:chunk:{index}"
# Example: "qdrant_ecosystem:qdrant_client_docs:_qdrant_qdrant-client_1-overview.md:chunk:0"
```

**Alternatives considered**:
- ❌ 6 separate collections: More complex to manage, harder to cross-search
- ❌ Flat structure without subdirs: Loses context, can't filter by source

### Decision 2: Single Proven Model (nomic-embed-code)

**Why**: Consistent embeddings across all content types, battle-tested for code + docs

**Implementation**:
```python
# Use nomic-embed-code for ALL content
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
VECTOR_DIMENSION = 768  # Consistent across all chunks

# Benefits:
# ✅ Proven model (already used successfully in kaggle_embed_docling.py)
# ✅ No dimension mismatches (all vectors 768-dim)
# ✅ Optimized for code AND documentation
# ✅ Smaller memory footprint (6.8GB vs 10GB+)
# ✅ Larger batch sizes = faster processing
```

**Alternatives considered**:
- ❌ Multi-model approach (CodeRankEmbed/CodeRankLLM): May not exist, dimension mismatches, complexity
- ❌ Content-based model selection: Different vector spaces = poor search quality
- ✅ **Chosen**: Single battle-tested model for all content

### Decision 3: Data Parallelism with Memory-Aware Batching

**Why**: Maximize GPU utilization while avoiding OOM errors

**Hardware**: Kaggle 2x Tesla T4 GPUs with **15.83 GB VRAM each** (verified)

**Implementation**:
```python
# Model loading (one model per GPU for data parallelism)
model_gpu0 = SentenceTransformer(EMBEDDING_MODEL, device='cuda:0')
model_gpu1 = SentenceTransformer(EMBEDDING_MODEL, device='cuda:1')

# Conservative VRAM estimate for nomic-embed-code
MODEL_VRAM = 6.8  # GB per model (verified from kaggle_embed_docling.py)

def calculate_batch_size(gpu_vram_gb: float = 15.83) -> int:
    """
    Calculate safe batch size for nomic-embed-code.
    
    Conservative approach:
    - Reserve 2GB buffer for PyTorch overhead, intermediate tensors
    - Estimate 0.15GB per chunk in batch (embeddings + gradients + activations)
    - Clamp to safe range to prevent OOM
    """
    available_vram = gpu_vram_gb - MODEL_VRAM - 2.0  # 2GB safety buffer
    
    # Conservative estimate: 0.15GB per chunk (includes all overhead)
    batch_size = int(available_vram / 0.15)
    
    # Clamp: min 4 (efficiency), max 24 (safety)
    return max(4, min(batch_size, 24))

# Calculation:
# (15.83 - 6.8 - 2.0) / 0.15 = 7.03 / 0.15 = 46 → clamped to 24 ✅
# Peak usage: 6.8 + 2.0 + (24 * 0.15) = 12.4 GB (3.43 GB margin) ✅
```

**Safety Mechanisms**:
1. **2GB buffer**: Accounts for PyTorch CUDA context, intermediate tensors
2. **Conservative per-chunk estimate**: 0.15GB includes embeddings + overhead
3. **Aggressive cache clearing**: `torch.cuda.empty_cache()` every 5 batches
4. **Max batch size cap**: 24 chunks (safe threshold with 3+ GB margin)

**Alternatives considered**:
- ❌ Model parallelism: Slower, more complex, overkill for these models
- ❌ Fixed batch size: May underutilize GPU
- ❌ Larger batches (32+): Unnecessary with 3.4GB safety margin
- ✅ **Chosen**: Adaptive batching with ultra-conservative estimates

### Decision 4: Chunk ID Format

**Why**: Need unique, hierarchical IDs that enable filtering and debugging

**Format**: `{collection}:{subdir}:{filename}:chunk:{index}`

**Examples**:
- `qdrant_ecosystem:qdrant_client_docs:_qdrant_qdrant-client_1-overview.md:chunk:0`
- `qdrant_ecosystem:qdrant_documentation:_documentation_advanced-tutorials_code-search.md:chunk:5`

**Benefits**:
- Globally unique (SHA-256 hash converted to int for Qdrant)
- Hierarchical (can extract collection/subdir from ID string)
- Debuggable (human-readable component structure)

**Alternatives considered**:
- ❌ UUID: Not reproducible, no semantic meaning
- ❌ Sequential integers: Not unique across reruns
- ✅ **Chosen**: Hierarchical hash-based IDs

### Decision 5: Reranking as Future Enhancement

**Why**: Keep this script focused on embedding generation, add reranking later

**Implementation** (separate helper script, future work):
```python
# After Qdrant search (NOT in embedding script)
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
top_k_results = qdrant_client.search(query_vector, limit=100)
reranked_results = reranker.rank(query, [r.payload['text'] for r in top_k_results])
final_results = reranked_results[:10]  # Top 10 after reranking
```

**Benefits**:
- ✅ 2-stage retrieval: Fast Qdrant search → Accurate reranking
- ✅ Separation of concerns: Embedding script stays simple
- ✅ Optional upgrade: Users can add reranking when needed
- ✅ No embedding dimension issues: Reranking works with any embeddings

**Alternatives considered**:
- ❌ Embed reranking in this script: Scope creep, complexity
- ❌ Skip reranking entirely: Leaves no upgrade path
- ✅ **Chosen**: Document as future enhancement, separate script

## Risks / Trade-offs

### Risk 1: CodeRank Models May Be Unavailable
**Impact**: Script fails if models not on HuggingFace Hub
**Mitigation**: 
- Implement fallback to nomic-embed-code
- Log warning when falling back
- Test availability before full run

### Risk 2: GPU Out-of-Memory Errors
**Impact**: Script crashes mid-processing, lose progress
**Mitigation**: 
- **Ultra-conservative batch sizing**: 2GB safety buffer + 0.15GB per chunk estimate
- **Verified hardware specs**: 15.83GB VRAM per Tesla T4 (exact measurements)
- **Max batch size cap**: 24 chunks (tested safe limit)
- **Aggressive cache clearing**: `torch.cuda.empty_cache()` every 5 batches
- **Checkpoint progress**: Save to JSONL incrementally (auto-resume capability)
- **OOM detection**: Catch `torch.cuda.OutOfMemoryError` and reduce batch size by 25%### Risk 3: Processing Time on Kaggle
**Impact**: May exceed Kaggle's 9-hour session limit
**Mitigation**:
- Estimate: 50K chunks × 0.05 sec/chunk = 2500 sec = 42 min (well under limit)
- Add progress reporting with ETA
- Support resume from checkpoint if needed

### Risk 4: Embedding Dimension Mismatch
**Impact**: CodeRank models may have different dimensions than nomic-embed-code
**Mitigation**:
- Store model name + dimension in metadata
- Validate all embeddings have same dimension before upload
- Separate collections if mixing dimensions is unavoidable

## Migration Plan

### Phase 1: Development (Local Testing)
1. Create script based on `kaggle_embed_docling.py`
2. Test with sample data (10 chunks per subdirectory)
3. Validate output format matches existing upload scripts

### Phase 2: Kaggle Dry Run
1. Upload sample dataset to Kaggle
2. Run script with CodeRank models (verify availability)
3. Test fallback to nomic-embed-code
4. Measure processing time and memory usage

### Phase 3: Full Production Run
1. Upload full `output/qdrant_ecosystem` to Kaggle dataset
2. Run script with optimized batch sizes
3. Download embeddings JSONL file
4. Validate with existing upload scripts

### Rollback Plan
- If CodeRank models fail: Use nomic-embed-code (proven stable)
- If script fails: Revert to manual processing per subdirectory
- If embeddings corrupt: Re-run with validated configuration

## Open Questions

1. **CodeRank Model Dimensions**: Need to verify actual dimensions (assumed 768 or 1024, may differ)
   - **Resolution**: Research HuggingFace model cards or test load
   
2. **Optimal Batch Size**: Conservative estimate may be too slow
   - **Resolution**: Run benchmark on Kaggle with different batch sizes
   
3. **Checkpoint Strategy**: Should we save progress every N chunks?
   - **Resolution**: Implement simple JSONL append (auto-resume capability)

4. **Model Selection Heuristics**: Should we use content analysis beyond file extension?
   - **Resolution**: Start simple (file extension only), enhance later if needed
