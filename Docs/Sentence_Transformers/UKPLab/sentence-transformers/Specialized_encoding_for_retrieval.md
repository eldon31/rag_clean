query_embeddings = model.encode_query("machine learning algorithms")
document_embeddings = model.encode_document([
    "Machine learning uses statistical techniques...",
    "Deep learning is a subset of machine learning..."
])
```

**Sources:** [sentence_transformers/sparse_encoder/SparseEncoder.py:181-293](), [sentence_transformers/sparse_encoder/SparseEncoder.py:295-410](), [README.md:134-167]()

## CrossEncoder: Reranking and Classification

`CrossEncoder` models take pairs of texts as input and output similarity scores or classification labels, providing high-precision reranking capabilities.

### Basic Usage

```python
from sentence_transformers import CrossEncoder

# Load a cross-encoder model
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

# Define query and candidate passages
query = "How many people live in Berlin?"
passages = [
    "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.",
    "Berlin has a yearly total of about 135 million day visitors, making it one of the most-visited cities in the European Union.",
    "In 2013 around 600,000 Berliners were registered in one of the more than 2,300 sport and fitness clubs.",
]

# Predict similarity scores for query-passage pairs
scores = model.predict([(query, passage) for passage in passages])
print(scores)
# [8.607139 5.506266 6.352977]
```

### Ranking Documents

```python