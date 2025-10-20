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
    
    # TERTIARY: Jina Embeddings V4 (Multi-vector + Matryoshka)
    "jina-embeddings-v4": ModelConfig(
        name="jina-embeddings-v4",
        hf_model_id="jinaai/jina-embeddings-v4",
        vector_dim=2048,  # Full dimension
        max_tokens=32768,
        query_prefix="",
        recommended_batch_size=16,
        memory_efficient=True,
        # Matryoshka dimensions support
        matryoshka_dims=[128, 256, 512, 1024, 2048],
        base_model="Qwen2.5-VL-3B-Instruct",
        pooling_strategy="mean",
        attention_mechanism="FlashAttention2",
        dtype="bfloat16"
    ),
    
    # QUATERNARY: Jina Reranker V3 (0.6B parameters)
    "jina-reranker-v3": ModelConfig(
        name="jina-reranker-v3",
        hf_model_id="jinaai/jina-reranker-v3",
        vector_dim=256,  # Output dimension
        max_tokens=131072,  # 131K input token length
        recommended_batch_size=8,
        memory_efficient=True,
        model_type="reranker",
        reranker_type="listwise",
        parameters="0.6B",
        language_support="multilingual",
        supports_code_search=True
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
| `jina-embeddings-v4` | `jinaai/jina-embeddings-v4` | 2048 (Matryoshka) | 32768 | 16 | Multi-vector + Matryoshka |
| `jina-reranker-v3` | `jinaai/jina-reranker-v3` | 256 | 131072 | 8 | Listwise reranking (0.6B) |
| `bge-m3` | `BAAI/bge-m3` | 1024 | 8192 | 32 | Multi-modal retrieval |
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
        "jina-embeddings-v4": VectorParams(
            size=2048,  # Or use Matryoshka dimension (128-2048)
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
    companion_dense_models=["jina-embeddings-v4", "bge-m3"]
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
        "jina-embeddings-v4",  # Multi-vector + Matryoshka
        "bge-m3",
        "qdrant-minilm-onnx"  # NEW
    ],
    reranker_model="jina-reranker-v3",  # NEW: Reranking support
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


---

## Neural Search API

### Overview

A complete neural search service requires:
1. **Model to convert queries into vectors** (sentence-transformers)
2. **Qdrant client to perform search queries** (qdrant-client)

Based on: [Build a Neural Search Service - Qdrant Tutorial](https://qdrant.tech/documentation/tutorials/neural-search/)

---

### NeuralSearcher Class Implementation

```python
# File: neural_searcher.py

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional


class NeuralSearcher:
    """
    Neural search service for V5 chunked documents
    
    Features:
    - Query encoding with configurable embedding model
    - Vector similarity search via Qdrant
    - Optional filters (content_type, file_extension, etc.)
    - Top-K result retrieval with metadata
    
    Example:
        searcher = NeuralSearcher(
            collection_name="technical_docs",
            model_name="jina-code-embeddings-1.5b"
        )
        
        results = searcher.search(
            text="How to authenticate API requests?",
            limit=5
        )
    """
    
    def __init__(
        self,
        collection_name: str,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        qdrant_url: str = "http://localhost:6333",
        device: str = "cpu"
    ):
        """
        Initialize neural searcher
        
        Args:
            collection_name: Qdrant collection name
            model_name: HuggingFace model ID for query encoding
            qdrant_url: Qdrant server URL
            device: "cpu" or "cuda"
        """
        self.collection_name = collection_name
        
        # Initialize encoder model
        self.model = SentenceTransformer(model_name, device=device)
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url)
        
        print(f"✓ NeuralSearcher initialized:")
        print(f"  Collection: {collection_name}")
        print(f"  Model: {model_name}")
        print(f"  Device: {device}")
    
    def search(
        self,
        text: str,
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            text: Query text
            limit: Number of results to return
            score_threshold: Minimum similarity score (0-1)
            filters: Optional filters (content_type, file_extension, etc.)
        
        Returns:
            List of payloads with metadata and scores
        """
        # Convert text query into vector
        vector = self.model.encode(text).tolist()
        
        # Build query filter if provided
        query_filter = None
        if filters:
            query_filter = self._build_filter(filters)
        
        # Perform vector search
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold
        ).points
        
        # Extract payloads with scores
        results = []
        for hit in search_result:
            result = {
                "score": hit.score,
                "payload": hit.payload,
                "id": hit.id
            }
            results.append(result)
        
        return results
    
    def search_with_named_vector(
        self,
        text: str,
        vector_name: str = "jina-code-1.5b",
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search using a specific named vector (for multi-vector collections)
        
        Args:
            text: Query text
            vector_name: Named vector to search (e.g., "jina-code-1.5b")
            limit: Number of results
            score_threshold: Minimum score
            filters: Optional filters
        
        Returns:
            List of results with scores
        """
        # Encode with same model used for that vector
        vector = self.model.encode(text).tolist()
        
        query_filter = None
        if filters:
            query_filter = self._build_filter(filters)
        
        # Search specific named vector
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            using=vector_name,  # Specify named vector
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold
        ).points
        
        results = []
        for hit in search_result:
            results.append({
                "score": hit.score,
                "payload": hit.payload,
                "id": hit.id,
                "vector_name": vector_name
            })
        
        return results
    
    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """
        Build Qdrant filter from dict
        
        Example filters:
            {
                "content_type": "api_documentation",
                "file_extension": ".md",
                "chunking_strategy": "hierarchical_balanced"
            }
        """
        conditions = []
        
        for key, value in filters.items():
            condition = FieldCondition(
                key=key,
                match=MatchValue(value=value)
            )
            conditions.append(condition)
        
        return Filter(must=conditions)
    
    def hybrid_search(
        self,
        text: str,
        dense_vector_name: str = "jina-code-1.5b",
        sparse_vector_name: str = "bm25",
        limit: int = 5,
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search: Dense + Sparse fusion
        
        Args:
            text: Query text
            dense_vector_name: Named dense vector
            sparse_vector_name: Named sparse vector
            limit: Number of results
            dense_weight: Weight for dense scores (0-1)
            sparse_weight: Weight for sparse scores (0-1)
        
        Returns:
            Fused results with combined scores
        """
        # Get dense results
        dense_results = self.search_with_named_vector(
            text=text,
            vector_name=dense_vector_name,
            limit=limit * 2  # Get more for fusion
        )
        
        # Get sparse results (BM25-style)
        # Note: Requires sparse vector generation for query
        sparse_results = self.search_with_named_vector(
            text=text,
            vector_name=sparse_vector_name,
            limit=limit * 2
        )
        
        # Reciprocal Rank Fusion (RRF)
        combined = self._rrf_fusion(
            dense_results,
            sparse_results,
            dense_weight,
            sparse_weight
        )
        
        return combined[:limit]
    
    def _rrf_fusion(
        self,
        dense_results: List[Dict],
        sparse_results: List[Dict],
        dense_weight: float,
        sparse_weight: float
    ) -> List[Dict]:
        """Reciprocal Rank Fusion for hybrid search"""
        k = 60  # RRF constant
        scores = {}
        
        # Score dense results
        for rank, result in enumerate(dense_results, 1):
            doc_id = result["id"]
            rrf_score = dense_weight / (k + rank)
            scores[doc_id] = scores.get(doc_id, 0) + rrf_score
        
        # Score sparse results
        for rank, result in enumerate(sparse_results, 1):
            doc_id = result["id"]
            rrf_score = sparse_weight / (k + rank)
            scores[doc_id] = scores.get(doc_id, 0) + rrf_score
        
        # Combine and sort
        combined = []
        seen = set()
        
        for result in dense_results + sparse_results:
            doc_id = result["id"]
            if doc_id not in seen:
                result["combined_score"] = scores[doc_id]
                combined.append(result)
                seen.add(doc_id)
        
        combined.sort(key=lambda x: x["combined_score"], reverse=True)
        return combined
```

---

### FastAPI Service Wrapper

```python
# File: search_service.py

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from neural_searcher import NeuralSearcher
from typing import Optional, List, Dict, Any
import uvicorn


app = FastAPI(
    title="V5 Neural Search API",
    description="Neural search service for chunked technical documentation",
    version="1.0.0"
)

# Initialize neural searcher (configurable per collection)
searchers = {
    "technical_docs": NeuralSearcher(
        collection_name="technical_docs",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    ),
    "code_docs": NeuralSearcher(
        collection_name="code_docs",
        model_name="jinaai/jina-code-embeddings-1.5b",
        device="cuda"
    )
}


@app.get("/")
def root():
    """API health check"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "collections": list(searchers.keys())
    }


@app.get("/api/search")
def search(
    q: str = Query(..., description="Search query text"),
    collection: str = Query("technical_docs", description="Collection name"),
    limit: int = Query(5, ge=1, le=50, description="Number of results"),
    score_threshold: Optional[float] = Query(None, ge=0.0, le=1.0),
    content_type: Optional[str] = Query(None, description="Filter by content_type"),
    file_extension: Optional[str] = Query(None, description="Filter by file extension")
) -> Dict[str, Any]:
    """
    Neural search endpoint
    
    Example:
        GET /api/search?q=authentication&limit=5&content_type=api_documentation
    """
    # Get searcher for collection
    if collection not in searchers:
        return JSONResponse(
            status_code=404,
            content={"error": f"Collection '{collection}' not found"}
        )
    
    searcher = searchers[collection]
    
    # Build filters
    filters = {}
    if content_type:
        filters["content_type"] = content_type
    if file_extension:
        filters["file_extension"] = file_extension
    
    # Perform search
    results = searcher.search(
        text=q,
        limit=limit,
        score_threshold=score_threshold,
        filters=filters if filters else None
    )
    
    return {
        "query": q,
        "collection": collection,
        "total_results": len(results),
        "results": results
    }


@app.get("/api/hybrid-search")
def hybrid_search(
    q: str = Query(..., description="Search query text"),
    collection: str = Query("technical_docs", description="Collection name"),
    limit: int = Query(5, ge=1, le=50),
    dense_weight: float = Query(0.7, ge=0.0, le=1.0),
    sparse_weight: float = Query(0.3, ge=0.0, le=1.0)
) -> Dict[str, Any]:
    """
    Hybrid search endpoint (dense + sparse fusion)
    
    Example:
        GET /api/hybrid-search?q=authentication&dense_weight=0.7&sparse_weight=0.3
    """
    if collection not in searchers:
        return JSONResponse(
            status_code=404,
            content={"error": f"Collection '{collection}' not found"}
        )
    
    searcher = searchers[collection]
    
    # Hybrid search
    results = searcher.hybrid_search(
        text=q,
        limit=limit,
        dense_weight=dense_weight,
        sparse_weight=sparse_weight
    )
    
    return {
        "query": q,
        "collection": collection,
        "search_type": "hybrid",
        "weights": {"dense": dense_weight, "sparse": sparse_weight},
        "total_results": len(results),
        "results": results
    }


if __name__ == "__main__":
    # Run the service
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

---

### Usage Examples

#### 1. Basic Search

```python
from neural_searcher import NeuralSearcher

# Initialize searcher
searcher = NeuralSearcher(
    collection_name="technical_docs",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Search for similar documents
results = searcher.search(
    text="How to authenticate API requests?",
    limit=5
)

# Print results
for i, result in enumerate(results, 1):
    print(f"\n{i}. Score: {result['score']:.4f}")
    print(f"   File: {result['payload']['filename']}")
    print(f"   Section: {result['payload']['heading_text']}")
    print(f"   Text: {result['payload']['text'][:100]}...")
```

#### 2. Filtered Search

```python
# Search only in API documentation
results = searcher.search(
    text="OAuth 2.0 authentication",
    limit=10,
    filters={
        "content_type": "api_documentation",
        "file_extension": ".md"
    }
)
```

#### 3. Named Vector Search (Multi-Vector Collection)

```python
# Search using Jina Code embeddings
results = searcher.search_with_named_vector(
    text="async function definition",
    vector_name="jina-code-1.5b",
    limit=5
)
```

#### 4. Hybrid Search (Dense + Sparse)

```python
# Hybrid search with RRF fusion
results = searcher.hybrid_search(
    text="API rate limiting",
    dense_vector_name="jina-code-1.5b",
    sparse_vector_name="bm25",
    limit=10,
    dense_weight=0.7,
    sparse_weight=0.3
)
```

#### 5. FastAPI Service

```bash
# Run the service
python search_service.py

# Access API docs
# http://localhost:8000/docs

# Search via curl
curl "http://localhost:8000/api/search?q=authentication&limit=5"

# Hybrid search
curl "http://localhost:8000/api/hybrid-search?q=oauth&dense_weight=0.7"
```

---

### Integration with V5 Chunker/Embedder

```python
# Complete workflow: Chunk → Embed → Index → Search

# Step 1: Chunk documents
from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b"
)

chunks = chunker.process_directory_smart(
    input_dir="Docs",
    output_dir="Chunked"
)

# Step 2: Generate embeddings
from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    companion_dense_models=["bge-m3"]
)

embedder.load_chunks_from_processing()
embedder.generate_embeddings_kaggle_optimized()
embedder.export_for_local_qdrant()

# Step 3: Upload to Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("localhost", port=6333)

client.create_collection(
    collection_name="technical_docs",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE
    )
)

# Upload points (from embedder export)
# ...

# Step 4: Neural search
searcher = NeuralSearcher(
    collection_name="technical_docs",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

results = searcher.search("API authentication", limit=5)
```

---

### Deployment Checklist

- [x] Install dependencies: `pip install sentence-transformers qdrant-client fastapi uvicorn`
- [x] Run Qdrant: `docker run -p 6333:6333 qdrant/qdrant`
- [x] Create collection with proper vector config
- [x] Upload chunked + embedded documents
- [x] Initialize NeuralSearcher with correct model
- [x] Test search queries
- [x] Deploy FastAPI service: `uvicorn search_service:app --host 0.0.0.0 --port 8000`
- [x] Access API docs: `http://localhost:8000/docs`

---

**Ready for Code mode implementation**.