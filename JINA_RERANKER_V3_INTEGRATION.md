# Jina Reranker V3 - Default Integration

## Summary

Successfully configured `jina-reranker-v3` as the default reranker model across the entire codebase.

## Changes Made

### 1. Priority Order Update

**File:** `processor/ultimate_embedder/config.py`

Changed `RERANKING_MODEL_PRIORITY` to make `jina-reranker-v3` the first choice:

```python
RERANKING_MODEL_PRIORITY: List[str] = [
    "jina-reranker-v3",        # ← NOW FIRST (was third)
    "coderank-bi-encoder",     # ← Fallback if jina fails
    "bge-reranker-v2-m3",      # ← Second fallback
]
```

### 2. Model Specification

**File:** `processor/ultimate_embedder/config.py`

Jina reranker v3 configuration (already correct, enhanced with dtype="auto"):

```python
"jina-reranker-v3": RerankingModelSpec(
    hf_model_id="jinaai/jina-reranker-v3",
    trust_remote_code=True,
    model_kwargs={"dtype": "auto"},  # ← Added for optimal dtype selection
    loader="jina_reranker",
    description=(
        "Jina reranker v3 with pretrained scoring head; requires trust_remote_code "
        "to restore custom modules."
    ),
)
```

### 3. CLI Default

**File:** `scripts/embed_collections_v7.py`

Changed CLI default from CodeRank to Jina:

```python
DEFAULT_RERANK_MODEL = "jinaai/jina-reranker-v3"  # ← Changed from "nomic-ai/CodeRankLLM"
```

### 4. Loading Implementation

**File:** `processor/ultimate_embedder/rerank_pipeline.py`

The loader already implements the exact pattern specified:

```python
def create_reranker_from_spec(...):
    if getattr(spec, "loader", "cross_encoder") == "jina_reranker":
        model_kwargs = dict(getattr(spec, "model_kwargs", {}))

        if spec.trust_remote_code:
            model_kwargs.setdefault("trust_remote_code", True)

        base_model = AutoModel.from_pretrained(
            spec.hf_model_id,      # 'jinaai/jina-reranker-v3'
            **model_kwargs,        # dtype="auto", trust_remote_code=True
        )
        base_model.eval()

        if device and device != "cpu":
            base_model.to(device)

        return _JinaRerankerAdapter(base_model)
```

## Loading Pattern

The model will be loaded exactly as specified:

```python
from transformers import AutoModel

model = AutoModel.from_pretrained(
    'jinaai/jina-reranker-v3',
    dtype="auto",
    trust_remote_code=True,
)
model.eval()
```

## Verification

Run the verification script to confirm configuration:

```bash
python scripts/verify_jina_reranker_config.py
```

Expected output:

```
✓ jina-reranker-v3 is first priority
✓ Default is jina-reranker-v3
✓ All spec parameters correct
✓ Loading pattern matches expected
✓ ALL CHECKS PASSED
```

## Fallback Chain

If jina-reranker-v3 fails to load, the system will automatically try:

1. `coderank-bi-encoder` (nomic-ai/CodeRankEmbed)
2. `bge-reranker-v2-m3` (BAAI/bge-reranker-v2-m3)

## Usage

### Default behavior (uses jina-reranker-v3)

```bash
python scripts/embed_collections_v7.py \
    --chunked-dir ./Chunked/Docling \
    --output-dir ./output
```

### Explicit specification

```bash
python scripts/embed_collections_v7.py \
    --chunked-dir ./Chunked/Docling \
    --output-dir ./output \
    --rerank-model jinaai/jina-reranker-v3
```

### Disable reranking

```bash
python scripts/embed_collections_v7.py \
    --chunked-dir ./Chunked/Docling \
    --output-dir ./output \
    --disable-rerank
```

## Integration Points

### Core Embedder

The `UltimateKaggleEmbedderV4` class will:

1. Check `RERANKING_MODEL_PRIORITY` list
2. Try to load `jina-reranker-v3` first
3. Fall back to other models if loading fails
4. Log the selected model and any fallback reasons

### CLI

The CLI script will:

1. Default `--rerank-model` to `jinaai/jina-reranker-v3`
2. Pass the model name to the embedder configuration
3. Display model readiness status at startup

### Processing Summary

The `processing_summary.json` will include:

- Selected reranker model name
- Fallback information (if applicable)
- Reranking execution metrics

## Testing

Relevant test files:

- `tests/test_reranker_selection.py` - Reranker fallback chain
- `tests/test_cross_encoder_executor.py` - Reranker execution
- `tests/test_embed_collections_cli.py` - CLI integration
- `tests/test_processing_summary.py` - Summary schema

## Notes

- **Trust Remote Code**: Required for jina-reranker-v3 to load custom modules
- **Auto dtype**: Automatically selects optimal precision based on hardware
- **Device Placement**: Model is moved to CUDA device after loading if available
- **Eval Mode**: Model is set to evaluation mode (no gradient computation)
