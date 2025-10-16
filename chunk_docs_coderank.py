#!/usr/bin/env python3
"""
Docs Chunking with CodeRankEmbed Tokenizer
==========================================

Process docs collections using the existing DoclingHybridChunker with CodeRankEmbed tokenizer.

Usage:
    python chunk_docs_coderank.py fast_docs
    python chunk_docs_coderank.py pydantic_docs
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docs-chunker")

class DocsChunkerCodeRank:
    """Chunk docs using DoclingHybridChunker with CodeRankEmbed tokenizer."""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.docs_path = Path(__file__).parent / "Docs"
        self.output_path = Path(__file__).parent / "output" / f"{collection_name}_chunked"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Configure chunking for CodeRankEmbed (768D, 2048 tokens)
        self.config = ChunkingConfig(
            chunk_size=1024,          # Optimal for CodeRankEmbed
            chunk_overlap=150,        # 15% overlap
            max_tokens=2048,          # CodeRankEmbed limit
            use_semantic_splitting=True,
            preserve_structure=True
        )
        
        # This will automatically use nomic-ai/CodeRankEmbed tokenizer
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
            
        logger.info(f"🚀 Processing {self.collection_name} with CodeRankEmbed tokenizer")
        logger.info(f"📂 Source: {source_path}")
        logger.info(f"📁 Output: {self.output_path}")
        logger.info("=" * 60)
        
        total_files = 0
        total_chunks = 0
        subdirs_processed = []
        
        # Process subdirectories and files
        if source_path.name == "FAST_DOCS":
            # FAST_DOCS has subdirectories
            for subdir in source_path.iterdir():
                if subdir.is_dir():
                    logger.info(f"📁 Processing subdirectory: {subdir.name}")
                    stats = await self.process_subdirectory(subdir)
                    subdirs_processed.append(subdir.name)
                    total_files += stats["files"]
                    total_chunks += stats["chunks"]
                    logger.info(f"   ✅ {stats['files']} files, {stats['chunks']} chunks")
        else:
            # pydantic_pydantic has files directly
            logger.info(f"📄 Processing files in: {source_path.name}")
            for md_file in source_path.glob("*.md"):
                stats = await self.process_single_file(md_file, "root")
                total_files += stats["files"]
                total_chunks += stats["chunks"]
                logger.info(f"   📄 {md_file.name}: {stats['chunks']} chunks")
        
        # Create summary
        summary = {
            "collection_name": self.collection_name,
            "subdirectories": subdirs_processed if subdirs_processed else ["root"],
            "total_files": total_files,
            "total_chunks": total_chunks,
            "chunking_config": {
                "chunk_size": self.config.chunk_size,
                "chunk_overlap": self.config.chunk_overlap,
                "max_tokens": self.config.max_tokens,
                "tokenizer_model": "nomic-ai/CodeRankEmbed",
                "embedding_model": "nomic-ai/CodeRankEmbed",
                "vector_dimensions": 768
            },
            "processed_at": datetime.now().isoformat()
        }
        
        summary_file = self.output_path / f"{self.collection_name}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        logger.info("\n🎯 Collection Processing Complete:")
        logger.info(f"Files: {total_files}")
        logger.info(f"Chunks: {total_chunks}")
        logger.info(f"Average chunks per file: {total_chunks/max(total_files,1):.1f}")
        logger.info(f"Summary: {summary_file}")
        logger.info("✅ Ready for Kaggle GPU embedding with CodeRankEmbed!")
        
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
                logger.warning(f"    ⚠️  Empty file: {md_file.name}")
                return {"files": 0, "chunks": 0}
                
            # Generate source ID for Qdrant collection organization
            source_id = f"{self.collection_name}/{subdirectory}/{md_file.name}"
            
            # Chunk using DoclingHybridChunker with CodeRankEmbed tokenizer
            chunks = await self.chunker.chunk_document(
                content=content,
                title=md_file.stem,
                source=source_id
            )
            
            # Add Qdrant-optimized metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    # Qdrant collection organization
                    "collection": self.collection_name,
                    "subdirectory": subdirectory,
                    "source_file": md_file.name,
                    "source_path": source_id,
                    "chunk_id": f"{self.collection_name}_{subdirectory}_{md_file.stem}_{i:03d}",
                    
                    # Embedding model info
                    "embedding_model": "nomic-ai/CodeRankEmbed",
                    "vector_dimensions": 768,
                    "tokenizer_model": "nomic-ai/CodeRankEmbed",
                    "max_tokens": 2048,
                    
                    # Processing metadata
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "processed_at": datetime.now().isoformat()
                })
            
            # Save chunks for this file
            chunks_file = self.output_path / f"_{self.collection_name}_{subdirectory}_{md_file.stem}_chunks.json"
            chunks_data = {
                "source": source_id,
                "total_chunks": len(chunks),
                "embedding_config": {
                    "model": "nomic-ai/CodeRankEmbed",
                    "dimensions": 768,
                    "max_tokens": 2048
                },
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
            logger.error(f"    ❌ Error processing {md_file.name}: {e}")
            return {"files": 0, "chunks": 0}

async def main():
    """Main function."""
    
    if len(sys.argv) != 2:
        logger.info("Usage: python chunk_docs_coderank.py <collection_name>")
        logger.info("Available collections:")
        logger.info("  fast_docs     - Process Docs/FAST_DOCS/")
        logger.info("  pydantic_docs - Process Docs/pydantic_pydantic/")
        logger.info("\nThis uses DoclingHybridChunker with CodeRankEmbed tokenizer")
        logger.info("Optimized for nomic-ai/CodeRankEmbed (768D) embedding in Kaggle")
        return
        
    collection_name = sys.argv[1]
    chunker = DocsChunkerCodeRank(collection_name)
    await chunker.process_collection()

if __name__ == "__main__":
    asyncio.run(main())