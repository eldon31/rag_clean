trainer = CrossEncoderTrainer(
    model=model,
    train_dataset=train_dataset,
    loss=loss,
)
trainer.train()
```

### Configuration Parameters

Common parameters across learning-to-rank losses:

| Parameter | Type | Purpose |
|-----------|------|---------|
| `model` | `CrossEncoder` | Model to train |
| `activation_fn` | `nn.Module` | Applied to logits before loss computation |
| `mini_batch_size` | `int` | Controls memory usage and processing speed |

Sources: [examples/cross_encoder/training/ms_marco/training_ms_marco_listmle.py:93-94](), [examples/cross_encoder/training/ms_marco/training_ms_marco_plistmle.py:96]()

## Performance Recommendations

Based on the documentation and implementation comments:

1. **LambdaLoss with NDCGLoss2PPScheme**: Generally performs best for ranking tasks
2. **PListMLELoss**: Outperforms standard ListMLELoss due to position weighting
3. **Mini-batch size**: Critical for memory management when processing many documents per query
4. **Hard negative mining**: Use `mine_hard_negatives` with `output_format="labeled-list"` for better training data

The learning-to-rank losses are optimized for handling variable numbers of documents per query and support both binary and continuous relevance labels.

Sources: [sentence_transformers/cross_encoder/losses/LambdaLoss.py:175-176](), [sentence_transformers/cross_encoder/losses/PListMLELoss.py:105-111](), [examples/cross_encoder/training/ms_marco/training_ms_marco_cmnrl.py:62-71]()

# Memory-Efficient Training




This document covers memory-efficient training techniques in sentence-transformers that allow training with large batch sizes and complex loss functions while maintaining reasonable memory usage. These techniques are essential for achieving optimal performance on modern embedding models without requiring excessive GPU memory.

For general training information, see [SentenceTransformer Training](#3.1). For specific loss functions, see [Loss Functions for SentenceTransformer](#3.4).

## Cached Loss Functions

The primary memory-efficient training technique uses **GradCache**, which enables training with much larger effective batch sizes while maintaining constant memory usage. This is implemented through cached versions of standard loss functions.

### GradCache Architecture

```mermaid
flowchart TD
    Input["Input Batch (e.g., 1024 samples)"] --> CMNRL["CachedMultipleNegativesRankingLoss.forward()"]
    CMNRL --> Split["Split into mini_batch_size chunks"]
    Split --> Step1["Step 1: Forward Pass (torch.no_grad)"]
    Step1 --> EmbedIter["embed_minibatch_iter()"]
    EmbedIter --> EmbedMB["embed_minibatch()"]
    EmbedMB --> RandCtx["RandContext.copy_random_state"]
    RandCtx --> CacheEmb["reps.detach().requires_grad_()"]
    CacheEmb --> Step2["Step 2: Loss Calculation"]
    Step2 --> CalcLoss["calculate_loss_and_cache_gradients()"]
    CalcLoss --> GradCache["self.cache = [[r.grad for r in rs]]"]
    GradCache --> Step3["Step 3: Second Forward Pass (torch.enable_grad)"]
    Step3 --> Hook["loss.register_hook(_backward_hook)"]
    Hook --> Surrogate["torch.dot(reps_mb.flatten(), grad_mb.flatten())"]
    Surrogate --> Backprop["surrogate.backward()"]
```

**Sources:** [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:278-305](), [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:42-62](), [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:18-39]()

### Available Cached Loss Functions

| Standard Loss | Cached Version | Memory Benefit |
|---------------|----------------|----------------|
| `MultipleNegativesRankingLoss` | `CachedMultipleNegativesRankingLoss` | Constant memory for any batch size |
| `GISTEmbedLoss` | `CachedGISTEmbedLoss` | Large batch sizes with guide model |
| `MultipleNegativesSymmetricRankingLoss` | `CachedMultipleNegativesSymmetricRankingLoss` | Symmetric loss with caching |

**Sources:** [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:64](), [sentence_transformers/losses/CachedGISTEmbedLoss.py:65](), [sentence_transformers/losses/CachedMultipleNegativesSymmetricRankingLoss.py:41]()

### Mini-batch Processing Implementation

```mermaid
graph LR
    Batch["Full Batch"] --> Iterator["embed_minibatch_iter()"]
    Iterator --> MB1["Mini-batch 1<br/>embed_minibatch()"]
    Iterator --> MB2["Mini-batch 2<br/>embed_minibatch()"]
    Iterator --> MB3["Mini-batch N<br/>embed_minibatch()"]
    MB1 --> RS1["RandContext<br/>(Random State)"]
    MB2 --> RS2["RandContext<br/>(Random State)"]
    MB3 --> RS3["RandContext<br/>(Random State)"]
    RS1 --> Cache1["Cached Embeddings"]
    RS2 --> Cache2["Cached Embeddings"]
    RS3 --> Cache3["Cached Embeddings"]
