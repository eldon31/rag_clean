
#!/usr/bin/env python3
"""CLI tool to upload pre-generated embeddings (JSONL) into Qdrant.

Usage:
    python scripts/upload_qdrant_embeddings.py \\
        --embeddings output/embed/qdrant_ecosystem_embeddings.jsonl \\
        --collection qdrant_ecosystem \\
        --verbose

    python scripts/upload_qdrant_embeddings.py --truncate --force
"""

import argparse
import logging
import sys
from pathlib import Path

from qdrant_client import QdrantClient

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.qdrant_upload import QdrantUploadConfig
from src.storage.upload_utils import (
    assert_health,
    ensure_collection,
    truncate_collection,
    stream_embeddings_to_qdrant,
    validate_ingestion,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Upload embeddings from JSONL to Qdrant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic upload
  python scripts/upload_qdrant_embeddings.py

  # Upload to custom collection
  python scripts/upload_qdrant_embeddings.py \\
      --collection my_collection \\
      --embeddings path/to/embeddings.jsonl

  # Truncate and upload with force (no prompts)
  python scripts/upload_qdrant_embeddings.py --truncate --force

  # Dry run (validate without uploading)
  python scripts/upload_qdrant_embeddings.py --dry-run --verbose

Environment Variables:
  QDRANT_URL         Qdrant server URL (default: http://localhost:6333)
  QDRANT_API_KEY     API key for authentication (optional)
  QDRANT_COLLECTION  Target collection name (default: qdrant_ecosystem)
  QDRANT_TIMEOUT     Connection timeout in seconds (default: 60)
        """
    )
    
    # Connection arguments
    parser.add_argument(
        "--url",
        type=str,
        help="Qdrant server URL (env: QDRANT_URL, default: http://localhost:6333)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Qdrant API key (env: QDRANT_API_KEY)"
    )
    
    # Collection arguments
    parser.add_argument(
        "--collection",
        type=str,
        help="Target collection name (env: QDRANT_COLLECTION, default: qdrant_ecosystem)"
    )
    
    # Upload arguments
    parser.add_argument(
        "--embeddings",
        type=Path,
        help="Path to embeddings JSONL file (default: output/embed/qdrant_ecosystem_embeddings.jsonl)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Upsert batch size (default: 256)"
    )
    
    # Behavior flags
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Delete all points before upload"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts and recreate on dimension mismatch"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate without uploading to Qdrant"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG logging"
    )
    
    return parser.parse_args()


def main():
    """Main CLI entrypoint."""
    # 1. Parse arguments
    args = parse_args()
    
    # 2. Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    
    # 3. Load config from environment
    config = QdrantUploadConfig.from_env()
    
    # 4. Override with CLI arguments
    if args.url:
        config.url = args.url
    if args.api_key:
        config.api_key = args.api_key
    if args.collection:
        config.collection_name = args.collection
    if args.embeddings:
        config.embeddings_path = args.embeddings
    if args.batch_size:
        config.batch_size = args.batch_size
    
    config.truncate_before_upload = args.truncate
    config.force = args.force
    config.dry_run = args.dry_run
    config.verbose = args.verbose
    
    # Re-run post_init to update derived paths
    config.__post_init__()
    
    logger.info("=" * 60)
    logger.info("Qdrant Embedding Upload")
    logger.info("=" * 60)
    logger.info(f"Server: {config.url}")
    logger.info(f"Collection: {config.collection_name}")
    logger.info(f"Embeddings: {config.embeddings_path}")
    logger.info(f"Batch size: {config.batch_size}")
    if config.dry_run:
        logger.info("Mode: DRY RUN (no actual upload)")
    logger.info("=" * 60)
    
    # 5. Validate inputs
    if not config.embeddings_path.exists():
        logger.error(f"✗ Embeddings file not found: {config.embeddings_path}")
        sys.exit(1)
    
    # 6. Connect to Qdrant
    try:
        client = QdrantClient(
            url=config.url,
            api_key=config.api_key,
            timeout=config.timeout
        )
    except Exception as e:
        logger.error(f"✗ Failed to create Qdrant client: {e}")
        sys.exit(2)
    
    # 7. Health check
    try:
        assert_health(client)
        logger.info(f"✓ Connected to Qdrant at {config.url}")
    except ConnectionError as e:
        logger.error(f"✗ {e}")
        logger.error("  → Check that Qdrant is running: docker compose up -d qdrant")
        logger.error(f"  → Verify URL is correct: {config.url}")
        sys.exit(2)
    
    # 8. Collection setup
    try:
        ensure_collection(client, config, force=args.force)
    except ValueError as e:
        logger.error(f"✗ {e}")
        logger.error("  → Use --force to recreate collection with correct dimension")
        sys.exit(3)
    except Exception as e:
        logger.error(f"✗ Collection setup failed: {e}")
        sys.exit(3)
    
    # 9. Optional truncation
    if config.truncate_before_upload:
        try:
            deleted = truncate_collection(
                client,
                config.collection_name,
                force=config.force
            )
            if deleted > 0:
                logger.info(f"✓ Truncated {deleted} points")
        except SystemExit:
            # User cancelled truncation
            raise
        except Exception as e:
            logger.error(f"✗ Truncation failed: {e}")
            sys.exit(4)
    
    # 10. Upload
    if config.dry_run:
        logger.info("DRY RUN: Reading and validating embeddings without upload...")
    
    try:
        stats = stream_embeddings_to_qdrant(client, config)
        logger.info(
            f"✓ Upload complete: {stats.inserted} points in {stats.elapsed:.1f}s "
            f"({stats.qps:.1f} qps)"
        )
        if stats.skipped > 0:
            logger.warning(f"⚠ Skipped {stats.skipped} malformed records")
    except Exception as e:
        logger.error(f"✗ Upload failed: {e}")
        logger.error("  → Check logs above for details")
        logger.error("  → Verify JSONL format is correct")
        sys.exit(4)
    
    # 11. Validate
    if config.dry_run:
        logger.info("DRY RUN: Skipping validation (no data uploaded)")
    else:
        logger.info("Validating upload...")
        try:
            result = validate_ingestion(client, config, stats)
            
            if result.count_match and result.sample_search_success:
                logger.info("✓ Validation passed")
                logger.info(f"  Collection count: {result.collection_count}")
                logger.info(f"  Expected: {result.expected_count}")
                logger.info(f"  Sample search: ✓")
            else:
                logger.error("✗ Validation failed")
                for err in result.errors:
                    logger.error(f"  - {err}")
                sys.exit(5)
        except Exception as e:
            logger.error(f"✗ Validation error: {e}")
            sys.exit(5)
    
    # 12. Success
    logger.info("=" * 60)
    logger.info("✅ All done!")
    logger.info(f"Collection '{config.collection_name}' is ready for queries")
    logger.info(f"Dashboard: {config.url}/dashboard")
    logger.info("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
