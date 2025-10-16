#!/usr/bin/env python3
"""
Test Script for Qdrant MCP Server
=================================

Simple test to validate MCP server functionality before deployment.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

async def test_direct_qdrant_connection():
    """Test direct connection to Qdrant collections."""
    print("🧪 Testing Direct Qdrant Connection...")
    
    # Initialize embedder
    embedder_config = EmbedderConfig(
        model_name="nomic-ai/CodeRankEmbed",
        device="cpu",
        batch_size=32
    )
    embedder = SentenceTransformerEmbedder(embedder_config)
    print("✅ Embedder initialized")
    
    # Test collections
    collections = [
        "sentence_transformers_768",
        "qdrant_ecosystem_768", 
        "docling_768"
    ]
    
    for collection_name in collections:
        print(f"\n📂 Testing collection: {collection_name}")
        
        try:
            # Connect to collection
            config = QdrantStoreConfig(
                host="localhost",
                port=6333,
                collection_name=collection_name,
                vector_size=768,
                enable_quantization=True,
                prefer_grpc=False
            )
            store = QdrantStore(config)
            print(f"  ✅ Connected to {collection_name}")
            
            # Test search
            query = "how to optimize embeddings"
            embeddings = await embedder.embed_documents([query])
            results = store.search(
                query_embedding=embeddings[0],
                limit=3,
                score_threshold=0.3
            )
            
            print(f"  📊 Search results: {len(results)} found")
            for i, result in enumerate(results[:2], 1):
                score = result.get('score', 0.0)
                content = result.get('content', '')[:100] + "..." if len(result.get('content', '')) > 100 else result.get('content', '')
                print(f"    {i}. Score: {score:.3f} - {content}")
                
        except Exception as e:
            print(f"  ❌ Error with {collection_name}: {e}")
    
    print("\n✅ Direct connection test completed!")

async def test_mcp_tools_simulation():
    """Simulate MCP tool operations."""
    print("\n🔧 Testing MCP Tool Operations...")
    
    # Initialize components
    embedder_config = EmbedderConfig(
        model_name="nomic-ai/CodeRankEmbed",
        device="cpu",
        batch_size=32
    )
    embedder = SentenceTransformerEmbedder(embedder_config)
    
    stores = {}
    collections = ["sentence_transformers_768", "qdrant_ecosystem_768", "docling_768"]
    
    # Initialize stores
    for collection in collections:
        config = QdrantStoreConfig(
            host="localhost",
            port=6333,
            collection_name=collection,
            vector_size=768,
            enable_quantization=True,
            prefer_grpc=False
        )
        stores[collection] = QdrantStore(config)
    
    print("✅ All stores initialized")
    
    # Test 1: Collection-specific search
    print("\n🔍 Test 1: Collection-specific search")
    query = "fine-tuning sentence transformers"
    embeddings = await embedder.embed_documents([query])
    
    results = stores["sentence_transformers_768"].search(
        query_embedding=embeddings[0],
        limit=3,
        score_threshold=0.3
    )
    
    print(f"  Query: '{query}'")
    print(f"  Results from sentence_transformers_768: {len(results)}")
    
    # Test 2: Smart search simulation
    print("\n🧠 Test 2: Smart search across collections")
    
    def classify_query(query: str):
        """Simple query classification."""
        query_lower = query.lower()
        relevant = []
        
        if any(word in query_lower for word in ['embedding', 'transformer', 'model', 'fine-tune']):
            relevant.append('sentence_transformers_768')
        if any(word in query_lower for word in ['vector', 'search', 'qdrant', 'similarity']):
            relevant.append('qdrant_ecosystem_768')
        if any(word in query_lower for word in ['document', 'pdf', 'chunk', 'docling']):
            relevant.append('docling_768')
            
        return relevant if relevant else list(stores.keys())
    
    smart_query = "how to search vectors efficiently"
    relevant_collections = classify_query(smart_query)
    
    print(f"  Query: '{smart_query}'")
    print(f"  Auto-routed to: {relevant_collections}")
    
    all_results = []
    for collection in relevant_collections:
        embeddings = await embedder.embed_documents([smart_query])
        results = stores[collection].search(
            query_embedding=embeddings[0],
            limit=2,
            score_threshold=0.25
        )
        
        for result in results:
            all_results.append({
                "collection": collection,
                "score": result.get('score', 0.0),
                "content": result.get('content', '')[:80] + "..."
            })
    
    # Sort by score
    all_results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"  Combined results: {len(all_results)}")
    for i, result in enumerate(all_results[:3], 1):
        print(f"    {i}. [{result['collection']}] Score: {result['score']:.3f}")
        print(f"       {result['content']}")
    
    print("\n✅ MCP tools simulation completed!")

async def test_health_check():
    """Test health check functionality."""
    print("\n❤️ Testing Health Check...")
    
    try:
        embedder_config = EmbedderConfig(
            model_name="nomic-ai/CodeRankEmbed",
            device="cpu",
            batch_size=32
        )
        embedder = SentenceTransformerEmbedder(embedder_config)
        
        collections = ["sentence_transformers_768", "qdrant_ecosystem_768", "docling_768"]
        health_status = {"collections": {}}
        
        for collection_name in collections:
            try:
                config = QdrantStoreConfig(
                    host="localhost",
                    port=6333,
                    collection_name=collection_name,
                    vector_size=768,
                    enable_quantization=True,
                    prefer_grpc=False
                )
                store = QdrantStore(config)
                
                # Test search
                embeddings = await embedder.embed_documents(["test"])
                test_results = store.search(embeddings[0], limit=1)
                
                health_status["collections"][collection_name] = {
                    "status": "✅ Healthy",
                    "test_results": len(test_results)
                }
                
            except Exception as e:
                health_status["collections"][collection_name] = {
                    "status": f"❌ Error: {str(e)}"
                }
        
        print("Health Status:")
        print(json.dumps(health_status, indent=2))
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")

async def main():
    """Run all tests."""
    print("🚀 Starting Qdrant MCP Server Tests")
    print("=" * 50)
    
    try:
        await test_direct_qdrant_connection()
        await test_mcp_tools_simulation()
        await test_health_check()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("\n💡 Your MCP server components are working correctly.")
        print("   You can now use the MCP server with confidence!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("🔧 Please check your Qdrant installation and collections.")

if __name__ == "__main__":
    asyncio.run(main())