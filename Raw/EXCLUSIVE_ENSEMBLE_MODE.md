# Exclusive Ensemble Mode

## Overview

Exclusive Ensemble Mode is an opt-in feature that enables ensemble models to run in isolated passes with exclusive GPU access, allowing for larger batch sizes without OOM risk. Instead of rotating models batch-by-batch, this mode processes **all chunks** for one model before releasing the GPUs and moving to the next model.

## Motivation

Sequential ensemble mode rotates models batch-by-batch but keeps each encoder resident on GPU memory until eviction, forcing conservative batch hints to avoid exceeding memory limits. Exclusive ensemble mode addresses this by:

- **Leasing both GPUs exclusively** to the active model during its full collection pass
- **Staging other models on CPU** until their turn
- **Enabling larger batch sizes** up to the 12 GB soft ceiling without concurrency-induced OOM
- **Simplifying GPU resource management** with deterministic lease lifecycle

## How It Works

### Model-First Iteration

Exclusive mode changes the execution order:

**Standard Sequential:**
```
for batch in chunks:
    for model in ensemble_models:
        encode(model, batch)
```

**Exclusive Sequential:**
```
for model in ensemble_models:
    acquire_gpu_lease(model)
    for batch in chunks:
        encode(model, batch)
    release_gpu_lease(model)
```

### GPU Lease Lifecycle

1. **Acquisition**: Reserve both GPUs, evict previous model caches, capture VRAM snapshots
2. **Hydration**: Move model from CPU to GPU, rebuild DataParallel wrappers if needed
3. **Processing**: Encode all batches with exclusive GPU access
4. **Release**: Capture final VRAM, evict cache, move model back to CPU

### Adaptive Batching

Each model pass **resets the adaptive batch controller** with fresh hints, allowing per-model tuning based on the model's memory footprint.

## Configuration

### Via CLI (scripts/embed_collections_v6.py)

```bash
python scripts/embed_collections_v6.py \
    --chunked-dir ./Chunked \
    --exclusive-ensemble \
    --ensemble-models jina-code-embeddings-1.5b bge-m3 qwen3-embedding-0.6b
```

**Note**: On Kaggle, `--exclusive-ensemble` defaults to `True` automatically.

### Via Environment Variable

```bash
export EMBEDDER_EXCLUSIVE_ENSEMBLE=1
export EMBEDDER_SEQUENTIAL_ENSEMBLE=1
```

### Via Code

```python
from processor.ultimate_embedder.config import EnsembleConfig
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4

ensemble_config = EnsembleConfig(
  ensemble_models=["jina-code-embeddings-1.5b", "bge-m3", "qwen3-embedding-0.6b"],
  sequential_passes=True,
  exclusive_mode=True,  # Enable exclusive ensemble
  warm_cache_after_release=False,  # Set True to keep models resident after passes
)

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    enable_ensemble=True,
    ensemble_config=ensemble_config,
)
```

## Telemetry

Exclusive mode adds GPU lease events to the telemetry stream:

```json
{
  "gpu_lease_events": [
    {
      "timestamp": 1234567890.123,
      "event_type": "acquire",
      "model": "bge-m3",
      "device_ids": [0, 1],
      "vram": {
        "0": {"allocated_gb": 2.1, "reserved_gb": 2.5},
        "1": {"allocated_gb": 0.3, "reserved_gb": 0.5}
      }
    },
    {
      "timestamp": 1234567920.456,
      "event_type": "release",
      "model": "bge-m3",
      "device_ids": [0, 1],
      "vram": {
        "0": {"allocated_gb": 0.1, "reserved_gb": 0.2},
        "1": {"allocated_gb": 0.0, "reserved_gb": 0.0}
      }
    }
  ]
}
```

### Trade-offs

### Advantages
- ✅ **Larger batch sizes** per model without OOM risk
- ✅ **Deterministic resource allocation** with explicit lease lifecycle
- ✅ **Better GPU utilization** for memory-intensive models
- ✅ **Per-model telemetry** for VRAM usage and pass duration
- ✅ Optional **warm-cache mode** to retain models on GPU between passes when capacity allows

### Disadvantages
- ⚠️ **Repeated model transfers** between CPU and GPU add latency (when warm cache disabled)
- ⚠️ **No batch-level concurrency** between models
- ⚠️ **Requires sequential_passes=True** (mutually exclusive with parallel encoding)
- ⚠️ Warm cache mode retains VRAM between passes and should be used only when memory headroom is known

## Best Practices

1. **Enable only when needed**: Use standard sequential mode unless you're hitting OOM with conservative batch sizes
2. **Monitor lease events**: Check telemetry for VRAM deltas to validate memory gains
3. **Tune per-model batch hints**: Exclusive mode allows larger batch sizes; adjust `base_batch_size` in `KaggleGPUConfig` accordingly
4. **Validate aggregation parity**: Confirm that per-model-then-aggregate produces the same results as batch-by-batch rotation

## Example Run Summary

```json
{
  "ensemble_mode": "exclusive",
  "models_executed": ["jina-code-embeddings-1.5b", "bge-m3", "qwen3-embedding-0.6b"],
  "total_embeddings_generated": 3096,
  "processing_time_seconds": 45.2,
  "chunks_per_second": 68.5,
  "lease_events": [
    {"model": "jina-code-embeddings-1.5b", "duration": 15.1, "vram_delta_gb": {"gpu_0": 0.8, "gpu_1": 0.7}},
    {"model": "bge-m3", "duration": 14.5, "vram_delta_gb": {"gpu_0": 1.1, "gpu_1": 1.0}},
    {"model": "qwen3-embedding-0.6b", "duration": 15.6, "vram_delta_gb": {"gpu_0": 0.5, "gpu_1": 0.5}}
  ]
}
```

## Migration Path

Exclusive mode is **opt-in** and disabled by default. Existing workflows remain unchanged unless `--exclusive-ensemble` is explicitly passed or `EMBEDDER_EXCLUSIVE_ENSEMBLE=1` is set.

## Related Configuration

- `ensemble_config.sequential_passes`: Must be `True` for exclusive mode
- `ensemble_config.sequential_data_parallel`: Rewraps models with DataParallel when multiple GPUs are leased
- `ensemble_config.preferred_devices`: Device order for leasing (e.g., `["cuda:1", "cuda:0"]`)
- `gpu_config.base_batch_size`: Initial batch hint before adaptive controller adjustments

## Validation

Run integration tests with exclusive mode enabled:

```bash
python -m pytest tests/test_exclusive_ensemble_integration.py --verbose
```

Validate that:
- ✅ Models are staged to CPU before passes
- ✅ GPU leases are acquired and released correctly
- ✅ VRAM is freed between passes
- ✅ Final embeddings match non-exclusive aggregation
- ✅ Warm cache flag skips CPU staging when enabled (see `tests/test_exclusive_ensemble_integration.py`)
