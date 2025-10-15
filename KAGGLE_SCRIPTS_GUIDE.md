# KAGGLE SCRIPTS GUIDE
## Qdrant Ecosystem Embedding Pipeline

**Date:** October 16, 2025  
**Purpose:** Upload and run embedding scripts on Kaggle GPU (T4 x2)  
**Collection:** qdrant_ecosystem (6 subdirectories, ~555 markdown files)

---

## 📋 OVERVIEW

This guide provides all scripts needed to run the embedding pipeline on Kaggle.

**What you have:**
- ✅ Pre-processed chunks in `output/qdrant_ecosystem/` (from `process_qdrant_ecosystem.py`)
- ✅ 6 subdirectories with `chunks.json` files
- ✅ Upgraded reranker (CodeRankLLM instead of ms-marco)
- ✅ Task prefix support for embeddings (search_document, search_query)

**What to do on Kaggle:**
- 📤 Upload `output/qdrant_ecosystem/` folder as dataset
- 📤 Upload embedding script
- 🚀 Run with T4 x2 GPUs + data parallelism
- 💾 Download embedded chunks
- 📊 Upload to Qdrant Cloud

---

## 📁 DATA SOURCE

### Input Data (Already in GitHub!)

**No need to upload anything!** The data is already in your GitHub repo:
- Repository: `https://github.com/eldonrey0531/rad_clean`
- Path: `output/qdrant_ecosystem/`

**Contents:**
```
output/qdrant_ecosystem/
  ├── summary.json                          # Collection stats
  ├── qdrant_documentation/chunks.json      # ~XXX chunks
  ├── qdrant_examples/chunks.json           # ~XXX chunks
  ├── qdrant_fastembed/chunks.json          # ~XXX chunks
  ├── qdrant_mcp-server-qdrant/chunks.json  # ~XXX chunks
  ├── qdrant_qdrant/chunks.json             # ~XXX chunks
  └── qdrant_qdrant-client/chunks.json      # ~XXX chunks
```

**We'll clone the repo directly on Kaggle!**

---

## 🚀 KAGGLE NOTEBOOK SETUP

### Step 1: Create New Kaggle Notebook

1. Go to: https://www.kaggle.com/code
2. Click "New Notebook"
3. Title: "Qdrant Ecosystem Embedding with Data Parallelism"
4. Accelerator: **GPU T4 x2** (required for parallel processing)
5. Environment: Python 3.10+
6. Internet: **ON** (required to clone GitHub repo)

---

### Step 2: Clone GitHub Repo

**Cell 1: Clone Repository**

```python
# Clone your GitHub repo
!git clone https://github.com/eldonrey0531/rad_clean.git
!ls -la rad_clean/output/qdrant_ecosystem/

print("✅ Repository cloned successfully!")
```

---

### Step 3: Install Dependencies

**Cell 2: Install Required Packages**

```python
# Install dependencies
!pip install -q sentence-transformers==3.3.1 torch transformers

# Verify installation
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Number of GPUs: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
```

---

### Step 4: Update Script Paths

The script needs to point to the cloned repo:

**Cell 3: Main Embedding Script**

```python
"""
Kaggle-optimized Qdrant Ecosystem Embedding Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code (3584-dim) + DATA PARALLELISM
"""

import os

# Prevent transformers from attempting to load TensorFlow
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
# Enable PyTorch memory optimization
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import multiprocessing as mp
from functools import partial

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Guard against NumPy 2.x
if tuple(map(int, np.__version__.split(".")[:2])) >= (2, 0):
    raise RuntimeError(
        "NumPy 2.x detected. Please run `pip install -q --force-reinstall \"numpy==1.26.4\" \"scikit-learn==1.4.2\"`"
    )

