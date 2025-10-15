"""Utility functions for uploading embeddings to Qdrant."""

import hashlib
import json
import logging
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    HnswConfigDiff,
    PointStruct,
    Filter,
)

from src.config.qdrant_upload import QdrantUploadConfig

logger = logging.getLogger(__name__)


def string_to_uuid(text: str) -> str:
    """Convert a string to a deterministic UUID.
    
    Args:
        text: String to convert
        
    Returns:
        UUID string (deterministic hash of input)
    """
    # Use MD5 hash for deterministic UUID generation
    hash_digest = hashlib.md5(text.encode('utf-8')).digest()
    return str(uuid.UUID(bytes=hash_digest))


@dataclass
class UploadStats:
    """Statistics for embedding upload process."""
    
    total_lines: int = 0
    inserted: int = 0
    skipped: int = 0
    failed: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    
    @property
    def elapsed(self) -> float:
        """Calculate elapsed time in seconds."""
        return self.end_time - self.start_time if self.end_time > 0 else 0.0
    
    @property
    def qps(self) -> float:
        """Calculate queries per second (throughput)."""
        return self.inserted / self.elapsed if self.elapsed > 0 else 0.0
    
    def __str__(self) -> str:
        """Pretty print statistics."""
        return (
            f"UploadStats(total={self.total_lines}, inserted={self.inserted}, "
            f"skipped={self.skipped}, failed={self.failed}, "
            f"elapsed={self.elapsed:.1f}s, qps={self.qps:.1f})"
        )


@dataclass
class ValidationResult:
    """Result of post-upload validation."""
    
    collection_count: int
    expected_count: int
    count_match: bool
    sample_search_success: bool
    errors: list[str]


def assert_health(client: QdrantClient) -> None:
    """Verify Qdrant is reachable and healthy.
    
    Args:
        client: Qdrant client instance
        
    Raises:
        ConnectionError: If Qdrant is unreachable or unhealthy
    """
    try:
        client.get_collections()
        logger.info("✓ Qdrant health check passed")
    except Exception as e:
        raise ConnectionError(f"Qdrant health check failed: {e}")


def ensure_collection(
    client: QdrantClient,
    config: QdrantUploadConfig,
    force: bool = False
) -> None:
    """Create collection or verify existing schema.
    
    Steps:
    1. Check if collection exists
    2. If exists, validate vector dimension
    3. If dimension mismatch and force=True, recreate collection
    4. If dimension mismatch and force=False, raise error
    5. If not exists, create with proper config
    6. Create payload indexes for indexed_fields
    
    Args:
        client: Qdrant client instance
        config: Upload configuration
        force: If True, recreate collection on dimension mismatch
        
    Raises:
        ValueError: Dimension mismatch without force flag
    """
    collection_name = config.collection_name
    
    # Check if collection exists
    collections = client.get_collections().collections
    exists = any(col.name == collection_name for col in collections)
    
    if exists:
        # Validate vector dimension
        collection_info = client.get_collection(collection_name)
        existing_dim = collection_info.config.params.vectors.size
        
        if existing_dim != config.vector_dim:
            if force:
                logger.warning(
                    f"⚠ Recreating collection due to dimension mismatch "
                    f"({existing_dim} → {config.vector_dim})"
                )
                client.delete_collection(collection_name)
                exists = False  # Recreate below
            else:
                raise ValueError(
                    f"Vector dimension mismatch: collection has {existing_dim}, "
                    f"embeddings have {config.vector_dim}. "
                    f"Use --force to recreate collection."
                )
    
    if not exists:
        # Create collection with proper configuration
        logger.info(f"Creating collection '{collection_name}' with dimension {config.vector_dim}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=config.vector_dim,
                distance=config.distance_metric
            ),
            hnsw_config=HnswConfigDiff(
                m=16,
                ef_construct=100
            )
        )
    
    # Create payload indexes for frequently queried fields
    for field in config.indexed_fields:
        try:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema="keyword"
            )
            logger.debug(f"Created index on field '{field}'")
        except Exception as e:
            # Index might already exist
            logger.debug(f"Index creation for '{field}' skipped: {e}")
    
    logger.info(f"✓ Collection '{collection_name}' ready")


