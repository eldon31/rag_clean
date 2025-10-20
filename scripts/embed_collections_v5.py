#!/usr/bin/env python3
"""
V5 Embedding Script - Simplified with Defaults
Loads chunks and generates embeddings using kaggle_ultimate_embedder_v4.py

DEFAULT PATHS (Kaggle structure):
- Input:  /kaggle/working/rag_clean/Chunked
- Output: /kaggle/working/rag_clean/Embeddings
- Model:  jina-code-embeddings-1.5b
- Matryoshka: 1536 (full dimension)

USAGE:
    # With defaults (full 1536D embeddings):
    python scripts/embed_collections_v5.py
    
    # With custom model/paths:
    python scripts/embed_collections_v5.py <chunks_dir> <output_dir> <model_name> <matryoshka_dim>
    
    # Example with Matryoshka truncation (1536D → 1024D):
    python scripts/embed_collections_v5.py ./Chunked ./Embeddings jina-code-embeddings-1.5b 1024
    
    # Example with different model:
    python scripts/embed_collections_v5.py ./Chunked ./Embeddings nomic-coderank none
"""

import sys
import json
import logging
import time
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.kaggle_ultimate_embedder_v4 import UltimateKaggleEmbedderV4

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main embedding workflow"""
    
    # ============================================================================
    # DEFAULTS (Kaggle structure)
    # ============================================================================
    chunks_dir = "/kaggle/working/rag_clean/Chunked"
    output_dir = "/kaggle/working/rag_clean/Embeddings"
    model_name = "jina-code-embeddings-1.5b"
    matryoshka_dim = 1536  # Full dimension (Matryoshka-capable model)
    
    # ============================================================================
    # OPTIONAL: Override via sys.argv
    # ============================================================================
    if len(sys.argv) > 1:
        chunks_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        model_name = sys.argv[3]
    if len(sys.argv) > 4:
        dim_arg = sys.argv[4]
        matryoshka_dim = None if dim_arg.lower() in ('none', 'null', '0') else int(dim_arg)
    
    # ============================================================================
    # CONFIGURATION
    # ============================================================================
    logger.info("="*80)
    logger.info("V5 EMBEDDING GENERATION")
    logger.info("="*80)
    logger.info(f"Chunks Dir:      {chunks_dir}")
    logger.info(f"Output Dir:      {output_dir}")
    logger.info(f"Model:           {model_name}")
    if matryoshka_dim:
        logger.info(f"Matryoshka Dim:  {matryoshka_dim}D (truncated)")
    else:
        logger.info(f"Matryoshka Dim:  Full (no truncation)")
    logger.info("="*80)
    
    # V5 Features
    enable_sparse = True  # Enable sparse embeddings for hybrid search
    sparse_models = ["qdrant-bm25"]  # BM25-style sparse vectors
    companion_models = None  # Optional: add companion dense models
    
    # ============================================================================
    # STEP 1: Initialize Embedder
    # ============================================================================
    logger.info("\nInitializing embedder...")
    try:
        embedder = UltimateKaggleEmbedderV4(
            model_name=model_name,
            enable_sparse=enable_sparse,
            sparse_models=sparse_models,
            matryoshka_dim=matryoshka_dim,
            companion_dense_models=companion_models,
        )
        logger.info("✓ Embedder initialized")
    except Exception as e:
        logger.error(f"Failed to initialize embedder: {e}")
        sys.exit(1)
    
    # ============================================================================
    # STEP 2: Load Chunks
    # ============================================================================
    logger.info(f"\nLoading chunks from: {chunks_dir}")
    try:
        load_results = embedder.load_chunks_from_processing(chunks_dir=chunks_dir)
        
        total_chunks = load_results.get('total_chunks_loaded', 0)
        if total_chunks == 0:
            logger.error("No chunks loaded!")
            sys.exit(1)
        
        logger.info(f"✓ Loaded {total_chunks} chunks")
        logger.info(f"  Collections: {load_results.get('collections_loaded', 0)}")
        logger.info(f"  Memory: {load_results.get('memory_usage_mb', 0):.1f}MB")
        
        if load_results.get('sparse_vectors_generated', 0) > 0:
            logger.info(f"  Sparse vectors: {load_results['sparse_vectors_generated']}")
        
    except Exception as e:
        logger.error(f"Failed to load chunks: {e}")
        sys.exit(1)
    
    # ============================================================================
    # STEP 3: Generate Embeddings
    # ============================================================================
    logger.info("\nGenerating embeddings (this may take a while)...")
    start_time = time.time()
    
    try:
        embed_results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True,
            save_intermediate=True
        )
        
        elapsed = time.time() - start_time
        
        logger.info(f"\n✓ Embeddings generated in {elapsed:.1f}s")
        logger.info(f"  Total: {embed_results['total_embeddings_generated']}")
        logger.info(f"  Dimension: {embed_results['embedding_dimension']}D")
        logger.info(f"  Speed: {embed_results['chunks_per_second']:.1f} chunks/sec")
        logger.info(f"  Memory: {embed_results['embedding_memory_mb']:.1f}MB")
        
        if 'companion_models' in embed_results:
            logger.info(f"  Companion models: {len(embed_results['companion_models'])}")
        
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        sys.exit(1)
    
    # ============================================================================
    # STEP 4: Export to Qdrant Format
    # ============================================================================
    logger.info("\nExporting to Qdrant format...")
    
    try:
        export_results = embedder.export_for_local_qdrant()
        
        # Get collection name
        collection_name = embedder.get_target_collection_name()
        
        logger.info(f"✓ Export complete")
        logger.info(f"  Collection: {collection_name}")
        logger.info(f"  Files exported: {len(export_results)}")
        
        # Log key files
        if 'jsonl' in export_results:
            logger.info(f"  JSONL: {Path(export_results['jsonl']).name}")
        if 'numpy' in export_results:
            logger.info(f"  NumPy: {Path(export_results['numpy']).name}")
        if 'upload_script' in export_results:
            logger.info(f"  Upload Script: {Path(export_results['upload_script']).name}")
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        sys.exit(1)
    
    # ============================================================================
    # STEP 5: Create Download Package (Kaggle)
    # ============================================================================
    if '/kaggle' in str(Path.cwd()):
        logger.info("\nCreating download package...")
        try:
            zip_base = "/kaggle/working/embeddings_v5"
            
            # Get the working directory from export config
            working_dir = embedder.export_config.working_dir
            
            shutil.make_archive(zip_base, 'zip', working_dir)
            logger.info(f"✓ Package created: {zip_base}.zip")
        except Exception as e:
            logger.warning(f"Failed to create ZIP: {e}")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    logger.info("\n" + "="*80)
    logger.info("EMBEDDING COMPLETE")
    logger.info("="*80)
    logger.info(f"Total Chunks:    {total_chunks}")
    logger.info(f"Embedding Dim:   {embed_results['embedding_dimension']}D")
    logger.info(f"Processing Time: {elapsed:.1f}s")
    logger.info(f"Collection Name: {collection_name}")
    
    if '/kaggle' in str(Path.cwd()):
        logger.info(f"\n📥 Download embeddings_v5.zip from Kaggle Output panel")
        logger.info(f"📤 Then run the upload script on your local machine")
    
    logger.info("="*80)


if __name__ == "__main__":
    main()
