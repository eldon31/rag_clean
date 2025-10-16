sentences = ["This is a test sentence", "This is another test"]
embeddings = model.encode(sentences)
print(f"Generated embeddings shape: {embeddings.shape}")
```

### Backend-Specific Verification

Test different backends if installed:

```python
# Test ONNX backend (if installed)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2', backend='onnx')

# Test OpenVINO backend (if installed)  
model = SentenceTransformer('all-MiniLM-L6-v2', backend='openvino')

# Check GPU availability
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
```

**Sources:** [docs/installation.md:1-177]()