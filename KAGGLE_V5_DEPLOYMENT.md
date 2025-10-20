# Kaggle V5 Deployment Guide - Updated with Flash Attention 2

**Last Updated**: 2025-01-20
**Changes**: Upgraded to `sentence-transformers>=3.0.0` and `flash-attn>=2.5.0` for 3x faster inference

**Deployment Architecture:**
- **GPU Processing (Kaggle):** Chunking + Embedding generation
- **CPU Processing (Local):** Qdrant vector database upload

**Hardware Configuration:**
- **Kaggle:** 2x Tesla T4 GPUs (14GB each) + CPU
- **Local:** CPU only (Qdrant server)

---

## 🎯 Overview

This guide covers deploying the V5 RAG system in a **hybrid setup**:

1. **Kaggle Notebook (GPU):** Document chunking and embedding generation
2. **Local Machine (CPU):** Qdrant vector database for search

### Why This Architecture?

✅ **Cost-effective:** Free Kaggle GPU quota (30 hrs/week)  
✅ **Fast embedding:** 2x T4 GPUs accelerate transformer models  
✅ **Local control:** Your data stays on your machine via local Qdrant  
✅ **Flexible:** Download embeddings as ZIP from Kaggle, upload to local Qdrant

---

## 📦 Part 1: Kaggle Setup (GPU Processing)

### Step 1: Create Kaggle Notebook

1. Go to https://www.kaggle.com/code
2. Click "New Notebook"
3. **Settings:**
   - **Accelerator:** GPU T4 x2
   - **Language:** Python
   - **Internet:** ON (required for pip installs)

### Step 2: Install Dependencies (One-Line Command)

```python
# Cell 1: Install V5 dependencies optimized for Kaggle GPU (single line)
!pip install --upgrade "protobuf>=3.20.0,<4.0.0" sentence-transformers transformers scikit-learn faiss-gpu-cu11 onnxruntime-gpu "optimum[onnxruntime-gpu]" accelerate datasets psutil requests tqdm qdrant-client tiktoken tree-sitter semchunk llama-index llama-index-core docling docling-core pdfplumber python-docx Pillow jsonlines pandas pyarrow
```

### Step 3: Verify GPU Configuration

```python
# Cell 2: Verify GPU setup
import torch

print("CUDA Configuration:")
print(f"✓ CUDA available: {torch.cuda.is_available()}")
print(f"✓ CUDA device count: {torch.cuda.device_count()}")

for i in range(torch.cuda.device_count()):
    print(f"  - GPU {i}: {torch.cuda.get_device_name(i)} - {torch.cuda.get_device_properties(i).total_memory // 1024**3}GB")

# Verify FAISS GPU
try:
    import faiss
    print(f"\n✓ FAISS version: {faiss.__version__}")
    print(f"✓ FAISS GPU support: Available")
except ImportError:
    print("✗ FAISS not available")
```

### Step 4: Clone Repository from GitHub

```python
# Cell 3: Clone the rag_clean repository
!git clone https://github.com/eldon31/rag_clean.git /kaggle/working/rag_clean
%cd /kaggle/working/rag_clean

print("✓ Repository cloned successfully!")
print(f"✓ Working directory: /kaggle/working/rag_clean")
```

**Note:** This automatically gives you:
- All processor files ([`enhanced_ultimate_chunker_v5.py`](processor/enhanced_ultimate_chunker_v5.py), [`kaggle_ultimate_embedder_v4.py`](processor/kaggle_ultimate_embedder_v4.py))
- All scripts ([`chunk_docs_v5.py`](scripts/chunk_docs_v5.py), [`embed_collections_v5.py`](scripts/embed_collections_v5.py))
- All documentation in [`Docs/`](Docs/) folder

### Step 5: Directory Structure

```python
# Cell 4: Create directory structure
import os
from pathlib import Path

# Kaggle working directory structure
base_dir = Path("/kaggle/working/rag_clean")
base_dir.mkdir(parents=True, exist_ok=True)

# Create subdirectories
(base_dir / "Docs").mkdir(exist_ok=True)
(base_dir / "Chunked").mkdir(exist_ok=True)
(base_dir / "Embeddings").mkdir(exist_ok=True)
(base_dir / "processor").mkdir(exist_ok=True)
(base_dir / "scripts").mkdir(exist_ok=True)

print("✓ Directory structure created:")
print(f"  📁 {base_dir}/Docs")
print(f"  📁 {base_dir}/Chunked")
print(f"  📁 {base_dir}/Embeddings")
```

