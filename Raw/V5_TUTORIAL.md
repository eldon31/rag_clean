# V5 RAG System Tutorial

**Phase 2 Track 5 - Task 5.3**

Step-by-step guide to using the Enhanced Ultimate Chunker V5 RAG system.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Chunking](#basic-chunking)
3. [Multi-Model Embeddings](#multi-model-embeddings)
4. [Sparse Vector Generation](#sparse-vector-generation)
5. [LlamaIndex Integration](#llamaindex-integration)
6. [Qdrant Upload](#qdrant-upload)
7. [Advanced Features](#advanced-features)
8. [Best Practices](#best-practices)

---

## Getting Started

### Installation

```bash
# Install core dependencies
pip install tiktoken numpy scikit-learn

# Install optional frameworks (recommended)
pip install llama-index sentence-transformers
pip install tree-sitter tree-sitter-languages
pip install semchunk
```

### Quick Start

```python
from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

# Initialize chunker
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b"
)

# Process a document
chunks = chunker.process_file_smart("document.md")
print(f"Generated {len(chunks)} chunks")
```

---

## Basic Chunking

### Example 1: Single Document Processing

```python
from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

# Initialize with specific model
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",  # 32,768 max tokens
    safety_margin=0.8,  # Use 80% = 26,214 tokens per chunk
    use_tree_sitter=True,  # Enable code chunking
    use_semchunk=True  # Enable semantic boundaries
)

# Process markdown file
chunks = chunker.process_file_smart(
    "docs/README.md",
    output_dir="output/chunks",
    auto_detect=True  # Auto-detect content type
)

# Inspect chunks
for i, chunk in enumerate(chunks[:3]):
    print(f"\n{'='*60}")
    print(f"Chunk {i + 1}")
    print(f"{'='*60}")
    print(f"Tokens: {chunk['metadata']['token_count']}")
    print(f"Quality: {chunk['advanced_scores']['overall']:.3f}")
    print(f"Content Type: {chunk['metadata']['content_type']}")
    print(f"\nText preview:")
    print(chunk['text'][:200] + "...")
```

**Output:**
```
============================================================
Chunk 1
============================================================
Tokens: 512
Quality: 0.756
Content Type: workflow_documentation

Text preview:
# Getting Started

This guide will help you get started with the RAG system...
```

### Example 2: Batch Directory Processing

```python
# Process entire documentation directory
summary = chunker.process_directory_smart(
    input_dir="docs/",
    output_dir="output/chunks",
    file_extensions=[".md", ".txt", ".rst"]
)

print(f"\n{'='*60}")
print("Processing Summary")
print(f"{'='*60}")
print(f"Files processed: {summary['processed_files']}")
print(f"Total chunks: {summary['total_chunks']}")
print(f"Processing time: {summary['processing_time']:.2f}s")
print(f"\nContent types:")
for ctype, count in summary['content_types'].items():
    print(f"  {ctype}: {count} files")
```

### Example 3: Model Validation

```python
# Validate chunks are within model limits
validation = chunker.validate_chunks(chunks)

print(f"\n{'='*60}")
print("Validation Report")
print(f"{'='*60}")
print(f"Total chunks: {validation['total_chunks']}")
print(f"Valid chunks: {validation['valid_chunks']}")
print(f"Invalid chunks: {validation['invalid_chunks']}")
print(f"Status: {'✓ PASSED' if validation['validation_passed'] else '✗ FAILED'}")

if not validation['validation_passed']:
    print(f"\nOversized chunks:")
    for detail in validation['oversized_chunk_details']:
        print(f"  Chunk {detail['chunk_index']}: "
              f"{detail['estimated_tokens']} tokens "
              f"(+{detail['overflow']} over limit)")
```

---

## Multi-Model Embeddings

### Example 4: Generate Embeddings from Multiple Models

```python
from processor.llamaindex_embedder_v5 import MultiModelEmbedder

# Initialize embedder with multiple models
embedder = MultiModelEmbedder(
    model_names=[
        "jinaai/jina-embeddings-v2-base-code",  # Code-specialized
        "BAAI/bge-m3"  # Multilingual
    ],
    device="cpu",  # or "cuda" if GPU available
    batch_size=32
)

# Get texts from chunks
texts = [chunk['text'] for chunk in chunks]

# Generate embeddings
embeddings = embedder.get_multi_model_embeddings(texts)

# Access embeddings
jina_embeddings = embeddings["jinaai/jina-embeddings-v2-base-code"]
bge_embeddings = embeddings["BAAI/bge-m3"]

print(f"\nJina embeddings shape: {jina_embeddings.shape}")
print(f"BGE embeddings shape: {bge_embeddings.shape}")
```

### Example 5: Matryoshka Dimension Truncation

```python
# Initialize with Matryoshka truncation
embedder = MultiModelEmbedder(
    model_names=["jinaai/jina-embeddings-v2-base-code"],
    matryoshka_dims={
        "jinaai/jina-embeddings-v2-base-code": 1024  # Truncate to 1024D
    }
)

embeddings = embedder.get_multi_model_embeddings(texts[:10])
print(f"Truncated dimension: {embeddings['jinaai/jina-embeddings-v2-base-code'].shape[1]}D")
```

---

## Sparse Vector Generation

### Example 6: BM25 Sparse Vectors

```python
from processor.sparse_embedder_v5 import BM25SparseEncoder

# Initialize BM25 encoder
sparse_encoder = BM25SparseEncoder(
    k1=1.5,  # Term frequency saturation
    b=0.75,  # Length normalization
    top_k=20  # Keep top 20 terms
)

# Fit on corpus
corpus_texts = [chunk['text'] for chunk in chunks]
sparse_encoder.fit(corpus_texts)

# Encode texts
sparse_vectors = sparse_encoder.encode(corpus_texts[:5])

# Inspect sparse vector
sv = sparse_vectors[0]
print(f"\nSparse Vector Example:")
print(f"Non-zero terms: {len(sv['indices'])}")
print(f"Top 5 terms: {sv['tokens'][:5]}")
print(f"Top 5 weights: {[f'{v:.3f}' for v in sv['values'][:5]]}")
```

**Output:**
```
Sparse Vector Example:
Non-zero terms: 20
Top 5 terms: ['algorithm', 'learning', 'neural', 'model', 'training']
Top 5 weights: ['0.856', '0.743', '0.621', '0.589', '0.512']
```

### Example 7: Hybrid Sparse Encoding

```python
from processor.sparse_embedder_v5 import HybridSparseEncoder

# Initialize hybrid encoder (BM25 + attention)
hybrid_encoder = HybridSparseEncoder(
    use_bm25=True,
    use_attention=False,  # Set True if GPU available
    bm25_weight=0.7,
    attention_weight=0.3,
    combination_strategy="weighted_sum"
)

# Fit and encode
hybrid_encoder.fit(corpus_texts)
hybrid_vectors = hybrid_encoder.encode(corpus_texts[:5])

print(f"Generated {len(hybrid_vectors)} hybrid sparse vectors")
```

---

## LlamaIndex Integration

### Example 8: Create LlamaIndex Index

```python
from llama_index.core import Document, VectorStoreIndex
from processor.llamaindex_chunker_v5 import HierarchicalNodeParser

# Initialize node parser
node_parser = HierarchicalNodeParser(
    chunker=chunker,
    include_metadata=True
)

# Create documents
documents = [
    Document(text=open("docs/README.md").read()),
    Document(text=open("docs/TUTORIAL.md").read())
]

# Parse to nodes
nodes = node_parser.get_nodes_from_documents(documents)

print(f"Generated {len(nodes)} nodes")

# Create index
index = VectorStoreIndex(nodes)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("How do I install the system?")

print(f"\nQuery: How do I install the system?")
print(f"Response: {response}")
```

### Example 9: Code-Specific Chunking

```python
from processor.llamaindex_chunker_v5 import TreeSitterNodeParser

# Initialize Tree-sitter parser
code_parser = TreeSitterNodeParser(
    chunker=chunker,
    language="python"
)

# Parse Python file
code_doc = Document(text=open("processor/chunker.py").read())
code_nodes = code_parser.get_nodes_from_documents([code_doc])

print(f"Extracted {len(code_nodes)} code nodes")

# Inspect node
node = code_nodes[0]
print(f"\nNode text preview:")
print(node.text[:200])
print(f"\nMetadata: {node.metadata}")
```

---

## Qdrant Upload

### Example 10: Prepare Points for Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")

# Create collection with named vectors
collection_name = "documents_v5"
client.create_collection(
    collection_name=collection_name,
    vectors_config={
        "jina": VectorParams(size=768, distance=Distance.COSINE),
        "bge": VectorParams(size=1024, distance=Distance.COSINE)
    }
)

# Prepare points
points = []
for i, chunk in enumerate(chunks):
    # Get embeddings
    text = chunk['text']
    embeddings = embedder.get_multi_model_embeddings([text])
    sparse_vector = sparse_encoder.encode([text])[0]
    
    # Create point
    point = PointStruct(
        id=i,
        vector={
            "jina": embeddings["jinaai/jina-embeddings-v2-base-code"][0].tolist(),
            "bge": embeddings["BAAI/bge-m3"][0].tolist()
        },
        payload={
            **chunk['metadata'],
            "text": text,
            "sparse_indices": sparse_vector['indices'],
            "sparse_values": sparse_vector['values']
        }
    )
    points.append(point)

# Upload to Qdrant
client.upsert(collection_name=collection_name, points=points)
print(f"✓ Uploaded {len(points)} points to Qdrant")
```

### Example 11: Hybrid Search Query

```python
from qdrant_client.models import SearchRequest, NamedVector

# Query text
query = "How to implement machine learning algorithms?"

# Generate query embeddings
query_dense = embedder.get_multi_model_embeddings([query])
query_sparse = sparse_encoder.encode([query])[0]

# Hybrid search
results = client.search(
    collection_name=collection_name,
    query_vector=NamedVector(
        name="jina",
        vector=query_dense["jinaai/jina-embeddings-v2-base-code"][0].tolist()
    ),
    limit=5
)

print(f"\nTop 5 Results for: '{query}'")
for i, result in enumerate(results):
    print(f"\n{i+1}. Score: {result.score:.3f}")
    print(f"   Text: {result.payload['text'][:100]}...")
    print(f"   Source: {result.payload['source_filename']}")
```

---

## Advanced Features

### Monitoring Batch Progress

The batch embedder surfaces deterministic progress metadata for both the CLI and the collection summary JSON generated by `scripts/embed_collections_v5.py`.

- **CLI preview:** tqdm descriptions now display `Batches(<primary_source>)` while a batch encodes. After completion the script prints a short summary showing how many progress events were captured along with the latest labels, models, and devices. When running in "quiet" mode (logging level ≥ `WARNING`), the structured JSON still contains all telemetry even though the console preview is suppressed.
- **Summary JSON:** every collection entry includes an optional `batch_progress` array with `batch_index`, `total_batches`, `label`, `model`, `device`, and `status`. Consumers can correlate these records with the CLI output or dashboards. See `Docs/EMBEDDING_SUMMARY_SCHEMA.md` for field definitions.
- **Troubleshooting:** retries triggered by adaptive batching or CPU fallbacks append events marked with `status="failed"` alongside retry counters so you can pinpoint bottlenecks without sifting through raw logs.

These additions are backwards compatible—pipelines that ignore `batch_progress` continue to function unmodified while operators gain richer runtime observability.

### Example 12: Docling PDF Processing

```python
# Initialize with Docling
chunker_pdf = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    use_docling=True  # Enable Docling
)

# Process PDF with table/figure extraction
chunks_pdf = chunker_pdf.process_docling_document(
    "document.pdf",
    preserve_tables=True,
    extract_figures=True,
    resolve_references=True
)

# Check for tables
table_chunks = [c for c in chunks_pdf if c['metadata'].get('is_table_chunk')]
figure_chunks = [c for c in chunks_pdf if c['metadata'].get('is_figure_chunk')]

print(f"Total chunks: {len(chunks_pdf)}")
print(f"Table chunks: {len(table_chunks)}")
print(f"Figure chunks: {len(figure_chunks)}")
```

### Example 13: Quality Filtering

```python
# Filter chunks by quality score
high_quality_chunks = [
    chunk for chunk in chunks
    if chunk['advanced_scores']['overall'] >= 0.7
]

print(f"High quality chunks: {len(high_quality_chunks)}/{len(chunks)}")

# Group by content type
from collections import defaultdict
by_content_type = defaultdict(list)
for chunk in chunks:
    content_type = chunk['metadata']['content_type']
    by_content_type[content_type].append(chunk)

for ctype, cchunks in by_content_type.items():
    avg_quality = sum(c['advanced_scores']['overall'] for c in cchunks) / len(cchunks)
    print(f"{ctype}: {len(cchunks)} chunks, avg quality: {avg_quality:.3f}")
```

### Example 14: Custom Strategy Override

```python
# Use specific chunking strategy
chunks_precise = chunker.process_file_smart(
    "document.md",
    strategy_override="hierarchical_precise"  # Smaller, tighter chunks
)

chunks_context = chunker.process_file_smart(
    "document.md",
    strategy_override="hierarchical_context"  # Larger, more context
)

print(f"Precise strategy: {len(chunks_precise)} chunks")
print(f"Context strategy: {len(chunks_context)} chunks")
```

---

## Best Practices

### 1. Model Selection

```python
# For code-heavy documents
chunker_code = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",  # 32K tokens
    use_tree_sitter=True
)

# For general text
chunker_text = EnhancedUltimateChunkerV5Unified(
    target_model="bge-m3",  # 8K tokens
    use_semchunk=True
)

# For small models (edge deployment)
chunker_small = EnhancedUltimateChunkerV5Unified(
    target_model="all-miniLM-l6",  # 256 tokens
    safety_margin=0.9  # Conservative chunking
)
```

### 2. Error Handling

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Process with error handling
failed_files = []
successful_chunks = []

for file_path in file_list:
    try:
        chunks = chunker.process_file_smart(file_path)
        validation = chunker.validate_chunks(chunks)
        
        if validation['validation_passed']:
            successful_chunks.extend(chunks)
        else:
            logging.warning(f"Validation failed for {file_path}")
            
    except Exception as e:
        logging.error(f"Failed to process {file_path}: {e}")
        failed_files.append(file_path)

print(f"✓ Successfully processed: {len(successful_chunks)} chunks")
print(f"✗ Failed files: {len(failed_files)}")
```

### 3. Performance Optimization

```python
# For maximum speed (disable frameworks)
fast_chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    use_tree_sitter=False,  # Disable
    use_semchunk=False,  # Disable
    enable_semantic_scoring=False  # Disable
)

# For maximum quality (enable all features)
quality_chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    use_tree_sitter=True,
    use_semchunk=True,
    enable_semantic_scoring=True  # Requires model download
)
```

### 4. Memory Management

```python
import gc

# Process large datasets in batches
batch_size = 100
all_chunks = []

for i in range(0, len(file_list), batch_size):
    batch_files = file_list[i:i+batch_size]
    
    # Process batch
    batch_chunks = []
    for file_path in batch_files:
        chunks = chunker.process_file_smart(file_path)
        batch_chunks.extend(chunks)
    
    # Process embeddings immediately
    batch_embeddings = embedder.get_multi_model_embeddings(
        [c['text'] for c in batch_chunks]
    )
    
    # Upload to Qdrant (or save)
    # ... upload code ...
    
    # Clear memory
    del batch_embeddings
    gc.collect()
    
    print(f"Processed batch {i//batch_size + 1}")
```

---

## Next Steps

1. **Read API Reference**: `docs/API_REFERENCE_V5.md`
2. **Review Deployment Guide**: `docs/V5_DEPLOYMENT_GUIDE.md`
3. **Check Model Configurations**: `notes/V5_MODEL_CONFIGURATIONS.md`
4. **Run Integration Tests**: `python -m pytest tests/test_v5_integration.py`
5. **Benchmark Performance**: `python benchmarks/v4_vs_v5_comparison.py`

---

## Troubleshooting

**Q: ImportError for optional dependencies?**
```python
# Check which frameworks are available
import importlib

frameworks = ['tree_sitter', 'semchunk', 'docling', 'llama_index']
for fw in frameworks:
    try:
        importlib.import_module(fw)
        print(f"✓ {fw} available")
    except ImportError:
        print(f"✗ {fw} not installed")
```

**Q: Chunks exceeding token limits?**
```python
# Increase safety margin
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    safety_margin=0.6  # Use only 60% of max tokens
)
```

**Q: Poor chunk quality?**
```python
# Adjust quality thresholds
config = ChunkerConfig(
    quality_thresholds={
        "min_semantic_score": 0.50,  # Lower threshold
        "min_structural_score": 0.55,
        "min_retrieval_quality": 0.45
    },
    fallback_promotion_ratio=0.30  # Promote more chunks
)
```

---

**Last Updated**: 2025-01-20  
**Version**: V5 Unified Phase 2  
**Status**: Production Ready