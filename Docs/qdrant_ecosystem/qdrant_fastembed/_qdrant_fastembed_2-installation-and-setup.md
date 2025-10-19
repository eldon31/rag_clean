Installation and Setup | qdrant/fastembed | DeepWiki

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

# Installation and Setup

Relevant source files

- [.github/workflows/python-tests.yml](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml)
- [.gitignore](https://github.com/qdrant/fastembed/blob/b785640b/.gitignore)
- [.pre-commit-config.yaml](https://github.com/qdrant/fastembed/blob/b785640b/.pre-commit-config.yaml)
- [LICENSE](https://github.com/qdrant/fastembed/blob/b785640b/LICENSE)
- [experiments/02\_SPLADE\_to\_ONNX.ipynb](https://github.com/qdrant/fastembed/blob/b785640b/experiments/02_SPLADE_to_ONNX.ipynb)
- [pyproject.toml](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml)

This page provides comprehensive instructions for installing and setting up FastEmbed, a high-performance embedding library. FastEmbed is designed for fast, light, and accurate embedding generation, with a focus on production environments. For an overview of the library's capabilities, see [Overview](qdrant/fastembed/1-overview.md).

## System Requirements

Before installing FastEmbed, ensure your system meets the following requirements:

| Requirement       | Details                                          |
| ----------------- | ------------------------------------------------ |
| Python Version    | Python 3.9 or newer                              |
| Operating Systems | Windows, macOS, Linux (all supported)            |
| Disk Space        | \~600MB (varies depending on models downloaded)  |
| RAM               | 1GB minimum (4GB+ recommended for larger models) |

Sources: [pyproject.toml13-14](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L13-L14)

## Installation Methods

### Using pip (Recommended)

The simplest way to install FastEmbed is using pip:

```
```

For specific versions:

```
```

### Using Poetry

If you use Poetry for dependency management:

```
```

### From Source

For the latest development version or to contribute:

```
```

Or with Poetry:

```
```

Sources: [pyproject.toml1-12](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L1-L12) [.github/workflows/python-tests.yml37-42](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml#L37-L42)

## Installation Flow

The following diagram illustrates the FastEmbed installation flow:

```
```

Sources: [pyproject.toml13-33](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L13-L33) [.github/workflows/python-tests.yml37-47](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml#L37-L47)

## Dependencies

FastEmbed automatically installs the following core dependencies:

| Dependency       | Purpose              | Version Requirement                |
| ---------------- | -------------------- | ---------------------------------- |
| numpy            | Numerical operations | ≥1.21 (varies by Python version)   |
| onnxruntime      | Model inference      | ≥1.17.0 (varies by Python version) |
| tokenizers       | Text tokenization    | ≥0.15,<1.0                         |
| huggingface-hub  | Model downloading    | ≥0.20,<1.0                         |
| tqdm             | Progress bars        | ^4.66                              |
| requests         | HTTP requests        | ^2.31                              |
| loguru           | Logging              | ^0.7.2                             |
| pillow           | Image processing     | ≥10.3.0,<12.0.0                    |
| mmh3             | Hash functions       | ≥4.1.0,<6.0.0                      |
| py-rust-stemmers | Text stemming        | ^0.1.0                             |

The version requirements ensure compatibility with different Python versions, including the latest 3.13.

Sources: [pyproject.toml15-33](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L15-L33)

## Dependency Architecture

```
```

Sources: [pyproject.toml15-33](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L15-L33)

## Verifying Installation

After installation, you can verify that FastEmbed is working correctly:

```
```

On first use, FastEmbed will automatically download the default model (typically `BAAI/bge-small-en-v1.5`). The model files are stored in a local cache directory.

## Model Cache Location

FastEmbed stores downloaded models in a local cache directory:

| Platform | Default Cache Location                                        |
| -------- | ------------------------------------------------------------- |
| Linux    | `~/.cache/fastembed`                                          |
| macOS    | `~/Library/Caches/fastembed`                                  |
| Windows  | `C:\Users\<username>\AppData\Local\fastembed\fastembed\Cache` |

You can override this location by setting the `FASTEMBED_CACHE_PATH` environment variable:

```
```

## Python Version Support

FastEmbed supports different Python versions with appropriate dependency configurations:

```
```

Sources: [pyproject.toml15-25](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L15-L25)

## Common Installation Issues

| Issue                                                       | Solution                                                 |
| ----------------------------------------------------------- | -------------------------------------------------------- |
| `ImportError: DLL load failed while importing _onnxruntime` | Ensure Visual C++ Redistributable is installed (Windows) |
| `ModuleNotFoundError: No module named 'fastembed'`          | Verify installation with `pip list \| grep fastembed`    |
| `Model download failed`                                     | Check internet connection and firewall settings          |
| Slow model downloads                                        | Configure HuggingFace token for faster downloads         |

## Using HuggingFace Authentication

For faster model downloads and access to gated models, configure a HuggingFace token:

```
```

## Next Steps

After successful installation, proceed to:

- [Core Embedding Classes](qdrant/fastembed/3-core-embedding-classes.md) to learn about the main embedding functionality
- [Usage Examples](qdrant/fastembed/7-usage-examples.md) for practical implementation examples
- [Performance Optimization](qdrant/fastembed/8-performance-optimization.md) to optimize for your specific use case

Sources: [pyproject.toml1-33](https://github.com/qdrant/fastembed/blob/b785640b/pyproject.toml#L1-L33) [.github/workflows/python-tests.yml37-47](https://github.com/qdrant/fastembed/blob/b785640b/.github/workflows/python-tests.yml#L37-L47)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Installation and Setup](#installation-and-setup.md)
- [System Requirements](#system-requirements.md)
- [Installation Methods](#installation-methods.md)
- [Using pip (Recommended)](#using-pip-recommended.md)
- [Using Poetry](#using-poetry.md)
- [From Source](#from-source.md)
- [Installation Flow](#installation-flow.md)
- [Dependencies](#dependencies.md)
- [Dependency Architecture](#dependency-architecture.md)
- [Verifying Installation](#verifying-installation.md)
- [Model Cache Location](#model-cache-location.md)
- [Python Version Support](#python-version-support.md)
- [Common Installation Issues](#common-installation-issues.md)
- [Using HuggingFace Authentication](#using-huggingface-authentication.md)
- [Next Steps](#next-steps.md)
