similarity_matrix = util.cos_sim(query_embeddings, passage_embeddings)
```

**Sources:** [docs/pretrained-models/msmarco-v3.md:7-16](), [docs/cross_encoder/pretrained_models.md:16-23]()

## Model Training Evolution

The MS MARCO models have evolved through multiple versions with different training methodologies:

### Training Code Flow

```mermaid
graph TB
    subgraph "Training Components"
        TRAINER["SentenceTransformerTrainer"]
        LOSS_FUNC["MultipleNegativesRankingLoss"]
        EVALUATOR["InformationRetrievalEvaluator"]
        MINING["util.mine_hard_negatives()"]
    end
    
    subgraph "Version Evolution"
        V1_DATA["Basic Pairs<br/>msmarco-v1 datasets"]
        V2_DATA["Improved Negatives<br/>msmarco-v2 datasets"] 
        V3_PROCESS["Hard Negative Mining<br/>cross-encoder/ms-marco-electra-base"]
        V4_DATA["Refined Training<br/>msmarco-v4 models"]
    end
    
    subgraph "Training Pipeline"
        LOAD_MODEL["SentenceTransformer.load()"]
        TRAIN["trainer.train()"]
        EVAL["evaluator.evaluate()"]
        SAVE["model.save()"]
    end
    
    V1_DATA --> V2_DATA
    V2_DATA --> V3_PROCESS
    V3_PROCESS --> V4_DATA
    
    TRAINER --> TRAIN
    LOSS_FUNC --> TRAINER
    EVALUATOR --> EVAL
    MINING --> V3_PROCESS
    
    LOAD_MODEL --> TRAIN
    TRAIN --> EVAL
    EVAL --> SAVE
```

### Version 3 Hard Negative Mining Process

The v3 models used an automated hard negative mining pipeline implemented with sentence-transformers utilities:

1. **Initial Retrieval**: v2 `SentenceTransformer` models encoded queries and retrieved similar passages
2. **Cross-Encoder Scoring**: `CrossEncoder("cross-encoder/ms-marco-electra-base")` scored query-passage pairs
3. **Hard Negative Mining**: `util.mine_hard_negatives()` identified passages with high bi-encoder similarity but low cross-encoder relevance scores
4. **Retraining**: Models trained with `MultipleNegativesRankingLoss` using the mined hard negatives

### Training Loss Functions Used

| Model Version | Primary Loss | Secondary Loss | Evaluation |
|---------------|-------------|----------------|------------|
| v1-v2 | `MultipleNegativesRankingLoss` | - | `InformationRetrievalEvaluator` |
| v3 | `MultipleNegativesRankingLoss` | Hard negative augmentation | `InformationRetrievalEvaluator` |
| v4 | `MultipleNegativesRankingLoss` | Advanced hard negatives | `InformationRetrievalEvaluator` |

**Sources:** [docs/pretrained-models/msmarco-v3.md:53-58](), [docs/sentence_transformer/dataset_overview.md:78-89]()

## Model Selection Guidelines

### Choose Based on Similarity Method

- **Cosine Similarity Models**: Use when you need normalized similarity scores and prefer shorter, focused passages
- **Dot Product Models**: Use when longer, comprehensive passages are preferred and unnormalized scores are acceptable

### Choose Based on Architecture

```mermaid
graph TD
    RETRIEVAL_TASK["Retrieval Task"]
    
    RETRIEVAL_TASK --> FIRST_STAGE["First Stage Retrieval<br/>encode() + similarity search"]
    RETRIEVAL_TASK --> SECOND_STAGE["Second Stage Reranking<br/>predict() on pairs"]
    
    FIRST_STAGE --> ST_CLASS["SentenceTransformer class"]
    SECOND_STAGE --> CE_CLASS["CrossEncoder class"]
    
    ST_CLASS --> ST_FAST["Fast: msmarco-MiniLM-L6-v3<br/>18k queries/sec GPU"]
    ST_CLASS --> ST_BALANCED["Balanced: msmarco-distilbert-base-v4<br/>7k queries/sec, 70.24 NDCG@10"]
    ST_CLASS --> ST_ACCURATE["Accurate: msmarco-distilbert-base-tas-b<br/>71.04 NDCG@10, 34.43 MRR@10"]
    
    CE_CLASS --> CE_FAST["Fast: cross-encoder/ms-marco-TinyBERT-L2-v2<br/>9k docs/sec"]
    CE_CLASS --> CE_ACCURATE["Accurate: cross-encoder/ms-marco-MiniLM-L6-v2<br/>74.30 NDCG@10, 39.01 MRR@10"]
    
    subgraph "Integration Methods"
        UTIL_COS["util.cos_sim()"]
        UTIL_DOT["util.dot_score()"] 
        PREDICT_METHOD["predict() method"]
    end
    
    ST_FAST --> UTIL_COS
    ST_BALANCED --> UTIL_COS
    ST_ACCURATE --> UTIL_DOT
    CE_FAST --> PREDICT_METHOD
    CE_ACCURATE --> PREDICT_METHOD
