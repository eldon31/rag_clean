# V5 Quick Start Guide

Complete walkthrough of the V5 chunking and embedding pipeline with expected outputs.

---

## Table of Contents

1. [Overview](#overview)
2. [Step 1: Document Chunking](#step-1-document-chunking)
3. [Step 2: Embedding Generation](#step-2-embedding-generation)
4. [Step 3: Upload to Qdrant](#step-3-upload-to-qdrant)
5. [Troubleshooting](#troubleshooting)

---

## Overview

**V5 Pipeline Flow**:
```
Raw Documents → Chunker (V5) → Chunk JSONs → Embedder (V4) → JSONL/NumPy → Qdrant Upload
```

**Key Components**:
- **Chunker**: [`processor/enhanced_ultimate_chunker_v5.py`](processor/enhanced_ultimate_chunker_v5.py)
- **Embedder**: [`processor/kaggle_ultimate_embedder_v4.py`](processor/kaggle_ultimate_embedder_v4.py)
- **Chunk Script**: [`scripts/chunk_docs_v5.py`](scripts/chunk_docs_v5.py)
- **Embed Script**: [`scripts/embed_collections_v5.py`](scripts/embed_collections_v5.py)

---

## Step 1: Document Chunking

### Purpose
Convert raw documentation (Markdown, Python, etc.) into semantically-meaningful chunks with rich metadata.

### Command (Kaggle)

```bash
# Cell 5: Chunking
python scripts/chunk_docs_v5.py /kaggle/working/rag_clean/Docs /kaggle/working/rag_clean/Chunked
```

### Command (Local)

```bash
python scripts/chunk_docs_v5.py ./Docs ./Chunked
```

### What It Does

1. **Scans** the `Docs/` directory for documentation files
2. **Routes** content based on file type:
   - **Code files** (`.py`, `.js`, etc.) → Tree-sitter parser (AST-based chunking)
   - **Text files** (`.md`, `.txt`) → Semchunk (semantic chunking)
   - **PDFs** → Docling converter (layout-aware extraction)
3. **Enriches** chunks with metadata:
   - `hierarchy_path`: Full section path (e.g., "Introduction > Installation > Requirements")
   - `content_type`: Type classification (`code`, `prose`, `table`, `json`)
   - `search_keywords`: Extracted keywords from headings and content
   - `sparse_features`: BM25-style term weights for hybrid search
4. **Exports** to JSON files in `Chunked/` directory

### Expected Output Structure

```
Chunked/
├── sentence_transformers/
│   ├── Basic_encoding_mcp_repository_chunks.json
│   ├── Calculate_similarity_programming_documentation_chunks.json
│   ├── Core_Model_Types_programming_documentation_chunks.json
│   └── ... (more chunk files)
├── qdrant_ecosystem/
│   ├── qdrant_qdrant_1-introduction_chunks.json
│   ├── qdrant_qdrant_2-system-architecture_chunks.json
│   └── ...
└── docling/
    ├── docling_1-overview_chunks.json
    └── ...
```

### Example Chunk JSON

```json
{
  "text": "The `SentenceTransformer` class is the main interface...",
  "metadata": {
    "source_file": "Docs/sentence_transformers/basic_usage.md",
    "heading_text": "Basic Encoding",
    "hierarchy_path": "Getting Started > Basic Usage > Basic Encoding",
    "section_path": ["Getting Started", "Basic Usage", "Basic Encoding"],
    "content_type": "prose",
    "token_count": 245,
    "char_count": 1432,
    "search_keywords": ["SentenceTransformer", "encoding", "embeddings"],
    "qdrant_collection": "sentence_transformers",
    "chunk_hash": "a3f2e91b4c8d",
    "sparse_features": {
      "term_weights": [
        {"term": "sentencetransformer", "weight": 0.85},
        {"term": "encode", "weight": 0.72},
        {"term": "embedding", "weight": 0.68}
      ],
      "unique_terms": 87,
      "total_terms": 245,
      "weighting": "tf-normalized"
    }
  }
}
```

### Console Output (Chunking)

```
================================================================================
V5 DOCUMENT CHUNKING
================================================================================
Input Dir:  /kaggle/working/rag_clean/Docs
Output Dir: /kaggle/working/rag_clean/Chunked
================================================================================

Scanning for documentation files...
✓ Found 156 files to process

Processing files...
[1/156] sentence_transformers/basic_usage.md
  ✓ 12 chunks created (semchunk: 8, tree-sitter: 4)
[2/156] qdrant_ecosystem/introduction.md
  ✓ 8 chunks created (semchunk: 8)
...

================================================================================
CHUNKING COMPLETE
================================================================================
Total Files:     156
Total Chunks:    3,847
Output Dir:      /kaggle/working/rag_clean/Chunked
Processing Time: 45.3s
Average:         25.0 chunks/sec
================================================================================

Collections created:
  - sentence_transformers: 1,245 chunks
  - qdrant_ecosystem: 987 chunks
  - docling: 654 chunks
  - pydantic: 512 chunks
  - fast_docs: 449 chunks
```

### Key Metrics (Chunking)

- **Speed**: ~20-30 chunks/sec (depends on file complexity)
- **Memory**: ~200-500MB (for 4,000 chunks)
- **Chunk Size**: Average 200-400 tokens per chunk
- **Collections**: Auto-detected from directory structure

---

## Step 2: Embedding Generation

### Purpose
Convert text chunks into dense vector embeddings (and optionally sparse vectors) for semantic search in Qdrant.

### Command (Kaggle - Default)

```bash
# Cell 6: Embedding (uses full 1536D, no Matryoshka truncation)
python scripts/embed_collections_v5.py
```

### Command (Kaggle - With Matryoshka Truncation)

```bash
# Cell 6: Embedding with Matryoshka truncation (1536D → 1024D)
# WARNING: Only use with confirmed Matryoshka models (jina-embeddings-v4, jina-code-embeddings-1.5b)
python scripts/embed_collections_v5.py /kaggle/working/rag_clean/Chunked /kaggle/working/rag_clean/Embeddings jina-code-embeddings-1.5b 1024
```

### Command (Local)

```bash
python scripts/embed_collections_v5.py ./Chunked ./Embeddings nomic-coderank
```

### What It Does

1. **Loads** chunks from `Chunked/` directory
2. **Initializes** embedding model (e.g., `jina-code-embeddings-1.5b` = 1536D)
3. **Generates** embeddings in batches (GPU-optimized for Kaggle T4 x2)
4. **Optional**: Applies Matryoshka truncation (e.g., 1536D → 1024D for 33% size reduction)
5. **Optional**: Generates sparse embeddings (BM25-style) for hybrid search
6. **Exports** multiple formats:
   - **JSONL**: For Qdrant upload (includes metadata + vectors)
   - **NumPy**: For fast loading (`.npy` arrays)
   - **FAISS**: For local similarity search testing
   - **Upload Script**: Auto-generated Python script for local Qdrant

### Expected Output Structure

```
Embeddings/
├── ultimate_embeddings_v4_embeddings.npy        # Primary dense vectors
├── ultimate_embeddings_v4_qdrant.jsonl          # Qdrant upload format
├── ultimate_embeddings_v4_sparse.jsonl          # Sparse vectors (optional)
├── ultimate_embeddings_v4_metadata.json         # All chunk metadata
├── ultimate_embeddings_v4_texts.json            # All chunk texts
├── ultimate_embeddings_v4_stats.json            # Processing statistics
├── ultimate_embeddings_v4_index.faiss           # FAISS index for testing
└── ultimate_embeddings_v4_upload_script.py      # Auto-generated upload script
```

### Example JSONL Entry (Qdrant Format)

```json
{
  "id": 0,
  "vectors": {
    "jina-code-embeddings-1.5b": [0.234, -0.112, 0.567, ...],  // 1536D or truncated
    "bge-small": [0.123, 0.445, -0.234, ...]                    // Optional companion
  },
  "payload": {
    "text_preview": "The `SentenceTransformer` class is the main...",
    "full_text_length": 1432,
    "source_file": "Docs/sentence_transformers/basic_usage.md",
    "hierarchy_path": "Getting Started > Basic Usage > Basic Encoding",
    "content_type": "prose",
    "token_count": 245,
    "search_keywords": ["SentenceTransformer", "encoding", "embeddings"],
    "qdrant_collection": "sentence_transformers",
    "model_info": {
      "name": "jina-code-embeddings-1.5b",
      "hf_model_id": "jinaai/jina-code-embeddings-1.5b",
      "dimension": 1536,
      "version": "v4"
    },
    "sparse_vector": {
      "indices": [12453, 45821, 89342, ...],
      "values": [0.85, 0.72, 0.68, ...],
      "tokens": ["sentencetransformer", "encode", "embedding", ...],
      "stats": {
        "weight_norm": 3.42,
        "unique_terms": 87,
        "total_terms": 245
      }
    },
    "kaggle_export_timestamp": "2025-01-20T03:00:00",
    "primary_vector_name": "jina-code-embeddings-1.5b",
    "dense_vector_names": ["jina-code-embeddings-1.5b", "bge-small"]
  }
}
```

### Console Output (Embedding)

```
================================================================================
V5 EMBEDDING GENERATION
================================================================================
Chunks Dir:      /kaggle/working/rag_clean/Chunked
Output Dir:      /kaggle/working/rag_clean/Embeddings
Model:           jina-code-embeddings-1.5b (1536D)
Matryoshka Dim:  None (full 1536D, no truncation)
================================================================================

Initializing embedder...
Selected model: jina-code-embeddings-1.5b (1536D)
Kaggle environment detected - optimizing for T4 x2
Detected 2 GPU(s)
  GPU 0: Tesla T4 (15.8GB)
  GPU 1: Tesla T4 (15.8GB)
Optimal batch size: 32 (16 per GPU)
✓ Embedder initialized

Loading chunks from: /kaggle/working/rag_clean/Chunked
✓ Loaded 3847 chunks
  Collections: 5
  Memory: 245.3MB
  Sparse vectors: 3847

Generating embeddings (this may take a while)...
Processing batch 1/121 (32 chunks)
Batch 1: 45.2 chunks/sec, Progress: 0.8%
...
Processing batch 121/121 (7 chunks)
Batch 121: 48.1 chunks/sec, Progress: 100.0%

✓ Embeddings generated in 85.2s
  Total: 3847
  Dimension: 1536D
  Speed: 45.1 chunks/sec
  Memory: 23.8MB

Exporting to Qdrant format...
✓ Export complete
  Collection: sentence_transformers_v4_jina_code_embeddings_1_5b
  Files exported: 8
  JSONL: ultimate_embeddings_v4_qdrant.jsonl
  NumPy: ultimate_embeddings_v4_embeddings.npy
  Upload Script: ultimate_embeddings_v4_upload_script.py

Creating download package...
✓ Package created: /kaggle/working/embeddings_v5.zip

================================================================================
EMBEDDING COMPLETE
================================================================================
Total Chunks:    3847
Embedding Dim:   1536D
Processing Time: 85.2s
Collection Name: sentence_transformers_v4_jina_code_embeddings_1_5b

📥 Download embeddings_v5.zip from Kaggle Output panel
📤 Then run the upload script on your local machine
================================================================================
```

### Key Metrics (Embedding)

**Performance (Kaggle T4 x2 GPU)**:
- **Speed**: 40-50 chunks/sec (for 1536D model)
- **Memory**: ~25-30MB per 1,000 embeddings (fp32)
- **Processing Time**: ~80-100s for 4,000 chunks
- **GPU Utilization**: 70-80% on both T4s

**Performance (Local CPU)**:
- **Speed**: 5-10 chunks/sec
- **Memory**: ~25-30MB per 1,000 embeddings
- **Processing Time**: ~400-800s for 4,000 chunks

**File Sizes**:
- **JSONL**: ~15-20MB per 1,000 chunks (with metadata)
- **NumPy**: ~6-8MB per 1,000 chunks (1536D, fp32)
- **FAISS**: ~6-8MB per 1,000 chunks
- **Total**: ~30-40MB per 1,000 chunks

---

## Step 3: Upload to Qdrant

### Purpose
Upload embeddings and metadata to your local Qdrant instance for semantic search.

### Prerequisites

1. **Qdrant running locally**:
   ```bash
   docker-compose up -d
   ```

2. **Download embeddings from Kaggle**:
   - Click "Output" panel in Kaggle
   - Download `embeddings_v5.zip`
   - Extract to local directory

### Command (Auto-Generated Script)

```bash
# Run the auto-generated upload script
python ultimate_embeddings_v4_upload_script.py
```

### What It Does

1. **Loads** exported embeddings (NumPy, JSONL, metadata)
2. **Connects** to local Qdrant (localhost:6333)
3. **Creates** collection with:
   - **Named vectors**: Primary + companion models
   - **Sparse vectors**: Optional BM25-style vectors
   - **HNSW indexing**: Optimized for similarity search
   - **Scalar quantization**: int8 compression for memory efficiency
4. **Uploads** points in batches (1,000 per batch)
5. **Verifies** upload with test search

### Console Output (Upload)

```
================================================================================
QDRANT UPLOAD - ULTIMATE KAGGLE EMBEDDER V4
================================================================================
Connected to Qdrant at localhost:6333

Loading exported data...
Loaded 3847 embeddings for jina-code-embeddings-1.5b (1536D)
Loaded 3847 embeddings for bge-small (384D)
Sparse sidecar detected: ultimate_embeddings_v4_sparse.jsonl

Creating collection: sentence_transformers_v4_jina_code_embeddings_1_5b
Collection created with named vectors:
  - jina-code-embeddings-1.5b: 1536D (COSINE)
  - bge-small: 384D (COSINE)

Preparing points for upload...
Uploading 3847 points in 4 batches...
Uploaded batch 1/4 (1000 points)
Uploaded batch 2/4 (1000 points)
Uploaded batch 3/4 (1000 points)
Uploaded batch 4/4 (847 points)

Upload complete; collection has 3847 points

Testing search...
Search test successful; found 5 results
Top result: "The `SentenceTransformer` class..." (score: 0.923)

Embeddings are ready for use in collection: sentence_transformers_v4_jina_code_embeddings_1_5b
================================================================================
```

### Verify in Qdrant Console

Visit http://localhost:6333/dashboard and check:
- **Collections**: Should see your collection listed
- **Points Count**: Should match total chunks (e.g., 3,847)
- **Vectors**: Should show named vectors (primary + companions)

### Test Search (Python)

```python
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# Search using primary vector
results = client.search(
    collection_name="sentence_transformers_v4_jina_code_embeddings_1_5b",
    query_vector=(
        "jina-code-embeddings-1.5b",
        [0.123, -0.456, ...]  # Your query embedding
    ),
    limit=5
)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Text: {result.payload['text_preview']}")
    print(f"Source: {result.payload['source_file']}\n")
```

---

## Troubleshooting

### Chunking Issues

**Problem**: No chunks generated
- **Check**: Verify `Docs/` directory exists and contains files
- **Check**: File extensions match expected types (`.md`, `.py`, etc.)
- **Solution**: Add `--verbose` flag to see detailed processing logs

**Problem**: Chunks too large/small
- **Check**: Model's `max_tokens` parameter in chunker config
- **Solution**: Adjust `chunk_size` and `chunk_overlap` in script

### Embedding Issues

**Problem**: Out of memory (GPU)
- **Check**: Batch size is too large for available VRAM
- **Solution**: Reduce `base_batch_size` in GPU config
- **Solution**: Use `matryoshka_dim` to reduce vector size

**Problem**: Slow embedding speed
- **Check**: Running on CPU instead of GPU
- **Solution**: Verify CUDA is available: `torch.cuda.is_available()`
- **Solution**: Use smaller model (e.g., `all-miniLM-l6`)

**Problem**: Matryoshka warning
- **Warning**: `⚠️ MATRYOSHKA WARNING: Model 'nomic-coderank' does not have confirmed support`
- **Meaning**: Truncation may degrade quality for this model
- **Solution**: Use `matryoshka_dim=None` for full dimension OR switch to confirmed model

### Upload Issues

**Problem**: Connection refused
- **Check**: Qdrant is running: `docker ps | grep qdrant`
- **Solution**: Start Qdrant: `docker-compose up -d`

**Problem**: Collection already exists
- **Solution**: Delete existing: `client.delete_collection("collection_name")`
- **Or**: Modify upload script to skip creation

---

## Summary

**Complete Pipeline** (Kaggle → Local):

```bash
# KAGGLE: Cell 5 - Chunking
python scripts/chunk_docs_v5.py /kaggle/working/rag_clean/Docs /kaggle/working/rag_clean/Chunked

# KAGGLE: Cell 6 - Embedding
python scripts/embed_collections_v5.py

# KAGGLE: Download embeddings_v5.zip

# LOCAL: Upload to Qdrant
python ultimate_embeddings_v4_upload_script.py
```

**Expected Timeline**:
- **Chunking**: 1-2 minutes (for 150 files)
- **Embedding**: 1-2 minutes (for 4,000 chunks on T4 x2)
- **Upload**: 30-60 seconds (for 4,000 points)
- **Total**: ~3-5 minutes end-to-end

**Expected Results**:
- **Chunks**: 3,000-5,000 (depends on documentation size)
- **Embeddings**: Same as chunks, stored in multiple formats
- **Qdrant Points**: Same as chunks, ready for semantic search
- **Search Quality**: High-quality semantic search with metadata filtering

---

**Next Steps**: See [V5_COMPLETE_SUMMARY.md](V5_COMPLETE_SUMMARY.md) for advanced features and [MATRYOSHKA_EMBEDDINGS_GUIDE.md](notes/MATRYOSHKA_EMBEDDINGS_GUIDE.md) for dimension optimization.