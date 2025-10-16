# ⚡ KAGGLE QUICK START

## 📦 Installation Cell (Run First!)

```python
# Install dependencies for Kaggle with GPU acceleration
!pip install -q sentence-transformers faiss-gpu-cu11
```

**Why `faiss-gpu-cu11`?**
- Kaggle uses CUDA 11, so must use CUDA-specific FAISS
- Generic `faiss-gpu` will fail with "No matching distribution found"
- `faiss-gpu-cu11` provides GPU acceleration on T4 x2 GPUs

**Installs**:
- `sentence-transformers` - For embeddings
- `faiss-gpu-cu11` - GPU-accelerated similarity search
- `nvidia-cuda-runtime-cu11` - CUDA runtime (auto-installed)
- `nvidia-cublas-cu11` - cuBLAS library (auto-installed)

---

## 🚀 Full Notebook Cells

### Cell 1: Markdown
```markdown
# 🚀 Ultimate Kaggle Embedder V4
```

### Cell 2: Install Dependencies
```python
!pip install -q sentence-transformers faiss-gpu-cu11
```

### Cell 3: Clone Repository
```python
!git clone https://github.com/eldonrey0531/rad_clean.git
```

### Cell 4: Navigate to Repo
```python
%cd rad_clean
```

### Cell 5: Update to Latest
```python
!git pull
```

### Cell 6: Process Docling (47 chunks)
```python
!python process_docling.py
```

### Cell 7: Process Other Collections
```python
!python process_fast_docs.py
!python process_pydantic.py
!python process_qdrant.py
!python process_sentence_transformers.py
```

---

## ✅ Expected Output (Cell 6)

```
================================================================================
🚀 PROCESSING: Docling Collection
================================================================================
✅ Found collection at: /kaggle/working/rad_clean/DOCS_CHUNKS_OUTPUT/Docling

🔄 STEP 1: Initializing Ultimate Kaggle Embedder V4...
⚠️ torch_dtype not supported, loading model without it
✅ Converted model to FP16 after loading
✅ V4 initialized! GPU Count: 2

🔄 STEP 2: Loading chunks...
✅ Loaded 47 chunks

🔄 STEP 3: Generating embeddings...
✅ Generated 47 embeddings
   ⚡ Speed: 325.4 chunks/sec

🔄 STEP 4: Exporting...
✅ Exported 3 files

🎉 Docling PROCESSING COMPLETE!
   ⏱️ Total time: 2.47s
```

---

## 📊 Output Files (in /kaggle/working/)

- `Docling_v4_embeddings.npy` - Embeddings array (47×768)
- `Docling_v4_metadata.jsonl` - Metadata for each chunk
- `Docling_v4_faiss.index` - FAISS index for similarity search
- `Docling_results.json` - Processing statistics

---

## 🐛 Common Issues

### ❌ "No matching distribution found for faiss-gpu"
**Fix**: Use `faiss-gpu-cu11` instead
```python
!pip install faiss-gpu-cu11  # ✅
```

### ❌ "Collection not found"
**Fix**: Run `!git pull` to get latest path updates
```python
%cd rad_clean
!git pull
```

### ⚠️ CUDA warnings (cuDNN, cuBLAS)
**Status**: Safe to ignore - TensorFlow warnings, doesn't affect PyTorch

---

## 🎯 Ready to Run!

1. **Create new Kaggle notebook**
2. **Set accelerator to GPU T4 x2**
3. **Copy cells above**
4. **Run sequentially**
5. **Download output files from /kaggle/working/**

---

**Updated**: 2025-10-17  
**Tested on**: Kaggle with T4 x2 GPUs, CUDA 11  
**Repository**: https://github.com/eldonrey0531/rad_clean
