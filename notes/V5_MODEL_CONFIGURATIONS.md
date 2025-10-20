# V5 Model Configurations
**Qdrant-Optimized Embedding Models**

**Date**: 2025-10-20  
**Purpose**: Comprehensive model registry for V5 chunker/embedder with Qdrant-optimized models

---

## Dense Embedding Models

### Primary Models (Existing V4)

```python
# Add to KAGGLE_OPTIMIZED_MODELS in processor/kaggle_ultimate_embedder_v4.py

KAGGLE_OPTIMIZED_MODELS = {
    # Existing models...
    
    # PRIMARY: Code-optimized
    "jina-code-embeddings-1.5b": ModelConfig(
        name="jina-code-embeddings-1.5b",
        hf_model_id="jinaai/jina-code-embeddings-1.5b",
        vector_dim=1536,
        max_tokens=32768,
        query_prefix="Encode this code snippet for semantic retrieval: ",
        recommended_batch_size=16,
        memory_efficient=True
    ),
    
    # SECONDARY: Multi-modal
    "bge-m3": ModelConfig(
        name="bge-m3",
        hf_model_id="BAAI/bge-m3", 
        vector_dim=1024,
        max_tokens=8192,
        recommended_batch_size=32,
        memory_efficient=True
    ),
    
    # TERTIARY: Code ranking
    "nomic-coderank": ModelConfig(
        name="nomic-coderank",
        hf_model_id="nomic-ai/CodeRankEmbed",
        vector_dim=768,
        max_tokens=2048,
        query_prefix="Represent this query for searching relevant code: ",
        recommended_batch_size=64,
        memory_efficient=True
    ),
}
```

### Qdrant-Optimized Models (NEW for V5)

```python
# ADD these to KAGGLE_OPTIMIZED_MODELS

# Qdrant ONNX-optimized model (ultra-fast inference)
"qdrant-minilm-onnx": ModelConfig(
    name="qdrant-minilm-onnx",
    hf_model_id="Qdrant/all-MiniLM-L6-v2-onnx",
    vector_dim=384,
    max_tokens=256,
    recommended_batch_size=128,  # Large batch for tiny model
    memory_efficient=True,
    # ONNX backend for 2-3x faster inference
    backend="onnx"  # NEW field
),

# Alternative: Regular (non-ONNX) version if ONNX not available
"all-miniLM-l6": ModelConfig(
    name="all-miniLM-l6",
    hf_model_id="sentence-transformers/all-MiniLM-L6-v2",
    vector_dim=384,
    max_tokens=256,
    recommended_batch_size=128,
    memory_efficient=True
),
```

---

## Sparse Embedding Models (NEW for V5)

### BM25-Style Sparse Vectors

```python
# NEW section: SPARSE_MODELS configuration

SPARSE_MODELS = {
    # Qdrant BM25 model (term frequency-based)
    "qdrant-bm25": {
        "name": "qdrant-bm25",
        "hf_model_id": "Qdrant/bm25",
        "type": "bm25",
        "description": "BM25-style term frequency sparse vectors",
        "recommended_batch_size": 64
    },
    
    # Qdrant attention-based sparse model
    "qdrant-minilm-attention": {
        "name": "qdrant-minilm-attention",
        "hf_model_id": "Qdrant/all_miniLM_L6_v2_with_attentions",
        "type": "attention",
        "description": "Attention-based sparse vectors from MiniLM",
        "recommended_batch_size": 64
    }
}
```

### Sparse Vector Usage

