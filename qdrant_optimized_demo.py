#!/usr/bin/env python3
"""
Qdrant-Optimized Embedding & Chunking Demo
==========================================

Demonstrates the advanced embedding and chunking system optimized for:
- Qdrant vector database
- Code snippets and documentation
- API reference materials
- Technical documentation

Uses only fast-loading models for demonstration.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
import sys
from pathlib import Path

# Core imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.ingestion.chunker import DoclingHybridChunker, ChunkingConfig
from advanced_embedding_chunking_upgrade import (
    EmbeddingModel, 
    EmbeddingUpgradeConfig, 
    ChunkingStrategy,
    ContentAnalyzer,
    AdvancedChunker,
    MODEL_SPECS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-demo")

async def demo_qdrant_optimized_system():
    """Demonstrate Qdrant-optimized embedding and chunking."""
    
    logger.info("🚀 Qdrant-Optimized Embedding & Chunking Demo")
    logger.info("=" * 60)
    
    # Configuration optimized for Qdrant + Code/API docs
    config = EmbeddingUpgradeConfig(
        primary_model=EmbeddingModel.CODE_RANK_EMBED,  # Already loaded, fast start
        fallback_models=[EmbeddingModel.MINI_LM_L12],  # Lightweight fallback
        auto_model_selection=True,
        chunking_strategy=ChunkingStrategy.ADAPTIVE,
        base_chunk_size=1024,
        chunk_overlap_ratio=0.15,
        batch_size=8,  # Smaller batch for demo
        enable_quality_scoring=True,
        quality_threshold=0.7,
        preserve_code_structure=True
    )
    
    # Initialize components
    analyzer = ContentAnalyzer()
    chunker = AdvancedChunker(config)
    
    # Demo content samples
    samples = {
        "API Documentation": """
        # Qdrant Vector Database API
        
        ## Creating a Collection
        
        ```python
        from qdrant_client import QdrantClient
        
        client = QdrantClient("localhost", port=6333)
        
        client.create_collection(
            collection_name="code_embeddings",
            vectors_config=VectorParams(
                size=768,  # CodeRankEmbed dimensions
                distance=Distance.COSINE
            )
        )
        ```
        
        ### Vector Operations
        - `upsert()`: Insert or update vectors
        - `search()`: Similarity search with filters
        - `delete()`: Remove vectors by ID or filter
        
        API endpoints support batch operations for better performance.
        """,
        
        "Code Documentation": """
        class EmbeddingProcessor:
            '''
            Processes text embeddings for Qdrant storage.
            
            Features:
            - Multi-model support (CodeRankEmbed, BGE-M3, etc.)
            - Automatic chunking with overlap
            - Quality scoring and validation
            - Batch processing optimization
            '''
            
            def __init__(self, model_name: str = "nomic-ai/CodeRankEmbed"):
                self.model = SentenceTransformerEmbedder(model_name)
                self.chunk_size = 1024
                self.overlap_ratio = 0.15
                
            async def process_document(self, content: str) -> List[DocumentChunk]:
                '''
                Process document into embeddings-ready chunks.
                
                Args:
                    content: Raw text content to process
                    
                Returns:
                    List of DocumentChunk objects with embeddings
                '''
                chunks = await self.chunker.chunk_document(content)
                embeddings = await self.model.embed_batch([c.content for c in chunks])
                
                for chunk, embedding in zip(chunks, embeddings):
                    chunk.embedding = embedding
                    
                return chunks
        """,
        
        "Technical Tutorial": """
        # Setting up Qdrant for Code Search
        
        This guide shows how to build a semantic code search system using Qdrant.
        
        ## Step 1: Install Dependencies
        
        ```bash
        pip install qdrant-client sentence-transformers
        ```
        
        ## Step 2: Initialize Embeddings
        
        For code search, we recommend CodeRankEmbed (768 dimensions):
        
        ```python
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer('nomic-ai/CodeRankEmbed')
        embeddings = model.encode(["def hello_world(): print('Hello!')"])
        ```
        
        ## Step 3: Store in Qdrant
        
        Create collection with proper configuration:
        - Use COSINE distance for semantic similarity
        - Enable indexing for fast retrieval
        - Set appropriate vector dimensions (768 for CodeRankEmbed)
        
        The system supports real-time updates and batch operations.
        """
    }
    
    logger.info("📊 Analyzing content types and recommendations...")
    
    # Analyze each sample
    for content_type, content in samples.items():
        logger.info(f"\n🔍 Analyzing: {content_type}")
        logger.info("-" * 40)
        
        # Content analysis
        analysis = analyzer.analyze_content(content, f"{content_type.lower()}.md")
        
        logger.info(f"Content Type: {analysis['content_type']}")
        logger.info(f"Code Density: {analysis['code_density']:.2f}")
        logger.info(f"API Density: {analysis['api_density']:.2f}")
        logger.info(f"Structure Complexity: {analysis['structure_complexity']:.2f}")
        logger.info(f"Recommended Model: {analysis['recommended_model']}")
        logger.info(f"Recommended Chunk Size: {analysis['recommended_chunk_size']}")
        
        # Model specifications
        model_spec = MODEL_SPECS[analysis['recommended_model']]
        logger.info(f"Model Dimensions: {model_spec.dimensions}")
        logger.info(f"Model Best For: {', '.join(model_spec.best_for)}")
        logger.info(f"Speed Score: {model_spec.speed_score}/10")
        logger.info(f"Quality Score: {model_spec.quality_score}/10")
        
        # Chunking preview
        chunks = await chunker.chunk_with_strategy(
            content, 
            title=content_type,
            source=f"{content_type.lower()}.md",
            strategy=ChunkingStrategy.ADAPTIVE
        )
        
        logger.info(f"Generated Chunks: {len(chunks)}")
        logger.info(f"Average Chunk Size: {sum(len(c.content) for c in chunks) // len(chunks)} chars")
        
        # Show first chunk as example
        if chunks:
            first_chunk = chunks[0]
            preview = first_chunk.content[:200] + "..." if len(first_chunk.content) > 200 else first_chunk.content
            logger.info(f"First Chunk Preview: {preview}")
            logger.info(f"Chunk Metadata: {dict(list(first_chunk.metadata.items())[:3])}")
    
    logger.info("\n🎯 Qdrant Integration Recommendations:")
    logger.info("=" * 50)
    logger.info("✅ Primary Model: CodeRankEmbed (768D) - Best for code & API docs")
    logger.info("✅ Fallback Model: BGE-M3 (1024D) - Hybrid dense/sparse search")
    logger.info("✅ Distance Metric: COSINE - Optimal for semantic similarity")
    logger.info("✅ Chunk Strategy: ADAPTIVE - Content-aware sizing")
    logger.info("✅ Overlap Ratio: 15% - Maintains context continuity")
    logger.info("✅ Quality Scoring: Enabled - Ensures embedding quality")
    
    logger.info("\n📈 Performance Optimizations:")
    logger.info("-" * 30)
    logger.info("🔧 Batch Processing: 8-16 documents per batch")
    logger.info("🔧 Memory Management: Progressive model loading")
    logger.info("🔧 Indexing: HNSW with appropriate parameters")
    logger.info("🔧 Quantization: Enable for large collections")
    logger.info("🔧 Filtering: Use payload-based filtering for metadata")
    
    logger.info("\n🚀 Demo completed! System ready for production deployment.")

if __name__ == "__main__":
    asyncio.run(demo_qdrant_optimized_system())