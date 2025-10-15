args = SparseEncoderTrainingArguments(
    router_mapping={
        "question": "query",
        "answer": "document",
    },
    learning_rate_mapping={
        r"SparseStaticEmbedding\.*": 1e-3,  # Higher LR for static embeddings
    }
)
```

**Sources:** [docs/sparse_encoder/training_overview.md:149-168]()

### Multi-Dataset Training

The system supports training on multiple datasets simultaneously with different batch sampling strategies:

```python
args = SparseEncoderTrainingArguments(
    multi_dataset_batch_sampler=BatchSamplers.PROPORTIONAL,
    batch_sampler=BatchSamplers.NO_DUPLICATES,
)
```

**Sources:** [docs/sparse_encoder/training_overview.md:419-425]()

### Memory Optimization

For large models, several memory optimization techniques are available:

- **Gradient Checkpointing**: `gradient_checkpointing=True`
- **Mixed Precision**: `fp16=True` or `bf16=True`
- **Chunked Processing**: Configure `chunk_size` in `SpladePooling`
- **Gradient Accumulation**: `gradient_accumulation_steps=N`

**Sources:** [docs/sparse_encoder/training_overview.md:400-425](), [sentence_transformers/sparse_encoder/models/SpladePooling.py:92-128]()