---

## 🔨 Part 2: Kaggle Execution (Chunking + Embedding)

### Cell 5: Run V5 Chunking

```python
# Run with defaults (uses git clone structure automatically)
!python scripts/chunk_docs_v5.py

# Or with custom paths:
# !python scripts/chunk_docs_v5.py /kaggle/working/rag_clean/Docs /kaggle/working/rag_clean/Chunked jina-code-embeddings-1.5b
```

### Cell 6: Run V5 Embedding

```python
# Run with defaults (full 1536D embeddings)
!python scripts/embed_collections_v5.py

# Or with Matryoshka truncation to 1024D (optional, saves space):
# !python scripts/embed_collections_v5.py /kaggle/working/rag_clean/Chunked /kaggle/working/rag_clean/Embeddings jina-code-embeddings-1.5b 1024

# Or with Matryoshka truncation to 512D (aggressive reduction):
# !python scripts/embed_collections_v5.py /kaggle/working/rag_clean/Chunked /kaggle/working/rag_clean/Embeddings jina-code-embeddings-1.5b 512
```

**Note:** Matryoshka dimensions for jina-code-embeddings-1.5b:
- `1536` (default): Full Matryoshka dimension, best quality
- `1024`: 33% dimension reduction, minimal quality loss (~2-3%)
- `512`: 67% dimension reduction, moderate quality loss (~5-8%)
- `256`: 83% dimension reduction, higher quality loss (~12-15%)

### Cell 7: Package Embeddings for Download

```python
# Create ZIP file for download
import shutil
from datetime import datetime

# Create timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_filename = f"embeddings_v5_{timestamp}"

# Package embeddings directory
print("Creating download package...")
shutil.make_archive(
    f"/kaggle/working/{zip_filename}",
    'zip',
    '/kaggle/working/rag_clean/Embeddings'
)

zip_path = f"/kaggle/working/{zip_filename}.zip"
zip_size = os.path.getsize(zip_path) / (1024**2)  # MB

print(f"\n✓ Package created:")
print(f"  📦 {zip_filename}.zip")
print(f"  📊 Size: {zip_size:.2f} MB")
print(f"\n📥 Download from Kaggle Output panel")
```

---

## 💻 Part 3: Local Setup (Qdrant Upload)

### Step 1: Install Qdrant Locally

**Option A: Docker (Recommended)**
```bash
# Pull and run Qdrant
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

**Option B: Binary**
```bash
# Download from https://github.com/qdrant/qdrant/releases
# Run locally
./qdrant
```

### Step 2: Extract Kaggle Embeddings

```bash
# Extract downloaded ZIP file
unzip embeddings_v5_20250120_123456.zip -d ~/rag_embeddings/

# Verify contents
ls -lh ~/rag_embeddings/
# Should show:
# - *.jsonl (Qdrant JSONL files)
# - upload_to_qdrant_*.py (Upload scripts)
```

### Step 3: Install Local Dependencies

```bash
# Install only what's needed for upload (CPU only)
pip install qdrant-client requests tqdm
```

### Step 4: Upload to Local Qdrant

```bash
# Navigate to embeddings directory
cd ~/rag_embeddings/

# Run auto-generated upload script
python upload_to_qdrant_jina-code-embeddings-1.5b.py

# Or manually specify Qdrant URL
python upload_to_qdrant_jina-code-embeddings-1.5b.py --url http://localhost:6333
```

---

## 🔍 Part 4: Verification

### Verify in Kaggle (After Embedding)

```python
# Cell 8: Check embedding statistics
import json
from pathlib import Path

embeddings_dir = Path("/kaggle/working/rag_clean/Embeddings")

# Count JSONL files
jsonl_files = list(embeddings_dir.glob("*.jsonl"))
print(f"📊 Generated {len(jsonl_files)} JSONL file(s)")

# Check first file
if jsonl_files:
    with open(jsonl_files[0], 'r') as f:
        first_line = json.loads(f.readline())
        
    print(f"\n📋 Sample point structure:")
    print(f"  - ID: {first_line.get('id')}")
    print(f"  - Vector keys: {list(first_line.get('vector', {}).keys())}")
    print(f"  - Payload keys: {list(first_line.get('payload', {}).keys())}")
