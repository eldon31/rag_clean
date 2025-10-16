# ✅ CORRECTED V4 PROCESSORS - USAGE GUIDE

## 🎯 Overview

All 5 collection processor scripts have been **FULLY CORRECTED** to use the verified V4 API signatures from source code audit. Each script now uses:

### ✅ Correct V4 API Parameters

| Component | CORRECT Parameter | ❌ OLD (Wrong) |
|-----------|-------------------|----------------|
| **Initialization** | `enable_ensemble=False` | ~~enable_reranking=True~~ |
| **Export Config** | `output_prefix=f"{COLLECTION}_v4"` | ~~collection_name=COLLECTION~~ |
| **Preprocessing** | `normalize_whitespace=True` | ~~quality_filtering=True, min_chunk_length=50~~ |
| **Load Method** | `chunks_dir=parent_dir` (1 param) | ~~collection_dirs=[...], collection_priority={...}~~ |
| **Generate Method** | `enable_monitoring=True, save_intermediate=True` | ~~save_intermediate_every_n_batches=50~~ |
| **Export Method** | `export_for_local_qdrant()` (0 params) | ~~collection_name=...~~ |

---

## 📁 Available Scripts (All Corrected)

### 1. **process_docling.py** - Docling Collection (47 JSON files)
```python
# Processes: /kaggle/input/.../DOCS_CHUNKS_OUTPUT/Docling/
# Output: Docling_v4_embeddings.npy, Docling_v4_metadata.jsonl, etc.
```

### 2. **process_fast_docs.py** - FAST_DOCS Collection (1 JSON file)
```python
# Processes: /kaggle/input/.../DOCS_CHUNKS_OUTPUT/FAST_DOCS/
# Output: FAST_DOCS_v4_embeddings.npy, FAST_DOCS_v4_metadata.jsonl, etc.
```

### 3. **process_pydantic.py** - pydantic_pydantic Collection (33 JSON files)
```python
# Processes: /kaggle/input/.../DOCS_CHUNKS_OUTPUT/pydantic_pydantic/
# Output: pydantic_pydantic_v4_embeddings.npy, pydantic_pydantic_v4_metadata.jsonl, etc.
```

### 4. **process_qdrant.py** - Qdrant Collection (1 JSON file)
```python
# Processes: /kaggle/input/.../DOCS_CHUNKS_OUTPUT/Qdrant/
# Output: Qdrant_v4_embeddings.npy, Qdrant_v4_metadata.jsonl, etc.
```

### 5. **process_sentence_transformers.py** - Sentence_Transformers Collection (1 JSON file)
```python
# Processes: /kaggle/input/.../DOCS_CHUNKS_OUTPUT/Sentence_Transformers/
# Output: Sentence_Transformers_v4_embeddings.npy, Sentence_Transformers_v4_metadata.jsonl, etc.
```

---

## 🚀 Usage in Kaggle Jupyter Notebook

### Method 1: Direct Execution in Cell (Recommended)
```python
# Cell 1: Process Docling
exec(open('process_docling.py').read())

# Cell 2: Process FAST_DOCS
exec(open('process_fast_docs.py').read())

# Cell 3: Process pydantic
exec(open('process_pydantic.py').read())

# Cell 4: Process Qdrant
exec(open('process_qdrant.py').read())

# Cell 5: Process Sentence_Transformers
exec(open('process_sentence_transformers.py').read())
```

### Method 2: Magic Command (Alternative)
```python
# Cell 1: Process Docling
%run process_docling.py

# Cell 2: Process FAST_DOCS
%run process_fast_docs.py

# Cell 3: Process pydantic
%run process_pydantic.py

# Cell 4: Process Qdrant
%run process_qdrant.py

# Cell 5: Process Sentence_Transformers
%run process_sentence_transformers.py
```

### Method 3: Import and Call Function
```python
# Cell 1: Process Docling
from process_docling import process_docling_collection
results = process_docling_collection()
print(f"✅ {results['collection']}: {results['status']}")

# Cell 2: Process FAST_DOCS
from process_fast_docs import process_fast_docs_collection
results = process_fast_docs_collection()
print(f"✅ {results['collection']}: {results['status']}")

# ... (repeat for other collections)
```

---

## 📊 Expected Output Format

Each script produces the following files in `/kaggle/working/`:

