# kaggle-embedding Specification

## Purpose
TBD - created by archiving change add-coderank-qdrant-embedder. Update Purpose after archive.
## Requirements
### Requirement: Qdrant Ecosystem Single-Model Embedding

The system SHALL provide a Kaggle-optimized script that processes the entire `output/qdrant_ecosystem` directory structure using the proven nomic-ai/nomic-embed-code model.

#### Scenario: Process all subdirectories under unified collection
- **GIVEN** a `output/qdrant_ecosystem` directory with 6 subdirectories (qdrant_client_docs, qdrant_documentation, qdrant_examples, qdrant_fastembed, qdrant_mcp-server-qdrant, qdrant_web_docs)
- **WHEN** the script executes on Kaggle with 2x Tesla T4 GPUs
- **THEN** all JSON chunk files from all subdirectories are embedded under a single `qdrant_ecosystem` collection
- **AND** all embeddings use nomic-ai/nomic-embed-code (768-dim vectors)
- **AND** each chunk has metadata tracking its source subdirectory
- **AND** chunk IDs follow format: `qdrant_ecosystem:{subdir}:{filename}:chunk:{index}`

#### Scenario: Use proven embedding model consistently
- **GIVEN** the embedding pipeline is initializing
- **WHEN** the model is loaded
- **THEN** nomic-ai/nomic-embed-code is used for ALL chunks
- **AND** vector dimension is 768 for ALL embeddings
- **AND** no model selection logic is needed (single model for all content)
- **AND** model memory footprint is ~6.8GB per GPU

### Requirement: GPU Memory-Aware Data Parallelism

The system SHALL utilize Kaggle's 2x Tesla T4 GPUs (15.83 GB VRAM each) efficiently while preventing OOM errors.

#### Scenario: Calculate safe batch size for nomic-embed-code
- **GIVEN** the nomic-embed-code model with 6.8GB VRAM footprint
- **WHEN** batch size calculation executes
- **THEN** batch size is computed as: `(15.83GB - 6.8GB - 2GB_buffer) / 0.15GB_per_chunk`
- **AND** calculated batch size is 46 (7.03 / 0.15)
- **AND** batch size is clamped to maximum of 24 for safety
- **AND** total VRAM usage per GPU stays below 12.4GB (3.43GB safety margin)

#### Scenario: Distribute batches across 2 GPUs with data parallelism
- **GIVEN** 2 GPUs are available and data parallelism is enabled
- **WHEN** a batch of N chunks is processed
- **THEN** model instance 1 loads on GPU 0
- **AND** model instance 2 loads on GPU 1
- **AND** first half of batch (chunks 0 to N/2-1) processes on GPU 0
- **AND** second half of batch (chunks N/2 to N-1) processes on GPU 1
- **AND** embeddings are concatenated in original order

#### Scenario: Prevent OOM with aggressive cache clearing
- **GIVEN** processing is in progress on Kaggle GPUs
- **WHEN** 5 batches have been processed
- **THEN** `torch.cuda.empty_cache()` is called on all GPUs
- **AND** GPU memory is freed for subsequent batches
- **AND** processing continues without OOM errors

### Requirement: Hierarchical Metadata Enrichment

The system SHALL enrich chunk metadata with subdirectory information for filtered search capabilities.

#### Scenario: Add subdirectory metadata to all chunks
- **GIVEN** a chunk loaded from `output/qdrant_ecosystem/qdrant_client_docs/_qdrant_qdrant-client_1-overview_chunks.json`
- **WHEN** chunk metadata is enriched
- **THEN** `metadata.collection` is set to `"qdrant_ecosystem"`
- **AND** `metadata.source_subdir` is set to `"qdrant_client_docs"`
- **AND** `metadata.source` contains the full relative path
- **AND** all original metadata from JSON is preserved

#### Scenario: Generate unique hierarchical chunk IDs
- **GIVEN** a chunk at index 5 from file `_qdrant_qdrant-client_1-overview.md` in subdirectory `qdrant_client_docs`
- **WHEN** chunk ID is generated
- **THEN** string ID is `"qdrant_ecosystem:qdrant_client_docs:_qdrant_qdrant-client_1-overview.md:chunk:5"`
- **AND** integer ID is SHA-256 hash of string ID modulo 2^63 (for Qdrant compatibility)
- **AND** ID is globally unique across all subdirectories

### Requirement: Kaggle Environment Compatibility

The system SHALL detect and adapt to Kaggle notebook environments automatically.

