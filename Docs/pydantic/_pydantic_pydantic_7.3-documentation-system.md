Documentation System | pydantic/pydantic | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[pydantic/pydantic](https://github.com/pydantic/pydantic "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 11 October 2025 ([76ef0b](https://github.com/pydantic/pydantic/commits/76ef0b08))

- [Overview](pydantic/pydantic/1-overview.md)
- [Core Model System](pydantic/pydantic/2-core-model-system.md)
- [BaseModel](pydantic/pydantic/2.1-basemodel.md)
- [Field System](pydantic/pydantic/2.2-field-system.md)
- [Model Configuration](pydantic/pydantic/2.3-model-configuration.md)
- [Type System](pydantic/pydantic/3-type-system.md)
- [Constrained Types](pydantic/pydantic/3.1-constrained-types.md)
- [Network Types](pydantic/pydantic/3.2-network-types.md)
- [TypeAdapter](pydantic/pydantic/3.3-typeadapter.md)
- [Generics and Forward References](pydantic/pydantic/3.4-generics-and-forward-references.md)
- [Validation and Serialization](pydantic/pydantic/4-validation-and-serialization.md)
- [Validators](pydantic/pydantic/4.1-validators.md)
- [Serializers](pydantic/pydantic/4.2-serializers.md)
- [JSON Conversion](pydantic/pydantic/4.3-json-conversion.md)
- [Schema Generation](pydantic/pydantic/5-schema-generation.md)
- [Core Schema Generation](pydantic/pydantic/5.1-core-schema-generation.md)
- [JSON Schema Generation](pydantic/pydantic/5.2-json-schema-generation.md)
- [Advanced Features](pydantic/pydantic/6-advanced-features.md)
- [Dataclass Support](pydantic/pydantic/6.1-dataclass-support.md)
- [Function Validation](pydantic/pydantic/6.2-function-validation.md)
- [RootModel and Computed Fields](pydantic/pydantic/6.3-rootmodel-and-computed-fields.md)
- [Plugin System](pydantic/pydantic/6.4-plugin-system.md)
- [Development and Deployment](pydantic/pydantic/7-development-and-deployment.md)
- [Testing Framework](pydantic/pydantic/7.1-testing-framework.md)
- [CI/CD Pipeline](pydantic/pydantic/7.2-cicd-pipeline.md)
- [Documentation System](pydantic/pydantic/7.3-documentation-system.md)
- [Versioning and Dependencies](pydantic/pydantic/7.4-versioning-and-dependencies.md)
- [Migration and Compatibility](pydantic/pydantic/8-migration-and-compatibility.md)
- [V1 to V2 Migration](pydantic/pydantic/8.1-v1-to-v2-migration.md)
- [Backported Modules](pydantic/pydantic/8.2-backported-modules.md)

Menu

# Documentation System

Relevant source files

- [README.md](https://github.com/pydantic/pydantic/blob/76ef0b08/README.md)
- [docs/extra/tweaks.css](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/extra/tweaks.css)
- [docs/index.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/index.md)
- [docs/install.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/install.md)
- [docs/theme/main.html](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/theme/main.html)
- [docs/why.md](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/why.md)
- [mkdocs.yml](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml)

This document describes the documentation system used by Pydantic. It covers the technical infrastructure, build tools, customizations, and workflow for maintaining and generating the Pydantic documentation found at [docs.pydantic.dev](https://docs.pydantic.dev/).

## Overview

Pydantic's documentation system is built using MkDocs with the Material theme, enhanced with custom plugins and extensions. The system provides comprehensive documentation including conceptual guides, API references, examples, error messages, and integration information.

The documentation system provides:

1. Versioned documentation (latest/stable release, development, and previous versions)
2. API documentation generated from docstrings
3. Integrated search with Algolia
4. Interactive code examples
5. Optimized presentation for both human readers and AI assistants

Sources: [mkdocs.yml1-333](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L1-L333) [README.md32-34](https://github.com/pydantic/pydantic/blob/76ef0b08/README.md#L32-L34)

## Documentation Architecture

### Documentation Build System

```
```

Sources: [mkdocs.yml189-211](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L189-L211) [docs/plugins/main.py1-43](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/plugins/main.py#L1-L43) [docs/plugins/algolia.py1-50](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/plugins/algolia.py#L1-L50)

### Documentation Structure

```
```

Sources: [mkdocs.yml89-189](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L89-L189)

## Documentation Generation Process

The documentation generation process involves several stages:

1. **Pre-build preparation**:

   - Converting `HISTORY.md` to a format suitable for the docs
   - Setting up dependencies for interactive code examples

2. **Markdown processing**:

   - Upgrading Python code examples to be compatible with different Python versions
   - Formatting JSON output for code examples
   - Rendering templates for dynamic content

3. **API documentation generation**:

   - Extracting docstrings from Python source files
   - Formatting and organizing API reference pages

4. **Output generation**:

   - Creating HTML files for web viewing
   - Generating search indices for Algolia
   - Creating LLMs.txt for AI consumption
   - Setting up redirects for backward compatibility

### Hooks and Plugins

The documentation system uses several custom hooks in the MkDocs build process:

| Hook               | Function                                         | Description                                          |
| ------------------ | ------------------------------------------------ | ---------------------------------------------------- |
| `on_pre_build`     | `add_changelog()`, `add_mkdocs_run_deps()`       | Prepares changelog and code example dependencies     |
| `on_files`         | -                                                | Processes files after loading                        |
| `on_page_markdown` | `upgrade_python()`, `insert_json_output()`, etc. | Processes Markdown content before conversion to HTML |
| `on_page_content`  | Processing for Algolia search                    | Processes HTML content for search indexing           |
| `on_post_build`    | Finalize Algolia records                         | Final processing after site generation               |

Sources: [docs/plugins/main.py37-75](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/plugins/main.py#L37-L75) [docs/plugins/algolia.py46-147](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/plugins/algolia.py#L46-L147)

### Markdown Extensions and Customization

Pydantic's documentation uses several Markdown extensions to enhance the content:

```
markdown_extensions:
- tables
- toc
- admonition
- pymdownx.details
- pymdownx.superfences
- pymdownx.highlight
- pymdownx.extra
- pymdownx.emoji
- pymdownx.tabbed
```

These extensions enable features like tables, code highlighting, tabs, admonitions, and more.

Sources: [mkdocs.yml190-205](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L190-L205)

## Documentation Versioning

Pydantic maintains versioned documentation using the `mike` plugin. This allows for multiple versions of the documentation to be available simultaneously.

```
```

The workflow for documentation updates involves:

1. Regular changes go through PRs to the `main` branch

2. On merge to `main`, the development docs are updated

3. On a new release, a new versioned docs path is created

4. Out-of-cycle documentation updates follow a special process:

   - PR against `main` with docs changes
   - Once merged, changes are cherry-picked to the `docs-update` branch
   - When merged to `docs-update`, the changes are reflected in the "latest" docs

Sources: [docs/contributing.md125-136](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/contributing.md#L125-L136) [mkdocs.yml215-218](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L215-L218)

## Search Integration

Pydantic's documentation uses Algolia for enhanced search capabilities:

1. During the build process, content is processed and indexed for search
2. Search records are created with content, titles, and URLs
3. Records are uploaded to Algolia for fast, fuzzy searching
4. The search UI is customized to match the site design

The search system provides:

- Section-based search results
- Content snippets
- Highlighted search terms
- Keyboard navigation

Sources: [docs/plugins/algolia.py1-197](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/plugins/algolia.py#L1-L197) [docs/extra/algolia.js1-108](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/extra/algolia.js#L1-L108) [docs/theme/partials/search.html1-32](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/theme/partials/search.html#L1-L32)

## LLMs Integration

Pydantic's documentation system includes a feature for generating AI-friendly documentation snapshots:

```
```

This generates an LLMs.txt file that provides a comprehensive, AI-friendly snapshot of the Pydantic documentation, making it easier for AI assistants to provide accurate information about Pydantic.

Sources: [mkdocs.yml219-237](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L219-L237) [README.md9-10](https://github.com/pydantic/pydantic/blob/76ef0b08/README.md#L9-L10)

## Code Examples Processing

Pydantic's documentation includes interactive and consistently formatted code examples:

1. **Code Example Upgrading**: The `upgrade_python()` function in `main.py` uses `pyupgrade` to optimize Python code examples for different Python versions
2. **JSON Output Formatting**: The `insert_json_output()` function replaces JSON string outputs with formatted JSON
3. **Interactive Examples**: The documentation supports running code examples in the browser

Sources: [docs/plugins/main.py133-207](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/plugins/main.py#L133-L207) [mkdocs.yml85-87](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L85-L87)

## Contributing to Documentation

Guidelines for contributing to Pydantic's documentation:

1. **Documentation Style**:

   - Written in Markdown
   - API documentation from Google-style docstrings
   - Code examples should be complete, self-contained, and runnable

2. **Testing Documentation**:

   - Code examples in documentation are tested
   - Use `pytest tests/test_docs.py --update-examples` to test and update code examples

3. **Building Documentation**:

   - Use `make docs` to build documentation
   - Use `uv run mkdocs serve` to serve documentation locally

4. **Documentation Updates**:

   - Regular updates through normal PR process
   - Out-of-cycle updates through the cherry-pick process to the `docs-update` branch

Sources: [docs/contributing.md105-137](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/contributing.md#L105-L137) [docs/contributing.md147-212](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/contributing.md#L147-L212)

## Styling and Theming

The documentation uses the Material for MkDocs theme with custom styling:

1. **Theme Customization**:

   - Custom directory: `docs/theme`
   - Custom color palette with light/dark mode support
   - Custom navigation and search features

2. **CSS Customizations**:

   - `docs/extra/terminal.css` for terminal-style displays
   - `docs/extra/tweaks.css` for general styling tweaks

3. **JavaScript Enhancements**:

   - `docs/extra/algolia.js` for search integration
   - `docs/extra/feedback.js` for user feedback
   - `docs/extra/fluff.js` for UI enhancements

The styling provides a consistent, readable experience with good support for code blocks, admonitions, and other technical content.

Sources: [mkdocs.yml6-50](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L6-L50) [docs/extra/tweaks.css1-196](https://github.com/pydantic/pydantic/blob/76ef0b08/docs/extra/tweaks.css#L1-L196)

## Redirects and URL Management

The documentation system includes extensive URL redirects to maintain backward compatibility:

```
```

This ensures that links to old documentation paths continue to work, providing a smoother experience for users transitioning from older documentation versions.

Sources: [mkdocs.yml260-332](https://github.com/pydantic/pydantic/blob/76ef0b08/mkdocs.yml#L260-L332)

Dismiss

Refresh this wiki

This wiki was recently refreshed. Please wait 4 days to refresh again.

### On this page

- [Documentation System](#documentation-system.md)
- [Overview](#overview.md)
- [Documentation Architecture](#documentation-architecture.md)
- [Documentation Build System](#documentation-build-system.md)
- [Documentation Structure](#documentation-structure.md)
- [Documentation Generation Process](#documentation-generation-process.md)
- [Hooks and Plugins](#hooks-and-plugins.md)
- [Markdown Extensions and Customization](#markdown-extensions-and-customization.md)
- [Documentation Versioning](#documentation-versioning.md)
- [Search Integration](#search-integration.md)
- [LLMs Integration](#llms-integration.md)
- [Code Examples Processing](#code-examples-processing.md)
- [Contributing to Documentation](#contributing-to-documentation.md)
- [Styling and Theming](#styling-and-theming.md)
- [Redirects and URL Management](#redirects-and-url-management.md)