```

### Performance vs Speed Trade-offs

- **Fastest**: `msmarco-MiniLM-L6-v3` (18,000 queries/sec GPU)
- **Best Balance**: `msmarco-distilbert-base-v4` (7,000 queries/sec GPU, highest accuracy)
- **Highest Quality**: `msmarco-distilbert-base-tas-b` (34.43 MRR@10)

**Sources:** [docs/pretrained-models/msmarco-v3.md:45-50]()

## Integration with Search Systems

MS MARCO models integrate with various search architectures for production deployment. For detailed integration patterns, see [Retrieve & Rerank Architecture](#6.3) and [Semantic Search](#6.1).

**Sources:** [docs/pretrained-models/msmarco-v3.md:19](), [docs/cross_encoder/pretrained_models.md:44]()

# Applications




This page provides an overview of real-world applications and integration patterns using sentence-transformers models. It covers how the three core model types (`SentenceTransformer`, `SparseEncoder`, and `CrossEncoder`) are deployed in production systems for semantic search, retrieval, reranking, and other natural language processing tasks.

For specific implementation details of individual applications, see [Semantic Search](#6.1), [Sparse Search Integration](#6.2), [Retrieve & Rerank Architecture](#6.3), [Semantic Textual Similarity](#6.4), and [Multimodal Applications](#6.5). For information about available pretrained models optimized for specific applications, see [Pretrained Models](#5).

## Core Application Categories

The sentence-transformers library enables three primary categories of applications, each leveraging different model architectures optimized for specific use cases:

### Application Architecture Overview

```mermaid
graph TB
    subgraph "Dense Embedding Applications"
        ST["SentenceTransformer"]
        ST --> SemanticSearch["Semantic Search"]
        ST --> Clustering["Document Clustering"]
        ST --> STS["Semantic Textual Similarity"]
        ST --> Recommendation["Content Recommendation"]
    end
    
    subgraph "Sparse Embedding Applications" 
        SE["SparseEncoder"]
        SE --> NeuralLexical["Neural Lexical Search"]
        SE --> HybridRetrieval["Hybrid Dense-Sparse Retrieval"]
        SE --> KeywordSearch["Enhanced Keyword Search"]
    end
    
    subgraph "Cross-Attention Applications"
        CE["CrossEncoder"]
        CE --> Reranking["Search Result Reranking"]
        CE --> Classification["Text Pair Classification"]
        CE --> ScoreRegression["Similarity Score Regression"]
    end
    
    subgraph "Output Formats"
        SemanticSearch --> DenseVectors["Dense Vectors (384-1024 dim)"]
        NeuralLexical --> SparseVectors["Sparse Vectors (30k+ dim)"]
        Reranking --> SimilarityScores["Similarity Scores (0-1)"]
    end
