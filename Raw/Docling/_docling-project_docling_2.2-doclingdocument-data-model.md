DoclingDocument Data Model | docling-project/docling | DeepWiki

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

# DoclingDocument Data Model

Relevant source files

- [docling/cli/main.py](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py)
- [docling/datamodel/base\_models.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py)
- [docling/datamodel/document.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py)
- [docling/datamodel/pipeline\_options.py](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/pipeline_options.py)
- [docling/document\_converter.py](https://github.com/docling-project/docling/blob/f7244a43/docling/document_converter.py)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json)
- [tests/data/groundtruth/docling\_v2/2203.01017v2.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.md)
- [tests/data/groundtruth/docling\_v2/2206.01062.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2206.01062.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2206.01062.json)
- [tests/data/groundtruth/docling\_v2/2305.03393v1.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2305.03393v1.doctags.txt)
- [tests/data/groundtruth/docling\_v2/2305.03393v1.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2305.03393v1.json)
- [tests/data/groundtruth/docling\_v2/multi\_page.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/multi_page.json)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.doctags.txt](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.doctags.txt)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json)
- [tests/data/groundtruth/docling\_v2/redp5110\_sampled.md](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.md)

This document describes the `DoclingDocument` data model, which is the unified representation format produced by all Docling conversion pipelines. It defines the schema for representing document structure, content, and metadata in a format-agnostic way that enables downstream processing, export to multiple formats, and semantic analysis.

For information about the conversion process that produces `DoclingDocument` instances, see [Document Conversion Flow](docling-project/docling/2.1-document-conversion-flow.md). For details on export formats, see [Export Formats](docling-project/docling/8.1-export-formats.md).

---

## Purpose and Scope

The `DoclingDocument` data model serves as the central unified representation in Docling's architecture. All processing pipelines—whether `StandardPdfPipeline`, `VlmPipeline`, or `SimplePipeline`—produce a `DoclingDocument` instance that captures:

- **Document structure**: Hierarchical organization of content using parent-child relationships
- **Content elements**: Text blocks, tables, pictures, lists, and other semantic units
- **Provenance information**: Spatial coordinates, page numbers, and character spans linking elements to source locations
- **Metadata**: Document origin, format information, and processing metadata
- **Content layers**: Separation between body content and document furniture (headers, footers)

The model is defined in the `docling-core` package and imported into Docling for use across the conversion pipeline.

Sources: [docling/datamodel/document.py24-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L24-L32) [docling/datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L215) [tests/data/groundtruth/docling\_v2/2203.01017v2.json1-15](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L1-L15)

---

## Schema Structure Overview

### Top-Level Schema

```
```

**Diagram: DoclingDocument top-level structure showing schema information, origin metadata, root nodes, and element collections**

The document consists of:

1. **Schema metadata**: `schema_name` (always "DoclingDocument"), `version`, and document `name`
2. **Origin information**: Source file metadata including MIME type, binary hash, and filename
3. **Root nodes**: `body` and `furniture` as entry points into the document hierarchy
4. **Typed collections**: Arrays holding all instances of each element type (texts, tables, pictures, groups)

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json1-16](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L1-L16) [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json1-17](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json#L1-L17)

---

## Hierarchical Structure with JSON References

### Reference-Based Hierarchy

DoclingDocument uses a JSON reference system (`$ref`) to establish parent-child relationships without duplicating data. Each element has:

- `self_ref`: A JSON pointer to the element's location (e.g., `"#/texts/42"`)
- `parent`: A `$ref` to the parent element (e.g., `{"$ref": "#/body"}`)
- `children`: A list of `$ref` objects pointing to child elements

```
```

**Diagram: Document hierarchy using JSON $ref pointers. Solid arrows show parent-to-child references via children array, dotted arrows show child-to-parent references via parent field**

This design provides several advantages:

1. **No duplication**: Each element appears exactly once in its typed array
2. **Efficient traversal**: Both top-down (via `children`) and bottom-up (via `parent`) navigation
3. **Clear ownership**: Every element except roots has exactly one parent
4. **Type safety**: Elements remain in their typed collections for easy access

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json17-60](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L17-L60) [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json466-527](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json#L466-L527)

---

## Content Layers: Body vs Furniture

The document is divided into two primary content layers:

### Body Layer

The `body` node contains the main semantic content of the document:

- Section headers
- Paragraphs and text blocks
- Tables
- Figures and pictures
- Lists and enumerations
- Formulas and equations
- Code blocks

```
```

### Furniture Layer

The `furniture` node contains document furniture—elements that provide context but are not primary content:

- Page headers
- Page footers
- Footnotes
- Marginal notes
- Page numbers

```
```

Elements have a `content_layer` field indicating their layer membership. This separation enables:

- **Clean export**: Body-only exports for main content extraction
- **Layout analysis**: Identification of page layout patterns
- **Semantic processing**: Focus on primary content without distractions

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json10-16](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L10-L16) [tests/data/groundtruth/docling\_v2/2203.01017v2.json17-489](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L17-L489) [docling/datamodel/document.py80-99](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L80-L99)

