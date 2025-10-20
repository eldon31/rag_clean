# V5 Chunker & Embedder Implementation Plan
**Focused Scope**: Chunking + Embedding → Qdrant Vector Database

**Date**: 2025-10-20  
**Goal**: Enhance V4 chunker/embedder with 5-framework integration for Qdrant

---

## Project Scope

### In Scope ✅
- **Chunking**: Enhanced document chunking (Docling + Tree-sitter + Semchunk)
- **Embedding**: Multi-model embedding generation (Sentence-Transformers)
- **Export**: Qdrant-ready JSONL with named vectors + sparse vectors
- **Backward Compatibility**: V4 interface preserved

### Out of Scope ❌
- Query engines (handled by Qdrant search)
- Retrieval logic (handled by Qdrant HNSW)
- LLM integration (separate concern)
- Web UI/API (separate concern)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│              INPUT: Documents/Files                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│         CHUNKING (Enhanced Ultimate Chunker V5)             │
├─────────────────────────────────────────────────────────────┤
│  Step 1: Docling Document Conversion                        │
│    PDF/Office/HTML → Structured DoclingDocument             │
│    - Extract tables, figures, headings                      │
│    - Preserve document hierarchy                            │
│                                                              │
│  Step 2: Content-Type Routing                               │
│    ├─ Code blocks → Tree-sitter (AST-based)                │
│    ├─ Text blocks → Semchunk (semantic boundaries)         │
│    └─ Tables/Figures → Structure-aware chunking            │
│                                                              │
│  Step 3: Metadata Enrichment                                │
│    - Hierarchy paths (chapter > section > subsection)       │
│    - Content type tags (code, prose, table, list)          │
│    - Search keywords extraction                             │
│    - Sparse features (term weights for BM25-style)         │
│                                                              │
│  Output: List[ChunkDict] with rich metadata                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│       EMBEDDING (Ultimate Kaggle Embedder V4+)              │
├─────────────────────────────────────────────────────────────┤
│  Step 1: Multi-Model Embedding Generation                   │
│    Dense Vectors (Hugging Face local):                     │
│    ├─ Primary: jina-code-1.5b (1536D)                      │
│    ├─ Secondary: bge-m3 (1024D)                            │
│    ├─ Tertiary: nomic-coderank (768D)                      │
│    └─ Qdrant-optimized: Qdrant/all-MiniLM-L6-v2-onnx (384D)│
│                                                              │
│    Sparse Vectors (Hugging Face local):                    │
│    ├─ Qdrant/all_miniLM_L6_v2_with_attentions (sparse)    │
│    └─ Qdrant/bm25 (BM25-style term weights)               │
│                                                              │
│  Step 2: Matryoshka Support (Jina models)                   │
│    - Flexible dimensions: 128/256/512/1024/1536/2048       │
│    - Runtime dimension selection                            │
│                                                              │
│  Step 3: Vector Normalization                               │
│    - L2 normalization for cosine similarity                │
│    - Float32 compression for storage efficiency            │
│                                                              │
│  Output: embeddings_by_model Dict[str, np.ndarray]         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           EXPORT: Qdrant-Ready JSONL Files                  │
├─────────────────────────────────────────────────────────────┤
│  File 1: Dense Embeddings (primary_qdrant.jsonl)           │
│    {                                                         │
│      "id": 0,                                               │
│      "vectors": {                                           │
│        "jina-code-1.5b": [1536D vector],                   │
│        "bge-m3": [1024D vector],                           │
│        "nomic-coderank": [768D vector],                    │
│        "qdrant-minilm": [384D vector]                      │
│      },                                                     │
│      "payload": {                                           │
│        "text": "...",                                       │
│        "metadata": {...},                                   │
│        "hierarchy_path": "...",                             │
│        "content_type": "code|prose|table",                 │
│        "search_keywords": [...]                            │
│      }                                                      │
│    }                                                        │
│                                                              │
│  File 2: Sparse Vectors (sparse.jsonl)                     │
│    {                                                         │
│      "id": 0,                                               │
│      "sparse_vectors": {                                    │
│        "bm25": {                                            │
│          "indices": [hash_int, ...],                       │
│          "values": [weight, ...]                           │
│        },                                                   │
│        "minilm_attention": {                               │
│          "indices": [hash_int, ...],                       │
│          "values": [attention_weight, ...]                 │
│        }                                                    │
│      },                                                     │
│      "tokens": ["term1", "term2", ...]                     │
│    }                                                        │
│                                                              │
│  File 3: Upload Script (upload_to_qdrant.py)               │
│    - Auto-generated Python script                          │
│    - Creates Qdrant collection with named vectors          │
│    - Batch uploads with progress tracking                  │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              QDRANT VECTOR DATABASE                         │
├─────────────────────────────────────────────────────────────┤
│  Collection: docs_v5_multi                                  │
│                                                              │
│  Named Dense Vectors:                                       │
│  ├─ jina-code-1.5b: 1536D, cosine, HNSW                   │
│  ├─ bge-m3: 1024D, cosine, HNSW                           │
│  ├─ nomic-coderank: 768D, cosine, HNSW                    │
│  └─ qdrant-minilm: 384D, cosine, HNSW (ONNX-optimized)   │
│                                                              │
│  Named Sparse Vectors:                                      │
│  ├─ bm25: BM25-style term weights (Qdrant/bm25)          │
│  └─ minilm_attention: Attention-based sparse weights       │
│     (Qdrant/all_miniLM_L6_v2_with_attentions)            │
│                                                              │
│  Payload Indexing:                                          │
│  ├─ content_type (keyword)                                 │
│  ├─ hierarchy_path (text)                                  │
│  └─ search_keywords (keyword array)                        │
│                                                              │
│  Quantization: int8 scalar quantization                    │
│  HNSW: m=48, ef_construct=512                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Tasks

