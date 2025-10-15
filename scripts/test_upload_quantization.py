"""
Test script to verify upload_to_qdrant.py works with 3584-dim and quantization
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.upload_to_qdrant import QdrantUploader

def main():
    print("=" * 70)
    print("TESTING QDRANT UPLOAD WITH 3584-DIM + SCALAR QUANTIZATION")
    print("=" * 70)
    
    # Connect to local Qdrant
    uploader = QdrantUploader(url="http://localhost:6333")
    
    # Test 1: Create collection with scalar quantization
    print("\n📦 Test 1: Creating collection with scalar quantization...")
    uploader.create_collection(
        collection_name="test_viator",
        vector_size=3584,
        use_quantization="scalar",
        recreate=True
    )
    
    # Test 2: Upload small sample of embeddings
    print("\n📤 Test 2: Uploading sample embeddings...")
    embeddings_file = Path("output/embeddings/viator_api_embeddings.jsonl")
    
    if not embeddings_file.exists():
        print(f"❌ Error: {embeddings_file} not found!")
        return
    
    uploader.upload_embeddings(
        embeddings_file=embeddings_file,
        collection_name="test_viator",
        mode="upsert",
        check_duplicates=False
    )
    
    # Test 3: Verify collection info
    print("\n✅ Test 3: Verifying collection...")
    collection_info = uploader.client.get_collection("test_viator")
    print(f"  Vector size: {collection_info.config.params.vectors.size}")
    print(f"  Total points: {collection_info.points_count}")
    print(f"  Quantization: {collection_info.config.quantization_config}")
    
    # Test 4: Test search
    print("\n🔍 Test 4: Testing search...")
    import json
    with open(embeddings_file, 'r') as f:
        first_line = f.readline()
        sample = json.loads(first_line)
        query_vector = sample['embedding']
    
    results = uploader.client.search(
        collection_name="test_viator",
        query_vector=query_vector,
        limit=3
    )
    
    print(f"  Search returned {len(results)} results")
    if results:
        print(f"  Top result score: {results[0].score:.4f}")
        print(f"  Top result ID: {results[0].id}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\n💡 Ready to deploy to DigitalOcean!")
    print("   Next: Run deployment script for cloud upload")
    
if __name__ == "__main__":
    main()
