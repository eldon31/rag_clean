#!/usr/bin/env python3
"""
Script to list all existing Qdrant collections
"""

from qdrant_client import QdrantClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_collections():
    """List all collections in Qdrant"""
    
    # Configuration
    QDRANT_HOST = "localhost"
    QDRANT_PORT = 6333
    
    try:
        # Connect to Qdrant
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        logger.info(f"✅ Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        
        # Get all existing collections
        collections_response = client.get_collections()
        collections = collections_response.collections
        
        logger.info(f"\n📋 Found {len(collections)} existing collections:\n")
        
        for col in collections:
            logger.info(f"  - {col.name}")
            # Get collection info for point count
            try:
                info = client.get_collection(col.name)
                logger.info(f"    Points: {info.points_count}, Vectors: {info.vectors_count}")
            except Exception as e:
                logger.info(f"    (Could not get details: {e})")
        
        return [col.name for col in collections]
        
    except Exception as e:
        logger.error(f"❌ Failed to list collections: {e}")
        raise

if __name__ == "__main__":
    list_collections()
