
# GEMINI.md

## Project Overview

This project is a Python-based "Universal File-to-Knowledge Converter" designed for Retrieval-Augmented Generation (RAG). It transforms various file formats (including PDFs, DOCX, and audio files) into a searchable knowledge base.

The core technologies used are:

*   **Backend:** Python with FastAPI for the API.
*   **Vector Database:** Qdrant for storing and searching vector embeddings.
*   **Containerization:** Docker and Docker Compose for orchestrating the application services.
*   **Development:** The project follows modern Python development practices, using `pyproject.toml` for dependency management, `ruff` for linting, `mypy` for type checking, and `pytest` for testing.

The architecture is modular, with separate components for document ingestion, data retrieval, and API services. The system is designed to be extensible, with a clear separation of concerns between the different parts of the application.

## Building and Running

### Docker (Recommended)

The most straightforward way to run the project is by using Docker Compose.

1.  **Start Services:**
    ```bash
    docker-compose up -d
    ```
    This command will start the Qdrant database and any other services defined in the `docker-compose.yml` file.

### Local Development

For local development, you can set up a Python virtual environment.

1.  **Create Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -e ".[dev]"
    ```

3.  **Run Tests:**
    ```bash
    pytest
    ```

4.  **Code Quality Checks:**
    ```bash
    ruff check src/
    mypy src/
    ```

## Development Conventions

*   **Configuration:** Application configuration is managed using Pydantic models and environment variables. Key configuration files are located in the `src/config` directory.
*   **Linting and Formatting:** The project uses `ruff` for linting and `black` for code formatting. Please ensure your contributions adhere to the styles defined in `pyproject.toml`.
*   **Type Checking:** `mypy` is used for static type checking. All new code should include type hints.
*   **Testing:** Tests are written using `pytest` and are located in the `tests` directory. Please add tests for any new features or bug fixes.

## Key Workflows

### Document Ingestion

The document ingestion process is handled by the `src/ingestion` module. The main components are:

*   **`ingest.py`:** Orchestrates the ingestion pipeline, from reading the source file to storing the embeddings in Qdrant.
*   **`chunker.py`:** Implements a `DoclingHybridChunker` for intelligently splitting documents into smaller chunks suitable for embedding.
*   **`embedder.py`:** Generates vector embeddings for the document chunks using a sentence-transformer model.

### Data Retrieval

The `src/retrieval` module is responsible for searching the knowledge base.

*   **`vector_search.py`:** Provides functionality to perform vector similarity searches against the Qdrant database.
*   **`hybrid_search.py`:** Implements a hybrid search strategy that can combine results from vector search with other search methods.

### Qdrant Management

The `scripts` directory contains several utility scripts for managing the Qdrant database:

*   **`check_collections.py`:** Checks the status of all collections in Qdrant.
*   **`cleanup_empty_collections.py`:** Removes any empty collections from the database.
*   **`migrate_to_coderank.py`:** A script for migrating data to a new embedding model, including creating new collections and uploading embeddings.
