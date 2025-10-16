#!/usr/bin/env python3
"""
Modern MCP Server for Qdrant with CodeRankEmbed
==============================================

FastMCP-based server for your deployed 768-dim collections:
- sentence_transformers_768
- qdrant_ecosystem_768  
- docling_768

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
logger = logging.getLogger("qdrant-mcp-768")

# Initialize FastMCP server
mcp = FastMCP("qdrant-coderank-768")

# Global state
embedder: Optional[SentenceTransformerEmbedder] = None
stores: Dict[str, QdrantStore] = {}

# Configuration
EMBEDDING_MODEL = "nomic-ai/CodeRankEmbed"  # Updated to 768-dim model
VECTOR_SIZE = 768  # Updated dimension
COLLECTIONS = {
    "sentence_transformers_768": {
        "description": "Advanced embedding techniques and model optimization",
        "specialties": ["fine-tuning", "training", "model selection", "performance optimization"],
        "best_for": "Learning embedding strategies and implementation techniques"
    },
    "qdrant_ecosystem_768": {
        "description": "Vector search, sparse embeddings, and database optimization", 
        "specialties": ["vector search", "sparse embeddings", "quantization", "hybrid search"],
        "best_for": "Understanding vector database strategies and implementation"
    },
    "docling_768": {
        "description": "Document processing, structure extraction, and chunking",
        "specialties": ["document parsing", "structure extraction", "chunking strategies", "text processing"],
        "best_for": "Learning document processing and preparation techniques"
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
            device="cpu",
            batch_size=32
        )
        embedder = SentenceTransformerEmbedder(embedder_config)
        logger.info("✅ Embedder initialized")
    return embedder

async def get_store(collection_name: str) -> Optional[QdrantStore]:
    """Lazy-load and return a Qdrant store for the specified collection."""
    global stores
    
    if collection_name not in COLLECTIONS:
        logger.error(f"❌ Unknown collection: {collection_name}")
        return None
        
    if collection_name not in stores:
        logger.info(f"🔌 Connecting to Qdrant collection: {collection_name}")
        try:
            config = QdrantStoreConfig(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
                collection_name=collection_name,
                vector_size=VECTOR_SIZE,
                enable_quantization=True,
                prefer_grpc=False
            )
            stores[collection_name] = QdrantStore(config)
            logger.info(f"✅ Connected to collection: {collection_name}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to {collection_name}: {e}")
            return None
            
    return stores[collection_name]

def classify_query_for_collection(query: str) -> List[str]:
    """Classify which collections are most relevant for a query."""
    query_lower = query.lower()
    relevant_collections = []
    
    # Sentence Transformers queries
    if any(word in query_lower for word in [
        'embedding', 'transformer', 'model', 'fine-tune', 'training',
        'sentence', 'semantic', 'similarity', 'bert', 'roberta'
    ]):
        relevant_collections.append('sentence_transformers_768')
        
    # Qdrant/Vector search queries  
    if any(word in query_lower for word in [
        'vector', 'search', 'qdrant', 'similarity', 'index', 'query',
        'sparse', 'dense', 'hybrid', 'quantization', 'collection'
    ]):
        relevant_collections.append('qdrant_ecosystem_768')
        
    # Document processing queries
    if any(word in query_lower for word in [
        'document', 'pdf', 'text', 'chunk', 'parse', 'extract',
        'structure', 'docling', 'processing', 'conversion'
    ]):
        relevant_collections.append('docling_768')
        
    # Default to all collections if no specific match
    if not relevant_collections:
        relevant_collections = list(COLLECTIONS.keys())
        
    return relevant_collections

# MCP Tools
@mcp.tool()
async def search_collection(
    collection: str,
    query: str,
    limit: int = 5,
    score_threshold: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Search a specific Qdrant collection using semantic similarity.
    
    Args:
        collection: Collection name (sentence_transformers_768, qdrant_ecosystem_768, docling_768)
        query: Search query
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score (default: 0.3)
    
    Returns:
        List of search results with content, score, and metadata
    """
    try:
        # Validate collection
        if collection not in COLLECTIONS:
            return [{"error": f"Unknown collection: {collection}. Available: {list(COLLECTIONS.keys())}"}]
        
        # Get embedder and store
        embedder = await get_embedder()
        store = await get_store(collection)
        
        if not store:
            return [{"error": f"Failed to connect to collection: {collection}"}]
        
        # Generate embedding
        logger.info(f"🔍 Searching {collection} for: '{query}'")
        embeddings = await embedder.embed_documents([query])
        
        # Search collection
        results = store.search(
            query_embedding=embeddings[0],
            limit=limit,
            score_threshold=score_threshold
        )
        
        # Format results
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append({
                "rank": i,
                "score": round(result.get('score', 0.0), 3),
                "content": result.get('content', ''),
                "source": result.get('source_file', 'unknown'),
                "collection": collection,
                "metadata": result.get('metadata', {})
            })
        
        logger.info(f"✅ Found {len(formatted_results)} results in {collection}")
        return formatted_results
        
    except Exception as e:
        logger.error(f"❌ Search error: {e}")
        return [{"error": f"Search failed: {str(e)}"}]

