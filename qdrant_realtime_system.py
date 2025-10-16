#!/usr/bin/env python3
"""
Qdrant Real-Time Vector System Implementation
============================================

Advanced real-time implementation with practical examples addressing
the gaps identified in our analysis:

1. Real-time updates (Current: 0.499 → Target: 0.8+)
2. Memory optimization (Current: 0.558 → Target: 0.8+) 
3. Search latency (Current: 0.582 → Target: 0.8+)
4. Scalability patterns (Current: 0.613 → Target: 0.8+)
"""

import asyncio
import json
import time
import logging
import psutil
from datetime import datetime
from typing import Dict, List, Any, Optional, AsyncGenerator
from pathlib import Path
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-realtime")

@dataclass
class RealTimeConfig:
    """Configuration for real-time Qdrant operations."""
    # Memory optimization settings
    memory_threshold_mb: int = 1024
    batch_size: int = 100
    max_cache_size: int = 1000
    
    # Performance optimization
    hnsw_ef: int = 32  # Lower for speed
    hnsw_m: int = 16   # Lower for speed
    search_timeout_ms: int = 1000
    
    # Real-time update settings
    update_buffer_size: int = 10000
    batch_interval_seconds: float = 1.0
    
    # Monitoring settings
    metrics_retention_count: int = 1000
    log_interval_seconds: float = 10.0

@dataclass
class PerformanceMetrics:
    """Real-time performance metrics."""
    timestamp: float
    operation: str
    latency_ms: float
    memory_mb: float
    success: bool
    details: Optional[Dict[str, Any]] = None

