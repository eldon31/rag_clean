Web and Markup Backends | docling-project/docling | DeepWiki

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

# Web and Markup Backends

Relevant source files

- [docling/backend/html\_backend.py](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py)
- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [tests/data/groundtruth/docling\_v2/example\_06.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_06.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.json)
- [tests/data/groundtruth/docling\_v2/example\_06.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_06.html.md)
- [tests/data/groundtruth/docling\_v2/example\_09.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.itxt)
- [tests/data/groundtruth/docling\_v2/example\_09.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.json)
- [tests/data/groundtruth/docling\_v2/example\_09.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/example_09.html.md)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.itxt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.itxt)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.json)
- [tests/data/groundtruth/docling\_v2/wiki\_duck.html.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/wiki_duck.html.md)
- [tests/test\_backend\_html.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_html.py)

## Purpose and Scope

This document covers the document backends for web and markup formats: HTML, Markdown, and AsciiDoc. These backends parse structured text documents and convert them into the unified `DoclingDocument` representation. All three formats share the `SimplePipeline` processing path and produce documents with hierarchical structure, content layers, and rich formatting.

For PDF document backends, see [PDF Processing Backends](docling-project/docling/3.1-pdf-processing-backends.md). For Office document formats, see [Office Document Backends](docling-project/docling/3.2-office-document-backends.md).

## Architecture Overview

Web and markup backends inherit from `DeclarativeDocumentBackend` and implement format-specific parsing logic. Unlike PDF backends that require complex page-by-page processing, these backends parse the entire document structure in a single pass.

```
```

**Sources:** [docling/backend/html\_backend.py183-237](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L183-L237) [docling/document\_converter.py102-114](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L102-L114) [docling/datamodel/base\_models.py54-72](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L54-L72)

## Backend Configuration

### Format Options

Each backend is paired with a `FormatOption` that specifies the pipeline class and backend class. All web and markup formats use `SimplePipeline`:

| Format   | FormatOption Class     | Backend Class             | Pipeline         |
| -------- | ---------------------- | ------------------------- | ---------------- |
| HTML     | `HTMLFormatOption`     | `HTMLDocumentBackend`     | `SimplePipeline` |
| Markdown | `MarkdownFormatOption` | `MarkdownDocumentBackend` | `SimplePipeline` |
| AsciiDoc | `AsciiDocFormatOption` | `AsciiDocBackend`         | `SimplePipeline` |

```
```

**Sources:** [docling/document\_converter.py102-114](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L102-L114) [docling/document\_converter.py132-181](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L132-L181)

### MIME Type and Extension Detection

Format detection uses both MIME types and file extensions to identify document types:

**HTML:**

- MIME types: `text/html`, `application/xhtml+xml`
- Extensions: `.html`, `.htm`, `.xhtml`

**Markdown:**

- MIME types: `text/markdown`, `text/x-markdown`
- Extensions: `.md`

**AsciiDoc:**

- MIME types: `text/asciidoc`
- Extensions: `.adoc`, `.asciidoc`, `.asc`

**Sources:** [docling/datamodel/base\_models.py83-133](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L83-L133) [docling/datamodel/document.py376-400](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L376-L400)

## HTML Backend

The `HTMLDocumentBackend` is the most sophisticated web/markup backend, handling complex HTML structures including tables, lists, formatting, hyperlinks, and images.

### Core Implementation

```
```

**Sources:** [docling/backend/html\_backend.py183-237](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L183-L237) [docling/backend/html\_backend.py239-292](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L239-L292)

### Content Layer Management

HTML backend implements a content layer system that distinguishes between document body and furniture (metadata/navigation):

```
```

The backend determines content layers as follows:

1. **Initial state:** Content is `ContentLayer.FURNITURE` if no headers exist in the document
2. **First header transition:** When the first `<h1>`-`<h6>` tag is encountered (excluding headers inside tables), content layer switches to `ContentLayer.BODY`
3. **Footer handling:** `<footer>` tags temporarily switch back to `ContentLayer.FURNITURE`

**Sources:** [docling/backend/html\_backend.py276-288](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L276-L288) [docling/backend/html\_backend.py751-776](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L751-L776)

### Tag Processing Strategy

The backend uses a block-based buffering strategy to handle mixed inline and block-level HTML elements:

**Block Tags** (create distinct DocItem boundaries):

- `address`, `details`, `figure`, `footer`
- `h1` through `h6`
- `ol`, `ul`, `p`, `pre`, `summary`, `table`

**Format Tags** (apply inline formatting):

- `b`, `strong` → bold
- `i`, `em`, `var` → italic
- `s`, `del` → strikethrough
- `u`, `ins` → underline
- `sub` → subscript
- `sup` → superscript
- `code`, `kbd`, `samp` → code formatting

```
```

**Sources:** [docling/backend/html\_backend.py467-559](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L467-L559) [docling/backend/html\_backend.py40-77](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L40-L77)

### List Handling

The backend tracks list context to properly number ordered lists and handle nested structures:

```
```

The `_Context` class maintains:

- `list_ordered_flag_by_ref`: Tracks whether each list is ordered
- `list_start_by_ref`: Tracks the starting number for ordered lists

**Sources:** [docling/backend/html\_backend.py80-83](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L80-L83) [docling/backend/html\_backend.py913-1014](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L913-L1014)