### Phase 1: Enhanced Chunker (Week 1)

#### Task 1.1: Docling Integration
**File**: `processor/enhanced_ultimate_chunker_v5.py`

```python
class EnhancedUltimateChunkerV5:
    """
    V5 Chunker with Docling document conversion.
    Backward compatible with V4 interface.
    """
    
    def __init__(
        self,
        use_docling: bool = True,
        use_tree_sitter: bool = True,
        use_semchunk: bool = True,
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        backward_compatible: bool = True  # V4 output format
    ):
        # Docling converter for PDF/Office/HTML
        if use_docling:
            from docling.document_converter import DocumentConverter
            self.docling_converter = DocumentConverter()
        
        # V4 chunkers (preserved)
        self.tree_sitter_chunker = TreeSitterChunker(...)
        self.semchunk_chunker = SemchunkChunker(...)
    
    def chunk_documents(
        self,
        file_paths: List[str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Main chunking method.
        Returns V4-compatible chunks or V5 enhanced chunks.
        """
        chunks = []
        
        for file_path in file_paths:
            # Step 1: Docling conversion (if supported format)
            if self._is_docling_supported(file_path):
                docling_doc = self.docling_converter.convert(file_path)
                doc_chunks = self._chunk_docling_document(docling_doc)
            else:
                # Fallback to V4 logic
                doc_chunks = self._chunk_v4_style(file_path)
            
            chunks.extend(doc_chunks)
        
        return chunks
```

**Deliverables**:
- ✅ Docling converter integration
- ✅ PDF/Office/HTML support
- ✅ V4 backward compatibility
- ✅ Enhanced metadata extraction

#### Task 1.2: Content-Type Routing
**Enhancement**: Route chunks to appropriate sub-chunkers

```python
def _chunk_by_content_type(
    self,
    text: str,
    content_type: str,
    metadata: Dict
) -> List[Dict]:
    """Route to specialized chunker based on content type."""
    
    if content_type == "code":
        # Use Tree-sitter for code-aware chunking
        return self.tree_sitter_chunker.chunk(text, metadata)
    
    elif content_type in ["prose", "documentation"]:
        # Use Semchunk for semantic boundaries
        return self.semchunk_chunker.chunk(text, metadata)
    
    elif content_type == "table":
        # Table-specific chunking (preserve structure)
        return self._chunk_table(text, metadata)
    
    else:
        # Default chunking
        return self._chunk_default(text, metadata)
```

#### Task 1.3: Metadata Enrichment
**Enhancement**: Rich metadata for Qdrant payload indexing

```python
def _enrich_metadata(
    self,
    chunk: Dict,
    docling_doc: Optional[DoclingDocument]
) -> Dict:
    """Add V5 metadata enhancements."""
    
    metadata = chunk["metadata"]
    
    # Hierarchy path (from Docling structure)
    if docling_doc:
        metadata["hierarchy_path"] = self._build_hierarchy_path(
            docling_doc, chunk
        )
        metadata["document_title"] = docling_doc.title
        metadata["page_number"] = chunk.get("page_num")
    
    # Content type classification
    metadata["content_type"] = self._classify_content_type(chunk["text"])
    
    # Search keywords extraction
    metadata["search_keywords"] = self._extract_keywords(chunk["text"])
    
    # Sparse features (for BM25-style hybrid search)
    metadata["sparse_features"] = self._extract_sparse_features(
        chunk["text"]
    )
    
    return metadata
```

### Phase 2: Enhanced Embedder (Week 2)

#### Task 2.1: Multi-Model Embedding
**File**: `processor/kaggle_ultimate_embedder_v4.py` (enhance existing)

