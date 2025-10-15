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

### Step 4: Run the Embedding Script

**Cell 3: Execute the script**

```python
!python rad_clean/scripts/kaggle_embed_qdrant_ecosystem.py
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
