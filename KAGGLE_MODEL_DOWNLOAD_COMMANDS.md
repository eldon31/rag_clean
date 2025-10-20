# Kaggle V5 Model Download Commands

## Quick Setup for Kaggle Notebook

### Step 1: Install HuggingFace CLI
```bash
pip install -q huggingface_hub
```

### Step 2: Download Models

#### Primary Model (Required - 3.0 GB)
```bash
huggingface-cli download jinaai/jina-code-embeddings-1.5b \
  --local-dir /kaggle/working/models/jina-code-embeddings-1.5b \
  --local-dir-use-symlinks False
```

#### Secondary Model (Optional - 2.2 GB)
```bash
huggingface-cli download BAAI/bge-m3 \
  --local-dir /kaggle/working/models/bge-m3 \
  --local-dir-use-symlinks False
```

#### Reranker Model (Optional - 1.2 GB)
```bash
huggingface-cli download jinaai/jina-reranker-v3 \
  --local-dir /kaggle/working/models/jina-reranker-v3 \
  --local-dir-use-symlinks False
```

#### Sparse BM25 Model (Optional - 0.4 GB)
```bash
huggingface-cli download Qdrant/bm25 \
  --local-dir /kaggle/working/models/qdrant-bm25 \
  --local-dir-use-symlinks False
```

#### ONNX Fast Model (Optional - 0.08 GB)
```bash
huggingface-cli download Qdrant/all-MiniLM-L6-v2-onnx \
  --local-dir /kaggle/working/models/qdrant-minilm-onnx \
  --local-dir-use-symlinks False
```

---

## Single Command Download (All Models)

```bash
# Download all V5 models at once
huggingface-cli download jinaai/jina-code-embeddings-1.5b --local-dir /kaggle/working/models/jina-code-embeddings-1.5b --local-dir-use-symlinks False && \
huggingface-cli download BAAI/bge-m3 --local-dir /kaggle/working/models/bge-m3 --local-dir-use-symlinks False && \
huggingface-cli download jinaai/jina-reranker-v3 --local-dir /kaggle/working/models/jina-reranker-v3 --local-dir-use-symlinks False && \
huggingface-cli download Qdrant/bm25 --local-dir /kaggle/working/models/qdrant-bm25 --local-dir-use-symlinks False && \
huggingface-cli download Qdrant/all-MiniLM-L6-v2-onnx --local-dir /kaggle/working/models/qdrant-minilm-onnx --local-dir-use-symlinks False
```

**Total Size**: ~6.88 GB  
**Download Time**: ~10-15 minutes on Kaggle

---

## Minimal Setup (Primary Model Only)

If you only need basic embedding without reranking or sparse vectors:

```bash
# Just the primary model (3.0 GB)
huggingface-cli download jinaai/jina-code-embeddings-1.5b \
  --local-dir /kaggle/working/models/jina-code-embeddings-1.5b \
  --local-dir-use-symlinks False
```

---

## Alternative: Using Python

```python
from huggingface_hub import snapshot_download

# Download primary model
snapshot_download(
    repo_id="jinaai/jina-code-embeddings-1.5b",
    local_dir="/kaggle/working/models/jina-code-embeddings-1.5b",
    local_dir_use_symlinks=False
)

# Download reranker
snapshot_download(
    repo_id="jinaai/jina-reranker-v3",
    local_dir="/kaggle/working/models/jina-reranker-v3",
    local_dir_use_symlinks=False
)
```

---

## Model Cache Configuration

The embedder will automatically find models in:
1. `/kaggle/working/models/{model_name}`
2. HuggingFace cache (`~/.cache/huggingface/hub`)
3. Auto-download from HF if not found

To force use of pre-downloaded models:

```python
from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    # Will look in /kaggle/working/models/ first
)
```

---

## Verification

After downloading, verify models are present:

```bash
ls -lh /kaggle/working/models/
```

Expected output:
```
drwxr-xr-x 2 root root 4.0K jina-code-embeddings-1.5b/
drwxr-xr-x 2 root root 4.0K bge-m3/
drwxr-xr-x 2 root root 4.0K jina-reranker-v3/
drwxr-xr-x 2 root root 4.0K qdrant-bm25/
drwxr-xr-x 2 root root 4.0K qdrant-minilm-onnx/
```

Check model files:
```bash
ls -lh /kaggle/working/models/jina-code-embeddings-1.5b/
```

Expected:
```
config.json
model.safetensors (or pytorch_model.bin)
tokenizer.json
tokenizer_config.json
...
```

---

## Troubleshooting

### Model Not Found
```python
# If embedder can't find model, specify full path
embedder = UltimateKaggleEmbedderV4(
    model_name="/kaggle/working/models/jina-code-embeddings-1.5b"
)
```

### Out of Space
```bash
# Check available space
df -h /kaggle/working

# Clean up if needed
rm -rf /kaggle/working/models/*  # Remove all models
```

### Download Failed
```bash
# Retry with verbose output
huggingface-cli download jinaai/jina-code-embeddings-1.5b \
  --local-dir /kaggle/working/models/jina-code-embeddings-1.5b \
  --local-dir-use-symlinks False \
  --resume-download  # Resume interrupted downloads
```

---

## Model Size Summary

| Model | Size | Required | Purpose |
|-------|------|----------|---------|
| jina-code-embeddings-1.5b | 3.0 GB | ✅ Yes | Primary embeddings |
| bge-m3 | 2.2 GB | ❌ No | Ensemble/companion |
| jina-reranker-v3 | 1.2 GB | ❌ No | Reranking |
| qdrant-bm25 | 0.4 GB | ❌ No | Sparse vectors |
| qdrant-minilm-onnx | 0.08 GB | ❌ No | Fast inference |

**Minimum**: 3.0 GB (primary only)  
**Recommended**: 4.2 GB (primary + sparse)  
**Full Setup**: 6.88 GB (all models)

---

## Usage in Notebook

After downloading models, use them in your embedder:

```python
from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4

# Basic usage (primary model only)
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b"
)

# With sparse vectors
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    enable_sparse=True,
    sparse_models=["qdrant-bm25"]
)

# With reranking
from processor.kaggle_ultimate_embedder_v4 import RerankingConfig

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    reranking_config=RerankingConfig(
        model_name="jina-reranker-v3",
        enable_reranking=True
    )
)