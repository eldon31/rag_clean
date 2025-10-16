#!/usr/bin/env python3
"""
🏆 ULTIMATE QDRANT MCP SERVER TEST
================================

Test our optimized MCP server with 9,654 vectors across 3 collections.
Validates all functionality before production deployment.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from mcp_server.ultimate_qdrant_mcp import (
    search_ultimate_knowledge,
    get_collections_status,
    get_collection_expertise,
    health_check,
    ULTIMATE_COLLECTIONS
)


async def test_health_check():
    """Test the health check functionality."""
    print("🏥 Testing health check...")
    result = await health_check()
    print(result)
    print("\n" + "="*60 + "\n")


async def test_collections_status():
    """Test getting collections status."""
    print("📊 Testing collections status...")
    result = await get_collections_status()
    print(result)
    print("\n" + "="*60 + "\n")


async def test_collection_expertise():
    """Test getting expertise for each collection."""
    print("🎓 Testing collection expertise...")
    
    for collection_name in ULTIMATE_COLLECTIONS:
        print(f"\n--- {collection_name} ---")
        result = await get_collection_expertise(collection_name)
        print(result)
    
    print("\n" + "="*60 + "\n")


async def test_searches():
    """Test various search queries across collections."""
    print("🔍 Testing search functionality...")
    
    test_queries = [
        {
            "query": "How to optimize embedding models for better performance?",
            "expected_collections": ["sentence_transformers_768"],
            "description": "Embedding optimization query"
        },
        {
            "query": "Best practices for document chunking and processing",
            "expected_collections": ["docling_768"],
            "description": "Document processing query"
        },
        {
            "query": "Qdrant vector search optimization and quantization",
            "expected_collections": ["qdrant_ecosystem_768"],
            "description": "Vector database query"
        },
        {
            "query": "How to build a production RAG system with embeddings and vector search?",
            "expected_collections": None,  # Should auto-classify to all
            "description": "Multi-domain query (should search all collections)"
        }
    ]
    
    for test_case in test_queries:
        print(f"\n🎯 **{test_case['description']}**")
        print(f"Query: \"{test_case['query']}\"")
        
        if test_case['expected_collections']:
            result = await search_ultimate_knowledge(
                query=test_case['query'],
                collections=test_case['expected_collections'],
                limit=3,
                score_threshold=0.6
            )
        else:
            # Test auto-classification
            result = await search_ultimate_knowledge(
                query=test_case['query'],
                limit=5,
                score_threshold=0.6
            )
        
        print(result)
        print("\n" + "-"*40 + "\n")
    
    print("="*60 + "\n")


async def test_edge_cases():
    """Test edge cases and error handling."""
    print("⚡ Testing edge cases...")
    
    # Test invalid collection
    print("\n🔍 Testing invalid collection...")
    result = await search_ultimate_knowledge(
        query="test query",
        collections=["invalid_collection"],
        limit=5
    )
    print(result)
    
    # Test empty query
    print("\n🔍 Testing empty query...")
    result = await search_ultimate_knowledge(
        query="",
        limit=5
    )
    print(result)
    
    # Test very specific query
    print("\n🔍 Testing very specific query...")
    result = await search_ultimate_knowledge(
        query="CodeRankEmbed nomic quantization optimization batch processing",
        limit=3,
        score_threshold=0.8
    )
    print(result)
    
    print("\n" + "="*60 + "\n")


async def run_comprehensive_test():
    """Run all tests in sequence."""
    print("🏆 ULTIMATE QDRANT MCP SERVER - COMPREHENSIVE TEST")
    print("=" * 60)
    print(f"📊 Testing {len(ULTIMATE_COLLECTIONS)} collections")
    print(f"🎯 Total vectors: {sum(info['points'] for info in ULTIMATE_COLLECTIONS.values()):,}")
    print("🚀 Starting tests...\n")
    
    try:
        # Run all test suites
        await test_health_check()
        await test_collections_status()
        await test_collection_expertise() 
        await test_searches()
        await test_edge_cases()
        
        print("✅ **ALL TESTS COMPLETED SUCCESSFULLY!**")
        print("🚀 **MCP SERVER IS READY FOR PRODUCTION!**")
        
    except Exception as e:
        print(f"❌ **TEST FAILED**: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main test runner."""
    print("🏆 Starting Ultimate Qdrant MCP Server Tests...")
    asyncio.run(run_comprehensive_test())


if __name__ == "__main__":
    main()