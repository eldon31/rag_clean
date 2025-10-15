Performance Optimization | qdrant/fastembed | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/fastembed](https://github.com/qdrant/fastembed "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 20 April 2025 ([b78564](https://github.com/qdrant/fastembed/commits/b785640b))

- [Overview](qdrant/fastembed/1-overview.md)
- [Installation and Setup](qdrant/fastembed/2-installation-and-setup.md)
- [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md)
- [TextEmbedding](qdrant/fastembed/3.1-textembedding.md)
- [SparseTextEmbedding](qdrant/fastembed/3.2-sparsetextembedding.md)
- [LateInteractionTextEmbedding](qdrant/fastembed/3.3-lateinteractiontextembedding.md)
- [ImageEmbedding](qdrant/fastembed/3.4-imageembedding.md)
- [LateInteractionMultimodalEmbedding](qdrant/fastembed/3.5-lateinteractionmultimodalembedding.md)
- [TextCrossEncoder](qdrant/fastembed/3.6-textcrossencoder.md)
- [Architecture](qdrant/fastembed/4-architecture.md)
- [Model Management](qdrant/fastembed/4.1-model-management.md)
- [ONNX Runtime Integration](qdrant/fastembed/4.2-onnx-runtime-integration.md)
- [Parallel Processing](qdrant/fastembed/4.3-parallel-processing.md)
- [Implementation Details](qdrant/fastembed/5-implementation-details.md)
- [Dense Text Embeddings](qdrant/fastembed/5.1-dense-text-embeddings.md)
- [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md)
- [Late Interaction Models](qdrant/fastembed/5.3-late-interaction-models.md)
- [Multimodal Models](qdrant/fastembed/5.4-multimodal-models.md)
- [Supported Models](qdrant/fastembed/6-supported-models.md)
- [Usage Examples](qdrant/fastembed/7-usage-examples.md)
- [Basic Text Embedding](qdrant/fastembed/7.1-basic-text-embedding.md)
- [Sparse and Hybrid Search](qdrant/fastembed/7.2-sparse-and-hybrid-search.md)
- [ColBERT and Late Interaction](qdrant/fastembed/7.3-colbert-and-late-interaction.md)
- [Image Embedding](qdrant/fastembed/7.4-image-embedding.md)
- [Performance Optimization](qdrant/fastembed/8-performance-optimization.md)
- [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md)
- [Development Guide](qdrant/fastembed/10-development-guide.md)

Menu

# Performance Optimization

Relevant source files

- [docs/examples/ColBERT\_with\_FastEmbed.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb)
- [docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_vs_HF_Comparison.ipynb)
- [docs/examples/Hybrid\_Search.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb)
- [docs/qdrant/Retrieval\_with\_FastEmbed.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/docs/qdrant/Retrieval_with_FastEmbed.ipynb)
- [fastembed/text/onnx\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py)

FastEmbed is designed for high performance and efficient embedding generation. This page covers the various optimization techniques implemented in the library and how to configure them to maximize performance for your specific use case.

For information about the overall architecture of FastEmbed, see [Architecture](qdrant/fastembed/4-architecture.md). For detailed information about ONNX Runtime integration, see [ONNX Runtime Integration](qdrant/fastembed/4.2-onnx-runtime-integration.md). For specific information about parallel processing implementation, see [Parallel Processing](qdrant/fastembed/4.3-parallel-processing.md).

## Key Performance Features

FastEmbed incorporates several key performance optimization techniques that allow it to generate embeddings significantly faster than traditional embedding methods:

1. **ONNX Runtime Integration**: Accelerated inference through ONNX optimization
2. **Parallel Processing**: Multi-core utilization for faster embedding generation
3. **Lazy Loading**: Efficient memory management for multiple models
4. **Batch Processing**: Optimized throughput through batched operations
5. **Hardware Acceleration**: Support for both CPU and GPU (CUDA) execution
6. **Model Caching**: Efficient model storage and retrieval

```
```

Sources: [fastembed/text/onnx\_embedding.py198-229](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L198-L229)

## ONNX Runtime Integration

FastEmbed uses ONNX Runtime as its inference engine, which provides significant performance improvements over traditional PyTorch or TensorFlow implementations. ONNX (Open Neural Network Exchange) is an open standard for machine learning model representation that enables model interoperability between different frameworks.

### Benefits of ONNX Runtime

- **Optimized inference**: ONNX Runtime includes various optimizations specific to the hardware and platform
- **Reduced memory usage**: More efficient memory management compared to PyTorch/TensorFlow
- **Cross-platform compatibility**: Same model works across different environments

### Configuration Options

When initializing an embedding model, you can configure ONNX Runtime execution parameters:

```
```

Sources: [fastembed/text/onnx\_embedding.py199-246](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L199-L246)

## Parallel Processing

FastEmbed implements data-parallel processing to distribute embedding workloads across multiple CPU cores or GPU devices, enabling significant speedups for large dataset processing.

### How Parallel Processing Works in FastEmbed

```
```

### Configuring Parallel Processing

When calling the `embed()` method, you can specify the level of parallelism:

```
```

The `parallel` parameter accepts:

- A positive integer: Use the specified number of workers
- 0: Use all available cores
- None: Don't use data parallel processing (use default ONNX Runtime threading)

Performance benchmarks from example notebooks demonstrate significant speedups using parallel processing:

| Processing Mode | User Time | System Time | Wall Clock Time | Speedup |
| --------------- | --------- | ----------- | --------------- | ------- |
| Sequential      | 16min 23s | 31.7s       | 3min            | 1x      |
| Parallel        | 6min 19s  | 22s         | 1min 37s        | \~2x    |

Sources: [docs/examples/Hybrid\_Search.ipynb726-739](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb#L726-L739)

## Lazy Loading

Lazy loading allows you to instantiate models without immediately loading their weights into memory, which can be useful when working with multiple models or in resource-constrained environments.

### How to Enable Lazy Loading

```
```

When lazy loading is enabled, the model weights are only loaded when the first embedding request is made, reducing initial memory usage and startup time.

Sources: [fastembed/text/onnx\_embedding.py221-222](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L221-L222) [fastembed/text/onnx\_embedding.py255-258](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L255-L258)

## Batch Processing

FastEmbed optimizes throughput by processing inputs in batches, which enables more efficient hardware utilization and minimizes overhead.

### Configuring Batch Size

You can adjust the batch size when calling the `embed()` method:

```
```

Optimal batch size depends on:

- Available memory
- Input document length
- Model size
- Hardware characteristics

For large datasets, combining batch processing with parallel processing can provide the best performance.

Sources: [fastembed/text/onnx\_embedding.py260-292](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L260-L292)

## Hardware Acceleration

FastEmbed supports both CPU and GPU execution, allowing you to leverage available hardware for maximum performance.

### CPU Optimization

When running on CPU, you can specify the number of threads to use:

```
```

### GPU Acceleration

To use GPU acceleration (if available):

```
```

When using multiple GPUs with `device_ids`, FastEmbed will automatically distribute the workload across the specified devices when parallel processing is enabled.

Sources: [fastembed/text/onnx\_embedding.py202-246](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L202-L246)

## Performance Comparison

FastEmbed significantly outperforms traditional embedding libraries by combining ONNX optimization with efficient parallel processing.

```
```

### Benchmark Results

From comparing FastEmbed vs. Hugging Face Transformers (using the same BGE-small-en-v1.5 model):

| Library                   | Avg Processing Time | Chars/Second | Relative Performance |
| ------------------------- | ------------------- | ------------ | -------------------- |
| Hugging Face Transformers | 0.047s              | \~811        | 1x (baseline)        |
| FastEmbed                 | 0.044s              | \~871        | \~1.07x faster       |

For large datasets, the performance gap widens significantly due to parallel processing capabilities:

| Dataset Size  | Traditional Library | FastEmbed | Speedup |
| ------------- | ------------------- | --------- | ------- |
| Small (10s)   | 1x                  | 1-2x      | 1-2x    |
| Medium (100s) | 1x                  | 2-3x      | 2-3x    |
| Large (1000s) | 1x                  | 3-5x      | 3-5x    |

Sources: [docs/examples/FastEmbed\_vs\_HF\_Comparison.ipynb245-278](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/FastEmbed_vs_HF_Comparison.ipynb#L245-L278)

## Advanced Configuration Parameters

The following table summarizes the key parameters that affect performance:

| Parameter    | Description                                        | Default | When to Modify                                     |
| ------------ | -------------------------------------------------- | ------- | -------------------------------------------------- |
| `threads`    | Number of threads for ONNX session                 | `None`  | When you want to control CPU thread usage          |
| `providers`  | ONNX Runtime providers                             | `None`  | For custom execution providers                     |
| `cuda`       | Enable CUDA for GPU acceleration                   | `False` | When GPU is available                              |
| `device_ids` | GPU device IDs for data parallel processing        | `None`  | When using multiple GPUs                           |
| `lazy_load`  | Load model on demand rather than at initialization | `False` | When working with multiple models                  |
| `batch_size` | Number of documents processed per batch            | `256`   | Adjust based on available memory and document size |
| `parallel`   | Number of worker processes for parallel processing | `None`  | Set to >1 or 0 for large datasets                  |

Sources: [fastembed/text/onnx\_embedding.py199-246](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L199-L246) [fastembed/text/onnx\_embedding.py260-292](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L260-L292)

## Best Practices for Performance Optimization

### Model Selection

- Smaller models (like BGE-small) are faster but may be less accurate
- Larger models provide better quality but require more resources
- Select the smallest model that meets your quality requirements

### Processing Configuration

1. **Enable parallel processing for large datasets**

   ```
   ```

2. **Optimize batch size**

   ```
   ```

3. **Use GPU acceleration when available**

   ```
   ```

4. **Combine strategies for maximum performance**

   ```
   ```

### Performance Debugging

If you encounter performance issues:

1. Try reducing batch size if you're running out of memory
2. Reduce the number of parallel workers if you experience excessive CPU/GPU contention
3. Try a smaller model if speed is more important than quality
4. Enable lazy loading if working with multiple models to manage memory more efficiently

Sources: [fastembed/text/onnx\_embedding.py260-292](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L260-L292) [docs/examples/Hybrid\_Search.ipynb726-739](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/Hybrid_Search.ipynb#L726-L739)

## Late Interaction Models and Performance

Late interaction models like ColBERT require special consideration for performance optimization:

```
```

Due to their computational requirements, consider using late interaction models like ColBERT in a two-stage pipeline:

1. **First stage**: Use a faster dense embedding model to retrieve candidate documents (100-500)
2. **Second stage**: Use the more resource-intensive late interaction model to rerank results for higher precision

This approach balances speed and accuracy, leveraging the strengths of both approaches.

Sources: [docs/examples/ColBERT\_with\_FastEmbed.ipynb373-398](https://github.com/qdrant/fastembed/blob/b785640b/docs/examples/ColBERT_with_FastEmbed.ipynb#L373-L398)

## Summary

FastEmbed offers multiple performance optimization techniques that can be combined to achieve significant speedups in embedding generation. By choosing the right configuration for your specific use case, you can achieve optimal performance while maintaining high-quality embeddings.

For most cases, enabling parallel processing (`parallel=0`) with an appropriate batch size and GPU acceleration (if available) will provide the best balance of performance and resource utilization.

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Performance Optimization](#performance-optimization.md)
- [Key Performance Features](#key-performance-features.md)
- [ONNX Runtime Integration](#onnx-runtime-integration.md)
- [Benefits of ONNX Runtime](#benefits-of-onnx-runtime.md)
- [Configuration Options](#configuration-options.md)
- [Parallel Processing](#parallel-processing.md)
- [How Parallel Processing Works in FastEmbed](#how-parallel-processing-works-in-fastembed.md)
- [Configuring Parallel Processing](#configuring-parallel-processing.md)
- [Lazy Loading](#lazy-loading.md)
- [How to Enable Lazy Loading](#how-to-enable-lazy-loading.md)
- [Batch Processing](#batch-processing.md)
- [Configuring Batch Size](#configuring-batch-size.md)
- [Hardware Acceleration](#hardware-acceleration.md)
- [CPU Optimization](#cpu-optimization.md)
- [GPU Acceleration](#gpu-acceleration.md)
- [Performance Comparison](#performance-comparison.md)
- [Benchmark Results](#benchmark-results.md)
- [Advanced Configuration Parameters](#advanced-configuration-parameters.md)
- [Best Practices for Performance Optimization](#best-practices-for-performance-optimization.md)
- [Model Selection](#model-selection.md)
- [Processing Configuration](#processing-configuration.md)
- [Performance Debugging](#performance-debugging.md)
- [Late Interaction Models and Performance](#late-interaction-models-and-performance.md)
- [Summary](#summary.md)
