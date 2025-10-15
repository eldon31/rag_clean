evaluator = NanoBEIREvaluator(
    dataset_names=["msmarco", "nfcorpus"],
    query_prompts={
        "msmarco": "Retrieve relevant passages: ",
        "nfcorpus": "Find related documents: "
    }
)
```

### Sparse Model Evaluation  

```python
from sentence_transformers import SparseEncoder
from sentence_transformers.sparse_encoder.evaluation import SparseNanoBEIREvaluator

# Evaluation with sparsity constraints
evaluator = SparseNanoBEIREvaluator(
    dataset_names=["msmarco", "scifact"],
    max_active_dims=100,
    show_progress_bar=True
)
results = evaluator(sparse_model)
```

Sources: [sentence_transformers/evaluation/NanoBEIREvaluator.py:101-120](), [sentence_transformers/sparse_encoder/evaluation/SparseNanoBEIREvaluator.py:58-77]()

## Configuration Options

### Core Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `dataset_names` | `List[DatasetNameType]` | Datasets to evaluate on | All 13 datasets |
| `aggregate_fn` | `Callable` | Function to aggregate scores | `np.mean` |
| `aggregate_key` | `str` | Key for aggregated results | `"mean"` |
| `batch_size` | `int` | Batch size for encoding | `32` |
| `show_progress_bar` | `bool` | Show evaluation progress | `False` |

### Metric Configuration

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `mrr_at_k` | `List[int]` | MRR calculation values | `[10]` |
| `ndcg_at_k` | `List[int]` | NDCG calculation values | `[10]` |
| `accuracy_at_k` | `List[int]` | Accuracy calculation values | `[1, 3, 5, 10]` |
| `precision_recall_at_k` | `List[int]` | P/R calculation values | `[1, 3, 5, 10]` |
| `map_at_k` | `List[int]` | MAP calculation values | `[100]` |

### Prompt Configuration

Both `query_prompts` and `corpus_prompts` can be:
- `str`: Same prompt for all datasets
- `Dict[str, str]`: Dataset-specific prompts
- `None`: No prompts used

Sources: [sentence_transformers/evaluation/NanoBEIREvaluator.py:193-211](), [sentence_transformers/evaluation/NanoBEIREvaluator.py:447-466]()

## Key Methods and Data Flow

### Evaluation Process

```mermaid
graph TD
    __call__["__call__(model, output_path, epoch, steps)<br/>Main evaluation entry"]
    _validate_dataset_names["_validate_dataset_names()<br/>Check dataset validity against<br/>dataset_name_to_id.keys()"]
    _validate_prompts["_validate_prompts()<br/>Validate prompt configuration<br/>for each dataset_name"]
    
    create_evaluators["Create self.evaluators list<br/>via _load_dataset() in __init__"]
    
    per_dataset_loop["for evaluator in tqdm(self.evaluators)<br/>desc='Evaluating datasets'"]
    evaluator_call["evaluation = evaluator(model)<br/>Returns dict[metric_name, score]"]
    
    split_metrics["splits = full_key.split('_', maxsplit=<br/>num_underscores_in_name)"]
    collect_per_metric["per_metric_results[metric].append(<br/>metric_value)"]
    
    aggregate_metrics["agg_results[metric] = <br/>self.aggregate_fn(per_metric_results[metric])"]
    
    determine_primary["if not self.primary_metric:<br/>score_function with max ndcg@k"]
    store_metrics["store_metrics_in_model_card_data()<br/>Save to model.model_card_data"]
    write_csv["Write to self.csv_file<br/>(if self.write_csv)"]
    
    __call__ --> _validate_dataset_names
    __call__ --> _validate_prompts
    __call__ --> create_evaluators
    create_evaluators --> per_dataset_loop
    per_dataset_loop --> evaluator_call
    evaluator_call --> split_metrics
    split_metrics --> collect_per_metric
    collect_per_metric --> aggregate_metrics
    aggregate_metrics --> determine_primary
    determine_primary --> store_metrics
    determine_primary --> write_csv
