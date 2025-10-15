similarity_fn_names = ["cosine", "dot", "euclidean", "manhattan"]
```

This generates metrics for each function, with optional `max_*` aggregated metrics for overall performance assessment.

### Prediction Output

The `InformationRetrievalEvaluator` supports `write_predictions=True` to output retrieval results in JSONL format, enabling downstream analysis and fusion with other retrieval systems.

### Embedding Optimization

Several evaluators support advanced embedding configurations:
- **Precision Control**: `precision` parameter for quantized embeddings (`"int8"`, `"binary"`, etc.)
- **Dimension Truncation**: `truncate_dim` for reduced-dimension evaluation
- **Normalization**: Automatic normalization for certain precision modes

Sources: [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:171-176](), [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:374-396]()

# SentenceTransformer Evaluators




This document covers the evaluation system for `SentenceTransformer` models, including the base evaluator architecture and all available evaluator implementations. These evaluators are used during training to assess model performance on various downstream tasks, enabling automatic model selection and performance monitoring.

For evaluation of sparse encoder models, see [SparseEncoder Evaluators](#4.2). For cross-encoder evaluation, see [CrossEncoder Evaluators](#4.3). For comprehensive benchmark evaluation, see [NanoBEIR Evaluation](#4.4).

## Evaluator Architecture

All SentenceTransformer evaluators inherit from the `SentenceEvaluator` base class, which provides a standardized interface for evaluation during training and inference.

### Base Evaluator Structure

```mermaid
classDiagram
    class SentenceEvaluator {
        +bool greater_is_better
        +str primary_metric
        +__call__(model, output_path, epoch, steps)
        +prefix_name_to_metrics(metrics, name)
        +store_metrics_in_model_card_data(model, metrics, epoch, steps)
        +embed_inputs(model, sentences)
        +get_config_dict()
        +description : str
    }
    
    class InformationRetrievalEvaluator {
        +dict queries
        +dict corpus
        +dict relevant_docs
        +compute_metrices(model)
        +compute_metrics(queries_result_list)
    }
    
    class EmbeddingSimilarityEvaluator {
        +list sentences1
        +list sentences2
        +list scores
        +compute_metrices(model)
    }
    
    class BinaryClassificationEvaluator {
        +list sentences1
        +list sentences2
        +list labels
        +find_best_acc_and_threshold()
        +find_best_f1_and_threshold()
    }
    
    class RerankingEvaluator {
        +list samples
        +int at_k
        +compute_metrices_batched(model)
        +compute_metrices_individual(model)
    }
    
    class TripletEvaluator {
        +list anchors
        +list positives
        +list negatives
        +dict margin
    }
    
    class ParaphraseMiningEvaluator {
        +dict sentences_map
        +dict duplicates
        +add_transitive_closure()
    }
    
    SentenceEvaluator <|-- InformationRetrievalEvaluator
    SentenceEvaluator <|-- EmbeddingSimilarityEvaluator
    SentenceEvaluator <|-- BinaryClassificationEvaluator
    SentenceEvaluator <|-- RerankingEvaluator
    SentenceEvaluator <|-- TripletEvaluator
    SentenceEvaluator <|-- ParaphraseMiningEvaluator
```

**Sources:** [sentence_transformers/evaluation/SentenceEvaluator.py:13-121]()

### Key Base Class Features

The `SentenceEvaluator` base class provides several critical features:

| Feature | Purpose | Key Methods |
|---------|---------|-------------|
| **Primary Metric** | Identifies the main metric for model selection | `primary_metric` attribute |
| **Metric Direction** | Indicates if higher scores are better | `greater_is_better` attribute |
| **Metric Prefixing** | Adds evaluator names to metric keys | `prefix_name_to_metrics()` |
| **Model Card Integration** | Stores evaluation results in model metadata | `store_metrics_in_model_card_data()` |
| **Embedding Interface** | Standardized text encoding | `embed_inputs()` |

**Sources:** [sentence_transformers/evaluation/SentenceEvaluator.py:26-121]()

## Core Evaluator Types

### Information Retrieval Evaluator

The `InformationRetrievalEvaluator` is designed for search and retrieval tasks, computing standard IR metrics across large corpora.

```mermaid
graph TB
    subgraph "InformationRetrievalEvaluator"
        Queries["queries: Dict[str, str]"]
        Corpus["corpus: Dict[str, str]"]
        RelevantDocs["relevant_docs: Dict[str, Set[str]]"]
        
        subgraph "Metrics Computed"
            MRR["MRR@k (Mean Reciprocal Rank)"]
            NDCG["NDCG@k (Normalized DCG)"]
            MAP["MAP@k (Mean Average Precision)"]
            Accuracy["Accuracy@k"]
            PrecisionRecall["Precision@k / Recall@k"]
        end
        
        subgraph "Configuration"
            ChunkSize["corpus_chunk_size: 50000"]
            BatchSize["batch_size: 32"]
            ScoreFunctions["score_functions: Dict"]
            Prompts["query_prompt / corpus_prompt"]
        end
    end
    
    Queries --> MRR
    Corpus --> MRR
    RelevantDocs --> MRR
    ChunkSize --> MRR
