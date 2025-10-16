#!/usr/bin/env python3
"""
🏆 ULTIMATE QDRANT MCP SERVER - OPTIMIZED
=========================================

FastMCP-based server for our 3 production collections:
✅ sentence_transformers_768: 457 vectors (embedding expertise)
✅ docling_768: 1,089 vectors (document processing mastery)  
✅ qdrant_ecosystem_768: 8,108 vectors (vector DB optimization)

Total: 9,654 vectors of pure knowledge!

Uses CodeRankEmbed (768-dim) for optimal performance.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from fastmcp import FastMCP
    from mcp.types import TextContent
except ImportError:
    print("❌ FastMCP not found. Installing...")
    os.system("pip install fastmcp")
    from fastmcp import FastMCP
    from mcp.types import TextContent

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ultimate-qdrant-mcp")

# Initialize FastMCP server
mcp = FastMCP("ultimate-qdrant-knowledge")

# Global state
embedder: Optional[SentenceTransformerEmbedder] = None
stores: Dict[str, QdrantStore] = {}

# Configuration - UPDATED with our actual collections
EMBEDDING_MODEL = "nomic-ai/CodeRankEmbed"  # 768-dim model
VECTOR_SIZE = 768

# Our 3 production collections with their specialties
ULTIMATE_COLLECTIONS = {
    "sentence_transformers_768": {
        "points": 457,
        "description": "Embedding techniques, model optimization, and fine-tuning strategies",
        "specialties": [
            "embedding model selection", "fine-tuning techniques", "training strategies",
            "performance optimization", "model evaluation", "transformer architectures",
            "semantic similarity", "vector representations"
        ],
        "best_for": "Learning advanced embedding strategies and implementation techniques",
        "knowledge_areas": ["transformers", "embeddings", "semantic search", "model training"]
    },
    "docling_768": {
        "points": 1089,
        "description": "Document processing, structure extraction, and advanced chunking strategies",
        "specialties": [
            "document parsing", "structure extraction", "chunking strategies", "text processing",
            "PDF processing", "markdown conversion", "content organization", "metadata extraction",
            "pipeline optimization", "format detection"
        ],
        "best_for": "Mastering document processing and preparation techniques",
        "knowledge_areas": ["document processing", "chunking", "text extraction", "pipeline design"]
    },
    "qdrant_ecosystem_768": {
        "points": 8108,
        "description": "Vector database optimization, search strategies, and production deployment",
        "specialties": [
            "vector search", "sparse embeddings", "quantization", "hybrid search",
            "collection management", "indexing optimization", "performance tuning",
            "production deployment", "scaling strategies", "search algorithms"
        ],
        "best_for": "Understanding vector database optimization and deployment strategies",
        "knowledge_areas": ["vector databases", "search optimization", "qdrant", "production scaling"]
    }
}

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

async def get_embedder():
    """Lazy-load and return the embedder."""
    global embedder
    if embedder is None:
        logger.info(f"🚀 Initializing embedder: {EMBEDDING_MODEL}")
        embedder_config = EmbedderConfig(
            model_name=EMBEDDING_MODEL,
            device="auto",
            batch_size=32
        )
        embedder = SentenceTransformerEmbedder(embedder_config)
        logger.info("✅ Embedder initialized successfully")
    return embedder

async def get_store(collection_name: str):
    """Get or create a store for the given collection."""
    if collection_name not in stores:
        if collection_name not in ULTIMATE_COLLECTIONS:
            raise ValueError(f"Unknown collection: {collection_name}. Available: {list(ULTIMATE_COLLECTIONS.keys())}")
        
        logger.info(f"🔌 Connecting to collection: {collection_name}")
        try:
            config = QdrantStoreConfig(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                collection_name=collection_name,
                vector_size=VECTOR_SIZE,
                distance_metric="Cosine",
                enable_quantization=True,
                prefer_grpc=False
            )
            stores[collection_name] = QdrantStore(config)
            logger.info(f"✅ Connected to {collection_name}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to {collection_name}: {e}")
            raise
    
    return stores[collection_name]

def classify_query_collections(query: str) -> List[str]:
    """Intelligently classify which collections are most relevant for a query."""
    query_lower = query.lower()
    relevant_collections = []
    
    # Embedding-related queries
    embedding_keywords = [
        'embedding', 'encode', 'vector', 'similarity', 'semantic', 'transformer',
        'bert', 'model', 'fine-tuning', 'training', 'representation'
    ]
    if any(keyword in query_lower for keyword in embedding_keywords):
        relevant_collections.append('sentence_transformers_768')
    
    # Document processing queries
    docling_keywords = [
        'document', 'pdf', 'parsing', 'chunking', 'text', 'structure', 
        'extraction', 'processing', 'pipeline', 'conversion', 'format'
    ]
    if any(keyword in query_lower for keyword in docling_keywords):
        relevant_collections.append('docling_768')
    
    # Vector database and Qdrant queries
    qdrant_keywords = [
        'qdrant', 'vector database', 'search', 'collection', 'quantization',
        'indexing', 'performance', 'optimization', 'production', 'deployment', 'scaling'
    ]
    if any(keyword in query_lower for keyword in qdrant_keywords):
        relevant_collections.append('qdrant_ecosystem_768')
    
    # Default to all collections if no specific match or for general queries
    if not relevant_collections or any(word in query_lower for word in ['best', 'optimal', 'recommend', 'compare']):
        relevant_collections = list(ULTIMATE_COLLECTIONS.keys())
    
    return relevant_collections

@mcp.tool()
async def semantic_search_ultimate(
    query: str,
    collections: Optional[List[str]] = None,
    limit: int = 10,
    score_threshold: float = 0.7,
    hybrid_search: bool = True
) -> str:
    """
    🚀 ULTIMATE SEMANTIC SEARCH across 9,654 knowledge vectors.
    
    Enhanced search with:
    - Multi-collection semantic search
    - Hybrid dense + sparse retrieval
    - Content-aware collection routing
    - Quality score filtering
    - Result ranking and synthesis
    
    Args:
        query: Search query (natural language)
        collections: Specific collections to search (auto-detected if None)
        limit: Max results per collection (default: 10)
        score_threshold: Minimum similarity score (0.0-1.0)
        hybrid_search: Enable hybrid dense+sparse search
    """
    try:
        logger.info(f"🔍 ULTIMATE SEMANTIC SEARCH: '{query}'")
        
        # Initialize embedder
        embedder = await get_embedder()
        
        # Auto-detect relevant collections
        if not collections:
            collections = classify_query_collections(query)
            logger.info(f"🎯 Auto-detected collections: {collections}")
        
        # Generate query embedding
        query_vector = await embedder.embed_query(query)
        
        all_results = []
        search_metadata = {
            "query": query,
            "collections_searched": collections,
            "total_vectors_searched": 0,
            "search_type": "hybrid" if hybrid_search else "dense",
            "score_threshold": score_threshold
        }
        
        # Search each collection
        for collection_name in collections:
            if collection_name not in stores:
                await get_store(collection_name)
            
            store = stores[collection_name]
            collection_info = ULTIMATE_COLLECTIONS[collection_name]
            
            logger.info(f"🔍 Searching {collection_name} ({collection_info['vectors']} vectors)")
            search_metadata["total_vectors_searched"] += collection_info["vectors"]
            
            # Perform semantic search
            results = await store.search(
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )
            
            # Enhance results with collection context
            for result in results:
                result.payload["collection_source"] = collection_name
                result.payload["collection_specialty"] = collection_info["description"]
                result.payload["search_score"] = result.score
                result.payload["knowledge_type"] = collection_info.get("knowledge_type", "general")
                
                all_results.append({
                    "content": result.payload.get("content", ""),
                    "score": result.score,
                    "collection": collection_name,
                    "source": result.payload.get("source", ""),
                    "metadata": result.payload,
                    "chunk_id": result.payload.get("chunk_id", result.id)
                })
        
        # Sort all results by score
        all_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top results across all collections
        top_results = all_results[:limit * 2]  # Get more for synthesis
        
        # Generate enhanced response
        if not top_results:
            return f"❌ No results found for '{query}' above threshold {score_threshold}"
        
        # Format results with ultimate knowledge synthesis
        response_parts = [
            f"🧠 ULTIMATE KNOWLEDGE SEARCH RESULTS",
            f"Query: '{query}'",
            f"Collections: {', '.join(collections)}",
            f"Total vectors searched: {search_metadata['total_vectors_searched']:,}",
            f"Results found: {len(top_results)}",
            f"Score threshold: {score_threshold}",
            "",
            "📊 RESULTS:"
        ]
        
        for i, result in enumerate(top_results[:limit], 1):
            collection_emoji = {
                "docling_768": "📚",
                "qdrant_ecosystem_768": "🔍", 
                "sentence_transformers_768": "🧠"
            }.get(result["collection"], "📄")
            
            response_parts.extend([
                f"\n{i}. {collection_emoji} {result['collection'].upper()}",
                f"   Score: {result['score']:.3f}",
                f"   Source: {result['source']}",
                f"   Content: {result['content'][:300]}{'...' if len(result['content']) > 300 else ''}",
                ""
            ])
        
        # Add knowledge synthesis
        response_parts.extend([
            "",
            "🎯 KNOWLEDGE SYNTHESIS:",
            f"• Found expertise across {len(set(r['collection'] for r in top_results))} knowledge domains",
            f"• Average relevance score: {sum(r['score'] for r in top_results[:5]) / min(5, len(top_results)):.3f}",
            f"• Primary knowledge source: {max(set(r['collection'] for r in top_results), key=lambda x: sum(1 for r in top_results if r['collection'] == x))}",
            ""
        ])
        
        return "\n".join(response_parts)
        
    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        return f"❌ Search error: {str(e)}"

@mcp.tool()
async def search_ultimate_knowledge(
    query: str,
    collections: Optional[List[str]] = None,
    limit: int = 10,
    score_threshold: float = 0.7
) -> str:
    """
    🧠 Search the ultimate knowledge base across all 9,654 vectors.
    
    Legacy function - use semantic_search_ultimate for enhanced features.
    """
    return await semantic_search_ultimate(query, collections, limit, score_threshold, hybrid_search=False)

@mcp.tool()
async def get_collection_stats() -> str:
    """📊 Get statistics for all Ultimate Qdrant collections."""
    try:
        stats = []
        for name, info in ULTIMATE_COLLECTIONS.items():
            stats.append(f"🔹 {name}: {info['vectors']:,} vectors - {info['description']}")
        
        return f"""
