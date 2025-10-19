Image Data Applications | qdrant/examples | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/examples](https://github.com/qdrant/examples "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 26 June 2025 ([b3c4b2](https://github.com/qdrant/examples/commits/b3c4b28f))

- [Overview](qdrant/examples/1-overview.md)
- [Getting Started with Qdrant](qdrant/examples/2-getting-started-with-qdrant.md)
- [Text Data Applications](qdrant/examples/3-text-data-applications.md)
- [Code Search with Dual Embeddings](qdrant/examples/3.1-code-search-with-dual-embeddings.md)
- [Extractive Question Answering](qdrant/examples/3.2-extractive-question-answering.md)
- [Movie Recommendations with Sparse Vectors](qdrant/examples/3.3-movie-recommendations-with-sparse-vectors.md)
- [Image Data Applications](qdrant/examples/4-image-data-applications.md)
- [E-commerce Reverse Image Search](qdrant/examples/4.1-e-commerce-reverse-image-search.md)
- [Medical Image Search with Vision Transformers](qdrant/examples/4.2-medical-image-search-with-vision-transformers.md)
- [Audio Data Applications](qdrant/examples/5-audio-data-applications.md)
- [Music Recommendation Engine](qdrant/examples/5.1-music-recommendation-engine.md)
- [Advanced RAG Systems](qdrant/examples/6-advanced-rag-systems.md)
- [Multivector RAG with DSPy](qdrant/examples/6.1-multivector-rag-with-dspy.md)
- [Graph-Enhanced RAG with Neo4j](qdrant/examples/6.2-graph-enhanced-rag-with-neo4j.md)
- [PDF Retrieval at Scale](qdrant/examples/6.3-pdf-retrieval-at-scale.md)
- [Agentic Systems with CrewAI](qdrant/examples/7-agentic-systems-with-crewai.md)
- [Meeting Analysis with Agentic RAG](qdrant/examples/7.1-meeting-analysis-with-agentic-rag.md)
- [Additional Use Cases](qdrant/examples/8-additional-use-cases.md)
- [Self-Query Systems with LangChain](qdrant/examples/8.1-self-query-systems-with-langchain.md)
- [Development Environment Setup](qdrant/examples/8.2-development-environment-setup.md)

Menu

# Image Data Applications

Relevant source files

- [ecommerce\_reverse\_image\_search/ecommerce-reverse-image-search.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/ecommerce-reverse-image-search.ipynb)
- [ecommerce\_reverse\_image\_search/queries/cable.jpg](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/queries/cable.jpg)
- [ecommerce\_reverse\_image\_search/queries/cleaning.jpg](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/queries/cleaning.jpg)
- [ecommerce\_reverse\_image\_search/queries/skating.jpg](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/queries/skating.jpg)
- [ecommerce\_reverse\_image\_search/queries/spoon.jpg](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/queries/spoon.jpg)
- [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb)
- [qdrant\_101\_image\_data/README.md](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md)

This document covers image-based applications using Qdrant vector database for visual similarity search and retrieval. The content focuses on two primary implementations: e-commerce reverse image search and medical image analysis systems. These applications demonstrate how to extract visual embeddings from images and perform semantic search operations.

For text-based search applications, see [Text Data Applications](qdrant/examples/3-text-data-applications.md). For audio processing systems, see [Audio Data Applications](qdrant/examples/5-audio-data-applications.md).

## Core Architecture and Components

Image data applications in Qdrant follow a common pattern of embedding extraction, storage, and similarity search. The architecture involves image preprocessing, feature extraction using pre-trained models, vector storage, and search operations.

```
```

**Core Technical Components**

| Component             | Implementation            | Purpose                                    |
| --------------------- | ------------------------- | ------------------------------------------ |
| `ViTImageProcessor`   | Hugging Face Transformers | Image preprocessing and tokenization       |
| `ViTModel`            | Vision Transformer models | Feature extraction from images             |
| `QdrantClient`        | Qdrant Python client      | Vector database operations                 |
| `models.VectorParams` | Qdrant configuration      | Collection setup with embedding dimensions |
| `models.Filter`       | Qdrant filtering          | Metadata-based search refinement           |

Sources: [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb137-142](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L137-L142) [ecommerce\_reverse\_image\_search/ecommerce-reverse-image-search.ipynb1-100](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/ecommerce-reverse-image-search.ipynb#L1-L100)

## E-commerce Reverse Image Search

The e-commerce implementation enables visual product search using the Amazon Product Dataset 2020. Users can submit product images to find visually similar items in the catalog.

### Dataset and Setup

The system processes product data with image URLs and metadata including product names, categories, and pricing information. The implementation uses a configurable dataset fraction for testing and development.

```
```

**Key Implementation Details**

The dataset fraction is controlled by the `DATASET_FRACTION` variable, typically set to `0.1` for development to process only 10% of the full dataset. The system downloads images from provided URLs and extracts embeddings using vision models.

Sources: [ecommerce\_reverse\_image\_search/ecommerce-reverse-image-search.ipynb275-277](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/ecommerce-reverse-image-search.ipynb#L275-L277) [ecommerce\_reverse\_image\_search/ecommerce-reverse-image-search.ipynb51-58](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/ecommerce-reverse-image-search.ipynb#L51-L58)

### Visual Search Implementation

The search system processes query images through the same embedding pipeline and performs cosine similarity matching against stored product vectors.

```
```

Sources: [ecommerce\_reverse\_image\_search/ecommerce-reverse-image-search.ipynb1-50](https://github.com/qdrant/examples/blob/b3c4b28f/ecommerce_reverse_image_search/ecommerce-reverse-image-search.ipynb#L1-L50)

## Medical Image Search with Vision Transformers

The medical application focuses on skin cancer image analysis using the `marmal88/skin_cancer` dataset from Hugging Face. This system assists medical professionals in comparing diagnostic images.

### Dataset Structure and Medical Metadata

The skin cancer dataset contains 9,577 images with comprehensive medical metadata including diagnosis types, patient demographics, and lesion locations.

**Dataset Schema**

| Field          | Type      | Description                                               |
| -------------- | --------- | --------------------------------------------------------- |
| `image`        | PIL Image | 600x450 RGB medical images                                |
| `image_id`     | String    | Unique image identifier                                   |
| `lesion_id`    | String    | Lesion type identifier                                    |
| `dx`           | String    | Diagnosis (melanoma, basal\_cell\_carcinoma, etc.)        |
| `dx_type`      | String    | Diagnosis method (histo, follow\_up, consensus, confocal) |
| `age`          | Float     | Patient age (5-86 years)                                  |
| `sex`          | String    | Patient gender (female, male, unknown)                    |
| `localization` | String    | Body location of lesion                                   |

Sources: [qdrant\_101\_image\_data/README.md23-34](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/README.md#L23-L34) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb257-258](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L257-L258)

### Vision Transformer Integration

The system uses Facebook's DINO model (`facebook/dino-vits16`) for feature extraction. The implementation processes images through `ViTImageProcessor` and generates 384-dimensional embeddings.

```
```

**Key Technical Implementation**

The embedding process uses mean pooling across patches to compress the 197-patch ViT output into a single 384-dimensional vector per image.

```
```

Sources: [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb204-207](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L204-L207) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb296-302](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L296-L302) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb187-192](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L187-L192)

### Medical Search and Filtering

The medical search system supports demographic filtering to find cases similar to specific patient profiles. This enables targeted diagnostic assistance based on patient characteristics.

```
```

**Filter Implementation Example**

The system implements complex demographic filtering using Qdrant's filter syntax:

```
```

Sources: [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb484-492](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L484-L492) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb496-503](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L496-L503)

## Data Processing and Storage Pipeline

Both applications follow similar patterns for data ingestion, embedding generation, and vector storage in Qdrant collections.

### Batch Processing and Collection Management

The systems implement batch processing for efficient embedding generation and storage. The medical application processes images in batches of 16, while the e-commerce system uses configurable batch sizes of 1000 for vector uploads.

```
```

**Collection Configuration**

Both systems use cosine distance for similarity measurement, with embedding dimensions matching the model output (384 for ViT models).

Sources: [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb306-307](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L306-L307) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb380-398](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L380-L398) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb187-192](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L187-L192)

