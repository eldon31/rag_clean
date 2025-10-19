#!/usr/bin/env python3
"""Test Qdrant search directly to debug MCP server issues."""

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

# Initialize
client = QdrantClient(host="localhost", port=6333)
embedder = SentenceTransformer('nomic-ai/CodeRankEmbed', trust_remote_code=True)

# Test query
query = "vector database"
query_vector = embedder.encode([query])[0].tolist()

print(f"Query: {query}")
print(f"Vector dimension: {len(query_vector)}")
print()

# Test simple search
collection_name = "ultimate_embeddings_v4_nomic-coderank_qdrant"

try:
    print(f"Testing query_points on {collection_name}...")
    points = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=5,
        score_threshold=0.3
    ).points
    
    print(f"Found {len(points)} results")
    for i, point in enumerate(points, 1):
        print(f"\nResult {i}:")
        print(f"  Score: {point.score}")
        print(f"  ID: {point.id}")
        if point.payload:
            print(f"  Keys: {list(point.payload.keys())}")
            text = point.payload.get('text', point.payload.get('content', ''))[:100]
            print(f"  Text preview: {text}...")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Try search() method instead
try:
    print(f"\n\nTesting search() method on {collection_name}...")
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5,
        score_threshold=0.3
    )
    
    print(f"Found {len(results)} results")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Score: {result.score}")
        print(f"  ID: {result.id}")
        if result.payload:
            print(f"  Keys: {list(result.payload.keys())}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