```

Sources: [sentence_transformers/evaluation/NanoBEIREvaluator.py:283-396](), [sentence_transformers/evaluation/NanoBEIREvaluator.py:314-325](), [sentence_transformers/evaluation/NanoBEIREvaluator.py:358-366]()

### Dataset Loading Process

The `_load_dataset` method handles the conversion from Hugging Face dataset format to the format expected by `InformationRetrievalEvaluator`:

```mermaid
graph LR
    load_dataset["load_dataset()<br/>corpus, queries, qrels"]
    corpus_dict["corpus_dict<br/>{sample['_id']: sample['text']}"]
    queries_dict["queries_dict<br/>{sample['_id']: sample['text']}"]
    qrels_dict["qrels_dict<br/>{query-id: set(corpus-ids)}"]
    
    apply_prompts["Apply query_prompts/<br/>corpus_prompts"]
    create_evaluator["self.information_retrieval_class()<br/>InformationRetrievalEvaluator or<br/>SparseInformationRetrievalEvaluator"]
    
    load_dataset --> corpus_dict
    load_dataset --> queries_dict
    load_dataset --> qrels_dict
    
    corpus_dict --> apply_prompts
    queries_dict --> apply_prompts
    qrels_dict --> apply_prompts
    
    apply_prompts --> create_evaluator
```

1. **Load dataset splits**: `corpus`, `queries`, `qrels` from Hub using `datasets.load_dataset`
2. **Convert to dictionaries**: Transform to `{sample["_id"]: sample["text"]}` format
3. **Build relevance mapping**: Create `{sample["query-id"]: set(sample["corpus-id"])}` from qrels
4. **Apply prompts**: Add dataset-specific `query_prompt`/`corpus_prompt` if configured
5. **Create evaluator**: Instantiate via `self.information_retrieval_class` attribute

Sources: [sentence_transformers/evaluation/NanoBEIREvaluator.py:404-434](), [sentence_transformers/evaluation/NanoBEIREvaluator.py:415-421]()

## Output Format and Metrics

### Individual Dataset Results

Each dataset evaluation produces metrics with the pattern: `{dataset_name}_{score_function}_{metric}@{k}`:
- `NanoMSMARCO_cosine_ndcg@10`
- `NanoSciFact_dot_mrr@10`
- `NanoQuoraRetrieval_cosine_map@100`

### Aggregated Results

Aggregated metrics follow the pattern: `NanoBEIR_{aggregate_key}_{score_function}_{metric}@{k}`:
- `NanoBEIR_mean_cosine_ndcg@10`
- `NanoBEIR_mean_dot_mrr@10`

### Sparse Model Additional Metrics

`SparseNanoBEIREvaluator` extends the base functionality with sparsity tracking via `defaultdict(list)` collections:

| Metric | Calculation | Description |
|--------|-------------|-------------|
| `{name}_query_active_dims` | Weighted average by query count | Average active dimensions across all queries |
| `{name}_query_sparsity_ratio` | Weighted average by query count | Sparsity ratio (1 - active/total) for queries |
| `{name}_corpus_active_dims` | Weighted average by corpus size | Average active dimensions across all documents |
| `{name}_corpus_sparsity_ratio` | Weighted average by corpus size | Sparsity ratio for corpus documents |

The sparsity calculation process:

```mermaid
graph LR
    per_evaluator["Each evaluator.sparsity_stats<br/>{key: value}"]
    collect["self.sparsity_stats[key]<br/>.append(value)"]
    weight_calc["sum(val * length for val, length in <br/>zip(value, self.lengths[key.split('_')[0]])"]
    normalize["/ sum(self.lengths[key.split('_')[0]])"]
    
    prefix_metrics["self.prefix_name_to_metrics(<br/>self.sparsity_stats, self.name)"]
    
    per_evaluator --> collect
    collect --> weight_calc
    weight_calc --> normalize
    normalize --> prefix_metrics
