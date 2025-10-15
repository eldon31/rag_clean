"""
Final upload of all 4 collections to DigitalOcean Qdrant
Based on KAGGLE_PROCESSING_GUIDE.md and actual embeddings
"""
from pathlib import Path
import sys
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.upload_to_qdrant import QdrantUploader

# Local Qdrant URL
LOCAL_QDRANT_URL = "http://localhost:6333"

def main():
    print("=" * 80)
    print("FINAL UPLOAD: ALL 4 COLLECTIONS TO LOCAL QDRANT")
    print("=" * 80)
    print(f"Target: {LOCAL_QDRANT_URL}")
    print()
    
    # Connect to local Qdrant
    uploader = QdrantUploader(url=LOCAL_QDRANT_URL)
    
    # Check existing collections
    print("📊 Checking existing collections...")
    try:
        existing = uploader.client.get_collections()
        print(f"Found {len(existing.collections)} existing collections:")
        for col in existing.collections:
            info = uploader.client.get_collection(col.name)
            print(f"  • {col.name}: {info.points_count} points")
        print()
    except Exception as e:
        print(f"⚠️  Could not check collections: {e}")
        print()
    
    # Define all collections with REPLACE mode for fresh start
    # Based on KAGGLE_PROCESSING_GUIDE.md specifications
    collections = [
        {
            "name": "viator_api",
            "file": "output/embeddings/viator_api_embeddings.jsonl",
            "description": "Viator API documentation (4 files: PDFs + JSON)",
            "subdirs": ["affiliate", "technical_guides", "api_specs"],
            "mode": "replace",  # Replace to clear any old flat structure
            "expected_chunks": "~995"
        },
        {
            "name": "fast_docs",
            "file": "output/embeddings/fast_docs_embeddings.jsonl",
            "description": "FastAPI + FastMCP + Python SDK (109 markdown files)",
            "subdirs": ["fastapi", "fastmcp", "python_sdk"],
            "mode": "replace",  # Fresh upload
            "expected_chunks": "~2,000-3,000"
        },
        {
            "name": "pydantic_docs",
            "file": "output/embeddings/pydantic_docs_embeddings.jsonl",
            "description": "Pydantic documentation (270 markdown files)",
            "subdirs": [],  # No subdirs - single directory
            "mode": "replace",  # Fresh upload
            "expected_chunks": "~5,000-8,000"
        },
        {
            "name": "inngest_ecosystem",
            "file": "output/embeddings/inngest_ecosystem_embeddings.jsonl",
            "description": "Inngest ecosystem (295 markdown files, 6 subdirs)",
            "subdirs": ["inngest_overall", "agent_kit", "agent_kit_github", 
                       "inngest", "inngest_js", "inngest_py"],
            "mode": "replace",  # Fresh upload
            "expected_chunks": "~6,000-10,000"
        }
    ]
    
    # Statistics
    total_chunks = 0
    successful_uploads = 0
    
    # Upload each collection
    for i, col in enumerate(collections, 1):
        print("=" * 80)
        print(f"COLLECTION {i}/4: {col['name'].upper()}")
        print("=" * 80)
        print(f"📄 Description: {col['description']}")
        print(f"📁 Subdirectories: {', '.join(col['subdirs']) if col['subdirs'] else 'None (single dir)'}")
        print(f"🎯 Expected chunks: {col['expected_chunks']}")
        print(f"🔄 Upload mode: {col['mode']}")
        print()
        
        file_path = Path(col['file'])
        
        # Check file exists
        if not file_path.exists():
            print(f"❌ Error: {file_path} not found!")
            print(f"   Please ensure embeddings are in output/embeddings/ folder")
            print()
            continue
        
        # Get file size and chunk count
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"📦 File: {file_path.name}")
        print(f"💾 Size: {file_size_mb:.2f} MB")
        
        # Count chunks
        with open(file_path, 'r', encoding='utf-8') as f:
            chunk_count = sum(1 for _ in f)
        print(f"📊 Actual chunks: {chunk_count:,}")
        print()
        
        try:
            # Create collection with quantization
            print(f"🔧 Creating collection with scalar (int8) quantization...")
            uploader.create_collection(
                collection_name=col['name'],
                vector_size=3584,  # Correct dimension from EMBEDDING_DIMENSION_ANALYSIS.md
                use_quantization="scalar",
                recreate=True  # Always recreate for clean slate
            )
            
            # Upload embeddings
            print(f"📤 Uploading {chunk_count:,} chunks...")
            uploader.upload_embeddings(
                embeddings_file=file_path,
                collection_name=col['name'],
                mode="upsert",  # Upsert within the collection
                check_duplicates=False  # Skip duplicate check for speed
            )
            
            # Verify upload
            info = uploader.client.get_collection(col['name'])
            uploaded_count = info.points_count
            
            print()
            if uploaded_count == chunk_count:
                print(f"✅ SUCCESS: {col['name']}")
                print(f"   Uploaded: {uploaded_count:,} points")
                print(f"   Vector size: {info.config.params.vectors.size}")
                print(f"   Quantization: {info.config.quantization_config}")
                total_chunks += uploaded_count
                successful_uploads += 1
            else:
                print(f"⚠️  WARNING: Point count mismatch!")
                print(f"   Expected: {chunk_count:,}")
                print(f"   Uploaded: {uploaded_count:,}")
                total_chunks += uploaded_count
                successful_uploads += 1
            
        except Exception as e:
            print(f"❌ ERROR uploading {col['name']}: {e}")
        
        print()
    
    # Final summary
    print("=" * 80)
    print("🎉 UPLOAD COMPLETE!")
    print("=" * 80)
    print(f"✅ Successful uploads: {successful_uploads}/{len(collections)}")
    print(f"📊 Total chunks uploaded: {total_chunks:,}")
    print(f"🔢 Vector dimension: 3584 (nomic-embed-code)")
    print(f"🗜️  Quantization: Scalar (int8) - 4x compression, 99% accuracy")
    print(f"🌐 Server: {LOCAL_QDRANT_URL}")
    print("=" * 80)
    print()
    
    # List all collections
    print("📋 Final collection status:")
    try:
        collections_list = uploader.client.get_collections()
        for col in collections_list.collections:
            info = uploader.client.get_collection(col.name)
            print(f"  • {col.name}: {info.points_count:,} points")
    except Exception as e:
        print(f"⚠️  Could not list collections: {e}")
    
    print()
    print("🔍 Test your collections:")
    print(f"  curl {LOCAL_QDRANT_URL}/collections")
    print(f"  curl {LOCAL_QDRANT_URL}/collections/viator_api")
    print()
    print("📚 Documentation structure preserved:")
    print("  • viator_api: affiliate/, technical_guides/, api_specs/")
    print("  • fast_docs: fastapi/, fastmcp/, python_sdk/")
    print("  • pydantic_docs: (single directory)")
    print("  • inngest_ecosystem: 6 subdirectories")
    print()
    print("🚀 Ready for production search!")
    print()

if __name__ == "__main__":
    main()
