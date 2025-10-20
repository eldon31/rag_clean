#!/usr/bin/env python3
"""
Test script for V5 embedder with new chunk file structure

Tests that the embedder can:
1. Discover collections with subdirectories
2. Load individual chunk files recursively
3. Process V5 metadata fields
4. Generate embeddings correctly
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.embed_collections_v5 import _discover_collections, _run_for_collection
from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4, KaggleGPUConfig, KaggleExportConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_collection_discovery():
    """Test that collections are discovered correctly"""
    print("\n" + "="*70)
    print("TEST 1: Collection Discovery")
    print("="*70)
    
    chunks_root = Path("Chunked")
    if not chunks_root.exists():
        print("✗ Chunked directory not found")
        return False
    
    collections = _discover_collections(chunks_root, None)
    
    if not collections:
        print("✗ No collections discovered")
        return False
    
    print(f"✓ Discovered {len(collections)} collections:")
    for col in collections:
        chunk_count = len(list(col.rglob("*_chunks.json")))
        print(f"   - {col.name}: {chunk_count} chunk files")
    
    return True


def test_chunk_loading():
    """Test that chunk files are loaded correctly"""
    print("\n" + "="*70)
    print("TEST 2: Chunk Loading (Individual Files)")
    print("="*70)
    
    chunks_root = Path("Chunked")
    collections = _discover_collections(chunks_root, None)
    
    if not collections:
        print("✗ No collections to test")
        return False
    
    # Test first collection
    test_collection = collections[0]
    print(f"Testing collection: {test_collection.name}")
    
    try:
        # Initialize embedder (CPU mode for testing)
        gpu_config = KaggleGPUConfig()
        export_config = KaggleExportConfig(working_dir="./test_output")
        
        embedder = UltimateKaggleEmbedderV4(
            model_name="all-miniLM-l6",  # Small model for testing
            gpu_config=gpu_config,
            export_config=export_config,
        )
        
        # Load chunks
        load_result = embedder.load_chunks_from_processing(str(test_collection))
        
        total_chunks = load_result.get("total_chunks_loaded", 0)
        print(f"✓ Loaded {total_chunks} chunks")
        
        if total_chunks == 0:
            print("✗ No chunks loaded")
            return False
        
        # Check V5 metadata
        if embedder.chunks_metadata:
            first_meta = embedder.chunks_metadata[0]
            v5_fields = {
                "model_aware_chunking": first_meta.get("model_aware_chunking"),
                "chunker_version": first_meta.get("chunker_version"),
                "within_token_limit": first_meta.get("within_token_limit"),
                "estimated_tokens": first_meta.get("estimated_tokens"),
            }
            print(f"✓ V5 metadata present: {v5_fields}")
        
        # Check hierarchical structure is preserved
        print(f"✓ Collections loaded: {load_result.get('collections_loaded', 0)}")
        print(f"✓ Memory usage: {load_result.get('memory_usage_mb', 0):.1f}MB")
        
        return True
        
    except Exception as e:
        print(f"✗ Loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_embedding_generation():
    """Test that embeddings can be generated from V5 chunks"""
    print("\n" + "="*70)
    print("TEST 3: Embedding Generation")
    print("="*70)
    
    chunks_root = Path("Chunked")
    collections = _discover_collections(chunks_root, None)
    
    if not collections:
        print("✗ No collections to test")
        return False
    
    # Test first collection with small sample
    test_collection = collections[0]
    print(f"Testing collection: {test_collection.name}")
    
    try:
        gpu_config = KaggleGPUConfig()
        export_config = KaggleExportConfig(working_dir="./test_output")
        
        embedder = UltimateKaggleEmbedderV4(
            model_name="all-miniLM-l6",  # Small, fast model
            gpu_config=gpu_config,
            export_config=export_config,
        )
        
        # Load chunks
        load_result = embedder.load_chunks_from_processing(str(test_collection))
        total_chunks = load_result.get("total_chunks_loaded", 0)
        
        if total_chunks == 0:
            print("✗ No chunks to embed")
            return False
        
        # Limit to first 10 chunks for quick test
        embedder.chunk_texts = embedder.chunk_texts[:10]
        embedder.chunks_metadata = embedder.chunks_metadata[:10]
        embedder.raw_chunk_texts = embedder.raw_chunk_texts[:10]
        embedder.sparse_vectors = embedder.sparse_vectors[:10]
        
        print(f"✓ Testing with {len(embedder.chunk_texts)} chunks")
        
        # Generate embeddings
        print("Generating embeddings...")
        perf = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=False,
            save_intermediate=False
        )
        
        print(f"✓ Generated {perf['total_embeddings_generated']} embeddings")
        print(f"✓ Dimension: {perf['embedding_dimension']}")
        print(f"✓ Time: {perf['processing_time_seconds']:.2f}s")
        print(f"✓ Speed: {perf['chunks_per_second']:.1f} chunks/sec")
        
        return True
        
    except Exception as e:
        print(f"✗ Embedding generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("V5 EMBEDDER TEST SUITE")
    print("Testing compatibility with V5 Unified Chunker output")
    print("="*70)
    
    tests = [
        ("Collection Discovery", test_collection_discovery),
        ("Chunk Loading", test_chunk_loading),
        ("Embedding Generation", test_embedding_generation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! V5 embedder is compatible with new chunk structure.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())