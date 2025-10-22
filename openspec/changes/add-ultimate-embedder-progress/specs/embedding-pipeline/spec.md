## ADDED Requirements
### Requirement: Batch Progress Visibility
The embedder SHALL emit deterministic batch-progress metadata for every encode call, including the current batch index, total batch count, and a primary source label derived from chunk metadata, and MUST expose this metadata to both interactive progress renderers and structured telemetry so operators can correlate CLI output with run summaries.

#### Scenario: Progress label displayed in CLI
- **GIVEN** `scripts/embed_collections_v5.py` initiates the "Generating embeddings" phase
- **WHEN** the embedder processes batch `n` of `N`
- **THEN** the CLI renders a tqdm progress bar with the description `Batches(<primary_source>)`
- **AND** the bar reaches 100% when `n == N`

#### Scenario: Progress telemetry persisted
- **GIVEN** batch progress metadata is emitted during an embedding run
- **WHEN** the run summary is written to disk
- **THEN** the summary entry for the collection includes the batch label, index, and total for each processed batch

#### Scenario: Sequential ensemble progress captured
- **GIVEN** sequential ensemble mode is enabled for the embedder
- **WHEN** each ensemble pass encodes a batch
- **THEN** batch-progress telemetry is recorded for every pass so operators can audit per-model progress
