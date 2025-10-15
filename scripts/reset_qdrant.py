"""
Reset Qdrant - Delete All Collections
Prepares for fresh deployment of new embeddings
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models

# Connect to Qdrant
QDRANT_URL = "http://localhost:6333"

def reset_qdrant():
    """Delete all collections from Qdrant"""
    print("=" * 60)
    print("QDRANT RESET - DELETE ALL COLLECTIONS")
    print("=" * 60)
    
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        # Get all collections
        collections = client.get_collections().collections
        
        if not collections:
            print("\n✓ No collections found - Qdrant is already clean!")
            return
        
        print(f"\nFound {len(collections)} collections:")
        for collection in collections:
            print(f"  - {collection.name}")
        
        print("\n🗑️  Deleting all collections...")
        
        # Delete each collection
        for collection in collections:
            collection_name = collection.name
            client.delete_collection(collection_name)
            print(f"  ✓ Deleted: {collection_name}")
        
        print("\n" + "=" * 60)
        print("✅ ALL COLLECTIONS DELETED")
        print("=" * 60)
        print("\nQdrant is now clean and ready for fresh deployment!")
        print("\nNext steps:")
        print("1. Wait for Kaggle embedding to complete")
        print("2. Download docling_embeddings.jsonl")
        print("3. Run: python scripts/upload_to_qdrant.py")
        
    except Exception as e:
        print(f"\n❌ Error connecting to Qdrant: {e}")
        print("\nMake sure Qdrant is running:")
        print("  docker-compose up -d")
        print(f"  Check: {QDRANT_URL}/dashboard")

if __name__ == "__main__":
    reset_qdrant()
