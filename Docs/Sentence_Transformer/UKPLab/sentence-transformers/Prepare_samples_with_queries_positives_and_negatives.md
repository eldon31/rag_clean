samples = [
    {
        "query": "What is machine learning?",
        "positive": ["Machine learning is a subset of AI"],
        "negative": ["The weather is nice today", "Cats are animals"]
    }
]

evaluator = RerankingEvaluator(samples=samples, name="rerank_test")
results = evaluator(model)
print(f"NDCG@10: {results['rerank_test_ndcg@10']}")
```

### Information Retrieval Evaluation

```python
from sentence_transformers.evaluation import InformationRetrievalEvaluator

# Prepare queries, corpus, and relevance judgments
queries = {"q1": "machine learning definition"}
corpus = {"d1": "ML is AI subset", "d2": "Weather is sunny"}  
relevant_docs = {"q1": {"d1"}}

evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus, 
    relevant_docs=relevant_docs,
    name="ir_test"
)
results = evaluator(model)
print(f"MAP@100: {results['ir_test_cosine_map@100']}")
```

Sources: [sentence_transformers/evaluation/BinaryClassificationEvaluator.py:49-83](), [sentence_transformers/evaluation/RerankingEvaluator.py:48-87](), [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:54-123](), [tests/test_pretrained_stsb.py:74-79]()

## Training Integration

Evaluators integrate with training systems to monitor model performance during training. They are called at specified intervals to compute metrics and store results in CSV files and model metadata.

**Training and Evaluation Integration**
```mermaid
flowchart TD
    subgraph training["Training System"]
        TR["Trainer"]
        TD["Training Data"]
        LOSS["Loss Functions"]
    end
    
    subgraph evaluation["Evaluation System"]  
        BCE["BinaryClassificationEvaluator"]
        RE["RerankingEvaluator"]
        IRE["InformationRetrievalEvaluator"] 
        CSV["CSV Results"]
        MCD["ModelCardData"]
    end
    
    subgraph model["Model"]
        CE["CrossEncoder"]
    end
    
    TD --> TR
    LOSS --> TR
    TR --> CE
    
    CE --> BCE
    CE --> RE  
    CE --> IRE
    
    BCE --> CSV
    RE --> CSV
    IRE --> CSV
    
    BCE --> MCD
    RE --> MCD
    IRE --> MCD
    
    MCD --> CE
```

### Evaluation During Training

Evaluators are called with epoch and step parameters to track training progress:

```python
# Called automatically during training
results = evaluator(model, output_path="./results", epoch=1, steps=100)

# Results are written to CSV files like:
# - binary_classification_evaluation_results.csv  
# - RerankingEvaluator_results_@10.csv
# - Information-Retrieval_evaluation_results.csv
```

### Model Card Integration

Evaluation results are automatically stored in the model's metadata via the `store_metrics_in_model_card_data()` method, which updates `model.model_card_data` with performance metrics.

Sources: [sentence_transformers/evaluation/BinaryClassificationEvaluator.py:151-221](), [sentence_transformers/evaluation/RerankingEvaluator.py:137-198](), [sentence_transformers/evaluation/InformationRetrievalEvaluator.py:211-290]()

## 6. Creating Custom Evaluators

You can create custom evaluators for specialized evaluation tasks by:

1. Inheriting from the base evaluator class
2. Implementing the required evaluation methods
3. Defining metrics that are relevant to your task

A custom evaluator class typically implements:
- An initialization method that accepts test data
- An evaluation method that computes scores for the test data
- Methods to compute task-specific metrics

## 7. Common Evaluation Metrics

Different tasks require different evaluation metrics:

| Task Type | Common Metrics | Description |
|-----------|----------------|-------------|
| Binary Classification | Accuracy, F1, AUC | Measure classification performance |
| Ranking | nDCG, MAP, MRR | Assess ranking quality |
| Retrieval | Precision@k, Recall@k | Evaluate retrieval effectiveness |
| Regression | MSE, Pearson/Spearman correlation | Measure score prediction accuracy |

Sources: System architecture diagrams from prompt, tests/test_pretrained_stsb.py (lines 39-46)

## 8. Performance Considerations

When evaluating large datasets, consider:

- Batch processing: Evaluate models in batches to avoid memory issues
- Caching: Cache model outputs to avoid redundant computation
- Metrics selection: Choose metrics appropriate for your task and dataset size

Efficient evaluation is especially important when working with resource-intensive models or large test sets.

## 9. Comparison with SentenceTransformer Evaluators

While both types of evaluators assess model performance, they differ in key ways:

| CrossEncoder Evaluators | SentenceTransformer Evaluators |
|------------------------|--------------------------------|
| Evaluate pair scoring | Evaluate embedding quality |
| Focus on classification/ranking metrics | Focus on similarity and retrieval metrics |
| Work with direct text pair inputs | Work with embeddings |
| Suited for reranking tasks | Suited for retrieval and similarity tasks |

Understanding these differences helps in selecting the appropriate evaluation method for your model type and task.