"""
Enable quantization on existing 768-dim collections.

This script enables binary quantization on already-migrated collections
to achieve 40x query speedup.

USAGE:
    # Enable on all collections
    python scripts/enable_quantization.py --all
    
    # Enable on specific collection
    python scripts/enable_quantization.py --collection qdrant_ecosystem
    
    # Dry run
    python scripts/enable_quantization.py --all --dry-run
"""

import os
import argparse
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import (
    BinaryQuantization,
    BinaryQuantizationConfig,
    ScalarQuantization,
    ScalarQuantizationConfig,
    ScalarType,
    QuantizationConfig
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Collections to enable quantization on
COLLECTIONS = ["qdrant_ecosystem", "docling", "sentence_transformers"]


def enable_quantization(client: QdrantClient, collection_name: str, dry_run: bool = False):
    """Enable binary quantization with scalar fallback."""
    logger.info(f"\n📦 Processing: {collection_name}")
    
    # Check collection exists
    try:
        info = client.get_collection(collection_name)
        logger.info(f"  ✅ Collection found: {info.points_count} points")
    except Exception as e:
        logger.error(f"  ❌ Collection not found: {e}")
        return False
    
    if dry_run:
        logger.info(f"  🔍 [DRY RUN] Would enable binary quantization")
        return True
    
    # Try binary quantization
    try:
        client.update_collection(
            collection_name=collection_name,
            quantization_config=BinaryQuantization(
                binary=BinaryQuantizationConfig(
                    always_ram=True
                )
            )
        )
        logger.info(f"  ✅ Binary quantization enabled (40x speedup)")
        return True
    except Exception as e:
        logger.warning(f"  ⚠️  Binary quantization failed: {e}")
        logger.info(f"  Trying scalar quantization...")
        
        # Fallback to scalar
        try:
            client.update_collection(
                collection_name=collection_name,
                quantization_config=ScalarQuantization(
                    scalar=ScalarQuantizationConfig(
                        type=ScalarType.INT8,
                        quantile=0.99,
                        always_ram=True
                    )
                )
            )
            logger.info(f"  ✅ Scalar quantization enabled (4x speedup)")
            return True
        except Exception as e2:
            logger.error(f"  ❌ Quantization failed: {e2}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Enable quantization on existing collections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help="Enable quantization on all collections"
    )
    parser.add_argument(
        '--collection',
        type=str,
        help="Enable quantization on specific collection"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.all and not args.collection:
        parser.error("Must specify --all or --collection")
    
    logger.info("=" * 60)
    logger.info("ENABLE QUANTIZATION - CodeRank Optimization")
    logger.info("=" * 60)
    logger.info(f"Qdrant URL: {QDRANT_URL}")
    
    if args.dry_run:
        logger.info("Mode: DRY RUN (no changes will be made)")
    else:
        logger.info("Mode: LIVE (will enable quantization)")
    
    logger.info("=" * 60)
    
    # Connect to Qdrant
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=60
        )
        
        collections = client.get_collections()
        logger.info(f"✅ Connected to Qdrant ({len(collections.collections)} collections)")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Qdrant: {e}")
        return 1
    
    # Determine which collections to process
    if args.all:
        collections_to_process = COLLECTIONS
    else:
        collections_to_process = [args.collection]
    
    # Enable quantization
    results = {}
    for collection_name in collections_to_process:
        success = enable_quantization(client, collection_name, dry_run=args.dry_run)
        results[collection_name] = success
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("SUMMARY")
    logger.info("=" * 60)
    
    successful = [name for name, success in results.items() if success]
    failed = [name for name, success in results.items() if not success]
    
    logger.info(f"✅ Successful: {len(successful)}/{len(results)}")
    for name in successful:
        logger.info(f"  ✅ {name}")
    
    if failed:
        logger.info(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for name in failed:
            logger.info(f"  ❌ {name}")
    
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("\n💡 This was a dry run. Remove --dry-run to actually enable.")
    elif len(successful) > 0:
        logger.info("\n🎉 Quantization enabled! Queries should be 4-40x faster.")
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