```

The `mini_batch_size` parameter controls memory usage during training. Each mini-batch is processed through `embed_minibatch()` with `RandContext` ensuring reproducible embeddings across forward passes.

**Sources:** [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:175-223](), [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:18-39]()

## Matryoshka Training

Matryoshka training allows models to work efficiently at multiple embedding dimensions, reducing storage and computation costs for downstream applications.

### MatryoshkaLoss Architecture

```mermaid
flowchart TD
    Model["SentenceTransformer"] --> Forward["ForwardDecorator"]
    Loss["Base Loss Function"] --> Matryoshka["MatryoshkaLoss"]
    Dims["matryoshka_dims<br/>[768, 512, 256, 128, 64]"] --> Matryoshka
    Weights["matryoshka_weights<br/>[1, 1, 1, 1, 1]"] --> Matryoshka
    
    Forward --> Cache["Cache Full Embeddings"]
    Cache --> Shrink1["shrink(embeddings, 768)"]
    Cache --> Shrink2["shrink(embeddings, 512)"]
    Cache --> Shrink3["shrink(embeddings, 256)"]
    Cache --> Shrink4["shrink(embeddings, 128)"]
    Cache --> Shrink5["shrink(embeddings, 64)"]
    
    Shrink1 --> Loss1["Loss at 768d"]
    Shrink2 --> Loss2["Loss at 512d"]
    Shrink3 --> Loss3["Loss at 256d"]
    Shrink4 --> Loss4["Loss at 128d"]
    Shrink5 --> Loss5["Loss at 64d"]
    
    Loss1 --> Combine["Weighted Sum"]
    Loss2 --> Combine
    Loss3 --> Combine
    Loss4 --> Combine
    Loss5 --> Combine
```

**Sources:** [sentence_transformers/losses/MatryoshkaLoss.py:113-253](), [sentence_transformers/losses/MatryoshkaLoss.py:30-111]()

### Cached Matryoshka Integration

For cached losses, Matryoshka uses `CachedLossDecorator` instead of `ForwardDecorator`:

```mermaid
graph TD
    CachedLoss["CachedMultipleNegativesRankingLoss"] --> Decorator["CachedLossDecorator"]
    Embeddings["Pre-computed Embeddings"] --> Decorator
    Decorator --> Shrink["shrink() for each dimension"]
    Shrink --> Calculate["calculate_loss()"]
    Calculate --> Weighted["Apply matryoshka_weights"]
```

**Sources:** [sentence_transformers/losses/MatryoshkaLoss.py:67-111](), [sentence_transformers/losses/MatryoshkaLoss.py:195-204]()

## Router-based Asymmetric Models

The `Router` module enables memory-efficient asymmetric architectures where different encoders are used for queries and documents.

### Router Architecture

```mermaid
graph TD
    Input["features: dict[str, Tensor]"] --> RouterFwd["Router.forward()"]
    RouterFwd --> TaskCheck{"task = features.get('task', self.default_route)"}
    TaskCheck -->|"task='query'"| QuerySeq["self.sub_modules['query']"]
    TaskCheck -->|"task='document'"| DocSeq["self.sub_modules['document']"]
    TaskCheck -->|"None"| DefaultRoute["self.default_route"]
    
    QuerySeq --> QMod1["SparseStaticEmbedding"]
    QuerySeq --> QMod2["Additional Query Modules"]
    
    DocSeq --> DMod1["MLMTransformer"]
    DocSeq --> DMod2["SpladePooling"]
    
    Training["Training Phase"] --> RouterMap["router_mapping in TrainingArguments"]
    RouterMap --> DataCollator["SentenceTransformerDataCollator"]
    DataCollator --> TaskAssign["task = router_mapping.get(column_name)"]
    TaskAssign --> TokenizeFn["self.tokenize_fn(inputs, task=task)"]
```

This enables memory-efficient asymmetric training where lightweight query encoders (e.g., `SparseStaticEmbedding`) can be combined with powerful document encoders, reducing both training and inference costs.

**Sources:** [sentence_transformers/models/Router.py:217-245](), [sentence_transformers/models/Router.py:287-324](), [sentence_transformers/data_collator.py:90-118]()

## Batch Sampling and Multi-Dataset Training

The `SentenceTransformerTrainer` provides memory-efficient batch sampling strategies for large-scale training:

### Batch Sampler Architecture

```mermaid
graph TD
    TrainingArgs["SentenceTransformerTrainingArguments"] --> BatchSampler["args.batch_sampler"]
    BatchSampler --> DefaultBS["DefaultBatchSampler"]
    BatchSampler --> NoDupBS["NoDuplicatesBatchSampler"]
    BatchSampler --> GroupBS["GroupByLabelBatchSampler"]
    
    MultiDataset["Multi-Dataset Training"] --> MultiBS["args.multi_dataset_batch_sampler"]
    MultiBS --> PropBS["ProportionalBatchSampler"]
    MultiBS --> RoundRobinBS["RoundRobinBatchSampler"]
    
    Trainer["SentenceTransformerTrainer"] --> GetBatchSampler["get_batch_sampler()"]
    GetBatchSampler --> ConcatDS["ConcatDataset"]
    ConcatDS --> GetMultiBS["get_multi_dataset_batch_sampler()"]
