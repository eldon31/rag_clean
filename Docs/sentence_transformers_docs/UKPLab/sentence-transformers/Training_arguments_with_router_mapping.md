args = SentenceTransformerTrainingArguments(
    router_mapping={
        "question": "query",
        "positive": "document", 
        "negative": "document"
    }
)
```

### Data Collator Integration

The data collator uses `router_mapping` to pass task information to the `Router.tokenize()` method:

Sources: [sentence_transformers/data_collator.py:55-68](), [sentence_transformers/data_collator.py:92-94](), [sentence_transformers/models/Router.py:287-324]()

### Validation

The trainer validates that models using `Router` modules have proper `router_mapping` configured:

Sources: [sentence_transformers/trainer.py:206-212]()

## Memory-Efficient Training Features

The training system includes several memory optimization features:

| Feature | Purpose | Implementation |
|---------|---------|----------------|
| Gradient Caching | Enables larger effective batch sizes | `CachedMultipleNegativesRankingLoss` |
| Multi-Dataset Batching | Efficient sampling across datasets | `MultiDatasetBatchSampler` classes |
| Loss Component Tracking | Monitors complex loss breakdowns | `track_loss_components()` |
| Model Card Generation | Automatic documentation | `SentenceTransformerModelCardCallback` |

Sources: [sentence_transformers/trainer.py:443-462](), [sentence_transformers/trainer.py:327-345]()

## Next Steps

For detailed training guides specific to each model type:
- [SentenceTransformer Training](#3.1) - Dense embedding model training
- [SparseEncoder Training](#3.2) - Sparse embedding model training  
- [CrossEncoder Training](#3.3) - Cross-encoder reranking model training
- [Memory-Efficient Training](#3.7) - Advanced memory optimization techniques

# SentenceTransformer Training




This document covers the comprehensive training system for SentenceTransformer models, including the trainer architecture, data processing pipeline, loss functions, and evaluation mechanisms. It focuses on the `SentenceTransformerTrainer` class and its supporting infrastructure for training dense embedding models.

For information about training sparse encoder models, see [SparseEncoder Training](#3.2). For training cross-encoder models, see [CrossEncoder Training](#3.3). For detailed information about available loss functions, see [Loss Functions for SentenceTransformer](#3.4).

## Training System Architecture

The SentenceTransformer training system is built around the `SentenceTransformerTrainer` class, which extends the Hugging Face Transformers `Trainer` with specialized functionality for embedding model training.

```mermaid
graph TB
    subgraph "Training Infrastructure"
        ST["SentenceTransformerTrainer"]
        STA["SentenceTransformerTrainingArguments"]
        DC["SentenceTransformerDataCollator"]
        MC["SentenceTransformerModelCardCallback"]
    end
    
    subgraph "Model Components"
        Model["SentenceTransformer"]
        Router["Router Module"]
        Transformer["Transformer"]
        Pooling["Pooling"]
    end
    
    subgraph "Data Processing"
        Dataset["Dataset/DatasetDict"]
        Prompts["Prompts System"]
        RouterMapping["Router Mapping"]
        BatchSampler["Batch Samplers"]
    end
    
    subgraph "Loss & Evaluation"
        Loss["Loss Functions"]
        Evaluator["SentenceEvaluator"]
        SequentialEvaluator["SequentialEvaluator"]
    end
    
    ST --> Model
    ST --> STA
    ST --> DC
    ST --> MC
    ST --> Dataset
    ST --> Loss
    ST --> Evaluator
    
    STA --> Prompts
    STA --> RouterMapping
    STA --> BatchSampler
    
    DC --> Prompts
    DC --> RouterMapping
    
    Model --> Router
    Model --> Transformer
    Model --> Pooling
    
    Evaluator --> SequentialEvaluator
```

**Sources:** [sentence_transformers/trainer.py:59-127](), [sentence_transformers/training_args.py](), [sentence_transformers/data_collator.py:13-23]()

## Core Training Flow

The training process follows a structured pipeline from data input to model optimization:

```mermaid
graph TD
    Input["Input Dataset"] --> Validate["validate_column_names()"]
    Validate --> Preprocess["preprocess_dataset()"]
    Preprocess --> DC["SentenceTransformerDataCollator"]
    
    subgraph "Data Collation"
        DC --> ExtractLabels["Extract Labels"]
        DC --> ApplyPrompts["Apply Prompts"]
        DC --> Tokenize["tokenize_fn()"]
        DC --> RouterMap["Apply Router Mapping"]
    end
    
    Tokenize --> Features["Tokenized Features"]
    Features --> ComputeLoss["compute_loss()"]
    
    subgraph "Loss Computation"
        ComputeLoss --> CollectFeatures["collect_features()"]
        CollectFeatures --> LossForward["loss.forward()"]
        LossForward --> TrackComponents["track_loss_components()"]
    end
    
    TrackComponents --> Optimizer["Optimizer Step"]
    Optimizer --> Evaluate["evaluation_loop()"]
    
    subgraph "Evaluation"
        Evaluate --> EvalDataset["Eval Dataset Loss"]
        Evaluate --> Evaluator["evaluator()"]
        Evaluator --> Metrics["Evaluation Metrics"]
    end
    
    Metrics --> Log["log()"]
    Log --> SaveModel["Save Model/Checkpoint"]