```

Sources: [sentence_transformers/sparse_encoder/evaluation/SparseNanoBEIREvaluator.py:222-231](), [sentence_transformers/sparse_encoder/evaluation/SparseInformationRetrievalEvaluator.py:202-212]()

## Primary Metric Selection

The primary metric is determined by:
1. **Explicit main_score_function**: Use `{main_score_function}_ndcg@{max(ndcg_at_k)}`
2. **Automatic selection**: Choose score function with highest NDCG@k score
3. **Format**: `NanoBEIR_{aggregate_key}_{score_function}_ndcg@{k}`

The primary metric is used for model selection and optimization during training.

Sources: [sentence_transformers/evaluation/NanoBEIREvaluator.py:358-366]()

# Pretrained Models




This page provides an overview of the extensive collection of pretrained models available in the sentence-transformers library and guidance on selecting the right model for your task. With over 15,000 models available on the Hugging Face Hub, this overview helps you navigate the three main model architectures and understand when to use each type.

The library offers three distinct model architectures, each optimized for different use cases:
- **SentenceTransformer**: Dense vector embeddings for semantic similarity and clustering
- **SparseEncoder**: Sparse vector embeddings for efficient retrieval and search engine integration  
- **CrossEncoder**: Pairwise scoring models for reranking and classification

For detailed model catalogs and specific recommendations, see [SentenceTransformer Models](#5.1), [SparseEncoder Models](#5.2), [CrossEncoder Models](#5.3), and [MSMARCO Models](#5.4).

## Model Architecture Overview

Model Architecture Comparison
```mermaid
graph TB
    subgraph "sentence_transformers.SentenceTransformer"
        ST_CLASS["SentenceTransformer"]
        ST_ENCODE["model.encode()"]
        ST_SIM["model.similarity()"]
        ST_MODELS["all-mpnet-base-v2<br/>all-MiniLM-L6-v2<br/>paraphrase-mpnet-base-v2"]
    end
    
    subgraph "sentence_transformers.SparseEncoder"  
        SE_CLASS["SparseEncoder"]
        SE_ENCODE["model.encode()"]
        SE_SPARSE["model.sparsity()"]
        SE_MODELS["naver/splade-cocondenser-ensembledistil<br/>prithivida/Splade_PP_en_v1"]
    end
    
    subgraph "sentence_transformers.CrossEncoder"
        CE_CLASS["CrossEncoder"] 
        CE_PREDICT["model.predict()"]
        CE_RANK["model.rank()"]
        CE_MODELS["cross-encoder/ms-marco-MiniLM-L6-v2<br/>cross-encoder/ms-marco-TinyBERT-L2-v2"]
    end
    
    subgraph "Output_Types"
        DENSE["Dense Vectors<br/>torch.Tensor[batch, 384-1024]<br/>util.cos_sim()"]
        SPARSE["Sparse Vectors<br/>torch.Tensor[batch, vocab_size]<br/>util.dot_score()"]
        SCORES["Scalar Scores<br/>torch.Tensor[batch]<br/>torch.sigmoid()"]
    end
    
    ST_CLASS --> DENSE
    SE_CLASS --> SPARSE  
    CE_CLASS --> SCORES
```

Model Selection Decision Tree
```mermaid
graph TD
    START["What is your use case?"]
    
    START --> SEMANTIC["Semantic Search<br/>Similarity Comparison<br/>Clustering"]
    START --> RETRIEVAL["Document Retrieval<br/>Search Engine Integration<br/>Keyword + Semantic"]
    START --> RANKING["Reranking<br/>Pairwise Classification<br/>Relevance Scoring"]
    
    SEMANTIC --> ST_CHOICE["Use SentenceTransformer<br/>See page 5.1"]
    RETRIEVAL --> SE_CHOICE["Use SparseEncoder<br/>See page 5.2"] 
    RANKING --> CE_CHOICE["Use CrossEncoder<br/>See page 5.3"]
    
    ST_CHOICE --> ST_SPEED["Speed Priority?"]
    ST_SPEED --> ST_FAST["all-MiniLM-L6-v2<br/>14,200 sent/sec"]
    ST_SPEED --> ST_QUALITY["all-mpnet-base-v2<br/>Best quality"]
    
    SE_CHOICE --> SE_LANG["Language?"]
    SE_LANG --> SE_EN["English:<br/>splade-cocondenser-ensembledistil"]
    SE_LANG --> SE_MULTI["Multilingual:<br/>Available models limited"]
    
    CE_CHOICE --> CE_DOMAIN["Domain?"]
    CE_DOMAIN --> CE_GENERAL["General:<br/>cross-encoder/ms-marco-MiniLM-L6-v2"]
    CE_DOMAIN --> CE_SPECIFIC["Domain-specific:<br/>See MSMARCO page 5.4"]