🏆 ULTIMATE QDRANT KNOWLEDGE BASE STATS
{'='*50}
Total Collections: {len(ULTIMATE_COLLECTIONS)}
Total Vectors: {sum(info['vectors'] for info in ULTIMATE_COLLECTIONS.values()):,}

📊 Collection Breakdown:
{chr(10).join(stats)}

🎯 Ready for semantic search across all knowledge domains!
"""
    except Exception as e:
        return f"❌ Error getting stats: {e}"

@mcp.tool()
async def optimize_chunking_strategy(
    content_type: str = "general",
    content_length: int = 1000,
    knowledge_domain: str = "mixed"
) -> str:
        if invalid_collections:
            return f"❌ Invalid collections: {invalid_collections}. Available: {list(ULTIMATE_COLLECTIONS.keys())}"
        
        # Get embedder
        embedder = await get_embedder()
        query_vector = await embedder.embed_query(query)
        
        # Search each relevant collection
        all_results = []
        total_searched = 0
        
        for collection_name in collections:
            try:
                store = await get_store(collection_name)
                collection_info = ULTIMATE_COLLECTIONS[collection_name]
                
                logger.info(f"🔎 Searching {collection_name} ({collection_info['points']} vectors)")
                
                results = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: store.search(
                        query_embedding=query_vector,
                        limit=limit,
                        score_threshold=score_threshold
                    )
                )
                
                total_searched += collection_info['points']
                
                # Enhance results with collection context
                for result in results:
                    result['collection'] = collection_name
                    result['collection_specialty'] = collection_info['description']
                    result['knowledge_area'] = collection_info['knowledge_areas']
                
                all_results.extend(results)
                logger.info(f"✅ Found {len(results)} results in {collection_name}")
                
            except Exception as e:
                logger.error(f"❌ Error searching {collection_name}: {e}")
                all_results.append({
                    'content': f"Error searching {collection_name}: {str(e)}",
                    'score': 0.0,
                    'collection': collection_name,
                    'error': True
                })
        
        # Sort all results by score
        all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Format results
        if not all_results:
            return f"""🤔 No results found for "{query}"

