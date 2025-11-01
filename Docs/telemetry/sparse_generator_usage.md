# Sparse Vector Generator Usage Guide

## Overview

The `SparseVectorGenerator` module provides live SPLADE-style sparse inference with GPU leasing support and automatic fallback handling. It integrates with the Ultimate Embedder's GPU management infrastructure and telemetry system.

## Quick Start

```python
from processor.ultimate_embedder.sparse_generator import (
    SparseVectorGenerator,
    ChunkRecord,
)

# Initialize generator with embedder instance
generator = SparseVectorGenerator(embedder, logger=custom_logger)

# Prepare chunks
chunks = [
    ChunkRecord(
        text="Sample document text",
        metadata={"sparse_features": {...}},
        chunk_id="chunk_001",
    ),
    # ... more chunks
]

# Generate sparse vectors (CPU)
result = generator.generate(
    chunks=chunks,
    model_name="qdrant-bm25",
    use_gpu=False,
)

# Generate with GPU acceleration
result = generator.generate(
    chunks=chunks,
    model_name="qdrant-bm25",
    use_gpu=True,
    device_ids=[0, 1],  # Optional: specify GPUs
)

# Access results
for i, vector in enumerate(result.vectors):
    if vector:
        print(f"Chunk {i}: {len(vector['indices'])} non-zero terms")
    else:
        print(f"Chunk {i}: No sparse vector available")

print(f"Fallback count: {result.fallback_count}/{len(chunks)}")
print(f"Latency: {result.latency_ms:.2f}ms")
print(f"Device: {result.device}")
```

## Features

### 1. Live Sparse Inference

The generator executes SPLADE-style sparse inference using SentenceTransformer models:

- **CPU Mode**: Processes chunks on CPU without GPU overhead
- **GPU Mode**: Uses GPU leasing for accelerated inference with automatic staging

### 2. Automatic Fallback Handling

When inference fails or models are unavailable, the generator automatically falls back to metadata-derived sparse vectors:

- Model not loaded → metadata fallback
- Encoding failure → metadata fallback  
- GPU lease exhaustion → CPU fallback → metadata fallback (if CPU fails)

### 3. GPU Leasing Integration

GPU mode uses the embedder's leasing infrastructure:

```python
# Generator automatically:
# 1. Acquires GPU lease
# 2. Hydrates model to GPU
# 3. Runs inference
# 4. Stages model back to CPU
# 5. Releases lease

result = generator.generate(
    chunks=chunks,
    model_name="qdrant-bm25",
    use_gpu=True,
    device_ids=[0],  # Lease GPU 0
)
```

Leasing ensures:
- Exclusive GPU access during inference
- VRAM cap enforcement (12 GB limit)
- Proper cache eviction between models
- Telemetry of GPU utilization

### 4. Telemetry Emission

The generator automatically records telemetry for observability:

**Span Attributes**:
- `model`: Sparse model name
- `device`: Execution device (cpu, cuda:0, etc.)
- `latency_ms`: Inference duration
- `fallback_count`: Number of chunks using fallback
- `chunk_count`: Total chunks processed
- `fallback_ratio`: Ratio of fallback to total chunks

**Metrics**:
- `sparse` stage metrics with latency, fallback count, and device info

Access telemetry:
```python
# Telemetry is automatically recorded in embedder.telemetry
span_data = embedder.telemetry.span_events.get("sparse_inference")
metrics_data = embedder.telemetry.metrics_reports.get("sparse")
```

## API Reference

### `SparseVectorGenerator`

#### `__init__(embedder, logger=None)`

Initialize the generator.

**Parameters**:
- `embedder` (UltimateKaggleEmbedderV4): Embedder instance providing models and config
- `logger` (logging.Logger, optional): Custom logger instance

#### `generate(chunks, model_name, use_gpu=False, device_ids=None)`

Generate sparse vectors for a batch of chunks.

**Parameters**:
- `chunks` (Sequence[ChunkRecord]): Chunks to process
- `model_name` (str): Sparse model name (must be loaded in embedder)
- `use_gpu` (bool): Enable GPU-accelerated inference
- `device_ids` (List[int], optional): GPU device IDs for leasing

**Returns**:
- `SparseInferenceResult`: Result containing vectors and metadata

