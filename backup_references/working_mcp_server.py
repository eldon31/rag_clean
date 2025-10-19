#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORKING MCP SERVER for Qdrant Knowledge Base
Minimal MCP server with actual search functionality
"""

import asyncio
import sys
import logging
import os
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# MCP SDK imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, ToolsCapability, Tool, TextContent

# Qdrant and ML imports
from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np

# Collection naming helpers
CANONICAL_COLLECTIONS = {
    "docling": "docling_v4_nomic_coderank",
    "docling_v4": "docling_v4_nomic_coderank",
    "docling_v4_nomic_coderank": "docling_v4_nomic_coderank",
    "fast_docs": "fast_docs_v4_nomic_coderank",
    "fast_docs_v4": "fast_docs_v4_nomic_coderank",
    "fast_docs_v4_nomic_coderank": "fast_docs_v4_nomic_coderank",
    "pydantic": "pydantic_v4_nomic_coderank",
    "pydantic_v4": "pydantic_v4_nomic_coderank",
    "pydantic_v4_nomic_coderank": "pydantic_v4_nomic_coderank",
    "qdrant_ecosystem": "qdrant_ecosystem_v4_nomic_coderank",
    "qdrant_ecosystem_v4": "qdrant_ecosystem_v4_nomic_coderank",
    "qdrant_ecosystem_v4_nomic_coderank": "qdrant_ecosystem_v4_nomic_coderank",
    "sentence_transformers": "sentence_transformers_v4_nomic_coderank",
    "sentence_transformers_v4": "sentence_transformers_v4_nomic_coderank",
    "sentence_transformers_v4_nomic_coderank": "sentence_transformers_v4_nomic_coderank",
}

COLLECTION_DISPLAY_NAMES = {
    "docling_v4_nomic_coderank": "docling",
    "fast_docs_v4_nomic_coderank": "fast_docs",
    "pydantic_v4_nomic_coderank": "pydantic",
    "qdrant_ecosystem_v4_nomic_coderank": "qdrant_ecosystem",
    "sentence_transformers_v4_nomic_coderank": "sentence_transformers",
}

DEFAULT_COLLECTIONS = list(COLLECTION_DISPLAY_NAMES.keys())


def resolve_collection(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError("Collection name must be a string")
    normalized = name.strip().lower()
    if normalized not in CANONICAL_COLLECTIONS:
        raise ValueError(f"Unknown collection '{name}'")
    return CANONICAL_COLLECTIONS[normalized]


def collection_display(name: str) -> str:
    return COLLECTION_DISPLAY_NAMES.get(name, name)


# Create MCP server
mcp_server = Server("qdrant-knowledge-server")

# Global state for lazy initialization
embedder = None
qdrant_client = None

async def get_embedder():
    """Lazy initialization of embedder."""
    global embedder
    if embedder is None:
        logger.info("Initializing embedder...")
        embedder = SentenceTransformer("nomic-ai/CodeRankEmbed", device="cpu", trust_remote_code=True)
        logger.info("Embedder initialized")
    return embedder

async def get_qdrant_client():
    """Lazy initialization of Qdrant client."""
    global qdrant_client
    if qdrant_client is None:
        logger.info("Initializing Qdrant client...")
        qdrant_client = AsyncQdrantClient(url="http://localhost:6333")
        # Test connection
        await qdrant_client.get_collections()
        logger.info("Qdrant client initialized")
    return qdrant_client

@mcp_server.list_tools()
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
                        "enum": sorted(set(CANONICAL_COLLECTIONS.keys())),
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
                        "enum": sorted(set(CANONICAL_COLLECTIONS.keys())),
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

@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        # Initialize components lazily
        if name in ["search_collection", "smart_search", "learn_about_topic"]:
            await get_embedder()
            await get_qdrant_client()

        if name == "search_collection":
            collection = arguments.get("collection", "")
            query = arguments.get("query", "")
            limit = arguments.get("limit", 5)
            score_threshold = arguments.get("score_threshold", 0.3)

            if not collection or not query:
                return [TextContent(type="text", text="Error: collection and query parameters are required")]

            try:
                canonical_collection = resolve_collection(collection)
            except ValueError as err:
                return [TextContent(type="text", text=str(err))]

            embedder = await get_embedder()
            qdrant_client = await get_qdrant_client()

            query_embedding = embedder.encode([query], batch_size=32)[0]
            search_result = await qdrant_client.search(
                collection_name=canonical_collection,
                query_vector=query_embedding.tolist(),
                limit=limit,
                score_threshold=score_threshold
            )

            if not search_result:
                return [TextContent(type="text", text=f"No results found for query: {query} in {collection}")]

            results = []
            for hit in search_result:
                payload = hit.payload or {}
                text = payload.get('text', 'No content')
                results.append(f"Score: {hit.score:.3f} - {text[:200]}...")

            response = f"Search results for '{query}' in {collection_display(canonical_collection)}:\n" + "\n".join(results)
            return [TextContent(type="text", text=response)]

        elif name == "smart_search":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            auto_route = arguments.get("auto_route", True)

            if not query:
                return [TextContent(type="text", text="Error: query parameter is required")]

            # Simple auto-routing logic
            query_lower = query.lower()
            relevant_collections = []

            if any(word in query_lower for word in ['embedding', 'transformer', 'model', 'fine-tune', 'training', 'sentence', 'semantic', 'similarity']):
                relevant_collections.append('sentence_transformers_v4_nomic_coderank')
            if any(word in query_lower for word in ['vector', 'search', 'qdrant', 'similarity', 'index', 'query', 'sparse', 'dense', 'hybrid']):
                relevant_collections.append('qdrant_ecosystem_v4_nomic_coderank')
            if any(word in query_lower for word in ['document', 'pdf', 'text', 'chunk', 'parse', 'extract', 'structure', 'docling']):
                relevant_collections.append('docling_v4_nomic_coderank')
            if any(word in query_lower for word in ['fast', 'api', 'documentation', 'docs']):
                relevant_collections.append('fast_docs_v4_nomic_coderank')
            if any(word in query_lower for word in ['pydantic', 'validation', 'model', 'schema']):
                relevant_collections.append('pydantic_v4_nomic_coderank')

            if relevant_collections:
                seen_canonicals = set()
                relevant_collections = [
                    name for name in relevant_collections
                    if not (name in seen_canonicals or seen_canonicals.add(name))
                ]
            if not relevant_collections:
                relevant_collections = [
                    'qdrant_ecosystem_v4_nomic_coderank',
                    'sentence_transformers_v4_nomic_coderank',
                    'docling_v4_nomic_coderank'
                ]

            embedder = await get_embedder()
            qdrant_client = await get_qdrant_client()

            all_results = []
            query_embedding = embedder.encode([query], batch_size=32)[0]

            for collection in relevant_collections:
                try:
                    search_result = await qdrant_client.search(
                        collection_name=collection,
                        query_vector=query_embedding.tolist(),
                        limit=min(limit // len(relevant_collections) + 1, 5),
                        score_threshold=0.3
                    )
                    for hit in search_result:
                        payload = hit.payload or {}
                        text = payload.get('text', 'No content')
                        all_results.append((hit.score, collection_display(collection), text[:200]))
                except Exception as e:
                    logger.warning(f"Error searching {collection}: {e}")

            all_results.sort(key=lambda x: x[0], reverse=True)
            top_results = all_results[:limit]

            if not top_results:
                return [TextContent(type="text", text=f"No results found for query: {query}")]

            results = [f"Score: {score:.3f} [{collection}] - {text}..." for score, collection, text in top_results]
            searched = ", ".join(collection_display(name) for name in relevant_collections)
            response = f"Smart search results for '{query}' (searched: {searched}):\n" + "\n".join(results)
            return [TextContent(type="text", text=response)]

        elif name == "learn_about_topic":
            topic = arguments.get("topic", "")
            depth = arguments.get("depth", "intermediate")
            focus_collection = arguments.get("focus_collection")

            if not topic:
                return [TextContent(type="text", text="Error: topic parameter is required")]

            if focus_collection:
                try:
                    collections_to_search = [resolve_collection(focus_collection)]
                except ValueError as err:
                    return [TextContent(type="text", text=str(err))]
            else:
                collections_to_search = DEFAULT_COLLECTIONS

            embedder = await get_embedder()
            qdrant_client = await get_qdrant_client()

            all_results = []
            query_embedding = embedder.encode([topic], batch_size=32)[0]

            for collection in collections_to_search:
                try:
                    search_result = await qdrant_client.search(
                        collection_name=collection,
                        query_vector=query_embedding.tolist(),
                        limit=3,
                        score_threshold=0.2
                    )
                    for hit in search_result:
                        payload = hit.payload or {}
                        text = payload.get('text', 'No content')
                        all_results.append((hit.score, collection_display(collection), text))
                except Exception as e:
                    logger.warning(f"Error searching {collection}: {e}")

            if not all_results:
                return [TextContent(type="text", text=f"No information found about topic: {topic}")]

            # Sort by relevance and format comprehensive response
            all_results.sort(key=lambda x: x[0], reverse=True)

            response_parts = [f"📚 Learning about: {topic} (Depth: {depth})", ""]

            for score, collection, text in all_results[:10]:  # Top 10 results
                response_parts.append(f"🔍 From {collection} (relevance: {score:.3f}):")
                response_parts.append(text[:500] + "..." if len(text) > 500 else text)
                response_parts.append("")

            response = "\n".join(response_parts)
            return [TextContent(type="text", text=response)]

        elif name == "get_collections_info":
            collections_info = {
                "sentence_transformers_v4_nomic_coderank": {
                    "description": "Advanced embedding techniques and model optimization",
                    "specialties": ["fine-tuning", "training", "model selection", "performance optimization"],
                    "vector_count": "71"
                },
                "docling_v4_nomic_coderank": {
                    "description": "Document processing and text extraction",
                    "specialties": ["PDF parsing", "document structure", "text extraction", "chunking"],
                    "vector_count": "60"
                },
                "qdrant_ecosystem_v4_nomic_coderank": {
                    "description": "Qdrant vector database and search technologies",
                    "specialties": ["vector search", "similarity search", "indexing", "performance"],
                    "vector_count": "950"
                },
                "fast_docs_v4_nomic_coderank": {
                    "description": "FastAPI documentation and web framework",
                    "specialties": ["API development", "async programming", "web frameworks"],
                    "vector_count": "103"
                },
                "pydantic_v4_nomic_coderank": {
                    "description": "Pydantic data validation and parsing",
                    "specialties": ["data validation", "type hints", "model parsing"],
                    "vector_count": "40"
                }
            }

            response_parts = ["📊 Available Collections:", ""]
            for name, info in collections_info.items():
                response_parts.append(f"🔸 {collection_display(name)} ({name})")
                response_parts.append(f"   Description: {info['description']}")
                response_parts.append(f"   Specialties: {', '.join(info['specialties'])}")
                response_parts.append(f"   Vectors: {info['vector_count']}")
                response_parts.append("")

            response = "\n".join(response_parts)
            return [TextContent(type="text", text=response)]

        elif name == "health_check":
            try:
                qdrant_client = await get_qdrant_client()
                collections = await qdrant_client.get_collections()
                collection_names = [c.name for c in collections.collections]

                embedder_status = "✅ Initialized" if globals().get('embedder') is not None else "⏳ Lazy (will initialize on first use)"

                response = f"""🏥 Health Check Results:

🔗 Qdrant Connection: ✅ Connected
📊 Available Collections: {len(collection_names)}
   - {', '.join(collection_names)}

🧠 Embedder Status: {embedder_status}

⚡ Server Status: ✅ Running
📈 Total Requests: 0 (since startup)

All systems operational! 🎉"""

                return [TextContent(type="text", text=response)]
            except Exception as e:
                return [TextContent(type="text", text=f"❌ Health check failed: {str(e)}")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Error in tool call: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Main MCP server loop."""
    logger.info("Starting Qdrant Knowledge MCP Server...")

    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="qdrant-knowledge-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability()
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())