**Enhancement**: Already supports multi-model via `companion_dense_models`

```python
# V5 Usage example with Qdrant-optimized models
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",  # Primary (1536D)
    companion_dense_models=[
        "bge-m3",              # 1024D
        "nomic-coderank",      # 768D
        "all-miniLM-l6"        # 384D (Qdrant-optimized ONNX)
    ],
    gpu_config=KaggleGPUConfig(...)
)

# Add to KAGGLE_OPTIMIZED_MODELS in kaggle_ultimate_embedder_v4.py:
"qdrant-minilm-onnx": ModelConfig(
    name="qdrant-minilm-onnx",
    hf_model_id="Qdrant/all-MiniLM-L6-v2-onnx",
    vector_dim=384,
    max_tokens=256,
    recommended_batch_size=128,
    memory_efficient=True
)
```

**Status**: ⚠️ Needs Qdrant ONNX model addition to V4

#### Task 2.2: Matryoshka Dimension Support
**Enhancement**: Runtime dimension selection for Jina models

```python
class MatryoshkaEmbedder:
    """Wrapper for Matryoshka-aware models."""
    
    SUPPORTED_DIMENSIONS = {
        "jina-code-1.5b": [128, 256, 512, 1024, 1536],
        "jina-embeddings-v4": [128, 256, 512, 1024, 2048]
    }
    
    def encode(
        self,
        texts: List[str],
        dimension: Optional[int] = None
    ) -> np.ndarray:
        """
        Encode with optional dimension truncation.
        If dimension=512, return only first 512 dims.
        """
        full_embeddings = self.model.encode(texts)
        
        if dimension and dimension < full_embeddings.shape[1]:
            return full_embeddings[:, :dimension]
        
        return full_embeddings
```

#### Task 2.3: Sparse Embedding Generation
**Enhancement**: Multiple sparse vector types (BM25 + Attention-based)

```python
def generate_sparse_embeddings(
    self,
    chunks: List[Dict]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate multiple types of sparse vectors:
    1. BM25-style: Qdrant/bm25 model
    2. Attention-based: Qdrant/all_miniLM_L6_v2_with_attentions
    """
    
    sparse_vectors = {
        "bm25": [],
        "minilm_attention": []
    }
    
    # Load Qdrant sparse models
    from sentence_transformers import SentenceTransformer
    
    # BM25 model (term frequency-based)
    bm25_model = SentenceTransformer("Qdrant/bm25")
    
    # Attention-based sparse model
    attention_model = SentenceTransformer(
        "Qdrant/all_miniLM_L6_v2_with_attentions"
    )
    
    for chunk in chunks:
        text = chunk["text"]
        
        # BM25 sparse vectors
        bm25_sparse = self._generate_bm25_sparse(text, bm25_model)
        sparse_vectors["bm25"].append(bm25_sparse)
        
        # Attention-based sparse vectors
        attention_sparse = self._generate_attention_sparse(
            text, attention_model
        )
        sparse_vectors["minilm_attention"].append(attention_sparse)
    
    return sparse_vectors

def _generate_bm25_sparse(
    self,
    text: str,
    model: SentenceTransformer
) -> Dict[str, Any]:
    """Generate BM25-style sparse vector."""
    # Model returns sparse representation
    sparse_output = model.encode(
        text,
        convert_to_tensor=False,
        output_value="token_embeddings"  # Get sparse outputs
    )
    
    # Extract non-zero indices and values
    indices = []
    values = []
    tokens = []
    
    # Process sparse output from Qdrant/bm25 model
    # (implementation depends on model's output format)
    
    return {
        "indices": indices,
        "values": values,
        "tokens": tokens
    }

def _generate_attention_sparse(
    self,
    text: str,
    model: SentenceTransformer
) -> Dict[str, Any]:
    """Generate attention-based sparse vector."""
    # Model returns attention weights as sparse vectors
    sparse_output = model.encode(
        text,
        convert_to_tensor=False,
        output_value="attention_weights"
    )
    
    # Extract attention-based sparse representation
    indices = []
    values = []
    tokens = []
    
    # Process attention output from model
    
    return {
        "indices": indices,
        "values": values,
        "tokens": tokens
    }
```

### Phase 3: Qdrant Export (Week 3)

#### Task 3.1: Enhanced JSONL Export
**Enhancement**: Named vectors + sparse vectors

