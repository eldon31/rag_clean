"""
FastMCP-based Qdrant server with nomic-ai/nomic-embed-code embeddings.
Supports viator_api, fast_docs, pydantic_docs, and inngest_ecosystem collections.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastmcp import FastMCP

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-fastmcp")

# Initialize FastMCP server
mcp = FastMCP("qdrant-codes")

# Global state
embedder: Optional[SentenceTransformerEmbedder] = None
stores: dict[str, QdrantStore] = {}

EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
VECTOR_SIZE = 3584
COLLECTIONS = ["viator_api", "fast_docs", "pydantic_docs", "inngest_ecosystem"]
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))


def get_embedder():
    """Lazy-load and return the embedder."""
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
    return embedder


def get_store(collection: str) -> QdrantStore:
    """Lazy-load and return a Qdrant store."""
    global stores
    if collection not in stores:
        logger.info(f"Connecting to Qdrant collection: {collection}")
        config = QdrantStoreConfig(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            collection_name=collection,
            vector_size=VECTOR_SIZE,
            enable_quantization=False,  # Disable quantization for search compatibility
            prefer_grpc=False
        )
        stores[collection] = QdrantStore(config)
        logger.info(f"Connected to collection: {collection}")
    return stores[collection]


@mcp.tool()
async def qdrant_search_viator_api(query: str, limit: int = 5, score_threshold: float = 0.7, subdir: Optional[str] = None) -> str:
    """
    Search the viator_api collection (Viator Partner API documentation) using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score 0-1 (default: 0.7)
        subdir: Filter by subdirectory (e.g., 'converted')
    
    Returns:
        Formatted search results with scores and metadata
    """
    return await _search_collection("viator_api", query, limit, score_threshold, subdir)


@mcp.tool()
async def qdrant_search_fast_docs(query: str, limit: int = 5, score_threshold: float = 0.7, subdir: Optional[str] = None) -> str:
    """
    Search the fast_docs collection (FastAPI, FastMCP, and Python SDK documentation) using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score 0-1 (default: 0.7)
        subdir: Filter by subdirectory (e.g., 'fastapi', 'fastmcp', 'python_sdk')
    
    Returns:
        Formatted search results with scores and metadata
    """
    return await _search_collection("fast_docs", query, limit, score_threshold, subdir)


@mcp.tool()
async def qdrant_search_pydantic_docs(query: str, limit: int = 5, score_threshold: float = 0.7) -> str:
    """
    Search the pydantic_docs collection (Pydantic validation library documentation) using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score 0-1 (default: 0.7)
    
    Returns:
        Formatted search results with scores and metadata
    """
    return await _search_collection("pydantic_docs", query, limit, score_threshold)


@mcp.tool()
async def qdrant_search_inngest_ecosystem(query: str, limit: int = 5, score_threshold: float = 0.7, subdir: Optional[str] = None) -> str:
    """
    Search the inngest_ecosystem collection (Inngest workflow platform and agent kit documentation) using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score 0-1 (default: 0.7)
        subdir: Filter by subdirectory (e.g., 'inngest_overall', 'agent_kit', 'agent_kit_github', 'inngest', 'inngest_js', 'inngest_py')
    
    Returns:
        Formatted search results with scores and metadata
    """
    return await _search_collection("inngest_ecosystem", query, limit, score_threshold, subdir)


@mcp.tool()
async def qdrant_get_stats() -> str:
    """
    Get statistics for both Qdrant collections (vector counts, index status, etc.).
    
    Returns:
        Formatted statistics for all collections
    """
    stats_lines = ["Qdrant Collection Statistics:\n"]
    
    for collection in COLLECTIONS:
        store = get_store(collection)
        stats = store.get_stats()
        
        stats_lines.append(f"\n{collection}:")
        stats_lines.append(f"  Points: {stats.get('points_count', 0)}")
        stats_lines.append(f"  Indexed: {stats.get('indexed_vectors_count', 0)}")
        stats_lines.append(f"  Status: {stats.get('status', 'unknown')}")
        stats_lines.append(f"  Quantization: {stats.get('quantization_enabled', False)}")
    
    return "\n".join(stats_lines)


def _extract_subdir(collection: str, result: Dict[str, Any]) -> Optional[str]:
    """Extract subdirectory from search result based on collection type."""
    result_id = result.get("id", "")
    metadata = result.get("metadata", {})
    
    if collection == "viator_api":
        # Subdir is in metadata.source path: "output\viator_api\{subdir}\..."
        source = metadata.get("source", "")
        if source:
            parts = source.split(os.sep)
            if len(parts) >= 3:
                return parts[2]  # output/viator_api/subdir/...
    
    elif collection in ["fast_docs", "inngest_ecosystem"]:
        # Subdir is in id: "{collection}:{subdir}:{file}:chunk:{N}"
        if isinstance(result_id, str):
            parts = result_id.split(":")
            if len(parts) >= 2:
                return parts[1]  # collection:subdir:...
    
    # pydantic_docs has no subdirs
    return None


async def _search_collection(collection: str, query: str, limit: int, score_threshold: float, subdir: Optional[str] = None) -> str:
    """Internal search implementation with subdirectory filtering."""
    if not query:
        return "Error: query is required"
    
    logger.info(f"Searching {collection} for: {query[:50]}... with subdir: {subdir}")
    
    # Generate query embedding
    emb = get_embedder()
    embedding = await emb.embed_documents([query])
    query_vector = embedding[0]
    
    # Search Qdrant (without filters, we'll filter client-side)
    store = get_store(collection)
    results = store.search(
        query_embedding=query_vector,
        limit=limit * 3,  # Get more results to filter
        score_threshold=score_threshold
    )
    
    # Filter by subdirectory if specified
    if subdir:
        filtered_results = []
        for result in results:
            result_subdir = _extract_subdir(collection, result)
            if result_subdir == subdir:
                filtered_results.append(result)
        results = filtered_results[:limit]  # Limit after filtering
    else:
        results = results[:limit]
    
    # Format results
    if not results:
        filter_msg = f" in subdir '{subdir}'" if subdir else ""
        return f"No results found in {collection}{filter_msg} for query: {query}"
    
    output_lines = [f"Found {len(results)} results in {collection}:"]
    if subdir:
        output_lines[0] += f" (filtered by subdir: {subdir})"
    output_lines[0] += "\n"
    
    for idx, result in enumerate(results, 1):
        score = result.get("score", 0)
        content = result.get("content", "")
        metadata = result.get("metadata", {})
        
        output_lines.append(f"\n--- Result {idx} (Score: {score:.3f}) ---")
        output_lines.append(f"Content: {content[:500]}..." if len(content) > 500 else f"Content: {content}")
        
        if metadata:
            output_lines.append(f"Metadata:")
            for key, value in metadata.items():
                if key not in ["content", "embedding"]:
                    output_lines.append(f"  {key}: {value}")
    
    return "\n".join(output_lines)


if __name__ == "__main__":
    logger.info("Starting Qdrant FastMCP Server")
    logger.info(f"Collections: {', '.join(COLLECTIONS)}")
    logger.info(f"Embedding model: {EMBEDDING_MODEL}")
    logger.info(f"Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
    
    mcp.run()