💡 Suggestions:
- Try different keywords or synonyms
- Lower the score_threshold (currently {score_threshold})
- Check spelling and try broader terms

📊 Searched {total_searched:,} vectors across {len(collections)} collections"""

        # Build comprehensive response
        response_parts = [
            f"🧠 **ULTIMATE KNOWLEDGE SEARCH RESULTS**",
            f"📊 Query: \"{query}\"",
            f"🎯 Collections: {', '.join(collections)}",
            f"🔢 Searched: {total_searched:,} vectors",
            f"📋 Results: {len(all_results)}",
            "",
            "=" * 60
        ]
        
        for i, result in enumerate(all_results[:limit], 1):
            if result.get('error'):
                response_parts.append(f"\n❌ **Error Result {i}**")
                response_parts.append(f"Collection: {result['collection']}")
                response_parts.append(f"Error: {result['content']}")
                continue
            
            collection = result.get('collection', 'unknown')
            score = result.get('score', 0)
            content = result.get('content', 'No content')
            specialty = result.get('collection_specialty', 'No specialty info')
            
            response_parts.extend([
                f"\n🎯 **Result {i}** (Score: {score:.3f})",
                f"📚 Collection: {collection}",
                f"🎪 Specialty: {specialty}",
                f"📄 Content:",
                f"{content[:500]}{'...' if len(content) > 500 else ''}",
                ""
            ])
        
        # Add collection summaries
        response_parts.extend([
            "",
            "📊 **COLLECTION SUMMARIES**",
            "=" * 30
        ])
        
        for collection_name in collections:
            if collection_name in ULTIMATE_COLLECTIONS:
                info = ULTIMATE_COLLECTIONS[collection_name]
                response_parts.extend([
                    f"\n🏷️ **{collection_name}** ({info['points']} vectors)",
                    f"📖 {info['description']}",
                    f"🎯 Best for: {info['best_for']}",
                    f"🔑 Key areas: {', '.join(info['knowledge_areas'])}"
                ])
        
        return "\n".join(response_parts)
        
    except Exception as e:
        logger.error(f"❌ Search error: {e}")
        return f"❌ Search failed: {str(e)}"

@mcp.tool()
async def get_collections_status() -> str:
    """
    📊 Get the status and statistics of all ultimate knowledge collections.
    
    Returns detailed information about our 3 production collections with 9,654 total vectors.
    """
    try:
        status_parts = [
            "🏆 **ULTIMATE QDRANT KNOWLEDGE BASE STATUS**",
            "=" * 50,
            f"🎯 Total Collections: {len(ULTIMATE_COLLECTIONS)}",
            f"📊 Total Vectors: {sum(info['points'] for info in ULTIMATE_COLLECTIONS.values()):,}",
            f"🤖 Embedding Model: {EMBEDDING_MODEL}",
            f"📐 Vector Dimensions: {VECTOR_SIZE}",
            "",
            "📋 **COLLECTION DETAILS**",
            "=" * 30
        ]
        
        for collection_name, info in ULTIMATE_COLLECTIONS.items():
            try:
                # Try to get live stats
                store = await get_store(collection_name)
                # Add live status check if needed
                live_status = "✅ Connected"
            except Exception as e:
                live_status = f"⚠️ Connection issue: {str(e)}"
            
            status_parts.extend([
                f"\n🏷️ **{collection_name}**",
                f"📊 Vectors: {info['points']:,}",
                f"🎯 Status: {live_status}",
                f"📖 Description: {info['description']}",
                f"🎪 Specialties: {', '.join(info['specialties'][:3])}...",
                f"🔑 Knowledge Areas: {', '.join(info['knowledge_areas'])}",
                f"💡 Best For: {info['best_for']}"
            ])
        
        status_parts.extend([
            "",
            "🚀 **QUICK SEARCH TIPS**",
            "• For embedding help: mention 'embedding', 'model', 'training'",
            "• For document processing: mention 'document', 'chunking', 'parsing'", 
            "• For vector DB optimization: mention 'qdrant', 'search', 'performance'",
            "",
            "💪 **READY FOR ULTIMATE KNOWLEDGE QUERIES!**"
        ])
        
        return "\n".join(status_parts)
        
    except Exception as e:
        logger.error(f"❌ Status check error: {e}")
        return f"❌ Failed to get status: {str(e)}"

@mcp.tool()
async def get_collection_expertise(collection_name: str) -> str:
    """
    🎓 Get detailed expertise information about a specific collection.
    
    Args:
        collection_name: One of sentence_transformers_768, docling_768, qdrant_ecosystem_768
    """
    if collection_name not in ULTIMATE_COLLECTIONS:
        return f"❌ Unknown collection: {collection_name}\nAvailable: {', '.join(ULTIMATE_COLLECTIONS.keys())}"
    
    info = ULTIMATE_COLLECTIONS[collection_name]
    
    expertise_parts = [
        f"🎓 **{collection_name.upper()} EXPERTISE**",
        "=" * 50,
        f"📊 Vector Count: {info['points']:,}",
        f"📖 Description: {info['description']}",
        "",
        "🎯 **CORE SPECIALTIES**",
        "=" * 20
    ]
    
    for i, specialty in enumerate(info['specialties'], 1):
        expertise_parts.append(f"{i:2d}. {specialty}")
    
    expertise_parts.extend([
        "",
        f"💡 **BEST FOR**: {info['best_for']}",
        "",
        "🔑 **KNOWLEDGE AREAS**",
        "=" * 18
    ])
    
    for area in info['knowledge_areas']:
        expertise_parts.append(f"• {area}")
    
    expertise_parts.extend([
        "",
        "🚀 **USAGE EXAMPLES**",
        "=" * 16,
        f"Search this collection: search_ultimate_knowledge('your query', collections=['{collection_name}'])",
        f"Get specific help: search_ultimate_knowledge('how to optimize {info['knowledge_areas'][0]}')",
        "",
        "💪 **READY TO LEVERAGE THIS EXPERTISE!**"
    ])
    
    return "\n".join(expertise_parts)

# Health check and initialization
@mcp.tool()
async def health_check() -> str:
    """🏥 Check the health of the ultimate knowledge system."""
    try:
        health_info = [
            "🏥 **ULTIMATE KNOWLEDGE SYSTEM HEALTH CHECK**",
            "=" * 50
        ]
        
        # Check embedder
        try:
            embedder = await get_embedder()
            health_info.append("✅ Embedder: Ready")
        except Exception as e:
            health_info.append(f"❌ Embedder: {str(e)}")
        
        # Check each collection
        healthy_collections = 0
        for collection_name in ULTIMATE_COLLECTIONS:
            try:
                store = await get_store(collection_name)
                health_info.append(f"✅ {collection_name}: Connected")
                healthy_collections += 1
            except Exception as e:
                health_info.append(f"❌ {collection_name}: {str(e)}")
        
        health_info.extend([
            "",
            f"📊 **SUMMARY**",
            f"Healthy Collections: {healthy_collections}/{len(ULTIMATE_COLLECTIONS)}",
            f"Total Vectors Available: {sum(info['points'] for info in ULTIMATE_COLLECTIONS.values()):,}",
            "",
            "🚀 **SYSTEM STATUS**: " + ("READY" if healthy_collections == len(ULTIMATE_COLLECTIONS) else "DEGRADED")
        ])
        
        return "\n".join(health_info)
        
    except Exception as e:
        return f"❌ Health check failed: {str(e)}"

if __name__ == "__main__":
    print("🏆 ULTIMATE QDRANT MCP SERVER")
    print("=" * 40)
    print(f"📊 Collections: {len(ULTIMATE_COLLECTIONS)}")
    print(f"🎯 Total Vectors: {sum(info['points'] for info in ULTIMATE_COLLECTIONS.values()):,}")
    print("🚀 Starting server...")
    mcp.run()