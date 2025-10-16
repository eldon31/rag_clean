ColBERT and Late Interaction | qdrant/fastembed | DeepWiki

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

# ColBERT and Late Interaction

Relevant source files

- [fastembed/late\_interaction/colbert.py](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py)

This page explains how to use FastEmbed's implementation of ColBERT for late interaction embeddings. Late interaction is a retrieval approach that defers token-to-token interaction between queries and documents until the final ranking stage, offering improved precision compared to traditional dense embeddings. For information about other embedding approaches, see [Dense Text Embeddings](qdrant/fastembed/5.1-dense-text-embeddings.md) or [Sparse Text Embeddings](qdrant/fastembed/5.2-sparse-text-embeddings.md).

## What is ColBERT and Late Interaction?

ColBERT (Contextualized Late Interaction over BERT) is a retrieval model architecture that represents documents and queries as bags of contextualized embeddings rather than single vector representations. Unlike dense text embeddings that compress entire texts into single vectors, ColBERT preserves token-level information by:

1. Embedding each token in a document or query separately
2. Performing "late interaction" by computing fine-grained similarity between tokens only at retrieval time

This approach provides higher precision because it retains more context and semantic information, making it particularly effective for complex information retrieval tasks.

```
```

Sources: [fastembed/late\_interaction/colbert.py39-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L65)

## ColBERT in FastEmbed Architecture

FastEmbed implements ColBERT through the `LateInteractionTextEmbedding` entry point class, which uses the `Colbert` implementation class. This fits into the larger FastEmbed architecture as follows:

```
```

Sources: [fastembed/late\_interaction/colbert.py39-40](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L39-L40)

## Supported Models

FastEmbed currently supports these ColBERT models:

| Model Name                            | Dimensions | Description                                                       | License    | Size (GB) |
| ------------------------------------- | ---------- | ----------------------------------------------------------------- | ---------- | --------- |
| colbert-ir/colbertv2.0                | 128        | Late interaction model                                            | MIT        | 0.44      |
| answerdotai/answerai-colbert-small-v1 | 96         | Text embeddings, Multilingual (\~100 languages), 512 input tokens | Apache 2.0 | 0.13      |

Sources: [fastembed/late\_interaction/colbert.py17-36](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L17-L36)

## Using ColBERT in FastEmbed

### Basic Usage

Here's how to use ColBERT for late interaction embeddings:

```
```

The key difference between ColBERT and standard dense embeddings is that:

- Documents are embedded at indexing time
- Queries are embedded at search time
- The two never interact until the final similarity calculation

### ColBERT Embedding Process

```
```

Sources: [fastembed/late\_interaction/colbert.py67-104](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L67-L104) [fastembed/late\_interaction/colbert.py205-249](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L205-L249)

## Implementation Details

### Special Token Handling

ColBERT uses different marker tokens for queries and documents to help the model distinguish their roles:

- `QUERY_MARKER_TOKEN_ID = 1` - Added to queries
- `DOCUMENT_MARKER_TOKEN_ID = 2` - Added to documents

For queries, ColBERT also pads shorter queries with mask tokens up to a minimum length (31 tokens) to improve retrieval performance through query augmentation.

Sources: [fastembed/late\_interaction/colbert.py40-43](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L40-L43) [fastembed/late\_interaction/colbert.py86-104](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L86-L104)

### Document Embedding Post-Processing

A key aspect of ColBERT is how document embeddings are post-processed:

1. Punctuation and padding tokens are masked out (attention mask set to 0)
2. The attention mask is applied to the model output
3. Token embeddings are normalized to unit length

```
```

Sources: [fastembed/late\_interaction/colbert.py45-65](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L45-L65)

### Tokenization Process

The tokenization process differs between queries and documents:

1. **Documents**: Standard tokenization with truncation
2. **Queries**: Tokenized and padded with `[MASK]` tokens to a minimum length

The tokenizer also handles special considerations like truncation to avoid overflow after adding marker tokens.

Sources: [fastembed/late\_interaction/colbert.py79-108](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L79-L108) [fastembed/late\_interaction/colbert.py195-203](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L195-L203)

## Performance Considerations

The ColBERT approach offers higher precision but comes with trade-offs:

1. **Storage**: Requires more storage than dense embeddings (token-level vs. single vector)
2. **Computation**: Late interaction calculation is more computationally intensive at search time
3. **Memory**: Uses more memory during search due to token-level operations

For optimal performance, FastEmbed implements ColBERT using ONNX Runtime for efficient inference and supports parallel processing for batch embedding.

Sources: [fastembed/late\_interaction/colbert.py205-237](https://github.com/qdrant/fastembed/blob/b785640b/fastembed/late_interaction/colbert.py#L205-L237)

## Working with Vector Databases

When using ColBERT with vector databases like Qdrant, you'll need to store the token-level embeddings and implement the late interaction scoring during retrieval. This often requires custom extensions or specialized vector database support for ColBERT's retrieval mechanism.

For more information on integrating with Qdrant specifically, see [Integration with Qdrant](qdrant/fastembed/9-integration-with-qdrant.md).

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [ColBERT and Late Interaction](#colbert-and-late-interaction.md)
- [What is ColBERT and Late Interaction?](#what-is-colbert-and-late-interaction.md)
- [ColBERT in FastEmbed Architecture](#colbert-in-fastembed-architecture.md)
- [Supported Models](#supported-models.md)
- [Using ColBERT in FastEmbed](#using-colbert-in-fastembed.md)
- [Basic Usage](#basic-usage.md)
- [ColBERT Embedding Process](#colbert-embedding-process.md)
- [Implementation Details](#implementation-details.md)
- [Special Token Handling](#special-token-handling.md)
- [Document Embedding Post-Processing](#document-embedding-post-processing.md)
- [Tokenization Process](#tokenization-process.md)
- [Performance Considerations](#performance-considerations.md)
- [Working with Vector Databases](#working-with-vector-databases.md)