### Table Processing

HTML tables are converted to `TableItem` objects with support for both simple and rich cells:

```
```

**Rich Table Cells** are created when:

- A cell contains multiple document items (e.g., multiple paragraphs)
- A cell contains non-text items (e.g., images, nested lists)

The backend creates a `GroupItem` to contain all child elements and references this group from the `RichTableCell`.

**Sources:** [docling/backend/html\_backend.py1016-1132](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L1016-L1132) [docling/backend/html\_backend.py294-349](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L294-L349) [docling/backend/html\_backend.py351-465](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L351-L465)

### Formatting and Hyperlinks

The backend tracks formatting and hyperlink context as it recursively walks the DOM tree:

**Formatting Stack:**

- Uses `self.format_tags: list[str]` to maintain active formatting
- Format tags are pushed/popped using context managers
- Combined into `Formatting` objects when creating text items

**Hyperlink Context:**

- Uses `self.hyperlink: Union[AnyUrl, Path, None]` to track current link
- Handles relative URLs by joining with `original_url`
- Falls back to `Path` for relative links that fail URL validation

**Text Annotation Classes:**

```
```

**Sources:** [docling/backend/html\_backend.py85-181](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L85-L181) [docling/backend/html\_backend.py573-580](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L573-L580) [docling/backend/html\_backend.py662-684](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L662-L684)

### Image Handling

Images are extracted from `<img>` tags and added as `PictureItem` objects:

```
```

**Sources:** [docling/backend/html\_backend.py1134-1218](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L1134-L1218)

### Heading Hierarchy

The backend manages document hierarchy based on heading levels:

1. `<h1>` tags create level-1 `SectionHeaderItem` and reset parent hierarchy
2. `<h2>` through `<h6>` tags create nested section headers
3. The `self.level` counter tracks current hierarchy depth
4. The `self.parents` dictionary maintains parent references at each level

```
```

**Sources:** [docling/backend/html\_backend.py778-839](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L778-L839) [docling/backend/html\_backend.py196-201](https://github.com/docling-project/docling/blob/f7244a43/docling/backend/html_backend.py#L196-L201)

## Markdown and AsciiDoc Backends

The Markdown and AsciiDoc backends follow similar patterns to the HTML backend but with format-specific parsers:

**MarkdownDocumentBackend:**

- Uses `marko` library for Markdown parsing
- Converts Markdown AST to DoclingDocument structure
- Handles CommonMark and extensions

**AsciiDocBackend:**

- Parses AsciiDoc markup format
- Converts AsciiDoc structure to DoclingDocument
- Preserves document structure and formatting

Both backends:

- Inherit from `DeclarativeDocumentBackend`
- Use `SimplePipeline` for processing
- Produce `DoclingDocument` output with hierarchical structure
- Support the same content layer system (BODY/FURNITURE)

**Sources:** [docling/document\_converter.py92-99](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L92-L99) [docling/document\_converter.py146-160](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py#L146-L160)

## Integration with SimplePipeline

All web and markup backends use `SimplePipeline`, which provides:

1. **Direct conversion:** Calls `backend.convert()` to get `DoclingDocument`
2. **Optional enrichment:** Can apply picture classification and description models
3. **No page-level processing:** Unlike PDF pipelines, processes entire document at once

```
```

**Configuration via CLI:**

```
```

**Sources:** [docling/pipeline/simple\_pipeline.py](https://github.com/docling-project/docling/blob/f7244a43/docling/pipeline/simple_pipeline.py) [docling/cli/main.py670-697](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L670-L697)

## Testing and Ground Truth

The test suite validates HTML backend functionality with multiple test cases:

**Test Coverage:**

- Heading level processing
- Ordered/unordered lists with start attributes
- Unicode character handling
- Hyperlink extraction (including parent context)
- Furniture vs body content layers
- End-to-end conversions with ground truth validation

**Ground Truth Structure:**

- JSON files contain full `DoclingDocument` serialization
- Markdown files contain exported markdown for comparison
- `.itxt` files contain indented text representation for hierarchy validation

**Sources:** [tests/test\_backend\_html.py](https://github.com/docling-project/docling/blob/f7244a43/tests/test_backend_html.py) [tests/data/groundtruth/docling\_v2/](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Web and Markup Backends](#web-and-markup-backends.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Architecture Overview](#architecture-overview.md)
- [Backend Configuration](#backend-configuration.md)
- [Format Options](#format-options.md)
- [MIME Type and Extension Detection](#mime-type-and-extension-detection.md)
- [HTML Backend](#html-backend.md)
- [Core Implementation](#core-implementation.md)
- [Content Layer Management](#content-layer-management.md)
- [Tag Processing Strategy](#tag-processing-strategy.md)
- [List Handling](#list-handling.md)
- [Table Processing](#table-processing.md)
- [Formatting and Hyperlinks](#formatting-and-hyperlinks.md)
- [Image Handling](#image-handling.md)
- [Heading Hierarchy](#heading-hierarchy.md)
- [Markdown and AsciiDoc Backends](#markdown-and-asciidoc-backends.md)
- [Integration with SimplePipeline](#integration-with-simplepipeline.md)
- [Testing and Ground Truth](#testing-and-ground-truth.md)
