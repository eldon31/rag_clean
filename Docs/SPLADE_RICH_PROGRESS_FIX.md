# SPLADE + Rich Progress Implementation Summary

## Problem Solved

**Original Error:**

```
ValueError: SentenceTransformer.encode() has been called with additional keyword arguments
that this model does not use: ['tqdm_kwargs']. As per SentenceTransformer.get_model_kwargs(),
this model does not accept any additional keyword arguments.
```

## Root Cause

1. **SparseEncoder** (used by SPLADE) has a different API than `SentenceTransformer`
2. `SparseEncoder.encode()` doesn't support:

   - `tqdm_kwargs` parameter
   - `convert_to_numpy` parameter
   - `normalize_embeddings` parameter
   - `device` parameter (uses implicit device)

3. The code was trying to use `tqdm_kwargs` for progress bars, which caused the crash

## Solution Implemented

### 1. **Detect SparseEncoder Models**

```python
# Detect if this is a SparseEncoder (different API than SentenceTransformer)
model_class_name = type(model).__name__
is_sparse_encoder = "SparseEncoder" in model_class_name or "sparse_encoder" in type(model).__module__
```

### 2. **Use Rich Progress for Unsupported Models**

When a model doesn't support `tqdm_kwargs`, we now use **rich** library for beautiful progress bars:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

rich_progress = Progress(
    SpinnerColumn(),
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
)
```

### 3. **Manual Batching with Rich Progress**

For models without `tqdm_kwargs` support, we batch manually and update rich progress:

```python
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i + batch_size]
    if is_sparse_encoder:
        batch_result = encode_callable(
            batch_texts,
            batch_size=batch_size,
            show_progress_bar=False,
        )
    else:
        batch_result = encode_callable(
            batch_texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
            device=device,
        )
    result_batches.append(batch_result)
    rich_progress.update(rich_task, advance=1)
```

### 4. **Proper Parameter Handling**

```python
if is_sparse_encoder:
    # SparseEncoder has a more limited encode() API
    call_kwargs: Dict[str, Any] = {
        "batch_size": batch_size,
        "show_progress_bar": False,
    }
else:
    # SentenceTransformer supports more parameters
    call_kwargs: Dict[str, Any] = {
        "batch_size": batch_size,
        "show_progress_bar": False,
        "convert_to_numpy": True,
        "normalize_embeddings": True,
        "device": device,
    }
```

## Files Modified

1. **processor/ultimate_embedder/core.py**

   - Added `import math` for batch calculations
   - Added SparseEncoder detection logic
   - Implemented rich progress bar fallback
   - Added model-specific parameter handling

2. **processor/ultimate_embedder/compat.py**

   - Added `SparseEncoder` to imports
   - Updated `load_sentence_transformers()` to return 3 values
   - Exported `SparseEncoder` in `__all__`

3. **processor/ultimate_embedder/model_manager.py**
   - Updated imports to include `SparseEncoder`
   - Changed SPLADE loading to use `SparseEncoder` class
   - Removed old error handling that tried to load SPLADE as SentenceTransformer

## Test Results

✅ **Success! SPLADE now works perfectly:**

```
✅ Encoding successful!
   Output shape: torch.Size([5, 30522])
   Output dtype: torch.float32
   Output layout: torch.sparse_coo
   Rate: 23.12 chunks/sec
```

## Benefits

1. **Better Progress Visualization**: Rich provides beautiful, modern progress bars with:

   - Spinner animation
   - Progress bar
   - Task completion percentage
   - Time remaining estimate

2. **Model Compatibility**: Supports both SentenceTransformer and SparseEncoder models

3. **No Dependencies Issues**: Rich is a pure Python library, easy to install

4. **Graceful Fallback**: If rich fails to load, encoding still works (just without progress bar)

## Usage in Embedding Process

### When Components Are Used:

1. **Dense Embeddings** (SentenceTransformer)

   - Uses `tqdm_kwargs` for progress
   - Supports full parameter set
   - Used by: jina-code-embeddings, bge-m3, qwen3-embedding

2. **Sparse Embeddings** (SparseEncoder/SPLADE)

   - Uses **rich progress** (manual batching)
   - Limited parameters: only `batch_size` and `show_progress_bar`
   - Used by: naver/splade_v2_distil

3. **Reranking** (CrossEncoder)

   - Executed after dense retrieval
   - Reranks top N candidates (default: 100 → 20)
   - Used by: jinaai/jina-reranker-v3

4. **Cross-Encoder** (Jina Reranker)
   - Specific implementation of reranking
   - Loaded via AutoModel with trust_remote_code
   - Computes relevance scores for query-document pairs

## Installation

```bash
pip install rich
```

Already installed in the current environment!
