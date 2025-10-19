#!/usr/bin/env python3
"""
Delete all existing collections before fresh upload
This ensures clean state for new embeddings upload
"""

import logging
import sys
from qdrant_client import QdrantClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_all_collections():
    """Delete all collections to start fresh"""
    
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    
    # Collections to delete (both old and new naming)
    COLLECTIONS_TO_DELETE = [
        # Old v4 naming
        "ultimate_embeddings_v4_nomic-coderank_docling",
        "ultimate_embeddings_v4_nomic-coderank_fast_docs",
        "ultimate_embeddings_v4_nomic-coderank_pydantic",
        "ultimate_embeddings_v4_nomic-coderank_qdrant",
        "ultimate_embeddings_v4_nomic-coderank_sentence_transformers",
        # New MCP naming
        "sentence_transformers",
        "docling",
        "qdrant_ecosystem",
        "fast_docs",
        "pydantic"
    ]
    
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        logger.info(f"✅ Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        
        # Get existing collections
        collections_info = client.get_collections()
        existing_collections = {c.name for c in collections_info.collections}
        
        logger.info(f"📋 Found {len(existing_collections)} existing collections:")
        for name in existing_collections:
            logger.info(f"   - {name}")
        
        # Delete collections
        deleted_count = 0
        for collection_name in COLLECTIONS_TO_DELETE:
            if collection_name in existing_collections:
                logger.info(f"🗑️  Deleting collection: {collection_name}")
                client.delete_collection(collection_name=collection_name)
                deleted_count += 1
                logger.info(f"✅ Deleted: {collection_name}")
            else:
                logger.info(f"⏭️  Skipping (not found): {collection_name}")
        
        logger.info(f"\n🎯 Deletion complete! Removed {deleted_count} collections")
        logger.info("✨ Ready for fresh upload!")
        
    except Exception as e:
        logger.error(f"❌ Deletion failed: {e}")
        raise

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("DELETING ALL COLLECTIONS - FRESH START")
    logger.info("=" * 60)
    
    # Check for --force flag
    if "--force" in sys.argv or "-f" in sys.argv:
        logger.info("⚡ Force mode enabled - skipping confirmation")
        delete_all_collections()
    else:
        response = input("\n⚠️  This will DELETE all existing collections. Continue? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            delete_all_collections()
        else:
            logger.info("❌ Cancelled by user")