```

**Dense embedding applications** use `SentenceTransformer` models to convert text into fixed-size dense vectors that capture semantic meaning. These applications excel at finding semantically similar content even when lexical overlap is minimal.

**Sparse embedding applications** use `SparseEncoder` models to generate high-dimensional sparse vectors that preserve lexical information while adding semantic understanding. These applications bridge the gap between traditional keyword search and semantic search.

**Cross-attention applications** use `CrossEncoder` models that jointly process text pairs to produce precise similarity scores. These applications provide the highest accuracy for ranking and classification tasks but with higher computational cost.

Sources: [docs/pretrained-models/msmarco-v2.md:1-39]()

## Integration Patterns

Production systems typically integrate sentence-transformers models through several common patterns, each optimized for different scalability and accuracy requirements:

### System Integration Architecture

```mermaid
graph LR
    subgraph "Data Sources"
        Documents["Document Corpus"]
        Queries["User Queries"]
        TextPairs["Text Pairs"]
    end
    
    subgraph "sentence_transformers"
        STModel["SentenceTransformer.encode()"]
        SEModel["SparseEncoder.encode_query()"]
        CEModel["CrossEncoder.predict()"]
    end
    
    subgraph "Storage Systems"
        VectorDB["Vector Databases<br/>Pinecone, Weaviate, Qdrant"]
        SearchEngines["Search Engines<br/>Elasticsearch, OpenSearch"]
        Cache["Embedding Cache<br/>Redis, Memcached"]
    end
    
    subgraph "Application Layer"
        SearchAPI["Search API"]
        RerankAPI["Reranking API"]
        SimilarityAPI["Similarity API"]
    end
    
    Documents --> STModel
    Documents --> SEModel
    STModel --> VectorDB
    SEModel --> SearchEngines
    
    Queries --> STModel
    Queries --> SEModel
    Queries --> CEModel
    
    VectorDB --> SearchAPI
    SearchEngines --> SearchAPI
    Cache --> SearchAPI
    
    TextPairs --> CEModel
    CEModel --> RerankAPI
    CEModel --> SimilarityAPI
    
    SearchAPI --> RerankAPI
```

**Vector database integration** stores dense embeddings from `SentenceTransformer.encode()` in specialized vector databases optimized for similarity search. Common databases include Pinecone, Weaviate, and Qdrant, which provide approximate nearest neighbor search capabilities.

**Search engine integration** indexes sparse embeddings from `SparseEncoder.encode_query()` and `SparseEncoder.encode_document()` in traditional search engines like Elasticsearch or OpenSearch, enabling hybrid lexical-semantic search.

**API-based reranking** uses `CrossEncoder.predict()` to refine initial retrieval results, typically processing the top-k candidates from a faster first-stage retrieval system.

Sources: [docs/pretrained-models/msmarco-v2.md:7-16]()

## Production Deployment Patterns

### Two-Stage Retrieval Architecture

The most common production pattern combines fast retrieval with precise reranking:

```mermaid
graph TD
    UserQuery["User Query"]
    
    subgraph "Stage 1: Fast Retrieval"
        BiEncoder["SentenceTransformer<br/>or SparseEncoder"]
        CandidateRetrieval["Retrieve Top-100<br/>Candidates"]
    end
    
    subgraph "Stage 2: Precise Reranking"
        CrossEncoder["CrossEncoder.predict()"]
        FinalRanking["Return Top-10<br/>Results"]
    end
    
    UserQuery --> BiEncoder
    BiEncoder --> CandidateRetrieval
    CandidateRetrieval --> CrossEncoder
    CrossEncoder --> FinalRanking
```

This architecture balances computational efficiency with accuracy by using fast bi-encoder models for initial retrieval and slower but more accurate cross-encoder models for final ranking.

### Model Selection by Application Requirements

| Application Type | Model Architecture | Latency | Accuracy | Storage Requirements |
|------------------|-------------------|---------|----------|---------------------|
| Real-time search | `SentenceTransformer` | ~1ms | Good | Dense vectors (384-1024 dim) |
| Hybrid search | `SparseEncoder` | ~2ms | Better | Sparse vectors (30k+ dim) |
| Reranking | `CrossEncoder` | ~10ms | Best | No storage (computed on-demand) |
| Batch processing | Any | Variable | Highest | Depends on architecture |

### Memory and Scaling Considerations

Production deployments must consider memory requirements and scaling patterns:

- **Dense embeddings**: Require 4 bytes per dimension per document (e.g., 1.5KB for 384-dim embeddings)
- **Sparse embeddings**: Store only non-zero values, typically 50-200 active dimensions per document
- **Cross-encoders**: No storage overhead but higher compute cost per query

## Common Integration Libraries

The sentence-transformers library integrates with numerous downstream frameworks and applications:

| Integration Type | Libraries | Use Case |
|------------------|-----------|----------|
| RAG Frameworks | LangChain, LlamaIndex, Haystack | Document retrieval for LLMs |
| Topic Modeling | BERTopic, Top2Vec | Document clustering and topic discovery |
| Few-shot Learning | SetFit | Classification with minimal training data |
| Keyword Extraction | KeyBERT | Semantic keyword extraction |
| Search Applications | txtai | End-to-end search applications |

These integrations typically use the standard `encode()` and `predict()` methods provided by the core model classes, enabling drop-in replacement of embedding models without changing application code.

Sources: [docs/pretrained-models/msmarco-v2.md:19-38]()