**Raises**:
- May log warnings/errors but does not raise exceptions (uses fallback)

### `ChunkRecord`

Lightweight chunk container for inference.

**Attributes**:
- `text` (str): Chunk text content
- `metadata` (Dict[str, Any]): Chunk metadata including sparse_features
- `chunk_id` (str, optional): Unique chunk identifier

### `SparseInferenceResult`

Inference result with vectors and telemetry data.

**Attributes**:
- `vectors` (List[Optional[Dict[str, Any]]]): Sparse vectors (one per chunk)
- `fallback_count` (int): Number of chunks using metadata fallback
- `fallback_indices` (List[int]): Indices of chunks that used fallback
- `latency_ms` (float): Total inference duration in milliseconds
- `device` (str): Device used for inference
- `model_name` (str): Model name used
- `success` (bool): Whether inference completed without model-level errors
- `error_message` (str, optional): Error message if success=False

### Sparse Vector Structure

Each sparse vector is a dict with:
```python
{
    "indices": [123, 456, 789],      # Token indices (int)
    "values": [0.8, 0.6, 0.4],       # Normalized weights (float)
    "tokens": ["word1", "word2"],    # Token strings (for debugging)
    "stats": {
        "weight_norm": 1.0,          # Original norm before normalization
        "unique_terms": 3,            # Number of non-zero terms
        "total_terms": 512,           # Vocabulary size
        "weighting": "normalized"    # Weighting scheme
    }
}
```

## Configuration

### Sparse Model Registry

Sparse models must be registered in the embedder's config:

```python
SPARSE_MODELS = {
    "qdrant-bm25": {
        "name": "qdrant-bm25",
        "hf_model_id": "Qdrant/bm25",
        "type": "bm25",
        "recommended_batch_size": 64,
    },
    "qdrant-minilm-attention": {
        "name": "qdrant-minilm-attention",
        "hf_model_id": "Qdrant/all_miniLM_L6_v2_with_attentions",
        "type": "attention",
        "recommended_batch_size": 64,
    },
}
```

### Runtime Toggles

Sparse inference can be controlled via runtime config:

```python
# Enable/disable sparse mode
embedder.enable_sparse = True

# Configure sparse models to load
embedder.sparse_model_names = ["qdrant-bm25"]

# Check runtime status
if embedder._sparse_runtime_reason:
    print(f"Sparse disabled: {embedder._sparse_runtime_reason}")
```

## Best Practices

### 1. Batch Size Optimization

Process chunks in reasonable batch sizes:

```python
BATCH_SIZE = 64  # Recommended for sparse models

for i in range(0, len(all_chunks), BATCH_SIZE):
    batch = all_chunks[i:i + BATCH_SIZE]
    result = generator.generate(batch, model_name="qdrant-bm25")
```

### 2. GPU vs CPU Selection

Choose execution mode based on workload:

- **Use CPU** for:
  - Small batches (< 32 chunks)
  - When GPU is busy with dense models
  - When VRAM is constrained

- **Use GPU** for:
  - Large batches (> 100 chunks)  
  - When GPU capacity is available
  - When latency is critical

### 3. Fallback Monitoring

Monitor fallback ratio to detect issues:

```python
result = generator.generate(chunks, model_name="qdrant-bm25")

if result.fallback_count > len(chunks) * 0.1:  # > 10% fallback
    logger.warning(
        "High fallback rate: %d/%d (%.1f%%)",
        result.fallback_count,
        len(chunks),
        100 * result.fallback_count / len(chunks),
    )
```

### 4. Error Handling

The generator uses fallback instead of raising exceptions:

```python
result = generator.generate(chunks, model_name="qdrant-bm25")

if not result.success:
    logger.error("Sparse inference failed: %s", result.error_message)
    # Vectors still available via metadata fallback
    
# Always check vector availability
for i, vector in enumerate(result.vectors):
    if vector is None:
        logger.warning("No vector available for chunk %d", i)
```

### 5. Telemetry Review

Regularly review telemetry for performance insights:

```python
# After generation
span = embedder.telemetry.span_events.get("sparse_inference")
metrics = embedder.telemetry.metrics_reports.get("sparse")

print(f"Latency: {span['attributes']['latency_ms']:.2f}ms")
print(f"Device: {span['attributes']['device']}")
print(f"Fallback ratio: {span['attributes']['fallback_ratio']:.2%}")
```

