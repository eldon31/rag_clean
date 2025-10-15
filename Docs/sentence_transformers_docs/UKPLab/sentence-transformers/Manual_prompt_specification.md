emb = model.encode("Text to encode", prompt="Represent this text: ")
```

**Performance Optimization**:
- `normalize_embeddings=True`: Enable dot-product similarity
- `convert_to_tensor=False`: Return numpy arrays for storage
- `precision="int8"`: Quantized embeddings for memory efficiency
- `batch_size=64`: Adjust for your hardware

Sources: [sentence_transformers/SentenceTransformer.py:309-386](), [sentence_transformers/SentenceTransformer.py:424-432]()

## Model Discovery and Metadata

The interactive model browser provides comprehensive model information:

```mermaid
graph TB
    subgraph "Model Browser Interface"
        HTML["models_en_sentence_embeddings.html"] --> Filters["Performance Filters"]
        HTML --> Sort["Sortable Columns"]
        HTML --> Details["Expandable Details"]
    end
    
    subgraph "Model Metadata"
        Name["Model Name"] --> HFHub["Hugging Face Hub"]
        Perf["Performance Metrics"] --> Benchmarks["14 Sentence Tasks<br/>6 Search Tasks"]
        Speed["Encoding Speed"] --> Hardware["V100 GPU Benchmarks"]
        Size["Model Size"] --> Storage["MB Requirements"]
    end
    
    subgraph "Selection Criteria"
        Task["Task Requirements"] --> Filter1["Performance Threshold"]
        Hardware["Hardware Constraints"] --> Filter2["Speed/Size Limits"]
        Quality["Quality Needs"] --> Filter3["Metric Requirements"]
    end
```

The browser enables filtering by performance, speed, and size to find optimal models for specific requirements.

Sources: [docs/_static/html/models_en_sentence_embeddings.html:106-228](), [docs/sentence_transformer/pretrained_models.md:41-49]()