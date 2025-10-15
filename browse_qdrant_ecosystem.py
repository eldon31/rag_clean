"""
Browse qdrant_ecosystem collection for Qdrant documentation
"""
from qdrant_client import QdrantClient

client = QdrantClient(host='localhost', port=6333)

print("Retrieving sample documents from qdrant_ecosystem...")
results, next_offset = client.scroll(
    collection_name='qdrant_ecosystem',
    limit=20,
    with_payload=True,
    with_vectors=False
)

print(f"\nRetrieved {len(results)} points from qdrant_ecosystem collection\n")
print(f"{'='*80}")

for i, p in enumerate(results[:10]):
    print(f"\n{i+1}. ID: {p.id}")
    if p.payload:
        content = p.payload.get('content', 'N/A')
        metadata = p.payload.get('metadata', {})
        print(f"   Metadata: {metadata}")
        print(f"   Content ({len(content)} chars):")
        print(f"   {content[:600]}...")
    print(f"\n{'='*80}")

# Search for documents mentioning "dimension" or "quantization"
print("\n\nSearching metadata for 'quantization' or 'dimension' keywords...")
keywords_found = []
for p in results:
    if p.payload:
        content = p.payload.get('content', '').lower()
        if 'dimension' in content or 'quantization' in content or 'cpu' in content or 'performance' in content:
            keywords_found.append(p)
            
print(f"\nFound {len(keywords_found)} documents with relevant keywords:\n")
for i, p in enumerate(keywords_found[:5]):
    print(f"\n{i+1}. ID: {p.id}")
    if p.payload:
        content = p.payload.get('content', '')
        metadata = p.payload.get('metadata', {})
        print(f"   Metadata: {metadata}")
        print(f"   Content preview: {content[:500]}...")
    print(f"\n{'-'*80}")