```

Key features:
- **Chunked Processing**: Handles large corpora via `corpus_chunk_size` parameter [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:130]()
- **Multiple Score Functions**: Supports different similarity functions via `score_functions` [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:141]()
- **Asymmetric Encoding**: Different prompts for queries vs documents [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:143-146]()
- **Prediction Export**: Optional JSONL output for downstream analysis [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:147]()

**Sources:** [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:23-568]()

### Embedding Similarity Evaluator

The `EmbeddingSimilarityEvaluator` measures correlation between predicted and ground-truth similarity scores.

```mermaid
graph LR
    subgraph "Input Data"
        S1["sentences1: List[str]"]
        S2["sentences2: List[str]"]
        GoldScores["scores: List[float]"]
    end
    
    subgraph "Similarity Functions"
        Cosine["cosine: pairwise_cos_sim"]
        Dot["dot: pairwise_dot_score"]
        Euclidean["euclidean: pairwise_euclidean_sim"]
        Manhattan["manhattan: pairwise_manhattan_sim"]
    end
    
    subgraph "Correlation Metrics"
        Pearson["Pearson Correlation"]
        Spearman["Spearman Correlation"]
    end
    
    S1 --> Cosine
    S2 --> Cosine
    Cosine --> Pearson
    Cosine --> Spearman
    GoldScores --> Pearson
    GoldScores --> Spearman
```

Key features:
- **Multiple Similarity Functions**: Supports cosine, dot product, Euclidean, and Manhattan distance [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:184-189]()
- **Precision Support**: Handles quantized embeddings (int8, uint8, binary, ubinary) [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:93]()
- **Automatic Deduplication**: Avoids re-encoding identical sentences [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:225-237]()

**Sources:** [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:27-272]()

### Binary Classification Evaluator

The `BinaryClassificationEvaluator` treats similarity as a binary classification problem.

```mermaid
graph TD
    subgraph "Input Processing"
        Pairs["sentence pairs + binary labels"]
        Embeddings["encode sentence pairs"]
        Similarities["compute pairwise similarities"]
    end
    
    subgraph "Threshold Optimization"
        AccThreshold["find_best_acc_and_threshold()"]
        F1Threshold["find_best_f1_and_threshold()"]
    end
    
    subgraph "Metrics Output"
        Accuracy["Accuracy + optimal threshold"]
        F1Score["F1, Precision, Recall + threshold"]
        AP["Average Precision"]
        MCC["Matthews Correlation Coefficient"]
    end
    
    Pairs --> Embeddings
    Embeddings --> Similarities
    Similarities --> AccThreshold
    Similarities --> F1Threshold
    AccThreshold --> Accuracy
    F1Threshold --> F1Score
    Similarities --> AP
    F1Threshold --> MCC
```

**Sources:** [sentence_transformers/evaluation/BinaryClassificationEvaluator.py:27-379]()

### Reranking Evaluator

The `RerankingEvaluator` evaluates models on reranking tasks with query-document relevance.

```mermaid
graph TB
    subgraph "Sample Structure"
        Query["query: str"]
        Positive["positive: List[str]"]
        Negative["negative: List[str]"]
    end
    
    subgraph "Processing Modes"
        Batched["compute_metrices_batched()"]
        Individual["compute_metrices_individual()"]
    end
    
    subgraph "Ranking Metrics"
        MAP["Mean Average Precision"]
        MRR["MRR@k"]
        NDCG["NDCG@k"]
    end
    
    Query --> Batched
    Positive --> Batched
    Negative --> Batched
    
    Batched --> MAP
    Batched --> MRR
    Batched --> NDCG
```

Key features:
- **Flexible Processing**: Choice between batched and individual encoding [sentence_transformers/evaluation/RerankingEvaluator.py:98]()
- **Memory Optimization**: Batched mode for speed, individual mode for memory efficiency [sentence_transformers/evaluation/RerankingEvaluator.py:210-214]()

**Sources:** [sentence_transformers/evaluation/RerankingEvaluator.py:25-372]()

## Specialized Evaluators

### Triplet Evaluator

Evaluates triplet ranking performance where positive examples should be closer than negative examples.

```mermaid
graph LR
    subgraph "Triplet Components"
        Anchors["anchors: List[str]"]
        Positives["positives: List[str]"]
        Negatives["negatives: List[str]"]
    end
    
    subgraph "Margin Configuration"
        MarginDict["margin: Dict[str, float]"]
        DefaultMargin["default: 0.0 for all metrics"]
    end
    
    subgraph "Evaluation Logic"
        Condition["similarity(anchor, positive) > similarity(anchor, negative) + margin"]
        Accuracy["accuracy per similarity function"]
    end
    
    Anchors --> Condition
    Positives --> Condition
    Negatives --> Condition
    MarginDict --> Condition
    Condition --> Accuracy
