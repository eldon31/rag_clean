"""Quick script to check all collections in Qdrant."""
from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")

print("\n=== ALL COLLECTIONS IN QDRANT ===\n")

collections = client.get_collections().collections

for coll in collections:
    info = client.get_collection(coll.name)
    
    # Get vector size
    vectors = info.config.params.vectors
    if isinstance(vectors, dict):
        # Multiple named vectors
        vector_info = {name: v.size for name, v in vectors.items()}
    else:
        # Single vector config
        vector_info = vectors.size
    
    print(f"📦 {coll.name}")
    print(f"   Points: {info.points_count:,}")
    print(f"   Vectors: {vector_info}")
    print()

print("\n=== CHECKING FOR OLD 3584-DIM COLLECTIONS ===\n")

for coll in collections:
    info = client.get_collection(coll.name)
    vectors = info.config.params.vectors
    
    if isinstance(vectors, dict):
        for name, v in vectors.items():
            if v.size == 3584:
                print(f"⚠️  FOUND OLD: {coll.name} ({name}): {v.size} dim")
    else:
        if vectors.size == 3584:
            print(f"⚠️  FOUND OLD: {coll.name}: {vectors.size} dim")

print("\n=== CHECKING NEW 768-DIM COLLECTIONS ===\n")

target_collections = ['qdrant_ecosystem', 'docling', 'sentence_transformers']

for name in target_collections:
    try:
        info = client.get_collection(name)
        vectors = info.config.params.vectors
        
        if isinstance(vectors, dict):
            print(f"❌ {name}: Has multiple vectors (unexpected)")
        else:
            dim = vectors.size
            if dim == 768:
                print(f"✅ {name}: {info.points_count:,} points, {dim} dim (CodeRankEmbed)")
            else:
                print(f"❌ {name}: {info.points_count:,} points, {dim} dim (WRONG!)")
    except Exception as e:
        print(f"❌ {name}: Not found - {e}")
