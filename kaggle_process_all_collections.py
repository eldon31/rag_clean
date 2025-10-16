#!/usr/bin/env python3
"""
🚀 KAGGLE COLLECTION PROCESSOR - ULTIMATE EMBEDDER V4
Process all collections from DOCS_CHUNKS_OUTPUT with V4 pipeline

USAGE IN KAGGLE JUPYTER (connected to VSCode):
    %run kaggle_process_all_collections.py
    
Or in Python cell:
    exec(open('kaggle_process_all_collections.py').read())
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import shutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# 🎯 CONFIGURATION
# ============================================================================

# Local path (will be uploaded to Kaggle)
LOCAL_CHUNKS_PATH = r"C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG\RAG_CLEAN\DOCS_CHUNKS_OUTPUT"

# Kaggle working directory
KAGGLE_WORKING_DIR = "/kaggle/working"
KAGGLE_INPUT_DIR = "/kaggle/input"  # If you upload as dataset

# Output configuration
OUTPUT_BASE_DIR = f"{KAGGLE_WORKING_DIR}/embeddings_output"
RESULTS_FILE = f"{KAGGLE_WORKING_DIR}/processing_results.json"

# Model selection (choose one or process with multiple)
DEFAULT_MODEL = "nomic-coderank"  # Best for code/docs
ALTERNATIVE_MODELS = ["bge-m3", "gte-large", "all-miniLM-l6"]

# ============================================================================
# 🔍 COLLECTION DISCOVERY
# ============================================================================

def discover_collections(base_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Discover all collections in DOCS_CHUNKS_OUTPUT directory
    Each collection is a level 1 subdirectory with JSON files
    """
    logger.info(f"🔍 Discovering collections in: {base_path}")
    
    collections = {}
    base_path_obj = Path(base_path)
    
    if not base_path_obj.exists():
        logger.error(f"❌ Path not found: {base_path}")
        return collections
    
    # Scan level 1 subdirectories
    for item in base_path_obj.iterdir():
        if item.is_dir():
            collection_name = item.name
            json_files = list(item.glob("*.json"))
            
            if json_files:
                collections[collection_name] = {
                    "path": str(item),
                    "json_files": [str(f) for f in json_files],
                    "file_count": len(json_files),
                    "total_size_mb": sum(f.stat().st_size for f in json_files) / 1024 / 1024
                }
                
                logger.info(f"  📦 {collection_name}: {len(json_files)} JSON files ({collections[collection_name]['total_size_mb']:.2f}MB)")
    
    logger.info(f"✅ Found {len(collections)} collections")
    return collections

# ============================================================================
# 📥 COLLECTION LOADING
# ============================================================================

def load_collection_chunks(collection_path: str) -> List[Dict[str, Any]]:
    """
    Load all JSON chunks from a collection directory
    """
    chunks = []
    collection_path_obj = Path(collection_path)
    
    for json_file in collection_path_obj.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Handle both single dict and list of dicts
                if isinstance(data, list):
                    chunks.extend(data)
                else:
                    chunks.append(data)
                    
        except Exception as e:
            logger.warning(f"⚠️ Error loading {json_file.name}: {e}")
    
    return chunks

# ============================================================================
# 🚀 V4 PROCESSING PIPELINE
# ============================================================================

