document_embeddings = model.encode_document([
    "Climate change affects marine ecosystems...",
    "AI development began in the 1950s..."
])
```

**Sources:** [sentence_transformers/SentenceTransformer.py:416-543](), [sentence_transformers/SentenceTransformer.py:545-675](), [README.md:60-87]()

## SparseEncoder: Sparse Embeddings

`SparseEncoder` models create sparse vector representations where most values are zero, enabling efficient neural lexical search and hybrid retrieval systems.

### Basic Usage

```python
from sentence_transformers import SparseEncoder

# Load a sparse encoder model
model = SparseEncoder("naver/splade-cocondenser-ensembledistil")

sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
]

# Generate sparse embeddings
embeddings = model.encode(sentences)
print(embeddings.shape)
# (3, 30522) - vocabulary size dimensions

# Calculate similarities (using dot product for sparse vectors)
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[35.629, 9.154, 0.098],
#         [9.154, 27.478, 0.019],
#         [0.098, 0.019, 29.553]])

# Check sparsity statistics
stats = SparseEncoder.sparsity(embeddings)
print(f"Sparsity: {stats['sparsity_ratio']:.2%}")
# Sparsity: 99.84%
```

### Query and Document Encoding

```python