```

**Sources:** [README.md:19](), [docs/sentence_transformer/pretrained_models.md:16-27](), [index.rst:37-132]()

## Model Discovery and Selection

Model Discovery Pathways
```mermaid
graph TB
    subgraph "Official_Sources"
        HF_ORG["huggingface.co/sentence-transformers<br/>Official model organization<br/>~100 curated models"]
        DOCS_HTML["docs/_static/html/models_en_sentence_embeddings.html<br/>Interactive Vue.js browser<br/>Sortable performance tables"]
    end
    
    subgraph "Community_Sources"
        HF_COMMUNITY["huggingface.co/models?library=sentence-transformers<br/>15,000+ community models<br/>Diverse domains and languages"]
        MTEB_BOARD["huggingface.co/spaces/mteb/leaderboard<br/>MTEB benchmark rankings<br/>State-of-the-art performance"]
    end
    
    subgraph "Selection_Criteria"
        TASK_FIT["Task Compatibility<br/>sentence_performance: 49-70<br/>semantic_search: 22-57"]
        SPEED_REQ["Speed Requirements<br/>GPU: 800-34000 sent/sec<br/>CPU: 30-750 sent/sec"]
        RESOURCE_LIMIT["Resource Constraints<br/>Model size: 43-1360 MB<br/>Memory requirements"]
    end
    
    HF_ORG --> TASK_FIT
    DOCS_HTML --> SPEED_REQ
    MTEB_BOARD --> RESOURCE_LIMIT
```

Selection Criteria and Properties
| Property | Code Reference | Typical Values | Impact |
|---|---|---|---|
| Dimensions | `model.get_sentence_embedding_dimension()` | 384, 768, 1024 | Memory usage, similarity computation speed |
| Normalized Embeddings | `normalized_embeddings: true/false` | Boolean | Score function compatibility |
| Score Functions | `score_functions: ["cos", "dot", "eucl"]` | Array of strings | Similarity computation method |
| Max Sequence Length | `max_seq_length` | 128, 256, 512 | Input text limitations |
| Model Size | File size in MB | 43-1360 MB | Storage and loading time |

**Sources:** [README.md:2](), [docs/_static/html/models_en_sentence_embeddings.html:236-550](), [docs/sentence_transformer/pretrained_models.md:4-7]()

## Benchmark Evaluation Framework

Evaluation Metrics and Datasets
```mermaid
graph TB
    subgraph "SentenceTransformer_Evaluation"
        ST_SENTENCE["Sentence Performance<br/>14 diverse tasks<br/>STS, classification, clustering"]
        ST_SEARCH["Semantic Search<br/>6 retrieval datasets<br/>Query-passage matching"]
        ST_SPEED["Inference Speed<br/>V100 GPU / 8-core CPU<br/>sentences per second"]
    end
    
    subgraph "SparseEncoder_Evaluation" 
        SE_SPARSITY["Sparsity Metrics<br/>SparseEncoder.sparsity()<br/>sparsity_ratio calculation"]
        SE_RETRIEVAL["Sparse Retrieval<br/>BEIR benchmark<br/>Neural-lexical search"]
        SE_EFFICIENCY["Memory Efficiency<br/>Storage compression<br/>Index size optimization"]
    end
    
    subgraph "CrossEncoder_Evaluation"
        CE_RERANK["Reranking Performance<br/>TREC-DL datasets<br/>NDCG@10 scores"]
        CE_CLASSIFICATION["Classification Tasks<br/>Binary/multi-class<br/>Accuracy and F1"]
        CE_SPEED["Prediction Speed<br/>Pairs per second<br/>GPU/CPU throughput"]
    end
