cosine_similarity = util.cos_sim(query_embedding, passage_embedding)
dot_product_similarity = util.dot_score(query_embedding, passage_embedding)

print("Cosine similarity:", cosine_similarity)
```

### Cross-Encoder Model Usage

```python
from sentence_transformers import CrossEncoder
import torch

# Load cross-encoder with sigmoid activation for 0-1 scores
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2", activation_fn=torch.nn.Sigmoid())

# Score query-passage pairs
scores = model.predict([
    ("How big is London", "London has 9,787,426 inhabitants at the 2011 census"),
    ("How big is London", "London is well known for its museums")
])
# Returns array([0.9998173, 0.01312432], dtype=float32)
```

### Batch Processing for Production

```python