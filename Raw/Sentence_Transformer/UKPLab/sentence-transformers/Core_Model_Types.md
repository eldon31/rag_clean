This document covers the three core model architectures in the sentence-transformers library: `SentenceTransformer`, `SparseEncoder`, and `CrossEncoder`. Each serves distinct use cases in text encoding and similarity tasks.

For information about training these model types, see pages [3.1](#3.1), [3.2](#3.2), and [3.3](#3.3). For details on available pretrained models, see pages [5.1](#5.1), [5.2](#5.2), and [5.3](#5.3).

## Architecture Overview

The sentence-transformers library provides three main model architectures that differ in their encoding approach and use cases:

```mermaid
graph TB
    subgraph "Input Processing"
        Text["Text Input(s)"]
    end
    
    subgraph "Core Model Types"
        ST["SentenceTransformer<br/>Dense Embeddings"]
        SE["SparseEncoder<br/>Sparse Embeddings"]
        CE["CrossEncoder<br/>Pairwise Scoring"]
    end
    
    subgraph "Output Types"
        Dense["Dense Vectors<br/>[batch_size, embedding_dim]"]
        Sparse["Sparse Vectors<br/>[batch_size, vocab_size]"]
        Scores["Similarity Scores<br/>[batch_size] or [batch_size, num_labels]"]
    end
    
    subgraph "Use Cases"
        SemanticSearch["Semantic Search"]
        Clustering["Clustering"]
        LexicalSearch["Neural Lexical Search"]
        HybridRetrieval["Hybrid Retrieval"]
        Reranking["Reranking"]
        Classification["Text Classification"]
    end
    
    Text --> ST
    Text --> SE
    Text --> CE
    
    ST --> Dense
    SE --> Sparse
    CE --> Scores
    
    Dense --> SemanticSearch
    Dense --> Clustering
    Sparse --> LexicalSearch
    Sparse --> HybridRetrieval
    Scores --> Reranking
    Scores --> Classification
```

**Sources:** [sentence_transformers/SentenceTransformer.py:61-163](), [sentence_transformers/sparse_encoder/SparseEncoder.py:27-129](), [sentence_transformers/cross_encoder/CrossEncoder.py:48-116](), [README.md:15-17]()

## SentenceTransformer

The `SentenceTransformer` class is the primary model for generating dense vector embeddings from text. It encodes individual sentences or documents into fixed-size dense vectors suitable for semantic similarity tasks.

### Core Architecture

```mermaid
graph LR
    subgraph "SentenceTransformer Pipeline"
        Input["Text Input"]
        Tokenizer["tokenize()"]
        Transformer["Transformer Module"]
        Pooling["Pooling Module"]
        Optional["Optional Modules<br/>(Normalize, Dense, etc.)"]
        Output["Dense Embedding"]
    end
    
    Input --> Tokenizer
    Tokenizer --> Transformer
    Transformer --> Pooling
    Pooling --> Optional
    Optional --> Output
    
    subgraph "Key Methods"
        Encode["encode()"]
        EncodeQuery["encode_query()"]
        EncodeDoc["encode_document()"]
        Similarity["similarity()"]
    end
```

The `SentenceTransformer` class inherits from `nn.Sequential`, `FitMixin`, and `PeftAdapterMixin`, allowing it to function as a sequential pipeline of modules while supporting training and PEFT adapters.

### Key Features

- **Modular Design**: Composed of sequential modules like `Transformer`, `Pooling`, `Normalize`
- **Prompt Support**: Configurable prompts for different tasks via `prompts` dictionary
- **Task-Specific Encoding**: `encode_query()` and `encode_document()` methods for asymmetric retrieval
- **Multiple Backends**: Supports PyTorch, ONNX, and OpenVINO backends
- **Similarity Functions**: Built-in similarity computation with configurable functions

### Usage Patterns

```python