```

**Sources:** [sentence_transformers/trainer.py:391-441](), [sentence_transformers/trainer.py:531-592](), [sentence_transformers/data_collator.py:35-119]()

## SentenceTransformerTrainer

The `SentenceTransformerTrainer` class is the central component that orchestrates the entire training process. It extends the Hugging Face `Trainer` with specialized functionality for embedding models.

### Key Features

- **Multi-dataset training support** through `DatasetDict`
- **Loss component tracking** for complex loss functions that return dictionaries
- **Router module integration** for asymmetric training architectures
- **Prompt system support** for instruction-based training
- **Automatic model card generation** during training

### Initialization and Configuration

The trainer accepts several key parameters:

```python
# Key trainer initialization parameters from trainer.py:129-148
model: SentenceTransformer | None = None
args: SentenceTransformerTrainingArguments | None = None
train_dataset: Dataset | DatasetDict | IterableDataset | dict[str, Dataset] | None = None
eval_dataset: Dataset | DatasetDict | IterableDataset | dict[str, Dataset] | None = None
loss: nn.Module | dict[str, nn.Module] | Callable | dict[str, Callable] | None = None
evaluator: SentenceEvaluator | list[SentenceEvaluator] | None = None
```

**Sources:** [sentence_transformers/trainer.py:129-148](), [sentence_transformers/trainer.py:291-310]()

### Loss Computation Pipeline

The trainer implements a sophisticated loss computation system that supports both single and multi-dataset training:

```mermaid
graph TD
    ComputeLoss["compute_loss()"] --> ExtractDataset["Extract dataset_name"]
    ExtractDataset --> CollectFeatures["collect_features()"]
    CollectFeatures --> SelectLoss["Select Loss Function"]
    
    subgraph "Feature Collection"
        CollectFeatures --> ParseColumns["Parse Input Columns"]
        ParseColumns --> ExtractLabels["Extract Labels"]
        ParseColumns --> GroupFeatures["Group by Prefix"]
    end
    
    subgraph "Loss Selection"
        SelectLoss --> SingleLoss["Single Loss"]
        SelectLoss --> DictLoss["Dictionary Loss"]
        DictLoss --> DatasetMapping["Map dataset_name to loss"]
    end
    
    GroupFeatures --> LossForward["loss.forward(features, labels)"]
    DatasetMapping --> LossForward
    SingleLoss --> LossForward
    
    LossForward --> CheckDict["Loss is dict?"]
    CheckDict -->|Yes| TrackComponents["track_loss_components()"]
    CheckDict -->|No| ReturnLoss["Return Loss"]
    TrackComponents --> SumComponents["Sum Loss Components"]
    SumComponents --> ReturnLoss
```

**Sources:** [sentence_transformers/trainer.py:391-441](), [sentence_transformers/trainer.py:496-529](), [sentence_transformers/trainer.py:443-462]()

## Training Arguments

The `SentenceTransformerTrainingArguments` class extends Hugging Face's `TrainingArguments` with additional parameters specific to embedding model training.

### Key SentenceTransformer-Specific Arguments

- **`batch_sampler`**: Controls how batches are constructed (e.g., `NO_DUPLICATES`, `GROUP_BY_LABEL`)
- **`multi_dataset_batch_sampler`**: Strategy for sampling from multiple datasets
- **`prompts`**: System for adding prompts to input text
- **`router_mapping`**: Maps dataset columns to Router module routes
- **`learning_rate_mapping`**: Allows different learning rates for different model components

**Sources:** [sentence_transformers/training_args.py](), [sentence_transformers/trainer.py:156-163]()

## Data Processing System

### SentenceTransformerDataCollator

The data collator handles the conversion from raw dataset samples to tokenized model inputs:

```mermaid
graph TD
    DataCollator["SentenceTransformerDataCollator"] --> ProcessFeatures["Process Features"]
    
    subgraph "Feature Processing"
        ProcessFeatures --> ExtractDatasetName["Extract dataset_name"]
        ProcessFeatures --> ExtractLabels["Extract Labels"]
        ProcessFeatures --> ProcessColumns["Process Text Columns"]
    end
    
    subgraph "Column Processing"
        ProcessColumns --> GetTask["Get Router Task"]
        ProcessColumns --> GetPrompt["Get Column Prompt"]
        ProcessColumns --> ApplyPrompt["Apply Prompt Prefix"]
        ProcessColumns --> TokenizeColumn["tokenize_fn(texts, task)"]
    end
    
    subgraph "Prompt System"
        GetPrompt --> SinglePrompt["Single String Prompt"]
        GetPrompt --> DatasetPrompts["Dataset-specific Prompts"]
        GetPrompt --> ColumnPrompts["Column-specific Prompts"]
    end
    
    TokenizeColumn --> PrefixKeys["Prefix with column_name"]
    PrefixKeys --> BatchOutput["Final Batch Dict"]
