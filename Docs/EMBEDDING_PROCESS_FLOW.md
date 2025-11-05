# Embedding Process Flow - Component Usage

This document explains when and how each component (Dense, Sparse/SPLADE, Reranker, Cross-Encoder) is used during the embedding generation and retrieval process.

## Overview

The embedding system uses a **3-stage pipeline**:

1. **Dense Embedding Generation** (Always)
2. **Sparse Vector Generation** (Optional, if enabled)
3. **Reranking** (Optional, at search/retrieval time)

---

## Stage 1: Dense Embedding Generation (Always Active)

### When Used

- **Always** - This is the core embedding stage
- Executed during: `embed_collections_v7.py` script, batch processing

### What Happens

1. **Primary Model** generates dense embeddings (e.g., 384D, 768D, 1024D vectors)
2. **Ensemble Models** (if enabled on GPU) generate additional dense embeddings
3. Embeddings are normalized and converted to numpy arrays

### Models Used

- **SentenceTransformer** class models:
  - `jina-code-embeddings-1.5b` (1024D)
  - `bge-m3` (1024D)
  - `qwen3-embedding-0.6b` (1024D)
  - `all-miniLM-l6` (384D)
  - `nomic-coderank` (768D)
  - `jina-embeddings-v4` (1024D)

### Code Location

- `processor/ultimate_embedder/core.py`: `_call_encode()`
- `processor/ultimate_embedder/batch_runner.py`: `generate_ensemble_embeddings()`

### Output

- Dense vector arrays stored in memory and exported to Qdrant format
- Saved as `.npy` files and included in `processing_summary.json`

---

## Stage 2: Sparse Vector Generation (Optional)

### When Used

- **Only if `enable_sparse=True`** (default: enabled)
- Can be disabled with `--disable-sparse` flag
- Executed **in parallel** with dense embedding generation

### What Happens

1. **SparseEncoder** (SPLADE) model generates sparse term-weighted vectors
2. Sparse vectors use ~30,522 dimensions (vocabulary size)
3. Typically >99% sparse (only ~100-200 non-zero weights per text)
4. Provides lexical/keyword-based retrieval capability

### Models Used

- **SparseEncoder** class models:
  - `splade` → `naver/splade_v2_distil` (default)
  - Uses MLM (Masked Language Model) + SpladePooling architecture

### Key Difference from Dense

- **Class**: `SparseEncoder` (not `SentenceTransformer`)
- **Method**: `.encode()` but with different signature
- **Output**: Sparse CSR tensors/arrays instead of dense vectors
- **Purpose**: Keyword/lexical matching (complements semantic dense vectors)

### Code Location

- `processor/ultimate_embedder/model_manager.py`: `initialize_sparse_models()`
- `processor/ultimate_embedder/sparse_pipeline.py`: sparse generation logic

### Output

- Sparse vectors exported alongside dense embeddings
- Stored in Qdrant's sparse vector format
- Enables hybrid search (dense + sparse fusion)

---

## Stage 3: Reranking (At Search/Retrieval Time)

### When Used

- **At retrieval/search time**, not during embedding generation
- Only if `enable_rerank=True` (default: enabled)
- Can be disabled with `--disable-rerank` flag

### What Happens

1. **Initial Retrieval**: Fetch top-N candidates using dense (and optionally sparse) vectors
   - Default: 100 candidates (`--rerank-candidates`)
2. **Reranking**: CrossEncoder scores each (query, candidate) pair
3. **Top-K Selection**: Return top-20 (default, `--rerank-top-k`) highest-scored results

### Models Used (Cross-Encoders)

- **CrossEncoder** class models:
  - `jinaai/jina-reranker-v3` (default, uses AutoModel)
  - `Alibaba-NLP/gte-multilingual-reranker-base` (fallback)
  - `BAAI/bge-reranker-v2-m3` (fallback)

### Key Difference from Embedders

- **Class**: Uses `AutoModel` (for Jina) or `CrossEncoder` class
- **Input**: (query, document) **pairs** not individual texts
- **Output**: Relevance scores (not embeddings)
- **Purpose**: Re-score and re-order initial retrieval results

### Code Location

- `processor/ultimate_embedder/rerank_pipeline.py`: `create_reranker_from_spec()`
- `processor/ultimate_embedder/cross_encoder_executor.py`: batch execution
- `processor/ultimate_embedder/core.py`: `search_with_reranking()`

### Configuration

