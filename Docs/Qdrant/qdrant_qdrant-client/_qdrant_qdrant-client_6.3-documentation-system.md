Documentation System | qdrant/qdrant-client | DeepWiki

[Index your code with Devin](private-repo.md)

[DeepWiki](https://deepwiki.com)

[DeepWiki](.md)

[qdrant/qdrant-client](https://github.com/qdrant/qdrant-client "Open repository")

[Index your code with](private-repo.md)

[Devin](private-repo.md)

Share

Last indexed: 9 July 2025 ([ac6f6c](https://github.com/qdrant/qdrant-client/commits/ac6f6cd2))

- [Overview](qdrant/qdrant-client/1-overview.md)
- [Client Architecture](qdrant/qdrant-client/2-client-architecture.md)
- [Client Interface](qdrant/qdrant-client/2.1-client-interface.md)
- [Local Mode](qdrant/qdrant-client/2.2-local-mode.md)
- [Remote Mode](qdrant/qdrant-client/2.3-remote-mode.md)
- [Protocol Handling](qdrant/qdrant-client/2.4-protocol-handling.md)
- [Core Operations](qdrant/qdrant-client/3-core-operations.md)
- [Search Operations](qdrant/qdrant-client/3.1-search-operations.md)
- [Collection Management](qdrant/qdrant-client/3.2-collection-management.md)
- [Point Operations](qdrant/qdrant-client/3.3-point-operations.md)
- [Advanced Features](qdrant/qdrant-client/4-advanced-features.md)
- [FastEmbed Integration](qdrant/qdrant-client/4.1-fastembed-integration.md)
- [Batch Operations](qdrant/qdrant-client/4.2-batch-operations.md)
- [Hybrid Search](qdrant/qdrant-client/4.3-hybrid-search.md)
- [Local Inference](qdrant/qdrant-client/4.4-local-inference.md)
- [Implementation Details](qdrant/qdrant-client/5-implementation-details.md)
- [Payload Filtering](qdrant/qdrant-client/5.1-payload-filtering.md)
- [Type Inspector System](qdrant/qdrant-client/5.2-type-inspector-system.md)
- [Expression Evaluation](qdrant/qdrant-client/5.3-expression-evaluation.md)
- [Development & Testing](qdrant/qdrant-client/6-development-and-testing.md)
- [Project Setup](qdrant/qdrant-client/6.1-project-setup.md)
- [Testing Framework](qdrant/qdrant-client/6.2-testing-framework.md)
- [Documentation System](qdrant/qdrant-client/6.3-documentation-system.md)

Menu

# Documentation System

Relevant source files

- [docs/source/conf.py](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py)
- [docs/source/index.rst](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst)
- [docs/source/quickstart.ipynb](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb)

The Qdrant Client documentation system generates comprehensive API documentation from Python docstrings using Sphinx. The system includes API reference documentation, interactive examples, and automated deployment to a public website.

## Documentation Architecture

The documentation system processes Python source code and generates structured HTML documentation:

```
```

Sources: [docs/source/conf.py30-37](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L30-L37) [docs/source/index.rst1-183](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L1-L183) [docs/source/quickstart.ipynb1-358](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L1-L358)

## Sphinx Configuration

The documentation system uses Sphinx with several extensions configured in `docs/source/conf.py`:

| Extension                                        | Purpose                                    |
| ------------------------------------------------ | ------------------------------------------ |
| `sphinx.ext.napoleon`                            | Parses NumPy and Google-style docstrings   |
| `sphinx.ext.autodoc`                             | Generates documentation from docstrings    |
| `sphinx.ext.viewcode`                            | Adds source code links to documentation    |
| `sphinx.ext.intersphinx`                         | Links to other Sphinx documentations       |
| `nbsphinx`                                       | Renders Jupyter notebooks as documentation |
| `IPython.sphinxext.ipython_console_highlighting` | Syntax highlighting for IPython            |

Key configuration settings:

```
```

The system uses the `qdrant_sphinx_theme` for consistent styling and excludes test files and gRPC-generated code from documentation.

Sources: [docs/source/conf.py30-37](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L30-L37) [docs/source/conf.py40-55](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L40-L55) [docs/source/conf.py71-74](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L71-L74) [docs/source/conf.py80](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L80-L80)

## Interactive Examples System

The documentation includes a comprehensive Jupyter notebook at `docs/source/quickstart.ipynb` that demonstrates:

### Installation Options

- Standard installation: `pip install qdrant-client`
- FastEmbed integration: `pip install 'qdrant-client[fastembed]'`

### Client Initialization Examples

```
```

### API Usage Patterns

The notebook demonstrates two main usage patterns:

```
```

### Code Examples Integration

The notebook includes working examples for:

- Collection creation with `VectorParams` and `Distance` enums
- Point insertion using `PointStruct`
- Search operations with `Filter`, `FieldCondition`, and `MatchValue`
- Async/await patterns for asynchronous operations

Sources: [docs/source/quickstart.ipynb40-41](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L40-L41) [docs/source/quickstart.ipynb100-108](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L100-L108) [docs/source/quickstart.ipynb210-217](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L210-L217) [docs/source/quickstart.ipynb244-257](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L244-L257)

## Documentation Generation Process

The documentation build process transforms Python source code into structured HTML documentation:

```
```

### Local Development Build

For local development, the build command generates API documentation and builds HTML output:

```
```

The `--force` flag overwrites existing files, `--separate` creates individual files for each module, and `--no-toc` excludes table of contents files.

Sources: [docs/source/conf.py71-74](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L71-L74) [docs/source/conf.py30-37](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L30-L37)

## Code Documentation Coverage

The documentation system provides comprehensive coverage of the client library's public API:

### Primary Client Classes

| Class                  | Module                              | Documentation Focus               |
| ---------------------- | ----------------------------------- | --------------------------------- |
| `QdrantClient`         | `qdrant_client.qdrant_client`       | Main synchronous client interface |
| `AsyncQdrantClient`    | `qdrant_client.async_qdrant_client` | Asynchronous client interface     |
| `QdrantFastembedMixin` | `qdrant_client.qdrant_fastembed`    | FastEmbed integration methods     |

### Data Models and Types

The documentation extensively covers data models from `qdrant_client.http.models.models`:

```
```

### Exception Handling

The system documents all exception types from `qdrant_client.http.exceptions`, providing developers with comprehensive error handling guidance.

Sources: [docs/source/index.rst146-149](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L146-L149) [docs/source/index.rst172-176](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L172-L176) [docs/source/index.rst168-182](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L168-L182)

## Documentation Theme and Styling

The documentation uses a custom theme configuration optimized for the Qdrant ecosystem:

### Theme Configuration

```
```

### Content Filtering

The documentation system excludes certain modules from generation:

```
```

This ensures the documentation focuses on the public API without including internal implementation details or test code.

Sources: [docs/source/conf.py80](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L80-L80) [docs/source/conf.py93-105](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L93-L105) [docs/source/conf.py71-74](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/conf.py#L71-L74)

## Documentation Structure

The main documentation structure is defined in `docs/source/index.rst`:

```
```

### Key Documentation Sections

The documentation includes these main sections:

| Section                 | Content                                                       | File Reference                                                                                                                  |
| ----------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Examples**            | Installation, basic usage, async client examples              | [docs/source/index.rst15-142](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L15-L142)             |
| **Highlighted Classes** | `PointStruct`, `Filter`, `VectorParams`, `BinaryQuantization` | [docs/source/index.rst146-149](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L146-L149)           |
| **API Reference**       | Individual module documentation                               | [docs/source/index.rst168-176](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L168-L176)           |
| **Quickstart Notebook** | Interactive examples with FastEmbed                           | [docs/source/quickstart.ipynb1-358](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L1-L358) |
| **Complete API**        | Full client API documentation                                 | [docs/source/index.rst178-182](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L178-L182)           |

Sources: [docs/source/index.rst151-182](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L151-L182) [docs/source/index.rst146-149](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/index.rst#L146-L149) [docs/source/quickstart.ipynb1-358](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/docs/source/quickstart.ipynb#L1-L358)

## Documentation References in Code

The README file contains references to the documentation:

```
```

This indicates that the primary documentation for the API is hosted on the website, which is automatically generated from the codebase.

Sources: [README.md32-34](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L32-L34)

## Documentation and Testing

The repository contains benchmark tests for both REST and gRPC upload operations, which include documentation in the form of comments and print statements. While these aren't part of the formal documentation system, they provide information about the performance characteristics of different API modes.

Sources: [tests/benches/test\_rest\_upload.py1-50](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/benches/test_rest_upload.py#L1-L50) [tests/benches/test\_grpc\_upload.py1-50](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/tests/benches/test_grpc_upload.py#L1-L50)

## Accessing the Documentation

Users can access the Qdrant Client documentation in several ways:

1. **Online Documentation**: The primary documentation is hosted at [python-client.qdrant.tech](https://python-client.qdrant.tech/)
2. **Local Documentation**: After building locally, documentation is available in the `docs/html` directory
3. **GitHub README**: Basic usage examples and installation instructions are provided in the README
4. **Code Docstrings**: Documentation is embedded in the code itself

Sources: [README.md21-37](https://github.com/qdrant/qdrant-client/blob/ac6f6cd2/README.md#L21-L37)

Dismiss

Refresh this wiki

Enter email to refresh

### On this page

- [Documentation System](#documentation-system.md)
- [Documentation Architecture](#documentation-architecture.md)
- [Sphinx Configuration](#sphinx-configuration.md)
- [Interactive Examples System](#interactive-examples-system.md)
- [Installation Options](#installation-options.md)
- [Client Initialization Examples](#client-initialization-examples.md)
- [API Usage Patterns](#api-usage-patterns.md)
- [Code Examples Integration](#code-examples-integration.md)
- [Documentation Generation Process](#documentation-generation-process.md)
- [Local Development Build](#local-development-build.md)
- [Code Documentation Coverage](#code-documentation-coverage.md)
- [Primary Client Classes](#primary-client-classes.md)
- [Data Models and Types](#data-models-and-types.md)
- [Exception Handling](#exception-handling.md)
- [Documentation Theme and Styling](#documentation-theme-and-styling.md)
- [Theme Configuration](#theme-configuration.md)
- [Content Filtering](#content-filtering.md)
- [Documentation Structure](#documentation-structure.md)
- [Key Documentation Sections](#key-documentation-sections.md)
- [Documentation References in Code](#documentation-references-in-code.md)
- [Documentation and Testing](#documentation-and-testing.md)
- [Accessing the Documentation](#accessing-the-documentation.md)
