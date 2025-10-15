"""
Upload Docling Embeddings to Qdrant
Uses the existing upload infrastructure with docling-specific paths
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.upload_to_qdrant import QdrantUploader

def main():
    """Upload Docling embeddings to Qdrant"""
    
    # Initialize uploader
    uploader = QdrantUploader()
    
    # Embeddings file location
    embeddings_file = Path("output/embeddings/docling_embeddings.jsonl")
    
    # Verify file exists
    if not embeddings_file.exists():
        print(f"❌ Embeddings file not found: {embeddings_file}")
        print(f"\nExpected location: {embeddings_file.absolute()}")
        print("\nPlease ensure you've downloaded the file from Kaggle and placed it in output/embeddings/")
        return
    
    print("\n" + "="*60)
    print("DOCLING EMBEDDINGS → QDRANT UPLOAD")
    print("="*60)
    print(f"File: {embeddings_file}")
    print(f"Collection: docling")
    print(f"Vector size: 3584 (nomic-embed-code)")
    print(f"Quantization: int8 scalar (4x compression)")
    print("="*60 + "\n")
    
    # Create collection with quantization
    uploader.create_collection(
        collection_name="docling",
        vector_size=3584,
        recreate=False,  # Don't recreate if exists
        use_quantization="scalar"  # int8 quantization for 4x memory savings
    )
    
    # Upload embeddings
    uploader.upload_embeddings(
        embeddings_file=embeddings_file,
        collection_name="docling",
        mode="upsert",  # Update if exists, insert if new
        check_duplicates=True
    )
    
    print("\n" + "="*60)
    print("✅ DOCLING DEPLOYMENT COMPLETE")
    print("="*60)
    print("\nVerify at: http://localhost:6333/dashboard")
    print("Collection: docling")
    print("\nYou can now query the collection!")

if __name__ == "__main__":
    main()
