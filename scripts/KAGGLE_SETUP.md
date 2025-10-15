# Kaggle Embedding Setup Guide

## 📋 Overview

This guide shows how to embed all 3 collections on Kaggle using Tesla T4 x2 GPUs with CodeRankEmbed (768-dim).

---

## 🚀 Quick Start (All Collections)

### **Step 1: Upload Chunked Datasets to Kaggle**

1. Go to https://www.kaggle.com/datasets
2. Click "New Dataset"
3. Upload each chunked folder:
   - `output/docling-project_docling_chunked/` → Dataset: "docling-project-docling-chunked"
   - `output/qdrant_ecosystem_chunked/` → Dataset: "qdrant-ecosystem-chunked"
   - `output/sentence_transformers_docs_chunked/` → Dataset: "sentence-transformers-docs-chunked"

### **Step 2: Create Kaggle Notebooks**

Create 3 separate notebooks (one per collection):

#### **Notebook 1: docling-project_docling**
```bash
# 1. Create new Kaggle notebook
# 2. Settings → Accelerator → GPU T4 x2
# 3. Add data:
#    - Input dataset: docling-project-docling-chunked
# 4. Upload files to notebook:
#    - src/templates/embedder_template.py
#    - scripts/kaggle_embed_docling.py
# 5. Run:
!python scripts/kaggle_embed_docling.py
```

#### **Notebook 2: qdrant_ecosystem**
```bash
# 1. Create new Kaggle notebook
# 2. Settings → Accelerator → GPU T4 x2
# 3. Add data:
#    - Input dataset: qdrant-ecosystem-chunked
# 4. Upload files to notebook:
#    - src/templates/embedder_template.py
#    - scripts/kaggle_embed_qdrant_ecosystem.py
# 5. Run:
!python scripts/kaggle_embed_qdrant_ecosystem.py
```

#### **Notebook 3: sentence_transformers_docs**
```bash
# 1. Create new Kaggle notebook
# 2. Settings → Accelerator → GPU T4 x2
# 3. Add data:
#    - Input dataset: sentence-transformers-docs-chunked
# 4. Upload files to notebook:
#    - src/templates/embedder_template.py
#    - scripts/kaggle_embed_sentence_transformers.py
# 5. Run:
!python scripts/kaggle_embed_sentence_transformers.py
```

---

## 📦 Expected Results

| Collection | Chunks | Output File | Size | Time (T4 x2) |
|-----------|--------|-------------|------|--------------|
| docling-project_docling | 1,089 | docling_embeddings_768.jsonl | ~8-12 MB | 2-5 min |
| qdrant_ecosystem | 8,108 | qdrant_ecosystem_embeddings_768.jsonl | ~60-80 MB | 10-15 min |
| sentence_transformers_docs | 457 | sentence_transformers_embeddings_768.jsonl | ~3-5 MB | 1-3 min |
| **TOTAL** | **9,654** | **3 files** | **~70-100 MB** | **~15-25 min** |

---

## 📥 Download Embeddings

After each notebook completes:

1. Click **Output** tab in Kaggle notebook
2. Find the `.jsonl` file
3. Click **Download**
4. Save to local machine

---

## 🔄 Upload to Qdrant (Local)

Once all 3 embeddings are downloaded, upload to Qdrant:

```bash
# Collection 1: docling-project_docling
python -m src.templates.qdrant_uploader_template \
    --file docling_embeddings_768.jsonl \
    --collection docling-project_docling \
    --url http://localhost:6333

# Collection 2: qdrant_ecosystem
python -m src.templates.qdrant_uploader_template \
    --file qdrant_ecosystem_embeddings_768.jsonl \
    --collection qdrant_ecosystem \
    --url http://localhost:6333

# Collection 3: sentence_transformers_docs
python -m src.templates.qdrant_uploader_template \
    --file sentence_transformers_embeddings_768.jsonl \
    --collection sentence_transformers_docs \
    --url http://localhost:6333
```

---

## 🛠️ Troubleshooting

### **GPU Not Available**
```python
# Check GPU availability in Kaggle notebook
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
```

### **Out of Memory (OOM)**
- Reduce batch size in embedder_template.py (line 127):
  ```python
  batch_size_per_gpu: int = 16  # Reduce from 32
  ```

### **Dataset Not Found**
- Verify dataset name matches exactly in Kaggle
- Check input path in script matches dataset name

### **Import Error**
- Ensure `embedder_template.py` is uploaded to notebook
- Check `sys.path.insert()` in script

---

## 📊 GPU Performance

**Tesla T4 x2 Specifications:**
- **VRAM per GPU**: 15.83 GB
- **Total VRAM**: 31.66 GB
- **Batch size per GPU**: 32 (safe)
- **Total batch size**: 64 (dual-GPU)
- **CodeRankEmbed params**: 137M (lightweight)

**Expected Speed:**
- ~100-150 chunks/second with dual T4
- ~50-75 chunks/second with single T4

---

## 🎯 Success Criteria

✅ All 3 notebooks complete without errors  
✅ 3 JSONL files downloaded from Kaggle  
✅ Total embeddings: 9,654 chunks  
✅ All embeddings are 768-dimensional  
✅ Files upload successfully to Qdrant  

---

## 📝 Notes

- **Cost**: Kaggle provides 30 hours/week of free GPU time
- **Sessions**: Each embedding session counts toward quota
- **Optimization**: Run all 3 notebooks in parallel if quota allows
- **Checkpointing**: Kaggle auto-saves notebooks (resume if interrupted)

---

## 🔗 Resources

- [Kaggle Notebooks](https://www.kaggle.com/code)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Kaggle GPU Quota](https://www.kaggle.com/account)
- [CodeRankEmbed Model](https://huggingface.co/nomic-ai/CodeRankEmbed)
