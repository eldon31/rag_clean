Export Formats | docling-project/docling | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[docling-project/docling](https://github.com/docling-project/docling "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 12 October 2025 ([f7244a](https://github.com/docling-project/docling/commits/f7244a43))

- [Overview](docling-project/docling/1-overview.md)
- [Installation](docling-project/docling/1.1-installation.md)
- [Quick Start](docling-project/docling/1.2-quick-start.md)
- [Core Architecture](docling-project/docling/2-core-architecture.md)
- [Document Conversion Flow](docling-project/docling/2.1-document-conversion-flow.md)
- [DoclingDocument Data Model](docling-project/docling/2.2-doclingdocument-data-model.md)
- [Configuration and Pipeline Options](docling-project/docling/2.3-configuration-and-pipeline-options.md)
- [Format Detection and Routing](docling-project/docling/2.4-format-detection-and-routing.md)
- [Document Backends](docling-project/docling/3-document-backends.md)
- [PDF Processing Backends](docling-project/docling/3.1-pdf-processing-backends.md)
- [Office Document Backends](docling-project/docling/3.2-office-document-backends.md)
- [Web and Markup Backends](docling-project/docling/3.3-web-and-markup-backends.md)
- [AI/ML Models](docling-project/docling/4-aiml-models.md)
- [OCR Models](docling-project/docling/4.1-ocr-models.md)
- [Layout and Table Structure Models](docling-project/docling/4.2-layout-and-table-structure-models.md)
- [Vision Language Models](docling-project/docling/4.3-vision-language-models.md)
- [Inline VLM Models](docling-project/docling/4.3.1-inline-vlm-models.md)
- [API-Based VLM Models](docling-project/docling/4.3.2-api-based-vlm-models.md)
- [Enrichment Models](docling-project/docling/4.4-enrichment-models.md)
- [Processing Pipelines](docling-project/docling/5-processing-pipelines.md)
- [Standard PDF Pipeline](docling-project/docling/5.1-standard-pdf-pipeline.md)
- [Threaded PDF Pipeline](docling-project/docling/5.2-threaded-pdf-pipeline.md)
- [VLM Pipeline](docling-project/docling/5.3-vlm-pipeline.md)
- [Extraction Pipeline](docling-project/docling/5.4-extraction-pipeline.md)
- [ASR Pipeline](docling-project/docling/5.5-asr-pipeline.md)
- [Base Pipeline Architecture](docling-project/docling/5.6-base-pipeline-architecture.md)
- [Command Line Interface](docling-project/docling/6-command-line-interface.md)
- [Document Conversion CLI](docling-project/docling/6.1-document-conversion-cli.md)
- [Model Management CLI](docling-project/docling/6.2-model-management-cli.md)
- [Python SDK](docling-project/docling/7-python-sdk.md)
- [DocumentConverter API](docling-project/docling/7.1-documentconverter-api.md)
- [DocumentExtractor API](docling-project/docling/7.2-documentextractor-api.md)
- [Usage Examples](docling-project/docling/7.3-usage-examples.md)
- [Output and Integration](docling-project/docling/8-output-and-integration.md)
- [Export Formats](docling-project/docling/8.1-export-formats.md)
- [Document Chunking](docling-project/docling/8.2-document-chunking.md)
- [Framework Integrations](docling-project/docling/8.3-framework-integrations.md)
- [Development and Testing](docling-project/docling/9-development-and-testing.md)
- [Testing Framework](docling-project/docling/9.1-testing-framework.md)
- [Ground Truth Data](docling-project/docling/9.2-ground-truth-data.md)
- [CI/CD and Development Workflow](docling-project/docling/9.3-cicd-and-development-workflow.md)
- [Deployment](docling-project/docling/10-deployment.md)
- [Docker Deployment](docling-project/docling/10.1-docker-deployment.md)
- [Model Artifacts Management](docling-project/docling/10.2-model-artifacts-management.md)

Menu

# Export Formats

Relevant source files

- [docling/backend/html\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.md)
- [tests/data/groundtruth/docling\_v2/2206.01062.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2206.01062.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.json)
- [tests/data/groundtruth/docling\_v2/2305.03393v1.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2305.03393v1.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2305.03393v1.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2305.03393v1.json)
- [tests/data/groundtruth/docling\_v2/example\_06.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_06.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.json)
- [tests/data/groundtruth/docling\_v2/example\_06.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.md)
- [tests/data/groundtruth/docling\_v2/example\_09.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_09.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.json)
- [tests/data/groundtruth/docling\_v2/example\_09.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.md)
- [tests/data/groundtruth/docling\_v2/multi\_page.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/multi_page.json)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.doctags.txt)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.md)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.itxt)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.json)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.md)
- [tests/test\_backend\_html.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_html.py)

This document covers the various output formats supported by Docling for exporting converted documents. It details the available export formats, their structure, and the APIs used to generate them.

For information about document chunking strategies that work with these export formats, see [Document Chunking](docling-project/docling/8.2-document-chunking.md). For framework-specific integrations that consume these formats, see [Framework Integrations](docling-project/docling/8.3-framework-integrations.md).

## Overview

Docling provides multiple export formats to support different downstream use cases, from human-readable documents to machine-processable structured data. All export formats are generated from the universal `DoclingDocument` representation that serves as the intermediate format after document conversion.

## Export Format Architecture

The export system in Docling follows a layered architecture where the `DoclingDocument` serves as the central hub for all export operations:

```
```

