from qdrant_client import QdrantClient

client = QdrantClient(host='localhost', port=6333)

print("🔍 PAYLOAD INSPECTION")
print("=" * 40)

# Inspect payload structure for each collection
for collection_name in ['qdrant_ecosystem_768', 'docling_768', 'sentence_transformers_768']:
    print(f"\n📊 {collection_name}:")
    
    try:
        # Get a few sample points
        points, _ = client.scroll(collection_name=collection_name, limit=3)
        
        for i, point in enumerate(points, 1):
            print(f"  Point {i}:")
            print(f"    ID: {point.id}")
            
            if point.payload:
                print(f"    Payload keys: {list(point.payload.keys())}")
                # Show first few characters of each payload field
                for key, value in point.payload.items():
                    if isinstance(value, str):
                        preview = value[:100] + "..." if len(value) > 100 else value
                        print(f"      {key}: {preview}")
                    else:
                        print(f"      {key}: {value}")
            else:
                print("    ❌ NO PAYLOAD")
            print()
    except Exception as e:
        print(f"    ❌ Error: {e}")

print("🎯 Payload inspection complete!")