#!/usr/bin/env python3
"""
🚀 KAGGLE PROCESSOR: pydantic_pydantic Collection (CORRECTED V4 API)
Ultimate Embedder V4 - Single Collection Processing

✅ CORRECTED PARAMETERS (verified from source audit):
   - enable_ensemble=False (NOT enable_reranking)
   - output_prefix in KaggleExportConfig (NOT collection_name)
   - chunks_dir in load_chunks_from_processing (auto-discovers collections)
   - enable_monitoring, save_intermediate in generate_embeddings_kaggle_optimized
   - export_for_local_qdrant() takes NO parameters

USAGE IN KAGGLE JUPYTER:
    exec(open('process_pydantic.py').read())
"""

import os
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from kaggle_ultimate_embedder_v4 import (
    UltimateKaggleEmbedderV4,
    KaggleGPUConfig,
    KaggleExportConfig,
    AdvancedPreprocessingConfig
)

def process_pydantic_collection():
    """Process pydantic_pydantic collection with V4"""
    
    print("="*80)
    print("🚀 PROCESSING: pydantic_pydantic Collection")
    print("="*80)
    
    COLLECTION_NAME = "pydantic_pydantic"
    WORKING_DIR = "/kaggle/working"
    
    POSSIBLE_PATHS = [
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
        return None
    
    print(f"✅ Found collection at: {collection_path}")
    start_time = time.time()
    
    try:
        print(f"\n🔄 STEP 1: Initializing V4...")
        
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
        
        print(f"✅ V4 initialized! GPU Count: {embedder.device_count}")
        
        print(f"\n🔄 STEP 2: Loading chunks...")
        # Point to parent directory, V4 auto-discovers pydantic_pydantic subdirectory
        parent_dir = os.path.dirname(collection_path)  # Gets DOCS_CHUNKS_OUTPUT directory
        chunks_loaded = embedder.load_chunks_from_processing(
            chunks_dir=parent_dir
        )
        print(f"✅ Loaded {chunks_loaded['total_chunks']} chunks")
        
        print(f"\n🔄 STEP 3: Generating embeddings...")
        embedding_results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True,
            save_intermediate=True
        )
        print(f"✅ Generated {embedding_results.get('total_embeddings', 0)} embeddings")
        print(f"   ⚡ Speed: {embedding_results.get('chunks_per_second', 0):.1f} chunks/sec")
        
        print(f"\n🔄 STEP 4: Exporting...")
        export_files = embedder.export_for_local_qdrant()
        print(f"✅ Exported {len(export_files)} files")
        
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
        
        print(f"\n🎉 {COLLECTION_NAME} COMPLETE! Time: {results['processing_time_seconds']:.2f}s")
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {'collection': COLLECTION_NAME, 'status': 'ERROR', 'error': str(e)}

if __name__ == "__main__":
    results = process_pydantic_collection()
    print(f"\nStatus: {results['status'] if results else 'FAILED'}")
