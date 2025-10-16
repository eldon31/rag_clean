#!/usr/bin/env python3
"""
Quick Qdrant Collection Cleanup Script
=====================================

Delete the specified collections quickly via API.
"""

import asyncio
import requests
import json

# Qdrant configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
BASE_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

# Collections to delete (as specified by user)
COLLECTIONS_TO_DELETE = [
    "docling",
    "fast_docs", 
    "inngest_ecosystem",
    "pydantic_docs",
    "realtime_system_768",
    "viator_api"
]

def get_collections():
    """Get all collections."""
    try:
        response = requests.get(f"{BASE_URL}/collections")
        if response.status_code == 200:
            collections = response.json()["result"]["collections"]
            return [col["name"] for col in collections]
        else:
            print(f"❌ Error getting collections: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def delete_collection(collection_name):
    """Delete a specific collection."""
    try:
        response = requests.delete(f"{BASE_URL}/collections/{collection_name}")
        if response.status_code == 200:
            print(f"✅ Deleted collection: {collection_name}")
            return True
        else:
            print(f"❌ Failed to delete {collection_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting {collection_name}: {e}")
        return False

def main():
    """Main cleanup function."""
    print("🧹 QDRANT COLLECTION CLEANUP")
    print("=" * 40)
    
    # Get current collections
    print("📋 Current collections:")
    current_collections = get_collections()
    for col in current_collections:
        print(f"   - {col}")
    
    print(f"\n🗑️  Collections to delete: {len(COLLECTIONS_TO_DELETE)}")
    for col in COLLECTIONS_TO_DELETE:
        print(f"   - {col}")
    
    print("\n🚀 Starting deletion...")
    
    # Delete each collection
    deleted_count = 0
    for collection_name in COLLECTIONS_TO_DELETE:
        if collection_name in current_collections:
            if delete_collection(collection_name):
                deleted_count += 1
        else:
            print(f"⚠️  Collection '{collection_name}' not found (already deleted?)")
    
    print(f"\n✅ Cleanup complete! Deleted {deleted_count} collections.")
    
    # Show remaining collections
    print("\n📋 Remaining collections:")
    remaining_collections = get_collections()
    for col in remaining_collections:
        print(f"   - {col}")
    
    if remaining_collections:
        print(f"\n🎯 Found {len(remaining_collections)} remaining collections")
        print("These should be our 3 main collections:")
        print("   ✅ docling_768")
        print("   ✅ qdrant_ecosystem_768") 
        print("   ✅ sentence_transformers_768")
    else:
        print("⚠️  No collections remaining")

if __name__ == "__main__":
    main()