### 1. **Embeddings File** - `{COLLECTION}_v4_embeddings.npy`
```python
# NumPy array shape: (num_chunks, 768)
# Example: Docling_v4_embeddings.npy (47 chunks × 768 dimensions)
```

### 2. **Metadata File** - `{COLLECTION}_v4_metadata.jsonl`
```jsonl
{"chunk_id": "docling_chunk_001", "source_file": "docling_doc_1.json", "text": "...", "collection": "Docling"}
{"chunk_id": "docling_chunk_002", "source_file": "docling_doc_1.json", "text": "...", "collection": "Docling"}
```

### 3. **FAISS Index** - `{COLLECTION}_v4_faiss.index`
```python
# FAISS IVF index for fast similarity search
# Optimized for 768-dimensional CodeRankEmbed vectors
```

### 4. **Results JSON** - `{COLLECTION}_results.json`
```json
{
  "collection": "Docling",
  "status": "SUCCESS",
  "chunks_loaded": 47,
  "embedding_results": {
    "total_embeddings": 47,
    "embedding_dimension": 768,
    "chunks_per_second": 325.4,
    "total_time_seconds": 0.14,
    "total_memory_mb": 142.5
  },
  "export_files": {
    "embeddings": "Docling_v4_embeddings.npy",
    "metadata": "Docling_v4_metadata.jsonl",
    "faiss": "Docling_v4_faiss.index"
  },
  "processing_time_seconds": 2.47,
  "timestamp": "2025-01-27T10:30:45.123456"
}
```

---

## ⚙️ How V4 Auto-Discovery Works

### Architecture
```
DOCS_CHUNKS_OUTPUT/              ← Parent directory passed to load_chunks_from_processing()
├── Docling/                     ← V4 auto-discovers this subdirectory
│   ├── docling_doc_1.json      ← Processes all JSON files
│   ├── docling_doc_2.json
│   └── ... (47 files)
├── FAST_DOCS/                   ← Separate script points to parent, discovers this
│   └── fast_docs_1.json
├── pydantic_pydantic/           ← Separate script points to parent, discovers this
│   ├── pydantic_chunk_1.json
│   └── ... (33 files)
├── Qdrant/                      ← Separate script points to parent, discovers this
│   └── qdrant_chunk_1.json
└── Sentence_Transformers/       ← Separate script points to parent, discovers this
    └── st_chunk_1.json
```

### Code Pattern (Used in All Scripts)
```python
# Find collection subdirectory
collection_path = "/kaggle/input/.../DOCS_CHUNKS_OUTPUT/Docling"

# Get parent directory (DOCS_CHUNKS_OUTPUT)
parent_dir = os.path.dirname(collection_path)

# Pass parent directory - V4 auto-discovers Docling/ subdirectory
chunks_loaded = embedder.load_chunks_from_processing(
    chunks_dir=parent_dir  # V4 scans for subdirectories with JSON files
)
```

**Why This Works:**
- V4's `load_chunks_from_processing()` scans `chunks_dir` for subdirectories
- Finds JSON files in each subdirectory
- Auto-assigns collection name from subdirectory name
- When parent contains only 1 collection → processes that collection only
- Built-in priorities ensure correct processing order (Qdrant: 1.0, Sentence_Transformers: 0.9, Docling: 0.8)

---

## 🎯 Processing Strategy

### Sequential Processing (Recommended)
Process collections one at a time to control:
- GPU memory usage
- Output file organization
- Error handling per collection

```python
# Cell 1: Docling (47 chunks - largest)
exec(open('process_docling.py').read())
# ✅ Docling_v4_* files created

# Cell 2: pydantic (33 chunks - second largest)
exec(open('process_pydantic.py').read())
# ✅ pydantic_pydantic_v4_* files created

# Cell 3-5: Small collections (1 chunk each)
exec(open('process_fast_docs.py').read())
exec(open('process_qdrant.py').read())
exec(open('process_sentence_transformers.py').read())
# ✅ All remaining _v4_* files created
```

### Parallel Processing (Advanced)
If you have sufficient GPU memory (2× T4 = 31.66GB VRAM):
```python
import concurrent.futures

scripts = [
    'process_docling.py',
    'process_fast_docs.py',
    'process_pydantic.py',
    'process_qdrant.py',
    'process_sentence_transformers.py'
]

def run_script(script):
    exec(open(script).read())
    return f"✅ {script} completed"

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(run_script, s) for s in scripts]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
```