### Metadata and Payload Management

The applications store comprehensive metadata alongside vectors to enable filtering and result enrichment. The medical system handles missing values by filling NaN ages with 0, while preserving other patient information.

**Payload Structure**

```
```

The payload conversion process transforms HuggingFace dataset columns into Qdrant-compatible dictionary records, ensuring proper handling of missing values and data type compatibility.

Sources: [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb332-337](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L332-L337) [qdrant\_101\_image\_data/04\_qdrant\_101\_cv.ipynb363-365](https://github.com/qdrant/examples/blob/b3c4b28f/qdrant_101_image_data/04_qdrant_101_cv.ipynb#L363-L365)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Image Data Applications](#image-data-applications.md)
- [Core Architecture and Components](#core-architecture-and-components.md)
- [E-commerce Reverse Image Search](#e-commerce-reverse-image-search.md)
- [Dataset and Setup](#dataset-and-setup.md)
- [Visual Search Implementation](#visual-search-implementation.md)
- [Medical Image Search with Vision Transformers](#medical-image-search-with-vision-transformers.md)
- [Dataset Structure and Medical Metadata](#dataset-structure-and-medical-metadata.md)
- [Vision Transformer Integration](#vision-transformer-integration.md)
- [Medical Search and Filtering](#medical-search-and-filtering.md)
- [Data Processing and Storage Pipeline](#data-processing-and-storage-pipeline.md)
- [Batch Processing and Collection Management](#batch-processing-and-collection-management.md)
- [Metadata and Payload Management](#metadata-and-payload-management.md)