@mcp.tool()
async def smart_search(
    query: str,
    limit: int = 10,
    auto_route: bool = True
) -> Dict[str, Any]:
    """
    Intelligent multi-collection search with automatic routing.
    
    Args:
        query: Search query
        limit: Total number of results across collections (default: 10)
        auto_route: Automatically determine relevant collections (default: True)
    
    Returns:
        Comprehensive search results across relevant collections
    """
    try:
        # Determine relevant collections
        if auto_route:
            target_collections = classify_query_for_collection(query)
        else:
            target_collections = list(COLLECTIONS.keys())
        
        logger.info(f"🎯 Smart search targeting: {target_collections}")
        
        # Search each relevant collection
        all_results = []
        results_per_collection = max(2, limit // len(target_collections))
        
        for collection in target_collections:
            collection_results = await search_collection(
                collection=collection,
                query=query,
                limit=results_per_collection,
                score_threshold=0.25
            )
            
            # Add collection context
            for result in collection_results:
                if "error" not in result:
                    result["collection_info"] = COLLECTIONS[collection]
                    
            all_results.extend(collection_results)
        
        # Sort by relevance and limit
        valid_results = [r for r in all_results if "error" not in r]
        valid_results.sort(key=lambda x: x.get('score', 0), reverse=True)
        top_results = valid_results[:limit]
        
        # Generate synthesis
        synthesis = generate_synthesis(query, top_results, target_collections)
        
        return {
            "query": query,
            "collections_searched": target_collections,
            "total_results": len(top_results),
            "results": top_results,
            "synthesis": synthesis,
            "query_classification": {
                "auto_routed": auto_route,
                "target_collections": target_collections,
                "query_type": classify_query_intent(query)
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Smart search error: {e}")
        return {"error": f"Smart search failed: {str(e)}"}

def classify_query_intent(query: str) -> str:
    """Classify the intent of a query."""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['how to', 'implement', 'example', 'tutorial']):
        return 'tutorial'
    elif any(word in query_lower for word in ['technique', 'method', 'approach', 'strategy']):
        return 'technique'  
    elif any(word in query_lower for word in ['concept', 'what is', 'explain', 'definition']):
        return 'concept'
    else:
        return 'implementation'

def generate_synthesis(query: str, results: List[Dict], collections: List[str]) -> str:
    """Generate a synthesis of search results."""
    if not results:
        return "No relevant information found."
    
    synthesis = f"Found {len(results)} relevant results across {len(set(r['collection'] for r in results))} collections.\n\n"
    
    # Group by collection
    by_collection = {}
    for result in results:
        collection = result['collection']
        if collection not in by_collection:
            by_collection[collection] = []
        by_collection[collection].append(result)
    
    # Summarize each collection's contributions
    for collection, coll_results in by_collection.items():
        clean_name = collection.replace('_768', '').replace('_', ' ').title()
        collection_info = COLLECTIONS[collection]
        
        synthesis += f"**{clean_name}** ({len(coll_results)} results):\n"
        synthesis += f"Expertise: {collection_info['description']}\n"
        
        # Show top results
        for i, result in enumerate(coll_results[:2], 1):
            score = result['score']
            preview = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
            synthesis += f"  {i}. (Score: {score}) {preview}\n"
        
        synthesis += "\n"
    
    return synthesis

@mcp.tool()
async def get_collections_info() -> Dict[str, Any]:
    """
    Get information about available collections and their specialties.
    
    Returns:
        Dictionary with collection information and statistics
    """
    try:
        collections_info = {}
        
        for collection_name, info in COLLECTIONS.items():
            # Test connection
            store = await get_store(collection_name)
            connection_status = "✅ Connected" if store else "❌ Error"
            
            collections_info[collection_name] = {
                "description": info["description"],
                "specialties": info["specialties"],
                "best_for": info["best_for"],
                "connection_status": connection_status,
                "vector_dimension": VECTOR_SIZE,
                "embedding_model": EMBEDDING_MODEL
            }
        
        return {
            "total_collections": len(COLLECTIONS),
            "embedding_model": EMBEDDING_MODEL,
            "vector_dimension": VECTOR_SIZE,
            "qdrant_host": QDRANT_HOST,
            "qdrant_port": QDRANT_PORT,
            "collections": collections_info
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting collections info: {e}")
        return {"error": f"Failed to get collections info: {str(e)}"}

@mcp.tool()
async def learn_about_topic(
    topic: str,
    depth: str = "intermediate",
    focus_collection: Optional[str] = None
) -> Dict[str, Any]:
    """
    Learn comprehensively about a specific topic using the knowledge base.
    
    Args:
        topic: Topic to learn about
        depth: Learning depth (basic, intermediate, advanced)
        focus_collection: Specific collection to focus on (optional)
    
    Returns:
        Structured learning content about the topic
    """
    try:
        # Generate learning-focused query
        depth_prefixes = {
            'basic': 'introduction to',
            'intermediate': 'how to implement',
            'advanced': 'advanced techniques for'
        }
        
        prefix = depth_prefixes.get(depth, 'how to use')
        learning_query = f"{prefix} {topic}"
        
        # Determine collections to search
        if focus_collection and focus_collection in COLLECTIONS:
            target_collections = [focus_collection]
        else:
            target_collections = classify_query_for_collection(topic)
        
        logger.info(f"📚 Learning about '{topic}' at {depth} level")
        
        # Search for learning content
        all_results = []
        for collection in target_collections:
            results = await search_collection(
                collection=collection,
                query=learning_query,
                limit=8,
                score_threshold=0.25
            )
            all_results.extend([r for r in results if "error" not in r])
        
        # Structure learning content
        learning_content = structure_learning_content(topic, all_results, depth)
        
        return learning_content
        
    except Exception as e:
        logger.error(f"❌ Learning error: {e}")
        return {"error": f"Learning failed: {str(e)}"}

def structure_learning_content(topic: str, results: List[Dict], depth: str) -> Dict[str, Any]:
    """Structure search results into comprehensive learning content."""
    
    content = {
        'topic': topic,
        'depth_level': depth,
        'summary': f"Learning about {topic} at {depth} level",
        'key_concepts': [],
        'implementation_guide': [],
        'code_examples': [],
        'best_practices': [],
        'related_topics': [],
        'learning_path': generate_learning_path(topic, depth),
        'sources': []
    }
    
    for result in results:
        text = result.get('content', '')
        score = result.get('score', 0.0)
        source = result.get('source', 'unknown')
        collection = result.get('collection', 'unknown')
        
        # Categorize content
        text_lower = text.lower()
        
        # Key concepts
        if any(keyword in text_lower for keyword in ['concept', 'definition', 'what is', 'principle']):
            content['key_concepts'].append({
                'text': text[:300] + "..." if len(text) > 300 else text,
                'relevance': score,
                'source': source,
                'collection': collection
            })
        
        # Implementation details
        if any(keyword in text_lower for keyword in ['how to', 'implementation', 'step', 'process']):
            content['implementation_guide'].append({
                'text': text[:400] + "..." if len(text) > 400 else text,
                'relevance': score,
                'source': source,
                'collection': collection
            })
        
        # Code examples
        if any(keyword in text_lower for keyword in ['example', 'code', 'snippet', '```', 'def ', 'class ']):
            content['code_examples'].append({
                'text': text[:500] + "..." if len(text) > 500 else text,
                'relevance': score,
                'source': source,
                'collection': collection
            })
        
        # Best practices
        if any(keyword in text_lower for keyword in ['best practice', 'recommendation', 'should', 'avoid']):
            content['best_practices'].append({
                'text': text[:300] + "..." if len(text) > 300 else text,
                'relevance': score,
                'source': source,
                'collection': collection
            })
        
        content['sources'].append({
            'file': source,
            'collection': collection,
            'relevance': score,
            'preview': text[:150] + "..." if len(text) > 150 else text
        })
    
    # Sort by relevance and limit
    for key in ['key_concepts', 'implementation_guide', 'code_examples', 'best_practices']:
        content[key].sort(key=lambda x: x['relevance'], reverse=True)
        content[key] = content[key][:5]  # Top 5 for each category
    
    content['sources'].sort(key=lambda x: x['relevance'], reverse=True)
    content['sources'] = content['sources'][:10]  # Top 10 sources
    
    return content

def generate_learning_path(topic: str, depth: str) -> List[str]:
    """Generate a suggested learning path for the topic."""
    base_path = [
        f"Understand {topic} fundamentals",
        f"Explore {topic} implementation approaches",
        f"Practice {topic} with examples",
        f"Apply {topic} to real scenarios"
    ]
    
    depth_specific = {
        'basic': [
            f"Follow {topic} tutorials",
            f"Run basic {topic} examples"
        ],
        'intermediate': [
            f"Implement {topic} in projects",
            f"Optimize {topic} performance"
        ],
        'advanced': [
            f"Research latest {topic} developments",
            f"Contribute to {topic} community"
        ]
    }
    
    return base_path + depth_specific.get(depth, [])

# Health check
@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check the health of the MCP server and Qdrant connections.
    
    Returns:
        Health status of all components
    """
    try:
        health_status = {
            "server": "✅ MCP Server running",
            "embedding_model": EMBEDDING_MODEL,
            "vector_dimension": VECTOR_SIZE,
            "collections": {}
        }
        
        # Check each collection
        for collection_name in COLLECTIONS.keys():
            try:
                store = await get_store(collection_name)
                if store:
                    # Test with a simple search
                    embedder = await get_embedder()
                    test_embeddings = await embedder.embed_documents(["test"])
                    test_results = store.search(test_embeddings[0], limit=1)
                    
                    health_status["collections"][collection_name] = {
                        "status": "✅ Healthy",
                        "test_search": f"Found {len(test_results)} results"
                    }
                else:
                    health_status["collections"][collection_name] = {
                        "status": "❌ Connection failed"
                    }
            except Exception as e:
                health_status["collections"][collection_name] = {
                    "status": f"❌ Error: {str(e)}"
                }
        
        return health_status
        
    except Exception as e:
        return {"error": f"Health check failed: {str(e)}"}

# Server startup
async def main():
    """Main server function."""
    logger.info("🚀 Starting Qdrant MCP Server (CodeRankEmbed 768-dim)")
    logger.info(f"📊 Collections: {list(COLLECTIONS.keys())}")
    logger.info(f"🤖 Embedding Model: {EMBEDDING_MODEL}")
    logger.info(f"🔌 Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
    
    # Pre-initialize embedder
    await get_embedder()
    
    # Test connections
    logger.info("🔍 Testing collection connections...")
    for collection in COLLECTIONS.keys():
        store = await get_store(collection)
        if store:
            logger.info(f"✅ {collection} connected")
        else:
            logger.warning(f"⚠️ {collection} connection failed")
    
    logger.info("✅ MCP Server ready!")
    
    # Run the server
    await mcp.run()

if __name__ == "__main__":
    asyncio.run(main())