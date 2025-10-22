# Kaggle Validation Plan: Exclusive Ensemble Mode

## Overview

This document outlines the manual validation steps for exclusive ensemble mode on Kaggle's dual-T4 GPU environment. Local testing is CPU-only; GPU-specific behavior must be validated in Kaggle.

## Prerequisites

- Kaggle notebook with dual T4 GPUs enabled
- Access to chunked data (small test collection recommended)
- `--exclusive-ensemble` flag implemented in `embed_collections_v5.py`

## Test Scenarios

### 1. Basic Exclusive Mode Activation

**Goal:** Verify exclusive mode activates correctly and models are staged to CPU.

**Steps:**
```python
from processor.ultimate_embedder.config import EnsembleConfig, KaggleGPUConfig
from processor.ultimate_embedder.core import UltimateKaggleEmbedderV4

ensemble_config = EnsembleConfig(
    ensemble_models=["jina-code-embeddings-1.5b", "bge-m3"],
    sequential_passes=True,
    exclusive_mode=True,
)

embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    enable_ensemble=True,
    ensemble_config=ensemble_config,
)

# Check that models are staged on CPU
for model_name, model in embedder.models.items():
    device = next(model.parameters()).device if hasattr(model, 'parameters') else 'unknown'
    print(f"{model_name}: {device}")
```

**Expected:**
- All ensemble models should be on CPU initially
- Log message: "Exclusive ensemble mode: staging primary model to CPU"

### 2. GPU Lease Lifecycle

**Goal:** Verify GPU leases acquire and release correctly with telemetry.

**Steps:**
```python
# Load small test collection
embedder.load_chunks_from_processing(chunks_dir="/kaggle/input/test-chunks/")

# Run exclusive ensemble
results = embedder.generate_embeddings_kaggle_optimized()

# Check lease events
lease_events = embedder.telemetry.gpu_lease_events
print(f"Total lease events: {len(lease_events)}")

for event in lease_events:
    print(f"{event['event_type']}: {event['model']} on devices {event['device_ids']}")
    if 'vram' in event:
        for dev_id, vram in event['vram'].items():
            print(f"  GPU {dev_id}: {vram.get('allocated_gb', 0):.2f} GB allocated")
```

**Expected:**
- 2 acquire events and 2 release events (for 2 models)
- Each acquire should show both GPU IDs [0, 1]
- VRAM should be captured for both events

### 3. VRAM Release Between Passes

**Goal:** Verify GPU memory is freed between model passes.

**Steps:**
```python
import torch

# Run with monitoring
embedder.load_chunks_from_processing(chunks_dir="/kaggle/input/test-chunks/")

# Manually check VRAM before run
print("Before run:")
for i in range(torch.cuda.device_count()):
    allocated = torch.cuda.memory_allocated(i) / 1e9
    print(f"  GPU {i}: {allocated:.2f} GB allocated")

results = embedder.generate_embeddings_kaggle_optimized()

# Check VRAM deltas in telemetry
for event in embedder.telemetry.gpu_lease_events:
    if event['event_type'] == 'release':
        print(f"\n{event['model']} release:")
        for dev_id, vram in event['vram'].items():
            print(f"  GPU {dev_id}: {vram.get('allocated_gb', 0):.2f} GB allocated")
```

**Expected:**
- VRAM should drop significantly after each release event
- GPU 0 should be under 1 GB between passes
- GPU 1 should be close to 0 GB between passes

### 4. Enlarged Batch Sizes

**Goal:** Verify that exclusive mode allows larger batch sizes without OOM.

**Steps:**
```python
# Standard sequential mode
embedder_standard = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    enable_ensemble=True,
    ensemble_config=EnsembleConfig(
        ensemble_models=["jina-code-embeddings-1.5b", "bge-m3"],
        sequential_passes=True,
        exclusive_mode=False,  # Standard mode
    ),
)

embedder_standard.load_chunks_from_processing(chunks_dir="/kaggle/input/test-chunks/")
results_standard = embedder_standard.generate_embeddings_kaggle_optimized()

# Exclusive mode
embedder_exclusive = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    enable_ensemble=True,
    ensemble_config=EnsembleConfig(
        ensemble_models=["jina-code-embeddings-1.5b", "bge-m3"],
        sequential_passes=True,
        exclusive_mode=True,  # Exclusive mode
    ),
)

embedder_exclusive.load_chunks_from_processing(chunks_dir="/kaggle/input/test-chunks/")
results_exclusive = embedder_exclusive.generate_embeddings_kaggle_optimized()

# Compare batch sizes
print(f"Standard batch size: {results_standard.get('optimal_batch_size', 'N/A')}")
print(f"Exclusive batch size: {results_exclusive.get('optimal_batch_size', 'N/A')}")
```