def truncate_collection(
    client: QdrantClient,
    collection_name: str,
    force: bool = False
) -> int:
    """Delete all points from collection.
    
    Args:
        client: Qdrant client instance
        collection_name: Collection to truncate
        force: Skip confirmation if True
        
    Returns:
        Number of points deleted
    """
    # Get current count
    count_result = client.count(collection_name)
    current_count = count_result.count
    
    if current_count == 0:
        logger.info(f"Collection '{collection_name}' is already empty")
        return 0
    
    # Prompt for confirmation unless force is True
    if not force:
        response = input(f"Delete {current_count} points from {collection_name}? [y/N] ")
        if response.lower() not in ['y', 'yes']:
            logger.info("Truncation cancelled by user")
            raise SystemExit(0)
    
    # Delete all points
    client.delete(
        collection_name=collection_name,
        points_selector=Filter()  # Empty filter selects all
    )
    
    logger.info(f"✓ Truncated {current_count} points")
    return current_count


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
    
    Args:
        client: Qdrant client instance
        config: Upload configuration
        
    Returns:
        UploadStats with metrics
    """
    stats = UploadStats(start_time=time.time())
    
    # Batch accumulation
    batch_ids = []
    batch_vectors = []
    batch_payloads = []
    
    last_log_time = time.time()
    last_log_count = 0
    
    def upsert_batch():
        """Upsert current batch with retry logic."""
        nonlocal last_log_time, last_log_count
        
        if not batch_ids:
            return
        
        for attempt in range(config.max_retries):
            try:
                points = [
                    PointStruct(id=id_, vector=vec, payload=payload)
                    for id_, vec, payload in zip(batch_ids, batch_vectors, batch_payloads)
                ]
                
                if not config.dry_run:
                    client.upsert(
                        collection_name=config.collection_name,
                        points=points
                    )
                
                stats.inserted += len(batch_ids)
                
                # Progress logging every 1000 records or 5 seconds
                current_time = time.time()
                if (stats.inserted - last_log_count >= 1000 or 
                    current_time - last_log_time >= 5):
                    elapsed = current_time - stats.start_time
                    qps = stats.inserted / elapsed if elapsed > 0 else 0
                    logger.info(
                        f"Progress: {stats.inserted}/{stats.total_lines} records "
                        f"({stats.inserted/stats.total_lines*100:.1f}%) - {qps:.0f} qps"
                    )
                    last_log_time = current_time
                    last_log_count = stats.inserted
                
                break  # Success
                
            except Exception as e:
                if attempt == config.max_retries - 1:
                    logger.error(f"Batch upsert failed after {config.max_retries} attempts: {e}")
                    stats.failed += len(batch_ids)
                    raise
                else:
                    delay = config.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Retry {attempt + 1}/{config.max_retries} for batch "
                        f"starting at record {stats.inserted} after {delay}s delay"
                    )
                    time.sleep(delay)
        
        # Clear batch
        batch_ids.clear()
        batch_vectors.clear()
        batch_payloads.clear()
    
    # Read and process JSONL
    logger.info(f"Reading embeddings from {config.embeddings_path}")
    
    with open(config.embeddings_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            stats.total_lines += 1
            
            try:
                # Parse JSON
                record = json.loads(line.strip())
                
                # Validate required fields
                required_fields = ['id', 'embedding', 'metadata', 'text']
                missing = [field for field in required_fields if field not in record]
                if missing:
                    logger.warning(
                        f"⚠ Skipping malformed record at line {line_num}: "
                        f"missing fields {missing}"
                    )
                    stats.skipped += 1
                    continue
                
                # Validate embedding dimension
                embedding = record['embedding']
                if len(embedding) != config.vector_dim:
                    logger.warning(
                        f"⚠ Skipping malformed record at line {line_num}: "
                        f"embedding dimension mismatch ({len(embedding)} != {config.vector_dim})"
                    )
                    stats.skipped += 1
                    continue
                
                # Prepare payload (metadata + text)
                payload = {**record['metadata'], 'text': record['text']}
                
                # Convert string ID to UUID (Qdrant requires UUID or integer IDs)
                point_id = record['id']
                if isinstance(point_id, str):
                    point_id = string_to_uuid(point_id)
                
                # Store original ID in payload for reference
                payload['original_id'] = record['id']
                
                # Add to batch
                batch_ids.append(point_id)
                batch_vectors.append(embedding)
                batch_payloads.append(payload)
                
                # Upsert when batch is full
                if len(batch_ids) >= config.batch_size:
                    upsert_batch()
                    
            except json.JSONDecodeError as e:
                logger.warning(f"⚠ Skipping invalid JSON at line {line_num}: {e}")
                stats.skipped += 1
            except Exception as e:
                logger.error(f"Error processing line {line_num}: {e}")
                stats.skipped += 1
    
    # Upsert final partial batch
    if batch_ids:
        logger.debug(f"Uploading final partial batch of {len(batch_ids)} records")
        upsert_batch()
    
    stats.end_time = time.time()
    logger.info(f"✓ Upload complete: {stats}")
    
    return stats


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
    
    Args:
        client: Qdrant client instance
        config: Upload configuration
        stats: Upload statistics
        
    Returns:
        ValidationResult with detailed metrics
    """
    errors = []
    
    # Check collection count
    collection_count = client.count(config.collection_name).count
    expected_count = stats.inserted
    
    # Load summary JSON if exists
    if config.summary_path and config.summary_path.exists():
        try:
            with open(config.summary_path, 'r') as f:
                summary = json.load(f)
                summary_total = summary.get('total_chunks', 0)
                if summary_total != collection_count:
                    errors.append(
                        f"Summary file expects {summary_total}, "
                        f"but collection has {collection_count}"
                    )
                expected_count = summary_total
        except Exception as e:
            logger.warning(f"Could not load summary file: {e}")
    
    # Check count match
    count_match = collection_count == expected_count
    if not count_match:
        diff = expected_count - collection_count
        errors.append(
            f"Count mismatch: expected {expected_count}, got {collection_count} "
            f"({abs(diff)} points {'missing' if diff > 0 else 'extra'})"
        )
    
    # Sample search test
    sample_search_success = False
    try:
        # Get first point
        scroll_result = client.scroll(
            collection_name=config.collection_name,
            limit=1,
            with_vectors=True
        )
        
        if scroll_result[0]:  # Has points
            first_point = scroll_result[0][0]
            sample_vector = first_point.vector
            
            # Search with sample vector
            search_results = client.search(
                collection_name=config.collection_name,
                query_vector=sample_vector,
                limit=5
            )
            
            sample_search_success = len(search_results) > 0
            if not sample_search_success:
                errors.append("Sample search failed: no results returned")
        else:
            errors.append("Cannot perform sample search: collection is empty")
            
    except Exception as e:
        errors.append(f"Sample search failed: {e}")
        sample_search_success = False
    
    return ValidationResult(
        collection_count=collection_count,
        expected_count=expected_count,
        count_match=count_match,
        sample_search_success=sample_search_success,
        errors=errors
    )
