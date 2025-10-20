# 🔧 Kaggle Embedding Troubleshooting Guide

## ⚠️ Current Issues from Log

### **Issue 1: Model Download Failures (HTTP 500)**
```
pytorch_model.bin: 0%|  | 0.00/2.27G [00:00<?, ?B/s]
WARN Status Code: 500. Retrying...
```

**Cause**: HuggingFace download failures on Kaggle  
**Solution**: **PRE-DOWNLOAD MODELS** before running embedder

---

### **Issue 2: CUDA Out of Memory**
```
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 54.00 MiB. 
GPU 0 has a total capacity of 14.74 GiB of which 18.12 MiB is free.
Process 11655 has 14.72 GiB memory in use.
```

**Cause**: Ensemble mode loading multiple 2.27GB models simultaneously  
**Solution**: **DISABLE ENSEMBLE MODE** or clear GPU between collections

---

### **Issue 3: Ensemble Failure**
```
RuntimeError: No ensemble models generated embeddings successfully
```

**Cause**: Models failed to download, so ensemble has no models  
**Solution**: Use **single-model mode** with pre-downloaded model

---

## ✅ FIXES

### **Fix 1: Pre-Download Models (CRITICAL)**

Add this cell **BEFORE** running embedder:

```python
# Cell 1: Pre-download models (run ONCE at start)
import os
from huggingface_hub import snapshot_download

os.makedirs("/kaggle/working/models", exist_ok=True)

# Download primary model FIRST
print("Downloading jina-code-embeddings-1.5b...")
snapshot_download(
    repo_id="jinaai/jina-code-embeddings-1.5b",
    local_dir="/kaggle/working/models/jina-code-embeddings-1.5b",
    local_dir_use_symlinks=False,
    ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.safetensors"],  # Only get PyTorch
)
print("✓ Model downloaded successfully")

# OPTIONAL: Download ensemble models (only if you have enough memory)
# print("Downloading BGE-M3...")
# snapshot_download(
#     repo_id="BAAI/bge-m3",
#     local_dir="/kaggle/working/models/bge-m3",
#     local_dir_use_symlinks=False,
# )
```

Then modify embedder initialization to use local path:

```python
# Update model path in script
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    gpu_config=gpu_config,
    export_config=export_config,
    enable_ensemble=False,  # DISABLE ensemble to save memory
    matryoshka_dim=1536,
)

# Override HF model path to use local download
embedder.model_config.hf_model_id = "/kaggle/working/models/jina-code-embeddings-1.5b"
```

---

### **Fix 2: Disable Ensemble Mode**

**Modify script invocation**:

```bash
# BEFORE (fails):
python scripts/embed_collections_v5.py --enable-ensemble

# AFTER (works):
python scripts/embed_collections_v5.py  # ensemble defaults to False
```

**Or modify KAGGLE_DEFAULTS** in `scripts/embed_collections_v5.py`:

```python
# Line 46-61
KAGGLE_DEFAULTS = {
    "chunks_root": Path("/kaggle/working/rag_clean/Chunked"),
    "output_root": Path("/kaggle/working/Embeddings"),
    "collections": [
        "Qdrant",
        "Sentence_Transformer", 
        "Docling",
        "FAST_DOCS",
        "pydantic",
    ],
    "model": "jina-code-embeddings-1.5b",
    "enable_ensemble": False,  # CHANGE FROM True TO False
    "skip_existing": True,
    "summary": "embedding_summary.json",
    "zip_output": True,
}
```

---

### **Fix 3: GPU Memory Management**

Add GPU cleanup between collections:

**Option A**: Modify `_run_for_collection()` in `embed_collections_v5.py`:

```python
def _run_for_collection(...):
    # At the START of function (line 242)
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
    
    # ... rest of function ...
    
    # At the END of function (line 312)
    del embedder
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    
    return summary
```

**Option B**: Add environment variable before script:

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python scripts/embed_collections_v5.py
```

---

## 🚀 CORRECTED KAGGLE WORKFLOW

### **Step 1: Setup Cell**
```python
# Install dependencies
!pip install -q sentence-transformers transformers torch faiss-cpu

# Create directories
!mkdir -p /kaggle/working/models
!mkdir -p /kaggle/working/rag_clean/Chunked
!mkdir -p /kaggle/working/rag_clean/Embeddings
```

### **Step 2: Download Model Cell**
```python
from huggingface_hub import snapshot_download
import os

