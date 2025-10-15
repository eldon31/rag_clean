# Specification: Qdrant Embedding Upload CLI

## Overview

This specification defines the implementation details for `scripts/upload_qdrant_embeddings.py`, a standalone CLI tool that ingests embedding artifacts (JSONL format) into a Qdrant vector database with validation, progress tracking, and error handling.

## File Structure

```
scripts/
  upload_qdrant_embeddings.py          # Main CLI entrypoint
src/
  config/
    qdrant_upload.py                   # Configuration dataclass
  storage/
    upload_utils.py                    # Helper functions for validation/streaming
tests/
  integration/
    test_qdrant_upload.py              # Integration tests
    fixtures/
      sample_embeddings.jsonl          # 20-record test fixture
```

## 1. Configuration (`src/config/qdrant_upload.py`)

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict
from qdrant_client.models import Distance

@dataclass
class QdrantUploadConfig:
    """Configuration for Qdrant embedding upload process."""
    
    # Connection
    url: str = "http://localhost:6333"
    api_key: Optional[str] = None
    timeout: int = 60
    
    # Collection settings
    collection_name: str = "qdrant_ecosystem"
    vector_dim: int = 768
    distance_metric: Distance = Distance.COSINE
    
    # Payload schema (for indexing)
    indexed_fields: list[str] = field(default_factory=lambda: [
        "subdirectory",
        "source_file",
        "source_path"
    ])
    
    # Upload settings
    embeddings_path: Path = Path("output/embed/qdrant_ecosystem_embeddings.jsonl")
    summary_path: Optional[Path] = None  # Auto-derived from embeddings_path
    batch_size: int = 256
    max_retries: int = 3
    retry_delay: float = 0.5
    
    # Flags
    truncate_before_upload: bool = False
    force: bool = False  # Skip confirmations
    dry_run: bool = False
    verbose: bool = False
    
    def __post_init__(self):
        """Derive summary path if not provided."""
        if self.summary_path is None:
            base = self.embeddings_path.stem
            self.summary_path = self.embeddings_path.parent / f"{base}_summary.json"
        
        # Convert string paths to Path objects
        self.embeddings_path = Path(self.embeddings_path)
        if self.summary_path:
            self.summary_path = Path(self.summary_path)
    
    @classmethod
    def from_env(cls) -> "QdrantUploadConfig":
        """Load config from environment variables."""
        import os
        return cls(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=os.getenv("QDRANT_COLLECTION", "qdrant_ecosystem"),
        )
```

## 2. CLI Interface (`scripts/upload_qdrant_embeddings.py`)

### Command Signature

```bash
python scripts/upload_qdrant_embeddings.py \
  --embeddings output/embed/qdrant_ecosystem_embeddings.jsonl \
  --collection qdrant_ecosystem \
  --url http://localhost:6333 \
  --batch-size 256 \
  [--truncate] \
  [--force] \
  [--dry-run] \
  [--verbose]
```

### Argument Parsing

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--embeddings` | Path | `output/embed/qdrant_ecosystem_embeddings.jsonl` | Input JSONL file |
| `--collection` | str | `qdrant_ecosystem` | Target collection name |
| `--url` | str | `http://localhost:6333` | Qdrant server URL |
| `--api-key` | str | `None` | API key (or use `QDRANT_API_KEY` env) |
| `--batch-size` | int | `256` | Upsert batch size |
| `--truncate` | flag | `False` | Delete all points before upload |
| `--force` | flag | `False` | Skip confirmation prompts |
| `--dry-run` | flag | `False` | Validate without uploading |
| `--verbose` | flag | `False` | Enable DEBUG logging |

### Exit Codes

- `0`: Success
- `1`: Configuration error (missing file, invalid args)
- `2`: Connection error (Qdrant unreachable)
- `3`: Schema error (dimension mismatch, invalid collection)
- `4`: Upload error (failed after retries)
- `5`: Validation error (post-upload count mismatch)

## 3. Implementation Functions

### 3.1 Health Check

```python
def assert_health(client: QdrantClient) -> None:
    """Verify Qdrant is reachable and healthy.
    
    Raises:
        ConnectionError: If Qdrant is unreachable
    """
    try:
        client.get_collections()
    except Exception as e:
        raise ConnectionError(f"Qdrant health check failed: {e}")
```

### 3.2 Collection Management

