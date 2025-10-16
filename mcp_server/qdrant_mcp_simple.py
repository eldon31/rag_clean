#!/usr/bin/env python3
"""
Qdrant MCP Server - Simplified Version
=====================================

MCP server for your deployed 768-dim collections using stdio protocol.
Provides tools to search and learn from your knowledge base.
"""

import asyncio
import logging
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    LoggingLevel
)

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-mcp-768")

# Global state
embedder: Optional[SentenceTransformerEmbedder] = None
stores: Dict[str, QdrantStore] = {}

# Configuration
EMBEDDING_MODEL = "nomic-ai/CodeRankEmbed"
VECTOR_SIZE = 768
COLLECTIONS = {
    "sentence_transformers_768": {
        "description": "Advanced embedding techniques and model optimization",
        "specialties": ["fine-tuning", "training", "model selection", "performance optimization"]
    },
    "qdrant_ecosystem_768": {
        "description": "Vector search, sparse embeddings, and database optimization", 
        "specialties": ["vector search", "sparse embeddings", "quantization", "hybrid search"]
    },
    "docling_768": {
        "description": "Document processing, structure extraction, and chunking",
        "specialties": ["document parsing", "structure extraction", "chunking strategies"]
    }
}

async def initialize_embedder():
    """Initialize the embedding model."""
    global embedder
    if embedder is None:
        logger.info(f"Initializing embedder: {EMBEDDING_MODEL}")
        embedder_config = EmbedderConfig(
            model_name=EMBEDDING_MODEL,
            device="cpu",
            batch_size=32
        )
        embedder = SentenceTransformerEmbedder(embedder_config)
        logger.info("Embedder initialized")

async def initialize_qdrant_stores():
    """Initialize Qdrant connections for all collections."""
    global stores
    
    for collection in COLLECTIONS.keys():
        if collection not in stores:
            logger.info(f"Connecting to Qdrant collection: {collection}")
            config = QdrantStoreConfig(
                host="localhost",
                port=6333,
                collection_name=collection,
                vector_size=VECTOR_SIZE,
                enable_quantization=True,
                prefer_grpc=False
            )
            stores[collection] = QdrantStore(config)
            logger.info(f"Connected to collection: {collection}")

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

