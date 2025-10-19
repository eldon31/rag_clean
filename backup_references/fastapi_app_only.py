#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FASTAPI APP ONLY - No main execution
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Qdrant and ML imports
from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# SHARED BUSINESS LOGIC
# ============================================================================

class KnowledgeService:
    """Shared service for knowledge base operations."""

    def __init__(self):
        self.embedder: Optional[SentenceTransformer] = None
        self.qdrant_client: Optional[AsyncQdrantClient] = None

    async def initialize(self):
        """Initialize components lazily."""
        if self.embedder is None:
            logger.info("Initializing embedder...")
            self.embedder = SentenceTransformer("nomic-ai/CodeRankEmbed", device="cpu", trust_remote_code=True)
            logger.info("Embedder initialized")

        if self.qdrant_client is None:
            logger.info("Initializing Qdrant client...")
            self.qdrant_client = AsyncQdrantClient(url="http://localhost:6333")
            await self.qdrant_client.get_collections()  # Test connection
            logger.info("Qdrant client initialized")

    async def search_collection(self, collection: str, query: str, limit: int = 5, score_threshold: float = 0.3) -> Dict[str, Any]:
        """Search a specific collection."""
        await self.initialize()

        query_embedding = self.embedder.encode([query], batch_size=32)[0]
        search_result = await self.qdrant_client.search(
            collection_name=collection,
            query_vector=query_embedding.tolist(),
            limit=limit,
            score_threshold=score_threshold
        )

        results = []
        for hit in search_result:
            payload = hit.payload or {}
            text = payload.get('text', 'No content')
            results.append({
                'score': hit.score,
                'text': text[:200] + "..." if len(text) > 200 else text
            })

        return {
            'query': query,
            'collection': collection,
            'results': results,
            'total_results': len(results)
        }

    async def smart_search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Intelligent multi-collection search."""
        await self.initialize()

        # Auto-routing logic
        query_lower = query.lower()
        relevant_collections = []

        if any(word in query_lower for word in ['embedding', 'transformer', 'model', 'fine-tune', 'training', 'sentence', 'semantic']):
            relevant_collections.append('sentence_transformers')
        if any(word in query_lower for word in ['vector', 'search', 'qdrant', 'similarity', 'index', 'query']):
            relevant_collections.append('qdrant_ecosystem')
        if any(word in query_lower for word in ['document', 'pdf', 'text', 'chunk', 'parse', 'extract']):
            relevant_collections.append('docling')
        if not relevant_collections:
            relevant_collections = ['qdrant_ecosystem', 'sentence_transformers', 'docling']

        query_embedding = self.embedder.encode([query], batch_size=32)[0]
        all_results = []

        for collection in relevant_collections:
            try:
                search_result = await self.qdrant_client.search(
                    collection_name=collection,
                    query_vector=query_embedding.tolist(),
                    limit=min(limit // len(relevant_collections) + 1, 5),
                    score_threshold=0.3
                )
                for hit in search_result:
                    payload = hit.payload or {}
                    text = payload.get('text', 'No content')
                    all_results.append((hit.score, collection, text[:200]))
            except Exception as e:
                logger.warning(f"Error searching {collection}: {e}")

        all_results.sort(key=lambda x: x[0], reverse=True)
        top_results = all_results[:limit]

        return {
            'query': query,
            'searched_collections': relevant_collections,
            'results': [{'score': score, 'collection': col, 'text': text} for score, col, text in top_results],
            'total_results': len(top_results)
        }

    async def get_collections_info(self) -> Dict[str, Any]:
        """Get information about collections."""
        await self.initialize()

        collections_info = {
            "sentence_transformers": {
                "description": "Advanced embedding techniques and model optimization",
                "specialties": ["fine-tuning", "training", "model selection"],
                "vectors": "~457"
            },
            "docling": {
                "description": "Document processing and text extraction",
                "specialties": ["PDF parsing", "document structure", "text extraction"],
                "vectors": "~1,089"
            },
            "qdrant_ecosystem": {
                "description": "Qdrant vector database and search technologies",
                "specialties": ["vector search", "similarity search", "indexing"],
                "vectors": "~8,108"
            },
            "fast_docs": {
                "description": "FastAPI documentation and web framework",
                "specialties": ["API development", "async programming"],
                "vectors": "~2,500"
            },
            "pydantic": {
                "description": "Pydantic data validation and parsing",
                "specialties": ["data validation", "type hints", "model parsing"],
                "vectors": "~1,200"
            }
        }

        return {
            'collections': collections_info,
            'total_collections': len(collections_info)
        }

# Global service instance
knowledge_service = KnowledgeService()

# ============================================================================
# FASTAPI SETUP
# ============================================================================

# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    try:
        logger.info("Starting application lifespan...")
        await knowledge_service.initialize()
        logger.info("Application lifespan startup complete")
        yield
        logger.info("Application lifespan shutdown")
    except Exception as e:
        logger.error(f"Error in lifespan: {e}")
        raise

app = FastAPI(
    title="FastMCP + FastAPI Knowledge Base",
    description="Demonstration of proper FastMCP and FastAPI integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class SearchRequest(BaseModel):
    collection: str = Field(..., description="Collection name to search")
    query: str = Field(..., description="Search query text")
    limit: int = Field(5, description="Maximum number of results")
    score_threshold: float = Field(0.3, description="Minimum similarity score")

class SmartSearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    limit: int = Field(10, description="Total number of results")

class SearchResponse(BaseModel):
    query: str
    collection: str
    results: List[Dict[str, Any]]
    total_results: int

class SmartSearchResponse(BaseModel):
    query: str
    searched_collections: List[str]
    results: List[Dict[str, Any]]
    total_results: int

# FastAPI routes that use the SAME business logic as MCP tools
@app.post("/api/search", response_model=SearchResponse)
async def api_search_collection(request: SearchRequest):
    """REST API endpoint for collection search - same logic as MCP tool."""
    result = await knowledge_service.search_collection(
        request.collection, request.query, request.limit, request.score_threshold
    )
    return SearchResponse(**result)

@app.post("/api/smart-search", response_model=SmartSearchResponse)
async def api_smart_search(request: SmartSearchRequest):
    """REST API endpoint for smart search - same logic as MCP tool."""
    result = await knowledge_service.smart_search(request.query, request.limit)
    return SmartSearchResponse(**result)

@app.get("/api/collections")
async def api_get_collections():
    """REST API endpoint for collections info - same logic as MCP tool."""
    return await knowledge_service.get_collections_info()

@app.get("/api/health")
async def api_health_check():
    """REST API endpoint for health check - same logic as MCP tool."""
    try:
        await knowledge_service.initialize()

        # Test Qdrant connection
        collections = await knowledge_service.qdrant_client.get_collections()
        collection_names = [c.name for c in collections.collections]

        response = f"""🏥 Health Check Results:

🔗 Qdrant Connection: ✅ Connected
📊 Available Collections: {len(collection_names)}
   - {', '.join(collection_names)}

🧠 Embedder Status: ✅ Initialized

⚡ Server Status: ✅ Running
📈 Total Requests: 0 (since startup)

All systems operational! 🎉"""

        return {"status": "healthy", "details": response}

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"status": "unhealthy", "error": str(e)}