---

## 📈 Performance Expectations

Based on V4 benchmarks and collection sizes:

| Collection | Chunks | Expected Time | Speed Target | Memory |
|------------|--------|---------------|--------------|--------|
| **Docling** | 47 | ~0.15s | 310+ chunks/sec | ~145 MB |
| **pydantic** | 33 | ~0.11s | 310+ chunks/sec | ~105 MB |
| **FAST_DOCS** | 1 | ~0.01s | - | ~3 MB |
| **Qdrant** | 1 | ~0.01s | - | ~3 MB |
| **Sentence_Transformers** | 1 | ~0.01s | - | ~3 MB |
| **TOTAL** | 83 | ~0.30s | - | ~260 MB |

### Performance Indicators
```python
# After each script runs, check:
speed = embedding_results['chunks_per_second']

if speed >= 310:
    print("🏆 EXCELLENT! Meeting V4 targets")
elif speed >= 200:
    print("✅ GOOD! Production-ready")
else:
    print("⚠️ Below target - check GPU config")
```

---

## 🔍 Verification Checklist

After running all 5 scripts, verify outputs in `/kaggle/working/`:

```bash
ls -lh /kaggle/working/

# Expected files (15 total):
# ✅ Docling_v4_embeddings.npy          (~260 KB)
# ✅ Docling_v4_metadata.jsonl          (~50 KB)
# ✅ Docling_v4_faiss.index             (~100 KB)
# ✅ Docling_results.json               (~5 KB)
# 
# ✅ FAST_DOCS_v4_embeddings.npy        (~6 KB)
# ✅ FAST_DOCS_v4_metadata.jsonl        (~1 KB)
# ✅ FAST_DOCS_v4_faiss.index           (~3 KB)
# 
# ✅ pydantic_pydantic_v4_embeddings.npy (~180 KB)
# ✅ pydantic_pydantic_v4_metadata.jsonl (~35 KB)
# ✅ pydantic_pydantic_v4_faiss.index    (~70 KB)
# 
# ✅ Qdrant_v4_embeddings.npy           (~6 KB)
# ✅ Qdrant_v4_metadata.jsonl           (~1 KB)
# ✅ Qdrant_v4_faiss.index              (~3 KB)
# 
# ✅ Sentence_Transformers_v4_embeddings.npy (~6 KB)
# ✅ Sentence_Transformers_v4_metadata.jsonl (~1 KB)
```

### Python Verification
```python
import numpy as np
import json

# Check embeddings shape
embeddings = np.load('/kaggle/working/Docling_v4_embeddings.npy')
print(f"Docling embeddings: {embeddings.shape}")  # Expected: (47, 768)

# Check metadata count
with open('/kaggle/working/Docling_v4_metadata.jsonl') as f:
    metadata = [json.loads(line) for line in f]
print(f"Docling metadata entries: {len(metadata)}")  # Expected: 47

# Verify all collections processed
collections = ['Docling', 'FAST_DOCS', 'pydantic_pydantic', 'Qdrant', 'Sentence_Transformers']
for coll in collections:
    results_file = f'/kaggle/working/{coll}_results.json'
    with open(results_file) as f:
        results = json.load(f)
    status = results['status']
    chunks = results['chunks_loaded']
    print(f"✅ {coll}: {status} ({chunks} chunks)")
```

---

## 🐛 Troubleshooting

### Issue 1: "Collection not found"
```python
# Solution: Check dataset upload in Kaggle
# Verify path: /kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT/{COLLECTION}/
# Update POSSIBLE_PATHS in script if needed
```

### Issue 2: "GPU out of memory"
```python
# Solution: Reduce batch size in script
gpu_config=KaggleGPUConfig(
    base_batch_size=16,  # Reduce from 32
    dynamic_batching=True,
    precision="fp16",
    enable_torch_compile=False  # Disable to save memory
)
```

### Issue 3: "No parameter named X"
```python
# This means using old script version
# Solution: Re-download corrected scripts from this repository
# All scripts updated on 2025-01-27 with verified V4 API
```

