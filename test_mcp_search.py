"""Test search functionality in the MCP server."""
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/app')

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

async def test_search():
    print("Initializing embedder...")
    embedder = SentenceTransformerEmbedder(
        EmbedderConfig(model_name='nomic-ai/nomic-embed-code')
    )
    
    print("Generating query embedding...")
    query = "API documentation"
    vec = await embedder.embed_documents([query])
    print(f"Vector shape: {len(vec[0])}")
    
    # Test all collections
    collections = ["viator_api", "fast_docs", "pydantic_docs", "inngest_ecosystem"]
    
    for collection in collections:
        print(f"\n--- Testing {collection} ---")
        try:
            store = QdrantStore(
                QdrantStoreConfig(
                    host='host.docker.internal',
                    port=6333,
                    collection_name=collection,
                    vector_size=3584,
                    prefer_grpc=False
                )
            )
            
            print(f"Searching {collection} for: {query}")
            results = store.search(
                query_embedding=vec[0],
                limit=2,
                score_threshold=0.3
            )
            
            print(f"Results found: {len(results)}")
            if results:
                for idx, result in enumerate(results, 1):
                    print(f"  Result {idx}: Score {result.get('score', 0):.3f}")
                    content = result.get('content', '')
                    print(f"    Content: {content[:100]}...")
        except Exception as e:
            print(f"Error testing {collection}: {e}")

if __name__ == "__main__":
    asyncio.run(test_search())