```python
from sentence_transformers import SentenceTransformer

# Load sparse models
bm25_model = SentenceTransformer("Qdrant/bm25")
attention_model = SentenceTransformer("Qdrant/all_miniLM_L6_v2_with_attentions")

# Generate sparse vectors
def generate_sparse_vectors(texts: List[str]) -> Dict[str, List[Dict]]:
    """
    Generate multiple types of sparse vectors for hybrid search.
    
    Returns:
        {
            "bm25": [{"indices": [...], "values": [...], "tokens": [...]}, ...],
            "attention": [{"indices": [...], "values": [...], "tokens": [...]}, ...]
        }
    """
    sparse_vectors = {
        "bm25": [],
        "attention": []
    }
    
    for text in texts:
        # BM25 sparse encoding
        bm25_output = bm25_model.encode(
            text,
            convert_to_tensor=False,
            output_value="token_embeddings"
        )
        sparse_vectors["bm25"].append(_process_sparse_output(bm25_output))
        
        # Attention sparse encoding
        attention_output = attention_model.encode(
            text,
            convert_to_tensor=False,
            output_value="token_embeddings"
        )
        sparse_vectors["attention"].append(_process_sparse_output(attention_output))
    
    return sparse_vectors

def _process_sparse_output(sparse_output) -> Dict[str, Any]:
    """Convert model sparse output to Qdrant format."""
    # Extract non-zero indices and values
    # (Implementation depends on model output format)
    
    indices = []  # Token hash indices
    values = []   # Weight values
    tokens = []   # Original tokens
    
    # Process sparse_output to extract indices/values/tokens
    # ...
    
    return {
        "indices": indices,
        "values": values,
        "tokens": tokens
    }
```

---

## Complete V5 Model Registry

### Dense Models Summary

| Model Name | HF Model ID | Dimensions | Max Tokens | Batch Size | Purpose |
|------------|-------------|------------|------------|------------|---------|
| `jina-code-1.5b` | `jinaai/jina-code-embeddings-1.5b` | 1536 | 32768 | 16 | Primary code embedding |
| `bge-m3` | `BAAI/bge-m3` | 1024 | 8192 | 32 | Multi-modal retrieval |
| `nomic-coderank` | `nomic-ai/CodeRankEmbed` | 768 | 2048 | 64 | Code ranking |
| `qdrant-minilm-onnx` | `Qdrant/all-MiniLM-L6-v2-onnx` | 384 | 256 | 128 | Fast ONNX inference |

### Sparse Models Summary

| Model Name | HF Model ID | Type | Batch Size | Purpose |
|------------|-------------|------|------------|---------|
| `qdrant-bm25` | `Qdrant/bm25` | BM25 | 64 | Term frequency sparse |
| `qdrant-minilm-attention` | `Qdrant/all_miniLM_L6_v2_with_attentions` | Attention | 64 | Attention-based sparse |

---

## Qdrant Collection Configuration

### Named Vectors Setup

```python
# Qdrant collection with named dense + sparse vectors

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

# Create collection with named vectors
client.create_collection(
    collection_name="docs_v5_multi",
    vectors_config={
        # Dense vectors (named)
        "jina-code-1.5b": VectorParams(
            size=1536,
            distance=Distance.COSINE,
            on_disk=False
        ),
        "bge-m3": VectorParams(
            size=1024,
            distance=Distance.COSINE,
            on_disk=False
        ),
        "nomic-coderank": VectorParams(
            size=768,
            distance=Distance.COSINE,
            on_disk=False
        ),
        "qdrant-minilm": VectorParams(
            size=384,
            distance=Distance.COSINE,
            on_disk=False
        ),
        
        # Sparse vectors (named)
        "bm25": VectorParams(
            size=0,  # Sparse vector (size determined by vocabulary)
            distance=Distance.DOT,  # Dot product for sparse
            sparse=True,
            modifier="idf"  # IDF weighting
        ),
        "minilm-attention": VectorParams(
            size=0,
            distance=Distance.DOT,
            sparse=True,
            modifier="none"  # Raw attention weights
        )
    },
    
    # HNSW configuration
    hnsw_config={
        "m": 48,
        "ef_construct": 512,
        "full_scan_threshold": 50000
    },
    
    # Quantization (int8 for memory efficiency)
    quantization_config={
        "scalar": {
            "type": "int8",
            "quantile": 0.99,
            "always_ram": True
        }
    }
)
```

### Hybrid Search Example

```python
# Hybrid search: Dense + Sparse fusion

# 1. Dense vector search (primary)
dense_results = client.search(
    collection_name="docs_v5_multi",
    query_vector=("jina-code-1.5b", query_embedding),
    limit=50
)

# 2. Sparse vector search (BM25)
sparse_results = client.search(
    collection_name="docs_v5_multi",
    query_vector=("bm25", sparse_query_vector),
    limit=50
)

# 3. Fusion (combine dense + sparse scores)
# Using Reciprocal Rank Fusion (RRF) or weighted sum
combined_results = fusion_algorithm(dense_results, sparse_results)
```

