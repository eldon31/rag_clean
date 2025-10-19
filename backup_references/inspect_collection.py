#!/usr/bin/env python3
"""Inspect what's actually in a Qdrant collection."""

from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

collection_name = "ultimate_embeddings_v4_nomic-coderank_qdrant"

# Get a few random points
print(f"Inspecting collection: {collection_name}\n")

# Scroll through first few points
results = client.scroll(
    collection_name=collection_name,
    limit=3,
    with_payload=True,
    with_vectors=False
)

points = results[0]

print(f"Found {len(points)} sample points\n")

for i, point in enumerate(points, 1):
    print(f"Point {i}:")
    print(f"  ID: {point.id}")
    print(f"  Payload keys: {list(point.payload.keys()) if point.payload else 'None'}")
    if point.payload:
        for key, value in point.payload.items():
            if isinstance(value, str):
                display_value = value[:100] + "..." if len(value) > 100 else value
            else:
                display_value = value
            print(f"    {key}: {display_value}")
    print()
