#!/usr/bin/env python3
"""
Qdrant Search Example - How to invoke Qdrant for semantic search
"""
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Initialize the embedding model (same as used for indexing)
model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)

def search_qdrant(query: str, collection_name: str, limit: int = 5):
    """
    Search Qdrant collection using semantic similarity
    """
    # Generate embedding for the query
    query_embedding = model.encode(query).tolist()

    # Connect to Qdrant
    client = QdrantClient("http://localhost:6333")

    # Perform search
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=limit
    )

    return results

def list_collections():
    """List all available collections"""
    client = QdrantClient("http://localhost:6333")
    collections = client.get_collections()
    return [col.name for col in collections.collections]

if __name__ == "__main__":
    # Example usage
    print("Available collections:", list_collections())

    # Search example
    query = "How do I create a FastAPI endpoint?"
    collection = "fast_mcp_api_python"

    results = search_qdrant(query, collection, limit=3)

    print(f"\nSearch results for: '{query}'")
    print("=" * 50)

    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result.score:.3f}")
        print(f"   Content: {result.payload.get('content', '')[:200]}...")
        print(f"   Source: {result.payload.get('source', 'Unknown')}")
        print()