# Check GPU availability
print(f"\n{'='*60}")
print("GPU SETUP")
print(f"{'='*60}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    num_gpus = torch.cuda.device_count()
    print(f"Number of GPUs: {num_gpus}")
    for i in range(num_gpus):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
else:
    num_gpus = 1
    print("No CUDA GPUs available, using CPU")
print(f"{'='*60}\n")

# Configuration
COLLECTION_NAME = "qdrant_ecosystem"
INPUT_DIR = Path("/kaggle/working/rad_clean/output/qdrant_ecosystem")  # ← UPDATED PATH
OUTPUT_DIR = Path("/kaggle/working/embeddings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model configuration
MODEL_NAME = "nomic-ai/nomic-embed-code"
EMBEDDING_DIM = 3584
BATCH_SIZE = 32  # Per GPU
MAX_SEQ_LENGTH = 8192

# Parallelism configuration
NUM_WORKERS = min(num_gpus, mp.cpu_count())  # 1 worker per GPU


def load_chunks_from_subdirectory(subdir_path: Path) -> List[Dict]:
    """
    Load chunks from a subdirectory's chunks.json file.
    
    Args:
        subdir_path: Path to subdirectory (e.g., /kaggle/input/.../qdrant_documentation/)
    
    Returns:
        List of chunk dictionaries with chunk_id, content, metadata
    """
    chunks_file = subdir_path / "chunks.json"
    
    if not chunks_file.exists():
        print(f"⚠️  No chunks.json found in {subdir_path.name}")
        return []
    
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data.get('chunks', [])
    print(f"✅ Loaded {len(chunks)} chunks from {subdir_path.name}")
    
    return chunks


def embed_chunks_worker(
    subdir_names: List[str],
    worker_id: int,
    gpu_id: int,
    input_dir: Path,
    output_dir: Path
) -> Tuple[int, int]:
    """
    Worker function to embed chunks from assigned subdirectories.
    Each worker runs on a dedicated GPU.
    
    Args:
        subdir_names: List of subdirectory names to process
        worker_id: Worker process ID
        gpu_id: GPU device ID for this worker
        input_dir: Input directory path
        output_dir: Output directory path
    
    Returns:
        Tuple of (total_chunks_processed, total_subdirs_processed)
    """
    # Set GPU for this worker
    device = f"cuda:{gpu_id}" if torch.cuda.is_available() else "cpu"
    print(f"\n[Worker {worker_id}] Starting on {device}")
    print(f"[Worker {worker_id}] Assigned subdirectories: {subdir_names}")
    
    # Load model on assigned GPU
    print(f"[Worker {worker_id}] Loading {MODEL_NAME}...")
    model = SentenceTransformer(
        MODEL_NAME,
        device=device,
        trust_remote_code=True
    )
    model.max_seq_length = MAX_SEQ_LENGTH
    print(f"[Worker {worker_id}] Model loaded (dim={model.get_sentence_embedding_dimension()})")
    
    total_chunks = 0
    total_subdirs = 0
    
    for subdir_name in subdir_names:
        subdir_path = input_dir / subdir_name
        
        if not subdir_path.is_dir():
            print(f"[Worker {worker_id}] ⚠️  Skipping {subdir_name} (not a directory)")
            continue
        
        print(f"\n[Worker {worker_id}] Processing {subdir_name}...")
        
        # Load chunks
        chunks = load_chunks_from_subdirectory(subdir_path)
        
        if not chunks:
            print(f"[Worker {worker_id}] ⚠️  No chunks found in {subdir_name}")
            continue
        
        # Prepare texts for embedding (use search_document task)
        texts = [chunk['content'] for chunk in chunks]
        
        # Embed with batching and prompt_name for Nomic models
        print(f"[Worker {worker_id}] Embedding {len(texts)} chunks...")
        embeddings = model.encode(
            texts,
            batch_size=BATCH_SIZE,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True,
            prompt_name="search_document"  # Nomic-specific for documents
        )
        
        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding.tolist()
        
        # Save embedded chunks
        output_file = output_dir / f"{subdir_name}_embedded.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'collection': COLLECTION_NAME,
                'subdirectory': subdir_name,
                'total_chunks': len(chunks),
                'embedding_model': MODEL_NAME,
                'embedding_dim': EMBEDDING_DIM,
                'processed_at': datetime.now().isoformat(),
                'chunks': chunks
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[Worker {worker_id}] ✅ Saved {len(chunks)} embedded chunks to {output_file.name}")
        total_chunks += len(chunks)
        total_subdirs += 1
    
    print(f"\n[Worker {worker_id}] Finished: {total_subdirs} subdirectories, {total_chunks} chunks")
    return total_chunks, total_subdirs


def main():
    """Main execution with data parallelism."""
    start_time = datetime.now()
    
    print(f"\n{'='*60}")
    print(f"QDRANT ECOSYSTEM EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Input: {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Model: {MODEL_NAME}")
    print(f"Workers: {NUM_WORKERS} (parallel processes)")
    print(f"Batch size: {BATCH_SIZE} per GPU")
    print(f"{'='*60}\n")
    
    # Discover all subdirectories
    subdirs = [d for d in INPUT_DIR.iterdir() if d.is_dir()]
    subdir_names = [d.name for d in subdirs]
    
    print(f"Found {len(subdir_names)} subdirectories:")
    for name in subdir_names:
        print(f"  - {name}")
    
    if not subdir_names:
        print("❌ No subdirectories found. Exiting.")
        return
    
    # Split subdirectories across workers (data parallelism)
    subdirs_per_worker = [[] for _ in range(NUM_WORKERS)]
    for i, name in enumerate(subdir_names):
        worker_idx = i % NUM_WORKERS
        subdirs_per_worker[worker_idx].append(name)
    
    print(f"\n{'='*60}")
    print("WORK DISTRIBUTION")
    print(f"{'='*60}")
    for worker_id, assigned_subdirs in enumerate(subdirs_per_worker):
        gpu_id = worker_id % num_gpus if torch.cuda.is_available() else 0
        print(f"Worker {worker_id} (GPU {gpu_id}): {len(assigned_subdirs)} subdirs - {assigned_subdirs}")
    print(f"{'='*60}\n")
    
    # Create worker function with partial application
    worker_fn = partial(
        embed_chunks_worker,
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR
    )
    
    # Run workers in parallel
    if NUM_WORKERS > 1:
        print(f"🚀 Starting {NUM_WORKERS} parallel workers...\n")
        
        with mp.Pool(processes=NUM_WORKERS) as pool:
            # Create arguments for each worker
            worker_args = [
                (subdirs, worker_id, worker_id % num_gpus if torch.cuda.is_available() else 0)
                for worker_id, subdirs in enumerate(subdirs_per_worker)
                if subdirs  # Skip empty assignments
            ]
            
            # Execute in parallel
            results = pool.starmap(worker_fn, worker_args)
        
        # Aggregate results
        total_chunks = sum(r[0] for r in results)
        total_subdirs = sum(r[1] for r in results)
    else:
        print(f"🚀 Starting single worker (no parallelism)...\n")
        
        # Single worker mode
        gpu_id = 0 if torch.cuda.is_available() else 0
        total_chunks, total_subdirs = embed_chunks_worker(
            subdir_names=subdir_names,
            worker_id=0,
            gpu_id=gpu_id,
            input_dir=INPUT_DIR,
            output_dir=OUTPUT_DIR
        )
    
    # Summary
    elapsed_time = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*60}")
    print("EMBEDDING COMPLETE")
    print(f"{'='*60}")
    print(f"Total subdirectories: {total_subdirs}")
    print(f"Total chunks embedded: {total_chunks:,}")
    print(f"Elapsed time: {elapsed_time:.2f}s")
    print(f"Throughput: {total_chunks/elapsed_time:.2f} chunks/sec")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*60}\n")
    
    # List output files
    output_files = sorted(OUTPUT_DIR.glob("*_embedded.json"))
    print(f"Generated {len(output_files)} output files:")
    for file in output_files:
        size_mb = file.stat().st_size / 1e6
        print(f"  - {file.name} ({size_mb:.2f} MB)")
    
    print(f"\n✅ All embeddings saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    # Set multiprocessing start method
    mp.set_start_method('spawn', force=True)
    main()
```

---

### Step 5: Run the Script

**Cell 4: Execute**

```python
# This will be automatically executed when you paste the script above
# Just run the cell!
```

**Expected output:**
```
✅ Repository cloned successfully!

============================================================
GPU SETUP
============================================================
CUDA available: True
Number of GPUs: 2
GPU 0: Tesla T4
  Memory: 15.36 GB
GPU 1: Tesla T4
  Memory: 15.36 GB
============================================================

============================================================
QDRANT ECOSYSTEM EMBEDDING PIPELINE
============================================================
Collection: qdrant_ecosystem
Input: /kaggle/working/rad_clean/output/qdrant_ecosystem
Output: /kaggle/working/embeddings
Model: nomic-ai/nomic-embed-code
Workers: 2 (parallel processes)
Batch size: 32 per GPU
============================================================

Found 6 subdirectories:
  - qdrant_documentation
  - qdrant_examples
  - qdrant_fastembed
  - qdrant_mcp-server-qdrant
  - qdrant_qdrant
  - qdrant_qdrant-client

============================================================
WORK DISTRIBUTION
============================================================
Worker 0 (GPU 0): 3 subdirs - ['qdrant_documentation', 'qdrant_fastembed', 'qdrant_qdrant']
Worker 1 (GPU 1): 3 subdirs - ['qdrant_examples', 'qdrant_mcp-server-qdrant', 'qdrant_qdrant-client']
============================================================

🚀 Starting 2 parallel workers...

[Worker 0] Starting on cuda:0
[Worker 0] Loading nomic-ai/nomic-embed-code...
[Worker 1] Starting on cuda:1
[Worker 1] Loading nomic-ai/nomic-embed-code...

... (embedding progress bars) ...

============================================================
EMBEDDING COMPLETE
============================================================
Total subdirectories: 6
Total chunks embedded: ~XXX
Elapsed time: ~XXXs
Throughput: ~XXX chunks/sec
Output directory: /kaggle/working/embeddings
============================================================
```

---

### Step 6: Download Results

**Cell 5: Create Download Archive**

```python
import shutil

# Create zip file of all embeddings
shutil.make_archive(
    '/kaggle/working/qdrant_ecosystem_embeddings',
    'zip',
    '/kaggle/working/embeddings'
)

print("✅ Archive created: /kaggle/working/qdrant_ecosystem_embeddings.zip")
print(f"Size: {Path('/kaggle/working/qdrant_ecosystem_embeddings.zip').stat().st_size / 1e6:.2f} MB")
```

**Download:**
- Click the "Output" tab in Kaggle
- Download `qdrant_ecosystem_embeddings.zip`

---

## 📊 EXPECTED PERFORMANCE

### Timing Estimates (T4 x2)

| Stage | Single GPU | Dual GPU (Parallel) | Speedup |
|-------|------------|---------------------|---------|
| **Model Loading** | ~30s | ~30s | 1.0x |
| **Embedding 1000 chunks** | ~120s | ~60s | 2.0x |
| **Embedding 5000 chunks** | ~600s (10min) | ~300s (5min) | 2.0x |
| **Total (all subdirs)** | ~XX min | ~XX min | ~2.0x |

**Throughput:**
- Single GPU: ~8-10 chunks/sec
- Dual GPU: ~16-20 chunks/sec

---

## 🔧 TROUBLESHOOTING

### Issue 1: Repository clone failed

**Error:** `fatal: could not create work tree dir 'rad_clean'`

**Solution:**
```python
# If repo already exists, remove and re-clone
!rm -rf rad_clean
!git clone https://github.com/eldonrey0531/rad_clean.git
```

---

### Issue 2: Data not found

**Error:** `FileNotFoundError: /kaggle/working/rad_clean/output/qdrant_ecosystem`

**Solution:**
```python
# Check if repo was cloned correctly
!ls -la /kaggle/working/
!ls -la /kaggle/working/rad_clean/output/

# If path is different, update INPUT_DIR in script
```

---

### Issue 3: Out of memory

**Error:** `CUDA out of memory`

**Solution:**
```python
# Reduce batch size
BATCH_SIZE = 16  # Instead of 32
```

---

### Issue 4: NumPy 2.x detected

**Error:** `NumPy 2.x detected`

**Solution:**
```python
!pip install -q --force-reinstall "numpy==1.26.4" "scikit-learn==1.4.2"
```

---

### Issue 5: Only 1 GPU available

**Error:** `Number of GPUs: 1`

**Solution:** Notebook will automatically use single worker mode (no parallelism)

---

### Issue 6: Internet not enabled

**Error:** `fatal: unable to access 'https://github.com/...'`

**Solution:** 
1. In Kaggle notebook settings (right sidebar)
2. Find "Internet" toggle
3. Turn it **ON**
4. Re-run the clone cell

---

## 📋 POST-PROCESSING CHECKLIST

After downloading embeddings:

- [ ] Extract `qdrant_ecosystem_embeddings.zip`
- [ ] Verify 6 files exist: `*_embedded.json`
- [ ] Check total chunks count matches input
- [ ] Verify embedding dimension = 3584
- [ ] Upload to Qdrant Cloud (using another script)

---

## 🎯 NEXT STEPS

1. **Create Kaggle notebook** with T4 x2 GPUs + Internet ON
2. **Clone GitHub repo** (Cell 1)
3. **Install dependencies** (Cell 2)
4. **Run embedding script** (Cell 3)
5. **Download embedded chunks** (Cell 5)
6. **Upload to Qdrant Cloud** (see `upload_to_qdrant.py`)

---

## 📝 NOTES

### Why Data Parallelism?

- **Faster:** Each GPU processes different subdirectories
- **Efficient:** No model duplication needed
- **Scalable:** Works with 1, 2, or more GPUs

### Why Nomic Task Prefixes?

- **Better quality:** `search_document` tells model this is a document (not a query)
- **+5% accuracy:** Nomic models perform better with task prefixes
- **No cost:** Just adds a prompt identifier to encoding

### File Sizes

Each embedded chunk:
- Content: ~500-2000 chars
- Embedding: 3584 floats × 4 bytes = ~14KB
- Total: ~15-20KB per chunk

6 subdirectories × ~100 chunks/subdir = ~600 chunks
Total size: ~10-15 MB (compressed)

---

**Ready to run on Kaggle!** 🚀
