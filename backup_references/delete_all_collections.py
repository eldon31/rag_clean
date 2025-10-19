#!/usr/bin/env python3
"""
Script to delete all Qdrant collections before re-uploading
"""

from qdrant_client import QdrantClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_all_collections():
    """Delete all target collections from Qdrant"""
    
    # Configuration
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    
    # Collections to delete (actual collection names from Qdrant)
    COLLECTIONS = [
        "docling_v4",
        "sentence_transformers_v4",
        "qdrant_v4",
        "fast_docs_v4",
        "pydantic_v4"
    ]
    
    try:
        # Connect to Qdrant
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        logger.info(f"✅ Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        
        # Get all existing collections
        existing_collections = client.get_collections().collections
        existing_names = [col.name for col in existing_collections]
        
        logger.info(f"📋 Found {len(existing_names)} existing collections")
        
        # Delete each target collection
        deleted_count = 0
        for collection_name in COLLECTIONS:
            if collection_name in existing_names:
                logger.info(f"🗑️  Deleting collection: {collection_name}")
                client.delete_collection(collection_name)
                deleted_count += 1
                logger.info(f"✅ Deleted: {collection_name}")
            else:
                logger.info(f"⏭️  Collection not found (skipping): {collection_name}")
        
        logger.info(f"🎯 Deletion complete! Deleted {deleted_count} collections")
        
    except Exception as e:
        logger.error(f"❌ Deletion failed: {e}")
        raise

if __name__ == "__main__":
    delete_all_collections()