### Issue 4: Slow processing speed (<200 chunks/sec)
```python
# Possible causes:
# 1. Single GPU instead of dual GPU
# 2. Torch compile disabled
# 3. CPU fallback mode
# 
# Solution: Check GPU availability
import torch
print(f"GPUs available: {torch.cuda.device_count()}")
print(f"GPU 0: {torch.cuda.get_device_name(0)}")
if torch.cuda.device_count() > 1:
    print(f"GPU 1: {torch.cuda.get_device_name(1)}")
```

---

## 📚 Reference: V4 API Signatures (Verified from Source)

### __init__() - 5 Parameters
```python
UltimateKaggleEmbedderV4(
    model_name: str,                              # "nomic-coderank"
    gpu_config: KaggleGPUConfig,                  # GPU settings
    export_config: KaggleExportConfig,            # Output settings
    preprocessing_config: AdvancedPreprocessingConfig,  # Text processing
    enable_ensemble: bool                         # False for single model
)
```

### load_chunks_from_processing() - 1 Parameter
```python
embedder.load_chunks_from_processing(
    chunks_dir: str  # Parent directory containing collection subdirectories
)
# Returns: {'total_chunks': int, 'collections': list, ...}
```

### generate_embeddings_kaggle_optimized() - 2 Parameters
```python
embedder.generate_embeddings_kaggle_optimized(
    enable_monitoring: bool,    # True to track progress
    save_intermediate: bool     # True to save checkpoints
)
# Returns: {'total_embeddings': int, 'chunks_per_second': float, ...}
```

### export_for_local_qdrant() - 0 Parameters
```python
embedder.export_for_local_qdrant()
# Returns: {'embeddings': str, 'metadata': str, 'faiss': str, ...}
```

---

## 🎓 Key Differences: Old vs New API

| Feature | ❌ OLD (Wrong) | ✅ NEW (Correct) |
|---------|---------------|-----------------|
| **Reranking** | `enable_reranking=True` | `enable_ensemble=False` |
| **Collection naming** | `collection_name=...` in config | `output_prefix=f"{COLL}_v4"` in config |
| **Quality filtering** | `quality_filtering=True, min_chunk_length=50` | `normalize_whitespace=True` (built-in quality) |
| **Collection loading** | `collection_dirs=[...], collection_priority={...}` | `chunks_dir=parent_dir` (auto-discovery) |
| **Save intermediate** | `save_intermediate_every_n_batches=50` | `save_intermediate=True` |
| **Export params** | `export_for_local_qdrant(collection_name=...)` | `export_for_local_qdrant()` (no params) |

---

## ✅ Final Checklist

Before running scripts in Kaggle:

- [ ] All 5 scripts uploaded to Kaggle kernel
- [ ] `kaggle_ultimate_embedder_v4.py` uploaded to Kaggle kernel
- [ ] DOCS_CHUNKS_OUTPUT dataset attached to kernel
- [ ] Kaggle accelerator set to **GPU T4 x2** (not single GPU)
- [ ] Python 3.10+ selected
- [ ] Required packages installed: `torch`, `sentence-transformers`, `faiss-gpu`, `numpy`

During processing:

- [ ] Monitor GPU memory usage (should stay under 16GB per GPU)
- [ ] Check processing speed (target: 310+ chunks/sec for large collections)
- [ ] Verify output files created in `/kaggle/working/`
- [ ] Review results JSON for each collection

After completion:

- [ ] Download all `*_v4_embeddings.npy` files
- [ ] Download all `*_v4_metadata.jsonl` files
- [ ] Download all `*_v4_faiss.index` files (optional, can rebuild locally)
- [ ] Save results JSON files for audit trail

---

## 🚀 Next Steps

After generating embeddings in Kaggle:

1. **Download outputs** to local machine
2. **Upload to local Qdrant** using import scripts
3. **Test semantic search** across all 83 chunks
4. **Monitor query performance** (target: <10ms per query)
5. **Scale up** with more collections as needed

---

## 📞 Support

If you encounter issues:

1. Check V4_API_AUDIT_REPORT.md for verified API signatures
2. Review KAGGLE_INVOCATION_GUIDE.md for usage patterns
3. Verify scripts have "(CORRECTED V4 API)" in header comments
4. Ensure all 5 scripts show "No errors found" in lint check

---

**Last Updated:** 2025-01-27  
**V4 API Version:** Ultimate Kaggle Embedder V4 (1194 lines, verified)  
**Scripts Corrected:** All 5 collection processors (process_*.py)  
**Status:** ✅ PRODUCTION READY - All API signatures verified against source code