def process_collection_with_v4(
    collection_name: str,
    collection_path: str,
    model_name: str = "nomic-coderank",
    gpu_config: Any = None,
    export_config: Any = None
) -> Dict[str, Any]:
    """
    Process a single collection with Ultimate Kaggle Embedder V4
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"🚀 PROCESSING COLLECTION: {collection_name}")
    logger.info(f"{'='*70}")
    
    start_time = time.time()
    
    try:
        # Import V4 classes (must be available in notebook)
        from kaggle_ultimate_embedder_v4 import (
            UltimateKaggleEmbedderV4,
            KaggleGPUConfig,
            KaggleExportConfig,
            AdvancedPreprocessingConfig
        )
        
        # Load chunks
        logger.info(f"📂 Loading chunks from: {collection_path}")
        chunks = load_collection_chunks(collection_path)
        
        if not chunks:
            logger.warning(f"⚠️ No chunks found in {collection_name}")
            return {
                "status": "SKIPPED",
                "reason": "No chunks found",
                "collection_name": collection_name
            }
        
        logger.info(f"✅ Loaded {len(chunks)} chunks")
        
        # Initialize V4 embedder
        logger.info(f"🔄 Initializing V4 Embedder with model: {model_name}")
        
        embedder = UltimateKaggleEmbedderV4(
            model_name=model_name,
            gpu_config=gpu_config or KaggleGPUConfig(
                base_batch_size=32,
                dynamic_batching=True,
                precision="fp16",
                enable_torch_compile=True
            ),
            export_config=export_config or KaggleExportConfig(
                working_dir=f"{OUTPUT_BASE_DIR}/{collection_name}",
                export_numpy=True,
                export_jsonl=True,
                export_faiss=True,
                output_prefix=f"{collection_name}_v4"
            ),
            preprocessing_config=AdvancedPreprocessingConfig(
                enable_text_caching=True,
                quality_filtering=True,
                min_chunk_length=50
            ),
            enable_reranking=False  # Disable for speed
        )
        
        logger.info(f"✅ V4 Embedder initialized!")
        logger.info(f"🎯 Model: {embedder.model_name}")
        logger.info(f"🔥 GPU Count: {embedder.device_count}")
        logger.info(f"📊 Vector Dimension: {embedder.model_config.vector_dim}")
        
        # Prepare chunk texts and metadata
        logger.info(f"🔄 Preparing chunks for embedding generation...")
        chunk_texts = []
        chunks_metadata = []
        
        for idx, chunk in enumerate(chunks):
            # Extract text
            if isinstance(chunk, dict):
                text = chunk.get('text', chunk.get('content', str(chunk)))
                metadata = chunk.get('metadata', {})
            else:
                text = str(chunk)
                metadata = {}
            
            # Preprocess
            processed_text = embedder.preprocess_text_advanced(text)
            chunk_texts.append(processed_text)
            
            # Enhanced metadata
            metadata.update({
                "collection": collection_name,
                "chunk_id": idx,
                "original_length": len(text),
                "processed_length": len(processed_text)
            })
            chunks_metadata.append(metadata)
        
        # Store in embedder
        embedder.chunk_texts = chunk_texts
        embedder.chunks_metadata = chunks_metadata
        
        logger.info(f"✅ Prepared {len(chunk_texts)} chunks")
        
        # Generate embeddings
        logger.info(f"🔥 Generating embeddings with V4 pipeline...")
        logger.info(f"🎯 Target speed: 310-516 chunks/sec")
        
        embedding_results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True
        )
        
        logger.info(f"✅ Embeddings generated!")
        logger.info(f"📊 Total embeddings: {embedding_results['total_embeddings_generated']}")
        logger.info(f"📏 Dimension: {embedding_results['embedding_dimension']}")
        logger.info(f"⚡ Speed: {embedding_results['chunks_per_second']:.1f} chunks/sec")
        logger.info(f"⏱️ Time: {embedding_results['processing_time_seconds']:.2f}s")
        logger.info(f"💾 Memory: {embedding_results['embedding_memory_mb']:.1f}MB")
        
        # Performance assessment
        speed = embedding_results['chunks_per_second']
        if speed >= 310:
            logger.info(f"🏆 PERFORMANCE: EXCELLENT! Meeting V4 targets")
        elif speed >= 200:
            logger.info(f"✅ PERFORMANCE: GOOD! Production-ready")
        else:
            logger.info(f"⚠️ PERFORMANCE: Below target")
        
        # Export for local Qdrant
        logger.info(f"📦 Exporting to local Qdrant format...")
        
        # Create output directory
        os.makedirs(f"{OUTPUT_BASE_DIR}/{collection_name}", exist_ok=True)
        
        export_files = embedder.export_for_local_qdrant()
        
        logger.info(f"✅ Export complete!")
        for file_type, file_path in export_files.items():
            if os.path.exists(file_path):
                file_size_mb = os.path.getsize(file_path) / 1024 / 1024
                logger.info(f"  📁 {file_type}: {os.path.basename(file_path)} ({file_size_mb:.1f}MB)")
        
        # Calculate total processing time
        total_time = time.time() - start_time
        
        # Return comprehensive results
        return {
            "status": "SUCCESS",
            "collection_name": collection_name,
            "model_used": model_name,
            "chunks_processed": len(chunks),
            "embeddings_generated": embedding_results['total_embeddings_generated'],
            "embedding_dimension": embedding_results['embedding_dimension'],
            "processing_time_seconds": total_time,
            "embedding_generation_seconds": embedding_results['processing_time_seconds'],
            "chunks_per_second": embedding_results['chunks_per_second'],
            "memory_usage_mb": embedding_results['embedding_memory_mb'],
            "export_files": export_files,
            "gpu_count": embedding_results['gpu_count'],
            "backend": embedding_results['backend'],
            "precision": embedding_results['precision'],
            "performance_rating": "EXCELLENT" if speed >= 310 else "GOOD" if speed >= 200 else "NEEDS_OPTIMIZATION",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing {collection_name}: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "status": "ERROR",
            "collection_name": collection_name,
            "error": str(e),
            "error_type": type(e).__name__,
            "processing_time_seconds": time.time() - start_time,
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# 📊 BATCH PROCESSING
# ============================================================================

def process_all_collections(
    collections: Dict[str, Dict[str, Any]],
    model_name: str = "nomic-coderank",
    process_in_priority_order: bool = True
) -> Dict[str, Any]:
    """
    Process all collections in batch
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"🚀 BATCH PROCESSING ALL COLLECTIONS")
    logger.info(f"{'='*70}")
    logger.info(f"📊 Total collections: {len(collections)}")
    logger.info(f"🎯 Model: {model_name}")
    
    # Collection priority (based on importance)
    collection_priority = {
        "Docling": 1,
        "pydantic_pydantic": 2,
        "Qdrant": 3,
        "FAST_DOCS": 4,
        "Sentence_Transformers": 5
    }
    
    # Sort by priority if enabled
    if process_in_priority_order:
        sorted_collections = sorted(
            collections.items(),
            key=lambda x: collection_priority.get(x[0], 99)
        )
    else:
        sorted_collections = list(collections.items())
    
    # Process each collection
    all_results = {}
    successful = 0
    failed = 0
    skipped = 0
    
    for idx, (collection_name, collection_info) in enumerate(sorted_collections, 1):
        logger.info(f"\n{'='*70}")
        logger.info(f"📍 Collection {idx}/{len(collections)}: {collection_name}")
        logger.info(f"{'='*70}")
        
        result = process_collection_with_v4(
            collection_name=collection_name,
            collection_path=collection_info['path'],
            model_name=model_name
        )
        
        all_results[collection_name] = result
        
        # Update counters
        if result['status'] == 'SUCCESS':
            successful += 1
        elif result['status'] == 'ERROR':
            failed += 1
        else:
            skipped += 1
    
    # Generate summary
    summary = {
        "total_collections": len(collections),
        "successful": successful,
        "failed": failed,
        "skipped": skipped,
        "model_used": model_name,
        "results": all_results,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save results
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n{'='*70}")
    logger.info(f"🎉 BATCH PROCESSING COMPLETE!")
    logger.info(f"{'='*70}")
    logger.info(f"✅ Successful: {successful}/{len(collections)}")
    logger.info(f"❌ Failed: {failed}/{len(collections)}")
    logger.info(f"⚠️ Skipped: {skipped}/{len(collections)}")
    logger.info(f"📄 Results saved to: {RESULTS_FILE}")
    
    return summary

# ============================================================================
# 📊 RESULTS DISPLAY
# ============================================================================

def display_results_summary(summary: Dict[str, Any]):
    """
    Display a formatted summary of processing results
    """
    print("\n" + "="*70)
    print("📊 ULTIMATE EMBEDDER V4 - PROCESSING SUMMARY")
    print("="*70)
    
    print(f"\n🎯 Overall Status:")
    print(f"   Total Collections: {summary['total_collections']}")
    print(f"   ✅ Successful: {summary['successful']}")
    print(f"   ❌ Failed: {summary['failed']}")
    print(f"   ⚠️ Skipped: {summary['skipped']}")
    print(f"   🤖 Model: {summary['model_used']}")
    
    print(f"\n📋 Collection Details:")
    print("="*70)
    
    total_embeddings = 0
    total_time = 0
    
    for collection_name, result in summary['results'].items():
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌" if result['status'] == 'ERROR' else "⚠️"
        
        print(f"\n{status_icon} {collection_name}:")
        
        if result['status'] == 'SUCCESS':
            print(f"   📊 Chunks: {result['chunks_processed']}")
            print(f"   🚀 Embeddings: {result['embeddings_generated']}")
            print(f"   📏 Dimension: {result['embedding_dimension']}")
            print(f"   ⚡ Speed: {result['chunks_per_second']:.1f} chunks/sec")
            print(f"   ⏱️ Time: {result['processing_time_seconds']:.2f}s")
            print(f"   💾 Memory: {result['memory_usage_mb']:.1f}MB")
            print(f"   🏆 Performance: {result['performance_rating']}")
            print(f"   📦 Export files: {len(result['export_files'])}")
            
            total_embeddings += result['embeddings_generated']
            total_time += result['processing_time_seconds']
            
        elif result['status'] == 'ERROR':
            print(f"   ❌ Error: {result['error']}")
            print(f"   🔍 Type: {result['error_type']}")
        else:
            print(f"   ⚠️ Reason: {result.get('reason', 'Unknown')}")
    
    if summary['successful'] > 0:
        print(f"\n📊 Aggregate Statistics:")
        print("="*70)
        print(f"   🚀 Total Embeddings: {total_embeddings:,}")
        print(f"   ⏱️ Total Time: {total_time:.2f}s")
        print(f"   ⚡ Overall Speed: {total_embeddings/total_time:.1f} chunks/sec" if total_time > 0 else "   ⚡ Overall Speed: N/A")
        print(f"   📦 Output Directory: {OUTPUT_BASE_DIR}")
    
    print("\n" + "="*70)
    print("🎉 PROCESSING COMPLETE!")
    print("="*70)

# ============================================================================
# 🚀 MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function
    """
    print("="*70)
    print("🚀 KAGGLE ULTIMATE EMBEDDER V4 - COLLECTION PROCESSOR")
    print("="*70)
    print(f"📂 Source: {LOCAL_CHUNKS_PATH}")
    print(f"📁 Output: {OUTPUT_BASE_DIR}")
    print("="*70)
    
    # Create output directory
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    
    # Discover collections
    collections = discover_collections(LOCAL_CHUNKS_PATH)
    
    if not collections:
        logger.error("❌ No collections found!")
        return
    
    # Process all collections
    summary = process_all_collections(
        collections=collections,
        model_name=DEFAULT_MODEL,
        process_in_priority_order=True
    )
    
    # Display results
    display_results_summary(summary)
    
    # Instructions for next steps
    print("\n📋 Next Steps:")
    print("="*70)
    print("1. Download all files from /kaggle/working/embeddings_output/")
    print("2. Transfer to your local machine")
    print("3. Run the generated upload scripts to populate Qdrant")
    print("4. Check processing_results.json for detailed statistics")
    print("="*70)

if __name__ == "__main__":
    main()
