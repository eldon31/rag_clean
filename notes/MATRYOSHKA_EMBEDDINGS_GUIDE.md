# Matryoshka Embeddings Guide

## What Are Matryoshka Embeddings?

Matryoshka Representation Learning (MRL) is a technique where models are trained to produce embeddings that remain meaningful when truncated to smaller dimensions. This allows you to use the same model at different dimensionalities depending on your needs (speed vs. accuracy trade-off).

**Key Concept**: A 1536D Matryoshka embedding can be truncated to 1024D, 512D, 256D, etc., and still maintain good semantic quality - **without retraining**.

## Supported Models in Our Registry

### ✅ CONFIRMED Matryoshka Support

These models are **explicitly trained** with Matryoshka Representation Learning:

1. **jina-embeddings-v4** (2048D → 1024D/512D/256D)
   - HF: `jinaai/jina-embeddings-v4`
   - Matryoshka dimensions: 256, 512, 768, 1024, 2048
   - Source: [Jina AI documentation](https://jina.ai/news/jina-embeddings-v4/)

2. **jina-code-embeddings-1.5b** (1536D → 1024D/512D/256D)
   - HF: `jinaai/jina-code-embeddings-1.5b`
   - Matryoshka dimensions: 256, 512, 1024, 1536
   - Source: Jina AI MRL training

### ⚠️ UNKNOWN / UNCONFIRMED

These models **may or may not** support Matryoshka truncation. Use with caution:

3. **nomic-coderank** (768D)
   - HF: `nomic-ai/CodeRankEmbed`
   - Status: **Unknown** - no official Matryoshka documentation
   - Recommendation: Use full 768D

4. **bge-m3** (1024D)
   - HF: `BAAI/bge-m3`
   - Status: **Unknown** - not mentioned in BAAI documentation
   - Recommendation: Use full 1024D

5. **gte-qwen2-1.5b** (1536D)
   - HF: `Alibaba-NLP/gte-Qwen2-1.5B-instruct`
   - Status: **Unknown**
   - Recommendation: Use full 1536D

6. **e5-mistral-7b** (4096D)
   - HF: `intfloat/e5-mistral-7b-instruct`
   - Status: **Unknown**
   - Recommendation: Use full 4096D

### ❌ NO Matryoshka Support

These models are **NOT trained** with Matryoshka and should use full dimensions:

7. **all-miniLM-l6** (384D)
   - HF: `sentence-transformers/all-MiniLM-L6-v2`
   - Classic BERT-based model - no Matryoshka training

8. **gte-large** (1024D)
   - HF: `thenlper/gte-large`
   - Classic model - no Matryoshka training

9. **bge-small** (384D)
   - HF: `BAAI/bge-small-en-v1.5`
   - Classic model - no Matryoshka training

10. **qdrant-minilm-onnx** (384D)
    - HF: `Qdrant/all-MiniLM-L6-v2-onnx`
    - ONNX-optimized, no Matryoshka training

## Implementation in Our Code

### Current Behavior (V5)

The embedder **now correctly applies Matryoshka truncation** when configured:

```python
# In kaggle_ultimate_embedder_v4.py, line ~1838
if self.matryoshka_dim and batch_embeddings.shape[1] > self.matryoshka_dim:
    batch_embeddings = batch_embeddings[:, :self.matryoshka_dim]
```

### Validation

The embedder validates dimensions at initialization (lines 536-550):

```python
if matryoshka_dim:
    supported_dims = {128, 256, 512, 1024, 1536, 2048}
    if matryoshka_dim not in supported_dims:
        logger.warning(f"Matryoshka dimension {matryoshka_dim} not in standard set")
    if matryoshka_dim > self.model_config.vector_dim:
        raise ValueError("Matryoshka dimension cannot exceed model dimension")
```

### Usage Examples

**Safe Usage (Confirmed Matryoshka Models)**:
```python
# jina-embeddings-v4: 2048D → 1024D
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-embeddings-v4",
    matryoshka_dim=1024  # ✅ Safe truncation
)

# jina-code-embeddings-1.5b: 1536D → 512D
embedder = UltimateKaggleEmbedderV4(
    model_name="jina-code-embeddings-1.5b",
    matryoshka_dim=512  # ✅ Safe truncation
)
```

**Risky Usage (Unconfirmed Models)**:
```python
# nomic-coderank: Unknown Matryoshka support
embedder = UltimateKaggleEmbedderV4(
    model_name="nomic-coderank",
    matryoshka_dim=512  # ⚠️ May degrade quality - NOT CONFIRMED
)
```

**Safe Default (No Truncation)**:
```python
# Any model: Use full dimension
embedder = UltimateKaggleEmbedderV4(
    model_name="nomic-coderank",
    matryoshka_dim=None  # ✅ Full 768D - always safe
)
```

## Recommendations

### When to Use Matryoshka Truncation

1. **Storage Constraints**: Reduce vector database size by 25-50%
2. **Speed Optimization**: Faster similarity search with smaller vectors
3. **Memory Limits**: Lower RAM usage during indexing

### When NOT to Use Truncation

1. **Maximum Quality Needed**: Critical applications requiring best accuracy
2. **Unconfirmed Models**: Models without official Matryoshka documentation
3. **Small Collections**: < 100K vectors where storage isn't an issue

### Best Practices

1. **Always test quality**: Compare search results before/after truncation
2. **Use standard dimensions**: 256D, 512D, 1024D (powers of 2)
3. **Document your choice**: Note why you chose a specific dimension
4. **Prefer confirmed models**: Use Jina models if Matryoshka is critical

## Script Defaults (V5)

**Current default**: `matryoshka_dim=None` (use full dimension)

This is the **safest default** because:
- Works for ALL models (confirmed or not)
- No risk of quality degradation
- Explicit opt-in required for truncation

**To enable truncation**:
```bash
# Kaggle Cell 6
python scripts/embed_collections_v5.py /kaggle/working/rag_clean/Chunked /kaggle/working/rag_clean/Embeddings jina-code-embeddings-1.5b 1024
```

## Performance Impact

### jina-embeddings-v4 (Confirmed Matryoshka)

| Dimension | Storage | Speed | Quality Loss |
|-----------|---------|-------|--------------|
| 2048D (full) | 100% | 1.0x | 0% |
| 1024D | 50% | 1.8x | ~2-3% |
| 512D | 25% | 3.2x | ~5-8% |
| 256D | 12.5% | 5.5x | ~12-15% |

*Quality loss estimates based on Jina AI benchmarks*

### Unknown Models (e.g., nomic-coderank)

**Quality loss is UNPREDICTABLE** - could be anywhere from 5% to 50%+ depending on whether the model was trained with Matryoshka techniques.

## Verification Process

To verify if a model supports Matryoshka:

1. **Check model card** on Hugging Face
2. **Look for keywords**: "Matryoshka", "MRL", "variable dimension"
3. **Check training details**: Was it trained with dimension truncation?
4. **Test empirically**: Compare full vs. truncated performance

## Future Work

1. **Add model-specific validation**: Warn when truncating non-Matryoshka models
2. **Quality benchmarks**: Measure actual quality loss for each model
3. **Auto-detection**: Check model config for Matryoshka metadata
4. **Recommended dimensions**: Per-model optimal truncation points

## References

- [Matryoshka Representation Learning Paper](https://arxiv.org/abs/2205.13147)
- [Jina AI Embeddings V4](https://jina.ai/news/jina-embeddings-v4/)
- [Hugging Face Matryoshka Guide](https://huggingface.co/blog/matryoshka)

---

**Last Updated**: 2025-01-20  
**Status**: Implementation complete, model verification in progress