## Integration Example

Full integration with batch processing:

```python
from processor.ultimate_embedder.sparse_generator import (
    SparseVectorGenerator,
    ChunkRecord,
)

def process_collection_with_sparse(embedder, chunks_data):
    """Process collection with sparse vector generation."""
    
    # Initialize generator
    generator = SparseVectorGenerator(embedder)
    
    # Prepare chunk records
    chunks = [
        ChunkRecord(
            text=chunk["text"],
            metadata=chunk.get("metadata", {}),
            chunk_id=chunk.get("id"),
        )
        for chunk in chunks_data
    ]
    
    # Generate sparse vectors with GPU if available
    use_gpu = embedder.device == "cuda" and embedder.device_count > 0
    
    result = generator.generate(
        chunks=chunks,
        model_name=embedder.sparse_model_names[0],
        use_gpu=use_gpu,
    )
    
    # Process results
    sparse_vectors = []
    for i, vector in enumerate(result.vectors):
        if vector:
            sparse_vectors.append({
                "chunk_id": chunks[i].chunk_id,
                "vector": vector,
                "fallback_used": i in result.fallback_indices,
            })
        else:
            # Handle missing vectors
            sparse_vectors.append({
                "chunk_id": chunks[i].chunk_id,
                "vector": None,
                "fallback_used": True,
            })
    
    # Log summary
    logger.info(
        "Sparse generation: %d vectors, %d fallbacks, %.2fms, device=%s",
        len(sparse_vectors),
        result.fallback_count,
        result.latency_ms,
        result.device,
    )
    
    return sparse_vectors, result

# Usage
sparse_vectors, result = process_collection_with_sparse(embedder, chunks_data)
```

## Troubleshooting

### Model Not Loading

**Symptom**: `error_message` says "Model {name} not loaded"

**Solution**:
1. Verify model is in `SPARSE_MODELS` registry
2. Check embedder initialized sparse models:
   ```python
   print(embedder.sparse_models.keys())
   ```
3. Review initialization logs for load failures

### High Fallback Rate

**Symptom**: `fallback_count` is high relative to chunk count

**Possible Causes**:
- Metadata quality issues (missing `sparse_features`)
- Encoding failures (check logs for exceptions)
- GPU memory exhaustion

**Actions**:
1. Review chunk metadata structure
2. Enable debug logging: `logger.setLevel(logging.DEBUG)`
3. Monitor GPU memory during inference

### GPU Lease Failures

**Symptom**: Always falls back to CPU despite `use_gpu=True`

**Possible Causes**:
- VRAM cap exceeded
- Lease pool exhausted
- Model hydration fails

**Actions**:
1. Check GPU memory availability
2. Review lease telemetry: `embedder.telemetry.gpu_lease_events`
3. Reduce batch size or disable GPU mode

### Low Performance

**Symptom**: High latency for sparse inference

**Optimization**:
1. Increase batch size (up to 64-128 for sparse models)
2. Enable GPU mode for large batches
3. Use smaller/faster sparse models (e.g., BM25 vs attention-based)
4. Profile with telemetry to identify bottlenecks

## Schema Integration

The generator's output aligns with the `SparseInferenceRun` schema:

```python
# Processing summary includes sparse_run section
sparse_stage_data = {
    "enabled": True,
    "models": ["qdrant-bm25"],
    "executed": True,
    "vectors": {
        "total": len(chunks),
        "available": len(chunks) - result.fallback_count,
        "coverage_ratio": 1.0 - (result.fallback_count / len(chunks)),
    },
    "devices": {"qdrant-bm25": result.device},
    "fallback_used": result.fallback_count > 0,
    "fallback_reason": result.error_message if not result.success else None,
}

# This data populates processing_summary.json["sparse_run"]
```

## See Also

- `processor/ultimate_embedder/sparse_pipeline.py` - Metadata fallback utilities
- `processor/ultimate_embedder/gpu_lease.py` - GPU leasing infrastructure
- `processor/ultimate_embedder/telemetry.py` - Telemetry system
- `docs/architecture/observability.md` - Observability architecture
- `docs/stories/2.2.story.md` - Batch runner integration (upcoming)
