"""
Upload all embeddings to DigitalOcean Qdrant with scalar quantization
"""
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.upload_to_qdrant import QdrantUploader

# DigitalOcean Qdrant URL
CLOUD_QDRANT_URL = "http://165.232.174.154:6333"

def main():
    print("=" * 70)
    print("UPLOADING TO DIGITALOCEAN QDRANT")
    print("=" * 70)
    print(f"Target: {CLOUD_QDRANT_URL}")
    print()
    
    # Connect to cloud Qdrant
    uploader = QdrantUploader(url=CLOUD_QDRANT_URL)
    
    # Define all collections
    collections = [
        {
            "name": "viator_api",
            "file": "output/embeddings/viator_api_embeddings.jsonl",
            "description": "Viator API documentation (995 chunks)"
        },
        {
            "name": "fast_docs",
            "file": "output/embeddings/fast_docs_embeddings.jsonl",
            "description": "FastAPI + FastMCP + Python SDK (1,443 chunks)"
        },
        {
            "name": "pydantic_docs",
            "file": "output/embeddings/pydantic_docs_embeddings.jsonl",
            "description": "Pydantic documentation (752 chunks)"
        },
        {
            "name": "inngest_ecosystem",
            "file": "output/embeddings/inngest_ecosystem_embeddings.jsonl",
            "description": "Inngest ecosystem docs (3,687 chunks)"
        }
    ]
    
    total_chunks = 0
    
    # Upload each collection
    for i, col in enumerate(collections, 1):
        print(f"\n{'='*70}")
        print(f"COLLECTION {i}/4: {col['name'].upper()}")
        print(f"{'='*70}")
        print(f"Description: {col['description']}")
        print()
        
        # Create collection with quantization
        uploader.create_collection(
            collection_name=col['name'],
            vector_size=3584,
            use_quantization="scalar",
            recreate=False  # Don't recreate if exists
        )
        
        # Upload embeddings
        file_path = Path(col['file'])
        if not file_path.exists():
            print(f"❌ Error: {file_path} not found!")
            continue
        
        uploader.upload_embeddings(
            embeddings_file=file_path,
            collection_name=col['name'],
            mode="upsert",
            check_duplicates=False
        )
        
        # Get collection info
        info = uploader.client.get_collection(col['name'])
        total_chunks += info.points_count
        print(f"\n✅ {col['name']}: {info.points_count} points uploaded")
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("=" * 70)
    print(f"Total collections: {len(collections)}")
    print(f"Total chunks: {total_chunks:,}")
    print(f"Vector dimension: 3584")
    print(f"Quantization: Scalar (int8) - 4x compression, 99% accuracy")
    print(f"Server: {CLOUD_QDRANT_URL}")
    print("=" * 70)
    print()
    print("🔍 Test search:")
    print(f"  curl {CLOUD_QDRANT_URL}/collections")
    print()
    print("📊 Next steps:")
    print("  1. Run search quality tests")
    print("  2. Update MCP servers to use cloud URL")
    print("  3. Implement Integration Plan Phase 1")
    print()

if __name__ == "__main__":
    main()
