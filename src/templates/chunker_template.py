"""
TEMPLATE 1: Universal Document Chunker (CPU-Optimized)

PURPOSE:
    Process ANY collection of documents into optimized chunks.
    Run locally on CPU before sending to Kaggle for embedding.

WORKFLOW POSITION: Step 1 of 3
    [This Script] → Kaggle Embedder → Qdrant Uploader

USAGE:
    # Chunk a new collection
    python -m src.templates.chunker_template \\
        --collection my_docs \\
        --input Docs/my_docs/ \\
        --output output/my_docs_chunked/ \\
        --chunk-size 1024
    
    # Re-chunk existing collection with new settings
    python -m src.templates.chunker_template \\
        --collection qdrant_ecosystem \\
        --input Docs/qdrant_ecosystem/ \\
        --output output/qdrant_ecosystem_rechunked/ \\
        --chunk-size 1024 \\
        --overlap 100

OPTIMIZATION FOR CODERANK (768-dim):
    - Smaller chunks (1024 chars) for better granularity with 768-dim
    - Token-aware splitting (uses CodeRankEmbed tokenizer)
    - Structure preservation (respects code blocks, headings)
    - Minimal overlap (100 chars) for efficiency

OUTPUT FORMAT:
    output/<collection>_chunked/
        ├── file1_chunks.json
        ├── file2_chunks.json
        └── ...
    
    Each JSON contains:
    [
        {
            "chunk_id": "collection:file:chunk:0",
            "content": "chunk text...",
            "metadata": {
                "source_file": "path/to/file.md",
                "chunk_index": 0,
                "token_count": 245,
                ...
            }
        },
        ...
    ]

NEXT STEP:
    Upload output/ directory to Kaggle for embedding with Template 2.
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

from pydantic import BaseModel, Field
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig, DocumentChunk
from src.ingestion.processor import DocumentProcessor
from src.config.docling_config import DoclingConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

class ChunkerConfig(BaseModel):
    """Configuration for universal chunker template."""
    
    # Input/Output
    collection_name: str = Field(..., description="Collection name (e.g., 'qdrant_ecosystem')")
    input_path: Path = Field(..., description="Input directory with markdown files")
    output_path: Path = Field(..., description="Output directory for chunked JSON")
    
    # Chunking parameters (optimized for CodeRankEmbed)
    chunk_size: int = Field(default=1024, description="Target chunk size (optimized for 768-dim)")
    chunk_overlap: int = Field(default=100, description="Overlap between chunks")
    max_tokens: int = Field(default=2048, description="Max tokens (CodeRankEmbed limit)")
    
    # Processing options
    file_pattern: str = Field(default="**/*.md", description="Glob pattern for files")
    skip_pattern: Optional[str] = Field(default="_index.md", description="Files to skip")
    preserve_structure: bool = Field(default=True, description="Preserve document structure")
    
    # Metadata enrichment
    extract_subdirs: bool = Field(default=True, description="Extract subdirectory metadata")
    add_stats: bool = Field(default=True, description="Add token/char count stats")


# ============================================================================
# UNIVERSAL CHUNKER ENGINE
# ============================================================================

class UniversalChunker:
    """
    Universal document chunker optimized for any collection.
    
    Features:
    - CPU-optimized (no GPU required)
    - Structure-preserving (respects code blocks, headings, sections)
    - Token-aware (uses CodeRankEmbed tokenizer for accuracy)
    - Metadata-rich (tracks source, position, stats)
    - Resumable (skips already processed files)
    """
    
    def __init__(self, config: ChunkerConfig):
        """
        Initialize universal chunker.
        
        Args:
            config: Chunker configuration
        """
        self.config = config
        
        logger.info(f"🔧 Initializing UniversalChunker")
        logger.info(f"  Collection: {config.collection_name}")
        logger.info(f"  Chunk size: {config.chunk_size} chars")
        logger.info(f"  Max tokens: {config.max_tokens}")
        logger.info(f"  Overlap: {config.chunk_overlap} chars")
        
        # Initialize chunking config (optimized for CodeRankEmbed)
        self.chunking_config = ChunkingConfig(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            max_tokens=config.max_tokens,
            preserve_structure=config.preserve_structure,
            use_semantic_splitting=True
        )
        
        # Initialize chunker
        self.chunker = DoclingHybridChunker(self.chunking_config)
        
        # Initialize document processor
        self.processor = DocumentProcessor()
        
        logger.info(f"✓ Chunker initialized")
        
        # Statistics
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "skipped_files": 0,
            "failed_files": 0,
            "total_chunks": 0,
            "start_time": None,
            "end_time": None
        }
    
    def discover_files(self) -> List[Path]:
        """
        Discover all files matching pattern.
        
        Returns:
            List of file paths to process
        """
        logger.info(f"📂 Discovering files in: {self.config.input_path}")
        logger.info(f"  Pattern: {self.config.file_pattern}")
        
        all_files = list(self.config.input_path.glob(self.config.file_pattern))
        
        # Filter out skip pattern
        if self.config.skip_pattern:
            files = [f for f in all_files if self.config.skip_pattern not in f.name]
            skipped = len(all_files) - len(files)
            logger.info(f"  Skipped {skipped} files matching '{self.config.skip_pattern}'")
        else:
            files = all_files
        
        self.stats["total_files"] = len(files)
        
        logger.info(f"✓ Found {len(files)} files to process")
        
        return files
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from file path.
        
        Args:
            file_path: Path to file
        
        Returns:
            Metadata dictionary
        """
        # Get relative path from input root
        relative_path = file_path.relative_to(self.config.input_path)
        
        # Extract subdirectory (first folder)
        parts = relative_path.parts
        if len(parts) > 1:
            subdir = parts[0]
        else:
            subdir = "root"
        
        metadata = {
            "source_file": str(relative_path),
            "source_collection": self.config.collection_name,
            "subdirectory": subdir,
            "filename": file_path.name,
            "file_extension": file_path.suffix
        }
        
        return metadata
    
    def chunk_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Chunk a single file.
        
        Args:
            file_path: Path to markdown file
        
        Returns:
            List of chunk dictionaries
        """
        try:
            # Process document with Docling
            doc_result = self.processor.process_file(str(file_path))
            
            # Extract base metadata
            base_metadata = self.extract_metadata(file_path)
            
            # Chunk document (async call, but we'll run synchronously)
            import asyncio
            chunks = asyncio.run(self.chunker.chunk_document(
                content=doc_result.content,
                title=file_path.stem,
                source=str(file_path),
                metadata=base_metadata,
                docling_doc=doc_result.docling_document
            ))
            
            # Convert to JSON-serializable format
            chunk_dicts = []
            for i, chunk in enumerate(chunks):
                # Generate chunk ID
                chunk_id = f"{self.config.collection_name}:{base_metadata['source_file']}:chunk:{i}"
                
                # Merge metadata
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    "chunk_index": i,
                    "token_count": chunk.token_count,
                    "char_count": len(chunk.content),
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char
                })
                
                chunk_dict = {
                    "chunk_id": chunk_id,
                    "content": chunk.content,
                    "metadata": chunk_metadata
                }
                
                chunk_dicts.append(chunk_dict)
            
            return chunk_dicts
        
        except Exception as e:
            logger.error(f"✗ Failed to chunk {file_path.name}: {e}")
            self.stats["failed_files"] += 1
            return []
    
    def save_chunks(self, chunks: List[Dict[str, Any]], source_file: Path):
        """
        Save chunks to JSON file, preserving ONE level of subfolder structure.
        
        If there are nested subfolders (subfolders inside subfolders), they are
        flattened into the first-level subfolder.
        
        Examples:
            Input: Docs/collection/file.md
            Output: output/collection_chunked/file_chunks.json
            
            Input: Docs/collection/subfolder/file.md
            Output: output/collection_chunked/subfolder/file_chunks.json
            
            Input: Docs/collection/subfolder/nested/deep/file.md
            Output: output/collection_chunked/subfolder/file_chunks.json (flattened)
        
        Args:
            chunks: List of chunk dictionaries
            source_file: Original source file path
        """
        # Get relative path from input root
        relative_path = source_file.relative_to(self.config.input_path)
        
        # Create output filename
        output_filename = f"{relative_path.stem}_chunks.json"
        
        # Determine output location based on depth
        if len(relative_path.parts) == 1:
            # File is in root - save directly to output path
            self.config.output_path.mkdir(parents=True, exist_ok=True)
            output_file = self.config.output_path / output_filename
            save_location = output_filename
        else:
            # File is in a subfolder - preserve ONLY first-level subfolder
            # Flatten any deeper nesting into the first subfolder
            first_level_subdir = relative_path.parts[0]
            output_subdir = self.config.output_path / first_level_subdir
            output_subdir.mkdir(parents=True, exist_ok=True)
            output_file = output_subdir / output_filename
            save_location = f"{first_level_subdir}/{output_filename}"
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        
        logger.debug(f"  Saved {len(chunks)} chunks to {save_location}")
    
    def process_all(self):
        """Process all files in input directory."""
        self.stats["start_time"] = datetime.now()
        
        # Discover files
        files = self.discover_files()
        
        if not files:
            logger.warning("⚠️  No files found to process")
            return
        
        # Process files
        logger.info(f"\\n🔄 Processing {len(files)} files...")
        
        for file_path in tqdm(files, desc="Chunking files", unit="file"):
            # Check if already processed (resume capability)
            # Need to check with preserved first-level subfolder only
            relative_path = file_path.relative_to(self.config.input_path)
            
            if len(relative_path.parts) == 1:
                # File in root
                output_file = self.config.output_path / f"{file_path.stem}_chunks.json"
            else:
                # File in subfolder - use only first-level subfolder
                first_level_subdir = relative_path.parts[0]
                output_file = self.config.output_path / first_level_subdir / f"{file_path.stem}_chunks.json"
            
            if output_file.exists():
                logger.debug(f"  Skipping {file_path.name} (already processed)")
                self.stats["skipped_files"] += 1
                continue
            
            # Chunk file
            chunks = self.chunk_file(file_path)
            
            if chunks:
                # Save chunks
                self.save_chunks(chunks, file_path)
                
                # Update stats
                self.stats["processed_files"] += 1
                self.stats["total_chunks"] += len(chunks)
        
        self.stats["end_time"] = datetime.now()
    
    def print_summary(self):
        """Print processing summary."""
        elapsed = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        
        logger.info(f"\\n{'='*60}")
        logger.info(f"✓ CHUNKING COMPLETED")
        logger.info(f"{'='*60}")
        logger.info(f"Collection: {self.config.collection_name}")
        logger.info(f"Total files: {self.stats['total_files']}")
        logger.info(f"Processed: {self.stats['processed_files']}")
        logger.info(f"Skipped: {self.stats['skipped_files']}")
        logger.info(f"Failed: {self.stats['failed_files']}")
        logger.info(f"Total chunks: {self.stats['total_chunks']}")
        logger.info(f"Average chunks/file: {self.stats['total_chunks'] / max(self.stats['processed_files'], 1):.1f}")
        logger.info(f"Time elapsed: {elapsed/60:.1f} minutes")
        logger.info(f"Output directory: {self.config.output_path}")
        logger.info(f"{'='*60}\\n")
        
        logger.info(f"📦 NEXT STEPS:")
        logger.info(f"1. Upload {self.config.output_path}/ to Kaggle as a dataset")
        logger.info(f"2. Run Template 2 (embedder_template.py) on Kaggle GPU:")
        logger.info(f"   python embedder_template.py \\\\")
        logger.info(f"       --collection {self.config.collection_name} \\\\")
        logger.info(f"       --input /kaggle/input/{self.config.collection_name}_chunked/ \\\\")
        logger.info(f"       --output /kaggle/working/{self.config.collection_name}_embeddings.jsonl")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Universal Document Chunker (Template 1 of 3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument(
        '--collection',
        required=True,
        help="Collection name (e.g., 'qdrant_ecosystem')"
    )
    parser.add_argument(
        '--input',
        required=True,
        type=Path,
        help="Input directory with markdown files"
    )
    parser.add_argument(
        '--output',
        required=True,
        type=Path,
        help="Output directory for chunked JSON files"
    )
    
    # Optional arguments
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1024,
        help="Target chunk size in characters (default: 1024 for CodeRankEmbed)"
    )
    parser.add_argument(
        '--overlap',
        type=int,
        default=100,
        help="Overlap between chunks (default: 100)"
    )
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=2048,
        help="Maximum tokens per chunk (default: 2048 for CodeRankEmbed)"
    )
    parser.add_argument(
        '--file-pattern',
        default="**/*.md",
        help="Glob pattern for input files (default: **/*.md)"
    )
    parser.add_argument(
        '--skip-pattern',
        default="_index.md",
        help="Skip files matching this pattern (default: _index.md)"
    )
    
    args = parser.parse_args()
    
    # Create config
    config = ChunkerConfig(
        collection_name=args.collection,
        input_path=args.input,
        output_path=args.output,
        chunk_size=args.chunk_size,
        chunk_overlap=args.overlap,
        max_tokens=args.max_tokens,
        file_pattern=args.file_pattern,
        skip_pattern=args.skip_pattern
    )
    
    # Run chunker
    try:
        logger.info(f"{'='*60}")
        logger.info(f"TEMPLATE 1: UNIVERSAL DOCUMENT CHUNKER")
        logger.info(f"{'='*60}\\n")
        
        chunker = UniversalChunker(config)
        chunker.process_all()
        chunker.print_summary()
    
    except KeyboardInterrupt:
        logger.info("\\n⚠️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\\n❌ Processing failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
