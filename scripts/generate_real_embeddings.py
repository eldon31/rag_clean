#!/usr/bin/env python3
"""
Generate Real CodeRankEmbed (768-dim) Embeddings

This script generates REAL embeddings from chunked data using the embedder_template,
replacing the fake data in output/embed_outputs/ with legitimate CodeRankEmbed vectors.

USAGE:
    # Generate embeddings for all collections
    python scripts/generate_real_embeddings.py --all
    
    # Generate for specific collection
    python scripts/generate_real_embeddings.py --collection qdrant_ecosystem
    
    # CPU-only mode (slower but doesn't require GPU)
    python scripts/generate_real_embeddings.py --all --cpu-only

INPUT:
    - output/qdrant_ecosystem_chunked/     (chunked data)
    - output/docling-project_docling_chunked/
    - output/sentence_transformers_docs_chunked/

OUTPUT:
    - output/embed_outputs/qdrant_ecosystem_embeddings_768_REAL.jsonl
    - output/embed_outputs/docling_embeddings_768_REAL.jsonl  
    - output/embed_outputs/sentence_transformers_embeddings_768_REAL.jsonl

FEATURES:
    - Uses CodeRankEmbed (nomic-ai/CodeRankEmbed) for 768-dim vectors
    - Optimized for code and technical documentation
    - Batch processing with progress tracking
    - GPU acceleration (if available)
    - Preserves all metadata from chunked files
    - Deterministic IDs for Qdrant compatibility
    - JSONL format ready for Qdrant upload

QDRANT COMPATIBILITY:
    - Vector dimension: 768 (matches collection config)
    - Distance metric: Cosine similarity
    - ID format: Deterministic hex strings
    - Payload: text + metadata (subdirectory, source_file, etc.)
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.templates.embedder_template import UniversalEmbedder, EmbedderConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Collection mapping: collection_name -> (input_folder, output_file)
COLLECTION_MAPPING = {
    "qdrant_ecosystem": {
        "input_folder": "output/qdrant_ecosystem_chunked",
        "output_file": "output/embed_outputs/qdrant_ecosystem_embeddings_768_REAL.jsonl",
        "description": "Qdrant ecosystem documentation and examples"
    },
    "docling": {
        "input_folder": "output/docling-project_docling_chunked", 
        "output_file": "output/embed_outputs/docling_embeddings_768_REAL.jsonl",
        "description": "Docling project documentation"
    },
    "sentence_transformers": {
        "input_folder": "output/sentence_transformers_docs_chunked",
        "output_file": "output/embed_outputs/sentence_transformers_embeddings_768_REAL.jsonl", 
        "description": "Sentence Transformers documentation"
    }
}


def validate_input_folder(folder_path: Path) -> bool:
    """Validate that input folder exists and has chunk files."""
    if not folder_path.exists():
        logger.error(f"❌ Input folder not found: {folder_path}")
        return False
    
    # Check for chunk files (JSON)
    chunk_files = list(folder_path.rglob("*.json"))
    if not chunk_files:
        logger.error(f"❌ No chunk files (*.json) found in: {folder_path}")
        return False
    
    logger.info(f"✅ Found {len(chunk_files)} chunk files in {folder_path}")
    return True


def generate_embeddings_for_collection(
    collection_name: str,
    use_gpu: bool = True,
    force: bool = False
) -> bool:
    """Generate embeddings for a single collection."""
    
    if collection_name not in COLLECTION_MAPPING:
        logger.error(f"❌ Unknown collection: {collection_name}")
        logger.error(f"   Available: {', '.join(COLLECTION_MAPPING.keys())}")
        return False
    
    config = COLLECTION_MAPPING[collection_name]
    input_path = Path(config["input_folder"])
    output_path = Path(config["output_file"])
    
    logger.info(f"\n{'='*60}")
    logger.info(f"GENERATING: {collection_name}")
    logger.info(f"{'='*60}")
    logger.info(f"Description: {config['description']}")
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")
    logger.info(f"GPU: {'Yes' if use_gpu else 'No (CPU-only)'}")
    
    # Validate input
    if not validate_input_folder(input_path):
        return False
    
    # Check if output exists
    if output_path.exists() and not force:
        logger.warning(f"⚠️  Output file already exists: {output_path}")
        logger.warning(f"   Use --force to overwrite")
        return False
    
    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure embedder
    try:
        embedder_config = EmbedderConfig(
            collection_name=collection_name,
            input_path=input_path,
            output_path=output_path,
            use_gpu=use_gpu,
            use_data_parallel=False  # Single GPU for local use
        )
        
        # Initialize embedder
        logger.info("🔧 Initializing CodeRankEmbed embedder...")
        embedder = UniversalEmbedder(embedder_config)
        
        # Generate embeddings
        start_time = time.time()
        logger.info("🚀 Starting embedding generation...")
        
        embedder.run()
        
        elapsed = time.time() - start_time
        
        # Validate output
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f if line.strip())
            
            logger.info(f"✅ Generated {line_count:,} embeddings")
            logger.info(f"⏱️  Processing time: {elapsed:.1f} seconds")
            logger.info(f"📁 Output saved to: {output_path}")
            
            if line_count == 0:
                logger.error("❌ No embeddings generated!")
                return False
                
            return True
        else:
            logger.error("❌ Output file was not created!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error generating embeddings: {e}")
        logger.exception("Full traceback:")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate real CodeRankEmbed embeddings from chunked data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help="Generate embeddings for all collections"
    )
    parser.add_argument(
        '--collection',
        type=str,
        choices=list(COLLECTION_MAPPING.keys()),
        help="Generate embeddings for specific collection"
    )
    parser.add_argument(
        '--cpu-only',
        action='store_true',
        help="Use CPU-only mode (no GPU acceleration)"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Overwrite existing output files"
    )
    parser.add_argument(
        '--list-collections',
        action='store_true',
        help="List available collections and exit"
    )
    
    args = parser.parse_args()
    
    # List collections and exit
    if args.list_collections:
        print("\nAvailable Collections:")
        print("=" * 60)
        for name, config in COLLECTION_MAPPING.items():
            print(f"📚 {name}")
            print(f"   Description: {config['description']}")
            print(f"   Input: {config['input_folder']}")
            print(f"   Output: {config['output_file']}")
            print()
        return 0
    
    # Validate arguments
    if not args.all and not args.collection:
        parser.error("Must specify --all or --collection")
    
    logger.info("=" * 60)
    logger.info("REAL EMBEDDING GENERATION - CodeRankEmbed (768-dim)")
    logger.info("=" * 60)
    logger.info(f"Model: nomic-ai/CodeRankEmbed")
    logger.info(f"Dimension: 768")
    logger.info(f"GPU: {'Disabled (CPU-only)' if args.cpu_only else 'Enabled (if available)'}")
    logger.info(f"Force overwrite: {args.force}")
    logger.info("=" * 60)
    
    # Determine collections to process
    if args.all:
        collections_to_process = list(COLLECTION_MAPPING.keys())
    else:
        collections_to_process = [args.collection]
    
    # Process collections
    results = {}
    for collection_name in collections_to_process:
        success = generate_embeddings_for_collection(
            collection_name=collection_name,
            use_gpu=not args.cpu_only,
            force=args.force
        )
        results[collection_name] = success
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("GENERATION SUMMARY")
    logger.info("=" * 60)
    
    successful = [name for name, success in results.items() if success]
    failed = [name for name, success in results.items() if not success]
    
    logger.info(f"✅ Successful: {len(successful)}/{len(results)}")
    for name in successful:
        output_file = COLLECTION_MAPPING[name]["output_file"]
        logger.info(f"  ✅ {name} → {output_file}")
    
    if failed:
        logger.info(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for name in failed:
            logger.info(f"  ❌ {name}")
    
    logger.info("=" * 60)
    
    if successful:
        logger.info("\n🎉 Real embeddings generated successfully!")
        logger.info("   Next steps:")
        logger.info("   1. Update migrate_to_coderank.py to use *_REAL.jsonl files")
        logger.info("   2. Run migration: python scripts/migrate_to_coderank.py --all")
        logger.info("   3. Verify: python scripts/verify_migration.py")
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())