```

**Sources:** [sentence_transformers/evaluation/TripletEvaluator.py:26-271]()

### Paraphrase Mining Evaluator

Evaluates paraphrase detection performance by mining similar sentences from a corpus.

Key features:
- **Transitive Closure**: Optional transitive relationship enforcement [sentence_transformers/evaluation/ParaphraseMiningEvaluator.py:97]()
- **Scalable Mining**: Uses `paraphrase_mining` utility for efficient processing [sentence_transformers/evaluation/ParaphraseMiningEvaluator.py:172-182]()
- **F1 Optimization**: Finds optimal similarity threshold for paraphrase detection [sentence_transformers/evaluation/ParaphraseMiningEvaluator.py:187-212]()

**Sources:** [sentence_transformers/evaluation/ParaphraseMiningEvaluator.py:18-279]()

### Translation Evaluator

Measures cross-lingual alignment by checking if translations have highest mutual similarity.

**Sources:** [sentence_transformers/evaluation/TranslationEvaluator.py:22-192]()

### Knowledge Distillation Evaluators

Two evaluators support knowledge distillation scenarios:

- **MSEEvaluator**: Computes MSE between teacher and student embeddings [sentence_transformers/evaluation/MSEEvaluator.py:18-158]()
- **MSEEvaluatorFromDataFrame**: Structured multilingual distillation evaluation [sentence_transformers/evaluation/MSEEvaluatorFromDataFrame.py:20-139]()

## Common Usage Patterns

### Evaluation During Training

All evaluators follow the same calling convention for integration with training loops:

```python
# Standard evaluator call signature
results = evaluator(
    model=sentence_transformer_model,
    output_path="./evaluation_results",
    epoch=current_epoch,
    steps=current_step
)
```

### Metric Organization

```mermaid
graph TD
    subgraph "Metric Processing Pipeline"
        RawMetrics["evaluator.compute_metrices()"]
        PrefixedMetrics["evaluator.prefix_name_to_metrics()"]
        ModelCard["evaluator.store_metrics_in_model_card_data()"]
        CSVOutput["CSV file output (optional)"]
    end
    
    subgraph "Metric Structure"
        PrimaryMetric["evaluator.primary_metric"]
        AllMetrics["Dict[str, float] return value"]
        GreaterIsBetter["evaluator.greater_is_better"]
    end
    
    RawMetrics --> PrefixedMetrics
    PrefixedMetrics --> ModelCard
    PrefixedMetrics --> CSVOutput
    PrefixedMetrics --> AllMetrics
    PrimaryMetric --> AllMetrics
```

**Sources:** [sentence_transformers/evaluation/SentenceEvaluator.py:57-75]()

### Configuration Management

Each evaluator provides configuration introspection via `get_config_dict()`:

| Evaluator | Key Configuration Parameters |
|-----------|------------------------------|
| `InformationRetrievalEvaluator` | `truncate_dim`, `query_prompt`, `corpus_prompt` |
| `EmbeddingSimilarityEvaluator` | `truncate_dim`, `precision` |
| `BinaryClassificationEvaluator` | `truncate_dim` |
| `RerankingEvaluator` | `at_k`, `truncate_dim` |
| `TripletEvaluator` | `margin`, `truncate_dim` |

**Sources:** Multiple evaluator `get_config_dict()` methods across evaluation files

## Integration with Training

Evaluators integrate seamlessly with the SentenceTransformer training system:

```mermaid
sequenceDiagram
    participant Trainer as "SentenceTransformerTrainer"
    participant Evaluator as "SentenceEvaluator"
    participant Model as "SentenceTransformer"
    participant ModelCard as "ModelCardData"
    
    Trainer->>Evaluator: __call__(model, output_path, epoch, steps)
    Evaluator->>Model: encode(sentences, **kwargs)
    Model-->>Evaluator: embeddings
    Evaluator->>Evaluator: compute_metrices()
    Evaluator->>Evaluator: prefix_name_to_metrics()
    Evaluator->>ModelCard: store_metrics_in_model_card_data()
    Evaluator-->>Trainer: metrics dict with primary_metric
```

The training system uses `evaluator.primary_metric` and `evaluator.greater_is_better` for:
- **Model Selection**: Choosing best checkpoint when `load_best_model_at_end=True`
- **Early Stopping**: Monitoring convergence based on evaluation metrics
- **Logging**: Tracking primary metrics across training runs

**Sources:** [sentence_transformers/evaluation/SentenceEvaluator.py:26-75]()