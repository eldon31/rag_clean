# Quick Reference: Embedding Script Logging

## 🚀 Quick Start

### Before You Run
Check this section in the output to confirm your setup:

```
Model Configuration:
================================================================================
Current embedding model: jina-code-embeddings-1.5b  ← Your selected model
✓ Model found in registry                            ← Should see checkmark
  - HuggingFace ID: jinaai/jina-embeddings-v3       ← Actual model ID
  - Vector dimension: 1024                           ← Output dimension
  - Matryoshka dimension: 1024                       ← If using Matryoshka

✓ Ensemble mode: ENABLED                             ← Check if ensemble is active
Available models in registry (8 total):              ← All available models
  ✓ SELECTED - jina-code-embeddings-1.5b            ← Your current selection
================================================================================
```

### During Processing
Watch for these indicators per collection:

```
1. Creating embedder instance...
   ✓ Embedder instance created                       ← Initialization success

2. Model Availability Check:
   ✓ PRIMARY MODEL: jina-code-embeddings-1.5b       ← Main model loaded
   ✓ All expected models loaded successfully        ← No missing models

3. Loading chunks from Qdrant...
   ✓ Loaded 554 chunks                              ← Chunks discovered

4. Generating embeddings...
   ✓ Generated 554 embeddings                       ← Embeddings created
   ✓ Speed: 310.5 chunks/sec                        ← Processing speed
   ✓ Time: 1.78s                                    ← Total time

5. Exporting embeddings...
   ✓ Exported 4 file(s)                             ← Files saved
```

## 🔍 What to Look For

### ✅ Success Indicators
- `✓` checkmarks throughout the output
- "All expected models loaded successfully"
- Reasonable processing speed (>100 chunks/sec)
- Export confirmation with file count

### ⚠️ Warning Signs
- `⚠️` warning symbols
- "Model not found in registry"
- "MISSING" status for any models
- "No chunks found - skipping collection"
- Very slow processing speed (<50 chunks/sec)

### ✗ Error Indicators
- `✗` error markers
- "FAILED" status
- Missing model files
- Python exceptions/tracebacks

## 🎯 Common Scenarios

### Scenario 1: First Time Setup
**What you'll see:**
- Long model download times (first run only)
- Models being cached to disk
- Slower initial processing

**Expected behavior:**
```
Downloading model: jinaai/jina-embeddings-v3
[██████████████████████████████] 100%
✓ Model cached for future use
```

### Scenario 2: Ensemble Mode Active
**What you'll see:**
- Multiple models listed in "Expected models"
- Longer initialization time
- Slightly slower embedding generation

**Expected output:**
```
2. Model Availability Check:
   Expected models: 3  ← Multiple models

   ✓ PRIMARY MODEL: jina-code-embeddings-1.5b
   
   Additional models (2):  ← Extra models for ensemble
   - bge-m3: ✓ loaded
   - nomic-embed-text-v1.5: ✓ loaded
```

### Scenario 3: Model Loading Failure
**What you'll see:**
```
   Additional models (2):
   - bge-m3: ✗ MISSING  ← Failed to load
     └─ HF ID: BAAI/bge-m3
     └─ Dimension: 1024D

   ⚠️  WARNING: 1 model(s) not loaded:
     - bge-m3
   This may affect ensemble quality if ensemble mode is enabled.
```

**Action:** Check model availability, re-download if needed

### Scenario 4: No Chunks Found
**What you'll see:**
```
3. Loading chunks from EmptyCollection...
   ⚠️  No chunks found - skipping collection
```

**Action:** Verify chunking completed successfully for that collection

## 📊 Performance Benchmarks

### Expected Speeds (Kaggle T4 x2)
- **Good**: 250-400 chunks/sec
- **Acceptable**: 100-250 chunks/sec
- **Slow**: <100 chunks/sec (investigate)

### Timing Expectations
| Collection | Chunks | Expected Time |
|-----------|--------|---------------|
| Small (50) | 50 | 0.15-0.25s |
| Medium (200) | 200 | 0.6-1.0s |
| Large (500+) | 500+ | 1.5-3.0s |

## 🛠️ Troubleshooting Quick Guide

### Issue: Model Not Found
```
⚠️  Model 'xyz' not found in KAGGLE_OPTIMIZED_MODELS registry
```
**Fix:** Check available models in output, use one of those

### Issue: Model Failed to Load
```
- model-name: ✗ MISSING
```
**Fix:** 
1. Check internet connection
2. Try re-running (download may have failed)
3. Check HuggingFace model availability

### Issue: Slow Processing
```
✓ Speed: 45.2 chunks/sec  ← Very slow
```
**Fix:**
1. Check GPU availability (`torch.cuda.is_available()`)
2. Reduce batch size if OOM
3. Disable ensemble mode if not needed

### Issue: No Chunks Loaded
```
✓ Loaded 0 chunks
⚠️  No chunks found - skipping collection
```
**Fix:**
1. Verify chunking step completed
2. Check `--chunks-root` path is correct
3. Look for `*_chunks.json` files in collection dir

## 📝 Command Line Examples

### Basic Usage
```bash
python scripts/embed_collections_v5.py \
    --chunks-root ./Chunked \
    --output-root ./Embeddings \
    --model jina-code-embeddings-1.5b
```

### With Ensemble
```bash
python scripts/embed_collections_v5.py \
    --chunks-root ./Chunked \
    --output-root ./Embeddings \
    --model jina-code-embeddings-1.5b \
    --enable-ensemble
```

### With Matryoshka Dimensions
```bash
python scripts/embed_collections_v5.py \
    --chunks-root ./Chunked \
    --output-root ./Embeddings \
    --model jina-code-embeddings-1.5b \
    --matryoshka-dim 1024
```

### Specific Collections Only
```bash
python scripts/embed_collections_v5.py \
    --chunks-root ./Chunked \
    --output-root ./Embeddings \
    --model jina-code-embeddings-1.5b \
    --collections Qdrant Docling
```

### Skip Already Processed
```bash
python scripts/embed_collections_v5.py \
    --chunks-root ./Chunked \
    --output-root ./Embeddings \
    --model jina-code-embeddings-1.5b \
    --skip-existing
```

## 🔑 Key Takeaways

1. **Always check** the Model Configuration section at the start
2. **Watch for** ✗ MISSING indicators in model loading
3. **Monitor** processing speed for performance issues
4. **Verify** export confirmation at the end of each collection
5. **Review** the final summary for any failed collections

## 📞 Need Help?

Check these files:
- `EMBEDDING_LOGGING_ENHANCEMENTS.md` - Detailed technical docs
- `notes/EMBEDDING_LOG_OUTPUT_EXAMPLE.md` - Full output examples
- `EMBEDDING_SCRIPT_ENHANCEMENT_SUMMARY.md` - Complete change summary

Look for patterns in the logs:
- Multiple ✗ MISSING → Model download issue
- Low chunk counts → Chunking issue
- Slow speeds → GPU/performance issue
- Export failures → Disk space issue
