#!/usr/bin/env python3
"""
Quick Qdrant Stats Check
========================
"""

import requests
import json

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
BASE_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

def get_collection_info(collection_name):
    """Get detailed info for a collection."""
    try:
        response = requests.get(f"{BASE_URL}/collections/{collection_name}")
        if response.status_code == 200:
            return response.json()["result"]
        return None
    except Exception as e:
        print(f"Error getting {collection_name}: {e}")
        return None

def main():
    collections = ["sentence_transformers_768", "docling_768", "qdrant_ecosystem_768"]
    
    print("🎯 QDRANT COLLECTIONS STATS")
    print("=" * 50)
    
    total_vectors = 0
    
    for col_name in collections:
        info = get_collection_info(col_name)
        if info:
            points = info.get("points_count", 0)
            vectors_config = info.get("config", {}).get("params", {}).get("vectors", {})
            if isinstance(vectors_config, dict) and "default" in vectors_config:
                size = vectors_config["default"]["size"]
                distance = vectors_config["default"]["distance"]
            else:
                size = "unknown"
                distance = "unknown"
            
            total_vectors += points
            
            print(f"📊 {col_name}:")
            print(f"   Points: {points:,}")
            print(f"   Dimensions: {size}")
            print(f"   Distance: {distance}")
            print()
        else:
            print(f"❌ Could not get info for {col_name}")
    
    print(f"🎯 TOTAL VECTORS: {total_vectors:,}")
    print("✅ Ready for MCP server optimization!")

if __name__ == "__main__":
    main()