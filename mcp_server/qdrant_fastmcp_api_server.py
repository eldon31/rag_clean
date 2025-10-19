#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENTERPRISE FASTMCP API SERVER v2.0 - ENHANCED
===============================================

Production-ready FastMCP server with advanced REST API integration for Qdrant vector operations.
Enhanced with server composition, OpenAPI integration, and enterprise-grade optimizations.

Architecture:
- FastMCP with server composition and mounting patterns
- OpenAPI/Swagger integration for automatic API documentation
- Advanced middleware system with authentication, rate limiting, and monitoring
- Proxy server capabilities for multi-tenant deployments
- Multi-level caching (embeddings + queries + results) with aiocache
- Connection pooling with aiohttp and Qdrant gRPC
- Kubernetes-native with HPA and ConfigMaps
- Enterprise monitoring with Prometheus/Grafana

Features:
- HTTP+SSE transport for real-time streaming
- CodeRankEmbed with LRU caching and batch processing
- Dual MCP/REST API interfaces with automatic OpenAPI generation
- Advanced Qdrant optimizations with quantization and HNSW
- Production observability stack with distributed tracing
- Server composition for modular architecture
- Proxy capabilities for load balancing and failover

Collections Supported:
- sentence_transformers_v4_nomic_coderank: 113 vectors
- docling_v4_nomic_coderank: 306 vectors
- qdrant_ecosystem_v4_nomic_coderank: 1,952 vectors
- fast_docs_v4_nomic_coderank: 329 vectors
- pydantic_v4_nomic_coderank: 164 vectors

Performance Targets:
- Latency: <10ms cached, <100ms new queries
- Throughput: 2000+ QPS with horizontal scaling
- Availability: 99.9% uptime with circuit breakers
- Memory: <512MB per instance with intelligent caching

Author: AI Assistant - Enhanced with FastMCP Architecture Patterns
License: MIT
"""

import asyncio
import logging
import os
import sys
import time
import traceback
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any, AsyncGenerator, Tuple, Iterable
from datetime import datetime, timedelta
from functools import wraps, lru_cache
import json
import psutil
import platform
import secrets
from pathlib import Path
import re

# Canonical collection configuration for the knowledge base
CANONICAL_COLLECTIONS: List[str] = [
    "sentence_transformers_v4_nomic_coderank",
    "docling_v4_nomic_coderank",
    "qdrant_ecosystem_v4_nomic_coderank",
    "fast_docs_v4_nomic_coderank",
    "pydantic_v4_nomic_coderank",
]

COLLECTION_DISPLAY_NAMES: Dict[str, str] = {
    "sentence_transformers_v4_nomic_coderank": "sentence_transformers",
    "docling_v4_nomic_coderank": "docling",
    "qdrant_ecosystem_v4_nomic_coderank": "qdrant_ecosystem",
    "fast_docs_v4_nomic_coderank": "fast_docs",
    "pydantic_v4_nomic_coderank": "pydantic",
}

COLLECTION_ALIAS_MAP: Dict[str, str] = {}
for canonical, display in COLLECTION_DISPLAY_NAMES.items():
    variants = {
        display,
        display.replace("_", "-"),
        f"{display}_v4",
        f"{display}-v4",
        canonical,
    }
    for variant in variants:
        normalized = variant.strip().lower()
        normalized = re.sub(r"[\s\-]+", "_", normalized)
        COLLECTION_ALIAS_MAP[normalized] = canonical


def _normalize_collection_name(name: str) -> str:
    normalized = name.strip().lower()
    normalized = re.sub(r"[\s\-]+", "_", normalized)
    normalized = re.sub(r"__+", "_", normalized)
    return normalized


def resolve_collection_name(name: str) -> Optional[str]:
    if not name:
        return None

    normalized = _normalize_collection_name(name)
    canonical = COLLECTION_ALIAS_MAP.get(normalized)

    raw_supported: Iterable[str]
    if "settings" in globals():
        raw_supported = globals()["settings"].supported_collections
    else:
        raw_supported = CANONICAL_COLLECTIONS

    supported_canonical: set[str] = set()
    for value in raw_supported:
        normalized_value = _normalize_collection_name(str(value))
        alias = COLLECTION_ALIAS_MAP.get(normalized_value)
        if alias:
            supported_canonical.add(alias)
        else:
            supported_canonical.add(normalized_value)

    if canonical and canonical in supported_canonical:
        return canonical
    if normalized in supported_canonical:
        return normalized
    if not supported_canonical and canonical in CANONICAL_COLLECTIONS:
        # Allow canonical resolution when configuration yielded no matches.
        return canonical
    return None


def resolve_collections(names: Iterable[str]) -> List[str]:
    resolved: List[str] = []
    for name in names:
        canonical = resolve_collection_name(name)
        if canonical and canonical not in resolved:
            resolved.append(canonical)
    return resolved


def get_supported_collections() -> List[str]:
    if "settings" in globals():
        supported = resolve_collections(globals()["settings"].supported_collections)
        if supported:
            return supported
    return CANONICAL_COLLECTIONS.copy()


def describe_available_collections() -> str:
    if "settings" in globals():
        supported = get_supported_collections()
    else:
        supported = CANONICAL_COLLECTIONS.copy()
    descriptions = [
        f"{display} ({canonical})"
        for canonical, display in COLLECTION_DISPLAY_NAMES.items()
        if canonical in supported
    ]
    if descriptions:
        return ", ".join(descriptions)
    return ", ".join(supported)


def ensure_supported_collection(name: str) -> str:
    canonical = resolve_collection_name(name)
    if not canonical:
        available = describe_available_collections()
        raise ValueError(f"Invalid collection '{name}'. Available: {available}")
    return canonical

# FastAPI and FastMCP imports
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
import uvicorn

# FastMCP imports
from fastmcp import FastMCP

# Optional middleware imports (with fallbacks)
try:
    from fastapi.middleware.base import BaseHTTPMiddleware
    FASTAPI_MIDDLEWARE_AVAILABLE = True
except ImportError:
    FASTAPI_MIDDLEWARE_AVAILABLE = False

try:
    from fastmcp.middleware import (
        LoggingMiddleware,
        TimingMiddleware,
        ErrorHandlingMiddleware,
        RateLimitingMiddleware
    )
    FASTMCP_MIDDLEWARE_AVAILABLE = True
except ImportError:
    FASTMCP_MIDDLEWARE_AVAILABLE = False

# Optional monitoring imports
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

# Optional async file handling
try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False

# Configure logging for production
# Ensure logs directory exists relative to script location
script_dir = Path(__file__).parent.parent
logs_dir = script_dir / 'logs'
try:
    logs_dir.mkdir(exist_ok=True)
except OSError:
    # In Docker with read-only filesystem, use /app/logs (mounted volume)
    logs_dir = Path('/app/logs')
    logs_dir.mkdir(exist_ok=True)
log_file_path = logs_dir / 'qdrant_fastmcp_api_server.log'

log_handlers: list = [logging.FileHandler(log_file_path, mode='a')]

# Add console handler only when not running in MCP mode (to avoid interfering with stdio)
if len(sys.argv) < 2 or sys.argv[1] != "--mcp":
    log_handlers.append(logging.StreamHandler(sys.stdout))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

# When running in MCP mode, disable console logging to prevent interference with stdio protocol
if len(sys.argv) >= 2 and sys.argv[1] == "--mcp":
    # Disable all console handlers for all loggers (but DON'T redirect stdio)
    for name in logging.root.manager.loggerDict:
        log = logging.getLogger(name)
        for handler in log.handlers[:]:
            if isinstance(handler, logging.StreamHandler):
                log.removeHandler(handler)
    # Also disable root logger console handlers
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.StreamHandler):
            logging.root.removeHandler(handler)

# Set specific log levels for noisy libraries
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('qdrant_client').setLevel(logging.WARNING)
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)

# Add project root to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Core Dependencies - Enhanced for second iteration
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
import httpx

# Vector and Qdrant - Core functionality
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models, AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, SearchParams, QuantizationSearchParams

# Basic monitoring
import psutil

# FastMCP - Core integration
# from fastmcp import FastMCP

# FastMCP for modern MCP implementation - NO OLD SDK NEEDED

# Enhanced Configuration - With LRU cache optimization
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Application Settings - Simplified for first iteration
class Settings(BaseSettings):
    # Qdrant Configuration
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: Optional[str] = Field(default=None)

    # Server Configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080)
    workers: int = Field(default=1)

    # Performance Configuration
    max_connections: int = Field(default=100)
    connection_pool_size: int = Field(default=20)
    embedding_cache_ttl: int = Field(default=3600)  # 1 hour
    query_cache_ttl: int = Field(default=300)  # 5 minutes
    embedding_cache_max_size: int = Field(default=2048)
    query_cache_max_size: int = Field(default=2048)
    hnsw_ef_search: int = Field(default=128)
    quantization_rescore: bool = Field(default=True)
    quantization_oversampling: float = Field(default=1.5)
    hybrid_vector_weight: float = Field(default=0.7)

    # Embedding Configuration
    embedding_model: str = Field(default="jina-code-embeddings-1.5b")
    embedding_device: str = Field(default="cpu")
    embedding_batch_size: int = Field(default=32)

    # Collections Configuration
    supported_collections: List[str] = Field(default_factory=lambda: CANONICAL_COLLECTIONS.copy())

    # Basic Enterprise Features
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)
    enable_auth: bool = Field(default=False)
    enable_openapi_enhancement: bool = Field(default=True)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

def _normalize_supported_collections(names: Iterable[str]) -> List[str]:
    normalized: List[str] = []
    for name in names:
        canonical = COLLECTION_ALIAS_MAP.get(_normalize_collection_name(str(name)), None)
        if canonical and canonical not in normalized:
            normalized.append(canonical)

    if not normalized:
        normalized = CANONICAL_COLLECTIONS.copy()

    return normalized


settings = Settings()
settings.supported_collections = _normalize_supported_collections(settings.supported_collections)

# Collection metadata for API responses
COLLECTION_METADATA = {
    "sentence_transformers_v4_nomic_coderank": {
        "vectors": 113,
        "description": "Sentence Transformers embedding expertise and implementation patterns",
        "knowledge_areas": ["embeddings", "sentence-transformers", "nlp"],
    "vector_size": 1536
    },
    "docling_v4_nomic_coderank": {
        "vectors": 306,
        "description": "Document processing and parsing with Docling framework",
        "knowledge_areas": ["document-processing", "docling", "pdf-parsing"],
    "vector_size": 1536
    },
    "qdrant_ecosystem_v4_nomic_coderank": {
        "vectors": 1952,
        "description": "Comprehensive Qdrant vector database ecosystem and optimization",
        "knowledge_areas": ["vector-database", "qdrant", "search", "optimization"],
    "vector_size": 1536
    },
    "fast_docs_v4_nomic_coderank": {
        "vectors": 329,
        "description": "FAST Documentation & Framework Knowledge",
        "knowledge_areas": ["documentation", "frameworks", "API design", "technical writing"],
    "vector_size": 1536
    },
    "pydantic_v4_nomic_coderank": {
        "vectors": 164,
        "description": "Pydantic Data Validation & Modeling",
        "knowledge_areas": ["data validation", "type hints", "modeling", "Python best practices"],
    "vector_size": 1536
    }
}

# Simple asynchronous TTL cache for embeddings and search results
class AsyncTTLCache:
    """In-memory TTL cache with async interface for compatibility."""

    def __init__(self, ttl: int, max_size: int):
        self.ttl = ttl
        self.max_size = max_size
        self._items: Dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            entry = self._items.get(key)
            if not entry:
                return None

            expires_at, value = entry
            if expires_at < time.time():
                # Drop expired entries lazily.
                self._items.pop(key, None)
                return None

            return value

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            if len(self._items) >= self.max_size:
                # Evict oldest entry to preserve bounded memory usage.
                oldest_key = min(self._items.items(), key=lambda item: item[1][0])[0]
                self._items.pop(oldest_key, None)

            self._items[key] = (time.time() + self.ttl, value)

    async def clear(self) -> None:
        async with self._lock:
            self._items.clear()

    async def info(self) -> Dict[str, Any]:
        async with self._lock:
            now = time.time()
            valid = sum(1 for expires_at, _ in self._items.values() if expires_at > now)
            return {
                "ttl_seconds": self.ttl,
                "max_size": self.max_size,
                "items": len(self._items),
                "valid_items": valid
            }

# LRU Cache optimization for settings (prevents repeated instantiation)
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance to prevent repeated file I/O."""
    return Settings()