#### Scenario: Auto-detect Kaggle paths
- **GIVEN** script executes in Kaggle notebook environment
- **WHEN** input/output paths are configured
- **THEN** input directory is `/kaggle/working/rad_clean/output/qdrant_ecosystem` (if exists)
- **OR** fallback to local path `output/qdrant_ecosystem` (if Kaggle path not found)
- **AND** output directory is `/kaggle/working` for easy download
- **AND** embeddings JSONL file is saved to output directory

#### Scenario: Validate GPU availability and count
- **GIVEN** script starts execution
- **WHEN** GPU setup validation runs
- **THEN** CUDA availability is checked and logged
- **AND** GPU count is logged (expected: 2 for Kaggle T4 x2)
- **AND** each GPU name and VRAM capacity is logged (expected: 15.83 GB each)
- **AND** script warns if VRAM is less than 15.5 GB (may affect batch sizes)
- **AND** script aborts with clear error if no GPUs detected

#### Scenario: Report progress with ETA
- **GIVEN** processing is in progress with N total chunks
- **WHEN** each batch completes
- **THEN** progress is logged as `{processed}/{total} chunks ({percentage}%)`
- **AND** processing rate is calculated as `chunks/second`
- **AND** ETA is calculated as `(total - processed) / rate` in minutes
- **AND** user can monitor progress in Kaggle logs

### Requirement: Output Format Compatibility

The system SHALL generate output files compatible with existing Qdrant upload scripts.

#### Scenario: Generate JSONL embeddings file
- **GIVEN** all chunks have been embedded
- **WHEN** output file is saved
- **THEN** file format is JSONL (one JSON object per line)
- **AND** each line contains: `{"id": string_id, "text": content, "embedding": [float], "metadata": {...}}`
- **AND** embedding vectors have consistent dimensions (verified before save)
- **AND** file is saved as `{collection}_embeddings.jsonl`

#### Scenario: Generate processing summary JSON
- **GIVEN** embedding pipeline completes
- **WHEN** summary file is saved
- **THEN** summary contains: `collection`, `timestamp`, `model`, `vector_dimension`, `total_chunks`, `total_embeddings`
- **AND** summary contains: `processing_time_minutes`, `average_speed_chunks_per_sec`, `gpu_count`, `batch_size`
- **AND** summary contains: `subdirectories_processed` (list of 6 subdirs)
- **AND** summary contains: `chunks_per_subdirectory` (breakdown by subdir)
- **AND** file is saved as `{collection}_embedding_summary.json`

### Requirement: Error Handling and Resilience

The system SHALL handle common errors gracefully with clear error messages.

#### Scenario: Handle missing input directory
- **GIVEN** `output/qdrant_ecosystem` directory does not exist
- **WHEN** chunk loading executes
- **THEN** FileNotFoundError is raised with message: "Directory not found at {path}. Please upload the output/qdrant_ecosystem folder as a Kaggle dataset."
- **AND** script execution stops immediately
- **AND** user receives actionable error message

#### Scenario: Handle model loading failures
- **GIVEN** nomic-ai/nomic-embed-code fails to load from HuggingFace
- **WHEN** model initialization executes
- **THEN** error is logged with model name and failure reason
- **AND** script aborts with clear error message
- **AND** user is instructed to check internet connection or HuggingFace availability

#### Scenario: Handle corrupted JSON chunk files
- **GIVEN** a JSON chunk file is corrupted or malformed
- **WHEN** file loading executes
- **THEN** error is caught and logged with filename
- **AND** file is skipped (not loaded)
- **AND** processing continues with remaining files
- **AND** summary reports number of skipped files

### Requirement: Future Reranking Support

The system documentation SHALL describe reranking as a future enhancement for improved search accuracy.

#### Scenario: Document reranking approach
- **GIVEN** the script documentation is being written
- **WHEN** future enhancements are described
- **THEN** reranking is documented as 2-stage retrieval approach
- **AND** CrossEncoder model (e.g., ms-marco-MiniLM-L-6-v2) is recommended
- **AND** reranking is described as post-search step (not during embedding)
- **AND** example code shows Qdrant search → rerank top-K → return final results

#### Scenario: Reranking does not affect embedding pipeline
- **GIVEN** reranking is a future enhancement
- **WHEN** the embedding script executes
- **THEN** no reranking code is present in the script
- **AND** embeddings are generated without reranking overhead
- **AND** reranking can be added later without re-embedding data

