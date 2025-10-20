## ADDED Requirements
### Requirement: Resilient Collection Discovery
The batch embedding runner script (`scripts/embed_collections_v5.py`) MUST only schedule top-level directories that contain chunk JSON files (matching `*_chunks.json`) or nested folders that contain them, and it MUST respect any explicit allow list provided by the caller. Directories without chunk files MUST be logged and marked as skipped without invoking the embedder.

#### Scenario: Autodiscover nested chunk directories
- **WHEN** the runner scans a chunks root that contains multiple collections with chunk files inside nested subdirectories
- **THEN** it schedules only the directories that contain chunk JSON payloads
- **AND** directories that contain only summaries or other JSON artifacts are ignored

#### Scenario: Skip missing allow-listed collections
- **GIVEN** the user passes `--collections` with a directory name that does not contain any chunk JSON files
- **WHEN** discovery executes
- **THEN** the runner logs a warning about the missing collection
- **AND** the run summary records the collection with `status="skipped_no_chunks"`

### Requirement: Embedder Path Resolution
The Kaggle embedder implementation (`processor/kaggle_ultimate_embedder_v4.py`) MUST honour the explicit `chunks_dir` argument on both Kaggle and local runs, only falling back to heuristics when that path is missing. Repository-specific absolute paths MUST NOT override caller input.

#### Scenario: Local override respected
- **GIVEN** the embedder is running outside the Kaggle environment
- **WHEN** `load_chunks_from_processing` receives an absolute chunks directory
- **THEN** the embedder attempts to load chunk files from that directory first
- **AND** only falls back to heuristic discovery when the explicit path is absent or empty

### Requirement: Structured Run Summary
The batch runner script (`scripts/embed_collections_v5.py`) MUST emit a structured JSON summary describing each collection processed (or skipped) and the embedder (`processor/kaggle_ultimate_embedder_v4.py`) MUST surface the data needed to populate that summary without additional scraping.

#### Scenario: Successful run summary emission
- **WHEN** a collection completes successfully
- **THEN** the saved summary item includes `status="completed"`, the total chunk count, export artifact paths, and the resolved Qdrant collection name
- **AND** the overall summary file is written to the requested location
