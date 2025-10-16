"""
Search qdrant_ecosystem collection for Qdrant best practices documentation
"""
import asyncio
import time
from qdrant_client import QdrantClient
from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder


async def main():
    # Initialize embedder (CPU-based)
    print("Initializing embedder (this may take 30+ seconds on CPU)...")
    embedder_config = EmbedderConfig(
        model_name='nomic-ai/CodeRankEmbed',
        device='cpu',
        batch_size=1
    )
    embedder = SentenceTransformerEmbedder(embedder_config)
    
    # Initialize Qdrant client
    client = QdrantClient(host='localhost', port=6333)
    
    # Query for vector dimension best practices
    query = "vector dimension recommendations best practices CPU performance inference optimization embedding size"
    print(f"\nGenerating embedding for query: '{query}'")
    print("(Note: This will be SLOW on CPU - demonstrating the exact problem we're trying to solve!)\n")
    
    start = time.time()
    query_vec = await embedder.embed_query(query)
    elapsed = time.time() - start
    
    print(f"✓ Embedding generated in {elapsed:.2f} seconds")
    print(f"  Vector dimension: {len(query_vec)}")
    print(f"\nSearching qdrant_ecosystem collection...")
    
    # Search
    results = client.search(
        collection_name='qdrant_ecosystem',
        query_vector=query_vec,
        limit=5,
        score_threshold=0.5
    )
    
    print(f"\n{'='*80}")
    print(f"Top {len(results)} results for dimension/performance best practices:")
    print(f"{'='*80}\n")
    
    for i, r in enumerate(results):
        print(f"{i+1}. Score: {r.score:.3f}")
        print(f"   ID: {r.id}")
        if r.payload:
            content = r.payload.get('content', 'N/A')
            print(f"   Content preview: {content[:300]}...")
            print(f"   Metadata: {r.payload.get('metadata', {})}")
        print()
    
    # Also search for quantization and optimization
    print(f"\n{'='*80}")
    print(f"Searching for 'quantization optimization performance'...")
    print(f"{'='*80}\n")
    
    query2 = "quantization optimization performance CPU memory efficiency"
    print(f"Generating embedding for query 2 (again, this will be slow)...")
    start2 = time.time()
    query_vec2 = await embedder.embed_query(query2)
    elapsed2 = time.time() - start2
    print(f"✓ Embedding generated in {elapsed2:.2f} seconds\n")
    
    results2 = client.search(
        collection_name='qdrant_ecosystem',
        query_vector=query_vec2,
        limit=5,
        score_threshold=0.5
    )
    
    for i, r in enumerate(results2):
        print(f"{i+1}. Score: {r.score:.3f}")
        print(f"   ID: {r.id}")
        if r.payload:
            content = r.payload.get('content', 'N/A')
            print(f"   Content preview: {content[:300]}...")
        print()
    
    print(f"\n{'='*80}")
    print(f"TOTAL EMBEDDING TIME: {elapsed + elapsed2:.2f} seconds for 2 queries")
    print(f"This demonstrates why CPU-based CodeRankEmbed is problematic for MCP server!")
    print(f"{'='*80}")


if __name__ == "__main__":
    asyncio.run(main())