```python
# Default settings (embed_collections_v7.py)
DEFAULT_RERANK_MODEL = "jinaai/jina-reranker-v3"
DEFAULT_RERANK_CANDIDATES = 100  # Initial retrieval pool
DEFAULT_RERANK_TOP_K = 20        # Final results after reranking
```

---

## Complete Workflow Example

### Embedding Generation (Kaggle)

```bash
python scripts/embed_collections_v7.py \
  --chunked-dir /kaggle/working/Chunked \
  --output-dir /kaggle/working/Embeddings \
  --rerank-candidates 100 \
  --rerank-top-k 20
```

**What Happens:**

1. ✅ **Dense Stage**: Generate embeddings using ensemble models
2. ✅ **Sparse Stage**: Generate SPLADE sparse vectors (parallel)
3. ⏭️ **Reranking Stage**: Skipped (only loads reranker model for validation)

**Output Files:**

- `dense_vectors.npy` - Dense embeddings
- `sparse_indices.npy` - Sparse vector indices
- `sparse_values.npy` - Sparse vector weights
- `processing_summary.json` - Metadata

### Retrieval/Search (Local Qdrant)

```python
# After importing embeddings to Qdrant
embedder = UltimateKaggleEmbedderV4(...)
results = embedder.search_with_reranking(
    query="What is SPLADE?",
    top_k=20,
    initial_candidates=100
)
```

**What Happens:**

1. ✅ **Dense Retrieval**: Fetch 100 candidates using vector similarity
2. ✅ **Sparse Retrieval**: (Optional) Fuse sparse scores
3. ✅ **Reranking Stage**: CrossEncoder scores 100 candidates
4. ✅ **Return**: Top 20 highest-scored results

---

## Summary Table

| Component                 | Stage      | When Used  | Input              | Output                     | Class                        |
| ------------------------- | ---------- | ---------- | ------------------ | -------------------------- | ---------------------------- |
| **Dense Embeddings**      | Generation | Always     | Text chunks        | Dense vectors (384D-1024D) | `SentenceTransformer`        |
| **Sparse/SPLADE**         | Generation | If enabled | Text chunks        | Sparse vectors (~30K dim)  | `SparseEncoder`              |
| **Reranker/CrossEncoder** | Retrieval  | If enabled | (query, doc) pairs | Relevance scores           | `CrossEncoder` / `AutoModel` |

---

## Key Differences Between Models

### SentenceTransformer (Dense)

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("bge-m3")
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
# Output: Dense numpy array [N, 1024]
```

### SparseEncoder (SPLADE)

```python
from sentence_transformers import SparseEncoder
model = SparseEncoder("naver/splade_v2_distil")
sparse_embeddings = model.encode(texts)
# Output: Sparse CSR matrix [N, ~30522] with ~99% zeros
```

### CrossEncoder (Reranker)

```python
from sentence_transformers import CrossEncoder
model = CrossEncoder("BAAI/bge-reranker-v2-m3")
scores = model.predict([("query", "doc1"), ("query", "doc2")])
# Output: Relevance scores [0.85, 0.42]
```

### AutoModel (Jina Reranker)

```python
from transformers import AutoModel
model = AutoModel.from_pretrained(
    "jinaai/jina-reranker-v3",
    dtype="auto",
    trust_remote_code=True
)
# Custom scoring logic required
```

---

## Configuration Flags

### Enable/Disable Components

```bash
# Disable sparse vectors
python scripts/embed_collections_v7.py --disable-sparse

# Disable reranking
python scripts/embed_collections_v7.py --disable-rerank

# Both disabled (dense only)
python scripts/embed_collections_v7.py --disable-sparse --disable-rerank
```

### Adjust Reranking Parameters

```bash
# Larger candidate pool, more final results
python scripts/embed_collections_v7.py \
  --rerank-candidates 200 \
  --rerank-top-k 50
```

---

## Monitoring

The enhanced `ThroughputMonitor` tracks all three stages:

```python
# Example output
[throughput] Dense encoding: 1000 chunks in 45.2s (22.1 chunks/s)
[throughput] Sparse encoding: 1000 chunks in 12.8s (78.1 chunks/s)
[throughput] Reranking: 100 pairs in 3.4s (29.4 pairs/s)
```

Errors in any stage are captured and displayed:

```python
[throughput] Errors:
  - Dense stage: No errors
  - Sparse stage: SPLADE model failed (1 error)
  - Rerank stage: No errors
```
