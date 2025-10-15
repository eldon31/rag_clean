"""
DOCLING EMBEDDING PIPELINE - COMPLETE WORKFLOW
===============================================

This document outlines the complete workflow for processing Docling documentation
from chunking to Qdrant upload, with full auditing at each step.

## WORKFLOW OVERVIEW

1. Local: Chunk documents
2. Local: Audit chunks  
3. Upload: Chunks to Kaggle dataset
4. Kaggle: Generate embeddings (GPU T4 x2)
5. Download: Embeddings from Kaggle
6. Local: Audit embeddings
7. Local: Upload to Qdrant
8. Verify: Collection in Qdrant

## STEP-BY-STEP IMPLEMENTATION

### STEP 1: Chunk Documents (LOCAL)
```bash
python scripts/chunk_docling_simple.py
```

Output:
- `output/docling/chunked/*.json` - Individual chunk files (46 files)
- `output/docling/chunked/chunking_summary.json` - Processing stats

Expected results:
- 1,060 chunks
- 46 markdown files processed
- ~184 tokens per chunk average
- ~196K total tokens

### STEP 2: Audit Chunks (LOCAL)
```bash
python scripts/audit_chunks.py
```

Checks:
✅ All chunk files valid JSON
✅ No duplicate IDs (1,060 unique)
✅ No empty content
✅ Complete metadata
✅ Proper file structure

Output:
- `output/docling/pre_kaggle_audit.txt` - Detailed audit report
- Console output with statistics

Expected result: All checks should pass ✅

### STEP 3: Prepare for Kaggle Upload

#### 3a. Create ZIP file
```bash
# Windows PowerShell
Compress-Archive -Path output/docling/chunked -DestinationPath docling_chunks.zip

# Or manually:
# Right-click output/docling/chunked -> Send to -> Compressed folder
```

#### 3b. Upload to Kaggle
1. Go to https://www.kaggle.com/datasets
2. Click "New Dataset"
3. Upload `docling_chunks.zip`
4. Title: "Docling Documentation Chunks"
5. Subtitle: "Pre-chunked Docling docs for embedding generation"
6. Make it private (or public if sharing)
7. Click "Create"
8. Note the dataset path: `<username>/docling-chunks`

### STEP 4: Generate Embeddings (KAGGLE)

#### 4a. Create Kaggle Notebook
1. Go to https://www.kaggle.com/code
2. Click "New Notebook"
3. Title: "Docling Embedding Generation"
4. Settings:
   - Accelerator: **GPU T4 x2** (REQUIRED)
   - Language: Python
   - Environment: Latest

#### 4b. Add Dataset to Notebook
1. Click "+ Add Data" 
2. Search for your "docling-chunks" dataset
3. Click "Add"

#### 4c. Upload Processing Script
1. Upload `scripts/kaggle_embed_docling.py` to notebook
2. Or copy-paste the entire script into a cell

#### 4d. Update Paths in Script
```python
# Update this line in kaggle_embed_docling.py:
CHUNKED_INPUT_DIR = Path("/kaggle/input/docling-chunks")
```

#### 4e. Run the Notebook
Execute all cells or run the script:
```python
!python kaggle_embed_docling.py
```

Expected output:
- Processing time: ~2-3 minutes (GPU T4 x2)
- 1,060 embeddings generated
- Vector dimension: 3584
- Output: `/kaggle/working/docling_embeddings.jsonl`

#### 4f. Monitor Progress
Watch for:
- GPU initialization (should show 2x T4 GPUs)
- Model loading (model parallelism across GPUs)
- Batch processing (8 chunks per second expected)
- No errors or warnings
- Final summary with stats

### STEP 5: Download Embeddings (KAGGLE -> LOCAL)

1. In Kaggle notebook, check output files:
```python
!ls -lh /kaggle/working/
```

2. Download files:
   - `docling_embeddings.jsonl` - Main embeddings file (~15 MB)
   - `docling_embedding_summary.json` - Processing statistics

3. Save to local:
   - `output/docling/embeddings/docling_embeddings.jsonl`

### STEP 6: Audit Embeddings (LOCAL)
```bash
python scripts/audit_embeddings.py
```

Checks:
✅ All embeddings have IDs
✅ All have text content
✅ Vector dimension = 3584 (nomic-embed-code)
✅ No NaN or inf values
✅ No zero vectors
✅ Metadata consistency
✅ Vector norm statistics

Output:
- `output/docling/post_kaggle_audit.txt` - Detailed audit report
- Console output with validation results

Expected result: All checks should pass ✅

### STEP 7: Upload to Qdrant (LOCAL)

#### 7a. Start Qdrant
```bash
# Using Docker
docker-compose up -d

# Or Docker command directly
docker run -p 6333:6333 qdrant/qdrant
```

Verify Qdrant is running:
```bash
curl http://localhost:6333
```

#### 7b. Upload Embeddings
```bash
python scripts/upload_to_qdrant.py --collection docling --file output/docling/embeddings/docling_embeddings.jsonl
```

Expected output:
- Collection created with:
  - Vector size: 3584
  - Distance: Cosine
  - Quantization: int8 (enabled)
- 1,060 points uploaded
- Batch upload (100 points per batch)
- Upload time: ~5-10 seconds

### STEP 8: Verify Upload (LOCAL)

#### 8a. Check Collection
```bash
curl http://localhost:6333/collections/docling
```

Expected response:
```json
{
  "result": {
    "status": "green",
    "vectors_count": 1060,
    "indexed_vectors_count": 1060,
    "points_count": 1060
  }
}
```

#### 8b. Test Search
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Get a sample embedding
results = client.scroll(
    collection_name="docling",
    limit=1,
    with_vectors=True
)

# Use it to search
if results[0]:
    sample_vector = results[0][0].vector
    search_results = client.search(
        collection_name="docling",
        query_vector=sample_vector,
        limit=5
    )
    
    print(f"Found {len(search_results)} results")
    for result in search_results:
        print(f"  Score: {result.score:.4f}")
        print(f"  Text: {result.payload.get('text', '')[:100]}...")
```

## TROUBLESHOOTING

### Issue: NumPy 2.x error on Kaggle
**Solution:**
```python
!pip install -q --force-reinstall "numpy==1.26.4" "scikit-learn==1.4.2"
# Then restart kernel
```

### Issue: Out of memory on Kaggle
**Solutions:**
1. Reduce BATCH_SIZE from 8 to 4
2. Use single GPU instead of dual GPU
3. Enable gradient checkpointing

### Issue: Wrong vector dimensions
**Solution:**
- Verify model: `nomic-ai/nomic-embed-code` (not nomic-embed-text)
- Check audit_embeddings.py output
- Re-run Kaggle notebook with correct model

### Issue: Qdrant connection refused
**Solutions:**
1. Check Docker: `docker ps`
2. Start Qdrant: `docker-compose up -d`
3. Verify port: `curl http://localhost:6333`

### Issue: Slow embedding generation
**Expected speeds:**
- GPU T4 x2: 8-10 chunks/sec (~2-3 min total)
- GPU T4 x1: 4-5 chunks/sec (~4-5 min total)
- CPU only: 0.5-1 chunk/sec (~20-30 min total)

**Solution:** Ensure GPU T4 x2 is selected in Kaggle settings

## VERIFICATION CHECKLIST

Before each step, verify:

- [ ] STEP 1: Chunks created (1,060 chunks in 46 files)
- [ ] STEP 2: Pre-audit passed (all ✅)
- [ ] STEP 3: ZIP created and uploaded to Kaggle
- [ ] STEP 4: Kaggle GPU T4 x2 selected
- [ ] STEP 4: Embeddings generated (3584-dim vectors)
- [ ] STEP 5: Downloaded embeddings file (~15 MB)
- [ ] STEP 6: Post-audit passed (all ✅)
- [ ] STEP 7: Qdrant running (port 6333)
- [ ] STEP 7: Upload completed (1,060 points)
- [ ] STEP 8: Collection verified (green status)
- [ ] STEP 8: Search test successful

## FILE MANIFEST

### Input Files
```
Docs/docling-project_docling/
├── _docling-project_docling.md
├── _docling-project_docling_1-overview.md
├── ... (46 markdown files total)
```

### Generated Files
```
output/docling/
├── chunked/
│   ├── *_chunks.json (46 files)
│   ├── chunking_summary.json
│   └── (ZIP this folder for Kaggle)
├── embeddings/
│   ├── docling_embeddings.jsonl (~15 MB)
│   └── docling_embedding_summary.json
├── pre_kaggle_audit.txt
└── post_kaggle_audit.txt
```

### Scripts Used
```
scripts/
├── chunk_docling_simple.py          # STEP 1
├── audit_chunks.py                  # STEP 2
├── kaggle_embed_docling.py          # STEP 4 (run on Kaggle)
├── audit_embeddings.py              # STEP 6
└── upload_to_qdrant.py              # STEP 7
```

## FINAL METRICS

Expected final state:
- **Chunks:** 1,060
- **Embeddings:** 1,060 (3584-dim vectors)
- **Qdrant collection:** "docling"
- **Vector count:** 1,060
- **Quantization:** int8 enabled
- **Memory usage:** ~3.7 MB (with quantization)
- **Search ready:** ✅

## NEXT STEPS

After successful upload:
1. Build RAG application using the collection
2. Implement semantic search endpoints
3. Add metadata filtering (source, heading_level, etc.)
4. Enable hybrid search (dense + sparse)
5. Monitor query performance and accuracy
"""

# Save this as a reference document
if __name__ == "__main__":
    print(__doc__)
