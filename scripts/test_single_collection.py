#!/usr/bin/env python3
"""Test chunking for a single collection to verify the new structure"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Test with Docling collection (smallest)"""
    
    # Initialize chunker
    logger.info("Initializing chunker...")
    chunker = EnhancedUltimateChunkerV5Unified(
        target_model="jina-code-embeddings-1.5b",
        use_tree_sitter=True,
        use_semchunk=True,
        safety_margin=0.8
    )
    
    # Get Docling files
    docs_dir = Path("Docs")
    docling_dir = docs_dir / "Docling"
    
    if not docling_dir.exists():
        logger.error(f"Directory not found: {docling_dir}")
        return
    
    files = list(docling_dir.rglob("*.md"))
    logger.info(f"Found {len(files)} files in Docling collection")
    
    # Test with first 3 files
    test_files = files[:3]
    output_dir = Path("Chunked")
    
    for file_path in test_files:
        try:
            logger.info(f"\nProcessing: {file_path.name}")
            
            # Chunk the file
            chunks = chunker.process_file_smart(
                file_path=str(file_path),
                output_dir=None,
                auto_detect=True
            )
            
            if not chunks:
                logger.warning(f"  No chunks generated")
                continue
            
            # Add collection metadata
            for chunk in chunks:
                chunk["metadata"]["collection_name"] = "Docling"
                chunk["metadata"]["collection_hints"] = ["docling"]
            
            # Determine output path preserving subdirectory structure
            try:
                relative_file_path = file_path.relative_to(docling_dir)
            except ValueError:
                relative_file_path = Path(file_path.name)
            
            # Create output directory structure
            output_file_dir = output_dir / "Docling" / relative_file_path.parent
            output_file_dir.mkdir(parents=True, exist_ok=True)
            
            # Save individual file chunks
            import json
            output_file = output_file_dir / f"{file_path.stem}_chunks.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            
            logger.info(f"  ✓ Saved {len(chunks)} chunks to {output_file}")
            
        except Exception as e:
            logger.error(f"  ✗ Failed: {e}")
    
    logger.info("\nTest complete!")

if __name__ == "__main__":
    main()