Parallel Processing | qdrant/fastembed | DeepWiki

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

# Parallel Processing

Relevant source files

- [fastembed/common/onnx\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py)
- [fastembed/parallel\_processor.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py)
- [fastembed/rerank/cross\_encoder/onnx\_text\_model.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py)
- [fastembed/text/onnx\_embedding.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py)

FastEmbed provides a robust parallel processing system that enables efficient generation of embeddings for large datasets by distributing workloads across multiple CPU cores or GPU devices. This system significantly improves throughput when processing large batches of documents or images.

For information about the general architecture of FastEmbed, see [Architecture](qdrant/fastembed/4-architecture.md), and for details on ONNX integration, see [ONNX Runtime Integration](qdrant/fastembed/4.2-onnx-runtime-integration.md).

## Parallel Processing Architecture

FastEmbed's parallel processing is implemented through a worker pool architecture that manages multiple processes, each running its own instance of an embedding model. The core of this system is the `ParallelWorkerPool` class, which handles process creation, workload distribution, and result collection.

```
```

Sources: [fastembed/parallel\_processor.py91-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L91-L253) [fastembed/text/onnx\_embedding.py260-292](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L260-L292)

## Worker Interface and Implementation

The parallel processing system defines a `Worker` interface that all worker implementations must adhere to. Each embedding type in FastEmbed has its own worker implementation that handles the specific requirements for that type of embedding.

```
```