Sources: [docs/examples/minimal.py8](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal.py#L8-L8) [docs/examples/hybrid\_chunking.ipynb81](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/hybrid_chunking.ipynb#L81-L81) [docs/concepts/chunking.md8-14](https://github.com/docling-project/docling/blob/f7244a43/docs/concepts/chunking.md#L8-L14)

## DoclingDocument Structure

The `DoclingDocument` serves as the universal document representation from which all export formats are derived. Understanding its structure is key to understanding the export formats:

```
```

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json1-16](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L1-L16) [tests/data/groundtruth/docling\_v2/2206.01062.json1-16](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.json#L1-L16)

## JSON Export Format

The JSON format is the native serialization of the `DoclingDocument` object, preserving all structural information and metadata.

### Structure

The JSON export maintains the complete document hierarchy with element references:

| Field         | Description                | Example                                                  |
| ------------- | -------------------------- | -------------------------------------------------------- |
| `schema_name` | Document schema identifier | `"DoclingDocument"`                                      |
| `version`     | Schema version             | `"1.6.0"`                                                |
| `name`        | Document identifier        | `"2203.01017v2"`                                         |
| `origin`      | Source file metadata       | `{"mimetype": "application/pdf", "filename": "doc.pdf"}` |
| `body`        | Main content tree          | Contains references to text, table, picture elements     |
| `texts`       | Text element array         | Individual text blocks with provenance                   |
| `tables`      | Table element array        | Structured table data                                    |
| `pictures`    | Picture element array      | Image elements with captions                             |

### Element References

The JSON format uses JSON Pointer references to maintain document structure:

```
```

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json17-32](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L17-L32) [tests/data/groundtruth/docling\_v2/2206.01062.json17-32](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.json#L17-L32)

## Markdown Export Format

The Markdown export provides a human-readable, text-based representation suitable for documentation and display purposes.

### Features

- Hierarchical heading structure based on document sections
- Table preservation using Markdown table syntax
- Image handling with alt text from captions
- List formatting for grouped content
- Metadata preservation in frontmatter

### Usage

```
```

The Markdown export flattens the hierarchical document structure while preserving logical organization through heading levels and formatting.

Sources: [docs/examples/minimal.py8](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/minimal.py#L8-L8) [docs/concepts/chunking.md8](https://github.com/docling-project/docling/blob/f7244a43/docs/concepts/chunking.md#L8-L8)

## HTML Export Format

The HTML export generates web-compatible markup while preserving document structure and styling information.

### Structure

- Semantic HTML elements for different document components
- CSS classes for styling preservation
- Table export with proper HTML table markup
- Image embedding with captions
- Accessibility attributes from document metadata

Sources: [docs/v2.md19](https://github.com/docling-project/docling/blob/f7244a43/docs/v2.md#L19-L19)

## YAML Export Format

The YAML export provides a human-readable structured format alternative to JSON, useful for configuration and data interchange.

### Characteristics

- Hierarchical structure similar to JSON but more readable
- Preserves all document metadata and provenance
- Suitable for version control and manual editing
- Compatible with YAML-based toolchains

## DocTags Export Format

DocTags is a specialized export format that provides a compact representation of document structure optimized for specific use cases.

## Text Chunking for RAG Applications

Beyond direct export formats, Docling provides sophisticated chunking capabilities for generating text segments suitable for Retrieval-Augmented Generation (RAG) and embedding workflows:

```
```

### Chunking Methods

| Chunker Type          | Description                                         | Use Case                           |
| --------------------- | --------------------------------------------------- | ---------------------------------- |
| `HierarchicalChunker` | Structure-aware chunking based on document elements | Preserving document hierarchy      |
| `HybridChunker`       | Token-aware refinement with merge/split logic       | RAG applications with token limits |

### Chunk Contextualization

The `contextualize()` method enriches chunk text with relevant metadata:

```
```

Sources: [docs/examples/hybrid\_chunking.ipynb106-110](https://github.com/docling-project/docling/blob/f7244a43/docs/examples/hybrid_chunking.ipynb#L106-L110) [docs/concepts/chunking.md30-36](https://github.com/docling-project/docling/blob/f7244a43/docs/concepts/chunking.md#L30-L36)

## Export Format Selection

The choice of export format depends on the intended use case:

- **JSON**: Complete data preservation, programmatic access, archival
- **Markdown**: Human-readable documentation, content management systems
- **HTML**: Web publishing, styled presentation
- **YAML**: Configuration files, human-editable structured data
- **Text Chunks**: RAG applications, embedding models, search indexing

Each format is optimized for specific downstream consumers while maintaining traceability back to the source document through provenance information.

Sources: [docs/v2.md15-29](https://github.com/docling-project/docling/blob/f7244a43/docs/v2.md#L15-L29) [docs/concepts/chunking.md3-14](https://github.com/docling-project/docling/blob/f7244a43/docs/concepts/chunking.md#L3-L14)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Export Formats](#export-formats.md)
- [Overview](#overview.md)
- [Export Format Architecture](#export-format-architecture.md)
- [DoclingDocument Structure](#doclingdocument-structure.md)
- [JSON Export Format](#json-export-format.md)
- [Structure](#structure.md)
- [Element References](#element-references.md)
- [Markdown Export Format](#markdown-export-format.md)
- [Features](#features.md)
- [Usage](#usage.md)
- [HTML Export Format](#html-export-format.md)
- [Structure](#structure-1.md)
- [YAML Export Format](#yaml-export-format.md)
- [Characteristics](#characteristics.md)
- [DocTags Export Format](#doctags-export-format.md)
- [Text Chunking for RAG Applications](#text-chunking-for-rag-applications.md)
- [Chunking Methods](#chunking-methods.md)
- [Chunk Contextualization](#chunk-contextualization.md)
- [Export Format Selection](#export-format-selection.md)
