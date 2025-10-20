#!/usr/bin/env python3
"""
Local Documentation Chunking Script
Chunk Docs folder locally, generate embeddings in Kaggle later

Usage:
    python scripts/chunk_docs_local.py
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chunk_docs.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main chunking workflow"""
    
    logger.info("="*70)
    logger.info("Documentation Chunking - Local Execution")
    logger.info("="*70)
    
    try:
        # Initialize chunker (CPU-friendly configuration)
        logger.info("Initializing chunker...")
        chunker = EnhancedUltimateChunkerV5Unified(
            target_model="jina-code-embeddings-1.5b",
            
            # CPU-only features (all enabled)
            use_tree_sitter=True,         # ✅ Code block parsing
            use_semchunk=True,            # ✅ Smart text boundaries
            extract_keywords=True,        # ✅ Keyword extraction
            generate_sparse_features=True, # ✅ Sparse features
            classify_content_type=True,   # ✅ Content classification
            preserve_hierarchy=True,      # ✅ Hierarchy preservation
            
            # GPU features (disabled for local CPU)
            use_docling=False,            # ❌ Not needed (no PDFs)
            enable_semantic_scoring=False, # ❌ No GPU needed
            
            # Quality settings
            safety_margin=0.8,  # Use 80% of 32K = 26,214 tokens
            fallback_promotion_ratio=0.25,
            fallback_promotion_cap=40
        )
        
        logger.info("✓ Chunker initialized")
        logger.info(f"  Target model: jina-code-embeddings-1.5b")
        logger.info(f"  Chunk size: ~26,214 tokens")
        logger.info(f"  Features: Tree-sitter, Semchunk, Keywords, Sparse, Hierarchy")
        
        # Process Docs directory
        logger.info("\n" + "="*70)
        logger.info("Processing Docs directory...")
        logger.info("="*70)
        
        summary = chunker.process_directory_smart(
            input_dir="Docs",
            output_dir="Chunked",
            file_extensions=[".md", ".txt", ".rst", ".py"]
        )
        
        # Display summary
        logger.info("\n" + "="*70)
        logger.info("Processing Summary")
        logger.info("="*70)
        logger.info(f"Files processed: {summary['processed_files']}")
        logger.info(f"Total chunks: {summary['total_chunks']}")
        logger.info(f"Processing time: {summary['processing_time']:.2f}s")
        logger.info(f"Throughput: {summary['total_chunks'] / summary['processing_time']:.2f} chunks/sec")
        
        logger.info("\nContent Types:")
        for ctype, count in summary['content_types'].items():
            logger.info(f"  {ctype}: {count} files")
        
        logger.info("\nChunking Strategies Used:")
        for strategy, count in summary['strategies_used'].items():
            logger.info(f"  {strategy}: {count} chunks")
        
        # Display chunker statistics
        logger.info("\n" + "="*70)
        logger.info("Chunker Statistics")
        logger.info("="*70)
        logger.info(f"Total documents: {chunker.stats['total_documents']}")
        logger.info(f"Total chunks: {chunker.stats['total_chunks']}")
        logger.info(f"Oversized chunks: {chunker.stats['oversized_chunks']}")
        logger.info(f"Quality promoted: {chunker.stats['quality_promoted']}")
        
        # Validate all chunks
        logger.info("\n" + "="*70)
        logger.info("Validating Chunks...")
        logger.info("="*70)
        
        # Load all chunks from Chunked directory
        import json
        all_chunks = []
        chunked_dir = Path("Chunked")
        
        for chunk_file in chunked_dir.glob("*_chunks.json"):
            with open(chunk_file) as f:
                chunks = json.load(f)
                all_chunks.extend(chunks)
        
        logger.info(f"Loaded {len(all_chunks)} chunks for validation")
        
        # Validate
        validation = chunker.validate_chunks(all_chunks)
        
        logger.info(f"Total chunks: {validation['total_chunks']}")
        logger.info(f"Valid chunks: {validation['valid_chunks']}")
        logger.info(f"Invalid chunks: {validation['invalid_chunks']}")
        logger.info(f"Model max tokens: {validation['model_max_tokens']}")
        
        if validation['validation_passed']:
            logger.info("✓ Validation PASSED - All chunks within token limits")
        else:
            logger.warning(f"⚠️  Validation FAILED - {validation['invalid_chunks']} oversized chunks")
            if validation['oversized_chunk_details']:
                logger.warning("First 5 oversized chunks:")
                for detail in validation['oversized_chunk_details'][:5]:
                    logger.warning(f"  Chunk {detail['chunk_index']}: "
                                 f"{detail['estimated_tokens']} tokens "
                                 f"(+{detail['overflow']} over limit)")
        
        # Success message
        logger.info("\n" + "="*70)
        logger.info("✓ CHUNKING COMPLETE!")
        logger.info("="*70)
        logger.info(f"Output directory: Chunked/")
        logger.info(f"Summary file: Chunked/chunk_summary.json")
        logger.info(f"Log file: chunk_docs.log")
        logger.info("")
        logger.info("Next Steps:")
        logger.info("  1. Upload chunks to Kaggle")
        logger.info("  2. Run embedder: kaggle_ultimate_embedder_v4.py")
        logger.info("  3. Download embeddings from Kaggle")
        logger.info("  4. Upload to Qdrant locally")
        logger.info("="*70)
        
        return 0
        
    except Exception as e:
        logger.error("\n" + "="*70)
        logger.error("✗ CHUNKING FAILED")
        logger.error("="*70)
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())