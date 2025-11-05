## Where to See Sparse/SPLADE Throughput Output

### 1. Console Logs (Real-time)

When sparse is **enabled** and running, you'll see:

```
Sparse configuration check: enable_sparse=True, sparse_models_loaded=True
Sparse models available: ['splade']
======================================================================
SPARSE VECTOR GENERATION STAGE
======================================================================
[sparse] Starting inference: chunks=738 model=splade device_hint=cpu
[throughput] stage_start | stage=sparse | model=splade | device=cpu
```

Then during processing:

```
[throughput] [OK] success | duration=0.35s | rate=14.22/s | errors=0
```

At the end of the run:

```
[throughput] done | model=<model> | chunks=738 | duration=45.2s | rate=16.32/s | stages=1 | errors=0 | warnings=0
```

The `stages=1` indicates sparse stage ran successfully.

### 2. If Sparse is NOT Running

You'll see one of these messages:

```
Skipping sparse stage: sparse disabled
```

or

```
Skipping sparse stage: no sparse models loaded
```

### How to Enable Sparse

**Option A: Don't use `--disable-sparse` flag**

```bash
python scripts/embed_collections_v7.py --collection-name mydata --chunk-dir ./Chunked
# Sparse is enabled by default
```

**Option B: Explicitly specify sparse models**

```bash
python scripts/embed_collections_v7.py \
  --collection-name mydata \
  --chunk-dir ./Chunked \
  --sparse-models splade
```

### Expected Output Files

After successful run with sparse enabled:

1. **Sparse vectors**: `{output_dir}/ultimate_embeddings_v7_sparse.jsonl`
2. **Processing summary**: `{output_dir}/processing_summary.json`

The summary will contain:

```json
{
  "sparse_run": {
    "executed": true,
    "models": ["splade"],
    "chunks_processed": 738,
    "latency_ms": 350.5,
    "throughput_chunks_per_sec": 14.22,
    "device": "cpu",
    "fallback_count": 0
  }
}
```

### Quick Verification

To quickly check if sparse ran, look for:

1. `stages=1` or `stages=2` in throughput logs (0 = no stages ran)
2. `Sparse models available: ['splade']` in logs
3. `_sparse.jsonl` file in output directory
