def _append_csv_headers(self, similarity_fn_names):
    super()._append_csv_headers(similarity_fn_names)
    self.csv_headers.extend([
        "query_active_dims", "query_sparsity_ratio", 
        "corpus_active_dims", "corpus_sparsity_ratio"
    ])
```

### Model Card Integration

Sparse evaluators store evaluation metrics in the model's card data for documentation:

```python
def store_metrics_in_model_card_data(self, model, metrics, epoch=0, step=0):
    model.model_card_data.set_evaluation_metrics(self, metrics, epoch=epoch, step=step)
```

Sources: [sentence_transformers/sparse_encoder/evaluation/SparseInformationRetrievalEvaluator.py:271-274](), [sentence_transformers/sparse_encoder/evaluation/SparseEmbeddingSimilarityEvaluator.py:159-162]()