**Expected:**
- Exclusive mode should have equal or larger batch sizes
- No OOM errors in exclusive mode

### 5. Deterministic Aggregation Parity

**Goal:** Verify that exclusive mode produces the same embeddings as standard sequential mode.

**Steps:**
```python
import numpy as np

# Run both modes on same data
embedder_standard.load_chunks_from_processing(chunks_dir="/kaggle/input/test-chunks/")
results_standard = embedder_standard.generate_embeddings_kaggle_optimized()
embeddings_standard = embedder_standard.embeddings

embedder_exclusive.load_chunks_from_processing(chunks_dir="/kaggle/input/test-chunks/")
results_exclusive = embedder_exclusive.generate_embeddings_kaggle_optimized()
embeddings_exclusive = embedder_exclusive.embeddings

# Compare
similarity = np.dot(embeddings_standard.flatten(), embeddings_exclusive.flatten())
similarity /= (np.linalg.norm(embeddings_standard.flatten()) * np.linalg.norm(embeddings_exclusive.flatten()))

print(f"Cosine similarity: {similarity:.6f}")
print(f"Max absolute difference: {np.max(np.abs(embeddings_standard - embeddings_exclusive)):.10f}")
```

**Expected:**
- Cosine similarity should be >= 0.9999 (near-identical)
- Max absolute difference should be < 1e-5 (numerical precision)

### 6. CLI Flag Integration

**Goal:** Verify the `--exclusive-ensemble` flag works end-to-end.

**Steps:**
```bash
# In Kaggle notebook cell
!python scripts/embed_collections_v5.py \
    --chunks-root /kaggle/input/test-chunks \
    --output-root /kaggle/working/embeddings \
    --model jina-code-embeddings-1.5b \
    --enable-ensemble \
    --ensemble-mode sequential \
    --exclusive-ensemble \
    --collections test_collection
```

**Expected:**
- Script completes without errors
- Log shows "Exclusive ensemble mode detected"
- Output summary includes `"ensemble_mode": "exclusive"`
- Lease events appear in processing stats JSON

## Validation Checklist

- [ ] Models are staged to CPU at initialization
- [ ] GPU leases are acquired with correct device IDs
- [ ] VRAM is captured in acquire and release events
- [ ] VRAM drops significantly between model passes
- [ ] Batch sizes are equal or larger in exclusive mode
- [ ] No OOM errors occur during exclusive mode runs
- [ ] Embeddings match standard sequential mode (cosine similarity >= 0.9999)
- [ ] CLI flag `--exclusive-ensemble` activates the feature correctly
- [ ] Telemetry includes lease_events in processing stats export
- [ ] DataParallel wrappers are reconstructed correctly per pass

## Troubleshooting

### Issue: Models not staged to CPU
**Solution:** Check that `exclusive_mode=True` in ensemble_config and `enable_ensemble=True`.

### Issue: OOM during exclusive mode
**Solution:** Verify that models are actually being released between passes. Check lease events for proper release telemetry.

### Issue: Embeddings don't match
**Solution:** Ensure aggregation weights are consistent between modes. Check that matryoshka dimension is the same for both runs.

### Issue: No lease events in telemetry
**Solution:** Verify that `run_exclusive_ensemble` is being called (check logs for "Exclusive ensemble mode detected").

## Success Criteria

✅ All validation checklist items pass  
✅ No OOM errors occur in exclusive mode  
✅ Embeddings match standard mode within numerical precision  
✅ Telemetry correctly captures lease lifecycle  
✅ VRAM is freed between model passes  

## Notes

- Test with small collections first (< 1000 chunks) to iterate quickly
- Monitor Kaggle resource usage to avoid session limits
- Save intermediate outputs for comparison
- Capture full logs for debugging
