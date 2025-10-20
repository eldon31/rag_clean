# V5 Ensemble Configuration - Final Design

## Date: 2025-01-20

## Overview

V5 is configured for **multi-model ensemble embedding** by default, using **1024D as the standard dimension** across all ensemble models.

## Ensemble Models (All at 1024D)

### 1. jina-code-embeddings-1.5b
- **Native dimension**: 1536D
- **Ensemble dimension**: 1024D (Matryoshka truncation)
- **Specialization**: Code and technical documentation
- **Matryoshka support**: YES (256, 512, 1024, 1536)

### 2. jina-embeddings-v4
- **Native dimension**: 2048D
- **Ensemble dimension**: 1024D (Matryoshka truncation)
- **Specialization**: Long-context general text
- **Matryoshka support**: YES (256, 512, 768, 1024, 2048)

### 3. BAAI/bge-m3
- **Native dimension**: 1024D
- **Ensemble dimension**: 1024D (no truncation needed)
- **Specialization**: Multi-lingual, multi-modal
- **Matryoshka support**: NO (native 1024D)

## Why 1024D for Ensemble?

### Technical Alignment
- **jina-code-1.5b**: 1536D → 1024D (Matryoshka trained, minimal quality loss)
- **jina-v4**: 2048D → 1024D (Matryoshka trained, minimal quality loss)
- **bge-m3**: 1024D native (perfect fit, no truncation)

### Benefits
1. **Uniform Dimension**: All models output same vector size
2. **Ensemble Compatibility**: Can average/combine embeddings
3. **Storage Efficiency**: 33-50% smaller than full dimensions
4. **Speed**: Faster similarity search with 1024D vectors
5. **Matryoshka Quality**: Minimal loss (~2-3%) for Jina models

## Configuration

### Model Registry
```python
# processor/kaggle_ultimate_embedder_v4.py
KAGGLE_OPTIMIZED_MODELS = {
    "jina-code-embeddings-1.5b": ModelConfig(
        vector_dim=1024,  # Ensemble dimension (not 1536D)
    ),
    "jina-embeddings-v4": ModelConfig(
        vector_dim=1024,  # Ensemble dimension (not 2048D)
    ),
    "bge-m3": ModelConfig(
        vector_dim=1024,  # Native dimension
    ),
}
```

### Default Script Configuration
```python
# scripts/embed_collections_v5.py
EMBEDDING_CONFIG = {
    "model": "jina-code-embeddings-1.5b",
    "matryoshka_dim": 1024,  # Ensemble dimension
    "enable_ensemble": True,  # Multi-model enabled
}
```

### Embedder Usage
```python
# Default: Uses registry dimension (1024D)
embedder = KaggleUltimateEmbedderV4("jina-code-embeddings-1.5b")
# Produces 1024D embeddings (not 1536D)

# Override: Use different dimension if needed
embedder = KaggleUltimateEmbedderV4(
    "jina-code-embeddings-1.5b",
    matryoshka_dim=1536  # Override to full dimension
)
```

## Ensemble Workflow

### Phase 1: Document Chunking
```python
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b"
)
chunks = chunker.process_file_smart("document.md")
# Chunks sized for 1024D embeddings
```

### Phase 2: Multi-Model Embedding
```python
embedder = KaggleUltimateEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    enable_ensemble=True,
    ensemble_models=[
        "jina-code-embeddings-1.5b",  # 1024D
        "jina-embeddings-v4",          # 1024D
        "bge-m3"                        # 1024D
    ]
)

# Each chunk gets 3 embeddings, all 1024D
embeddings = embedder.embed_batch([chunk["text"] for chunk in chunks])
# Shape: (num_chunks, 1024)
```

### Phase 3: Storage in Qdrant
```python
# All embeddings are 1024D, stored uniformly
qdrant_client.upsert(
    collection_name="my_collection",
    points=[
        {
            "id": chunk["metadata"]["chunk_id"],
            "vector": embedding,  # 1024D
            "payload": chunk["metadata"]
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]
)
```

---

## Reranker Question: Why Not Used During Embedding?

### Understanding the Two-Stage Retrieval Pipeline

#### Stage 1: Embedding & Retrieval (Fast, Broad)
**Purpose**: Quickly retrieve top-k candidates from millions of documents

**Process**:
1. Query → Embedding (1024D vector)
2. Vector similarity search in Qdrant
3. Retrieve top 100-1000 candidates
4. **Speed**: <100ms for millions of vectors

**Why Embedders (Not Rerankers)**:
- Embedders create **pre-computed vectors** stored in vector DB
- Search is **O(log n)** with HNSW index (very fast)
- Can scale to millions/billions of documents

#### Stage 2: Reranking (Slow, Precise)
**Purpose**: Precisely reorder top-k candidates for best matches