---

## Implementation Notes

### Adding Qdrant Models to V4 Embedder

**Location**: `processor/kaggle_ultimate_embedder_v4.py`

1. Add Qdrant models to `KAGGLE_OPTIMIZED_MODELS` dict (lines 116-214)
2. Add sparse model support to `SPARSE_MODELS` dict (new section)
3. Update `companion_dense_models` parameter to accept Qdrant models
4. Add sparse vector generation methods

### Backward Compatibility

- V4 interface preserved: existing code works unchanged
- V5 features optional: use `enable_sparse=True` to activate
- Model selection flexible: can use any combination of dense models

### Performance Targets

**Dense Embeddings**:
- Jina Code 1.5B: ~150-200 chunks/sec (T4 x2)
- BGE-M3: ~200-300 chunks/sec
- Nomic CodeRank: ~300-400 chunks/sec
- Qdrant MiniLM ONNX: ~500-800 chunks/sec (ONNX optimized)

**Sparse Embeddings**:
- BM25: ~400-600 chunks/sec
- Attention-based: ~300-500 chunks/sec

**Combined throughput**: ~250-350 chunks/sec (all models active)

---

## Usage Examples

### Example 1: Dense Only (V4 Compatible)

```python
from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    companion_dense_models=["bge-m3", "nomic-coderank"]
)

embedder.load_chunks_from_processing()
embedder.generate_embeddings_kaggle_optimized()
embedder.export_for_local_qdrant()
```

### Example 2: Dense + Sparse (V5 Enhanced)

```python
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    companion_dense_models=[
        "bge-m3", 
        "nomic-coderank", 
        "qdrant-minilm-onnx"  # NEW
    ],
    enable_sparse=True,  # NEW parameter
    sparse_models=["qdrant-bm25", "qdrant-minilm-attention"]  # NEW
)

embedder.load_chunks_from_processing()
results = embedder.generate_embeddings_kaggle_optimized()

# Results now include sparse vectors
print(f"Dense models: {list(embedder.embeddings_by_model.keys())}")
print(f"Sparse vectors: {len(embedder.sparse_vectors)}")

embedder.export_for_local_qdrant()
```

### Example 3: ONNX-Optimized Fast Inference

```python
# Ultra-fast embedding with Qdrant ONNX model
embedder = UltimateKaggleEmbedderV4(
    model_name="qdrant-minilm-onnx",  # ONNX-optimized
    gpu_config=KaggleGPUConfig(
        backend="onnx",  # Force ONNX backend
        base_batch_size=128  # Large batch for small model
    )
)

# Expected: 500-800 chunks/sec on T4 x2
embedder.load_chunks_from_processing()
embedder.generate_embeddings_kaggle_optimized()
```

---

## Migration from V4 to V5

### Step 1: Update Model Registry

Add Qdrant models to `KAGGLE_OPTIMIZED_MODELS` in `kaggle_ultimate_embedder_v4.py`

### Step 2: Add Sparse Support

Create new `SPARSE_MODELS` dict and sparse vector generation methods

### Step 3: Update Export Logic

Modify `_export_qdrant_jsonl()` to include sparse vectors in JSONL output

### Step 4: Test Incrementally

1. Test Qdrant dense model only: `qdrant-minilm-onnx`
2. Test sparse generation: `qdrant-bm25`
3. Test combined: dense + sparse export
4. Test Qdrant upload: named vectors + sparse vectors

---

## Next Steps

1. ✅ Document Qdrant models (this file)
2. ⚠️ Add models to `kaggle_ultimate_embedder_v4.py` (requires Code mode)
3. ⚠️ Implement sparse vector generation (requires Code mode)
4. ⚠️ Update export logic for named + sparse vectors (requires Code mode)
5. ⚠️ Test end-to-end: chunk → embed → export → Qdrant upload

**Ready for Code mode implementation**.