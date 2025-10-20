# Kaggle Installation Commands for Ultimate Embedder V4

## Complete Installation Command (Copy-Paste Ready)

```bash
# CRITICAL: Install protobuf 3.x FIRST to avoid MessageFactory errors
pip install --upgrade "protobuf>=3.20.0,<4.0.0"

# Then install all other dependencies
pip install sentence-transformers transformers scikit-learn faiss-gpu psutil requests tqdm accelerate datasets

# Optional: ONNX Runtime for backend optimization (if not already installed)
pip install onnxruntime-gpu optimum[onnxruntime-gpu]
```

## Single-Line Installation (Alternative)

```bash
pip install --upgrade "protobuf>=3.20.0,<4.0.0" sentence-transformers transformers scikit-learn faiss-gpu psutil requests tqdm accelerate datasets onnxruntime-gpu "optimum[onnxruntime-gpu]"
```

## Troubleshooting

### If you see "Multiple distributions found for package optimum"

Run this cleanup command:
```bash
pip uninstall optimum optimum-onnx -y && pip install "optimum[onnxruntime-gpu]"
```

### If you still see protobuf errors

Force reinstall protobuf:
```bash
pip uninstall protobuf -y && pip install "protobuf==3.20.3"
```

### Verify Installation

```python
import protobuf
print(f"Protobuf version: {protobuf.__version__}")
# Should show 3.x.x (NOT 4.x.x)

import sentence_transformers
import onnxruntime
print("All imports successful!")
```

## Notes

- **protobuf < 4.0** is CRITICAL to avoid `AttributeError: 'MessageFactory' object has no attribute 'GetPrototype'`
- The environment variable `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` is already set in the embedder code
- FAISS GPU version is used for Kaggle's T4 GPUs
- ONNX Runtime GPU provides backend optimization for faster inference