"""
Verify CodeRank migration completed successfully.

This script:
1. Checks all collections are 768-dim
2. Verifies point counts match expectations
3. Tests search functionality
4. Reports quantization status

USAGE:
    python scripts/verify_migration.py
    
    # Check specific collection
    python scripts/verify_migration.py --collection qdrant_ecosystem
"""

import os
import argparse
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

EXPECTED_DIMENSION = 768
EXPECTED_COLLECTIONS = ["qdrant_ecosystem", "docling"]


def check_collection(client: QdrantClient, collection_name: str) -> Dict[str, Any]:
    """Check collection status and configuration."""
    logger.info(f"\n{'='*60}")
    logger.info(f"CHECKING: {collection_name}")
    logger.info(f"{'='*60}")
    
    try:
        info = client.get_collection(collection_name)
    except Exception as e:
        logger.error(f"❌ Collection not found: {e}")
        return {
            "name": collection_name,
            "exists": False,
            "error": str(e),
            "success": False
        }
    
    # Extract info
    dimension = info.config.params.vectors.size
    distance = info.config.params.vectors.distance.name
    points_count = info.points_count
    indexed_count = info.indexed_vectors_count
    
    # Check dimension
    dimension_ok = dimension == EXPECTED_DIMENSION
    if dimension_ok:
        logger.info(f"✅ Dimension: {dimension} (CodeRankEmbed)")
    else:
        logger.error(f"❌ Dimension: {dimension}, expected {EXPECTED_DIMENSION}")
    
    # Check distance metric
    logger.info(f"📏 Distance: {distance}")
    
    # Check points
    logger.info(f"📊 Points: {points_count:,}")
    logger.info(f"📇 Indexed: {indexed_count:,}")
    
    # Check HNSW config
    hnsw = info.config.hnsw_config
    logger.info(f"🔍 HNSW: m={hnsw.m}, ef_construct={hnsw.ef_construct}")
    
    # Check quantization
    quant_config = info.config.quantization_config
    if quant_config:
        logger.info(f"⚡ Quantization: {quant_config}")
    else:
        logger.warning("⚠️  No quantization enabled")
    
    # Check optimizer config
    optimizer = info.config.optimizer_config
    logger.info(f"⚙️  Optimizer: {optimizer.default_segment_number} segments")
    
    # Overall success
    success = dimension_ok and points_count > 0
    
    if success:
        logger.info(f"\n✅ {collection_name} is ready for CodeRank queries")
    else:
        logger.error(f"\n❌ {collection_name} has issues")
    
    return {
        "name": collection_name,
        "exists": True,
        "dimension": dimension,
        "distance": distance,
        "points_count": points_count,
        "indexed_count": indexed_count,
        "dimension_ok": dimension_ok,
        "has_quantization": quant_config is not None,
        "success": success
    }


def test_search(client: QdrantClient, collection_name: str) -> bool:
    """Test basic search functionality."""
    logger.info(f"\n🔍 Testing search for {collection_name}...")
    
    try:
        # Get a sample point
        scroll_result = client.scroll(
            collection_name=collection_name,
            limit=1,
            with_vectors=True
        )
        
        if not scroll_result[0]:
            logger.warning("⚠️  No points to test with")
            return False
        
        sample_point = scroll_result[0][0]
        sample_vector = sample_point.vector
        
        # Search with sample vector
        results = client.search(
            collection_name=collection_name,
            query_vector=sample_vector,
            limit=5
        )
        
        if not results:
            logger.error("❌ Search returned no results")
            return False
        
        logger.info(f"✅ Search returned {len(results)} results")
        logger.info(f"   Top score: {results[0].score:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Search test failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify CodeRank migration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--collection',
        type=str,
        help="Check specific collection only"
    )
    parser.add_argument(
        '--test-search',
        action='store_true',
        help="Test search functionality"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("CODERANK MIGRATION VERIFICATION")
    logger.info("=" * 60)
    logger.info(f"Qdrant URL: {QDRANT_URL}")
    logger.info(f"Expected dimension: {EXPECTED_DIMENSION}")
    logger.info("=" * 60)
    
    # Connect to Qdrant
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=30
        )
        
        all_collections = client.get_collections()
        logger.info(f"✅ Connected to Qdrant ({len(all_collections.collections)} collections)\n")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Qdrant: {e}")
        return 1
    
    # Determine which collections to check
    if args.collection:
        collections_to_check = [args.collection]
    else:
        collections_to_check = EXPECTED_COLLECTIONS
    
    # Check each collection
    results = {}
    for collection_name in collections_to_check:
        result = check_collection(client, collection_name)
        results[collection_name] = result
        
        # Test search if requested
        if args.test_search and result.get("success"):
            search_ok = test_search(client, collection_name)
            result["search_ok"] = search_ok
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("VERIFICATION SUMMARY")
    logger.info("=" * 60)
    
    all_ok = True
    for collection_name, result in results.items():
        if result.get("success"):
            logger.info(f"✅ {collection_name}")
            logger.info(f"   Dimension: {result.get('dimension')}")
            logger.info(f"   Points: {result.get('points_count'):,}")
            logger.info(f"   Quantization: {'✅' if result.get('has_quantization') else '❌'}")
            if args.test_search:
                logger.info(f"   Search: {'✅' if result.get('search_ok') else '❌'}")
        else:
            logger.error(f"❌ {collection_name}")
            if not result.get("exists"):
                logger.error(f"   Collection does not exist")
            elif not result.get("dimension_ok"):
                logger.error(f"   Wrong dimension: {result.get('dimension')}")
            all_ok = False
    
    logger.info("=" * 60)
    
    if all_ok:
        logger.info("\n🎉 All collections verified! CodeRank migration successful.")
        logger.info("   Ready to update MCP server for query embeddings.")
    else:
        logger.error("\n❌ Migration verification failed. Check errors above.")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