```

### Verify Locally (After Upload)

```bash
# Check Qdrant collections
curl http://localhost:6333/collections

# Check collection info
curl http://localhost:6333/collections/your_collection_name

# Test search
curl -X POST http://localhost:6333/collections/your_collection_name/points/search \
  -H 'Content-Type: application/json' \
  -d '{
    "vector": {"name": "jina-code-primary", "vector": [0.1, 0.2, ...]},
    "limit": 5
  }'
```

---

## 📊 Performance Tips

### GPU Optimization (Kaggle)

1. **Batch Size Tuning:**
   ```python
   # For 2x T4 GPUs (14GB each)
   --batch_size 64  # Dense embeddings
   --batch_size 128 # Sparse embeddings (lighter)
   ```

2. **Model Selection:**
   ```python
   # Fast: all-MiniLM-L6-v2 (384D)
   # Balanced: jina-code-embeddings-1.5b (1536D)
   # Best Quality: bge-m3 (1024D, slower)
   ```

3. **Matryoshka Truncation:**
   ```bash
   # Reduce dimension for faster upload/search (positional argument)
   python scripts/embed_collections_v5.py <chunks_dir> <output_dir> <model> 512   # 67% reduction
   python scripts/embed_collections_v5.py <chunks_dir> <output_dir> <model> 1024  # 33% reduction
   ```

### Local Upload Optimization

1. **Batch Upload:**
   ```python
   # In upload script, increase batch size
   batch_size = 1000  # Default: 100
   ```

2. **Parallel Upload:**
   ```python
   # Use multiple workers if you have many collections
   from concurrent.futures import ThreadPoolExecutor
   ```

---

## 🐛 Troubleshooting

### Kaggle Issues

**Problem:** CUDA out of memory
```python
# Solution: Reduce batch size
--batch_size 16  # Instead of 32
```

**Problem:** Kernel restart during embedding
```python
# Solution: Process in smaller batches
# Split large document collections into chunks
```

**Problem:** Session timeout
```python
# Solution: Save checkpoints
# Enable auto-save in embedder
```

### Local Qdrant Issues

**Problem:** Connection refused (6333)
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Restart if needed
docker restart <container_id>
```

**Problem:** Slow upload
```bash
# Increase batch size in upload script
# Or use SSD for Qdrant storage
```

---

## 📈 Cost Analysis

### Kaggle (Free Tier)
- **GPU Quota:** 30 hours/week (Tesla T4 x2)
- **Storage:** 20GB temporary
- **Cost:** FREE

**Example Processing Times:**
- 1,000 chunks: ~5-10 minutes
- 10,000 chunks: ~30-60 minutes
- 100,000 chunks: ~5-8 hours

### Local Qdrant
- **Hardware:** Any CPU (no GPU needed)
- **RAM:** 4GB+ recommended
- **Storage:** Depends on collection size
- **Cost:** FREE (self-hosted)

---

## 🎯 Quick Reference

### Kaggle Workflow
```python
1. Install dependencies → 2. Upload docs → 3. Run chunking → 
4. Run embedding → 5. Download ZIP
```

### Local Workflow
```bash
1. Start Qdrant → 2. Extract embeddings → 3. Run upload script → 
4. Verify collections
```

### Directory Mapping

| Kaggle Path | Local Path | Content |
|-------------|-----------|---------|
| `/kaggle/working/rag_clean/Docs` | Upload manually | Source documents |
| `/kaggle/working/rag_clean/Chunked` | Not needed locally | Temporary chunks |
| `/kaggle/working/rag_clean/Embeddings` | `~/rag_embeddings/` | **Download & upload** |

---

## 🚀 Next Steps

After successful deployment:

1. **Test Search:** Query your Qdrant collections
2. **Integrate with App:** Connect to your RAG application
3. **Monitor Performance:** Track search quality and speed
4. **Scale Up:** Add more collections as needed

---

## 📚 Additional Resources

- [Kaggle GPU Docs](https://www.kaggle.com/docs/notebooks#gpu)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [V5 Architecture Plan](notes/V5_CHUNKER_EMBEDDER_PLAN.md)
- [Model Configurations](notes/V5_MODEL_CONFIGURATIONS.md)

---

**Ready to deploy? Start with Part 1 in your Kaggle notebook!** 🎉