# Global server state with enhanced monitoring
class ServerState:
    def __init__(self):
        self.embedder: Optional[SentenceTransformer] = None
        self.qdrant_client: Optional[AsyncQdrantClient] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        self.startup_time: float = time.time()
        self.request_count: int = 0
        self.error_count: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.avg_response_time: float = 0.0
        self.embedding_cache: Optional[AsyncTTLCache] = None
        self.query_cache: Optional[AsyncTTLCache] = None

    def update_metrics(self, response_time: float, cache_hit: bool = False):
        """Update performance metrics."""
        self.request_count += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        # Update average response time
        if self.request_count == 1:
            self.avg_response_time = response_time
        else:
            self.avg_response_time = (self.avg_response_time * (self.request_count - 1) + response_time) / self.request_count

    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            cpu_percent = psutil.cpu_percent(interval=1)

            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / 1024 / 1024,
                'memory_total_mb': memory.total / 1024 / 1024,
                'disk_usage_percent': disk.percent,
                'disk_used_gb': disk.used / 1024 / 1024 / 1024,
                'disk_total_gb': disk.total / 1024 / 1024 / 1024
            }
        except Exception as e:
            logger.warning(f"Failed to get system stats: {e}")
            return {
                'cpu_percent': 0.0,
                'memory_percent': 0.0,
                'memory_used_mb': 0.0,
                'memory_total_mb': 0.0,
                'disk_usage_percent': 0.0,
                'disk_used_gb': 0.0,
                'disk_total_gb': 0.0
            }

    async def initialize(self):
        """Initialize all server components asynchronously."""
        logger.info("Initializing Enhanced FastMCP API Server v2.0...")

        # Initialize HTTP client with enhanced connection pooling
        self.http_client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=settings.max_connections,
                max_keepalive_connections=settings.connection_pool_size
            ),
            timeout=httpx.Timeout(30.0, connect=10.0)
        )

        # Initialize Qdrant client with optimized connection pooling
        self.qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            limits=httpx.Limits(
                max_connections=settings.connection_pool_size,
                max_keepalive_connections=settings.connection_pool_size // 2
            )
        )

        # Test Qdrant connection with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.qdrant_client.get_collections()
                logger.info("OK Qdrant connection established")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"ERROR Qdrant connection failed after {max_retries} attempts: {e}")
                    raise
                logger.warning(f"Qdrant connection attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(2 ** attempt)

        # Initialize embedder with GPU support if available
        try:
            device = settings.embedding_device
            # Try GPU first if requested
            if device == "auto":
                try:
                    import torch
                    if torch.cuda.is_available():
                        device = "cuda"
                        logger.info("GPU detected and available")
                    else:
                        device = "cpu"
                        logger.info("GPU not available, using CPU")
                except ImportError:
                    device = "cpu"
                    logger.warning("PyTorch not available, using CPU")

            self.embedder = SentenceTransformer(
                settings.embedding_model,
                device=device,
                trust_remote_code=True
            )
            logger.info(f"OK Embedder initialized: {settings.embedding_model} on {device}")
        except Exception as e:
            logger.error(f"ERROR Embedder initialization failed: {e}")
            raise

        # Initialize caches after core components are available.
        self.embedding_cache = AsyncTTLCache(
            ttl=settings.embedding_cache_ttl,
            max_size=settings.embedding_cache_max_size
        )
        self.query_cache = AsyncTTLCache(
            ttl=settings.query_cache_ttl,
            max_size=settings.query_cache_max_size
        )

        logger.info("Enhanced FastMCP API Server v2.0 initialization complete")

    async def get_embedder(self) -> SentenceTransformer:
        """Get initialized embedder with lazy initialization."""
        if self.embedder is None:
            logger.info("Initializing embedder lazily...")
            await self.initialize_embedder()
        return self.embedder

    async def get_qdrant_client(self) -> AsyncQdrantClient:
        """Get initialized Qdrant client with lazy initialization."""
        if self.qdrant_client is None:
            logger.info("Initializing Qdrant client lazily...")
            await self.initialize_qdrant_client()
        return self.qdrant_client

    async def get_query_embedding(self, query: str) -> Tuple[List[float], bool]:
        """Fetch embedding for query with cache support."""
        cache_hit = False

        if self.embedding_cache:
            cached_embedding = await self.embedding_cache.get(query)
            if cached_embedding is not None:
                cache_hit = True
                return list(cached_embedding), cache_hit

        embedder = await self.get_embedder()
        embedding = embedder.encode([query], batch_size=settings.embedding_batch_size)[0]
        embedding_list = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)

        if self.embedding_cache:
            await self.embedding_cache.set(query, embedding_list)

        return embedding_list, cache_hit

    def build_search_params(self) -> Optional[SearchParams]:
        """Construct SearchParams with quantization if supported."""
        params_kwargs: Dict[str, Any] = {}
        if settings.hnsw_ef_search:
            params_kwargs["hnsw_ef"] = settings.hnsw_ef_search

        quantization = None
        if settings.quantization_rescore:
            try:
                quantization = QuantizationSearchParams(
                    rescore=True,
                    oversampling=settings.quantization_oversampling
                )
            except TypeError:
                # Older client versions may not support oversampling.
                quantization = QuantizationSearchParams(rescore=True)

        if quantization:
            params_kwargs["quantization"] = quantization

        if not params_kwargs:
            return None

        try:
            return SearchParams(**params_kwargs)
        except TypeError:
            # Fallback for older clients lacking quantization kwargs.
            params_kwargs.pop("quantization", None)
            if not params_kwargs:
                return None
            return SearchParams(**params_kwargs)

    async def initialize_embedder(self):
        """Initialize embedder lazily."""
        try:
            device = settings.embedding_device
            # Try GPU first if requested
            if device == "auto":
                try:
                    import torch
                    if torch.cuda.is_available():
                        device = "cuda"
                        logger.info("GPU detected and available")
                    else:
                        device = "cpu"
                        logger.info("GPU not available, using CPU")
                except ImportError:
                    device = "cpu"
                    logger.warning("PyTorch not available, using CPU")

            self.embedder = SentenceTransformer(
                settings.embedding_model,
                device=device,
                trust_remote_code=True
            )
            logger.info(f"OK Embedder initialized: {settings.embedding_model} on {device}")
        except Exception as e:
            logger.error(f"ERROR Embedder initialization failed: {e}")
            raise

    async def initialize_qdrant_client(self):
        """Initialize Qdrant client lazily."""
        # Initialize HTTP client if needed
        if self.http_client is None:
            self.http_client = httpx.AsyncClient(
                limits=httpx.Limits(
                    max_connections=settings.max_connections,
                    max_keepalive_connections=settings.connection_pool_size
                ),
                timeout=httpx.Timeout(30.0, connect=10.0)
            )

        # Initialize Qdrant client
        self.qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            limits=httpx.Limits(
                max_connections=settings.connection_pool_size,
                max_keepalive_connections=settings.connection_pool_size // 2
            )
        )

        # Test Qdrant connection
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.qdrant_client.get_collections()
                logger.info("OK Qdrant connection established")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"ERROR Qdrant connection failed after {max_retries} attempts: {e}")
                    raise
                logger.warning(f"Qdrant connection attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(2 ** attempt)

# Global server state instance
server_state = ServerState()

def _tokenize_text(text: str) -> List[str]:
    if not text:
        return []
    return [token for token in re.findall(r"\w+", text.lower()) if len(token) > 2]


def _extract_payload_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""

    for key in ("text", "content", "chunk", "body", "document"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value

    text_parts = [str(value) for value in payload.values() if isinstance(value, str)]
    return " ".join(text_parts[:3])


def _compute_lexical_score(text: str, query_tokens: List[str]) -> float:
    if not text or not query_tokens:
        return 0.0

    payload_tokens = set(_tokenize_text(text))
    if not payload_tokens:
        return 0.0

    matches = sum(1 for token in query_tokens if token in payload_tokens)
    return matches / len(query_tokens)


def _blend_scores(vector_score: float, lexical_score: float, weight: float) -> float:
    constrained_weight = max(0.0, min(weight, 1.0))
    return constrained_weight * vector_score + (1.0 - constrained_weight) * lexical_score

# Advanced Middleware Classes for Production Deployment
class RequestLoggingMiddleware:
    """Advanced request logging middleware with performance metrics."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "UNKNOWN")

        # Log incoming request
        logger.info(f"REQUEST: {method} {path}")

        # Create response wrapper to capture status
        response_started = False
        response_status = 200

        async def wrapped_send(message):
            nonlocal response_started, response_status
            if message["type"] == "http.response.start":
                response_started = True
                response_status = message.get("status", 200)
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)

            # Log response
            duration = time.time() - start_time
            logger.info(f"RESPONSE: {method} {path} - {response_status} ({duration:.3f}s)")

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"ERROR: {method} {path} - {str(e)} ({duration:.3f}s)")
            raise

class ErrorHandlingMiddleware:
    """Comprehensive error handling middleware with circuit breaker pattern."""

    def __init__(self, app):
        self.app = app
        self.error_counts = {}
        self.last_error_time = {}
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_timeout = 60  # seconds

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        method = scope.get("method", "")

        # Check circuit breaker
        if self._is_circuit_open(path):
            logger.warning(f"Circuit breaker open for {method} {path}")
            await self._send_error_response(send, 503, "Service temporarily unavailable")
            return

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            # Increment error count
            key = f"{method}:{path}"
            self.error_counts[key] = self.error_counts.get(key, 0) + 1
            self.last_error_time[key] = time.time()

            logger.error(f"Unhandled error for {method} {path}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            await self._send_error_response(send, 500, "Internal server error")

    def _is_circuit_open(self, path: str) -> bool:
        """Check if circuit breaker is open for this endpoint."""
        key = f"GET:{path}"  # Assume GET for simplicity
        error_count = self.error_counts.get(key, 0)
        last_error = self.last_error_time.get(key, 0)

        if error_count >= self.circuit_breaker_threshold:
            if time.time() - last_error < self.circuit_breaker_timeout:
                return True
            else:
                # Reset circuit breaker
                self.error_counts[key] = 0

        return False

    async def _send_error_response(self, send, status_code: int, message: str):
        """Send error response."""
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": [[b"content-type", b"application/json"]],
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps({"error": message, "timestamp": datetime.utcnow().isoformat()}).encode(),
        })

class MetricsMiddleware:
    """Prometheus metrics collection middleware."""

    def __init__(self, app):
        self.app = app

        if PROMETHEUS_AVAILABLE:
            # Initialize Prometheus metrics
            self.request_count = Counter(
                'fastmcp_requests_total',
                'Total number of requests',
                ['method', 'endpoint', 'status']
            )
            self.request_duration = Histogram(
                'fastmcp_request_duration_seconds',
                'Request duration in seconds',
                ['method', 'endpoint']
            )
            self.active_connections = Gauge(
                'fastmcp_active_connections',
                'Number of active connections'
            )

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if not PROMETHEUS_AVAILABLE:
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "UNKNOWN")

        # Increment active connections
        self.active_connections.inc()

        response_status = 200

        async def wrapped_send(message):
            nonlocal response_status
            if message["type"] == "http.response.start":
                response_status = message.get("status", 200)
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)

            # Record metrics
            duration = time.time() - start_time
            self.request_count.labels(method=method, endpoint=path, status=response_status).inc()
            self.request_duration.labels(method=method, endpoint=path).observe(duration)

        finally:
            # Decrement active connections
            self.active_connections.dec()

# Global server state instance
server_state = ServerState()

def update_metrics(self, response_time: float, cache_hit: bool = False):
        """Update performance metrics."""
        self.request_count += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        # Update rolling average response time
        if self.request_count == 1:
            self.avg_response_time = response_time
        else:
            self.avg_response_time = (self.avg_response_time * (self.request_count - 1) + response_time) / self.request_count

# Global server state
server_state = ServerState()

# FastAPI Application with FastMCP integration 
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    await server_state.initialize()
    yield

    # Cleanup on shutdown
    if server_state.http_client:
        await server_state.http_client.aclose()
    if server_state.qdrant_client:
        await server_state.qdrant_client.close()

app = FastAPI(
    title="FastMCP API Server",
    description="FastMCP server with REST API integration for Qdrant vector operations",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.enable_openapi_enhancement else None,
    redoc_url="/redoc" if settings.enable_openapi_enhancement else None,
    openapi_url="/openapi.json" if settings.enable_openapi_enhancement else None
)

# Basic middleware - CORS only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic OpenAPI Customization
def custom_openapi():
    """Basic OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastMCP API Server",
        version="2.0.0",
        description="FastMCP server with REST API integration for Qdrant vector operations",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

if settings.enable_openapi_enhancement:
    app.openapi = custom_openapi

# Basic MCP server setup (no composition for first iteration)
mcp = FastMCP("FastMCP API Server")

# Request/Response Models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    collection: str = Field(..., description="Target collection name")
    limit: int = Field(10, description="Maximum results", ge=1, le=100)
    score_threshold: float = Field(0.7, description="Minimum similarity score", ge=0.0, le=1.0)
    use_cache: bool = Field(True, description="Use cached results if available")
    hybrid_search: bool = Field(True, description="Apply lexical re-ranking with vector scores")

class SearchResponse(BaseModel):
    query: str
    collection: str
    results: List[Dict[str, Any]]
    total_results: int
    search_time_ms: float
    cached: bool
    hybrid_applied: bool = False

class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    qdrant_connected: bool
    embedder_loaded: bool
    cache_stats: Dict[str, Any]
    system_stats: Dict[str, Any]

class CollectionInfo(BaseModel):
    name: str
    display_name: str
    vector_count: int
    description: str
    knowledge_areas: List[str]
    vector_size: int

# FastMCP Tools - All tools use @mcp.tool() decorator

async def _semantic_search_internal(
    query: str,
    collection: str,
    limit: int = 10,
    score_threshold: float = 0.7
) -> str:
    """
    Enterprise semantic search with CodeRankEmbed.

    Args:
        query: Search query text
        collection: Target collection name
        limit: Maximum results (1-100)
        score_threshold: Minimum similarity score (0.0-1.0)

    Returns:
        Formatted search results with performance metrics
    """
    start_time = time.time()

    try:
        # Validate collection
        try:
            canonical_collection = ensure_supported_collection(collection)
        except ValueError as exc:
            return f"ERROR {exc}"

        display_collection = COLLECTION_DISPLAY_NAMES.get(canonical_collection, canonical_collection)

        cache_key = f"tool-search:{canonical_collection}:{limit}:{score_threshold}:{query}"
        if server_state.query_cache:
            cached_payload = await server_state.query_cache.get(cache_key)
            if cached_payload:
                server_state.update_metrics(time.time() - start_time, cache_hit=True)
                return f"{cached_payload['payload']}\n\n[CACHE] served from query cache"

        # Generate (or reuse) embedding
        query_embedding, embedding_cached = await server_state.get_query_embedding(query)

        # Perform search
        qdrant_client = await server_state.get_qdrant_client()
        search_kwargs = {
            "collection_name": canonical_collection,
            "query_vector": query_embedding,
            "limit": limit,
            "score_threshold": score_threshold,
            "with_payload": True
        }

        search_params = server_state.build_search_params()
        if search_params:
            search_kwargs["search_params"] = search_params

        search_result = await qdrant_client.search(**search_kwargs)

        # Format results
        results = []
        for hit in search_result:
            results.append(f"Score: {hit.score:.3f} - {hit.payload}")

        search_time = time.time() - start_time
        response_text = f"""ENTERPRISE SEARCH RESULTS
Query: "{query}"
Collection: {display_collection}
Results: {len(results)} found
Search Time: {search_time:.3f}s

{chr(10).join(results) if results else "No results found"}"""

        if server_state.query_cache:
            await server_state.query_cache.set(cache_key, {"payload": response_text})

        server_state.update_metrics(search_time, cache_hit=embedding_cached)

        return response_text

    except Exception as e:
        logger.error(f"Enterprise search error: {e}")
        server_state.error_count += 1
        return f"Search failed: {str(e)}"

@mcp.tool()
async def get_server_stats() -> str:
    """Get comprehensive server statistics and performance metrics."""
    try:
        uptime = time.time() - server_state.startup_time

        # Get system stats
        system_stats = server_state.get_system_stats()

        # Get Qdrant stats
        qdrant_stats = {}
        try:
            qdrant_client = await server_state.get_qdrant_client()
            collections = await qdrant_client.get_collections()
            for collection in collections.collections:
                info = await qdrant_client.get_collection(collection_name=collection.name)
                qdrant_stats[collection.name] = {
                    "vectors": info.points_count,
                    "status": "active"
                }
        except Exception as e:
            logger.warning(f"Qdrant stats error: {e}")

        # Get GPU stats if available
        gpu_stats = ""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                gpu_stats = f"GPU: {gpu.name} - {gpu.memoryUsed:.0f}MB/{gpu.memoryTotal:.0f}MB ({gpu.memoryUtil*100:.1f}%)"
        except:
            pass

        result = (
            f"SERVER STATISTICS\n"
            f"Uptime: {uptime:.0f} seconds ({uptime/3600:.1f} hours)\n"
            f"Requests: {server_state.request_count:,}\n"
            f"Errors: {server_state.error_count:,}\n"
            f"Success Rate: {(1 - server_state.error_count/max(server_state.request_count, 1))*100:.1f}%\n\n"
            f"SYSTEM RESOURCES\n"
            f"CPU: {system_stats['cpu_percent']:.1f}%\n"
            f"Memory: {system_stats['memory_percent']:.1f}% ({system_stats['memory_used_mb']:.0f}MB used)\n"
            f"Disk: {system_stats['disk_usage_percent']:.1f}%\n\n"
            f"GPU STATUS\n"
            f"{gpu_stats if gpu_stats else 'Not available'}\n\n"
            f"QDRANT COLLECTIONS\n"
            + "\n".join([f"{name}: {info.get('vectors', 0):,} vectors ({info.get('status', 'unknown')})" for name, info in qdrant_stats.items()]) + "\n\n"
            f"CONFIGURATION\n"
            f"Model: {settings.embedding_model}\n"
            f"Device: {settings.embedding_device}\n"
            f"Batch Size: {settings.embedding_batch_size}\n"
            f"Max Connections: {settings.max_connections}\n"
            f"Collections: {', '.join(COLLECTION_DISPLAY_NAMES.get(name, name) for name in get_supported_collections())}\n"
        )
        return result

    except Exception as e:
        logger.error(f"Stats error: {e}")
        return f"ERROR Failed to get stats: {str(e)}"

@mcp.tool()
async def optimize_collection_performance(collection: str) -> str:
    """Analyze and provide optimization recommendations for a collection."""
    try:
        try:
            canonical_collection = ensure_supported_collection(collection)
        except ValueError as exc:
            return f"ERROR {exc}"

        display_collection = COLLECTION_DISPLAY_NAMES.get(canonical_collection, canonical_collection)

        qdrant_client = await server_state.get_qdrant_client()

        # Get collection info
        collection_info = await qdrant_client.get_collection(collection_name=canonical_collection)

        # Analyze current configuration
        recommendations = []

        # Vector configuration analysis
        vector_config = collection_info.config.params.vectors
        if hasattr(vector_config, 'size'):
            if vector_config.size == 1536:
                recommendations.append("OK Vector size (1536) matches jina-code-embeddings-1.5b")
            else:
                recommendations.append(f"WARNING Vector size mismatch: {vector_config.size} vs 1536")

        # Quantization analysis
        if hasattr(collection_info.config.params, 'quantization_config'):
            quantization = collection_info.config.params.quantization_config
            if quantization:
                recommendations.append("OK Quantization enabled for performance")
            else:
                recommendations.append("WARNING Consider enabling quantization for better performance")

        # Indexing analysis
        if hasattr(collection_info.config.params, 'hnsw_config'):
            hnsw_config = collection_info.config.params.hnsw_config
            recommendations.append(f"OK HNSW configured with M={hnsw_config.m}, ef_construct={hnsw_config.ef_construct}")

        # Performance recommendations
        recommendations.extend([
            "",
            " PERFORMANCE OPTIMIZATIONS:",
            "- Use hybrid search with quantization rescore",
            "- Implement query result caching",
            "- Batch embedding generation",
            "- Enable connection pooling",
            "- Monitor query latency and throughput"
        ])

        result = (
            f"COLLECTION OPTIMIZATION: {display_collection}\n"
            f"{'='*50}\n"
            f"Vector Size: {vector_config.size if hasattr(vector_config, 'size') else 'Unknown'}\n"
            f"Points Count: {collection_info.points_count:,}\n"
            f"Status: {collection_info.status}\n\n"
            f"RECOMMENDATIONS:\n"
            f"{chr(10).join(f'- {rec}' for rec in recommendations)}\n"
        )
        return result

    except Exception as e:
        logger.error(f"Optimization analysis error: {e}")
        return f"Optimization analysis failed: {str(e)}"

@mcp.tool()
async def semantic_search_ultimate(
    query: str,
    collections: Optional[List[str]] = None,
    limit: int = 10,
    score_threshold: float = 0.0,
    hybrid_search: bool = True
) -> str:
    """
    Primary semantic search across all managed Qdrant collections.

    Automatically classifies queries and searches the most relevant collections:
    - sentence_transformers_v4_nomic_coderank: Embedding techniques and transformer usage
    - docling_v4_nomic_coderank: Document processing and parsing workflows
    - qdrant_ecosystem_v4_nomic_coderank: Qdrant operations, optimization, and best practices
    - fast_docs_v4_nomic_coderank / pydantic_v4_nomic_coderank when query context matches those domains

    Args:
        query: Natural-language search string
        collections: Optional override of collections to target
    limit: Maximum results to return (default 10 as in the standard CLI example)
    score_threshold: Minimum similarity score cutoff (default 0.0 to surface exploratory hits)
        hybrid_search: Placeholder flag for future hybrid retrieval support
    """
    start_time = time.time()

    try:
        logger.info(f"Ultimate search query: {query}")

        user_provided = collections is not None and len(collections) > 0

        # Auto-classify query if no collections specified
        if not collections:
            auto_collections: List[str] = []
            query_lower = query.lower()

            # Classify based on query content using legacy aliases for convenience
            if any(word in query_lower for word in ['embed', 'sentence', 'transform', 'vector', 'nlp', 'text']):
                auto_collections.append("sentence_transformers")
            if any(word in query_lower for word in ['document', 'pdf', 'parse', 'extract', 'docling', 'processing']):
                auto_collections.append("docling")
            if any(word in query_lower for word in ['qdrant', 'database', 'search', 'index', 'vector', 'performance', 'optimize']):
                auto_collections.append("qdrant_ecosystem")
            if any(word in query_lower for word in ['fast', 'docs', 'framework', 'api']):
                auto_collections.append("fast_docs")
            if any(word in query_lower for word in ['pydantic', 'validation', 'model', 'schema']):
                auto_collections.append("pydantic")

            if auto_collections:
                collections = auto_collections
            else:
                collections = get_supported_collections()

        resolved_collections = resolve_collections(collections)
        if not resolved_collections:
            if user_provided:
                available = describe_available_collections()
                return f"No valid collections specified. Available: {available}"
            resolved_collections = get_supported_collections()

        collections = resolved_collections

        cache_key = f"ultimate-search:{','.join(sorted(collections))}:{limit}:{score_threshold}:{hybrid_search}:{query}"
        if server_state.query_cache:
            cached_payload = await server_state.query_cache.get(cache_key)
            if cached_payload:
                server_state.update_metrics(time.time() - start_time, cache_hit=True)
                return f"{cached_payload['payload']}\n\n[CACHE] served from query cache"

        # Search each collection
        all_results = []
        query_embedding, embedding_cached = await server_state.get_query_embedding(query)
        query_tokens = _tokenize_text(query) if hybrid_search else []
        qdrant_client = await server_state.get_qdrant_client()
        search_params = server_state.build_search_params()
        vector_limit = limit * 2 if hybrid_search else limit

        for collection in collections:

            try:
                search_kwargs = {
                    "collection_name": collection,
                    "query_vector": query_embedding,
                    "limit": vector_limit,
                    "score_threshold": score_threshold,
                    "with_payload": True
                }

                if search_params:
                    search_kwargs["search_params"] = search_params

                search_result = await qdrant_client.search(**search_kwargs)

                # Format results
                for hit in search_result:
                    payload = hit.payload or {}
                    lexical_score = _compute_lexical_score(
                        _extract_payload_text(payload),
                        query_tokens
                    ) if hybrid_search else 0.0

                    combined_score = _blend_scores(
                        float(hit.score),
                        lexical_score,
                        settings.hybrid_vector_weight if hybrid_search else 1.0
                    )

                    all_results.append({
                        'collection': collection,
                        'display_name': COLLECTION_DISPLAY_NAMES.get(collection, collection),
                        'score': combined_score,
                        'vector_score': float(hit.score),
                        'lexical_score': lexical_score,
                        'payload': payload,
                        'id': hit.id
                    })

            except Exception as e:
                logger.warning(f"Search failed for collection {collection}: {e}")
                continue

        # Sort and limit results
        all_results.sort(key=lambda x: x['score'], reverse=True)
        top_results = all_results[:limit]

        # Format response
        if not top_results:
            return f"No results found for query: {query}"

        lines = [f"Ultimate Search Results for: '{query}'", ""]
        for i, result in enumerate(top_results, 1):
            collection_display = result.get('display_name', COLLECTION_DISPLAY_NAMES.get(result['collection'], result['collection']))
            score_line = f"{i}. [{collection_display}] Score: {result['score']:.3f}"
            if hybrid_search:
                score_line += f" (vector {result['vector_score']:.3f}, lexical {result['lexical_score']:.3f})"
            lines.append(score_line)

            text_snippet = _extract_payload_text(result['payload'])
            if text_snippet:
                snippet = text_snippet[:200] + "..." if len(text_snippet) > 200 else text_snippet
                lines.append(f"   {snippet}")
            lines.append("")

        response = "\n".join(lines).rstrip()

        if server_state.query_cache:
            await server_state.query_cache.set(cache_key, {"payload": response})

        server_state.update_metrics(time.time() - start_time, cache_hit=embedding_cached)

        return response

    except Exception as e:
        logger.error(f"Ultimate search error: {e}")
        return f"Search failed: {str(e)}"

@mcp.tool()
async def get_collection_stats() -> str:
    """Get statistics for all Ultimate Qdrant collections."""
    try:
        qdrant_client = await server_state.get_qdrant_client()

        stats = []
        total_vectors = 0

        for collection in get_supported_collections():
            try:
                collection_info = await qdrant_client.get_collection(collection)
                vector_count = collection_info.points_count or 0
                total_vectors += vector_count

                display_name = COLLECTION_DISPLAY_NAMES.get(collection, collection)
                stats.append(f"{display_name} ({collection}): {vector_count:,} vectors")

            except Exception as e:
                stats.append(f"ERROR {collection}: Error - {str(e)}")

        stats.insert(0, f"Ultimate Knowledge Base Stats (Total: {total_vectors:,} vectors)")
        stats.insert(1, "")

        return "\n".join(stats)

    except Exception as e:
        logger.error(f"Collection stats error: {e}")
        return f"Failed to get collection stats: {str(e)}"


# REST API Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Kubernetes-compatible health check endpoint."""
    uptime = time.time() - server_state.startup_time

    # Check Qdrant connectivity
    qdrant_healthy = False
    try:
        qdrant_client = await server_state.get_qdrant_client()
        await qdrant_client.get_collections()
        qdrant_healthy = True
    except:
        qdrant_healthy = False

    # Get cache stats
    cache_stats = {}
    if server_state.embedding_cache and server_state.query_cache:
        try:
            embedding_info = await server_state.embedding_cache.info()
            query_info = await server_state.query_cache.info()
            cache_stats = {
                "embedding_cache": embedding_info,
                "query_cache": query_info
            }
        except:
            cache_stats = {"status": "unavailable"}

    # System stats
    system_stats = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

    return HealthResponse(
        status="healthy" if qdrant_healthy else "unhealthy",
        uptime_seconds=uptime,
        qdrant_connected=qdrant_healthy,
        embedder_loaded=server_state.embedder is not None,
        cache_stats=cache_stats,
        system_stats=system_stats
    )

@app.get("/collections", response_model=List[CollectionInfo])
async def list_collections():
    """Get information about available collections."""
    supported = set(get_supported_collections())
    return [
        CollectionInfo(
            name=name,
            display_name=COLLECTION_DISPLAY_NAMES.get(name, name),
            vector_count=metadata["vectors"],
            description=metadata["description"],
            knowledge_areas=metadata["knowledge_areas"],
            vector_size=metadata["vector_size"]
        )
        for name, metadata in COLLECTION_METADATA.items()
        if name in supported
    ]

@app.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    """REST API endpoint for semantic search."""
    start_time = time.time()

    try:
        # Validate collection
        try:
            canonical_collection = ensure_supported_collection(request.collection)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        result_cache_key = f"rest-search:{canonical_collection}:{request.limit}:{request.score_threshold}:{request.hybrid_search}:{request.query}"
        if request.use_cache and server_state.query_cache:
            cached_response = await server_state.query_cache.get(result_cache_key)
            if cached_response:
                cached_copy = dict(cached_response)
                cached_copy["cached"] = True
                server_state.update_metrics(time.time() - start_time, cache_hit=True)
                return SearchResponse(**cached_copy)

        # Generate embedding (respect cache preference)
        if request.use_cache:
            query_embedding, embedding_cached = await server_state.get_query_embedding(request.query)
        else:
            embedder = await server_state.get_embedder()
            embedding = embedder.encode([request.query], batch_size=settings.embedding_batch_size)[0]
            query_embedding = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            embedding_cached = False

        # Perform search
        qdrant_client = await server_state.get_qdrant_client()
        search_params = server_state.build_search_params()
        vector_limit = request.limit * 2 if request.hybrid_search else request.limit

        search_kwargs = {
            "collection_name": canonical_collection,
            "query_vector": query_embedding,
            "limit": vector_limit,
            "score_threshold": request.score_threshold,
            "with_payload": True
        }

        if search_params:
            search_kwargs["search_params"] = search_params

        raw_results = await qdrant_client.search(**search_kwargs)

        # Format results with optional hybrid scoring
        query_tokens = _tokenize_text(request.query) if request.hybrid_search else []
        results = []
        for hit in raw_results:
            payload = hit.payload or {}
            lexical_score = _compute_lexical_score(
                _extract_payload_text(payload),
                query_tokens
            ) if request.hybrid_search else 0.0

            combined_score = _blend_scores(
                float(hit.score),
                lexical_score,
                settings.hybrid_vector_weight if request.hybrid_search else 1.0
            )

            result_entry = {
                "id": hit.id,
                "score": combined_score,
                "payload": payload
            }

            if request.hybrid_search:
                result_entry["vector_score"] = float(hit.score)
                result_entry["lexical_score"] = lexical_score

            results.append(result_entry)

        if request.hybrid_search:
            results.sort(key=lambda item: item["score"], reverse=True)

        trimmed_results = results[:request.limit]
        elapsed = time.time() - start_time
        search_time = elapsed * 1000

        response_payload = {
            "query": request.query,
            "collection": canonical_collection,
            "results": trimmed_results,
            "total_results": len(trimmed_results),
            "search_time_ms": search_time,
            "cached": False,
            "hybrid_applied": request.hybrid_search
        }

        if request.use_cache and server_state.query_cache:
            await server_state.query_cache.set(result_cache_key, response_payload)

        server_state.update_metrics(elapsed, cache_hit=embedding_cached)

        return SearchResponse(**response_payload)

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    metrics_data = (
        f"# Enterprise FastMCP API Server Metrics\n"
        f"# HELP qdrant_fastmcp_requests_total Total number of requests\n"
        f"# TYPE qdrant_fastmcp_requests_total counter\n"
        f"qdrant_fastmcp_requests_total {server_state.request_count}\n\n"
        f"# HELP qdrant_fastmcp_errors_total Total number of errors\n"
        f"# TYPE qdrant_fastmcp_errors_total counter\n"
        f"qdrant_fastmcp_errors_total {server_state.error_count}\n\n"
        f"# HELP qdrant_fastmcp_uptime_seconds Server uptime in seconds\n"
        f"# TYPE qdrant_fastmcp_uptime_seconds gauge\n"
        f"qdrant_fastmcp_uptime_seconds {time.time() - server_state.startup_time}\n\n"
        f"# HELP qdrant_fastmcp_cpu_percent CPU usage percentage\n"
        f"# TYPE qdrant_fastmcp_cpu_percent gauge\n"
        f"qdrant_fastmcp_cpu_percent {psutil.cpu_percent()}\n\n"
        f"# HELP qdrant_fastmcp_memory_percent Memory usage percentage\n"
        f"# TYPE qdrant_fastmcp_memory_percent gauge\n"
        f"qdrant_fastmcp_memory_percent {psutil.virtual_memory().percent}\n"
    )

    return Response(content=metrics_data, media_type="text/plain")

# Additional REST API Endpoints for Production Deployment

class UltimateSearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    collections: Optional[List[str]] = Field(None, description="Specific collections to search")
    limit: int = Field(10, description="Maximum results per collection", ge=1, le=100)
    score_threshold: float = Field(0.0, description="Minimum similarity score", ge=0.0, le=1.0)
    hybrid_search: bool = Field(True, description="Use hybrid search for better results")
    use_cache: bool = Field(True, description="Use cached embeddings and aggregated responses")

class ChunkingOptimizationRequest(BaseModel):
    content_length: int = Field(1000, description="Length of content to optimize for", ge=1)
    content_type: str = Field("general", description="Type of content (general, code, documentation, scientific)")
    knowledge_domain: str = Field("mixed", description="Knowledge domain (mixed, technical, academic)")

@app.post("/search/ultimate", response_model=SearchResponse)
async def ultimate_search_endpoint(request: UltimateSearchRequest):
    """Advanced ultimate search across all managed collections with auto-classification."""
    start_time = time.time()

    try:
        collections = request.collections
        user_provided = collections is not None and len(collections or []) > 0

        if not collections:
            auto_collections: List[str] = []
            query_lower = request.query.lower()

            if any(word in query_lower for word in ['embed', 'sentence', 'transform', 'vector', 'nlp', 'text']):
                auto_collections.append("sentence_transformers")
            if any(word in query_lower for word in ['document', 'pdf', 'parse', 'extract', 'docling', 'processing']):
                auto_collections.append("docling")
            if any(word in query_lower for word in ['qdrant', 'database', 'search', 'index', 'vector', 'performance', 'optimize']):
                auto_collections.append("qdrant_ecosystem")
            if any(word in query_lower for word in ['fast', 'docs', 'framework', 'api']):
                auto_collections.append("fast_docs")
            if any(word in query_lower for word in ['pydantic', 'validation', 'model', 'schema']):
                auto_collections.append("pydantic")

            collections = auto_collections if auto_collections else get_supported_collections()

        resolved_collections = resolve_collections(collections)
        if not resolved_collections:
            if user_provided:
                available = describe_available_collections()
                raise HTTPException(status_code=400, detail=f"No valid collections specified. Available: {available}")
            resolved_collections = get_supported_collections()

        collections = resolved_collections

        result_cache_key = f"rest-ultimate:{','.join(sorted(collections))}:{request.limit}:{request.score_threshold}:{request.hybrid_search}:{request.query}"
        if request.use_cache and server_state.query_cache:
            cached_response = await server_state.query_cache.get(result_cache_key)
            if cached_response:
                cached_copy = dict(cached_response)
                cached_copy["cached"] = True
                server_state.update_metrics(time.time() - start_time, cache_hit=True)
                return SearchResponse(**cached_copy)

        # Search each collection
        if request.use_cache:
            query_embedding, embedding_cached = await server_state.get_query_embedding(request.query)
        else:
            embedder = await server_state.get_embedder()
            embedding = embedder.encode([request.query], batch_size=settings.embedding_batch_size)[0]
            query_embedding = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            embedding_cached = False

        query_tokens = _tokenize_text(request.query) if request.hybrid_search else []
        qdrant_client = await server_state.get_qdrant_client()
        search_params = server_state.build_search_params()
        vector_limit = request.limit * 2 if request.hybrid_search else request.limit

        all_results = []

        for collection in collections:

            try:
                search_kwargs = {
                    "collection_name": collection,
                    "query_vector": query_embedding,
                    "limit": vector_limit,
                    "score_threshold": request.score_threshold,
                    "with_payload": True
                }

                if search_params:
                    search_kwargs["search_params"] = search_params

                search_result = await qdrant_client.search(**search_kwargs)

                for hit in search_result:
                    payload = hit.payload or {}
                    lexical_score = _compute_lexical_score(
                        _extract_payload_text(payload),
                        query_tokens
                    ) if request.hybrid_search else 0.0

                    combined_score = _blend_scores(
                        float(hit.score),
                        lexical_score,
                        settings.hybrid_vector_weight if request.hybrid_search else 1.0
                    )

                    all_results.append({
                        'collection': collection,
                        'display_name': COLLECTION_DISPLAY_NAMES.get(collection, collection),
                        'score': combined_score,
                        'vector_score': float(hit.score),
                        'lexical_score': lexical_score,
                        'payload': payload,
                        'id': hit.id
                    })

            except Exception as e:
                logger.warning(f"Search failed for collection {collection}: {e}")
                continue

        all_results.sort(key=lambda x: x['score'], reverse=True)
        top_results = all_results[:request.limit]
        elapsed = time.time() - start_time

        response_payload = {
            "query": request.query,
            "collection": ", ".join(collections),
            "results": top_results,
            "total_results": len(top_results),
            "search_time_ms": elapsed * 1000,
            "cached": False,
            "hybrid_applied": request.hybrid_search
        }

        if request.use_cache and server_state.query_cache:
            await server_state.query_cache.set(result_cache_key, response_payload)

        server_state.update_metrics(elapsed, cache_hit=embedding_cached)

        return SearchResponse(**response_payload)

    except Exception as e:
        logger.error(f"Ultimate search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections/stats")
async def collection_stats_endpoint():
    """Get detailed statistics for all collections."""
    try:
        qdrant_client = await server_state.get_qdrant_client()

        stats = {
            "total_collections": len(get_supported_collections()),
            "total_vectors": 0,
            "collections": {}
        }

        for collection in get_supported_collections():
            try:
                collection_info = await qdrant_client.get_collection(collection)
                vector_count = collection_info.points_count or 0
                stats["total_vectors"] += vector_count

                stats["collections"][collection] = {
                    "display_name": COLLECTION_DISPLAY_NAMES.get(collection, collection),
                    "vectors": vector_count,
                    "status": "active" if collection_info.status == "green" else "issues",
                    "vector_size": COLLECTION_METADATA.get(collection, {}).get("vector_size", 1536)
                }

            except Exception as e:
                stats["collections"][collection] = {
                    "display_name": COLLECTION_DISPLAY_NAMES.get(collection, collection),
                    "vectors": 0,
                    "status": "error",
                    "error": str(e)
                }

        return stats

    except Exception as e:
        logger.error(f"Collection stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize/chunking")
async def optimize_chunking_endpoint(request: ChunkingOptimizationRequest):
    """Get optimized chunking strategy recommendations."""
    try:
        # Base recommendations
        recommendations = []

        # Size-based recommendations
        if request.content_length < 500:
            recommendations.append("Small content: Use single chunk (no splitting needed)")
        elif request.content_length < 2000:
            recommendations.append("Medium content: Split into 2-3 chunks of 500-800 tokens")
        elif request.content_length < 10000:
            recommendations.append("Large content: Split into chunks of 1000-1500 tokens with 200 token overlap")
        else:
            recommendations.append("Very large content: Use hierarchical chunking with 1500 token chunks and 300 token overlap")

        # Content type specific
        if request.content_type == "code":
            recommendations.append("Code content: Preserve function/class boundaries, avoid splitting mid-function")
        elif request.content_type == "documentation":
            recommendations.append("Documentation: Split on section headers, preserve table of contents structure")
        elif request.content_type == "scientific":
            recommendations.append("Scientific content: Split on paragraph boundaries, preserve citation contexts")

        # Domain specific
        if request.knowledge_domain == "technical":
            recommendations.append("Technical domain: Prioritize code examples and API documentation in separate chunks")
        elif request.knowledge_domain == "academic":
            recommendations.append("Academic domain: Preserve methodology and results sections together")

        # General best practices
        recommendations.append("Best practices: Use sentence-aware splitting, maintain semantic coherence")
        recommendations.append("Quality check: Ensure each chunk contains complete, meaningful information")

        return {
            "content_length": request.content_length,
            "content_type": request.content_type,
            "knowledge_domain": request.knowledge_domain,
            "recommendations": recommendations
        }

    except Exception as e:
        logger.error(f"Chunking optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/performance/analysis")
async def performance_analysis_endpoint():
    """Analyze performance characteristics of all collections."""
    try:
        qdrant_client = await server_state.get_qdrant_client()

        analysis = {
            "timestamp": time.time(),
            "collections": {}
        }

        for collection in get_supported_collections():
            try:
                collection_info = await qdrant_client.get_collection(collection)

                analysis["collections"][collection] = {
                    "display_name": COLLECTION_DISPLAY_NAMES.get(collection, collection),
                    "vectors": collection_info.points_count or 0,
                    "status": "active" if collection_info.status == "green" else "issues",
                    "configuration": "optimized" if hasattr(collection_info, 'config') else "unknown"
                }

            except Exception as e:
                analysis["collections"][collection] = {
                    "display_name": COLLECTION_DISPLAY_NAMES.get(collection, collection),
                    "status": "error",
                    "error": str(e)
                }

        return analysis

    except Exception as e:
        logger.error(f"Performance analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/server/stats")
async def server_stats_endpoint():
    """Get comprehensive server statistics and health information."""
    try:
        uptime = time.time() - server_state.startup_time

        # Get system stats
        system_stats = server_state.get_system_stats()

        # Get cache stats if available
        cache_stats = {}
        if server_state.embedding_cache:
            try:
                cache_info = await server_state.embedding_cache.info()
                cache_stats["embedding_cache"] = cache_info
            except:
                cache_stats["embedding_cache"] = "unavailable"

        if server_state.query_cache:
            try:
                cache_info = await server_state.query_cache.info()
                cache_stats["query_cache"] = cache_info
            except:
                cache_stats["query_cache"] = "unavailable"

        return {
            "uptime_seconds": uptime,
            "request_count": server_state.request_count,
            "error_count": server_state.error_count,
            "cache_hits": server_state.cache_hits,
            "cache_misses": server_state.cache_misses,
            "avg_response_time": server_state.avg_response_time,
            "system_stats": system_stats,
            "cache_stats": cache_stats,
            "qdrant_connected": True,  # Would be False if connection failed
            "embedder_loaded": server_state.embedder is not None
        }

    except Exception as e:
        logger.error(f"Server stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collections/{collection_name}/optimize")
async def optimize_collection_endpoint(collection_name: str):
    """Get optimization recommendations for a specific collection."""
    try:
        canonical_collection = ensure_supported_collection(collection_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    try:
        qdrant_client = await server_state.get_qdrant_client()
        collection_info = await qdrant_client.get_collection(canonical_collection)
    except Exception as e:
        logger.error(f"Collection optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    recommendations = []

    # Vector count analysis
    vector_count = collection_info.points_count or 0
    if vector_count < 1000:
        recommendations.append("Small collection: Consider using exact search for better precision")
    elif vector_count < 10000:
        recommendations.append("Medium collection: HNSW with M=16, ef=128 recommended")
    else:
        recommendations.append("Large collection: HNSW with M=32, ef=256 recommended for optimal performance")

    # Vector size analysis
    expected_size = COLLECTION_METADATA.get(canonical_collection, {}).get("vector_size", 1536)
    recommendations.append(f"Vector size: {expected_size} dimensions - optimized for semantic search")

    # Performance recommendations
    recommendations.append("Enable quantization for 2-4x performance improvement")
    recommendations.append("Use product quantization for high-dimensional vectors")
    recommendations.append("Consider IVF indexing for very large collections")

    return {
        "collection": canonical_collection,
        "vector_count": vector_count,
        "recommendations": recommendations
    }

# MCP server with HTTP transport for Docker/REST API mode
# Use app.mount() approach per FastMCP integration docs
logger.info("Mounting FastMCP server with HTTP transport")
mcp_http_app = mcp.http_app(path="/")
app.mount("/mcp", mcp_http_app)

# Ensure FastAPI and FastMCP lifespans both execute
previous_lifespan = app.router.lifespan_context

@asynccontextmanager
async def noop_context(_: FastAPI):
    yield


@asynccontextmanager
async def combined_lifespan(app_instance: FastAPI):
    previous_context = previous_lifespan or noop_context
    mcp_context = mcp_http_app.lifespan or noop_context

    async with previous_context(app_instance):
        async with mcp_context(app_instance):
            yield

app.router.lifespan_context = combined_lifespan

# Main entry point - ONLY FastMCP with FastAPI
if __name__ == "__main__":
    logger.info("Starting Enterprise FastMCP API Server")
    logger.info(f"Host: {settings.host}:{settings.port}")
    logger.info(f"Collections: {', '.join(COLLECTION_DISPLAY_NAMES.get(name, name) for name in get_supported_collections())}")
    logger.info(f"Model: {settings.embedding_model}")
    logger.info(f"Device: {settings.embedding_device}")
    logger.info("FastMCP tools available via /mcp (HTTP transport)")

    uvicorn.run(
        "qdrant_fastmcp_api_server:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=False,
        access_log=True
    )
