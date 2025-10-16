"""Clean up empty collections from Qdrant."""
import logging
from qdrant_client import QdrantClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

QDRANT_URL = "http://localhost:6333"

def main():
    logger.info("=" * 70)
    logger.info("CLEANUP EMPTY QDRANT COLLECTIONS")
    logger.info("=" * 70)
    
    client = QdrantClient(QDRANT_URL)
    
    # Get all collections
    all_collections = client.get_collections().collections
    logger.info(f"Found {len(all_collections)} total collections\n")
    
    empty_collections = []
    active_collections = []
    
    # Check each collection
    for coll in all_collections:
        info = client.get_collection(coll.name)
        points = info.points_count
        
        if points == 0:
            empty_collections.append(coll.name)
            logger.info(f"🗑️  EMPTY: {coll.name} (0 points)")
        else:
            active_collections.append((coll.name, points))
            logger.info(f"✅ ACTIVE: {coll.name} ({points:,} points)")
    
    if not empty_collections:
        logger.info("\n✨ No empty collections found! Database is clean.")
        return
    
    # Show summary
    logger.info("\n" + "=" * 70)
    logger.info(f"SUMMARY: {len(empty_collections)} empty collections to delete")
    logger.info("=" * 70)
    
    for name in empty_collections:
        logger.info(f"  🗑️  {name}")
    
    # Delete empty collections
    logger.info("\n🗑️  Deleting empty collections...")
    
    deleted = []
    failed = []
    
    for name in empty_collections:
        try:
            client.delete_collection(name)
            deleted.append(name)
            logger.info(f"  ✅ Deleted: {name}")
        except Exception as e:
            failed.append((name, str(e)))
            logger.error(f"  ❌ Failed to delete {name}: {e}")
    
    # Final summary
    logger.info("\n" + "=" * 70)
    logger.info("CLEANUP COMPLETE")
    logger.info("=" * 70)
    logger.info(f"✅ Deleted: {len(deleted)} collections")
    if failed:
        logger.info(f"❌ Failed: {len(failed)} collections")
    
    logger.info(f"\n📊 Active collections remaining: {len(active_collections)}")
    for name, points in active_collections:
        logger.info(f"   ✅ {name}: {points:,} points")
    
    if deleted:
        logger.info(f"\n🎉 Successfully cleaned up {len(deleted)} empty collections!")


if __name__ == "__main__":
    main()
