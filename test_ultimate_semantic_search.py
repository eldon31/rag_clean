#!/usr/bin/env python3
"""
Test our Ultimate Qdrant knowledge with proper field mapping
"""
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

def test_ultimate_semantic_search():
    print("🧠 ULTIMATE SEMANTIC SEARCH TEST")
    print("=" * 50)
    
    # Connect and initialize
    client = QdrantClient(host='localhost', port=6333)
    embedder = SentenceTransformer('nomic-ai/CodeRankEmbed', trust_remote_code=True)
    
    # Test queries for our knowledge domains
    test_queries = [
        "How to optimize vector search performance in Qdrant?",
        "How to extract text from PDF documents using docling?", 
        "How to train better sentence transformer models?"
    ]
    
    collections = ['qdrant_ecosystem_768', 'docling_768', 'sentence_transformers_768']
    
    for query in test_queries:
        print(f"\n🎯 QUERY: {query}")
        print("-" * 60)
        
        query_vector = embedder.encode([query])[0].tolist()
        
        # Auto-classify which collection to search
        query_lower = query.lower()
        if any(kw in query_lower for kw in ['qdrant', 'vector database', 'search', 'optimization']):
            target_collections = ['qdrant_ecosystem_768']
        elif any(kw in query_lower for kw in ['pdf', 'document', 'docling', 'extract']):
            target_collections = ['docling_768']
        elif any(kw in query_lower for kw in ['transformer', 'embedding', 'model', 'train']):
            target_collections = ['sentence_transformers_768']
        else:
            target_collections = collections[:1]  # Default to largest
        
        print(f"📊 Searching: {', '.join(target_collections)}")
        
        for collection_name in target_collections:
            try:
                results = client.query_points(
                    collection_name=collection_name,
                    query=query_vector,
                    limit=2,
                    score_threshold=0.5
                )
                
                print(f"\n✅ {collection_name}: {len(results.points)} results")
                
                for i, point in enumerate(results.points, 1):
                    payload = point.payload or {}
                    content = payload.get('text', '')[:200] + '...'
                    source = payload.get('source_file', 'Unknown')
                    filename = payload.get('filename', 'Unknown')
                    
                    print(f"  {i}. Score: {point.score:.3f}")
                    print(f"     File: {filename}")
                    print(f"     Source: {source}")
                    print(f"     Content: {content}")
                    print()
                    
            except Exception as e:
                print(f"❌ Error in {collection_name}: {e}")
        
        print("=" * 60)
    
    print(f"\n🎯 ULTIMATE KNOWLEDGE BASE SUMMARY:")
    total_vectors = 0
    for collection in collections:
        info = client.get_collection(collection)
        total_vectors += info.points_count
        print(f"- {collection}: {info.points_count:,} vectors")
    
    print(f"\n📊 Total: {total_vectors:,} vectors ready for semantic search!")
    print("🚀 Ultimate knowledge system operational!")

if __name__ == "__main__":
    test_ultimate_semantic_search()