print("Downloading jina-code-embeddings-1.5b (2.27 GB)...")
snapshot_download(
    repo_id="jinaai/jina-code-embeddings-1.5b",
    local_dir="/kaggle/working/models/jina-code-embeddings-1.5b",
    local_dir_use_symlinks=False,
    ignore_patterns=["*.msgpack", "*.h5", "*.ot"],
)
print("✓ Model ready at /kaggle/working/models/jina-code-embeddings-1.5b")

# Verify download
import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("/kaggle/working/models/jina-code-embeddings-1.5b")
print(f"✓ Model loaded: {model.get_sentence_embedding_dimension()}D")
del model
torch.cuda.empty_cache()
```

### **Step 3: Upload Chunks**
```python
# Upload your Chunked.zip dataset to Kaggle
# Extract to /kaggle/working/rag_clean/Chunked

!unzip -q /kaggle/input/your-dataset/Chunked.zip -d /kaggle/working/rag_clean/
!ls -la /kaggle/working/rag_clean/Chunked/
```

### **Step 4: Run Embedder (FIXED)**
```python
!python /kaggle/working/rag_clean/scripts/embed_collections_v5.py \
    --chunks-root /kaggle/working/rag_clean/Chunked \
    --output-root /kaggle/working/rag_clean/Embeddings \
    --model jina-code-embeddings-1.5b \
    --matryoshka-dim 1536 \
    --zip-output \
    --skip-existing
    # NOTE: NO --enable-ensemble flag!
```

**Or modify the script directly** (recommended):

```python
# In processor/kaggle_ultimate_embedder_v4.py line 447
self.enable_ensemble = False  # Hardcode to False for Kaggle
```

### **Step 5: Download Results**
```python
# Results will be at:
# /kaggle/working/rag_clean/Embeddings.zip

!ls -lh /kaggle/working/rag_clean/Embeddings.zip
print("✓ Download Embeddings.zip from Kaggle output")
```

---

## 🔍 DIAGNOSTIC COMMANDS

### **Check GPU Memory Before Run**:
```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"GPU Count: {torch.cuda.device_count()}")
for i in range(torch.cuda.device_count()):
    print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    print(f"    Total: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
    print(f"    Allocated: {torch.cuda.memory_allocated(i) / 1e9:.2f} GB")
    print(f"    Cached: {torch.cuda.memory_reserved(i) / 1e9:.2f} GB")
```

### **Check Model Size**:
```bash
du -sh /kaggle/working/models/jina-code-embeddings-1.5b
# Expected: ~2.3 GB
```

### **Test Single Collection**:
```bash
python scripts/embed_collections_v5.py \
    --collections Qdrant \
    --chunks-root /kaggle/working/rag_clean/Chunked \
    --output-root /kaggle/working/rag_clean/Embeddings \
    --model jina-code-embeddings-1.5b \
    --matryoshka-dim 1536
```

---

## 📊 Memory Requirements

| Configuration | VRAM Needed | Works on T4 x2? |
|---------------|-------------|-----------------|
| **Single Model** (Jina 1.5B) | ~3.5 GB | ✅ Yes |
| **Ensemble** (Jina + BGE-M3) | ~8-10 GB | ⚠️  Tight |
| **Ensemble** (Jina + BGE + Reranker) | ~12-14 GB | ❌ No |

**Recommendation**: Use **single-model mode** on Kaggle T4 x2

---

## ✅ SUMMARY OF FIXES

1. **Pre-download model** using `huggingface_hub.snapshot_download()`
2. **Disable ensemble mode**: Remove `--enable-ensemble` flag
3. **Update KAGGLE_DEFAULTS**: Set `"enable_ensemble": False`
4. **Add GPU cleanup**: Between collections in `_run_for_collection()`
5. **Use local model path**: Override `hf_model_id` to point to downloaded model
6. **Process one collection at a time**: Use `--collections Qdrant` for testing

---

## 🎯 QUICK FIX COMMAND

**Single command to run with all fixes**:

```bash
# Download model first
python -c "from huggingface_hub import snapshot_download; snapshot_download('jinaai/jina-code-embeddings-1.5b', local_dir='/kaggle/working/models/jina-code-embeddings-1.5b', local_dir_use_symlinks=False)"

# Run embedder WITHOUT ensemble
python scripts/embed_collections_v5.py \
    --chunks-root /kaggle/working/rag_clean/Chunked \
    --output-root /kaggle/working/rag_clean/Embeddings \
    --model jina-code-embeddings-1.5b \
    --matryoshka-dim 1536 \
    --skip-existing \
    --zip-output
```

**Expected Result**: ✅ All collections process successfully without OOM errors