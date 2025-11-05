"""Test script to verify rich progress bars for batch processing."""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Run a simple embedding test
if __name__ == "__main__":
    from scripts.embed_collections_v7 import main
    
    # Use minimal test arguments
    sys.argv = [
        "embed_collections_v7.py",
        "--collection-name", "test_rich_batch_progress",
        "--chunk-dir", "Chunked/Docling",
        "--model-name", "sentence-transformers/all-MiniLM-L6-v2",
        "--batch-size", "8",
        "--limit", "32",  # Process only 32 chunks for quick test
        "--device", "cuda",
        "--no-sparse",  # Disable sparse for faster test
        "--no-rerank",  # Disable reranking for faster test
    ]
    
    print("=" * 80)
    print("Testing Rich Progress Bars for Batch Processing")
    print("=" * 80)
    print("This should show a clean rich progress bar without tqdm text pollution")
    print("=" * 80)
    
    try:
        main()
        print("\n" + "=" * 80)
        print("✓ Test completed successfully!")
        print("=" * 80)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