---

## Element Types and Labels

### DocItemLabel Enumeration

Elements are classified using `DocItemLabel` values, which map to specific semantic types:

| Label                | Description          | Common Use                         |
| -------------------- | -------------------- | ---------------------------------- |
| `section_header`     | Section heading      | Document structure, TOC generation |
| `title`              | Document title       | Metadata extraction                |
| `text` / `paragraph` | Body text            | Content extraction                 |
| `list_item`          | List entry           | List detection and formatting      |
| `table`              | Table structure      | Table extraction                   |
| `picture`            | Image or figure      | Image extraction, captioning       |
| `caption`            | Image/table caption  | Association with parent element    |
| `formula`            | Mathematical formula | LaTeX extraction                   |
| `code`               | Code block           | Syntax highlighting                |
| `page_header`        | Running header       | Furniture identification           |
| `page_footer`        | Running footer       | Furniture identification           |
| `footnote`           | Footnote reference   | Citation tracking                  |

Sources: [docling/datamodel/document.py80-99](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L80-L99) [docling/datamodel/base\_models.py6-13](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L6-L13)

### Element Type Overview

```
```

**Diagram: Element type hierarchy showing common base properties and specialized types**

Sources: [docling/datamodel/document.py24-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L24-L32) \[docling\_core.types.doc imports]

---

## Text Elements

### TextItem Structure

Text elements represent textual content with rich provenance information:

```
```

**Key fields:**

- `orig`: Original text as extracted from the source
- `text`: Processed/cleaned text for output
- `prov`: Provenance array linking text to source page(s)
- `label`: Semantic classification (text, paragraph, section\_header, etc.)

### SectionHeaderItem

Section headers extend TextItem with hierarchical level information:

```
```

The `level` field indicates nesting depth, enabling table of contents generation and document outline extraction.

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json834-916](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L834-L916) [tests/data/groundtruth/docling\_v2/2203.01017v2.json945-971](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L945-L971)

---

## Table Elements

### TableItem Structure

Tables are represented with complete structural information:

```
```

**Key components:**

- `otsl_seq`: Optimized Table Structure Language sequence (see OTSL documentation)
- `num_rows`, `num_cols`: Table dimensions
- `table_cells`: Array of cell objects with positions and spans
- Each cell contains bbox, span information, and text content

OTSL tokens used in sequence:

- `<ched>`: Column header
- `<rhed>`: Row header
- `<fcel>`: First cell in row
- `<lcel>`: Last cell in row
- `<nl>`: New line (row separator)

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.doctags.txt11-12](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.doctags.txt#L11-L12) [docling/datamodel/document.py42-44](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L42-L44)

---

## Picture Elements

### PictureItem Structure

Pictures (images, figures) are represented with optional annotations and captions:

```
```

**Key fields:**

- `annotations`: List of `PictureDataType` objects for image data (base64, PNG, etc.)
- `provenance`: String indicating annotation source (e.g., "model\_generated", "api\_described")
- `predicted_class`: Classification result (Figure, Chart, Diagram, etc.)
- `confidence`: Model confidence score
- `children`: Often contains a caption TextItem

The `prov` bbox defines the image's location on the page, enabling image extraction and spatial relationship analysis.

Sources: [docling/datamodel/base\_models.py218-233](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L218-L233) \[tests/data/groundtruth/docling\_v2/2203.01017v2.json]

---

## Group Elements

### GroupItem for Structural Aggregation

Groups aggregate related elements, most commonly for lists:

```
```

Groups serve multiple purposes:

- **List representation**: Unordered and ordered lists
- **Nested structures**: Lists can contain other groups for multi-level lists
- **Logical grouping**: Related content that should be processed together

The `name` field identifies the group type ("list", "group"), while `label` provides semantic classification. Children maintain document order.

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json490-541](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L490-L541) [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json466-527](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json#L466-L527)

---

## Provenance Tracking

### Provenance Structure

Every content element includes `prov` (provenance) information linking it to source locations:

```
```

**Diagram: Provenance structure linking elements to source locations**

### Bounding Box Coordinates

Coordinates follow PDF conventions with configurable origin:

```
```

- `l` (left), `t` (top), `r` (right), `b` (bottom): Coordinates in points (1/72 inch)
- `coord_origin`: Typically `"BOTTOMLEFT"` for PDF (origin at bottom-left of page)
- Coordinates enable precise spatial analysis and image cropping

### Character Spans

The `charspan` field provides character-level granularity:

```
```

This `[start, end)` range links the element to the character stream extracted from the page, enabling:

- Text selection and highlighting
- Precise text extraction from source
- Mapping between visual and textual representations

### Multi-Page Elements

Elements can span multiple pages using multiple provenance entries:

```
```

This structure supports:

- Tables spanning pages
- Text flowing across page boundaries
- Complete reconstruction of element layout

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json843-857](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L843-L857) [docling/datamodel/document.py35-40](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L35-L40) \[docling\_core.types.doc BoundingBox]

---

## Integration with Conversion Pipeline

### Creation in Pipeline

```
```