```

**Sources:** [sentence_transformers/data_collator.py:35-119](), [sentence_transformers/data_collator.py:90-118]()

### Prompt System

The training system supports a flexible prompting mechanism:

- **Single prompt**: Applied to all columns and datasets
- **Column-specific prompts**: Different prompts for different input columns
- **Dataset-specific prompts**: Different prompts for different datasets in multi-dataset training
- **Combined prompts**: Dataset and column-specific combinations

**Sources:** [sentence_transformers/data_collator.py:69-89](), [sentence_transformers/data_collator.py:96-101]()

## Router Module Integration

The Router module enables asymmetric training architectures where different input types (e.g., queries vs documents) are processed through different model paths.

### Router Training Requirements

When using a Router module, specific training arguments are required:

```mermaid
graph TD
    RouterModel["Model with Router"] --> CheckMapping["Check router_mapping"]
    CheckMapping -->|Missing| Error["ValueError: router_mapping required"]
    CheckMapping -->|Present| ValidateMapping["Validate Mapping"]
    
    subgraph "Router Mapping"
        ValidateMapping --> ColumnMapping["Column → Route Mapping"]
        ColumnMapping --> QueryRoute["'query' route"]
        ColumnMapping --> DocumentRoute["'document' route"]
    end
    
    subgraph "Data Collation"
        ColumnMapping --> DataCollator["SentenceTransformerDataCollator"]
        DataCollator --> ApplyRouting["Apply router_mapping"]
        ApplyRouting --> TokenizeWithTask["tokenize_fn(texts, task)"]
    end
    
    TokenizeWithTask --> RouterForward["router.forward(features, task)"]
```

**Sources:** [sentence_transformers/trainer.py:206-212](), [sentence_transformers/models/Router.py:217-245](), [sentence_transformers/data_collator.py:92-94]()

### Router Configuration Example

```python
# Router mapping example from training arguments
router_mapping = {
    "question": "query",
    "positive": "document", 
    "negative": "document"
}
```

**Sources:** [sentence_transformers/models/Router.py:45-54](), [tests/models/test_router.py:432-433]()

## Evaluation System

The training system supports evaluation through both dataset-based metrics and custom evaluators.

### Evaluation Pipeline

```mermaid
graph TD
    EvaluationLoop["evaluation_loop()"] --> EvalDataset["Eval Dataset Loss"]
    EvaluationLoop --> CheckEvaluator["evaluator exists?"]
    
    CheckEvaluator -->|No| ReturnMetrics["Return Dataset Metrics"]
    CheckEvaluator -->|Yes| RunEvaluator["evaluator(model, output_path, epoch, steps)"]
    
    subgraph "Evaluator Execution"
        RunEvaluator --> SingleEvaluator["Single Evaluator"]
        RunEvaluator --> SequentialEvaluator["SequentialEvaluator"]
        SequentialEvaluator --> MultipleEvaluators["Multiple Evaluators"]
    end
    
    SingleEvaluator --> EvaluatorMetrics["Evaluator Metrics"]
    MultipleEvaluators --> EvaluatorMetrics
    
    EvaluatorMetrics --> PrefixMetrics["Prefix with eval_"]
    PrefixMetrics --> MergeMetrics["Merge with Dataset Metrics"]
    MergeMetrics --> FinalMetrics["Final Evaluation Output"]
```

**Sources:** [sentence_transformers/trainer.py:545-592](), [sentence_transformers/trainer.py:312-315]()

## Batch Sampling Strategies

The training system provides several batch sampling strategies to optimize training performance:

### Available Batch Samplers

- **`DefaultBatchSampler`**: Standard random sampling
- **`NoDuplicatesBatchSampler`**: Ensures no duplicate samples in batch (useful for in-batch negatives)
- **`GroupByLabelBatchSampler`**: Groups samples by label
- **`ProportionalBatchSampler`**: Maintains dataset proportions in multi-dataset training
- **`RoundRobinBatchSampler`**: Alternates between datasets

**Sources:** [sentence_transformers/trainer.py:623-684](), [sentence_transformers/sampler.py]()

## Model Card Generation

The training system automatically generates model cards that document the training process:

```mermaid
graph TD
    TrainingStart["Training Initialization"] --> AddCallback["add_model_card_callback()"]
    AddCallback --> ModelCardCallback["SentenceTransformerModelCardCallback"]
    
    subgraph "Callback Lifecycle"
        ModelCardCallback --> OnInitEnd["on_init_end()"]
        ModelCardCallback --> OnTrainEnd["on_train_end()"]
        ModelCardCallback --> OnEvaluate["on_evaluate()"]
    end
    
    OnInitEnd --> TrackArgs["Track Training Arguments"]
    OnTrainEnd --> TrackMetrics["Track Training Metrics"]
    OnEvaluate --> TrackEvalMetrics["Track Evaluation Metrics"]
    
    TrackArgs --> GenerateCard["Generate Model Card"]
    TrackMetrics --> GenerateCard
    TrackEvalMetrics --> GenerateCard
    
    GenerateCard --> SaveCard["Save README.md"]
```

**Sources:** [sentence_transformers/trainer.py:327-345](), [sentence_transformers/model_card.py]()