```python
def ensure_collection(
    client: QdrantClient,
    config: QdrantUploadConfig,
    force: bool = False
) -> None:
    """Create collection or verify existing schema.
    
    Steps:
    1. Check if collection exists
    2. If exists, validate vector dimension
    3. If dimension mismatch and not force, raise error
    4. If force, recreate collection
    5. If not exists, create with proper config
    6. Create payload indexes for indexed_fields
    
    Args:
        client: Qdrant client
        config: Upload configuration
        force: If True, recreate on dimension mismatch
        
    Raises:
        ValueError: Dimension mismatch without force flag
    """
```

Implementation:
- Use `client.get_collection(name)` to check existence
- Compare `vectors_config.size` with `config.vector_dim`
- Create collection with:
  - `vectors_config=VectorParams(size=768, distance=Distance.COSINE)`
  - HNSW config: `hnsw_config=HnswConfigDiff(m=16, ef_construct=100)`
- Create indexes via `client.create_payload_index(collection, field, schema_type)`

### 3.3 Truncation (Optional)

```python
def truncate_collection(
    client: QdrantClient,
    collection_name: str,
    force: bool = False
) -> int:
    """Delete all points from collection.
    
    Args:
        client: Qdrant client
        collection_name: Collection to truncate
        force: Skip confirmation if True
        
    Returns:
        Number of points deleted
    """
```

Implementation:
- Get current count via `client.count(collection_name)`
- If not force, prompt: `f"Delete {count} points from {collection_name}? [y/N] "`
- Execute: `client.delete(collection_name, points_selector=FilterSelector(filter=Filter()))`
- Return deleted count

### 3.4 Embedding Streamer

```python
@dataclass
class UploadStats:
    total_lines: int = 0
    inserted: int = 0
    skipped: int = 0
    failed: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    
    @property
    def elapsed(self) -> float:
        return self.end_time - self.start_time
    
    @property
    def qps(self) -> float:
        return self.inserted / self.elapsed if self.elapsed > 0 else 0.0

def stream_embeddings_to_qdrant(
    client: QdrantClient,
    config: QdrantUploadConfig
) -> UploadStats:
    """Stream embeddings from JSONL into Qdrant with batching and retries.
    
    JSONL Format (per line):
    {
        "id": "file_abc_chunk_0",
        "embedding": [0.123, -0.456, ...],  # 768-dim
        "metadata": {
            "subdirectory": "qdrant_client_docs",
            "source_file": "overview.md",
            "source_path": "docs/overview.md",
            "chunk_index": 0
        },
        "text": "Chunk content here..."
    }
    
    Returns:
        UploadStats with metrics
    """
```

Implementation Details:
1. **Read JSONL**: Use `with open(path) as f: for line in f:`
2. **Parse & validate**:
   - `record = json.loads(line)`
   - Check required fields: `id`, `embedding`, `metadata`, `text`
   - Validate `len(embedding) == config.vector_dim`
   - Skip malformed with warning log
3. **Batch accumulation**:
   - Collect into `ids`, `vectors`, `payloads` lists
   - When batch reaches `config.batch_size`, upsert
4. **Upsert with retry**:
   ```python
   for attempt in range(config.max_retries):
       try:
           client.upsert(
               collection_name=config.collection_name,
               points=Batch(ids=ids, vectors=vectors, payloads=payloads)
           )
           break
       except Exception as e:
           if attempt == config.max_retries - 1:
               raise
           time.sleep(config.retry_delay * (2 ** attempt))
   ```
5. **Progress logging**: Every 1000 records or 5 seconds
6. **Final batch**: Upsert remaining records after loop

### 3.5 Post-Upload Validation

```python
@dataclass
class ValidationResult:
    collection_count: int
    expected_count: int
    count_match: bool
    sample_search_success: bool
    errors: list[str]

def validate_ingestion(
    client: QdrantClient,
    config: QdrantUploadConfig,
    stats: UploadStats
) -> ValidationResult:
    """Validate upload succeeded.
    
    Checks:
    1. Point count matches inserted count
    2. Summary JSON total (if exists) matches collection count
    3. Sample search returns results
    
    Returns:
        ValidationResult with detailed metrics
    """
```

Steps:
1. `collection_count = client.count(config.collection_name).count`
2. Load summary JSON if exists, extract `total_chunks`
3. Compare `collection_count` vs `stats.inserted` vs `summary.total_chunks`
4. Run sample search:
   - Get first point via `client.scroll(limit=1)`
   - Search with its vector: `client.search(vector=vec, limit=5)`
   - Confirm results returned
5. Return validation result

## 4. Main CLI Flow

