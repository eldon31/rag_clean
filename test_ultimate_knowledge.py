#!/usr/bin/env python3
"""
Quick test of our Ultimate Qdrant knowledge base
"""
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

def test_ultimate_knowledge():
    print("🔍 TESTING ULTIMATE QDRANT KNOWLEDGE BASE")
    print("=" * 50)
    
    # Connect to Qdrant
    client = QdrantClient(host='localhost', port=6333)
    embedder = SentenceTransformer('nomic-ai/CodeRankEmbed', trust_remote_code=True)
    
    # Test queries for each collection
    test_queries = [
        ("qdrant_ecosystem_768", "How to optimize vector search performance?"),
        ("docling_768", "How to extract text from PDF documents?"),
        ("sentence_transformers_768", "How to improve embedding model training?")
    ]
    
    for collection_name, query in test_queries:
        print(f"\n📊 TESTING: {collection_name}")
        print(f"🎯 Query: {query}")
        
        try:
            # Generate embedding
            query_vector = embedder.encode([query])[0].tolist()
            
            # Search collection using newer API
            results = client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=3,
                score_threshold=0.3  # Lower threshold to get results
            )
            
            print(f"✅ Found {len(results.points)} results")
            
            for i, point in enumerate(results.points, 1):
                payload = point.payload or {}
                content = payload.get('content', '')[:150] + '...' if payload.get('content') else 'No content'
                source = payload.get('source', 'Unknown')
                print(f"  {i}. Score: {point.score:.3f}")
                print(f"     Source: {source}")
                print(f"     Content: {content}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎯 SUMMARY:")
    collections = client.get_collections()
    total_points = 0
    for collection in collections.collections:
        info = client.get_collection(collection.name)
        total_points += info.points_count
        print(f"- {collection.name}: {info.points_count:,} vectors")
    
    print(f"📊 Total vectors: {total_points:,}")
    print("🚀 Ultimate knowledge base ready!")

if __name__ == "__main__":
    test_ultimate_knowledge()