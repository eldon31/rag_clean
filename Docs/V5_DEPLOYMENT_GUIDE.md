# V5 RAG System Deployment Guide

**Phase 2 Track 5 - Task 5.2**

Complete deployment guide for the Enhanced Ultimate Chunker V5 RAG system.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Deployment](#basic-deployment)
5. [Advanced Deployment](#advanced-deployment)
6. [Production Deployment](#production-deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.9+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB for models and data
- **CPU**: 4 cores recommended

### Recommended for Production
- **Python**: 3.10+
- **RAM**: 16GB+
- **Storage**: 50GB+ (SSD preferred)
- **CPU**: 8+ cores
- **GPU**: Optional, for attention-based sparse encoding

### Dependencies

**Core Dependencies:**
```
tiktoken>=0.5.0
numpy>=1.24.0
scikit-learn>=1.3.0
```

**Optional Framework Dependencies:**
```
# LlamaIndex integration
llama-index>=0.9.0

# Tree-sitter (code chunking)
tree-sitter>=0.20.0
tree-sitter-languages>=1.8.0

# Semchunk (semantic boundaries)
semchunk>=0.2.0

# Docling (PDF/Office conversion)
docling>=1.0.0

# Sentence Transformers (embeddings)
sentence-transformers>=2.2.0
transformers>=4.30.0
torch>=2.0.0
```

---

## Installation

### 1. Basic Installation

```bash
# Clone repository
git clone https://github.com/your-org/rag-system.git
cd rag-system

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install core dependencies
pip install -r requirements.txt
```

### 2. Install Optional Frameworks

**For Full Feature Set:**
```bash
pip install llama-index sentence-transformers torch
pip install tree-sitter tree-sitter-languages
pip install semchunk docling
```

**For Minimal Setup (no external frameworks):**
```bash
# Only core dependencies - uses basic chunking
pip install tiktoken numpy scikit-learn
```

### 3. Verify Installation

```python
from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

# Test initialization
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b"
)
print("✓ V5 chunker initialized successfully")
```

---

## Configuration

### 1. Model Registry Configuration

Edit `processor/ultimate_embedder/config.py` to add custom models (the legacy `processor/kaggle_ultimate_embedder_v4.py` module now re-exports from the modular package and emits a deprecation warning):

```python
KAGGLE_OPTIMIZED_MODELS = {
    "custom-model": ModelConfig(
        model_name="custom-model",
        hf_model_id="your-org/custom-model",
        max_tokens=8192,
        vector_dim=768,
        recommended_batch_size=32,
        backend="pytorch",
        memory_efficient=True
    )
}
```

### 2. Chunker Configuration

```python
from processor.enhanced_ultimate_chunker_v5_unified import ChunkerConfig

config = ChunkerConfig(
    # Model settings
    target_model="jina-code-embeddings-1.5b",
    chunk_size_tokens=None,  # Auto-calculated from model
    safety_margin=0.8,  # Use 80% of model's max tokens
    
    # Framework integration
    use_docling=False,  # PDF/Office conversion
    use_tree_sitter=True,  # Code chunking
    use_semchunk=True,  # Semantic boundaries
    
    # Quality control
    enable_semantic_scoring=False,  # Requires model download
    quality_thresholds={
        "min_semantic_score": 0.55,
        "min_structural_score": 0.60,
        "min_retrieval_quality": 0.50
    },
    
    # Metadata enrichment
    extract_keywords=True,
    generate_sparse_features=True,
    classify_content_type=True,
    
    # Output
    output_dir="Chunked",
    preserve_hierarchy=True
)
```

### 3. Ultimate Embedder Modular Layout

The Kaggle V4 embedder now lives in the `processor/ultimate_embedder/` package with clear service boundaries so each concern can evolve independently. The most important modules are:

- `core.py` – Orchestrates the end-to-end batch run, wiring the helper services together while preserving the legacy facade API.
- `chunk_loader.py` – Streams chunk batches from disk, enriches metadata, and validates chunk counts before encoding.
- `model_manager.py` – Resolves model configs, handles ensemble rotation, and manages device placement plus caching for warmed models.
- `backend_encoder.py` – Provides a thin adapter over the active embedding backend (Transformers, ONNX, TensorRT) used by the batch runner.
- `batch_runner.py` – Coordinates adaptive batching via `AdaptiveBatchController`, runs the ensemble aggregation loop, captures telemetry, and retries failed batches when safe.
- `sparse_pipeline.py` & `rerank_pipeline.py` – Build optional sparse vectors and reranker scores on demand without bloating the core loop.
- `export_runtime.py` & `monitoring.py` – Emit export artifacts, archive bundles, and runtime telemetry; `export.py` remains as a shim for old imports.
- `telemetry.py` – Centralises logging helpers and GPU snapshots consumed by the summary writer.

When extending the embedder, prefer adding a new helper module or injecting alternate implementations via the `UltimateKaggleEmbedderV4` constructor. Direct changes to `core.py` should remain thin wrappers so the executable-line guard stays green and responsibilities remain clear.

> **Guardrail:** `tests/test_core_line_limit.py` enforces that `core.py` stays under 800 executable lines using the baseline stored at `openspec/changes/refactor-ultimate-embedder-core/artifacts/core_executable_line_baseline.json`. Update the baseline after meaningful refactors, but only once the executable line count remains below the cap.

---

## Basic Deployment

### Single File Processing

```python
from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

# Initialize chunker
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    use_tree_sitter=True,
    use_semchunk=True
)

# Process single file
chunks = chunker.process_file_smart(
    "documents/example.md",
    output_dir="output/chunks",
    auto_detect=True
)

print(f"Generated {len(chunks)} chunks")

# Validate chunks
validation = chunker.validate_chunks(chunks)
if validation["validation_passed"]:
    print("✓ All chunks within token limits")
```

### Batch Directory Processing

```python
# Process entire directory
summary = chunker.process_directory_smart(
    input_dir="documents/",
    output_dir="output/chunks",
    file_extensions=[".md", ".txt", ".py"]
)

print(f"Processed {summary['processed_files']} files")
print(f"Total chunks: {summary['total_chunks']}")
print(f"Time: {summary['processing_time']:.2f}s")
```

---

## Advanced Deployment

### 1. LlamaIndex Integration

```python
from processor.llamaindex_chunker_v5 import HierarchicalNodeParser
from llama_index.core import VectorStoreIndex

# Initialize node parser
node_parser = HierarchicalNodeParser(
    chunker=chunker,
    include_metadata=True
)

# Create document and parse
from llama_index.core import Document
doc = Document(text=open("document.md").read())
nodes = node_parser.get_nodes_from_documents([doc])

# Create index
index = VectorStoreIndex(nodes)
query_engine = index.as_query_engine()

# Query
response = query_engine.query("What are the key features?")
print(response)
```

### 2. Multi-Model Embeddings

```python
from processor.llamaindex_embedder_v5 import MultiModelEmbedder

# Initialize embedder
embedder = MultiModelEmbedder(
    model_names=[
        "jinaai/jina-embeddings-v2-base-code",
        "BAAI/bge-m3"
    ]
)

# Generate embeddings
texts = [c["text"] for c in chunks]
embeddings = embedder.get_multi_model_embeddings(texts)

# Qdrant format
named_vectors = embedder.get_named_vectors_for_qdrant(texts)
```

### 3. Sparse Vector Generation

```python
from processor.sparse_embedder_v5 import HybridSparseEncoder

# Initialize hybrid encoder
sparse_encoder = HybridSparseEncoder(
    use_bm25=True,
    use_attention=False,  # Set True if GPU available
    bm25_weight=0.7,
    attention_weight=0.3
)

# Fit on corpus
sparse_encoder.fit(texts)

# Generate sparse vectors
sparse_vectors = sparse_encoder.encode(texts)

# Qdrant point format
points = []
for i, (chunk, sparse_vec) in enumerate(zip(chunks, sparse_vectors)):
    points.append({
        "id": i,
        "vector": {
            "dense": embeddings["jina"][i].tolist(),
            "sparse": {
                "indices": sparse_vec["indices"],
                "values": sparse_vec["values"]
            }
        },
        "payload": chunk["metadata"]
    })
```

---

## Production Deployment

### 1. Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY processor/ ./processor/
COPY scripts/ ./scripts/

# Set environment
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false

# Run chunker
CMD ["python", "scripts/chunk_docs_v5.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  chunker:
    build: .
    volumes:
      - ./documents:/app/documents
      - ./output:/app/output
    environment:
      - TARGET_MODEL=jina-code-embeddings-1.5b
      - USE_TREE_SITTER=true
      - USE_SEMCHUNK=true
    mem_limit: 8g
    cpus: 4
```

**Build and Run:**
```bash
docker-compose build
docker-compose up
```

### 2. Kubernetes Deployment

**k8s-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-chunker-v5
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-chunker
  template:
    metadata:
      labels:
        app: rag-chunker
    spec:
      containers:
      - name: chunker
        image: your-registry/rag-chunker-v5:latest
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        env:
        - name: TARGET_MODEL
          value: "jina-code-embeddings-1.5b"
        - name: USE_TREE_SITTER
          value: "true"
        - name: USE_SEMCHUNK
          value: "true"
        volumeMounts:
        - name: documents
          mountPath: /app/documents
        - name: output
          mountPath: /app/output
      volumes:
      - name: documents
        persistentVolumeClaim:
          claimName: documents-pvc
      - name: output
        persistentVolumeClaim:
          claimName: output-pvc
```

### 3. Production Script

**scripts/production_chunker.py:**
```python
#!/usr/bin/env python3
"""Production chunking script with error handling and logging"""

import logging
import sys
from pathlib import Path
from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chunker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize chunker
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            use_tree_sitter=True,
            use_semchunk=True,
            enable_semantic_scoring=False
        )
        
        # Process documents
        summary = chunker.process_directory_smart(
            input_dir="documents/",
            output_dir="output/chunks",
            file_extensions=[".md", ".txt", ".py", ".rst"]
        )
        
        logger.info(f"✓ Processing complete: {summary['processed_files']} files, "
                   f"{summary['total_chunks']} chunks")
        
        return 0
    
    except Exception as e:
        logger.error(f"✗ Processing failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## Monitoring & Maintenance

### 1. Health Checks

```python
def health_check(chunker):
    """Verify system health"""
    try:
        # Test chunking
        test_text = "# Test\nThis is a test document."
        test_file = Path("test.md")
        test_file.write_text(test_text)
        
        chunks = chunker.process_file_smart(str(test_file))
        validation = chunker.validate_chunks(chunks)
        
        test_file.unlink()
        
        return {
            "status": "healthy",
            "chunks_generated": len(chunks),
            "validation_passed": validation["validation_passed"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

### 2. Performance Monitoring

```python
import time
import tracemalloc

def monitor_performance(chunker, file_path):
    """Monitor chunking performance"""
    tracemalloc.start()
    start_time = time.time()
    
    chunks = chunker.process_file_smart(file_path)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        "processing_time": end_time - start_time,
        "memory_peak_mb": peak / 1024 / 1024,
        "chunks_generated": len(chunks),
        "throughput": len(chunks) / (end_time - start_time)
    }
```

### 3. Logging Configuration

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'chunker.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console']
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## Troubleshooting

### Common Issues

**1. Memory Errors**
```
Solution: Reduce batch size or chunk size
- Increase safety_margin (e.g., 0.6 instead of 0.8)
- Process smaller batches
- Disable semantic scoring if enabled
```

**2. Import Errors**
```
Solution: Install missing dependencies
pip install tree-sitter tree-sitter-languages semchunk
```

**3. Token Limit Exceeded**
```
Solution: Validation will catch this
- Check validation report
- Adjust safety_margin parameter
- Verify target_model configuration
```

**4. Slow Processing**
```
Solution: Optimize configuration
- Disable unused frameworks
- Use basic mode for speed
- Process files in parallel (external)
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Test with small file
chunker = EnhancedUltimateChunkerV5Unified(
    target_model="jina-code-embeddings-1.5b",
    use_tree_sitter=False,  # Disable for debugging
    use_semchunk=False
)

chunks = chunker.process_file_smart("test.md")
print(f"Generated {len(chunks)} chunks")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i}:")
    print(f"  Tokens: {chunk['metadata']['token_count']}")
    print(f"  Quality: {chunk['advanced_scores']['overall']:.3f}")
```

---

## Additional Resources

- **API Reference**: `docs/API_REFERENCE_V5.md`
- **Tutorial**: `docs/V5_TUTORIAL.md`
- **Configuration Guide**: `notes/V5_MODEL_CONFIGURATIONS.md`
- **Phase 2 Plan**: `notes/V5_PHASE2_IMPLEMENTATION_PLAN.md`

---

**Last Updated**: 2025-01-20  
**Version**: V5 Unified Phase 2  
**Status**: Production Ready