# Create MCP server
server = Server("qdrant-coderank-768")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_collection",
            description="Search a specific Qdrant collection using semantic similarity",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {
                        "type": "string",
                        "description": "Collection name",
                        "enum": list(COLLECTIONS.keys())
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results (default: 5)",
                        "default": 5
                    },
                    "score_threshold": {
                        "type": "number",
                        "description": "Minimum similarity score (default: 0.3)",
                        "default": 0.3
                    }
                },
                "required": ["collection", "query"]
            }
        ),
        Tool(
            name="smart_search",
            description="Intelligent multi-collection search with automatic routing",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Total number of results (default: 10)",
                        "default": 10
                    },
                    "auto_route": {
                        "type": "boolean",
                        "description": "Automatically determine relevant collections (default: true)",
                        "default": True
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="learn_about_topic",
            description="Learn comprehensively about a topic using the knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to learn about"
                    },
                    "depth": {
                        "type": "string",
                        "description": "Learning depth",
                        "enum": ["basic", "intermediate", "advanced"],
                        "default": "intermediate"
                    },
                    "focus_collection": {
                        "type": "string",
                        "description": "Specific collection to focus on (optional)",
                        "enum": list(COLLECTIONS.keys())
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="get_collections_info",
            description="Get information about available collections and their specialties",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="health_check",
            description="Check the health of the MCP server and Qdrant connections",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        # Initialize components if needed
        await initialize_embedder()
        await initialize_qdrant_stores()
        
        if name == "search_collection":
            result = await search_collection_impl(arguments)
        elif name == "smart_search":
            result = await smart_search_impl(arguments)
        elif name == "learn_about_topic":
            result = await learn_about_topic_impl(arguments)
        elif name == "get_collections_info":
            result = await get_collections_info_impl()
        elif name == "health_check":
            result = await health_check_impl()
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Tool call error: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

async def search_collection_impl(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Implementation for search_collection tool."""
    collection = arguments["collection"]
    query = arguments["query"]
    limit = arguments.get("limit", 5)
    score_threshold = arguments.get("score_threshold", 0.3)
    
    if collection not in COLLECTIONS:
        return {"error": f"Unknown collection: {collection}"}
    
    if collection not in stores:
        return {"error": f"Collection {collection} not connected"}
    
    # Ensure embedder is initialized
    if embedder is None:
        return {"error": "Embedder not initialized"}
    
    # Generate embedding
    embeddings = await embedder.embed_documents([query])
    
    # Search collection
    results = stores[collection].search(
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
            "collection": collection
        })
    
    return {
        "collection": collection,
        "query": query,
        "total_results": len(formatted_results),
        "results": formatted_results
    }

async def smart_search_impl(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Implementation for smart_search tool."""
    query = arguments["query"]
    limit = arguments.get("limit", 10)
    auto_route = arguments.get("auto_route", True)
    
    # Determine relevant collections
    if auto_route:
        target_collections = classify_query_for_collection(query)
    else:
        target_collections = list(COLLECTIONS.keys())
    
    # Search each relevant collection
    all_results = []
    results_per_collection = max(2, limit // len(target_collections))
    
    # Ensure embedder is initialized
    if embedder is None:
        return {"error": "Embedder not initialized"}
    
    for collection in target_collections:
        if collection in stores:
            # Generate embedding
            embeddings = await embedder.embed_documents([query])
            
            # Search collection
            results = stores[collection].search(
                query_embedding=embeddings[0],
                limit=results_per_collection,
                score_threshold=0.25
            )
            
            # Format results
            for i, result in enumerate(results, 1):
                all_results.append({
                    "rank": len(all_results) + 1,
                    "score": round(result.get('score', 0.0), 3),
                    "content": result.get('content', ''),
                    "source": result.get('source_file', 'unknown'),
                    "collection": collection,
                    "collection_info": COLLECTIONS[collection]
                })
    
    # Sort by relevance and limit
    all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_results = all_results[:limit]
    
    return {
        "query": query,
        "collections_searched": target_collections,
        "total_results": len(top_results),
        "results": top_results,
        "auto_routed": auto_route
    }

async def learn_about_topic_impl(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Implementation for learn_about_topic tool."""
    topic = arguments["topic"]
    depth = arguments.get("depth", "intermediate")
    focus_collection = arguments.get("focus_collection")
    
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
    
    # Search for learning content
    all_results = []
    
    # Ensure embedder is initialized
    if embedder is None:
        return {"error": "Embedder not initialized"}
    
    for collection in target_collections:
        if collection in stores:
            embeddings = await embedder.embed_documents([learning_query])
            results = stores[collection].search(
                query_embedding=embeddings[0],
                limit=5,
                score_threshold=0.25
            )
            
            for result in results:
                all_results.append({
                    "content": result.get('content', ''),
                    "score": round(result.get('score', 0.0), 3),
                    "source": result.get('source_file', 'unknown'),
                    "collection": collection
                })
    
    # Sort by relevance
    all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    return {
        "topic": topic,
        "depth_level": depth,
        "learning_query": learning_query,
        "collections_searched": target_collections,
        "total_results": len(all_results),
        "learning_content": all_results[:10]
    }

async def get_collections_info_impl() -> Dict[str, Any]:
    """Implementation for get_collections_info tool."""
    collections_info = {}
    
    for collection_name, info in COLLECTIONS.items():
        connection_status = "✅ Connected" if collection_name in stores else "❌ Not connected"
        
        collections_info[collection_name] = {
            "description": info["description"],
            "specialties": info["specialties"],
            "connection_status": connection_status,
            "vector_dimension": VECTOR_SIZE,
            "embedding_model": EMBEDDING_MODEL
        }
    
    return {
        "total_collections": len(COLLECTIONS),
        "embedding_model": EMBEDDING_MODEL,
        "vector_dimension": VECTOR_SIZE,
        "collections": collections_info
    }

async def health_check_impl() -> Dict[str, Any]:
    """Implementation for health_check tool."""
    health_status = {
        "server": "✅ MCP Server running",
        "embedding_model": EMBEDDING_MODEL,
        "vector_dimension": VECTOR_SIZE,
        "collections": {}
    }
    
    # Check each collection
    for collection_name in COLLECTIONS.keys():
        if collection_name in stores:
            try:
                # Ensure embedder is initialized
                if embedder is None:
                    health_status["collections"][collection_name] = {
                        "status": "❌ Embedder not initialized"
                    }
                    continue
                
                # Test with a simple search
                embeddings = await embedder.embed_documents(["test"])
                test_results = stores[collection_name].search(embeddings[0], limit=1)
                
                health_status["collections"][collection_name] = {
                    "status": "✅ Healthy",
                    "test_search": f"Found {len(test_results)} results"
                }
            except Exception as e:
                health_status["collections"][collection_name] = {
                    "status": f"❌ Error: {str(e)}"
                }
        else:
            health_status["collections"][collection_name] = {
                "status": "❌ Not connected"
            }
    
    return health_status

async def main():
    """Main server function."""
    logger.info("🚀 Starting Qdrant MCP Server (CodeRankEmbed 768-dim)")
    logger.info(f"📊 Collections: {list(COLLECTIONS.keys())}")
    logger.info(f"🤖 Embedding Model: {EMBEDDING_MODEL}")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="qdrant-coderank-768",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())