# Docling Mini Regression Corpus

This corpus trims `_docling-project_docling_1-overview_chunks.json` to six
deterministic chunks for regression harness coverage.

## Source

- Origin: `Chunked/Docling/_docling-project_docling_1-overview_chunks.json`
- Extracted: 2025-10-30
- Selection rules:
  1. Keep the first six prose chunks above 100 tokens.
  2. Preserve sparse feature payloads and headings.
  3. Normalize identifiers to the `docling-mini-000N` scheme.

## Usage

- Default CLI args recorded in `harness_config.yaml`.
- Chunk JSON lives under `chunked/docling-mini_chunks.json`.
- Golden artifacts sit in `goldens/` for schema assertions.