**Process**:
1. Take top 100 candidates from Stage 1
2. Reranker scores each (query, candidate) pair
3. Reorder by reranker scores
4. Return top 10 final results
5. **Speed**: ~1-2 seconds for 100 pairs

**Why NOT Used for Embedding**:
- Rerankers need **both query AND document** (not pre-computable)
- Must score **every pair** at query time (slow)
- Cannot be indexed in vector DB
- Computationally expensive for large collections

### Visual Comparison

```
EMBEDDER (Pre-computed):
Document → [1024D vector] → Stored in Qdrant
                              ↓
Query → [1024D vector] → Fast cosine search → Top 100 candidates
                                               (< 100ms)

RERANKER (Query-time only):
Query + Candidate1 → [score: 0.95]
Query + Candidate2 → [score: 0.87]  } Rerank top 100
Query + Candidate3 → [score: 0.92]  } (~1-2 seconds)
...
Query + Candidate100 → [score: 0.65]
                       ↓
                   Top 10 final results
```

### Why This Design?

#### Embedders (Stage 1):
- **Pre-compute once**: Embed all documents offline
- **Store vectors**: Index in Qdrant for fast search
- **Query-time**: Only embed the query (single vector)
- **Scalability**: Handles millions of documents

#### Rerankers (Stage 2):
- **Query-time only**: Cannot pre-compute (needs query context)
- **Small candidate set**: Only rerank top 100 (not millions)
- **Precision**: Better than embedders for final ranking
- **Trade-off**: Slow but accurate

### Example Workflow

```python
# STAGE 1: Embedding & Retrieval (Fast)
query = "How to implement async functions in Python?"

# Embed query (pre-computed doc embeddings already in Qdrant)
query_embedding = embedder.embed([query])[0]  # 1024D

# Fast vector search
candidates = qdrant_client.search(
    collection_name="code_docs",
    query_vector=query_embedding,
    limit=100  # Top 100 candidates
)
# Time: ~50ms for 1M documents

# STAGE 2: Reranking (Slow but Precise)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Score each (query, candidate) pair
scores = reranker.predict([
    (query, candidate.payload["text"])
    for candidate in candidates
])

# Reorder by reranker scores
final_results = sorted(
    zip(candidates, scores),
    key=lambda x: x[1],
    reverse=True
)[:10]  # Top 10 final
# Time: ~1-2 seconds for 100 pairs

# Total time: ~2 seconds (vs. 100+ seconds if reranking all 1M docs)
```

### Why NOT Embed with Reranker?

**Problem 1: Cannot Pre-compute**
```python
# ❌ WRONG: Reranker needs BOTH query and document
reranker_embedding = reranker.embed(document)  # NO! Doesn't work

# Reranker needs:
score = reranker.predict([(query, document)])  # Pair-based scoring
```

**Problem 2: Cannot Index**
```python
# ❌ WRONG: Cannot store reranker "scores" without query
qdrant_client.upsert(
    vector=reranker_score  # NO! No query at indexing time
)
```

**Problem 3: Too Slow for Millions**
```python
# ❌ WRONG: Reranking 1M documents = 1M forward passes
for doc in million_documents:
    score = reranker.predict([(query, doc)])  # 100+ seconds!

# ✅ CORRECT: Rerank only top 100 candidates
for doc in top_100_candidates:
    score = reranker.predict([(query, doc)])  # 1-2 seconds
```

## Summary

### Ensemble Configuration (FINAL)
- ✅ All models use **1024D** (registry default)
- ✅ **Ensemble enabled** by default
- ✅ Matryoshka truncation for Jina models (minimal quality loss)
- ✅ BGE-M3 native 1024D (no truncation)

### Reranker Usage
- ❌ **NOT used** during embedding phase
- ✅ **USED** in two-stage retrieval:
  1. **Embedder**: Fast retrieval (top 100)
  2. **Reranker**: Precise reordering (final top 10)

### Key Insight
**Embedders** and **Rerankers** serve different purposes:
- **Embedders**: Pre-computed vectors, fast search, scalable
- **Rerankers**: Query-time scoring, slow, precise, small candidate sets

You **cannot** use rerankers for embedding because they require **both query and document** at inference time, making them unsuitable for pre-computed vector search.

---

## Configuration Files

### Updated Registry
- ✅ `processor/kaggle_ultimate_embedder_v4.py` - All ensemble models at 1024D

### Updated Scripts  
- ✅ `scripts/embed_collections_v5.py` - Ensemble enabled, 1024D default

### Documentation
- ✅ `notes/V5_ENSEMBLE_CONFIGURATION.md` - This document
- ⏳ `notes/RERANKER_INTEGRATION_GUIDE.md` - Future: How to add reranking stage

---

**Document Version**: 1.0  
**Status**: ✅ FINAL ENSEMBLE CONFIGURATION  
**Date**: 2025-01-20  
**Author**: V5 Architecture Team