```

Performance Ranges by Model Type
| Model Type | Performance Metric | Range | Best Models |
|---|---|---|---|
| SentenceTransformer | Sentence Performance | 49-70 | `all-mpnet-base-v2` (69.57) |
| SentenceTransformer | Semantic Search | 22-57 | `all-mpnet-base-v2` (57.02) |
| SparseEncoder | Sparsity Ratio | 99.5-99.9% | `splade-cocondenser-ensembledistil` |
| CrossEncoder | NDCG@10 | 60-75 | `ms-marco-MiniLM-L6-v2` (74.30) |
| All Types | Inference Speed | 800-34000 sent/sec | GPU performance varies by size |

**Sources:** [docs/_static/html/models_en_sentence_embeddings.html:113-151](), [README.md:164-166](), [docs/pretrained-models/msmarco-v5.md:29-44]()

## Quick Start Recommendations

The following table provides starting points for common use cases, with links to detailed model catalogs:

| Use Case | Recommended Model | Performance | Speed | Documentation |
|---|---|---|---|---|
| **General Embeddings** | `all-mpnet-base-v2` | Best quality (69.57) | 2800 sent/sec | [Page 5.1](#5.1) |
| **Fast Embeddings** | `all-MiniLM-L6-v2` | Good quality (68.06) | 14200 sent/sec | [Page 5.1](#5.1) |
| **Semantic Search** | `multi-qa-mpnet-base-cos-v1` | High search (57.46) | 4000 sent/sec | [Page 5.1](#5.1) |
| **Sparse Retrieval** | `naver/splade-cocondenser-ensembledistil` | SPLADE architecture | Memory efficient | [Page 5.2](#5.2) |
| **Reranking** | `cross-encoder/ms-marco-MiniLM-L6-v2` | NDCG@10: 74.30 | 39.01 MRR@10 | [Page 5.3](#5.3) |
| **MSMARCO Tasks** | `msmarco-distilbert-dot-v5` | MRR@10: 37.25 | 7000 sent/sec | [Page 5.4](#5.4) |

### Model Series Overview

**General Purpose (`all-*` series)**
- Trained on 1B+ training pairs from diverse sources
- Best for general semantic understanding tasks
- Available in multiple sizes: MiniLM (fast), DistilRoBERTa (balanced), MPNet (quality)

**Search-Optimized (`multi-qa-*` and `msmarco-*` series)**  
- Fine-tuned for question-answering and information retrieval
- Optimized for query-passage similarity measurement
- Available in dot-product and cosine similarity variants

**Sparse Models (SPLADE variants)**
- Neural sparse representations for efficient retrieval
- Compatible with inverted index search engines
- High sparsity (99%+) while maintaining semantic understanding

**Cross-Encoder Rerankers**
- Highest accuracy for pairwise relevance scoring
- Computationally intensive but precise
- Ideal for reranking small candidate sets

### Navigation to Detailed Catalogs

- **[SentenceTransformer Models](#5.1)**: Complete catalog of dense embedding models with performance comparisons and specialized variants
- **[SparseEncoder Models](#5.2)**: Sparse model architectures, SPLADE variants, and search engine integration guides  
- **[CrossEncoder Models](#5.3)**: Reranking and classification models across different domains and tasks
- **[MSMARCO Models](#5.4)**: Specialized documentation for MSMARCO-trained models with version histories and performance evolution

**Sources:** [docs/sentence_transformer/pretrained_models.md:45-124](), [README.md:169-176](), [docs/_static/html/models_en_sentence_embeddings.html:470-550]()

## Loading and Usage Patterns

### Basic Loading Patterns

All pretrained models follow consistent loading and usage patterns through their respective classes from the `sentence_transformers` package:

```python
# SentenceTransformer - Dense vector embeddings
from sentence_transformers import SentenceTransformer

# Official models (no prefix needed)
model = SentenceTransformer("all-mpnet-base-v2")
# Community models (full path required)  
model = SentenceTransformer("BAAI/bge-large-en")

sentences = ["The weather is lovely today.", "It's sunny outside!"]
embeddings = model.encode(sentences)
similarities = model.similarity(embeddings, embeddings)
```

```python