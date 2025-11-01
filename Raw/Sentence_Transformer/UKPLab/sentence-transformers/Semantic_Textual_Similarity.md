This page covers the evaluation and measurement of semantic textual similarity using sentence-transformers. It focuses on the various evaluators, similarity functions, and metrics available for assessing how semantically similar two pieces of text are to each other.

For information about using similarity for information retrieval tasks, see [Information Retrieval](#6.1). For details on training models with similarity-based objectives, see [Loss Functions for SentenceTransformer](#3.4).

## Core Similarity Evaluators

The sentence-transformers library provides several specialized evaluators for measuring semantic textual similarity, each designed for different evaluation scenarios and data formats.

### EmbeddingSimilarityEvaluator

The `EmbeddingSimilarityEvaluator` is the primary evaluator for semantic similarity tasks. It computes Spearman and Pearson rank correlations between predicted similarities and gold standard similarity scores.

```mermaid
graph TD
    ESE["EmbeddingSimilarityEvaluator"]
    
    subgraph "Input Data"
        S1["sentences1: List[str]"]
        S2["sentences2: List[str]"] 
        SC["scores: List[float]"]
    end
    
    subgraph "Similarity Functions"
        COS["cosine"]
        DOT["dot"]
        EUC["euclidean"] 
        MAN["manhattan"]
    end
    
    subgraph "Metrics"
        PEAR["pearson"]
        SPEAR["spearman"]
    end
    
    subgraph "Embedding Process"
        EMB1["model.encode(sentences1)"]
        EMB2["model.encode(sentences2)"]
        SIMCALC["pairwise_similarity_functions"]
    end
    
    S1 --> EMB1
    S2 --> EMB2
    EMB1 --> SIMCALC
    EMB2 --> SIMCALC
    
    SIMCALC --> COS
    SIMCALC --> DOT
    SIMCALC --> EUC
    SIMCALC --> MAN
    
    COS --> PEAR
    COS --> SPEAR
    DOT --> PEAR
    DOT --> SPEAR
    EUC --> PEAR
    EUC --> SPEAR
    MAN --> PEAR
    MAN --> SPEAR
    
    SC --> PEAR
    SC --> SPEAR
    
    ESE --> S1
    ESE --> S2
    ESE --> SC
```

**Sources:** [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:27-272]()

### BinaryClassificationEvaluator

The `BinaryClassificationEvaluator` treats semantic similarity as a binary classification problem, determining whether pairs of sentences are similar (1) or dissimilar (0).

```mermaid
graph TD
    BCE["BinaryClassificationEvaluator"]
    
    subgraph "Input Processing"
        PAIRS["sentence pairs + binary labels"]
        EMBED["model.encode()"]
        HASHOPT["hashable optimization"]
    end
    
    subgraph "Similarity Computation"
        COSF["pairwise_cos_sim"]
        DOTF["pairwise_dot_score"]
        EUCF["pairwise_euclidean_sim"]
        MANF["pairwise_manhattan_sim"]
    end
    
    subgraph "Threshold Optimization"
        ACCTHRESH["find_best_acc_and_threshold"]
        F1THRESH["find_best_f1_and_threshold"]
    end
    
    subgraph "Metrics"
        ACC["accuracy"]
        F1["f1"]
        PREC["precision"]
        REC["recall"]
        AP["average_precision"]
        MCC["matthews_corrcoef"]
    end
    
    BCE --> PAIRS
    PAIRS --> EMBED
    EMBED --> HASHOPT
    HASHOPT --> COSF
    HASHOPT --> DOTF
    HASHOPT --> EUCF
    HASHOPT --> MANF
    
    COSF --> ACCTHRESH
    COSF --> F1THRESH
    DOTF --> ACCTHRESH
    DOTF --> F1THRESH
    EUCF --> ACCTHRESH
    EUCF --> F1THRESH
    MANF --> ACCTHRESH
    MANF --> F1THRESH
    
    ACCTHRESH --> ACC
    F1THRESH --> F1
    F1THRESH --> PREC
    F1THRESH --> REC
    COSF --> AP
    F1THRESH --> MCC
```

**Sources:** [sentence_transformers/evaluation/BinaryClassificationEvaluator.py:27-379]()

### TripletEvaluator

The `TripletEvaluator` evaluates models using triplets of (anchor, positive, negative) sentences, ensuring that the anchor is more similar to the positive than to the negative example.

```mermaid
graph TD
    TE["TripletEvaluator"]
    
    subgraph "Triplet Input"
        ANC["anchors: List[str]"]
        POS["positives: List[str]"]
        NEG["negatives: List[str]"]
        MAR["margin: float | Dict[str, float]"]
    end
    
    subgraph "Embedding Generation"
        EAANC["embed_inputs(model, anchors)"]
        EPOS["embed_inputs(model, positives)"]
        ENEG["embed_inputs(model, negatives)"]
    end
    
    subgraph "Similarity Calculation"
        SIMPOS["similarity(anchor, positive)"]
        SIMNEG["similarity(anchor, negative)"]
    end
    
    subgraph "Evaluation Logic"
        COMP["positive_scores > negative_scores + margin"]
        ACCUR["accuracy = mean(comparisons)"]
    end
    
    TE --> ANC
    TE --> POS  
    TE --> NEG
    TE --> MAR
    
    ANC --> EAANC
    POS --> EPOS
    NEG --> ENEG
    
    EAANC --> SIMPOS
    EPOS --> SIMPOS
    EAANC --> SIMNEG
    ENEG --> SIMNEG
    
    SIMPOS --> COMP
    SIMNEG --> COMP
    MAR --> COMP
    COMP --> ACCUR
```

**Sources:** [sentence_transformers/evaluation/TripletEvaluator.py:26-271]()

## Similarity Functions and Metrics

The evaluators support multiple similarity functions, each with different mathematical properties and use cases.

| Similarity Function | Implementation | Use Case | Greater is Better |
|-------------------|----------------|----------|------------------|
| `cosine` | `pairwise_cos_sim` | General semantic similarity | ✓ |
| `dot` | `pairwise_dot_score` | When magnitude matters | ✓ |
| `euclidean` | `pairwise_euclidean_sim` | Distance-based similarity | ✗ |
| `manhattan` | `pairwise_manhattan_sim` | L1 distance similarity | ✗ |

```mermaid
graph LR
    subgraph "SimilarityFunction Enum"
        COSINE_ENUM["SimilarityFunction.COSINE"]
        DOT_ENUM["SimilarityFunction.DOT_PRODUCT"] 
        EUC_ENUM["SimilarityFunction.EUCLIDEAN"]
        MAN_ENUM["SimilarityFunction.MANHATTAN"]
    end
    
    subgraph "Implementation Functions"
        COS_FUNC["pairwise_cos_sim"]
        DOT_FUNC["pairwise_dot_score"]
        EUC_FUNC["pairwise_euclidean_sim"]
        MAN_FUNC["pairwise_manhattan_sim"]
    end
    
    subgraph "Evaluator Integration"
        SIM_DICT["similarity_functions dict"]
        SCORE_COMP["score computation"]
        METRIC_CALC["metric calculation"]
    end
    
    COSINE_ENUM --> COS_FUNC
    DOT_ENUM --> DOT_FUNC
    EUC_ENUM --> EUC_FUNC
    MAN_ENUM --> MAN_FUNC
    
    COS_FUNC --> SIM_DICT
    DOT_FUNC --> SIM_DICT
    EUC_FUNC --> SIM_DICT
    MAN_FUNC --> SIM_DICT
    
    SIM_DICT --> SCORE_COMP
    SCORE_COMP --> METRIC_CALC
```

**Sources:** [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:184-189](), [sentence_transformers/evaluation/BinaryClassificationEvaluator.py:238-259](), [sentence_transformers/evaluation/TripletEvaluator.py:187-204]()

## STS Benchmark Integration

The library includes extensive testing and evaluation capabilities for the STS (Semantic Textual Similarity) benchmark, a standard dataset for evaluating semantic similarity models.

### STS Benchmark Testing Framework

```mermaid
graph TD
    subgraph "STS Dataset Loading"
        STSDATA["stsbenchmark.tsv.gz"]
        DOWNLOAD["util.http_get()"]
        PARSE["csv.DictReader parsing"]
    end
    
    subgraph "Data Processing"
        NORM["score normalization (0-5 → 0-1)"]
        SPLIT["train/test split"]
        INPUTEX["InputExample creation"]
    end
    
    subgraph "Evaluation Pipeline"
        EVALCREATE["EmbeddingSimilarityEvaluator.from_input_examples()"]
        MODELEVAL["model.evaluate()"]
        SCORERET["primary_metric score"]
    end
    
    subgraph "Pretrained Model Testing"
        MODLIST["pretrained model list"]
        PERFTEST["pretrained_model_score()"]
        ASSERT["performance assertions"]
    end
    
    STSDATA --> DOWNLOAD
    DOWNLOAD --> PARSE
    PARSE --> NORM
    NORM --> SPLIT
    SPLIT --> INPUTEX
    
    INPUTEX --> EVALCREATE
    EVALCREATE --> MODELEVAL
    MODELEVAL --> SCORERET
    
    MODLIST --> PERFTEST
    PERFTEST --> EVALCREATE
    SCORERET --> ASSERT
```

**Sources:** [tests/test_pretrained_stsb.py:18-49](), [tests/test_train_stsb.py:33-51]()

### Training with STS Data

The library supports training models specifically for semantic similarity using the STS benchmark:

```mermaid
graph TD
    subgraph "Training Setup"
        STSLOAD["STS data loading"]
        DATASET["SentencesDataset creation"]
        DATALOADER["DataLoader setup"]
    end
    
    subgraph "Loss Function"
        COSLOSS["CosineSimilarityLoss"]
        MODELREF["model reference"]
    end
    
    subgraph "Training Process"
        FIT["model.fit()"]
        TRAINOBJ["train_objectives"]
        EPOCHS["epoch configuration"]
    end
    
    subgraph "Evaluation"
        EVALFUNC["evaluate_stsb_test()"]
        THRESHOLD["expected score threshold"]
        ASSERTION["performance assertion"]
    end
    
    STSLOAD --> DATASET
    DATASET --> DATALOADER
    DATALOADER --> TRAINOBJ
    
    COSLOSS --> TRAINOBJ
    MODELREF --> COSLOSS
    
    TRAINOBJ --> FIT
    EPOCHS --> FIT
    
    FIT --> EVALFUNC
    EVALFUNC --> THRESHOLD
    THRESHOLD --> ASSERTION
```

**Sources:** [tests/test_train_stsb.py:74-103](), [tests/test_train_stsb.py:111-127]()

## Advanced Evaluation Features

### Precision and Quantization Support

The `EmbeddingSimilarityEvaluator` supports various embedding precisions for memory-efficient evaluation:

| Precision | Description | Binary Unpacking |
|-----------|-------------|------------------|
| `float32` | Standard floating point | ✗ |
| `int8` | 8-bit signed integer | ✗ |
| `uint8` | 8-bit unsigned integer | ✗ |
| `binary` | Binary with signed conversion | ✓ |
| `ubinary` | Unsigned binary | ✓ |

**Sources:** [sentence_transformers/evaluation/EmbeddingSimilarityEvaluator.py:171-176]()

### Multi-Metric Evaluation

All similarity evaluators support evaluation with multiple similarity functions simultaneously, computing max metrics across functions:

```python