"""
Vector Search Example for Docling Collection
Shows how to search the docling documentation embeddings
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "docling"
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"

def search_docling(query: str, top_k: int = 5):
    """
    Search the Docling documentation collection
    
    Args:
        query: Natural language question or search query
        top_k: Number of results to return (default: 5)
    
    Returns:
        List of search results with text and metadata
    """
    
    print(f"\n{'='*70}")
    print(f"SEARCHING DOCLING DOCS")
    print(f"{'='*70}")
    print(f"Query: {query}")
    print(f"Top K: {top_k}")
    print(f"{'='*70}\n")
    
    # Step 1: Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL)
    print(f"✓ Connected to Qdrant at {QDRANT_URL}")
    
    # Step 2: Load embedding model
    print(f"✓ Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
    
    # Step 3: Generate query embedding
    print(f"✓ Generating query embedding...")
    query_vector = model.encode(query).tolist()
    print(f"✓ Query vector dimension: {len(query_vector)}")
    
    # Step 4: Search Qdrant
    print(f"\n🔍 Searching collection '{COLLECTION_NAME}'...")
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,  # Include metadata
        with_vectors=False  # Don't return vectors (save bandwidth)
    )
    
    # Step 5: Display results
    print(f"\n{'='*70}")
    print(f"SEARCH RESULTS ({len(results)} found)")
    print(f"{'='*70}\n")
    
    for idx, hit in enumerate(results, 1):
        score = hit.score
        text = hit.payload.get('text', 'N/A')
        source = hit.payload.get('source', 'N/A')
        heading = hit.payload.get('heading', 'N/A')
        chunk_index = hit.payload.get('chunk_index', 'N/A')
        
        print(f"Result #{idx} (Score: {score:.4f})")
        print(f"{'─'*70}")
        print(f"Source: {source}")
        print(f"Heading: {heading}")
        print(f"Chunk: {chunk_index}")
        print(f"\nContent:")
        print(f"{text[:500]}..." if len(text) > 500 else text)
        print(f"\n{'='*70}\n")
    
    return results


def main():
    """Run example searches"""
    
    # Example 1: How to use Docling
    print("\n" + "="*70)
    print("EXAMPLE 1: Getting Started")
    print("="*70)
    search_docling("How do I install and use Docling?", top_k=3)
    
    # Example 2: PDF Processing
    print("\n" + "="*70)
    print("EXAMPLE 2: PDF Processing")
    print("="*70)
    search_docling("How does Docling process PDF documents?", top_k=3)
    
    # Example 3: Models
    print("\n" + "="*70)
    print("EXAMPLE 3: AI Models")
    print("="*70)
    search_docling("What AI models does Docling use?", top_k=3)
    
    # Example 4: Custom search
    print("\n" + "="*70)
    print("CUSTOM SEARCH")
    print("="*70)
    custom_query = input("\nEnter your search query: ").strip()
    if custom_query:
        search_docling(custom_query, top_k=5)


if __name__ == "__main__":
    # Quick test search
    search_docling("How to convert PDF to markdown with Docling?", top_k=3)
    
    # Uncomment to run interactive examples
    # main()