```python
def main():
    # 1. Parse args
    args = parse_args()
    
    # 2. Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    # 3. Load config
    config = QdrantUploadConfig.from_env()
    # Override with CLI args
    config.embeddings_path = args.embeddings
    config.collection_name = args.collection
    # ... etc
    
    # 4. Validate inputs
    if not config.embeddings_path.exists():
        logging.error(f"Embeddings file not found: {config.embeddings_path}")
        sys.exit(1)
    
    # 5. Connect to Qdrant
    client = QdrantClient(url=config.url, api_key=config.api_key, timeout=config.timeout)
    
    # 6. Health check
    try:
        assert_health(client)
        logging.info(f"✓ Connected to Qdrant at {config.url}")
    except ConnectionError as e:
        logging.error(f"✗ {e}")
        sys.exit(2)
    
    # 7. Collection setup
    try:
        ensure_collection(client, config, force=args.force)
        logging.info(f"✓ Collection '{config.collection_name}' ready")
    except ValueError as e:
        logging.error(f"✗ {e}")
        sys.exit(3)
    
    # 8. Optional truncation
    if config.truncate_before_upload:
        deleted = truncate_collection(client, config.collection_name, force=args.force)
        logging.info(f"✓ Truncated {deleted} points")
    
    # 9. Upload
    if config.dry_run:
        logging.info("DRY RUN: Skipping upload")
        sys.exit(0)
    
    try:
        stats = stream_embeddings_to_qdrant(client, config)
        logging.info(f"✓ Upload complete: {stats.inserted} points in {stats.elapsed:.1f}s ({stats.qps:.1f} qps)")
    except Exception as e:
        logging.error(f"✗ Upload failed: {e}")
        sys.exit(4)
    
    # 10. Validate
    result = validate_ingestion(client, config, stats)
    if result.count_match and result.sample_search_success:
        logging.info("✓ Validation passed")
        logging.info(f"  Collection count: {result.collection_count}")
        logging.info(f"  Expected: {result.expected_count}")
    else:
        logging.error("✗ Validation failed")
        for err in result.errors:
            logging.error(f"  - {err}")
        sys.exit(5)
    
    # 11. Success
    logging.info("✅ All done!")
    sys.exit(0)
```

## 5. Testing

### Unit Tests
- Config parsing from env vars
- Batch accumulation logic
- Retry exponential backoff

### Integration Test (`tests/integration/test_qdrant_upload.py`)

```python
def test_full_upload_flow(qdrant_docker):
    """End-to-end upload test with fixture data."""
    # Given: 20-record fixture JSONL
    fixture_path = Path("tests/integration/fixtures/sample_embeddings.jsonl")
    
    # When: Upload
    config = QdrantUploadConfig(
        url="http://localhost:6333",
        collection_name="test_upload",
        embeddings_path=fixture_path,
        batch_size=10
    )
    client = QdrantClient(url=config.url)
    
    ensure_collection(client, config)
    stats = stream_embeddings_to_qdrant(client, config)
    
    # Then: Verify
    assert stats.inserted == 20
    assert stats.skipped == 0
    assert client.count("test_upload").count == 20
    
    # Cleanup
    client.delete_collection("test_upload")
```

## 6. Documentation Updates

Add to `README.md`:

```markdown
### Uploading Embeddings to Qdrant

After generating embeddings (e.g., via Kaggle), upload them:

\```bash
# Start Qdrant (if not running)
docker compose up -d qdrant

# Upload
python scripts/upload_qdrant_embeddings.py \
  --embeddings output/embed/qdrant_ecosystem_embeddings.jsonl \
  --collection qdrant_ecosystem \
  --verbose

# With truncation (careful!)
python scripts/upload_qdrant_embeddings.py \
  --embeddings output/embed/qdrant_ecosystem_embeddings.jsonl \
  --truncate \
  --force
\```

See `scripts/upload_qdrant_embeddings.py --help` for all options.
```

## 7. Dependencies

Ensure in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
qdrant-client = "^1.9.0"
tqdm = "^4.66.0"  # Optional, for progress bars
```

## Acceptance Criteria

- [ ] CLI accepts all specified arguments
- [ ] Environment variables override defaults
- [ ] Health check fails fast on connection error
- [ ] Collection creation with correct vector dimension
- [ ] Dimension mismatch detected and reported
- [ ] Truncate flag prompts for confirmation (unless --force)
- [ ] Batched upserts with progress logging
- [ ] Retry logic handles transient errors
- [ ] Post-upload validation compares counts
- [ ] Sample search confirms data is searchable
- [ ] Dry-run mode validates without uploading
- [ ] Exit codes match specification
- [ ] Integration test passes with docker Qdrant
- [ ] README documentation added