```python
def export_for_qdrant_v5(self) -> Dict[str, str]:
    """
    Export embeddings in V5 format with:
    - Named dense vectors (jina-code, bge-m3, nomic-coderank)
    - Sparse vectors (BM25-style)
    - Rich payload metadata
    """
    
    exported_files = {}
    
    # 1. Dense vectors JSONL
    dense_jsonl = self._export_dense_vectors_jsonl()
    exported_files["dense_jsonl"] = dense_jsonl
    
    # 2. Sparse vectors JSONL (sidecar)
    if self.sparse_vectors:
        sparse_jsonl = self._export_sparse_vectors_jsonl()
        exported_files["sparse_jsonl"] = sparse_jsonl
    
    # 3. Upload script (auto-generated)
    upload_script = self._generate_qdrant_upload_script_v5()
    exported_files["upload_script"] = upload_script
    
    return exported_files
```

#### Task 3.2: Qdrant Collection Configuration
**Enhancement**: Named vectors support

```python
def _generate_qdrant_collection_config(self) -> Dict:
    """Generate Qdrant collection configuration."""
    
    vector_configs = {}
    
    # Dense vector configurations
    vector_configs["jina-code-1.5b"] = {
        "size": 1536,
        "distance": "Cosine",
        "on_disk": False
    }
    
    if "bge-m3" in self.embeddings_by_model:
        vector_configs["bge-m3"] = {
            "size": 1024,
            "distance": "Cosine",
            "on_disk": False
        }
    
    if "nomic-coderank" in self.embeddings_by_model:
        vector_configs["nomic-coderank"] = {
            "size": 768,
            "distance": "Cosine",
            "on_disk": False
        }
    
    # Qdrant-optimized ONNX model
    if "qdrant-minilm-onnx" in self.embeddings_by_model:
        vector_configs["qdrant-minilm"] = {
            "size": 384,
            "distance": "Cosine",
            "on_disk": False
        }
    
    # Sparse vector configurations
    if self.sparse_vectors:
        # BM25-style sparse vectors
        vector_configs["bm25"] = {
            "sparse": True,
            "modifier": "idf"
        }
        
        # Attention-based sparse vectors
        vector_configs["minilm_attention"] = {
            "sparse": True,
            "modifier": "none"  # Raw attention weights
        }
    
    return {
        "vectors": vector_configs,
        "hnsw_config": {
            "m": 48,
            "ef_construct": 512,
            "full_scan_threshold": 50000
        },
        "quantization_config": {
            "scalar": {
                "type": "int8",
                "quantile": 0.99,
                "always_ram": True
            }
        }
    }
```

---

## File Structure

```
processor/
├── enhanced_ultimate_chunker_v5.py      # NEW: V5 chunker with Docling
├── kaggle_ultimate_embedder_v4.py       # ENHANCED: Multi-model + sparse
├── docling_integration.py               # NEW: Docling helpers
├── sparse_encoder.py                    # NEW: Sparse vector generation
└── matryoshka_embedder.py              # NEW: Flexible dimensions

scripts/
├── chunk_docs_v5.py                    # NEW: V5 chunking script
├── embed_collections_v5.py              # NEW: V5 embedding script
└── upload_to_qdrant_v5.py              # NEW: Qdrant upload with named vectors
```

---

## Success Criteria

### Chunking Quality
- ✅ Document structure preserved (headings, sections, paragraphs)
- ✅ Code blocks properly parsed (function/class boundaries)
- ✅ Tables/figures extracted intact
- ✅ Semantic boundaries respected (no mid-sentence splits)

### Embedding Quality
- ✅ Multi-model embeddings generated (3+ models)
- ✅ Sparse vectors available for hybrid search
- ✅ Matryoshka dimensions supported (flexible precision)
- ✅ Processing speed: >250 chunks/sec on Kaggle T4 x2

### Qdrant Integration
- ✅ Named vectors properly configured
- ✅ Sparse vectors stored separately
- ✅ Payload metadata indexed (content_type, hierarchy_path, keywords)
- ✅ Auto-generated upload script works

### Backward Compatibility
- ✅ V4 interface preserved (drop-in replacement)
- ✅ V4 output format supported (via `backward_compatible=True`)
- ✅ Existing scripts work with minimal changes

---

## Timeline

### Week 1: Chunker V5
- Day 1-2: Docling integration
- Day 3-4: Content-type routing
- Day 5: Metadata enrichment + testing

### Week 2: Embedder Enhancements
- Day 1-2: Multi-model orchestration
- Day 3: Matryoshka support
- Day 4-5: Sparse embedding generation

### Week 3: Qdrant Export
- Day 1-2: Named vectors JSONL export
- Day 3: Upload script generation
- Day 4-5: Integration testing + optimization

---

## Next Action

**Ready to begin implementation**. Recommend starting with:

1. **Create `enhanced_ultimate_chunker_v5.py`** - New chunker with Docling
2. **Enhance `kaggle_ultimate_embedder_v4.py`** - Add sparse embedding support
3. **Test end-to-end** - Chunk → Embed → Export → Upload to Qdrant

Shall I proceed with implementation?