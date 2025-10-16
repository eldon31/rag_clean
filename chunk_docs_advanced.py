#!/usr/bin/env python3
"""
Advanced Docs Chunking Script
=============================

Chunks the Docs folder using the latest advanced embedding and chunking implementation.

Structure:
- Docs/FAST_DOCS/ → Collection: "fast_docs"
  - fastapi_fastapi/ → Subdirectory metadata
  - jlowin_fastmcp/ → Subdirectory metadata
  - modelcontextprotocol_python-sdk/ → Subdirectory metadata
- Docs/pydantic_pydantic/ → Collection: "pydantic_docs"

Features:
- Intelligent content analysis for optimal chunking
- Adaptive chunking strategies based on content type
- Metadata tracking for collection/subdirectory organization
- Optimized for Qdrant vector database storage
"""

import asyncio
import logging
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from advanced_embedding_chunking_upgrade import (
    EmbeddingUpgradeSystem,
    EmbeddingUpgradeConfig,
    EmbeddingModel,
    ChunkingStrategy,
    ContentAnalyzer,
    AdvancedChunker
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docs-chunker")

class DocsChunkingProcessor:
    """Process Docs folder with advanced chunking."""
    
    def __init__(self, docs_path: Path, output_path: Path):
        self.docs_path = docs_path
        self.output_path = output_path
        self.output_path.mkdir(exist_ok=True)
        
        # Configure advanced chunking system
        self.config = EmbeddingUpgradeConfig(
            primary_model=EmbeddingModel.CODE_RANK_EMBED,
            fallback_models=[EmbeddingModel.BGE_M3, EmbeddingModel.MINI_LM_L12],
            auto_model_selection=True,
            chunking_strategy=ChunkingStrategy.ADAPTIVE,
            base_chunk_size=1024,
            max_chunk_size=4096,
            min_chunk_size=200,
            chunk_overlap_ratio=0.15,
            batch_size=16,
            enable_quality_scoring=True,
            quality_threshold=0.7,
            enable_hierarchical_relationships=True,
            preserve_code_structure=True
        )
        
        self.chunker = AdvancedChunker(self.config)
        self.analyzer = ContentAnalyzer()
        
    async def process_all_docs(self):
        """Process all documentation folders."""
        
        logger.info("🚀 Starting Advanced Docs Chunking")
        logger.info("=" * 60)
        
        collections_processed = 0
        total_files = 0
        total_chunks = 0
        
        # Process FAST_DOCS
        fast_docs_path = self.docs_path / "FAST_DOCS"
        if fast_docs_path.exists():
            logger.info("📂 Processing FAST_DOCS collection...")
            stats = await self.process_collection(
                collection_path=fast_docs_path,
                collection_name="fast_docs"
            )
            collections_processed += 1
            total_files += stats["files"]
            total_chunks += stats["chunks"]
            
        # Process pydantic_pydantic
        pydantic_docs_path = self.docs_path / "pydantic_pydantic"
        if pydantic_docs_path.exists():
            logger.info("📂 Processing pydantic_pydantic collection...")
            stats = await self.process_collection(
                collection_path=pydantic_docs_path,
                collection_name="pydantic_docs"
            )
            collections_processed += 1
            total_files += stats["files"]
            total_chunks += stats["chunks"]
            
        logger.info("\n🎯 Processing Summary:")
        logger.info("=" * 40)
        logger.info(f"Collections: {collections_processed}")
        logger.info(f"Files: {total_files}")
        logger.info(f"Total Chunks: {total_chunks}")
        logger.info(f"Output: {self.output_path}")
        
    async def process_collection(self, collection_path: Path, collection_name: str) -> Dict[str, int]:
        """Process a single collection (e.g., FAST_DOCS)."""
        
        collection_output = self.output_path / f"{collection_name}_chunked"
        collection_output.mkdir(exist_ok=True)
        
        files_processed = 0
        total_chunks = 0
        subdirectories = []
        
        # Get all subdirectories
        for item in collection_path.iterdir():
            if item.is_dir():
                subdirectories.append(item)
        
        logger.info(f"Found {len(subdirectories)} subdirectories in {collection_name}")
        
        # Process each subdirectory
        for subdir in subdirectories:
            logger.info(f"  📁 Processing subdirectory: {subdir.name}")
            
            subdir_stats = await self.process_subdirectory(
                subdir_path=subdir,
                collection_name=collection_name,
                subdirectory_name=subdir.name,
                output_path=collection_output
            )
            
            files_processed += subdir_stats["files"]
            total_chunks += subdir_stats["chunks"]
            
        # Create collection summary
        collection_summary = {
            "collection_name": collection_name,
            "subdirectories": [d.name for d in subdirectories],
            "total_files": files_processed,
            "total_chunks": total_chunks,
            "processed_at": datetime.now().isoformat(),
            "chunking_config": {
                "strategy": self.config.chunking_strategy.value,
                "base_chunk_size": self.config.base_chunk_size,
                "overlap_ratio": self.config.chunk_overlap_ratio,
                "primary_model": self.config.primary_model.value
            }
        }
        
        summary_file = collection_output / f"{collection_name}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(collection_summary, f, indent=2, ensure_ascii=False)
            
        logger.info(f"✅ {collection_name}: {files_processed} files, {total_chunks} chunks")
        
        return {"files": files_processed, "chunks": total_chunks}
        
    async def process_subdirectory(self, subdir_path: Path, collection_name: str, 
                                 subdirectory_name: str, output_path: Path) -> Dict[str, int]:
        """Process all markdown files in a subdirectory."""
        
        files_processed = 0
        total_chunks = 0
        
        # Get all markdown files
        md_files = list(subdir_path.glob("*.md"))
        
        for md_file in md_files:
            try:
                # Read file content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    logger.warning(f"    ⚠️  Empty file: {md_file.name}")
                    continue
                    
                # Analyze content
                analysis = self.analyzer.analyze_content(content, str(md_file))
                
                # Determine source identifier for metadata
                source_id = f"{collection_name}/{subdirectory_name}/{md_file.name}"
                
                # Chunk with advanced strategy
                chunks = await self.chunker.chunk_with_strategy(
                    content=content,
                    title=md_file.stem,
                    source=source_id,
                    strategy=ChunkingStrategy.ADAPTIVE
                )
                
                # Enhance metadata for Qdrant collection organization
                for i, chunk in enumerate(chunks):
                    # Generate unique chunk ID
                    chunk_id = f"{collection_name}_{subdirectory_name}_{md_file.stem}_{i:03d}"
                    
                    chunk.metadata.update({
                        # Chunk identification
                        "chunk_id": chunk_id,
                        
                        # Collection organization
                        "collection": collection_name,
                        "subdirectory": subdirectory_name,
                        "source_file": md_file.name,
                        "source_path": source_id,
                        
                        # Content analysis
                        "content_type": analysis["content_type"].value,
                        "code_density": analysis["code_density"],
                        "api_density": analysis["api_density"],
                        "structure_complexity": analysis["structure_complexity"],
                        "recommended_model": analysis["recommended_model"].value,
                        "recommended_chunk_size": analysis["recommended_chunk_size"],
                        
                        # Chunking metadata
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "chunk_strategy": ChunkingStrategy.ADAPTIVE.value,
                        "processed_at": datetime.now().isoformat()
                    })
                
                # Save chunks for this file
                chunks_file = output_path / f"_{collection_name}_{subdirectory_name}_{md_file.stem}_chunks.json"
                chunks_data = {
                    "source": source_id,
                    "analysis": {
                        "content_type": analysis["content_type"].value,
                        "code_density": analysis["code_density"],
                        "api_density": analysis["api_density"],
                        "structure_complexity": analysis["structure_complexity"],
                        "recommended_model": analysis["recommended_model"].value,
                        "recommended_chunk_size": analysis["recommended_chunk_size"]
                    },
                    "chunks": [
                        {
                            "id": chunk.metadata.get("chunk_id", f"chunk_{i:03d}"),
                            "content": chunk.content,
                            "metadata": chunk.metadata,
                            "index": chunk.index,
                            "start_char": chunk.start_char,
                            "end_char": chunk.end_char,
                            "token_count": chunk.token_count
                        }
                        for i, chunk in enumerate(chunks)
                    ]
                }
                
                with open(chunks_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks_data, f, indent=2, ensure_ascii=False)
                
                files_processed += 1
                total_chunks += len(chunks)
                
                logger.info(f"    📄 {md_file.name}: {len(chunks)} chunks "
                          f"({analysis['content_type'].value}, "
                          f"model: {analysis['recommended_model'].value})")
                
            except Exception as e:
                logger.error(f"    ❌ Error processing {md_file.name}: {e}")
                continue
                
        return {"files": files_processed, "chunks": total_chunks}

async def main():
    """Main execution function."""
    
    # Setup paths
    docs_path = Path(__file__).parent / "Docs"
    output_path = Path(__file__).parent / "output" / "docs_chunked_advanced"
    
    if not docs_path.exists():
        logger.error(f"❌ Docs folder not found: {docs_path}")
        return
        
    logger.info(f"📂 Source: {docs_path}")
    logger.info(f"📁 Output: {output_path}")
    
    # Initialize processor
    processor = DocsChunkingProcessor(docs_path, output_path)
    
    # Process all documentation
    await processor.process_all_docs()
    
    logger.info("\n🎉 Advanced docs chunking completed!")
    logger.info("Ready for Kaggle GPU embedding processing.")

if __name__ == "__main__":
    asyncio.run(main())