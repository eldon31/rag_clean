#!/usr/bin/env python3
"""
Simple Docs Chunking - One Collection at a Time
===============================================

Process docs collections individually using CodeRankEmbed-optimized chunking.

Usage:
    python simple_chunk_docs.py fast_docs
    python simple_chunk_docs.py pydantic_docs
"""

import asyncio
import logging
import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig
from src.ingestion.processor import DocumentProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple-chunker")

class SimpleDocsChunker:
    """Simple docs chunker for one collection at a time."""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.docs_path = Path(__file__).parent / "Docs"
        self.output_path = Path(__file__).parent / "output" / f"{collection_name}_chunked"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Simple chunking config optimized for CodeRankEmbed
        self.config = ChunkingConfig(
            chunk_size=1024,      # Good size for CodeRankEmbed
            chunk_overlap=150,    # 15% overlap
            max_tokens=2048,      # CodeRankEmbed limit
            use_semantic_splitting=True,
            preserve_structure=True
        )
        
        self.chunker = DoclingHybridChunker(self.config)
        
    async def process_collection(self):
        """Process the specified collection."""
        
        # Determine source path
        if self.collection_name == "fast_docs":
            source_path = self.docs_path / "FAST_DOCS"
        elif self.collection_name == "pydantic_docs":
            source_path = self.docs_path / "pydantic_pydantic"
        else:
            logger.error(f"❌ Unknown collection: {self.collection_name}")
            logger.info("Available collections: fast_docs, pydantic_docs")
            return
            
        if not source_path.exists():
            logger.error(f"❌ Source path not found: {source_path}")
            return
            
        logger.info(f"🚀 Processing {self.collection_name}")
        logger.info(f"📂 Source: {source_path}")
        logger.info(f"📁 Output: {self.output_path}")
        logger.info("=" * 60)
        
        total_files = 0
        total_chunks = 0
        subdirs_processed = []
        
        # Process subdirectories
        for subdir in source_path.iterdir():
            if subdir.is_dir():
                logger.info(f"📁 Processing subdirectory: {subdir.name}")
                stats = await self.process_subdirectory(subdir)
                subdirs_processed.append(subdir.name)
                total_files += stats["files"]
                total_chunks += stats["chunks"]
                logger.info(f"   ✅ {stats['files']} files, {stats['chunks']} chunks")
            elif subdir.suffix == '.md':
                # Handle direct .md files (like in pydantic_pydantic)
                logger.info(f"📄 Processing file: {subdir.name}")
                stats = await self.process_single_file(subdir, "root")
                total_files += stats["files"]
                total_chunks += stats["chunks"]
                logger.info(f"   ✅ {stats['chunks']} chunks")
        
        # Create summary
        summary = {
            "collection_name": self.collection_name,
            "subdirectories": subdirs_processed,
            "total_files": total_files,
            "total_chunks": total_chunks,
            "chunking_config": {
                "chunk_size": self.config.chunk_size,
                "chunk_overlap": self.config.chunk_overlap,
                "max_tokens": self.config.max_tokens,
                "model_optimized_for": "nomic-ai/CodeRankEmbed"
            },
            "processed_at": datetime.now().isoformat()
        }
        
        summary_file = self.output_path / f"{self.collection_name}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        logger.info("\n🎯 Collection Processing Complete:")
        logger.info(f"Files: {total_files}")
        logger.info(f"Chunks: {total_chunks}")
        logger.info(f"Summary: {summary_file}")
        logger.info("✅ Ready for Kaggle GPU embedding!")
        
    async def process_subdirectory(self, subdir_path: Path) -> Dict[str, int]:
        """Process all .md files in a subdirectory."""
        
        files_processed = 0
        total_chunks = 0
        
        for md_file in subdir_path.glob("*.md"):
            stats = await self.process_single_file(md_file, subdir_path.name)
            files_processed += stats["files"]
            total_chunks += stats["chunks"]
            
        return {"files": files_processed, "chunks": total_chunks}
        
    async def process_single_file(self, md_file: Path, subdirectory: str) -> Dict[str, int]:
        """Process a single markdown file."""
        
        try:
            # Read content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content.strip():
                return {"files": 0, "chunks": 0}
                
            # Generate source ID
            source_id = f"{self.collection_name}/{subdirectory}/{md_file.name}"
            
            # Chunk the document
            chunks = await self.chunker.chunk_document(
                content=content,
                title=md_file.stem,
                source=source_id
            )
            
            # Add collection metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "collection": self.collection_name,
                    "subdirectory": subdirectory,
                    "source_file": md_file.name,
                    "source_path": source_id,
                    "chunk_id": f"{self.collection_name}_{subdirectory}_{md_file.stem}_{i:03d}",
                    "model_for_embedding": "nomic-ai/CodeRankEmbed",
                    "vector_dimensions": 768
                })
            
            # Save chunks
            chunks_file = self.output_path / f"_{self.collection_name}_{subdirectory}_{md_file.stem}_chunks.json"
            chunks_data = {
                "source": source_id,
                "total_chunks": len(chunks),
                "chunks": [
                    {
                        "id": chunk.metadata.get("chunk_id"),
                        "content": chunk.content,
                        "metadata": chunk.metadata,
                        "index": chunk.index,
                        "start_char": chunk.start_char,
                        "end_char": chunk.end_char,
                        "token_count": chunk.token_count
                    }
                    for chunk in chunks
                ]
            }
            
            with open(chunks_file, 'w', encoding='utf-8') as f:
                json.dump(chunks_data, f, indent=2, ensure_ascii=False)
                
            return {"files": 1, "chunks": len(chunks)}
            
        except Exception as e:
            logger.error(f"❌ Error processing {md_file.name}: {e}")
            return {"files": 0, "chunks": 0}

async def main():
    """Main function."""
    
    if len(sys.argv) != 2:
        logger.info("Usage: python simple_chunk_docs.py <collection_name>")
        logger.info("Available collections:")
        logger.info("  fast_docs     - Process Docs/FAST_DOCS/")
        logger.info("  pydantic_docs - Process Docs/pydantic_pydantic/")
        return
        
    collection_name = sys.argv[1]
    chunker = SimpleDocsChunker(collection_name)
    await chunker.process_collection()

if __name__ == "__main__":
    asyncio.run(main())