Sources: [fastembed/parallel\_processor.py26-32](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L26-L32) [fastembed/common/onnx\_model.py114-136](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/onnx_model.py#L114-L136) [fastembed/text/onnx\_embedding.py328-340](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L328-L340) [fastembed/rerank/cross\_encoder/onnx\_text\_model.py148-169](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L148-L169)

## Parallel Processing Flow

When parallel processing is enabled, the following sequence of operations occurs:

```
```

The system uses two queues to manage this workflow:

1. **Input Queue**: Sends batches of documents to worker processes
2. **Output Queue**: Receives processed embeddings from worker processes

The `ParallelWorkerPool` class provides two mapping methods:

- `semi_ordered_map()`: Returns results as soon as they are available (potentially out of order)
- `ordered_map()`: Ensures results are returned in the same order as inputs

Sources: [fastembed/parallel\_processor.py142-209](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L142-L209)

## Enabling Parallel Processing

To utilize parallel processing in FastEmbed, you can set the `parallel` parameter when calling the `embed()` method:

```
```

The `parallel` parameter accepts the following values:

- `None`: Disable parallel processing (default)
- `0`: Use all available CPU cores
- `n` (where n > 0): Use n worker processes

This parameter is available in all embedding classes in FastEmbed, including `TextEmbedding`, `SparseTextEmbedding`, `LateInteractionTextEmbedding`, `ImageEmbedding`, and `TextCrossEncoder`.

Sources: [fastembed/text/onnx\_embedding.py260-292](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L260-L292)

## GPU Support and Device Assignment

FastEmbed's parallel processing system includes robust GPU support, allowing distribution of worker processes across multiple GPUs:

```
```

To utilize GPU acceleration with parallel processing, you can configure the embedding model as follows:

```
```

In this configuration:

- The `cuda=True` parameter enables GPU acceleration
- The `device_ids=[0, 1]` parameter specifies which GPUs to use
- The `parallel=4` parameter creates 4 worker processes
- Worker processes are assigned to GPUs in a round-robin fashion

Sources: [fastembed/parallel\_processor.py120-126](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L120-L126) [fastembed/text/onnx\_embedding.py200-246](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L200-L246)

## Implementation Details

### Worker Process Management

The `ParallelWorkerPool` class manages worker processes through several key methods:

1. `start()`: Initializes worker processes and communication queues
2. `ordered_map()`: Maps input items to worker processes and returns results in order
3. `semi_ordered_map()`: Similar to `ordered_map()` but may return results out of order
4. `check_worker_health()`: Monitors worker processes for failures
5. `join_or_terminate()`: Handles emergency shutdown of worker processes
6. `join()`: Waits for all worker processes to complete

The system includes robust error handling to detect and manage failures in worker processes, including timeouts for detecting hanging processes.

Sources: [fastembed/parallel\_processor.py92-253](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L92-L253)

### Worker Communication

Communication between the main process and worker processes occurs through multiprocessing queues:

| Component     | Purpose                                                                       |
| ------------- | ----------------------------------------------------------------------------- |
| Input Queue   | Sends batches of documents to worker processes                                |
| Output Queue  | Receives processed embeddings from worker processes                           |
| Queue Signals | Special markers like `stop`, `confirm`, and `error` that control process flow |

The system uses a producer-consumer pattern where the main process produces items for the input queue and consumes results from the output queue, while worker processes do the opposite.

Sources: [fastembed/parallel\_processor.py20-24](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L20-L24) [fastembed/parallel\_processor.py35-89](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L35-L89)

### Worker Process Creation

When creating worker processes, FastEmbed handles several important considerations:

1. **Start Method**: Uses `forkserver` (if available) or `spawn` to create new processes
2. **Device Assignment**: Assigns GPU devices to workers in a round-robin fashion
3. **Model Loading**: Each worker loads its own instance of the model
4. **Synchronization**: Uses a shared counter to track active workers

This approach ensures that each worker process has its own isolated environment with access to the necessary resources.

Sources: [fastembed/rerank/cross\_encoder/onnx\_text\_model.py117-118](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/rerank/cross_encoder/onnx_text_model.py#L117-L118) [fastembed/parallel\_processor.py92-110](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/parallel_processor.py#L92-L110)

## Performance Considerations

When using parallel processing in FastEmbed, consider the following factors to optimize performance:

- **Number of Workers**: Start with a number equal to your CPU cores or GPU count and adjust based on performance
- **Batch Size**: Larger batch sizes typically improve throughput but increase memory usage
- **GPU Memory**: Each worker loads a separate model instance, so ensure your GPUs have sufficient memory
- **Process Creation Overhead**: There's an initial overhead to creating worker processes, so parallel processing is most beneficial for larger datasets
- **Lazy Loading**: Consider using `lazy_load=True` when creating models with parallel processing to avoid loading the model multiple times

Table of performance impacts:

| Configuration        | Best For                                     | Considerations                         |
| -------------------- | -------------------------------------------- | -------------------------------------- |
| Single Process       | Small datasets, low latency requirements     | Limited throughput                     |
| Multiple CPU Workers | Medium-sized datasets, no GPU available      | Higher throughput, increased CPU usage |
| Multiple GPU Workers | Large datasets, high throughput requirements | Highest performance, requires GPU(s)   |

Sources: [fastembed/text/onnx\_embedding.py199-257](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/onnx_embedding.py#L199-L257)

## Conclusion

FastEmbed's parallel processing system provides a powerful mechanism for scaling embedding generation across multiple CPU cores or GPU devices. By distributing workloads and managing worker processes effectively, it achieves significant performance improvements for large datasets while maintaining a simple, consistent API.

For information on model management and caching, see [Model Management](qdrant/fastembed/4.1-model-management.md), or for details on how to use specific embedding types, refer to [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Parallel Processing](#parallel-processing.md)
- [Parallel Processing Architecture](#parallel-processing-architecture.md)
- [Worker Interface and Implementation](#worker-interface-and-implementation.md)
- [Parallel Processing Flow](#parallel-processing-flow.md)
- [Enabling Parallel Processing](#enabling-parallel-processing.md)
- [GPU Support and Device Assignment](#gpu-support-and-device-assignment.md)
- [Implementation Details](#implementation-details.md)
- [Worker Process Management](#worker-process-management.md)
- [Worker Communication](#worker-communication.md)
- [Worker Process Creation](#worker-process-creation.md)
- [Performance Considerations](#performance-considerations.md)
- [Conclusion](#conclusion.md)