```

**Sources:** [sentence_transformers/trainer.py:623-684](), [sentence_transformers/trainer.py:685-737](), [sentence_transformers/sampler.py:28-35]()

### Memory Usage Patterns

```mermaid
graph LR
    subgraph Traditional["Traditional Training"]
        TB["Batch Size: 32"] --> TM["Memory: Base"]
        TB2["Batch Size: 1024"] --> TM2["Memory: 32x Base<br/>(OOM)"]
    end
    
    subgraph Cached["Cached Training"]
        CB["mini_batch_size: 32"] --> CM["Memory: Base + Cache"]
        CB2["per_device_train_batch_size: 1024"] --> CM2["Memory: Base + Cache<br/>(Constant!)"]
    end
    
    subgraph MultiDataset["Multi-Dataset Training"]
        MDS["DatasetDict"] --> CDS["ConcatDataset"]
        CDS --> TrackDS["track dataset_name"]
        TrackDS --> LossSelect["loss[dataset_name]"]
    end
```

**Sources:** [sentence_transformers/losses/CachedMultipleNegativesRankingLoss.py:100-107](), [sentence_transformers/trainer.py:416-422]()

### Data Collator Memory Optimizations

The `SentenceTransformerDataCollator` includes several memory-efficient features:

```mermaid
graph TD
    DataCollator["SentenceTransformerDataCollator.__call__()"] --> RouterMap["self.router_mapping"]
    DataCollator --> Prompts["self.prompts"]
    DataCollator --> PromptCache["self._prompt_length_mapping"]
    
    RouterMap --> TaskAssign["task = router_mapping.get(column_name)"]
    Prompts --> PromptCheck["if isinstance(prompts, str)"]
    PromptCheck --> PromptPrefix["prompt + row[column_name]"]
    
    PromptCache --> GetPromptLen["_get_prompt_length()"]
    GetPromptLen --> TokenizeOnce["tokenize_fn([prompt], task=task)"]
    TokenizeOnce --> CacheLen["_prompt_length_mapping[(prompt, task)]"]
    
    TaskAssign --> TokenizeFn["tokenize_fn(inputs, task=task)"]
    TokenizeFn --> BatchKeys["batch[f'{column_name}_{key}'] = value"]
```

The prompt length caching in `_get_prompt_length()` prevents repeated tokenization of the same prompts, significantly reducing memory overhead during data loading.

**Sources:** [sentence_transformers/data_collator.py:35-119](), [sentence_transformers/data_collator.py:121-138]()

## Implementation Examples

### Using Cached Losses

```python
# Standard approach - memory scales with batch size
loss = MultipleNegativesRankingLoss(model)

# Cached approach - constant memory usage
loss = CachedMultipleNegativesRankingLoss(
    model, 
    mini_batch_size=32,  # Controls actual memory usage
    show_progress_bar=True
)
```

## Trainer Memory Optimizations

The `SentenceTransformerTrainer` includes several memory-efficient features beyond cached losses:

### Loss Component Tracking

```mermaid
graph TD
    ComputeLoss["SentenceTransformerTrainer.compute_loss()"] --> TrackLoss["track_loss_components()"]
    TrackLoss --> AccumLoss["self.accum_loss_components[training_type]"]
    AccumLoss --> LogLoss["self.log()"]
    LogLoss --> NestedGather["self._nested_gather()"]
    NestedGather --> AvgLoss["value.sum() / steps"]
    
    LossDict["loss: dict[str, torch.Tensor]"] --> Stack["torch.stack(list(loss.values())).sum()"]
    Stack --> SingleLoss["Final Loss Tensor"]
```

This prevents memory spikes when losses return dictionaries with multiple components by accumulating and averaging them efficiently.

**Sources:** [sentence_transformers/trainer.py:443-462](), [sentence_transformers/trainer.py:464-494](), [sentence_transformers/trainer.py:431-441]()

### Training Arguments for Memory Efficiency

```python
args = SentenceTransformerTrainingArguments(
    per_device_train_batch_size=1024,  # Large effective batch size
    gradient_accumulation_steps=1,     # No additional accumulation needed
    dataloader_drop_last=True,         # Avoid uneven batches
    batch_sampler=BatchSamplers.NO_DUPLICATES,  # Memory-efficient sampling
    multi_dataset_batch_sampler=MultiDatasetBatchSamplers.PROPORTIONAL,
)
```

**Sources:** [sentence_transformers/trainer.py:623-684](), [sentence_transformers/training_args.py:37-39]()

### Router Training Configuration

```python