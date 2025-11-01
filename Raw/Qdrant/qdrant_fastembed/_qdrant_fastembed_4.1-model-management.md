Model Management | qdrant/fastembed | DeepWiki

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

# Model Management

Relevant source files

- [fastembed/common/\_\_init\_\_.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/__init__.py)
- [fastembed/common/model\_management.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py)
- [fastembed/common/types.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/types.py)
- [fastembed/common/utils.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/utils.py)
- [fastembed/text/text\_embedding\_base.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py)

This document explains how FastEmbed manages embedding models, including downloading, caching, and verification processes. Model Management is a core subsystem responsible for ensuring models are efficiently retrieved and stored locally for embedding generation. For information about the actual embedding process, see [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md).

## Overview

The Model Management subsystem provides a unified interface for:

- Downloading models from different sources (HuggingFace Hub, Google Cloud Storage)
- Caching models locally to avoid redundant downloads
- Verifying the integrity of downloaded models
- Supporting custom model registration

It serves as the foundation for all embedding classes in FastEmbed, enabling them to retrieve model files regardless of their source.

```
```

Sources: [fastembed/common/model\_management.py377-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L377-L458)

## Architecture

The Model Management system is designed as a generic base class that can handle different types of model descriptions. It integrates with the broader FastEmbed architecture as the foundation for embedding model access.

```
```

Sources: [fastembed/common/model\_management.py24-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L24-L458) [fastembed/text/text\_embedding\_base.py8-60](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py#L8-L60)

## Model Sources and Retrieval

FastEmbed supports retrieving models from multiple sources:

1. **HuggingFace Hub**: Primary source for many models, providing version control and metadata
2. **Google Cloud Storage**: Alternative source, especially for optimized ONNX models

The system intelligently chooses the appropriate source based on model description and availability.

```
```

Sources: [fastembed/common/model\_management.py377-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L377-L458)

### HuggingFace Download Process

When downloading from HuggingFace, FastEmbed follows these steps:

1. Check if files are already cached locally
2. Verify files against metadata if present
3. Download required files using `snapshot_download()`
4. Collect and store metadata for future verification

The system uses a pattern-based approach to download only necessary files, reducing download size and time.

```
```

Sources: [fastembed/common/model\_management.py132-288](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L132-L288)

### Google Cloud Storage Download Process

For models hosted on Google Cloud Storage:

1. Check if model is already cached locally
2. Download the compressed model archive
3. Decompress to temporary directory
4. Move to final cache location

This process handles compressed archives (`.tar.gz`) containing the ONNX model and supporting files.

Sources: [fastembed/common/model\_management.py327-375](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L327-L375) [fastembed/common/model\_management.py291-325](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L291-L325)

## Caching Mechanism

FastEmbed implements an efficient caching mechanism to avoid redundant downloads and improve performance.

### Cache Directory Structure

```
[CACHE_DIR]/
├── models--[ORGANIZATION]--[MODEL_NAME]/
│   ├── files_metadata.json
│   ├── model_file.onnx
│   ├── config.json
│   ├── tokenizer.json
│   └── ...
├── fast-[MODEL_NAME]/
│   ├── model_file.onnx
│   ├── config.json
│   └── ...
└── tmp/
    └── (temporary files during download)
```

The cache directory location is determined using the `define_cache_dir()` function, which checks:

1. The `cache_dir` parameter provided to the embedding class
2. The `FASTEMBED_CACHE_PATH` environment variable
3. A default location in the system temporary directory

Sources: [fastembed/common/utils.py48-59](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/utils.py#L48-L59) [fastembed/common/model\_management.py327-375](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L327-L375)

## Verification Process

To ensure model integrity, FastEmbed verifies downloaded files against metadata:

```
```

The verification process checks:

1. File existence
2. File sizes
3. Blob IDs (when online verification is possible)

This ensures that all model files are complete and uncorrupted.

Sources: [fastembed/common/model\_management.py152-202](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L152-L202)

## Model Description and Management

Models in FastEmbed are represented by description objects that inherit from `BaseModelDescription`:

```
```

These descriptions contain all necessary information to identify, download, and use a model, including:

- Model identifier
- Source locations (HuggingFace, GCS URL)
- File names
- Licensing information
- Size information

Sources: [fastembed/common/model\_management.py377-402](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L377-L402)

## Implementation Details

The `ModelManagement` class is implemented as a generic class parameterized by a type variable `T` that extends `BaseModelDescription`. This allows different embedding classes to use specialized model descriptions while sharing common functionality.

```
```

Key methods in `ModelManagement` include:

1. `download_model()`: Main entry point for retrieving models
2. `download_files_from_huggingface()`: Specialized for HuggingFace downloads
3. `retrieve_model_gcs()`: Specialized for Google Cloud Storage downloads
4. `_verify_files_from_metadata()`: Verifies downloaded files
5. `_collect_file_metadata()`: Collects metadata for verification

Each embedding class extends `ModelManagement` with specific type parameters and implementations of abstract methods like `_list_supported_models()`.

Sources: [fastembed/common/model\_management.py24-67](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L24-L67) [fastembed/text/text\_embedding\_base.py8-19](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/text/text_embedding_base.py#L8-L19)

## Error Handling and Retry Mechanism

FastEmbed implements a robust retry mechanism for model downloads:

1. First tries HuggingFace if available
2. Falls back to Google Cloud Storage if HuggingFace fails
3. Implements exponential backoff between retries
4. Provides detailed error messages for troubleshooting

This ensures maximum availability even in case of temporary issues with one source.

Sources: [fastembed/common/model\_management.py412-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L412-L458)

## Summary

The Model Management system in FastEmbed provides a comprehensive solution for handling embedding models through their lifecycle:

1. **Model Retrieval**: Downloads models from multiple sources
2. **Caching**: Stores models locally to improve performance
3. **Verification**: Ensures model integrity
4. **Abstraction**: Provides a unified interface for all embedding types

This system is a key component that enables FastEmbed to offer high-performance embeddings while maintaining a simple, user-friendly API.

Sources: [fastembed/common/model\_management.py24-458](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/common/model_management.py#L24-L458)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Model Management](#model-management.md)
- [Overview](#overview.md)
- [Architecture](#architecture.md)
- [Model Sources and Retrieval](#model-sources-and-retrieval.md)
- [HuggingFace Download Process](#huggingface-download-process.md)
- [Google Cloud Storage Download Process](#google-cloud-storage-download-process.md)
- [Caching Mechanism](#caching-mechanism.md)
- [Cache Directory Structure](#cache-directory-structure.md)
- [Verification Process](#verification-process.md)
- [Model Description and Management](#model-description-and-management.md)
- [Implementation Details](#implementation-details.md)
- [Error Handling and Retry Mechanism](#error-handling-and-retry-mechanism.md)
- [Summary](#summary.md)
