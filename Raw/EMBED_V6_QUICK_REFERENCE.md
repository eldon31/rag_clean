# Embed Collections V6 - Quick Reference Guide

**Purpose:** Fast lookup for developers working with `embed_collections_v6.py`

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Command Cheat Sheet](#command-cheat-sheet)
3. [Function Quick Reference](#function-quick-reference)
4. [Expected Outputs](#expected-outputs)
5. [Troubleshooting Guide](#troubleshooting-guide)

---

## Quick Start

### Local Development
```bash
# Process all collections (exclusive mode - ONLY MODE)
python scripts/embed_collections_v6.py --verbose

# Process specific collections only
python scripts/embed_collections_v6.py --collections Docling FAST_DOCS_fastapi
```

### Kaggle Production
```bash
# In Kaggle notebook cell (exclusive mode is the ONLY mode)
!python scripts/embed_collections_v6.py \
  --chunked_dir /kaggle/input/yourdata/Chunked \
  --output_dir /kaggle/working
```

---

## Command Cheat Sheet

### Basic Commands

| Command | Description |
|---------|-------------|
| `python scripts/embed_collections_v6.py` | Process all collections (exclusive mode only) |
| `python scripts/embed_collections_v6.py --help` | Show all available options |
| `python scripts/embed_collections_v6.py --verbose` | Enable debug logging |

### Common Argument Patterns

```bash
# Specify input directory
--chunked_dir /path/to/Chunked

# Specify output directory
--output_dir /path/to/output

# Process only specific collections
--collections Collection1 Collection2 Collection3

# Custom ensemble models
--ensemble_models model1 model2 model3

# Custom ensemble weights
--ensemble_weights 0.5 0.3 0.2

# Adjust batch size
--batch_size 64

# Custom model cache
--model_cache_dir /path/to/cache

# Custom Qdrant connection
--qdrant_host localhost --qdrant_port 6333

# ZIP Archive Export (NEW in V6.1)
--create-zip                        # Create ZIP archive after processing
--zip-compression deflated          # Use compression (default)
--zip-compression stored            # No compression (faster, larger)
```

### Complete Example

```bash
python scripts/embed_collections_v6.py \
  --chunked_dir ./Chunked \
  --output_dir ./output \
  --collections Docling FAST_DOCS_fastapi \
  --ensemble_models sentence-transformers/all-MiniLM-L6-v2 \
                    BAAI/bge-small-en-v1.5 \
                    nomic-ai/nomic-embed-text-v1.5 \
  --batch_size 64 \
  --verbose
```

### ZIP Export Example (NEW)

```bash
# Create compressed ZIP archive for download/distribution
python scripts/embed_collections_v6.py \
  --chunked_dir ./Chunked \
  --output_dir ./output \
  --create-zip \
  --zip-compression deflated

# Output: ./output/embeddings_2025-10-23_14-30-45.zip
#   - All collections packaged
#   - MANIFEST.txt included
#   - Integrity verified
#   - Ready for download
```

---

## Function Quick Reference

### Discovery Functions

#### `discover_collections(chunked_dir, max_depth=5)`
**Returns:** `dict[str, Path]`  
**Finds:** All directories containing `*_chunks.json` files up to 5 levels deep  
**Example:** `{"Docling": Path("Chunked/Docling"), ...}`

#### `_is_collection_directory(directory)`
**Returns:** `bool`  
**Checks:** If directory contains chunk files (non-recursive)  
**Use:** Identify collection directories

#### `_resolve_collection_name(collection_dir, chunked_dir, seen_names)`
**Returns:** `str` (unique collection name)  
**Handles:** Name collision with relative paths  
**Example:** `"FAST_DOCS_fastapi_fastapi"` for nested structure

---

### Processing Functions

#### `process_collection(name, path, embedder, args)`
**Returns:** `dict` with results and telemetry  
**Does:** Complete embedding pipeline for one collection  
**Keys:** `models_executed`, `lease_events`, `total_embeddings_generated`

#### `_extract_telemetry(results)`
**Returns:** `tuple[list, list, int]`  
**Extracts:** `(models_executed, lease_events, total_embeddings)`  
**Safe:** Returns defaults if fields missing

#### `_log_collection_completion(name, models, events, count, exclusive)`
**Returns:** `None`  
**Logs:** Completion summary with GPU lease events (if exclusive mode)  
**Format:** Structured INFO logs with checkmark

---

### Orchestration Functions

#### `_filter_collections(all_collections, requested)`
**Returns:** `dict[str, Path]` (filtered subset)  
**Validates:** Requested collections exist  
**Raises:** `ValueError` if collections not found

#### `_initialize_embedder(models, exclusive, weights)`
**Returns:** `UltimateKaggleEmbedderV4` instance  
**Creates:** All config objects (Ensemble, GPU, Export)  
**Raises:** `RuntimeError` if initialization fails

#### `_log_processing_summary(results, failed)`
**Returns:** `None`  
**Logs:** Final statistics (total/success/failure)  
**Shows:** Failed collections with exception types

#### `_export_summary_json(results, file, models, exclusive)`
**Returns:** `None`  
**Writes:** JSON summary to file  
**Includes:** Timestamp, environment, results, failures

---

### Utility Functions

#### `_get_ensemble_mode_label(exclusive_mode)`
**Returns:** `"EXCLUSIVE (model-at-a-time GPU lease)"` (always exclusive mode)  
**Use:** Display ensemble mode in logs

#### `parse_arguments()`
**Returns:** `argparse.Namespace`  
**Detects:** Kaggle vs Local environment  
**Sets:** Environment-aware defaults

---

## Expected Outputs

### Console Output (Summary)

```
INFO - Scanning for collections in: Chunked
INFO - Total collections discovered: 224
INFO - Initializing embedder...
INFO - Processing collection: Docling
INFO - ✅ Completed collection: Docling
...
INFO - PROCESSING COMPLETE
INFO - Total collections: 224
INFO - Successfully processed: 224
INFO - Failed: 0
INFO - Summary exported to output/embedding_summary_v6.json
INFO - Processing complete!
```

### File Outputs

| File | Location | Format | Content |
|------|----------|--------|---------|
| **Log File** | `{output_dir}/embedding_v6.log` | Text | Detailed logs with timestamps |
| **JSON Summary** | `{output_dir}/embedding_summary_v6.json` | JSON | Results and metadata |
| **Qdrant Collections** | Qdrant DB | Binary | Vector embeddings with payloads |

### JSON Summary Structure

```json
{
  "timestamp": "2025-10-22T14:35:22.123456",
  "environment": "Kaggle",
  "ensemble_models": ["model1", "model2", "model3"],
  "exclusive_ensemble_mode": true,
  "results": {
    "Docling": {
      "models_executed": ["model1", "model2", "model3"],
      "lease_events": [...],
      "total_embeddings_generated": 1000,
      "qdrant_collection": "Docling"
    }
  },
  "failed_collections": {}
}
```

### Qdrant Collection

```python
# Each collection contains:
{
    "collection_name": "Docling",
    "vectors_config": {
        "size": 384,  # Embedding dimension
        "distance": "Cosine"
    },
    "points_count": 1000,
    "points": [
        {
            "id": "chunk_id",
            "vector": [0.123, -0.456, ...],  # 384 dimensions
            "payload": {
                "text": "Chunk text content",
                "chunk_id": "doc1_chunk_0",
                "metadata": {...}
            }
        }
    ]
}
```

---

## Troubleshooting Guide

### Problem: No collections discovered

**Symptom:**
```
INFO - Total collections discovered: 0
ERROR - No collections discovered.
```

**Solutions:**
1. Verify chunk files exist: `ls -R Chunked/ | grep chunks.json`
2. Check file pattern matches: `*_chunks.json`
3. Verify directory structure is correct
4. Increase max depth if needed (edit `MAX_DISCOVERY_DEPTH`)

---

### Problem: Requested collection not found

**Symptom:**
```
ERROR - None of the requested collections were found.
ERROR - Requested: {'MyCollection'}
ERROR - Available: {'Docling', 'FAST_DOCS_fastapi', ...}
```

**Solutions:**
1. Run discovery first to see available names:
   ```bash
   python scripts/embed_collections_v6.py --verbose 2>&1 | grep "Discovered collection"
   ```
2. Use exact names from discovery output
3. Check for path-based names (e.g., `FAST_DOCS_fastapi_fastapi`)
4. Verify spelling and capitalization

---

### Problem: GPU out of memory

**Symptom:**
```
ERROR - CUDA out of memory
RuntimeError: CUDA out of memory. Tried to allocate ...
```

**Solutions:**
1. Reduce batch size:
   ```bash
   python scripts/embed_collections_v6.py --batch_size 32
   ```
2. Use fewer ensemble models
3. Check available GPU memory: `nvidia-smi`

**Note:** System now uses exclusive mode only (model-at-a-time), which significantly reduces GPU memory requirements compared to the old parallel mode.

---

### Problem: Qdrant connection failed

**Symptom:**
```
ERROR - Failed to connect to Qdrant: Connection refused
```

**Solutions:**
1. Start Qdrant server:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
2. Verify Qdrant is running: `curl http://localhost:6333/health`
3. Check host/port arguments match your setup
4. Verify firewall settings

---

### Problem: Slow processing on Kaggle

**Symptom:**
- Processing takes hours
- GPU lease events show long wait times

**Solutions:**
1. Already using exclusive mode (correct for Kaggle)
2. Reduce number of collections:
   ```bash
   python scripts/embed_collections_v6.py --collections Docling FAST_DOCS
   ```
3. Increase batch size (if memory allows):
   ```bash
   python scripts/embed_collections_v6.py --batch_size 128
   ```
4. Monitor GPU lease events in logs to identify bottlenecks

---

### Problem: Collection processing fails silently

**Symptom:**
```
INFO - Processing collection: MyCollection
# ... no completion log
```

**Solutions:**
1. Enable verbose logging:
   ```bash
   python scripts/embed_collections_v6.py --verbose
   ```
2. Check log file for detailed errors: `cat output/embedding_v6.log | grep ERROR`
3. Check JSON summary for failed_collections:
   ```bash
   cat output/embedding_summary_v6.json | jq '.failed_collections'
   ```
4. Verify chunk files are valid JSON

---

### Problem: Import errors

**Symptom:**
```
ImportError: cannot import name 'UltimateKaggleEmbedderV4'
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solutions:**
1. Install required packages:
   ```bash
   pip install sentence-transformers qdrant-client torch
   ```
2. Verify embedder module exists:
   ```bash
   ls processor/kaggle_ultimate_embedder_v4.py
   ```
3. Check Python path includes project root
4. Restart Python interpreter/kernel

---

## Performance Metrics

### Discovery Performance

| Collections | Files | Time |
|-------------|-------|------|
| 1 | 10 | <1s |
| 10 | 100 | ~2s |
| 100 | 1000 | ~10s |
| 224 | 2000+ | ~20s |

### Processing Performance (per collection)

**Note:** System now uses exclusive mode only (model-at-a-time GPU lease)

| Models | Chunks | Time | GPU Peak |
|--------|--------|------|----------|
| 3 | 100 | ~150s | 4GB |
| 3 | 1000 | ~750s | 5GB |
| 3 | 10000 | ~7500s | 5GB |

### Scalability Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| **Max Depth** | 5 levels | Configurable via `MAX_DISCOVERY_DEPTH` |
| **GPU Memory (Kaggle)** | 16GB T4 | Use exclusive mode |
| **Collections** | Unlimited | Tested with 224 |
| **Chunks per Collection** | Unlimited | Limited by disk space |

---

## Constants Reference

| Constant | Value | Purpose |
|----------|-------|---------|
| `CHUNK_FILE_PATTERN` | `"*_chunks.json"` | Identify collection directories |
| `MAX_DISCOVERY_DEPTH` | `5` | Maximum recursion depth |
| `RESULT_KEY_MODELS_EXECUTED` | `"models_executed"` | Results dict key |
| `RESULT_KEY_LEASE_EVENTS` | `"lease_events"` | Results dict key |
| `RESULT_KEY_TOTAL_EMBEDDINGS` | `"total_embeddings_generated"` | Results dict key |
| `DEFAULT_FALLBACK_MODEL` | `"nomic-ai/nomic-embed-text-v1.5"` | Fallback model |

---

## Default Configuration

### Local Environment
```python
chunked_dir = "./Chunked"
output_dir = "./Embeddings"
exclusive_ensemble = True  # Exclusive mode (ONLY MODE - parallel mode removed)
sequential_passes = True   # Required for exclusive mode
warm_cache_after_release = False
qdrant_host = "localhost"
qdrant_port = 6333
```

### Kaggle Environment
```python
chunked_dir = "/kaggle/input/yourdata/Chunked"
output_dir = "/kaggle/working"
exclusive_ensemble = True  # Exclusive mode (ONLY MODE - parallel mode removed)
sequential_passes = True   # Required for exclusive mode
warm_cache_after_release = False
qdrant_host = "localhost"
qdrant_port = 6333
model_cache_dir = "/kaggle/working/hf_cache"
```

---

## Testing Commands

### Run Unit Tests
```bash
# All tests
python -m pytest tests/test_embed_v6_refactor.py -v

# Specific test class
python -m pytest tests/test_embed_v6_refactor.py::TestCollectionDiscovery -v

# With coverage
python -m pytest tests/test_embed_v6_refactor.py --cov=scripts.embed_collections_v6
```

### Validate Discovery
```bash
# Test discovery logic
python test_discovery.py

# Check specific collection
python -c "
from pathlib import Path
from scripts.embed_collections_v6 import discover_collections
cols = discover_collections(Path('Chunked'))
print(f'Found {len(cols)} collections')
print(list(cols.keys())[:10])
"
```

### Check Help
```bash
# View all options
python scripts/embed_collections_v6.py --help

# View with current defaults
python scripts/embed_collections_v6.py --help | grep -A 20 "Current defaults"
```

---

## Monitoring & Debugging

### Monitor GPU Usage (During Run)
```bash
# Watch GPU memory
watch -n 1 nvidia-smi

# Log GPU stats
nvidia-smi --query-gpu=timestamp,memory.used,memory.free --format=csv -l 5 > gpu_log.csv
```

### Monitor Logs (During Run)
```bash
# Tail log file
tail -f output/embedding_v6.log

# Filter for errors
tail -f output/embedding_v6.log | grep ERROR

# Filter for completions
tail -f output/embedding_v6.log | grep "✅ Completed"
```

### Check Qdrant Collections
```bash
# List all collections
curl http://localhost:6333/collections | jq '.'

# Get collection info
curl http://localhost:6333/collections/Docling | jq '.'

# Count points in collection
curl http://localhost:6333/collections/Docling | jq '.result.points_count'
```

---

## Best Practices

### For Local Development
1. ✅ Use `--collections` to test specific collections first
2. ✅ Enable `--verbose` for debugging
3. ✅ Monitor GPU memory with `nvidia-smi` (exclusive mode uses less memory)
4. ✅ Test with small subset before full run
5. ✅ Exclusive mode is now the only mode (no configuration needed)

### For Kaggle Production
1. ✅ Exclusive mode is automatic (no flags needed)
2. ✅ Point to Kaggle input dataset paths
3. ✅ Output to `/kaggle/working`
4. ✅ Monitor GPU lease events in logs
5. ✅ Download JSON summary before notebook ends

### For Large-Scale Processing
1. ✅ Process in batches (use `--collections`)
2. ✅ Monitor disk space for Qdrant collections
3. ✅ Save JSON summary periodically
4. ✅ Use checkpointing (manual restart with filtered collections)
5. ✅ Monitor failed_collections in summary

---

## Quick Debug Checklist

Before asking for help, verify:

- [ ] Chunk files exist and match `*_chunks.json` pattern
- [ ] Qdrant is running and accessible
- [ ] GPU has sufficient memory (or using exclusive mode)
- [ ] Python packages installed (sentence-transformers, qdrant-client)
- [ ] Verbose logging enabled (`--verbose`)
- [ ] Log file checked for detailed errors
- [ ] JSON summary checked for failed_collections
- [ ] GPU usage monitored (for memory issues)
- [ ] Collection names match discovery output exactly

---

## Additional Resources

- **Full Architecture**: See `Docs/EMBED_V6_ARCHITECTURE.md`
- **Visual Flow**: See `Docs/EMBED_V6_VISUAL_FLOW.md`
- **Refactor Report**: See `notes/V6_REFACTOR_COMPLETION_REPORT.md`
- **Unit Tests**: See `tests/test_embed_v6_refactor.py`
- **Source Code**: `scripts/embed_collections_v6.py`

---

## Contact & Support

For issues or questions:
1. Check this quick reference first
2. Review verbose logs for errors
3. Check failed_collections in JSON summary
4. Verify configuration against defaults
5. Test with small subset using `--collections`

**Version:** V6.1 (Simplified Architecture)  
**Last Updated:** October 23, 2025  
**Status:** ✅ Parallel Mode Removed - Exclusive Mode Only
