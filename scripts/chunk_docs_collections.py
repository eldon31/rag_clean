#!/usr/bin/env python3
"""
Chunk Docs Directory with Collection-Based Structure
Flattens 2nd+ level subdirectories into 1st level subdirectories
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processor.enhanced_ultimate_chunker_v5_unified import EnhancedUltimateChunkerV5Unified

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def discover_collections(docs_dir: Path) -> Dict[str, List[Path]]:
    """
    Discover collections and flatten directory structure
    
    Structure:
    - Top-level folders = collection names
    - 1st level subdirs = preserved
    - 2nd+ level subdirs = flattened into 1st level
    
    Returns:
        Dict mapping collection_name -> list of files
    """
    collections = {}
    
    for collection_dir in docs_dir.iterdir():
        if not collection_dir.is_dir():
            # Skip root-level files
            continue
        
        collection_name = collection_dir.name
        files = []
        
        # Check if collection has subdirectories
        subdirs = [d for d in collection_dir.iterdir() if d.is_dir()]
        
        if subdirs:
            # Has subdirectories - process each 1st level subdir
            for first_level_subdir in subdirs:
                # Collect all files recursively from this 1st level subdir
                # (flattening any 2nd+ level subdirs)
                for file in first_level_subdir.rglob("*.md"):
                    files.append(file)
        else:
            # No subdirectories - just files at root of collection
            files.extend(collection_dir.glob("*.md"))
        
        if files:
            collections[collection_name] = sorted(files)
            logger.info(f"Collection '{collection_name}': {len(files)} files")
    
    return collections


def chunk_collection(
    chunker: EnhancedUltimateChunkerV5Unified,
    collection_name: str,
    files: List[Path],
    output_dir: Path,
    docs_root: Path
) -> Dict:
    """
    Chunk all files in a collection, preserving subdirectory structure
    
    Each file gets its own JSON output maintaining the directory hierarchy:
    Chunked/CollectionName/subdir/filename.json
    
    Returns:
        Summary statistics for the collection
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"Processing Collection: {collection_name}")
    logger.info(f"{'='*70}")
    
    file_stats = []
    total_chunks = 0
    
    for file_path in files:
        try:
            logger.info(f"  Chunking: {file_path.name}")
            
            # Chunk the file
            chunks = chunker.process_file_smart(
                file_path=str(file_path),
                output_dir=None,  # We'll save manually
                auto_detect=True
            )
            
            if not chunks:
                logger.warning(f"    No chunks generated for {file_path.name}")
                continue
            
            # Add collection metadata to each chunk
            for chunk in chunks:
                chunk["metadata"]["collection_name"] = collection_name
                chunk["metadata"]["collection_hints"] = [collection_name.lower()]
            
            # Determine output path preserving subdirectory structure
            # Get relative path from Docs/CollectionName/
            collection_root = docs_root / collection_name
            try:
                relative_file_path = file_path.relative_to(collection_root)
            except ValueError:
                # Fallback if path resolution fails
                relative_file_path = Path(file_path.name)
            
            # Create output directory structure
            output_file_dir = output_dir / collection_name / relative_file_path.parent
            output_file_dir.mkdir(parents=True, exist_ok=True)
            
            # Save individual file chunks
            output_file = output_file_dir / f"{file_path.stem}_chunks.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            
            total_chunks += len(chunks)
            
            file_stats.append({
                "file": str(relative_file_path),
                "output": str(output_file.relative_to(output_dir)),
                "chunks": len(chunks),
                "total_tokens": sum(c["metadata"]["token_count"] for c in chunks)
            })
            
            logger.info(f"    ✓ Saved {len(chunks)} chunks to {output_file.relative_to(output_dir)}")
            
        except Exception as e:
            logger.error(f"    ✗ Failed to chunk {file_path.name}: {e}")
    
    # Collection summary
    summary = {
        "collection_name": collection_name,
        "total_files": len(files),
        "processed_files": len(file_stats),
        "total_chunks": total_chunks,
        "total_tokens": sum(f["total_tokens"] for f in file_stats),
        "file_details": file_stats
    }
    
    return summary


def main():
    """Main execution"""
    logger.info("="*70)
    logger.info("Enhanced Ultimate Chunker V5 - Docs Collection Processing")
    logger.info("="*70)
    
    # Configuration
    docs_dir = Path("Docs")
    output_dir = Path("Chunked")
    
    if not docs_dir.exists():
        logger.error(f"Docs directory not found: {docs_dir}")
        return
    
    # Initialize chunker
    logger.info("\nInitializing chunker...")
    chunker = EnhancedUltimateChunkerV5Unified(
        target_model="jina-code-embeddings-1.5b",
        use_tree_sitter=True,
        use_semchunk=True,
        enable_semantic_scoring=False
    )
    
    # Discover collections
    logger.info(f"\nDiscovering collections in {docs_dir}...")
    collections = discover_collections(docs_dir)
    
    if not collections:
        logger.error("No collections found!")
        return
    
    logger.info(f"\nFound {len(collections)} collections:")
    for name, files in collections.items():
        logger.info(f"  - {name}: {len(files)} files")
    
    # Process each collection
    start_time = datetime.now()
    collection_summaries = []
    
    for collection_name, files in collections.items():
        summary = chunk_collection(chunker, collection_name, files, output_dir, docs_dir)
        collection_summaries.append(summary)
    
    processing_time = (datetime.now() - start_time).total_seconds()
    
    # Overall summary
    logger.info(f"\n{'='*70}")
    logger.info("Processing Complete!")
    logger.info(f"{'='*70}")
    
    total_files = sum(s["processed_files"] for s in collection_summaries)
    total_chunks = sum(s["total_chunks"] for s in collection_summaries)
    total_tokens = sum(s["total_tokens"] for s in collection_summaries)
    
    logger.info(f"\nOverall Statistics:")
    logger.info(f"  Collections processed: {len(collection_summaries)}")
    logger.info(f"  Total files processed: {total_files}")
    logger.info(f"  Total chunks generated: {total_chunks:,}")
    logger.info(f"  Total tokens: {total_tokens:,}")
    logger.info(f"  Processing time: {processing_time:.2f}s")
    
    logger.info(f"\nPer-Collection Summary:")
    for summary in collection_summaries:
        logger.info(f"  {summary['collection_name']}:")
        logger.info(f"    Files: {summary['processed_files']}")
        logger.info(f"    Chunks: {summary['total_chunks']:,}")
        logger.info(f"    Tokens: {summary['total_tokens']:,}")
    
    # Save overall summary
    summary_file = output_dir / "processing_summary.json"
    overall_summary = {
        "timestamp": datetime.now().isoformat(),
        "docs_directory": str(docs_dir),
        "output_directory": str(output_dir),
        "processing_time_seconds": processing_time,
        "total_collections": len(collection_summaries),
        "total_files": total_files,
        "total_chunks": total_chunks,
        "total_tokens": total_tokens,
        "collections": collection_summaries
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(overall_summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✓ Summary saved to {summary_file}")
    logger.info(f"{'='*70}")


if __name__ == "__main__":
    main()