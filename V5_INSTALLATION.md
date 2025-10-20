# V5 Installation Guide

## Overview
Complete installation instructions for the V5 RAG system with multi-framework integration.

## Prerequisites
- Python 3.9+
- CUDA 11.8+ (for GPU support)
- 16GB+ RAM (32GB recommended)
- 10GB+ disk space

## Installation Methods

### Method 1: Quick Install (Recommended)
```bash
# Install all V5 dependencies
pip install -r requirements_v5.txt
```

### Method 2: Kaggle Environment
```bash
# On Kaggle, use GPU-optimized versions
pip install -r requirements_v5.txt --extra-index-url https://download.pytorch.org/whl/cu118
```

### Method 3: Step-by-Step Installation

#### 1. Core ML Libraries
```bash
pip install torch>=2.1.0 transformers>=4.36.0 sentence-transformers>=2.3.0
pip install numpy>=1.24.0 scikit-learn>=1.3.0
```

#### 2. Vector Search
```bash
pip install faiss-cpu>=1.7.4  # or faiss-gpu for GPU
pip install qdrant-client>=1.7.0
```

#### 3. Document Processing (Docling)
```bash
pip install docling>=1.0.0 docling-core>=1.0.0
pip install pdfplumber>=0.10.0 python-docx>=1.1.0 Pillow>=10.0.0
```

#### 4. Code Parsing (Tree-sitter)
```bash
pip install tree-sitter>=0.20.0
pip install tree-sitter-python tree-sitter-javascript tree-sitter-typescript
pip install tree-sitter-rust tree-sitter-go tree-sitter-java tree-sitter-cpp
```

#### 5. Semantic Chunking (Semchunk)
```bash
pip install semchunk>=0.2.0 tiktoken>=0.5.0
```

#### 6. LlamaIndex Integration
```bash
pip install llama-index>=0.9.0 llama-index-core>=0.9.0
pip install llama-index-readers-file>=0.1.0
```

#### 7. GPU Optimization (Optional)
```bash
pip install onnxruntime-gpu>=1.16.0
pip install optimum[onnxruntime]>=1.16.0
pip install accelerate>=0.25.0
```

## Verification

### Test Installation
```python
# test_v5_installation.py
import sys

def test_imports():
    """Test that all V5 dependencies are installed correctly."""
    
    tests = {
        "PyTorch": lambda: __import__("torch"),
        "Transformers": lambda: __import__("transformers"),
        "Sentence Transformers": lambda: __import__("sentence_transformers"),
        "FAISS": lambda: __import__("faiss"),
        "Qdrant Client": lambda: __import__("qdrant_client"),
        "Docling": lambda: __import__("docling"),
        "Docling Core": lambda: __import__("docling_core"),
        "Tree-sitter": lambda: __import__("tree_sitter"),
        "Semchunk": lambda: __import__("semchunk"),
        "LlamaIndex": lambda: __import__("llama_index"),
        "Tiktoken": lambda: __import__("tiktoken"),
        "ONNX Runtime": lambda: __import__("onnxruntime"),
    }
    
    print("Testing V5 Installation...")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests.items():
        try:
            test_fn()
            print(f"✓ {name:<30} INSTALLED")
            passed += 1
        except ImportError as e:
            print(f"✗ {name:<30} MISSING")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        print("\nInstall missing packages:")
        print("pip install -r requirements_v5.txt")
        sys.exit(1)
    else:
        print("\n✓ All V5 dependencies installed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    test_imports()
```

Run the test:
```bash
python test_v5_installation.py
```

### Check GPU Support
```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU count: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
```

## Troubleshooting

### Common Issues

#### 1. CUDA/GPU Issues
```bash
# Check CUDA version
nvcc --version

# Reinstall PyTorch with correct CUDA version
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

#### 2. Protobuf Version Conflicts
```bash
# Fix protobuf compatibility
pip install protobuf>=3.20.0,<5.0.0
```

#### 3. Tree-sitter Build Errors
```bash
# Install build tools
# Windows: Install Visual Studio Build Tools
# Linux: sudo apt-get install build-essential
# macOS: xcode-select --install
```

#### 4. Out of Memory (OOM)
- Reduce batch size in configuration
- Use smaller models (e.g., all-miniLM-l6 instead of jina-code-1.5b)
- Enable gradient checkpointing
- Use CPU fallback mode

## Environment Setup

### Kaggle
```python
# Kaggle notebook cells
!pip install -q -r requirements_v5.txt
```

### Local Development
```bash
# Create virtual environment
python -m venv venv_v5
source venv_v5/bin/activate  # Linux/Mac
# venv_v5\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements_v5.txt
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_v5.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_v5.txt

# Copy application
COPY . .

CMD ["python", "scripts/chunk_docs_v5.py"]
```

## Next Steps

After successful installation:
1. Review [`V5_MODEL_CONFIGURATIONS.md`](notes/V5_MODEL_CONFIGURATIONS.md) for model options
2. Check [`V5_CHUNKER_EMBEDDER_PLAN.md`](notes/V5_CHUNKER_EMBEDDER_PLAN.md) for architecture
3. Run example scripts in `scripts/` directory
4. See [`V5_CHUNKER_EMBEDDER_INTEGRATION.md`](notes/V5_CHUNKER_EMBEDDER_INTEGRATION.md) for usage

## Support

For issues or questions:
- Check documentation in `notes/` directory
- Review error logs in `/kaggle/working/embedding_process.log` (Kaggle)
- Verify GPU availability with `torch.cuda.is_available()`