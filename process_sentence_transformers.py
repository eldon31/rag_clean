#!/usr/bin/env python3
"""
🚀 KAGGLE PROCESSOR: Sentence_Transformers Collection (CORRECTED V4 API)
Ultimate Embedder V4 - Single Collection Processing

✅ CORRECTED PARAMETERS (verified from source audit):
   - enable_ensemble=False (NOT enable_reranking)
   - output_prefix in KaggleExportConfig (NOT collection_name)
   - chunks_dir in load_chunks_from_processing (auto-discovers collections)
   - enable_monitoring, save_intermediate in generate_embeddings_kaggle_optimized
   - export_for_local_qdrant() takes NO parameters

USAGE IN KAGGLE JUPYTER:
    exec(open('process_sentence_transformers.py').read())
"""

import os
import json
import time
import logging
import zipfile
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from kaggle_ultimate_embedder_v4 import (
    UltimateKaggleEmbedderV4,
    KaggleGPUConfig,
    KaggleExportConfig,
    AdvancedPreprocessingConfig
)

def process_sentence_transformers_collection():
    """Process Sentence_Transformers collection with V4"""
    
    print("="*80)
    print("🚀 PROCESSING: Sentence_Transformers Collection")
    print("="*80)
    
    COLLECTION_NAME = "Sentence_Transformers"
    WORKING_DIR = "/kaggle/working"
    
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
        # Point directly to this collection's directory
        chunks_loaded = embedder.load_chunks_from_processing(
            chunks_dir=collection_path
        )
        print(f"✅ Loaded {chunks_loaded.get('total_chunks_loaded', 0)} chunks")
        
        print(f"\n🔄 STEP 3: Generating embeddings...")
        embedding_results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True,
            save_intermediate=True
        )
        print(f"✅ Generated {embedding_results.get('total_embeddings_generated', 0)} embeddings")
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
        
        # Create ZIP archive of all output files
        print(f"\n📦 Creating ZIP archive...")
        zip_filename = f"{COLLECTION_NAME}_v4_outputs.zip"
        zip_path = f"{WORKING_DIR}/{zip_filename}"
        
        # Collect all output files
        files_to_zip = []
        for file_type, file_path in export_files.items():
            if os.path.exists(file_path):
                files_to_zip.append((file_path, os.path.basename(file_path)))
        # Add results JSON
        files_to_zip.append((results_file, os.path.basename(results_file)))
        
        # Create ZIP
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, arcname in files_to_zip:
                zipf.write(file_path, arcname)
                size_kb = os.path.getsize(file_path) / 1024
                print(f"   ✅ Added: {arcname:40s} {size_kb:8.1f} KB")
        
        zip_size_mb = os.path.getsize(zip_path) / 1024 / 1024
        
        print(f"\n🎉 {COLLECTION_NAME} COMPLETE! Time: {results['processing_time_seconds']:.2f}s")
        print(f"   📦 ZIP: {zip_filename} ({zip_size_mb:.2f} MB)")
        print(f"   📥 Download from: /kaggle/working/{zip_filename}")
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {'collection': COLLECTION_NAME, 'status': 'ERROR', 'error': str(e)}

if __name__ == "__main__":
    results = process_sentence_transformers_collection()
    print(f"\nStatus: {results['status'] if results else 'FAILED'}")
