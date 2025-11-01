model = SparseEncoder("sentence-transformers/all-MiniLM-L6-v2")

loss = CSRLoss(
    model=model,
    loss=SparseMultipleNegativesRankingLoss(model),
    beta=0.1,  # L_aux weight
    gamma=1.0  # Main loss weight
)
```

### Architecture Requirements

```mermaid
graph TD
    subgraph "Model Architecture Requirements"
        SPLADE["SPLADE Models"]
        CSR["CSR Models"]
        
        MLMTransformer["MLMTransformer<br/>MLM head access"]
        SpladePooling["SpladePooling<br/>Sparse pooling"]
        
        Autoencoder["Autoencoder Components<br/>encode/decode methods"]
        BackboneEmb["sentence_embedding_backbone"]
        DecodedEmb["decoded_embedding_k/4k/aux"]
        
        SPLADE --> MLMTransformer
        SPLADE --> SpladePooling
        
        CSR --> Autoencoder
        CSR --> BackboneEmb
        CSR --> DecodedEmb
    end
```

Sources: [sentence_transformers/sparse_encoder/models/MLMTransformer.py:26-54](), [sentence_transformers/sparse_encoder/models/SpladePooling.py:13-39](), [sentence_transformers/sparse_encoder/losses/CSRLoss.py:68-98]()