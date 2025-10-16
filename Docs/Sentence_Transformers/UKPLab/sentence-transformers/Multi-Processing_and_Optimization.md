This page covers performance optimization techniques available in sentence-transformers, including multi-processing for distributed encoding, backend optimization with ONNX and OpenVINO, quantization strategies, and hardware acceleration. These optimization methods can significantly improve inference speed and reduce memory usage when working with large datasets or resource-constrained environments.

For general model usage and basic inference, see the quickstart guide in [2.1](#2.1). For training optimization techniques, see [3.7](#3.7).

## Multi-Processing Architecture

The sentence-transformers library provides built-in multi-processing capabilities that allow distributing encoding tasks across multiple devices or CPU processes. This is particularly useful when processing large datasets or when multiple GPUs are available.

```mermaid
graph TD
    MainProcess["Main Process<br/>SentenceTransformer"] --> ProcessPool["Multi-Process Pool<br/>start_multi_process_pool()"]
    ProcessPool --> Worker1["Worker Process 1<br/>Device: cuda:0"]
    ProcessPool --> Worker2["Worker Process 2<br/>Device: cuda:1"] 
    ProcessPool --> Worker3["Worker Process 3<br/>Device: cpu"]
    
    MainProcess --> ChunkDistribution["Data Chunking<br/>chunk_size parameter"]
    ChunkDistribution --> Worker1
    ChunkDistribution --> Worker2
    ChunkDistribution --> Worker3
    
    Worker1 --> Results1["Partial Results 1"]
    Worker2 --> Results2["Partial Results 2"]
    Worker3 --> Results3["Partial Results 3"]
    
    Results1 --> Aggregation["Result Aggregation<br/>_encode_multi_process()"]
    Results2 --> Aggregation
    Results3 --> Aggregation
    
    Aggregation --> FinalOutput["Final Embeddings<br/>numpy.ndarray or torch.Tensor"]
```

**Sources:** [sentence_transformers/SentenceTransformer.py:1046-1158](), [tests/test_multi_process.py:14-42]()

### Pool Management

Multi-processing pools are managed through dedicated methods that handle worker process lifecycle:

| Method | Purpose | Returns |
|--------|---------|---------|
| `start_multi_process_pool(target_devices)` | Creates worker processes for specified devices | Pool dictionary |
| `stop_multi_process_pool(pool)` | Terminates worker processes and cleanup | None |
| `encode(..., pool=pool)` | Uses existing pool for encoding | Embeddings |
| `encode(..., device=["cuda:0", "cuda:1"])` | Auto-creates temporary pool | Embeddings |

**Sources:** [sentence_transformers/SentenceTransformer.py:1915-1970](), [tests/test_multi_process.py:61-81]()

### Distributed Encoding Process

```mermaid
sequenceDiagram
    participant Client as "Client Code"
    participant ST as "SentenceTransformer"
    participant Pool as "Process Pool"
    participant W1 as "Worker 1"
    participant W2 as "Worker 2"
    
    Client->>ST: encode(sentences, device=["cuda:0", "cuda:1"])
    ST->>ST: _encode_multi_process()
    ST->>Pool: Create temporary pool
    Pool->>W1: Initialize on cuda:0
    Pool->>W2: Initialize on cuda:1
    
    ST->>ST: Split sentences into chunks
    ST->>W1: Send chunk 1
    ST->>W2: Send chunk 2
    
    W1->>W1: Process batch
    W2->>W2: Process batch
    
    W1->>ST: Return embeddings 1
    W2->>ST: Return embeddings 2
    
    ST->>ST: Concatenate results
    ST->>Pool: Cleanup processes
    ST->>Client: Return final embeddings
```

**Sources:** [sentence_transformers/SentenceTransformer.py:1077-1158](), [sentence_transformers/sparse_encoder/SparseEncoder.py:514-532]()

## Backend Optimization

Sentence-transformers supports multiple inference backends beyond PyTorch, enabling significant performance improvements for production deployments.

### Backend Architecture

```mermaid
graph LR
    Model["Model Loading"] --> BackendChoice{"Backend Selection"}
    
    BackendChoice -->|"backend='torch'"| PyTorchBackend["PyTorch Backend<br/>AutoModel.from_pretrained()"]
    BackendChoice -->|"backend='onnx'"| ONNXBackend["ONNX Backend<br/>load_onnx_model()"]
    BackendChoice -->|"backend='openvino'"| OpenVINOBackend["OpenVINO Backend<br/>load_openvino_model()"]
    
    PyTorchBackend --> PyTorchInference["PyTorch Inference<br/>model(**features)"]
    ONNXBackend --> ONNXInference["ONNX Runtime<br/>session.run()"]
    OpenVINOBackend --> OpenVINOInference["OpenVINO Runtime<br/>compiled_model()"]
    
    PyTorchInference --> Output["Embeddings Output"]
    ONNXInference --> Output
    OpenVINOInference --> Output
```

**Sources:** [sentence_transformers/models/Transformer.py:173-203](), [sentence_transformers/cross_encoder/CrossEncoder.py:236-257]()

### Backend Configuration

Each model type supports backend selection through the `backend` parameter:

| Model Type | Backend Support | Configuration |
|------------|----------------|---------------|
| `SentenceTransformer` | torch, onnx, openvino | `SentenceTransformer(model_name, backend="onnx")` |
| `SparseEncoder` | torch, onnx, openvino | `SparseEncoder(model_name, backend="openvino")` |
| `CrossEncoder` | torch, onnx, openvino | `CrossEncoder(model_name, backend="torch")` |

**Sources:** [sentence_transformers/SentenceTransformer.py:186](), [sentence_transformers/sparse_encoder/SparseEncoder.py:151](), [sentence_transformers/cross_encoder/CrossEncoder.py:135]()

### Backend-Specific Parameters

Additional configuration options are available through `model_kwargs`:

```python
# ONNX provider selection
model = SentenceTransformer(
    "model-name", 
    backend="onnx",
    model_kwargs={"provider": "CUDAExecutionProvider"}
)

# Optimized model file selection
model = SentenceTransformer(
    "model-name",
    backend="openvino", 
    model_kwargs={"file_name": "model_optimized.xml"}
)

# Auto-export control
model = SentenceTransformer(
    "model-name",
    backend="onnx",
    model_kwargs={"export": True}
)
```

**Sources:** [sentence_transformers/SentenceTransformer.py:113-119](), [sentence_transformers/backend.py]()

## Quantization and Precision

The library provides multiple quantization strategies to reduce memory usage and improve inference speed with minimal accuracy loss.

### Quantization Pipeline

```mermaid
graph TD
    FloatEmbeddings["Float32 Embeddings<br/>model.encode()"] --> QuantizationChoice{"Precision Parameter"}
    
    QuantizationChoice -->|"precision='float32'"| Float32["Float32 Output<br/>No quantization"]
    QuantizationChoice -->|"precision='int8'"| Int8Quant["INT8 Quantization<br/>quantize_embeddings()"]
    QuantizationChoice -->|"precision='uint8'"| UInt8Quant["UINT8 Quantization<br/>quantize_embeddings()"]
    QuantizationChoice -->|"precision='binary'"| BinaryQuant["Binary Quantization<br/>quantize_embeddings()"]
    QuantizationChoice -->|"precision='ubinary'"| UBinaryQuant["Unsigned Binary<br/>quantize_embeddings()"]
    
    Int8Quant --> MemoryReduction["Memory Usage<br/>4x reduction"]
    UInt8Quant --> MemoryReduction
    BinaryQuant --> MemoryReduction2["Memory Usage<br/>32x reduction"]
    UBinaryQuant --> MemoryReduction2
```

**Sources:** [sentence_transformers/SentenceTransformer.py:424](), [sentence_transformers/quantization.py]()

### Precision Performance Characteristics

| Precision | Memory Factor | Speed Factor | Use Case |
|-----------|---------------|--------------|----------|
| `float32` | 1x | 1x | Highest accuracy |
| `int8` | 4x smaller | ~2x faster | Balanced accuracy/speed |
| `uint8` | 4x smaller | ~2x faster | Positive-only embeddings |
| `binary` | 32x smaller | ~10x faster | Similarity search |
| `ubinary` | 32x smaller | ~10x faster | Unsigned binary encoding |

**Sources:** [sentence_transformers/quantization.py:15-142](), [sentence_transformers/SentenceTransformer.py:469-473]()

## Hardware Acceleration

### Device Management

The library automatically detects and utilizes available hardware acceleration:

```mermaid
graph TD
    DeviceDetection["Device Detection<br/>get_device_name()"] --> AvailableCheck{"Hardware Available?"}
    
    AvailableCheck -->|"torch.cuda.is_available()"| CUDA["CUDA Devices<br/>cuda:0, cuda:1, ..."]
    AvailableCheck -->|"torch.backends.mps.is_available()"| MPS["Apple MPS<br/>mps device"]
    AvailableCheck -->|"is_torch_npu_available()"| NPU["Neural Processing Unit<br/>npu device"]
    AvailableCheck -->|"HPU available"| HPU["Habana HPU<br/>hpu device"]
    AvailableCheck -->|"Default"| CPU["CPU Fallback<br/>cpu device"]
    
    CUDA --> OptimumHabana["Optimum Habana<br/>adapt_transformers_to_gaudi()"]
    NPU --> OptimumHabana
    HPU --> OptimumHabana
```

**Sources:** [sentence_transformers/SentenceTransformer.py:217-224](), [sentence_transformers/util.py:47-77]()

### Mixed Precision Support

Hardware acceleration includes mixed precision training and inference:

| `torch_dtype` | Description | Memory Savings |
|---------------|-------------|----------------|
| `"auto"` | Use model's default dtype | Varies |
| `torch.float16` | Half precision | 50% reduction |
| `torch.bfloat16` | Brain floating point | 50% reduction |
| `torch.float32` | Full precision | Baseline |

**Sources:** [sentence_transformers/SentenceTransformer.py:95-106](), [tests/test_sentence_transformer.py:96-106]()

## Memory Optimization Strategies

### Efficient Encoding Parameters

Several parameters help optimize memory usage during encoding:

```mermaid
graph LR
    Input["Large Dataset"] --> BatchSize["batch_size<br/>Control memory per batch"]
    BatchSize --> ChunkSize["chunk_size<br/>Multi-process distribution"]
    ChunkSize --> TruncateDim["truncate_dim<br/>Matryoshka model truncation"]
    TruncateDim --> Precision["precision<br/>Quantization strategy"]
    Precision --> Output["Optimized Embeddings"]
    
    TruncateDim --> MatryoshkaNote["Matryoshka Models<br/>Maintain quality with<br/>reduced dimensions"]
```

**Sources:** [sentence_transformers/SentenceTransformer.py:485-491](), [sentence_transformers/util.py:436-455]()

### Sparse Encoding Optimization

For `SparseEncoder` models, additional memory optimizations are available:

| Parameter | Effect | Usage |
|-----------|--------|-------|
| `max_active_dims` | Limits non-zero dimensions | Reduce memory and computation |
| `convert_to_sparse_tensor` | Use sparse tensor format | Memory efficient storage |
| `save_to_cpu` | Move results to CPU | Free GPU memory |

**Sources:** [sentence_transformers/sparse_encoder/SparseEncoder.py:192](), [sentence_transformers/sparse_encoder/SparseEncoder.py:467-469]()

### Pooling Configuration for Memory

The `Pooling` module provides memory-efficient pooling strategies:

```mermaid
graph TD
    TokenEmbeddings["Token Embeddings<br/>[batch_size, seq_len, hidden_dim]"] --> PoolingChoice{"Pooling Strategy"}
    
    PoolingChoice -->|"pooling_mode='mean'"| MeanPool["Mean Pooling<br/>Average across sequence"]
    PoolingChoice -->|"pooling_mode='max'"| MaxPool["Max Pooling<br/>Maximum values"]
    PoolingChoice -->|"pooling_mode='cls'"| CLSPool["CLS Token<br/>First token only"]
    PoolingChoice -->|"pooling_mode='lasttoken'"| LastPool["Last Token<br/>Final valid token"]
    
    MeanPool --> SentenceEmbedding["Sentence Embedding<br/>[batch_size, hidden_dim]"]
    MaxPool --> SentenceEmbedding
    CLSPool --> SentenceEmbedding
    LastPool --> SentenceEmbedding
    
    SentenceEmbedding --> IncludePrompt{"include_prompt=False"}
    IncludePrompt --> PromptExclusion["Exclude prompt tokens<br/>from pooling calculation"]
```

**Sources:** [sentence_transformers/models/Pooling.py:135-241](), [sentence_transformers/models/Pooling.py:142-152]()