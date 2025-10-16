#!/usr/bin/env python3
"""
🚀 CORRECTED KAGGLE PROCESSORS - Based on ACTUAL Ultimate Embedder V4 API
Process each collection from DOCS_CHUNKS_OUTPUT using the real V4 methods

USAGE IN KAGGLE JUPYTER (VSCode connected):
    exec(open('kaggle_corrected_processors.py').read())
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import V4 (must be uploaded to Kaggle)
from kaggle_ultimate_embedder_v4 import (
    UltimateKaggleEmbedderV4,
    KaggleGPUConfig,
    KaggleExportConfig,
    AdvancedPreprocessingConfig
)

def process_single_collection(collection_name: str, chunks_dir: str = None):
    """
    Process a single collection with ACTUAL V4 API
    
    Based on REAL kaggle_ultimate_embedder_v4.py implementation
    """
    
    print("="*80)
    print(f"🚀 PROCESSING: {collection_name} Collection")
    print("="*80)
    
    start_time = time.time()
    
    try:
        # STEP 1: Initialize V4 Embedder (CORRECT PARAMETERS)
        print(f"\n🔄 STEP 1: Initializing V4 with ACTUAL API...")
        
        embedder = UltimateKaggleEmbedderV4(
            model_name="nomic-coderank",
            gpu_config=KaggleGPUConfig(
                base_batch_size=32,
                dynamic_batching=True,
                precision="fp16",
                enable_torch_compile=True
            ),
            export_config=KaggleExportConfig(
                working_dir="/kaggle/working",
                export_numpy=True,
                export_jsonl=True,
                export_faiss=True
            ),
            preprocessing_config=AdvancedPreprocessingConfig(
                enable_text_caching=True
            ),
            enable_ensemble=False  # NOT enable_reranking
        )
        
        print(f"✅ V4 initialized!")
        print(f"   🎯 Model: {embedder.model_name}")
        print(f"   🔥 GPU Count: {embedder.device_count}")
        print(f"   📊 Vector Dimension: {embedder.model_config.vector_dim}")
        
        # STEP 2: Load Chunks (CORRECT METHOD SIGNATURE)
        print(f"\n🔄 STEP 2: Loading chunks with ACTUAL load_chunks_from_processing()...")
        
        # The REAL V4 method signature is:
        # def load_chunks_from_processing(self, chunks_dir: str = "/kaggle/input/docs-chunks-output")
        # It auto-detects collections inside that directory!
        
        if chunks_dir is None:
            # Let V4 use its auto-detection
            chunks_loaded = embedder.load_chunks_from_processing()
        else:
            chunks_loaded = embedder.load_chunks_from_processing(chunks_dir=chunks_dir)
        
        print(f"✅ Chunks loaded!")
        print(f"   📊 Total chunks: {chunks_loaded.get('total_chunks_loaded', 0)}")
        print(f"   📊 Collections: {chunks_loaded.get('collections_loaded', 0)}")
        print(f"   📊 By collection: {chunks_loaded.get('chunks_by_collection', {})}")
        
        # STEP 3: Generate Embeddings (CORRECT METHOD SIGNATURE)
        print(f"\n🔄 STEP 3: Generating embeddings with ACTUAL generate_embeddings_kaggle_optimized()...")
        
        # The REAL V4 method signature is:
        # def generate_embeddings_kaggle_optimized(self, enable_monitoring: bool = True, save_intermediate: bool = True)
        
        embedding_results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True,
            save_intermediate=True
        )
        
        print(f"✅ Embeddings generated!")
        print(f"   📊 Total: {embedding_results.get('total_embeddings', 0)}")
        print(f"   📏 Dimension: {embedding_results.get('embedding_dimension', 0)}")
        print(f"   ⚡ Speed: {embedding_results.get('chunks_per_second', 0):.1f} chunks/sec")
        print(f"   ⏱️ Time: {embedding_results.get('total_time_seconds', 0):.2f}s")
        
        # Performance assessment
        speed = embedding_results.get('chunks_per_second', 0)
        if speed >= 310:
            print(f"   🏆 EXCELLENT! Meeting V4 targets (310-516 chunks/sec)")
        elif speed >= 200:
            print(f"   ✅ GOOD! Production-ready")
        else:
            print(f"   ⚠️ Below target")
        
        # STEP 4: Export (CORRECT METHOD - just call it, no parameters needed)
        print(f"\n🔄 STEP 4: Exporting with ACTUAL export_for_local_qdrant()...")
        
        export_files = embedder.export_for_local_qdrant()
        
        print(f"✅ Export complete!")
        for file_type, file_path in export_files.items():
            if os.path.exists(file_path):
                size_mb = os.path.getsize(file_path) / 1024 / 1024
                print(f"   📁 {file_type}: {os.path.basename(file_path)} ({size_mb:.1f}MB)")
        
        # Save results
        results = {
            'collection': collection_name,
            'status': 'SUCCESS',
            'chunks_loaded': chunks_loaded,
            'embedding_results': embedding_results,
            'export_files': export_files,
            'processing_time_seconds': time.time() - start_time,
            'timestamp': datetime.now().isoformat()
        }
        
        results_file = f"/kaggle/working/{collection_name}_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n🎉 {collection_name} PROCESSING COMPLETE!")
        print(f"   ⏱️ Total time: {results['processing_time_seconds']:.2f}s")
        print(f"   📄 Results saved: {results_file}")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error processing {collection_name}: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'collection': collection_name,
            'status': 'ERROR',
            'error': str(e),
            'processing_time_seconds': time.time() - start_time
        }


def process_all_collections():
    """
    Process all collections using ACTUAL V4 API
    
    The REAL V4 auto-discovers all collections in chunks_dir!
    """
    
    print("="*80)
    print("🚀 ULTIMATE KAGGLE EMBEDDER V4 - BATCH PROCESSOR (CORRECTED API)")
    print("="*80)
    
    overall_start = time.time()
    
    # Check what collections are available
    possible_dirs = [
        "/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT",
        "/kaggle/input/docs-chunks-output",
        "/kaggle/working/DOCS_CHUNKS_OUTPUT"
    ]
    
    chunks_dir = None
    for dir_path in possible_dirs:
        if os.path.exists(dir_path):
            chunks_dir = dir_path
            print(f"✅ Found chunks directory: {chunks_dir}")
            break
    
    if not chunks_dir:
        print(f"❌ No chunks directory found. Tried:")
        for path in possible_dirs:
            print(f"   - {path}")
        print(f"\n💡 Upload DOCS_CHUNKS_OUTPUT to Kaggle as dataset")
        return None
    
    # List available collections
    collections = []
    for item in os.listdir(chunks_dir):
        item_path = os.path.join(chunks_dir, item)
        if os.path.isdir(item_path):
            json_count = len([f for f in os.listdir(item_path) if f.endswith('.json')])
            if json_count > 0:
                collections.append((item, json_count))
                print(f"   📦 {item}: {json_count} JSON files")
    
    print(f"\n📊 Found {len(collections)} collections")
    
    # Process using V4's auto-discovery
    print(f"\n🔄 Processing ALL collections with V4 auto-discovery...")
    
    result = process_single_collection("ALL_COLLECTIONS", chunks_dir)
    
    overall_time = time.time() - overall_start
    
    print(f"\n{'='*80}")
    print(f"📊 OVERALL SUMMARY")
    print(f"{'='*80}")
    print(f"⏱️ Total time: {overall_time:.2f}s")
    print(f"📊 Status: {result.get('status', 'UNKNOWN')}")
    print(f"{'='*80}")
    
    return result


# Individual collection processors (if you want to process one at a time)

def process_docling():
    """Process Docling collection specifically"""
    # For individual collections, you need to point to the specific subfolder
    base_dir = "/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT"
    docling_dir = os.path.join(base_dir, "Docling")
    
    if os.path.exists(docling_dir):
        return process_single_collection("Docling", docling_dir)
    else:
        print(f"❌ Docling not found at {docling_dir}")
        return None

def process_fast_docs():
    """Process FAST_DOCS collection"""
    base_dir = "/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT"
    fast_docs_dir = os.path.join(base_dir, "FAST_DOCS")
    
    if os.path.exists(fast_docs_dir):
        return process_single_collection("FAST_DOCS", fast_docs_dir)
    else:
        print(f"❌ FAST_DOCS not found at {fast_docs_dir}")
        return None

def process_pydantic():
    """Process pydantic_pydantic collection"""
    base_dir = "/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT"
    pydantic_dir = os.path.join(base_dir, "pydantic_pydantic")
    
    if os.path.exists(pydantic_dir):
        return process_single_collection("pydantic_pydantic", pydantic_dir)
    else:
        print(f"❌ pydantic_pydantic not found at {pydantic_dir}")
        return None

def process_qdrant():
    """Process Qdrant collection"""
    base_dir = "/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT"
    qdrant_dir = os.path.join(base_dir, "Qdrant")
    
    if os.path.exists(qdrant_dir):
        return process_single_collection("Qdrant", qdrant_dir)
    else:
        print(f"❌ Qdrant not found at {qdrant_dir}")
        return None

def process_sentence_transformers():
    """Process Sentence_Transformers collection"""
    base_dir = "/kaggle/input/docs-chunks-output/DOCS_CHUNKS_OUTPUT"
    st_dir = os.path.join(base_dir, "Sentence_Transformers")
    
    if os.path.exists(st_dir):
        return process_single_collection("Sentence_Transformers", st_dir)
    else:
        print(f"❌ Sentence_Transformers not found at {st_dir}")
        return None


# Main execution
if __name__ == "__main__":
    print("🚀 Starting CORRECTED V4 Batch Processor")
    print("="*80)
    
    # Process all collections at once (recommended - V4 handles auto-discovery)
    results = process_all_collections()
    
    print("\n🎉 Processing complete!")