**Diagram: DoclingDocument creation flow through pipeline phases**

### ConversionResult Container

The `ConversionResult` class wraps the document with metadata:

```
```

Key relationships:

- `input`: Source document information
- `pages`: Intermediate page-level representations (retained for debugging)
- `document`: Final unified DoclingDocument
- `status`: Conversion outcome
- `confidence`: Quality scores per page and overall

Sources: [docling/datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L215) \[docling/pipeline/base\_pipeline.py]

### Export Capabilities

Once created, DoclingDocument can be exported to multiple formats:

```
```

Export methods leverage the unified structure to generate:

- **JSON**: Complete serialization with provenance and structure
- **Markdown**: Semantic text with tables and images
- **HTML**: Rich rendering with CSS styling
- **DOCTAGS**: Tagged format for training VLM models

Sources: [docling/cli/main.py211-275](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L211-L275)

---

## JSON Schema Example

### Complete Document Structure

Here's a minimal complete DoclingDocument in JSON format:

```
```

This structure demonstrates:

1. Schema versioning for compatibility tracking
2. Origin metadata for provenance
3. Separation of furniture and body content
4. Reference-based hierarchy avoiding duplication
5. Type-specific collections for efficient access
6. Complete provenance linking to source pages

Sources: [tests/data/groundtruth/docling\_v2/2203.01017v2.json1-100](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/2203.01017v2.json#L1-L100) [tests/data/groundtruth/docling\_v2/redp5110\_sampled.json1-100](https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth/docling_v2/redp5110_sampled.json#L1-L100)

---

## Summary Table

| Aspect             | Description                                             | Key Files                                                                                                                                 |
| ------------------ | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Schema**         | DoclingDocument from docling-core with versioned schema | [docling/datamodel/document.py24-32](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L24-L32)      |
| **Structure**      | JSON with $ref pointers for hierarchy                   | [tests/data/groundtruth examples](<https://github.com/docling-project/docling/blob/f7244a43/tests/data/groundtruth examples>)             |
| **Content Layers** | body (main content) and furniture (page elements)       | [docling/datamodel/document.py80-99](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L80-L99)      |
| **Element Types**  | texts, tables, pictures, groups with DocItemLabel       | [docling/datamodel/base\_models.py6-13](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/base_models.py#L6-L13) |
| **Provenance**     | page\_no, bbox, charspan for each element               | [docling\_core.types.doc.base](https://github.com/docling-project/docling/blob/f7244a43/docling_core.types.doc.base)                      |
| **Integration**    | Created by pipelines, wrapped in ConversionResult       | [docling/datamodel/document.py198-215](https://github.com/docling-project/docling/blob/f7244a43/docling/datamodel/document.py#L198-L215)  |
| **Export**         | JSON, Markdown, HTML, DOCTAGS formats                   | [docling/cli/main.py211-275](https://github.com/docling-project/docling/blob/f7244a43/docling/cli/main.py#L211-L275)                      |

The DoclingDocument data model provides a robust, extensible representation that bridges the gap between raw document formats and structured semantic content, enabling high-quality document understanding and downstream processing.

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [DoclingDocument Data Model](#doclingdocument-data-model.md)
- [Purpose and Scope](#purpose-and-scope.md)
- [Schema Structure Overview](#schema-structure-overview.md)
- [Top-Level Schema](#top-level-schema.md)
- [Hierarchical Structure with JSON References](#hierarchical-structure-with-json-references.md)
- [Reference-Based Hierarchy](#reference-based-hierarchy.md)
- [Content Layers: Body vs Furniture](#content-layers-body-vs-furniture.md)
- [Body Layer](#body-layer.md)
- [Furniture Layer](#furniture-layer.md)
- [Element Types and Labels](#element-types-and-labels.md)
- [DocItemLabel Enumeration](#docitemlabel-enumeration.md)
- [Element Type Overview](#element-type-overview.md)
- [Text Elements](#text-elements.md)
- [TextItem Structure](#textitem-structure.md)
- [SectionHeaderItem](#sectionheaderitem.md)
- [Table Elements](#table-elements.md)
- [TableItem Structure](#tableitem-structure.md)
- [Picture Elements](#picture-elements.md)
- [PictureItem Structure](#pictureitem-structure.md)
- [Group Elements](#group-elements.md)
- [GroupItem for Structural Aggregation](#groupitem-for-structural-aggregation.md)
- [Provenance Tracking](#provenance-tracking.md)
- [Provenance Structure](#provenance-structure.md)
- [Bounding Box Coordinates](#bounding-box-coordinates.md)
- [Character Spans](#character-spans.md)
- [Multi-Page Elements](#multi-page-elements.md)
- [Integration with Conversion Pipeline](#integration-with-conversion-pipeline.md)
- [Creation in Pipeline](#creation-in-pipeline.md)
- [ConversionResult Container](#conversionresult-container.md)
- [Export Capabilities](#export-capabilities.md)
- [JSON Schema Example](#json-schema-example.md)
- [Complete Document Structure](#complete-document-structure.md)
- [Summary Table](#summary-table.md)