class MemoryOptimizer:
    """Memory optimization for Qdrant operations."""
    
    def __init__(self, config: RealTimeConfig):
        self.config = config
        self.process = psutil.Process()
        self.memory_history = deque(maxlen=100)
        
    def get_current_memory_mb(self) -> float:
        """Get current memory usage in MB."""
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        self.memory_history.append(memory_mb)
        return memory_mb
    
    def is_memory_pressure(self) -> bool:
        """Check if under memory pressure."""
        return self.get_current_memory_mb() > self.config.memory_threshold_mb
    
    def get_optimized_batch_size(self) -> int:
        """Get optimized batch size based on memory."""
        if self.is_memory_pressure():
            return max(10, self.config.batch_size // 2)
        return self.config.batch_size
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        current = self.get_current_memory_mb()
        history = list(self.memory_history)
        
        return {
            "current_mb": current,
            "threshold_mb": self.config.memory_threshold_mb,
            "under_pressure": self.is_memory_pressure(),
            "average_mb": sum(history) / len(history) if history else 0,
            "peak_mb": max(history) if history else 0
        }

class SearchOptimizer:
    """Search optimization with caching."""
    
    def __init__(self, config: RealTimeConfig):
        self.config = config
        self.query_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.search_latencies = deque(maxlen=1000)
        
    def get_cache_key(self, query: str, limit: int, threshold: float) -> str:
        """Generate cache key."""
        return f"{hash(query)}_{limit}_{threshold:.3f}"
    
    def get_cached_result(self, query: str, limit: int, threshold: float) -> Optional[List[Dict]]:
        """Get cached search result."""
        key = self.get_cache_key(query, limit, threshold)
        if key in self.query_cache:
            self.cache_hits += 1
            return self.query_cache[key]
        
        self.cache_misses += 1
        return None
    
    def cache_result(self, query: str, limit: int, threshold: float, results: List[Dict]):
        """Cache search result."""
        if len(self.query_cache) >= self.config.max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.query_cache))
            del self.query_cache[oldest_key]
        
        key = self.get_cache_key(query, limit, threshold)
        self.query_cache[key] = results
    
    def record_latency(self, latency_ms: float):
        """Record search latency."""
        self.search_latencies.append(latency_ms)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance stats."""
        total = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total if total > 0 else 0
        
        latencies = list(self.search_latencies)
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        
        return {
            "hit_rate": hit_rate,
            "cache_size": len(self.query_cache),
            "total_queries": total,
            "avg_latency_ms": avg_latency,
            "recent_latencies": latencies[-10:] if latencies else []
        }

class RealTimeQdrantSystem:
    """Real-time Qdrant system with optimization."""
    
    def __init__(self, config: Optional[RealTimeConfig] = None):
        self.config = config or RealTimeConfig()
        self.embedder: Optional[SentenceTransformerEmbedder] = None
        self.store: Optional[QdrantStore] = None
        
        # Optimization components
        self.memory_optimizer = MemoryOptimizer(self.config)
        self.search_optimizer = SearchOptimizer(self.config)
        
        # Metrics and monitoring
        self.metrics = deque(maxlen=self.config.metrics_retention_count)
        self.operation_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        
        # Real-time update buffer
        self.update_buffer = []
        self.last_batch_time = time.time()
        
    async def initialize(self):
        """Initialize the real-time system."""
        logger.info("🚀 Initializing Real-Time Qdrant System...")
        
        # Initialize embedder
        embedder_config = EmbedderConfig(
            model_name="nomic-ai/CodeRankEmbed",
            device="cpu",
            batch_size=self.config.batch_size
        )
        self.embedder = SentenceTransformerEmbedder(embedder_config)
        
        # Initialize Qdrant store  
        store_config = QdrantStoreConfig(
            host="localhost",
            port=6333,
            collection_name="realtime_system_768",
            vector_size=768,
            enable_quantization=True,
            prefer_grpc=False
        )
        self.store = QdrantStore(store_config)
        
        logger.info("✅ Real-time system initialized!")
        
    async def optimized_search(self, 
                             query: str,
                             limit: int = 10,
                             score_threshold: float = 0.3,
                             use_cache: bool = True) -> Dict[str, Any]:
        """Perform optimized search with caching and monitoring."""
        start_time = time.time()
        self.operation_counts["search"] += 1
        
        try:
            # Check cache first
            if use_cache:
                cached = self.search_optimizer.get_cached_result(query, limit, score_threshold)
                if cached is not None:
                    latency_ms = (time.time() - start_time) * 1000
                    self.search_optimizer.record_latency(latency_ms)
                    
                    return {
                        "query": query,
                        "results": cached,
                        "latency_ms": latency_ms,
                        "from_cache": True,
                        "memory_mb": self.memory_optimizer.get_current_memory_mb()
                    }
            
            # Generate embeddings
            if not self.embedder:
                raise RuntimeError("Embedder not initialized")
            embeddings = await self.embedder.embed_documents([query])
            
            # Search with optimized parameters
            if not self.store:
                raise RuntimeError("Store not initialized")
            results = self.store.search(
                query_embedding=embeddings[0],
                limit=limit,
                score_threshold=score_threshold
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "score": result.get("score", 0),
                    "content": result.get("content", ""),
                    "source": result.get("source_file", "unknown")
                })
            
            # Cache results
            if use_cache:
                self.search_optimizer.cache_result(query, limit, score_threshold, formatted_results)
            
            # Record metrics
            latency_ms = (time.time() - start_time) * 1000
            self.search_optimizer.record_latency(latency_ms)
            
            metric = PerformanceMetrics(
                timestamp=time.time(),
                operation="search",
                latency_ms=latency_ms,
                memory_mb=self.memory_optimizer.get_current_memory_mb(),
                success=True,
                details={"results_count": len(formatted_results), "cached": False}
            )
            self.metrics.append(metric)
            
            return {
                "query": query,
                "results": formatted_results,
                "latency_ms": latency_ms,
                "from_cache": False,
                "memory_mb": self.memory_optimizer.get_current_memory_mb(),
                "results_count": len(formatted_results)
            }
            
        except Exception as e:
            self.error_counts["search"] += 1
            latency_ms = (time.time() - start_time) * 1000
            
            error_metric = PerformanceMetrics(
                timestamp=time.time(),
                operation="search_error",
                latency_ms=latency_ms,
                memory_mb=self.memory_optimizer.get_current_memory_mb(),
                success=False,
                details={"error": str(e)}
            )
            self.metrics.append(error_metric)
            
            logger.error(f"Search error: {e}")
            return {"error": str(e), "latency_ms": latency_ms}
    
    async def add_realtime_update(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add content for real-time updating."""
        update_item = {
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        
        self.update_buffer.append(update_item)
        
        # Process batch if conditions met
        current_time = time.time()
        should_process = (
            len(self.update_buffer) >= self.memory_optimizer.get_optimized_batch_size() or
            current_time - self.last_batch_time >= self.config.batch_interval_seconds
        )
        
        if should_process and self.update_buffer:
            await self._process_update_batch()
    
    async def _process_update_batch(self):
        """Process batch of updates."""
        if not self.update_buffer:
            return
        
        start_time = time.time()
        batch_size = len(self.update_buffer)
        
        try:
            # Extract content for embedding
            contents = [item["content"] for item in self.update_buffer]
            
            # Generate embeddings
            if not self.embedder:
                raise RuntimeError("Embedder not initialized")
            embeddings = await self.embedder.embed_documents(contents)
            
            # Simulate batch insert (implementation depends on your store)
            await asyncio.sleep(0.01 * batch_size)  # Simulate processing
            
            # Clear buffer
            self.update_buffer.clear()
            self.last_batch_time = time.time()
            
            # Record metrics
            latency_ms = (time.time() - start_time) * 1000
            self.operation_counts["batch_update"] += 1
            
            metric = PerformanceMetrics(
                timestamp=time.time(),
                operation="batch_update",
                latency_ms=latency_ms,
                memory_mb=self.memory_optimizer.get_current_memory_mb(),
                success=True,
                details={"batch_size": batch_size}
            )
            self.metrics.append(metric)
            
            logger.info(f"✅ Processed batch: {batch_size} items in {latency_ms:.1f}ms")
            
        except Exception as e:
            self.error_counts["batch_update"] += 1
            logger.error(f"Batch update error: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        memory_stats = self.memory_optimizer.get_memory_stats()
        cache_stats = self.search_optimizer.get_cache_stats()
        
        # Performance analysis
        recent_metrics = [m for m in self.metrics if time.time() - m.timestamp < 300]  # Last 5 minutes
        successful_ops = [m for m in recent_metrics if m.success]
        
        avg_latency = sum(m.latency_ms for m in successful_ops) / len(successful_ops) if successful_ops else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "memory_stats": memory_stats,
            "cache_stats": cache_stats,
            "performance": {
                "avg_latency_ms": avg_latency,
                "total_operations": dict(self.operation_counts),
                "total_errors": dict(self.error_counts),
                "recent_metrics_count": len(recent_metrics)
            },
            "buffer_status": {
                "pending_updates": len(self.update_buffer),
                "last_batch_time": self.last_batch_time
            }
        }
    
    async def demonstrate_realtime_capabilities(self):
        """Demonstrate real-time capabilities."""
        logger.info("🎯 Starting Real-Time Capabilities Demo")
        
        # Demo 1: Memory-optimized search
        logger.info("\n📊 Demo 1: Memory-Optimized Search")
        test_queries = [
            "vector search optimization",
            "real-time machine learning",
            "memory management strategies"
        ]
        
        for query in test_queries:
            result = await self.optimized_search(query)
            logger.info(f"Query: '{query}' → {result.get('latency_ms', 0):.1f}ms, "
                       f"Results: {result.get('results_count', 0)}, "
                       f"Memory: {result.get('memory_mb', 0):.1f}MB")
        
        # Demo 2: Cache performance
        logger.info("\n🎯 Demo 2: Cache Performance")
        cache_test_query = "vector search optimization"
        for i in range(3):
            result = await self.optimized_search(cache_test_query)
            logger.info(f"Attempt {i+1}: {result.get('latency_ms', 0):.1f}ms, "
                       f"Cached: {result.get('from_cache', False)}")
        
        # Demo 3: Real-time updates
        logger.info("\n🔄 Demo 3: Real-Time Updates")
        update_contents = [
            "Real-time vector indexing for production systems",
            "Memory optimization techniques for large-scale deployments", 
            "Latency reduction strategies in vector databases",
            "Horizontal scaling patterns for distributed search"
        ]
        
        for content in update_contents:
            await self.add_realtime_update(content, {"demo": True})
            logger.info(f"Added update: '{content[:50]}...'")
        
        # Force process remaining updates
        if self.update_buffer:
            await self._process_update_batch()
        
        # Demo 4: System monitoring
        logger.info("\n📈 Demo 4: System Status")
        status = await self.get_system_status()
        
        logger.info(f"Memory: {status['memory_stats']['current_mb']:.1f}MB "
                   f"(Pressure: {status['memory_stats']['under_pressure']})")
        logger.info(f"Cache: {status['cache_stats']['hit_rate']:.2%} hit rate, "
                   f"{status['cache_stats']['cache_size']} entries")
        logger.info(f"Performance: {status['performance']['avg_latency_ms']:.1f}ms avg latency")
        logger.info(f"Operations: {status['performance']['total_operations']}")

# Example usage generator
async def generate_realtime_data() -> AsyncGenerator[str, None]:
    """Generate sample real-time data."""
    topics = [
        "vector search performance optimization",
        "memory management for large collections",
        "real-time indexing strategies",
        "distributed search architectures",
        "quantization techniques comparison",
        "hybrid search implementation patterns"
    ]
    
    for i in range(50):
        topic = topics[i % len(topics)]
        content = f"Sample content {i}: Advanced techniques for {topic} in production environments."
        yield content
        await asyncio.sleep(0.2)  # Simulate real-time data flow

async def main():
    """Main demonstration."""
    print("🚀 QDRANT REAL-TIME SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Initialize system
    config = RealTimeConfig(
        memory_threshold_mb=512,  # 512MB for demo
        batch_size=20,
        max_cache_size=100,
        batch_interval_seconds=2.0
    )
    
    system = RealTimeQdrantSystem(config)
    
    try:
        await system.initialize()
        
        # Run comprehensive demo
        await system.demonstrate_realtime_capabilities()
        
        # Real-time data processing simulation
        print(f"\n🔄 Processing Real-Time Data Stream...")
        async for content in generate_realtime_data():
            await system.add_realtime_update(content, {"source": "stream"})
            
            # Periodic status updates
            if (int(time.time()) % 10) == 0:  # Every 10 seconds
                status = await system.get_system_status()
                print(f"📊 Status: {status['buffer_status']['pending_updates']} pending, "
                      f"{status['memory_stats']['current_mb']:.1f}MB memory")
        
        # Final status report
        final_status = await system.get_system_status()
        print(f"\n🎉 FINAL PERFORMANCE REPORT:")
        print(f"   Memory Usage: {final_status['memory_stats']['current_mb']:.1f}MB")
        print(f"   Cache Hit Rate: {final_status['cache_stats']['hit_rate']:.2%}")
        print(f"   Average Latency: {final_status['performance']['avg_latency_ms']:.1f}ms")
        print(f"   Total Operations: {final_status['performance']['total_operations']}")
        print(f"   Total Errors: {final_status['performance']['total_errors']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())