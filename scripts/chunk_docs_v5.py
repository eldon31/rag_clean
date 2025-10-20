#!/usr/bin/env python3
"""
V5 Document Chunking Script - Simplified for Kaggle

Automatically chunks documents with sensible defaults.
Just run: python scripts/chunk_docs_v5.py

Default behavior:
- Input: /kaggle/working/rag_clean/Docs
- Output: /kaggle/working/rag_clean/Chunked
- Model: jina-code-embeddings-1.5b (1536D Matryoshka)
- Sparse features: enabled
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from processor.enhanced_ultimate_chunker_v5 import EnhancedUltimateChunkerV5
from processor.kaggle_ultimate_embedder_v4 import KAGGLE_OPTIMIZED_MODELS
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution with defaults for Kaggle"""
    
    # Default paths (Kaggle structure)
    input_dir = "/kaggle/working/rag_clean/Docs"
    output_dir = "/kaggle/working/rag_clean/Chunked"
    model_name = "jina-code-embeddings-1.5b"
    
    # Override from command line if provided
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        model_name = sys.argv[3]
    
    logger.info("="*80)
    logger.info("V5 DOCUMENT CHUNKING")
    logger.info("="*80)
    logger.info(f"Input Directory: {input_dir}")
    logger.info(f"Output Directory: {output_dir}")
    logger.info(f"Model: {model_name}")
    logger.info("="*80)
    
    # Validate paths
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.error(f"Input directory not found: {input_path}")
        logger.info("\nUsage: python scripts/chunk_docs_v5.py [input_dir] [output_dir] [model]")
        logger.info("  Defaults:")
        logger.info("    input_dir: /kaggle/working/rag_clean/Docs")
        logger.info("    output_dir: /kaggle/working/rag_clean/Chunked")
        logger.info("    model: jina-code-embeddings-1.5b")
        sys.exit(1)
    
    # Get model config
    if model_name not in KAGGLE_OPTIMIZED_MODELS:
        logger.error(f"Unknown model: {model_name}")
        logger.info(f"Available models: {', '.join(KAGGLE_OPTIMIZED_MODELS.keys())}")
        sys.exit(1)
    
    model_config = KAGGLE_OPTIMIZED_MODELS[model_name]
    logger.info(f"\nModel Configuration:")
    logger.info(f"  Max Tokens: {model_config.max_tokens:,}")
    logger.info(f"  Vector Dimension: {model_config.vector_dim}")
    logger.info(f"  Matryoshka Support: {'Yes (1536D full dimension)' if model_name == 'jina-code-embeddings-1.5b' else 'Unknown'}")
    logger.info(f"  Chunk Size: {int(model_config.max_tokens * 0.8):,} tokens (80% safety margin)")
    
    # Initialize chunker with defaults
    logger.info("\nInitializing V5 Chunker...")
    try:
        chunker = EnhancedUltimateChunkerV5(
            target_model=model_name,
            generate_sparse_features=True,  # Always enable for V5
            extract_keywords=True,
            classify_content_type=True
        )
        logger.info("✓ Chunker initialized")
    except Exception as e:
        logger.error(f"Failed to initialize chunker: {e}")
        sys.exit(1)
    
    # Collect all files recursively
    logger.info(f"\nScanning {input_path}...")
    all_files = list(input_path.rglob("*"))
    doc_files = [f for f in all_files if f.is_file() and not f.name.startswith('.')]
    
    logger.info(f"Found {len(doc_files)} files")
    
    if not doc_files:
        logger.warning("No files found to process")
        sys.exit(0)
    
    # Process documents
    logger.info("\nChunking documents...")
    results = chunker.chunk_documents(
        file_paths=[str(f) for f in doc_files],
        output_dir=output_dir
    )
    
    # Summary
    logger.info("\n" + "="*80)
    logger.info("CHUNKING COMPLETE")
    logger.info("="*80)
    logger.info(f"Total Chunks: {len(results)}")
    logger.info(f"Output Directory: {output_dir}")
    
    # Validate
    validation = chunker.validate_chunks(results)
    if validation.get('validation_passed', True):
        logger.info("✓ All chunks within token limits")
    else:
        logger.warning(f"⚠️  {validation['invalid_chunks']} chunks exceed token limit")
    
    logger.info("="*80)


if __name__ == "__main__":
    main()