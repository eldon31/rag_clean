#!/usr/bin/env python3
"""
🚀 KAGGLE PROCESSOR: Docling Collection (CORRECTED V4 API)
Based on V4 API Audit - Process ONLY Docling collection

USAGE IN KAGGLE JUPYTER:
    exec(open('process_docling.py').read())

OR:
    from process_docling import process_docling_collection
    results = process_docling_collection()
"""

import os
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import V4 with CORRECT API
from kaggle_ultimate_embedder_v4 import (
    UltimateKaggleEmbedderV4,
    KaggleGPUConfig,
    KaggleExportConfig,
    AdvancedPreprocessingConfig
)

def process_docling_collection():
    """Process Docling collection with V4"""
    
    print("="*80)
    print("🚀 PROCESSING: Docling Collection")
    print("="*80)
    
    # Configuration
    COLLECTION_NAME = "Docling"
    WORKING_DIR = "/kaggle/working"
    
    # Find collection path (adjust based on your Kaggle dataset structure)
    POSSIBLE_PATHS = [
        f"/kaggle/working/rad_clean/DOCS_CHUNKS_OUTPUT/{COLLECTION_NAME}",  # Cloned repo location
        f"/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT/{COLLECTION_NAME}",
        f"/kaggle/working/DOCS_CHUNKS_OUTPUT/{COLLECTION_NAME}",
        f"/kaggle/input/your-dataset/{COLLECTION_NAME}"
    ]
    
    collection_path = None
    for path in POSSIBLE_PATHS:
        if os.path.exists(path):
            collection_path = path
            break
    
    if not collection_path:
        print(f"❌ Collection not found. Tried:")
        for path in POSSIBLE_PATHS:
            print(f"   - {path}")
        print(f"\n💡 Please update POSSIBLE_PATHS in the script")
        return None
    
    print(f"✅ Found collection at: {collection_path}")
    
    start_time = time.time()
    
    try:
        # STEP 1: Initialize V4 Embedder
        print(f"\n🔄 STEP 1: Initializing Ultimate Kaggle Embedder V4...")
        
        embedder = UltimateKaggleEmbedderV4(
            model_name="nomic-coderank",
            gpu_config=KaggleGPUConfig(
                base_batch_size=32,
                dynamic_batching=True,
                precision="fp16",
                enable_torch_compile=True
            ),
            export_config=KaggleExportConfig(
                working_dir=WORKING_DIR,
                export_numpy=True,
                export_jsonl=True,
                export_faiss=True,
                output_prefix=f"{COLLECTION_NAME}_v4"
            ),
            preprocessing_config=AdvancedPreprocessingConfig(
                enable_text_caching=True,
                normalize_whitespace=True
            ),
            enable_ensemble=False
        )
        
        print(f"✅ V4 Embedder initialized!")
        print(f"   🎯 Model: {embedder.model_name}")
        print(f"   🔥 GPU Count: {embedder.device_count}")
        print(f"   📊 Vector Dimension: {embedder.model_config.vector_dim}")
        
        # STEP 2: Load Chunks (V4 auto-discovers collections in directory)
        print(f"\n🔄 STEP 2: Loading {COLLECTION_NAME} chunks...")
        
        # Point to the parent directory containing Docling folder
        parent_dir = os.path.dirname(collection_path)
        chunks_loaded = embedder.load_chunks_from_processing(
            chunks_dir=parent_dir
        )
        
        print(f"✅ Chunks loaded!")
        print(f"   📊 Total chunks: {chunks_loaded.get('total_chunks_loaded', 0)}")
        print(f"   � Collections: {chunks_loaded.get('collections_loaded', 0)}")
        if 'chunks_by_collection' in chunks_loaded:
            for coll, count in chunks_loaded['chunks_by_collection'].items():
                print(f"   📦 {coll}: {count} chunks")
        
        # STEP 3: Generate Embeddings
        print(f"\n🔄 STEP 3: Generating embeddings...")
        print(f"   🎯 Target: 310-516 chunks/sec")
        
        embedding_results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True,
            save_intermediate=True
        )
        
        print(f"✅ Embeddings generated!")
        print(f"   📊 Total: {embedding_results.get('total_embeddings', 0)}")
        print(f"   📏 Dimension: {embedding_results.get('embedding_dimension', 768)}")
        print(f"   ⚡ Speed: {embedding_results.get('chunks_per_second', 0):.1f} chunks/sec")
        print(f"   ⏱️ Time: {embedding_results.get('total_time_seconds', 0):.2f}s")
        print(f"   💾 Memory: {embedding_results.get('total_memory_mb', 0):.1f}MB")
        
        # Performance assessment
        speed = embedding_results['chunks_per_second']
        if speed >= 310:
            print(f"   🏆 EXCELLENT! Meeting V4 targets")
        elif speed >= 200:
            print(f"   ✅ GOOD! Production-ready")
        else:
            print(f"   ⚠️ Below target")
        
        # STEP 4: Export
        print(f"\n🔄 STEP 4: Exporting for local Qdrant deployment...")
        
        export_files = embedder.export_for_local_qdrant()
        
        print(f"✅ Export complete!")
        for file_type, file_path in export_files.items():
            if os.path.exists(file_path):
                size_mb = os.path.getsize(file_path) / 1024 / 1024
                print(f"   📁 {file_type}: {os.path.basename(file_path)} ({size_mb:.1f}MB)")
        
        # Save results
        results = {
            'collection': COLLECTION_NAME,
            'status': 'SUCCESS',
            'chunks_loaded': chunks_loaded,
            'embedding_results': embedding_results,
            'export_files': export_files,
            'processing_time_seconds': time.time() - start_time,
            'timestamp': datetime.now().isoformat()
        }
        
        results_file = f"{WORKING_DIR}/{COLLECTION_NAME}_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n🎉 {COLLECTION_NAME} PROCESSING COMPLETE!")
        print(f"   ⏱️ Total time: {results['processing_time_seconds']:.2f}s")
        print(f"   📄 Results saved: {results_file}")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error processing {COLLECTION_NAME}: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'collection': COLLECTION_NAME,
            'status': 'ERROR',
            'error': str(e),
            'processing_time_seconds': time.time() - start_time
        }

# Run if executed directly
if __name__ == "__main__":
    results = process_docling_collection()
    print("\n" + "="*80)
    print(f"Status: {results['status'] if results else 'FAILED'}")
    print("="*80)
