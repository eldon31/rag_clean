# V5 RAG System API Reference

**Phase 2 Track 5 - Task 5.1**

Complete API documentation for Enhanced Ultimate Chunker V5 and related components.

---

## Table of Contents

1. [Core Chunker API](#core-chunker-api)
2. [LlamaIndex Integration](#llamaindex-integration)
3. [Embedding API](#embedding-api)
4. [Sparse Vector API](#sparse-vector-api)
5. [Configuration Classes](#configuration-classes)
6. [Utility Functions](#utility-functions)

---

## Core Chunker API

### `EnhancedUltimateChunkerV5Unified`

Main chunking class combining V3 hierarchical capabilities with V5 model-aware approach.

#### Constructor

```python
EnhancedUltimateChunkerV5Unified(
    config: Optional[ChunkerConfig] = None,
    target_model: str = "jina-code-embeddings-1.5b",
    **kwargs
)
```

**Parameters:**
- `config` (ChunkerConfig, optional): Configuration object
- `target_model` (str): Target embedding model name
- `**kwargs`: Override config parameters

**Example:**
```python
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    use_tree_sitter=True,
    use_semchunk=True,
    safety_margin=0.8
)
```

#### Methods

##### `process_file_smart()`

Process single file with smart content detection.

```python
process_file_smart(
    file_path: str,
    output_dir: Optional[str] = None,
    auto_detect: bool = True,
    strategy_override: Optional[str] = None
) -> List[Dict[str, Any]]
```

**Parameters:**
- `file_path` (str): Path to file to process
- `output_dir` (str, optional): Output directory for chunks
- `auto_detect` (bool): Auto-detect content type and strategy
- `strategy_override` (str, optional): Override detected strategy

**Returns:**
- `List[Dict[str, Any]]`: List of chunk dictionaries

**Example:**
```python
chunks = chunker.process_file_smart(
    "document.md",
    output_dir="output/chunks",
    auto_detect=True
)
```

##### `process_directory_smart()`

Batch process entire directory.

```python
process_directory_smart(
    input_dir: str,
    output_dir: str,
    file_extensions: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `input_dir` (str): Input directory path
- `output_dir` (str): Output directory path
- `file_extensions` (List[str], optional): File extensions to process

**Returns:**
- `Dict[str, Any]`: Processing summary with statistics

**Example:**
```python
summary = chunker.process_directory_smart(
    "documents/",
    "output/chunks",
    file_extensions=[".md", ".txt", ".py"]
)
```

##### `process_docling_document()`

Process document via Docling pipeline (Phase 2C).

```python
process_docling_document(
    file_path: str,
    output_dir: Optional[str] = None,
    strategy_override: Optional[str] = None,
    preserve_tables: bool = True,
    extract_figures: bool = True,
    resolve_references: bool = True
) -> List[Dict[str, Any]]
```

**Parameters:**
- `file_path` (str): Path to document (PDF, DOCX, HTML)
- `output_dir` (str, optional): Output directory
- `strategy_override` (str, optional): Override strategy
- `preserve_tables` (bool): Preserve table structures
- `extract_figures` (bool): Extract figures with captions
- `resolve_references` (bool): Resolve cross-references

**Returns:**
- `List[Dict[str, Any]]`: List of enriched chunks

**Example:**
```python
chunks = chunker.process_docling_document(
    "document.pdf",
    preserve_tables=True,
    extract_figures=True
)
```

##### `chunk_documents()` (V5 API)

Backward-compatible V5 interface for batch processing.

```python
chunk_documents(
    file_paths: List[str],
    output_dir: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

**Parameters:**
- `file_paths` (List[str]): List of file paths
- `output_dir` (str, optional): Output directory
- `**kwargs`: Additional parameters

**Returns:**
- `List[Dict[str, Any]]`: Combined list of all chunks

##### `validate_chunks()`

Validate chunks for model compatibility.

```python
validate_chunks(
    chunks: List[Dict[str, Any]]
) -> Dict[str, Any]
```

**Parameters:**
- `chunks` (List[Dict[str, Any]]): List of chunks to validate

**Returns:**
- `Dict[str, Any]`: Validation report

**Example:**
```python
validation = chunker.validate_chunks(chunks)
if validation["validation_passed"]:
    print("✓ All chunks valid")
```

##### `create_hierarchical_chunks()`

Core hierarchical chunking method (V3 API).

```python
create_hierarchical_chunks(
    text: str,
    filename: str,
    strategy_name: str = "hierarchical_balanced"
) -> List[Dict[str, Any]]
```

**Parameters:**
- `text` (str): Document text
- `filename` (str): Source filename
- `strategy_name` (str): Chunking strategy name

**Returns:**
- `List[Dict[str, Any]]`: List of chunks with quality scores

---

## LlamaIndex Integration

### `HierarchicalNodeParser`

LlamaIndex NodeParser wrapper for V5 chunker.

#### Constructor

```python
HierarchicalNodeParser(
    chunker: Optional[EnhancedUltimateChunkerV5Unified] = None,
    target_model: str = "jina-code-embeddings-1.5b",
    strategy: str = "hierarchical_balanced",
    include_metadata: bool = True,
    include_prev_next_rel: bool = True
)
```

**Parameters:**
- `chunker` (EnhancedUltimateChunkerV5Unified, optional): Existing chunker instance
- `target_model` (str): Target embedding model
- `strategy` (str): Chunking strategy
- `include_metadata` (bool): Include chunk metadata
- `include_prev_next_rel` (bool): Include node relationships

#### Methods

##### `get_nodes_from_documents()`

Convert documents to LlamaIndex nodes.

```python
get_nodes_from_documents(
    documents: List[Document],
    show_progress: bool = False
) -> List[TextNode]
```

**Example:**
```python
from llama_index.core import Document
from processor.llamaindex_chunker_v5 import HierarchicalNodeParser

parser = HierarchicalNodeParser(target_model="jina-code-embeddings-1.5b")
doc = Document(text=open("document.md").read())
nodes = parser.get_nodes_from_documents([doc])
```

### Other NodeParser Classes

- **`DoclingNodeParser`**: Docling integration for PDF/Office
- **`TreeSitterNodeParser`**: AST-based code chunking
- **`SemchunkNodeParser`**: Semantic boundary detection

All share the same `get_nodes_from_documents()` interface.

---

## Embedding API

### `MultiModelEmbedder`

Generate embeddings from multiple models simultaneously.

#### Constructor

```python
MultiModelEmbedder(
    model_names: List[str],
    device: str = "cpu",
    batch_size: int = 32,
    matryoshka_dims: Optional[Dict[str, int]] = None
)
```

**Parameters:**
- `model_names` (List[str]): List of HuggingFace model IDs
- `device` (str): Computation device ("cpu" or "cuda")
- `batch_size` (int): Batch size for encoding
- `matryoshka_dims` (Dict[str, int], optional): Matryoshka dimension truncation

**Example:**
```python
embedder = MultiModelEmbedder(
    model_names=[
        "jinaai/jina-embeddings-v2-base-code",
        "BAAI/bge-m3"
    ],
    matryoshka_dims={"jinaai/jina-embeddings-v2-base-code": 1024}
)
```

#### Methods

##### `get_multi_model_embeddings()`

Generate embeddings from all models.

```python
get_multi_model_embeddings(
    texts: List[str],
    model_names: Optional[List[str]] = None
) -> Dict[str, np.ndarray]
```

**Parameters:**
- `texts` (List[str]): Texts to embed
- `model_names` (List[str], optional): Subset of models to use

**Returns:**
- `Dict[str, np.ndarray]`: Model name → embeddings array

**Example:**
```python
texts = ["Hello world", "Test document"]
embeddings = embedder.get_multi_model_embeddings(texts)

# Access embeddings
jina_embeddings = embeddings["jinaai/jina-embeddings-v2-base-code"]
print(jina_embeddings.shape)  # (2, 768)
```

##### `get_named_vectors_for_qdrant()`

Generate Qdrant-compatible named vectors.

```python
get_named_vectors_for_qdrant(
    texts: List[str],
    model_names: Optional[List[str]] = None
) -> List[Dict[str, List[float]]]
```

**Returns:**
- `List[Dict[str, List[float]]]`: List of named vector dictionaries

**Example:**
```python
named_vectors = embedder.get_named_vectors_for_qdrant(texts)

# Qdrant point format
points = []
for i, vectors in enumerate(named_vectors):
    points.append({
        "id": i,
        "vector": vectors,  # {"model1": [...], "model2": [...]}
        "payload": {"text": texts[i]}
    })
```

### Ultimate Embedder Services

The Kaggle-oriented embedder facade in `processor/ultimate_embedder/` keeps the legacy `UltimateKaggleEmbedderV4` API but routes work through lightweight service modules. Use the map below to find the right extension point:

| Module | Key Types | Responsibility |
| --- | --- | --- |
| `core.py` | `UltimateKaggleEmbedderV4` | Public facade; wires helpers, exposes CLI entry points, and maintains backward compatible methods. |
| `chunk_loader.py` | `ChunkLoader`, `ChunkLoadResult` | Streams chunk JSONL files, enriches metadata, and validates batch sizing before encoding. |
| `model_manager.py` | `ModelManager` | Resolves primary/ensemble/companion models, handles device placement, and caches loaded weights. |
| `backend_encoder.py` | `encode_with_backend()` | Reusable helper for non-standard backends (TensorRT/ONNX/HF) invoked when the facade falls back to custom models. |
| `controllers.py` | `AdaptiveBatchController`, `GPUMemorySnapshot` | Tracks GPU utilisation, adjusts batch sizes, and reports mitigation events. |
| `batch_runner.py` | `BatchRunner` | Coordinates the adaptive loop, retries failed batches, and writes embeddings/named vectors back to the facade. |
| `sparse_pipeline.py` | `build_sparse_vector_from_metadata()` | Normalises sparse vector payloads and modal hints emitted by the chunker for hybrid search. |
| `rerank_pipeline.py` | `RerankPipeline` | Optional CrossEncoder reranking wrapper with embedding-only fallback. |
| `monitoring.py` | `PerformanceMonitor` | Periodically samples GPU/CPU stats and surfaces live progress to logs. |
| `export_runtime.py` | `ExportRuntime` | Generates Qdrant JSONL, NumPy dumps, FAISS indexes, and helper scripts while respecting export config. |
| `telemetry.py` | `TelemetryTracker`, `resolve_rotation_payload_limit()` | Central store for mitigation, rotation, cache, and GPU telemetry tracked during runs. |

To customise behaviour, inject alternative helpers via the `UltimateKaggleEmbedderV4` constructor (for example, supply a patched `ModelManager` or turn off rerankers). Avoid expanding `core.py` directly—its executable-line guard enforces that orchestration remains slim.

---

## Sparse Vector API

### `BM25SparseEncoder`

Statistical BM25-based sparse vector generation.

#### Constructor

```python
BM25SparseEncoder(
    k1: float = 1.5,
    b: float = 0.75,
    top_k: Optional[int] = None
)
```

**Parameters:**
- `k1` (float): Term frequency saturation parameter
- `b` (float): Length normalization parameter
- `top_k` (int, optional): Keep only top-K terms

#### Methods

##### `fit()`

Fit BM25 on corpus to compute IDF scores.

```python
fit(texts: List[str]) -> None
```

##### `encode()`

Encode texts to sparse vectors.

```python
encode(texts: List[str]) -> List[Dict[str, Any]]
```

**Returns:**
- `List[Dict[str, Any]]`: Sparse vectors with indices, values, tokens

**Example:**
```python
encoder = BM25SparseEncoder(top_k=20)
encoder.fit(corpus_texts)

sparse_vectors = encoder.encode(query_texts)
for sv in sparse_vectors:
    print(f"Indices: {sv['indices']}")
    print(f"Values: {sv['values']}")
    print(f"Tokens: {sv['tokens']}")
```

### `AttentionSparseEncoder`

Attention-based sparse vector generation.

#### Constructor

```python
AttentionSparseEncoder(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    top_k: int = 20,
    device: str = "cpu"
)
```

**Parameters:**
- `model_name` (str): Transformer model for attention extraction
- `top_k` (int): Keep top-K attention tokens
- `device` (str): Computation device

#### Methods

Same as `BM25SparseEncoder`: `fit()` and `encode()`.

### `HybridSparseEncoder`

Multi-channel sparse encoding (BM25 + attention).

#### Constructor

```python
HybridSparseEncoder(
    use_bm25: bool = True,
    use_attention: bool = False,
    bm25_weight: float = 0.7,
    attention_weight: float = 0.3,
    combination_strategy: str = "weighted_sum"
)
```

**Parameters:**
- `use_bm25` (bool): Enable BM25 channel
- `use_attention` (bool): Enable attention channel
- `bm25_weight` (float): BM25 channel weight
- `attention_weight` (float): Attention channel weight
- `combination_strategy` (str): "weighted_sum" or "max_pool"

**Example:**
```python
encoder = HybridSparseEncoder(
    use_bm25=True,
    use_attention=True,
    bm25_weight=0.6,
    attention_weight=0.4
)

encoder.fit(corpus_texts)
sparse_vectors = encoder.encode(query_texts)
```

---

## Configuration Classes

### `ChunkerConfig`

Configuration for Enhanced Ultimate Chunker V5.

```python
@dataclass
class ChunkerConfig:
    # Model settings
    target_model: str = "jina-code-embeddings-1.5b"
    chunk_size_tokens: Optional[int] = None
    chunk_overlap_tokens: Optional[int] = None
    safety_margin: float = 0.8
    
    # Framework integration
    use_docling: bool = False
    use_tree_sitter: bool = True
    use_semchunk: bool = True
    
    # Quality control
    enable_semantic_scoring: bool = False
    quality_thresholds: Optional[Dict[str, float]] = None
    fallback_promotion_ratio: float = 0.25
    fallback_promotion_cap: int = 40
    
    # Tokenizer
    tokenizer_name: str = "cl100k_base"
    
    # Metadata enrichment
    extract_keywords: bool = True
    generate_sparse_features: bool = True
    classify_content_type: bool = True
    
    # Output
    output_dir: str = "Chunked"
    preserve_hierarchy: bool = True
    backward_compatible: bool = True
```

### `ModelConfig`

Model registry configuration (now located in `processor/ultimate_embedder/config.py`; the legacy `processor/kaggle_ultimate_embedder_v4.py` shim re-exports the same symbols).

```python
@dataclass
class ModelConfig:
    model_name: str
    hf_model_id: str
    max_tokens: int
    vector_dim: int
    recommended_batch_size: int
    backend: str = "pytorch"
    memory_efficient: bool = True
    query_prefix: str = ""
```

---

## Utility Functions

### Token Estimation

```python
def _estimate_tokens(text: str) -> int:
    """Estimate token count (4 chars per token for Jina models)"""
    return len(text) // 4
```

### Quality Scoring

```python
def calculate_semantic_coherence(text: str) -> float:
    """Calculate semantic coherence score (0-1)"""

def calculate_structural_score(chunk_text: str, structure_info: Dict) -> float:
    """Calculate structural quality score (0-1)"""

def calculate_retrieval_quality(chunk_text: str) -> float:
    """Calculate retrieval quality score (0-1)"""
```

### Content Detection

```python
def auto_detect_content_type(text: str, filename: str) -> Tuple[str, str]:
    """Auto-detect content type and select chunking strategy"""
    # Returns: (content_type, strategy_name)
```

---

## Data Structures

### Chunk Dictionary

```python
{
    "text": str,  # Chunk text content
    "metadata": {
        # V5 Model-aware fields
        "target_model": str,
        "chunk_size_tokens": int,
        "estimated_tokens": int,
        "within_token_limit": bool,
        "model_max_tokens": int,
        "embedding_dimension": int,
        
        # V3 Hierarchical fields
        "chunk_id": str,
        "document_id": str,
        "chunk_index": int,
        "source_file": str,
        "section_path": List[str],
        "hierarchy_path": str,
        "token_count": int,
        "char_count": int,
        "start_char": int,
        "end_char": int,
        
        # Content classification
        "content_type": str,
        "chunking_strategy": str,
        "modal_hint": str,
        
        # Quality metrics
        "semantic_score": float,
        "structural_score": float,
        "retrieval_quality": float,
        
        # Search features
        "search_keywords": List[str],
        "sparse_features": Dict[str, Any],
        
        # Processing metadata
        "processing_timestamp": str,
        "chunker_version": str,
        "payload_version": str
    },
    "advanced_scores": {
        "semantic": float,
        "structural": float,
        "retrieval_quality": float,
        "overall": float
    }
}
```

### Sparse Vector Format

```python
{
    "indices": List[int],  # Term indices
    "values": List[float],  # Term weights
    "tokens": List[str]  # Term strings (optional)
}
```

---

## Error Handling

All methods may raise:
- `ValueError`: Invalid parameters or configuration
- `FileNotFoundError`: File not found
- `ImportError`: Missing optional dependencies
- `RuntimeError`: Processing errors

**Example:**
```python
try:
    chunks = chunker.process_file_smart("document.md")
except FileNotFoundError:
    print("File not found")
except ImportError as e:
    print(f"Missing dependency: {e}")
except Exception as e:
    print(f"Processing error: {e}")
```

---

## Version Information

- **API Version**: V5 Unified Phase 2
- **Compatibility**: Python 3.9+
- **Status**: Production Ready
- **Last Updated**: 2025-01-20

---

## See Also

- **Deployment Guide**: `docs/V5_DEPLOYMENT_GUIDE.md`
- **Tutorial**: `docs/V5_TUTORIAL.md`
- **Model Configurations**: `notes/V5_MODEL_CONFIGURATIONS.md`
- **Implementation Plan**: `notes/V5_PHASE2_IMPLEMENTATION_PLAN.md`